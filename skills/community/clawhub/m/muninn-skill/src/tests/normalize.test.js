"use strict";
/**
 * Tests for Entity Normalization
 *
 * Tests LLM-based entity normalization that resolves pronouns to names,
 * expands abbreviations, normalizes dates, and stores aliases for retrieval.
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
var normalize_js_1 = require("../extractors/normalize.js");
// Mock LLM response generator for testing
var createMockLLM = function (responses) {
    return function (prompt) { return __awaiter(void 0, void 0, void 0, function () {
        var _i, _a, _b, key, response;
        return __generator(this, function (_c) {
            for (_i = 0, _a = Object.entries(responses); _i < _a.length; _i++) {
                _b = _a[_i], key = _b[0], response = _b[1];
                if (prompt.includes(key)) {
                    return [2 /*return*/, response];
                }
            }
            return [2 /*return*/, '[]'];
        });
    }); };
};
// Test runner
function runNormalizationTests() {
    return __awaiter(this, void 0, void 0, function () {
        var passed, failed, mockResponse, mockLLM, text, result, heEntity, err_1, mockResponse, mockLLM, text, result, nycEntity, err_2, mockResponse, mockLLM, text, result, sammyRefs, err_3, failingLLM, text, existingEntities, result, err_4, store, found1, found2, aliases, hasSammy, hasSam, store, found, text, result, nycEntity, err_5, text, result, tomorrowEntity, err_6, text, result, qld, nsw, err_7, text, result, colourEntity, err_8, text, result, organizeEntity, err_9, store_1, text, result, foundUS, foundUK, err_10, text, result, colour, centre, analyse, err_11;
        var _this = this;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log('🧪 Running Entity Normalization Tests\n');
                    console.log('='.repeat(60));
                    passed = 0;
                    failed = 0;
                    console.log('\n📝 Test: Resolves pronouns to canonical names');
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    mockResponse = JSON.stringify([
                        { original: 'He', canonical: 'Phillip', type: 'person', confidence: 0.9 }
                    ]);
                    mockLLM = createMockLLM({
                        'Phillip worked on Muninn': mockResponse
                    });
                    text = "Phillip worked on Muninn. He built the router.";
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text, undefined, mockLLM)];
                case 2:
                    result = _a.sent();
                    heEntity = result.find(function (e) { return e.original === 'He'; });
                    if (heEntity && heEntity.canonical === 'Phillip') {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: He not resolved to Phillip');
                        failed++;
                    }
                    return [3 /*break*/, 4];
                case 3:
                    err_1 = _a.sent();
                    console.log('   ❌ FAIL:', err_1);
                    failed++;
                    return [3 /*break*/, 4];
                case 4:
                    console.log('\n📝 Test: Expands abbreviations');
                    _a.label = 5;
                case 5:
                    _a.trys.push([5, 7, , 8]);
                    mockResponse = JSON.stringify([
                        { original: 'NYC', canonical: 'New York City', type: 'location', confidence: 0.95 }
                    ]);
                    mockLLM = createMockLLM({
                        'Working from NYC': mockResponse
                    });
                    text = "Working from NYC next week.";
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text, undefined, mockLLM)];
                case 6:
                    result = _a.sent();
                    nycEntity = result.find(function (e) { return e.original === 'NYC'; });
                    if (nycEntity && nycEntity.canonical === 'New York City') {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: NYC not expanded');
                        failed++;
                    }
                    return [3 /*break*/, 8];
                case 7:
                    err_2 = _a.sent();
                    console.log('   ❌ FAIL:', err_2);
                    failed++;
                    return [3 /*break*/, 8];
                case 8:
                    console.log('\n📝 Test: Stores aliases for retrieval');
                    _a.label = 9;
                case 9:
                    _a.trys.push([9, 11, , 12]);
                    mockResponse = JSON.stringify([
                        { original: 'Sammy Clemens', canonical: 'Sammy Clemens', type: 'person', confidence: 0.95 },
                        { original: 'Sammy', canonical: 'Sammy Clemens', type: 'person', confidence: 0.9 }
                    ]);
                    mockLLM = createMockLLM({
                        'Sammy Clemens drafted': mockResponse
                    });
                    text = "Sammy Clemens drafted the post. Sammy reviewed it.";
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text, undefined, mockLLM)];
                case 10:
                    result = _a.sent();
                    sammyRefs = result.filter(function (e) { return e.canonical === 'Sammy Clemens'; });
                    if (sammyRefs.length >= 1 && sammyRefs[0].aliases.includes('Sammy Clemens')) {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: Aliases not stored');
                        failed++;
                    }
                    return [3 /*break*/, 12];
                case 11:
                    err_3 = _a.sent();
                    console.log('   ❌ FAIL:', err_3);
                    failed++;
                    return [3 /*break*/, 12];
                case 12:
                    console.log('\n📝 Test: Falls back to original entities on LLM failure');
                    _a.label = 13;
                case 13:
                    _a.trys.push([13, 15, , 16]);
                    failingLLM = function () { return __awaiter(_this, void 0, void 0, function () { return __generator(this, function (_a) {
                        throw new Error('LLM unavailable');
                    }); }); };
                    text = "Phillip worked on Muninn.";
                    existingEntities = [
                        { text: 'Phillip', type: 'person', confidence: 0.95, context: 'Phillip worked' },
                        { text: 'Muninn', type: 'project', confidence: 0.95, context: 'worked on Muninn' }
                    ];
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text, existingEntities, failingLLM)];
                case 14:
                    result = _a.sent();
                    if (result.length === 2 && result[0].canonical === 'Phillip' && result[1].canonical === 'Muninn') {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: Fallback not working');
                        failed++;
                    }
                    return [3 /*break*/, 16];
                case 15:
                    err_4 = _a.sent();
                    console.log('   ❌ FAIL:', err_4);
                    failed++;
                    return [3 /*break*/, 16];
                case 16:
                    // Test 5: Alias store can find canonical forms
                    {
                        console.log('\n📝 Test: Alias store can find canonical forms');
                        try {
                            store = (0, normalize_js_1.createAliasStore)();
                            store.addAlias('Sammy Clemens', 'Sammy');
                            store.addAlias('Sammy Clemens', 'Sam');
                            found1 = store.findCanonical('Sammy');
                            found2 = store.findCanonical('sam');
                            aliases = store.getAliases('Sammy Clemens');
                            hasSammy = aliases.some(function (a) { return a.toLowerCase() === 'sammy'; });
                            hasSam = aliases.some(function (a) { return a.toLowerCase() === 'sam'; });
                            if (found1 === 'Sammy Clemens' && found2 === 'Sammy Clemens' && hasSammy && hasSam) {
                                console.log('   ✅ PASS');
                                passed++;
                            }
                            else {
                                console.log('   ❌ FAIL: Alias store not working correctly');
                                console.log('   found1:', found1, 'found2:', found2, 'aliases:', aliases);
                                failed++;
                            }
                        }
                        catch (err) {
                            console.log('   ❌ FAIL:', err);
                            failed++;
                        }
                    }
                    // Test 6: Alias store returns null for unknown aliases
                    {
                        console.log('\n📝 Test: Alias store returns null for unknown aliases');
                        try {
                            store = (0, normalize_js_1.createAliasStore)();
                            store.addAlias('Phillip', 'Phil');
                            found = store.findCanonical('Unknown');
                            if (found === null) {
                                console.log('   ✅ PASS');
                                passed++;
                            }
                            else {
                                console.log('   ❌ FAIL: Should have returned null');
                                failed++;
                            }
                        }
                        catch (err) {
                            console.log('   ❌ FAIL:', err);
                            failed++;
                        }
                    }
                    console.log('\n📝 Test: Rule-based abbreviation expansion (no LLM)');
                    _a.label = 17;
                case 17:
                    _a.trys.push([17, 19, , 20]);
                    text = "Working from NYC next week.";
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text)];
                case 18:
                    result = _a.sent();
                    nycEntity = result.find(function (e) { return e.original === 'NYC'; });
                    if (nycEntity && nycEntity.canonical === 'New York City') {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: Rule-based abbreviation not working');
                        failed++;
                    }
                    return [3 /*break*/, 20];
                case 19:
                    err_5 = _a.sent();
                    console.log('   ❌ FAIL:', err_5);
                    failed++;
                    return [3 /*break*/, 20];
                case 20:
                    console.log('\n📝 Test: Rule-based date normalization (no LLM)');
                    _a.label = 21;
                case 21:
                    _a.trys.push([21, 23, , 24]);
                    text = "Meeting scheduled for tomorrow.";
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text)];
                case 22:
                    result = _a.sent();
                    tomorrowEntity = result.find(function (e) { return e.original === 'tomorrow'; });
                    if (tomorrowEntity && tomorrowEntity.canonical === '2026-02-25') {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: Rule-based date not working');
                        console.log('   Got:', tomorrowEntity === null || tomorrowEntity === void 0 ? void 0 : tomorrowEntity.canonical);
                        failed++;
                    }
                    return [3 /*break*/, 24];
                case 23:
                    err_6 = _a.sent();
                    console.log('   ❌ FAIL:', err_6);
                    failed++;
                    return [3 /*break*/, 24];
                case 24:
                    console.log('\n📝 Test: Multiple abbreviation expansions');
                    _a.label = 25;
                case 25:
                    _a.trys.push([25, 27, , 28]);
                    text = "QLD and NSW are both in Australia.";
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text)];
                case 26:
                    result = _a.sent();
                    qld = result.find(function (e) { return e.original === 'QLD'; });
                    nsw = result.find(function (e) { return e.original === 'NSW'; });
                    if ((qld === null || qld === void 0 ? void 0 : qld.canonical) === 'Queensland' && (nsw === null || nsw === void 0 ? void 0 : nsw.canonical) === 'New South Wales') {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: Multiple abbreviations not working');
                        failed++;
                    }
                    return [3 /*break*/, 28];
                case 27:
                    err_7 = _a.sent();
                    console.log('   ❌ FAIL:', err_7);
                    failed++;
                    return [3 /*break*/, 28];
                case 28:
                    console.log('\n📝 Test: Normalizes UK spelling to canonical with US alias');
                    _a.label = 29;
                case 29:
                    _a.trys.push([29, 31, , 32]);
                    text = "The colour scheme needs work.";
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text)];
                case 30:
                    result = _a.sent();
                    colourEntity = result.find(function (e) { return e.original.toLowerCase() === 'colour'; });
                    if (colourEntity && colourEntity.aliases.includes('color') && colourEntity.aliases.includes('colour')) {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: Colour entity not normalized with color alias');
                        console.log('   Got:', colourEntity === null || colourEntity === void 0 ? void 0 : colourEntity.aliases);
                        failed++;
                    }
                    return [3 /*break*/, 32];
                case 31:
                    err_8 = _a.sent();
                    console.log('   ❌ FAIL:', err_8);
                    failed++;
                    return [3 /*break*/, 32];
                case 32:
                    console.log('\n📝 Test: Normalizes US spelling to canonical with UK alias');
                    _a.label = 33;
                case 33:
                    _a.trys.push([33, 35, , 36]);
                    text = "We need to organize the files.";
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text)];
                case 34:
                    result = _a.sent();
                    organizeEntity = result.find(function (e) { return e.original.toLowerCase() === 'organize'; });
                    if (organizeEntity && organizeEntity.aliases.includes('organise') && organizeEntity.aliases.includes('organize')) {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: Organize entity not normalized with organise alias');
                        console.log('   Got:', organizeEntity === null || organizeEntity === void 0 ? void 0 : organizeEntity.aliases);
                        failed++;
                    }
                    return [3 /*break*/, 36];
                case 35:
                    err_9 = _a.sent();
                    console.log('   ❌ FAIL:', err_9);
                    failed++;
                    return [3 /*break*/, 36];
                case 36:
                    console.log('\n📝 Test: Retrieval matches both spellings via alias store');
                    _a.label = 37;
                case 37:
                    _a.trys.push([37, 39, , 40]);
                    store_1 = (0, normalize_js_1.createAliasStore)();
                    text = "The behaviour was unusual.";
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text)];
                case 38:
                    result = _a.sent();
                    // Add to alias store
                    result.forEach(function (e) {
                        e.aliases.forEach(function (a) { return store_1.addAlias(e.canonical, a); });
                    });
                    foundUS = store_1.findCanonical('behavior');
                    foundUK = store_1.findCanonical('behaviour');
                    if (foundUS === 'behaviour' && foundUK === 'behaviour') {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: Alias store not finding canonical');
                        console.log('   foundUS:', foundUS, 'foundUK:', foundUK);
                        failed++;
                    }
                    return [3 /*break*/, 40];
                case 39:
                    err_10 = _a.sent();
                    console.log('   ❌ FAIL:', err_10);
                    failed++;
                    return [3 /*break*/, 40];
                case 40:
                    console.log('\n📝 Test: Multiple spelling variants in same text');
                    _a.label = 41;
                case 41:
                    _a.trys.push([41, 43, , 44]);
                    text = "The colour was marvelous but the centre needs more analyse.";
                    return [4 /*yield*/, (0, normalize_js_1.normalizeEntities)(text)];
                case 42:
                    result = _a.sent();
                    colour = result.find(function (e) { return e.original.toLowerCase() === 'colour'; });
                    centre = result.find(function (e) { return e.original.toLowerCase() === 'centre'; });
                    analyse = result.find(function (e) { return e.original.toLowerCase() === 'analyse'; });
                    if ((colour === null || colour === void 0 ? void 0 : colour.aliases.includes('color')) && (centre === null || centre === void 0 ? void 0 : centre.aliases.includes('center')) && (analyse === null || analyse === void 0 ? void 0 : analyse.aliases.includes('analyze'))) {
                        console.log('   ✅ PASS');
                        passed++;
                    }
                    else {
                        console.log('   ❌ FAIL: Multiple variants not all captured');
                        console.log('   colour:', colour === null || colour === void 0 ? void 0 : colour.aliases);
                        console.log('   centre:', centre === null || centre === void 0 ? void 0 : centre.aliases);
                        console.log('   analyse:', analyse === null || analyse === void 0 ? void 0 : analyse.aliases);
                        failed++;
                    }
                    return [3 /*break*/, 44];
                case 43:
                    err_11 = _a.sent();
                    console.log('   ❌ FAIL:', err_11);
                    failed++;
                    return [3 /*break*/, 44];
                case 44:
                    console.log('\n' + '='.repeat(60));
                    console.log("\n\uD83D\uDCCA Results: ".concat(passed, "/").concat(passed + failed, " passed (").concat(Math.round(passed / (passed + failed) * 100), "%)"));
                    return [2 /*return*/, { passed: passed, failed: failed }];
            }
        });
    });
}
// Run tests
runNormalizationTests()
    .then(function (_a) {
    var passed = _a.passed, failed = _a.failed;
    process.exit(failed > 0 ? 1 : 0);
})
    .catch(function (err) {
    console.error('Test error:', err);
    process.exit(1);
});
