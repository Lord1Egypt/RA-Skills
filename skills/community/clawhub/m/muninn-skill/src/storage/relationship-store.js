"use strict";
/**
 * Relationship Store for Knowledge Graph
 * Stores relationships with timestamps, sessionId, and contradiction tracking
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.RelationshipStore = void 0;
var uuid_1 = require("uuid");
var RelationshipStore = /** @class */ (function () {
    function RelationshipStore(db) {
        this.db = db;
        this.createTables();
    }
    RelationshipStore.prototype.createTables = function () {
        this.db.exec("\n      CREATE TABLE IF NOT EXISTS kg_relationships (\n        id TEXT PRIMARY KEY,\n        source TEXT NOT NULL,\n        target TEXT NOT NULL,\n        type TEXT NOT NULL,\n        value TEXT,\n        timestamp TEXT NOT NULL,\n        session_id TEXT,\n        confidence REAL DEFAULT 1.0,\n        superseded_by TEXT\n      );\n      \n      CREATE INDEX IF NOT EXISTS idx_kg_rel_source ON kg_relationships(source);\n      CREATE INDEX IF NOT EXISTS idx_kg_rel_target ON kg_relationships(target);\n      CREATE INDEX IF NOT EXISTS idx_kg_rel_type ON kg_relationships(type);\n      CREATE INDEX IF NOT EXISTS idx_kg_rel_timestamp ON kg_relationships(timestamp);\n    ");
    };
    /**
     * Add a relationship
     * Returns the relationship and any superseded relationship
     */
    RelationshipStore.prototype.addRelationship = function (rel) {
        var id = "rel_".concat((0, uuid_1.v4)().slice(0, 8));
        // Check for contradictions (same source, type, different value, not already superseded)
        var conflicting = this.findContradiction(rel.source, rel.type, rel.value);
        var supersededBy;
        var supersededRel;
        if (conflicting) {
            // Mark the old relationship as superseded
            var updateStmt = this.db.prepare("\n        UPDATE kg_relationships SET superseded_by = ? WHERE id = ?\n      ");
            updateStmt.run(id, conflicting.id);
            supersededBy = id;
            supersededRel = conflicting;
        }
        // Insert new relationship
        var stmt = this.db.prepare("\n      INSERT INTO kg_relationships (id, source, target, type, value, timestamp, session_id, confidence, superseded_by)\n      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)\n    ");
        stmt.run(id, rel.source, rel.target, rel.type, rel.value || null, rel.timestamp, rel.sessionId || null, rel.confidence, supersededBy || null);
        return {
            relationship: this.getById(id),
            superseded: supersededRel
        };
    };
    /**
     * Find contradiction (same source, same type, different value, not superseded)
     */
    RelationshipStore.prototype.findContradiction = function (source, type, value) {
        if (!value)
            return null;
        var stmt = this.db.prepare("\n      SELECT * FROM kg_relationships \n      WHERE source = ? AND type = ? AND value != ? AND superseded_by IS NULL\n      ORDER BY timestamp DESC\n      LIMIT 1\n    ");
        var row = stmt.get(source, type, value);
        if (!row)
            return null;
        return this.rowToRelationship(row);
    };
    /**
     * Get relationship by ID
     */
    RelationshipStore.prototype.getById = function (id) {
        var stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE id = ?');
        var row = stmt.get(id);
        if (!row)
            return null;
        return this.rowToRelationship(row);
    };
    /**
     * Get relationships from a source entity
     */
    RelationshipStore.prototype.getBySource = function (sourceId) {
        var _this = this;
        var stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE source = ? ORDER BY timestamp DESC');
        var rows = stmt.all(sourceId);
        return rows.map(function (row) { return _this.rowToRelationship(row); });
    };
    /**
     * Get relationships to a target entity
     */
    RelationshipStore.prototype.getByTarget = function (targetId) {
        var _this = this;
        var stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE target = ? ORDER BY timestamp DESC');
        var rows = stmt.all(targetId);
        return rows.map(function (row) { return _this.rowToRelationship(row); });
    };
    /**
     * Get relationships by type
     */
    RelationshipStore.prototype.getByType = function (type) {
        var _this = this;
        var stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE type = ? ORDER BY timestamp DESC');
        var rows = stmt.all(type);
        return rows.map(function (row) { return _this.rowToRelationship(row); });
    };
    /**
     * Get temporal history for an entity and relationship type
     * Returns all versions ordered chronologically
     */
    RelationshipStore.prototype.getHistory = function (sourceId, type) {
        var _this = this;
        var query = 'SELECT * FROM kg_relationships WHERE source = ?';
        var params = [sourceId];
        if (type) {
            query += ' AND type = ?';
            params.push(type);
        }
        query += ' ORDER BY timestamp ASC'; // Chronological order
        var stmt = this.db.prepare(query);
        var rows = stmt.all.apply(stmt, params);
        return rows.map(function (row) { return _this.rowToRelationship(row); });
    };
    /**
     * Get current (non-superseded) relationship for entity + type
     */
    RelationshipStore.prototype.getCurrent = function (sourceId, type) {
        var stmt = this.db.prepare("\n      SELECT * FROM kg_relationships \n      WHERE source = ? AND type = ? AND superseded_by IS NULL\n      ORDER BY timestamp DESC\n      LIMIT 1\n    ");
        var row = stmt.get(sourceId, type);
        if (!row)
            return null;
        return this.rowToRelationship(row);
    };
    /**
     * Get all relationships
     */
    RelationshipStore.prototype.getAll = function () {
        var _this = this;
        var stmt = this.db.prepare('SELECT * FROM kg_relationships ORDER BY timestamp DESC');
        var rows = stmt.all();
        return rows.map(function (row) { return _this.rowToRelationship(row); });
    };
    /**
     * Get relationships by session
     */
    RelationshipStore.prototype.getBySession = function (sessionId) {
        var _this = this;
        var stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE session_id = ? ORDER BY timestamp DESC');
        var rows = stmt.all(sessionId);
        return rows.map(function (row) { return _this.rowToRelationship(row); });
    };
    /**
     * Find all active contradictions (relationships that have been superseded)
     */
    RelationshipStore.prototype.getContradictions = function () {
        var stmt = this.db.prepare("\n      SELECT r.*, s.value as superseded_value\n      FROM kg_relationships r\n      LEFT JOIN kg_relationships s ON r.superseded_by = s.id\n      WHERE r.superseded_by IS NOT NULL\n      ORDER BY r.timestamp DESC\n    ");
        var rows = stmt.all();
        var contradictions = [];
        for (var _i = 0, rows_1 = rows; _i < rows_1.length; _i++) {
            var row = rows_1[_i];
            var current = this.rowToRelationship(row);
            if (row.superseded_by) {
                var superseded = this.getById(row.superseded_by);
                if (superseded) {
                    contradictions.push({ current: current, superseded: superseded });
                }
            }
        }
        return contradictions;
    };
    /**
     * Get all superseded relationships
     */
    RelationshipStore.prototype.getSuperseded = function () {
        var _this = this;
        var stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE superseded_by IS NOT NULL ORDER BY timestamp DESC');
        var rows = stmt.all();
        return rows.map(function (row) { return _this.rowToRelationship(row); });
    };
    RelationshipStore.prototype.rowToRelationship = function (row) {
        return {
            id: row.id,
            source: row.source,
            target: row.target,
            type: row.type,
            value: row.value,
            timestamp: row.timestamp,
            sessionId: row.session_id,
            confidence: row.confidence,
            supersededBy: row.superseded_by
        };
    };
    return RelationshipStore;
}());
exports.RelationshipStore = RelationshipStore;
