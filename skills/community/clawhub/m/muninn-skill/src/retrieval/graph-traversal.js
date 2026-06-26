"use strict";
/**
 * Graph Traversal for Knowledge Graph
 * BFS for multi-hop connections with path ranking
 */
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
exports.findPaths = findPaths;
exports.getConnectedEntities = getConnectedEntities;
exports.getEntityRelationships = getEntityRelationships;
exports.findEntitiesByRelationship = findEntitiesByRelationship;
exports.getEntityTimeline = getEntityTimeline;
/**
 * Find all paths between two entities using BFS
 */
function findPaths(entityStore, relationshipStore, fromEntityName, toEntityName, options) {
    var _a;
    if (options === void 0) { options = {}; }
    var maxHops = options.maxHops || 3;
    var includeSuperseded = (_a = options.includeSuperseded) !== null && _a !== void 0 ? _a : false;
    var fromEntity = entityStore.findEntity(fromEntityName);
    var toEntity = entityStore.findEntity(toEntityName);
    if (!fromEntity || !toEntity) {
        return [];
    }
    var paths = [];
    var visited = new Set();
    var queue = [{
            entityId: fromEntity.id,
            path: [fromEntity.id],
            relPath: []
        }];
    while (queue.length > 0) {
        var current = queue.shift();
        // Check if we reached the target
        if (current.entityId === toEntity.id && current.path.length > 1) {
            paths.push({
                entities: current.path,
                relationships: current.relPath,
                hops: current.path.length - 1,
                relevance: calculatePathRelevance(current.path, current.relPath, relationshipStore)
            });
            continue;
        }
        // Stop if max hops reached
        if (current.path.length >= maxHops + 1)
            continue;
        // Get neighbors (outgoing relationships)
        var relationships = relationshipStore.getBySource(current.entityId);
        // Filter relationships
        var filtered = relationships.filter(function (r) {
            if (!includeSuperseded && r.supersededBy)
                return false;
            if (options.relationshipTypes && !options.relationshipTypes.includes(r.type))
                return false;
            return true;
        });
        for (var _i = 0, filtered_1 = filtered; _i < filtered_1.length; _i++) {
            var rel = filtered_1[_i];
            if (!visited.has(rel.target)) {
                queue.push({
                    entityId: rel.target,
                    path: __spreadArray(__spreadArray([], current.path, true), [rel.target], false),
                    relPath: __spreadArray(__spreadArray([], current.relPath, true), [rel.id], false)
                });
            }
        }
        // Also check incoming relationships
        var incoming = relationshipStore.getByTarget(current.entityId);
        var filteredIncoming = incoming.filter(function (r) {
            if (!includeSuperseded && r.supersededBy)
                return false;
            if (options.relationshipTypes && !options.relationshipTypes.includes(r.type))
                return false;
            return true;
        });
        for (var _b = 0, filteredIncoming_1 = filteredIncoming; _b < filteredIncoming_1.length; _b++) {
            var rel = filteredIncoming_1[_b];
            if (!visited.has(rel.source)) {
                queue.push({
                    entityId: rel.source,
                    path: __spreadArray(__spreadArray([], current.path, true), [rel.source], false),
                    relPath: __spreadArray(__spreadArray([], current.relPath, true), [rel.id], false)
                });
            }
        }
    }
    // Sort by relevance (shorter paths with higher confidence first)
    paths.sort(function (a, b) {
        if (a.hops !== b.hops)
            return a.hops - b.hops;
        return b.relevance - a.relevance;
    });
    return paths.slice(0, 10); // Return top 10 paths
}
/**
 * Calculate path relevance score
 */
function calculatePathRelevance(entityPath, relationshipPath, relationshipStore) {
    if (relationshipPath.length === 0)
        return 0;
    var totalConfidence = 0;
    for (var _i = 0, relationshipPath_1 = relationshipPath; _i < relationshipPath_1.length; _i++) {
        var relId = relationshipPath_1[_i];
        var rel = relationshipStore.getById(relId);
        if (rel) {
            totalConfidence += rel.confidence;
        }
    }
    var avgConfidence = totalConfidence / relationshipPath.length;
    // Prefer shorter paths
    var hopPenalty = entityPath.length * 0.1;
    return Math.max(0, avgConfidence - hopPenalty);
}
/**
 * Get all entities connected to a given entity
 */
function getConnectedEntities(entityStore, relationshipStore, entityName, options) {
    if (options === void 0) { options = {}; }
    var entity = entityStore.findEntity(entityName);
    if (!entity)
        return [];
    var connectedIds = new Set();
    // Get outgoing
    var outgoing = relationshipStore.getBySource(entity.id);
    for (var _i = 0, outgoing_1 = outgoing; _i < outgoing_1.length; _i++) {
        var rel = outgoing_1[_i];
        if (!rel.supersededBy || options.includeSuperseded) {
            connectedIds.add(rel.target);
        }
    }
    // Get incoming
    var incoming = relationshipStore.getByTarget(entity.id);
    for (var _a = 0, incoming_1 = incoming; _a < incoming_1.length; _a++) {
        var rel = incoming_1[_a];
        if (!rel.supersededBy || options.includeSuperseded) {
            connectedIds.add(rel.source);
        }
    }
    // Convert IDs to entities
    var connected = [];
    for (var _b = 0, connectedIds_1 = connectedIds; _b < connectedIds_1.length; _b++) {
        var id = connectedIds_1[_b];
        var e = entityStore.getById(id);
        if (e)
            connected.push(e);
    }
    return connected;
}
/**
 * Get all relationships for an entity (both as source and target)
 */
function getEntityRelationships(entityStore, relationshipStore, entityName, options) {
    if (options === void 0) { options = {}; }
    var entity = entityStore.findEntity(entityName);
    if (!entity)
        return [];
    var relationships = [];
    // Get outgoing
    var outgoing = relationshipStore.getBySource(entity.id);
    for (var _i = 0, outgoing_2 = outgoing; _i < outgoing_2.length; _i++) {
        var rel = outgoing_2[_i];
        if (!rel.supersededBy || options.includeSuperseded) {
            relationships.push(rel);
        }
    }
    // Get incoming
    var incoming = relationshipStore.getByTarget(entity.id);
    for (var _a = 0, incoming_2 = incoming; _a < incoming_2.length; _a++) {
        var rel = incoming_2[_a];
        if (!rel.supersededBy || options.includeSuperseded) {
            relationships.push(rel);
        }
    }
    return relationships;
}
/**
 * Find entities by relationship pattern
 */
function findEntitiesByRelationship(entityStore, relationshipStore, relationshipType, value) {
    var relationships = value
        ? relationshipStore.getByType(relationshipType).filter(function (r) { return r.value === value; })
        : relationshipStore.getByType(relationshipType);
    var entityIds = new Set();
    for (var _i = 0, relationships_1 = relationships; _i < relationships_1.length; _i++) {
        var rel = relationships_1[_i];
        if (!rel.supersededBy) {
            entityIds.add(rel.source);
        }
    }
    var entities = [];
    for (var _a = 0, entityIds_1 = entityIds; _a < entityIds_1.length; _a++) {
        var id = entityIds_1[_a];
        var entity = entityStore.getById(id);
        if (entity)
            entities.push(entity);
    }
    return entities;
}
/**
 * Get timeline of an entity's relationships
 */
function getEntityTimeline(entityStore, relationshipStore, entityName, relationshipType) {
    var entity = entityStore.findEntity(entityName);
    if (!entity)
        return [];
    // Get all relationships ordered by timestamp
    var history = relationshipStore.getHistory(entity.id, relationshipType);
    var timeline = [];
    for (var _i = 0, history_1 = history; _i < history_1.length; _i++) {
        var rel = history_1[_i];
        // Get the other entity in the relationship
        var otherId = rel.source === entity.id ? rel.target : rel.source;
        var otherEntity = entityStore.getById(otherId);
        if (otherEntity) {
            timeline.push({
                relationship: rel,
                entity: otherEntity
            });
        }
    }
    return timeline;
}
