"use strict";
/**
 * Retrieval Filter Tests
 * Tests for LLM-based post-filtering on retrieval results
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
var filter_js_1 = require("../retrieval/filter.js");
// Mock memories for testing
var mockMemories = [
    {
        id: 'm1',
        type: 'semantic',
        content: 'Sammy Clemens prefers working late at night',
        embedding: [],
        entities: ['Sammy Clemens'],
        topics: ['preferences', 'work habits'],
        salience: 0.8,
        created_at: '2026-02-20T10:00:00Z',
        updated_at: '2026-02-20T10:00:00Z'
    },
    {
        id: 'm2',
        type: 'semantic',
        content: 'Charlie Babbage built the first mechanical computer in 1837',
        embedding: [],
        entities: ['Charlie Babbage'],
        topics: ['history', 'inventions'],
        salience: 0.9,
        created_at: '2026-02-19T10:00:00Z',
        updated_at: '2026-02-19T10:00:00Z'
    },
    {
        id: 'm3',
        type: 'episodic',
        content: 'Meeting with the team about the new feature launch',
        embedding: [],
        entities: ['team'],
        topics: ['meetings', 'product'],
        salience: 0.6,
        created_at: '2026-02-18T10:00:00Z',
        updated_at: '2026-02-18T10:00:00Z'
    },
    {
        id: 'm4',
        type: 'semantic',
        content: 'The weather in New York City is sunny today',
        embedding: [],
        entities: ['New York City'],
        topics: ['weather'],
        salience: 0.3,
        created_at: '2026-02-17T10:00:00Z',
        updated_at: '2026-02-17T10:00:00Z'
    },
    {
        id: 'm5',
        type: 'semantic',
        content: 'Robert prefers dark mode in VS Code settings',
        embedding: [],
        entities: ['Robert'],
        topics: ['preferences', 'tools'],
        salience: 0.7,
        created_at: '2026-02-16T10:00:00Z',
        updated_at: '2026-02-16T10:00:00Z'
    }
];
// Simple test runner
function runTests() {
    return __awaiter(this, void 0, void 0, function () {
        var passed, failed, result, smallList, promptUsed_1, error_1;
        var _this = this;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log('🧪 Running filter tests...\n');
                    passed = 0;
                    failed = 0;
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 8, , 9]);
                    return [4 /*yield*/, (0, filter_js_1.filterMemories)('test', [])];
                case 2:
                    result = _a.sent();
                    if (result.length === 0) {
                        console.log('✅ PASS: Empty list returns empty');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: Empty list should return empty');
                        failed++;
                    }
                    smallList = mockMemories.slice(0, 2);
                    return [4 /*yield*/, (0, filter_js_1.filterMemories)('test', smallList)];
                case 3:
                    result = _a.sent();
                    if (result.length === 2) {
                        console.log('✅ PASS: Small list (2) bypasses LLM');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: Small list should return all');
                        failed++;
                    }
                    // Test 3: LLM filtering
                    globalThis.generateLLMResponse = function () { return __awaiter(_this, void 0, void 0, function () {
                        return __generator(this, function (_a) {
                            return [2 /*return*/, JSON.stringify({ relevantIndices: [0, 2, 4] })];
                        });
                    }); };
                    return [4 /*yield*/, (0, filter_js_1.filterMemories)('preferences', mockMemories)];
                case 4:
                    result = _a.sent();
                    if (result.length === 3) {
                        console.log('✅ PASS: LLM filtering returns filtered results');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: LLM filtering - got', result.length, 'expected 3');
                        failed++;
                    }
                    return [4 /*yield*/, (0, filter_js_1.filterMemories)('test', mockMemories, { k: 2 })];
                case 5:
                    // Test 4: k limiting
                    result = _a.sent();
                    if (result.length <= 2) {
                        console.log('✅ PASS: k limiting works');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: k limiting - got', result.length);
                        failed++;
                    }
                    // Test 5: Error handling - fallback
                    globalThis.generateLLMResponse = function () { return __awaiter(_this, void 0, void 0, function () {
                        return __generator(this, function (_a) {
                            throw new Error('LLM fail');
                        });
                    }); };
                    return [4 /*yield*/, (0, filter_js_1.filterMemories)('test', mockMemories.slice(0, 3))];
                case 6:
                    result = _a.sent();
                    if (result.length === 3) {
                        console.log('✅ PASS: Error fallback returns original sorted by salience');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: Error fallback - got', result.length);
                        failed++;
                    }
                    promptUsed_1 = '';
                    globalThis.generateLLMResponse = function (prompt) { return __awaiter(_this, void 0, void 0, function () {
                        return __generator(this, function (_a) {
                            promptUsed_1 = prompt;
                            return [2 /*return*/, JSON.stringify({ relevantIndices: [0, 1] })];
                        });
                    }); };
                    return [4 /*yield*/, (0, filter_js_1.filterMemories)('developer preferences', mockMemories.slice(0, 3))];
                case 7:
                    _a.sent();
                    if (promptUsed_1.toLowerCase().includes('uncertain') ||
                        promptUsed_1.toLowerCase().includes('include') ||
                        promptUsed_1.toLowerCase().includes('relevant')) {
                        console.log('✅ PASS: Recall-biased prompt language present');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: Prompt missing recall-biased language');
                        failed++;
                    }
                    console.log("\n\uD83D\uDCCA Results: ".concat(passed, " passed, ").concat(failed, " failed"));
                    if (failed > 0) {
                        process.exit(1);
                    }
                    console.log('\n✅ All tests passed!');
                    return [3 /*break*/, 9];
                case 8:
                    error_1 = _a.sent();
                    console.error('❌ Test failed:', error_1);
                    process.exit(1);
                    return [3 /*break*/, 9];
                case 9: return [2 /*return*/];
            }
        });
    });
}
// Run if executed directly
runTests();
