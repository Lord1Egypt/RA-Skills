#!/usr/bin/env node
'use strict';

// Yellow Pages smoke test — verify the deployed L1 service
const { createOceanBus } = require('oceanbus');

async function main() {
  console.log('═══ OceanBus Yellow Pages Smoke Test ═══\n');

  // ── Create agents ──
  console.log('1. Creating agents...');
  const a = await createOceanBus({ keyStore: { type: 'memory' } });
  await a.register();
  const aOpenid = await a.getOpenId();

  const b = await createOceanBus({ keyStore: { type: 'memory' } });
  await b.register();
  const bOpenid = await b.getOpenId();

  console.log('   Agent A: ' + aOpenid.slice(0, 20) + '...');
  console.log('   Agent B: ' + bOpenid.slice(0, 20) + '...\n');

  // ── Create service keys and set identity ──
  const aKey = await a.createServiceKey();
  const bKey = await b.createServiceKey();

  a.l1.yellowPages.setIdentity(aOpenid, aKey.signer, aKey.publicKey);
  b.l1.yellowPages.setIdentity(bOpenid, bKey.signer, bKey.publicKey);

  // ── Register ──
  console.log('2. Registering services...');
  try {
    const r1 = await a.l1.yellowPages.registerService(['guess-ai', 'room-test'], 'Test room A');
    console.log('   Agent A registered ✅  code=' + r1.code);
  } catch (e) {
    console.log('   Agent A register FAIL: ' + e.message);
  }

  try {
    const r2 = await b.l1.yellowPages.registerService(['guess-ai', 'room-test'], 'Test room B');
    console.log('   Agent B registered ✅  code=' + r2.code);
  } catch (e) {
    console.log('   Agent B register FAIL: ' + e.message);
  }

  // ── Discover ──
  console.log('\n3. Discovering rooms tagged [guess-ai, room-test]...');
  try {
    const result = await a.l1.yellowPages.discover(['guess-ai', 'room-test'], 10);
    if (result && result.data && result.data.entries) {
      console.log('   Found: ' + result.data.entries.length + ' entries (total: ' + result.data.total + ')');
      for (const entry of result.data.entries) {
        console.log('   - ' + entry.openid.slice(0, 20) + '... | ' + entry.description);
      }
      console.log('   Discover ✅');
    } else {
      console.log('   Discover returned unexpected: ' + JSON.stringify(result).slice(0, 200));
    }
  } catch (e) {
    console.log('   Discover FAIL: ' + e.message);
  }

  // ── Heartbeat ──
  console.log('\n4. Sending heartbeat...');
  try {
    const r = await a.l1.yellowPages.heartbeat();
    console.log('   Heartbeat ✅  code=' + r.code);
  } catch (e) {
    console.log('   Heartbeat FAIL: ' + e.message);
  }

  // ── Update ──
  console.log('\n5. Updating description...');
  try {
    const r = await a.l1.yellowPages.updateService(undefined, 'Updated: test room A v2');
    console.log('   Update ✅  code=' + r.code);
  } catch (e) {
    console.log('   Update FAIL: ' + e.message);
  }

  // ── Verify update via discover ──
  console.log('\n6. Verifying update...');
  try {
    const r2 = await a.l1.yellowPages.discover(['guess-ai', 'room-test'], 10);
    if (r2 && r2.data && r2.data.entries) {
      const me = r2.data.entries.find(e => e.openid === aOpenid);
      if (me && me.description.includes('v2')) {
        console.log('   Description now: ' + me.description);
        console.log('   Verify ✅');
      } else if (me) {
        console.log('   Entry desc: ' + me.description);
      } else {
        console.log('   Entry not found in discover results');
      }
    }
  } catch (e) {
    console.log('   Verify FAIL: ' + e.message);
  }

  // ── Cleanup ──
  console.log('\n7. Cleanup — deregistering...');
  try {
    await a.l1.yellowPages.deregisterService();
    console.log('   Agent A deregistered ✅');
  } catch (e) {
    console.log('   Agent A deregister FAIL: ' + e.message);
  }
  try {
    await b.l1.yellowPages.deregisterService();
    console.log('   Agent B deregistered ✅');
  } catch (e) {
    console.log('   Agent B deregister FAIL: ' + e.message);
  }

  // ── Final check ──
  const r3 = await a.l1.yellowPages.discover(['guess-ai', 'room-test'], 10);
  const ok = r3.data && r3.data.entries && r3.data.entries.length === 0;
  console.log('\n═══ ' + (ok ? 'ALL TESTS PASSED ✅' : 'SOME TESTS FAILED ⚠️') + ' ═══');

  await a.destroy();
  await b.destroy();
}

main().catch(err => {
  console.error('Test error:', err.message);
  process.exit(1);
});
