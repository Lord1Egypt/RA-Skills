const NovyxMemory = require('./index');

async function testLifecycle() {
  console.log('--- NovyxMemory v3.0 Test Suite ---');

  const memory = new NovyxMemory({
    apiKey: process.env.NOVYX_API_KEY,
  });

  const sessionId = `test-memory-${Date.now()}`;
  const nonce = Date.now();
  let passed = 0;
  let failed = 0;

  function check(name, condition) {
    if (condition) {
      console.log(`    PASS: ${name}`);
      passed++;
    } else {
      console.log(`    FAIL: ${name}`);
      failed++;
    }
  }

  // 1. !remember — explicit save
  console.log('\n[1] Testing !remember...');
  const rememberResult = await memory.handleRemember(`!remember Test fact ${nonce}: Postgres is the primary database`);
  console.log(`    ${rememberResult}`);
  check('!remember returns confirmation', rememberResult.includes('Saved:'));

  // 2. Recall the memory via recall()
  console.log('\n[2] Testing recall...');
  await new Promise(r => setTimeout(r, 2000));
  const recalled = await memory.recall(`Test fact ${nonce} Postgres is the primary database`, 1);
  check('recall finds saved memory', recalled.length > 0 && recalled[0].observation.includes(String(nonce)));
  if (recalled.length > 0) {
    console.log(`    Recalled: "${recalled[0].observation.slice(0, 60)}..."`);
  }

  // 3. !search — semantic search with scores
  console.log('\n[3] Testing !search...');
  const searchResult = await memory.handleSearch(`!search Postgres ${nonce}`);
  console.log(`    ${searchResult.split('\n').join('\n    ')}`);
  check('!search returns scored results', searchResult.includes('%'));

  // 4. !list — list memories
  console.log('\n[4] Testing !list...');
  const listResult = await memory.handleList('!list --limit 3');
  console.log(`    ${listResult.split('\n').join('\n    ')}`);
  check('!list returns memories', listResult.includes('Memories') || listResult.includes('No memories'));

  // 5. !undo — delete last write
  console.log('\n[5] Testing !undo...');
  console.log(`    Write log has ${memory._writeLog.length} entries.`);
  const undoResult = await memory.handleUndo('!undo');
  console.log(`    ${undoResult}`);
  check('!undo deletes 1 memory', undoResult.includes('Undid 1'));

  // 6. !audit — operation log with hashes
  console.log('\n[6] Testing !audit...');
  const auditResult = await memory.handleAudit('!audit 5');
  console.log(`    ${auditResult.split('\n').join('\n    ')}`);
  check('!audit returns operations', auditResult.includes('POST') || auditResult.includes('GET') || auditResult.includes('DELETE'));

  // 7. !audit-verify — chain integrity
  console.log('\n[7] Testing !audit-verify...');
  const verifyResult = await memory.handleAuditVerify('!audit-verify');
  console.log(`    ${verifyResult.split('\n').join('\n    ')}`);
  check('!audit-verify returns result', verifyResult.includes('Audit chain') || verifyResult.includes('unavailable'));

  // 8. !status — usage info
  console.log('\n[8] Testing !status...');
  const statusResult = await memory.handleStatus();
  console.log(`    ${statusResult.split('\n').join('\n    ')}`);
  check('!status shows tier', statusResult.includes('Tier:'));
  check('!status shows rollbacks', statusResult.includes('Rollbacks:'));

  // 9. !dashboard
  console.log('\n[9] Testing !dashboard...');
  const dashResult = await memory.handleDashboard('!dashboard');
  console.log(`    ${dashResult.split('\n').join('\n    ')}`);
  check('!dashboard returns data', dashResult.includes('Dashboard') || dashResult.includes('unavailable'));

  // 10. !context
  console.log('\n[10] Testing !context...');
  const contextResult = await memory.handleContext('!context');
  console.log(`    ${contextResult.split('\n').join('\n    ')}`);
  check('!context returns data', contextResult.includes('Context') || contextResult.includes('unavailable'));

  // 11. !stats
  console.log('\n[11] Testing !stats...');
  const statsResult = await memory.handleStats('!stats');
  console.log(`    ${statsResult.split('\n').join('\n    ')}`);
  check('!stats returns data', statsResult.includes('Memory') || statsResult.includes('Stats') || statsResult.includes('unavailable'));

  // 12. !health
  console.log('\n[12] Testing !health...');
  const healthResult = await memory.handleHealth('!health');
  console.log(`    ${healthResult.split('\n').join('\n    ')}`);
  check('!health returns data', healthResult.includes('Health') || healthResult.includes('unavailable'));

  // 13. !help — verify all command groups listed
  console.log('\n[13] Testing !help...');
  const helpResult = await memory.handleHelp();
  check('!help lists Memory section', helpResult.includes('Memory'));
  check('!help lists Drafts section', helpResult.includes('Drafts'));
  check('!help lists Knowledge Graph section', helpResult.includes('Knowledge Graph'));
  check('!help lists Spaces section', helpResult.includes('Spaces'));
  check('!help lists Replay section', helpResult.includes('Replay'));
  check('!help lists Audit section', helpResult.includes('Audit'));
  check('!help lists Cortex section', helpResult.includes('Cortex'));
  check('!help lists Eval section', helpResult.includes('Eval'));
  check('!help lists Tracing section', helpResult.includes('Tracing'));
  check('!help lists Control section', helpResult.includes('Control'));
  check('!help lists Overview section', helpResult.includes('Overview'));

  // 14. Smart filtering — short messages skip API calls
  console.log('\n[14] Testing smart filtering...');
  const start = Date.now();
  const shortResult = await memory.onMessage('ok', sessionId);
  const elapsed = Date.now() - start;
  check('Short message returns immediately', shortResult === 'ok');
  check('Short message is fast (no API call)', elapsed < 100);

  // 15. onMessage context injection
  console.log('\n[15] Testing onMessage context injection...');
  const nonce2 = Date.now();
  const contextObs = `Context injection test ${nonce2}: We deploy to Fly.io using Docker`;
  await memory.remember(contextObs, ['test', `session:${sessionId}`]);
  await new Promise(r => setTimeout(r, 2000));
  const contextInjectResult = await memory.onMessage(`Tell me about deploying to Fly ${nonce2}`, sessionId);
  console.log(`    Result: "${typeof contextInjectResult === 'string' ? contextInjectResult.slice(0, 120) : contextInjectResult}..."`);
  check('onMessage injects recalled context', typeof contextInjectResult === 'string' && contextInjectResult.includes('[Recalled Memory]'));

  // 16. _parseRelativeTime
  console.log('\n[16] Testing _parseRelativeTime...');
  check('Parses "1h"', memory._parseRelativeTime('1h') !== null);
  check('Parses "30m"', memory._parseRelativeTime('30m') !== null);
  check('Parses "2 days ago"', memory._parseRelativeTime('2 days ago') !== null);
  check('Parses "1 hour ago"', memory._parseRelativeTime('1 hour ago') !== null);
  check('Rejects garbage', memory._parseRelativeTime('garbage') === null);
  check('Parses ISO timestamp', memory._parseRelativeTime('2026-01-01T00:00:00Z') !== null);

  // 17. _parseArgs
  console.log('\n[17] Testing _parseArgs...');
  const args1 = memory._parseArgs('!remember hello world --tags foo,bar', '!remember');
  check('_parseArgs extracts positional', args1._positional.includes('hello'));
  check('_parseArgs extracts --tags', args1.tags === 'foo,bar');
  const args2 = memory._parseArgs('!list --tag explicit --limit 5', '!list');
  check('_parseArgs extracts --tag', args2.tag === 'explicit');
  check('_parseArgs extracts --limit', args2.limit === '5');

  // 18. Command count
  console.log('\n[18] Testing command count...');
  check(`Has 60+ commands (actual: ${memory.commands.length})`, memory.commands.length >= 60);

  // Cleanup remaining test memories
  while (memory._writeLog.length > 0) {
    await memory.handleUndo('!undo 10');
  }

  // Summary
  console.log(`\n--- Results: ${passed} passed, ${failed} failed ---`);
  if (failed > 0) process.exit(1);
}

if (require.main === module) {
  testLifecycle().catch(err => {
    console.error('Test suite failed:', err);
    process.exit(1);
  });
}
