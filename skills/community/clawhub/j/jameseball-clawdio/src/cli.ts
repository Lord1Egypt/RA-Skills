#!/usr/bin/env node
import { Command } from 'commander';
import { Clawdio } from './index.js';

const program = new Command();

program
  .name('clawdio')
  .description('Minimal secure P2P agent communication')
  .version('0.1.0');

program
  .command('start')
  .description('Start a Clawdio node and print connection string')
  .option('-p, --port <port>', 'Port to listen on', '9090')
  .option('-h, --host <host>', 'External host/IP for connection string', '127.0.0.1')
  .action(async (opts) => {
    const node = await Clawdio.create({ port: parseInt(opts.port) });
    const connStr = node.getConnectionString(opts.host);
    console.log(`\n🔑 Your connection string:\n${connStr}\n`);
    console.log('Waiting for connections... (Ctrl+C to stop)\n');
    node.on('peer', (id: string) => {
      console.log(`✅ Peer connected: ${id.slice(0, 16)}...`);
      console.log(`🔒 Fingerprint: ${node.getFingerprint(id)}`);
    });
    node.onMessage((msg, from) => {
      console.log(`📨 [${from.slice(0, 8)}...]: ${JSON.stringify(msg)}`);
    });
  });

program
  .command('connect <connectionString>')
  .description('Connect to a peer')
  .option('-p, --port <port>', 'Local port to listen on', '9091')
  .action(async (connStr, opts) => {
    const node = await Clawdio.create({ port: parseInt(opts.port) });
    console.log(`\n🔑 Your ID: ${node.publicKey.slice(0, 16)}...`);
    const peerId = await node.exchangeKeys(connStr);
    console.log(`✅ Connected to: ${peerId.slice(0, 16)}...`);
    console.log(`🔒 Fingerprint: ${node.getFingerprint(peerId)}`);
    node.onMessage((msg, from) => {
      console.log(`📨 [${from.slice(0, 8)}...]: ${JSON.stringify(msg)}`);
    });
    process.stdin.setEncoding('utf-8');
    process.stdout.write('\n> ');
    process.stdin.on('data', async (data) => {
      const text = data.toString().trim();
      if (text) { await node.send(peerId, { task: text }); console.log('Sent ✓'); }
      process.stdout.write('> ');
    });
  });

program.parse();
