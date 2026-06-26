"use strict";
/**
 * Entity Extractor
 *
 * Extracts named entities with types from text.
 * Pattern-based approach (no LLM needed for speed).
 *
 * Entity types:
 * - person: Names of people
 * - organization: Companies, teams, groups
 * - project: Named projects, products, apps
 * - technology: Programming languages, frameworks, tools
 * - location: Places, cities, countries
 * - event: Named events, meetings, launches
 * - concept: Abstract ideas, methodologies
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
exports.extractEntities = extractEntities;
// ============================================
// KNOWN ENTITIES (Domain Knowledge)
// ============================================
var KNOWN_PEOPLE = [
    // OpenClaw team
    'Phillip', 'Phillip Neho', 'KakāpōHiko', 'KH', 'KakapoHiko',
    'Sammy Clemens', 'Sammy', 'Charlie Babbage', 'Charlie', 'Donna Paulsen', 'Donna', 'Ernie',
    // Common names
    'John', 'Jane', 'Mike', 'Sarah', 'David', 'Emma', 'Tom', 'Alex', 'Chris', 'Taylor',
];
var KNOWN_ORGANIZATIONS = [
    'OpenClaw', 'Elev8Advisory',
    'Google', 'Microsoft', 'Apple', 'Amazon', 'Meta', 'OpenAI', 'Anthropic',
    'GitHub', 'GitLab', 'Stripe', 'Vercel', 'Netlify',
];
var KNOWN_PROJECTS = [
    'Muninn', 'Mission Control', 'NRL Fantasy', 'GigHunter', 'BrandForge',
    'ClawHub', 'Moltbook', 'AgentMail', 'memory system',
];
var KNOWN_TECHNOLOGIES = [
    // Languages
    'TypeScript', 'JavaScript', 'Python', 'Rust', 'Go', 'Java', 'Kotlin', 'Swift',
    'Ruby', 'PHP', 'C#', 'C++', 'C', 'SQL',
    // Frameworks
    'React', 'Vue', 'Angular', 'Svelte', 'Next.js', 'Nuxt', 'SvelteKit',
    'Express', 'FastAPI', 'Django', 'Rails', 'Spring', 'Node.js',
    // Tools
    'Docker', 'Kubernetes', 'K8s', 'Terraform', 'Ansible', 'Jenkins', 'GitHub Actions',
    'npm', 'yarn', 'pnpm', 'pip', 'cargo', 'go mod',
    // Databases
    'PostgreSQL', 'Postgres', 'MySQL', 'MongoDB', 'Redis', 'SQLite', 'DynamoDB',
    // AI/ML
    'Ollama', 'OpenAI', 'Claude', 'GPT', 'LLM', 'LangChain', 'LlamaIndex',
    'embeddings', 'vector database', 'semantic search',
    // Other
    'Git', 'VS Code', 'Vim', 'Emacs', 'Linux', 'Ubuntu', 'macOS', 'Windows',
    'better-sqlite3', 'sqlite3',
];
var KNOWN_LOCATIONS = [
    // Australia
    'Brisbane', 'Sydney', 'Melbourne', 'Perth', 'Adelaide', 'Gold Coast', 'Canberra',
    'Queensland', 'NSW', 'Victoria', 'Australia', 'AEST',
    // Global
    'USA', 'UK', 'Europe', 'Asia', 'America', 'London', 'New York', 'San Francisco',
    'Tokyo', 'Singapore', 'homelab',
];
var KNOWN_EVENTS = [
    'planning session', 'product launch', 'meeting', 'standup', 'retro', 'retrospective',
    'sprint', 'demo', 'workshop', 'webinar', 'conference', 'hackathon',
];
var KNOWN_CONCEPTS = [
    'memory system', 'content router', 'entity extraction', 'semantic search',
    'knowledge graph', 'vector embedding', 'MCP server', 'agent architecture',
    'Australian English', 'machine learning', 'deep learning', 'neural network',
    'natural language processing', 'NLP', 'API', 'REST', 'GraphQL',
];
// ============================================
// PATTERN MATCHERS
// ============================================
// Capitalized words (potential names)
var CAPITALIZED_PATTERN = /\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g;
// CamelCase and PascalCase (potential tech/project names)
// Must have at least 2 actual words, not just a letter
var CAMELCASE_PATTERN = /\b[A-Z][a-z]{2,}[A-Z][a-z]{2,}(?:[A-Z][a-z]{2,})*\b/g;
// Technology patterns
var TECH_PATTERNS = [
    /\b[A-Z][a-z]*\.js\b/g, // React.js, Vue.js, Next.js
    /\b[A-Z][a-z]*\.ts\b/g, // Node.ts (rare)
    /\b[a-z]+-[a-z]+\d*\b/g, // better-sqlite3
];
// Event patterns
var EVENT_PATTERNS = [
    /Q[1-4]\s+\w+\s+(session|planning|review)/gi, // Q1 planning session
    /\w+\s+launch/gi, // product launch
    /(weekly|daily|monthly)\s+\w+/gi, // weekly standup
];
// ============================================
// CONTEXT WORDS (disambiguation)
// ============================================
var PERSON_CONTEXT = ['met', 'spoke', 'talked', 'discussed', 'called', 'emailed', 'said', 'told', 'asked', 'replied'];
var ORG_CONTEXT = ['company', 'team', 'organization', 'at', 'joined', 'left', 'works', 'partner'];
var PROJECT_CONTEXT = ['project', 'app', 'application', 'system', 'platform', 'built', 'developed', 'deployed'];
var TECH_CONTEXT = ['uses', 'using', 'built with', 'framework', 'library', 'language', 'tool', 'database'];
var LOCATION_CONTEXT = ['in', 'at', 'from', 'based', 'located', 'office', 'server'];
var EVENT_CONTEXT = ['meeting', 'session', 'launch', 'conference', 'workshop', 'attended', 'scheduled'];
// ============================================
// MAIN EXTRACTION FUNCTION
// ============================================
function extractEntities(text) {
    var entities = [];
    var found = new Set(); // Track found entities to avoid duplicates
    var lower = text.toLowerCase();
    // 1. Check known entities first (high confidence)
    // Use word boundary matching for single-word entities to avoid substring matches
    // Sort by length (longest first) to avoid substring matches
    var sortedPeople = __spreadArray([], KNOWN_PEOPLE, true).sort(function (a, b) { return b.length - a.length; });
    var sortedOrgs = __spreadArray([], KNOWN_ORGANIZATIONS, true).sort(function (a, b) { return b.length - a.length; });
    var sortedProjects = __spreadArray([], KNOWN_PROJECTS, true).sort(function (a, b) { return b.length - a.length; });
    var sortedTech = __spreadArray([], KNOWN_TECHNOLOGIES, true).sort(function (a, b) { return b.length - a.length; });
    var sortedLocations = __spreadArray([], KNOWN_LOCATIONS, true).sort(function (a, b) { return b.length - a.length; });
    for (var _i = 0, sortedPeople_1 = sortedPeople; _i < sortedPeople_1.length; _i++) {
        var person = sortedPeople_1[_i];
        var regex = new RegExp("\\b".concat(person.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "\\b"), 'i');
        if (regex.test(text) && !found.has(person.toLowerCase())) {
            entities.push(createEntity(person, 'person', 0.95, text));
            found.add(person.toLowerCase());
            // Also mark any contained names (e.g., "Sammy" when "Sammy Clemens" found)
            var parts = person.split(/\s+/);
            for (var _a = 0, parts_1 = parts; _a < parts_1.length; _a++) {
                var part = parts_1[_a];
                if (part.length > 2)
                    found.add(part.toLowerCase());
            }
        }
    }
    for (var _b = 0, sortedOrgs_1 = sortedOrgs; _b < sortedOrgs_1.length; _b++) {
        var org = sortedOrgs_1[_b];
        var regex = new RegExp("\\b".concat(org.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "\\b"), 'i');
        if (regex.test(text) && !found.has(org.toLowerCase())) {
            entities.push(createEntity(org, 'organization', 0.95, text));
            found.add(org.toLowerCase());
        }
    }
    for (var _c = 0, sortedProjects_1 = sortedProjects; _c < sortedProjects_1.length; _c++) {
        var project = sortedProjects_1[_c];
        var regex = new RegExp("\\b".concat(project.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "\\b"), 'i');
        if (regex.test(text) && !found.has(project.toLowerCase())) {
            entities.push(createEntity(project, 'project', 0.95, text));
            found.add(project.toLowerCase());
        }
    }
    for (var _d = 0, sortedTech_1 = sortedTech; _d < sortedTech_1.length; _d++) {
        var tech = sortedTech_1[_d];
        var regex = new RegExp("\\b".concat(tech.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "\\b"), 'i');
        if (regex.test(text) && !found.has(tech.toLowerCase())) {
            entities.push(createEntity(tech, 'technology', 0.95, text));
            found.add(tech.toLowerCase());
        }
    }
    for (var _e = 0, sortedLocations_1 = sortedLocations; _e < sortedLocations_1.length; _e++) {
        var location_1 = sortedLocations_1[_e];
        var regex = new RegExp("\\b".concat(location_1.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "\\b"), 'i');
        if (regex.test(text) && !found.has(location_1.toLowerCase())) {
            entities.push(createEntity(location_1, 'location', 0.95, text));
            found.add(location_1.toLowerCase());
        }
    }
    // 2. Extract events (pattern-based) - longest first
    var sortedEvents = __spreadArray([], KNOWN_EVENTS, true).sort(function (a, b) { return b.length - a.length; });
    for (var _f = 0, EVENT_PATTERNS_1 = EVENT_PATTERNS; _f < EVENT_PATTERNS_1.length; _f++) {
        var pattern = EVENT_PATTERNS_1[_f];
        var matches = text.match(pattern) || [];
        for (var _g = 0, matches_1 = matches; _g < matches_1.length; _g++) {
            var match = matches_1[_g];
            if (!found.has(match.toLowerCase())) {
                entities.push(createEntity(match, 'event', 0.85, text));
                found.add(match.toLowerCase());
            }
        }
    }
    for (var _h = 0, sortedEvents_1 = sortedEvents; _h < sortedEvents_1.length; _h++) {
        var event_1 = sortedEvents_1[_h];
        var regex = new RegExp("\\b".concat(event_1.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "\\b"), 'i');
        if (regex.test(text) && !found.has(event_1.toLowerCase())) {
            entities.push(createEntity(event_1, 'event', 0.85, text));
            found.add(event_1.toLowerCase());
        }
    }
    // 3. Extract concepts (pattern-based) - longest first
    var sortedConcepts = __spreadArray([], KNOWN_CONCEPTS, true).sort(function (a, b) { return b.length - a.length; });
    for (var _j = 0, sortedConcepts_1 = sortedConcepts; _j < sortedConcepts_1.length; _j++) {
        var concept = sortedConcepts_1[_j];
        var regex = new RegExp("\\b".concat(concept.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "\\b"), 'i');
        if (regex.test(text) && !found.has(concept.toLowerCase())) {
            entities.push(createEntity(concept, 'concept', 0.8, text));
            found.add(concept.toLowerCase());
        }
    }
    // 4. Extract CamelCase/PascalCase (potential tech/project names) - AFTER known entities
    var camelCase = text.match(CAMELCASE_PATTERN) || [];
    for (var _k = 0, camelCase_1 = camelCase; _k < camelCase_1.length; _k++) {
        var word = camelCase_1[_k];
        if (found.has(word.toLowerCase()))
            continue;
        entities.push(createEntity(word, 'technology', 0.7, text));
        found.add(word.toLowerCase());
    }
    // 5. Extract tech patterns (.js, etc.)
    for (var _l = 0, TECH_PATTERNS_1 = TECH_PATTERNS; _l < TECH_PATTERNS_1.length; _l++) {
        var pattern = TECH_PATTERNS_1[_l];
        var matches = text.match(pattern) || [];
        for (var _m = 0, matches_2 = matches; _m < matches_2.length; _m++) {
            var match = matches_2[_m];
            if (!found.has(match.toLowerCase())) {
                entities.push(createEntity(match, 'technology', 0.8, text));
                found.add(match.toLowerCase());
            }
        }
    }
    // 6. Extract capitalized words (potential names) - ONLY if not already found
    // This is the lowest confidence, so we're very conservative
    var capitalized = text.match(CAPITALIZED_PATTERN) || [];
    var _loop_1 = function (word) {
        // Skip if already found (handles "Sammy" vs "Sammy Clemens" case)
        if (found.has(word.toLowerCase()))
            return "continue";
        // Skip common words
        var commonWords = ['I', 'The', 'A', 'An', 'This', 'That', 'It', 'We', 'They', 'You',
            'He', 'She', 'But', 'However', 'When', 'Where', 'Why', 'How', 'What', 'If', 'Then',
            'Yesterday', 'Today', 'Tomorrow', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday', 'First', 'Second', 'Third', 'Finally', 'Last', 'Next'];
        if (commonWords.includes(word))
            return "continue";
        // Skip single words that are part of a known multi-word entity
        var isPartOfKnown = KNOWN_PEOPLE.some(function (p) { return p.toLowerCase().includes(word.toLowerCase()) && p !== word; }) ||
            KNOWN_ORGANIZATIONS.some(function (o) { return o.toLowerCase().includes(word.toLowerCase()) && o !== word; }) ||
            KNOWN_PROJECTS.some(function (p) { return p.toLowerCase().includes(word.toLowerCase()) && p !== word; });
        if (isPartOfKnown)
            return "continue";
        // Skip if looks like it's preceded by a time word (e.g., "Yesterday Charlie" shouldn't be a project)
        var wordIndex = lower.indexOf(word.toLowerCase());
        var precedingWords = lower.slice(Math.max(0, wordIndex - 15), wordIndex).trim().split(/\s+/);
        var timeWords = ['yesterday', 'today', 'tomorrow', 'last', 'next', 'this', 'previous'];
        if (precedingWords.some(function (w) { return timeWords.includes(w); }))
            return "continue";
        // Only infer type from context - don't guess
        var type = inferTypeFromContext(word, text);
        if (type) {
            entities.push(createEntity(word, type, 0.5, text));
            found.add(word.toLowerCase());
        }
    };
    for (var _o = 0, capitalized_1 = capitalized; _o < capitalized_1.length; _o++) {
        var word = capitalized_1[_o];
        _loop_1(word);
    }
    return entities;
}
// ============================================
// HELPER FUNCTIONS
// ============================================
function createEntity(text, type, confidence, fullText) {
    // Extract context (surrounding words)
    var index = fullText.toLowerCase().indexOf(text.toLowerCase());
    var start = Math.max(0, index - 20);
    var end = Math.min(fullText.length, index + text.length + 20);
    var context = fullText.slice(start, end);
    return { text: text, type: type, confidence: confidence, context: context };
}
function inferTypeFromContext(word, text) {
    var lower = text.toLowerCase();
    var wordLower = word.toLowerCase();
    var wordIndex = lower.indexOf(wordLower);
    // Get context around the word
    var contextStart = Math.max(0, wordIndex - 50);
    var contextEnd = Math.min(lower.length, wordIndex + word.length + 50);
    var context = lower.slice(contextStart, contextEnd);
    // Check for person context
    if (PERSON_CONTEXT.some(function (c) { return context.includes(c); })) {
        // But also check if it looks like a name (capitalized, not a common noun)
        if (/^[A-Z][a-z]+$/.test(word)) {
            return 'person';
        }
    }
    // Check for organization context
    if (ORG_CONTEXT.some(function (c) { return context.includes(c + ' ' + wordLower); })) {
        return 'organization';
    }
    // Check for project context
    if (PROJECT_CONTEXT.some(function (c) { return context.includes(c); })) {
        return 'project';
    }
    // Check for technology context
    if (TECH_CONTEXT.some(function (c) { return context.includes(c); })) {
        return 'technology';
    }
    // Check for location context
    if (LOCATION_CONTEXT.some(function (c) { return context.includes(c + ' ' + wordLower); })) {
        return 'location';
    }
    // Default: if capitalized and looks like a name, guess person
    if (/^[A-Z][a-z]+$/.test(word) && word.length > 2) {
        return 'person';
    }
    return null; // Skip if can't determine
}
