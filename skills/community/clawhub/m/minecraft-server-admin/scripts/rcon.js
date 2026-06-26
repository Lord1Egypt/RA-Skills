#!/usr/bin/env node
/**
 * rcon.js — Minecraft RCON client
 *
 * CLI usage:
 *   node rcon.js "list"
 *   node rcon.js "ban PlayerX griefing"
 *   node rcon.js "give Steve minecraft:diamond 64"
 *
 * Programmatic usage:
 *   const { rconExec, rconMulti } = require('./rcon');
 *   const result = await rconExec('list');
 *   const results = await rconMulti(['save-all', 'list']);
 *
 * Environment variables:
 *   MC_RCON_HOST      (default: localhost)
 *   MC_RCON_PORT      (default: 25575)
 *   MC_RCON_PASSWORD  (required)
 */

'use strict';

const net = require('net');

const RCON = {
  host: process.env.MC_RCON_HOST || 'localhost',
  port: parseInt(process.env.MC_RCON_PORT) || 25575,
  password: process.env.MC_RCON_PASSWORD || '',
  timeout: parseInt(process.env.MC_RCON_TIMEOUT) || 5000,
};

const TYPE = { AUTH: 3, AUTH_RESP: 2, CMD: 2, CMD_RESP: 0 };
const AUTH_FAIL_ID = -1;

function encodePacket(id, type, payload) {
  const payloadBytes = Buffer.from(payload + '\x00', 'utf8');
  const length = 4 + 4 + payloadBytes.length + 1;
  const buf = Buffer.allocUnsafe(4 + length);
  buf.writeInt32LE(length, 0);
  buf.writeInt32LE(id, 4);
  buf.writeInt32LE(type, 8);
  payloadBytes.copy(buf, 12);
  buf.writeUInt8(0, 12 + payloadBytes.length);
  return buf;
}

function decodePackets(buf) {
  const packets = [];
  let offset = 0;
  while (offset + 4 <= buf.length) {
    const length = buf.readInt32LE(offset);
    if (offset + 4 + length > buf.length) break;
    const id = buf.readInt32LE(offset + 4);
    const type = buf.readInt32LE(offset + 8);
    const payload = buf.slice(offset + 12, offset + 4 + length - 2).toString('utf8');
    packets.push({ id, type, payload });
    offset += 4 + length;
  }
  return packets;
}

function rconExec(command, options = {}) {
  const cfg = { ...RCON, ...options };

  return new Promise((resolve, reject) => {
    if (!cfg.password) {
      return reject(new Error('MC_RCON_PASSWORD is not set. Please set the environment variable.'));
    }

    const socket = new net.Socket();
    let buffer = Buffer.alloc(0);
    let authenticated = false;
    let responsePayload = '';
    const reqId = Math.floor(Math.random() * 0x7fffff) + 1;

    socket.connect(cfg.port, cfg.host, () => {
      socket.write(encodePacket(reqId, TYPE.AUTH, cfg.password));
    });

    socket.on('data', (data) => {
      buffer = Buffer.concat([buffer, data]);
      const packets = decodePackets(buffer);
      if (packets.length) {
        const consumed = packets.reduce((sum, p) => sum + 4 + (4 + 4 + Buffer.byteLength(p.payload, 'utf8') + 2), 0);
        buffer = buffer.slice(consumed);
      }

      for (const pkt of packets) {
        if (!authenticated) {
          if (pkt.id === AUTH_FAIL_ID) {
            socket.destroy();
            return reject(new Error('RCON authentication failed: wrong password.'));
          }
          if (pkt.id === reqId) {
            authenticated = true;
            const cmd = command.startsWith('/') ? command.slice(1) : command;
            socket.write(encodePacket(reqId, TYPE.CMD, cmd));
          }
        } else {
          responsePayload += pkt.payload;
          socket.destroy();
          resolve(responsePayload.trim() || '(command succeeded with no output)');
        }
      }
    });

    socket.on('error', (err) => {
      if (err.code === 'ECONNREFUSED') {
        reject(new Error(
          `Unable to connect to RCON (${cfg.host}:${cfg.port}).\n` +
          `Check:\n` +
          `  1. Is the server running?\n` +
          `  2. Is enable-rcon=true set in server.properties?\n` +
          `  3. Is rcon.port=${cfg.port} correct?`
        ));
      } else {
        reject(new Error(`RCON connection error: ${err.message}`));
      }
    });

    socket.setTimeout(cfg.timeout, () => {
      socket.destroy();
      reject(new Error(`RCON connection timed out (${cfg.timeout}ms)`));
    });
  });
}

async function rconMulti(commands) {
  const results = [];
  for (const command of commands) {
    try {
      const result = await rconExec(command);
      results.push({ command, result, error: null });
    } catch (err) {
      results.push({ command, result: null, error: err.message });
    }
  }
  return results;
}

async function testConnection() {
  const start = Date.now();
  try {
    const result = await rconExec('list');
    return { ok: true, latency: Date.now() - start, listOutput: result };
  } catch (err) {
    return { ok: false, error: err.message, latency: Date.now() - start };
  }
}

if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: node rcon.js "<command>"');
    console.log('Examples:');
    console.log('  node rcon.js "list"');
    console.log('  node rcon.js "ban PlayerX griefing"');
    console.log('  node rcon.js "give Steve minecraft:diamond 64"');
    console.log('\nEnvironment variables:');
    console.log('  MC_RCON_HOST     (default: localhost)');
    console.log('  MC_RCON_PORT     (default: 25575)');
    console.log('  MC_RCON_PASSWORD (required)');

    console.log('\nTesting current RCON connection...');
    testConnection().then(r => {
      if (r.ok) {
        console.log(`OK connection healthy (latency ${r.latency}ms)`);
        console.log(`   ${r.listOutput}`);
      } else {
        console.error(`Connection failed: ${r.error}`);
        process.exit(1);
      }
    });
    return;
  }

  const command = args.join(' ');
  rconExec(command)
    .then(result => {
      console.log(result);
      process.exit(0);
    })
    .catch(err => {
      console.error(err.message);
      process.exit(1);
    });
}

module.exports = { rconExec, rconMulti, testConnection };
