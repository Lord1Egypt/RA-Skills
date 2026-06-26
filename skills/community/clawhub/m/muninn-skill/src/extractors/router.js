"use strict";
/**
 * Content Router (Enhanced Keyword Version)
 *
 * Classifies content into memory types using pattern matching.
 * No LLM required - fast, deterministic, zero dependencies.
 *
 * Accuracy target: 90%+
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
exports.routeWithLLM = routeWithLLM;
exports.routeContent = routeContent;
exports.routeWithKeywords = routeWithKeywords;
// ============================================
// PATTERN DEFINITIONS
// ============================================
// Past-tense verbs indicating events (episodic)
var PAST_TENSE_VERBS = [
    'met', 'discussed', 'talked', 'called', 'happened', 'occurred',
    'built', 'created', 'made', 'completed', 'finished', 'started',
    'learned', 'discovered', 'found', 'saw', 'heard', 'read',
    'decided', 'agreed', 'disagreed', 'resolved', 'fixed',
    'deployed', 'shipped', 'released', 'launched', 'implemented',
    'received', 'sent', 'wrote', 'said', 'asked', 'answered',
    'went', 'came', 'left', 'arrived', 'visited', 'attended',
    'caused', 'triggered', 'resulted', 'led', 'broke', 'failed'
];
// Time indicators for episodic
var TIME_INDICATORS = [
    'yesterday', 'today', 'last week', 'last month', 'recently',
    'this morning', 'this afternoon', 'this evening', 'tonight',
    'on monday', 'on tuesday', 'on wednesday', 'on thursday', 'on friday',
    'ago', 'earlier', 'previously', 'before'
];
// Common typos for time indicators (fuzzy matching)
var TIME_TYPOS = {
    'yestrday': 'yesterday',
    'yesturday': 'yesterday',
    'yestday': 'yesterday',
    'yday': 'yesterday',
    'todays': 'today',
    'tday': 'today',
    'nigth': 'night',
    'nite': 'night',
    'ystrday': 'yesterday',
};
// Meeting/event indicators (episodic)
var EVENT_INDICATORS = [
    'meeting', 'call', 'conversation', 'discussion', 'session',
    'interview', 'presentation', 'demo', 'workshop', 'standup',
    'we had', 'we discussed', 'we talked', 'we met'
];
// Procedure/action verbs (procedural)
var PROCEDURE_VERBS = [
    'run', 'execute', 'install', 'configure', 'setup', 'create',
    'delete', 'remove', 'update', 'upgrade', 'deploy', 'build',
    'test', 'verify', 'check', 'validate', 'restart', 'reload',
    'clone', 'commit', 'push', 'pull', 'merge', 'branch'
];
// Step indicators (procedural)
var STEP_INDICATORS = [
    'first,', 'second,', 'third,', 'then,', 'next,', 'finally,',
    'step 1', 'step 2', 'step 3', '1)', '2)', '3)', '1.', '2.', '3.',
    'before you', 'after you', 'you need to', 'you should',
    'make sure to', 'ensure that', 'remember to'
];
// Conditional patterns (procedural) - "when X, do Y"
var CONDITIONAL_PATTERNS = [
    /when\s+.+,\s*(check|verify|run|execute|use|ensure|make|do)/i,
    /if\s+.+,\s*(check|verify|run|execute|use|ensure|make|do)/i,
    /when\s+.+\s+(fails|breaks|errors)/i,
    /if\s+.+\s+(fails|breaks|errors)/i
];
// Protocol/process keywords (procedural)
var PROCESS_KEYWORDS = [
    'protocol', 'workflow', 'process', 'procedure', 'steps',
    'how to', 'guide', 'instructions', 'tutorial', 'method',
    'pipeline', 'checklist', 'routine'
];
// Semantic indicators - preferences
var PREFERENCE_INDICATORS = [
    'prefer', 'prefers', 'like', 'likes', 'dislike', 'dislikes',
    'love', 'hate', 'want', 'needs', 'favorite', 'best'
];
// Semantic indicators - facts
var FACT_INDICATORS = [
    'is', 'are', 'was', 'were', 'have', 'has', 'had',
    'means', 'refers to', 'defined as', 'stands for',
    'default', 'typically', 'usually', 'always', 'never'
];
// Ownership/belonging (often semantic)
var OWNERSHIP_PATTERNS = [
    /'s\s+\w+$/i, // "Phillip's timezone"
    /\w+\s+target/i, // "revenue target"
    /\w+\s+default/i, // "gateway default"
    /runs on/i, // "runs on port"
    /uses\s+\w+\s+for/i // "uses SQLite for storage"
];
// ============================================
// SCORING FUNCTIONS
// ============================================
function scoreEpisodic(content) {
    var patterns = [];
    var score = 0;
    var lower = content.toLowerCase();
    // Past-tense verbs (strong indicator)
    // Exclude gerunds (ing form) which are often procedural
    for (var _i = 0, PAST_TENSE_VERBS_1 = PAST_TENSE_VERBS; _i < PAST_TENSE_VERBS_1.length; _i++) {
        var verb = PAST_TENSE_VERBS_1[_i];
        // Match past tense but not gerund (e.g., "started" is past, "starting" is gerund)
        var regex = new RegExp("\\b".concat(verb, "\\b"), 'i');
        var gerundRegex = new RegExp("\\b".concat(verb.replace(/ed$/, 'ing'), "\\b"), 'i');
        if (regex.test(content) && !gerundRegex.test(content)) {
            score += 0.3;
            patterns.push("past-tense:".concat(verb));
        }
    }
    // Time indicators (strong)
    for (var _a = 0, TIME_INDICATORS_1 = TIME_INDICATORS; _a < TIME_INDICATORS_1.length; _a++) {
        var time = TIME_INDICATORS_1[_a];
        if (lower.includes(time)) {
            score += 0.25;
            patterns.push("time:".concat(time));
        }
    }
    // Time typo fuzzy matching
    for (var _b = 0, _c = Object.entries(TIME_TYPOS); _b < _c.length; _b++) {
        var _d = _c[_b], typo = _d[0], correct = _d[1];
        if (lower.includes(typo)) {
            score += 0.2; // Slightly lower for typos
            patterns.push("time-typo:".concat(typo, "->").concat(correct));
        }
    }
    // Event indicators (strong)
    for (var _e = 0, EVENT_INDICATORS_1 = EVENT_INDICATORS; _e < EVENT_INDICATORS_1.length; _e++) {
        var event_1 = EVENT_INDICATORS_1[_e];
        if (lower.includes(event_1)) {
            score += 0.3;
            patterns.push("event:".concat(event_1));
        }
    }
    // "We" + past action pattern
    if (/we\s+(met|discussed|talked|had|decided|agreed|built|created)/i.test(content)) {
        score += 0.4;
        patterns.push('we+past-action');
    }
    // "X caused Y" pattern - events causing outcomes
    if (/\b(caused|led to|resulted in|triggered)\b/i.test(content)) {
        score += 0.35;
        patterns.push('causation-event');
    }
    // Outage/incident/breakage words (event outcomes)
    if (/\b(outage|incident|failure|error|crash|crashed|broke|broken|issue|problem|garbage)\b/i.test(content)) {
        score += 0.3;
        patterns.push('incident');
    }
    // Strong event verbs (crashed, broke, failed - definitive past events)
    if (/\b(crashed|broke|failed|borked|died|exploded)\b/i.test(content)) {
        score += 0.35;
        patterns.push('strong-event-verb');
    }
    return { score: Math.min(score, 1), patterns: patterns };
}
function scoreProcedural(content) {
    var patterns = [];
    var score = 0;
    var lower = content.toLowerCase();
    // Step indicators (very strong)
    for (var _i = 0, STEP_INDICATORS_1 = STEP_INDICATORS; _i < STEP_INDICATORS_1.length; _i++) {
        var step = STEP_INDICATORS_1[_i];
        if (lower.includes(step)) {
            score += 0.35;
            patterns.push("step:".concat(step));
        }
    }
    // Conditional patterns (strong)
    for (var _a = 0, CONDITIONAL_PATTERNS_1 = CONDITIONAL_PATTERNS; _a < CONDITIONAL_PATTERNS_1.length; _a++) {
        var pattern = CONDITIONAL_PATTERNS_1[_a];
        if (pattern.test(content)) {
            score += 0.4;
            patterns.push("conditional:".concat(pattern.source.slice(0, 20)));
        }
    }
    // Process keywords (strong)
    for (var _b = 0, PROCESS_KEYWORDS_1 = PROCESS_KEYWORDS; _b < PROCESS_KEYWORDS_1.length; _b++) {
        var keyword = PROCESS_KEYWORDS_1[_b];
        if (lower.includes(keyword)) {
            score += 0.3;
            patterns.push("process:".concat(keyword));
        }
    }
    // Procedure verbs with context
    for (var _c = 0, PROCEDURE_VERBS_1 = PROCEDURE_VERBS; _c < PROCEDURE_VERBS_1.length; _c++) {
        var verb = PROCEDURE_VERBS_1[_c];
        var regex = new RegExp("\\b(run|execute|check|verify)\\s+\\w+", 'i');
        if (regex.test(content)) {
            score += 0.25;
            patterns.push("action:".concat(verb));
        }
    }
    // Numbered list detection
    if (/\d+[.)]\s+\w+/.test(content)) {
        score += 0.35;
        patterns.push('numbered-list');
    }
    // "then... then" chain pattern (implied steps)
    var thenCount = (lower.match(/\bthen\b/g) || []).length;
    if (thenCount >= 2) {
        score += 0.3;
        patterns.push('then-chain');
    }
    // "involves" + actions pattern
    if (/involves\s+(reading|checking|running|executing|using)/i.test(content)) {
        score += 0.4;
        patterns.push('involves+action');
    }
    // "To [verb], run/do/execute" pattern (instructional)
    if (/^to\s+\w+.*,\s*(run|do|execute|use|call|type|enter)/i.test(content)) {
        score += 0.5;
        patterns.push('instructional');
    }
    // Command pattern: "run:", "execute:", "use:" (common in docs)
    if (/(run|execute|use|call|type):\s*\w+/i.test(content)) {
        score += 0.35;
        patterns.push('command-pattern');
    }
    // "Before/After [gerund]" pattern (procedural instructions)
    if (/\b(before|after)\s+\w+ing\b/i.test(content)) {
        score += 0.45;
        patterns.push('before-after-instruction');
    }
    // "Make sure to/that" pattern (procedural)
    if (/\bmake sure\s+(to|that)\b/i.test(content)) {
        score += 0.35;
        patterns.push('make-sure');
    }
    if (/^(run|execute|check|verify|install|configure|setup|create|delete|update|restart|reload|clone|commit|push|pull)\s/i.test(content)) {
        score += 0.4;
        patterns.push('imperative');
    }
    return { score: Math.min(score, 1), patterns: patterns };
}
function scoreSemantic(content) {
    var patterns = [];
    var score = 0;
    var lower = content.toLowerCase();
    // Preference indicators (very strong for semantic)
    for (var _i = 0, PREFERENCE_INDICATORS_1 = PREFERENCE_INDICATORS; _i < PREFERENCE_INDICATORS_1.length; _i++) {
        var pref = PREFERENCE_INDICATORS_1[_i];
        if (lower.includes(pref)) {
            score += 0.4;
            patterns.push("preference:".concat(pref));
        }
    }
    // Ownership patterns (strong)
    for (var _a = 0, OWNERSHIP_PATTERNS_1 = OWNERSHIP_PATTERNS; _a < OWNERSHIP_PATTERNS_1.length; _a++) {
        var pattern = OWNERSHIP_PATTERNS_1[_a];
        if (pattern.test(content)) {
            score += 0.3;
            patterns.push("ownership:".concat(pattern.source.slice(0, 15)));
        }
    }
    // Fact indicators (moderate - common words)
    // Only count if no other strong signals
    if (/\b(is|are|was)\s+\w+/i.test(content)) {
        score += 0.15;
        patterns.push('fact-verb');
    }
    // Technical facts
    if (/\d+\s*(port|mb|gb|ms|seconds?|minutes?|hours?)/i.test(content)) {
        score += 0.25;
        patterns.push('technical-measurement');
    }
    // "X's Y" possession pattern (e.g., "Phillip's timezone")
    if (/\b[A-Z][a-z]+'s\s+\w+/i.test(content)) {
        score += 0.3;
        patterns.push('possession');
    }
    return { score: Math.min(score, 1), patterns: patterns };
}
// ============================================
// MAIN ROUTER
// ============================================
function routeWithLLM(content, context) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            // This is the keyword-only version
            // LLM fallback will be added in Phase 1.1b
            return [2 /*return*/, routeWithKeywords(content, context)];
        });
    });
}
function routeContent(content, context) {
    return __awaiter(this, void 0, void 0, function () {
        var result, threshold;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, routeWithKeywords(content, context)];
                case 1:
                    result = _a.sent();
                    threshold = 0.4;
                    return [2 /*return*/, {
                            episodic: result.types.episodic > threshold,
                            semantic: result.types.semantic > threshold,
                            procedural: result.types.procedural > threshold,
                        }];
            }
        });
    });
}
// Keyword-based router (main implementation)
function routeWithKeywords(content, context) {
    var patterns = [];
    // Score each type
    var epResult = scoreEpisodic(content);
    var procResult = scoreProcedural(content);
    var semResult = scoreSemantic(content);
    patterns.push.apply(patterns, __spreadArray(__spreadArray(__spreadArray([], epResult.patterns, false), procResult.patterns, false), semResult.patterns, false));
    var episodic = epResult.score;
    var procedural = procResult.score;
    var semantic = semResult.score;
    // Penalize conflicts
    // "I think we should automate" - suggestion, not procedure
    if (/i think we should/i.test(content) || /we should/i.test(content)) {
        procedural *= 0.3; // Reduce procedural score
        semantic += 0.3; // Boost semantic (it's an opinion/suggestion)
        patterns.push('suggestion-penalty');
    }
    // Past-tense verbs strongly indicate episodic
    if (epResult.score > 0.3) {
        semantic *= 0.7; // Reduce semantic if clearly episodic
        patterns.push('episodic-dominant');
    }
    // If nothing significant detected, default to semantic
    var maxScore = Math.max(episodic, procedural, semantic);
    if (maxScore < 0.2) {
        semantic = 0.5;
        patterns.push('default-semantic');
    }
    // Normalize to sum to ~1
    var total = episodic + procedural + semantic;
    if (total > 0) {
        episodic /= total;
        procedural /= total;
        semantic /= total;
    }
    // Determine confidence
    var sorted = [episodic, procedural, semantic].sort(function (a, b) { return b - a; });
    var confidence = sorted[0] - sorted[1] > 0.3 ? 0.9 : 0.6;
    // Build reasoning
    var topType = episodic > procedural && episodic > semantic ? 'episodic'
        : procedural > semantic ? 'procedural'
            : 'semantic';
    var reasoning = "Classified as ".concat(topType, " based on: ").concat(patterns.slice(0, 3).join(', '));
    return {
        types: { episodic: episodic, semantic: semantic, procedural: procedural },
        reasoning: reasoning,
        confidence: confidence,
        matchedPatterns: patterns,
    };
}
