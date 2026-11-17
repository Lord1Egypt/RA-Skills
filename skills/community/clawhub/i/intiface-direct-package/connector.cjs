#!/usr/bin/env node
/**
 * Intiface Direct Connector — Buttplug v4 WebSocket Client
 *
 * Connects directly to Intiface Central using the Buttplug v4 protocol.
 * Bypasses unstable third-party MCP bridges.
 *
 * DESIGN: State persists until the next command. A vibration/pattern keeps
 * running until a later command stops it or starts a new one. Each command
 * process takes over a per-device lock (/tmp/intiface-locks/dev<N>.pid) so
 * the previous session is terminated before the new one starts sending.
 *
 * Usage:
 *   node connector.cjs                                   # localhost:12345
 *   INTIFACE_WS_URL=ws://192.168.0.13:12345 node connector.cjs  # remote
 *   node connector.cjs list                              # list devices
 *   node connector.cjs vibrate 0 0 70                    # steady 70 until stopped/replaced
 *   node connector.cjs vibrate 0 0 70 3                  # timed burst: 70 for 3s, then stop
 *   node connector.cjs loop 0 0 25 [intervalSec]         # steady 25, re-sent every 3s
 *   node connector.cjs pattern 0 0 wave                  # loop pattern until stopped/replaced
 *   node connector.cjs pattern 0 0 wave 2                # pattern, 2 cycles, then stop
 *   node connector.cjs pattern 0 0 list                  # list available patterns
 *   node connector.cjs stop 0                            # stop device 0 (ends any session)
 *
 * Patterns are timed sequences of intensity frames. Values 0-100, each held
 * for its millisecond duration. Without a cycle count a pattern loops
 * forever; SIGINT/SIGTERM (kill from another command) and the final stop send
 * a Vibrate 0 before the socket closes.
 */

const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');

const WS_URL = process.env.INTIFACE_WS_URL || 'ws://localhost:12345';

function clamp(v) {
  v = Math.round(Number(v) || 0);
  return Math.max(0, Math.min(100, v));
}

// ---- per-device session lock -------------------------------------------
const LOCK_DIR = process.env.INTIFACE_LOCK_DIR || '/tmp/intiface-locks';
let lockfile = null;

function acquireDeviceLock(deviceIdx) {
  try { fs.mkdirSync(LOCK_DIR, { recursive: true }); } catch (e) {}
  lockfile = path.join(LOCK_DIR, 'dev' + deviceIdx + '.pid');
  let old = null;
  try { old = fs.readFileSync(lockfile, 'utf8').trim(); } catch (e) {}
  if (old && old !== String(process.pid)) {
    const oldPid = parseInt(old, 10);
    if (oldPid > 0) {
      try {
        process.kill(oldPid, 0); // still alive?
        console.log('Stopping previous session (pid ' + oldPid + ')');
        process.kill(oldPid, 'SIGTERM');
      } catch (e) {
        console.log('Removing stale lock (pid ' + oldPid + ' not running)');
      }
    }
  }
  fs.writeFileSync(lockfile, String(process.pid));
}

function releaseDeviceLock() {
  if (!lockfile) return;
  try {
    if (fs.readFileSync(lockfile, 'utf8').trim() === String(process.pid)) {
      fs.unlinkSync(lockfile);
    }
  } catch (e) {}
}

// ---- command args -------------------------------------------------------
const cmd = process.argv[2];
const deviceIndex = parseInt(process.argv[3] || '0');
const featureIndex = parseInt(process.argv[4] || '0');
const rawValue = process.argv[5];
const value = clamp(rawValue);
const durationSec = parseFloat(process.argv[6] || '0');
const intervalSec = parseFloat(process.argv[6] || '3');

// ---- stateful commands take over the device lock before connecting ----
const holdsDevice = ['vibrate', 'loop', 'pattern', 'stop'].includes(cmd);
if (holdsDevice) acquireDeviceLock(deviceIndex);

const ws = new WebSocket(WS_URL);
let mid = 1;
let devices = {};

function sendMsg(type, params = {}) {
  const id = mid++;
  params.Id = id;
  ws.send(JSON.stringify([{[type]: params}]));
  return id;
}

function setVibrate(dev, feat, v) {
  sendMsg('OutputCmd', {
    DeviceIndex: dev,
    FeatureIndex: feat,
    Command: { Vibrate: { Value: clamp(v) } }
  });
}

// ---- pattern presets: frames of [value, holdMs] -------------------------
const PATTERNS = {
  // one smooth wave cycle: climb to 100, ease back down
  wave:   [[20,250],[45,250],[70,250],[90,250],[100,250],[90,250],[70,250],[45,250],[20,250]],
  // sharp on/off pulses
  pulse:  [[70,200],[0,200],[70,200],[0,200],[70,200],[0,300]],
  // slow climb to full, brief hold, drop
  rise:   [[15,300],[30,300],[45,300],[60,300],[75,300],[90,300],[100,400],[100,400],[0,300]],
  // gentle: low hum with a few spikes
  tease:  [[15,1500],[40,400],[15,1500],[60,400],[15,1500],[40,400],[15,1500],[0,400]],
};

function framesMs(name) {
  return (PATTERNS[name] || []).reduce((s, f) => s + f[1], 0);
}

let stopping = false;
function gracefulStop(reason) {
  if (stopping) return;
  stopping = true;
  console.log(reason || 'Stopping device ' + deviceIndex);
  if (ws.readyState === WebSocket.OPEN) {
    setVibrate(deviceIndex, 0, 0);
    setTimeout(() => { releaseDeviceLock(); try { ws.close(); } catch (e) {} }, 300);
  } else {
    releaseDeviceLock();
  }
  setTimeout(() => process.exit(0), 1000); // hard stop fallback
}
process.on('SIGINT', () => gracefulStop('Interrupted — stopping device ' + deviceIndex));
process.on('SIGTERM', () => gracefulStop('Stopped by new command'));

function runPattern(name, cycles) {
  const frames = PATTERNS[name];
  let idx = 0;
  let remaining = cycles; // NaN/Infinity handled by caller; undefined = forever
  console.log('Pattern "' + name + '" ' +
    (Number.isFinite(remaining) ? '(' + remaining + 'x)' : '(looping)') +
    ' on ' + deviceIndex + ':' + featureIndex +
    ' — send "stop ' + deviceIndex + '" or a new command to change');
  const step = () => {
    if (Number.isFinite(remaining) && idx === 0) {
      if (remaining <= 0) {
        console.log('Pattern done — stopping');
        gracefulStop('Pattern finished');
        return;
      }
      remaining--;
    }
    const [v, ms] = frames[idx++];
    if (idx >= frames.length) idx = 0;
    setVibrate(deviceIndex, featureIndex, v);
    setTimeout(step, ms);
  };
  step();
}

// ---- timed commands only: give up after a bound -------------------------
let overallTimeoutMs = 8000; // list / unknown
if (cmd === 'vibrate') overallTimeoutMs = durationSec > 0 ? durationSec * 1000 + 4000 : 0; // timed burst vs steady
if (cmd === 'pattern') {
  const cyclesArg = parseInt(process.argv[6] || '', 10);
  if (Number.isFinite(cyclesArg)) overallTimeoutMs = framesMs(process.argv[5] || '') * cyclesArg + 6000;
  else overallTimeoutMs = 0; // looping
}
if (cmd === 'loop') overallTimeoutMs = 0; // looping
if (cmd === 'stop') overallTimeoutMs = 4000;

ws.on('open', () => {
  sendMsg('RequestServerInfo', {
    ClientName: 'OpenClaw',
    ProtocolVersionMajor: 4,
    ProtocolVersionMinor: 0
  });
});

ws.on('message', (raw) => {
  const txt = raw.toString();
  try {
    const msgs = JSON.parse(txt);
    if (!Array.isArray(msgs)) return;
    for (const m of msgs) {
      if (m.ServerInfo) {
        if (cmd === 'list' || !cmd) {
          sendMsg('RequestDeviceList');
        } else if (cmd === 'vibrate') {
          setVibrate(deviceIndex, featureIndex, value);
          if (durationSec > 0) {
            console.log('Vibrate ' + deviceIndex + ':' + featureIndex + ' @ ' + value + ' for ' + durationSec + 's');
            setTimeout(() => gracefulStop('Timed burst done'), durationSec * 1000);
          } else {
            console.log('Vibrating ' + deviceIndex + ':' + featureIndex + ' @ ' + value +
              ' until stopped/replaced — send "stop ' + deviceIndex + '" or a new command');
            setInterval(() => setVibrate(deviceIndex, featureIndex, value), 3000); // keep-alive
          }
        } else if (cmd === 'loop') {
          console.log('Looping ' + deviceIndex + ':' + featureIndex + ' @ ' + value +
            ' (re-sent every ' + intervalSec + 's) until stopped/replaced');
          const loop = () => setVibrate(deviceIndex, featureIndex, value);
          loop();
          setInterval(loop, intervalSec * 1000);
        } else if (cmd === 'pattern') {
          const pname = process.argv[5] || '';
          if (pname === 'list') {
            console.log('Available patterns: ' + Object.keys(PATTERNS).join(', '));
            releaseDeviceLock();
            ws.close();
            return;
          }
          if (!PATTERNS[pname]) {
            console.error('Unknown pattern: ' + pname);
            console.error('Available patterns: ' + Object.keys(PATTERNS).join(', '));
            releaseDeviceLock();
            ws.close();
            return;
          }
          const cyclesArg = parseInt(process.argv[6] || '', 10);
          runPattern(pname, Number.isFinite(cyclesArg) ? cyclesArg : Infinity);
        } else if (cmd === 'stop') {
          setVibrate(deviceIndex, 0, 0);
          console.log('Stopped device ' + deviceIndex);
          setTimeout(() => { releaseDeviceLock(); ws.close(); }, 300);
        } else {
          console.log('Unknown command:', cmd);
          releaseDeviceLock();
          ws.close();
        }
      }
      else if (m.DeviceList) {
        devices = m.DeviceList.Devices || {};
        const keys = Object.keys(devices);
        console.log('Devices connected: ' + keys.length);
        for (const k of keys) {
          const d = devices[k];
          const features = Object.values(d.DeviceFeatures || {}).map(f =>
            Object.keys(f.Output || {}).join(',')
          ).filter(Boolean).join(', ') || 'none';
          console.log('  [' + d.DeviceIndex + '] ' + d.DeviceName + ' (features: ' + features + ')');
        }
        ws.close();
      }
      else if (m.Ok) {
        if (!['loop', 'pattern', 'vibrate'].includes(cmd)) {
          console.log('Command acknowledged (id: ' + m.Ok.Id + ')');
        }
      }
      else if (m.Error) {
        console.error('Error:', m.Error.ErrorMessage);
      }
    }
  } catch (e) {}
});

ws.on('error', (e) => {
  console.error('Connection failed:', e.message);
  releaseDeviceLock();
  process.exit(1);
});

ws.on('close', () => {
  releaseDeviceLock();
  process.exit(0);
});

if (overallTimeoutMs > 0) {
  setTimeout(() => { console.error('Timed out'); releaseDeviceLock(); process.exit(1); }, overallTimeoutMs);
}
