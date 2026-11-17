import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { esc, renderDefinitions, textUnits } from '../shared/utils.mjs';
import { animateAttr, focusEdgeAttrs, focusNodeAttrs, focusNodeTitle, loadDiagramWithBrandMarks, writeDiagram, svgAccessibleText, svgRootAttrs } from '../shared/cli.mjs';
import { throwDiagnosticProblems } from '../shared/diagnostics.mjs';
import { translateMessage as i18nText } from '../shared/i18n.mjs';
import {
  asArray,
  isFinitePoint,
  rectsOverlap,
  anchor,
  automaticPortSpread,
  defaultFromSide,
  defaultToSide,
  chosenSide,
  polylinePath,
  routePointsValue,
  labelPoint,
  arrowClassMap,
  variantAccent,
} from '../shared/geometry.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const { diagram: flow, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'flowchart',
  defaultExample: 'signup-flow.flowchart.json',
});

const viewBox = flow.meta?.viewBox;

const layout = {
  nodeMinW: 110,
  nodeMaxW: 190,
  nodeH: 48,
  decisionPad: 16,
  labelPadX: 12,
  colGap: 70,
  rowGap: 56,
  originX: 60,
  originY: 48,
  bottomPad: 40,
};

function measureNode(node) {
  const units = textUnits(node.label);
  const baseW = Math.min(layout.nodeMaxW, Math.max(layout.nodeMinW, Math.round(units * 6.2 + layout.labelPadX * 2)));
  // Decision diamonds need extra horizontal room for the four-point shape.
  const width = node.shape === 'decision' ? baseW + layout.decisionPad * 2 : baseW;
  const height = node.shape === 'decision' ? layout.nodeH + layout.decisionPad : layout.nodeH;
  return { ...node, width, height };
}

// ---- Layered DAG layout (shared with er/dependency) -------------------------
function orderByBarycenter(ids, weightOf) {
  return ids
    .map((id, index) => ({ id, index, weight: weightOf(id) }))
    .sort((a, b) => a.weight - b.weight || a.index - b.index)
    .map((entry) => entry.id);
}

function layeredLayout() {
  const nodes = asArray(flow.nodes).map(measureNode);
  const byId = new Map(nodes.map((n) => [n.id, n]));
  const ids = nodes.map((n) => n.id);

  const outgoing = new Map(ids.map((id) => [id, new Set()]));
  const incoming = new Map(ids.map((id) => [id, new Set()]));
  for (const edge of asArray(flow.edges)) {
    if (!byId.has(edge.from) || !byId.has(edge.to) || edge.from === edge.to) continue;
    outgoing.get(edge.from).add(edge.to);
    incoming.get(edge.to).add(edge.from);
  }

  const indegree = new Map([...incoming].map(([id, targets]) => [id, targets.size]));
  const layerOf = new Map();
  let frontier = ids.filter((id) => indegree.get(id) === 0).sort();
  let level = 0;
  const placed = new Set();
  while (frontier.length) {
    const next = [];
    for (const id of frontier) {
      if (placed.has(id)) continue;
      placed.add(id);
      layerOf.set(id, level);
      for (const target of [...outgoing.get(id)].sort()) {
        indegree.set(target, indegree.get(target) - 1);
        if (indegree.get(target) === 0) next.push(target);
      }
    }
    frontier = [...new Set(next)].sort();
    level += 1;
  }
  for (const id of ids) {
    if (!placed.has(id)) { layerOf.set(id, level); placed.add(id); level += 1; }
  }

  const layerCount = Math.max(0, ...layerOf.values()) + 1;
  const layers = Array.from({ length: layerCount }, () => []);
  for (const id of ids) layers[layerOf.get(id)].push(id);

  for (let pass = 0; pass < 4; pass += 1) {
    for (let layerIndex = 0; layerIndex < layerCount - 1; layerIndex += 1) {
      const indexAbove = new Map(layers[layerIndex].map((id, i) => [id, i]));
      layers[layerIndex + 1] = orderByBarycenter(layers[layerIndex + 1], (id) => {
        const parents = [...incoming.get(id)].filter((p) => indexAbove.has(p));
        return parents.length ? parents.reduce((sum, p) => sum + indexAbove.get(p), 0) / parents.length : Number.POSITIVE_INFINITY;
      });
    }
    for (let layerIndex = layerCount - 1; layerIndex > 0; layerIndex -= 1) {
      const indexBelow = new Map(layers[layerIndex].map((id, i) => [id, i]));
      layers[layerIndex - 1] = orderByBarycenter(layers[layerIndex - 1], (id) => {
        const children = [...outgoing.get(id)].filter((c) => indexBelow.has(c));
        return children.length ? children.reduce((sum, c) => sum + indexBelow.get(c), 0) / children.length : Number.POSITIVE_INFINITY;
      });
    }
  }

  const layerMaxHeights = layers.map((layerIds) => Math.max(...layerIds.map((id) => byId.get(id).height)));
  const layerWidths = layers.map((layerIds) => layerIds.reduce((sum, id) => sum + byId.get(id).width, 0)
    + Math.max(0, layerIds.length - 1) * layout.colGap);
  const graphWidth = Math.max(...layerWidths);
  const layerYs = [];
  let cursorY = layout.originY;
  for (let i = 0; i < layerCount; i += 1) {
    layerYs.push(cursorY);
    cursorY += layerMaxHeights[i] + layout.rowGap;
  }

  const positions = new Map();
  layers.forEach((layerIds, layerIndex) => {
    const layerY = layerYs[layerIndex];
    const layerHeight = layerMaxHeights[layerIndex];
    let cursorX = layout.originX + (graphWidth - layerWidths[layerIndex]) / 2;
    for (const id of layerIds) {
      const node = byId.get(id);
      const y = layerY + (layerHeight - node.height) / 2;
      positions.set(id, { x: cursorX, y });
      cursorX += node.width + layout.colGap;
    }
  });

  const measured = nodes.map((node) => {
    const { x, y } = positions.get(node.id);
    return { ...node, x, y, cx: x + node.width / 2, cy: y + node.height / 2 };
  });
  const maxX = Math.max(...measured.map((m) => m.x + m.width));
  const maxY = Math.max(...measured.map((m) => m.y + m.height));
  const minWidth = 960;
  return { nodes: measured, neededViewBox: [Math.max(minWidth, maxX + 40), maxY + layout.bottomPad] };
}

const { nodes: nodeList, neededViewBox } = layeredLayout();
const nodes = new Map(nodeList.map((n) => [n.id, n]));
const effectiveViewBox = viewBox
  ? [Math.max(viewBox[0], neededViewBox[0]), Math.max(viewBox[1], neededViewBox[1])]
  : neededViewBox;

// ---- Edge routing (shared box-and-arrow engine) -----------------------------
function edgeSides(edge) {
  const from = nodes.get(edge.from);
  const to = nodes.get(edge.to);
  return {
    fromSide: chosenSide(edge.fromSide, defaultFromSide(from, to)),
    toSide: chosenSide(edge.toSide, defaultToSide(from, to)),
  };
}

const automaticPorts = automaticPortSpread(flow.edges, nodes, {
  sideFor: (edge, endpoint) => edgeSides(edge)[endpoint === 'source' ? 'fromSide' : 'toSide'],
});

function routeVia(edge, from, to, start, end) {
  if (edge.via) return edge.via;
  switch (edge.route || 'auto') {
    case 'straight':
      return [];
    case 'vertical-channel': {
      const x = edge.channelX ?? start[0] + (end[0] > start[0] ? 44 : -44);
      return [[x, start[1]], [x, end[1]]];
    }
    case 'bottom-channel': {
      const y = edge.channelY ?? Math.max(from.y + from.height, to.y + to.height) + 26;
      return [[start[0], y], [end[0], y]];
    }
    case 'top-channel': {
      const y = edge.channelY ?? Math.min(from.y, to.y) - 24;
      return [[start[0], y], [end[0], y]];
    }
    case 'auto':
    default: {
      if (Math.abs(start[1] - end[1]) < 4) return [];
      const midX = start[0] + (end[0] - start[0]) / 2;
      return [[midX, start[1]], [midX, end[1]]];
    }
  }
}

const pathCache = new Map();

function pathFor(edge) {
  if (pathCache.has(edge)) return pathCache.get(edge);
  const from = nodes.get(edge.from);
  const to = nodes.get(edge.to);
  const ports = automaticPorts.get(edge);
  const { fromSide, toSide } = edgeSides(edge);
  const start = ports?.from || anchor(from, fromSide);
  const end = ports?.to || anchor(to, toSide);
  const rawPoints = [start, ...routeVia(edge, from, to, start, end), end];
  const points = [];
  for (const p of rawPoints) {
    const prev = points.at(-1);
    if (!prev || Math.abs(p[0] - prev[0]) > 0.0001 || Math.abs(p[1] - prev[1]) > 0.0001) {
      points.push(p);
    }
  }
  if (points.length < 2) points.push(end);
  const routed = { d: polylinePath(points), points };
  pathCache.set(edge, routed);
  return routed;
}

// ---- Validation -------------------------------------------------------------
function validateFlowchart() {
  const problems = [];
  if (nodes.size !== asArray(flow.nodes).length) problems.push('Node ids must be unique.');
  for (const node of nodes.values()) {
    if (!isFinitePoint(node.x, node.y, node.cx, node.cy)) {
      problems.push(`Node "${node.id}" produced non-finite coordinates.`);
    }
  }
  for (let i = 0; i < nodeList.length; i += 1) {
    for (let j = i + 1; j < nodeList.length; j += 1) {
      if (rectsOverlap(nodeList[i], nodeList[j], 10)) {
        problems.push(`Nodes "${nodeList[i].id}" and "${nodeList[j].id}" are less than 10px apart.`);
      }
    }
  }
  for (const edge of asArray(flow.edges)) {
    if (!nodes.has(edge.from)) problems.push(`Edge references unknown source "${edge.from}".`);
    if (!nodes.has(edge.to)) problems.push(`Edge references unknown target "${edge.to}".`);
  }
  if (problems.length) {
    throwDiagnosticProblems('Flowchart layout validation failed', problems, {
      subject: { diagramType: 'flowchart' },
    });
  }
}

// ---- Render (shape-aware) ---------------------------------------------------
function renderShape(node, cls) {
  const { x, y, width, height } = node;
  const rx = node.shape === 'start' || node.shape === 'end' ? height / 2 : 6;
  switch (node.shape) {
    case 'decision': {
      const halfW = width / 2;
      const halfH = height / 2;
      const points = `${node.cx},${y} ${x + width},${node.cy} ${node.cx},${y + height} ${x},${node.cy}`;
      return `<polygon points="${points}" class="${cls}"${animateAttr(flow.meta, 'node', 0)} stroke-width="1.5"/>`;
    }
    case 'io': {
      const skew = 16;
      const points = `${x + skew},${y} ${x + width},${y} ${x + width - skew},${y + height} ${x},${y + height}`;
      return `<polygon points="${points}" class="${cls}"${animateAttr(flow.meta, 'node', 0)} stroke-width="1.5"/>`;
    }
    default: {
      return `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="${rx}" class="${cls}"${animateAttr(flow.meta, 'node', 0)} stroke-width="1.5"/>`;
    }
  }
}

function shapeClass(shape) {
  switch (shape) {
    case 'start': return 'c-database';
    case 'end': return 'c-security';
    case 'decision': return 'c-cloud';
    case 'io': return 'c-messagebus';
    default: return 'c-frontend';
  }
}

function renderNode(node) {
  const passport = { kind: node.shape, sublabel: node.note, tag: node.shape };
  const cls = shapeClass(node.shape);
  const mask = `<rect x="${node.x - 4}" y="${node.y - 4}" width="${node.width + 8}" height="${node.height + 8}" rx="8" class="c-mask"/>`;
  return `        <g ${focusNodeAttrs(node.id, node.label, passport, flow.meta.locale)}>
          ${focusNodeTitle(node.label, passport)}
          ${mask}
          ${renderShape(node, cls)}
          <text x="${node.cx}" y="${node.cy + 3}" font-size="8.5" font-weight="600" class="t-primary" text-anchor="middle">${esc(node.label)}</text>
        </g>`;
}

function renderEdge(edge, index) {
  const [cls, marker] = arrowClassMap[edge.variant || 'default'] || arrowClassMap.default;
  const routed = pathFor(edge);
  const strokeWidth = edge.width || (edge.variant === 'emphasis' ? 1.8 : 1.4);
  return `        <g>
          <path ${focusEdgeAttrs(edge.from, edge.to, edge.label || '', index, edge.id)} data-composition-points="${routePointsValue(routed.points)}" d="${routed.d}" class="${cls}"${animateAttr(flow.meta, 'edge', index)} stroke-width="${strokeWidth}" marker-end="url(#${marker})"/>
        </g>`;
}

function renderEdgeLabel(edge, index) {
  if (!edge.label) return '';
  const routed = pathFor(edge);
  const [lx, ly] = labelPoint(edge, routed.points);
  const labelW = Math.max(34, Math.round(textUnits(edge.label) * 4.9 + 12));
  return `        <g data-detail="context" ${focusEdgeAttrs(edge.from, edge.to, edge.label, index, edge.id)}>
          <rect x="${lx - labelW / 2}" y="${ly - 9}" width="${labelW}" height="16" rx="4" class="c-mask"/>
          <text x="${lx}" y="${ly + 3}" class="${variantAccent(edge.variant)}" font-size="8" text-anchor="middle">${esc(edge.label)}</text>
        </g>`;
}

function renderSvg() {
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(flow.meta)}>
${svgAccessibleText(flow.meta, 'flowchart')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Edges -->
${asArray(flow.edges).map(renderEdge).join('\n')}

        <!-- Nodes -->
${nodeList.map(renderNode).join('\n\n')}

        <!-- Edge labels -->
${asArray(flow.edges).map(renderEdgeLabel).filter(Boolean).join('\n')}
      </svg>`;
}

validateFlowchart();
writeDiagram({
  outPath,
  template,
  diagramType: 'flowchart',
  meta: flow.meta,
  svg: renderSvg(),
  cards: flow.cards,
});
