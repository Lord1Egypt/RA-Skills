"use strict";
/**
 * Canonical Entity Table
 *
 * Solves the Single-Hop factual recall problem by assigning unique IDs
 * to all entities, regardless of how they're referenced.
 *
 * Example:
 * - "BHP" → ORG_001
 * - "the client" → ORG_001 (same entity)
 * - "Phillip" → PERSON_001
 * - "he" → PERSON_001 (after coreference resolution)
 *
 * This ensures all facts about an entity are linked, even if mentioned
 * with different names or pronouns.
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
exports.CanonicalEntityTable = void 0;
var CanonicalEntityTable = /** @class */ (function () {
    function CanonicalEntityTable(db) {
        this.db = db;
        this.initTable();
    }
    CanonicalEntityTable.prototype.initTable = function () {
        this.db.exec("\n      CREATE TABLE IF NOT EXISTS canonical_entities (\n        id TEXT PRIMARY KEY,\n        canonical_name TEXT NOT NULL,\n        aliases TEXT NOT NULL DEFAULT '[]',\n        type TEXT NOT NULL DEFAULT 'concept',\n        first_mentioned TEXT NOT NULL,\n        last_mentioned TEXT NOT NULL,\n        mention_count INTEGER DEFAULT 1,\n        metadata TEXT\n      );\n      \n      CREATE INDEX IF NOT EXISTS idx_entity_canonical ON canonical_entities(canonical_name);\n      CREATE INDEX IF NOT EXISTS idx_entity_type ON canonical_entities(type);\n    ");
    };
    /**
     * Find an entity by any of its aliases or canonical name
     */
    CanonicalEntityTable.prototype.findByAlias = function (name) {
        // Try exact match on canonical name first
        var exact = this.db.prepare("\n      SELECT * FROM canonical_entities WHERE canonical_name = ?\n    ").get(name);
        if (exact)
            return this.fromRow(exact);
        // Try alias match (JSON array contains)
        var aliasMatch = this.db.prepare("\n      SELECT * FROM canonical_entities WHERE aliases LIKE ?\n    ").get("%\"".concat(name, "\"%"));
        if (aliasMatch)
            return this.fromRow(aliasMatch);
        return null;
    };
    /**
     * Register a new entity or update an existing one
     */
    CanonicalEntityTable.prototype.register = function (name, type, aliases, metadata) {
        if (aliases === void 0) { aliases = []; }
        // Check if exists
        var existing = this.findByAlias(name);
        if (existing) {
            // Update: add new aliases, increment count
            var newAliases = __spreadArray([], new Set(__spreadArray(__spreadArray(__spreadArray([], existing.aliases, true), [name], false), aliases, true)), true);
            this.db.prepare("\n        UPDATE canonical_entities \n        SET aliases = ?, last_mentioned = ?, mention_count = mention_count + 1\n        WHERE id = ?\n      ").run(JSON.stringify(newAliases), new Date().toISOString(), existing.id);
            return __assign(__assign({}, existing), { aliases: newAliases, mentionCount: existing.mentionCount + 1 });
        }
        // Create new entity
        var typePrefix = {
            person: 'PERSON',
            org: 'ORG',
            project: 'PROJECT',
            location: 'LOC',
            event: 'EVENT',
            concept: 'CONCEPT'
        }[type] || 'ENTITY';
        // Get next ID number
        var count = this.db.prepare("\n      SELECT COUNT(*) as count FROM canonical_entities WHERE type = ?\n    ").get(type);
        var id = "".concat(typePrefix, "_").concat(String(count.count + 1).padStart(3, '0'));
        this.db.prepare("\n      INSERT INTO canonical_entities (id, canonical_name, aliases, type, first_mentioned, last_mentioned, mention_count, metadata)\n      VALUES (?, ?, ?, ?, ?, ?, 1, ?)\n    ").run(id, name, JSON.stringify(__spreadArray([name], aliases, true)), type, new Date().toISOString(), new Date().toISOString(), metadata ? JSON.stringify(metadata) : null);
        return {
            id: id,
            canonicalName: name,
            aliases: __spreadArray([name], aliases, true),
            type: type,
            firstMentioned: new Date().toISOString(),
            lastMentioned: new Date().toISOString(),
            mentionCount: 1,
            metadata: metadata
        };
    };
    /**
     * Link an alias to an existing entity
     */
    CanonicalEntityTable.prototype.linkAlias = function (entityId, alias) {
        var entity = this.db.prepare("\n      SELECT * FROM canonical_entities WHERE id = ?\n    ").get(entityId);
        if (!entity)
            return;
        var aliases = JSON.parse(entity.aliases || '[]');
        if (!aliases.includes(alias)) {
            aliases.push(alias);
            this.db.prepare("\n        UPDATE canonical_entities SET aliases = ? WHERE id = ?\n      ").run(JSON.stringify(aliases), entityId);
        }
    };
    /**
     * Get all entities of a type
     */
    CanonicalEntityTable.prototype.getByType = function (type) {
        var _this = this;
        var rows = this.db.prepare("\n      SELECT * FROM canonical_entities WHERE type = ? ORDER BY mention_count DESC\n    ").all(type);
        return rows.map(function (r) { return _this.fromRow(r); });
    };
    /**
     * Get most mentioned entities (for importance ranking)
     */
    CanonicalEntityTable.prototype.getTopEntities = function (limit) {
        var _this = this;
        if (limit === void 0) { limit = 10; }
        var rows = this.db.prepare("\n      SELECT * FROM canonical_entities ORDER BY mention_count DESC LIMIT ?\n    ").all(limit);
        return rows.map(function (r) { return _this.fromRow(r); });
    };
    /**
     * Resolve a mention to its canonical entity ID
     * Returns null if not found (new entity)
     */
    CanonicalEntityTable.prototype.resolve = function (mention) {
        var entity = this.findByAlias(mention);
        return (entity === null || entity === void 0 ? void 0 : entity.id) || null;
    };
    /**
     * Get canonical name for an entity ID
     */
    CanonicalEntityTable.prototype.getCanonicalName = function (entityId) {
        var row = this.db.prepare("\n      SELECT canonical_name FROM canonical_entities WHERE id = ?\n    ").get(entityId);
        return (row === null || row === void 0 ? void 0 : row.canonical_name) || null;
    };
    /**
     * Merge two entities (for deduplication)
     */
    CanonicalEntityTable.prototype.merge = function (primaryId, secondaryId) {
        var primary = this.db.prepare("\n      SELECT * FROM canonical_entities WHERE id = ?\n    ").get(primaryId);
        var secondary = this.db.prepare("\n      SELECT * FROM canonical_entities WHERE id = ?\n    ").get(secondaryId);
        if (!primary || !secondary)
            return;
        // Merge aliases
        var mergedAliases = __spreadArray([], new Set(__spreadArray(__spreadArray([], JSON.parse(primary.aliases || '[]'), true), JSON.parse(secondary.aliases || '[]'), true)), true);
        // Update primary
        this.db.prepare("\n      UPDATE canonical_entities \n      SET aliases = ?, mention_count = ? \n      WHERE id = ?\n    ").run(JSON.stringify(mergedAliases), primary.mention_count + secondary.mention_count, primaryId);
        // Delete secondary
        this.db.prepare("DELETE FROM canonical_entities WHERE id = ?").run(secondaryId);
    };
    CanonicalEntityTable.prototype.fromRow = function (row) {
        return {
            id: row.id,
            canonicalName: row.canonical_name,
            aliases: JSON.parse(row.aliases || '[]'),
            type: row.type,
            firstMentioned: row.first_mentioned,
            lastMentioned: row.last_mentioned,
            mentionCount: row.mention_count,
            metadata: row.metadata ? JSON.parse(row.metadata) : undefined
        };
    };
    return CanonicalEntityTable;
}());
exports.CanonicalEntityTable = CanonicalEntityTable;
