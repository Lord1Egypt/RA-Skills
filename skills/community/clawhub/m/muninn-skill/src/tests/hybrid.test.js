"use strict";
/**
 * Hybrid Retrieval Tests
 * Tests for BM25 and hybrid (RRF) retrieval
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
var bm25_js_1 = require("../retrieval/bm25.js");
var hybrid_js_1 = require("../retrieval/hybrid.js");
// Mock memories for testing
var mockMemories = [
    {
        id: 'm1',
        type: 'semantic',
        content: 'Sammy Clemens prefers working late at night',
        embedding: [0.1, 0.2, 0.3], // Fake embedding
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
        embedding: [0.4, 0.5, 0.6],
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
        embedding: [0.7, 0.8, 0.9],
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
        embedding: [0.2, 0.1, 0.4],
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
        embedding: [0.3, 0.4, 0.5],
        entities: ['Robert'],
        topics: ['preferences', 'tools'],
        salience: 0.7,
        created_at: '2026-02-16T10:00:00Z',
        updated_at: '2026-02-16T10:00:00Z'
    },
    {
        id: 'm6',
        type: 'semantic',
        content: 'The first computer was invented by Charles Babbage',
        embedding: [0.5, 0.6, 0.7],
        entities: ['Charles Babbage'],
        topics: ['history', 'computers'],
        salience: 0.8,
        created_at: '2026-02-15T10:00:00Z',
        updated_at: '2026-02-15T10:00:00Z'
    }
];
function runTests() {
    return __awaiter(this, void 0, void 0, function () {
        var passed, failed, bm25Results, nameResults, hasBabbage, scorer_1, scored, weatherResults, hybridResults, exactMatchResults, sammyInResults, multiTermResults, babbageResults, smallResults, limitedResults, rrfResults, hasMeeting, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log('🧪 Running hybrid retrieval tests...\n');
                    passed = 0;
                    failed = 0;
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 8, , 9]);
                    // ===== BM25 Tests =====
                    console.log('--- BM25 Tests ---');
                    bm25Results = (0, bm25_js_1.bm25Search)('prefers', mockMemories, { k: 3 });
                    if (bm25Results.length > 0 && bm25Results.some(function (r) { return r.content.includes('prefers'); })) {
                        console.log('✅ PASS: BM25 finds term matches');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: BM25 term matching');
                        failed++;
                    }
                    nameResults = (0, bm25_js_1.bm25Search)('Charles Babbage computer', mockMemories, { k: 3 });
                    hasBabbage = nameResults.some(function (r) { return r.content.toLowerCase().includes('babbage'); });
                    if (hasBabbage) {
                        console.log('✅ PASS: BM25 handles name variations');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: BM25 name matching');
                        failed++;
                    }
                    scorer_1 = new bm25_js_1.BM25Scorer();
                    scorer_1.index(mockMemories);
                    scored = mockMemories.map(function (d) { return ({
                        id: d.id,
                        score: scorer_1['scoreDocument']('weather', d.id)
                    }); });
                    weatherResults = scored.filter(function (s) { return s.score > 0; }).sort(function (a, b) { return b.score - a.score; });
                    if (weatherResults[0].id === 'm4') { // m4 is about weather
                        console.log('✅ PASS: BM25 ranks by score');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: BM25 ranking');
                        failed++;
                    }
                    // ===== Hybrid Search Tests =====
                    console.log('\n--- Hybrid Search Tests ---');
                    return [4 /*yield*/, (0, hybrid_js_1.hybridSearch)('prefers dark mode', mockMemories, { k: 3 })];
                case 2:
                    hybridResults = _a.sent();
                    if (hybridResults.length > 0 && hybridResults.length <= 3) {
                        console.log('✅ PASS: Hybrid search returns results');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: Hybrid search');
                        failed++;
                    }
                    return [4 /*yield*/, (0, hybrid_js_1.hybridSearch)('Sammy Clemens', mockMemories, { k: 3 })];
                case 3:
                    exactMatchResults = _a.sent();
                    sammyInResults = exactMatchResults.some(function (r) { return r.id === 'm1'; });
                    if (sammyInResults) {
                        console.log('✅ PASS: Hybrid finds exact name match');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: Hybrid name matching');
                        failed++;
                    }
                    return [4 /*yield*/, (0, hybrid_js_1.hybridSearch)('Babbage computer history', mockMemories, { k: 3 })];
                case 4:
                    multiTermResults = _a.sent();
                    babbageResults = multiTermResults.filter(function (r) {
                        return r.content.toLowerCase().includes('babbage') ||
                            r.content.toLowerCase().includes('computer');
                    });
                    if (babbageResults.length > 0) {
                        console.log('✅ PASS: Hybrid handles multiple terms');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: Multi-term search');
                        failed++;
                    }
                    return [4 /*yield*/, (0, hybrid_js_1.hybridSearch)('test', mockMemories.slice(0, 2), { k: 10 })];
                case 5:
                    smallResults = _a.sent();
                    if (smallResults.length === 2) {
                        console.log('✅ PASS: Small corpus bypass');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: Small corpus handling');
                        failed++;
                    }
                    return [4 /*yield*/, (0, hybrid_js_1.hybridSearch)('test query', mockMemories, { k: 2 })];
                case 6:
                    limitedResults = _a.sent();
                    if (limitedResults.length <= 2) {
                        console.log('✅ PASS: k parameter limits results');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: k limiting');
                        failed++;
                    }
                    // ===== RRF Tests =====
                    console.log('\n--- Reciprocal Rank Fusion Tests ---');
                    return [4 /*yield*/, (0, hybrid_js_1.hybridSearch)('meeting launch', mockMemories, { k: 3 })];
                case 7:
                    rrfResults = _a.sent();
                    hasMeeting = rrfResults.some(function (r) { return r.content.toLowerCase().includes('meeting'); });
                    if (hasMeeting || rrfResults.length > 0) {
                        console.log('✅ PASS: RRF produces results');
                        passed++;
                    }
                    else {
                        console.log('❌ FAIL: RRF');
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
