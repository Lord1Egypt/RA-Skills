#!/usr/bin/env node
"use strict";
/**
 * Entity List Builder CLI
 *
 * Usage:
 *   node entity-cli.js scan <db-path>     - Scan memories for entities
 *   node entity-cli.js list               - List all entities
 *   node entity-cli.js merge <from> <to>  - Merge entity A into B
 *   node entity-cli.js export             - Export for review
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
var better_sqlite3_1 = require("better-sqlite3");
var entity_builder_js_1 = require("../extractors/entity-builder.js");
var args = process.argv.slice(2);
var command = args[0];
function main() {
    return __awaiter(this, void 0, void 0, function () {
        var _a, dbPath, db, memories, result, stats, _i, _b, e, entities, type_1, filtered, _c, filtered_1, e, byType, _d, entities_1, e, _e, _f, _g, t, ents, _h, _j, e, fromId, toId, success, entityId, alias, success, name_1, entity, stats, _k, _l, _m, type, count, _o, _p, e, exportPath, fs;
        return __generator(this, function (_q) {
            switch (_q.label) {
                case 0:
                    _a = command;
                    switch (_a) {
                        case 'scan': return [3 /*break*/, 1];
                        case 'list': return [3 /*break*/, 3];
                        case 'merge': return [3 /*break*/, 4];
                        case 'alias': return [3 /*break*/, 5];
                        case 'find': return [3 /*break*/, 6];
                        case 'export': return [3 /*break*/, 7];
                        case 'clear': return [3 /*break*/, 9];
                    }
                    return [3 /*break*/, 10];
                case 1:
                    dbPath = args[1];
                    if (!dbPath) {
                        console.error('Usage: node entity-cli.js scan <db-path>');
                        process.exit(1);
                    }
                    console.log('📂 Scanning memories for entities...\n');
                    db = new better_sqlite3_1.default(dbPath, { readonly: true });
                    memories = db.prepare("\n        SELECT content, created_at as timestamp \n        FROM memories \n        ORDER BY created_at ASC\n      ").all();
                    console.log("Found ".concat(memories.length, " memories\n"));
                    return [4 /*yield*/, (0, entity_builder_js_1.scanMemoriesForEntities)(memories)];
                case 2:
                    result = _q.sent();
                    console.log('\n✅ Scan complete!');
                    console.log("   Total entities: ".concat(result.total));
                    console.log("   New entities: ".concat(result.newEntities));
                    stats = (0, entity_builder_js_1.exportEntityList)();
                    console.log('\n📊 Top mentioned entities:');
                    for (_i = 0, _b = stats.statistics.topMentioned.slice(0, 5); _i < _b.length; _i++) {
                        e = _b[_i];
                        console.log("   ".concat(e.id, ": ").concat(e.name, " (").concat(e.type, ") - ").concat(e.mentionCount, " mentions"));
                    }
                    db.close();
                    return [3 /*break*/, 11];
                case 3:
                    {
                        entities = (0, entity_builder_js_1.getAllEntities)();
                        type_1 = args[1];
                        if (type_1) {
                            filtered = entities.filter(function (e) { return e.type === type_1; });
                            console.log("\n\uD83D\uDCCB ".concat(type_1.toUpperCase(), " entities (").concat(filtered.length, "):\n"));
                            for (_c = 0, filtered_1 = filtered; _c < filtered_1.length; _c++) {
                                e = filtered_1[_c];
                                console.log("  ".concat(e.id, ": ").concat(e.name));
                                if (e.aliases.length > 1) {
                                    console.log("    Aliases: ".concat(e.aliases.slice(1).join(', ')));
                                }
                                console.log("    Mentions: ".concat(e.mentionCount));
                            }
                        }
                        else {
                            console.log("\n\uD83D\uDCCB All entities (".concat(entities.length, "):\n"));
                            byType = {};
                            for (_d = 0, entities_1 = entities; _d < entities_1.length; _d++) {
                                e = entities_1[_d];
                                byType[e.type] = byType[e.type] || [];
                                byType[e.type].push(e);
                            }
                            for (_e = 0, _f = Object.entries(byType); _e < _f.length; _e++) {
                                _g = _f[_e], t = _g[0], ents = _g[1];
                                console.log("\n".concat(t.toUpperCase(), " (").concat(ents.length, "):"));
                                for (_h = 0, _j = ents.slice(0, 10); _h < _j.length; _h++) {
                                    e = _j[_h];
                                    console.log("  ".concat(e.id, ": ").concat(e.name, " (").concat(e.mentionCount, ")"));
                                }
                                if (ents.length > 10) {
                                    console.log("  ... and ".concat(ents.length - 10, " more"));
                                }
                            }
                        }
                        return [3 /*break*/, 11];
                    }
                    _q.label = 4;
                case 4:
                    {
                        fromId = args[1];
                        toId = args[2];
                        if (!fromId || !toId) {
                            console.error('Usage: node entity-cli.js merge <from-id> <to-id>');
                            console.error('Example: node entity-cli.js merge PERSON_002 PERSON_001');
                            process.exit(1);
                        }
                        success = (0, entity_builder_js_1.mergeEntities)(fromId, toId);
                        if (success) {
                            console.log("\u2705 Merged ".concat(fromId, " into ").concat(toId));
                        }
                        else {
                            console.error("\u274C Failed to merge. Check IDs.");
                        }
                        return [3 /*break*/, 11];
                    }
                    _q.label = 5;
                case 5:
                    {
                        entityId = args[1];
                        alias = args[2];
                        if (!entityId || !alias) {
                            console.error('Usage: node entity-cli.js alias <entity-id> <alias>');
                            process.exit(1);
                        }
                        success = (0, entity_builder_js_1.addAlias)(entityId, alias);
                        if (success) {
                            console.log("\u2705 Added alias \"".concat(alias, "\" to ").concat(entityId));
                        }
                        else {
                            console.error("\u274C Failed to add alias.");
                        }
                        return [3 /*break*/, 11];
                    }
                    _q.label = 6;
                case 6:
                    {
                        name_1 = args.slice(1).join(' ');
                        if (!name_1) {
                            console.error('Usage: node entity-cli.js find <name>');
                            process.exit(1);
                        }
                        entity = (0, entity_builder_js_1.findEntity)(name_1);
                        if (entity) {
                            console.log("\n\u2705 Found: ".concat(entity.id));
                            console.log("   Name: ".concat(entity.name));
                            console.log("   Type: ".concat(entity.type));
                            console.log("   Aliases: ".concat(entity.aliases.join(', ')));
                            console.log("   Mentions: ".concat(entity.mentionCount));
                        }
                        else {
                            console.log("\u274C No entity found for \"".concat(name_1, "\""));
                        }
                        return [3 /*break*/, 11];
                    }
                    _q.label = 7;
                case 7:
                    stats = (0, entity_builder_js_1.exportEntityList)();
                    console.log('\n📊 Entity Statistics:');
                    console.log("   Total entities: ".concat(stats.statistics.total));
                    console.log('\n   By type:');
                    for (_k = 0, _l = Object.entries(stats.statistics.byType); _k < _l.length; _k++) {
                        _m = _l[_k], type = _m[0], count = _m[1];
                        console.log("     ".concat(type, ": ").concat(count));
                    }
                    console.log('\n   Top 10 mentioned:');
                    for (_o = 0, _p = stats.statistics.topMentioned; _o < _p.length; _o++) {
                        e = _p[_o];
                        console.log("     ".concat(e.name, " (").concat(e.type, "): ").concat(e.mentionCount, " mentions"));
                        if (e.aliases.length > 1) {
                            console.log("       Aliases: ".concat(e.aliases.slice(1).join(', ')));
                        }
                    }
                    exportPath = '/tmp/muninn-entities-export.json';
                    return [4 /*yield*/, Promise.resolve().then(function () { return require('fs'); })];
                case 8:
                    fs = _q.sent();
                    fs.writeFileSync(exportPath, JSON.stringify(stats, null, 2));
                    console.log("\n\uD83D\uDCC1 Exported to: ".concat(exportPath));
                    return [3 /*break*/, 11];
                case 9:
                    {
                        (0, entity_builder_js_1.clearCache)();
                        console.log('✅ Entity cache cleared');
                        return [3 /*break*/, 11];
                    }
                    _q.label = 10;
                case 10:
                    console.log("\nEntity List Builder CLI\n\nCommands:\n  scan <db-path>       Scan memories for entities\n  list [type]          List all entities (or by type)\n  merge <from> <to>    Merge entity A into B\n  alias <id> <alias>   Add alias to entity\n  find <name>          Find entity by name/alias\n  export               Export statistics and top entities\n  clear                Clear entity cache\n\nExamples:\n  node entity-cli.js scan /path/to/memories.db\n  node entity-cli.js list person\n  node entity-cli.js merge PERSON_002 PERSON_001\n  node entity-cli.js alias PERSON_001 \"Carrie\"\n  node entity-cli.js find Caroline\n");
                    _q.label = 11;
                case 11: return [2 /*return*/];
            }
        });
    });
}
main().catch(console.error);
