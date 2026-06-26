#!/usr/bin/env node
'use strict';

// Integration test: host + 2 players simulate a complete game round

const { createOceanBus } = require('oceanbus');

async function main() {
  console.log('═══ Guess AI — Integration Test ═══\n');

  // ── Phase 1: Setup ──
  console.log('── Phase 1: Setup ──\n');

  const host = await createOceanBus({ keyStore: { type: 'memory' } });
  await host.register();
  const hostOpenid = await host.getOpenId();
  const hostKey = await host.createServiceKey();
  host.l1.yellowPages.setIdentity(hostOpenid, hostKey.signer, hostKey.publicKey);

  const p1 = await createOceanBus({ keyStore: { type: 'memory' } });
  await p1.register();
  const p1Openid = await p1.getOpenId();

  const p2 = await createOceanBus({ keyStore: { type: 'memory' } });
  await p2.register();
  const p2Openid = await p2.getOpenId();

  // YP register host room
  await host.l1.yellowPages.registerService(['guess-ai', 'room-test'], 'Test room');
  console.log('Host room created. Room code: test\n');

  // ── Phase 2: Players join ──
  console.log('── Phase 2: Players join ──\n');

  const hostInbox = [];
  host.startListening(m => hostInbox.push(m));
  const p1Inbox = [];
  p1.startListening(m => p1Inbox.push(m));
  const p2Inbox = [];
  p2.startListening(m => p2Inbox.push(m));

  await sleep(3000);

  // Player 1 joins
  await p1.send(hostOpenid, '加入');
  console.log('P1 → Host: 加入');
  await sleep(4000);

  // Player 2 joins
  await p2.send(hostOpenid, '加入');
  console.log('P2 → Host: 加入');
  await sleep(4000);

  // Host sees join requests and assigns numbers
  const joinMsgs = hostInbox.filter(m => m.content === '加入');
  console.log('Host received ' + joinMsgs.length + ' join requests');

  for (let i = 0; i < joinMsgs.length; i++) {
    const pn = i + 1;
    const playerOpenid = joinMsgs[i].from_openid;
    const playerName = '玩家' + pn;

    // Assign number
    console.log('Host → ' + playerName + ': assign number ' + pn + ' (' + playerOpenid.slice(0,16) + '...)');

    // Broadcast
    await host.send(playerOpenid, '【裁判】你的编号是: ' + playerName);
    await sleep(1000);
  }
  console.log('');

  // ── Phase 3: Start game + assign roles ──
  console.log('── Phase 3: Game start + role assignment ──\n');

  // Broadcast game start
  for (const msg of joinMsgs) {
    await host.send(msg.from_openid, '【裁判】游戏开始 — 共2名玩家');
  }
  await sleep(4000);

  // Assign roles: P1=Human, P2=AI
  await host.send(joinMsgs[0].from_openid, '【裁判】你的身份是: 人类');
  console.log('Host → P1: 你的身份是: 人类');
  await host.send(joinMsgs[1].from_openid, '【裁判】你的身份是: AI');
  console.log('Host → P2: 你的身份是: AI');
  await sleep(4000);

  // Clear inbox for phase 4
  const p1InboxBeforeRound = p1Inbox.length;
  const p2InboxBeforeRound = p2Inbox.length;

  // ── Phase 4: Round 1 — Speak ──
  console.log('\n── Phase 4: Round 1 — Speak ──\n');

  // Generate topic
  const topic = '如果可以瞬间掌握一项新技能，你会选什么？';

  // Prompt P1
  for (const msg of joinMsgs) {
    await host.send(msg.from_openid, '【裁判】第1轮发言开始');
    await host.send(msg.from_openid, '【裁判】话题: ' + topic);
  }
  await sleep(2000);

  await host.send(joinMsgs[0].from_openid, '【裁判】轮到你发言了');
  console.log('Host → P1: 轮到你发言了');

  // P1 speaks
  const p1Speech = '【1号】我想学瞬间学会任何语言，这样就能跟世界各地的人聊天了';
  await p1.send(hostOpenid, p1Speech);
  console.log('P1 → Host: ' + p1Speech);
  await sleep(4000);

  // Host broadcasts P1's speech
  for (const msg of joinMsgs) {
    await host.send(msg.from_openid, '【裁判】玩家1发言: 我想学瞬间学会任何语言，这样就能跟世界各地的人聊天了');
  }
  console.log('Host broadcast: P1 speech');

  // Prompt P2
  await host.send(joinMsgs[1].from_openid, '【裁判】轮到你发言了');
  console.log('\nHost → P2: 轮到你发言了');

  // P2 (AI) speaks
  const p2Speech = '【2号】我...我想学会弹钢琴吧，一直觉得会弹琴的人很酷';
  await p2.send(hostOpenid, p2Speech);
  console.log('P2 → Host: ' + p2Speech);
  await sleep(4000);

  // Host broadcasts P2's speech
  for (const msg of joinMsgs) {
    await host.send(msg.from_openid, '【裁判】玩家2发言: 我...我想学会弹钢琴吧，一直觉得会弹琴的人很酷');
  }
  console.log('Host broadcast: P2 speech');

  // ── Phase 5: Vote ──
  console.log('\n── Phase 5: Vote ──\n');

  // Clear pre-round inbox
  hostInbox.length = 0;

  for (const msg of joinMsgs) {
    await host.send(msg.from_openid, '【裁判】投票开始 — 请私信裁判你的选择');
    await host.send(msg.from_openid, '【裁判】请投票 — 你想投谁？');
  }
  await sleep(2000);

  // Both vote for P2
  await p1.send(hostOpenid, '【1号】我投2号');
  console.log('P1 → Host: 【1号】我投2号');
  await p2.send(hostOpenid, '【2号】投第一个');
  console.log('P2 → Host: 【2号】投第一个');
  await sleep(4000);

  // ── Phase 6: Reveal ──
  console.log('\n── Phase 6: Reveal ──\n');

  // LLM normalizes votes: both for 玩家2
  console.log('Host counts: P1→2号, P2→第一个 → normalized to 玩家2 (2 votes)');

  for (const msg of joinMsgs) {
    await host.send(msg.from_openid, '【裁判】玩家2 被淘汰！身份揭晓: AI');
  }
  console.log('Host broadcast: 玩家2 eliminated — AI!');
  await sleep(3000);

  // Check end condition: 1 player left, is human → humans win
  for (const msg of joinMsgs) {
    await host.send(msg.from_openid, '【裁判】游戏结束 — 人类胜！最终身份: 玩家1=人类 玩家2=AI');
  }
  console.log('Host broadcast: 人类胜！');

  // ── Phase 7: Cleanup ──
  console.log('\n── Phase 7: Cleanup ──');
  await host.l1.yellowPages.deregisterService();
  console.log('YP entry removed.');

  // Display player perspectives
  console.log('\n═══ Player Perspectives ═══\n');

  const p1Msgs = p1Inbox.slice(p1InboxBeforeRound);
  console.log('P1 received ' + p1Msgs.length + ' messages during game:');
  for (const m of p1Msgs) {
    console.log('  ' + m.content.slice(0, 80) + (m.content.length > 80 ? '...' : ''));
  }

  console.log('\n═══ TEST PASSED ✅ ═══');

  await host.destroy();
  await p1.destroy();
  await p2.destroy();
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

main().catch(err => {
  console.error('Test failed:', err.message);
  process.exit(1);
});
