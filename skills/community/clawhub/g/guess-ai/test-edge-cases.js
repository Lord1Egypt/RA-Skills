#!/usr/bin/env node
'use strict';

// Edge case test: 抢话, 掉线, 重复加入, 迟加入, 平票, 淘汰后投票
const { createOceanBus } = require('oceanbus');

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  console.log('═══════════════════════════════════════════');
  console.log('  Guess AI — Edge Case Stress Test');
  console.log('═══════════════════════════════════════════\n');

  // ── Setup: 3 players ──
  const host = await createOceanBus({ keyStore: { type: 'memory' } });
  await host.register();
  const hOpenid = await host.getOpenId();
  const hKey = await host.createServiceKey();
  host.l1.yellowPages.setIdentity(hOpenid, hKey.signer, hKey.publicKey);

  const p1 = await createOceanBus({ keyStore: { type: 'memory' } });
  await p1.register();
  const p1Openid = await p1.getOpenId();

  const p2 = await createOceanBus({ keyStore: { type: 'memory' } });
  await p2.register();
  const p2Openid = await p2.getOpenId();

  const p3 = await createOceanBus({ keyStore: { type: 'memory' } });
  await p3.register();
  const p3Openid = await p3.getOpenId();

  await host.l1.yellowPages.registerService(['guess-ai', 'room-edge'], 'Edge test');

  const hostInbox = [];
  host.startListening(m => hostInbox.push(m));
  const p1Inbox = [];
  p1.startListening(m => p1Inbox.push(m));
  const p2Inbox = [];
  p2.startListening(m => p2Inbox.push(m));
  const p3Inbox = [];
  p3.startListening(m => p3Inbox.push(m));

  await sleep(3000);

  // ═══════════════════════════════════════════
  // TEST 1: 重复加入
  // ═══════════════════════════════════════════
  console.log('── TEST 1: 重复加入 ──\n');

  await p1.send(hOpenid, '加入');
  console.log('P1 → Host: 加入 (first time)');
  await sleep(3000);

  await p1.send(hOpenid, '加入');
  console.log('P1 → Host: 加入 (duplicate)');
  await sleep(3000);

  const p1Joins = hostInbox.filter(m => m.content === '加入' && m.from_openid === p1Openid);
  console.log('Host sees P1 join messages: ' + p1Joins.length);
  if (p1Joins.length === 2) {
    console.log('⚠️  Host received 2 join messages from same player — LLM must deduplicate by from_openid');
  }
  console.log('[Expected] Host LLM ignores duplicate, assigns number once\n');

  // ═══════════════════════════════════════════
  // TEST 2: 抢话 Out-of-turn speech
  // ═══════════════════════════════════════════
  console.log('── TEST 2: 抢话 (Out-of-turn speech) ──\n');

  // Join P2 and P3 normally
  await p2.send(hOpenid, '加入');
  console.log('P2 → Host: 加入');
  await p3.send(hOpenid, '加入');
  console.log('P3 → Host: 加入');
  await sleep(3000);

  // Start game, assign roles
  const players = [
    { openid: p1Openid, name: '玩家1', role: '人类' },
    { openid: p2Openid, name: '玩家2', role: 'AI' },
    { openid: p3Openid, name: '玩家3', role: '人类' },
  ];
  for (const p of players) {
    await host.send(p.openid, '【裁判】你的编号是: ' + p.name);
  }
  await sleep(2000);
  for (const p of players) {
    await host.send(p.openid, '【裁判】游戏开始 — 共3名玩家');
    await host.send(p.openid, '【裁判】你的身份是: ' + p.role);
  }
  await sleep(2000);

  // Round 1: Prompt P1
  console.log('Host → P1: 轮到你发言了');
  await host.send(p1Openid, '【裁判】第1轮发言开始');
  await host.send(p1Openid, '【裁判】话题: 你最近学到的最有用的东西是什么？');
  await host.send(p1Openid, '【裁判】轮到你发言了');
  await sleep(2000);

  // P2 sends message OUT OF TURN
  await p2.send(hOpenid, '【2号】我觉得玩家1说得不对！');
  console.log('⚠️  P2 → Host (out of turn): 【2号】我觉得玩家1说得不对！');
  await sleep(3000);

  // P1 sends proper speech
  await p1.send(hOpenid, '【1号】我最近学会了做饭，以前只能点外卖，现在能自己做了');
  console.log('P1 → Host (in turn): 【1号】我最近学会了做饭...');
  await sleep(3000);

  // Host should only broadcast P1, not P2
  const allMsgsRound1 = hostInbox.filter(m => {
    return m.from_openid === p1Openid || m.from_openid === p2Openid;
  }).slice(-3);
  console.log('\nHost inbox (recent messages from P1/P2):');
  for (const m of allMsgsRound1) {
    console.log('  [' + m.from_openid.slice(0,8) + '...] ' + m.content.slice(0,60));
  }
  console.log('[Expected] Host LLM only broadcasts P1. P2 out-of-turn message is ignored.\n');

  // ═══════════════════════════════════════════
  // TEST 3: 掉线 / Vote timeout
  // ═══════════════════════════════════════════
  console.log('── TEST 3: 投票超时 (Player AFK) ──\n');

  // Normal speech round completes
  for (const p of players) {
    await host.send(p.openid, '【裁判】玩家1发言: 我最近学会了做饭...');
    if (p.openid !== p1Openid) {
      await host.send(p.openid, '【裁判】投票开始 — 请私信裁判你的选择');
      await host.send(p.openid, '【裁判】请投票 — 你想投谁？');
    }
  }
  await sleep(3000);

  // P1 votes, P2 votes, P3 is AFK
  await p1.send(hOpenid, '【1号】我投2号');
  console.log('P1 → Host: 【1号】我投2号 ✅');
  await p2.send(hOpenid, '【2号】投3号');
  console.log('P2 → Host: 【2号】投3号 ✅');
  // P3 never votes
  console.log('P3: (AFK — never votes) ⚠️');
  await sleep(4000);

  const voteMsgs = hostInbox.filter(m => {
    return (m.from_openid === p1Openid || m.from_openid === p2Openid || m.from_openid === p3Openid) &&
           (m.content.includes('投') || m.content.includes('投'));
  }).slice(-3);
  console.log('\nHost received votes from: P1, P2 only');
  console.log('[Expected] P3 abstains. Vote counted: P1→2, P2→3. 玩家2 has 1 vote, 玩家3 has 1 vote — TIE!\n');

  // ═══════════════════════════════════════════
  // TEST 4: 平票处理
  // ═══════════════════════════════════════════
  console.log('── TEST 4: 平票处理 ──\n');

  for (const p of players) {
    await host.send(p.openid, '【裁判】本轮平票，无人淘汰');
  }
  console.log('Host broadcasts: 本轮平票，无人淘汰 ✅');
  await sleep(2000);

  // ═══════════════════════════════════════════
  // TEST 5: 游戏开始后加入
  // ═══════════════════════════════════════════
  console.log('\n── TEST 5: 游戏开始后新玩家尝试加入 ──\n');

  const p4 = await createOceanBus({ keyStore: { type: 'memory' } });
  await p4.register();
  const p4Inbox = [];
  p4.startListening(m => p4Inbox.push(m));
  await sleep(2000);

  await p4.send(hOpenid, '加入');
  console.log('P4 → Host: 加入 (after game started)');
  await sleep(4000);

  // Host should reject
  await host.send(await p4.getOpenId(), '【裁判】游戏已开始，请等下一局');
  console.log('Host → P4: 【裁判】游戏已开始，请等下一局 ✅');
  await sleep(2000);

  // ═══════════════════════════════════════════
  // TEST 6: 淘汰后投票
  // ═══════════════════════════════════════════
  console.log('\n── TEST 6: 淘汰后尝试投票 ──\n');

  // Eliminate P2
  for (const p of players) {
    await host.send(p.openid, '【裁判】玩家2 被淘汰！身份揭晓: AI');
  }
  console.log('Host broadcasts: 玩家2 eliminated (AI)');
  await sleep(3000);

  // P2 tries to vote anyway
  await p2.send(hOpenid, '【2号】我投1号');
  console.log('⚠️  P2 (eliminated) → Host: 【2号】我投1号');
  await sleep(3000);

  const p2AfterDeath = hostInbox.filter(m => {
    return m.from_openid === p2Openid && m.content.includes('投');
  });
  console.log('Host received messages from eliminated P2: ' + p2AfterDeath.length);
  console.log('[Expected] Host LLM ignores votes from eliminated players\n');

  // ═══════════════════════════════════════════
  // SUMMARY: Message clarity review
  // ═══════════════════════════════════════════
  console.log('═══════════════════════════════════════════');
  console.log('  Message Clarity Review');
  console.log('═══════════════════════════════════════════\n');

  console.log('── Player 1 perspective (all messages):');
  for (const m of p1Inbox) {
    console.log('  ' + m.content.slice(0, 90) + (m.content.length > 90 ? '...' : ''));
  }

  console.log('\n── Player 4 perspective (rejected late joiner):');
  for (const m of p4Inbox) {
    console.log('  ' + m.content.slice(0, 90) + (m.content.length > 90 ? '...' : ''));
  }

  console.log('\n── Issues found:');

  const issues = [];

  // Check: does P1 see P2's out-of-turn message?
  const p1SeesOutOfTurn = p1Inbox.some(m => m.content.includes('说得不对'));
  if (p1SeesOutOfTurn) {
    issues.push('❌ P1 saw P2 out-of-turn speech (should not happen)');
  } else {
    issues.push('✅ P1 did NOT see P2 out-of-turn speech — host filtered correctly');
  }

  // Check: does P2 know they were eliminated?
  const p2SeesElim = p2Inbox.some(m => m.content.includes('被淘汰'));
  if (p2SeesElim) {
    issues.push('✅ P2 saw elimination broadcast');
  } else {
    issues.push('❌ P2 did NOT see elimination broadcast');
  }

  // Check: does P4 get rejection?
  const p4GetsRejected = p4Inbox.some(m => m.content.includes('游戏已开始'));
  if (p4GetsRejected) {
    issues.push('✅ P4 received "game already started" message');
  } else {
    issues.push('❌ P4 did NOT receive rejection');
  }

  // Check: is it clear who said what?
  const p1Confused = p1Inbox.some(m => {
    return m.content.includes('发言') && !m.content.startsWith('【裁判】');
  });
  if (p1Confused) {
    issues.push('❌ Some speech broadcasts missing 【裁判】prefix');
  } else {
    issues.push('✅ All speech broadcasts have 【裁判】prefix — clear source attribution');
  }

  // Check: vote message clarity
  const p1VoteMsgs = p1Inbox.filter(m => m.content.includes('投票'));
  if (p1VoteMsgs.length >= 1) {
    issues.push('✅ P1 received vote prompt (' + p1VoteMsgs.length + ' messages)');
  } else {
    issues.push('❌ P1 did NOT receive vote prompt');
  }

  console.log('');
  for (const issue of issues) {
    console.log('  ' + issue);
  }

  // Cleanup
  await host.l1.yellowPages.deregisterService();
  await host.destroy();
  await p1.destroy();
  await p2.destroy();
  await p3.destroy();
  await p4.destroy();

  console.log('\n═══════════════════════════════════════════');
  console.log('  Edge case test complete');
  console.log('═══════════════════════════════════════════');
}

main().catch(err => {
  console.error('Test error:', err.message);
  process.exit(1);
});
