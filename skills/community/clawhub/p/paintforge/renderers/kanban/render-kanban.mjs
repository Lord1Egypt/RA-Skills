import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { esc, renderDefinitions, textUnits } from '../shared/utils.mjs';
import { animateAttr, focusNodeAttrs, focusNodeTitle, loadDiagramWithBrandMarks, writeDiagram, svgAccessibleText, svgRootAttrs } from '../shared/cli.mjs';
import { throwDiagnosticProblems } from '../shared/diagnostics.mjs';
import { asArray, isFinitePoint, rectsOverlap } from '../shared/geometry.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const { diagram: kanban, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'kanban',
  defaultExample: 'sprint-board.kanban.json',
});

const viewBox = kanban.meta?.viewBox;

const layout = {
  boardX: 60,
  boardY: 70,
  colGap: 24,
  colPad: 16,
  cardH: 48,
  cardGap: 14,
  headerH: 44,
  labelPadX: 12,
  minWidth: 960,
};

// ---- Column layout ----------------------------------------------------------
const columns = asArray(kanban.columns);
const cards = asArray(kanban.cards);

const colCount = columns.length;
const boardW = 900;
const colW = (boardW - (colCount - 1) * layout.colGap) / colCount;

// Group cards per column.
const cardsByColumn = new Map(columns.map((c) => [c.id, []]));
for (const card of cards) {
  if (cardsByColumn.has(card.column)) cardsByColumn.get(card.column).push(card);
  else cardsByColumn.set(card.column, [card]);
}

const columnX = new Map(columns.map((c, i) => [c.id, layout.boardX + i * (colW + layout.colGap)]));

const positionedCards = [];
for (const col of columns) {
  const x = columnX.get(col.id);
  const colCards = cardsByColumn.get(col.id);
  colCards.forEach((card, index) => {
    const y = layout.boardY + layout.headerH + layout.colPad + index * (layout.cardH + layout.cardGap);
    positionedCards.push({
      ...card,
      x: x + layout.colPad,
      y,
      width: colW - 2 * layout.colPad,
      height: layout.cardH,
      cx: x + layout.colPad + (colW - 2 * layout.colPad) / 2,
      cy: y + layout.cardH / 2,
    });
  });
}

const maxCardsInColumn = Math.max(...columns.map((c) => cardsByColumn.get(c.id).length), 1);
const boardH = layout.headerH + layout.colPad + maxCardsInColumn * (layout.cardH + layout.cardGap) + layout.colPad;
const neededViewBox = [Math.max(layout.minWidth, layout.boardX + boardW + 40), layout.boardY + boardH + 80];
const effectiveViewBox = viewBox
  ? [Math.max(viewBox[0], neededViewBox[0]), Math.max(viewBox[1], neededViewBox[1])]
  : neededViewBox;

// ---- Validation -------------------------------------------------------------
function validateKanban() {
  const problems = [];
  const seen = new Set();
  for (const card of positionedCards) {
    if (seen.has(card.id)) problems.push(`Card id "${card.id}" is duplicated.`);
    seen.add(card.id);
    if (!isFinitePoint(card.x, card.y, card.cx, card.cy)) problems.push(`Card "${card.id}" produced non-finite coordinates.`);
    const labelUnits = textUnits(card.label);
    if (labelUnits * 6.2 > card.width - 16) {
      problems.push(`Card "${card.id}" label is wider than its column.`);
    }
  }
  for (const card of asArray(kanban.cards)) {
    if (!columnX.has(card.column)) problems.push(`Card "${card.id}" references unknown column "${card.column}".`);
  }
  const colIds = new Set();
  for (const col of columns) {
    if (colIds.has(col.id)) problems.push(`Column id "${col.id}" is duplicated.`);
    colIds.add(col.id);
  }
  if (problems.length) {
    throwDiagnosticProblems('Kanban layout validation failed', problems, {
      subject: { diagramType: 'kanban' },
    });
  }
}

// ---- Render -----------------------------------------------------------------
function renderColumn(col, index) {
  const x = columnX.get(col.id);
  const y = layout.boardY;
  return `        <g>
          <rect x="${x}" y="${y}" width="${colW}" height="${boardH}" rx="10" class="c-lane" stroke-width="1"/>
          <text x="${x + colW / 2}" y="${y + 28}" font-size="10" font-weight="700" class="t-primary" text-anchor="middle">${esc(col.label)}</text>
          <text x="${x + colW / 2}" y="${y + 42}" font-size="7" class="t-dim" text-anchor="middle">${cardsByColumn.get(col.id).length} card${cardsByColumn.get(col.id).length === 1 ? '' : 's'}</text>
        </g>`;
}

function renderCard(card) {
  const passport = { kind: 'card', sublabel: card.note, tag: card.tag };
  const tag = card.tag
    ? `<text x="${card.x + card.width - 8}" y="${card.y + card.height - 10}" font-size="6.5" class="t-dim" text-anchor="end">${esc(card.tag)}</text>`
    : '';
  return `        <g ${focusNodeAttrs(card.id, card.label, passport, kanban.meta.locale)}>
          ${focusNodeTitle(card.label, passport)}
          <rect x="${card.x}" y="${card.y}" width="${card.width}" height="${card.height}" rx="6" class="c-mask"/>
          <rect x="${card.x}" y="${card.y}" width="${card.width}" height="${card.height}" rx="6" class="c-frontend"${animateAttr(kanban.meta, 'node', 0)} stroke-width="1.5"/>
          <text x="${card.x + layout.labelPadX}" y="${card.y + 20}" font-size="8.5" font-weight="600" class="t-primary">${esc(card.label)}</text>
          ${card.note ? `<text x="${card.x + layout.labelPadX}" y="${card.y + 34}" font-size="7" class="t-muted">${esc(card.note)}</text>` : ''}${tag}
        </g>`;
}

function renderSvg() {
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(kanban.meta)}>
${svgAccessibleText(kanban.meta, 'kanban')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Columns -->
${columns.map(renderColumn).join('\n')}

        <!-- Cards -->
${positionedCards.map(renderCard).join('\n\n')}
      </svg>`;
}

validateKanban();
writeDiagram({
  outPath,
  template,
  diagramType: 'kanban',
  meta: kanban.meta,
  svg: renderSvg(),
  cards: kanban.notes,
});
