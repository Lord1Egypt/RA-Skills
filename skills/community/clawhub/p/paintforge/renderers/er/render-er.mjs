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
const { diagram: er, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'er',
  defaultExample: 'order-system.er.json',
});

const viewBox = er.meta?.viewBox;

const layout = {
  headerH: 28,
  attrRowH: 18,
  attrPadTop: 8,
  attrPadBottom: 8,
  entityMinW: 150,
  entityMaxW: 240,
  labelPadX: 12,
  colGap: 90,
  rowGap: 56,
  originX: 60,
  originY: 56,
  bottomPad: 44,
};

const CARDINALITY_TEXT = {
  one: '1',
  many: '*',
  'zero-or-one': '0..1',
  'zero-or-many': '0..*',
  'exactly-one': '1..1',
};

function attrWidth(attr) {
  const nameUnits = textUnits(attr.name);
  const typeUnits = textUnits(attr.type || '');
  const keyUnits = attr.key ? 3 : 0;
  return nameUnits + (typeUnits ? typeUnits + 2 : 0) + keyUnits + 4;
}

function measureEntity(entity) {
  const attrs = asArray(entity.attributes);
  const headerUnits = textUnits(entity.label);
  const contentUnits = Math.max(headerUnits + 2, ...attrs.map(attrWidth));
  const width = Math.min(layout.entityMaxW, Math.max(layout.entityMinW, Math.round(contentUnits * 6.2 + layout.labelPadX * 2)));
  const height = layout.headerH + attrs.length * layout.attrRowH + layout.attrPadTop + layout.attrPadBottom;
  return { ...entity, width, height };
}

// ---- Layered DAG layout -----------------------------------------------------
// ER graphs are near-universally directed acyclic: parent entities feed child
// entities. A deterministic layered layout (Kahn topological layering, then
// barycenter ordering, then center-aligned coordinates) places related
// entities in adjacent layers with no edge crossings — the requirement for
// showcase-quality output. Cycles and disconnected nodes fall back to source
// order on their own layer without reordering authored semantics.
function orderByBarycenter(ids, weightOf) {
  return ids
    .map((id, index) => ({ id, index, weight: weightOf(id) }))
    .sort((a, b) => a.weight - b.weight || a.index - b.index)
    .map((entry) => entry.id);
}

function layeredLayout() {
  const entities = asArray(er.entities).map(measureEntity);
  const byId = new Map(entities.map((entity) => [entity.id, entity]));
  const ids = entities.map((entity) => entity.id);

  const outgoing = new Map(ids.map((id) => [id, new Set()]));
  const incoming = new Map(ids.map((id) => [id, new Set()]));
  for (const rel of asArray(er.relationships)) {
    if (!byId.has(rel.from) || !byId.has(rel.to) || rel.from === rel.to) continue;
    outgoing.get(rel.from).add(rel.to);
    incoming.get(rel.to).add(rel.from);
  }

  // Kahn topological layering with deterministic (sorted) tie-breaking.
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

  // Barycenter ordering: order each layer by the mean index of its neighbours
  // in the adjacent layer, so edges stay short and uncrossed.
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

  // Coordinate assignment: layers stack vertically and are centered on the
  // graph's widest layer so single-parent/single-child edges align exactly.
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
      const entity = byId.get(id);
      const y = layerY + (layerHeight - entity.height) / 2;
      positions.set(id, { x: cursorX, y });
      cursorX += entity.width + layout.colGap;
    }
  });

  const measured = entities.map((entity) => {
    const { x, y } = positions.get(entity.id);
    return { ...entity, x, y, cx: x + entity.width / 2, cy: y + entity.height / 2 };
  });
  const maxX = Math.max(...measured.map((m) => m.x + m.width));
  const maxY = Math.max(...measured.map((m) => m.y + m.height));
  // A narrow viewBox is stretched to the reader width by the Viewer, which
  // proportionally inflates the height and overflows the desktop viewport.
  // Keep the authored width at a desktop-reader scale so the aspect ratio
  // stays close to 1:1 under that stretch.
  const minWidth = 960;
  return { entities: measured, neededViewBox: [Math.max(minWidth, maxX + 40), maxY + layout.bottomPad] };
}

const { entities: entityList, neededViewBox } = layeredLayout();
const entities = new Map(entityList.map((e) => [e.id, e]));
const effectiveViewBox = viewBox
  ? [Math.max(viewBox[0], neededViewBox[0]), Math.max(viewBox[1], neededViewBox[1])]
  : neededViewBox;

// ---- Relationship routing (mirrors dataflow's box-and-arrow engine) ----------
function relationshipSides(rel) {
  const from = entities.get(rel.from);
  const to = entities.get(rel.to);
  return {
    fromSide: chosenSide(rel.fromSide, defaultFromSide(from, to)),
    toSide: chosenSide(rel.toSide, defaultToSide(from, to)),
  };
}

const automaticPorts = automaticPortSpread(er.relationships, entities, {
  sideFor: (rel, endpoint) => relationshipSides(rel)[endpoint === 'source' ? 'fromSide' : 'toSide'],
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
  const from = entities.get(rel.from);
  const to = entities.get(rel.to);
  const ports = automaticPorts.get(rel);
  const { fromSide, toSide } = relationshipSides(rel);
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

// ---- Cardinality marker placement at each endpoint --------------------------
// A crow's-foot endpoint needs the line's local direction. For the "from" end
// the direction is the first segment; for the "to" end it is the last segment.
function endpointDirection(points, end) {
  if (points.length < 2) return [1, 0];
  const [start, next] = end === 'from' ? [points[0], points[1]] : [points[points.length - 1], points[points.length - 2]];
  const dx = next[0] - start[0];
  const dy = next[1] - start[1];
  const len = Math.hypot(dx, dy) || 1;
  return [dx / len, dy / len];
}

function renderCardinalityMark(rel, end) {
  const cardinality = end === 'from' ? rel.fromCardinality : rel.toCardinality;
  if (!cardinality) return '';
  const routed = pathFor(rel);
  const endpoint = end === 'from' ? routed.points[0] : routed.points[routed.points.length - 1];
  const [dx, dy] = endpointDirection(routed.points, end);
  // Place the text just outside the entity box, along the line direction.
  const offset = 16;
  const x = endpoint[0] + dx * offset;
  const y = endpoint[1] + dy * offset;
  const text = CARDINALITY_TEXT[cardinality] || cardinality;
  const many = cardinality === 'many' || cardinality === 'zero-or-many';
  // Crow's foot: three prongs opening away from the entity. Reuse the
  // relationship's arrow class for a matching stroke color, but omit
  // marker-end so the artifact checker does not treat the prongs as a routed
  // relationship arrow (they are endpoint notation, not a route).
  const footLen = 10;
  const angle = 25 * Math.PI / 180;
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  const rotate = (cx, cy) => [dx * cx - dy * cy, dx * cy + dy * cx];
  const [lx, ly] = rotate(cos, sin);
  const [rx, ry] = rotate(cos, -sin);
  const prongs = many
    ? `<path d="M ${endpoint[0]} ${endpoint[1]} L ${(endpoint[0] + dx * footLen).toFixed(1)} ${(endpoint[1] + dy * footLen).toFixed(1)} M ${endpoint[0]} ${endpoint[1]} L ${(endpoint[0] + lx * footLen).toFixed(1)} ${(endpoint[1] + ly * footLen).toFixed(1)} M ${endpoint[0]} ${endpoint[1]} L ${(endpoint[0] + rx * footLen).toFixed(1)} ${(endpoint[1] + ry * footLen).toFixed(1)}" class="a-default" stroke-width="1"/>`
    : '';
  return `<g data-detail="fine" class="t-dim">
    <text x="${x}" y="${y}" font-size="8" font-weight="600" text-anchor="middle">${esc(text)}</text>${prongs}
  </g>`;
}

// ---- Validation -------------------------------------------------------------
function validateEr() {
  const problems = [];
  if (entities.size !== asArray(er.entities).length) problems.push('Entity ids must be unique.');
  for (const entity of entities.values()) {
    if (!isFinitePoint(entity.x, entity.y, entity.cx, entity.cy)) {
      problems.push(`Entity "${entity.id}" produced non-finite coordinates.`);
    }
    const attrNames = new Set();
    for (const attr of asArray(entity.attributes)) {
      if (attrNames.has(attr.name)) problems.push(`Entity "${entity.id}" has duplicate attribute "${attr.name}".`);
      attrNames.add(attr.name);
    }
  }
  const list = entityList;
  for (let i = 0; i < list.length; i += 1) {
    for (let j = i + 1; j < list.length; j += 1) {
      if (rectsOverlap(list[i], list[j], 10)) {
        problems.push(`Entities "${list[i].id}" and "${list[j].id}" are less than 10px apart — adjust meta.columns or entity count.`);
      }
    }
  }
  for (const rel of asArray(er.relationships)) {
    if (!entities.has(rel.from)) problems.push(`Relationship "${rel.label}" references unknown source "${rel.from}".`);
    if (!entities.has(rel.to)) problems.push(`Relationship "${rel.label}" references unknown target "${rel.to}".`);
    if (!rel.label) problems.push(`Relationship "${rel.from}" -> "${rel.to}" must include a label.`);
  }
  if (problems.length) {
    throwDiagnosticProblems('Entity-relationship layout validation failed', problems, {
      subject: { diagramType: 'er' },
    });
  }
}

// ---- Render -----------------------------------------------------------------
function renderAttributeRow(attr, x, y, width) {
  const keyMark = attr.key === 'pk' ? 'PK' : attr.key === 'fk' ? 'FK' : attr.key === 'unique' ? 'UQ' : '';
  const keyClass = attr.key === 'pk' ? 't-backend' : attr.key === 'fk' ? 't-security' : 't-dim';
  const nameUnits = textUnits(attr.name);
  const typeUnits = textUnits(attr.type || '');
  const nameX = x + layout.labelPadX;
  const typeX = x + width - layout.labelPadX;
  const keyTag = keyMark
    ? `<text x="${x + width - layout.labelPadX - 30}" y="${y}" font-size="6.5" font-weight="700" class="${keyClass}" text-anchor="end">${keyMark}</text>`
    : '';
  const typeText = attr.type
    ? `<text x="${typeX}" y="${y}" font-size="7" class="t-dim" text-anchor="end">${esc(attr.type)}</text>`
    : '';
  return `<text x="${nameX}" y="${y}" font-size="8" class="t-primary">${esc(attr.name)}</text>${keyTag}${typeText}`;
}

function renderEntity(entity) {
  const attrs = asArray(entity.attributes);
  const passport = { kind: 'entity', sublabel: entity.sublabel, tag: `${attrs.length} attributes` };
  const rows = attrs.map((attr, index) => {
    const y = entity.y + layout.headerH + layout.attrPadTop + index * layout.attrRowH + 13;
    return renderAttributeRow(attr, entity.x, y, entity.width);
  }).join('\n');
  const headerY = entity.y + 18;
  const dividerY = entity.y + layout.headerH;
  return `        <g ${focusNodeAttrs(entity.id, entity.label, passport, er.meta.locale)}>
          ${focusNodeTitle(entity.label, passport)}
          <rect x="${entity.x}" y="${entity.y}" width="${entity.width}" height="${entity.height}" rx="6" class="c-mask"/>
          <rect x="${entity.x}" y="${entity.y}" width="${entity.width}" height="${entity.height}" rx="6" class="c-frontend"${animateAttr(er.meta, 'node', 0)} stroke-width="1.5"/>
          <text x="${entity.x + layout.labelPadX}" y="${headerY}" font-size="9" font-weight="700" class="t-primary">${esc(entity.label)}</text>
          <line x1="${entity.x}" y1="${dividerY}" x2="${entity.x + entity.width}" y2="${dividerY}" class="c-grid" stroke-width="1"/>
${rows}
        </g>`;
}

function renderRelationship(rel, index) {
  const [cls, marker] = arrowClassMap[rel.variant || 'default'] || arrowClassMap.default;
  const routed = pathFor(rel);
  const strokeWidth = rel.width || (rel.variant === 'emphasis' ? 1.8 : 1.4);
  return `        <g>
          <path ${focusEdgeAttrs(rel.from, rel.to, rel.label, index, rel.id)} data-composition-points="${routePointsValue(routed.points)}" d="${routed.d}" class="${cls}"${animateAttr(er.meta, 'edge', index)} stroke-width="${strokeWidth}" marker-end="url(#${marker})"/>
          ${renderCardinalityMark(rel, 'from')}
          ${renderCardinalityMark(rel, 'to')}
        </g>`;
}

function renderRelationshipLabel(rel, index) {
  const routed = pathFor(rel);
  const [lx, ly] = labelPoint(rel, routed.points);
  const labelW = Math.max(34, Math.round(textUnits(rel.label) * 4.9 + 12));
  return `        <g data-detail="context" ${focusEdgeAttrs(rel.from, rel.to, rel.label, index, rel.id)}>
          <rect x="${lx - labelW / 2}" y="${ly - 9}" width="${labelW}" height="16" rx="4" class="c-mask"/>
          <text x="${lx}" y="${ly + 3}" class="${variantAccent(rel.variant)}" font-size="8" text-anchor="middle">${esc(rel.label)}</text>
        </g>`;
}

function renderSvg() {
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(er.meta)}>
${svgAccessibleText(er.meta, 'er')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Relationship paths -->
${asArray(er.relationships).map(renderRelationship).join('\n')}

        <!-- Entities -->
${entityList.map(renderEntity).join('\n\n')}

        <!-- Relationship labels -->
${asArray(er.relationships).map(renderRelationshipLabel).join('\n')}
      </svg>`;
}

validateEr();
writeDiagram({
  outPath,
  template,
  diagramType: 'er',
  meta: er.meta,
  svg: renderSvg(),
  cards: er.cards,
});
