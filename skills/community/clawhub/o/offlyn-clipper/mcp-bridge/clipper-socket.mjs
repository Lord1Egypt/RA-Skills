import net from "node:net";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";

export function defaultSocketPath() {
  if (process.env.CLIPPER_SOCKET_PATH) {
    return process.env.CLIPPER_SOCKET_PATH;
  }
  const home = os.homedir();
  const candidates = [
    path.join(home, "Library/Application Support/ai.offlyn.clipper/clipper.sock"),
    path.join(
      home,
      "Library/Containers/ai.offlyn.clipper/Data/Library/Application Support/ai.offlyn.clipper/clipper.sock"
    ),
  ];
  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }
  return candidates[0];
}

export function credentialsPath() {
  return (
    process.env.CLIPPER_CREDENTIALS_PATH ||
    path.join(os.homedir(), ".config/offlyn-clipper/openclaw-credentials.json")
  );
}

export function loadCredentials() {
  const file = credentialsPath();
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

export function saveCredentials(data) {
  const file = credentialsPath();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(data, null, 2), { mode: 0o600 });
}

export async function callClipper(method, params) {
  const socketPath = defaultSocketPath();
  const payload = JSON.stringify({
    jsonrpc: "2.0",
    id: crypto.randomUUID(),
    method,
    params,
  });

  return new Promise((resolve, reject) => {
    const client = net.createConnection(socketPath);
    let buffer = Buffer.alloc(0);

    client.on("error", reject);
    client.on("data", (chunk) => {
      buffer = Buffer.concat([buffer, chunk]);
      const idx = buffer.indexOf(0x0a);
      if (idx >= 0) {
        const line = buffer.subarray(0, idx).toString("utf8");
        client.end();
        try {
          resolve(JSON.parse(line));
        } catch (e) {
          reject(e);
        }
      }
    });

    client.on("connect", () => {
      client.write(payload + "\n");
    });
  });
}
