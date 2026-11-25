// Oasis-Blueprints · https://github.com/oasiseng/Oasis-Blueprints · MIT License, Copyright (c) 2026 Oasis Engineering, LLC
// views/sunroom.js — job type "sunroom": a sloped roof on posts against a house (sunroom, porch, lean-to).
// Everything is drawn from PROJECT.geometry, in inches. x runs along the house (door end at left),
// y runs away from the house, z is up from the top of the slab.
// This file is also the worked example for writing a new job type: see JOB at the bottom.
'use strict';

function derive(P) {
  const g = P.geometry, post = g.post, xl = -post / 2, xr = g.clearL + post / 2, yo = g.clearD + post / 2;
  const longX = [xl]; for (const b of g.longBays) longX.push(longX[longX.length - 1] + b);
  const cols = longX.map(x => ({ x, y: yo, line: 'front' }));
  cols.push({ x: xl, y: g.door[0] - post / 2, line: 'left' }, { x: xl, y: g.door[1] + post / 2, line: 'left' }, { x: xl, y: post / 2, line: 'left', atWall: true });
  cols.push({ x: xr, y: g.rightMid, line: 'right' }, { x: xr, y: post / 2, line: 'right', atWall: true });
  const rx0 = (g.clearL - g.roofL) / 2, rx1 = rx0 + g.roofL, slope = g.slopeRise / g.slopeRun, rb = y => g.h0 - slope * y, bt = rb(yo);
  const rafters = []; let x = rx0 + 0.75, last = x;
  while (x < rx1 - 0.75 + 0.01) { rafters.push(x); last = x; x += g.rafterSpacing; }
  if (rx1 - 0.75 - last > 1) rafters.push(rx1 - 0.75);
  return { xl, xr, yo, longX, cols, rx0, rx1, slope, rb, bt, rafters };
}

// ------------------------------------------------------------------ 1  ROOF FRAMING PLAN
function viewPlan(P, G, den = 24) {
  const g = P.geometry, v = new View(den, 'plan'), { xl, xr, yo, longX, cols, rx0, rx1, rafters } = G;
  const WT = g.wallT, L = g.clearL, D = g.clearD, RD = g.roofD, post = g.post, h = post / 2;
  // house wall with openings
  let a = -22; const ops = g.openings.slice().sort((p, q) => p.x0 - q.x0);
  for (const op of ops.concat([{ x0: L + 22 }])) { v.rect(a, -WT, op.x0, 0, 'exw', { fill: v.pat('wall') }); a = op.x1; }
  for (const op of ops) { for (const y of [0, -WT / 2, -WT]) v.line(op.x0, y, op.x1, y, 'o2'); v.text(op.label, (op.x0 + op.x1) / 2, -WT - 7.5, { cls: 'ts', anchor: 'middle' }); }
  v.text('(E) RESIDENCE', (ops[0].x1 + ops[1].x0) / 2, -WT - 15.5, { cls: 'tb', anchor: 'middle' });
  // existing beams below the rafters (dashed), ledger at the house
  v.rect(xl - h, yo - 1.5, xr + h, yo + 1.5, 'exh'); v.rect(xl - 1.5, 0, xl + 1.5, yo - 1.5, 'exh'); v.rect(xr - 1.5, 0, xr + 1.5, yo - 1.5, 'exh');
  v.rect(rx0, 0, rx1, 1.5, 'ex');
  // new rafters, roof edge, new columns
  for (const x of rafters) v.rect(x - 0.75, 1.5, x + 0.75, RD - 0.75, 'new');
  v.rect(rx0, 0, rx1, RD, 'o2');
  for (const c of cols) v.rect(c.x - h, c.y - h, c.x + h, c.y + h, 'newS');
  // door at the left end
  v.line(xl - 2, g.door[0], xl - 2 - 36, g.door[0], 'o'); v.arc(xl - 2, g.door[0], 36, 90, 180, 'o2');
  v.text("(E) 3'-0\" DOOR", xl - 26, g.door[0] - 7, { cls: 'ts', anchor: 'middle' });
  // rafter span and slope
  const ax = 150; v.line(ax, 6, ax, yo - 5, 'ld'); v.arrow(ax, 6, ax, 20); v.arrow(ax, yo - 5, ax, yo - 20);
  v.text(`(N) 2×8 ROOF RAFTERS @ ${g.rafterSpacing}" O.C.\nW/ SIMPSON H2.5A EA. END\nSEE ${REF.d2} AND ${REF.d3}/${REF.sheet}`, ax + 5, 84, { cls: 'tN' });
  v.line(72, 38, 72, 64, 'o'); v.arrow(72, 64, 72, 38); v.text(`SLOPE\n${g.slopeRise}:${g.slopeRun}`, 76, 56, { cls: 'tb' });
  // dimensions: top
  const y1 = RD + 11, y2 = RD + 20, y3 = RD + 29;
  for (let i = 0; i < longX.length - 1; i++) v.dimH(longX[i], longX[i + 1], y1, yo + h, { approx: true });
  v.dimH(xl, xr, y2, yo + h, { text: ftin(xr - xl) + ' C/C COLUMNS' });
  v.dimH(rx0, rx1, y3, RD, { text: ftin(rx1 - rx0) + ' ROOF (OUT TO OUT)' });
  v.dimH(0, L, 24, 24, { text: ftin(L) + ' CLEAR (INSIDE OF COLUMNS)' });
  // left
  const xa = rx0 - 14, xb = rx0 - 26;
  v.dimV(0, g.door[0], xa, xl - h, { approx: true }); v.dimV(g.door[0], g.door[1], xa, xl - h, { text: ftin(g.door[1] - g.door[0]) + ' DOOR' }); v.dimV(g.door[1], D, xa, xl - h, { approx: true });
  v.dimV(0, RD, xb, rx0, { text: ftin(RD) + ' ROOF (OUT TO OUT)' });
  // right
  const xc = rx1 + 12, xd = rx1 + 23;
  v.dimV(0, g.rightMid, xc, xr + h, { approx: true }); v.dimV(g.rightMid, yo, xc, xr + h, { approx: true });
  v.dimV(0, D, xd, xr + h, { text: ftin(D) + ' CLEAR' });
  // bottom, along the house wall
  const yb = -WT - 28, xs = [0].concat(...ops.map(o => [o.x0, o.x1]), [L]);
  for (let i = 0; i < xs.length - 1; i++) v.dimH(xs[i], xs[i + 1], yb, -WT, { approx: i % 2 === 0 });
  // notes
  v.note(`(E) (2) 2×8 BUILT-UP BEAM TO REMAIN\nTYP. 3 SIDES. CHECK FOR ROT / WDO`, 92, yo, 30, 116, { side: 'r' });
  v.note(`(N) PT 4×4 COLUMN AT (E) LOCATION\nON SIMPSON ABU44Z. TYP. OF ${cols.length}\nSEE ${REF.d1}/${REF.sheet}`, longX[3] - 1, yo - 2, 176, 119, { side: 'r', kind: 'N' });
  v.note(`(E) LEDGER / ATTACHMENT TO HOUSE\nV.I.F. SEE ${REF.d3}/${REF.sheet}`, 232, 0.75, 222, 12, { side: 'l' });
  // section cut
  const sx = 103; v.line(sx, -WT - 3, sx, RD + 3, 'cutl'); v.line(sx, y3 + 6, sx, y3 + 14, 'cutl2'); v.line(sx, y3 + 14, sx + 8, y3 + 14, 'cutl2'); v.arrow(sx + 8, y3 + 14, sx, y3 + 14);
  v.bubble(sx - 10, y3 + 12, String(REF.section), REF.sheet);
  return v.svg();
}

// ------------------------------------------------------------------ 2  SECTION
function viewSection(P, G, den = 32) {
  const g = P.geometry, v = new View(den, 'sect'), { yo, rb, bt, slope } = G, RD = g.rafterDepth, BD = g.beamDepth, h = g.post / 2, WT = g.wallT, top = rb(0) + RD + 14;
  const RE = g.roofD + 1.5;   // roof edge: decking and roofing run 1.5 in past the rafter tails (as in the picture)
  v.rect(0, -4, g.roofD + 8, 0, 'exw', { fill: v.pat('conc') }); v.line(g.roofD + 8, -3, g.roofD + 34, -3, 'o2');
  v.rect(-WT, -4, 0, top, 'exw', { fill: v.pat('wall') });
  v.poly([[-WT - 3, top], [-WT * 0.6, top], [-WT * 0.5, top + 3], [-WT * 0.4, top - 3], [-WT * 0.3, top], [3, top]], 'o2', false);
  // roof: decking + roofing over the rafters
  v.line(0, rb(0) + RD + 0.6, RE - 0.5, rb(RE - 0.5) + RD + 0.6, 'o2'); v.line(0, rb(0) + RD + 1.3, RE, rb(RE) + RD + 1.3, 'o'); v.line(RE, rb(RE) + RD + 1.3, RE, rb(RE) - 0.5, 'o');
  v.poly([[1.5, rb(1.5)], [g.roofD - 0.75, rb(g.roofD - 0.75)], [g.roofD - 0.75, rb(g.roofD - 0.75) + RD], [1.5, rb(1.5) + RD]], 'new');
  v.lumber(0, rb(0) - 1, 1.5, rb(0) + RD, 'ex');
  v.lumber(yo - 1.5, bt - BD, yo, bt, 'ex'); v.lumber(yo, bt - BD, yo + 1.5, bt, 'ex');
  v.rect(yo - h, 1, yo + h, bt - BD, 'new');
  v.rect(yo - 2.2, 0, yo + 2.2, 1, 'steel'); v.rect(yo - 2.05, 1, yo - h, 6.5, 'steel'); v.rect(yo + h, 1, yo + 2.05, 6.5, 'steel');
  v.rect(yo + 1.5, bt - 3, yo + 2.2, bt + 3.5, 'steel');
  // slope symbol
  const sx = g.roofD - 40, sy = rb(sx) + RD + 6; v.poly([[sx, sy], [sx + 24, sy], [sx, sy + 24 * slope]], 'o2');
  v.text(String(g.slopeRun), sx + 12, sy - 4.6, { cls: 'ts', anchor: 'middle' }); v.text(String(g.slopeRise), sx - 3, sy - 0.6, { cls: 'ts', anchor: 'middle' });
  // dimensions and levels
  v.dimH(0, yo, -15, -4, { text: `RAFTER SPAN ${ftin(yo, true)} (FACE OF WALL TO C.L. BEAM)` });
  v.dimH(0, g.clearD, 20, 20, { text: ftin(g.clearD) + ' CLEAR' });
  v.datum(`U/S OF RAFTER AT HOUSE\n${ftin(g.h0, true)}  V.I.F.`, -34, g.h0, -WT);
  v.datum(`TOP OF (E) SLAB\n0'-0"`, -34, 0, -WT);
  v.datum(`B.O. (E) BEAM\n${ftin(bt - BD, true)}  V.I.F.`, g.roofD + 52, bt - BD, yo + 6);
  // notes
  v.note(`(E) PLYWOOD DECKING + SELF-ADHERED MOD. BIT. ROOFING\n${P.project.relatedPermit ? 'PERMIT ' + P.project.relatedPermit + '. ' : ''}VERIFY THICKNESS & EXTENT`, 30, rb(30) + RD + 1.3, 40, rb(0) + RD + 13, { side: 'r' });
  v.note(`(N) 2×8 RAFTERS @ ${g.rafterSpacing}" O.C.`, 60, rb(60) + 3.5, 74, 70, { side: 'r', kind: 'N' });
  v.note(`(E) LEDGER AT HOUSE\nV.I.F. SEE ${REF.d3}/${REF.sheet}`, 1.5, rb(0) + 2, 14, 52, { side: 'r' });
  v.note(`(N) SIMPSON H2.5A EA. RAFTER, EA. END\nSEE ${REF.d2}/${REF.sheet}`, yo + 2.2, bt + 2, yo + 16, rb(0) + RD + 4, { side: 'r', kind: 'N' });
  v.note(`(N) PT 4×4 COLUMN`, yo + h, 52, yo + 16, 60, { side: 'r', kind: 'N' });
  v.note(`(N) SIMPSON ABU44Z\nSEE ${REF.d1}/${REF.sheet}`, yo + 2.2, 3.5, yo + 16, 34, { side: 'r', kind: 'N' });
  v.note(`(E) CONC. SLAB / FOUNDATION\nVERIFY THICKNESS & CONDITION`, 100, -2, 92, 8, { side: 'l' });
  v.text('(E) RESIDENCE', -WT / 2 + 1.4, 46, { cls: 'ts', anchor: 'middle', rot: 90 });
  return v.svg();
}

// ------------------------------------------------------------------ 3  FRONT ELEVATION (seen from the yard, so the door end is on the right)
function viewElevation(P, G, den = 48) {
  const g = P.geometry, v = new View(den, 'elev'), { xl, xr, longX, rx0, rx1, rb, bt, rafters } = G, RD = g.rafterDepth, BD = g.beamDepth, h = g.post / 2, L = g.clearL;
  const F = x => L - x, top = rb(0) + RD + 30, rt = bt + RD + 1.3, rh = rb(0) + RD + 1.3;
  v.rect(F(rx1) - 14, 0, F(rx0) + 14, top, 'exb'); v.text('(E) RESIDENCE BEYOND', L / 2 + 30, top - 11, { cls: 'ts', anchor: 'middle' });
  v.rect(-10, -4, L + 10, 0, 'exw', { fill: v.pat('conc') }); v.line(F(rx1) - 30, -3, -10, -3, 'o2'); v.line(L + 10, -3, F(rx0) + 30, -3, 'o2');
  v.rect(F(rx1), rt, F(rx0), rh, 'ex'); v.rect(F(rx1), bt + RD, F(rx0), rt, 'ex');
  for (const x of rafters) v.rect(F(x) - 0.75, bt, F(x) + 0.75, bt + RD, 'new');
  v.rect(F(xr) - h, bt - BD, F(xl) + h, bt, 'ex');
  for (const x of longX) { v.rect(F(x) - h, 1, F(x) + h, bt - BD, 'new'); v.rect(F(x) - 2.2, 0, F(x) + 2.2, 1, 'steel'); }
  const xs = longX.map(F).reverse();
  for (let i = 0; i < xs.length - 1; i++) v.dimH(xs[i], xs[i + 1], -17, -4, { approx: true });
  v.dimH(F(rx1), F(rx0), -30, -4, { text: ftin(rx1 - rx0) + ' ROOF (OUT TO OUT)' });
  const dx = F(rx1) - 30;
  v.datum(`B.O. (E) BEAM\n${ftin(bt - BD, true)}  V.I.F.`, dx, bt - BD, F(xr) - h); v.datum(`TOP OF (E) SLAB\n0'-0"`, dx, 0, -10);
  v.note(`(N) 2×8 RAFTERS\n@ ${g.rafterSpacing}" O.C.`, F(rafters[13]), bt + 3.6, F(rafters[13]) - 8, rh + 15, { side: 'r', kind: 'N' });
  v.note('(N) PT 4×4\nCOLUMN, TYP.', xs[1] + h, 46, xs[1] + 9, 56, { side: 'r', kind: 'N' });
  v.note('(E) (2) 2×8\nBEAM', xs[2] + 12, bt - 3.6, xs[2] + 8, 64, { side: 'r' });
  v.note('(N) ABU44Z\nBASE, TYP.', xs[3] + 2.2, 0.5, xs[3] + 9, 16, { side: 'r', kind: 'N' });
  return v.svg();
}

// ------------------------------------------------------------------ 4  COLUMN BASE
function detailBase(P, G, den = 4) {
  const v = new View(den, 'base'), h = P.geometry.post / 2;
  v.rect(-13, -5, 13, 0, 'exw', { fill: v.pat('conc') });
  v.rect(-h, 1, h, 13.2, 'newF'); v.poly([[-h, 13.2], [-h, 1], [h, 1], [h, 13.2]], 'new', false);
  v.poly([[-h - 0.7, 13.2], [-0.5, 13.2], [-0.15, 14], [0.15, 12.4], [0.5, 13.2], [h + 0.7, 13.2]], 'o2', false);
  v.rect(-1.85, 0, 1.85, 1, 'steel'); v.rect(-2.0, 1, -h, 6.5, 'steel'); v.rect(h, 1, 2.0, 6.5, 'steel');
  for (const y of [2.6, 4.9]) { v.line(-2.0, y, -0.7, y, 'o2'); v.line(2.0, y, 0.7, y, 'o2'); }
  const anc = answer(P, 'anchor');   // open item "anchor": red until the engineer answers it
  v.line(0, 1.7, 0, -3.6, anc ? 'anchOk' : 'anch'); v.line(-0.55, 1.7, 0.55, 1.7, anc ? 'anchOk' : 'anch');
  v.dimV(0, 1, -5.2, -1.85, { text: '1"' });
  v.note('(N) PT 4×4 COLUMN', h, 10.6, 5.2, 11.6, { kind: 'N' });
  v.note('(N) SIMPSON ABU44Z\nMFR. FASTENERS TO COLUMN', 2.0, 4, 5.2, 7.2, { kind: 'N' });
  v.note(anc ? 'ANCHOR TO (E) CONCRETE:\n' + wrap(anc.toUpperCase(), 38) : 'ANCHOR TO (E) CONCRETE:\nTYPE, SIZE, EMBEDMENT, EDGE DISTANCE', 0, -2.2, 5.2, 2.6, { kind: anc ? 'N' : 'R' });
  v.note('STANDOFF BASE', -1.85, 0.5, -6.4, 4.6, { side: 'l' });
  v.note('(E) CONC. SLAB / FOUNDATION\nVERIFY THICKNESS & CONDITION', -8.5, -1.6, -6.4, 8.4, { side: 'l' });
  return v.svg();
}

// ------------------------------------------------------------------ 5  RAFTER / BEAM / COLUMN
function detailBeam(P, G, den = 4) {
  const g = P.geometry, v = new View(den, 'beam'), h = g.post / 2, RD = g.rafterDepth, BD = g.beamDepth, s = G.slope, ct = 2.2, rt = ct + BD, x0 = -12.5, x1 = 2.25;
  v.rect(-h, 0, h, ct, 'newF'); v.poly([[-h, 0], [-h, ct], [h, ct], [h, 0]], 'new', false);
  v.poly([[-h - 0.7, 0], [-0.5, 0], [-0.15, 0.8], [0.15, -0.8], [0.5, 0], [h + 0.7, 0]], 'o2', false);
  v.lumber(-1.5, ct, 0, rt, 'ex'); v.lumber(0, ct, 1.5, rt, 'ex');
  v.poly([[x0, rt - x0 * s], [x1, rt - x1 * s], [x1, rt - x1 * s + RD], [x0, rt - x0 * s + RD]], 'new');
  v.poly([[x0, rt - x0 * s - 0.6], [x0 - 0.35, rt - x0 * s + RD * 0.3], [x0 + 0.35, rt - x0 * s + RD * 0.7], [x0, rt - x0 * s + RD + 0.6]], 'o2', false);
  v.line(x0 - 0.3, rt - x0 * s + RD + 0.75, x1 + 0.7, rt - x1 * s + RD + 0.75, 'o'); v.line(x1 + 0.7, rt - x1 * s + RD + 0.75, x1 + 0.7, rt - x1 * s - 0.4, 'o');
  v.rect(1.5, rt - 3, 1.95, rt + 3.5, 'steel');
  v.note(`(N) 2×8 RAFTER @ ${g.rafterSpacing}" O.C.`, -9, rt + 9 * s + 2.4, -6.6, rt - 2.6, { side: 'l', kind: 'N' });
  v.note('(E) PLYWOOD DECKING + ROOFING', -3, rt + 3 * s + RD + 0.75, 4.6, rt + 9.4, { side: 'r' });
  v.note('(N) SIMPSON H2.5A EA. RAFTER\nMFR. FASTENERS', 1.95, rt + 1.6, 4.6, rt + 6.6, { kind: 'N' });
  v.note('(E) (2) 2×8 BUILT-UP BEAM TO REMAIN\nCHECK FOR ROT / WDO', 1.5, ct + 3.2, 4.6, ct + 2.4, {});
  const bc = answer(P, 'beamToColumn');
  v.note(bc ? 'BEAM TO COLUMN:\n' + wrap(bc.toUpperCase(), 38) : 'BEAM-TO-COLUMN CONNECTION', h, ct - 0.3, 4.6, ct - 2.4, { kind: bc ? 'N' : 'R' });
  v.note('(N) PT 4×4 COLUMN', -h, 1.0, -6.6, 0.6, { side: 'l', kind: 'N' });
  return v.svg();
}

// ------------------------------------------------------------------ 6  RAFTER AT HOUSE
function detailHouse(P, G, den = 4) {
  const g = P.geometry, v = new View(den, 'house'), RD = g.rafterDepth, s = G.slope, lb = 5, x1 = 15.5, top = lb + RD + 5.2;
  v.rect(-6, 0, 0, top, 'exw', { fill: v.pat('wall') });
  for (const y of [0, top]) v.poly([[-6.8, y], [-3.6, y], [-3.2, y + 0.8], [-2.8, y - 0.8], [-2.4, y], [0.8, y]], 'o2', false);
  v.lumber(0, lb - 1, 1.5, lb + RD, 'ex');
  v.poly([[1.5, lb - 1.5 * s], [x1, lb - x1 * s], [x1, lb - x1 * s + RD], [1.5, lb - 1.5 * s + RD]], 'new');
  v.poly([[x1, lb - x1 * s - 0.6], [x1 - 0.35, lb - x1 * s + RD * 0.3], [x1 + 0.35, lb - x1 * s + RD * 0.7], [x1, lb - x1 * s + RD + 0.6]], 'o2', false);
  v.line(0, lb + RD + 0.75, x1 + 0.3, lb - x1 * s + RD + 0.75, 'o');
  v.rect(1.5, lb + 0.9, 3.6, lb + 5.6, 'steelo'); for (const [x, y] of [[2.1, lb + 1.8], [3.0, lb + 1.8], [2.1, lb + 3.2], [3.0, lb + 3.2], [2.1, lb + 4.6], [3.0, lb + 4.6]]) v.circle(x, y, 0.13, 'dot');
  v.note(`(N) 2×8 RAFTER @ ${g.rafterSpacing}" O.C.`, 10.5, lb - 10.5 * s + 5, 12.4, lb + RD + 4.2, { side: 'r', kind: 'N' });
  v.note('(N) SIMPSON H2.5A EA. RAFTER\n(REPORTED) V.I.F.', 3.6, lb + 2.6, 9.5, lb - 2.6, { side: 'r', kind: 'N' });
  v.note('(E) LEDGER / RAFTER SUPPORT AT HOUSE\nV.I.F. SIZE & FASTENING.\nREPORT TO ENGINEER', 0.75, lb + 0.4, -8.4, 3.4, { side: 'l' });
  v.note('(E) EXTERIOR WALL OF RESIDENCE', -3, top - 2, -8.4, top - 0.8, { side: 'l' });
  return v.svg();
}

// ------------------------------------------------------------------ isometric overview and step pictures
// mode: colour key per group. 'new' | 'exist' | 'ghost' | 'check'. shores: draw temporary shoring.
function isoScene(P, G, o = {}) {
  const g = P.geometry, iso = new Iso(o.den || 60, o.id || 'iso'), { xl, xr, yo, cols, rx0, rx1, rb, bt, rafters } = G;
  const m = Object.assign({ cols: 'new', beams: 'exist', rafters: 'new', base: 'ghostBase', roof: 1 }, o.mode || {});
  const RD = g.rafterDepth, BD = g.beamDepth, h = g.post / 2, L = g.clearL, quiet = !!o.quiet;
  const C = k => ({ new: PAL.newSolid, exist: PAL.existSolid, ghost: '#dfe3e9', check: PAL.check, shore: PAL.shore }[k]);
  const S = k => k === 'ghost' ? { stroke: '#b3bbc8' } : {};
  iso.solid(-10, L + 10, 0, g.roofD + 6, -4, 0, quiet ? '#e4e7eb' : PAL.slab, { order: 0, stroke: quiet ? '#b9c0cb' : null });
  iso.solid(-26, L + 26, -g.wallT, 0, -4, rb(0) + RD + 16, quiet ? '#eef0f2' : PAL.wall, { order: 1, stroke: quiet ? '#b9c0cb' : null });
  for (const op of g.openings) { const z0 = op.sill || 0, z1 = op.head || 80; iso.quad([[op.x0, 0, z0], [op.x1, 0, z0], [op.x1, 0, z1], [op.x0, 0, z1]], quiet ? '#e3eaef' : PAL.glass, { order: 1.5, stroke: '#9fb2c2' }); }
  for (const c of cols) {
    const topZ = (c.line === 'front' ? bt : rb(c.y)) - BD;
    iso.solid(c.x - 2.2, c.x + 2.2, c.y - 2.2, c.y + 2.2, 0, 1, m.cols === 'ghost' ? '#c9ced6' : PAL.steel, { order: 2 });
    iso.solid(c.x - h, c.x + h, c.y - h, c.y + h, 1, topZ, C(m.cols), Object.assign({ order: 2 }, S(m.cols)));
  }
  if (o.shores) for (const i of o.shores) for (const dx of [-11, 11]) iso.solid(G.longX[i] + dx - h, G.longX[i] + dx + h, yo - h, yo + h, 0, bt - BD, PAL.shore, { order: 2 });
  iso.solid(xl - h, xr + h, yo - 1.5, yo + 1.5, bt - BD, bt, C(m.beams), Object.assign({ order: 3 }, S(m.beams)));
  for (const x of [xl, xr]) iso.solid(x - 1.5, x + 1.5, 0, yo - 1.5, y => rb(y) - BD, rb, C(m.beams), Object.assign({ order: 3 }, S(m.beams)));
  iso.solid(rx0, rx1, 0, 1.5, rb(0) - 1, rb(0) + RD, C(m.beams), Object.assign({ order: 3 }, S(m.beams)));
  for (const x of rafters) iso.solid(x - 0.75, x + 0.75, 1.5, g.roofD - 0.75, rb, y => rb(y) + RD, C(m.rafters), Object.assign({ order: 4 }, S(m.rafters)));
  if (m.roof) { const z = y => rb(y) + RD + 1.3, e = g.roofD + 1.5; iso.poly3([[rx0, 0, z(0)], [rx1, 0, z(0)], [rx1, e, z(e)], [rx0, e, z(e)]], m.roof === 'solid' ? 'roofS' : 'roofl'); }
  return iso;
}

// ------------------------------------------------------------------ the job type
// layout.js asks JOB for everything it draws. A new job type is a new file in views/ that defines JOB the same way.
const STEP_PICTURES = {
  verify:  { mode: { cols: 'ghost', beams: 'check', rafters: 'ghost', roof: 0 } },
  shore:   { mode: { cols: 'ghost', beams: 'exist', rafters: 'ghost', roof: 0 }, shores: [1, 2, 3] },
  columns: { mode: { cols: 'new', beams: 'exist', rafters: 'ghost', roof: 0 }, shores: [1, 2, 3] },
  rafters: { mode: { cols: 'ghost', beams: 'exist', rafters: 'new', roof: 0 } },
  roof:    { mode: { cols: 'ghost', beams: 'ghost', rafters: 'ghost', roof: 'solid' } },
  all:     { mode: { cols: 'new', beams: 'exist', rafters: 'new', roof: 0 } },
};
const JOB = {
  type: 'sunroom',
  derive,
  picture: (P, G, o) => isoScene(P, G, o),
  // Label elbows are in the picture's own screen units (see Iso.p). This scene spans about -249..139 by -138..211.
  labels(P, G, iso) {
    const g = P.geometry, h = g.post / 2;
    iso.label(`(N) 2×8 RAFTERS @ ${g.rafterSpacing}" O.C.\nSIMPSON H2.5A EACH END`, [G.rafters[8], 20, G.rb(20) + g.rafterDepth], -64, -118, { kind: 'N', side: 'l' });
    iso.label('(E) RESIDENCE', [40, 0, 112], 42, -130, { side: 'r' });
    iso.label('(E) (2) 2×8 BEAMS, 3 SIDES\nKEEP. CHECK FOR ROT / WDO', [G.xl, G.yo + 1.5, G.bt - 4], 172, 150, { side: 'l' });
    iso.label(`(N) PT 4×4 COLUMNS (${G.cols.length})\nON SIMPSON ABU44Z BASES`, [G.longX[2], G.yo + h, 30], 10, 222, { kind: 'N', side: 'l' });
    iso.label('(E) CONCRETE SLAB', [240, 100, 0], -158, 202, { side: 'l' });
  },
  stepPicture: (P, G, step, k) => isoScene(P, G, Object.assign({ den: 128, id: 'st' + k, quiet: true }, STEP_PICTURES[step.pic] || STEP_PICTURES.all)).svg(),
  field: {
    pictureNote: 'Roof deck and roofing not shown',
    plan:    { title: 'Roof framing plan', den: 24, draw: viewPlan },
    section: { title: 'Section through the sunroom', den: 32, draw: viewSection },
    side:    { title: 'Front elevation', den: 48, draw: viewElevation, note: 'Seen from the yard. Door end on the right' },
    details: [
      { title: 'Column base', den: 4, draw: detailBase, note: (P, G) => 'Typical of ' + G.cols.length },
      { title: 'Rafter, beam and column', den: 4, draw: detailBeam, note: 'At the outer beam' },
      { title: 'Rafter at the house', den: 4, draw: detailHouse, note: 'Existing condition, verify' },
    ],
  },
};
