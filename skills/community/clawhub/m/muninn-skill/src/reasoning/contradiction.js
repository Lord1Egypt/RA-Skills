"use strict";
/**
 * Contradiction Detection and Temporal Reasoning
 * Detects when new information contradicts old, tracks temporal history
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.detectContradiction = detectContradiction;
exports.getEntityContradictions = getEntityContradictions;
exports.getTemporalHistory = getTemporalHistory;
exports.synthesizeTemporalAnswer = synthesizeTemporalAnswer;
exports.synthesizeContradictionAnswer = synthesizeContradictionAnswer;
exports.getSupersededRelationships = getSupersededRelationships;
exports.isCurrentValue = isCurrentValue;
exports.getValueWithHistory = getValueWithHistory;
/**
 * Check if a new relationship contradicts existing ones
 */
function detectContradiction(relationshipStore, sourceEntityId, type, newValue) {
    // Get current (non-superseded) relationship
    var current = relationshipStore.getCurrent(sourceEntityId, type);
    if (!current)
        return null;
    // Check if values differ
    if (newValue && current.value !== newValue) {
        return current;
    }
    return null;
}
/**
 * Get all contradictions involving an entity
 */
function getEntityContradictions(relationshipStore, entityStore, entityName) {
    var entity = entityStore.findEntity(entityName);
    if (!entity)
        return [];
    var contradictions = relationshipStore.getContradictions();
    return contradictions
        .filter(function (c) { return c.superseded.source === entity.id || c.superseded.target === entity.id; })
        .map(function (c) { return ({
        current: c.current,
        superseded: c.superseded,
        timestamp: c.current.timestamp,
        sessionId: c.current.sessionId
    }); });
}
/**
 * Get temporal history for an entity's relationship
 * Returns chronological list of all changes
 */
function getTemporalHistory(relationshipStore, entityStore, entityName, relationshipType) {
    var entity = entityStore.findEntity(entityName);
    if (!entity)
        return [];
    var history = relationshipStore.getHistory(entity.id, relationshipType);
    var changes = [];
    var previousValue;
    for (var _i = 0, history_1 = history; _i < history_1.length; _i++) {
        var rel = history_1[_i];
        // Get the target entity name for context
        var targetEntity = entityStore.getById(rel.target);
        var targetName = (targetEntity === null || targetEntity === void 0 ? void 0 : targetEntity.name) || rel.target;
        if (rel.value !== previousValue) {
            changes.push({
                entity: targetName,
                relationshipType: rel.type,
                oldValue: previousValue,
                newValue: rel.value,
                timestamp: rel.timestamp,
                sessionId: rel.sessionId
            });
        }
        previousValue = rel.value;
    }
    return changes;
}
/**
 * Synthesize a temporal answer for a question about an entity
 */
function synthesizeTemporalAnswer(relationshipStore, entityStore, entityName, relationshipType) {
    return __awaiter(this, void 0, void 0, function () {
        var history, timeline;
        return __generator(this, function (_a) {
            history = getTemporalHistory(relationshipStore, entityStore, entityName, relationshipType);
            if (history.length === 0) {
                return [2 /*return*/, "No temporal history found for ".concat(entityName)];
            }
            timeline = history.map(function (h) {
                var when = new Date(h.timestamp).toLocaleDateString();
                var change = h.oldValue
                    ? "changed from ".concat(h.oldValue, " to ").concat(h.newValue)
                    : "set to ".concat(h.newValue);
                return "- ".concat(when, " (").concat(h.sessionId, "): ").concat(change);
            }).join('\n');
            return [2 /*return*/, "Timeline for ".concat(entityName, ":\n").concat(timeline)];
        });
    });
}
/**
 * Synthesize a contradiction-aware answer
 */
function synthesizeContradictionAnswer(relationshipStore, entityStore, entityName, question) {
    var entity = entityStore.findEntity(entityName);
    if (!entity) {
        return "Entity not found: ".concat(entityName);
    }
    // Get current value
    var relationships = relationshipStore.getBySource(entity.id);
    var current = relationships.find(function (r) { return !r.supersededBy; });
    if (!current) {
        return "No current relationship found for ".concat(entityName);
    }
    // Get contradictions
    var contradictions = getEntityContradictions(relationshipStore, entityStore, entityName);
    var targetEntity = entityStore.getById(current.target);
    var targetName = (targetEntity === null || targetEntity === void 0 ? void 0 : targetEntity.name) || current.target;
    var answer = "Current value for ".concat(entityName, ": ").concat(current.type, " ").concat(targetName);
    if (current.value) {
        answer += " = ".concat(current.value);
    }
    if (contradictions.length > 0) {
        answer += "\n\nHistorical changes:";
        for (var _i = 0, contradictions_1 = contradictions; _i < contradictions_1.length; _i++) {
            var c = contradictions_1[_i];
            var supersededTarget = entityStore.getById(c.superseded.target);
            answer += "\n- Previously: ".concat(c.superseded.type, " ").concat((supersededTarget === null || supersededTarget === void 0 ? void 0 : supersededTarget.name) || c.superseded.target);
            if (c.superseded.value) {
                answer += " = ".concat(c.superseded.value);
            }
            answer += " (".concat(new Date(c.superseded.timestamp).toLocaleDateString(), ")");
        }
    }
    return answer;
}
/**
 * Get all superseded relationships for an entity
 */
function getSupersededRelationships(relationshipStore, entityStore, entityName) {
    var entity = entityStore.findEntity(entityName);
    if (!entity)
        return [];
    var all = relationshipStore.getBySource(entity.id);
    return all.filter(function (r) { return r.supersededBy !== undefined; });
}
/**
 * Check if a specific value is current (not superseded)
 */
function isCurrentValue(relationshipStore, entityStore, entityName, relationshipType, value) {
    var entity = entityStore.findEntity(entityName);
    if (!entity)
        return false;
    var current = relationshipStore.getCurrent(entity.id, relationshipType);
    return (current === null || current === void 0 ? void 0 : current.value) === value;
}
/**
 * Get latest value with history
 */
function getValueWithHistory(relationshipStore, entityStore, entityName, relationshipType) {
    var entity = entityStore.findEntity(entityName);
    if (!entity) {
        return { history: [] };
    }
    var history = relationshipStore.getHistory(entity.id, relationshipType);
    var result = {
        history: []
    };
    for (var _i = 0, history_2 = history; _i < history_2.length; _i++) {
        var rel = history_2[_i];
        if (rel.value) {
            result.history.push({
                value: rel.value,
                timestamp: rel.timestamp,
                superseded: rel.supersededBy !== undefined
            });
            if (!rel.supersededBy) {
                result.current = rel.value;
            }
        }
    }
    return result;
}
