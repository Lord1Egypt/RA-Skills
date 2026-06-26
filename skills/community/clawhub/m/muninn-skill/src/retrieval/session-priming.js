"use strict";
/**
 * Session Priming (Working Memory Buffer)
 *
 * At session start, preloads "stale but important" entities - those
 * mentioned frequently in past sessions but not recently.
 *
 * This ensures continuity between sessions by surfacing relevant
 * context that would otherwise be forgotten.
 *
 * Based on: MemGPT/Letta architecture for working memory
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
exports.findStaleImportantEntities = findStaleImportantEntities;
exports.cohesionQuery = cohesionQuery;
exports.simpleCohesionQuery = simpleCohesionQuery;
exports.calculateSessionCohesion = calculateSessionCohesion;
var DEFAULT_OPTIONS = {
    minMentions: 3,
    staleHours: 48,
    maxEntities: 5,
    memoriesPerEntity: 2
};
/**
 * Query for stale-but-important entities
 * Returns entities that were frequently referenced but haven't been
 * mentioned recently - good candidates for session context
 */
function findStaleImportantEntities(entityStore_1) {
    return __awaiter(this, arguments, void 0, function (entityStore, options) {
        var opts, now, staleThreshold, allEntities, staleImportant, _i, allEntities_1, entity, lastSeen, hoursSince;
        if (options === void 0) { options = {}; }
        return __generator(this, function (_a) {
            opts = __assign(__assign({}, DEFAULT_OPTIONS), options);
            now = new Date();
            staleThreshold = new Date(now.getTime() - opts.staleHours * 60 * 60 * 1000);
            allEntities = entityStore.getAll();
            staleImportant = [];
            for (_i = 0, allEntities_1 = allEntities; _i < allEntities_1.length; _i++) {
                entity = allEntities_1[_i];
                lastSeen = new Date(entity.lastSeen);
                hoursSince = (now.getTime() - lastSeen.getTime()) / (1000 * 60 * 60);
                // Check if stale AND important
                if (hoursSince >= opts.staleHours && entity.mentions >= opts.minMentions) {
                    staleImportant.push({
                        entity: {
                            id: entity.id,
                            name: entity.name,
                            type: entity.type,
                            mentions: entity.mentions
                        },
                        lastMentioned: lastSeen,
                        hoursSinceMention: hoursSince
                    });
                }
            }
            // Sort by importance (mentions * recency)
            staleImportant.sort(function (a, b) {
                // Score: more mentions = more important, but stale = needs priming
                var scoreA = a.entity.mentions * (1 / (1 + a.hoursSinceMention / 24));
                var scoreB = b.entity.mentions * (1 / (1 + b.hoursSinceMention / 24));
                return scoreB - scoreA;
            });
            return [2 /*return*/, staleImportant.slice(0, opts.maxEntities)];
        });
    });
}
/**
 * Get all sessions an entity was mentioned in
 */
function getEntitySessions(relationshipStore, entityId) {
    var sessions = new Set();
    // Check as source
    var asSource = relationshipStore.getBySource(entityId);
    for (var _i = 0, asSource_1 = asSource; _i < asSource_1.length; _i++) {
        var rel = asSource_1[_i];
        if (rel.sessionId) {
            sessions.add(rel.sessionId);
        }
    }
    // Check as target
    var asTarget = relationshipStore.getByTarget(entityId);
    for (var _a = 0, asTarget_1 = asTarget; _a < asTarget_1.length; _a++) {
        var rel = asTarget_1[_a];
        if (rel.sessionId) {
            sessions.add(rel.sessionId);
        }
    }
    return Array.from(sessions);
}
/**
 * Cohesion Query - main function for session priming
 *
 * Finds entities that are frequently mentioned across sessions but have
 * gone stale, then retrieves recent memories about them.
 *
 * @param entityStore - Entity store for finding stale-important entities
 * @param relationshipStore - Relationship store for session tracking
 * @param recallFn - Function to recall memories (context, options) => Promise<Memory[]>
 * @param options - Configuration options
 * @returns Array of primed memories for session context
 */
function cohesionQuery(entityStore_1, relationshipStore_1, recallFn_1) {
    return __awaiter(this, arguments, void 0, function (entityStore, relationshipStore, recallFn, options) {
        var opts, staleEntities, primedMemories, seenIds, _i, staleEntities_1, staleEntity, memories, _a, memories_1, mem, entityNames, summary;
        if (options === void 0) { options = {}; }
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    opts = __assign(__assign({}, DEFAULT_OPTIONS), options);
                    return [4 /*yield*/, findStaleImportantEntities(entityStore, opts)];
                case 1:
                    staleEntities = _b.sent();
                    if (staleEntities.length === 0) {
                        return [2 /*return*/, {
                                primedMemories: [],
                                staleEntities: [],
                                summary: 'No stale-but-important entities found for session priming.'
                            }];
                    }
                    primedMemories = [];
                    seenIds = new Set();
                    _i = 0, staleEntities_1 = staleEntities;
                    _b.label = 2;
                case 2:
                    if (!(_i < staleEntities_1.length)) return [3 /*break*/, 5];
                    staleEntity = staleEntities_1[_i];
                    return [4 /*yield*/, recallFn(staleEntity.entity.name, {
                            limit: opts.memoriesPerEntity
                        })];
                case 3:
                    memories = _b.sent();
                    for (_a = 0, memories_1 = memories; _a < memories_1.length; _a++) {
                        mem = memories_1[_a];
                        if (!seenIds.has(mem.id)) {
                            seenIds.add(mem.id);
                            primedMemories.push(mem);
                        }
                    }
                    _b.label = 4;
                case 4:
                    _i++;
                    return [3 /*break*/, 2];
                case 5:
                    entityNames = staleEntities.map(function (e) { return e.entity.name; }).join(', ');
                    summary = "Session Priming: Preloaded ".concat(primedMemories.length, " memories about stale entities (").concat(entityNames, ")");
                    return [2 /*return*/, {
                            primedMemories: primedMemories,
                            staleEntities: staleEntities,
                            summary: summary
                        }];
            }
        });
    });
}
/**
 * Simple cohesion query that works with memory store
 *
 * @param entityStore - Entity store
 * @param relationshipStore - Relationship store
 * @param memories - All available memories
 * @param options - Configuration options
 * @returns Primed memories
 */
function simpleCohesionQuery(entityStore_1, relationshipStore_1, memories_2) {
    return __awaiter(this, arguments, void 0, function (entityStore, relationshipStore, memories, options) {
        var opts, staleEntities, primedMemories, seenIds, _i, staleEntities_2, staleEntity, entityName, _a, memories_3, mem, memEntities;
        if (options === void 0) { options = {}; }
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    opts = __assign(__assign({}, DEFAULT_OPTIONS), options);
                    return [4 /*yield*/, findStaleImportantEntities(entityStore, opts)];
                case 1:
                    staleEntities = _b.sent();
                    if (staleEntities.length === 0) {
                        return [2 /*return*/, { primedMemories: [], staleEntities: [] }];
                    }
                    primedMemories = [];
                    seenIds = new Set();
                    for (_i = 0, staleEntities_2 = staleEntities; _i < staleEntities_2.length; _i++) {
                        staleEntity = staleEntities_2[_i];
                        entityName = staleEntity.entity.name.toLowerCase();
                        // Find memories containing this entity
                        for (_a = 0, memories_3 = memories; _a < memories_3.length; _a++) {
                            mem = memories_3[_a];
                            if (seenIds.has(mem.id))
                                continue;
                            memEntities = mem.entities.map(function (e) { return e.toLowerCase(); });
                            if (memEntities.includes(entityName)) {
                                seenIds.add(mem.id);
                                // Boost salience for primed memories
                                primedMemories.push(__assign(__assign({}, mem), { salience: Math.min(1.0, (mem.salience || 0.5) * 1.5) // 50% boost
                                 }));
                            }
                        }
                    }
                    // Sort by boosted salience
                    primedMemories.sort(function (a, b) { return (b.salience || 0.5) - (a.salience || 0.5); });
                    return [2 /*return*/, {
                            primedMemories: primedMemories,
                            staleEntities: staleEntities
                        }];
            }
        });
    });
}
/**
 * Get session cohesion score
 * Measures how well connected the current session is to past sessions
 */
function calculateSessionCohesion(currentSessionEntities, staleEntities) {
    if (currentSessionEntities.length === 0 || staleEntities.length === 0) {
        return 0;
    }
    var currentSet = new Set(currentSessionEntities.map(function (e) { return e.toLowerCase(); }));
    var overlap = 0;
    for (var _i = 0, staleEntities_3 = staleEntities; _i < staleEntities_3.length; _i++) {
        var stale = staleEntities_3[_i];
        if (currentSet.has(stale.entity.name.toLowerCase())) {
            overlap++;
        }
    }
    return overlap / staleEntities.length;
}
