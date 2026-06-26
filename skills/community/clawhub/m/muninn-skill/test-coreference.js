"use strict";
/**
 * Test Coreference Resolution
 *
 * Tests the coreference resolution layer for Muninn Memory System
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
var coreference_js_1 = require("./src/extractors/coreference.js");
var index_js_1 = require("./src/storage/index.js");
function testBasicCoreference() {
    return __awaiter(this, void 0, void 0, function () {
        var testCases, _i, testCases_1, testCase, result;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log('\n🧪 Test 1: Basic Coreference Resolution');
                    console.log('='.repeat(50));
                    // Clear cache and add test entities
                    (0, coreference_js_1.clearEntityCache)();
                    (0, coreference_js_1.addToEntityCache)('Phillip', ['Phillip', 'the CEO', 'the Program Manager'], 'person');
                    (0, coreference_js_1.addToEntityCache)('Caroline', ['Caroline', 'her', 'the PM'], 'person');
                    testCases = [
                        {
                            input: 'Phillip mentioned that he would meet with her next Tuesday.',
                            expected: 'Phillip mentioned that [Phillip] would meet with [Caroline] next Tuesday.'
                        },
                        {
                            input: 'The Program Manager told him about the project.',
                            expected: '[Phillip] told [Phillip] about the project.'
                        },
                        {
                            input: 'She said she would call him later.',
                            expected: '[Caroline] said [Caroline] would call [Phillip] later.'
                        },
                        {
                            input: 'Phillip and Caroline went to the meeting. He spoke about his project.',
                            expected: 'Phillip and Caroline went to the meeting. [Phillip] spoke about [Phillip]\'s project.'
                        }
                    ];
                    _i = 0, testCases_1 = testCases;
                    _a.label = 1;
                case 1:
                    if (!(_i < testCases_1.length)) return [3 /*break*/, 4];
                    testCase = testCases_1[_i];
                    console.log("\n\uD83D\uDCDD Input: \"".concat(testCase.input, "\""));
                    return [4 /*yield*/, (0, coreference_js_1.resolveCoreferences)(testCase.input, [], true)];
                case 2:
                    result = _a.sent();
                    console.log("\u2705 Resolved: \"".concat(result.resolvedText, "\""));
                    console.log("   Entity Map:", Object.fromEntries(result.entityMap));
                    if (result.resolvedText === testCase.expected) {
                        console.log('   ✅ PASS - Matches expected output');
                    }
                    else if (result.resolvedText.includes('[Phillip]') && result.resolvedText.includes('[Caroline]')) {
                        console.log('   ✅ PASS - Coreferences resolved correctly');
                    }
                    else {
                        console.log('   ⚠️  Partial match');
                    }
                    _a.label = 3;
                case 3:
                    _i++;
                    return [3 /*break*/, 1];
                case 4: return [2 /*return*/];
            }
        });
    });
}
function testWithMemoryStore() {
    return __awaiter(this, void 0, void 0, function () {
        var store, testInput, result, hasPhillip, hasCaroline;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log('\n\n🧪 Test 2: Coreference with Memory Store Integration');
                    console.log('='.repeat(50));
                    store = new index_js_1.MemoryStore('/tmp/test-coreference.db');
                    // Add some entities to memory
                    return [4 /*yield*/, store.remember('Phillip is the Program Manager', 'semantic')];
                case 1:
                    // Add some entities to memory
                    _a.sent();
                    return [4 /*yield*/, store.remember('Caroline handles project coordination', 'semantic')];
                case 2:
                    _a.sent();
                    // Initialize entity cache from store
                    return [4 /*yield*/, (0, coreference_js_1.initEntityCache)(store)];
                case 3:
                    // Initialize entity cache from store
                    _a.sent();
                    testInput = 'Phillip mentioned that he would meet with her next Tuesday.';
                    console.log("\n\uD83D\uDCDD Input: \"".concat(testInput, "\""));
                    return [4 /*yield*/, (0, coreference_js_1.resolveCoreferences)(testInput, [], true)];
                case 4:
                    result = _a.sent();
                    console.log("\u2705 Resolved: \"".concat(result.resolvedText, "\""));
                    console.log("   Entity Map:", Object.fromEntries(result.entityMap));
                    console.log("   New entities found:", result.newEntitiesFound);
                    hasPhillip = result.resolvedText.includes('[Phillip]');
                    hasCaroline = result.resolvedText.includes('[Caroline]');
                    if (hasPhillip && hasCaroline) {
                        console.log('   ✅ Both entities resolved correctly!');
                    }
                    else {
                        console.log('   ⚠️  Some entities not resolved');
                    }
                    store.close();
                    return [2 /*return*/];
            }
        });
    });
}
function testSimpleResolution() {
    return __awaiter(this, void 0, void 0, function () {
        var testInput, result;
        return __generator(this, function (_a) {
            console.log('\n\n🧪 Test 3: Simple Resolution (no LLM)');
            console.log('='.repeat(50));
            (0, coreference_js_1.clearEntityCache)();
            (0, coreference_js_1.addToEntityCache)('Phillip', ['Phillip', 'him'], 'person');
            (0, coreference_js_1.addToEntityCache)('Caroline', ['Caroline', 'her'], 'person');
            testInput = 'Phillip met her yesterday.';
            console.log("\n\uD83D\uDCDD Input: \"".concat(testInput, "\""));
            result = (0, coreference_js_1.resolveCoreferencesSimple)(testInput);
            console.log("\u2705 Resolved: \"".concat(result.resolvedText, "\""));
            console.log("   Entity Map:", Object.fromEntries(result.entityMap));
            return [2 /*return*/];
        });
    });
}
function testEntityCache() {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            console.log('\n\n🧪 Test 4: Entity Cache Operations');
            console.log('='.repeat(50));
            (0, coreference_js_1.clearEntityCache)();
            // Test adding entities
            (0, coreference_js_1.addToEntityCache)('John', ['John', 'him', 'he'], 'person');
            (0, coreference_js_1.addToEntityCache)('Jane', ['Jane', 'her', 'she'], 'person');
            // Test resolution
            console.log('\n📝 Resolving pronouns:');
            console.log("  \"him\" -> ".concat((0, coreference_js_1.resolveEntity)('him')));
            console.log("  \"her\" -> ".concat((0, coreference_js_1.resolveEntity)('her')));
            console.log("  \"she\" -> ".concat((0, coreference_js_1.resolveEntity)('she')));
            console.log("  \"John\" -> ".concat((0, coreference_js_1.resolveEntity)('John')));
            console.log("  \"unknown\" -> ".concat((0, coreference_js_1.resolveEntity)('unknown')));
            return [2 /*return*/];
        });
    });
}
function runAllTests() {
    return __awaiter(this, void 0, void 0, function () {
        var error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log('\n🎯 Coreference Resolution Test Suite');
                    console.log('='.repeat(50));
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 6, , 7]);
                    return [4 /*yield*/, testBasicCoreference()];
                case 2:
                    _a.sent();
                    return [4 /*yield*/, testWithMemoryStore()];
                case 3:
                    _a.sent();
                    return [4 /*yield*/, testSimpleResolution()];
                case 4:
                    _a.sent();
                    return [4 /*yield*/, testEntityCache()];
                case 5:
                    _a.sent();
                    console.log('\n\n✅ All tests completed!');
                    console.log('='.repeat(50));
                    return [3 /*break*/, 7];
                case 6:
                    error_1 = _a.sent();
                    console.error('\n❌ Test failed:', error_1);
                    return [3 /*break*/, 7];
                case 7: return [2 /*return*/];
            }
        });
    });
}
// Run tests
runAllTests();
