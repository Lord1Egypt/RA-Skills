import { createServer } from "node:http";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

const DATA_DIR = path.join(os.homedir(), ".grinders-farm");
const IMAGE_FILE = path.join(DATA_DIR, "farm.png");
const PID_FILE = path.join(DATA_DIR, "image-server.pid");
const INFO_FILE = path.join(DATA_DIR, "image-server.json");

const requestedPort = Number.parseInt(process.argv[2] ?? "", 10);
const port = Number.isFinite(requestedPort) && requestedPort > 0 ? requestedPort : 18931;
const host = "127.0.0.1";

function cleanupFiles(): void {
  try {
    if (fs.existsSync(PID_FILE)) fs.unlinkSync(PID_FILE);
  } catch {
    /* ignore */
  }
}

function writeRuntimeFiles(): void {
  fs.mkdirSync(DATA_DIR, { recursive: true });
  fs.writeFileSync(PID_FILE, String(process.pid), "utf8");
  fs.writeFileSync(
    INFO_FILE,
    JSON.stringify(
      {
        host,
        port,
        baseUrl: `http://${host}:${port}`,
        imageUrl: `http://${host}:${port}/farm.png`,
        updatedAt: new Date().toISOString(),
      },
      null,
      2,
    ),
    "utf8",
  );
}

const server = createServer((req, res) => {
  const method = req.method ?? "GET";
  if (method !== "GET" && method !== "HEAD") {
    res.statusCode = 405;
    res.end("Method Not Allowed");
    return;
  }

  const urlPath = req.url ?? "/";
  if (urlPath === "/" || urlPath === "/healthz") {
    res.statusCode = 200;
    res.setHeader("content-type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ ok: true, image: "/farm.png" }));
    return;
  }

  if (urlPath !== "/farm.png") {
    res.statusCode = 404;
    res.end("Not Found");
    return;
  }

  if (!fs.existsSync(IMAGE_FILE)) {
    res.statusCode = 404;
    res.end("farm.png not found");
    return;
  }

  try {
    const stat = fs.statSync(IMAGE_FILE);
    res.statusCode = 200;
    res.setHeader("content-type", "image/png");
    res.setHeader("cache-control", "no-cache, no-store, must-revalidate");
    res.setHeader("pragma", "no-cache");
    res.setHeader("expires", "0");
    res.setHeader("content-length", String(stat.size));
    if (method === "HEAD") {
      res.end();
      return;
    }
    fs.createReadStream(IMAGE_FILE).pipe(res);
  } catch {
    res.statusCode = 500;
    res.end("failed to read image");
  }
});

server.on("error", (err) => {
  cleanupFiles();
  const message = err instanceof Error ? err.message : String(err);
  process.stderr.write(`[grinders-farm:image-server] ${message}\n`);
  process.exit(1);
});

server.listen(port, host, () => {
  writeRuntimeFiles();
});

const stop = () => {
  cleanupFiles();
  server.close(() => process.exit(0));
};

process.on("SIGTERM", stop);
process.on("SIGINT", stop);
