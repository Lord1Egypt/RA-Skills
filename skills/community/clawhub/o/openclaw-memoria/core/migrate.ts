/**
 * Migration script: facts.json → memoria.db (SQLite)
 * 
 * Run: npx tsx migrate.ts
 */

import { MemoriaDB } from "./db.js";
import { readFileSync } from "fs";
import path from "path";

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || `${process.env.HOME}/.openclaw/workspace`;
const FACTS_JSON = path.join(WORKSPACE, "memory", "facts.json");

interface OldFact {
  _id: string;
  fact: string;
  category: string;
  agent: string;
  confidence: number;
  source?: string;
  tags?: string[];
  factHash?: string;
  keywordHash?: string;
  superseded?: boolean;
  supersededBy?: string;
  supersededAt?: number;
  accessCount?: number;
  lastAccessedAt?: number;
  createdAt: number;
  updatedAt: number;
}

async function main() {
  console.log("🧠 Memoria Migration: facts.json → memoria.db");
  
  const raw = readFileSync(FACTS_JSON, "utf-8");
  const oldFacts: OldFact[] = JSON.parse(raw);
  console.log(`  📦 Loaded ${oldFacts.length} facts from facts.json`);

  const db = new MemoriaDB(WORKSPACE);

  let imported = 0;
  let skipped = 0;

  for (const old of oldFacts) {
    try {
      db.storeFact({
        id: old._id || `migrated_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
        fact: old.fact,
        category: old.category,
        confidence: old.confidence,
        source: old.source || "convex-import",
        tags: JSON.stringify(old.tags || []),
        agent: old.agent || "koda",
        created_at: old.createdAt,
        updated_at: old.updatedAt,
        access_count: old.accessCount ?? 0,
        last_accessed_at: old.lastAccessedAt ?? null,
        superseded: old.superseded ? 1 : 0,
        fact_type: "semantic",
        superseded_by: old.supersededBy ?? null,
        superseded_at: old.supersededAt ?? null,
      } as any);
      imported++;
    } catch (err) {
      console.warn(`  ⚠ Skipped: ${String(err)}`);
      skipped++;
    }
  }

  const stats = db.stats();
  console.log(`  ✅ Imported: ${imported}, Skipped: ${skipped}`);
  console.log(`  📊 DB stats: ${stats.active} active, ${stats.superseded} superseded`);
  console.log(`  📁 Categories:`, stats.categories);

  db.close();
  console.log("  🧠 Migration complete!");
}

main().catch(console.error);
