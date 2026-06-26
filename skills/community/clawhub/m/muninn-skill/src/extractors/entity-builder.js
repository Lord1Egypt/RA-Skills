"use strict";
/**
 * Canonical Entity List Builder
 *
 * Scans memories and builds a canonical entity list with:
 * - Entity extraction (NER + LLM)
 * - Alias clustering
 * - Manual merge/dedup support
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
exports.registerEntity = registerEntity;
exports.addAlias = addAlias;
exports.findEntity = findEntity;
exports.getAllEntities = getAllEntities;
exports.getEntitiesByType = getEntitiesByType;
exports.mergeEntities = mergeEntities;
exports.extractEntitiesFromText = extractEntitiesFromText;
exports.scanMemoriesForEntities = scanMemoriesForEntities;
exports.exportEntityList = exportEntityList;
exports.clearCache = clearCache;
var fs_1 = require("fs");
var ENTITY_CACHE_PATH = '/tmp/muninn-entity-cache.json';
// Global cache
var cache = null;
function loadCache() {
    if (cache)
        return cache;
    if (fs_1.default.existsSync(ENTITY_CACHE_PATH)) {
        try {
            var data = JSON.parse(fs_1.default.readFileSync(ENTITY_CACHE_PATH, 'utf-8'));
            cache = {
                entities: data.entities || {},
                aliasToEntity: data.aliasToEntity || {},
                lastId: data.lastId || 0
            };
            return cache;
        }
        catch (e) {
            // Corrupted, start fresh
        }
    }
    cache = {
        entities: {},
        aliasToEntity: {},
        lastId: 0
    };
    return cache;
}
function saveCache() {
    if (!cache)
        return;
    fs_1.default.writeFileSync(ENTITY_CACHE_PATH, JSON.stringify(cache, null, 2));
}
function generateId(type) {
    var c = loadCache();
    c.lastId++;
    var prefix = {
        person: 'PERSON',
        org: 'ORG',
        project: 'PROJECT',
        location: 'LOC',
        event: 'EVENT',
        concept: 'CONCEPT',
        other: 'ENTITY'
    }[type] || 'ENTITY';
    return "".concat(prefix, "_").concat(String(c.lastId).padStart(3, '0'));
}
/**
 * Register a new entity or add alias to existing
 */
function registerEntity(name, type, timestamp) {
    var c = loadCache();
    var normalizedName = name.trim().toLowerCase();
    // Check if already exists as alias
    var existingId = c.aliasToEntity[normalizedName];
    if (existingId) {
        var existing = c.entities[existingId];
        if (existing) {
            existing.mentionCount++;
            existing.lastMentioned = timestamp || new Date().toISOString();
            saveCache();
            return existing;
        }
    }
    // Check if similar name exists (fuzzy match)
    for (var _i = 0, _a = Object.entries(c.entities); _i < _a.length; _i++) {
        var _b = _a[_i], id_1 = _b[0], entity_1 = _b[1];
        if (entity_1.merged)
            continue;
        // Check if names are similar
        if (isSimilarName(normalizedName, entity_1.name.toLowerCase())) {
            // Add as alias
            entity_1.aliases.push(name);
            c.aliasToEntity[normalizedName] = entity_1.id;
            entity_1.mentionCount++;
            entity_1.lastMentioned = timestamp || new Date().toISOString();
            saveCache();
            return entity_1;
        }
    }
    // Create new entity
    var id = generateId(type);
    var entity = {
        id: id,
        name: name.trim(),
        type: type,
        aliases: [name],
        mentionCount: 1,
        firstMentioned: timestamp || new Date().toISOString(),
        lastMentioned: timestamp || new Date().toISOString(),
        confidence: 1.0
    };
    c.entities[id] = entity;
    c.aliasToEntity[normalizedName] = id;
    saveCache();
    return entity;
}
/**
 * Add alias to existing entity
 */
function addAlias(entityId, alias) {
    var c = loadCache();
    var entity = c.entities[entityId];
    if (!entity)
        return false;
    var normalizedAlias = alias.trim().toLowerCase();
    // Check if alias already mapped
    var existingId = c.aliasToEntity[normalizedAlias];
    if (existingId && existingId !== entityId) {
        // Alias belongs to another entity - would need merge
        return false;
    }
    if (!entity.aliases.includes(alias)) {
        entity.aliases.push(alias);
    }
    c.aliasToEntity[normalizedAlias] = entityId;
    saveCache();
    return true;
}
/**
 * Find entity by name or alias
 */
function findEntity(nameOrAlias) {
    var c = loadCache();
    var normalized = nameOrAlias.trim().toLowerCase();
    // Check alias map
    var entityId = c.aliasToEntity[normalized];
    if (entityId) {
        var entity = c.entities[entityId];
        if (entity && !entity.merged)
            return entity;
    }
    // Fuzzy search
    for (var _i = 0, _a = Object.values(c.entities); _i < _a.length; _i++) {
        var entity = _a[_i];
        if (entity.merged)
            continue;
        if (isSimilarName(normalized, entity.name.toLowerCase())) {
            return entity;
        }
        for (var _b = 0, _c = entity.aliases; _b < _c.length; _b++) {
            var alias = _c[_b];
            if (isSimilarName(normalized, alias.toLowerCase())) {
                return entity;
            }
        }
    }
    return null;
}
/**
 * Get all entities
 */
function getAllEntities() {
    var c = loadCache();
    return Object.values(c.entities).filter(function (e) { return !e.merged; });
}
/**
 * Get entities by type
 */
function getEntitiesByType(type) {
    return getAllEntities().filter(function (e) { return e.type === type; });
}
/**
 * Merge entity A into entity B
 */
function mergeEntities(sourceId, targetId) {
    var c = loadCache();
    var source = c.entities[sourceId];
    var target = c.entities[targetId];
    if (!source || !target)
        return false;
    // Move all aliases to target
    for (var _i = 0, _a = source.aliases; _i < _a.length; _i++) {
        var alias = _a[_i];
        if (!target.aliases.includes(alias)) {
            target.aliases.push(alias);
        }
        c.aliasToEntity[alias.toLowerCase()] = targetId;
    }
    // Update mention count
    target.mentionCount += source.mentionCount;
    // Mark source as merged
    source.merged = true;
    source.mergedInto = targetId;
    saveCache();
    return true;
}
/**
 * Extract entities from text using LLM
 */
function extractEntitiesFromText(text, timestamp) {
    return __awaiter(this, void 0, void 0, function () {
        var prompt, response, data, output, jsonMatch, entities, registered, _i, entities_1, e, registered_entity, e_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    prompt = "Extract all named entities from the following text. Return JSON array with objects containing: name, type (person|org|project|location|event|concept|other).\n\nText: ".concat(text, "\n\nEntities (JSON array):");
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 4, , 5]);
                    return [4 /*yield*/, fetch('http://localhost:11434/api/generate', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                model: 'qwen2.5:1.5b',
                                prompt: prompt,
                                stream: false,
                                options: { num_predict: 500, temperature: 0.1 }
                            })
                        })];
                case 2:
                    response = _a.sent();
                    return [4 /*yield*/, response.json()];
                case 3:
                    data = _a.sent();
                    output = data.response || data.thinking || '';
                    jsonMatch = output.match(/\[[\s\S]*\]/);
                    if (!jsonMatch)
                        return [2 /*return*/, []];
                    entities = JSON.parse(jsonMatch[0]);
                    registered = [];
                    for (_i = 0, entities_1 = entities; _i < entities_1.length; _i++) {
                        e = entities_1[_i];
                        if (e.name && e.type) {
                            registered_entity = registerEntity(e.name, e.type, timestamp);
                            registered.push(registered_entity);
                        }
                    }
                    return [2 /*return*/, registered];
                case 4:
                    e_1 = _a.sent();
                    console.error('Entity extraction error:', e_1);
                    return [2 /*return*/, []];
                case 5: return [2 /*return*/];
            }
        });
    });
}
/**
 * Scan all memories and build entity list
 */
function scanMemoriesForEntities(memories) {
    return __awaiter(this, void 0, void 0, function () {
        var newEntities, beforeCount, _i, memories_1, memory, extracted, afterCount;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    newEntities = 0;
                    beforeCount = getAllEntities().length;
                    _i = 0, memories_1 = memories;
                    _a.label = 1;
                case 1:
                    if (!(_i < memories_1.length)) return [3 /*break*/, 4];
                    memory = memories_1[_i];
                    return [4 /*yield*/, extractEntitiesFromText(memory.content, memory.timestamp)];
                case 2:
                    extracted = _a.sent();
                    newEntities += extracted.length;
                    _a.label = 3;
                case 3:
                    _i++;
                    return [3 /*break*/, 1];
                case 4:
                    afterCount = getAllEntities().length;
                    return [2 /*return*/, {
                            total: afterCount,
                            newEntities: afterCount - beforeCount,
                            entities: getAllEntities()
                        }];
            }
        });
    });
}
/**
 * Export entity list for review
 */
function exportEntityList() {
    var entities = getAllEntities();
    var byType = {};
    for (var _i = 0, entities_2 = entities; _i < entities_2.length; _i++) {
        var entity = entities_2[_i];
        byType[entity.type] = (byType[entity.type] || 0) + 1;
    }
    var topMentioned = __spreadArray([], entities, true).sort(function (a, b) { return b.mentionCount - a.mentionCount; })
        .slice(0, 10);
    return {
        entities: entities,
        statistics: {
            total: entities.length,
            byType: byType,
            topMentioned: topMentioned
        }
    };
}
/**
 * Clear cache (for testing)
 */
function clearCache() {
    cache = null;
    if (fs_1.default.existsSync(ENTITY_CACHE_PATH)) {
        fs_1.default.unlinkSync(ENTITY_CACHE_PATH);
    }
}
// Fuzzy name matching
function isSimilarName(a, b) {
    // Exact match
    if (a === b)
        return true;
    // One contains the other (e.g., "BHP" in "BHP Billiton")
    if (a.includes(b) || b.includes(a))
        return true;
    // Common nicknames
    var nicknames = {
        'william': ['will', 'bill', 'billy'],
        'elizabeth': ['liz', 'beth', 'betty', 'eliza'],
        'michael': ['mike', 'mikey'],
        'jennifer': ['jen', 'jenny'],
        'katherine': ['kate', 'kathy', 'katie'],
        'robert': ['rob', 'bob', 'bobby'],
        'richard': ['rick', 'dick', 'rich'],
        'charles': ['charlie', 'chuck'],
        'margaret': ['maggie', 'meg', 'peggy'],
        'patricia': ['pat', 'patty'],
        'david': ['dave', 'davey'],
        'james': ['jim', 'jimmy', 'jamie'],
        'caroline': ['carol', 'carrie'],
        'melanie': ['mel', 'melody']
    };
    var aLower = a.toLowerCase();
    var bLower = b.toLowerCase();
    for (var _i = 0, _a = Object.entries(nicknames); _i < _a.length; _i++) {
        var _b = _a[_i], full = _b[0], nicks = _b[1];
        if ((aLower === full && nicks.includes(bLower)) ||
            (bLower === full && nicks.includes(aLower)) ||
            (nicks.includes(aLower) && nicks.includes(bLower))) {
            return true;
        }
    }
    // Levenshtein distance for short names
    if (a.length <= 5 && b.length <= 5) {
        var distance = levenshteinDistance(a, b);
        if (distance <= 1)
            return true;
    }
    return false;
}
function levenshteinDistance(a, b) {
    var matrix = [];
    for (var i = 0; i <= b.length; i++) {
        matrix[i] = [i];
    }
    for (var j = 0; j <= a.length; j++) {
        matrix[0][j] = j;
    }
    for (var i = 1; i <= b.length; i++) {
        for (var j = 1; j <= a.length; j++) {
            if (b.charAt(i - 1) === a.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            }
            else {
                matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j] + 1);
            }
        }
    }
    return matrix[b.length][a.length];
}
