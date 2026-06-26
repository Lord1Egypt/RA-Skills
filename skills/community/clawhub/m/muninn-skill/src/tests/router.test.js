"use strict";
/**
 * Content Router Tests
 *
 * Tests for LLM-powered content classification.
 * Run: npx ts-node src/tests/router.test.ts
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
// Test fixtures - 20 inputs with expected classifications
var TEST_CASES = [
    // Episodic (events, conversations, things that happened)
    { input: "Yesterday I met with Phillip at the coffee shop to discuss the project roadmap", expected: { episodic: true, semantic: false, procedural: false } },
    { input: "We had a meeting about the Q1 targets and decided to pivot the strategy", expected: { episodic: true, semantic: false, procedural: false } },
    { input: "Today I learned that the API is rate limiting at 100 requests per minute", expected: { episodic: true, semantic: false, procedural: false } },
    { input: "The client called and mentioned they're unhappy with the current timeline", expected: { episodic: true, semantic: false, procedural: false } },
    { input: "Last week's deployment caused a 2-hour outage due to a database migration issue", expected: { episodic: true, semantic: false, procedural: false } },
    // Semantic (facts, preferences, knowledge)
    { input: "Phillip prefers Australian English spelling and high signal-to-noise communication", expected: { episodic: false, semantic: true, procedural: false } },
    { input: "The OpenClaw gateway runs on port 18789 by default", expected: { episodic: false, semantic: true, procedural: false } },
    { input: "Elev8Advisory's revenue target is $2000 per month", expected: { episodic: false, semantic: true, procedural: false } },
    { input: "MongoDB uses BSON for document storage which supports more data types than JSON", expected: { episodic: false, semantic: true, procedural: false } },
    { input: "Phillip's timezone is Australia/Brisbane (AEST)", expected: { episodic: false, semantic: true, procedural: false } },
    // Procedural (workflows, how-tos, processes)
    { input: "To deploy the gateway, run: systemctl --user restart openclaw-gateway", expected: { episodic: false, semantic: false, procedural: true } },
    { input: "The heartbeat check protocol involves reading HEARTBEAT.md, checking the state file, and executing the appropriate window task", expected: { episodic: false, semantic: false, procedural: true } },
    { input: "First, clone the repo. Then install dependencies with npm install. Finally, run npm start.", expected: { episodic: false, semantic: false, procedural: true } },
    { input: "When the Telegram channel fails, check IPv6 connectivity and force IPv4 with IPAddressDeny=any", expected: { episodic: false, semantic: false, procedural: true } },
    { input: "The job application process: 1) Find posting, 2) Apply via form, 3) Log to JSON, 4) Track responses", expected: { episodic: false, semantic: false, procedural: true } },
    // Ambiguous cases (should report lower confidence)
    { input: "I think we should automate the testing process", expected: { episodic: false, semantic: true, procedural: true }, ambiguous: true },
    { input: "The new feature was discussed in yesterday's meeting and requires a build step", expected: { episodic: true, semantic: false, procedural: true }, ambiguous: true },
    { input: "Charlie built the memory system and it stores facts in SQLite", expected: { episodic: true, semantic: true, procedural: false }, ambiguous: true },
    // Additional edge cases
    { input: "The server crashed yesterday after we pushed the new release", expected: { episodic: true, semantic: false, procedural: false } },
    { input: "Before starting, make sure you have Node.js installed", expected: { episodic: false, semantic: false, procedural: true } },
    { input: "OpenClaw uses SQLite for storage and Ollama for embeddings", expected: { episodic: false, semantic: true, procedural: false } },
    { input: "We agreed to meet again next Tuesday to review the progress", expected: { episodic: true, semantic: false, procedural: false } },
    // ========================================
    // MESSY INPUT - Typos, informal, slang
    // ========================================
    // Typos and misspellings - Episodic
    { input: "yestrday i met with phillip at the coffe shop and we tlaked about roadmap", expected: { episodic: true, semantic: false, procedural: false }, messy: true },
    { input: "the deployemnt last nite caused a huge outgae and everything was broken lol", expected: { episodic: true, semantic: false, procedural: false }, messy: true },
    { input: "client called and sed their not happy with timline", expected: { episodic: true, semantic: false, procedural: false }, messy: true },
    { input: "we discused the Q1 targets yestrday and decided to piviot", expected: { episodic: true, semantic: false, procedural: false }, messy: true },
    { input: "today i lernt that the api rate limts at 100 req/min", expected: { episodic: true, semantic: false, procedural: false }, messy: true },
    // Typos and misspellings - Semantic
    { input: "phillip perfers australian english speling", expected: { episodic: false, semantic: true, procedural: false }, messy: true },
    { input: "the gatway runs on port 18789 by defalt", expected: { episodic: false, semantic: true, procedural: false }, messy: true },
    { input: "elev8advisory reveneu target is 2k/month", expected: { episodic: false, semantic: true, procedural: false }, messy: true },
    { input: "mongodb uses bson for storarge which is better than json", expected: { episodic: false, semantic: true, procedural: false }, messy: true },
    // Typos and misspellings - Procedural
    { input: "to deploy run: systemctl restart openclaw-gatway", expected: { episodic: false, semantic: false, procedural: true }, messy: true },
    { input: "first clone the repo then npm isntall then npm start", expected: { episodic: false, semantic: false, procedural: true }, messy: true },
    { input: "when telegram fails chck ipv6 and force ipv4", expected: { episodic: false, semantic: false, procedural: true }, messy: true },
    { input: "1) find job 2) apply 3) track respnses 4) profit", expected: { episodic: false, semantic: false, procedural: true }, messy: true },
    // Informal/slang
    { input: "bro the server literally crashed after we pushed that garbage code smh", expected: { episodic: true, semantic: false, procedural: false }, messy: true },
    { input: "ngl phillip hates corporate jargon with a passion", expected: { episodic: false, semantic: true, procedural: false }, messy: true },
    { input: "ur gonna wanna restart the service before testing just saying", expected: { episodic: false, semantic: false, procedural: true }, messy: true },
    { input: "the api is total garbage rn rate limiting every 5 seconds lol", expected: { episodic: true, semantic: true, procedural: false }, ambiguous: true },
    // Run-on sentences, no punctuation
    { input: "so yesterday we had this meeting and phillip was like we need to pivot and i was like yeah makes sense", expected: { episodic: true, semantic: false, procedural: false }, messy: true },
    { input: "gateway port is 18789 thats the default just fyi", expected: { episodic: false, semantic: true, procedural: false }, messy: true },
    { input: "first you clone then you install then you run pretty simple", expected: { episodic: false, semantic: false, procedural: true }, messy: true },
    // All lowercase
    { input: "yesterday met phillip coffee shop discuss roadmap", expected: { episodic: true, semantic: false, procedural: false }, messy: true },
    { input: "phillip prefers australian english spelling", expected: { episodic: false, semantic: true, procedural: false }, messy: true },
    { input: "clone repo install deps run start", expected: { episodic: false, semantic: false, procedural: true }, messy: true },
    // Very short fragments
    { input: "met phillip yesterday", expected: { episodic: true, semantic: false, procedural: false }, messy: true },
    { input: "gateway port 18789", expected: { episodic: false, semantic: true, procedural: false }, messy: true },
    { input: "restart service if fails", expected: { episodic: false, semantic: false, procedural: true }, messy: true },
];
function runRouterTests() {
    return __awaiter(this, void 0, void 0, function () {
        var results, passed, failed, _i, TEST_CASES_1, test_1, result, expectedTypes, expectedPrimaries, primaryActual, correct;
        return __generator(this, function (_a) {
            results = [];
            passed = 0;
            failed = 0;
            console.log('🧪 Content Router Tests\n');
            console.log('='.repeat(80));
            for (_i = 0, TEST_CASES_1 = TEST_CASES; _i < TEST_CASES_1.length; _i++) {
                test_1 = TEST_CASES_1[_i];
                result = (0, router_js_1.routeWithKeywords)(test_1.input);
                expectedTypes = test_1.expected;
                expectedPrimaries = Object.entries(expectedTypes)
                    .filter(function (_a) {
                    var _ = _a[0], v = _a[1];
                    return v;
                })
                    .map(function (_a) {
                    var k = _a[0];
                    return k;
                });
                primaryActual = Object.entries(result.types)
                    .sort(function (a, b) { return b[1] - a[1]; })[0][0];
                correct = test_1.ambiguous
                    ? expectedPrimaries.includes(primaryActual)
                    : primaryActual === expectedPrimaries[0];
                if (correct) {
                    passed++;
                    console.log("\u2705 PASS: \"".concat(test_1.input.slice(0, 50), "...\""));
                }
                else {
                    failed++;
                    console.log("\u274C FAIL: \"".concat(test_1.input.slice(0, 50), "...\""));
                    console.log("   Expected: ".concat(expectedPrimaries.join(' or '), ", Got: ").concat(primaryActual));
                }
                results.push({
                    input: test_1.input,
                    expected: test_1.expected,
                    actual: result.types,
                    correct: correct,
                    confidence: result.confidence,
                });
            }
            console.log('\n' + '='.repeat(80));
            console.log("\n\uD83D\uDCCA Results: ".concat(passed, "/").concat(TEST_CASES.length, " passed (").concat(Math.round(passed / TEST_CASES.length * 100), "%)"));
            return [2 /*return*/, { passed: passed, failed: failed, results: results }];
        });
    });
}
// Run tests
runRouterTests()
    .then(function (_a) {
    var passed = _a.passed, failed = _a.failed;
    process.exit(failed > 0 ? 1 : 0);
})
    .catch(function (err) {
    console.error('Test error:', err);
    process.exit(1);
});
