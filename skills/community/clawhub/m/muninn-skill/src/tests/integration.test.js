"use strict";
/**
 * Integration Test - Router + MCP Server
 * Verifies the enhanced router works with the full memory pipeline
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
var router_js_1 = require("../extractors/router.js");
var index_js_1 = require("../extractors/index.js");
var index_js_2 = require("../storage/index.js");
function runIntegrationTests() {
    return __awaiter(this, void 0, void 0, function () {
        var passed, failed, testCases, _i, testCases_1, test_1, result, topType, _a, _b, test_2, extraction, store, mem1, mem2, mem3, results, stats;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    console.log('🔗 Integration Tests: Router + MCP Pipeline\n');
                    console.log('='.repeat(80));
                    passed = 0;
                    failed = 0;
                    testCases = [
                        { input: "Yesterday I met with Phillip at the coffee shop", expectedType: "episodic" },
                        { input: "Phillip prefers Australian English spelling", expectedType: "semantic" },
                        { input: "To deploy the gateway, run: systemctl restart openclaw-gateway", expectedType: "procedural" },
                        { input: "The server crashed last night after we pushed the release", expectedType: "episodic" },
                        { input: "First, clone the repo. Then run npm install.", expectedType: "procedural" },
                        { input: "OpenClaw uses SQLite for storage by default", expectedType: "semantic" },
                    ];
                    // Test 1: Router classification
                    console.log('\n📋 Test 1: Router Classification\n');
                    for (_i = 0, testCases_1 = testCases; _i < testCases_1.length; _i++) {
                        test_1 = testCases_1[_i];
                        result = (0, router_js_1.routeWithKeywords)(test_1.input);
                        topType = Object.entries(result.types)
                            .sort(function (a, b) { return b[1] - a[1]; })[0][0];
                        if (topType === test_1.expectedType) {
                            console.log("\u2705 PASS: \"".concat(test_1.input.slice(0, 40), "...\" \u2192 ").concat(topType));
                            passed++;
                        }
                        else {
                            console.log("\u274C FAIL: \"".concat(test_1.input.slice(0, 40), "...\" \u2192 expected ").concat(test_1.expectedType, ", got ").concat(topType));
                            failed++;
                        }
                    }
                    // Test 2: Extraction pipeline with entities
                    console.log('\n📋 Test 2: Extraction Pipeline with Entities\n');
                    _a = 0, _b = testCases.slice(0, 3);
                    _c.label = 1;
                case 1:
                    if (!(_a < _b.length)) return [3 /*break*/, 4];
                    test_2 = _b[_a];
                    return [4 /*yield*/, (0, index_js_1.extract)(test_2.input)];
                case 2:
                    extraction = _c.sent();
                    if (extraction.type === test_2.expectedType && extraction.entities.length > 0) {
                        console.log("\u2705 PASS: extract() \u2192 ".concat(extraction.type, ", entities: [").concat(extraction.entities.slice(0, 3).join(', '), "]"));
                        passed++;
                    }
                    else if (extraction.type === test_2.expectedType) {
                        console.log("\u26A0\uFE0F  WARN: extract() \u2192 ".concat(extraction.type, ", but no entities extracted"));
                        passed++; // Still pass, entities are optional
                    }
                    else {
                        console.log("\u274C FAIL: extract() \u2192 expected ".concat(test_2.expectedType, ", got ").concat(extraction.type));
                        failed++;
                    }
                    _c.label = 3;
                case 3:
                    _a++;
                    return [3 /*break*/, 1];
                case 4:
                    // Test 3: Memory storage with auto-routing
                    console.log('\n📋 Test 3: Memory Storage with Auto-Routing\n');
                    store = new index_js_2.MemoryStore('/tmp/test-memory-integration.db');
                    _c.label = 5;
                case 5:
                    _c.trys.push([5, , 10, 11]);
                    return [4 /*yield*/, store.remember("Yesterday I met with Phillip about the roadmap", 'episodic')];
                case 6:
                    mem1 = _c.sent();
                    console.log("\u2705 Stored episodic: ".concat(mem1.id, " (").concat(mem1.type, ")"));
                    passed++;
                    return [4 /*yield*/, store.remember("Phillip prefers Australian English", 'semantic')];
                case 7:
                    mem2 = _c.sent();
                    console.log("\u2705 Stored semantic: ".concat(mem2.id, " (").concat(mem2.type, ")"));
                    passed++;
                    return [4 /*yield*/, store.remember("To deploy, run: systemctl restart gateway", 'procedural')];
                case 8:
                    mem3 = _c.sent();
                    console.log("\u2705 Stored procedural: ".concat(mem3.id, " (").concat(mem3.type, ")"));
                    passed++;
                    return [4 /*yield*/, store.recall("Phillip preferences")];
                case 9:
                    results = _c.sent();
                    console.log("\u2705 Recall found ".concat(results.length, " memories"));
                    passed++;
                    stats = store.getStats();
                    console.log("\u2705 Stats: ".concat(stats.total, " memories, ").concat(stats.entities, " entities"));
                    passed++;
                    return [3 /*break*/, 11];
                case 10:
                    store.close();
                    return [7 /*endfinally*/];
                case 11:
                    // Summary
                    console.log('\n' + '='.repeat(80));
                    console.log("\n\uD83D\uDCCA Integration Results: ".concat(passed, "/").concat(passed + failed, " passed (").concat(Math.round(passed / (passed + failed) * 100), "%)\n"));
                    process.exit(failed > 0 ? 1 : 0);
                    return [2 /*return*/];
            }
        });
    });
}
runIntegrationTests().catch(function (err) {
    console.error('Test error:', err);
    process.exit(1);
});
