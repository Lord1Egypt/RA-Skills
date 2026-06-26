"use strict";
/**
 * Relationship Extractor
 * Extracts relationships from memory content using pattern matching
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractRelationships = extractRelationships;
exports.extractAndResolveRelationships = extractAndResolveRelationships;
exports.inferTypeFromContext = inferTypeFromContext;
exports.inferEntityType = inferEntityType;
// Pattern definitions for relationship extraction
var RELATIONSHIP_PATTERNS = {
    has_target: [
        // "X target revenue is $Y/month" - value is the target
        /(\w+)\s+(?:target|revenue target|goal)\s+(?:revenue\s+)?(?:is|of|at)\s+\$?([\d,]+(?:\/\w+)?)/gi,
        /(\w+)\s+target\s+(?:revenue\s+)?(?:is|at|of)\s+\$?([\d,]+(?:\/\w+)?)/gi,
        /target\s+(?:revenue\s+)?(?:for|of)\s+(\w+)\s+(?:is|at|of)\s+\$?([\d,]+(?:\/\w+)?)/gi,
        // Simpler pattern: "Elev8Advisory target revenue is $2000/month"
        /(\w+(?:\w+)*)\s+target\s+.*?\$?([\d,]+\/\w+)/gi,
    ],
    has_customer: [
        // "X has customer paying $Y/month" - value is the target
        /(\w+)\s+(?:has|got|acquired)\s+(?:a\s+)?customer\s+(?:paying\s+)?(?:us\s+)?\$?([\d,]+(?:\/\w+)?)/gi,
        /customer\s+(?:for|of)\s+(\w+)\s+(?:pays|paying)\s+\$?([\d,]+(?:\/\w+)?)/gi,
        /(\w+)\s+(?:has|with)\s+(?:a\s+)?(?:paying\s+)?(?:customer|customer paying)\s+\$?([\d,]+(?:\/\w+)?)/gi,
    ],
    uses: [
        /(\w+)\s+uses?\s+(\w+)/gi,
        /(\w+)\s+(?:built|powered|built on|built with)\s+(\w+)/gi,
        /using\s+(\w+)\s+(?:for|with|in)\s+(\w+)/gi,
    ],
    built_by: [
        /(\w+)\s+(?:built|created|developed|made)\s+by\s+(\w+)/gi,
        /(\w+)\s+is\s+(?:built|created|developed)\s+by\s+(\w+)/gi,
    ],
    employs: [
        /(\w+)\s+(?:handles?|does|manages?|works on)\s+(\w+)/gi,
        /(\w+)\s+(?:specialist|expert|agent)\s+(?:for|in)\s+(\w+)/gi,
        /(\w+)\s+(?:team includes?|has)\s+(\w+)\s+(?:for|as)/gi,
    ],
    has_priority: [
        /(\w+)\s+(?:is\s+)?(?:priority|first|primary|main)\s+(?:project|focus|item)?/gi,
        /priority\s+(?:is|shifted|changed|moved)\s+(?:to|from)\s+(\w+)/gi,
        /focus\s+(?:is|on)\s+(\w+)/gi,
    ],
    part_of: [
        /(\w+)\s+(?:part of|part of the|from)\s+(\w+)/gi,
    ],
    // P7: Conversational relationships for multi-hop reasoning
    went_to: [
        /([A-Z][a-z]+)\s+(?:went to|visited|attended)\s+(?:a\s+|an\s+|the\s+)?([A-Za-z]+(?:\s+[A-Za-z]+)?)/gi,
        /([A-Z][a-z]+)\s+(?:goes to|goes)\s+(?:to\s+)?(?:a\s+|an\s+|the\s+)?([A-Za-z]+(?:\s+[A-Za-z]+)?)/gi,
    ],
    works_at: [
        /([A-Z][a-z]+)\s+(?:works|worked|is working)\s+(?:at|for|in|on)\s+(?:a\s+)?([A-Za-z]+(?:\s+[A-Za-z]+)?)/gi,
        /([A-Z][a-z]+)'?\s*(?:job|work|position)\s+(?:is|at)\s+([A-Za-z]+)/gi,
    ],
    knows: [
        /([A-Z][a-z]+)\s+(?:knows|met|spoke with|talked to|spoke to)\s+([A-Z][a-z]+)/gi,
        /([A-Z][a-z]+)\s+(?:and|&)\s+([A-Z][a-z]+)\s+(?:are|were|discussed|talked)/gi,
    ],
    has_interest: [
        /([A-Z][a-z]+)\s+(?:is interested in|enjoys|likes|loves|passionate about)\s+([a-z]+(?:\s+[a-z]+)?)/gi,
        /([A-Z][a-z]+)'?\s*(?:interest|hobby|passion)\s+(?:is|includes?)\s+([a-z]+)/gi,
    ],
    has_identity: [
        /([A-Z][a-z]+)\s+(?:is|identifies as|identifies with)\s+(?:a\s+|an\s+)?([a-z]+(?:\s+[a-z]+)?)/gi,
        /([A-Z][a-z]+)\s+(?:told|said|mentioned)\s+(?:me\s+)?(?:that\s+)?(?:he|she|they)\s+(?:is|are)\s+(?:a\s+)?([a-z]+)/gi,
    ],
    has_plan: [
        /([A-Z][a-z]+)\s+(?:plans|planning|wants|wants to|going to)\s+([a-z]+(?:\s+[a-z]+)?)/gi,
        /([A-Z][a-z]+)'?\s*(?:plan|goal|aim)\s+(?:is|to)\s+([a-z]+)/gi,
    ],
};
// Entity type inference based on name patterns
function inferEntityType(name) {
    var lower = name.toLowerCase();
    // Project names often have specific patterns
    if (lower.includes('advisory') || lower.includes('forge') || lower.includes('system')) {
        return 'project';
    }
    // Agent/person names
    if (lower.includes('hiko') || lower.includes('babbage') || lower.includes('clemens') ||
        lower.includes('paulsen') || lower.includes('kakapo')) {
        return 'person';
    }
    // Organizations
    if (lower.includes('inc') || lower.includes('llc') || lower.includes('corp')) {
        return 'organization';
    }
    // Technologies
    if (lower.includes('react') || lower.includes('node') || lower.includes('sql') ||
        lower.includes('ollama') || lower.includes('stripe') || lower.includes('postgres')) {
        return 'technology';
    }
    // Locations
    if (lower.includes('brisbane') || lower.includes('australia') || lower.includes('city')) {
        return 'location';
    }
    return 'project'; // Default for SaaS projects
}
/**
 * Extract relationships from content
 */
function extractRelationships(content, knownEntities // entity name -> entity id
) {
    var _a, _b;
    var relationships = [];
    for (var _i = 0, _c = Object.entries(RELATIONSHIP_PATTERNS); _i < _c.length; _i++) {
        var _d = _c[_i], type = _d[0], patterns = _d[1];
        for (var _e = 0, patterns_1 = patterns; _e < patterns_1.length; _e++) {
            var pattern = patterns_1[_e];
            // Reset regex state
            var regex = new RegExp(pattern.source, pattern.flags);
            var match = void 0;
            while ((match = regex.exec(content)) !== null) {
                var source = (_a = match[1]) === null || _a === void 0 ? void 0 : _a.trim();
                var target = (_b = match[2]) === null || _b === void 0 ? void 0 : _b.trim();
                if (source && target && source.length > 1 && target.length > 1) {
                    // Skip if source equals target
                    if (source.toLowerCase() === target.toLowerCase())
                        continue;
                    // Check if target is a numeric value (for has_target, has_customer)
                    var isNumericValue = /^\$?[\d,]+(?:\/\w+)?$/.test(target);
                    // Calculate confidence based on match quality
                    var confidence = 0.7;
                    // For numeric values, the target becomes the value
                    var finalValue = void 0;
                    var finalTarget = target;
                    if (isNumericValue && (type === 'has_target' || type === 'has_customer')) {
                        finalValue = target;
                        finalTarget = "$".concat(target); // Use numeric as value, create placeholder target
                    }
                    else {
                        // Boost confidence if entities are known
                        if (knownEntities.has(source.toLowerCase()))
                            confidence += 0.1;
                        if (knownEntities.has(target.toLowerCase()))
                            confidence += 0.1;
                    }
                    relationships.push({
                        source: source,
                        target: finalTarget,
                        type: type,
                        value: finalValue,
                        confidence: Math.min(1, confidence),
                        matchedText: match[0]
                    });
                }
            }
        }
    }
    // Deduplicate by source+target+type
    var seen = new Set();
    var unique = [];
    for (var _f = 0, relationships_1 = relationships; _f < relationships_1.length; _f++) {
        var rel = relationships_1[_f];
        var key = "".concat(rel.source.toLowerCase(), "|").concat(rel.target.toLowerCase(), "|").concat(rel.type);
        if (!seen.has(key)) {
            seen.add(key);
            unique.push(rel);
        }
    }
    return unique;
}
/**
 * Extract relationships and resolve to entity IDs
 */
function extractAndResolveRelationships(content, entityResolver) {
    // Build known entities map
    var knownEntities = new Map();
    // We can't easily get all entities here, so we'll use the resolver
    // Extract raw relationships
    var rawRelationships = extractRelationships(content, knownEntities);
    // Resolve to entity IDs
    var resolved = [];
    for (var _i = 0, rawRelationships_1 = rawRelationships; _i < rawRelationships_1.length; _i++) {
        var rel = rawRelationships_1[_i];
        var sourceId = entityResolver(rel.source);
        var targetId = entityResolver(rel.target);
        if (sourceId && targetId) {
            resolved.push({
                source: sourceId,
                target: targetId,
                type: rel.type,
                value: rel.value,
                timestamp: new Date().toISOString(),
                sessionId: '', // Will be set by caller
                confidence: rel.confidence
            });
        }
    }
    return resolved;
}
/**
 * Infer entity type from context
 */
function inferTypeFromContext(content, entityName) {
    var lower = content.toLowerCase();
    var entityLower = entityName.toLowerCase();
    // Check for explicit mentions
    if (entityLower.includes('agent') || lower.includes("".concat(entityLower, " handles"))) {
        return 'person';
    }
    if (lower.includes("".concat(entityLower, " is a")) || lower.includes("".concat(entityLower, " is an"))) {
        var definition = lower.match(new RegExp("".concat(entityLower, " is (?:a|an) ([\\w-]+)")));
        if (definition) {
            var type = definition[1].toLowerCase();
            if (type.includes('tool') || type.includes('system') || type.includes('platform')) {
                return 'project';
            }
        }
    }
    return inferEntityType(entityName);
}
