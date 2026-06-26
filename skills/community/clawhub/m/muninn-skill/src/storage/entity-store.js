"use strict";
/**
 * Entity Store for Knowledge Graph
 * Stores entities with aliases, mentions, and timestamps
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
exports.EntityStore = void 0;
var uuid_1 = require("uuid");
var EntityStore = /** @class */ (function () {
    function EntityStore(db) {
        this.db = db;
        this.createTables();
    }
    EntityStore.prototype.createTables = function () {
        this.db.exec("\n      CREATE TABLE IF NOT EXISTS kg_entities (\n        id TEXT PRIMARY KEY,\n        name TEXT NOT NULL,\n        type TEXT NOT NULL,\n        aliases TEXT DEFAULT '[]',\n        mentions INTEGER DEFAULT 1,\n        first_seen TEXT NOT NULL,\n        last_seen TEXT NOT NULL\n      );\n      \n      CREATE INDEX IF NOT EXISTS idx_kg_entities_type ON kg_entities(type);\n      CREATE INDEX IF NOT EXISTS idx_kg_entities_name ON kg_entities(name);\n    ");
    };
    /**
     * Add or update an entity
     */
    EntityStore.prototype.addEntity = function (entity) {
        var now = new Date().toISOString();
        var existing = this.getByName(entity.name);
        if (existing) {
            // Update existing entity
            var aliases = __spreadArray([], new Set(__spreadArray(__spreadArray([], existing.aliases, true), entity.aliases, true)), true);
            var stmt_1 = this.db.prepare("\n        UPDATE kg_entities \n        SET aliases = ?, mentions = mentions + 1, last_seen = ?\n        WHERE name = ?\n      ");
            stmt_1.run(JSON.stringify(aliases), now, entity.name);
            return this.getByName(entity.name);
        }
        // Create new entity
        var id = "ent_".concat((0, uuid_1.v4)().slice(0, 8));
        var stmt = this.db.prepare("\n      INSERT INTO kg_entities (id, name, type, aliases, mentions, first_seen, last_seen)\n      VALUES (?, ?, ?, ?, 1, ?, ?)\n    ");
        stmt.run(id, entity.name, entity.type, JSON.stringify(entity.aliases), entity.firstSeen || now, entity.lastSeen || now);
        return this.getById(id);
    };
    /**
     * Get entity by ID
     */
    EntityStore.prototype.getById = function (id) {
        var stmt = this.db.prepare('SELECT * FROM kg_entities WHERE id = ?');
        var row = stmt.get(id);
        if (!row)
            return null;
        return __assign(__assign({}, row), { aliases: JSON.parse(row.aliases || '[]') });
    };
    /**
     * Get entity by name (case-insensitive)
     */
    EntityStore.prototype.getByName = function (name) {
        var stmt = this.db.prepare('SELECT * FROM kg_entities WHERE LOWER(name) = LOWER(?)');
        var row = stmt.get(name);
        if (!row)
            return null;
        return __assign(__assign({}, row), { aliases: JSON.parse(row.aliases || '[]') });
    };
    /**
     * Get all entities of a specific type
     */
    EntityStore.prototype.getByType = function (type) {
        var stmt = this.db.prepare('SELECT * FROM kg_entities WHERE type = ? ORDER BY mentions DESC');
        var rows = stmt.all(type);
        return rows.map(function (row) { return (__assign(__assign({}, row), { aliases: JSON.parse(row.aliases || '[]') })); });
    };
    /**
     * Get all entities
     */
    EntityStore.prototype.getAll = function () {
        var stmt = this.db.prepare('SELECT * FROM kg_entities ORDER BY mentions DESC');
        var rows = stmt.all();
        return rows.map(function (row) { return (__assign(__assign({}, row), { aliases: JSON.parse(row.aliases || '[]') })); });
    };
    /**
     * Find entity by exact name or alias
     */
    EntityStore.prototype.findEntity = function (nameOrAlias) {
        // Try exact name match first
        var byName = this.getByName(nameOrAlias);
        if (byName)
            return byName;
        // Search aliases
        var stmt = this.db.prepare('SELECT * FROM kg_entities WHERE aliases LIKE ?');
        var rows = stmt.all("%".concat(nameOrAlias, "%"));
        for (var _i = 0, rows_1 = rows; _i < rows_1.length; _i++) {
            var row = rows_1[_i];
            var aliases = JSON.parse(row.aliases || '[]');
            if (aliases.some(function (a) { return a.toLowerCase() === nameOrAlias.toLowerCase(); })) {
                return __assign(__assign({}, row), { aliases: aliases });
            }
        }
        return null;
    };
    /**
     * Get entity history (all updates)
     */
    EntityStore.prototype.getHistory = function (entityName) {
        // Since we don't track history in the current schema, return current state
        var entity = this.getByName(entityName);
        if (!entity)
            return [];
        return [{
                mentions: entity.mentions,
                lastSeen: entity.lastSeen
            }];
    };
    return EntityStore;
}());
exports.EntityStore = EntityStore;
