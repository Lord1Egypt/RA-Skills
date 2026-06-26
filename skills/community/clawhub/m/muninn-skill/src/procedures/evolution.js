"use strict";
/**
 * Procedure Evolution Module
 * LLM-powered failure analysis and auto-improvement
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
exports.analyzeFailure = analyzeFailure;
exports.calculateReliability = calculateReliability;
exports.shouldAutoEvolve = shouldAutoEvolve;
exports.evolveProcedure = evolveProcedure;
/**
 * Analyze a procedure failure using LLM
 */
function analyzeFailure(procedure, failedAtStep, context) {
    return __awaiter(this, void 0, void 0, function () {
        var prompt, response, data, analysis, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    prompt = "You are a workflow optimization expert. Analyze this procedure failure and suggest improvements.\n\nPROCEDURE: \"".concat(procedure.title, "\"\nDESCRIPTION: ").concat(procedure.description || 'N/A', "\n\nSTEPS:\n").concat(procedure.steps.map(function (s, i) { return "".concat(i + 1, ". ").concat(s.description); }).join('\n'), "\n\nFAILURE:\n- Failed at step ").concat(failedAtStep, "\n- Context: ").concat(context, "\n\nAnalyze what went wrong and suggest improved steps. Respond in JSON format:\n{\n  \"failedStep\": <number>,\n  \"failureReason\": \"<why it failed>\",\n  \"suggestedFix\": \"<specific improvement>\",\n  \"newSteps\": [\"<improved step 1>\", \"<improved step 2>\", ...],\n  \"confidence\": <0.0-1.0>\n}");
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 4, , 5]);
                    return [4 /*yield*/, fetch('http://localhost:11434/api/generate', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                model: 'llama3.2:latest',
                                prompt: prompt,
                                format: 'json',
                                stream: false
                            })
                        })];
                case 2:
                    response = _a.sent();
                    if (!response.ok) {
                        throw new Error("LLM request failed: ".concat(response.statusText));
                    }
                    return [4 /*yield*/, response.json()];
                case 3:
                    data = _a.sent();
                    analysis = JSON.parse(data.response);
                    return [2 /*return*/, analysis];
                case 4:
                    error_1 = _a.sent();
                    // Fallback: simple heuristic-based fix
                    return [2 /*return*/, {
                            failedStep: failedAtStep,
                            failureReason: context || 'Unknown failure',
                            suggestedFix: 'Add error handling and retry logic',
                            newSteps: procedure.steps.map(function (s, i) {
                                return i + 1 === failedAtStep
                                    ? "".concat(s.description, " [NOTE: Add error handling]")
                                    : s.description;
                            }),
                            confidence: 0.5
                        }];
                case 5: return [2 /*return*/];
            }
        });
    });
}
/**
 * Calculate reliability score with decay
 * Recent successes count more than old ones
 */
function calculateReliability(procedure) {
    var total = procedure.success_count + procedure.failure_count;
    if (total === 0) {
        return {
            successRate: 0,
            recentTrend: 'stable',
            lastFailures: [],
            reliability: 0
        };
    }
    // Base success rate
    var successRate = procedure.success_count / total;
    // Calculate trend from evolution log
    // Weight recent events more heavily
    var recentEvents = procedure.evolution_log.slice(-5);
    // Calculate weighted score (more recent = higher weight)
    var weightedSuccess = 0;
    var weightedFailure = 0;
    for (var i = 0; i < recentEvents.length; i++) {
        var weight = i + 1; // Older events have lower weight
        var event_1 = recentEvents[i];
        if (event_1.trigger === 'success_pattern') {
            weightedSuccess += weight;
        }
        else if (event_1.trigger === 'failure') {
            weightedFailure += weight;
        }
    }
    var recentTrend;
    if (weightedSuccess > weightedFailure) {
        recentTrend = 'improving';
    }
    else if (weightedFailure > weightedSuccess) {
        recentTrend = 'declining';
    }
    else {
        recentTrend = 'stable';
    }
    var recentFailures = recentEvents.filter(function (e) { return e.trigger === 'failure'; }).length;
    // Decay-weighted reliability
    // More recent events have higher weight
    var decayFactor = 0.9; // Each older event has 90% weight
    var weightedScore = 0;
    var totalWeight = 0;
    for (var i = recentEvents.length - 1; i >= 0; i--) {
        var weight = Math.pow(decayFactor, recentEvents.length - 1 - i);
        var isSuccess = recentEvents[i].trigger === 'success_pattern';
        weightedScore += weight * (isSuccess ? 1 : 0);
        totalWeight += weight;
    }
    var reliability = totalWeight > 0 ? weightedScore / totalWeight : successRate;
    // Extract last failure reasons
    var lastFailures = recentEvents
        .filter(function (e) { return e.trigger === 'failure'; })
        .map(function (e) { return e.change; })
        .slice(0, 3);
    return {
        successRate: successRate,
        recentTrend: recentTrend,
        lastFailures: lastFailures,
        reliability: reliability
    };
}
/**
 * Decide if a procedure should be auto-evolved
 */
function shouldAutoEvolve(procedure) {
    var metrics = calculateReliability(procedure);
    // Auto-evolve if:
    // 1. Reliability is declining
    // 2. At least 2 failures
    // 3. Last failure was recent (within last 3 events)
    var recentFailures = procedure.evolution_log
        .slice(-3)
        .filter(function (e) { return e.trigger === 'failure'; }).length;
    return (metrics.recentTrend === 'declining' &&
        procedure.failure_count >= 2 &&
        recentFailures >= 1);
}
/**
 * Generate improved procedure version
 */
function evolveProcedure(procedure, failedAtStep, context) {
    return __awaiter(this, void 0, void 0, function () {
        var analysis, newSteps, evolutionEvent;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, analyzeFailure(procedure, failedAtStep, context)];
                case 1:
                    analysis = _a.sent();
                    newSteps = analysis.newSteps.map(function (desc, i) { return ({
                        id: "step_".concat(Date.now(), "_").concat(i),
                        order: i + 1,
                        description: desc
                    }); });
                    evolutionEvent = {
                        version: procedure.version + 1,
                        trigger: 'failure',
                        change: "LLM analysis: ".concat(analysis.suggestedFix, ". Confidence: ").concat((analysis.confidence * 100).toFixed(0), "%"),
                        timestamp: new Date().toISOString()
                    };
                    return [2 /*return*/, {
                            newSteps: newSteps,
                            evolutionEvent: evolutionEvent,
                            analysis: analysis
                        }];
            }
        });
    });
}
