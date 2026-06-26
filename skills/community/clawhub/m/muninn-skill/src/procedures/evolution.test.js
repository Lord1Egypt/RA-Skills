"use strict";
/**
 * Tests for Procedure Evolution Module
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
var evolution_js_1 = require("./evolution.js");
// Test data
var testProcedure = {
    id: 'proc_test123',
    title: 'Deploy to Production',
    description: 'Deploy code to production environment',
    steps: [
        { id: 'step_1', order: 1, description: 'Run tests' },
        { id: 'step_2', order: 2, description: 'Build Docker image' },
        { id: 'step_3', order: 3, description: 'Push to registry' },
        { id: 'step_4', order: 4, description: 'Deploy to cluster' }
    ],
    version: 1,
    success_count: 3,
    failure_count: 2,
    is_reliable: false,
    evolution_log: [
        { version: 1, trigger: 'success_pattern', change: 'Initial success', timestamp: '2026-02-20T10:00:00Z' },
        { version: 1, trigger: 'failure', change: 'Failed at step 3: registry timeout', timestamp: '2026-02-21T14:00:00Z' },
        { version: 1, trigger: 'success_pattern', change: 'Success after retry', timestamp: '2026-02-22T09:00:00Z' },
        { version: 1, trigger: 'failure', change: 'Failed at step 4: cluster unreachable', timestamp: '2026-02-23T16:00:00Z' }
    ],
    created_at: '2026-02-20T08:00:00Z',
    updated_at: '2026-02-23T16:00:00Z'
};
function runTests() {
    return __awaiter(this, void 0, void 0, function () {
        var results, metrics, test1a, test1b, test1c, test1d, shouldEvolve, test2, analysis, test3a, test3b, test3c, test3d, evolution, test4a, test4b, test4c, reliableProcedure, reliableMetrics, shouldNotEvolve, test5a, test5b, _i, results_1, result, passed, total;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    results = [];
                    console.log('🧪 Procedure Evolution Tests\n');
                    console.log('='.repeat(80));
                    // Test 1: calculateReliability
                    console.log('\n📋 Test 1: Reliability Calculation\n');
                    metrics = (0, evolution_js_1.calculateReliability)(testProcedure);
                    test1a = metrics.successRate === 3 / 5;
                    results.push({
                        name: 'Success rate calculation',
                        passed: test1a,
                        message: test1a ? "\u2705 Success rate: ".concat((metrics.successRate * 100).toFixed(0), "%") : "\u274C Expected 60%, got ".concat(metrics.successRate)
                    });
                    test1b = metrics.recentTrend === 'declining';
                    results.push({
                        name: 'Trend detection',
                        passed: test1b,
                        message: test1b ? "\u2705 Trend: ".concat(metrics.recentTrend) : "\u274C Expected declining, got ".concat(metrics.recentTrend)
                    });
                    test1c = metrics.reliability > 0 && metrics.reliability <= 1;
                    results.push({
                        name: 'Reliability score range',
                        passed: test1c,
                        message: test1c ? "\u2705 Reliability: ".concat(metrics.reliability.toFixed(2)) : "\u274C Reliability out of range: ".concat(metrics.reliability)
                    });
                    test1d = metrics.lastFailures.length === 2;
                    results.push({
                        name: 'Last failures extracted',
                        passed: test1d,
                        message: test1d ? "\u2705 Found ".concat(metrics.lastFailures.length, " failures") : "\u274C Expected 2 failures, got ".concat(metrics.lastFailures.length)
                    });
                    // Test 2: shouldAutoEvolve
                    console.log('\n📋 Test 2: Auto-Evolution Decision\n');
                    shouldEvolve = (0, evolution_js_1.shouldAutoEvolve)(testProcedure);
                    test2 = shouldEvolve === true;
                    results.push({
                        name: 'Auto-evolve decision',
                        passed: test2,
                        message: test2
                            ? "\u2705 Correctly identified procedure for auto-evolution"
                            : "\u274C Should have recommended evolution (declining, 2 failures)"
                    });
                    // Test 3: analyzeFailure (LLM call - may fallback)
                    console.log('\n📋 Test 3: Failure Analysis (LLM)\n');
                    return [4 /*yield*/, (0, evolution_js_1.analyzeFailure)(testProcedure, 4, 'cluster unreachable')];
                case 1:
                    analysis = _a.sent();
                    test3a = analysis.failedStep === 4;
                    results.push({
                        name: 'Failed step identified',
                        passed: test3a,
                        message: test3a ? "\u2705 Step ".concat(analysis.failedStep) : "\u274C Expected step 4, got ".concat(analysis.failedStep)
                    });
                    test3b = analysis.failureReason.length > 0;
                    results.push({
                        name: 'Failure reason provided',
                        passed: test3b,
                        message: test3b ? "\u2705 Reason: ".concat(analysis.failureReason.slice(0, 50), "...") : "\u274C No failure reason"
                    });
                    test3c = analysis.newSteps.length > 0;
                    results.push({
                        name: 'New steps suggested',
                        passed: test3c,
                        message: test3c ? "\u2705 ".concat(analysis.newSteps.length, " new steps") : "\u274C No new steps"
                    });
                    test3d = analysis.confidence >= 0 && analysis.confidence <= 1;
                    results.push({
                        name: 'Confidence score valid',
                        passed: test3d,
                        message: test3d ? "\u2705 Confidence: ".concat((analysis.confidence * 100).toFixed(0), "%") : "\u274C Invalid confidence: ".concat(analysis.confidence)
                    });
                    // Test 4: evolveProcedure
                    console.log('\n📋 Test 4: Full Evolution\n');
                    return [4 /*yield*/, (0, evolution_js_1.evolveProcedure)(testProcedure, 4, 'cluster unreachable')];
                case 2:
                    evolution = _a.sent();
                    test4a = evolution.newSteps.length > 0;
                    results.push({
                        name: 'New steps generated',
                        passed: test4a,
                        message: test4a ? "\u2705 ".concat(evolution.newSteps.length, " steps in new version") : "\u274C No steps generated"
                    });
                    test4b = evolution.evolutionEvent.version === 2;
                    results.push({
                        name: 'Version incremented',
                        passed: test4b,
                        message: test4b ? "\u2705 Version ".concat(evolution.evolutionEvent.version) : "\u274C Expected version 2, got ".concat(evolution.evolutionEvent.version)
                    });
                    test4c = evolution.evolutionEvent.trigger === 'failure';
                    results.push({
                        name: 'Evolution trigger recorded',
                        passed: test4c,
                        message: test4c ? "\u2705 Trigger: ".concat(evolution.evolutionEvent.trigger) : "\u274C Wrong trigger: ".concat(evolution.evolutionEvent.trigger)
                    });
                    // Test 5: Reliable procedure (should NOT auto-evolve)
                    console.log('\n📋 Test 5: Stable Procedure Decision\n');
                    reliableProcedure = __assign(__assign({}, testProcedure), { success_count: 10, failure_count: 1, is_reliable: true, evolution_log: [
                            { version: 1, trigger: 'success_pattern', change: 'Success 1', timestamp: '2026-02-20T10:00:00Z' },
                            { version: 1, trigger: 'success_pattern', change: 'Success 2', timestamp: '2026-02-21T10:00:00Z' },
                            { version: 1, trigger: 'success_pattern', change: 'Success 3', timestamp: '2026-02-22T10:00:00Z' }
                        ] });
                    reliableMetrics = (0, evolution_js_1.calculateReliability)(reliableProcedure);
                    shouldNotEvolve = (0, evolution_js_1.shouldAutoEvolve)(reliableProcedure);
                    test5a = reliableMetrics.recentTrend === 'improving';
                    results.push({
                        name: 'Reliable trend detection',
                        passed: test5a,
                        message: test5a ? "\u2705 Trend: improving" : "\u274C Expected improving, got ".concat(reliableMetrics.recentTrend)
                    });
                    test5b = shouldNotEvolve === false;
                    results.push({
                        name: 'Should NOT auto-evolve',
                        passed: test5b,
                        message: test5b ? "\u2705 Correctly skipped evolution" : "\u274C Should not recommend evolution for stable procedure"
                    });
                    // Print results
                    console.log('\n' + '='.repeat(80));
                    console.log('\n📊 Test Results:\n');
                    for (_i = 0, results_1 = results; _i < results_1.length; _i++) {
                        result = results_1[_i];
                        console.log("".concat(result.passed ? '✅' : '❌', " ").concat(result.name, ": ").concat(result.message));
                    }
                    passed = results.filter(function (r) { return r.passed; }).length;
                    total = results.length;
                    console.log("\n".concat('='.repeat(80)));
                    console.log("\n\uD83D\uDCCA Results: ".concat(passed, "/").concat(total, " passed (").concat(Math.round(passed / total * 100), "%)"));
                    if (passed < total) {
                        process.exit(1);
                    }
                    return [2 /*return*/];
            }
        });
    });
}
runTests().catch(console.error);
