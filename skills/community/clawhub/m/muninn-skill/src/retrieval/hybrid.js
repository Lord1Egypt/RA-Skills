"use strict";
/**
 * Hybrid Retrieval using Reciprocal Rank Fusion (RRF)
 *
 * Combines dense (semantic/embedding) and sparse (BM25) retrieval
 * to get the best of both worlds: semantic understanding + exact term matching.
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
exports.hybridSearch = hybridSearch;
exports.getRetrievalBreakdown = getRetrievalBreakdown;
var index_js_1 = require("../storage/index.js");
var bm25_js_1 = require("./bm25.js");
var temporal_decay_js_1 = require("./temporal-decay.js");
/**
 * Cosine similarity (inline to avoid import issues)
 */
function cosineSimilarity(a, b) {
    if (a.length !== b.length || a.length === 0)
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
/**
 * Default options
 */
var DEFAULT_RRF_K = 60;
var DEFAULT_K = 10;
/**
 * Hybrid retrieval combining semantic and BM25 search
 *
 * @param query - Search query
 * @param documents - All documents to search
 * @param options - Configuration options
 * @returns Combined and ranked results
 */
function hybridSearch(query_1, documents_1) {
    return __awaiter(this, arguments, void 0, function (query, documents, options) {
        var k, rrfK, denseResults, sparseResults, fused, results, scorer, baseScores, _i, results_1, mem, scored;
        if (options === void 0) { options = {}; }
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    k = options.k || DEFAULT_K;
                    rrfK = options.rrfK || DEFAULT_RRF_K;
                    return [4 /*yield*/, denseSearch(query, documents, k * 2)];
                case 1:
                    denseResults = _a.sent();
                    sparseResults = sparseSearch(query, documents, k * 2);
                    fused = reciprocalRankFusion(denseResults, sparseResults, rrfK, query);
                    results = fused.slice(0, k);
                    if (options.enableTemporalDecay) {
                        scorer = new temporal_decay_js_1.TemporalDecayScorer({
                            halfLifeDays: options.temporalHalfLifeDays || 30
                        });
                        baseScores = new Map();
                        for (_i = 0, results_1 = results; _i < results_1.length; _i++) {
                            mem = results_1[_i];
                            baseScores.set(mem.id, mem._finalScore || (mem.salience || 0.5));
                        }
                        // Apply temporal decay with contradictions
                        if (options.entityStore && options.relationshipStore) {
                            results = (0, temporal_decay_js_1.applyTemporalDecayWithContradictions)(results, baseScores, options.entityStore, options.relationshipStore, { halfLifeDays: options.temporalHalfLifeDays || 30 });
                        }
                        else {
                            scored = scorer.applyDecay(results);
                            scored.sort(function (a, b) { return b._combinedScore - a._combinedScore; });
                            results = scored;
                        }
                    }
                    return [2 /*return*/, results];
            }
        });
    });
}
/**
 * Dense retrieval using embeddings
 */
function denseSearch(query, documents, k) {
    return __awaiter(this, void 0, void 0, function () {
        var queryEmbedding, scored;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, (0, index_js_1.generateEmbedding)(query)];
                case 1:
                    queryEmbedding = _a.sent();
                    scored = documents.map(function (doc) {
                        var _a;
                        var sim = ((_a = doc.embedding) === null || _a === void 0 ? void 0 : _a.length)
                            ? cosineSimilarity(queryEmbedding, doc.embedding)
                            : 0;
                        return { doc: doc, sim: sim };
                    });
                    // Sort by similarity
                    scored.sort(function (a, b) { return b.sim - a.sim; });
                    // Return with rank
                    return [2 /*return*/, scored.slice(0, k).map(function (item, rank) { return ({
                            doc: item.doc,
                            rank: rank + 1,
                            score: item.sim
                        }); })];
            }
        });
    });
}
/**
 * Sparse retrieval using BM25
 */
function sparseSearch(query, documents, k) {
    var results = (0, bm25_js_1.bm25Search)(query, documents, { k: k });
    return results.map(function (doc, rank) { return ({
        doc: doc,
        rank: rank + 1,
        score: doc._bm25Score || 0
    }); });
}
/**
 * Deduplicate results based on content similarity
 * Removes near-duplicate memories before final scoring
 */
function deduplicateResults(memories, threshold) {
    if (threshold === void 0) { threshold = 0.85; }
    if (memories.length <= 1)
        return memories;
    var unique = [];
    var seenContent = new Set();
    for (var _i = 0, memories_1 = memories; _i < memories_1.length; _i++) {
        var m = memories_1[_i];
        // Normalize content for comparison
        var normalized = m.content.toLowerCase().replace(/\s+/g, ' ').trim();
        // Check for exact duplicate
        if (seenContent.has(normalized)) {
            continue;
        }
        // Check for near-duplicate (high similarity to existing)
        var isDuplicate = false;
        for (var _a = 0, unique_1 = unique; _a < unique_1.length; _a++) {
            var existing = unique_1[_a];
            var existingNorm = existing.content.toLowerCase().replace(/\s+/g, ' ').trim();
            var similarity = calculateSimilarity(normalized, existingNorm);
            if (similarity >= threshold) {
                // Keep the one with higher salience
                if ((m.salience || 0.5) > (existing.salience || 0.5)) {
                    // Replace the existing one
                    var idx = unique.indexOf(existing);
                    unique[idx] = m;
                }
                isDuplicate = true;
                break;
            }
        }
        if (!isDuplicate) {
            unique.push(m);
            seenContent.add(normalized);
        }
    }
    return unique;
}
/**
 * Simple word overlap similarity
 */
function calculateSimilarity(a, b) {
    var wordsA = new Set(a.split(/\s+/).filter(function (w) { return w.length > 2; }));
    var wordsB = new Set(b.split(/\s+/).filter(function (w) { return w.length > 2; }));
    if (wordsA.size === 0 || wordsB.size === 0)
        return 0;
    var intersection = 0;
    for (var _i = 0, wordsA_1 = wordsA; _i < wordsA_1.length; _i++) {
        var w = wordsA_1[_i];
        if (wordsB.has(w))
            intersection++;
    }
    return intersection / Math.min(wordsA.size, wordsB.size);
}
/**
 * Extract entities from query
 */
function extractQueryEntities(query) {
    var entities = [];
    // Known entities to look for
    var knownEntities = [
        'Phillip', 'KakāpōHiko', 'Kakāpō', 'Hiko',
        'Elev8Advisory', 'BrandForge', 'Muninn', 'OpenClaw',
        'Sammy Clemens', 'Charlie Babbage', 'Donna Paulsen',
        'Brisbane', 'Australia', 'React', 'Node.js', 'PostgreSQL',
        'SQLite', 'Ollama', 'Stripe', 'gateway', 'port',
        'priority', 'revenue', 'team', 'agents', 'projects'
    ];
    var lowerQuery = query.toLowerCase();
    for (var _i = 0, knownEntities_1 = knownEntities; _i < knownEntities_1.length; _i++) {
        var e = knownEntities_1[_i];
        if (lowerQuery.includes(e.toLowerCase())) {
            entities.push(e);
        }
    }
    return entities;
}
/**
 * Reciprocal Rank Fusion
 *
 * Combines rankings from multiple retrieval methods.
 * RRF score = sum(1 / (k + rank)) for each ranking where item appears
 */
function reciprocalRankFusion(denseResults, sparseResults, k, query) {
    if (k === void 0) { k = 60; }
    if (query === void 0) { query = ''; }
    // Map doc ID to accumulated RRF score
    var rrfScores = new Map();
    // Extract entities from query for boosting
    var queryEntities = extractQueryEntities(query);
    var useEntityBoost = queryEntities.length > 0;
    // Add dense scores
    for (var _i = 0, denseResults_1 = denseResults; _i < denseResults_1.length; _i++) {
        var _a = denseResults_1[_i], doc = _a.doc, rank = _a.rank;
        var rrfScore = 1 / (k + rank);
        var existing = rrfScores.get(doc.id);
        if (existing) {
            existing.score += rrfScore;
        }
        else {
            rrfScores.set(doc.id, { doc: doc, score: rrfScore });
        }
    }
    // Add sparse scores
    for (var _b = 0, sparseResults_1 = sparseResults; _b < sparseResults_1.length; _b++) {
        var _c = sparseResults_1[_b], doc = _c.doc, rank = _c.rank;
        var rrfScore = 1 / (k + rank);
        var existing = rrfScores.get(doc.id);
        if (existing) {
            existing.score += rrfScore;
        }
        else {
            rrfScores.set(doc.id, { doc: doc, score: rrfScore });
        }
    }
    // Convert to array and apply boosts
    var sorted = __spreadArray([], rrfScores.values(), true).sort(function (a, b) { return b.score - a.score; });
    // Apply entity-based boosting
    if (useEntityBoost) {
        sorted = sorted.map(function (s) {
            var docEntities = s.doc.entities || [];
            var entityBoost = 0;
            for (var _i = 0, queryEntities_1 = queryEntities; _i < queryEntities_1.length; _i++) {
                var qe = queryEntities_1[_i];
                for (var _a = 0, docEntities_1 = docEntities; _a < docEntities_1.length; _a++) {
                    var de = docEntities_1[_a];
                    if (de.toLowerCase().includes(qe.toLowerCase()) ||
                        qe.toLowerCase().includes(de.toLowerCase())) {
                        entityBoost += 0.3; // 30% boost per matching entity
                        break;
                    }
                }
            }
            return __assign(__assign({}, s), { score: s.score * (1 + entityBoost) });
        });
        // Re-sort after entity boost
        sorted.sort(function (a, b) { return b.score - a.score; });
    }
    // Apply salience boost
    var boosted = sorted.map(function (s) {
        var salience = s.doc.salience || 0.5;
        var boostFactor = salience * 2; // 0.8 → 1.6, 0.5 → 1.0, 0.3 → 0.6
        return __assign(__assign({}, s.doc), { _rrfScore: s.score, _finalScore: s.score * boostFactor });
    });
    // Sort by final score
    boosted.sort(function (a, b) { return (b._finalScore || 0) - (a._finalScore || 0); });
    // Deduplicate results
    var deduplicated = deduplicateResults(boosted);
    return deduplicated;
}
/**
 * Get retrieval scores breakdown for debugging
 */
function getRetrievalBreakdown(query_1, documents_1) {
    return __awaiter(this, arguments, void 0, function (query, documents, k) {
        var denseResults, sparseResults, fusedResults;
        if (k === void 0) { k = 5; }
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, denseSearch(query, documents, k * 2)];
                case 1:
                    denseResults = _a.sent();
                    sparseResults = sparseSearch(query, documents, k * 2);
                    fusedResults = reciprocalRankFusion(denseResults, sparseResults, 60, query);
                    return [2 /*return*/, {
                            query: query,
                            dense: denseResults.map(function (d) { return ({
                                id: d.doc.id,
                                content: d.doc.content.substring(0, 50) + '...',
                                similarity: d.score,
                                rank: d.rank
                            }); }),
                            sparse: sparseResults.map(function (s) { return ({
                                id: s.doc.id,
                                content: s.doc.content.substring(0, 50) + '...',
                                bm25: s.score,
                                rank: s.rank
                            }); }),
                            fused: fusedResults.slice(0, k).map(function (f) {
                                var denseRank = denseResults.findIndex(function (d) { return d.doc.id === f.id; });
                                var sparseRank = sparseResults.findIndex(function (s) { return s.doc.id === f.id; });
                                return {
                                    id: f.id,
                                    content: f.content.substring(0, 50) + '...',
                                    rrfScore: (denseRank >= 0 ? 1 / (60 + denseRank + 1) : 0) +
                                        (sparseRank >= 0 ? 1 / (60 + sparseRank + 1) : 0)
                                };
                            })
                        }];
            }
        });
    });
}
