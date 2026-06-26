import { fetchEtaDb, fetchEtas } from "hk-bus-eta";
import type { EtaDb, Company } from "hk-bus-eta";
import { readFile, writeFile, mkdir, stat } from "node:fs/promises";
import { join } from "node:path";
import { homedir } from "node:os";

const CACHE_DIR = join(homedir(), ".cache", "hk-route");
const CACHE_FILE = join(CACHE_DIR, "etaDb.json");
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

/** Operators where real-time ETA is skipped (high frequency makes it unnecessary) */
const SKIP_ETA_OPERATORS = new Set<string>(["mtr"]);

export interface EtaResult {
  /** ISO 8601 timestamp of the predicted arrival */
  eta: string;
  /** Minutes from now until arrival, rounded */
  minutes_from_now: number;
}

/**
 * Load the hk-bus-eta database, using a local file cache with 24h TTL.
 * Downloads fresh data on first call or when cache is stale.
 */
export async function loadEtaDb(): Promise<EtaDb> {
  try {
    const stats = await stat(CACHE_FILE);
    const ageMs = Date.now() - stats.mtimeMs;
    if (ageMs < CACHE_TTL_MS) {
      const raw = await readFile(CACHE_FILE, "utf-8");
      return JSON.parse(raw) as EtaDb;
    }
  } catch {
    // Cache missing or unreadable — will fetch fresh
  }

  const db = await fetchEtaDb();
  await mkdir(CACHE_DIR, { recursive: true });
  await writeFile(CACHE_FILE, JSON.stringify(db));
  return db;
}

/**
 * Fetch real-time ETAs for a given operator, route, and stop.
 *
 * Returns up to 2 next arrivals with ISO timestamps and minutes-from-now.
 * Returns `null` for MTR/subway (skipped by design, not an error).
 * Returns `[]` when ETA data is unavailable (late night, no service, etc.).
 */
export async function getRealtimeEta(
  etaDb: EtaDb,
  operator: string,
  routeNumber: string,
  stopId: string,
): Promise<EtaResult[] | null> {
  if (SKIP_ETA_OPERATORS.has(operator)) {
    return null;
  }

  // Find route entries matching this operator + route number
  // Route keys follow: "{route}+{seq}+{origin_en}+{dest_en}"
  const matchingKeys = Object.keys(etaDb.routeList).filter((key) => {
    const entry = etaDb.routeList[key];
    return (
      entry.route === routeNumber &&
      entry.co.includes(operator as Company)
    );
  });

  if (matchingKeys.length === 0) {
    return [];
  }

  // Try each matching route variant to find one containing this stop
  for (const key of matchingKeys) {
    const routeEntry = etaDb.routeList[key];
    const stops = routeEntry.stops[operator as Company];
    if (!stops) continue;

    const stopIdx = stops.indexOf(stopId);
    if (stopIdx === -1) continue;

    try {
      const etas = await fetchEtas({
        ...routeEntry,
        seq: stopIdx,
        language: "en",
        stopList: etaDb.stopList,
        holidays: etaDb.holidays,
        serviceDayMap: etaDb.serviceDayMap,
      });

      const now = Date.now();
      return etas
        .filter((e) => e.eta && new Date(e.eta).getTime() > now)
        .slice(0, 2)
        .map((e) => ({
          eta: e.eta,
          minutes_from_now: Math.round(
            (new Date(e.eta).getTime() - now) / 60000,
          ),
        }));
    } catch {
      return [];
    }
  }

  // Stop not found on any variant of this route
  return [];
}
