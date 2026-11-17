import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { esc, renderDefinitions, textUnits } from '../shared/utils.mjs';
import { animateAttr, focusNodeAttrs, focusNodeTitle, loadDiagramWithBrandMarks, writeDiagram, svgAccessibleText, svgRootAttrs } from '../shared/cli.mjs';
import { throwDiagnosticProblems } from '../shared/diagnostics.mjs';
import { asArray } from '../shared/geometry.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const { diagram: venn, template, outPath } = await loadDiagramWithBrandMarks({
  rendererDir: __dirname,
  diagramType: 'venn',
  defaultExample: 'devops-shared.venn.json',
});

const viewBox = venn.meta?.viewBox;

const layout = {
  cx: 480,
  cy: 250,
  r: 140,
  distance: 170,
  minWidth: 960,
};

// ---- Circle centers ---------------------------------------------------------
// 2 sets: two circles side by side. 3 sets: equilateral triangle.
const sets = asArray(venn.sets);
const centers = new Map();
if (sets.length === 2) {
  centers.set(sets[0].id, { x: layout.cx - layout.distance / 2, y: layout.cy });
  centers.set(sets[1].id, { x: layout.cx + layout.distance / 2, y: layout.cy });
} else {
  const angle = (2 * Math.PI) / 3;
  sets.forEach((set, i) => {
    const a = -Math.PI / 2 + i * angle;
    centers.set(set.id, {
      x: layout.cx + Math.cos(a) * layout.distance,
      y: layout.cy + Math.sin(a) * layout.distance,
    });
  });
}

const neededViewBox = [Math.max(layout.minWidth, layout.cx + layout.r + layout.distance + 60), layout.cy + layout.r + layout.distance + 40];
const effectiveViewBox = viewBox
  ? [Math.max(viewBox[0], neededViewBox[0]), Math.max(viewBox[1], neededViewBox[1])]
  : neededViewBox;

// ---- Intersection label centers --------------------------------------------
// An intersection label sits at the centroid of the sets it names.
function intersectionCenter(setsInvolved) {
  const pts = setsInvolved.map((id) => centers.get(id)).filter(Boolean);
  if (!pts.length) return { x: layout.cx, y: layout.cy };
  const x = pts.reduce((sum, p) => sum + p.x, 0) / pts.length;
  const y = pts.reduce((sum, p) => sum + p.y, 0) / pts.length;
  return { x, y };
}

// ---- Validation -------------------------------------------------------------
function validateVenn() {
  const problems = [];
  const setIds = new Set();
  for (const set of sets) {
    if (setIds.has(set.id)) problems.push(`Set id "${set.id}" is duplicated.`);
    setIds.add(set.id);
  }
  for (const inter of asArray(venn.intersections)) {
    for (const sid of inter.sets) {
      if (!setIds.has(sid)) problems.push(`Intersection "${inter.id}" references unknown set "${sid}".`);
    }
    if (inter.sets.length < 2) problems.push(`Intersection "${inter.id}" must name at least two sets.`);
  }
  if (problems.length) {
    throwDiagnosticProblems('Venn layout validation failed', problems, {
      subject: { diagramType: 'venn' },
    });
  }
}

// ---- Render -----------------------------------------------------------------
function renderSet(set) {
  const c = centers.get(set.id);
  const passport = { kind: 'set', sublabel: set.note };
  return `        <g ${focusNodeAttrs(set.id, set.label, passport, venn.meta.locale)}>
          ${focusNodeTitle(set.label, passport)}
          <circle cx="${c.x}" cy="${c.y}" r="${layout.r}" class="c-mask" fill="none"/>
          <circle cx="${c.x}" cy="${c.y}" r="${layout.r}" class="c-cloud"${animateAttr(venn.meta, 'node', 0)} stroke-width="1.5" opacity="0.55"/>
          <text x="${c.x}" y="${c.y - layout.r - 18}" font-size="10" font-weight="700" class="t-primary" text-anchor="middle">${esc(set.label)}</text>
        </g>`;
}

function renderIntersection(inter) {
  const c = intersectionCenter(inter.sets);
  const labelW = Math.max(40, Math.round(textUnits(inter.label) * 4.5 + 12));
  return `        <g>
          <rect x="${c.x - labelW / 2}" y="${c.y - 9}" width="${labelW}" height="16" rx="4" class="c-mask"/>
          <text x="${c.x}" y="${c.y + 3}" font-size="8" font-weight="600" class="t-primary" text-anchor="middle">${esc(inter.label)}</text>
        </g>`;
}

function renderSvg() {
  return `      <svg viewBox="0 0 ${effectiveViewBox[0]} ${effectiveViewBox[1]}" ${svgRootAttrs(venn.meta)}>
${svgAccessibleText(venn.meta, 'venn')}
${renderDefinitions()}

        <!-- Background Grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Sets -->
${sets.map(renderSet).join('\n\n')}

        <!-- Intersections -->
${asArray(venn.intersections).map(renderIntersection).join('\n')}
      </svg>`;
}

validateVenn();
writeDiagram({
  outPath,
  template,
  diagramType: 'venn',
  meta: venn.meta,
  svg: renderSvg(),
  cards: venn.cards,
});
