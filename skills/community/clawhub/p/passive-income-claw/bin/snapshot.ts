#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import {
  SNAPSHOT_PATH, ensureDir, utcTimestamp, diffSnapshots, parseSnapshotContent,
  parseArgs, die, out, main,
} from "./lib.ts";
import type { SnapshotProduct, SnapshotData } from "./lib.ts";

function parseSnapshot(path: string): SnapshotProduct[] {
  if (!existsSync(path)) return [];
  return parseSnapshotContent(readFileSync(path, "utf-8"));
}

function getUpdatedAt(path: string): string {
  if (!existsSync(path)) return "";
  const content = readFileSync(path, "utf-8");
  const m = content.match(/^updated_at:\s*(.+)/m);
  return m ? m[1].trim() : "";
}

const commands: Record<string, (args: Record<string, string | true>) => void> = {
  diff: (args) => {
    const threshold = typeof args.threshold === "string" ? parseFloat(args.threshold) : 0.5;
    const oldProducts = parseSnapshot(SNAPSHOT_PATH);

    let input = "";
    try { input = readFileSync(0, "utf-8"); } catch { die("No data on stdin. Pipe JSON array of products."); }

    let newProducts: SnapshotProduct[];
    try { newProducts = JSON.parse(input); } catch { die("Invalid JSON on stdin"); }

    out(diffSnapshots(oldProducts, newProducts, threshold));
  },

  update: () => {
    let input = "";
    try { input = readFileSync(0, "utf-8"); } catch { die("No data on stdin"); }

    let products: SnapshotProduct[];
    try { products = JSON.parse(input); } catch { die("Invalid JSON on stdin"); }

    const ts = utcTimestamp();
    const lines = [`# Opportunity Snapshot`, `updated_at: ${ts}`, ""];
    for (const p of products) {
      lines.push(
        `## ${p.name}`, `type: ${p.type || "flexible"}`, `apy: ${p.apy}%`,
        `risk: ${p.risk || "low"}`, `liquidity: ${p.liquidity || "flexible"}`,
        `asset: ${p.asset || ""}`, `productId: ${p.productId || ""}`,
        `projectId: ${p.projectId || ""}`, `minPurchaseAmount: ${p.minPurchaseAmount || ""}`,
        `status: pushed`, ""
      );
    }
    ensureDir(SNAPSHOT_PATH);
    writeFileSync(SNAPSHOT_PATH, lines.join("\n"));
    out({ updated: true, timestamp: ts, count: products.length });
  },

  read: () => {
    out({ updated_at: getUpdatedAt(SNAPSHOT_PATH), products: parseSnapshot(SNAPSHOT_PATH) } satisfies SnapshotData);
  },
};

main(() => {
  const [cmd, ...rest] = process.argv.slice(2);
  if (!cmd || !commands[cmd]) die("Usage: snapshot.ts <diff|update|read> [options]");
  commands[cmd](parseArgs(rest));
});
