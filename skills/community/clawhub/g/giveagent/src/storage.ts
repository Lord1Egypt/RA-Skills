import fs from "fs/promises";
import os from "os";
import path from "path";
import { UserConfig, WantListItem, InventoryItem, MatchState } from "./types.js";

// ============================================
// Public interfaces
// ============================================

export interface ActiveMatch {
  id: string;
  apiMatchId?: string;
  wantItemId: string;
  givingPostId: string;
  counterpartAgentId: string;
  state: MatchState;
  role: "giver" | "claimer";
  item: string;
  postId: string;
  area?: string;
  available?: string;
  pickupDetails?: {
    address: string;
    date: string;
    time: string;
    contact?: string;
    notes?: string;
  };
  createdAt: Date;
  updatedAt: Date;
  expiresAt: Date;
}

export interface StorageStats {
  totalGiven: number;
  totalReceived: number;
  totalMatches: number;
  totalExpired: number;
}

export interface StorageManager {
  // Config
  getConfig(): Promise<UserConfig>;
  saveConfig(config: Partial<UserConfig>): Promise<void>;

  // Inventory (giving items)
  getInventory(): Promise<InventoryItem[]>;
  addInventoryItem(item: InventoryItem): Promise<void>;
  updateInventoryItem(id: string, updates: Partial<InventoryItem>): Promise<void>;
  removeInventoryItem(id: string): Promise<void>;

  // Want list
  getWantList(): Promise<WantListItem[]>;
  addWantItem(item: WantListItem): Promise<void>;
  updateWantItem(id: string, updates: Partial<WantListItem>): Promise<void>;
  removeWantItem(id: string): Promise<void>;

  // Active matches
  getMatches(): Promise<ActiveMatch[]>;
  addMatch(match: ActiveMatch): Promise<void>;
  updateMatchState(matchId: string, state: MatchState): Promise<void>;
  updateMatch(matchId: string, updates: Partial<ActiveMatch>): Promise<void>;

  // Seen posts (for browse dedup)
  getSeenPostIds(): Promise<Set<string>>;
  markPostSeen(postId: string): Promise<void>;

  // Stats
  getStats(): Promise<StorageStats>;
  incrementStat(key: keyof StorageStats): Promise<void>;
}

// ============================================
// Defaults
// ============================================

const DEFAULT_CONFIG: UserConfig = {
  giveagentApiKey: "",
  giveagentApiUrl: "https://api.giveagent.ai",
  agentId: "",
  defaultLocation: { city: "", country: "", postalPrefix: "" },
  defaultPickup: "Flexible",
  autoScan: true,
  scanIntervalMs: 4 * 60 * 60 * 1000, // 4 hours
  maxActiveWants: 10,
  maxActiveGivings: 20,
  autoClaimEnabled: false,
};

const DEFAULT_STATS: StorageStats = {
  totalGiven: 0,
  totalReceived: 0,
  totalMatches: 0,
  totalExpired: 0,
};

// ============================================
// Date-aware JSON serialization
// ============================================

// ISO 8601 date string pattern
const ISO_DATE_RE = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/;

function reviver(_key: string, value: unknown): unknown {
  if (typeof value === "string" && ISO_DATE_RE.test(value)) {
    return new Date(value);
  }
  return value;
}

function serialize(data: unknown): string {
  return JSON.stringify(data, null, 2);
}

function deserialize<T>(text: string): T {
  return JSON.parse(text, reviver) as T;
}

// ============================================
// File locking helpers
// ============================================

const LOCK_TIMEOUT_MS = 5000; // 5 seconds max wait for lock
const LOCK_RETRY_DELAY_MS = 50; // Check every 50ms

/**
 * Simple file-based locking to prevent race conditions.
 * Uses exclusive file creation (wx flag) for atomic lock acquisition.
 */
async function acquireLock(lockPath: string): Promise<() => Promise<void>> {
  const startTime = Date.now();

  while (true) {
    try {
      // Try to create lock file exclusively (atomic operation)
      await fs.writeFile(lockPath, String(process.pid), { flag: "wx" });

      // Lock acquired - return cleanup function
      return async () => {
        try {
          await fs.unlink(lockPath);
        } catch {
          // Lock file might already be deleted - ignore
        }
      };
    } catch (err: unknown) {
      // Lock file exists - wait and retry
      if (Date.now() - startTime > LOCK_TIMEOUT_MS) {
        throw new Error(`Failed to acquire lock ${lockPath} after ${LOCK_TIMEOUT_MS}ms`);
      }

      // Wait before retry
      await new Promise(resolve => setTimeout(resolve, LOCK_RETRY_DELAY_MS));
    }
  }
}

/**
 * Execute a function with file locking.
 */
async function withLock<T>(lockPath: string, fn: () => Promise<T>): Promise<T> {
  const releaseLock = await acquireLock(lockPath);
  try {
    return await fn();
  } finally {
    await releaseLock();
  }
}

// ============================================
// Low-level file helpers
// ============================================

async function ensureDir(dirPath: string): Promise<void> {
  await fs.mkdir(dirPath, { recursive: true });
}

/**
 * Atomic write: write to a temp file in the same directory, then rename.
 * Rename is atomic on the same filesystem, so readers never see a partial file.
 */
async function atomicWrite(filePath: string, content: string): Promise<void> {
  const dir = path.dirname(filePath);
  const tmp = path.join(dir, `.tmp-${path.basename(filePath)}-${process.pid}-${Date.now()}`);
  await fs.writeFile(tmp, content, "utf8");
  await fs.rename(tmp, filePath);
}

/**
 * Read and parse a JSON file. Returns `defaultValue` if the file is missing
 * or contains corrupt JSON, logging a warning in the corrupt case.
 */
async function readJson<T>(filePath: string, defaultValue: T): Promise<T> {
  let text: string;
  try {
    text = await fs.readFile(filePath, "utf8");
  } catch (err: unknown) {
    if (isNodeError(err) && err.code === "ENOENT") {
      return defaultValue;
    }
    throw err;
  }

  try {
    return deserialize<T>(text);
  } catch {
    console.warn(`[storage] Corrupt JSON in ${filePath} — returning defaults`);
    return defaultValue;
  }
}

async function writeJson(filePath: string, data: unknown): Promise<void> {
  await atomicWrite(filePath, serialize(data));
}

function isNodeError(err: unknown): err is NodeJS.ErrnoException {
  return typeof err === "object" && err !== null && "code" in err;
}

// ============================================
// Factory
// ============================================

export function createStorage(basePath?: string): StorageManager {
  const baseDir = basePath ?? path.join(os.homedir(), ".giveagent");

  const configFile     = () => path.join(baseDir, "config.json");
  const inventoryFile  = () => path.join(baseDir, "inventory.json");
  const wantlistFile   = () => path.join(baseDir, "wantlist.json");
  const matchesFile    = () => path.join(baseDir, "matches.json");
  const seenPostsFile  = () => path.join(baseDir, "seen-posts.json");
  const statsFile      = () => path.join(baseDir, "stats.json");

  // Lock files for each data file
  const inventoryLock  = () => path.join(baseDir, ".inventory.lock");
  const wantlistLock   = () => path.join(baseDir, ".wantlist.lock");
  const matchesLock    = () => path.join(baseDir, ".matches.lock");
  const seenPostsLock  = () => path.join(baseDir, ".seen-posts.lock");
  const statsLock      = () => path.join(baseDir, ".stats.lock");

  async function init(): Promise<void> {
    await ensureDir(baseDir);
  }

  // ---- Config ----

  async function getConfig(): Promise<UserConfig> {
    await init();
    return readJson<UserConfig>(configFile(), DEFAULT_CONFIG);
  }

  async function saveConfig(updates: Partial<UserConfig>): Promise<void> {
    await init();
    const current = await getConfig();
    const merged = { ...current, ...updates };
    await writeJson(configFile(), merged);
  }

  // ---- Inventory ----

  async function getInventory(): Promise<InventoryItem[]> {
    await init();
    return readJson<InventoryItem[]>(inventoryFile(), []);
  }

  async function addInventoryItem(item: InventoryItem): Promise<void> {
    await init();
    await withLock(inventoryLock(), async () => {
      const items = await getInventory();
      items.push(item);
      await writeJson(inventoryFile(), items);
    });
  }

  async function updateInventoryItem(id: string, updates: Partial<InventoryItem>): Promise<void> {
    await init();
    await withLock(inventoryLock(), async () => {
      const items = await getInventory();
      const idx = items.findIndex((i) => i.id === id);
      if (idx === -1) return;
      items[idx] = { ...items[idx], ...updates };
      await writeJson(inventoryFile(), items);
    });
  }

  async function removeInventoryItem(id: string): Promise<void> {
    await init();
    await withLock(inventoryLock(), async () => {
      const items = await getInventory();
      await writeJson(inventoryFile(), items.filter((i) => i.id !== id));
    });
  }

  // ---- Want list ----

  async function getWantList(): Promise<WantListItem[]> {
    await init();
    return readJson<WantListItem[]>(wantlistFile(), []);
  }

  async function addWantItem(item: WantListItem): Promise<void> {
    await init();
    await withLock(wantlistLock(), async () => {
      const items = await getWantList();
      items.push(item);
      await writeJson(wantlistFile(), items);
    });
  }

  async function updateWantItem(id: string, updates: Partial<WantListItem>): Promise<void> {
    await init();
    await withLock(wantlistLock(), async () => {
      const items = await getWantList();
      const idx = items.findIndex((i) => i.id === id);
      if (idx === -1) return;
      items[idx] = { ...items[idx], ...updates };
      await writeJson(wantlistFile(), items);
    });
  }

  async function removeWantItem(id: string): Promise<void> {
    await init();
    await withLock(wantlistLock(), async () => {
      const items = await getWantList();
      await writeJson(wantlistFile(), items.filter((i) => i.id !== id));
    });
  }

  // ---- Matches ----

  async function getMatches(): Promise<ActiveMatch[]> {
    await init();
    return readJson<ActiveMatch[]>(matchesFile(), []);
  }

  async function addMatch(match: ActiveMatch): Promise<void> {
    await init();
    await withLock(matchesLock(), async () => {
      const matches = await getMatches();
      matches.push(match);
      await writeJson(matchesFile(), matches);
    });
  }

  async function updateMatchState(matchId: string, state: MatchState): Promise<void> {
    await init();
    await withLock(matchesLock(), async () => {
      const matches = await getMatches();
      const idx = matches.findIndex((m) => m.id === matchId);
      if (idx === -1) return;
      matches[idx] = { ...matches[idx], state, updatedAt: new Date() };
      await writeJson(matchesFile(), matches);
    });
  }

  async function updateMatch(matchId: string, updates: Partial<ActiveMatch>): Promise<void> {
    await init();
    await withLock(matchesLock(), async () => {
      const matches = await getMatches();
      const idx = matches.findIndex((m) => m.id === matchId);
      if (idx === -1) return;
      matches[idx] = { ...matches[idx], ...updates, updatedAt: new Date() };
      await writeJson(matchesFile(), matches);
    });
  }

  // ---- Seen posts ----

  async function getSeenPostIds(): Promise<Set<string>> {
    await init();
    const arr = await readJson<string[]>(seenPostsFile(), []);
    return new Set(arr);
  }

  async function markPostSeen(postId: string): Promise<void> {
    await init();
    await withLock(seenPostsLock(), async () => {
      const seen = await getSeenPostIds();
      seen.add(postId);
      await writeJson(seenPostsFile(), Array.from(seen));
    });
  }

  // ---- Stats ----

  async function getStats(): Promise<StorageStats> {
    await init();
    return readJson<StorageStats>(statsFile(), { ...DEFAULT_STATS });
  }

  async function incrementStat(key: keyof StorageStats): Promise<void> {
    await init();
    await withLock(statsLock(), async () => {
      const stats = await getStats();
      stats[key] += 1;
      await writeJson(statsFile(), stats);
    });
  }

  return {
    getConfig,
    saveConfig,
    getInventory,
    addInventoryItem,
    updateInventoryItem,
    removeInventoryItem,
    getWantList,
    addWantItem,
    updateWantItem,
    removeWantItem,
    getMatches,
    addMatch,
    updateMatchState,
    updateMatch,
    getSeenPostIds,
    markPostSeen,
    getStats,
    incrementStat,
  };
}
