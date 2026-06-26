/**
 * knowledge-server-ts — 知识仓库搜索界面（TypeScript 版）
 *
 * 架构：
 *   TS (Express) 负责 Web 层 — 静态文件、配置读写、请求路由
 *   Python (FastAPI) 负责 RAG 层 — 向量搜索、索引管理、文件扫描
 *
 * 启动顺序：
 *   1. uvicorn knowledge_api:app --host 0.0.0.0 --port 8765
 *   2. npx tsx src/server.ts
 */

import express, { type Request, type Response, type NextFunction } from "express";
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

// ─── 路径 ───────────────────────────────────────────────

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KNOWLEDGE_DIR = path.join(homedir(), "workspace", "knowledge");
const PUBLIC_DIR = path.join(__dirname, "..", "public");
const CONFIG_FILE = path.join(KNOWLEDGE_DIR, ".knowledge-config.json");
const PYTHON_API = "http://127.0.0.1:8768";

// ─── 类型定义 ────────────────────────────────────────────

interface KnowledgeConfig {
  knowledge_dir: string;
  sources: string[];
  ollama_host: string;
  embed_model: string;
}

interface BrowseEntry {
  name: string;
  type: "dir";
  path: string;
}

interface BrowseResult {
  current: string;
  parent: string;
  entries: BrowseEntry[];
}

interface SearchResultItem {
  title: string;
  author: string;
  date: string;
  bvid: string;
  source_type: string;
  source_label: string;
  text: string;
  score: number;
}

interface SearchResponse {
  results?: SearchResultItem[];
  error?: string;
}

interface StatsResponse {
  index: {
    total_chunks: number;
    source_stats: Record<string, number>;
  };
  files: Array<{
    name: string;
    dir: string;
    size: number;
    path: string;
  }>;
  ollama: {
    online: boolean;
    models?: string[];
    embed_ready?: boolean;
    error?: string;
  };
  indexed_files?: string[];
}

interface StatusResponse {
  online: boolean;
  models?: string[];
  embed_ready?: boolean;
  error?: string;
}

interface ReindexResponse {
  ok: boolean;
  chunks?: number;
  error?: string;
}

// ─── 配置读写 ────────────────────────────────────────────

const DEFAULT_CONFIG: KnowledgeConfig = {
  knowledge_dir: "~/workspace/knowledge",
  sources: ["bilibili", "notes", "wechat-articles", "other"],
  ollama_host: "http://localhost:11434",
  embed_model: "qwen3-embedding:0.6b",
};

function loadConfig(): KnowledgeConfig {
  try {
    const raw = readFileSync(CONFIG_FILE, "utf-8");
    return JSON.parse(raw) as KnowledgeConfig;
  } catch {
    saveConfig(DEFAULT_CONFIG);
    return { ...DEFAULT_CONFIG };
  }
}

function saveConfig(cfg: KnowledgeConfig): void {
  mkdirSync(KNOWLEDGE_DIR, { recursive: true });
  writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2), "utf-8");
}

// ─── 工具函数 ────────────────────────────────────────────

/** 目录浏览（纯 Node.js，无需 Python） */
function browseDir(dirPath: string): BrowseResult {
  let p = dirPath.replace(/^~/, homedir());
  if (!existsSync(p)) p = homedir();
  try {
    if (!statSync(p).isDirectory()) p = path.dirname(p);
  } catch {
    p = homedir();
  }
  p = path.resolve(p);

  const entries: BrowseEntry[] = [];
  try {
    const names = readdirSync(p).sort();
    for (const name of names) {
      const full = path.join(p, name);
      try {
        if (statSync(full).isDirectory()) {
          entries.push({ name, type: "dir", path: full });
        }
      } catch {
        // skip inaccessible
      }
    }
  } catch {
    // permission denied
  }

  const parent = p === "/" ? "/" : path.dirname(p);
  return { current: p, parent, entries };
}

// ─── Express 应用 ───────────────────────────────────────

const app = express();
const PORT = parseInt(process.env["PORT"] ?? "5777");

app.use(express.json());

app.use((_req: Request, res: Response, next: NextFunction) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  next();
});

app.use(express.static(PUBLIC_DIR));

// ─── API Proxy: 转发到 Python FastAPI ─────────────────

async function proxyToPython(req: Request, res: Response, path: string): Promise<void> {
  try {
    const url = `${PYTHON_API}${path}${req.url.includes("?") ? req.url.substring(req.url.indexOf("?")) : ""}`;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    const options: RequestInit = {
      method: req.method,
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
    };
    if (req.method === "POST" && req.body) {
      options.body = JSON.stringify(req.body);
    }
    const pythonResp = await fetch(url, options);
    clearTimeout(timeout);
    const data: unknown = await pythonResp.json();
    res.status(pythonResp.status).json(data);
  } catch (err) {
    const errResponse: Record<string, string> = { error: `Python API 不可用: ${err}` };
    res.status(502).json(errResponse);
  }
}

app.post("/api/search", async (req: Request, res: Response) => {
  await proxyToPython(req, res, "/api/search");
});

app.post("/search", async (req: Request, res: Response) => {
  await proxyToPython(req, res, "/api/search");
});

app.get("/api/stats", async (req: Request, res: Response) => {
  await proxyToPython(req, res, "/api/stats");
});

app.post("/api/reindex", async (req: Request, res: Response) => {
  await proxyToPython(req, res, "/api/reindex");
});

app.get("/api/status", async (req: Request, res: Response) => {
  await proxyToPython(req, res, "/api/status");
});

app.delete("/api/delete-file", async (req: Request, res: Response) => {
  await proxyToPython(req, res, "/api/delete-file");
});

// ─── API: 目录浏览（TS 本地处理） ──────────────────────

app.get("/api/browse", (req: Request, res: Response) => {
  try {
    const dirPath = (req.query["path"] as string) || homedir();
    const result = browseDir(dirPath);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: String(err) });
  }
});

// ─── API: 配置（代理到 Python API 处理，确保能写入） ──

app.get("/api/config", async (req: Request, res: Response) => {
  await proxyToPython(req, res, "/api/config");
});

app.post("/api/config", async (req: Request, res: Response) => {
  await proxyToPython(req, res, "/api/config");
});

// ─── 前端 SPA 路由 ──────────────────────────────────────

app.use((_req: Request, res: Response) => {
  res.sendFile(path.join(PUBLIC_DIR, "index.html"));
});

// ─── 启动 ────────────────────────────────────────────────

app.listen(PORT, () => {
  console.log(`🌐 知识仓库搜索界面 (TypeScript 版)`);
  console.log(`   打开 http://localhost:${PORT} 使用`);
  console.log(`   Python API → ${PYTHON_API}`);
  console.log(`   按 Ctrl+C 停止服务`);
});
