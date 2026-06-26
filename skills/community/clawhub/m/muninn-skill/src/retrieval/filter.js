"use strict";
/**
 * LLM-Based Retrieval Filter
 *
 * Post-filters semantic search results using LLM to improve precision
 * while maintaining recall by using recall-biased prompts.
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
exports.filterMemories = filterMemories;
exports.scoreForQuestionType = scoreForQuestionType;
/**
 * Filter memories using LLM to improve relevance ranking
 * With fast timeout fallback to avoid hanging
 *
 * @param query - The search query
 * @param memories - Candidate memories from semantic search
 * @param options - Filter options
 * @returns Filtered and ranked memories
 */
function filterMemories(query_1, memories_1) {
    return __awaiter(this, arguments, void 0, function (query, memories, options) {
        var _a, k, _b, recallBiased, _c, timeout, result, error_1;
        if (options === void 0) { options = {}; }
        return __generator(this, function (_d) {
            switch (_d.label) {
                case 0:
                    _a = options.k, k = _a === void 0 ? memories.length : _a, _b = options.recallBiased, recallBiased = _b === void 0 ? true : _b, _c = options.timeout, timeout = _c === void 0 ? 2000 : _c;
                    // Return all if too few
                    if (memories.length === 0)
                        return [2 /*return*/, []];
                    if (memories.length <= 2)
                        return [2 /*return*/, memories.slice(0, k)];
                    _d.label = 1;
                case 1:
                    _d.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, Promise.race([
                            llmFilter(query, memories, { recallBiased: recallBiased }),
                            new Promise(function (_, reject) {
                                return setTimeout(function () { return reject(new Error('LLM timeout')); }, timeout);
                            })
                        ])];
                case 2:
                    result = _d.sent();
                    if (result && result.length > 0) {
                        return [2 /*return*/, result.slice(0, k)];
                    }
                    return [3 /*break*/, 4];
                case 3:
                    error_1 = _d.sent();
                    console.warn('LLM filter failed or timed out, using fallback:', error_1 instanceof Error ? error_1.message : 'unknown');
                    return [3 /*break*/, 4];
                case 4: 
                // Fallback: Return top-k by salience + recency
                return [2 /*return*/, fallbackFilter(memories, k)];
            }
        });
    });
}
/**
 * Fallback filter: score by salience + recency
 */
function fallbackFilter(memories, k) {
    var now = Date.now();
    var msPerMonth = 1000 * 60 * 60 * 24 * 30;
    return __spreadArray([], memories, true).sort(function (a, b) {
        // Combine salience with recency boost
        var scoreA = a.salience + (now - new Date(a.created_at).getTime()) / msPerMonth * 0.1;
        var scoreB = b.salience + (now - new Date(b.created_at).getTime()) / msPerMonth * 0.1;
        return scoreB - scoreA;
    })
        .slice(0, k);
}
/**
 * Post-retrieval scorer for temporal/contradiction questions
 */
function scoreForQuestionType(memories, query) {
    var lowerQuery = query.toLowerCase();
    // ========================================================================
    // PHASE 1.5: ENHANCED TEMPORAL & CONTRADICTION HANDLING
    // ========================================================================
    // Boost recent memories for "current" questions
    if (lowerQuery.includes('current') || lowerQuery.includes('now') || lowerQuery.includes('priority') || lowerQuery.includes('target') || lowerQuery.includes('revenue')) {
        // For revenue/target questions, sort by timestamp descending (most recent first)
        return __spreadArray([], memories, true).sort(function (a, b) {
            var timeA = a.timestamp ? new Date(a.timestamp).getTime() : new Date(a.created_at).getTime();
            var timeB = b.timestamp ? new Date(b.timestamp).getTime() : new Date(b.created_at).getTime();
            return timeB - timeA; // Most recent first
        });
    }
    // For temporal "how did X change" questions, return all for synthesis
    if (lowerQuery.includes('change') || lowerQuery.includes('over time') || lowerQuery.includes('history') || lowerQuery.includes('evolve')) {
        // Sort chronologically for change tracking
        return __spreadArray([], memories, true).sort(function (a, b) {
            var timeA = a.timestamp ? new Date(a.timestamp).getTime() : new Date(a.created_at).getTime();
            var timeB = b.timestamp ? new Date(b.timestamp).getTime() : new Date(b.created_at).getTime();
            return timeA - timeB; // Oldest first for change tracking
        });
    }
    // For contradiction questions (original vs now), return all sorted by time
    if (lowerQuery.includes('original') || lowerQuery.includes('was ') || lowerQuery.includes('previously')) {
        return __spreadArray([], memories, true).sort(function (a, b) {
            var timeA = a.timestamp ? new Date(a.timestamp).getTime() : new Date(a.created_at).getTime();
            var timeB = b.timestamp ? new Date(b.timestamp).getTime() : new Date(b.created_at).getTime();
            return timeA - timeB; // Oldest first to see evolution
        });
    }
    // For "what features were discussed on Tuesday", return all for synthesis
    if (lowerQuery.includes('discussed') || lowerQuery.includes('talked about') || lowerQuery.includes('mentioned')) {
        return memories; // Return all, let synthesis handle it
    }
    return memories;
}
/**
 * Actual LLM filter implementation
 */
function llmFilter(query, memories, options) {
    return __awaiter(this, void 0, void 0, function () {
        var _a, recallBiased, candidatesText, prompt_1, response, relevantIndices, filtered, error_2;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    _a = options.recallBiased, recallBiased = _a === void 0 ? true : _a;
                    // Return all if too few
                    if (memories.length === 0)
                        return [2 /*return*/, []];
                    if (memories.length <= 2)
                        return [2 /*return*/, memories];
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 3, , 4]);
                    candidatesText = formatCandidatesForLLM(memories);
                    prompt_1 = recallBiased
                        ? buildRecallBiasedPrompt(query, candidatesText)
                        : buildPrecisionPrompt(query, candidatesText);
                    return [4 /*yield*/, generateLLMResponse(prompt_1)];
                case 2:
                    response = _b.sent();
                    relevantIndices = parseLLMResponse(response).relevantIndices;
                    filtered = relevantIndices
                        .filter(function (i) { return i >= 0 && i < memories.length; })
                        .map(function (i) { return memories[i]; });
                    // If LLM returns empty or invalid, fall back to original
                    if (filtered.length === 0) {
                        return [2 /*return*/, memories];
                    }
                    return [2 /*return*/, filtered];
                case 3:
                    error_2 = _b.sent();
                    console.warn('LLM filter failed, using fallback:', error_2);
                    // Fallback: return original memories sorted by salience
                    return [2 /*return*/, __spreadArray([], memories, true).sort(function (a, b) { return b.salience - a.salience; })];
                case 4: return [2 /*return*/];
            }
        });
    });
}
/**
 * Format memories as numbered list for LLM consumption
 */
function formatCandidatesForLLM(memories) {
    return memories
        .map(function (m, i) { return "[".concat(i, "] ").concat(m.content); })
        .join('\n\n');
}
/**
 * Build recall-biased prompt (prefer including borderline cases)
 */
function buildRecallBiasedPrompt(query, candidates) {
    return "Given the question: \"".concat(query, "\"\n\nSelect ALL memory entries that could be relevant, even if uncertain.\nIt's better to include borderline cases than miss relevant information.\nWhen in doubt, include the memory.\n\nMemories to evaluate:\n").concat(candidates, "\n\nReturn JSON with \"relevantIndices\" array containing indices of relevant memories:\n{\"relevantIndices\": [0, 3, 5]}");
}
/**
 * Build precision-biased prompt (only highly relevant)
 */
function buildPrecisionPrompt(query, candidates) {
    return "Given the question: \"".concat(query, "\"\n\nSelect ONLY the most directly relevant memory entries.\nExclude entries that are tangentially related or uncertain.\n\nMemories to evaluate:\n").concat(candidates, "\n\nReturn JSON with \"relevantIndices\" array containing indices of highly relevant memories:\n{\"relevantIndices\": [0, 3, 5]}");
}
/**
 * Parse LLM JSON response
 */
function parseLLMResponse(response) {
    try {
        // Try to extract JSON from response
        var jsonMatch = response.match(/\{[\s\S]*\}/);
        if (!jsonMatch) {
            console.warn('No JSON found in LLM response');
            return { relevantIndices: [] };
        }
        var parsed = JSON.parse(jsonMatch[0]);
        // Handle different response formats
        if (Array.isArray(parsed)) {
            return { relevantIndices: parsed };
        }
        if (parsed.relevantIndices) {
            return { relevantIndices: parsed.relevantIndices };
        }
        if (parsed.relevant || parsed.indices || parsed.results) {
            return { relevantIndices: parsed.relevant || parsed.indices || parsed.results };
        }
        // Try to extract any array of numbers
        for (var _i = 0, _a = Object.keys(parsed); _i < _a.length; _i++) {
            var key = _a[_i];
            if (Array.isArray(parsed[key]) && parsed[key].every(function (v) { return typeof v === 'number'; })) {
                return { relevantIndices: parsed[key] };
            }
        }
        console.warn('Could not parse LLM response format');
        return { relevantIndices: [] };
    }
    catch (error) {
        console.warn('Failed to parse LLM response:', error);
        return { relevantIndices: [] };
    }
}
/**
 * Generate LLM response (uses global mock or Ollama)
 */
function generateLLMResponse(prompt_2) {
    return __awaiter(this, arguments, void 0, function (prompt, timeoutMs) {
        var model, controller_1, timeoutId, response, data, e_1;
        if (timeoutMs === void 0) { timeoutMs = 10000; }
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    // Use global mock if available (for testing)
                    if (typeof globalThis.generateLLMResponse === 'function') {
                        return [2 /*return*/, globalThis.generateLLMResponse(prompt)];
                    }
                    model = 'glm-5:cloud';
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 5, , 6]);
                    controller_1 = new AbortController();
                    timeoutId = setTimeout(function () { return controller_1.abort(); }, timeoutMs);
                    return [4 /*yield*/, fetch('http://localhost:11434/api/generate', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                model: model,
                                prompt: prompt,
                                stream: false,
                                format: 'json'
                            }),
                            signal: controller_1.signal
                        })];
                case 2:
                    response = _a.sent();
                    clearTimeout(timeoutId);
                    if (!response.ok) return [3 /*break*/, 4];
                    return [4 /*yield*/, response.json()];
                case 3:
                    data = _a.sent();
                    return [2 /*return*/, data.response];
                case 4: throw new Error("Model ".concat(model, ": ").concat(response.statusText));
                case 5:
                    e_1 = _a.sent();
                    throw e_1;
                case 6: return [2 /*return*/];
            }
        });
    });
}
