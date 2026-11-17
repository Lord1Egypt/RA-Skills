import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { esc, renderDefinitions, textUnits } from '../shared/utils.mjs';
import { animateAttr, focusEdgeAttrs, focusNodeAttrs, focusNodeTitle, loadDiagramWithBrandMarks, writeDiagram, svgAccessibleText, svgRootAttrs } from '../shared/cli.mjs';
import { throwDiagnosticProblems } from '../shared/diagnostics.mjs';
import {
  asArray,
  isFinitePoint,
} from '../shared/geometry.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const { diagram: network, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'network',
  defaultExample: 'office-network.network.json',
});

const viewBox = network.meta?.viewBox;

const layout = {
  nodeMinW: 110,
  nodeMaxW: 190,
  nodeH: 44,
  labelPadX: 12,
  width: 940,
  height: 620,
  padding: 70,
  minWidth: 960,
};

function measureNode(node) {
  const units = textUnits(node.label);
  const width = Math.min(layout.nodeMaxW, Math.max(layout.nodeMinW, Math.round(units * 6.2 + layout.labelPadX * 2)));
  return { ...node, width, height: layout.nodeH };
}

// ---- Force-directed layout with a fixed seed --------------------------------
// Fruchterman-Reingold spring embedding, seeded deterministically so the same
// JSON always yields the same coordinates (deliver's SHA-256 receipt stays
// meaningful). The geometric quality gates (edge crossing, corridor merge) are
// intentionally not applied to this type: arbitrary topologies cross by
// nature, and the honest trade-off is visual clarity over deterministic
// acceptance. The skill states this explicitly.
function seededRandom(seed) {
  let state = seed >>> 0;
  return () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 4294967296;
  };
}

function forceLayout() {
  const nodes = asArray(network.nodes).map(measureNode);
  const byId = new Map(nodes.map((n) => [n.id, n]));
  const ids = nodes.map((n) => n.id);

  const adjacency = new Map(ids.map((id) => [id, new Set()]));
  for (const link of asArray(network.links)) {
    if (!byId.has(link.from) || !byId.has(link.to) || link.from === link.to) continue;
    adjacency.get(link.from).add(link.to);
    adjacency.get(link.to).add(link.from);
  }

  const random = seededRandom(42);
  const positions = new Map();
  const cx = layout.width / 2;
  const cy = layout.height / 2;
  for (const id of ids) {
    positions.set(id, {
      x: cx + (random() - 0.5) * layout.width * 0.8,
      y: cy + (random() - 0.5) * layout.height * 0.8,
    });
  }

  // Fruchterman-Reingold: repulsive force between all pairs, attractive force
  // along edges, cooling over iterations.
  const k = Math.sqrt((layout.width * layout.height) / ids.length);
  const iterations = 300;
  let temperature = layout.width / 10;
  const displacement = new Map(ids.map((id) => [id, { x: 0, y: 0 }]));

  for (let iter = 0; iter < iterations; iter += 1) {
    for (const id of ids) displacement.get(id).x = 0, displacement.get(id).y = 0;

    // Repulsion between all pairs.
    for (let i = 0; i < ids.length; i += 1) {
      for (let j = i + 1; j < ids.length; j += 1) {
        const a = positions.get(ids[i]);
        const b = positions.get(ids[j]);
        let dx = a.x - b.x;
        let dy = a.y - b.y;
        let distSq = dx * dx + dy * dy;
        if (distSq < 0.01) { dx = random() - 0.5; dy = random() - 0.5; distSq = dx * dx + dy * dy; }
        const dist = Math.sqrt(distSq);
        const force = (k * k) / dist;
        const fx = (dx / dist) * force;
        const fy = (dy / dist) * force;
        displacement.get(ids[i]).x += fx;
        displacement.get(ids[i]).y += fy;
        displacement.get(ids[j]).x -= fx;
        displacement.get(ids[j]).y -= fy;
      }
    }

    // Attraction along edges.
    for (const link of asArray(network.links)) {
      if (!byId.has(link.from) || !byId.has(link.to) || link.from === link.to) continue;
      const a = positions.get(link.from);
      const b = positions.get(link.to);
      const dx = a.x - b.x;
      const dy = a.y - b.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
      const force = (dist * dist) / k;
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;
      displacement.get(link.from).x -= fx;
      displacement.get(link.from).y -= fy;
      displacement.get(link.to).x += fx;
      displacement.get(link.to).y += fy;
    }

    // Apply displacement, bounded by temperature.
    for (const id of ids) {
      const d = displacement.get(id);
      const dist = Math.sqrt(d.x * d.x + d.y * d.y) || 0.01;
      const capped = Math.min(dist, temperature);
      const pos = positions.get(id);
      pos.x += (d.x / dist) * capped;
      pos.y += (d.y / dist) * capped;
      pos.x = Math.max(layout.padding, Math.min(layout.width - layout.padding, pos.x));
      pos.y = Math.max(layout.padding, Math.min(layout.height - layout.padding, pos.y));
    }

    temperature *= 0.95;
  }

  // Normalize into viewBox coordinates with node sizes accounted for.
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const id of ids) {
    const pos = positions.get(id);
    minX = Math.min(minX, pos.x);
    minY = Math.min(minY, pos.y);
    maxX = Math.max(maxX, pos.x);
    maxY = Math.max(maxY, pos.y);
  }
  const spanX = Math.max(1, maxX - minX);
  const spanY = Math.max(1, maxY - minY);
  const scale = Math.min((layout.width - 2 * layout.padding) / spanX, (layout.height - 2 * layout.padding) / spanY);

  const measured = nodes.map((node) => {
    const pos = positions.get(node.id);
    const x = layout.padding + (pos.x - minX) * scale;
    const y = layout.padding + (pos.y - minY) * scale;
    return { ...node, x, y, cx: x + node.width / 2, cy: y + node.height / 2 };
  });

  const maxXNode = Math.max(...measured.map((m) => m.x + m.width));
  const maxYNode = Math.max(...measured.map((m) => m.y + m.height));
  return {
    nodes: measured,
    neededViewBox: [Math.max(layout.minWidth, maxXNode + 40), maxYNode + layout.padding],
  };
}

const { nodes: nodeList, neededViewBox } = forceLayout();
const nodes = new Map(nodeList.map((n) => [n.id, n]));
const effectiveViewBox = viewBox
  ? [Math.max(viewBox[0], neededViewBox[0]), Math.max(viewBox[1], neededViewBox[1])]
  : neededViewBox;

// ---- Link rendering (undirected straight lines) -----------------------------
const linkCache = new Map();

function linkLine(link) {
  const key = [link.from, link.to].sort().join('\u0000');
  if (linkCache.has(key)) return linkCache.get(key);
  const from = nodes.get(link.from);
  const to = nodes.get(link.to);
  const line = { x1: from.cx, y1: from.cy, x2: to.cx, y2: to.cy };
  linkCache.set(key, line);
  return line;
}

// ---- Validation -------------------------------------------------------------
function validateNetwork() {
  const problems = [];
  if (nodes.size !== asArray(network.nodes).length) problems.push('Node ids must be unique.');
  for (const node of nodes.values()) {
    if (!isFinitePoint(node.x, node.y, node.cx, node.cy)) {
      problems.push(`Node "${node.id}" produced non-finite coordinates.`);
    }
  }
  for (const link of asArray(network.links)) {
    if (!nodes.has(link.from)) problems.push(`Link references unknown source "${link.from}".`);
    if (!nodes.has(link.to)) problems.push(`Link references unknown target "${link.to}".`);
  }
  if (problems.length) {
    throwDiagnosticProblems('Network layout validation failed', problems, {
      subject: { diagramType: 'network' },
    });
  }
}

// ---- Render -----------------------------------------------------------------
function kindClass(kind) {
  switch (kind) {
    case 'router': return 'c-cloud';
    case 'switch': return 'c-messagebus';
    case 'firewall': return 'c-security';
    case 'server': return 'c-backend';
    case 'client': return 'c-frontend';
    case 'database': return 'c-database';
    case 'cloud': return 'c-external';
    default: return 'c-frontend';
  }
}

function renderNode(node) {
  const passport = { kind: node.kind || 'server', sublabel: node.note, tag: node.kind || 'server' };
  const cls = kindClass(node.kind);
  return `        <g ${focusNodeAttrs(node.id, node.label, passport, network.meta.locale)}>
          ${focusNodeTitle(node.label, passport)}
          <rect x="${node.x - 4}" y="${node.y - 4}" width="${node.width + 8}" height="${node.height + 8}" rx="8" class="c-mask"/>
          <rect x="${node.x}" y="${node.y}" width="${node.width}" height="${node.height}" rx="10" class="${cls}"${animateAttr(network.meta, 'node', 0)} stroke-width="1.5"/>
          <text x="${node.cx}" y="${node.cy + 3}" font-size="8.5" font-weight="600" class="t-primary" text-anchor="middle">${esc(node.label)}</text>
        </g>`;
}

function renderLink(link, index) {
  const line = linkLine(link);
  const strokeWidth = link.width || (link.variant === 'emphasis' ? 1.8 : 1.2);
  const cls = link.variant === 'emphasis' ? 'a-emphasis' : link.variant === 'security' ? 'a-security' : link.variant === 'dashed' ? 'a-dashed' : 'a-default';
  return `        <line x1="${line.x1}" y1="${line.y1}" x2="${line.x2}" y2="${line.y2}" data-edge-from="${esc(link.from)}" data-edge-to="${esc(link.to)}" data-edge-label="${esc(link.label || '')}" data-edge-id="${esc(link.id || '')}" class="${cls}"${animateAttr(network.meta, 'edge', index)} stroke-width="${strokeWidth}"/>`;
}

function renderLinkLabel(link) {
  if (!link.label) return '';
  const line = linkLine(link);
  const lx = (line.x1 + line.x2) / 2;
  const ly = (line.y1 + line.y2) / 2;
  const labelW = Math.max(30, Math.round(textUnits(link.label) * 4.5 + 10));
  return `        <g data-detail="context">
          <rect x="${lx - labelW / 2}" y="${ly - 9}" width="${labelW}" height="15" rx="3" class="c-mask"/>
          <text x="${lx}" y="${ly + 2}" font-size="7" class="t-muted" text-anchor="middle">${esc(link.label)}</text>
        </g>`;
}

function renderSvg() {
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(network.meta, undefined, 'unverified')}>
${svgAccessibleText(network.meta, 'network')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Links -->
${asArray(network.links).map(renderLink).join('\n')}

        <!-- Nodes -->
${nodeList.map(renderNode).join('\n\n')}

        <!-- Link labels -->
${asArray(network.links).map(renderLinkLabel).filter(Boolean).join('\n')}
      </svg>`;
}

validateNetwork();
writeDiagram({
  outPath,
  template,
  diagramType: 'network',
  meta: network.meta,
  svg: renderSvg(),
  cards: network.cards,
});
