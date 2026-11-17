import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { esc, renderDefinitions, textUnits } from '../shared/utils.mjs';
import { animateAttr, focusNodeAttrs, focusNodeTitle, loadDiagramWithBrandMarks, writeDiagram, svgAccessibleText, svgRootAttrs } from '../shared/cli.mjs';
import { throwDiagnosticProblems } from '../shared/diagnostics.mjs';
import { asArray, isFinitePoint, rectsOverlap } from '../shared/geometry.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const { diagram: matrix, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'matrix',
  defaultExample: 'feature-priority.matrix.json',
});

const viewBox = matrix.meta?.viewBox;

const layout = {
  plotX: 90,
  plotY: 60,
  plotW: 780,
  plotH: 440,
  dotR: 7,
  labelPadX: 12,
  labelH: 34,
  minWidth: 960,
};

// ---- Axis scale mapping -----------------------------------------------------
// Map item x/y (arbitrary author values) into plot pixel space, with a small
// padding so dots never touch the axis lines.
function computeScale(items, key) {
  const values = items.map((item) => item[key]);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  return { min, max, span };
}

const items = asArray(matrix.items).map((item) => ({ ...item }));
const xScale = computeScale(items, 'x');
const yScale = computeScale(items, 'y');

function plotPoint(item) {
  const pad = 30;
  const px = layout.plotX + pad + ((item.x - xScale.min) / xScale.span) * (layout.plotW - 2 * pad);
  // y axis: author's high value should go up (top), so invert.
  const py = layout.plotY + layout.plotH - pad - ((item.y - yScale.min) / yScale.span) * (layout.plotH - 2 * pad);
  return { px, py };
}

const positioned = items.map((item) => {
  const { px, py } = plotPoint(item);
  return { ...item, px, py };
});

const neededViewBox = [
  Math.max(layout.minWidth, layout.plotX + layout.plotW + 60),
  layout.plotY + layout.plotH + 90,
];
const effectiveViewBox = viewBox
  ? [Math.max(viewBox[0], neededViewBox[0]), Math.max(viewBox[1], neededViewBox[1])]
  : neededViewBox;

// ---- Validation -------------------------------------------------------------
function validateMatrix() {
  const problems = [];
  const seen = new Set();
  for (const item of positioned) {
    if (seen.has(item.id)) problems.push(`Item id "${item.id}" is duplicated.`);
    seen.add(item.id);
    if (!isFinitePoint(item.px, item.py)) problems.push(`Item "${item.id}" produced non-finite coordinates.`);
  }
  // Dot overlap (label collisions) — dots closer than 2r + label clearance.
  const boxes = positioned.map((item) => ({
    id: item.id,
    x: item.px - layout.dotR,
    y: item.py - layout.dotR,
    width: layout.dotR * 2,
    height: layout.dotR * 2,
  }));
  for (let i = 0; i < boxes.length; i += 1) {
    for (let j = i + 1; j < boxes.length; j += 1) {
      if (rectsOverlap(boxes[i], boxes[j], 8)) {
        problems.push(`Items "${boxes[i].id}" and "${boxes[j].id}" are too close on the matrix.`);
      }
    }
  }
  if (problems.length) {
    throwDiagnosticProblems('Matrix layout validation failed', problems, {
      subject: { diagramType: 'matrix' },
    });
  }
}

// ---- Render -----------------------------------------------------------------
function renderAxes() {
  const cx = layout.plotX + layout.plotW / 2;
  const cy = layout.plotY + layout.plotH / 2;
  const axisClass = 'c-grid';
  const quadrantFill = 'c-lane';
  return `        <!-- Quadrant background -->
        <rect x="${layout.plotX}" y="${layout.plotY}" width="${layout.plotW / 2}" height="${layout.plotH / 2}" class="${quadrantFill}" opacity="0.4"/>
        <rect x="${cx}" y="${layout.plotY}" width="${layout.plotW / 2}" height="${layout.plotH / 2}" class="${quadrantFill}" opacity="0.15"/>
        <rect x="${layout.plotX}" y="${cy}" width="${layout.plotW / 2}" height="${layout.plotH / 2}" class="${quadrantFill}" opacity="0.15"/>
        <rect x="${cx}" y="${cy}" width="${layout.plotW / 2}" height="${layout.plotH / 2}" class="${quadrantFill}" opacity="0.25"/>

        <!-- Axes -->
        <line x1="${layout.plotX}" y1="${cy}" x2="${layout.plotX + layout.plotW}" y2="${cy}" class="${axisClass}" stroke-width="1"/>
        <line x1="${cx}" y1="${layout.plotY}" x2="${cx}" y2="${layout.plotY + layout.plotH}" class="${axisClass}" stroke-width="1"/>

        <!-- Axis labels -->
        <text x="${layout.plotX + layout.plotW / 2}" y="${layout.plotY + layout.plotH + 24}" font-size="9" font-weight="600" class="t-primary" text-anchor="middle">${esc(matrix.axes.x.label)}</text>
        <text x="${layout.plotX - 16}" y="${layout.plotY + layout.plotH / 2}" font-size="9" font-weight="600" class="t-primary" text-anchor="middle" transform="rotate(-90 ${layout.plotX - 16} ${layout.plotY + layout.plotH / 2})">${esc(matrix.axes.y.label)}</text>

        <!-- Axis ends -->
        <text x="${layout.plotX}" y="${layout.plotY + layout.plotH + 44}" font-size="7" class="t-dim" text-anchor="start">${esc(matrix.axes.x.low || '')}</text>
        <text x="${layout.plotX + layout.plotW}" y="${layout.plotY + layout.plotH + 44}" font-size="7" class="t-dim" text-anchor="end">${esc(matrix.axes.x.high || '')}</text>
        <text x="${layout.plotX - 16}" y="${layout.plotY}" font-size="7" class="t-dim" text-anchor="end">${esc(matrix.axes.y.high || '')}</text>
        <text x="${layout.plotX - 16}" y="${layout.plotY + layout.plotH}" font-size="7" class="t-dim" text-anchor="end">${esc(matrix.axes.y.low || '')}</text>`;
}

function renderItem(item) {
  const passport = { kind: 'item', sublabel: item.note };
  const labelY = item.py - layout.dotR - 6;
  return `        <g ${focusNodeAttrs(item.id, item.label, passport, matrix.meta.locale)}>
          ${focusNodeTitle(item.label, passport)}
          <circle cx="${item.px}" cy="${item.py}" r="${layout.dotR}" class="c-security"${animateAttr(matrix.meta, 'node', 0)} stroke-width="1.5"/>
          <text x="${item.px}" y="${labelY}" font-size="8" font-weight="600" class="t-primary" text-anchor="middle">${esc(item.label)}</text>
        </g>`;
}

function renderSvg() {
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(matrix.meta)}>
${svgAccessibleText(matrix.meta, 'matrix')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

${renderAxes()}

        <!-- Items -->
${positioned.map(renderItem).join('\n\n')}
      </svg>`;
}

validateMatrix();
writeDiagram({
  outPath,
  template,
  diagramType: 'matrix',
  meta: matrix.meta,
  svg: renderSvg(),
  cards: matrix.cards,
});
