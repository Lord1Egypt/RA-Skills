const http = require('http');
const { spawn } = require('child_process');
const { httpRequest, getBaseUrl } = require('./http');

async function isPortInUse(port) {
  return new Promise((resolve) => {
    const checkPort = (host) => {
      return new Promise((r) => {
        const req = http.get(`http://${host}:${port}/session`, (res) => {
          r(true);
        });
        req.on('error', () => r(false));
        req.setTimeout(1000, () => {
          req.destroy();
          r(false);
        });
      });
    };

    (async () => {
      if (await checkPort('127.0.0.1')) {
        resolve(true);
        return;
      }
      if (await checkPort('localhost')) {
        resolve(true);
        return;
      }
      resolve(false);
    })();
  });
}

async function findAvailablePort(startPort = 4096) {
  for (let port = startPort; port < 4200; port++) {
    const inUse = await isPortInUse(port);
    if (!inUse) {
      return port;
    }
  }
  throw new Error('No available port found');
}

async function startServer(port) {
  return new Promise((resolve, reject) => {
    const serverProcess = spawn('opencode', ['serve', '--hostname', '127.0.0.1', '--port', String(port)], {
      stdio: ['ignore', 'pipe', 'pipe']
    });

    const checkServer = setInterval(async () => {
      try {
        const result = await httpRequest(`http://127.0.0.1:${port}/session`, { method: 'GET' });
        if (Array.isArray(result)) {
          clearInterval(checkServer);
          resolve({ process: serverProcess, port });
        }
      } catch {}
    }, 500);

    serverProcess.on('error', (err) => {
      clearInterval(checkServer);
      reject(err);
    });

    setTimeout(() => {
      if (!serverProcess.killed) {
        clearInterval(checkServer);
        serverProcess.kill();
        reject(new Error('Server startup timeout'));
      }
    }, 30000);
  });
}

async function findExistingServer() {
  for (let port = 4096; port < 4110; port++) {
    try {
      const result = await httpRequest(`${getBaseUrl('127.0.0.1', port)}/session`, { method: 'GET' });
      if (Array.isArray(result)) {
        return port;
      }
    } catch {
      continue;
    }
  }
  return null;
}

async function getOrStartServer() {
  const port = await findAvailablePort(4096);
  console.log(`Starting new server on port ${port}...`);
  
  const serverInfo = await startServer(port);
  
  return { port, serverProcess: serverInfo.process, close: () => serverInfo.process?.kill() };
}

module.exports = {
  findAvailablePort,
  startServer,
  findExistingServer,
  getOrStartServer
};