import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { esc, renderDefinitions, textUnits } from '../shared/utils.mjs';
import { animateAttr, focusNodeAttrs, focusNodeTitle, loadDiagramWithBrandMarks, writeDiagram, svgAccessibleText, svgRootAttrs } from '../shared/cli.mjs';
import { throwDiagnosticProblems } from '../shared/diagnostics.mjs';
import { asArray, isFinitePoint } from '../shared/geometry.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const { diagram: sankey, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'sankey',
  defaultExample: 'energy-flow.sankey.json',
});

const viewBox = sankey.meta?.viewBox;

const layout = {
  chartX: 60,
  chartY: 60,
  chartW: 840,
  chartH: 440,
  nodeW: 14,
  minWidth: 960,
};

// ---- Node total flow + column grouping ------------------------------------
const nodes = asArray(sankey.nodes);
const flows = asArray(sankey.flows);

const byId = new Map(nodes.map((n) => [n.id, n]));
const flowSum = new Map(nodes.map((n) => [n.id, 0]));
for (const flow of flows) {
  if (!byId.has(flow.from) || !byId.has(flow.to)) continue;
  flowSum.set(flow.from, flowSum.get(flow.from) + flow.value);
  flowSum.set(flow.to, flowSum.get(flow.to) + flow.value);
}

const maxColumn = Math.max(...nodes.map((n) => n.column), 0);
const columns = Array.from({ length: maxColumn + 1 }, () => []);
for (const node of nodes) columns[node.column].push(node);

// Order nodes within a column by descending flow (larger bundles at top).
for (const col of columns) col.sort((a, b) => (flowSum.get(b.id) || 0) - (flowSum.get(a.id) || 0));

const colX = columns.map((_, i) => layout.chartX + (i * layout.chartW) / Math.max(1, maxColumn));

// Assign node y positions: stack node heights (flow-proportional) with gaps.
const nodeBox = new Map();
columns.forEach((col, colIndex) => {
  const x = colX[colIndex];
  const totalFlow = col.reduce((sum, n) => sum + (flowSum.get(n.id) || 0), 0);
  let cursorY = layout.chartY + (layout.chartH - totalFlow) / 2;
  for (const node of col) {
    const h = Math.max(10, flowSum.get(node.id) || 0);
    nodeBox.set(node.id, {
      x,
      y: cursorY,
      width: layout.nodeW,
      height: h,
      cx: x + layout.nodeW / 2,
      cy: cursorY + h / 2,
    });
    cursorY += h;
  }
});

// ---- Flow ribbons -----------------------------------------------------------
// A ribbon is a quad: top edge from source top to target top, bottom edge from
// source bottom to target bottom, both as a gentle horizontal curve.
function ribbonPath(sourceBox, targetBox) {
  const x1 = sourceBox.x + sourceBox.width;
  const x2 = targetBox.x;
  const y1t = sourceBox.y;
  const y1b = sourceBox.y + sourceBox.height;
  const y2t = targetBox.y;
  const y2b = targetBox.y + targetBox.height;
  const mx = (x1 + x2) / 2;
  return `M ${x1} ${y1t} C ${mx} ${y1t}, ${mx} ${y2t}, ${x2} ${y2t} L ${x2} ${y2b} C ${mx} ${y2b}, ${mx} ${y1b}, ${x1} ${y1b} Z`;
}

// Stack flows so ribbons leaving a node are offset from its top edge.
const outgoingOffset = new Map(nodes.map((n) => [n.id, 0]));
const incomingOffset = new Map(nodes.map((n) => [n.id, 0]));

const positionedFlows = flows.map((flow) => {
  const source = nodeBox.get(flow.from);
  const target = nodeBox.get(flow.to);
  if (!source || !target) return null;
  const sourceBox = { ...source, y: source.y + (outgoingOffset.get(flow.from) || 0), height: flow.value };
  const targetBox = { ...target, y: target.y + (incomingOffset.get(flow.to) || 0), height: flow.value };
  outgoingOffset.set(flow.from, (outgoingOffset.get(flow.from) || 0) + flow.value);
  incomingOffset.set(flow.to, (incomingOffset.get(flow.to) || 0) + flow.value);
  return { ...flow, sourceBox, targetBox };
}).filter(Boolean);

const neededViewBox = [Math.max(layout.minWidth, layout.chartX + layout.chartW + 60), layout.chartY + layout.chartH + 80];
const effectiveViewBox = viewBox
  ? [Math.max(viewBox[0], neededViewBox[0]), Math.max(viewBox[1], neededViewBox[1])]
  : neededViewBox;

// ---- Validation -------------------------------------------------------------
function validateSankey() {
  const problems = [];
  const seen = new Set();
  for (const node of nodes) {
    if (seen.has(node.id)) problems.push(`Node id "${node.id}" is duplicated.`);
    seen.add(node.id);
  }
  for (const flow of flows) {
    if (!byId.has(flow.from)) problems.push(`Flow references unknown source "${flow.from}".`);
    if (!byId.has(flow.to)) problems.push(`Flow references unknown target "${flow.to}".`);
    if (flow.value <= 0) problems.push(`Flow "${flow.from} -> ${flow.to}" has non-positive value.`);
    const sourceNode = byId.get(flow.from);
    const targetNode = byId.get(flow.to);
    if (sourceNode && targetNode && sourceNode.column >= targetNode.column) {
      problems.push(`Flow "${flow.from} -> ${flow.to}" goes backward or stays in the same column (columns must increase left to right).`);
    }
  }
  if (problems.length) {
    throwDiagnosticProblems('Sankey layout validation failed', problems, {
      subject: { diagramType: 'sankey' },
    });
  }
}

// ---- Render -----------------------------------------------------------------
function renderNode(node) {
  const box = nodeBox.get(node.id);
  const passport = { kind: 'node', tag: String(flowSum.get(node.id) || 0) };
  const labelX = box.x - 10;
  const labelSide = node.column === 0 ? 'end' : 'start';
  const labelActualX = node.column === 0 ? box.x - 10 : box.x + box.width + 10;
  return `        <g ${focusNodeAttrs(node.id, node.label, passport, sankey.meta.locale)}>
          ${focusNodeTitle(node.label, passport)}
          <rect x="${box.x}" y="${box.y}" width="${box.width}" height="${box.height}" class="c-mask"/>
          <rect x="${box.x}" y="${box.y}" width="${box.width}" height="${box.height}" class="c-security"${animateAttr(sankey.meta, 'node', node.column)} stroke-width="1"/>
          <text x="${labelActualX}" y="${box.cy + 3}" font-size="8" font-weight="600" class="t-primary" text-anchor="${labelSide}">${esc(node.label)}</text>
        </g>`;
}

function renderFlow(flow, index) {
  const d = ribbonPath(flow.sourceBox, flow.targetBox);
  const label = flow.label
    ? `<text x="${(flow.sourceBox.x + flow.targetBox.x) / 2}" y="${(flow.sourceBox.y + flow.targetBox.y) / 2 - 4}" font-size="7" class="t-muted" text-anchor="middle">${esc(flow.label)}</text>`
    : '';
  return `        <g>
          <path d="${d}" data-edge-from="${esc(flow.from)}" data-edge-to="${esc(flow.to)}" class="a-default"${animateAttr(sankey.meta, 'edge', index)} stroke-width="0.5" fill="url(#grid)" opacity="0.55"/>
          ${label}
        </g>`;
}

function renderSvg() {
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(sankey.meta)}>
${svgAccessibleText(sankey.meta, 'sankey')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Flows -->
${positionedFlows.map(renderFlow).join('\n')}

        <!-- Nodes -->
${nodes.map(renderNode).join('\n\n')}
      </svg>`;
}

validateSankey();
writeDiagram({
  outPath,
  template,
  diagramType: 'sankey',
  meta: sankey.meta,
  svg: renderSvg(),
  cards: sankey.cards,
});
