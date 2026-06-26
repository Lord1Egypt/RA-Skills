"use strict";
/**
 * Entity Normalization
 *
 * Resolves entity mentions to canonical forms:
 * - Pronouns → Names (when resolvable)
 * - Abbreviations → Full names
 * - Dates → ISO 8601
 * - Aliases stored for retrieval
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
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.normalizeEntities = normalizeEntities;
exports.createAliasStore = createAliasStore;
exports.extractWithNormalization = extractWithNormalization;
// Current date for date calculations
var CURRENT_DATE = new Date('2026-02-24');
/**
 * English spelling variants (UK/Aus ↔ US)
 * Both forms should map to the same concept for retrieval
 */
var SPELLING_VARIANTS = {
    // -our ↔ -or
    'colour': ['color'],
    'flavour': ['flavor'],
    'honour': ['honor'],
    'humour': ['humor'],
    'labour': ['labor'],
    'neighbour': ['neighbor'],
    'rumour': ['rumor'],
    'savour': ['savor'],
    'valour': ['valor'],
    'vigour': ['vigor'],
    'ardour': ['ardor'],
    'clamour': ['clamor'],
    'dolour': ['dolor'],
    'enamour': ['enamor'],
    'fervour': ['fervor'],
    'glamour': ['glamor'],
    'odour': ['odor'],
    'parlour': ['parlor'],
    'splendour': ['splendor'],
    'tumour': ['tumor'],
    'vapour': ['vapor'],
    // -ise ↔ -ize
    'organise': ['organize'],
    'realise': ['realize'],
    'recognise': ['recognize'],
    'analyse': ['analyze'],
    'paralyse': ['paralyze'],
    'apologise': ['apologize'],
    'authorise': ['authorize'],
    'capitalise': ['capitalize'],
    'categorise': ['categorize'],
    'centralise': ['centralize'],
    'characterise': ['characterize'],
    'civilise': ['civilize'],
    'commercialise': ['commercialize'],
    'criticise': ['criticize'],
    'customise': ['customize'],
    'emphasise': ['emphasize'],
    'familiarise': ['familiarize'],
    'finalise': ['finalize'],
    'formalise': ['formalize'],
    'harmonise': ['harmonize'],
    'hypothesise': ['hypothesize'],
    'idealise': ['idealize'],
    'industrialise': ['industrialize'],
    'initialise': ['initialize'],
    'maximise': ['maximize'],
    'minimise': ['minimize'],
    'modernise': ['modernize'],
    'normalise': ['normalize'],
    'optimise': ['optimize'],
    'popularise': ['popularize'],
    'prioritise': ['prioritize'],
    'publicise': ['publicize'],
    'rationalise': ['rationalize'],
    'revolutionise': ['revolutionize'],
    'satirise': ['satirize'],
    'specialise': ['specialize'],
    'standardise': ['standardize'],
    'symbolise': ['symbolize'],
    'sympathise': ['sympathize'],
    'synchronise': ['synchronize'],
    'systematise': ['systematize'],
    'theorise': ['theorize'],
    'utilise': ['utilize'],
    'visualise': ['visualize'],
    // -re ↔ -er
    'centre': ['center'],
    'theatre': ['theater'],
    'fibre': ['fiber'],
    'litre': ['liter'],
    'metre': ['meter'],
    'sabre': ['saber'],
    'spectre': ['specter'],
    'lustre': ['luster'],
    'meagre': ['meager'],
    'sombre': ['somber'],
    // -ce ↔ -se
    'defence': ['defense'],
    'offence': ['offense'],
    'pretence': ['pretense'],
    'licence': ['license'],
    'practise': ['practice'],
    // -ogue ↔ -og
    'catalogue': ['catalog'],
    'dialogue': ['dialog'],
    'monologue': ['monolog'],
    'prologue': ['prolog'],
    'epilogue': ['epilog'],
    'analogue': ['analog'],
    // Double consonants
    'cancelled': ['canceled'],
    'cancellation': ['cancelation'],
    'counsellor': ['counselor'],
    'jewellery': ['jewelry'],
    'travelling': ['traveling'],
    'traveller': ['traveler'],
    'marvellous': ['marvelous'],
    'woollen': ['woolen'],
    'waggon': ['wagon'],
    // Miscellaneous
    'cheque': ['check'],
    'programme': ['program'],
    'tyre': ['tire'],
    'aluminium': ['aluminum'],
    'aeroplane': ['airplane'],
    'storey': ['story'],
    'moustache': ['mustache'],
    'plough': ['plow'],
    'sceptre': ['scepter'],
    'behaviour': ['behavior'],
    'behavioural': ['behavioral'],
    'behaviourism': ['behaviorism'],
};
/**
 * Get all spelling variants for a word (both directions)
 */
function getSpellingVariants(word) {
    var lower = word.toLowerCase();
    // Check if word is a key
    if (SPELLING_VARIANTS[lower]) {
        return __spreadArray([lower], SPELLING_VARIANTS[lower], true);
    }
    // Check if word is a variant
    for (var _i = 0, _a = Object.entries(SPELLING_VARIANTS); _i < _a.length; _i++) {
        var _b = _a[_i], canonical = _b[0], variants = _b[1];
        if (variants.includes(lower)) {
            return __spreadArray([canonical], variants, true);
        }
    }
    return [lower]; // No variants found
}
/**
 * Calculate ISO date from relative date string
 */
function normalizeRelativeDate(dateStr) {
    var lower = dateStr.toLowerCase().trim();
    var today = new Date(CURRENT_DATE);
    switch (lower) {
        case 'today':
            return formatDate(today);
        case 'yesterday':
            return formatDate(new Date(today.getTime() - 24 * 60 * 60 * 1000));
        case 'tomorrow':
            return formatDate(new Date(today.getTime() + 24 * 60 * 60 * 1000));
        case 'day after tomorrow':
            return formatDate(new Date(today.getTime() + 2 * 24 * 60 * 60 * 1000));
        case 'day before yesterday':
        case 'day before':
            return formatDate(new Date(today.getTime() - 2 * 24 * 60 * 60 * 1000));
        default:
            // Try to parse "next Monday", "last Friday", etc.
            var dayMatch = lower.match(/(next|last|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)/);
            if (dayMatch) {
                var modifier = dayMatch[1], dayName = dayMatch[2];
                var dayIndex = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'].indexOf(dayName);
                var currentDay = today.getDay();
                var targetDay = dayIndex;
                if (modifier === 'next') {
                    targetDay = currentDay <= dayIndex ? dayIndex : dayIndex + 7;
                }
                else if (modifier === 'last') {
                    targetDay = currentDay >= dayIndex ? dayIndex : dayIndex - 7;
                }
                var diff = targetDay - currentDay;
                return formatDate(new Date(today.getTime() + diff * 24 * 60 * 60 * 1000));
            }
            // Return as-is if can't parse
            return dateStr;
    }
}
function formatDate(date) {
    return date.toISOString().split('T')[0];
}
/**
 * Common abbreviation expansions
 */
var ABBREVIATION_MAP = {
    // US Cities
    'NYC': 'New York City',
    'LA': 'Los Angeles',
    'SF': 'San Francisco',
    'DC': 'Washington DC',
    'Chi': 'Chicago',
    'Philly': 'Philadelphia',
    // Australian
    'QLD': 'Queensland',
    'NSW': 'New South Wales',
    'VIC': 'Victoria',
    'WA': 'Western Australia',
    'SA': 'South Australia',
    'TAS': 'Tasmania',
    'ACT': 'Australian Capital Territory',
    'NT': 'Northern Territory',
    // General
    'USA': 'United States',
    'UK': 'United Kingdom',
    'EU': 'European Union',
    'UN': 'United Nations',
    'NATO': 'North Atlantic Treaty Organization',
    'AI': 'Artificial Intelligence',
    'ML': 'Machine Learning',
    'DL': 'Deep Learning',
    'NLP': 'Natural Language Processing',
    'API': 'Application Programming Interface',
    'URL': 'Uniform Resource Locator',
    'HTTP': 'HyperText Transfer Protocol',
    'HTTPS': 'HyperText Transfer Protocol Secure',
    'SQL': 'Structured Query Language',
    'NoSQL': 'Non-Relational Database',
    'CTO': 'Chief Technology Officer',
    'CFO': 'Chief Financial Officer',
    'COO': 'Chief Operating Officer',
    'PM': 'Project Manager',
    'DevOps': 'Development Operations',
};
/**
 * Pronoun resolution patterns
 * Maps pronouns to potential antecedents found in text
 */
var PRONOUN_PATTERNS = [
    { pronoun: 'he', pattern: /([A-Z][a-z]+)\s+(?:worked|built|created|designed|developed|wrote|said|mentioned|told|asked)/gi },
    { pronoun: 'she', pattern: /([A-Z][a-z]+)\s+(?:worked|built|created|designed|developed|wrote|said|mentioned|told|asked)/gi },
    { pronoun: 'they', pattern: /([A-Z][a-z]+)\s+(?:worked|built|created|designed|developed)/gi },
    { pronoun: 'it', pattern: /([A-Z][a-z]+)\s+(?:is|was|was built|was created)/gi },
];
/**
 * Find potential antecedent for a pronoun in text
 */
function findPronounAntecedent(text, pronoun) {
    var lowerPronoun = pronoun.toLowerCase();
    for (var _i = 0, PRONOUN_PATTERNS_1 = PRONOUN_PATTERNS; _i < PRONOUN_PATTERNS_1.length; _i++) {
        var _a = PRONOUN_PATTERNS_1[_i], p = _a.pronoun, pattern = _a.pattern;
        if (p === lowerPronoun) {
            var matches = text.matchAll(pattern);
            for (var _b = 0, matches_1 = matches; _b < matches_1.length; _b++) {
                var match = matches_1[_b];
                if (match[1]) {
                    return match[1];
                }
            }
        }
    }
    return null;
}
/**
 * Normalize entities using LLM (optional) or rule-based fallback
 *
 * @param text - Input text
 * @param existingEntities - Pre-extracted entities (optional)
 * @param llmProvider - Optional LLM function for advanced normalization
 * @returns Normalized entities with aliases
 */
function normalizeEntities(text, existingEntities, llmProvider) {
    return __awaiter(this, void 0, void 0, function () {
        var ruleBased, prompt_1, response, llmNormalized, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    ruleBased = normalizeEntitiesRuleBased(text, existingEntities || []);
                    // If no LLM provider, return rule-based results
                    if (!llmProvider) {
                        return [2 /*return*/, ruleBased];
                    }
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    prompt_1 = buildNormalizationPrompt(text, existingEntities);
                    return [4 /*yield*/, llmProvider(prompt_1)];
                case 2:
                    response = _a.sent();
                    llmNormalized = parseLLMResponse(response);
                    // Merge LLM results with rule-based (LLM takes precedence)
                    return [2 /*return*/, mergeNormalizationResults(ruleBased, llmNormalized)];
                case 3:
                    error_1 = _a.sent();
                    console.warn('Entity normalization failed, using rule-based fallback:', error_1);
                    return [2 /*return*/, ruleBased];
                case 4: return [2 /*return*/];
            }
        });
    });
}
/**
 * Rule-based entity normalization (always available)
 */
function normalizeEntitiesRuleBased(text, existingEntities) {
    var results = [];
    var processed = new Set();
    // 1. Process existing entities
    for (var _i = 0, existingEntities_1 = existingEntities; _i < existingEntities_1.length; _i++) {
        var entity = existingEntities_1[_i];
        var normalized = normalizeSingleEntity(entity, text);
        results.push(normalized);
        processed.add(entity.text.toLowerCase());
    }
    // 2. Look for abbreviations in text
    for (var _a = 0, _b = Object.entries(ABBREVIATION_MAP); _a < _b.length; _a++) {
        var _c = _b[_a], abbr = _c[0], expansion = _c[1];
        var regex = new RegExp("\\b".concat(abbr, "\\b"), 'g');
        if (regex.test(text) && !processed.has(abbr.toLowerCase())) {
            results.push({
                original: abbr,
                canonical: expansion,
                type: determineAbbreviationType(abbr),
                confidence: 0.9,
                aliases: [abbr, expansion],
                context: ''
            });
            processed.add(abbr.toLowerCase());
        }
    }
    // 3. Look for relative dates in text
    var datePatterns = [
        /\b(today|yesterday|tomorrow|day after tomorrow)\b/gi,
        /\b(next|last|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b/gi,
    ];
    for (var _d = 0, datePatterns_1 = datePatterns; _d < datePatterns_1.length; _d++) {
        var pattern = datePatterns_1[_d];
        var matches = text.match(pattern);
        if (matches) {
            for (var _e = 0, matches_2 = matches; _e < matches_2.length; _e++) {
                var match = matches_2[_e];
                if (!processed.has(match.toLowerCase())) {
                    var normalizedDate = normalizeRelativeDate(match);
                    results.push({
                        original: match,
                        canonical: normalizedDate,
                        type: 'event',
                        confidence: 0.85,
                        aliases: [match, normalizedDate],
                        context: ''
                    });
                    processed.add(match.toLowerCase());
                }
            }
        }
    }
    // 4. Check for spelling variants
    for (var _f = 0, _g = Object.entries(SPELLING_VARIANTS); _f < _g.length; _f++) {
        var _h = _g[_f], canonical = _h[0], variants = _h[1];
        // Check if canonical (UK/Aus) form appears in text
        var canonicalRegex = new RegExp("\\b".concat(canonical, "\\b"), 'gi');
        if (canonicalRegex.test(text) && !processed.has(canonical.toLowerCase())) {
            results.push({
                original: canonical,
                canonical: canonical, // Use UK/Aus as canonical
                type: 'concept',
                confidence: 0.95,
                aliases: __spreadArray([canonical], variants, true),
                context: ''
            });
            processed.add(canonical.toLowerCase());
            variants.forEach(function (v) { return processed.add(v.toLowerCase()); });
        }
        var _loop_1 = function (variant) {
            var variantRegex = new RegExp("\\b".concat(variant, "\\b"), 'gi');
            if (variantRegex.test(text) && !processed.has(variant.toLowerCase())) {
                results.push({
                    original: variant,
                    canonical: canonical, // Map to canonical UK/Aus form
                    type: 'concept',
                    confidence: 0.95,
                    aliases: __spreadArray([variant, canonical], variants.filter(function (v) { return v !== variant; }), true),
                    context: ''
                });
                processed.add(variant.toLowerCase());
                processed.add(canonical.toLowerCase());
                variants.forEach(function (v) { return processed.add(v.toLowerCase()); });
            }
        };
        // Check if any variant (US) form appears in text
        for (var _j = 0, variants_1 = variants; _j < variants_1.length; _j++) {
            var variant = variants_1[_j];
            _loop_1(variant);
        }
    }
    return results;
}
/**
 * Normalize a single entity
 */
function normalizeSingleEntity(entity, text) {
    // Check if entity text is an abbreviation
    var abbrExpansion = ABBREVIATION_MAP[entity.text];
    if (abbrExpansion) {
        return __assign(__assign({}, entity), { original: entity.text, canonical: abbrExpansion, aliases: [entity.text, abbrExpansion] });
    }
    // Check if entity text is a pronoun that can be resolved
    var pronouns = ['he', 'she', 'they', 'it', 'him', 'her', 'them'];
    if (pronouns.includes(entity.text.toLowerCase())) {
        var antecedent = findPronounAntecedent(text, entity.text);
        if (antecedent) {
            return __assign(__assign({}, entity), { original: entity.text, canonical: antecedent, aliases: [entity.text, antecedent] });
        }
    }
    // Check if entity text contains a date reference
    var dateMatch = entity.text.match(/\b(today|yesterday|tomorrow)\b/i);
    if (dateMatch) {
        return __assign(__assign({}, entity), { original: entity.text, canonical: normalizeRelativeDate(entity.text), aliases: [entity.text, normalizeRelativeDate(entity.text)] });
    }
    // Default: keep as-is
    return __assign(__assign({}, entity), { original: entity.text, canonical: entity.text, aliases: [entity.text] });
}
/**
 * Determine type for abbreviation
 */
function determineAbbreviationType(abbr) {
    var locationAbbreviations = ['NYC', 'LA', 'SF', 'DC', 'Chi', 'Philly', 'QLD', 'NSW', 'VIC', 'WA', 'SA', 'TAS', 'ACT', 'NT'];
    var orgAbbreviations = ['USA', 'UK', 'EU', 'UN', 'NATO'];
    var techAbbreviations = ['AI', 'ML', 'DL', 'NLP', 'API', 'URL', 'HTTP', 'HTTPS', 'SQL', 'NoSQL'];
    if (locationAbbreviations.includes(abbr))
        return 'location';
    if (orgAbbreviations.includes(abbr))
        return 'organization';
    if (techAbbreviations.includes(abbr))
        return 'technology';
    return 'concept';
}
/**
 * Build LLM prompt for normalization
 */
function buildNormalizationPrompt(text, entities) {
    var entityList = (entities === null || entities === void 0 ? void 0 : entities.map(function (e) { return "- ".concat(e.text, " (").concat(e.type, ")"); }).join('\n')) || 'None pre-extracted';
    return "Analyze the following text and normalize all entity mentions.\n\nText: \"".concat(text, "\"\n\nPre-extracted entities:\n").concat(entityList, "\n\nNormalization rules:\n1. PRONOUNS: Resolve to canonical names when context is clear\n   - \"Phillip worked on Muninn. He built...\" \u2192 \"He\" = \"Phillip\"\n   - If pronoun reference is unclear, leave as-is\n   \n2. ABBREVIATIONS: Expand to full names\n   - \"NYC\" \u2192 \"New York City\"\n   - \"SF\" \u2192 \"San Francisco\"\n   - \"QLD\" \u2192 \"Queensland\"\n   \n3. DATES: Normalize to ISO 8601 (YYYY-MM-DD)\n   - \"tomorrow\" \u2192 2026-02-25\n   - \"yesterday\" \u2192 2026-02-23\n   - \"next week\" \u2192 calculate date range\n   \n4. NAME VARIANTS: Link aliases\n   - \"Sammy Clemens\" and \"Sammy\" \u2192 same canonical \"Sammy Clemens\"\n\nReturn JSON array of normalized entities:\n[\n  {\n    \"original\": \"He\",\n    \"canonical\": \"Phillip\",\n    \"type\": \"person\",\n    \"confidence\": 0.9\n  }\n]\n\nOnly include entities that CAN be normalized. Skip entities that are already in canonical form.");
}
/**
 * Parse LLM response into NormalizedEntity array
 */
function parseLLMResponse(response) {
    try {
        var jsonMatch = response.match(/\[[\s\S]*\]/);
        if (!jsonMatch)
            return [];
        var parsed = JSON.parse(jsonMatch[0]);
        return parsed.map(function (e) { return ({
            original: e.original,
            canonical: e.canonical,
            type: e.type || 'concept',
            confidence: e.confidence || 0.8,
            aliases: [e.original, e.canonical],
            context: ''
        }); });
    }
    catch (error) {
        console.warn('Failed to parse normalization response:', error);
        return [];
    }
}
/**
 * Merge rule-based and LLM normalization results
 */
function mergeNormalizationResults(ruleBased, llmResults) {
    var _a;
    var merged = new Map();
    // Add rule-based results first
    for (var _i = 0, ruleBased_1 = ruleBased; _i < ruleBased_1.length; _i++) {
        var entity = ruleBased_1[_i];
        merged.set(entity.original.toLowerCase(), entity);
    }
    // LLM results override rule-based (more accurate)
    for (var _b = 0, llmResults_1 = llmResults; _b < llmResults_1.length; _b++) {
        var entity = llmResults_1[_b];
        var key = entity.original.toLowerCase();
        if (entity.confidence > (((_a = merged.get(key)) === null || _a === void 0 ? void 0 : _a.confidence) || 0)) {
            merged.set(key, entity);
        }
    }
    return Array.from(merged.values());
}
function createAliasStore() {
    var aliases = new Map();
    var canonicals = new Map(); // Store original case
    return {
        getAliases: function (canonical) {
            return __spreadArray([], (aliases.get(canonical.toLowerCase()) || new Set()), true);
        },
        addAlias: function (canonical, alias) {
            var key = canonical.toLowerCase();
            if (!aliases.has(key)) {
                aliases.set(key, new Set([canonical]));
                canonicals.set(key, canonical); // Store original case
            }
            // Store lowercase for case-insensitive lookup
            aliases.get(key).add(alias.toLowerCase());
        },
        findCanonical: function (alias) {
            var aliasLower = alias.toLowerCase();
            for (var _i = 0, aliases_1 = aliases; _i < aliases_1.length; _i++) {
                var _a = aliases_1[_i], canonical = _a[0], aliasSet = _a[1];
                if (aliasSet.has(aliasLower)) {
                    return canonicals.get(canonical) || canonical; // Return with original case
                }
            }
            return null;
        }
    };
}
/**
 * Extract with normalization (combined function)
 */
function extractWithNormalization(text, existingEntities, llmProvider) {
    return __awaiter(this, void 0, void 0, function () {
        var extractEntities, entities, normalized;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return require('./entities.js'); })];
                case 1:
                    extractEntities = (_a.sent()).extractEntities;
                    entities = extractEntities(text);
                    return [4 /*yield*/, normalizeEntities(text, entities, llmProvider)];
                case 2:
                    normalized = _a.sent();
                    return [2 /*return*/, { entities: entities, normalized: normalized }];
            }
        });
    });
}
