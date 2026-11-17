/**
 * Memoria — Layer 11a: .md Sync
 * 
 * DB → .md: When Memoria captures a fact, it appends to the right workspace .md file
 * Category mapping: savoir/erreur → MEMORY.md, outil → TOOLS.md, preference → USER.md, rh/client → COMPANY.md
 * 
 * Each fact is appended with format: `- **[date]** fact text _(confidence%)_`
 * Sets synced_to_md = 1 after successful write.
 * 
 * Mapping catégorie → fichier :
 *   outil     → TOOLS.md
 *   savoir    → MEMORY.md (section 🧠 Savoir)
 *   erreur    → MEMORY.md (section ❌ Erreurs)
 *   chronologie → MEMORY.md (section 📅 Chronologie)
 *   preference → USER.md
 *   client    → COMPANY.md
 *   rh        → COMPANY.md
 */

import { readFileSync, writeFileSync, existsSync, statSync } from "node:fs";
import { join } from "node:path";
import type { MemoriaDB, Fact } from "./db.js";

// ─── Config ───

export interface SyncConfig {
  /** Workspace root. Default ~/.openclaw/workspace */
  workspacePath: string;
  /** Enable DB→MD sync. Default true */
  dbToMd: boolean;
  /** Enable MD→DB sync. Default false (safety: avoid importing noise) */
  mdToDb: boolean;
  /** Max facts to sync per run. Default 10 */
  batchSize: number;
}

export const DEFAULT_SYNC_CONFIG: SyncConfig = {
  workspacePath: process.env.HOME + "/.openclaw/workspace",
  dbToMd: true,
  mdToDb: false,
  batchSize: 10,
};

// ─── Category → File mapping ───

interface FileMapping {
  file: string;
  section?: string;      // Section header to find/create
  format: "bullet" | "entry";
}

const CATEGORY_MAP: Record<string, FileMapping> = {
  outil: { file: "TOOLS.md", format: "bullet" },
  savoir: { file: "MEMORY.md", section: "## 🧠 Savoir", format: "bullet" },
  erreur: { file: "MEMORY.md", section: "## ❌ Erreurs", format: "bullet" },
  chronologie: { file: "MEMORY.md", section: "## 📅 Chronologie", format: "entry" },
  preference: { file: "USER.md", format: "bullet" },
  client: { file: "COMPANY.md", format: "bullet" },
  rh: { file: "COMPANY.md", format: "bullet" },
};

// ─── Sync Manager ───

export class MdSync {
  private db: MemoriaDB;
  private cfg: SyncConfig;
  private lastSyncTimestamps: Map<string, number> = new Map();

  constructor(db: MemoriaDB, config?: Partial<SyncConfig>) {
    this.db = db;
    this.cfg = { ...DEFAULT_SYNC_CONFIG, ...config };
  }

  // ─── DB → MD: Write new facts to .md files ───

  /**
   * Sync recent facts from DB to their corresponding .md files.
   * Only syncs facts that haven't been synced yet (tracked via `synced_to_md` flag).
   */
  syncToMd(db: MemoriaDB): { synced: number; errors: string[] } {
    if (!this.cfg.dbToMd) return { synced: 0, errors: [] };

    // Get unsynced facts
    const unsynced = db.raw.prepare(
      "SELECT * FROM facts WHERE superseded = 0 AND (synced_to_md IS NULL OR synced_to_md = 0) ORDER BY created_at DESC LIMIT ?"
    ).all(this.cfg.batchSize) as (Fact & { synced_to_md?: number })[];

    if (unsynced.length === 0) return { synced: 0, errors: [] };

    let synced = 0;
    const errors: string[] = [];

    for (const fact of unsynced) {
      try {
        const mapping = CATEGORY_MAP[fact.category];
        if (!mapping) {
          // Mark as synced anyway to avoid retrying
          this.markSynced(db, fact.id);
          continue;
        }

        const filePath = join(this.cfg.workspacePath, mapping.file);
        
        // Check if fact already exists in file (dedup)
        if (this.factExistsInFile(filePath, fact.fact)) {
          this.markSynced(db, fact.id);
          continue;
        }

        // Append to file
        this.appendToFile(filePath, fact, mapping);
        this.markSynced(db, fact.id);
        synced++;
      } catch (err) {
        errors.push(`${fact.id}: ${err}`);
      }
    }

    return { synced, errors };
  }

  // ─── MD → DB: Import new content from .md files ───

  /**
   * Check if .md files were modified and import new lines as facts.
   * Conservative: only imports clearly new bullet points.
   */
  syncFromMd(db: MemoriaDB): { imported: number; files: string[] } {
    if (!this.cfg.mdToDb) return { imported: 0, files: [] };

    let imported = 0;
    const files: string[] = [];

    for (const [category, mapping] of Object.entries(CATEGORY_MAP)) {
      const filePath = join(this.cfg.workspacePath, mapping.file);
      if (!existsSync(filePath)) continue;

      const stat = statSync(filePath);
      const lastMod = stat.mtimeMs;
      const lastSync = this.lastSyncTimestamps.get(filePath) || 0;

      if (lastMod <= lastSync) continue;

      // File was modified — extract new bullet points
      const content = readFileSync(filePath, "utf-8");
      const newFacts = this.extractNewFacts(db, content, category, mapping);

      for (const factText of newFacts) {
        try {
          db.storeFact({
            fact: factText,
            category,
            confidence: 0.7,
            source: "md-sync",
            agent: "koda",
          } as any);
          imported++;
        } catch (_e) { /* dedup or error */ }
      }

      if (newFacts.length > 0) files.push(mapping.file);
      this.lastSyncTimestamps.set(filePath, Date.now());
    }

    return { imported, files };
  }

  // ─── Ensure synced_to_md column exists ───

  ensureSchema(db: MemoriaDB): void {
    try {
      // Check if column exists
      const info = db.raw.prepare("PRAGMA table_info(facts)").all() as Array<{ name: string }>;
      const hasColumn = info.some(col => col.name === "synced_to_md");
      if (!hasColumn) {
        db.raw.prepare("ALTER TABLE facts ADD COLUMN synced_to_md INTEGER DEFAULT 0").run();
      }
    } catch (_e) { /* column might already exist */ }
  }

  // ─── Private ───

  private markSynced(db: MemoriaDB, factId: string): void {
    db.raw.prepare("UPDATE facts SET synced_to_md = 1 WHERE id = ?").run(factId);
  }

  private factExistsInFile(filePath: string, factText: string): boolean {
    if (!existsSync(filePath)) return false;
    const content = readFileSync(filePath, "utf-8");
    // Check if first 60 chars of the fact appear in the file
    const snippet = factText.slice(0, 60).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return new RegExp(snippet, "i").test(content);
  }

  private appendToFile(filePath: string, fact: Fact, mapping: FileMapping): void {
    if (!existsSync(filePath)) return; // Don't create files

    let content = readFileSync(filePath, "utf-8");

    const line = mapping.format === "entry"
      ? `- **${this.formatDate()}** : ${fact.fact}`
      : `- ${fact.fact}`;

    if (mapping.section) {
      // Find section and append after it
      const sectionIdx = content.indexOf(mapping.section);
      if (sectionIdx !== -1) {
        // Find the next section or end of file
        const afterSection = content.indexOf("\n## ", sectionIdx + mapping.section.length);
        const insertAt = afterSection !== -1 ? afterSection : content.length;

        // Find last non-empty line before insertAt
        const beforeInsert = content.slice(sectionIdx, insertAt);
        const lastNewline = beforeInsert.lastIndexOf("\n");
        const insertPos = sectionIdx + lastNewline + 1;

        content = content.slice(0, insertPos) + line + "\n" + content.slice(insertPos);
      } else {
        // Section doesn't exist — append at end
        content += `\n\n${mapping.section}\n\n${line}\n`;
      }
    } else {
      // Append at end of file
      content = content.trimEnd() + "\n" + line + "\n";
    }

    writeFileSync(filePath, content, "utf-8");
  }

  private extractNewFacts(db: MemoriaDB, content: string, category: string, mapping: FileMapping): string[] {
    const lines = content.split("\n");
    const newFacts: string[] = [];

    for (const line of lines) {
      // Only process bullet points
      const match = line.match(/^[-*]\s+(.+)$/);
      if (!match) continue;

      const text = match[1].trim();
      if (text.length < 15) continue; // Skip short lines

      // Clean markdown formatting
      const cleaned = text.replace(/\*\*([^*]+)\*\*/g, "$1").replace(/`([^`]+)`/g, "$1");

      // Check if already in DB (approximate: search by first 50 chars)
      const existing = db.raw.prepare(
        "SELECT id FROM facts WHERE fact LIKE ? AND superseded = 0 LIMIT 1"
      ).get(`${cleaned.slice(0, 50)}%`) as { id: string } | undefined;

      if (!existing) {
        newFacts.push(cleaned);
      }
    }

    return newFacts.slice(0, this.cfg.batchSize);
  }

  private formatDate(): string {
    const d = new Date();
    return `${d.getDate().toString().padStart(2, "0")}/${(d.getMonth() + 1).toString().padStart(2, "0")}`;
  }
}
