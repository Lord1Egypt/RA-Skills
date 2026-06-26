#!/usr/bin/env node
'use strict';

// Register Lobster Captain on Yellow Pages
// Creates a directory entry so agents can discover the lobster captain L1 game server

const { createOceanBus } = require('oceanbus');
const fs = require('fs');
const path = require('path');
const os = require('os');

const DATA_DIR = path.join(os.homedir(), '.oceanbus', 'lobster-yp');
const CRED_FILE = path.join(DATA_DIR, 'credentials.json');

async function main() {
  console.log('═══ Register Lobster Captain on Yellow Pages ═══\n');

  fs.mkdirSync(DATA_DIR, { recursive: true });

  let agentId, apiKey, openid;

  // Check if we already registered
  if (fs.existsSync(CRED_FILE)) {
    const saved = JSON.parse(fs.readFileSync(CRED_FILE, 'utf-8'));
    agentId = saved.agent_id;
    apiKey = saved.api_key;
    openid = saved.openid;
    console.log('Using existing agent: ' + openid.slice(0, 24) + '...\n');
  } else {
    const ob = await createOceanBus({ keyStore: { type: 'memory' } });
    try {
      const reg = await ob.createIdentity();
      openid = await ob.getAddress();
      agentId = reg.agent_id;
      apiKey = reg.api_key;
      fs.writeFileSync(CRED_FILE, JSON.stringify({ agent_id: agentId, api_key: apiKey, openid }, null, 2));
      console.log('New agent registered: ' + openid.slice(0, 24) + '...\n');
    } catch (e) {
      if (typeof e.isRateLimited === 'function' && e.isRateLimited()) {
        const wait = e.retryAfterSeconds
          ? `${Math.ceil(e.retryAfterSeconds / 3600)}h`
          : 'a while';
        console.error(`Rate limited. Wait ${wait} before retrying.`);
      } else {
        console.error('Registration failed: ' + e.message);
      }
      await ob.destroy();
      process.exit(1);
    }
    await ob.destroy();
  }

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: agentId, api_key: apiKey },
  });

  const key = await ob.createServiceKey();
  ob.l1.yellowPages.setIdentity(openid, key.signer, key.publicKey);

  // Register Yellow Pages entry
  console.log('Registering on Yellow Pages...');
  try {
    const result = await ob.l1.yellowPages.registerService(
      ['lobster-captain', 'game', 'trading', 'zero-player', 'p2p'],
      '龙虾船长 (Captain Lobster) — 零玩家大航海贸易游戏。L1 Game Server OpenID: oa9EliN5y6HhsovCV-Q8uy4CKsQb3oM29GACCZ-6Jpn9YpZn9WNiX9pTJ6DpmgE49nmA_kyIyFk09-hA | 安装: clawhub install captain-lobster'
    );
    console.log('✅ Lobster Captain registered on Yellow Pages');
    console.log('   code: ' + result.code);
    console.log('');
    console.log('Discovery test:');
  } catch (e) {
    if (e.message && (e.message.includes('OPENID_TAKEN') || e.message.includes('11000'))) {
      console.log('⚠️  Already registered (dup key). Updating instead...');
      try {
        await ob.l1.yellowPages.updateService(
          ['lobster-captain', 'game', 'trading', 'zero-player', 'p2p'],
          '龙虾船长 (Captain Lobster) — 零玩家大航海贸易游戏。L1 Game Server OpenID: oa9EliN5y6HhsovCV-Q8uy4CKsQb3oM29GACCZ-6Jpn9YpZn9WNiX9pTJ6DpmgE49nmA_kyIyFk09-hA | 安装: clawhub install captain-lobster'
        );
        console.log('✅ Updated existing entry');
      } catch (e2) {
        console.log('Update also failed: ' + e2.message);
      }
    } else {
      console.log('❌ Registration failed: ' + e.message);
    }
  }

  // Verify: discover our own entry
  console.log('\nVerifying — searching Yellow Pages...');
  try {
    const r = await ob.l1.yellowPages.discover(['lobster-captain'], 5);
    if (r.data && r.data.entries) {
      console.log('Found ' + r.data.entries.length + ' entries for "lobster-captain":');
      for (const e of r.data.entries) {
        console.log('  - ' + e.description.slice(0, 80) + '...');
        console.log('    OpenID: ' + e.openid.slice(0, 24) + '...');
      }
    }
  } catch (e) {
    console.log('Discovery test failed: ' + e.message);
  }

  await ob.destroy();
  console.log('\nDone.');
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
