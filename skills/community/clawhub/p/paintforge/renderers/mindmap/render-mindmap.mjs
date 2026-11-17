import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { esc, renderDefinitions, textUnits } from '../shared/utils.mjs';
import { animateAttr, focusNodeAttrs, focusNodeTitle, loadDiagramWithBrandMarks, writeDiagram, svgAccessibleText, svgRootAttrs } from '../shared/cli.mjs';
import { throwDiagnosticProblems } from '../shared/diagnostics.mjs';
import { translateMessage as i18nText } from '../shared/i18n.mjs';
import {
  asArray,
  isFinitePoint,
  rectsOverlap,
  polylinePath,
} from '../shared/geometry.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const { diagram: mindmap, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'mindmap',
  defaultExample: 'product-roadmap.mindmap.json',
});

const viewBox = mindmap.meta?.viewBox;

const layout = {
  nodeH: 34,
  minW: 72,
  maxW: 200,
  labelPadX: 12,
  depthGap: 120,
  rowGap: 18,
  rootX: 60,
  rootY: 60,
  bottomPad: 44,
  minWidth: 960,
};

function measureNode(node) {
  const units = textUnits(node.label);
  const width = Math.min(layout.maxW, Math.max(layout.minW, Math.round(units * 6.2 + layout.labelPadX * 2)));
  return { ...node, width, height: layout.nodeH };
}

// ---- Rightward tree layout --------------------------------------------------
// Mind maps are strict trees with a single root. The root sits at the left;
// each depth level is a column, and Y positions come from leaf-slot counting
// so siblings stack without overlap and parents center on their children.
function mindmapLayout() {
  const root = measureNode(mindmap.root);
  const topics = asArray(mindmap.topics).map(measureNode);
  const byId = new Map([[root.id, root], ...topics.map((t) => [t.id, t])]);
  const all = [root, ...topics];
  const ids = all.map((n) => n.id);

  const children = new Map(ids.map((id) => [id, []]));
  const parentOf = new Map();
  for (const t of topics) {
    if (!byId.has(t.parent) || t.parent === t.id) continue;
    children.get(t.parent).push(t.id);
    parentOf.set(t.id, t.parent);
  }
  for (const list of children.values()) list.sort();

  // Leaf-slot assignment: each leaf gets a slot; parents center on children.
  let leafSlot = 0;
  const slotOf = new Map();
  const spanOf = new Map();

  function assign(nodeId) {
    const kids = children.get(nodeId);
    if (kids.length === 0) {
      slotOf.set(nodeId, leafSlot);
      leafSlot += 1;
      spanOf.set(nodeId, [leafSlot - 1, leafSlot - 1]);
      return;
    }
    let minSlot = Infinity;
    let maxSlot = -Infinity;
    for (const kid of kids) {
      assign(kid);
      const [a, b] = spanOf.get(kid);
      minSlot = Math.min(minSlot, a);
      maxSlot = Math.max(maxSlot, b);
    }
    spanOf.set(nodeId, [minSlot, maxSlot]);
    slotOf.set(nodeId, (minSlot + maxSlot) / 2);
  }
  assign(root.id);
  // Unreachable topics (bad parent, cycles) fall through to trailing slots.
  for (const id of ids) {
    if (!slotOf.has(id)) {
      slotOf.set(id, leafSlot);
      leafSlot += 1;
      spanOf.set(id, [leafSlot - 1, leafSlot - 1]);
    }
  }

  // Depth via BFS from root.
  const depthOf = new Map();
  function assignDepth(nodeId, depth) {
    if (depthOf.has(nodeId)) return;
    depthOf.set(nodeId, depth);
    for (const kid of children.get(nodeId)) assignDepth(kid, depth + 1);
  }
  assignDepth(root.id, 0);
  for (const id of ids) if (!depthOf.has(id)) depthOf.set(id, 0);

  const maxDepth = Math.max(0, ...depthOf.values());
  const columns = Array.from({ length: maxDepth + 1 }, () => []);
  for (const id of ids) columns[depthOf.get(id)].push(id);
  for (const col of columns) col.sort((a, b) => slotOf.get(a) - slotOf.get(b));

  // Y: slot pitch = node height + row gap.
  const slotPitch = layout.nodeH + layout.rowGap;
  const colCounts = columns.map((c) => c.length);
  const maxSlots = Math.max(...colCounts);
  const graphHeight = Math.max(1, maxSlots) * slotPitch;

  const positions = new Map();
  columns.forEach((col, colIndex) => {
    const x = layout.rootX + colIndex * layout.depthGap;
    for (const id of col) {
      const node = byId.get(id);
      const y = layout.rootY + slotOf.get(id) * slotPitch;
      positions.set(id, { x, y });
    }
  });

  const measured = all.map((n) => {
    const { x, y } = positions.get(n.id);
    return { ...n, x, y, cx: x + n.width / 2, cy: y + n.height / 2 };
  });
  const maxX = Math.max(...measured.map((m) => m.x + m.width));
  const maxY = Math.max(...measured.map((m) => m.y + m.height));
  return {
    root: measured[0],
    topics: measured.slice(1),
    parentOf,
    neededViewBox: [Math.max(layout.minWidth, maxX + 40), maxY + layout.bottomPad],
  };
}

const { root: rootNode, topics: topicList, parentOf, neededViewBox } = mindmapLayout();
const byId = new Map([rootNode, ...topicList].map((n) => [n.id, n]));
const effectiveViewBox = viewBox
  ? [Math.max(viewBox[0], neededViewBox[0]), Math.max(viewBox[1], neededViewBox[1])]
  : neededViewBox;

// ---- Branch routing ---------------------------------------------------------
// Each branch is a gentle elbow from parent's right edge to child's left edge.
const pathCache = new Map();

function pathFor(childId) {
  if (pathCache.has(childId)) return pathCache.get(childId);
  const parentId = parentOf.get(childId) || mindmap.root.id;
  const parent = byId.get(parentId);
  const child = byId.get(childId);
  const start = [parent.x + parent.width, parent.cy];
  const end = [child.x, child.cy];
  const midX = start[0] + (end[0] - start[0]) / 2;
  const points = [start, [midX, start[1]], [midX, end[1]], end];
  const routed = { d: polylinePath(points), points };
  pathCache.set(childId, routed);
  return routed;
}

// ---- Validation -------------------------------------------------------------
function validateMindmap() {
  const problems = [];
  const allIds = [rootNode.id, ...topicList.map((t) => t.id)];
  if (new Set(allIds).size !== allIds.length) problems.push('Topic ids must be unique and distinct from the root.');
  for (const node of [rootNode, ...topicList]) {
    if (!isFinitePoint(node.x, node.y, node.cx, node.cy)) {
      problems.push(`Topic "${node.id}" produced non-finite coordinates.`);
    }
  }
  const boxes = [rootNode, ...topicList];
  for (let i = 0; i < boxes.length; i += 1) {
    for (let j = i + 1; j < boxes.length; j += 1) {
      if (rectsOverlap(boxes[i], boxes[j], 4)) {
        problems.push(`Topics "${boxes[i].id}" and "${boxes[j].id}" overlap.`);
      }
    }
  }
  for (const t of topicList) {
    if (!byId.has(t.parent)) problems.push(`Topic "${t.id}" references unknown parent "${t.parent}".`);
  }
  if (problems.length) {
    throwDiagnosticProblems('Mind map layout validation failed', problems, {
      subject: { diagramType: 'mindmap' },
    });
  }
}

// ---- Render -----------------------------------------------------------------
function renderNode(node, isRoot) {
  const passport = { kind: isRoot ? 'root' : 'topic', sublabel: node.note, tag: isRoot ? 'central topic' : 'topic' };
  const rx = isRoot ? 10 : 8;
  const cls = isRoot ? 'c-security' : 'c-frontend';
  return `        <g ${focusNodeAttrs(node.id, node.label, passport, mindmap.meta.locale)}>
          ${focusNodeTitle(node.label, passport)}
          <rect x="${node.x}" y="${node.y}" width="${node.width}" height="${node.height}" rx="${rx}" class="c-mask"/>
          <rect x="${node.x}" y="${node.y}" width="${node.width}" height="${node.height}" rx="${rx}" class="${cls}"${animateAttr(mindmap.meta, 'node', 0)} stroke-width="1.5"/>
          <text x="${node.cx}" y="${node.cy + 3}" font-size="${isRoot ? 10 : 8}" font-weight="${isRoot ? '700' : '600'}" class="t-primary" text-anchor="middle">${esc(node.label)}</text>
        </g>`;
}

function renderBranch(childId) {
  const routed = pathFor(childId);
  const child = byId.get(childId);
  const variant = child.variant || 'default';
  const strokeWidth = variant === 'emphasis' ? 1.8 : 1.4;
  const cls = variant === 'emphasis' ? 'a-emphasis' : variant === 'security' ? 'a-security' : variant === 'dashed' ? 'a-dashed' : 'a-default';
  const marker = variant === 'emphasis' ? 'arrowhead-emphasis' : variant === 'security' ? 'arrowhead-security' : variant === 'dashed' ? 'arrowhead-dashed' : 'arrowhead';
  return `        <path data-edge-from="${esc(parentOf.get(childId) || mindmap.root.id)}" data-edge-to="${esc(childId)}" d="${routed.d}" class="${cls}"${animateAttr(mindmap.meta, 'edge', 0)} stroke-width="${strokeWidth}" marker-end="url(#${marker})"/>`;
}

function renderSvg() {
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(mindmap.meta)}>
${svgAccessibleText(mindmap.meta, 'mindmap')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Branches -->
${topicList.map((t) => renderBranch(t.id)).join('\n')}

        <!-- Root -->
${renderNode(rootNode, true)}

        <!-- Topics -->
${topicList.map((t) => renderNode(t, false)).join('\n\n')}
      </svg>`;
}

validateMindmap();
writeDiagram({
  outPath,
  template,
  diagramType: 'mindmap',
  meta: mindmap.meta,
  svg: renderSvg(),
  cards: mindmap.cards,
});
