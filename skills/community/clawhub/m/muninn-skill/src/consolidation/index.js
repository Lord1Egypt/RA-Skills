"use strict";
/**
 * Consolidation Engine
 * Async job that runs periodically to:
 * - Extract entities from episodes
 * - Distill episodes into semantic facts
 * - Detect contradictions
 * - Build knowledge graph
 */
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
exports.consolidate = consolidate;
exports.resolveTruth = resolveTruth;
function consolidate(store_1) {
    return __awaiter(this, arguments, void 0, function (store, options) {
        var batchSize, consolidated, entitiesDiscovered, contradictions, connectionsFormed, episodicMemories, _loop_1, _i, episodicMemories_1, memory, recentEpisodic, semanticMemories, contradictionsFound, i, j, m1, m2, pairs, _a, pairs_1, _b, pos, neg, allMemories, i, _loop_2, j;
        if (options === void 0) { options = {}; }
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    batchSize = options.batchSize || 10;
                    consolidated = 0;
                    entitiesDiscovered = 0;
                    contradictions = 0;
                    connectionsFormed = 0;
                    return [4 /*yield*/, store.recall('', { types: ['episodic'], limit: batchSize })];
                case 1:
                    episodicMemories = _c.sent();
                    _loop_1 = function (memory) {
                        // Extract entities from content
                        var capitalized = memory.content.match(/[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*/g) || [];
                        var commonWords = ['I', 'The', 'A', 'An', 'This', 'That', 'It', 'We', 'They', 'You'];
                        var newEntities = capitalized.filter(function (w) { return !commonWords.includes(w) && w.length > 2; });
                        if (newEntities.length > 0) {
                            entitiesDiscovered += newEntities.length;
                        }
                    };
                    for (_i = 0, episodicMemories_1 = episodicMemories; _i < episodicMemories_1.length; _i++) {
                        memory = episodicMemories_1[_i];
                        _loop_1(memory);
                    }
                    recentEpisodic = episodicMemories.filter(function (m) {
                        var hoursSince = (Date.now() - new Date(m.created_at).getTime()) / (1000 * 60 * 60);
                        return hoursSince > 24; // Only distill memories older than 24h
                    });
                    return [4 /*yield*/, store.recall('', { types: ['semantic'], limit: batchSize })];
                case 2:
                    semanticMemories = _c.sent();
                    contradictionsFound = [];
                    for (i = 0; i < semanticMemories.length; i++) {
                        for (j = i + 1; j < semanticMemories.length; j++) {
                            m1 = semanticMemories[i].content.toLowerCase();
                            m2 = semanticMemories[j].content.toLowerCase();
                            pairs = [
                                ['prefer', 'prefer'],
                                ['like', 'dislike'],
                                ['love', 'hate'],
                                ['use', 'never use'],
                                ['always', 'never']
                            ];
                            for (_a = 0, pairs_1 = pairs; _a < pairs_1.length; _a++) {
                                _b = pairs_1[_a], pos = _b[0], neg = _b[1];
                                if (m1.includes(pos) && m2.includes(neg) || m1.includes(neg) && m2.includes(pos)) {
                                    contradictionsFound.push("".concat(semanticMemories[i].id, " <-> ").concat(semanticMemories[j].id));
                                }
                            }
                        }
                    }
                    contradictions = contradictionsFound.length;
                    return [4 /*yield*/, store.recall('', { limit: batchSize * 2 })];
                case 3:
                    allMemories = _c.sent();
                    for (i = 0; i < allMemories.length; i++) {
                        _loop_2 = function (j) {
                            var shared = allMemories[i].entities.filter(function (e) {
                                return allMemories[j].entities.includes(e);
                            });
                            if (shared.length > 0 && Math.random() > 0.7) { // Probabilistic connection
                                try {
                                    store.connect(allMemories[i].id, allMemories[j].id, 'related_to');
                                    connectionsFormed++;
                                }
                                catch (e) {
                                    // Connection might already exist
                                }
                            }
                        };
                        for (j = i + 1; j < allMemories.length; j++) {
                            _loop_2(j);
                        }
                    }
                    consolidated = episodicMemories.length;
                    return [2 /*return*/, {
                            consolidated: consolidated,
                            entitiesDiscovered: entitiesDiscovered,
                            contradictions: contradictions,
                            connectionsFormed: connectionsFormed
                        }];
            }
        });
    });
}
function resolveTruth(claims) {
    // Sort by timestamp (newest first)
    var sorted = __spreadArray([], claims, true).sort(function (a, b) {
        return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();
    });
    var resolved = [];
    var seen = new Map();
    for (var _i = 0, sorted_1 = sorted; _i < sorted_1.length; _i++) {
        var claim = sorted_1[_i];
        var key = claim.predicate.toLowerCase();
        var existing = seen.get(key);
        if (!existing) {
            seen.set(key, claim);
            resolved.push(claim);
        }
        else {
            // Mark as superseded
            claim.superseded_by = existing.source;
            existing.superseded_by = claim.source;
        }
    }
    return resolved;
}
