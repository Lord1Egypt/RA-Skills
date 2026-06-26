"use strict";
/**
 * Temporal Reasoning Module
 *
 * Tracks how facts change over time and answers temporal queries:
 * - "When did X change?"
 * - "How did X evolve over sessions?"
 * - "What was X's value at time Y?"
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
exports.extractTemporalEvents = extractTemporalEvents;
exports.buildTimeline = buildTimeline;
exports.answerTemporalQuery = answerTemporalQuery;
exports.detectTemporalRelationships = detectTemporalRelationships;
// Attributes that commonly change over time
var temporalAttributes = [
    'revenue', 'target', 'priority', 'focus', 'status',
    'progress', 'price', 'value', 'count', 'stage'
];
// Entities to track (extracted from content)
var trackedEntityPatterns = [
    /Elev8Advisory/gi,
    /BrandForge/gi,
    /Muninn/gi,
    /OpenClaw/gi,
    /Phillip/gi,
    /KakāpōHiko/gi,
    /Sammy/gi,
    /Charlie/gi,
    /Donna/gi,
    /\$[\d,]+k?(?:\/mo|\/month)?/gi
];
/**
 * Extract temporal events from a memory
 */
function extractTemporalEvents(memory) {
    var _a;
    var events = [];
    var content = memory.content;
    // Extract numeric values with context
    var numericPattern = /\$?(\d+[,\d]*)\s*(k|thousand|m|million)?\s*(?:\/mo|\/month|revenue|target|price)?/gi;
    var matches = __spreadArray([], content.matchAll(numericPattern), true);
    for (var _i = 0, matches_1 = matches; _i < matches_1.length; _i++) {
        var match = matches_1[_i];
        var value = match[0];
        var context = content.slice(Math.max(0, match.index - 30), match.index + match[0].length + 30);
        // Determine attribute
        var attribute = 'value';
        if (context.toLowerCase().includes('revenue'))
            attribute = 'revenue';
        else if (context.toLowerCase().includes('target'))
            attribute = 'target';
        else if (context.toLowerCase().includes('price'))
            attribute = 'price';
        // Extract related entity
        var entity = 'unknown';
        for (var _b = 0, trackedEntityPatterns_1 = trackedEntityPatterns; _b < trackedEntityPatterns_1.length; _b++) {
            var pattern = trackedEntityPatterns_1[_b];
            var entityMatch = content.match(pattern);
            if (entityMatch) {
                entity = entityMatch[0];
                break;
            }
        }
        events.push({
            timestamp: memory.created_at,
            memory: memory,
            change_type: 'created',
            value: value,
            previous_value: undefined
        });
    }
    // Extract priority changes
    var priorityPattern = /(first|primary|priority|top|main|focus)/i;
    var secondaryPattern = /(second|secondary|backseat|lower)/i;
    if (priorityPattern.test(content) || secondaryPattern.test(content)) {
        var entityMatch = trackedEntityPatterns.find(function (p) { return content.match(p); });
        if (entityMatch) {
            var entity = ((_a = content.match(entityMatch)) === null || _a === void 0 ? void 0 : _a[0]) || 'unknown';
            events.push({
                timestamp: memory.created_at,
                memory: memory,
                change_type: 'updated',
                value: priorityPattern.test(content) ? 'priority' : 'secondary',
                previous_value: undefined
            });
        }
    }
    return events;
}
/**
 * Build a timeline for a specific entity and attribute
 */
function buildTimeline(store, entity, attribute) {
    return __awaiter(this, void 0, void 0, function () {
        var memories, events, _loop_1, _i, memories_1, memory, i, prev, curr, trend;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, store.recall(entity, { limit: 50 })];
                case 1:
                    memories = _a.sent();
                    if (memories.length === 0)
                        return [2 /*return*/, null];
                    events = [];
                    _loop_1 = function (memory) {
                        var memEvents = extractTemporalEvents(memory);
                        // Filter to relevant attribute
                        var relevant = memEvents.filter(function (e) {
                            var context = memory.content.toLowerCase();
                            return context.includes(attribute.toLowerCase());
                        });
                        events.push.apply(events, relevant);
                    };
                    for (_i = 0, memories_1 = memories; _i < memories_1.length; _i++) {
                        memory = memories_1[_i];
                        _loop_1(memory);
                    }
                    // Sort by timestamp
                    events.sort(function (a, b) {
                        return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
                    });
                    // Detect changes between events
                    for (i = 1; i < events.length; i++) {
                        prev = events[i - 1];
                        curr = events[i];
                        if (prev.value !== curr.value) {
                            curr.change_type = 'updated';
                            curr.previous_value = prev.value;
                        }
                        else {
                            curr.change_type = 'reinforced';
                            curr.previous_value = prev.value;
                        }
                    }
                    trend = calculateTrend(events);
                    return [2 /*return*/, {
                            entity: entity,
                            attribute: attribute,
                            events: events,
                            current_value: events.length > 0 ? events[events.length - 1].value : '',
                            trend: trend
                        }];
            }
        });
    });
}
/**
 * Calculate trend from temporal events
 */
function calculateTrend(events) {
    if (events.length < 2)
        return 'stable';
    // Extract numeric values
    var values = [];
    for (var _i = 0, events_1 = events; _i < events_1.length; _i++) {
        var event_1 = events_1[_i];
        var numMatch = event_1.value.match(/\$?(\d+[,\d]*)/);
        if (numMatch) {
            values.push(parseInt(numMatch[1].replace(/,/g, '')));
        }
    }
    if (values.length < 2) {
        // Check for priority changes
        var priorities = events.map(function (e) { return e.value; });
        if (priorities.some(function (p) { return p === 'priority'; }) && priorities.some(function (p) { return p === 'secondary'; })) {
            return 'volatile';
        }
        return 'stable';
    }
    // Count direction changes
    var increases = 0;
    var decreases = 0;
    for (var i = 1; i < values.length; i++) {
        if (values[i] > values[i - 1])
            increases++;
        else if (values[i] < values[i - 1])
            decreases++;
    }
    if (increases > 0 && decreases === 0)
        return 'increasing';
    if (decreases > 0 && increases === 0)
        return 'decreasing';
    if (increases > 0 && decreases > 0)
        return 'volatile';
    return 'stable';
}
/**
 * Answer a temporal query
 */
function answerTemporalQuery(store, query) {
    return __awaiter(this, void 0, void 0, function () {
        var entityMatch, entity, attribute, _i, temporalAttributes_1, attr, askingChange, askingCurrent, timeline, answer, changes, changes;
        var _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    entityMatch = trackedEntityPatterns.find(function (p) { return query.match(p); });
                    if (!entityMatch) {
                        return [2 /*return*/, {
                                question: query,
                                timeline: null,
                                answer: 'Could not identify entity in query',
                                confidence: 0
                            }];
                    }
                    entity = ((_a = query.match(entityMatch)) === null || _a === void 0 ? void 0 : _a[0]) || '';
                    attribute = 'value';
                    for (_i = 0, temporalAttributes_1 = temporalAttributes; _i < temporalAttributes_1.length; _i++) {
                        attr = temporalAttributes_1[_i];
                        if (query.toLowerCase().includes(attr)) {
                            attribute = attr;
                            break;
                        }
                    }
                    askingChange = /how.*change|evolve|over time|when|history/i.test(query);
                    askingCurrent = /current|now|today|latest/i.test(query);
                    return [4 /*yield*/, buildTimeline(store, entity, attribute)];
                case 1:
                    timeline = _b.sent();
                    if (!timeline || timeline.events.length === 0) {
                        return [2 /*return*/, {
                                question: query,
                                timeline: null,
                                answer: "No temporal data found for ".concat(entity),
                                confidence: 0
                            }];
                    }
                    answer = '';
                    if (askingChange) {
                        changes = timeline.events
                            .filter(function (e) { return e.change_type === 'updated' || e.change_type === 'created'; })
                            .map(function (e) {
                            var date = new Date(e.timestamp).toLocaleDateString();
                            if (e.previous_value && e.previous_value !== e.value) {
                                return "".concat(date, ": changed from ").concat(e.previous_value, " to ").concat(e.value);
                            }
                            return "".concat(date, ": ").concat(e.value);
                        });
                        answer = "".concat(entity, " ").concat(attribute, " history:\n").concat(changes.join('\n'));
                    }
                    else if (askingCurrent) {
                        answer = "Current ".concat(entity, " ").concat(attribute, ": ").concat(timeline.current_value, " (as of ").concat(new Date(timeline.events[timeline.events.length - 1].timestamp).toLocaleDateString(), ")");
                    }
                    else {
                        changes = timeline.events.filter(function (e) { return e.change_type === 'updated'; }).length;
                        answer = "".concat(entity, " ").concat(attribute, " has ").concat(timeline.trend, " over time. Current: ").concat(timeline.current_value, ". ").concat(changes, " changes recorded.");
                    }
                    return [2 /*return*/, {
                            question: query,
                            timeline: timeline,
                            answer: answer,
                            confidence: timeline.events.length > 3 ? 0.9 : 0.6
                        }];
            }
        });
    });
}
/**
 * Detect temporal relationships between memories
 */
function detectTemporalRelationships(memories) {
    var relationships = new Map();
    // Group by entity
    for (var _i = 0, memories_2 = memories; _i < memories_2.length; _i++) {
        var memory = memories_2[_i];
        for (var _a = 0, _b = memory.entities; _a < _b.length; _a++) {
            var entity = _b[_a];
            if (!relationships.has(entity)) {
                relationships.set(entity, []);
            }
            relationships.get(entity).push(memory);
        }
    }
    // Sort each group by time
    for (var _c = 0, relationships_1 = relationships; _c < relationships_1.length; _c++) {
        var _d = relationships_1[_c], entity = _d[0], mems = _d[1];
        mems.sort(function (a, b) {
            return new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
        });
    }
    return relationships;
}
