#!/usr/bin/env node
// C1/C2 Usage Checker & Auto-Switcher
// 5h使用率 OR 7d使用率 のどちらかが80%超えたら切り替え
// tokens.jsonからAPIキーを読む（1Password不要）
import { readFileSync, writeFileSync, renameSync } from 'fs';

const AUTH_FILE = `${process.env.HOME}/.openclaw/agents/main/agent/auth-profiles.json`;
const TOKENS_FILE = `${process.env.HOME}/.openclaw/workspace/tools/usage-switch/tokens.json`;
const THRESHOLD   = 0.80;

function loadTokens() {
  try {
    return JSON.parse(readFileSync(TOKENS_FILE, 'utf-8'));
  } catch {
    return null;
  }
}

async function getUsage(token) {
  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'anthropic-version': '2023-06-01',
        'anthropic-beta': 'claude-code-20250219,oauth-2025-04-20',
        'content-type': 'application/json',
      },
      body: JSON.stringify({model:'claude-sonnet-4-20250514', max_tokens:1, messages:[{role:'user',content:'.'}]}),
    });
    if (!res.ok) return null;
    const h5  = parseFloat(res.headers.get('anthropic-ratelimit-unified-5h-utilization')  || '0');
    const h7d = parseFloat(res.headers.get('anthropic-ratelimit-unified-7d-utilization')  || '0');
    return { h5, h7d, over: h5 >= THRESHOLD || h7d >= THRESHOLD };
  } catch { return null; }
}

async function main() {
  const tokens = loadTokens();
  if (!tokens?.c1 || !tokens?.c2) {
    console.log(JSON.stringify({error:'tokens.json not found. Run setup-tokens.sh first.'}));
    process.exit(1);
  }

  const [c1, c2] = await Promise.all([getUsage(tokens.c1), getUsage(tokens.c2)]);

  const c1_5h  = Math.round((c1?.h5  || 0) * 100);
  const c1_7d  = Math.round((c1?.h7d || 0) * 100);
  const c2_5h  = Math.round((c2?.h5  || 0) * 100);
  const c2_7d  = Math.round((c2?.h7d || 0) * 100);
  const c1Over = c1?.over ?? false;
  const c2Over = c2?.over ?? false;

  const auth = JSON.parse(readFileSync(AUTH_FILE, 'utf-8'));
  const current = auth.profiles['anthropic:default'].token;
  const usingC1     = current === tokens.c1;
  const currentName = usingC1 ? 'C1' : 'C2';
  const altToken    = usingC1 ? tokens.c2 : tokens.c1;
  const altName     = usingC1 ? 'C2' : 'C1';
  const currentOver = usingC1 ? c1Over : c2Over;
  const altOver     = usingC1 ? c2Over : c1Over;

  // 現在使用中が80%超え かつ 代替が80%未満 → 切り替え
  const needSwitch = currentOver && !altOver;

  if (needSwitch) {
    auth.profiles['anthropic:default'].token = altToken;
    const tmpFile = AUTH_FILE + ".tmp";
    writeFileSync(tmpFile, JSON.stringify(auth, null, 2));
    renameSync(tmpFile, AUTH_FILE); // アトミック操作
  }

  console.log(JSON.stringify({
    c1: { '5h': c1_5h, '7d': c1_7d, over: c1Over },
    c2: { '5h': c2_5h, '7d': c2_7d, over: c2Over },
    current: currentName,
    needSwitch,
    switched: needSwitch ? `${currentName}→${altName}` : null,
    bothOver: currentOver && altOver
  }));
}

main().catch(e => { console.log(JSON.stringify({error:String(e)})); process.exit(1); });
