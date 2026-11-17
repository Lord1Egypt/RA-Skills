import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { esc, renderDefinitions, textUnits } from '../shared/utils.mjs';
import { animateAttr, focusNodeAttrs, focusNodeTitle, loadDiagramWithBrandMarks, writeDiagram, svgAccessibleText, svgRootAttrs } from '../shared/cli.mjs';
import { throwDiagnosticProblems } from '../shared/diagnostics.mjs';
import { asArray, isFinitePoint } from '../shared/geometry.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const { diagram: gantt, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'gantt',
  defaultExample: 'release-plan.gantt.json',
});

const viewBox = gantt.meta?.viewBox;

const layout = {
  chartX: 200,
  chartY: 60,
  chartW: 720,
  rowH: 40,
  rowGap: 8,
  barH: 22,
  minWidth: 960,
};

// ---- Date parsing + time scale ---------------------------------------------
// Parse YYYY-MM-DD into a day index. Reject invalid dates loudly.
function parseDate(value) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(value || ''));
  if (!match) throw new Error(`Invalid date "${value}"; expected YYYY-MM-DD.`);
  const [year, month, day] = match.slice(1).map(Number);
  const ms = Date.UTC(year, month - 1, day);
  if (new Date(ms).getUTCFullYear() !== year || new Date(ms).getUTCMonth() !== month - 1 || new Date(ms).getUTCDate() !== day) {
    throw new Error(`Invalid date "${value}" (not a real calendar day).`);
  }
  return ms / 86400000; // day index
}

const tasks = asArray(gantt.tasks).map((t) => ({ ...t, startDay: parseDate(t.start), endDay: parseDate(t.end) }));

const allDays = tasks.flatMap((t) => [t.startDay, t.endDay]);
const minDay = Math.min(...allDays);
const maxDay = Math.max(...allDays);
const daySpan = Math.max(1, maxDay - minDay);

function dayToX(day) {
  return layout.chartX + ((day - minDay) / daySpan) * layout.chartW;
}

// ---- Row layout (group by task group, then source order) -------------------
const rowOf = new Map();
let rowIndex = 0;
for (const task of tasks) {
  rowOf.set(task.id, rowIndex);
  rowIndex += 1;
}
const totalRows = tasks.length;

const chartH = totalRows * (layout.rowH + layout.rowGap);
const neededViewBox = [Math.max(layout.minWidth, layout.chartX + layout.chartW + 60), layout.chartY + chartH + 80];
const effectiveViewBox = viewBox
  ? [Math.max(viewBox[0], neededViewBox[0]), Math.max(viewBox[1], neededViewBox[1])]
  : neededViewBox;

// ---- Validation -------------------------------------------------------------
function validateGantt() {
  const problems = [];
  const seen = new Set();
  for (const task of tasks) {
    if (seen.has(task.id)) problems.push(`Task id "${task.id}" is duplicated.`);
    seen.add(task.id);
    if (task.endDay < task.startDay) problems.push(`Task "${task.id}" ends before it starts (${task.start} -> ${task.end}).`);
  }
  if (problems.length) {
    throwDiagnosticProblems('Gantt layout validation failed', problems, {
      subject: { diagramType: 'gantt' },
    });
  }
}

// ---- Render -----------------------------------------------------------------
function renderGridlines() {
  // Month-ish gridlines every ~30 days.
  const lines = [];
  const step = Math.ceil(daySpan / 6);
  for (let d = minDay; d <= maxDay; d += step) {
    const x = dayToX(d);
    lines.push(`<line x1="${x}" y1="${layout.chartY}" x2="${x}" y2="${layout.chartY + chartH}" class="c-grid" stroke-width="0.5"/>`);
    const label = new Date(d * 86400000).toISOString().slice(0, 10);
    lines.push(`<text x="${x}" y="${layout.chartY - 10}" font-size="7" class="t-dim" text-anchor="middle">${esc(label)}</text>`);
  }
  return lines.join('\n');
}

function renderTask(task) {
  const row = rowOf.get(task.id);
  const y = layout.chartY + row * (layout.rowH + layout.rowGap);
  const x1 = dayToX(task.startDay);
  const x2 = dayToX(task.endDay);
  const barW = Math.max(6, x2 - x1);
  const passport = { kind: 'task', sublabel: task.note, tag: task.group };
  const labelX = layout.chartX - 16;
  return `        <g ${focusNodeAttrs(task.id, task.label, passport, gantt.meta.locale)}>
          ${focusNodeTitle(task.label, passport)}
          <text x="${labelX}" y="${y + layout.barH / 2 + 3}" font-size="8" class="t-primary" text-anchor="end">${esc(task.label)}</text>
          <rect x="${x1}" y="${y}" width="${barW}" height="${layout.barH}" rx="4" class="c-mask"/>
          <rect x="${x1}" y="${y}" width="${barW}" height="${layout.barH}" rx="4" class="c-frontend"${animateAttr(gantt.meta, 'node', row)} stroke-width="1.5"/>
        </g>`;
}

function renderSvg() {
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(gantt.meta)}>
${svgAccessibleText(gantt.meta, 'gantt')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Time gridlines -->
${renderGridlines()}

        <!-- Tasks -->
${tasks.map(renderTask).join('\n\n')}
      </svg>`;
}

validateGantt();
writeDiagram({
  outPath,
  template,
  diagramType: 'gantt',
  meta: gantt.meta,
  svg: renderSvg(),
  cards: gantt.cards,
});
