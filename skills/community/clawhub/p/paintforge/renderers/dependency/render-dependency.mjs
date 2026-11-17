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
const { diagram: dep, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'dependency',
  defaultExample: 'web-app.dependency.json',
});

const viewBox = dep.meta?.viewBox;

const layout = {
  nodeMinW: 120,
  nodeMaxW: 220,
  nodeH: 56,
  labelPadX: 12,
  versionPadTop: 34,
  colGap: 70,
  rowGap: 64,
  originX: 60,
  originY: 56,
  bottomPad: 44,
};

function measureNode(node) {
  const labelUnits = textUnits(node.label);
  const versionUnits = textUnits(node.version || '');
  const contentUnits = Math.max(labelUnits + 2, versionUnits);
  const width = Math.min(layout.nodeMaxW, Math.max(layout.nodeMinW, Math.round(contentUnits * 6.2 + layout.labelPadX * 2)));
  return { ...node, width, height: layout.nodeH };
}

// ---- Layered DAG layout -----------------------------------------------------
// Same deterministic layered layout as the ER renderer: Kahn topological
// layering, barycenter ordering, center-aligned coordinates. Dependency graphs
// may contain cycles (e.g. peer dependencies); the Kahn pass leaves cycle
// members unplaced and they fall through to their own trailing layer, so the
// layout degrades gracefully instead of failing.
function orderByBarycenter(ids, weightOf) {
  return ids
    .map((id, index) => ({ id, index, weight: weightOf(id) }))
    .sort((a, b) => a.weight - b.weight || a.index - b.index)
    .map((entry) => entry.id);
}

function layeredLayout() {
  const nodes = asArray(dep.nodes).map(measureNode);
  const byId = new Map(nodes.map((node) => [node.id, node]));
  const ids = nodes.map((node) => node.id);

  const outgoing = new Map(ids.map((id) => [id, new Set()]));
  const incoming = new Map(ids.map((id) => [id, new Set()]));
  for (const rel of asArray(dep.dependencies)) {
    if (!byId.has(rel.from) || !byId.has(rel.to) || rel.from === rel.to) continue;
    outgoing.get(rel.from).add(rel.to);
    incoming.get(rel.to).add(rel.from);
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

// ---- Dependency routing (mirrors ER's box-and-arrow engine) ------------------
function dependencySides(rel) {
  const from = nodes.get(rel.from);
  const to = nodes.get(rel.to);
  return {
    fromSide: chosenSide(rel.fromSide, defaultFromSide(from, to)),
    toSide: chosenSide(rel.toSide, defaultToSide(from, to)),
  };
}

const automaticPorts = automaticPortSpread(dep.dependencies, nodes, {
  sideFor: (rel, endpoint) => dependencySides(rel)[endpoint === 'source' ? 'fromSide' : 'toSide'],
});

function routeVia(rel, from, to, start, end) {
  if (rel.via) return rel.via;
  switch (rel.route || 'auto') {
    case 'straight':
      return [];
    case 'vertical-channel': {
      const x = rel.channelX ?? start[0] + (end[0] > start[0] ? 44 : -44);
      return [[x, start[1]], [x, end[1]]];
    }
    case 'bottom-channel': {
      const y = rel.channelY ?? Math.max(from.y + from.height, to.y + to.height) + 26;
      return [[start[0], y], [end[0], y]];
    }
    case 'top-channel': {
      const y = rel.channelY ?? Math.min(from.y, to.y) - 24;
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

function pathFor(rel) {
  if (pathCache.has(rel)) return pathCache.get(rel);
  const from = nodes.get(rel.from);
  const to = nodes.get(rel.to);
  const ports = automaticPorts.get(rel);
  const { fromSide, toSide } = dependencySides(rel);
  const start = ports?.from || anchor(from, fromSide);
  const end = ports?.to || anchor(to, toSide);
  const rawPoints = [start, ...routeVia(rel, from, to, start, end), end];
  const points = [];
  for (const p of rawPoints) {
    const prev = points.at(-1);
    if (!prev || Math.abs(p[0] - prev[0]) > 0.0001 || Math.abs(p[1] - prev[1]) > 0.0001) {
      points.push(p);
    }
  }
  if (points.length < 2) points.push(end);
  const routed = { d: polylinePath(points), points };
  pathCache.set(rel, routed);
  return routed;
}

// ---- Validation -------------------------------------------------------------
function validateDependency() {
  const problems = [];
  if (nodes.size !== asArray(dep.nodes).length) problems.push('Node ids must be unique.');
  for (const node of nodes.values()) {
    if (!isFinitePoint(node.x, node.y, node.cx, node.cy)) {
      problems.push(`Node "${node.id}" produced non-finite coordinates.`);
    }
  }
  const list = nodeList;
  for (let i = 0; i < list.length; i += 1) {
    for (let j = i + 1; j < list.length; j += 1) {
      if (rectsOverlap(list[i], list[j], 10)) {
        problems.push(`Nodes "${list[i].id}" and "${list[j].id}" are less than 10px apart.`);
      }
    }
  }
  for (const rel of asArray(dep.dependencies)) {
    if (!nodes.has(rel.from)) problems.push(`Dependency references unknown source "${rel.from}".`);
    if (!nodes.has(rel.to)) problems.push(`Dependency references unknown target "${rel.to}".`);
  }
  if (problems.length) {
    throwDiagnosticProblems('Dependency layout validation failed', problems, {
      subject: { diagramType: 'dependency' },
    });
  }
}

// ---- Render -----------------------------------------------------------------
function renderNode(node) {
  const passport = { kind: node.kind || 'package', sublabel: node.version, tag: node.kind || 'package' };
  const version = node.version
    ? `<text x="${node.cx}" y="${node.y + layout.versionPadTop}" font-size="7" class="t-dim" text-anchor="middle">${esc(node.version)}</text>`
    : '';
  return `        <g ${focusNodeAttrs(node.id, node.label, passport, dep.meta.locale)}>
          ${focusNodeTitle(node.label, passport)}
          <rect x="${node.x}" y="${node.y}" width="${node.width}" height="${node.height}" rx="6" class="c-mask"/>
          <rect x="${node.x}" y="${node.y}" width="${node.width}" height="${node.height}" rx="6" class="c-backend"${animateAttr(dep.meta, 'node', 0)} stroke-width="1.5"/>
          <text x="${node.cx}" y="${node.y + 22}" font-size="9" font-weight="700" class="t-primary" text-anchor="middle">${esc(node.label)}</text>${version}
        </g>`;
}

function renderDependency(rel, index) {
  const [cls, marker] = arrowClassMap[rel.variant || 'default'] || arrowClassMap.default;
  const routed = pathFor(rel);
  const strokeWidth = rel.width || (rel.variant === 'emphasis' ? 1.8 : 1.4);
  return `        <g>
          <path ${focusEdgeAttrs(rel.from, rel.to, rel.label || '', index, rel.id)} data-composition-points="${routePointsValue(routed.points)}" d="${routed.d}" class="${cls}"${animateAttr(dep.meta, 'edge', index)} stroke-width="${strokeWidth}" marker-end="url(#${marker})"/>
        </g>`;
}

function renderDependencyLabel(rel, index) {
  if (!rel.label) return '';
  const routed = pathFor(rel);
  const [lx, ly] = labelPoint(rel, routed.points);
  const labelW = Math.max(34, Math.round(textUnits(rel.label) * 4.9 + 12));
  return `        <g data-detail="context" ${focusEdgeAttrs(rel.from, rel.to, rel.label, index, rel.id)}>
          <rect x="${lx - labelW / 2}" y="${ly - 9}" width="${labelW}" height="16" rx="4" class="c-mask"/>
          <text x="${lx}" y="${ly + 3}" class="${variantAccent(rel.variant)}" font-size="8" text-anchor="middle">${esc(rel.label)}</text>
        </g>`;
}

function renderSvg() {
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(dep.meta)}>
${svgAccessibleText(dep.meta, 'dependency')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Dependency paths -->
${asArray(dep.dependencies).map(renderDependency).join('\n')}

        <!-- Nodes -->
${nodeList.map(renderNode).join('\n\n')}

        <!-- Dependency labels -->
${asArray(dep.dependencies).map(renderDependencyLabel).filter(Boolean).join('\n')}
      </svg>`;
}

validateDependency();
writeDiagram({
  outPath,
  template,
  diagramType: 'dependency',
  meta: dep.meta,
  svg: renderSvg(),
  cards: dep.cards,
});
