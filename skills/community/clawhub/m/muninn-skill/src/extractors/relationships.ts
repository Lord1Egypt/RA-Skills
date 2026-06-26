/**
 * Relationship Extractor
 * Extracts relationships from memory content using pattern matching
 */

import { RelationshipType } from '../storage/relationship-store.js';

// Pattern definitions for relationship extraction
const RELATIONSHIP_PATTERNS: Record<RelationshipType, RegExp[]> = {
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
  // Co-occurrence relationships (entities mentioned together in same memory)
  co_occurs_with: [],  // Populated dynamically during memory storage, not via pattern matching
};

export interface ExtractedRelationship {
  source: string;
  target: string;
  type: RelationshipType;
  value?: string;
  confidence: number;
  matchedText: string;
}

// Entity type inference based on name patterns
function inferEntityType(name: string): string {
  const lower = name.toLowerCase();
  
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
export function extractRelationships(
  content: string,
  knownEntities: Map<string, string> // entity name -> entity id
): ExtractedRelationship[] {
  const relationships: ExtractedRelationship[] = [];
  
  for (const [type, patterns] of Object.entries(RELATIONSHIP_PATTERNS) as [RelationshipType, RegExp[]][]) {
    for (const pattern of patterns) {
      // Reset regex state
      const regex = new RegExp(pattern.source, pattern.flags);
      
      let match;
      while ((match = regex.exec(content)) !== null) {
        const source = match[1]?.trim();
        const target = match[2]?.trim();
        
        if (source && target && source.length > 1 && target.length > 1) {
          // Skip if source equals target
          if (source.toLowerCase() === target.toLowerCase()) continue;
          
          // Check if target is a numeric value (for has_target, has_customer)
          const isNumericValue = /^\$?[\d,]+(?:\/\w+)?$/.test(target);
          
          // Calculate confidence based on match quality
          let confidence = 0.7;
          
          // For numeric values, the target becomes the value
          let finalValue: string | undefined;
          let finalTarget = target;
          
          if (isNumericValue && (type === 'has_target' || type === 'has_customer')) {
            finalValue = target;
            finalTarget = `$${target}`; // Use numeric as value, create placeholder target
          } else {
            // Boost confidence if entities are known
            if (knownEntities.has(source.toLowerCase())) confidence += 0.1;
            if (knownEntities.has(target.toLowerCase())) confidence += 0.1;
          }
          
          relationships.push({
            source,
            target: finalTarget,
            type,
            value: finalValue,
            confidence: Math.min(1, confidence),
            matchedText: match[0]
          });
        }
      }
    }
  }
  
  // Deduplicate by source+target+type
  const seen = new Set<string>();
  const unique: ExtractedRelationship[] = [];
  
  for (const rel of relationships) {
    const key = `${rel.source.toLowerCase()}|${rel.target.toLowerCase()}|${rel.type}`;
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
export function extractAndResolveRelationships(
  content: string,
  entityResolver: (name: string) => string | null
): Omit<import('../storage/relationship-store.js').Relationship, 'id'>[] {
  // Build known entities map
  const knownEntities = new Map<string, string>();
  // We can't easily get all entities here, so we'll use the resolver
  
  // Extract raw relationships
  const rawRelationships = extractRelationships(content, knownEntities);
  
  // Resolve to entity IDs
  const resolved: Omit<import('../storage/relationship-store.js').Relationship, 'id'>[] = [];
  
  for (const rel of rawRelationships) {
    const sourceId = entityResolver(rel.source);
    const targetId = entityResolver(rel.target);
    
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
export function inferTypeFromContext(content: string, entityName: string): string {
  const lower = content.toLowerCase();
  const entityLower = entityName.toLowerCase();
  
  // Check for explicit mentions
  if (entityLower.includes('agent') || lower.includes(`${entityLower} handles`)) {
    return 'person';
  }
  
  if (lower.includes(`${entityLower} is a`) || lower.includes(`${entityLower} is an`)) {
    const definition = lower.match(new RegExp(`${entityLower} is (?:a|an) ([\\w-]+)`));
    if (definition) {
      const type = definition[1].toLowerCase();
      if (type.includes('tool') || type.includes('system') || type.includes('platform')) {
        return 'project';
      }
    }
  }
  
  return inferEntityType(entityName);
}

export { inferEntityType };
