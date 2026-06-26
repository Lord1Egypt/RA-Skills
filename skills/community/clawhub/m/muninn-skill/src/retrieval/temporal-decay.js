"use strict";
/**
 * Temporal Decay Scorer
 *
 * Applies exponential half-life decay to memory scores based on age.
 * Memories older than the half-life are penalized but never fully removed.
 *
 * Also handles contradiction chains - when an entity has been superseded,
 * the entire chain is boosted to provide context.
 *
 * Based on: "Temporal RAG: Why RAG Always Gets 'When' Questions Wrong" (SOTA Blog, Jan 2026)
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
exports.defaultTemporalScorer = exports.TemporalDecayScorer = void 0;
exports.getContradictionChain = getContradictionChain;
exports.applyTemporalDecayWithContradictions = applyTemporalDecayWithContradictions;
exports.getTemporalScore = getTemporalScore;
var DEFAULT_OPTIONS = {
    halfLifeDays: 30,
    minScore: 0.1,
    contradictionBoost: 1.5
};
/**
 * Calculate decay rate from half-life
 * λ = ln(2) / half_life_days
 */
function calculateDecayRate(halfLifeDays) {
    return Math.log(2) / halfLifeDays;
}
/**
 * Temporal Decay Scorer class
 */
var TemporalDecayScorer = /** @class */ (function () {
    function TemporalDecayScorer(options) {
        if (options === void 0) { options = {}; }
        this.options = __assign(__assign({}, DEFAULT_OPTIONS), options);
        this.decayRate = calculateDecayRate(this.options.halfLifeDays);
    }
    /**
     * Calculate temporal score for a memory
     * Score = e^(-λt) where t is age in days
     *
     * @param memory - The memory to score
     * @param referenceDate - Reference date for calculating age (default: now)
     * @returns Score between minScore and 1.0
     */
    TemporalDecayScorer.prototype.score = function (memory, referenceDate) {
        if (referenceDate === void 0) { referenceDate = new Date(); }
        // Get memory timestamp (use created_at if no timestamp)
        var memTime = memory.timestamp
            ? new Date(memory.timestamp)
            : new Date(memory.created_at);
        // Calculate age in days
        var ageMs = referenceDate.getTime() - memTime.getTime();
        var ageDays = ageMs / (1000 * 60 * 60 * 24);
        // Calculate exponential decay
        var temporalScore = Math.exp(-this.decayRate * ageDays);
        // Apply minimum floor
        return Math.max(temporalScore, this.options.minScore);
    };
    /**
     * Get the decay rate
     */
    TemporalDecayScorer.prototype.getDecayRate = function () {
        return this.decayRate;
    };
    /**
     * Get the half-life in days
     */
    TemporalDecayScorer.prototype.getHalfLifeDays = function () {
        return this.options.halfLifeDays;
    };
    /**
     * Apply temporal decay to an array of memories
     *
     * @param memories - Array of memories with existing scores
     * @param scoreProperty - Property name containing the base score (default: '_finalScore')
     * @param referenceDate - Reference date for calculating age
     * @returns Memories with temporal scores applied
     */
    TemporalDecayScorer.prototype.applyDecay = function (memories, scoreProperty, referenceDate) {
        var _this = this;
        if (scoreProperty === void 0) { scoreProperty = '_finalScore'; }
        if (referenceDate === void 0) { referenceDate = new Date(); }
        return memories.map(function (mem) {
            var temporalScore = _this.score(mem, referenceDate);
            var baseScore = mem[scoreProperty] || 1.0;
            var combinedScore = baseScore * temporalScore;
            return __assign(__assign({}, mem), { _temporalScore: temporalScore, _combinedScore: combinedScore });
        });
    };
    /**
     * Sort memories by combined score (base score * temporal decay)
     */
    TemporalDecayScorer.prototype.sortByTemporalScore = function (memories, scoreProperty) {
        if (scoreProperty === void 0) { scoreProperty = '_finalScore'; }
        var scored = this.applyDecay(memories, scoreProperty);
        scored.sort(function (a, b) { return b._combinedScore - a._combinedScore; });
        return scored;
    };
    return TemporalDecayScorer;
}());
exports.TemporalDecayScorer = TemporalDecayScorer;
/**
 * Check if an entity has contradictions and get the chain
 */
function getContradictionChain(entityStore, relationshipStore, entityName) {
    var entity = entityStore.findEntity(entityName);
    if (!entity) {
        return { superseded: [] };
    }
    // Get all relationships for this entity
    var outgoing = relationshipStore.getBySource(entity.id);
    var incoming = relationshipStore.getByTarget(entity.id);
    // Find contradictions (relationships with supersededBy set)
    var superseded = [];
    var current;
    for (var _i = 0, _a = __spreadArray(__spreadArray([], outgoing, true), incoming, true); _i < _a.length; _i++) {
        var rel = _a[_i];
        if (rel.supersededBy) {
            // This relationship has been superseded
            var supersededRel = relationshipStore.getById(rel.supersededBy);
            if (supersededRel) {
                superseded.push(supersededRel);
            }
        }
        else {
            // This is the current relationship
            if (!current || new Date(rel.timestamp) > new Date(current.timestamp)) {
                current = rel;
            }
        }
    }
    return { current: current, superseded: superseded };
}
/**
 * Apply temporal decay with contradiction handling
 *
 * @param memories - Base memories to score
 * @param baseScores - Map of memory ID to base score
 * @param entityStore - Entity store for contradiction lookup
 * @param relationshipStore - Relationship store for contradiction lookup
 * @param options - Temporal decay options
 * @returns Memories with temporal scores and contradiction boosts applied
 */
function applyTemporalDecayWithContradictions(memories, baseScores, entityStore, relationshipStore, options) {
    if (options === void 0) { options = {}; }
    var scorer = new TemporalDecayScorer(options);
    var referenceDate = new Date();
    // First, collect all entities that have contradictions
    var contradictionEntities = new Map();
    for (var _i = 0, memories_1 = memories; _i < memories_1.length; _i++) {
        var mem = memories_1[_i];
        for (var _a = 0, _b = mem.entities; _a < _b.length; _a++) {
            var entityName = _b[_a];
            if (!contradictionEntities.has(entityName)) {
                var chain = getContradictionChain(entityStore, relationshipStore, entityName);
                if (chain.superseded.length > 0) {
                    contradictionEntities.set(entityName, chain);
                }
            }
        }
    }
    // Apply temporal decay and contradiction boosts
    var scored = memories.map(function (mem) {
        var baseScore = baseScores.get(mem.id) || (mem.salience || 0.5);
        var temporalScore = scorer.score(mem, referenceDate);
        // Check if this memory's entities have contradictions
        var hasContradiction = false;
        for (var _i = 0, _a = mem.entities; _i < _a.length; _i++) {
            var entityName = _a[_i];
            if (contradictionEntities.has(entityName)) {
                hasContradiction = true;
                break;
            }
        }
        // Apply boost if entity has contradictions
        var contradictionBoost = hasContradiction ? (options.contradictionBoost || DEFAULT_OPTIONS.contradictionBoost) : 1.0;
        var finalScore = baseScore * temporalScore * contradictionBoost;
        return __assign(__assign({}, mem), { _baseScore: baseScore, _temporalScore: temporalScore, _contradictionBoost: contradictionBoost, _finalScore: finalScore, _hasContradiction: hasContradiction });
    });
    // Sort by final score
    scored.sort(function (a, b) { return (b._finalScore || 0) - (a._finalScore || 0); });
    // Also collect superseded memories from contradiction chains
    var additionalMemories = [];
    for (var _c = 0, contradictionEntities_1 = contradictionEntities; _c < contradictionEntities_1.length; _c++) {
        var _d = contradictionEntities_1[_c], chain = _d[1];
        for (var _e = 0, _f = chain.superseded; _e < _f.length; _e++) {
            var superseded = _f[_e];
            // Find memories related to this superseded relationship
            // For now, we just flag them - full implementation would retrieve the memories
        }
    }
    return scored;
}
/**
 * Default scorer instance with 30-day half-life
 */
exports.defaultTemporalScorer = new TemporalDecayScorer();
/**
 * Quick score function for simple use cases
 */
function getTemporalScore(memory, halfLifeDays) {
    if (halfLifeDays === void 0) { halfLifeDays = 30; }
    var scorer = new TemporalDecayScorer({ halfLifeDays: halfLifeDays });
    return scorer.score(memory);
}
