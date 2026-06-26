"use strict";
/**
 * Entity Extraction Tests
 *
 * Tests for NER-style entity extraction with types.
 * Run: npx ts-node src/tests/entities.test.ts
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
var entities_js_1 = require("../extractors/entities.js");
// Test fixtures - inputs with expected entities
var TEST_CASES = [
    // People
    {
        input: "Yesterday I met with Phillip at the coffee shop to discuss the roadmap",
        expected: [
            { text: "Phillip", type: "person" }
        ]
    },
    {
        input: "Sammy Clemens wrote the content for BrandForge",
        expected: [
            { text: "Sammy Clemens", type: "person" },
            { text: "BrandForge", type: "project" }
        ]
    },
    {
        input: "Charlie Babbage and Donna Paulsen are part of the agent team",
        expected: [
            { text: "Charlie Babbage", type: "person" },
            { text: "Donna Paulsen", type: "person" }
        ]
    },
    // Organizations
    {
        input: "We need to follow up with Elev8Advisory about the partnership",
        expected: [
            { text: "Elev8Advisory", type: "organization" }
        ]
    },
    {
        input: "OpenClaw uses SQLite for storage and Ollama for embeddings",
        expected: [
            { text: "OpenClaw", type: "organization" },
            { text: "SQLite", type: "technology" },
            { text: "Ollama", type: "technology" }
        ]
    },
    // Projects
    {
        input: "Mission Control dashboard now shows NRL Fantasy tracking",
        expected: [
            { text: "Mission Control", type: "project" },
            { text: "NRL Fantasy", type: "project" }
        ]
    },
    {
        input: "GigHunter is scraping remote jobs from multiple platforms",
        expected: [
            { text: "GigHunter", type: "project" }
        ]
    },
    // Technologies
    {
        input: "The router is built with TypeScript and uses better-sqlite3",
        expected: [
            { text: "TypeScript", type: "technology" },
            { text: "better-sqlite3", type: "technology" }
        ]
    },
    {
        input: "We're using React for the frontend and Node.js for the backend",
        expected: [
            { text: "React", type: "technology" },
            { text: "Node.js", type: "technology" }
        ]
    },
    // Locations
    {
        input: "Phillip is based in Brisbane, Australia",
        expected: [
            { text: "Phillip", type: "person" },
            { text: "Brisbane", type: "location" },
            { text: "Australia", type: "location" }
        ]
    },
    {
        input: "The team met at the Sydney office last week",
        expected: [
            { text: "Sydney", type: "location" }
        ]
    },
    // Events
    {
        input: "We discussed the Q1 planning session and the product launch",
        expected: [
            { text: "Q1 planning session", type: "event" },
            { text: "product launch", type: "event" }
        ]
    },
    // Concepts
    {
        input: "The memory system uses embeddings for semantic search",
        expected: [
            { text: "memory system", type: "project" }, // Could be concept or project
            { text: "embeddings", type: "technology" }, // Could be concept or technology
            { text: "semantic search", type: "technology" } // Could be concept or technology
        ]
    },
    // Mixed - complex cases
    {
        input: "Yesterday Charlie deployed Muninn to the homelab server using Docker",
        expected: [
            { text: "Charlie", type: "person" },
            { text: "Muninn", type: "project" },
            { text: "homelab", type: "location" },
            { text: "Docker", type: "technology" }
        ]
    },
    {
        input: "Phillip prefers Australian English and uses VS Code for development",
        expected: [
            { text: "Phillip", type: "person" },
            { text: "Australian English", type: "concept" },
            { text: "VS Code", type: "technology" }
        ]
    },
    // Edge cases - should NOT extract
    {
        input: "The system should handle this automatically",
        expected: [] // No named entities
    },
    {
        input: "We need to think about how to approach this problem",
        expected: [] // No named entities
    },
    // Typos and variations
    {
        input: "phillip and sammy discussed the project yesterday",
        expected: [
            { text: "phillip", type: "person" },
            { text: "sammy", type: "person" }
        ]
    },
];
function runEntityTests() {
    return __awaiter(this, void 0, void 0, function () {
        var results, passed, failed, _i, TEST_CASES_1, test_1, entities, matched, _loop_1, _a, _b, expected, precision, recall, correct, avgPrecision, avgRecall;
        return __generator(this, function (_c) {
            results = [];
            passed = 0;
            failed = 0;
            console.log('🧪 Entity Extraction Tests\n');
            console.log('='.repeat(80));
            for (_i = 0, TEST_CASES_1 = TEST_CASES; _i < TEST_CASES_1.length; _i++) {
                test_1 = TEST_CASES_1[_i];
                entities = (0, entities_js_1.extractEntities)(test_1.input);
                matched = 0;
                _loop_1 = function (expected) {
                    var found = entities.find(function (e) {
                        return e.text.toLowerCase() === expected.text.toLowerCase() &&
                            e.type === expected.type;
                    });
                    if (found)
                        matched++;
                };
                for (_a = 0, _b = test_1.expected; _a < _b.length; _a++) {
                    expected = _b[_a];
                    _loop_1(expected);
                }
                precision = entities.length > 0 ? matched / entities.length : (test_1.expected.length === 0 ? 1 : 0);
                recall = test_1.expected.length > 0 ? matched / test_1.expected.length : 1;
                correct = recall >= 1.0 && precision >= 0.5;
                if (correct) {
                    passed++;
                    console.log("\u2705 PASS: \"".concat(test_1.input.slice(0, 50), "...\""));
                    console.log("   Found: ".concat(entities.map(function (e) { return "".concat(e.text, "(").concat(e.type, ")"); }).join(', ') || 'none'));
                }
                else {
                    failed++;
                    console.log("\u274C FAIL: \"".concat(test_1.input.slice(0, 50), "...\""));
                    console.log("   Expected: ".concat(test_1.expected.map(function (e) { return "".concat(e.text, "(").concat(e.type, ")"); }).join(', ') || 'none'));
                    console.log("   Got: ".concat(entities.map(function (e) { return "".concat(e.text, "(").concat(e.type, ")"); }).join(', ') || 'none'));
                    console.log("   Precision: ".concat((precision * 100).toFixed(0), "%, Recall: ").concat((recall * 100).toFixed(0), "%"));
                }
                results.push({
                    input: test_1.input,
                    expected: test_1.expected.map(function (e) { return ({ text: e.text, type: e.type, confidence: 1, context: '' }); }),
                    actual: entities,
                    correct: correct,
                    precision: precision,
                    recall: recall
                });
            }
            console.log('\n' + '='.repeat(80));
            console.log("\n\uD83D\uDCCA Results: ".concat(passed, "/").concat(TEST_CASES.length, " passed (").concat(Math.round(passed / TEST_CASES.length * 100), "%)"));
            avgPrecision = results.reduce(function (sum, r) { return sum + r.precision; }, 0) / results.length;
            avgRecall = results.reduce(function (sum, r) { return sum + r.recall; }, 0) / results.length;
            console.log("\uD83D\uDCCA Average Precision: ".concat((avgPrecision * 100).toFixed(0), "%"));
            console.log("\uD83D\uDCCA Average Recall: ".concat((avgRecall * 100).toFixed(0), "%"));
            return [2 /*return*/, { passed: passed, failed: failed, results: results }];
        });
    });
}
// Run tests
runEntityTests()
    .then(function (_a) {
    var passed = _a.passed, failed = _a.failed;
    process.exit(failed > 0 ? 1 : 0);
})
    .catch(function (err) {
    console.error('Test error:', err);
    process.exit(1);
});
