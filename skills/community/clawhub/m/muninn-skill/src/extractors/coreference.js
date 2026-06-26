"use strict";
/**
 * Coreference Resolution for Muninn Memory System
 *
 * Resolves pronouns, aliases, and references to canonical entity names
 * BEFORE memory storage to prevent entity fragmentation.
 *
 * This fixes the LOCOMO benchmark gap where "Phillip", "him", and
 * "the Program Manager" were seen as 3 different entities.
 *
 * Uses LLM-based entity linking via local Ollama.
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
exports.initEntityCache = initEntityCache;
exports.addToEntityCache = addToEntityCache;
exports.resolveEntity = resolveEntity;
exports.clearEntityCache = clearEntityCache;
exports.resolveCoreferences = resolveCoreferences;
exports.resolveCoreferencesSimple = resolveCoreferencesSimple;
exports.preprocessForMemory = preprocessForMemory;
exports.preprocessForMemorySimple = preprocessForMemorySimple;
var entities_js_1 = require("./entities.js");
// Pronoun patterns to resolve
var PRONOUN_PATTERNS = /\b(he|she|him|her|his|hers|they|them|their|theirs|it|its|this|that|these|those)\b/gi;
// Possessive determiners
var POSSESSIVE_PATTERNS = /\b(my|your|his|her|its|our|their)\b/gi;
// ============================================
// ENTITY CACHE (from memory store)
// ============================================
var entityCache = new Map();
/**
 * Initialize entity cache from memory store
 * Should be called when memory system starts
 */
function initEntityCache(store) {
    return __awaiter(this, void 0, void 0, function () {
        var kgEntities, _i, kgEntities_1, ent, aliases;
        return __generator(this, function (_a) {
            try {
                kgEntities = store.getEntityStore().getAll();
                for (_i = 0, kgEntities_1 = kgEntities; _i < kgEntities_1.length; _i++) {
                    ent = kgEntities_1[_i];
                    aliases = __spreadArray([
                        ent.name
                    ], ent.aliases, true);
                    entityCache.set(ent.name.toLowerCase(), {
                        canonical: ent.name,
                        aliases: aliases,
                        type: ent.type
                    });
                }
                console.log("\uD83D\uDCC7 Coreference: Initialized with ".concat(entityCache.size, " known entities"));
            }
            catch (error) {
                console.warn('Coreference: Failed to initialize entity cache:', error);
            }
            return [2 /*return*/];
        });
    });
}
/**
 * Add a new entity to the cache
 */
function addToEntityCache(canonical, aliases, type) {
    var existing = entityCache.get(canonical.toLowerCase());
    if (existing) {
        // Merge aliases
        var mergedAliases = __spreadArray([], new Set(__spreadArray(__spreadArray([], existing.aliases, true), aliases, true)), true);
        entityCache.set(canonical.toLowerCase(), {
            canonical: canonical,
            aliases: mergedAliases,
            type: type
        });
    }
    else {
        entityCache.set(canonical.toLowerCase(), {
            canonical: canonical,
            aliases: __spreadArray(__spreadArray([], aliases, true), [canonical], false),
            type: type
        });
    }
}
/**
 * Get canonical name for a pronoun or alias
 */
function resolveEntity(mention) {
    var lower = mention.toLowerCase();
    // Check if it's a known alias
    for (var _i = 0, entityCache_1 = entityCache; _i < entityCache_1.length; _i++) {
        var _a = entityCache_1[_i], _ = _a[0], entity = _a[1];
        if (entity.aliases.some(function (a) { return a.toLowerCase() === lower; })) {
            return entity.canonical;
        }
    }
    // Check if it's the canonical name itself
    if (entityCache.has(lower)) {
        return entityCache.get(lower).canonical;
    }
    return null;
}
/**
 * Clear entity cache (for testing)
 */
function clearEntityCache() {
    entityCache.clear();
}
// ============================================
// LLM-BASED COREFERENCE RESOLUTION
// ============================================
/**
 * Call Ollama for coreference resolution
 * Uses a focused prompt to rewrite text with resolved entities
 *
 * Example:
 * Raw: "Met with Caroline regarding the BHP MSP. She is worried about the rollout. It needs to be delayed."
 * Resolved: "Met with Caroline regarding the BHP MSP. Caroline is worried about the BHP MSP rollout. The BHP MSP rollout needs to be delayed."
 */
function resolveWithLLM(text, knownEntities, entityAliases) {
    return __awaiter(this, void 0, void 0, function () {
        var entityContext, entries, _i, entityAliases_1, _a, canonical, aliases, prompt, response, data, resolvedText, entityMap, error_1;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    entityContext = '';
                    if (entityAliases && entityAliases.size > 0) {
                        entries = [];
                        for (_i = 0, entityAliases_1 = entityAliases; _i < entityAliases_1.length; _i++) {
                            _a = entityAliases_1[_i], canonical = _a[0], aliases = _a[1];
                            entries.push("".concat(canonical, " (aliases: ").concat(aliases.join(', '), ")"));
                        }
                        entityContext = "\n\nKnown entities with aliases:\n".concat(entries.join('\n'));
                    }
                    else if (knownEntities.length > 0) {
                        entityContext = "\n\nKnown entities: ".concat(knownEntities.join(', '));
                    }
                    prompt = "You are a Coreference Resolution Engine. Rewrite the provided user note by replacing all pronouns (he, she, they, it, his, her, their, the project, the client) with the specific entities they refer to based on the immediate context.\n\nRules:\n1. Maintain the original tone and substance\n2. Replace pronouns with the actual entity name\n3. Replace vague references (the project, the client, the program) with specific names\n4. If an entity is ambiguous, keep the pronoun but append the most likely identity in brackets\n5. Do NOT change any other words\n".concat(entityContext, "\n\nInput: \"").concat(text, "\"\n\nOutput the rewritten text with coreferences resolved. Output ONLY the resolved text, nothing else:");
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 4, , 5]);
                    return [4 /*yield*/, fetch('http://localhost:11434/api/generate', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                model: 'qwen2.5:1.5b',
                                prompt: prompt,
                                stream: false,
                                options: {
                                    temperature: 0.1,
                                    num_predict: 512
                                }
                            })
                        })];
                case 2:
                    response = _b.sent();
                    if (!response.ok) {
                        throw new Error("Ollama request failed: ".concat(response.statusText));
                    }
                    return [4 /*yield*/, response.json()];
                case 3:
                    data = _b.sent();
                    resolvedText = (data.response || data.thinking || '').trim();
                    entityMap = extractEntityMap(text, resolvedText);
                    return [2 /*return*/, { resolvedText: resolvedText, entityMap: entityMap }];
                case 4:
                    error_1 = _b.sent();
                    console.warn('Coreference LLM resolution failed:', error_1);
                    return [2 /*return*/, { resolvedText: text, entityMap: new Map() }];
                case 5: return [2 /*return*/];
            }
        });
    });
}
/**
 * Extract entity mappings by comparing original and resolved text
 */
function extractEntityMap(original, resolved) {
    var map = new Map();
    // Find pronouns in original
    var pronouns = original.match(PRONOUN_PATTERNS) || [];
    // Look for entity names in brackets in resolved text
    var bracketPattern = /\[([^\]]+)\]/g;
    var match;
    while ((match = bracketPattern.exec(resolved)) !== null) {
        // Find corresponding pronoun (approximate)
        var entityName = match[1];
        for (var _i = 0, pronouns_1 = pronouns; _i < pronouns_1.length; _i++) {
            var pronoun = pronouns_1[_i];
            if (!map.has(pronoun.toLowerCase())) {
                map.set(pronoun.toLowerCase(), entityName);
                break;
            }
        }
    }
    return map;
}
// ============================================
// MAIN COREFERENCE RESOLUTION
// ============================================
/**
 * Resolve coreferences in text
 *
 * @param text - Raw input text
 * @param knownEntities - Optional list of known entities (from memory store)
 * @param useLLM - Whether to use LLM for resolution (default: true)
 * @returns CoreferenceResult with resolved text and entity mappings
 */
function resolveCoreferences(text_1, knownEntities_1) {
    return __awaiter(this, arguments, void 0, function (text, knownEntities, useLLM) {
        var originalText, entityMap, newEntitiesFound, extractedEntities, currentEntities, allEntities, _i, entityCache_2, _a, _, entity, _b, knownEntities_2, e, resolvedText, entityAliases, _c, entityCache_3, _d, _, entity, llmResult, _e, _f, _g, pronoun, canonical, definitePattern, match, phrase, resolved, sortedMappings, _h, sortedMappings_1, _j, mention, canonical, regex, _k, currentEntities_1, entity;
        if (useLLM === void 0) { useLLM = true; }
        return __generator(this, function (_l) {
            switch (_l.label) {
                case 0:
                    originalText = text;
                    entityMap = new Map();
                    newEntitiesFound = [];
                    extractedEntities = (0, entities_js_1.extractEntities)(text);
                    currentEntities = extractedEntities
                        .filter(function (e) { return e.type === 'person'; })
                        .map(function (e) { return e.text; });
                    allEntities = __spreadArray([], currentEntities, true);
                    // Add entities from cache
                    for (_i = 0, entityCache_2 = entityCache; _i < entityCache_2.length; _i++) {
                        _a = entityCache_2[_i], _ = _a[0], entity = _a[1];
                        if (!allEntities.includes(entity.canonical)) {
                            allEntities.push(entity.canonical);
                        }
                    }
                    // Add provided known entities
                    if (knownEntities) {
                        for (_b = 0, knownEntities_2 = knownEntities; _b < knownEntities_2.length; _b++) {
                            e = knownEntities_2[_b];
                            if (!allEntities.includes(e)) {
                                allEntities.push(e);
                            }
                        }
                    }
                    resolvedText = text;
                    if (!(useLLM && allEntities.length > 0)) return [3 /*break*/, 2];
                    entityAliases = new Map();
                    for (_c = 0, entityCache_3 = entityCache; _c < entityCache_3.length; _c++) {
                        _d = entityCache_3[_c], _ = _d[0], entity = _d[1];
                        entityAliases.set(entity.canonical, entity.aliases);
                    }
                    return [4 /*yield*/, resolveWithLLM(text, allEntities, entityAliases)];
                case 1:
                    llmResult = _l.sent();
                    resolvedText = llmResult.resolvedText;
                    // Merge LLM entity map
                    for (_e = 0, _f = llmResult.entityMap; _e < _f.length; _e++) {
                        _g = _f[_e], pronoun = _g[0], canonical = _g[1];
                        entityMap.set(pronoun.toLowerCase(), canonical);
                    }
                    _l.label = 2;
                case 2:
                    definitePattern = /the\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)/g;
                    while ((match = definitePattern.exec(text)) !== null) {
                        phrase = match[1];
                        resolved = resolveEntity(phrase);
                        if (resolved) {
                            entityMap.set(phrase.toLowerCase(), resolved);
                        }
                    }
                    sortedMappings = __spreadArray([], entityMap.entries(), true).sort(function (a, b) { return b[0].length - a[0].length; });
                    for (_h = 0, sortedMappings_1 = sortedMappings; _h < sortedMappings_1.length; _h++) {
                        _j = sortedMappings_1[_h], mention = _j[0], canonical = _j[1];
                        regex = new RegExp("\\b".concat(mention, "\\b"), 'gi');
                        resolvedText = resolvedText.replace(regex, "[".concat(canonical, "]"));
                    }
                    // Step 6: Add any new entities found to cache
                    for (_k = 0, currentEntities_1 = currentEntities; _k < currentEntities_1.length; _k++) {
                        entity = currentEntities_1[_k];
                        if (!entityCache.has(entity.toLowerCase())) {
                            newEntitiesFound.push(entity);
                            addToEntityCache(entity, [], 'person');
                        }
                    }
                    return [2 /*return*/, {
                            originalText: originalText,
                            resolvedText: resolvedText,
                            entityMap: entityMap,
                            newEntitiesFound: newEntitiesFound
                        }];
            }
        });
    });
}
/**
 * Simple coreference resolution without LLM
 * Uses pattern matching and entity cache only
 */
function resolveCoreferencesSimple(text, knownEntities) {
    var originalText = text;
    var entityMap = new Map();
    var newEntitiesFound = [];
    // Extract entities from text
    var extractedEntities = (0, entities_js_1.extractEntities)(text);
    // Add extracted entities to cache if new
    for (var _i = 0, extractedEntities_1 = extractedEntities; _i < extractedEntities_1.length; _i++) {
        var entity = extractedEntities_1[_i];
        if (entity.type === 'person' && !entityCache.has(entity.text.toLowerCase())) {
            newEntitiesFound.push(entity.text);
            addToEntityCache(entity.text, [], entity.type);
        }
    }
    // Add known entities to cache
    if (knownEntities) {
        for (var _a = 0, knownEntities_1 = knownEntities; _a < knownEntities_1.length; _a++) {
            var e = knownEntities_1[_a];
            if (!entityCache.has(e.toLowerCase())) {
                addToEntityCache(e, [], 'unknown');
            }
        }
    }
    // Resolve pronouns using cache
    var pronouns = text.match(PRONOUN_PATTERNS) || [];
    for (var _b = 0, pronouns_2 = pronouns; _b < pronouns_2.length; _b++) {
        var pronoun = pronouns_2[_b];
        var resolved = resolveEntity(pronoun);
        if (resolved) {
            entityMap.set(pronoun.toLowerCase(), resolved);
        }
    }
    // Resolve definite noun phrases
    var definitePattern = /the\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)/g;
    var match;
    while ((match = definitePattern.exec(text)) !== null) {
        var phrase = match[1];
        var resolved = resolveEntity(phrase);
        if (resolved) {
            entityMap.set(phrase.toLowerCase(), resolved);
        }
    }
    // Build resolved text
    var resolvedText = text;
    var sortedMappings = __spreadArray([], entityMap.entries(), true).sort(function (a, b) { return b[0].length - a[0].length; });
    for (var _c = 0, sortedMappings_2 = sortedMappings; _c < sortedMappings_2.length; _c++) {
        var _d = sortedMappings_2[_c], mention = _d[0], canonical = _d[1];
        var regex = new RegExp("\\b".concat(mention, "\\b"), 'gi');
        resolvedText = resolvedText.replace(regex, "[".concat(canonical, "]"));
    }
    return {
        originalText: originalText,
        resolvedText: resolvedText,
        entityMap: entityMap,
        newEntitiesFound: newEntitiesFound
    };
}
/**
 * Pre-process content before memory storage
 */
function preprocessForMemory(content, store) {
    return __awaiter(this, void 0, void 0, function () {
        var knownEntities, entities, result;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    knownEntities = [];
                    if (store) {
                        entities = store.getEntities();
                        knownEntities = entities.map(function (e) { return e.name; });
                    }
                    return [4 /*yield*/, resolveCoreferences(content, knownEntities, true)];
                case 1:
                    result = _a.sent();
                    return [2 /*return*/, {
                            originalContent: result.originalText,
                            resolvedContent: result.resolvedText,
                            coreferenceMap: Object.fromEntries(result.entityMap),
                            newEntities: result.newEntitiesFound
                        }];
            }
        });
    });
}
/**
 * Simple version without LLM (faster, for batch processing)
 */
function preprocessForMemorySimple(content, store) {
    var knownEntities = [];
    if (store) {
        var entities = store.getEntities();
        knownEntities = entities.map(function (e) { return e.name; });
    }
    var result = resolveCoreferencesSimple(content, knownEntities);
    return {
        originalContent: result.originalText,
        resolvedContent: result.resolvedText,
        coreferenceMap: Object.fromEntries(result.entityMap),
        newEntities: result.newEntitiesFound
    };
}
