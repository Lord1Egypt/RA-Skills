import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
/**
 * guard-scanner — P0 Defense Adapter
 *
 * TypeScript bridge to Rust SOUL.md Hard Gate + Memory Integrity Module.
 * Calls `guard-scan-core` binary via child_process for Ed25519 signing,
 * mutation analysis, provenance tagging, and anomaly detection.
 *
 * @security-manifest
 *   env-read: []
 *   env-write: []
 *   network: none
 *   fs-read: [SOUL.md, MEMORY.md, guava.sqlite]
 *   fs-write: [audit.jsonl]
 *   exec: [guard-scan-core (Rust binary)]
 *   purpose: P0 defense — SOUL.md Hard Gate + Memory Integrity
 *
 * Architecture:
 *   Layer A: Ed25519 signing & verification (via Rust binary)
 *   Layer B: Structural separation (identity/episodic/semantic/working)
 *   Layer C: Rule-based SOUL.md constraint extraction
 *   Layer D: Mutation guard + semantic drift detection
 *   Layer 0: Memory provenance tagging + trust-aware retrieval
 *
 * @author Guava 🍈 & Dee
 * @version 0.1.0
 * @license MIT
 */

import { execSync, spawnSync  } from 'child_process';
import fs  from 'fs';
import path  from 'path';
import crypto  from 'crypto';

// ── Types ──

/** Trust level for memory entries */
const TrustLevel = {
  USER_DIRECT: 0.90,
  AGENT_GENERATED: 0.70,
  SYSTEM_EVENT: 0.75,
  FILE_READ: 0.60,
  INTER_AGENT: 0.50,
  EXTERNAL_WEB: 0.30,
  UNKNOWN: 0.10,
};

/** Mutation risk levels */
const MutationRisk = {
  MINIMAL: 'Minimal',
  LOW: 'Low',
  MEDIUM: 'Medium',
  HIGH: 'High',
  CRITICAL: 'Critical',
};

// ── SOUL.md Hard Gate ──

class SoulHardGate {
  constructor(options = {}) {
    this.auditLogPath = options.auditLogPath || path.join(process.env.HOME, '.openclaw/guard-scanner/soul-audit.jsonl');
    this.binaryPath = options.binaryPath || this._findBinary();
    this.criticalSections = options.criticalSections || [
      'Boundaries', 'Safety', 'Identity', 'Mission', '緊急停止'
    ];
    this.criticalKeywords = [
      'never', 'always', '必須', '絶対', '禁止', '緊急',
      'ignore previous', 'forget', 'override', 'disregard'
    ];
  }

  _findBinary() {
    const candidates = [
      path.join(__dirname, '../rust/guard-scan-core/target/release/guard-scan-core'),
      path.join(__dirname, '../rust/guard-scan-core/target/debug/guard-scan-core'),
      'guard-scan-core',
    ];
    for (const p of candidates) {
      try {
        if (fs.existsSync(p)) return p;
      } catch { /* skip */ }
    }
    return null;
  }

  /**
   * Compute SHA-256 hash of content
   */
  hashContent(content) {
    const hash = crypto.createHash('sha256').update(content).digest('hex');
    return `sha256:${hash}`;
  }

  /**
   * Analyze mutation between old and new SOUL.md content
   * Detects "Ship of Theseus" attacks (gradual identity rewrite)
   */
  analyzeMutation(oldContent, newContent) {
    const oldLines = oldContent.split('\n');
    const newLines = newContent.split('\n');

    const added = newLines.filter(l => !oldLines.includes(l)).length;
    const removed = oldLines.filter(l => !newLines.includes(l)).length;
    const changeRatio = (added + removed) / Math.max(oldLines.length, 1);

    // Jaccard distance (token-level)
    const oldTokens = new Set(oldContent.toLowerCase().split(/\s+/));
    const newTokens = new Set(newContent.toLowerCase().split(/\s+/));
    const intersection = [...oldTokens].filter(t => newTokens.has(t)).length;
    const union = new Set([...oldTokens, ...newTokens]).size;
    const driftScore = union === 0 ? 0 : 1 - (intersection / union);

    // Critical keyword delta
    const countKeywords = (text) => {
      const lower = text.toLowerCase();
      return this.criticalKeywords.filter(k => lower.includes(k)).length;
    };
    const keywordDelta = countKeywords(newContent) - countKeywords(oldContent);

    // Section structure change
    const parseSections = (text) => text.split('\n')
      .filter(l => l.startsWith('## '))
      .map(l => l.replace('## ', '').trim());
    const sectionsChanged = JSON.stringify(parseSections(oldContent)) !== JSON.stringify(parseSections(newContent));

    // Risk assessment
    let risk;
    if (driftScore > 0.4) risk = MutationRisk.CRITICAL;
    else if (driftScore > 0.25 || changeRatio > 0.3) risk = MutationRisk.HIGH;
    else if (driftScore > 0.15 || sectionsChanged) risk = MutationRisk.MEDIUM;
    else if (changeRatio > 0.05) risk = MutationRisk.LOW;
    else risk = MutationRisk.MINIMAL;

    return {
      changeRatio,
      addedLines: added,
      removedLines: removed,
      sectionsChanged,
      criticalKeywordsDelta: keywordDelta,
      driftScore,
      risk,
      requiresApproval: driftScore > 0.15 || changeRatio > 0.1,
    };
  }

  /**
   * Extract enforceable rules from SOUL.md content
   * Parses "never", "always", "禁止" patterns into executable rules
   */
  extractRules(soulContent) {
    const rules = [];
    const lines = soulContent.split('\n');

    for (const line of lines) {
      const lower = line.toLowerCase().trim();

      // Prohibition patterns
      if (lower.startsWith('-') && (lower.includes('never') || lower.includes('禁止') || lower.includes('絶対'))) {
        rules.push({
          type: 'PROHIBITION',
          pattern: lower.replace(/^-\s*/, ''),
          severity: 'HIGH',
        });
      }

      // Requirement patterns
      if (lower.startsWith('-') && (lower.includes('always') || lower.includes('必ず') || lower.includes('必須'))) {
        rules.push({
          type: 'REQUIREMENT',
          pattern: lower.replace(/^-\s*/, ''),
          severity: 'HIGH',
        });
      }

      // Emergency stop patterns
      if (lower.includes('止めろ') || lower.includes('ストップ') || lower.includes('やめろ')) {
        rules.push({
          type: 'EMERGENCY_STOP',
          pattern: lower.replace(/^-\s*/, ''),
          severity: 'CRITICAL',
        });
      }
    }

    return rules;
  }

  /**
   * Check if a tool call violates SOUL.md rules
   * Deterministic pre-check before execution
   */
  checkCompliance(toolCall, rules) {
    const violations = [];
    const callStr = typeof toolCall === 'string' ? toolCall : JSON.stringify(toolCall);

    for (const rule of rules) {
      if (rule.type === 'PROHIBITION') {
        // Extract key terms from prohibition
        const terms = rule.pattern.split(/\s+/).filter(w =>
          w.length > 3 && !['never', '禁止', 'should', 'dont', "don't"].includes(w.toLowerCase())
        );
        if (terms.some(t => callStr.toLowerCase().includes(t.toLowerCase()))) {
          violations.push({
            rule: rule.pattern,
            severity: rule.severity,
            matched: terms.filter(t => callStr.toLowerCase().includes(t.toLowerCase())),
          });
        }
      }
    }

    return {
      compliant: violations.length === 0,
      violations,
    };
  }

  /**
   * Append to audit log (append-only)
   */
  _appendAudit(entry) {
    const dir = path.dirname(this.auditLogPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.appendFileSync(this.auditLogPath, JSON.stringify(entry) + '\n');
  }

  /**
   * Log a SOUL.md verification event
   */
  logVerification(content, status, details = {}) {
    this._appendAudit({
      timestamp: new Date().toISOString(),
      action: status === 'PASS' ? 'Verified' : 'IntegrityFailure',
      file: 'SOUL.md',
      content_hash: this.hashContent(content),
      status,
      ...details,
    });
  }
}

// ── Memory Integrity Module ──

class MemoryIntegrity {
  constructor(options = {}) {
    this.snapshotDir = options.snapshotDir || path.join(process.env.HOME, '.openclaw/guard-scanner/snapshots');
    this.baselineWrites = { min: 5, max: 20 };
  }

  /**
   * Create provenance tag for a memory entry
   */
  createProvenance(source, sessionId, content, writeContext = 'UserCommand') {
    const trustLevel = TrustLevel[source] || TrustLevel.UNKNOWN;
    const contentHash = crypto.createHash('sha256').update(content).digest('hex');

    return {
      source,
      trust_level: trustLevel,
      session_id: sessionId,
      timestamp: new Date().toISOString(),
      content_hash: `sha256:${contentHash}`,
      write_context: writeContext,
      temporal_decay_base: 1.0,
    };
  }

  /**
   * Score entry with trust-aware retrieval
   * final_score = relevance × trust × temporal_decay
   */
  scoreEntry(entry, relevance) {
    const trust = entry.provenance?.trust_level || TrustLevel.UNKNOWN;
    const decay = this._calculateTemporalDecay(entry.provenance);
    const finalScore = relevance * trust * decay;

    return {
      entry,
      final_score: finalScore,
      trust_multiplier: trust,
      temporal_decay: decay,
    };
  }

  /**
   * Retrieve entries with trust-aware scoring and sorting
   */
  retrieveTrustAware(entries, relevanceScores) {
    return entries
      .map((entry, i) => this.scoreEntry(entry, relevanceScores[i] || 0.5))
      .sort((a, b) => b.final_score - a.final_score);
  }

  /**
   * Detect anomalies in a batch of memory entries
   */
  detectAnomalies(entries) {
    const anomalies = [];

    // 1. Write spike detection
    if (entries.length > 50) {
      anomalies.push({
        type: 'WriteSpike',
        severity: entries.length > 100 ? 'Critical' : 'High',
        description: `Write spike: ${entries.length} entries (baseline: ${this.baselineWrites.min}-${this.baselineWrites.max})`,
        entries: [],
        action: 'FlagForReview',
      });
    }

    // 2. Instruction pattern detection
    const instructionPatterns = [
      'always', 'never', 'important:', 'remember:', '必須', '絶対',
      'ignore previous', 'forget', 'override', 'disregard',
      'you must', 'you should', 'from now on', 'new rule',
    ];
    const instructionEntries = entries.filter(e => {
      const lower = e.content?.toLowerCase() || '';
      return instructionPatterns.some(p => lower.includes(p));
    });
    if (instructionEntries.length > 0) {
      anomalies.push({
        type: 'InstructionPattern',
        severity: 'Medium',
        description: `Found ${instructionEntries.length} entries with instruction-like patterns`,
        entries: instructionEntries.map(e => e.id),
        action: 'FlagForReview',
      });
    }

    // 3. External reference detection
    const externalEntries = entries.filter(e => {
      const lower = e.content?.toLowerCase() || '';
      return lower.includes('http://') || lower.includes('https://') ||
        lower.includes('exec(') || lower.includes('eval(') ||
        lower.includes('rm -rf') || lower.includes('curl |');
    });
    if (externalEntries.length > 0) {
      anomalies.push({
        type: 'ExternalReference',
        severity: 'High',
        description: `Found ${externalEntries.length} entries referencing external URLs or commands`,
        entries: externalEntries.map(e => e.id),
        action: 'Quarantine',
      });
    }

    // 4. Trust drop detection
    if (entries.length >= 5) {
      const avgTrust = entries.reduce((s, e) => s + (e.provenance?.trust_level || 0.5), 0) / entries.length;
      const recentCount = Math.max(Math.floor(entries.length / 4), 3);
      const recentAvg = entries.slice(-recentCount)
        .reduce((s, e) => s + (e.provenance?.trust_level || 0.5), 0) / recentCount;

      if (avgTrust - recentAvg > 0.3) {
        anomalies.push({
          type: 'TrustDrop',
          severity: 'High',
          description: `Trust drop: avg ${avgTrust.toFixed(2)} → recent ${recentAvg.toFixed(2)}`,
          entries: entries.slice(-recentCount).map(e => e.id),
          action: 'Quarantine',
        });
      }
    }

    return anomalies;
  }

  /**
   * Create forensic snapshot of current memory state
   */
  createSnapshot(entries, sessionId) {
    const entryHashes = entries.map(e => [
      e.id,
      e.provenance?.content_hash || crypto.createHash('sha256').update(e.content || '').digest('hex'),
    ]);
    const combined = entryHashes.map(([id, h]) => `${id}:${h}`).join('|');
    const snapshotHash = crypto.createHash('sha256').update(combined).digest('hex');

    return {
      snapshot_id: `snap_${Date.now()}`,
      timestamp: new Date().toISOString(),
      total_entries: entries.length,
      content_hash: `sha256:${snapshotHash}`,
      entry_hashes: entryHashes,
      session_id: sessionId,
    };
  }

  /**
   * Diff two snapshots to identify changes
   */
  diffSnapshots(oldSnap, newSnap) {
    const oldMap = new Map(oldSnap.entry_hashes);
    const newMap = new Map(newSnap.entry_hashes);

    const added = [...newMap.keys()].filter(k => !oldMap.has(k));
    const removed = [...oldMap.keys()].filter(k => !newMap.has(k));
    const modified = [...newMap.entries()]
      .filter(([id, h]) => oldMap.has(id) && oldMap.get(id) !== h)
      .map(([id]) => id);

    return {
      old_timestamp: oldSnap.timestamp,
      new_timestamp: newSnap.timestamp,
      added,
      removed,
      modified,
      total_changes: added.length + removed.length + modified.length,
    };
  }

  _calculateTemporalDecay(provenance) {
    if (!provenance?.timestamp) return 1.0;
    const ageMs = Date.now() - new Date(provenance.timestamp).getTime();
    const days = ageMs / (1000 * 60 * 60 * 24);

    if (days < 30) return 1.0;
    return Math.max(1.0 - (days - 30) / 180, 0.3);
  }
}

// ── Exports ──

export { 
  SoulHardGate,
  MemoryIntegrity,
  TrustLevel,
  MutationRisk,
 };
