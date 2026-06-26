import type {
  Edict,
  EdictInput,
  EdictStoreOptions,
  HistoryEntry,
  EdictFileSchema,
  Tokenizer,
  Renderer,
  MutationResult,
  FindQuery,
  EdictStats,
  ImportResult,
  CapacityStatus,
  CompactionGroup,
  ReviewOptions,
  ReviewResult,
} from './types.js';
import { YamlStorage } from './storage/yaml.js';
import { JsonStorage } from './storage/json.js';
import type { Storage } from './storage/base.js';
import { DEFAULT_SCHEMA } from './storage/base.js';
import { defaultTokenizer } from './tokenizer.js';
import { renderPlain, renderMarkdown, renderJson } from './renderer.js';
import { normalizeCategory, normalizeTags } from './normalize.js';
import { validateEdictInput, validateFileSchema, pruneExpired } from './schema.js';
import { parseDuration } from './duration.js';
import {
  EdictBudgetExceededError,
  EdictCountLimitError,
  EdictConflictError,
  EdictCategoryError,
  EdictNotFoundError,
} from './errors.js';

export class EdictStore {
  private _edicts: Edict[] = [];
  private _history: HistoryEntry[] = [];
  private _fileConfig: EdictFileSchema['config'];
  private _fileHash: string | null = null;
  private _dirty = false;
  private _loaded = false;
  private _sequentialCounter = 0;
  private _loadWarnings: string[] = [];

  private readonly storage: Storage;
  private readonly tokenizer: Tokenizer;
  private readonly customRenderer: Renderer | undefined;
  private readonly maxEdicts: number;
  private readonly tokenBudget: number;
  private readonly categoryAllowlist: string[] | undefined;
  private readonly staleThresholdDays: number;
  private readonly categoryLimits: Record<string, number>;
  private readonly defaultCategoryLimit: number | undefined;
  private readonly defaultEphemeralTtlSeconds: number;
  private readonly autoSave: boolean;

  constructor(options?: EdictStoreOptions) {
    const opts = options ?? {};
    const path = opts.path ?? './edicts.yaml';
    const format = opts.format ?? (path.endsWith('.json') ? 'json' : 'yaml');
    this.storage = format === 'json' ? new JsonStorage(path) : new YamlStorage(path);

    this.tokenizer = opts.tokenizer ?? defaultTokenizer;
    this.customRenderer = opts.renderer;
    this.maxEdicts = opts.maxEdicts ?? 200;
    this.tokenBudget = opts.tokenBudget ?? 4000;
    this.categoryAllowlist =
      opts.categories && opts.categories.length > 0 ? opts.categories : undefined;
    this.staleThresholdDays = opts.staleThresholdDays ?? 90;
    this.categoryLimits = opts.categoryLimits ?? {};
    this.defaultCategoryLimit = opts.defaultCategoryLimit;
    this.defaultEphemeralTtlSeconds = opts.defaultEphemeralTtlSeconds ?? 86400;
    this.autoSave = opts.autoSave ?? true;

    this._fileConfig = { ...DEFAULT_SCHEMA.config };
  }

  async load(): Promise<void> {
    const schema = await this.storage.read();
    this._loadWarnings = validateFileSchema(schema);

    if (schema.config) {
      this._fileConfig = schema.config;
    }

    this._edicts = (schema.edicts ?? []).map((e) => ({
      ...e,
      category: normalizeCategory(e.category),
      tags: normalizeTags(e.tags ?? []),
    }));

    this._history = schema.history ?? [];

    const { active, expired } = pruneExpired(this._edicts);
    this._edicts = active;
    this._history = [...this._history, ...expired];

    this._sequentialCounter = this._computeNextSequential();

    for (const edict of this._edicts) {
      if (!edict.id) {
        edict.id = this._nextSequentialId();
      }
      edict._tokens = this.tokenizer(edict.text);
    }

    this._fileHash = await this.storage.hash();
    this._dirty = expired.length > 0;
    this._loaded = true;
  }

  async save(): Promise<void> {
    if (!this._loaded) {
      const currentHash = await this.storage.hash();
      if (currentHash !== null) {
        throw new EdictConflictError('(not loaded)', currentHash);
      }
    } else if (this._fileHash !== null) {
      const currentHash = await this.storage.hash();
      if (currentHash !== null && currentHash !== this._fileHash) {
        throw new EdictConflictError(this._fileHash, currentHash);
      }
    }

    const schema: EdictFileSchema = {
      version: 1,
      config: {
        maxEdicts: this._fileConfig.maxEdicts ?? this.maxEdicts,
        tokenBudget: this._fileConfig.tokenBudget ?? this.tokenBudget,
        categories: this._fileConfig.categories ?? this.categoryAllowlist ?? [],
        staleThresholdDays: this._fileConfig.staleThresholdDays ?? this.staleThresholdDays,
        categoryLimits: this._fileConfig.categoryLimits ?? this.categoryLimits,
        defaultCategoryLimit: this._fileConfig.defaultCategoryLimit ?? this.defaultCategoryLimit,
        defaultEphemeralTtlSeconds:
          this._fileConfig.defaultEphemeralTtlSeconds ?? this.defaultEphemeralTtlSeconds,
      },
      edicts: this._edicts.map(({ _tokens, ...rest }) => rest),
      history: this._history,
    };

    await this.storage.write(schema);
    this._fileHash = await this.storage.hash();
    this._dirty = false;
  }

  async add(input: EdictInput): Promise<MutationResult> {
    const pruned = await this._autoPrune();
    validateEdictInput(input);

    const category = normalizeCategory(input.category);
    this._validateCategory(category);
    const tags = normalizeTags(input.tags ?? []);
    const now = new Date().toISOString();
    const expiresAt = this._resolveExpiresAt(input);

    if (input.key) {
      const existingIdx = this._edicts.findIndex((e) => e.key === input.key);
      if (existingIdx !== -1) {
        const edict = this._supersede(existingIdx, input, category, tags, now, expiresAt);
        const result = this._buildMutationResult('superseded', edict, pruned);
        if (this.autoSave) await this.save();
        return result;
      }
    }

    if (this._edicts.length >= this.maxEdicts) {
      throw new EdictCountLimitError(this.maxEdicts, this._edicts.length);
    }

    const id = input.key ?? this._nextSequentialId();
    const edict: Edict = {
      id,
      text: input.text,
      category,
      tags,
      confidence: input.confidence ?? 'user',
      source: input.source ?? '',
      key: input.key,
      ttl: input.ttl ?? 'durable',
      expiresAt,
      created: now,
      updated: now,
      _tokens: this.tokenizer(input.text),
    };

    const newTotal = this.tokenCount() + (edict._tokens ?? 0);
    if (newTotal > this.tokenBudget) {
      throw new EdictBudgetExceededError(this.tokenBudget, newTotal);
    }

    this._edicts.push(edict);
    this._dirty = true;

    const result = this._buildMutationResult('created', edict, pruned);
    if (this.autoSave) await this.save();
    return result;
  }

  async remove(id: string): Promise<MutationResult> {
    const pruned = await this._autoPrune();
    const idx = this._edicts.findIndex((e) => e.id === id);
    if (idx === -1) {
      return this._buildMutationResult('not_found', undefined, pruned, { found: false, id });
    }
    const [removed] = this._edicts.splice(idx, 1);
    this._dirty = true;
    if (this.autoSave) await this.save();
    return this._buildMutationResult('deleted', removed, pruned, { found: true });
  }

  async update(id: string, patch: Partial<EdictInput>): Promise<MutationResult> {
    const pruned = await this._autoPrune();
    const edict = this._edicts.find((e) => e.id === id);
    if (!edict) throw new EdictNotFoundError(id);

    validateEdictInput({
      text: patch.text ?? edict.text,
      category: patch.category ?? edict.category,
      confidence: patch.confidence ?? edict.confidence,
      ttl: patch.ttl ?? edict.ttl,
      expiresAt:
        patch.expiresIn !== undefined
          ? undefined
          : patch.expiresAt !== undefined
            ? patch.expiresAt
            : edict.expiresAt,
      expiresIn: patch.expiresIn,
    });

    const nextText = patch.text ?? edict.text;
    const nextTokens =
      patch.text !== undefined ? this.tokenizer(patch.text) : edict._tokens ?? this.tokenizer(edict.text);
    const nextCategory = patch.category !== undefined ? normalizeCategory(patch.category) : edict.category;
    const nextTags = patch.tags !== undefined ? normalizeTags(patch.tags) : edict.tags;
    const nextConfidence = patch.confidence ?? edict.confidence;
    const nextSource = patch.source ?? edict.source;
    const nextTtl = patch.ttl ?? edict.ttl;
    const nextExpiresAt = this._resolveExpiresAt({ ...edict, ...patch, category: nextCategory, text: nextText, ttl: nextTtl });

    this._validateCategory(nextCategory);

    const currentTokens = edict._tokens ?? this.tokenizer(edict.text);
    const newTotal = this.tokenCount() - currentTokens + nextTokens;
    if (newTotal > this.tokenBudget) {
      throw new EdictBudgetExceededError(this.tokenBudget, newTotal);
    }

    edict.text = nextText;
    edict._tokens = nextTokens;
    edict.category = nextCategory;
    edict.tags = nextTags;
    edict.confidence = nextConfidence;
    edict.source = nextSource;
    edict.ttl = nextTtl;
    edict.expiresAt = nextExpiresAt;
    edict.updated = new Date().toISOString();
    this._dirty = true;

    const result = this._buildMutationResult('updated', edict, pruned);
    if (this.autoSave) await this.save();
    return result;
  }

  async get(id: string): Promise<Edict | undefined> {
    await this._autoPrune();
    const edict = this._edicts.find((e) => e.id === id);
    if (!edict) {
      return undefined;
    }

    edict.lastAccessed = new Date().toISOString();
    this._dirty = true;
    if (this.autoSave) await this.save();
    return structuredClone(edict);
  }

  has(id: string): boolean {
    return this._edicts.some((e) => e.id === id);
  }

  async all(): Promise<Edict[]> {
    await this._autoPrune();
    return this._edicts.map((e) => structuredClone(e));
  }

  async find(predicate: ((e: Edict) => boolean) | FindQuery): Promise<Edict[]> {
    await this._autoPrune();
    if (typeof predicate === 'function') {
      return this._edicts.filter(predicate).map((e) => structuredClone(e));
    }

    const query = predicate;
    const normalizedCategory = query.category ? normalizeCategory(query.category) : undefined;
    const normalizedTag = query.tag ? normalizeTags([query.tag])[0] : undefined;
    const normalizedText = query.text?.toLowerCase();

    return this._edicts
      .filter((e) => {
        if (query.id !== undefined && e.id !== query.id) return false;
        if (query.key !== undefined && e.key !== query.key) return false;
        if (normalizedCategory !== undefined && e.category !== normalizedCategory) return false;
        if (normalizedTag !== undefined && !e.tags.includes(normalizedTag)) return false;
        if (query.confidence !== undefined && e.confidence !== query.confidence) return false;
        if (query.ttl !== undefined && e.ttl !== query.ttl) return false;
        if (normalizedText !== undefined && !e.text.toLowerCase().includes(normalizedText)) return false;
        return true;
      })
      .map((e) => structuredClone(e));
  }

  async search(query: string): Promise<Edict[]> {
    await this._autoPrune();
    const needle = query.trim().toLowerCase();
    if (!needle) return this.all();

    return this._edicts
      .filter((e) => {
        return [e.id, e.key ?? '', e.text, e.category, e.source, ...e.tags].some((value) =>
          value.toLowerCase().includes(needle)
        );
      })
      .map((e) => structuredClone(e));
  }

  categories(): string[] {
    return [...new Set(this._edicts.map((e) => e.category))].sort();
  }

  history(): HistoryEntry[] {
    return structuredClone(this._history);
  }

  async stats(): Promise<EdictStats> {
    await this._autoPrune();
    const byCategory: Record<string, number> = {};
    const byConfidence: Record<string, number> = {};
    const byTtl: Record<string, number> = {};
    const byTag: Record<string, number> = {};

    for (const edict of this._edicts) {
      byCategory[edict.category] = (byCategory[edict.category] ?? 0) + 1;
      byConfidence[edict.confidence] = (byConfidence[edict.confidence] ?? 0) + 1;
      byTtl[edict.ttl] = (byTtl[edict.ttl] ?? 0) + 1;
      for (const tag of edict.tags) {
        byTag[tag] = (byTag[tag] ?? 0) + 1;
      }
    }

    return structuredClone({
      total: this._edicts.length,
      history: this._history.length,
      tokenCount: this.tokenCount(),
      tokenBudget: this.tokenBudget,
      tokenBudgetRemaining: this.tokenBudgetRemaining(),
      byCategory,
      byConfidence,
      byTtl,
      byTag,
    });
  }

  capacityStatus(): CapacityStatus {
    const categories: CapacityStatus['categories'] = {};
    for (const edict of this._edicts) {
      const category = edict.category;
      const limit = this.categoryLimits[category] ?? this.defaultCategoryLimit;
      const current = categories[category] ?? { count: 0, limit, overLimit: false };
      current.count += 1;
      current.limit = limit;
      current.overLimit = limit !== undefined ? current.count > limit : false;
      categories[category] = current;
    }

    const countUsage = this.maxEdicts === 0 ? 0 : this._edicts.length / this.maxEdicts;
    const tokenUsage = this.tokenBudget === 0 ? 0 : this.tokenCount() / this.tokenBudget;
    const warnings: string[] = [];

    if (countUsage >= 0.8) {
      warnings.push(
        `Store at ${Math.round(countUsage * 100)}% count capacity (${this._edicts.length}/${this.maxEdicts} edicts)`
      );
    }
    if (tokenUsage >= 0.8) {
      warnings.push(
        `Store at ${Math.round(tokenUsage * 100)}% token capacity (${this.tokenCount()}/${this.tokenBudget} tokens)`
      );
    }

    for (const [category, status] of Object.entries(categories)) {
      if (status.limit !== undefined && status.count > status.limit) {
        warnings.push(`Category "${category}" exceeds soft limit (${status.count}/${status.limit})`);
      }
    }

    return structuredClone({ countUsage, tokenUsage, categories, warnings });
  }

  async review(options?: ReviewOptions): Promise<ReviewResult> {
    await this._autoPrune();
    const now = Date.now();
    const staleThresholdMs = this.staleThresholdDays * 86400 * 1000;
    const lookaheadMs = (options?.expiryLookaheadDays ?? 7) * 86400 * 1000;

    const stale = this._edicts.filter((e) => {
      if (e.ttl !== 'durable') return false;
      const accessedAt = e.lastAccessed ?? e.created;
      return now - new Date(accessedAt).getTime() > staleThresholdMs;
    });

    const expiringSoon = this._edicts.filter((e) => {
      if (!e.expiresAt) return false;
      const expiresMs = new Date(e.expiresAt).getTime();
      const remaining = expiresMs - now;
      return remaining > 0 && remaining <= lookaheadMs;
    });

    const capacity = this.capacityStatus();
    const compactionCandidates = this._findCompactionCandidates();

    return structuredClone({ stale, expiringSoon, capacity, compactionCandidates });
  }

  async compact(group: CompactionGroup, merged: EdictInput): Promise<MutationResult> {
    const pruned = await this._autoPrune();
    const snapshotEdicts = this._edicts.map((e) => structuredClone(e));
    const snapshotHistory = this._history.map((h) => structuredClone(h));
    const snapshotDirty = this._dirty;
    const now = new Date().toISOString();

    try {
      validateEdictInput(merged);
      const ids = new Set(group.edicts.map((e) => e.id));
      const removed = this._edicts.filter((e) => ids.has(e.id));
      this._edicts = this._edicts.filter((e) => !ids.has(e.id));
      this._history = [
        ...this._history,
        ...removed.map((removedEdict) => ({
          id: `${removedEdict.id}__${now.replace(/[-:.TZ]/g, '')}_compacted`,
          text: removedEdict.text,
          supersededBy: 'compacted',
          archivedAt: now,
        })),
      ];

      const category = normalizeCategory(merged.category);
      this._validateCategory(category);
      const tags = normalizeTags(merged.tags ?? []);
      const expiresAt = this._resolveExpiresAt(merged);
      const id = merged.key ?? this._nextSequentialId();
      const edict: Edict = {
        id,
        text: merged.text,
        category,
        tags,
        confidence: merged.confidence ?? 'user',
        source: merged.source ?? '',
        key: merged.key,
        ttl: merged.ttl ?? 'durable',
        expiresAt,
        created: now,
        updated: now,
        _tokens: this.tokenizer(merged.text),
      };

      const newTotal = this.tokenCount() + (edict._tokens ?? 0);
      if (newTotal > this.tokenBudget) {
        throw new EdictBudgetExceededError(this.tokenBudget, newTotal);
      }

      this._edicts.push(edict);
      this._dirty = true;
      const result = this._buildMutationResult('created', edict, pruned);
      if (this.autoSave) await this.save();
      return result;
    } catch (error) {
      this._edicts = snapshotEdicts;
      this._history = snapshotHistory;
      this._dirty = snapshotDirty;
      throw error;
    }
  }

  exportData(): EdictFileSchema {
    return structuredClone({
      version: 1,
      config: {
        maxEdicts: this._fileConfig.maxEdicts ?? this.maxEdicts,
        tokenBudget: this._fileConfig.tokenBudget ?? this.tokenBudget,
        categories: this._fileConfig.categories ?? this.categoryAllowlist ?? [],
        staleThresholdDays: this._fileConfig.staleThresholdDays ?? this.staleThresholdDays,
        categoryLimits: this._fileConfig.categoryLimits ?? this.categoryLimits,
        defaultCategoryLimit: this._fileConfig.defaultCategoryLimit ?? this.defaultCategoryLimit,
        defaultEphemeralTtlSeconds:
          this._fileConfig.defaultEphemeralTtlSeconds ?? this.defaultEphemeralTtlSeconds,
      },
      edicts: this._edicts.map(({ _tokens, ...rest }) => rest),
      history: this._history,
    });
  }

  async importData(data: EdictFileSchema): Promise<ImportResult> {
    const warnings = validateFileSchema(data);
    if (warnings.length > 0) {
      this._loadWarnings = [...this._loadWarnings, ...warnings];
    }

    this._fileConfig = data.config ?? this._fileConfig;
    this._history = structuredClone(data.history ?? []);
    this._edicts = (data.edicts ?? []).map((e) => ({
      ...e,
      category: normalizeCategory(e.category),
      tags: normalizeTags(e.tags ?? []),
      _tokens: this.tokenizer(e.text),
    }));

    const { active, expired } = pruneExpired(this._edicts);
    this._edicts = active;
    this._history = [...this._history, ...expired];
    this._sequentialCounter = this._computeNextSequential();
    this._dirty = true;

    const result = structuredClone({
      imported: this._edicts.length,
      historyImported: data.history?.length ?? 0,
      pruned: expired.length,
    });

    if (this.autoSave) await this.save();
    return result;
  }

  async render(format?: 'plain' | 'markdown' | 'json'): Promise<string> {
    await this._autoPrune();
    const now = new Date().toISOString();
    for (const edict of this._edicts) {
      edict.lastAccessed = now;
    }
    if (this._edicts.length > 0) {
      this._dirty = true;
      if (this.autoSave) await this.save();
    }

    if (this.customRenderer && !format) {
      return this.customRenderer(this._edicts);
    }

    switch (format ?? 'plain') {
      case 'plain':
        return renderPlain(this._edicts);
      case 'markdown':
        return renderMarkdown(this._edicts);
      case 'json':
        return renderJson(this._edicts);
      default:
        return renderPlain(this._edicts);
    }
  }

  tokenCount(): number {
    return this._edicts.reduce((sum, e) => sum + (e._tokens ?? 0), 0);
  }

  tokenBudgetRemaining(): number {
    return this.tokenBudget - this.tokenCount();
  }

  isOverBudget(): boolean {
    return this.tokenCount() > this.tokenBudget;
  }

  get dirty(): boolean {
    return this._dirty;
  }

  get fileHash(): string {
    return this._fileHash ?? '';
  }

  get loadWarnings(): string[] {
    return [...this._loadWarnings];
  }

  private _resolveExpiresAt(input: Partial<EdictInput> & { ttl?: Edict['ttl'] }): string | undefined {
    if (input.expiresIn !== undefined) {
      const seconds = parseDuration(input.expiresIn);
      return new Date(Date.now() + seconds * 1000).toISOString();
    }

    if (input.expiresAt) {
      return input.expiresAt;
    }

    if (input.ttl === 'ephemeral') {
      return new Date(Date.now() + this.defaultEphemeralTtlSeconds * 1000).toISOString();
    }

    return undefined;
  }

  private _supersede(
    existingIdx: number,
    input: EdictInput,
    category: string,
    tags: string[],
    now: string,
    expiresAt: string | undefined
  ): Edict {
    const existing = this._edicts[existingIdx];
    const previousText = existing.text;
    const previousCategory = existing.category;
    const previousTags = [...existing.tags];
    const previousConfidence = existing.confidence;
    const previousSource = existing.source;
    const previousTtl = existing.ttl;
    const previousExpiresAt = existing.expiresAt;
    const previousUpdated = existing.updated;
    const previousTokens = existing._tokens ?? this.tokenizer(existing.text);

    const version =
      this._history.filter((entry) => entry.supersededBy === existing.id).length + 1;
    const ts = now.replace(/[-:.TZ]/g, '');
    const historyId = `${existing.id}__${ts}_${String(version).padStart(3, '0')}`;
    this._history.push({
      id: historyId,
      text: previousText,
      supersededBy: existing.id,
      archivedAt: now,
    });

    existing.text = input.text;
    existing.category = category;
    existing.tags = tags;
    existing.confidence = input.confidence ?? existing.confidence;
    existing.source = input.source ?? existing.source;
    existing.ttl = input.ttl ?? existing.ttl;
    existing.expiresAt = expiresAt;
    existing.updated = now;
    existing._tokens = this.tokenizer(input.text);

    const newTotal = this.tokenCount();
    if (newTotal > this.tokenBudget) {
      existing.text = previousText;
      existing.category = previousCategory;
      existing.tags = previousTags;
      existing.confidence = previousConfidence;
      existing.source = previousSource;
      existing.ttl = previousTtl;
      existing.expiresAt = previousExpiresAt;
      existing.updated = previousUpdated;
      existing._tokens = previousTokens;
      this._history.pop();
      throw new EdictBudgetExceededError(this.tokenBudget, newTotal);
    }

    this._dirty = true;
    return existing;
  }

  private _validateCategory(category: string): void {
    if (this.categoryAllowlist && !this.categoryAllowlist.includes(category)) {
      throw new EdictCategoryError(category, this.categoryAllowlist);
    }
  }

  private _nextSequentialId(): string {
    this._sequentialCounter++;
    return `e_${String(this._sequentialCounter).padStart(3, '0')}`;
  }

  private _computeNextSequential(): number {
    let max = 0;
    for (const edict of this._edicts) {
      if (!edict.id) continue;
      const match = edict.id.match(/^e_(\d+)$/);
      if (match) {
        max = Math.max(max, parseInt(match[1], 10));
      }
    }
    return max;
  }

  private async _autoPrune(): Promise<number> {
    const { active, expired } = pruneExpired(this._edicts);
    if (expired.length === 0) {
      return 0;
    }

    this._edicts = active;
    this._history = [...this._history, ...expired];
    this._dirty = true;
    if (this.autoSave) await this.save();
    return expired.length;
  }

  private _findCompactionCandidates(): CompactionGroup[] {
    const groups = new Map<string, Edict[]>();

    for (const edict of this._edicts) {
      if (!edict.key) continue;
      const keyPrefix = this._keyPrefix(edict.key);
      const groupKey = `${edict.category}::${keyPrefix}`;
      const existing = groups.get(groupKey) ?? [];
      existing.push(edict);
      groups.set(groupKey, existing);
    }

    return [...groups.entries()]
      .filter(([, edicts]) => edicts.length >= 2)
      .map(([groupKey, edicts]) => {
        const separatorIndex = groupKey.indexOf('::');
        const category = separatorIndex === -1 ? groupKey : groupKey.slice(0, separatorIndex);
        const keyPrefix = separatorIndex === -1 ? '' : groupKey.slice(separatorIndex + 2);
        return { keyPrefix, category, edicts: structuredClone(edicts) };
      });
  }

  private _keyPrefix(key: string): string {
    for (const separator of ['/', '.']) {
      if (key.includes(separator)) {
        const parts = key.split(separator);
        if (parts.length > 1) {
          return parts.slice(0, -1).join(separator);
        }
      }
    }
    return key;
  }

  private _buildMutationResult(
    action: MutationResult['action'],
    edict: Edict | undefined,
    pruned: number,
    extra: Partial<MutationResult> = {}
  ): MutationResult {
    const warnings = this.capacityStatus().warnings;
    return {
      action,
      edict: edict ? structuredClone(edict) : undefined,
      pruned,
      ...extra,
      warnings: warnings.length > 0 ? warnings : undefined,
    };
  }
}

