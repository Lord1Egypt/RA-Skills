import fs from 'node:fs/promises';
import path from 'node:path';
import { ManagerSettings, defaultStateRoot } from '../types';

export class FsStore {
  readonly rootDir: string;

  constructor(rootDir = defaultStateRoot()) {
    this.rootDir = rootDir;
  }

  get sessionsDir() {
    return path.join(this.rootDir, 'sessions');
  }

  get indexesDir() {
    return path.join(this.rootDir, 'indexes');
  }

  get connectorsDir() {
    return path.join(this.rootDir, 'connectors');
  }

  get connectorInboxDir() {
    return path.join(this.connectorsDir, 'inbox');
  }

  connectorInboxFile(connectorName: string) {
    return path.join(this.connectorInboxDir, `${connectorName}.jsonl`);
  }

  get connectorConfigsFile() {
    return path.join(this.connectorsDir, 'configs.json');
  }

  get snapshotsDir() {
    return path.join(this.rootDir, 'snapshots');
  }

  get exportsDir() {
    return path.join(this.rootDir, 'exports');
  }

  get settingsFile() {
    return path.join(this.rootDir, 'settings.json');
  }

  get capabilityFactsFile() {
    return path.join(this.indexesDir, 'capability_facts.jsonl');
  }

  get threadShadowsFile() {
    return path.join(this.indexesDir, 'thread_shadows.json');
  }

  get promotionQueueFile() {
    return path.join(this.indexesDir, 'promotion_queue.json');
  }

  sessionDir(sessionId: string) {
    return path.join(this.sessionsDir, sessionId);
  }

  runsDir(sessionId: string) {
    return path.join(this.sessionDir(sessionId), 'runs');
  }

  runDir(sessionId: string, runId: string) {
    return path.join(this.runsDir(sessionId), runId);
  }

  sessionFile(sessionId: string) {
    return path.join(this.sessionDir(sessionId), 'session.json');
  }

  summaryFile(sessionId: string) {
    return path.join(this.sessionDir(sessionId), 'summary.md');
  }

  attentionFile(sessionId: string) {
    return path.join(this.sessionDir(sessionId), 'attention.json');
  }

  shareDir(sessionId: string) {
    return path.join(this.sessionDir(sessionId), 'share');
  }

  artifactsDir(sessionId: string) {
    return path.join(this.sessionDir(sessionId), 'artifacts');
  }

  runFile(sessionId: string, runId: string) {
    return path.join(this.runDir(sessionId, runId), 'run.json');
  }

  eventsFile(sessionId: string, runId: string) {
    return path.join(this.runDir(sessionId, runId), 'events.jsonl');
  }

  spoolFile(sessionId: string, runId: string) {
    return path.join(this.runDir(sessionId, runId), 'spool.jsonl');
  }

  checkpointFile(sessionId: string, runId: string) {
    return path.join(this.runDir(sessionId, runId), 'checkpoint.json');
  }

  skillTracesFile(sessionId: string, runId: string) {
    return path.join(this.runDir(sessionId, runId), 'skill_traces.jsonl');
  }

  snapshotDir(snapshotId: string) {
    return path.join(this.snapshotsDir, snapshotId);
  }

  async ensureLayout() {
    const required = [
      this.sessionsDir,
      this.indexesDir,
      this.connectorsDir,
      this.connectorInboxDir,
      this.snapshotsDir,
      this.exportsDir,
    ];

    for (const dir of required) {
      await fs.mkdir(dir, { recursive: true });
    }

    await this.writeJsonIfMissing(path.join(this.indexesDir, 'sessions.json'), []);
    await this.writeJsonIfMissing(path.join(this.indexesDir, 'active_sessions.json'), []);
    await this.writeJsonIfMissing(path.join(this.indexesDir, 'attention_queue.json'), []);
    await this.writeJsonIfMissing(this.threadShadowsFile, []);
    await this.writeJsonIfMissing(this.promotionQueueFile, []);
    await this.writeJsonIfMissing(path.join(this.connectorsDir, 'bindings.json'), []);
    await this.writeJsonIfMissing(this.connectorConfigsFile, []);
    await this.writeJsonIfMissing(this.settingsFile, {
      sidecar_autostart_consent: false,
      consent_recorded_at: null,
      consent_source: 'default',
    } satisfies ManagerSettings);
    await this.writeTextIfMissing(this.capabilityFactsFile, '');
  }

  async ensureSessionLayout(sessionId: string, runId?: string) {
    await fs.mkdir(this.sessionDir(sessionId), { recursive: true });
    await fs.mkdir(this.shareDir(sessionId), { recursive: true });
    await fs.mkdir(this.artifactsDir(sessionId), { recursive: true });
    await fs.mkdir(this.runsDir(sessionId), { recursive: true });
    if (runId) {
      await fs.mkdir(this.runDir(sessionId, runId), { recursive: true });
    }
  }

  async exists(filePath: string) {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }

  async readJson<T>(filePath: string, fallback: T): Promise<T> {
    if (!(await this.exists(filePath))) {
      return fallback;
    }
    const text = await fs.readFile(filePath, 'utf8');
    return JSON.parse(text) as T;
  }

  async writeJson(filePath: string, value: unknown) {
    await fs.mkdir(path.dirname(filePath), { recursive: true });
    await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
  }

  async writeJsonIfMissing(filePath: string, value: unknown) {
    if (!(await this.exists(filePath))) {
      await this.writeJson(filePath, value);
    }
  }

  async writeText(filePath: string, text: string) {
    await fs.mkdir(path.dirname(filePath), { recursive: true });
    await fs.writeFile(filePath, text, 'utf8');
  }

  async readText(filePath: string, fallback = '') {
    if (!(await this.exists(filePath))) {
      return fallback;
    }
    return fs.readFile(filePath, 'utf8');
  }

  async writeTextIfMissing(filePath: string, text: string) {
    if (!(await this.exists(filePath))) {
      await this.writeText(filePath, text);
    }
  }

  async appendJsonl(filePath: string, value: unknown) {
    await fs.mkdir(path.dirname(filePath), { recursive: true });
    await fs.appendFile(filePath, `${JSON.stringify(value)}\n`, 'utf8');
  }

  async readJsonl<T>(filePath: string): Promise<T[]> {
    if (!(await this.exists(filePath))) {
      return [];
    }
    const text = await fs.readFile(filePath, 'utf8');
    return text
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => JSON.parse(line) as T);
  }
}
