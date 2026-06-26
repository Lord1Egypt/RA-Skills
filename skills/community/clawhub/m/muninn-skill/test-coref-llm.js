"use strict";
/**
 * Test Coreference Resolution with LLM
 *
 * Tests the LLM-based coreference resolution
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
console.log('\n🎯 Coreference Resolution - LLM Test Suite');
console.log('='.repeat(50));
// Clear and set up entity cache
(0, coreference_js_1.clearEntityCache)();
(0, coreference_js_1.addToEntityCache)('Phillip', ['Phillip', 'him', 'he', 'the CEO', 'the Program Manager'], 'person');
(0, coreference_js_1.addToEntityCache)('Caroline', ['Caroline', 'her', 'she', 'the PM', 'the Program Manager'], 'person');
function testLLMResolution() {
    return __awaiter(this, void 0, void 0, function () {
        var tests, _i, tests_1, test_1, result, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log('\n🧪 Test: LLM-Based Coreference Resolution');
                    tests = [
                        'Phillip mentioned that he would meet with her next Tuesday.',
                        'The Program Manager told him about the project.',
                        'She said she would call him later.',
                        'Phillip and Caroline went to the meeting. He spoke about his project.',
                        'John talked to Mary. He told her about the new product launch.'
                    ];
                    _i = 0, tests_1 = tests;
                    _a.label = 1;
                case 1:
                    if (!(_i < tests_1.length)) return [3 /*break*/, 6];
                    test_1 = tests_1[_i];
                    console.log("\n\uD83D\uDCDD Input: \"".concat(test_1, "\""));
                    _a.label = 2;
                case 2:
                    _a.trys.push([2, 4, , 5]);
                    return [4 /*yield*/, (0, coreference_js_1.resolveCoreferences)(test_1, [], true)];
                case 3:
                    result = _a.sent();
                    console.log("\u2705 Resolved: \"".concat(result.resolvedText, "\""));
                    console.log("   Entity Map:", Object.fromEntries(result.entityMap));
                    return [3 /*break*/, 5];
                case 4:
                    error_1 = _a.sent();
                    console.log("\u274C Error:", error_1);
                    return [3 /*break*/, 5];
                case 5:
                    _i++;
                    return [3 /*break*/, 1];
                case 6: return [2 /*return*/];
            }
        });
    });
}
function testSimpleComparison() {
    return __awaiter(this, void 0, void 0, function () {
        var test, simpleResult, llmResult;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log('\n\n🧪 Test: Simple vs LLM Comparison');
                    test = 'Phillip mentioned that he would meet with her next Tuesday.';
                    console.log("\n\uD83D\uDCDD Input: \"".concat(test, "\""));
                    console.log('\n--- Simple Resolution ---');
                    simpleResult = (0, coreference_js_1.resolveCoreferencesSimple)(test);
                    console.log("\u2705 \"".concat(simpleResult.resolvedText, "\""));
                    console.log('\n--- LLM Resolution ---');
                    return [4 /*yield*/, (0, coreference_js_1.resolveCoreferences)(test, [], true)];
                case 1:
                    llmResult = _a.sent();
                    console.log("\u2705 \"".concat(llmResult.resolvedText, "\""));
                    return [2 /*return*/];
            }
        });
    });
}
function main() {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, testLLMResolution()];
                case 1:
                    _a.sent();
                    return [4 /*yield*/, testSimpleComparison()];
                case 2:
                    _a.sent();
                    console.log('\n\n✅ Test Suite Complete!');
                    return [2 /*return*/];
            }
        });
    });
}
main().catch(console.error);
