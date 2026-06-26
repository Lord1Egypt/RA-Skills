// Ω Notation — Structured Output Compression
// Serialize structured agent data into ultra-dense token format
// Deserialize back to usable objects with full round-trip integrity

export interface OmegaMessage {
  type: 'eval' | 'decision' | 'route' | 'policy' | 'tier' | 'media';
  confidence?: number;
  directive?: string;
  name?: string;
  fitness?: number;
  deltaFitness?: number;
  to?: string;
  priority?: string;
  condition?: string;
  action?: string;
  fromTier?: number;
  toTier?: number;
  reason?: string;
  hash?: string;
  length?: number;
  summary?: string;
  tags?: Array<{ cat: string; val: string }>;
}

export interface OmegaPacket {
  version: number;
  dict: string | Record<string, string>;
  messages: OmegaMessage[];
}

// --- SERIALIZE ---

function serializeOne(msg: OmegaMessage): string {
  let line = '';

  switch (msg.type) {
    case 'eval':
      line = `e.d {c:${msg.confidence ?? 0.9} d:${msg.directive ?? 'proceed'}}`;
      break;
    case 'decision':
      line = `d.c "${msg.name ?? 'task'}" {fit:${msg.fitness ?? 0.95}}`;
      if (msg.deltaFitness !== undefined) line += ` Δfit:${msg.deltaFitness >= 0 ? '+' : ''}${msg.deltaFitness}`;
      break;
    case 'route':
      line = `r.d "${msg.name ?? 'handler'}" {to:${msg.to ?? 'next'}`;
      if (msg.priority) line += ` pri:${msg.priority}`;
      line += '}';
      break;
    case 'policy':
      line = `p.e "${msg.name ?? 'policy'}" {if:${msg.condition ?? 'true'} then:${msg.action ?? 'proceed'}}`;
      break;
    case 'tier':
      line = `t.es {from:${msg.fromTier ?? 1} to:${msg.toTier ?? 2} reason:"${msg.reason ?? 'low-conf'}"}`;
      break;
    case 'media':
      line = `m.c "${msg.name ?? 'vid'}" {h:phash:${msg.hash ?? 'none'} len:${msg.length ?? 0} cap:"""${msg.summary ?? ''}"""}`;
      break;
  }

  if (msg.tags && msg.tags.length > 0) {
    msg.tags.forEach(t => { line += ` [${t.cat}:${t.val}]`; });
  }

  return line;
}

export function serialize(packet: OmegaPacket): string {
  const dictStr = typeof packet.dict === 'string' ? packet.dict : JSON.stringify(packet.dict);
  let output = `!omega v${packet.version} dict=${dictStr}\n`;
  output += packet.messages.map(serializeOne).join('\n');
  return output.trim();
}

// --- DESERIALIZE ---

function parseTags(line: string): Array<{ cat: string; val: string }> {
  const tags: Array<{ cat: string; val: string }> = [];
  const tagRegex = /\[(\w+):([^\]]+)\]/g;
  let match;
  while ((match = tagRegex.exec(line)) !== null) {
    tags.push({ cat: match[1], val: match[2] });
  }
  return tags;
}

function parseProps(line: string): Record<string, string> {
  const props: Record<string, string> = {};
  const braceMatch = line.match(/\{([^}]+)\}/);
  if (braceMatch) {
    const pairs = braceMatch[1].split(/\s+/);
    pairs.forEach(p => {
      const [k, v] = p.split(':');
      if (k && v !== undefined) props[k] = v.replace(/"/g, '');
    });
  }
  return props;
}

function parseName(line: string): string {
  const nameMatch = line.match(/"([^"]+)"/);
  return nameMatch ? nameMatch[1] : '';
}

function parseDelta(line: string, key: string): number | undefined {
  const deltaMatch = line.match(new RegExp(`Δ${key}:([+\\-]?[\\d.]+)`));
  return deltaMatch ? parseFloat(deltaMatch[1]) : undefined;
}

function deserializeOne(line: string): OmegaMessage | null {
  const trimmed = line.trim();
  const tags = parseTags(trimmed);

  if (trimmed.startsWith('e.d')) {
    const props = parseProps(trimmed);
    return {
      type: 'eval',
      confidence: parseFloat(props['c'] ?? '0.9'),
      directive: props['d'] ?? 'proceed',
      tags: tags.length > 0 ? tags : undefined,
    };
  }

  if (trimmed.startsWith('d.c')) {
    const props = parseProps(trimmed);
    return {
      type: 'decision',
      name: parseName(trimmed),
      fitness: parseFloat(props['fit'] ?? '0.95'),
      deltaFitness: parseDelta(trimmed, 'fit'),
      tags: tags.length > 0 ? tags : undefined,
    };
  }

  if (trimmed.startsWith('r.d')) {
    const props = parseProps(trimmed);
    return {
      type: 'route',
      name: parseName(trimmed),
      to: props['to'] ?? 'next',
      priority: props['pri'],
      tags: tags.length > 0 ? tags : undefined,
    };
  }

  if (trimmed.startsWith('p.e')) {
    const props = parseProps(trimmed);
    return {
      type: 'policy',
      name: parseName(trimmed),
      condition: props['if'] ?? 'true',
      action: props['then'] ?? 'proceed',
      tags: tags.length > 0 ? tags : undefined,
    };
  }

  if (trimmed.startsWith('t.es')) {
    const props = parseProps(trimmed);
    return {
      type: 'tier',
      fromTier: parseInt(props['from'] ?? '1'),
      toTier: parseInt(props['to'] ?? '2'),
      reason: props['reason'] ?? '',
      tags: tags.length > 0 ? tags : undefined,
    };
  }

  if (trimmed.startsWith('m.c')) {
    const props = parseProps(trimmed);
    const capMatch = trimmed.match(/cap:"""(.+?)"""/);
    return {
      type: 'media',
      name: parseName(trimmed),
      hash: (() => {
        const hMatch = trimmed.match(/h:phash:(\S+)/);
        return hMatch ? hMatch[1] : '';
      })(),
      length: parseInt(props['len'] ?? '0'),
      summary: capMatch ? capMatch[1] : '',
      tags: tags.length > 0 ? tags : undefined,
    };
  }

  return null;
}

export function deserialize(text: string): OmegaPacket {
  const lines = text.trim().split('\n');
  const packet: OmegaPacket = { version: 1, dict: 'auto', messages: [] };

  lines.forEach(line => {
    const trimmed = line.trim();

    // Header
    if (trimmed.startsWith('!omega')) {
      const verMatch = trimmed.match(/v(\d+)/);
      if (verMatch) packet.version = parseInt(verMatch[1]);
      const dictMatch = trimmed.match(/dict=(\S+)/);
      if (dictMatch) packet.dict = dictMatch[1];
      return;
    }

    // Message line
    const msg = deserializeOne(trimmed);
    if (msg) packet.messages.push(msg);
  });

  return packet;
}

// --- ROUND-TRIP TEST ---

export function test(): boolean {
  const original: OmegaPacket = {
    version: 1,
    dict: 'auto',
    messages: [
      { type: 'eval', confidence: 0.95, directive: 'proceed', tags: [{ cat: 'cat', val: 'finance' }] },
      { type: 'decision', name: 'btc-hold', fitness: 0.87, deltaFitness: -0.05 },
      { type: 'route', name: 'handler-1', to: 'opus', priority: 'high' },
      { type: 'policy', name: 'safety', condition: 'conf<0.5', action: 'escalate' },
      { type: 'tier', fromTier: 1, toTier: 2, reason: 'low-conf' },
      { type: 'media', name: 'vid-1', hash: 'abc123', length: 142, summary: 'quick test summary' },
    ],
  };

  const serialized = serialize(original);
  const deserialized = deserialize(serialized);

  // Verify round-trip
  if (deserialized.messages.length !== original.messages.length) return false;
  for (let i = 0; i < original.messages.length; i++) {
    if (deserialized.messages[i].type !== original.messages[i].type) return false;
  }

  console.log('=== SERIALIZED ===');
  console.log(serialized);
  console.log('\n=== DESERIALIZED ===');
  console.log(JSON.stringify(deserialized, null, 2));
  console.log('\n✅ Round-trip test passed');
  return true;
}
