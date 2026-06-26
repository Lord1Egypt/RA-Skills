"use strict";
/**
 * Spreading Activation via Knowledge Graph
 *
 * Implements 2-hop graph traversal to expand initial retrieval results
 * with connected entities from the knowledge graph.
 *
 * Based on: arXiv:2512.15922 - "Leveraging Spreading Activation for Improved Document Retrieval"
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.spreadActivation = spreadActivation;
exports.spreadActivationSimple = spreadActivationSimple;
var DEFAULT_OPTIONS = {
    maxHops: 2,
    decayFactor: 0.5,
    maxNeighbors: 10,
    minActivation: 0.25
};
/**
 * Get all neighbors (connected entities) for a given entity
 */
function getNeighbors(entity, relationshipStore, maxNeighbors) {
    var neighbors = [];
    // Get outgoing relationships (as source)
    var outgoing = relationshipStore.getBySource(entity.id);
    for (var _i = 0, outgoing_1 = outgoing; _i < outgoing_1.length; _i++) {
        var rel = outgoing_1[_i];
        if (rel.supersededBy)
            continue;
        neighbors.push({
            entityId: rel.target,
            entityName: rel.value || rel.target,
            activation: 1.0,
            relationship: rel
        });
    }
    // Get incoming relationships (as target)
    var incoming = relationshipStore.getByTarget(entity.id);
    for (var _a = 0, incoming_1 = incoming; _a < incoming_1.length; _a++) {
        var rel = incoming_1[_a];
        if (rel.supersededBy)
            continue;
        neighbors.push({
            entityId: rel.source,
            entityName: rel.source,
            activation: 1.0,
            relationship: rel
        });
    }
    // Sort by confidence and limit
    neighbors.sort(function (a, b) { return b.relationship.confidence - a.relationship.confidence; });
    return neighbors.slice(0, maxNeighbors);
}
/**
 * Recursive spreading activation from an entity
 */
function spreadFromEntity(entity, currentActivation, currentHop, options, activated, relationshipStore, entityStore) {
    return __awaiter(this, void 0, void 0, function () {
        var neighbors, _i, neighbors_1, neighbor, newActivation, existing, neighborEntity;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    // Base cases
                    if (currentHop > options.maxHops)
                        return [2 /*return*/];
                    if (currentActivation < options.minActivation)
                        return [2 /*return*/];
                    neighbors = getNeighbors(entity, relationshipStore, options.maxNeighbors);
                    _i = 0, neighbors_1 = neighbors;
                    _a.label = 1;
                case 1:
                    if (!(_i < neighbors_1.length)) return [3 /*break*/, 4];
                    neighbor = neighbors_1[_i];
                    newActivation = currentActivation * options.decayFactor;
                    // Skip if below threshold
                    if (newActivation < options.minActivation)
                        return [3 /*break*/, 3];
                    existing = activated.get(neighbor.entityId);
                    if (!(!existing || newActivation > existing.activation)) return [3 /*break*/, 3];
                    activated.set(neighbor.entityId, {
                        activation: newActivation,
                        sourceRel: neighbor.relationship
                    });
                    neighborEntity = entityStore.findEntity(neighbor.entityName);
                    if (!neighborEntity) return [3 /*break*/, 3];
                    return [4 /*yield*/, spreadFromEntity(neighborEntity, newActivation, currentHop + 1, options, activated, relationshipStore, entityStore)];
                case 2:
                    _a.sent();
                    _a.label = 3;
                case 3:
                    _i++;
                    return [3 /*break*/, 1];
                case 4: return [2 /*return*/];
            }
        });
    });
}
/**
 * Get memories for activated entities
 */
function getActivatedMemories(activated, entityStore, relationshipStore, allMemories, minActivation) {
    return __awaiter(this, void 0, void 0, function () {
        var activatedMemories, memoryByEntity, _i, allMemories_1, mem, _a, _b, entityName, key, seenMemoryIds, _c, activated_1, _d, entityId, activation, entity, _e, allMemories_2, mem, memEntities;
        return __generator(this, function (_f) {
            activatedMemories = [];
            memoryByEntity = new Map();
            for (_i = 0, allMemories_1 = allMemories; _i < allMemories_1.length; _i++) {
                mem = allMemories_1[_i];
                for (_a = 0, _b = mem.entities; _a < _b.length; _a++) {
                    entityName = _b[_a];
                    key = entityName.toLowerCase();
                    if (!memoryByEntity.has(key)) {
                        memoryByEntity.set(key, []);
                    }
                    memoryByEntity.get(key).push(mem);
                }
            }
            seenMemoryIds = new Set();
            for (_c = 0, activated_1 = activated; _c < activated_1.length; _c++) {
                _d = activated_1[_c], entityId = _d[0], activation = _d[1].activation;
                if (activation < minActivation)
                    continue;
                // Skip if this is a memory ID (starts with m_)
                if (entityId.startsWith('m_'))
                    continue;
                entity = entityStore.getById(entityId);
                if (!entity) {
                    entity = entityStore.getByName(entityId);
                }
                if (!entity) {
                    entity = entityStore.findEntity(entityId);
                }
                if (entity) {
                    // Find memories containing this entity
                    for (_e = 0, allMemories_2 = allMemories; _e < allMemories_2.length; _e++) {
                        mem = allMemories_2[_e];
                        if (seenMemoryIds.has(mem.id))
                            continue;
                        memEntities = mem.entities.map(function (e) { return e.toLowerCase(); });
                        if (memEntities.includes(entity.name.toLowerCase())) {
                            seenMemoryIds.add(mem.id);
                            activatedMemories.push(__assign(__assign({}, mem), { salience: Math.max(mem.salience || 0.5, activation) // Boost by activation
                             }));
                        }
                    }
                }
            }
            return [2 /*return*/, activatedMemories];
        });
    });
}
/**
 * Merge initial results with activated neighbors, boosting by activation score
 */
function mergeWithActivation(initialResults, activatedMemories, options) {
    var resultMap = new Map();
    // Add initial results
    for (var _i = 0, initialResults_1 = initialResults; _i < initialResults_1.length; _i++) {
        var mem = initialResults_1[_i];
        resultMap.set(mem.id, __assign(__assign({}, mem), { _activationBoost: 1.0 }));
    }
    // Merge activated memories
    for (var _a = 0, activatedMemories_1 = activatedMemories; _a < activatedMemories_1.length; _a++) {
        var mem = activatedMemories_1[_a];
        var existing = resultMap.get(mem.id);
        if (!existing) {
            // New memory from spreading activation
            var boost = Math.max(mem.salience || 0.5, 0.25);
            resultMap.set(mem.id, __assign(__assign({}, mem), { _activationBoost: boost }));
        }
        else {
            // Already in results - boost if activation is higher
            existing._activationBoost = Math.max(existing._activationBoost, mem.salience || 0.5);
        }
    }
    // Sort by activation boost (descending), then by original salience
    var results = Array.from(resultMap.values());
    results.sort(function (a, b) {
        if (Math.abs(b._activationBoost - a._activationBoost) > 0.1) {
            return b._activationBoost - a._activationBoost;
        }
        return (b.salience || 0.5) - (a.salience || 0.5);
    });
    return results;
}
/**
 * Main spreading activation function
 *
 * Takes initial retrieval results and expands them via 2-hop graph traversal
 * to capture related entities that weren't in the initial query results.
 *
 * @param initialResults - Initial BM25 + Vector search results
 * @param relationshipStore - The knowledge graph relationship store
 * @param entityStore - The entity store
 * @param allMemories - All available memories for finding neighbor memories
 * @param options - Configuration options
 * @returns Expanded results with graph neighbors
 */
function spreadActivation(initialResults_2, relationshipStore_1, entityStore_1, allMemories_3) {
    return __awaiter(this, arguments, void 0, function (initialResults, relationshipStore, entityStore, allMemories, options) {
        var opts, activated, _i, initialResults_3, mem, _a, _b, entityName, entity, activatedMemories, merged;
        if (options === void 0) { options = {}; }
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    opts = __assign(__assign({}, DEFAULT_OPTIONS), options);
                    if (initialResults.length === 0) {
                        return [2 /*return*/, []];
                    }
                    console.log("[SpreadingActivation] Starting with ".concat(initialResults.length, " initial results"));
                    activated = new Map();
                    _i = 0, initialResults_3 = initialResults;
                    _c.label = 1;
                case 1:
                    if (!(_i < initialResults_3.length)) return [3 /*break*/, 6];
                    mem = initialResults_3[_i];
                    // Add initial memory with activation 1.0
                    activated.set(mem.id, { activation: 1.0, sourceRel: null });
                    _a = 0, _b = mem.entities;
                    _c.label = 2;
                case 2:
                    if (!(_a < _b.length)) return [3 /*break*/, 5];
                    entityName = _b[_a];
                    entity = entityStore.findEntity(entityName);
                    if (!entity) return [3 /*break*/, 4];
                    return [4 /*yield*/, spreadFromEntity(entity, 1.0, // Initial activation
                        1, // First hop
                        opts, activated, relationshipStore, entityStore)];
                case 3:
                    _c.sent();
                    _c.label = 4;
                case 4:
                    _a++;
                    return [3 /*break*/, 2];
                case 5:
                    _i++;
                    return [3 /*break*/, 1];
                case 6:
                    console.log("[SpreadingActivation] Activated ".concat(activated.size, " entities"));
                    return [4 /*yield*/, getActivatedMemories(activated, entityStore, relationshipStore, allMemories, opts.minActivation)];
                case 7:
                    activatedMemories = _c.sent();
                    console.log("[SpreadingActivation] Found ".concat(activatedMemories.length, " neighbor memories"));
                    merged = mergeWithActivation(initialResults, activatedMemories, opts);
                    console.log("[SpreadingActivation] Returning ".concat(merged.length, " total results"));
                    return [2 /*return*/, merged];
            }
        });
    });
}
/**
 * Simple version that only uses relationship store (for compatibility)
 */
function spreadActivationSimple(initialResults_2, relationshipStore_1) {
    return __awaiter(this, arguments, void 0, function (initialResults, relationshipStore, options) {
        var opts;
        if (options === void 0) { options = {}; }
        return __generator(this, function (_a) {
            opts = __assign(__assign({}, DEFAULT_OPTIONS), options);
            if (initialResults.length === 0) {
                return [2 /*return*/, []];
            }
            // For simple version, we return initial results with a flag
            // Full version needs entity store for proper implementation
            return [2 /*return*/, initialResults];
        });
    });
}
