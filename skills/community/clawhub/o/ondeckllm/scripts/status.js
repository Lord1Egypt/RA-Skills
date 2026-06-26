#!/usr/bin/env node
/**
 * OnDeckLLM status checker.
 * Checks if the OnDeckLLM dashboard is running and reachable.
 * Output: JSON with running, port, url, pid (if found)
 */

import { execSync } from 'child_process';
import http from 'http';

const DEFAULT_PORT = 3900;

function findProcess() {
  try {
    const out = execSync("ps aux | grep '[o]ndeckllm' | grep -v 'status.js'", {
      encoding: 'utf-8',
      timeout: 5000,
    }).trim();
    if (!out) return null;
    const lines = out.split('\n');
    // Extract PID from first match
    const parts = lines[0].trim().split(/\s+/);
    return { pid: parseInt(parts[1], 10), line: lines[0] };
  } catch {
    return null;
  }
}

function checkHttp(port) {
  return new Promise((resolve) => {
    const req = http.get(`http://localhost:${port}/`, { timeout: 3000 }, (res) => {
      resolve({ reachable: true, status: res.statusCode });
    });
    req.on('error', () => resolve({ reachable: false }));
    req.on('timeout', () => { req.destroy(); resolve({ reachable: false }); });
  });
}

async function main() {
  const proc = findProcess();
  const port = DEFAULT_PORT;
  const health = await checkHttp(port);

  const result = {
    running: health.reachable,
    port,
    url: `http://localhost:${port}`,
  };

  if (proc) result.pid = proc.pid;
  if (health.status) result.httpStatus = health.status;

  console.log(JSON.stringify(result));
}

main();
