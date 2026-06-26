// --- Parser ---

// Lines to strip from raw Navigator share text
const JUNK_PATTERNS = [
  /^Verbindung ansehen/i,
  /^https?:\/\//,
  /^Mehr$/i,
  /^Więcej$/i,
  /^More$/i,
  /^\u200f/,  // RTL mark
];

function isJunk(line) {
  const t = line.trim();
  if (!t) return false;
  return JUNK_PATTERNS.some(p => p.test(t));
}

function isTrainHeader(line) {
  const t = line.trim();
  if (!t) return false;
  // Bus RB66, ICE 933, IC 58100, RE3 (3309), S5X, S1, EC 123, etc.
  return /^(Bus\s+\S+|ICE?\s+\d+|EC\s+\d+|(?:RE|RB|IRE)\d*\s+\(\d+\)|S\d*\w*)$/.test(t);
}

export function parseConnection(raw) {
  // Strip junk lines and normalize
  let lines = raw.split('\n').map(l => l.trimEnd()).filter(l => !isJunk(l));

  // Line 1: "From → To"
  const headerLine = lines[0].trim();
  const arrow = headerLine.indexOf('→');
  if (arrow === -1) throw new Error(`Expected "From → To" header, got: ${headerLine}`);
  const from = headerLine.slice(0, arrow).trim();
  const to = headerLine.slice(arrow + 1).trim();

  // Line 2: date — may have train name appended: "05.03.2026  S8"
  const dateLine = lines[1].trim();
  const dateMatch = dateLine.match(/^(\d{1,2}\.\d{2}\.\d{4})/);
  if (!dateMatch) throw new Error(`Expected date on line 2, got: ${dateLine}`);
  const date = convertDate(dateMatch[1]);

  // If date line has a train name appended, inject it as a separate line
  const afterDate = dateLine.slice(dateMatch[0].length).trim();
  let restLines;
  if (afterDate && isTrainHeader(afterDate)) {
    restLines = [afterDate, ...lines.slice(2)];
  } else {
    restLines = lines.slice(2);
  }

  // Split into leg blocks: a new block starts at each train header line
  const blocks = [];
  let current = [];
  for (const line of restLines) {
    const t = line.trim();
    if (!t) {
      // Blank line — if we have content, it might be a separator
      if (current.length) {
        blocks.push(current.join('\n'));
        current = [];
      }
      continue;
    }
    if (isTrainHeader(t) && current.length > 0) {
      // New train header while we have an existing block → flush
      blocks.push(current.join('\n'));
      current = [t];
    } else {
      current.push(t);
    }
  }
  if (current.length) blocks.push(current.join('\n'));

  const legs = blocks.map(block => parseLeg(block.trim()));

  return { date, from, to, legs };
}

export function convertDate(ddmmyyyy) {
  const m = ddmmyyyy.match(/^(\d{1,2})\.(\d{2})\.(\d{4})$/);
  if (!m) throw new Error(`Bad date: ${ddmmyyyy}`);
  return `${m[3]}-${m[2]}-${m[1].padStart(2, '0')}`;
}

export function padTime(t) {
  // "8:45" → "08:45", "0:15" → "00:15", "14:22" → "14:22"
  const [h, m] = t.split(':');
  return `${h.padStart(2, '0')}:${m}`;
}

export function parseTrainHeader(line) {
  // Pattern 1: "Bus RB66" → category=Bus, number=RB66
  let m = line.match(/^Bus\s+(\S+)$/);
  if (m) return { train: `Bus ${m[1]}`, category: 'Bus', number: m[1] };

  // Pattern 2: "ICE 933", "IC 58100" → category=ICE/IC, number=933/58100
  m = line.match(/^(ICE?)\s+(\d+)$/);
  if (m) return { train: `${m[1]} ${m[2]}`, category: m[1], number: m[2] };

  // Pattern 3: "RE3 (3309)", "RE31 (4892)", "RB23 (79745)", "RE22 (57939)"
  // → category=RE/RB, line=RE3/RE31/RB23/RE22, number=3309/4892/79745/57939
  m = line.match(/^((?:RE|RB)\d+)\s+\((\d+)\)$/);
  if (m) {
    const lineName = m[1];
    const cat = lineName.startsWith('RB') ? 'RB' : 'RE';
    return { train: `${lineName} ${m[2]}`, category: cat, line: lineName, number: m[2] };
  }

  // Pattern 4: "S5X", "S1" → category=S, line=S5X/S1, number=S5X/S1
  m = line.match(/^(S\d*\w*)$/);
  if (m) return { train: m[1], category: 'S', line: m[1], number: m[1] };

  throw new Error(`Unknown train header: ${line}`);
}

export function parseStopLine(line) {
  // "Ab 8:45 Koszalin" or "Ab 13:32 Angermünde, Gleis 5"
  // "An 11:04 Szczecin Glowny" or "An 14:22 Berlin Gesundbrunnen, Gleis 6"
  const m = line.match(/^(Ab|An)\s+(\d{1,2}:\d{2})\s+(.+)$/);
  if (!m) return null;
  const type = m[1]; // Ab or An
  const time = padTime(m[2]);
  let station = m[3].trim();
  let platform = undefined;

  // Extract ", Gleis X" suffix
  const gm = station.match(/^(.+),\s*Gleis\s+(.+)$/);
  if (gm) {
    station = gm[1].trim();
    platform = gm[2].trim();
  }

  return { type, time, station, platform };
}

export function parseLeg(block) {
  const lines = block.split('\n').map(l => l.trim()).filter(Boolean);

  // First line: train header
  const header = parseTrainHeader(lines[0]);
  const leg = { ...header };

  let direction;
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];

    // "Nach DIRECTION"
    if (line.startsWith('Nach ')) {
      direction = line.slice(5).trim();
      continue;
    }

    const stop = parseStopLine(line);
    if (!stop) continue;

    if (stop.type === 'Ab') {
      leg.from = stop.station;
      leg.dep = stop.time;
      if (stop.platform) leg.depPlatform = stop.platform;
    } else {
      leg.to = stop.station;
      leg.arr = stop.time;
      if (stop.platform) leg.arrPlatform = stop.platform;
    }
  }

  if (direction) leg.direction = direction;

  // Reorder keys: train, category, [line], number, [direction], from, dep, [depPlatform], to, arr, [arrPlatform]
  const ordered = {};
  ordered.train = leg.train;
  ordered.category = leg.category;
  if (leg.line) ordered.line = leg.line;
  ordered.number = leg.number;
  if (leg.direction) ordered.direction = leg.direction;
  ordered.from = leg.from;
  ordered.dep = leg.dep;
  if (leg.depPlatform) ordered.depPlatform = leg.depPlatform;
  ordered.to = leg.to;
  ordered.arr = leg.arr;
  if (leg.arrPlatform) ordered.arrPlatform = leg.arrPlatform;

  return ordered;
}
