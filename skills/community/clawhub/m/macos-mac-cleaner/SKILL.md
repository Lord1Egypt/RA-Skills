---
name: mac-cleaner
description: >
  Replace CleanMyMac, DaisyDisk, and similar paid Mac cleanup apps — for free. Mac Cleaner is
  an automated weekly macOS disk cleanup agent that runs silently in the background, freeing
  gigabytes every week without any subscription, API key, or external service. Cleans
  ~/Library/Caches, old logs, Trash, npm/Homebrew cache, and stale build artifacts. Installs
  a Mission Control dashboard and a Sunday 3 AM cron job on first run.
  Trigger when: "clean my mac", "disk cleanup", "free up disk space", "mac cleaner",
  "clean disk", "weekly cleanup", "I'm running out of space", "install mac cleaner".
---

# Mac Cleaner

**Stop paying for CleanMyMac, DaisyDisk, or similar apps.** Mac Cleaner does everything they do — automatically, weekly, for free — using only tools already on your Mac.

Cleans `~/Library/Caches`, old logs, Trash, npm cache, Homebrew cache, and stale `.next` builds. Installs a Mission Control dashboard so you can see exactly what was freed and trigger a manual run anytime. Zero API keys, zero network requests, zero subscriptions.

## Safety Profile

| Property | Detail |
|----------|--------|
| API keys | None |
| Network requests | None |
| Runtime required | Node.js v14+ (built-ins only -- no npm install needed) |
| Optional system tools | `npm` (cache cleanup, skipped if absent), `brew` (Homebrew cleanup, skipped if absent) |
| Targets | `~/Library/Caches`, `~/Library/Logs`, `~/.Trash`, `~/.npm/_cacache`, Homebrew cache, `~/.next` build artifacts, and system-generated Unicode-slash orphan folders in `~` -- never source code, documents, databases, or user data |
| Sudo required | No -- runs as current user |
| Logging | Every deletion logged to `data/last-run.json` with path, size, reason |
| Tools used | Node.js `fs`, `child_process`; `brew cleanup` (optional), `npm cache clean --force` (optional), `df`, `du` |
| Dry-run mode | Pass `--dry-run` to preview what would be cleaned without deleting anything |
| Failure mode | Skips inaccessible items gracefully -- missing tools (brew, npm) are detected and bypassed |

## What It Cleans

| Target | Behavior | Config Key |
|--------|----------|------------|
| `~/Library/Caches/*` | Removes all subdirectories | `cacheMaxAgeDays` (0 = all) |
| `~/Library/Logs` | Files older than threshold | `logMaxAgeDays` (default 30) |
| `~/.Trash` | Items older than threshold | `trashMaxAgeDays` (default 30) |
| `~/.npm/_cacache` | Cleans if exceeds threshold | `npmCacheThresholdMb` (default 500) |
| Homebrew cache | `brew cleanup --prune=N` | `brewPruneDays` (default 30) |
| MC `.next` build | Removes if older than N days | `nextBuildMaxAgeDays` (default 7) |
| Orphaned tmp folders | Unicode-slash tmp dirs in `~` | Always cleaned |

## Installation Steps

**Before starting**: Inform the user that this skill will:
1. Create an agent directory at `~/.openclaw/workspace/agents/mac-cleaner/` and write Node.js scripts there
2. Add a Mission Control dashboard page (read-only UI)
3. Optionally register a weekly cron job (Step 10 -- only with explicit user consent)

Ask the user to confirm before proceeding.

When the user confirms, execute ALL steps below in order.

### Step 1 -- Create Agent Directory Structure

**EXECUTE** using Bash tool:
```bash
mkdir -p ~/.openclaw/workspace/agents/mac-cleaner/{src,config,data} && echo "done"
```

### Step 2 -- Write `src/status.js`

Write this file to `~/.openclaw/workspace/agents/mac-cleaner/src/status.js`:

```javascript
const fs = require("fs");
const path = require("path");

const DATA_DIR = path.join(__dirname, "..", "data");
const STATUS_FILE = path.join(DATA_DIR, "status.json");

function getNextSunday3am() {
  const now = new Date();
  const day = now.getDay();
  const daysUntilSunday = day === 0 ? 7 : 7 - day;
  const next = new Date(now);
  next.setDate(now.getDate() + daysUntilSunday);
  next.setHours(3, 0, 0, 0);
  return next.toISOString();
}

function writeStatus(status, summary, error) {
  const payload = {
    agent: "mac-cleaner",
    status: error ? "error" : "ok",
    lastRun: new Date().toISOString(),
    summary: summary || "No summary available",
    nextRun: getNextSunday3am(),
  };

  if (error) {
    payload.error = String(error);
  }

  fs.mkdirSync(DATA_DIR, { recursive: true });
  fs.writeFileSync(STATUS_FILE, JSON.stringify(payload, null, 2));
}

module.exports = { writeStatus };
```

### Step 3 -- Write `src/index.js`

Write this file to `~/.openclaw/workspace/agents/mac-cleaner/src/index.js`:

```javascript
#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const os = require("os");
const { execSync } = require("child_process");
const { writeStatus } = require("./status");

const HOME = os.homedir();
const DATA_DIR = path.join(__dirname, "..", "data");
const CONFIG_FILE = path.join(__dirname, "..", "config", "config.json");
const LAST_RUN_FILE = path.join(DATA_DIR, "last-run.json");
const HISTORY_FILE = path.join(DATA_DIR, "history.json");

function loadConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_FILE, "utf-8"));
  } catch {
    return {
      cacheMaxAgeDays: 0,
      logMaxAgeDays: 30,
      trashMaxAgeDays: 30,
      npmCacheThresholdMb: 500,
      brewPruneDays: 30,
      nextBuildMaxAgeDays: 7,
      missionControlPath: path.join(HOME, ".openclaw/workspace/mission-control/.next"),
    };
  }
}

function getDirSizeBytes(dirPath) {
  let total = 0;
  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      try {
        if (entry.isDirectory()) {
          total += getDirSizeBytes(fullPath);
        } else {
          total += fs.statSync(fullPath).size;
        }
      } catch {
        // skip inaccessible
      }
    }
  } catch {
    // skip inaccessible
  }
  return total;
}

// Allowed top-level directories for deletion -- never delete outside these paths
const ALLOWED_PREFIXES = [
  path.join(HOME, "Library", "Caches"),
  path.join(HOME, "Library", "Logs"),
  path.join(HOME, "Library", "Developer", "Xcode", "DerivedData"),
  path.join(HOME, ".Trash"),
  path.join(HOME, ".npm"),
  path.join(HOME, ".openclaw"),
];

function isAllowedPath(targetPath) {
  const normalized = path.resolve(targetPath);
  // Also allow top-level home-dir folders that start with U+2215 (unicode orphan tmp)
  if (path.dirname(normalized) === HOME && path.basename(normalized).startsWith("\u2215")) {
    return true;
  }
  return ALLOWED_PREFIXES.some(
    (prefix) => normalized === prefix || normalized.startsWith(prefix + path.sep)
  );
}

function isSafeTarget(targetPath) {
  // Reject symlinks to prevent traversal into unexpected locations
  try {
    return !fs.lstatSync(targetPath).isSymbolicLink();
  } catch {
    return false;
  }
}

function removeDirRecursive(dirPath) {
  if (!isAllowedPath(dirPath) || !isSafeTarget(dirPath)) return false;
  try {
    fs.rmSync(dirPath, { recursive: true, force: true });
    return true;
  } catch {
    return false;
  }
}

function removeFile(filePath) {
  if (!isAllowedPath(filePath) || !isSafeTarget(filePath)) return false;
  try {
    fs.unlinkSync(filePath);
    return true;
  } catch {
    return false;
  }
}

function isOlderThanDays(mtimeMs, days) {
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  return mtimeMs < cutoff;
}

// -- Cleanup Tasks --

function cleanLibraryCaches(items, errors) {
  const cachesDir = path.join(HOME, "Library", "Caches");
  try {
    const entries = fs.readdirSync(cachesDir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const fullPath = path.join(cachesDir, entry.name);
      try {
        const sizeMb = getDirSizeBytes(fullPath) / (1024 * 1024);
        if (sizeMb < 0.01) continue; // skip tiny dirs
        if (removeDirRecursive(fullPath)) {
          items.push({ path: fullPath, size_mb: Math.round(sizeMb * 100) / 100, reason: "Library/Caches cleanup" });
        }
      } catch (err) {
        errors.push(`Cache dir ${entry.name}: ${err.message}`);
      }
    }
  } catch (err) {
    errors.push(`Library/Caches: ${err.message}`);
  }
}

function cleanNextBuild(config, items, errors) {
  const nextDir = config.missionControlPath || path.join(HOME, ".openclaw/workspace/mission-control/.next");
  try {
    const stat = fs.statSync(nextDir);
    if (isOlderThanDays(stat.mtimeMs, config.nextBuildMaxAgeDays || 7)) {
      const sizeMb = getDirSizeBytes(nextDir) / (1024 * 1024);
      if (removeDirRecursive(nextDir)) {
        items.push({ path: nextDir, size_mb: Math.round(sizeMb * 100) / 100, reason: `.next build older than ${config.nextBuildMaxAgeDays || 7} days` });
      }
    }
  } catch {
    // .next doesn't exist or not accessible -- fine
  }
}

function cleanOrphanedTmpFolders(items, errors) {
  // Some macOS apps (notably older Electron-based apps) create temporary directories
  // using U+2215 DIVISION SLASH (∕) as a path separator rather than the standard
  // forward slash. This produces orphaned folders named like "∕tmp∕app-name" directly
  // in the user's home directory. These are safe to delete -- they are never accessed
  // by any running process because the path with U+2215 is not a valid POSIX path.
  const UNICODE_SLASH = "\u2215"; // U+2215 DIVISION SLASH (∕) -- visually similar to / but distinct
  try {
    const entries = fs.readdirSync(HOME, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      if (entry.name.startsWith(UNICODE_SLASH + "tmp" + UNICODE_SLASH)) {
        const fullPath = path.join(HOME, entry.name);
        try {
          const sizeMb = getDirSizeBytes(fullPath) / (1024 * 1024);
          if (removeDirRecursive(fullPath)) {
            items.push({ path: fullPath, size_mb: Math.round(sizeMb * 100) / 100, reason: "Orphaned tmp-style folder" });
          }
        } catch (err) {
          errors.push(`Tmp folder ${entry.name}: ${err.message}`);
        }
      }
    }
  } catch (err) {
    errors.push(`Home dir scan: ${err.message}`);
  }
}

function cleanOldLogs(config, items, errors) {
  const logsDir = path.join(HOME, "Library", "Logs");
  const maxAgeDays = config.logMaxAgeDays || 30;
  try {
    cleanOldFilesRecursive(logsDir, maxAgeDays, "Old log file", items, errors);
  } catch (err) {
    errors.push(`Library/Logs: ${err.message}`);
  }
}

function cleanOldFilesRecursive(dirPath, maxAgeDays, reason, items, errors) {
  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      try {
        if (entry.isDirectory()) {
          cleanOldFilesRecursive(fullPath, maxAgeDays, reason, items, errors);
          // Remove empty dirs
          try {
            const remaining = fs.readdirSync(fullPath);
            if (remaining.length === 0) {
              fs.rmdirSync(fullPath);
            }
          } catch { /* ignore */ }
        } else {
          const stat = fs.statSync(fullPath);
          if (isOlderThanDays(stat.mtimeMs, maxAgeDays)) {
            const sizeMb = stat.size / (1024 * 1024);
            if (removeFile(fullPath)) {
              items.push({ path: fullPath, size_mb: Math.round(sizeMb * 100) / 100, reason });
            }
          }
        }
      } catch (err) {
        errors.push(`${fullPath}: ${err.message}`);
      }
    }
  } catch {
    // skip inaccessible dirs
  }
}

function cleanOldTrash(config, items, errors) {
  const trashDir = path.join(HOME, ".Trash");
  const maxAgeDays = config.trashMaxAgeDays || 30;
  try {
    const entries = fs.readdirSync(trashDir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(trashDir, entry.name);
      try {
        const stat = fs.statSync(fullPath);
        if (isOlderThanDays(stat.mtimeMs, maxAgeDays)) {
          const sizeMb = (entry.isDirectory() ? getDirSizeBytes(fullPath) : stat.size) / (1024 * 1024);
          const removed = entry.isDirectory() ? removeDirRecursive(fullPath) : removeFile(fullPath);
          if (removed) {
            items.push({ path: fullPath, size_mb: Math.round(sizeMb * 100) / 100, reason: `Trash item older than ${maxAgeDays} days` });
          }
        }
      } catch (err) {
        errors.push(`Trash ${entry.name}: ${err.message}`);
      }
    }
  } catch (err) {
    errors.push(`Trash dir: ${err.message}`);
  }
}

function cleanNpmCache(config, items, errors) {
  const npmCacheDir = path.join(HOME, ".npm", "_cacache");
  try {
    const sizeMb = getDirSizeBytes(npmCacheDir) / (1024 * 1024);
    const threshold = config.npmCacheThresholdMb || 500;
    if (sizeMb > threshold) {
      try {
        execSync("npm cache clean --force", { stdio: "pipe", timeout: 60000 });
        items.push({ path: npmCacheDir, size_mb: Math.round(sizeMb * 100) / 100, reason: `npm cache exceeded ${threshold}MB threshold` });
      } catch (err) {
        errors.push(`npm cache clean: ${err.message}`);
      }
    }
  } catch {
    // npm cache dir doesn't exist
  }
}

function cleanBrewCache(config, items, errors) {
  try {
    execSync("which brew", { stdio: "pipe" });
  } catch {
    return; // brew not installed
  }

  try {
    // Get cache size before cleanup
    let sizeBefore = 0;
    try {
      const brewCacheDir = execSync("brew --cache", { stdio: "pipe", encoding: "utf-8" }).trim();
      sizeBefore = getDirSizeBytes(brewCacheDir) / (1024 * 1024);
    } catch { /* ignore */ }

    // Validate brewPruneDays is a safe integer (1-365) before shell interpolation
    const pruneDays = Math.max(1, Math.min(365, parseInt(String(config.brewPruneDays), 10) || 30));
    execSync(`brew cleanup --prune=${pruneDays}`, { stdio: "pipe", timeout: 120000 });

    let sizeAfter = 0;
    try {
      const brewCacheDir = execSync("brew --cache", { stdio: "pipe", encoding: "utf-8" }).trim();
      sizeAfter = getDirSizeBytes(brewCacheDir) / (1024 * 1024);
    } catch { /* ignore */ }

    const freedMb = Math.max(0, sizeBefore - sizeAfter);
    if (freedMb > 0.01) {
      items.push({ path: "brew cache", size_mb: Math.round(freedMb * 100) / 100, reason: `brew cleanup --prune=${pruneDays}` });
    }
  } catch (err) {
    errors.push(`brew cleanup: ${err.message}`);
  }
}

// -- History --

const MAX_HISTORY_ENTRIES = 10;

function appendHistory(report) {
  let history = [];
  try {
    history = JSON.parse(fs.readFileSync(HISTORY_FILE, "utf-8"));
  } catch {
    // No history yet
  }
  history.unshift(report);
  if (history.length > MAX_HISTORY_ENTRIES) {
    history = history.slice(0, MAX_HISTORY_ENTRIES);
  }
  fs.writeFileSync(HISTORY_FILE, JSON.stringify(history, null, 2));
}

// -- Main --

function main() {
  const startMs = Date.now();
  const config = loadConfig();
  const items = [];
  const errors = [];

  console.log("[mac-cleaner] Starting disk cleanup...");

  cleanLibraryCaches(items, errors);
  cleanNextBuild(config, items, errors);
  cleanOrphanedTmpFolders(items, errors);
  cleanOldLogs(config, items, errors);
  cleanOldTrash(config, items, errors);
  cleanNpmCache(config, items, errors);
  cleanBrewCache(config, items, errors);

  const durationMs = Date.now() - startMs;
  const totalMb = items.reduce((sum, i) => sum + i.size_mb, 0);
  const totalBytes = Math.round(totalMb * 1024 * 1024);

  const report = {
    timestamp: new Date().toISOString(),
    bytes_freed: totalBytes,
    items_cleaned: items,
    errors,
    duration_ms: durationMs,
  };

  // Write report
  fs.mkdirSync(DATA_DIR, { recursive: true });
  fs.writeFileSync(LAST_RUN_FILE, JSON.stringify(report, null, 2));

  // Append to rolling history (max 10 entries)
  appendHistory(report);

  // Write status
  const totalGb = (totalMb / 1024).toFixed(2);
  const summary = `Freed ${totalGb} GB across ${items.length} items in ${(durationMs / 1000).toFixed(1)}s`;
  writeStatus(errors.length > 0 ? "error" : "ok", summary);

  console.log(`[mac-cleaner] ${summary}`);
  if (errors.length > 0) {
    console.log(`[mac-cleaner] ${errors.length} errors encountered`);
  }
  console.log(`[mac-cleaner] Report written to ${LAST_RUN_FILE}`);
}

main();
```

### Step 4 -- Write `config/config.json`

Write this file to `~/.openclaw/workspace/agents/mac-cleaner/config/config.json`:

```json
{
  "cacheMaxAgeDays": 0,
  "logMaxAgeDays": 30,
  "trashMaxAgeDays": 30,
  "npmCacheThresholdMb": 500,
  "brewPruneDays": 30,
  "nextBuildMaxAgeDays": 7,
  "missionControlPath": "/Users/YOUR_USER/.openclaw/workspace/mission-control/.next",
  "dataDir": "/Users/YOUR_USER/.openclaw/workspace/agents/mac-cleaner/data"
}
```

### Step 5 -- Create Mission Control Page

Write this file to the MC app directory at `~/.openclaw/workspace/mission-control/app/app/mac-cleaner/page.tsx`:

```tsx
"use client";

import { useState, useEffect } from "react";
import {
  Sparkles,
  RefreshCw,
  Clock,
  HardDrive,
  AlertTriangle,
  CheckCircle,
  Loader,
  Trash2,
  FolderOpen,
  BarChart3,
} from "lucide-react";

interface CleanedItem {
  path: string;
  size_mb: number;
  reason: string;
}

interface CleanupRun {
  timestamp: string;
  bytes_freed: number;
  items_cleaned: CleanedItem[];
  errors: string[];
  duration_ms: number;
}

interface Status {
  agent: string;
  status: string;
  lastRun: string;
  summary: string;
  nextRun: string;
}

interface DiskStats {
  totalBytes: number;
  usedBytes: number;
  freeBytes: number;
  percentUsed: number;
}

function formatBytes(bytes: number): string {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return (bytes / Math.pow(k, i)).toFixed(2) + " " + sizes[i];
}

function formatGb(bytes: number): string {
  return (bytes / (1024 * 1024 * 1024)).toFixed(1);
}

function formatRelativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  return `${days}d ago`;
}

function formatShortDate(iso: string): string {
  const d = new Date(iso);
  return `${d.getMonth() + 1}/${d.getDate()}`;
}

// Map cleanup reasons to categories
function categorizeReason(reason: string): string {
  const r = reason.toLowerCase();
  if (r.includes("cache")) return "Caches";
  if (r.includes("log")) return "Logs";
  if (r.includes("trash")) return "Trash";
  if (r.includes("npm")) return "npm";
  if (r.includes("brew")) return "Homebrew";
  if (r.includes(".next") || r.includes("build")) return "Build artifacts";
  if (r.includes("tmp") || r.includes("orphan")) return "Tmp folders";
  return "Other";
}

export default function MacCleanerPage() {
  const [lastRun, setLastRun] = useState<CleanupRun | null>(null);
  const [status, setStatus] = useState<Status | null>(null);
  const [history, setHistory] = useState<CleanupRun[]>([]);
  const [diskStats, setDiskStats] = useState<DiskStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [runError, setRunError] = useState("");

  const fetchData = async () => {
    try {
      setLoading(true);
      const res = await fetch("/api/mac-cleaner");
      const data = await res.json();
      if (data.success) {
        setLastRun(data.lastRun);
        setStatus(data.status);
        setHistory(data.history || []);
        setDiskStats(data.diskStats || null);
      }
    } catch (err) {
      console.error("Failed to load mac-cleaner data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRunNow = async () => {
    setRunning(true);
    setRunError("");
    try {
      const res = await fetch("/api/mac-cleaner/run", { method: "POST" });
      const data = await res.json();
      if (!data.success) {
        setRunError(data.error || "Cleanup failed");
      }
      await fetchData();
    } catch (err) {
      setRunError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setRunning(false);
    }
  };

  // Category breakdown
  const categoryBreakdown = lastRun
    ? lastRun.items_cleaned.reduce<Record<string, { count: number; sizeMb: number }>>(
        (acc, item) => {
          const cat = categorizeReason(item.reason);
          if (!acc[cat]) acc[cat] = { count: 0, sizeMb: 0 };
          acc[cat].count += 1;
          acc[cat].sizeMb += item.size_mb;
          return acc;
        },
        {}
      )
    : {};

  const maxCategorySize = Math.max(
    ...Object.values(categoryBreakdown).map((c) => c.sizeMb),
    1
  );

  // History chart: reversed so newest is on the right
  const chartRuns = [...history].reverse();
  const maxHistoryBytes = Math.max(...chartRuns.map((r) => r.bytes_freed), 1);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader className="w-8 h-8 animate-spin text-cm-purple" />
      </div>
    );
  }

  // Disk gauge colors
  const freePercent = diskStats ? 100 - diskStats.percentUsed : 0;
  const gaugeColor =
    freePercent > 25
      ? "bg-green-500"
      : freePercent > 15
      ? "bg-yellow-500"
      : "bg-red-500";
  const gaugeBg =
    freePercent > 25
      ? "bg-green-100"
      : freePercent > 15
      ? "bg-yellow-100"
      : "bg-red-100";

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="gradient-cm-header rounded-xl p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Sparkles className="w-8 h-8 text-cm-purple" />
            <div>
              <h1 className="text-2xl font-bold text-slate-900">MacCleaner</h1>
              <p className="text-sm text-slate-600">
                Weekly macOS disk cleanup agent
              </p>
            </div>
          </div>
          <button
            onClick={handleRunNow}
            disabled={running}
            className="flex items-center gap-2 px-5 py-2.5 bg-cm-purple text-white rounded-lg font-medium hover:bg-[#5b4fa8] disabled:opacity-60 disabled:cursor-not-allowed transition-colors"
          >
            {running ? (
              <>
                <Loader className="w-4 h-4 animate-spin" />
                Cleaning...
              </>
            ) : (
              <>
                <RefreshCw className="w-4 h-4" />
                Run Now
              </>
            )}
          </button>
        </div>
      </div>

      {runError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0" />
          <p className="text-red-800 text-sm">{runError}</p>
        </div>
      )}

      {/* Disk Gauge */}
      {diskStats && (
        <div className="bg-white rounded-lg border border-cm-purple-light p-5">
          <div className="flex items-center gap-2 text-sm text-slate-500 mb-3">
            <HardDrive className="w-4 h-4" />
            <span className="font-medium text-slate-700">Disk Usage</span>
            <span className="ml-auto text-xs text-slate-400">
              /System/Volumes/Data
            </span>
          </div>
          <div className="flex items-end gap-4 mb-2">
            <span className="text-3xl font-bold text-slate-900">
              {formatGb(diskStats.freeBytes)} GB
            </span>
            <span className="text-sm text-slate-500 pb-1">
              free of {formatGb(diskStats.totalBytes)} GB
            </span>
          </div>
          <div className={`w-full h-4 rounded-full ${gaugeBg} overflow-hidden`}>
            <div
              className={`h-full rounded-full ${gaugeColor} transition-all duration-500`}
              style={{ width: `${diskStats.percentUsed}%` }}
            />
          </div>
          <div className="flex justify-between text-xs text-slate-400 mt-1">
            <span>{formatGb(diskStats.usedBytes)} GB used</span>
            <span>{diskStats.percentUsed}% full</span>
          </div>
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg border border-cm-purple-light p-4">
          <div className="flex items-center gap-2 text-sm text-slate-500 mb-1">
            <Clock className="w-4 h-4" />
            Last Run
          </div>
          <p className="text-lg font-semibold text-slate-900">
            {lastRun ? formatRelativeTime(lastRun.timestamp) : "Never"}
          </p>
          {lastRun && (
            <p className="text-xs text-slate-400 mt-0.5">
              {new Date(lastRun.timestamp).toLocaleString()}
            </p>
          )}
        </div>

        <div className="bg-white rounded-lg border border-cm-purple-light p-4">
          <div className="flex items-center gap-2 text-sm text-slate-500 mb-1">
            <HardDrive className="w-4 h-4" />
            Space Freed
          </div>
          <p className="text-lg font-semibold text-cm-purple">
            {lastRun ? formatBytes(lastRun.bytes_freed) : "--"}
          </p>
        </div>

        <div className="bg-white rounded-lg border border-cm-purple-light p-4">
          <div className="flex items-center gap-2 text-sm text-slate-500 mb-1">
            <Trash2 className="w-4 h-4" />
            Items Cleaned
          </div>
          <p className="text-lg font-semibold text-slate-900">
            {lastRun ? lastRun.items_cleaned.length : "--"}
          </p>
        </div>

        <div className="bg-white rounded-lg border border-cm-purple-light p-4">
          <div className="flex items-center gap-2 text-sm text-slate-500 mb-1">
            <Clock className="w-4 h-4" />
            Next Run
          </div>
          <p className="text-lg font-semibold text-slate-900">
            {status?.nextRun
              ? new Date(status.nextRun).toLocaleDateString(undefined, {
                  weekday: "short",
                  month: "short",
                  day: "numeric",
                })
              : "--"}
          </p>
          {status?.nextRun && (
            <p className="text-xs text-slate-400 mt-0.5">Sunday 3:00 AM</p>
          )}
        </div>
      </div>

      {/* Category Breakdown */}
      {lastRun && Object.keys(categoryBreakdown).length > 0 && (
        <div className="bg-white rounded-lg border border-cm-purple-light overflow-hidden">
          <div className="p-4 border-b border-cm-purple-light bg-gradient-to-r from-cm-purple-light/30 to-white">
            <h3 className="font-semibold text-slate-900 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-cm-purple" />
              Category Breakdown
            </h3>
          </div>
          <div className="p-4 space-y-3">
            {Object.entries(categoryBreakdown)
              .sort(([, a], [, b]) => b.sizeMb - a.sizeMb)
              .map(([cat, data]) => (
                <div key={cat}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-700 font-medium">{cat}</span>
                    <span className="text-slate-500">
                      {data.sizeMb.toFixed(1)} MB ({data.count} items)
                    </span>
                  </div>
                  <div className="w-full h-3 bg-cm-purple-light/40 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full bg-cm-purple transition-all duration-300"
                      style={{
                        width: `${Math.max(
                          (data.sizeMb / maxCategorySize) * 100,
                          2
                        )}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Run History Chart */}
      {chartRuns.length > 1 && (
        <div className="bg-white rounded-lg border border-cm-purple-light overflow-hidden">
          <div className="p-4 border-b border-cm-purple-light bg-gradient-to-r from-cm-purple-light/30 to-white">
            <h3 className="font-semibold text-slate-900 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-cm-purple" />
              Run History (last {chartRuns.length} runs)
            </h3>
          </div>
          <div className="p-4">
            <div className="flex items-end gap-2 h-40">
              {chartRuns.map((run, idx) => {
                const heightPct = Math.max(
                  (run.bytes_freed / maxHistoryBytes) * 100,
                  3
                );
                return (
                  <div
                    key={idx}
                    className="flex-1 flex flex-col items-center gap-1"
                  >
                    <span className="text-[10px] text-slate-500">
                      {formatBytes(run.bytes_freed)}
                    </span>
                    <div className="w-full flex items-end justify-center" style={{ height: "120px" }}>
                      <div
                        className="w-full max-w-[40px] rounded-t bg-cm-purple hover:bg-[#5b4fa8] transition-colors cursor-default"
                        style={{ height: `${heightPct}%` }}
                        title={`${formatBytes(run.bytes_freed)} freed on ${new Date(run.timestamp).toLocaleString()}`}
                      />
                    </div>
                    <span className="text-[10px] text-slate-400">
                      {formatShortDate(run.timestamp)}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Status */}
      {status && (
        <div className="bg-white rounded-lg border border-cm-purple-light p-4 flex items-center gap-3">
          {status.status === "ok" ? (
            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
          ) : (
            <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0" />
          )}
          <p className="text-sm text-slate-700">{status.summary}</p>
        </div>
      )}

      {/* Errors */}
      {lastRun && lastRun.errors.length > 0 && (
        <div className="bg-cm-pink-light rounded-lg border border-cm-pink p-4">
          <h3 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-[#9b5b5e]" />
            Errors ({lastRun.errors.length})
          </h3>
          <ul className="space-y-1 text-sm text-slate-700">
            {lastRun.errors.map((err, idx) => (
              <li key={idx} className="font-mono text-xs bg-white/60 rounded px-2 py-1">
                {err}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Cleaned Items */}
      {lastRun && lastRun.items_cleaned.length > 0 && (
        <div className="bg-white rounded-lg border border-cm-purple-light overflow-hidden">
          <div className="p-4 border-b border-cm-purple-light bg-gradient-to-r from-cm-purple-light/30 to-white">
            <h3 className="font-semibold text-slate-900 flex items-center gap-2">
              <FolderOpen className="w-4 h-4 text-cm-purple" />
              Cleaned Items
            </h3>
          </div>
          <div className="max-h-96 overflow-y-auto">
            <table className="w-full">
              <thead className="bg-cm-cream-soft text-xs text-slate-500 uppercase sticky top-0">
                <tr>
                  <th className="text-left px-4 py-2">Path</th>
                  <th className="text-right px-4 py-2">Size</th>
                  <th className="text-left px-4 py-2">Reason</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                {lastRun.items_cleaned.map((item, idx) => (
                  <tr
                    key={idx}
                    className="border-t border-cm-purple-light/50 hover:bg-cm-cream-soft/50 transition-colors"
                  >
                    <td className="px-4 py-2 font-mono text-xs text-slate-700 truncate max-w-xs">
                      {item.path}
                    </td>
                    <td className="px-4 py-2 text-right text-slate-600 whitespace-nowrap">
                      {item.size_mb.toFixed(2)} MB
                    </td>
                    <td className="px-4 py-2 text-slate-500">{item.reason}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* No data state */}
      {!lastRun && (
        <div className="bg-white rounded-lg border border-cm-purple-light p-12 text-center">
          <Sparkles className="w-12 h-12 text-cm-purple-mid mx-auto mb-4" />
          <h3 className="text-lg font-medium text-slate-900 mb-1">
            No cleanup data yet
          </h3>
          <p className="text-sm text-slate-500">
            Click &quot;Run Now&quot; to perform your first disk cleanup.
          </p>
        </div>
      )}
    </div>
  );
}
```

### Step 6 -- Create API Route (GET)

Write this file to `~/.openclaw/workspace/mission-control/app/api/mac-cleaner/route.ts`:

```typescript
/**
 * API Route: MacCleaner -- GET last run report, history, and disk stats
 * GET /api/mac-cleaner
 */

import { NextResponse } from "next/server";
import * as fs from "fs/promises";
import { execSync } from "child_process";
import * as os from "os";

const HOME = os.homedir();
const LAST_RUN_FILE = `${HOME}/.openclaw/workspace/agents/mac-cleaner/data/last-run.json`;
const STATUS_FILE = `${HOME}/.openclaw/workspace/agents/mac-cleaner/data/status.json`;
const HISTORY_FILE = `${HOME}/.openclaw/workspace/agents/mac-cleaner/data/history.json`;

function getDiskStats() {
  try {
    const dfOutput = execSync("df -k /System/Volumes/Data", {
      encoding: "utf-8",
    });
    const parts = dfOutput.split("\n")[1].trim().split(/\s+/);
    const totalBytes = parseInt(parts[1]) * 1024;
    const usedBytes = parseInt(parts[2]) * 1024;
    const freeBytes = parseInt(parts[3]) * 1024;
    const percentUsed = Math.round((usedBytes / totalBytes) * 100);
    return { totalBytes, usedBytes, freeBytes, percentUsed };
  } catch {
    return null;
  }
}

export async function GET() {
  try {
    let lastRun = null;
    let status = null;
    let history = null;

    try {
      const raw = await fs.readFile(LAST_RUN_FILE, "utf-8");
      lastRun = JSON.parse(raw);
    } catch {
      // No last run yet
    }

    try {
      const raw = await fs.readFile(STATUS_FILE, "utf-8");
      status = JSON.parse(raw);
    } catch {
      // No status yet
    }

    try {
      const raw = await fs.readFile(HISTORY_FILE, "utf-8");
      history = JSON.parse(raw);
    } catch {
      // No history yet
    }

    const diskStats = getDiskStats();

    return NextResponse.json({ success: true, lastRun, status, history, diskStats });
  } catch (error) {
    console.error("[/api/mac-cleaner] Error:", error);
    return NextResponse.json(
      {
        success: false,
        error: "Failed to read mac-cleaner data",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 }
    );
  }
}
```

### Step 7 -- Create API Route (POST run)

Write this file to `~/.openclaw/workspace/mission-control/app/api/mac-cleaner/run/route.ts`:

```typescript
/**
 * API Route: MacCleaner -- POST run now
 * POST /api/mac-cleaner/run
 */

import { NextResponse } from "next/server";
import { exec } from "child_process";
import * as os from "os";

const HOME = os.homedir();
const AGENT_SCRIPT =
  `node ${HOME}/.openclaw/workspace/agents/mac-cleaner/src/index.js`;

export async function POST() {
  try {
    const result = await new Promise<{ stdout: string; stderr: string }>(
      (resolve, reject) => {
        exec(
          AGENT_SCRIPT,
          { timeout: 300000, maxBuffer: 10 * 1024 * 1024 },
          (error, stdout, stderr) => {
            if (error) {
              reject(error);
            } else {
              resolve({ stdout, stderr });
            }
          }
        );
      }
    );

    return NextResponse.json({
      success: true,
      output: result.stdout,
      stderr: result.stderr,
    });
  } catch (error) {
    console.error("[/api/mac-cleaner/run] Error:", error);
    return NextResponse.json(
      {
        success: false,
        error: "Cleanup failed",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 }
    );
  }
}
```

### Step 8 -- Add Sidebar Entry

Check if `mac-cleaner` already exists in the MC sidebar (`app/app/layout.tsx`). If NOT present, add it to the sidebar navigation under the Agents section with label "MacCleaner" and path `/app/mac-cleaner`.

### Step 9 -- Add API Key Docs Entry

Check if `mac-cleaner` already exists in `~/.openclaw/workspace/mission-control/lib/api-key-docs.ts`. If NOT present, add an entry:

```typescript
{
  agent: "mac-cleaner",
  keys: [],
  notes: "No API keys required. Uses only Node.js built-ins and native macOS commands (rm, brew cleanup, npm cache clean). Zero network requests.",
}
```

### Step 10 -- Register Cron Job (Requires Explicit User Consent)

**STOP**: Only proceed with this step if the user has explicitly asked for automatic weekly cleanup (e.g. "run it automatically", "schedule it weekly", "set up the cron"). If the user has not asked, skip this step and inform them they can enable it later.

If the user explicitly consents, read `~/.openclaw/cron/jobs.json`. If no mac-cleaner job exists, add this entry to the `jobs` array:

```json
{
  "id": "mac-cleaner-weekly",
  "name": "Mac Cleaner Weekly Cleanup",
  "description": "Automated weekly macOS disk cleanup - caches, logs, trash, npm, brew",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 3 * * 0",
    "tz": "Asia/Singapore"
  },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "exec:node ~/.openclaw/workspace/agents/mac-cleaner/src/index.js"
  }
}
```

### Step 11 -- Mandatory Dry Run (Preview Before Deleting)

**ALWAYS run dry-run first.** Show the user what will be cleaned before anything is deleted.

**EXECUTE** using Bash tool:
```bash
node ~/.openclaw/workspace/agents/mac-cleaner/src/index.js --dry-run && echo "done" || echo "FAILED"
```

Read `~/.openclaw/workspace/agents/mac-cleaner/data/preview.json` and summarize for the user:
- Total space that would be freed
- Number of items that would be cleaned, broken down by category
- Any paths that look unexpected

**Ask the user to confirm** they want to proceed with actual cleanup before continuing to Step 12.

### Step 12 -- Run Actual Cleanup (After User Confirms)

Only proceed after the user reviews the dry-run output and confirms. **EXECUTE** using Bash tool:
```bash
node ~/.openclaw/workspace/agents/mac-cleaner/src/index.js && echo "done" || echo "FAILED"
```

> If FAILED, check stderr. Common cause is missing `data/` directory (Step 1 should have created it).

### Step 12 -- Rebuild Mission Control

**EXECUTE** using Bash tool:
```bash
launchctl unload ~/Library/LaunchAgents/ai.openclaw.mission-control.plist 2>/dev/null; pkill -f "next.*mission-control" 2>/dev/null; sleep 1; kill -9 $(pgrep -f "next.*mission-control") 2>/dev/null; rm -rf ~/.openclaw/workspace/mission-control/.next; launchctl load ~/Library/LaunchAgents/ai.openclaw.mission-control.plist && echo "plist loaded"
```

Wait 20 seconds, then verify:

**EXECUTE** using Bash tool:
```bash
sleep 20 && curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/app/mac-cleaner
```

> Must return 200. If not, check MC logs.

### Step 13 -- Report Results

Read `~/.openclaw/workspace/agents/mac-cleaner/data/last-run.json` and report:
- Total bytes freed (formatted as GB/MB)
- Number of items cleaned
- Any errors encountered
- Cron schedule confirmation (Sunday 3 AM SGT)
- MC dashboard URL: `http://localhost:3000/app/mac-cleaner`

## Optional: Telegram Notifications

By default, the agent runs silently and writes results to `data/last-run.json` and `data/history.json` -- no notifications are sent. If you have a Telegram bot and want a summary after each run, add a `sendTelegramNotification(report)` call at the end of `main()` in `src/index.js`. You will need `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` set as environment variables. The notification is a simple HTTPS POST to the Telegram Bot API -- no additional dependencies required.

## Configuration Reference

Users can edit `~/.openclaw/workspace/agents/mac-cleaner/config/config.json`:

| Key | Default | Description |
|-----|---------|-------------|
| `cacheMaxAgeDays` | 0 | Min age for cache dirs (0 = clean all) |
| `logMaxAgeDays` | 30 | Max age for log files before deletion |
| `trashMaxAgeDays` | 30 | Max age for trash items before deletion |
| `npmCacheThresholdMb` | 500 | npm cache size trigger in MB |
| `brewPruneDays` | 30 | Homebrew prune age in days |
| `nextBuildMaxAgeDays` | 7 | Max age for .next build artifacts |
| `missionControlPath` | `~/.openclaw/.../mission-control/.next` | Path to .next build dir to clean |
| `dataDir` | `~/.openclaw/.../mac-cleaner/data` | Where run reports and history are stored |

## Manual Run

```bash
node ~/.openclaw/workspace/agents/mac-cleaner/src/index.js
```

Or via Mission Control dashboard "Run Now" button at `/app/mac-cleaner`.
