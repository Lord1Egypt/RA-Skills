#!/usr/bin/env node
/**
 * Dream Lock - 防止并发巩固的锁机制
 * 用法：
 *   node dream-lock.js acquire
 *   node dream-lock.js release
 *   node dream-lock.js check
 *   node dream-lock.js force
 *
 * 原为 dream-lock.sh，已转为纯 JS
 */

const fs = require('fs');
const path = require('path');

const LOCK_DIR = process.argv[3] || path.join(process.env.HOME, '.openclaw', 'workspace', 'memory');
const LOCK_FILE = path.join(LOCK_DIR, '.dream.lock');
const HOLDER_STALE_MS = 30 * 60 * 1000; // 30 分钟

function nowMs() {
  return Date.now();
}

function acquire() {
  fs.mkdirSync(LOCK_DIR, { recursive: true });

  if (fs.existsSync(LOCK_FILE)) {
    const stat = fs.statSync(LOCK_FILE);
    const ageMs = nowMs() - stat.mtimeMs;

    if (ageMs < HOLDER_STALE_MS) {
      try {
        const holderPid = parseInt(fs.readFileSync(LOCK_FILE, 'utf8').trim());
        if (holderPid && process.pid !== holderPid) {
          // 检查进程是否存活
          try { process.kill(holderPid, 0); } catch {
            // 进程已退出，可以 reclaim
            fs.writeFileSync(LOCK_FILE, process.pid.toString());
            console.log(`ACQUIRED (stale PID ${holderPid})`);
            return 0;
          }
          console.log(`LOCKED: PID ${holderPid} 执行中 (${ageMs}ms)`);
          return 1;
        }
      } catch {}
    } else {
      console.log(`STALE: lock expired (${ageMs}ms), reclaim`);
    }
  }

  fs.writeFileSync(LOCK_FILE, process.pid.toString());
  console.log('ACQUIRED');
  return 0;
}

function release() {
  if (!fs.existsSync(LOCK_FILE)) {
    console.log('SKIP: no lock file');
    return 0;
  }

  try {
    const holderPid = parseInt(fs.readFileSync(LOCK_FILE, 'utf8').trim());
    if (!holderPid || holderPid === process.pid) {
      fs.unlinkSync(LOCK_FILE);
      console.log('RELEASED');
      return 0;
    } else {
      console.log(`SKIP: held by ${holderPid}`);
      return 1;
    }
  } catch {
    console.log('SKIP: could not read lock file');
    return 1;
  }
}

function check() {
  if (!fs.existsSync(LOCK_FILE)) {
    console.log('FREE');
    return 0;
  }

  const stat = fs.statSync(LOCK_FILE);
  const ageMs = nowMs() - stat.mtimeMs;

  try {
    const holderPid = parseInt(fs.readFileSync(LOCK_FILE, 'utf8').trim());
    if (holderPid && ageMs < HOLDER_STALE_MS) {
      try { process.kill(holderPid, 0); } catch {
        console.log(`FREE (stale: ${holderPid}, ${ageMs}ms)`);
        return 0;
      }
      console.log(`BUSY: PID ${holderPid} (${ageMs}ms)`);
      return 1;
    }
    console.log(`FREE (stale: ${holderPid}, ${ageMs}ms)`);
    return 0;
  } catch {
    console.log('FREE');
    return 0;
  }
}

function force() {
  fs.mkdirSync(LOCK_DIR, { recursive: true });
  fs.writeFileSync(LOCK_FILE, process.pid.toString());
  console.log('FORCED');
  return 0;
}

// 主函数
const cmd = process.argv[2] || 'check';
const commands = { acquire, release, check, force };

if (!commands[cmd]) {
  console.log(`用法: node dream-lock.js {acquire|release|check|force}`);
  process.exit(1);
}

process.exit(commands[cmd]());
