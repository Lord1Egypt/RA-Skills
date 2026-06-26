"use strict";
/**
 * Quick LOCOMO test — skip slow embedding generation
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
var index_js_1 = require("../storage/index.js");
var keyFacts = [
    { content: 'Phillip lives in Brisbane, Australia (timezone AEST)', entities: ['Phillip', 'Brisbane', 'Australia'] },
    { content: 'Elev8Advisory is an AI-powered HR tool that helps small businesses create HR policies automatically', entities: ['Elev8Advisory'] },
    { content: 'Elev8Advisory target revenue is $1000/month (updated from $2000)', entities: ['Elev8Advisory'] },
    { content: 'BrandForge is an AI-powered branding tool with $320 revenue', entities: ['BrandForge'] },
    { content: 'Tech stack: React frontend, Node.js backend, PostgreSQL', entities: ['React', 'Node.js', 'PostgreSQL'] },
    { content: 'Muninn is a memory system using SQLite storage and Nomic embeddings via Ollama, stores episodic/semantic/procedural memories', entities: ['Muninn', 'SQLite', 'Ollama'] },
    { content: 'OpenClaw gateway default port is 18789, configurable via OPENCLAW_PORT environment variable', entities: ['OpenClaw'] },
    { content: 'Phillip prefers Australian English for casual, British for formal documents', entities: ['Phillip'] },
    { content: 'KakāpōHiko handles strategy, Sammy Clemens handles content, Charlie Babbage handles code, Donna Paulsen handles operations', entities: ['KakāpōHiko', 'Sammy Clemens', 'Charlie Babbage', 'Donna Paulsen'] },
    { content: "Kakāpō is the world's rarest parrot, Hiko means lightning in Māori", entities: ['KakāpōHiko'] },
    { content: 'Muninn Phase 1 complete: 100% router accuracy, 91% entity precision', entities: ['Muninn'] },
    { content: 'Elev8Advisory has a customer paying $500/month for HR policy generation', entities: ['Elev8Advisory'] },
    { content: 'Current priority: Elev8Advisory first, then BrandForge (updated Feb 22)', entities: ['Elev8Advisory', 'BrandForge'] },
];
var questions = [
    { id: 'q14', query: 'What default port does OpenClaw gateway use?', expected: '18789' },
    { id: 'q11', query: 'Who are all the AI agents on Phillip\'s team?', expected: 'KakāpōHiko' },
    { id: 'q13', query: 'What projects is Phillip building?', expected: 'Elev8Advisory' },
];
function run() {
    return __awaiter(this, void 0, void 0, function () {
        var store, _i, keyFacts_1, fact, _a, questions_1, q, results, topResult, passed;
        var _b;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    console.log('⚡ Quick LOCOMO Test\n');
                    store = new index_js_1.default('/tmp/locomo-quick.db');
                    _i = 0, keyFacts_1 = keyFacts;
                    _c.label = 1;
                case 1:
                    if (!(_i < keyFacts_1.length)) return [3 /*break*/, 4];
                    fact = keyFacts_1[_i];
                    return [4 /*yield*/, store.remember(fact.content, 'semantic', { entities: fact.entities, salience: 0.8 })];
                case 2:
                    _c.sent();
                    _c.label = 3;
                case 3:
                    _i++;
                    return [3 /*break*/, 1];
                case 4:
                    console.log("Stored ".concat(keyFacts.length, " memories\n"));
                    _a = 0, questions_1 = questions;
                    _c.label = 5;
                case 5:
                    if (!(_a < questions_1.length)) return [3 /*break*/, 8];
                    q = questions_1[_a];
                    return [4 /*yield*/, store.recall(q.query, { limit: 3 })];
                case 6:
                    results = _c.sent();
                    topResult = ((_b = results[0]) === null || _b === void 0 ? void 0 : _b.content) || 'N/A';
                    passed = topResult.toLowerCase().includes(q.expected.toLowerCase());
                    console.log("".concat(q.id, ": ").concat(passed ? '✅' : '❌', " \"").concat(topResult.slice(0, 60), "...\""));
                    _c.label = 7;
                case 7:
                    _a++;
                    return [3 /*break*/, 5];
                case 8:
                    store.close();
                    return [2 /*return*/];
            }
        });
    });
}
run().catch(console.error);
