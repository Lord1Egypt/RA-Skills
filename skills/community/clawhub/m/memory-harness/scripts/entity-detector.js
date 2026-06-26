/**
 * Entity Detector
 * 
 * Detects known entities in user input.
 * Maps aliases to canonical names.
 */

// Known entities and their aliases
const KNOWN_ENTITIES = [
  'ClawHub', 'clawhub',
  'OpenClaw', 'openclaw',
  'Agent-OS', 'agent-os',
  'ByteRover', 'byterover',
  'MISO', 'miso',
  'BOSS-memory-loop', 'boss-memory-loop',
  'Obsidian', 'obsidian',
  'Telegram', 'telegram',
  'Gateway', 'gateway',
];

const ENTITY_ALIASES = {
  'ClawHub': ['clawhub', 'claw hub'],
  'OpenClaw': ['openclaw', 'open claw'],
  'Agent-OS': ['agent-os', 'agentos', 'agent os'],
  'ByteRover': ['byterover', 'byte rover', 'brv'],
};

/**
 * Detect known entities in input
 * @param {string} input - User input
 * @returns {Object} Detection result
 */
function detectEntities(input) {
  const trimmedInput = input.trim();
  const entities = [];
  
  for (const entity of KNOWN_ENTITIES) {
    if (trimmedInput.toLowerCase().includes(entity.toLowerCase())) {
      entities.push(entity);
    }
  }
  
  // Map aliases to canonical names
  const canonicalMap = new Map();
  for (const [canonical, aliases] of Object.entries(ENTITY_ALIASES)) {
    for (const alias of aliases) {
      canonicalMap.set(alias.toLowerCase(), canonical);
    }
    canonicalMap.set(canonical.toLowerCase(), canonical);
  }
  
  return {
    detected: entities.length > 0,
    entities: [...new Set(entities)],
    canonicalNames: canonicalMap,
  };
}

function addEntity(name, aliases = []) {
  KNOWN_ENTITIES.push(name);
  ENTITY_ALIASES[name] = aliases;
}

if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: node entity-detector.js "user input"');
    process.exit(1);
  }
  console.log(JSON.stringify(detectEntities(input), null, 2));
}

module.exports = { detectEntities, addEntity, KNOWN_ENTITIES, ENTITY_ALIASES };
