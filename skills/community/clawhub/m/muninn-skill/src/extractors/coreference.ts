/**
 * Coreference Resolution
 * 
 * Rule-based pronoun resolution for multi-hop queries.
 * Maps pronouns (she/her/he/him/they/them) to their antecedents
 * based on recent entity mentions in the text.
 * 
 * Based on: Muninn Multi-Hop Improvements Spec (2026-03-03)
 */

export interface CoreferenceResolution {
  pronoun: string;
  antecedent: string;
  position: number;
  replaced: boolean;
}

export interface CoreferenceResult {
  resolvedText: string;
  resolutions: CoreferenceResolution[];
}

/**
 * Gender and number pronoun mappings
 * Maps pronouns to potential antecedent categories
 */
const PRONOUN_MAP: Record<string, string[]> = {
  // Female singular
  'she': ['Caroline', 'Sarah', 'Jane', 'Hedy', 'Sammy', 'Donna'],
  'her': ['Caroline', 'Sarah', 'Jane', 'Hedy', 'Sammy', 'Donna'],
  'hers': ['Caroline', 'Sarah', 'Jane', 'Hedy', 'Sammy', 'Donna'],
  'herself': ['Caroline', 'Sarah', 'Jane', 'Hedy', 'Sammy', 'Donna'],
  
  // Male singular
  'he': ['Phillip', 'Charlie', 'David', 'John', 'KH', 'Melvil', 'Ernie'],
  'him': ['Phillip', 'Charlie', 'David', 'John', 'KH', 'Melvil', 'Ernie'],
  'his': ['Phillip', 'Charlie', 'David', 'John', 'KH', 'Melvil', 'Ernie'],
  'himself': ['Phillip', 'Charlie', 'David', 'John', 'KH', 'Melvil', 'Ernie'],
  
  // Neutral singular
  'they': ['team', 'group', 'organization', 'company'],
  'them': ['team', 'group', 'organization', 'company'],
  'their': ['team', 'group', 'organization', 'company'],
  'themselves': ['team', 'group', 'organization', 'company'],
  
  // Demonstrative
  'this': [],
  'that': [],
  'these': [],
  'those': [],
  
  // Relative
  'who': [],
  'whom': [],
  'which': [],
};

/**
 * Common verbs that establish entity identity
 */
const IDENTITY_VERBS = new Set([
  'is', 'are', 'was', 'were', 'be', 'been', 'being',
  'is_called', 'is_named', 'goes_by', 'refers_to'
]);

/**
 * Resolve coreferences in text using rule-based approach
 * 
 * Algorithm:
 * 1. Split text into sentences
 * 2. Track recent entities in context
 * 3. When pronoun found, match to most recent compatible entity
 * 4. Replace pronoun with antecedent if match found
 * 
 * @param text - Input text to resolve
 * @param knownEntities - Map of lowercase entity name -> entity name
 * @returns Resolved text and list of resolutions made
 */
export function resolveCoreferences(
  text: string,
  knownEntities: Map<string, string>
): CoreferenceResult {
  const resolutions: CoreferenceResolution[] = [];
  let resolvedText = text;
  
  // If no known entities, just return original text
  if (knownEntities.size === 0) {
    return { resolvedText, resolutions };
  }
  
  // Split into sentences to track context
  const sentences = text.split(/[.!?]+/);
  
  // Track most recent entities by gender/number
  const recentEntities: {
    female: string[];
    male: string[];
    neutral: string[];
  } = {
    female: [],
    male: [],
    neutral: []
  };
  
  // Process each sentence
  for (let sentenceIdx = 0; sentenceIdx < sentences.length; sentenceIdx++) {
    const sentence = sentences[sentenceIdx];
    if (!sentence.trim()) continue;
    
    // Extract words (simple tokenization)
    const words = sentence.split(/\s+/);
    
    // First pass: find known entities in this sentence and update recent
    for (const word of words) {
      const cleanWord = word.toLowerCase().replace(/[^a-z]/g, '');
      
      // Check if this word is a known entity
      if (knownEntities.has(cleanWord)) {
        const entityName = knownEntities.get(cleanWord)!;
        
        // Determine gender
        const entityLower = entityName.toLowerCase();
        
        // Check female names
        if (PRONOUN_MAP['she'].some(n => n.toLowerCase() === entityLower)) {
          recentEntities.female = [entityName, ...recentEntities.female].slice(0, 3);
        }
        // Check male names  
        else if (PRONOUN_MAP['he'].some(n => n.toLowerCase() === entityLower)) {
          recentEntities.male = [entityName, ...recentEntities.male].slice(0, 3);
        }
        // Neutral
        else {
          recentEntities.neutral = [entityName, ...recentEntities.neutral].slice(0, 3);
        }
      }
    }
    
    // Second pass: resolve pronouns
    for (let i = 0; i < words.length; i++) {
      const word = words[i];
      const cleanWord = word.toLowerCase().replace(/[^a-z]/g, '');
      
      // Skip if not a pronoun we handle
      if (!PRONOUN_MAP[cleanWord]) continue;
      
      // Get the appropriate recent entity list
      let antecedent: string | null = null;
      
      if (['she', 'her', 'hers', 'herself'].includes(cleanWord)) {
        // Female pronoun - look for female entities
        if (recentEntities.female.length > 0) {
          antecedent = recentEntities.female[0];
        }
      } else if (['he', 'him', 'his', 'himself'].includes(cleanWord)) {
        // Male pronoun - look for male entities
        if (recentEntities.male.length > 0) {
          antecedent = recentEntities.male[0];
        }
      } else if (['they', 'them', 'their', 'themselves'].includes(cleanWord)) {
        // Neutral/plural - look for neutral entities first, then any
        if (recentEntities.neutral.length > 0) {
          antecedent = recentEntities.neutral[0];
        } else if (recentEntities.female.length > 0) {
          antecedent = recentEntities.female[0];
        } else if (recentEntities.male.length > 0) {
          antecedent = recentEntities.male[0];
        }
      }
      
      // If we found an antecedent, replace the pronoun
      if (antecedent) {
        // Create regex to replace this specific occurrence
        // Use word boundary to avoid partial matches
        const regex = new RegExp(`\\b${escapeRegex(word)}`, 'g');
        
        // Check if already replaced (avoid double-replacement)
        const position = resolvedText.indexOf(word);
        
        if (position !== -1 && !resolutions.some(r => r.position === position && r.pronoun === cleanWord)) {
          resolvedText = resolvedText.replace(regex, antecedent);
          
          resolutions.push({
            pronoun: word,
            antecedent,
            position,
            replaced: true
          });
        }
      }
    }
  }
  
  return { resolvedText, resolutions };
}

/**
 * Resolve coreferences from extracted entities (simpler version)
 * 
 * @param text - Input text
 * @param entities - Array of entity names found in text
 * @returns Resolved text
 */
export function resolveCoreferencesFromEntities(
  text: string,
  entities: string[]
): CoreferenceResult {
  // Build known entities map
  const knownEntities = new Map<string, string>();
  
  for (const entity of entities) {
    knownEntities.set(entity.toLowerCase(), entity);
    
    // Also add aliases if entity has them
    const aliasMatch = entity.match(/\(aka ([^)]+)\)/i);
    if (aliasMatch) {
      knownEntities.set(aliasMatch[1].toLowerCase(), entity);
    }
  }
  
  return resolveCoreferences(text, knownEntities);
}

/**
 * Extract potential antecedents from query context
 * 
 * @param query - User query
 * @param entityNames - Known entity names
 * @returns Map of potential antecedents
 */
export function extractAntecedentsFromQuery(
  query: string,
  entityNames: string[]
): Map<string, string> {
  const antecedents = new Map<string, string>();
  
  for (const entity of entityNames) {
    if (query.toLowerCase().includes(entity.toLowerCase())) {
      antecedents.set(entity.toLowerCase(), entity);
    }
  }
  
  return antecedents;
}

/**
 * Check if text likely contains coreferences
 * 
 * @param text - Text to check
 * @returns True if likely contains pronouns needing resolution
 */
export function likelyHasCoreferences(text: string): boolean {
  const pronouns = ['she', 'her', 'he', 'him', 'they', 'them', 'this', 'that'];
  const lower = text.toLowerCase();
  
  return pronouns.some(p => {
    const regex = new RegExp(`\\b${p}\\b`, 'i');
    return regex.test(lower);
  });
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Escape special regex characters in a string
 */
function escapeRegex(string: string): string {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Get pronoun category
 */
function getPronounCategory(pronoun: string): 'female' | 'male' | 'neutral' | 'other' {
  if (['she', 'her', 'hers', 'herself'].includes(pronoun.toLowerCase())) {
    return 'female';
  }
  if (['he', 'him', 'his', 'himself'].includes(pronoun.toLowerCase())) {
    return 'male';
  }
  if (['they', 'them', 'their', 'themselves'].includes(pronoun.toLowerCase())) {
    return 'neutral';
  }
  return 'other';
}

// ============================================================================
// EXPORTS
// ============================================================================

export {
  PRONOUN_MAP,
  IDENTITY_VERBS,
  getPronounCategory,
  escapeRegex
};
