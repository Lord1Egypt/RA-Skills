"use strict";
/**
 * Compare simple vs hybrid retrieval
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
function run() {
    return __awaiter(this, void 0, void 0, function () {
        var store, facts, conversations, _i, facts_1, fact, _a, conversations_1, conv, query, results, top3, hasSemanticInTop3;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    console.log('🔍 Comparing Simple vs Hybrid Retrieval\n');
                    store = new index_js_1.default('/tmp/compare-test.db');
                    facts = [
                        { content: 'Tech stack: React frontend, Node.js backend, PostgreSQL', salience: 0.8 },
                        { content: 'Muninn uses Nomic embed text via Ollama for embeddings', salience: 0.8 },
                        { content: 'Current priority: Elev8Advisory first (updated Feb 22)', salience: 0.8 },
                        { content: 'Phillip prefers Australian English for casual, British for formal documents', salience: 0.8 },
                        { content: 'Elev8Advisory target revenue is $1000/month (updated from $2000)', salience: 0.8 },
                    ];
                    conversations = [
                        '[2026-02-10] assistant: Elev8Advisory sounds interesting! AI for HR is a growing space.',
                        '[2026-02-10] user: About 72% complete. Stripe integration is live.',
                        '[2026-02-12] assistant: BrandForge sounds like a natural complement to Elev8Advisory.',
                        '[2026-02-12] user: Yes, both use React frontend and Node.js backend with PostgreSQL.',
                        '[2026-02-15] assistant: Nice classification. What\'s the embedding model?',
                        // Add more episodic to match benchmark ratio
                        '[2026-02-10] user: I\'m building a SaaS called Elev8Advisory.',
                        '[2026-02-10] assistant: That\'s a clear value proposition.',
                        '[2026-02-10] user: Need to finish the AI content generator.',
                        '[2026-02-10] assistant: Those are critical features.',
                        '[2026-02-10] user: I work with an AI agent named KakāpōHiko.',
                        '[2026-02-12] user: I prefer Australian English spelling in all content.',
                        '[2026-02-12] assistant: Got it! I\'ll use Australian English.',
                        '[2026-02-12] user: I hate corporate jargon.',
                        '[2026-02-12] assistant: Noted - direct, authentic communication.',
                        '[2026-02-12] user: My background is in psychology and business.',
                        '[2026-02-12] assistant: Psychology and business - powerful combination.',
                        '[2026-02-12] user: BrandForge is another one - AI-powered branding tool.',
                        '[2026-02-12] assistant: Same tech stack?',
                        '[2026-02-12] user: Yes, both use React frontend.',
                        '[2026-02-15] assistant: Good to know. Is that configurable?',
                    ];
                    _i = 0, facts_1 = facts;
                    _b.label = 1;
                case 1:
                    if (!(_i < facts_1.length)) return [3 /*break*/, 4];
                    fact = facts_1[_i];
                    return [4 /*yield*/, store.remember(fact.content, 'semantic', { salience: fact.salience })];
                case 2:
                    _b.sent();
                    _b.label = 3;
                case 3:
                    _i++;
                    return [3 /*break*/, 1];
                case 4:
                    _a = 0, conversations_1 = conversations;
                    _b.label = 5;
                case 5:
                    if (!(_a < conversations_1.length)) return [3 /*break*/, 8];
                    conv = conversations_1[_a];
                    return [4 /*yield*/, store.remember(conv, 'episodic', { salience: 0.5 })];
                case 6:
                    _b.sent();
                    _b.label = 7;
                case 7:
                    _a++;
                    return [3 /*break*/, 5];
                case 8:
                    console.log("Stored ".concat(facts.length, " semantic + ").concat(conversations.length, " episodic memories\n"));
                    query = 'What tech stack does Phillip use for his projects?';
                    return [4 /*yield*/, store.recall(query, { limit: 5 })];
                case 9:
                    results = _b.sent();
                    console.log("Query: \"".concat(query, "\"\n"));
                    console.log('Top 5 results:');
                    results.forEach(function (r, i) {
                        console.log("".concat(i + 1, ". [").concat(r.type, "] [sal: ").concat(r.salience, "] ").concat(r.content.slice(0, 60), "..."));
                    });
                    top3 = results.slice(0, 3);
                    hasSemanticInTop3 = top3.some(function (r) { return r.type === 'semantic'; });
                    console.log("\nSemantic memory in top 3: ".concat(hasSemanticInTop3 ? '✅' : '❌'));
                    store.close();
                    return [2 /*return*/];
            }
        });
    });
}
run().catch(console.error);
