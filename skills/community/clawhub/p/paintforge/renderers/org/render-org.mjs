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
  polylinePath,
  routePointsValue,
  labelPoint,
  arrowClassMap,
  variantAccent,
} from '../shared/geometry.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const { diagram: org, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'org',
  defaultExample: 'engineering-team.org.json',
});

const viewBox = org.meta?.viewBox;

const layout = {
  nodeMinW: 120,
  nodeMaxW: 200,
  nodeH: 56,
  labelPadX: 10,
  titlePadTop: 36,
  colGap: 36,
  rowGap: 76,
  originX: 60,
  originY: 56,
  bottomPad: 44,
  minWidth: 960,
};

function measureNode(person) {
  const nameUnits = textUnits(person.name);
  const titleUnits = textUnits(person.title || '');
  const contentUnits = Math.max(nameUnits + 2, titleUnits);
  const width = Math.min(layout.nodeMaxW, Math.max(layout.nodeMinW, Math.round(contentUnits * 6.2 + layout.labelPadX * 2)));
  return { ...person, width, height: layout.nodeH };
}

// ---- Tree layout ------------------------------------------------------------
// Org charts are strict trees (each person reports to one manager). Assign each
// node a leaf slot, then center each parent over the span of its children.
// Depth sets the row; subtree width sets the horizontal slot span.
function treeLayout() {
  const people = asArray(org.people).map(measureNode);
  const byId = new Map(people.map((p) => [p.id, p]));
  const ids = people.map((p) => p.id);

  const children = new Map(ids.map((id) => [id, []]));
  const parentOf = new Map();
  for (const rel of asArray(org.reports)) {
    if (!byId.has(rel.from) || !byId.has(rel.to) || rel.from === rel.to) continue;
    children.get(rel.from).push(rel.to);
    parentOf.set(rel.to, rel.from);
  }

  // Roots: nodes with no parent, in authored order (deterministic).
  const roots = ids.filter((id) => !parentOf.has(id));

  // Depth-first assign leaf slots, then compute each subtree's slot span.
  let leafSlot = 0;
  const slotOf = new Map();
  const subtreeSpan = new Map(); // [minSlot, maxSlot]

  function assign(nodeId) {
    const kids = children.get(nodeId);
    if (kids.length === 0) {
      slotOf.set(nodeId, leafSlot);
      leafSlot += 1;
      subtreeSpan.set(nodeId, [leafSlot - 1, leafSlot - 1]);
      return;
    }
    const ordered = [...kids].sort();
    let minSlot = Infinity;
    let maxSlot = -Infinity;
    for (const kid of ordered) {
      assign(kid);
      const [a, b] = subtreeSpan.get(kid);
      minSlot = Math.min(minSlot, a);
      maxSlot = Math.max(maxSlot, b);
    }
    subtreeSpan.set(nodeId, [minSlot, maxSlot]);
    slotOf.set(nodeId, (minSlot + maxSlot) / 2);
  }
  for (const root of roots.sort()) assign(root);

  // Nodes with no parent and never reached (isolated cycles) fall through:
  // give them trailing slots so they still render.
  for (const id of ids) {
    if (!slotOf.has(id)) {
      slotOf.set(id, leafSlot);
      leafSlot += 1;
      subtreeSpan.set(id, [leafSlot - 1, leafSlot - 1]);
    }
  }

  // Depth (row) via BFS from roots so every node lands on a row.
  const depthOf = new Map();
  function assignDepth(nodeId, depth) {
    if (depthOf.has(nodeId)) return;
    depthOf.set(nodeId, depth);
    for (const kid of [...children.get(nodeId)].sort()) assignDepth(kid, depth + 1);
  }
  for (const root of roots.sort()) assignDepth(root, 0);
  for (const id of ids) if (!depthOf.has(id)) depthOf.set(id, 0);

  const maxDepth = Math.max(0, ...depthOf.values());
  const rows = Array.from({ length: maxDepth + 1 }, () => []);
  for (const id of ids) rows[depthOf.get(id)].push(id);
  for (const row of rows) row.sort((a, b) => slotOf.get(a) - slotOf.get(b));

  // Coordinate assignment: slot * (nodeWidth + gap), centered on the widest row.
  const slotPitch = layout.nodeMaxW + layout.colGap;
  const rowWidths = rows.map((row) => (row.length - 1) * slotPitch + layout.nodeMaxW);
  const graphWidth = Math.max(...rowWidths, layout.minWidth - 2 * layout.originX);

  const positions = new Map();
  const rowYs = [];
  let cursorY = layout.originY;
  for (let i = 0; i <= maxDepth; i += 1) {
    rowYs.push(cursorY);
    cursorY += layout.nodeH + layout.rowGap;
  }
  rows.forEach((row, rowIndex) => {
    const rowWidth = rowWidths[rowIndex];
    const offsetX = layout.originX + (graphWidth - rowWidth) / 2;
    for (const id of row) {
      const node = byId.get(id);
      const x = offsetX + slotOf.get(id) * slotPitch;
      const y = rowYs[rowIndex];
      positions.set(id, { x, y });
    }
  });

  const measured = people.map((p) => {
    const { x, y } = positions.get(p.id);
    return { ...p, x, y, cx: x + p.width / 2, cy: y + p.height / 2 };
  });
  const maxX = Math.max(...measured.map((m) => m.x + m.width));
  const maxY = Math.max(...measured.map((m) => m.y + m.height));
  return {
    people: measured,
    parentOf,
    neededViewBox: [Math.max(layout.minWidth, maxX + 40), maxY + layout.bottomPad],
  };
}

const { people: peopleList, parentOf, neededViewBox } = treeLayout();
const people = new Map(peopleList.map((p) => [p.id, p]));
const effectiveViewBox = viewBox
  ? [Math.max(viewBox[0], neededViewBox[0]), Math.max(viewBox[1], neededViewBox[1])]
  : neededViewBox;

// ---- Reporting-line routing --------------------------------------------------
// Org edges are manager -> report. Routes go top-to-bottom with a simple
// elbow: down from the manager's bottom, across, down to the report's top.
const pathCache = new Map();

function pathFor(rel) {
  if (pathCache.has(rel)) return pathCache.get(rel);
  const from = people.get(rel.from);
  const to = people.get(rel.to);
  const start = [from.cx, from.y + from.height];
  const end = [to.cx, to.y];
  const points = [];
  if (Math.abs(start[0] - end[0]) < 0.01) {
    points.push(start, end);
  } else {
    const midY = start[1] + (end[1] - start[1]) / 2;
    points.push(start, [start[0], midY], [end[0], midY], end);
  }
  const routed = { d: polylinePath(points), points };
  pathCache.set(rel, routed);
  return routed;
}

// ---- Validation -------------------------------------------------------------
function validateOrg() {
  const problems = [];
  if (people.size !== asArray(org.people).length) problems.push('Person ids must be unique.');
  for (const person of people.values()) {
    if (!isFinitePoint(person.x, person.y, person.cx, person.cy)) {
      problems.push(`Person "${person.id}" produced non-finite coordinates.`);
    }
  }
  for (let i = 0; i < peopleList.length; i += 1) {
    for (let j = i + 1; j < peopleList.length; j += 1) {
      if (rectsOverlap(peopleList[i], peopleList[j], 10)) {
        problems.push(`People "${peopleList[i].id}" and "${peopleList[j].id}" are less than 10px apart.`);
      }
    }
  }
  for (const rel of asArray(org.reports)) {
    if (!people.has(rel.from)) problems.push(`Report references unknown manager "${rel.from}".`);
    if (!people.has(rel.to)) problems.push(`Report references unknown person "${rel.to}".`);
  }
  if (problems.length) {
    throwDiagnosticProblems('Organization layout validation failed', problems, {
      subject: { diagramType: 'org' },
    });
  }
}

// ---- Render -----------------------------------------------------------------
function renderPerson(person) {
  const passport = { kind: 'person', sublabel: person.title, tag: person.team };
  const title = person.title
    ? `<text x="${person.cx}" y="${person.y + layout.titlePadTop}" font-size="7" class="t-dim" text-anchor="middle">${esc(person.title)}</text>`
    : '';
  return `        <g ${focusNodeAttrs(person.id, person.name, passport, org.meta.locale)}>
          ${focusNodeTitle(person.name, passport)}
          <rect x="${person.x}" y="${person.y}" width="${person.width}" height="${person.height}" rx="6" class="c-mask"/>
          <rect x="${person.x}" y="${person.y}" width="${person.width}" height="${person.height}" rx="6" class="c-security"${animateAttr(org.meta, 'node', 0)} stroke-width="1.5"/>
          <text x="${person.cx}" y="${person.y + 22}" font-size="9" font-weight="700" class="t-primary" text-anchor="middle">${esc(person.name)}</text>${title}
        </g>`;
}

function renderReport(rel, index) {
  const [cls, marker] = arrowClassMap[rel.variant || 'default'] || arrowClassMap.default;
  const routed = pathFor(rel);
  const strokeWidth = rel.width || (rel.variant === 'emphasis' ? 1.8 : 1.4);
  return `        <g>
          <path ${focusEdgeAttrs(rel.from, rel.to, rel.label || '', index, rel.id)} data-composition-points="${routePointsValue(routed.points)}" d="${routed.d}" class="${cls}"${animateAttr(org.meta, 'edge', index)} stroke-width="${strokeWidth}" marker-end="url(#${marker})"/>
        </g>`;
}

function renderReportLabel(rel, index) {
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
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(org.meta)}>
${svgAccessibleText(org.meta, 'org')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Report lines -->
${asArray(org.reports).map(renderReport).join('\n')}

        <!-- People -->
${peopleList.map(renderPerson).join('\n\n')}

        <!-- Report labels -->
${asArray(org.reports).map(renderReportLabel).filter(Boolean).join('\n')}
      </svg>`;
}

validateOrg();
writeDiagram({
  outPath,
  template,
  diagramType: 'org',
  meta: org.meta,
  svg: renderSvg(),
  cards: org.cards,
});
