#!/usr/bin/env node
/**
 * OSM-P2P Hybrid CLI
 */

import { Command } from 'commander';
import chalk from 'chalk';
import { OSMP2P } from '../index.js';

const program = new Command();
let app = null;

async function initApp() {
  if (!app) {
    app = new OSMP2P();
    await app.start();
    
    app.on('message', (msg, room) => {
      console.log(chalk`\n{cyan.bold [${room.topic || room.id}]} {green ${msg.sender}}: ${msg.content}`);
    });
  }
  return app;
}

program.name('osm-p2p').description('OSM-P2P Hybrid').version('1.0.0');

program.command('status').description('查看状态').action(async () => {
  const a = await initApp();
  const s = a.getStatus();
  console.log(chalk`{cyan.bold === 节点状态 ===}`);
  console.log(`节点: ${s.name} (${s.nodeId})`);
  console.log(`在线节点: ${s.peers}, 房间: ${s.rooms}`);
  if (s.stats.udp) console.log(`UDP: ${s.stats.udp.connected ? '已连接' : '断开'}`);
  if (s.stats.nostr) console.log(`Nostr: ${s.stats.nostr.connected ? '已连接' : '断开'}`);
});

program.command('list').description('列出节点').action(async () => {
  const a = await initApp();
  const peers = a.getPeers();
  if (peers.length === 0) {
    console.log(chalk`{yellow 未发现节点}`);
    return;
  }
  console.log(chalk`{cyan.bold === 在线节点 (${peers.length}) ===}`);
  for (const p of peers) {
    const t = p.udpReachable && p.nostrReachable ? 'UDP+Nostr' : p.udpReachable ? 'UDP' : 'Nostr';
    console.log(`• ${p.name} (${p.nodeId}) - ${t}`);
  }
});

program.command('qr').description('显示名片').action(async () => {
  const a = await initApp();
  console.log(chalk`{green ${a.generateCard()}}`);
});

program.command('add <card>').description('添加节点').action(async (card) => {
  const a = await initApp();
  const parsed = OSMP2P.parseCard(card);
  if (!parsed) { console.log(chalk`{red 无效名片}`); return; }
  const peer = a.discovery.addPeerFromCard(parsed);
  console.log(chalk`{green 已添加: ${peer.name}}`);
});

program.command('broadcast <msg>').description('广播消息').option('--no-nostr', '仅UDP').action(async (msg, opts) => {
  const a = await initApp();
  await a.broadcast(msg, opts.nostr);
  console.log(chalk`{green 广播完成}`);
});

program.command('chat').description('交互模式').action(async () => {
  const a = await initApp();
  a.createRoom('broadcast', '聊天室');
  console.log(chalk`{cyan.bold === 交互模式 (输入 /quit 退出) ===}`);
  
  const readline = await import('readline');
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  rl.setPrompt('> ');
  rl.prompt();
  
  rl.on('line', async (line) => {
    if (line.trim() === '/quit') { rl.close(); return; }
    if (line.trim()) await a.sendMessage(line.trim());
    rl.prompt();
  });
});

program.parse();

process.on('SIGINT', async () => {
  if (app) await app.stop();
  process.exit(0);
});
