"use strict";
/**
 * Contradiction Detection Module
 *
 * Identifies conflicting facts and resolves by:
 * - Detecting semantic contradictions (not just keyword matches)
 * - Resolving by timestamp (newer wins)
 * - Flagging ambiguous cases for review
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
exports.detectContradiction = detectContradiction;
exports.scanContradictions = scanContradictions;
exports.getResolvedValue = getResolvedValue;
// Patterns that indicate preference/opinion (prone to change)
var preferencePatterns = [
    /prefer(s|red|ence)?/i,
    /want(s|ed)?/i,
    /like(s|d)?/i,
    /hate(s|d)?/i,
    /focus(ing|ed)?/i,
    /priority/i,
    /target/i,
    /goal/i
];
// Patterns that indicate a change/update
var changeIndicators = [
    /actually/i,
    /now/i,
    /updated/i,
    /changed/i,
    /back to/i,
    /instead/i,
    /revised/i,
    /new/i
];
// Negation patterns
var negationPatterns = [
    /not\s+(anymore|now)/i,
    /don'?t\s+(want|like|prefer)/i,
    /no\s+longer/i,
    /stopped/i
];
/**
 * Check if two memories might contradict each other
 */
function detectContradiction(mem1, mem2) {
    return __awaiter(this, void 0, void 0, function () {
        var sharedEntities, mem1IsPreference, mem2IsPreference, mem1HasNegation, mem2HasNegation, mem1HasChange, mem2HasChange, content1Lower, content2Lower, numericContradiction, priorityContradiction, m1Time, m2Time, winner, resolution, confidence, conflict;
        return __generator(this, function (_a) {
            // Skip if same memory
            if (mem1.id === mem2.id)
                return [2 /*return*/, null];
            // Only check semantic memories for contradictions
            if (mem1.type !== 'semantic' || mem2.type !== 'semantic')
                return [2 /*return*/, null];
            sharedEntities = mem1.entities.filter(function (e) { return mem2.entities.includes(e); });
            if (sharedEntities.length === 0)
                return [2 /*return*/, null];
            mem1IsPreference = preferencePatterns.some(function (p) { return p.test(mem1.content); });
            mem2IsPreference = preferencePatterns.some(function (p) { return p.test(mem2.content); });
            if (!mem1IsPreference && !mem2IsPreference)
                return [2 /*return*/, null];
            mem1HasNegation = negationPatterns.some(function (p) { return p.test(mem1.content); });
            mem2HasNegation = negationPatterns.some(function (p) { return p.test(mem2.content); });
            mem1HasChange = changeIndicators.some(function (p) { return p.test(mem1.content); });
            mem2HasChange = changeIndicators.some(function (p) { return p.test(mem2.content); });
            content1Lower = mem1.content.toLowerCase();
            content2Lower = mem2.content.toLowerCase();
            numericContradiction = checkNumericContradiction(mem1.content, mem2.content);
            priorityContradiction = checkPriorityContradiction(mem1.content, mem2.content);
            if (!numericContradiction && !priorityContradiction &&
                !mem1HasNegation && !mem2HasNegation &&
                !mem1HasChange && !mem2HasChange) {
                // No clear contradiction signal
                return [2 /*return*/, null];
            }
            m1Time = new Date(mem1.created_at).getTime();
            m2Time = new Date(mem2.created_at).getTime();
            if (Math.abs(m1Time - m2Time) < 1000 * 60 * 60) {
                // Less than 1 hour apart - flag for review
                resolution = 'flag_for_review';
                winner = m1Time > m2Time ? mem1 : mem2;
                confidence = 0.5;
            }
            else {
                // Clear time difference - newer wins
                resolution = 'newer_wins';
                winner = m1Time > m2Time ? mem1 : mem2;
                confidence = 0.8;
            }
            conflict = describeConflict(mem1, mem2, numericContradiction || priorityContradiction || 'preference_change');
            return [2 /*return*/, {
                    memory1: mem1,
                    memory2: mem2,
                    conflict: conflict,
                    resolution: resolution,
                    winner: winner,
                    confidence: confidence
                }];
        });
    });
}
/**
 * Check for numeric value contradictions (revenue, targets, amounts)
 */
function checkNumericContradiction(content1, content2) {
    var numPattern = /\$?(\d+[,\d]*)\s*(k|thousand|million|m|mo|month)?/gi;
    var nums1 = __spreadArray([], content1.matchAll(numPattern), true).map(function (m) {
        var _a;
        return ({
            value: parseInt(m[1].replace(/,/g, '')),
            unit: ((_a = m[2]) === null || _a === void 0 ? void 0 : _a.toLowerCase()) || '',
            original: m[0]
        });
    });
    var nums2 = __spreadArray([], content2.matchAll(numPattern), true).map(function (m) {
        var _a;
        return ({
            value: parseInt(m[1].replace(/,/g, '')),
            unit: ((_a = m[2]) === null || _a === void 0 ? void 0 : _a.toLowerCase()) || '',
            original: m[0]
        });
    });
    if (nums1.length === 0 || nums2.length === 0)
        return null;
    // Check if same context (both about revenue, both about price, etc.)
    var contextWords = ['revenue', 'target', 'price', 'cost', 'budget', 'value'];
    var hasSharedContext = contextWords.some(function (w) {
        return content1.toLowerCase().includes(w) && content2.toLowerCase().includes(w);
    });
    if (!hasSharedContext)
        return null;
    // Check if values differ significantly
    for (var _i = 0, nums1_1 = nums1; _i < nums1_1.length; _i++) {
        var n1 = nums1_1[_i];
        for (var _a = 0, nums2_1 = nums2; _a < nums2_1.length; _a++) {
            var n2 = nums2_1[_a];
            var val1 = n1.unit.includes('k') ? n1.value * 1000 : n1.value;
            var val2 = n2.unit.includes('k') ? n2.value * 1000 : n2.value;
            if (Math.abs(val1 - val2) > Math.max(val1, val2) * 0.1) {
                return "numeric_mismatch: ".concat(n1.original, " vs ").concat(n2.original);
            }
        }
    }
    return null;
}
/**
 * Check for priority/ordering contradictions (first, second, primary, secondary)
 */
function checkPriorityContradiction(content1, content2) {
    var priorityWords = ['first', 'second', 'primary', 'secondary', 'priority', 'focus', 'top'];
    var priorities1 = priorityWords.filter(function (w) {
        return new RegExp("\\b".concat(w, "\\b"), 'i').test(content1);
    });
    var priorities2 = priorityWords.filter(function (w) {
        return new RegExp("\\b".concat(w, "\\b"), 'i').test(content2);
    });
    if (priorities1.length === 0 || priorities2.length === 0)
        return null;
    // Check for conflicting priorities
    var conflicts = [];
    if (content1.match(/first|primary|priority/i) && content2.match(/second|secondary/i)) {
        conflicts.push('first vs second');
    }
    if (content1.match(/second|secondary/i) && content2.match(/first|primary|priority/i)) {
        conflicts.push('second vs first');
    }
    return conflicts.length > 0 ? "priority_conflict: ".concat(conflicts.join(', ')) : null;
}
/**
 * Describe the conflict in human-readable form
 */
function describeConflict(mem1, mem2, type) {
    var t1 = new Date(mem1.created_at).toLocaleDateString();
    var t2 = new Date(mem2.created_at).toLocaleDateString();
    return "[".concat(t1, "] \"").concat(mem1.content.slice(0, 60), "...\" contradicts [").concat(t2, "] \"").concat(mem2.content.slice(0, 60), "...\" (").concat(type, ")");
}
/**
 * Scan all memories for contradictions
 */
function scanContradictions(store) {
    return __awaiter(this, void 0, void 0, function () {
        var allMemories, report, i, j, contradiction;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, store.recall('', { limit: 1000 })];
                case 1:
                    allMemories = _a.sent();
                    report = {
                        total_checked: 0,
                        contradictions_found: 0,
                        auto_resolved: 0,
                        flagged_for_review: 0,
                        details: []
                    };
                    i = 0;
                    _a.label = 2;
                case 2:
                    if (!(i < allMemories.length)) return [3 /*break*/, 7];
                    j = i + 1;
                    _a.label = 3;
                case 3:
                    if (!(j < allMemories.length)) return [3 /*break*/, 6];
                    report.total_checked++;
                    return [4 /*yield*/, detectContradiction(allMemories[i], allMemories[j])];
                case 4:
                    contradiction = _a.sent();
                    if (contradiction) {
                        report.contradictions_found++;
                        report.details.push(contradiction);
                        if (contradiction.resolution === 'flag_for_review') {
                            report.flagged_for_review++;
                        }
                        else {
                            report.auto_resolved++;
                        }
                    }
                    _a.label = 5;
                case 5:
                    j++;
                    return [3 /*break*/, 3];
                case 6:
                    i++;
                    return [3 /*break*/, 2];
                case 7: return [2 /*return*/, report];
            }
        });
    });
}
/**
 * Get the resolved value for a query (considering contradictions)
 */
function getResolvedValue(store, query) {
    return __awaiter(this, void 0, void 0, function () {
        var memories, contradictions, i, j, c, mostRecent, bestResolution;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, store.recall(query, { limit: 5 })];
                case 1:
                    memories = _a.sent();
                    if (memories.length === 0) {
                        return [2 /*return*/, { value: '', source: null, confidence: 0 }];
                    }
                    contradictions = [];
                    i = 0;
                    _a.label = 2;
                case 2:
                    if (!(i < memories.length)) return [3 /*break*/, 7];
                    j = i + 1;
                    _a.label = 3;
                case 3:
                    if (!(j < memories.length)) return [3 /*break*/, 6];
                    return [4 /*yield*/, detectContradiction(memories[i], memories[j])];
                case 4:
                    c = _a.sent();
                    if (c)
                        contradictions.push(c);
                    _a.label = 5;
                case 5:
                    j++;
                    return [3 /*break*/, 3];
                case 6:
                    i++;
                    return [3 /*break*/, 2];
                case 7:
                    if (contradictions.length === 0) {
                        mostRecent = memories.sort(function (a, b) {
                            return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
                        })[0];
                        return [2 /*return*/, {
                                value: mostRecent.content,
                                source: mostRecent,
                                confidence: 0.9
                            }];
                    }
                    bestResolution = contradictions.sort(function (a, b) { return b.confidence - a.confidence; })[0];
                    return [2 /*return*/, {
                            value: bestResolution.winner.content,
                            source: bestResolution.winner,
                            confidence: bestResolution.confidence
                        }];
            }
        });
    });
}
