"use strict";
/**
 * Content Extractors
 * Extract structured data from raw conversation/content
 *
 * Uses enhanced keyword router for classification (95%+ accuracy)
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
exports.extractEntities = exports.createAliasStore = exports.extractWithNormalization = exports.normalizeEntities = exports.routeWithKeywords = exports.routeContent = void 0;
exports.extractEpisodic = extractEpisodic;
exports.extractSemantic = extractSemantic;
exports.extractProcedural = extractProcedural;
exports.extract = extract;
// Re-export router
var router_js_1 = require("./router.js");
Object.defineProperty(exports, "routeContent", { enumerable: true, get: function () { return router_js_1.routeContent; } });
Object.defineProperty(exports, "routeWithKeywords", { enumerable: true, get: function () { return router_js_1.routeWithKeywords; } });
// Re-export normalization
var normalize_js_1 = require("./normalize.js");
Object.defineProperty(exports, "normalizeEntities", { enumerable: true, get: function () { return normalize_js_1.normalizeEntities; } });
Object.defineProperty(exports, "extractWithNormalization", { enumerable: true, get: function () { return normalize_js_1.extractWithNormalization; } });
Object.defineProperty(exports, "createAliasStore", { enumerable: true, get: function () { return normalize_js_1.createAliasStore; } });
// Import entity extraction
var entities_js_1 = require("./entities.js");
Object.defineProperty(exports, "extractEntities", { enumerable: true, get: function () { return entities_js_1.extractEntities; } });
// Extract episodic memory data (events, conversations)
function extractEpisodic(content) {
    var entities = [];
    var topics = [];
    // Extract potential entities (capitalized words, excluding common words)
    var capitalized = content.match(/[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*/g) || [];
    var commonWords = ['I', 'The', 'A', 'An', 'This', 'That', 'It', 'We', 'They', 'You', 'He', 'She', 'But', 'However', 'When', 'Where', 'Why', 'How', 'What'];
    var filtered = capitalized.filter(function (w) { return !commonWords.includes(w) && w.length > 2; });
    entities.push.apply(entities, filtered.slice(0, 5));
    // Extract topics (keywords)
    var topicKeywords = {
        'programming': ['code', 'function', 'api', 'bug', 'feature', 'deploy', 'build'],
        'business': ['customer', 'revenue', 'sales', 'meeting', 'partner', 'deal'],
        'personal': ['family', 'friend', 'home', 'health', 'fitness', 'hobby'],
        'ai': ['model', 'llm', 'agent', 'memory', 'embedding', 'training'],
        'project': ['task', 'milestone', 'deadline', 'sprint', 'release']
    };
    var lowerContent = content.toLowerCase();
    for (var _i = 0, _a = Object.entries(topicKeywords); _i < _a.length; _i++) {
        var _b = _a[_i], topic = _b[0], keywords = _b[1];
        if (keywords.some(function (k) { return lowerContent.includes(k); })) {
            topics.push(topic);
        }
    }
    // Generate summary (first 100 chars)
    var summary = content.length > 100 ? content.slice(0, 100) + '...' : content;
    return {
        type: 'episodic',
        summary: summary,
        entities: entities,
        topics: topics,
        salience: 0.7
    };
}
// Extract semantic memory data (facts, preferences)
function extractSemantic(content) {
    var entities = [];
    var topics = [];
    // Extract potential entities
    var capitalized = content.match(/[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*/g) || [];
    var commonWords = ['I', 'The', 'A', 'An', 'This', 'That', 'It', 'We', 'They', 'You', 'He', 'She', 'But', 'However', 'When', 'Where', 'Why', 'How', 'What', 'Prefer', 'Like', 'Use', 'Am'];
    var filtered = capitalized.filter(function (w) { return !commonWords.includes(w) && w.length > 2; });
    entities.push.apply(entities, filtered.slice(0, 5));
    // Preference detection
    var isPreference = /prefer|like|love|hate|dislike|want|need|always|never|usually/i.test(content);
    if (isPreference) {
        topics.push('preference');
    }
    // Fact detection
    var isFact = /is|are|was|were|have|has|had/i.test(content);
    if (isFact) {
        topics.push('fact');
    }
    // Skill detection
    var isSkill = /know|can|capable|expert|proficient|experience/i.test(content);
    if (isSkill) {
        topics.push('skill');
    }
    return {
        type: 'semantic',
        entities: entities,
        topics: topics,
        salience: isPreference ? 0.9 : 0.6
    };
}
// Extract procedural memory data (workflows, processes)
function extractProcedural(content) {
    var _a;
    // Try to extract steps from content
    var steps = [];
    // Numbered steps
    var numberedSteps = content.match(/^\d+[.)]\s*.+$/gm);
    if (numberedSteps) {
        steps.push.apply(steps, numberedSteps.map(function (s) { return s.replace(/^\d+[.)]\s*/, ''); }));
    }
    // Bullet points
    var bulletSteps = content.match(/^[-*•]\s*.+$/gm);
    if (bulletSteps) {
        steps.push.apply(steps, bulletSteps.map(function (s) { return s.replace(/^[-*•]\s*/, ''); }));
    }
    // Try to extract title
    var lines = content.split('\n');
    var title = ((_a = lines[0]) === null || _a === void 0 ? void 0 : _a.length) < 100 ? lines[0] : 'Untitled Procedure';
    return { title: title, steps: steps };
}
// Main extraction function
function extract(content, context) {
    return __awaiter(this, void 0, void 0, function () {
        var routeContent, routing, entityResults, proc;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return require('./router.js'); })];
                case 1:
                    routeContent = (_a.sent()).routeContent;
                    return [4 /*yield*/, routeContent(content, context)];
                case 2:
                    routing = _a.sent();
                    entityResults = (0, entities_js_1.extractEntities)(content);
                    if (routing.episodic) {
                        return [2 /*return*/, __assign(__assign({}, extractEpisodic(content)), { entities: entityResults.map(function (e) { return e.text; }) })];
                    }
                    else if (routing.procedural) {
                        proc = extractProcedural(content);
                        return [2 /*return*/, {
                                type: 'procedural',
                                title: proc.title,
                                entities: entityResults.map(function (e) { return e.text; }),
                                topics: ['workflow', 'process'],
                                salience: 0.8
                            }];
                    }
                    else {
                        return [2 /*return*/, __assign(__assign({}, extractSemantic(content)), { entities: entityResults.map(function (e) { return e.text; }) })];
                    }
                    return [2 /*return*/];
            }
        });
    });
}
