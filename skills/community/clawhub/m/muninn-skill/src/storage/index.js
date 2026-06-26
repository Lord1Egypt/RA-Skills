"use strict";
/**
 * OpenClaw Memory System v1
 * Storage Layer - SQLite + Vector Search
 *
 * Local-first, Ollama-compatible memory system
 * Forked from Engram patterns, optimized for OpenClaw
 */
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.MemoryStore = void 0;
exports.generateEmbedding = generateEmbedding;
var better_sqlite3_1 = require("better-sqlite3");
var uuid_1 = require("uuid");
var path_1 = require("path");
// ============================================================================
// PHASE 1.4 RETRIEVAL FEATURES - IMPORTS
// ============================================================================
var hybrid_js_1 = require("../retrieval/hybrid.js");
var filter_js_1 = require("../retrieval/filter.js");
var normalize_js_1 = require("../extractors/normalize.js");
// Alias store for spelling variants and entity aliases
var aliasStore = null;
function getAliasStore() {
    if (!aliasStore) {
        aliasStore = (0, normalize_js_1.createAliasStore)();
    }
    return aliasStore;
}
// ============================================================================
// ENTITY EXTRACTION (simple version for storage)
// ============================================================================
function extractEntitiesFromText(text) {
    var entities = [];
    var patterns = [
        'Phillip', 'KakāpōHiko', 'Kakāpō', 'Hiko',
        'Elev8Advisory', 'BrandForge', 'Muninn', 'OpenClaw',
        'Sammy Clemens', 'Charlie Babbage', 'Donna Paulsen',
        'Brisbane', 'Australia', 'React', 'Node.js', 'PostgreSQL',
        'SQLite', 'Ollama', 'Stripe'
    ];
    for (var _i = 0, patterns_1 = patterns; _i < patterns_1.length; _i++) {
        var p = patterns_1[_i];
        if (text.toLowerCase().includes(p.toLowerCase())) {
            entities.push(p);
        }
    }
    return __spreadArray([], new Set(entities), true);
}
// ============================================================================
// QUERY EXPANSION FOR SPELLING VARIANTS
// ============================================================================
/**
 * Expand query with spelling variants (UK↔US English)
 */
function expandQueryWithVariants(query) {
    var expandedQueries = [query];
    // Common spelling variants to check
    var variantPairs = [
        ['colour', 'color'],
        ['flavour', 'flavor'],
        ['honour', 'honor'],
        ['organise', 'organize'],
        ['realise', 'realize'],
        ['recognise', 'recognize'],
        ['analyse', 'analyze'],
        ['centre', 'center'],
        ['theatre', 'theater'],
        ['defence', 'defense'],
        ['offence', 'offense'],
        ['licence', 'license'],
        ['programme', 'program'],
        ['behaviour', 'behavior'],
    ];
    for (var _i = 0, variantPairs_1 = variantPairs; _i < variantPairs_1.length; _i++) {
        var _a = variantPairs_1[_i], uk = _a[0], us = _a[1];
        // If query contains UK form, add US version
        if (query.toLowerCase().includes(uk)) {
            expandedQueries.push(query.replace(new RegExp(uk, 'gi'), us));
        }
        // If query contains US form, add UK version  
        if (query.toLowerCase().includes(us)) {
            expandedQueries.push(query.replace(new RegExp(us, 'gi'), uk));
        }
    }
    return __spreadArray([], new Set(expandedQueries), true);
}
// Embedding function using Ollama
function generateEmbedding(text) {
    return __awaiter(this, void 0, void 0, function () {
        var response, data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch('http://localhost:11434/api/embeddings', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            model: 'nomic-embed-text',
                            prompt: text
                        })
                    })];
                case 1:
                    response = _a.sent();
                    if (!response.ok) {
                        throw new Error("Ollama embedding failed: ".concat(response.statusText));
                    }
                    return [4 /*yield*/, response.json()];
                case 2:
                    data = _a.sent();
                    return [2 /*return*/, data.embedding];
            }
        });
    });
}
// Cosine similarity
function cosineSimilarity(a, b) {
    if (a.length !== b.length)
        return 0;
    var dotProduct = 0;
    var normA = 0;
    var normB = 0;
    for (var i = 0; i < a.length; i++) {
        dotProduct += a[i] * b[i];
        normA += a[i] * a[i];
        normB += b[i] * b[i];
    }
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}
var MemoryStore = /** @class */ (function () {
    function MemoryStore(dbPath) {
        var defaultPath = path_1.default.join(process.cwd(), 'openclaw-memory.db');
        this.db = new better_sqlite3_1.default(dbPath || defaultPath);
        this.init();
    }
    MemoryStore.prototype.init = function () {
        // Enable vector similarity search using simple implementation
        this.db.exec("\n      CREATE TABLE IF NOT EXISTS memories (\n        id TEXT PRIMARY KEY,\n        type TEXT NOT NULL CHECK(type IN ('episodic', 'semantic', 'procedural')),\n        content TEXT NOT NULL,\n        title TEXT,\n        summary TEXT,\n        entities TEXT DEFAULT '[]',\n        topics TEXT DEFAULT '[]',\n        embedding BLOB,\n        salience REAL DEFAULT 0.5,\n        created_at TEXT DEFAULT (datetime('now')),\n        updated_at TEXT DEFAULT (datetime('now')),\n        deleted_at TEXT\n      );\n      \n      CREATE TABLE IF NOT EXISTS entities (\n        name TEXT PRIMARY KEY,\n        memory_count INTEGER DEFAULT 0,\n        last_seen TEXT DEFAULT (datetime('now'))\n      );\n      \n      CREATE TABLE IF NOT EXISTS edges (\n        id TEXT PRIMARY KEY,\n        source_id TEXT NOT NULL,\n        target_id TEXT NOT NULL,\n        relationship TEXT NOT NULL,\n        created_at TEXT DEFAULT (datetime('now')),\n        FOREIGN KEY (source_id) REFERENCES memories(id) ON DELETE CASCADE,\n        FOREIGN KEY (target_id) REFERENCES memories(id) ON DELETE CASCADE\n      );\n      \n      CREATE TABLE IF NOT EXISTS procedures (\n        id TEXT PRIMARY KEY,\n        title TEXT NOT NULL,\n        description TEXT,\n        steps TEXT DEFAULT '[]',\n        version INTEGER DEFAULT 1,\n        success_count INTEGER DEFAULT 0,\n        failure_count INTEGER DEFAULT 0,\n        is_reliable INTEGER DEFAULT 0,\n        evolution_log TEXT DEFAULT '[]',\n        created_at TEXT DEFAULT (datetime('now')),\n        updated_at TEXT DEFAULT (datetime('now'))\n      );\n      \n      CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);\n      CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);\n      CREATE INDEX IF NOT EXISTS idx_memories_deleted ON memories(deleted_at);\n      CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);\n      CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id);\n      CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id);\n    ");
        console.log('📦 Memory database initialized');
    };
    // Memory CRUD
    MemoryStore.prototype.remember = function (content_1) {
        return __awaiter(this, arguments, void 0, function (content, type, options) {
            var id, embedding, now, extractedEntities, entitiesForNormalization, normalized, aliasStore, _i, normalized_1, norm, _a, _b, alias, canonicalEntities, embeddingBuffer, stmt, entityStmt, _c, canonicalEntities_1, entity;
            if (type === void 0) { type = 'semantic'; }
            if (options === void 0) { options = {}; }
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        id = "m_".concat((0, uuid_1.v4)().slice(0, 8));
                        return [4 /*yield*/, generateEmbedding(content)];
                    case 1:
                        embedding = _d.sent();
                        now = new Date().toISOString();
                        extractedEntities = options.entities || extractEntitiesFromText(content);
                        entitiesForNormalization = extractedEntities.map(function (e) { return ({
                            text: e,
                            type: 'concept',
                            confidence: 0.8,
                            context: '',
                        }); });
                        return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(content, entitiesForNormalization)];
                    case 2:
                        normalized = _d.sent();
                        aliasStore = getAliasStore();
                        for (_i = 0, normalized_1 = normalized; _i < normalized_1.length; _i++) {
                            norm = normalized_1[_i];
                            for (_a = 0, _b = norm.aliases; _a < _b.length; _a++) {
                                alias = _b[_a];
                                aliasStore.addAlias(norm.canonical, alias);
                            }
                        }
                        canonicalEntities = __spreadArray([], new Set(normalized.map(function (n) { return n.canonical; })), true);
                        embeddingBuffer = Buffer.from(new Float32Array(embedding).buffer);
                        stmt = this.db.prepare("\n      INSERT INTO memories (id, type, content, title, summary, entities, topics, embedding, salience, created_at, updated_at)\n      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\n    ");
                        stmt.run(id, type, content, options.title || null, options.summary || null, JSON.stringify(canonicalEntities), JSON.stringify(options.topics || []), embeddingBuffer, options.salience || 0.5, now, now);
                        // Update entity counts (use canonical names)
                        if (canonicalEntities.length) {
                            entityStmt = this.db.prepare("\n        INSERT INTO entities (name, memory_count, last_seen)\n        VALUES (?, 1, ?)\n        ON CONFLICT(name) DO UPDATE SET\n          memory_count = memory_count + 1,\n          last_seen = ?\n      ");
                            for (_c = 0, canonicalEntities_1 = canonicalEntities; _c < canonicalEntities_1.length; _c++) {
                                entity = canonicalEntities_1[_c];
                                entityStmt.run(entity, now, now);
                            }
                        }
                        return [2 /*return*/, this.getMemory(id)];
                }
            });
        });
    };
    MemoryStore.prototype.getMemory = function (id) {
        var _a;
        var stmt = this.db.prepare('SELECT * FROM memories WHERE id = ? AND deleted_at IS NULL');
        var row = stmt.get(id);
        if (!row)
            return null;
        return __assign(__assign({}, row), { entities: JSON.parse(row.entities || '[]'), topics: JSON.parse(row.topics || '[]'), embedding: Array.from(new Float32Array(((_a = row.embedding) === null || _a === void 0 ? void 0 : _a.buffer) || new ArrayBuffer(0))) });
    };
    MemoryStore.prototype.recall = function (context_1) {
        return __awaiter(this, arguments, void 0, function (context, options) {
            var limit, memories, isFactualQuery, semanticOnly, semanticResults, error_1;
            var _a, _b;
            if (options === void 0) { options = {}; }
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        limit = options.limit || 10;
                        memories = this.db.prepare("\n      SELECT * FROM memories WHERE deleted_at IS NULL\n    ").all();
                        // Parse stored fields
                        memories = memories.map(function (row) {
                            var _a;
                            return (__assign(__assign({}, row), { entities: JSON.parse(row.entities || '[]'), topics: JSON.parse(row.topics || '[]'), embedding: Array.from(new Float32Array(((_a = row.embedding) === null || _a === void 0 ? void 0 : _a.buffer) || new ArrayBuffer(0))) }));
                        });
                        // Filter by type
                        if ((_a = options.types) === null || _a === void 0 ? void 0 : _a.length) {
                            memories = memories.filter(function (m) { return options.types.includes(m.type); });
                        }
                        // Filter by entities
                        if ((_b = options.entities) === null || _b === void 0 ? void 0 : _b.length) {
                            memories = memories.filter(function (m) {
                                return options.entities.some(function (e) { return m.entities.includes(e); });
                            });
                        }
                        // If too few memories, fall back to simple similarity
                        if (memories.length < 3) {
                            return [2 /*return*/, this.simpleRecall(context, limit)];
                        }
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 4, , 5]);
                        isFactualQuery = /^(what|who|which|when|where|how (does|do|is|did|can|was|were)|why|whose)/i.test(context) ||
                            /name|called|mean|stand for|relationship|port|model|database|stack|agents?|team|projects?|revenue|target|priority|embedding|spelling/i.test(context);
                        if (!(isFactualQuery && !options.types)) return [3 /*break*/, 3];
                        semanticOnly = memories.filter(function (m) { return m.type === 'semantic' && (m.salience || 0.5) >= 0.5; });
                        if (!(semanticOnly.length > 0)) return [3 /*break*/, 3];
                        return [4 /*yield*/, this.recallInternal(context, semanticOnly, limit)];
                    case 2:
                        semanticResults = _c.sent();
                        // If we got good results from semantic, return them
                        if (semanticResults.length > 0) {
                            return [2 /*return*/, semanticResults];
                        }
                        _c.label = 3;
                    case 3: return [2 /*return*/, this.recallInternal(context, memories, limit)];
                    case 4:
                        error_1 = _c.sent();
                        console.warn('Hybrid retrieval failed, using fallback:', error_1);
                        return [2 /*return*/, this.simpleRecall(context, limit)];
                    case 5: return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Internal recall with hybrid search
     */
    MemoryStore.prototype.recallInternal = function (context, memories, limit) {
        return __awaiter(this, void 0, void 0, function () {
            var expandedQueries, queryEntities_1, candidates, _i, _a, expandedQuery, expandedResults, existingIds, _b, expandedResults_1, m, _c, candidates_1, c, memoryEntities, overlap, scored, error_2;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _d.trys.push([0, 6, , 7]);
                        expandedQueries = expandQueryWithVariants(context);
                        queryEntities_1 = extractEntitiesFromText(context);
                        return [4 /*yield*/, (0, hybrid_js_1.hybridSearch)(context, memories, {
                                k: limit * 3,
                                enableLLMFilter: false
                            })];
                    case 1:
                        candidates = _d.sent();
                        _i = 0, _a = expandedQueries.slice(1);
                        _d.label = 2;
                    case 2:
                        if (!(_i < _a.length)) return [3 /*break*/, 5];
                        expandedQuery = _a[_i];
                        return [4 /*yield*/, (0, hybrid_js_1.hybridSearch)(expandedQuery, memories, {
                                k: limit * 2,
                                enableLLMFilter: false
                            })];
                    case 3:
                        expandedResults = _d.sent();
                        existingIds = new Set(candidates.map(function (m) { return m.id; }));
                        for (_b = 0, expandedResults_1 = expandedResults; _b < expandedResults_1.length; _b++) {
                            m = expandedResults_1[_b];
                            if (!existingIds.has(m.id)) {
                                candidates.push(m);
                            }
                        }
                        _d.label = 4;
                    case 4:
                        _i++;
                        return [3 /*break*/, 2];
                    case 5:
                        // 5. Boost by entity overlap
                        if (queryEntities_1.length > 0) {
                            for (_c = 0, candidates_1 = candidates; _c < candidates_1.length; _c++) {
                                c = candidates_1[_c];
                                memoryEntities = c.entities || [];
                                overlap = memoryEntities.filter(function (e) {
                                    return queryEntities_1.some(function (qe) { return e.toLowerCase() === qe.toLowerCase(); });
                                });
                                if (overlap.length > 0) {
                                    c._entityBoost = 1 + (overlap.length * 0.5); // 50% boost per matching entity
                                }
                            }
                        }
                        // 6. Re-sort with entity boost
                        candidates.sort(function (a, b) {
                            var scoreA = a._finalScore || a._rrfScore || 0;
                            var scoreB = b._finalScore || b._rrfScore || 0;
                            var boostA = a._entityBoost || 1;
                            var boostB = b._entityBoost || 1;
                            return (scoreB * boostB) - (scoreA * boostA);
                        });
                        scored = (0, filter_js_1.scoreForQuestionType)(candidates.slice(0, limit), context);
                        return [2 /*return*/, scored];
                    case 6:
                        error_2 = _d.sent();
                        console.warn('Recall internal failed:', error_2);
                        return [2 /*return*/, []];
                    case 7: return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Simple semantic recall fallback
     */
    MemoryStore.prototype.simpleRecall = function (context, limit) {
        return __awaiter(this, void 0, void 0, function () {
            var queryEmbedding, memories, scored;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, generateEmbedding(context)];
                    case 1:
                        queryEmbedding = _a.sent();
                        memories = this.db.prepare("\n      SELECT * FROM memories WHERE deleted_at IS NULL\n    ").all();
                        memories = memories.map(function (row) {
                            var _a;
                            return (__assign(__assign({}, row), { entities: JSON.parse(row.entities || '[]'), topics: JSON.parse(row.topics || '[]'), embedding: Array.from(new Float32Array(((_a = row.embedding) === null || _a === void 0 ? void 0 : _a.buffer) || new ArrayBuffer(0))) }));
                        });
                        scored = memories.map(function (m) { return (__assign(__assign({}, m), { _similarity: m.embedding.length > 0 ? cosineSimilarity(queryEmbedding, m.embedding) : 0 })); });
                        scored.sort(function (a, b) { return b._similarity - a._similarity; });
                        return [2 /*return*/, scored.slice(0, limit).map(function (_a) {
                                var _similarity = _a._similarity, m = __rest(_a, ["_similarity"]);
                                return m;
                            })];
                }
            });
        });
    };
    MemoryStore.prototype.forget = function (id, hard) {
        if (hard === void 0) { hard = false; }
        if (hard) {
            var stmt = this.db.prepare('DELETE FROM memories WHERE id = ?');
            return stmt.run(id).changes > 0;
        }
        else {
            var stmt = this.db.prepare("UPDATE memories SET deleted_at = datetime('now') WHERE id = ?");
            return stmt.run(id).changes > 0;
        }
    };
    // Entity management
    MemoryStore.prototype.getEntities = function () {
        return this.db.prepare('SELECT * FROM entities ORDER BY memory_count DESC').all();
    };
    // Graph edges
    MemoryStore.prototype.connect = function (sourceId, targetId, relationship) {
        var id = "e_".concat((0, uuid_1.v4)().slice(0, 8));
        var now = new Date().toISOString();
        var stmt = this.db.prepare("\n      INSERT INTO edges (id, source_id, target_id, relationship, created_at)\n      VALUES (?, ?, ?, ?, ?)\n    ");
        stmt.run(id, sourceId, targetId, relationship, now);
        return { id: id, source_id: sourceId, target_id: targetId, relationship: relationship, created_at: now };
    };
    MemoryStore.prototype.getNeighbors = function (memoryId, depth) {
        var _a;
        if (depth === void 0) { depth = 1; }
        var neighbors = new Set([memoryId]);
        var result = [];
        for (var i = 0; i < depth; i++) {
            var ids = Array.from(neighbors);
            if (ids.length === 0)
                break;
            var rows_2 = (_a = this.db.prepare("\n        SELECT DISTINCT target_id FROM edges WHERE source_id IN (".concat(ids.map(function () { return '?'; }).join(','), ")\n      "))).all.apply(_a, ids);
            for (var _i = 0, rows_1 = rows_2; _i < rows_1.length; _i++) {
                var row = rows_1[_i];
                if (!neighbors.has(row.target_id)) {
                    neighbors.add(row.target_id);
                }
            }
        }
        var memStmt = this.db.prepare("SELECT * FROM memories WHERE id IN (".concat(Array.from(neighbors).map(function () { return '?'; }).join(','), ")"));
        var rows = memStmt.all.apply(memStmt, Array.from(neighbors));
        return rows.map(function (row) {
            var _a;
            return (__assign(__assign({}, row), { entities: JSON.parse(row.entities || '[]'), topics: JSON.parse(row.topics || '[]'), embedding: Array.from(new Float32Array(((_a = row.embedding) === null || _a === void 0 ? void 0 : _a.buffer) || new ArrayBuffer(0))) }));
        });
    };
    // Stats
    MemoryStore.prototype.getStats = function () {
        var total = this.db.prepare('SELECT COUNT(*) as count FROM memories WHERE deleted_at IS NULL').get().count;
        var byType = {
            episodic: this.db.prepare("SELECT COUNT(*) as count FROM memories WHERE type = 'episodic' AND deleted_at IS NULL").get().count,
            semantic: this.db.prepare("SELECT COUNT(*) as count FROM memories WHERE type = 'semantic' AND deleted_at IS NULL").get().count,
            procedural: this.db.prepare("SELECT COUNT(*) as count FROM memories WHERE type = 'procedural' AND deleted_at IS NULL").get().count
        };
        var entities = this.db.prepare('SELECT COUNT(*) as count FROM entities').get().count;
        var edges = this.db.prepare('SELECT COUNT(*) as count FROM edges').get().count;
        var procedures = this.db.prepare('SELECT COUNT(*) as count FROM procedures').get().count;
        return { total: total, byType: byType, entities: entities, edges: edges, procedures: procedures };
    };
    // Procedure management
    MemoryStore.prototype.createProcedure = function (title, steps, description) {
        return __awaiter(this, void 0, void 0, function () {
            var id, now, procedureSteps, stmt;
            return __generator(this, function (_a) {
                id = "proc_".concat((0, uuid_1.v4)().slice(0, 8));
                now = new Date().toISOString();
                procedureSteps = steps.map(function (desc, i) { return ({
                    id: "step_".concat((0, uuid_1.v4)().slice(0, 8)),
                    order: i + 1,
                    description: desc
                }); });
                stmt = this.db.prepare("\n      INSERT INTO procedures (id, title, description, steps, version, success_count, failure_count, is_reliable, evolution_log, created_at, updated_at)\n      VALUES (?, ?, ?, ?, 1, 0, 0, 0, '[]', ?, ?)\n    ");
                stmt.run(id, title, description || null, JSON.stringify(procedureSteps), now, now);
                return [2 /*return*/, this.getProcedure(id)];
            });
        });
    };
    MemoryStore.prototype.getProcedure = function (id) {
        var stmt = this.db.prepare('SELECT * FROM procedures WHERE id = ?');
        var row = stmt.get(id);
        if (!row)
            return null;
        return __assign(__assign({}, row), { steps: JSON.parse(row.steps || '[]'), evolution_log: JSON.parse(row.evolution_log || '[]'), is_reliable: Boolean(row.is_reliable) });
    };
    MemoryStore.prototype.getAllProcedures = function () {
        var rows = this.db.prepare('SELECT * FROM procedures ORDER BY updated_at DESC').all();
        return rows.map(function (row) { return (__assign(__assign({}, row), { steps: JSON.parse(row.steps || '[]'), evolution_log: JSON.parse(row.evolution_log || '[]'), is_reliable: Boolean(row.is_reliable) })); });
    };
    MemoryStore.prototype.procedureFeedback = function (procedureId, success, failedAtStep, context) {
        return __awaiter(this, void 0, void 0, function () {
            var proc, now, newVersion, newCount, isReliable, evolutionEvent, newSteps, evolutionEvent;
            return __generator(this, function (_a) {
                proc = this.getProcedure(procedureId);
                if (!proc)
                    throw new Error('Procedure not found');
                now = new Date().toISOString();
                newVersion = proc.version + 1;
                if (success) {
                    newCount = proc.success_count + 1;
                    isReliable = newCount >= 3 && !proc.is_reliable;
                    evolutionEvent = {
                        version: newVersion,
                        trigger: 'success_pattern',
                        change: "Success count: ".concat(newCount, ". ").concat(isReliable ? 'Promoted to reliable workflow.' : ''),
                        timestamp: now
                    };
                    this.db.prepare("\n        UPDATE procedures SET \n          success_count = ?,\n          is_reliable = ?,\n          evolution_log = ?,\n          updated_at = ?\n        WHERE id = ?\n      ").run(newCount, isReliable ? 1 : 0, JSON.stringify(__spreadArray(__spreadArray([], proc.evolution_log, true), [evolutionEvent], false)), now, procedureId);
                }
                else {
                    newSteps = proc.steps;
                    if (failedAtStep) {
                        newSteps = proc.steps.map(function (step, i) {
                            if (i + 1 === failedAtStep) {
                                return __assign(__assign({}, step), { description: "".concat(step.description, " [RETRY: add error handling]") });
                            }
                            return step;
                        });
                    }
                    evolutionEvent = {
                        version: newVersion,
                        trigger: 'failure',
                        change: "Failed at step ".concat(failedAtStep || 'unknown', ". ").concat(context || '', " New version created."),
                        timestamp: now
                    };
                    this.db.prepare("\n        UPDATE procedures SET \n          version = ?,\n          failure_count = failure_count + 1,\n          steps = ?,\n          evolution_log = ?,\n          updated_at = ?\n        WHERE id = ?\n      ").run(newVersion, JSON.stringify(newSteps), JSON.stringify(__spreadArray(__spreadArray([], proc.evolution_log, true), [evolutionEvent], false)), now, procedureId);
                }
                return [2 /*return*/, this.getProcedure(procedureId)];
            });
        });
    };
    MemoryStore.prototype.close = function () {
        this.db.close();
    };
    return MemoryStore;
}());
exports.MemoryStore = MemoryStore;
// Default export
exports.default = MemoryStore;
