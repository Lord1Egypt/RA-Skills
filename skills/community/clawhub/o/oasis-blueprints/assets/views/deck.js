// Oasis-Blueprints · https://github.com/oasiseng/Oasis-Blueprints · MIT License, Copyright (c) 2026 Oasis Engineering, LLC
// views/deck.js — job type "deck": a freestanding rectangular deck on posts and footings. All new work.
// x runs along the beams, y runs along the joists, z is up from grade.
// This view is unit-safe: geometry may be in inches or millimetres. Sizes typed here in inches go through I(),
// dimensions are written with FMT(), and each view takes its scale from the layout (den), so the same file
// draws an imperial or a metric project. Use it as the pattern for a new job type.
'use strict';

const I = v => v * UPI;   // inches -> model units

function derive(P) {
  const g = P.geometry, jt = g.joistT, joists = [];
  for (let x = jt / 2; x < g.L - 2 * jt; x += g.joistSpacing) joists.push(x);
  joists.push(g.L - jt / 2);
  const posts = []; for (const y of g.beamY) for (const x of g.postsX) posts.push({ x, y });
  const zJoistTop = g.deckH - g.deckingT, zBeamTop = zJoistTop - g.joistDepth, zPostTop = zBeamTop - g.beamDepth;
  return { joists, posts, zJoistTop, zBeamTop, zPostTop, beamW: g.beamPlies * g.plyT };
}
const breakLine = (v, x0, x1, y) => { const m = (x0 + x1) / 2, a = I(0.35), b = I(0.8); v.poly([[x0 - I(0.7), y], [m - a, y], [m - a / 2, y + b], [m + a / 2, y - b], [m + a, y], [x1 + I(0.7), y]], 'o2', false); };

// ------------------------------------------------------------------ 1  FRAMING PLAN
function viewPlan(P, G, den) {
  const g = P.geometry, v = new View(den, 'plan'), { joists, posts, beamW } = G, h = g.post / 2, jt = g.joistT, L = g.L, D = g.D, px = g.postsX, nx = L + I(13);
  for (const p of posts) v.circle(p.x, p.y, g.footingDia / 2, 'newH');                       // footings, below
  for (const y of g.beamY) v.rect(0, y - beamW / 2, L, y + beamW / 2, 'newH');               // beams, below the joists
  for (const x of joists) v.rect(x - jt / 2, jt, x + jt / 2, D - jt, 'new');
  v.rect(0, 0, L, jt, 'new'); v.rect(0, D - jt, L, D, 'new');                                // rim joists
  for (const p of posts) v.rect(p.x - h, p.y - h, p.x + h, p.y + h, 'newS');
  // dimensions
  const xs = [0].concat(px, [L]), ys = [0].concat(g.beamY, [D]);
  for (let i = 0; i < xs.length - 1; i++) v.dimH(xs[i], xs[i + 1], D + I(11), D);
  v.dimH(0, L, D + I(21), D, { text: FMT(L) + ' OUT TO OUT' });
  for (let i = 0; i < ys.length - 1; i++) v.dimV(ys[i], ys[i + 1], -I(11), 0);
  v.dimV(0, D, -I(22), 0, { text: FMT(D) + ' OUT TO OUT' });
  // notes, all on the right
  const foot = answer(P, 'footing'), last = px[px.length - 1], top = g.beamY[g.beamY.length - 1], bot = g.beamY[0];
  v.note(`(N) ${g.joistName} JOISTS\n@ ${FMT(g.joistSpacing)} O.C.`, L - jt / 2, D * 0.5, nx, D * 0.5 + I(6), { side: 'r', kind: 'N' });
  v.note(`(N) ${g.beamName} BEAM\nBELOW JOISTS. SEE ${REF.d2}/${REF.sheet}`, L, top, nx, top + I(3), { side: 'r', kind: 'N' });
  v.note(`(N) ${g.postName} POST\nTYP. OF ${posts.length}. SEE ${REF.d1}/${REF.sheet}`, last + h, bot + h * 0.4, nx, bot + I(22), { side: 'r', kind: 'N' });
  v.note(foot ? '(N) CONCRETE FOOTING:\n' + wrap(foot.toUpperCase(), 26) : 'FOOTING: SIZE, DEPTH\nAND REINFORCING', last + g.footingDia * 0.35, bot - g.footingDia * 0.35, nx, bot - I(8), { side: 'r', kind: foot ? 'N' : 'R' });
  // section cut, between the first two post lines
  const sx = (px[0] + px[1]) / 2 + jt * 2, ty = D + I(27);
  v.line(sx, -I(5), sx, D + I(4), 'cutl'); v.line(sx, ty, sx, ty + I(8), 'cutl2'); v.line(sx, ty + I(8), sx + I(8), ty + I(8), 'cutl2'); v.arrow(sx + I(8), ty + I(8), sx, ty + I(8));
  v.bubble(sx - I(10), ty + I(6), String(REF.section), REF.sheet);
  return v.svg();
}

// ------------------------------------------------------------------ 2  SECTION (cut along the joists)
function viewSection(P, G, den) {
  const g = P.geometry, v = new View(den, 'sect'), { zJoistTop, zBeamTop, zPostTop, beamW } = G, h = g.post / 2, jt = g.joistT, D = g.D, fd = g.footingDia / 2, fz = g.footingDepth, nx = D + I(20);
  v.line(-I(22), 0, D + I(16), 0, 'o');                                                      // grade
  for (const y of g.beamY) {
    v.rect(y - fd, -fz, y + fd, I(1), 'new', { fill: v.pat('conc') });
    v.rect(y - h - I(0.3), I(1), y + h + I(0.3), I(2), 'steel');
    v.rect(y - h, I(2), y + h, zPostTop, 'new');
    for (let k = 0; k < g.beamPlies; k++) v.lumber(y - beamW / 2 + k * g.plyT, zPostTop, y - beamW / 2 + (k + 1) * g.plyT, zBeamTop, 'new');
  }
  v.rect(jt, zBeamTop, D - jt, zJoistTop, 'new'); v.lumber(0, zBeamTop, jt, zJoistTop, 'new'); v.lumber(D - jt, zBeamTop, D, zJoistTop, 'new');
  v.rect(-I(1), zJoistTop, D + I(1), g.deckH, 'new');                                        // decking
  const ys = [0].concat(g.beamY, [D]);
  for (let i = 0; i < ys.length - 1; i++) v.dimH(ys[i], ys[i + 1], -fz - I(9), -fz);
  v.datum(`TOP OF DECK\n${FMT(g.deckH, true)}`, -I(14), g.deckH, -I(1)); v.datum('FINISHED GRADE\n' + FMT(0), -I(14), 0, -I(8));
  const foot = answer(P, 'footing'), y1 = g.beamY[g.beamY.length - 1];
  v.note(`(N) ${g.deckingName} DECKING`, D * 0.8, g.deckH, nx, g.deckH + I(9), { side: 'r', kind: 'N' });
  v.note(`(N) ${g.joistName} JOISTS\n@ ${FMT(g.joistSpacing)} O.C.`, D - jt * 3, zJoistTop - g.joistDepth / 2, nx, zJoistTop - I(2), { side: 'r', kind: 'N' });
  v.note(`(N) ${g.beamName} BEAM\nSEE ${REF.d2}/${REF.sheet}`, y1 + beamW / 2, zBeamTop - g.beamDepth / 2, nx, zBeamTop - I(10), { side: 'r', kind: 'N' });
  v.note(`(N) ${g.postName} POST ON\nPOST BASE. SEE ${REF.d1}/${REF.sheet}`, y1 + h, I(5), nx, -I(3), { side: 'r', kind: 'N' });
  v.note(foot ? '(N) CONCRETE FOOTING:\n' + wrap(foot.toUpperCase(), 26) : 'FOOTING: SIZE, DEPTH\nAND REINFORCING', y1 + fd * 0.6, -fz * 0.6, nx, -fz * 0.75, { side: 'r', kind: foot ? 'N' : 'R' });
  return v.svg();
}

// ------------------------------------------------------------------ 3  POST BASE AND FOOTING
function detailBase(P, G, den) {
  const g = P.geometry, v = new View(den, 'base'), h = g.post / 2, fd = Math.min(g.footingDia / 2, I(9)), top = I(11.5), bot = -I(5.5);
  v.rect(-fd, bot, fd, I(1), 'new', { fill: v.pat('conc') }); breakLine(v, -fd, fd, bot);
  v.line(-fd - I(6), 0, -fd, 0, 'o'); v.line(fd, 0, fd + I(6), 0, 'o');                      // grade
  v.rect(-h - I(0.3), I(1), h + I(0.3), I(2), 'steel'); v.rect(-h - I(0.3), I(2), -h, I(7), 'steel'); v.rect(h, I(2), h + I(0.3), I(7), 'steel');
  v.rect(-h, I(2), h, top, 'newF'); v.poly([[-h, top], [-h, I(2)], [h, I(2)], [h, top]], 'new', false); breakLine(v, -h, h, top);
  const base = answer(P, 'postBase'), foot = answer(P, 'footing');
  v.line(0, I(2.6), 0, -I(4), base ? 'anchOk' : 'anch'); v.line(-I(0.55), I(2.6), I(0.55), I(2.6), base ? 'anchOk' : 'anch');
  v.note(`(N) ${g.postName} POST`, h, I(9.6), I(5.6), I(10.4), { kind: 'N' });
  v.note(base ? 'POST BASE AND ANCHOR:\n' + wrap(base.toUpperCase(), 34) : 'POST BASE AND ANCHOR:\nMODEL, ANCHOR SIZE, EMBEDMENT', h + I(0.3), I(4.5), I(5.6), I(7.4), { kind: base ? 'N' : 'R' });
  v.note(foot ? '(N) CONCRETE FOOTING:\n' + wrap(foot.toUpperCase(), 34) : 'FOOTING: SIZE, DEPTH,\nREINFORCING, BEARING', fd * 0.7, -I(3.4), I(5.6), -I(3), { kind: foot ? 'N' : 'R' });
  v.note('FINISHED GRADE', -fd - I(3), 0, -I(7.4) - fd * 0.3, I(4), { side: 'l' });
  v.note('TOP OF FOOTING\nABOVE GRADE', -fd * 0.6, I(1), -I(7.4) - fd * 0.3, I(8), { side: 'l' });
  return v.svg();
}

// ------------------------------------------------------------------ 4  JOIST, BEAM AND POST
function detailBeam(P, G, den) {
  const g = P.geometry, v = new View(den, 'beam'), h = g.post / 2, bw = G.beamW, pt = I(4), bt = pt + g.beamDepth, jt = bt + g.joistDepth, x0 = -I(10.5), x1 = I(10.5);
  v.rect(-h, 0, h, pt, 'newF'); v.poly([[-h, 0], [-h, pt], [h, pt], [h, 0]], 'new', false); breakLine(v, -h, h, 0);
  for (let k = 0; k < g.beamPlies; k++) v.lumber(-bw / 2 + k * g.plyT, pt, -bw / 2 + (k + 1) * g.plyT, bt, 'new');
  v.rect(-h - I(0.2), pt - I(0.2), h + I(0.2), pt, 'steel'); v.rect(-bw / 2 - I(0.2), pt, -bw / 2, pt + I(3.5), 'steel'); v.rect(bw / 2, pt, bw / 2 + I(0.2), pt + I(3.5), 'steel');
  v.rect(-h - I(0.2), pt - I(3), -h, pt, 'steel'); v.rect(h, pt - I(3), h + I(0.2), pt, 'steel');
  v.rect(x0, bt, x1, jt, 'newF'); v.line(x0, bt, x1, bt, 'new'); v.line(x0, jt, x1, jt, 'new');
  for (const x of [x0, x1]) v.poly([[x, bt - I(0.6)], [x - I(0.35), bt + g.joistDepth * 0.3], [x + I(0.35), bt + g.joistDepth * 0.7], [x, jt + I(0.6)]], 'o2', false);
  v.rect(x0 + I(0.4), jt, x1 - I(0.4), jt + g.deckingT, 'new');
  const cap = answer(P, 'postCap'), tie = answer(P, 'joistToBeam');
  v.note(`(N) ${g.deckingName} DECKING`, I(6), jt + g.deckingT, I(12.6), jt + I(3.4), { kind: 'N' });
  v.note(`(N) ${g.joistName} JOIST @ ${FMT(g.joistSpacing)} O.C.`, I(8), bt + g.joistDepth * 0.55, I(12.6), bt + g.joistDepth * 0.35, { kind: 'N' });
  v.note(tie ? 'JOIST TO BEAM:\n' + wrap(tie.toUpperCase(), 34) : 'JOIST-TO-BEAM CONNECTION', bw / 2 + I(0.1), bt, I(12.6), bt - I(2.6), { kind: tie ? 'N' : 'R' });
  v.note(cap ? 'BEAM TO POST:\n' + wrap(cap.toUpperCase(), 34) : 'BEAM-TO-POST CONNECTION', h + I(0.2), pt - I(1.2), I(12.6), pt - I(2), { kind: cap ? 'N' : 'R' });
  v.note(`(N) ${g.beamName} BEAM`, -bw / 2, pt + g.beamDepth * 0.6, -I(12.6), pt + g.beamDepth * 0.8, { side: 'l', kind: 'N' });
  v.note(`(N) ${g.postName} POST`, -h, I(1.6), -I(12.6), I(1.2), { side: 'l', kind: 'N' });
  return v.svg();
}

// ------------------------------------------------------------------ isometric overview and step pictures
// mode: 'new' (blue, this step) | 'done' (grey, built in an earlier step) | 0 (not shown). deck: share of the decking laid, 0 to 1.
function isoScene(P, G, o = {}) {
  const g = P.geometry, iso = new Iso(o.den || 56, o.id || 'iso'), m = Object.assign({ foot: 'new', posts: 'new', beams: 'new', joists: 'new', deck: 0.3, deckAs: 'new' }, o.mode || {});
  const C = k => (k === 'new' ? PAL.newSolid : PAL.existSolid), h = g.post / 2, fd = g.footingDia / 2, L = g.L, D = g.D, jt = g.joistT, bw = G.beamW, pad = I(20);
  iso.solid(-pad, L + pad, -pad, D + pad, -I(3), 0, o.quiet ? '#eceee9' : '#e2e7dc', { order: 0, stroke: '#b7bfae' });   // grade
  for (const p of G.posts) {
    if (m.foot) iso.solid(p.x - fd, p.x + fd, p.y - fd, p.y + fd, 0, I(1.5), m.foot === 'new' ? shade(PAL.newSolid, 0.45) : PAL.slab, { order: 1 });
    if (m.posts) iso.solid(p.x - h, p.x + h, p.y - h, p.y + h, I(1.5), G.zPostTop, C(m.posts), { order: 2 });
  }
  if (m.beams) for (const y of g.beamY) iso.solid(0, L, y - bw / 2, y + bw / 2, G.zPostTop, G.zBeamTop, C(m.beams), { order: 3 });
  if (m.joists) {
    for (const x of G.joists) iso.solid(x - jt / 2, x + jt / 2, jt, D - jt, G.zBeamTop, G.zJoistTop, C(m.joists), { order: 4 });
    iso.solid(0, L, 0, jt, G.zBeamTop, G.zJoistTop, C(m.joists), { order: 4 }); iso.solid(0, L, D - jt, D, G.zBeamTop, G.zJoistTop, C(m.joists), { order: 4.5 });
  }
  if (m.deck) for (let y = 0; y + I(5.5) <= D * m.deck + 0.01; y += I(5.75)) iso.solid(0, L, y, y + I(5.5), G.zJoistTop, g.deckH, m.deckAs === 'new' ? shade(PAL.newSolid, 0.25) : PAL.existSolid, { order: 5 });
  return iso;
}

// ------------------------------------------------------------------ the job type
const STEP_PICTURES = {
  footings: { foot: 'new', posts: 0, beams: 0, joists: 0, deck: 0 },
  posts:    { foot: 'done', posts: 'new', beams: 'new', joists: 0, deck: 0 },
  joists:   { foot: 'done', posts: 'done', beams: 'done', joists: 'new', deck: 0 },
  decking:  { foot: 'done', posts: 'done', beams: 'done', joists: 'done', deck: 1 },
  all:      { deck: 0 },
};
const JOB = {
  type: 'deck',
  derive,
  picture: (P, G, o) => isoScene(P, G, o),
  // Label elbows are in the picture's screen units: [(y - x) * 0.866, (x + y) / 2 - z]. They are worked out from the deck size,
  // and sit above and below the object (not beside it), so the picture can fill the width of its panel.
  labels(P, G, iso) {
    const g = P.geometry, L = g.L, D = g.D, pad = I(20), foot = answer(P, 'footing'), yb = g.beamY[g.beamY.length - 1];
    const left = -(L + pad) * 0.866, right = (D + pad) * 0.866, fx = (D - L) * 0.866, fy = (L + D) / 2 + pad, top = -g.deckH - I(18);   // edges of the scene
    iso.label(`(N) ${g.deckingName} DECKING`, [L * 0.3, D * 0.1, g.deckH], right * 0.15, top, { kind: 'N', side: 'r' });
    iso.label(`(N) ${g.joistName} JOISTS @ ${FMT(g.joistSpacing)} O.C.`, [G.joists[Math.floor(G.joists.length * 0.6)], D * 0.42, G.zJoistTop], left * 0.33, top, { kind: 'N', side: 'l' });
    iso.label(`(N) ${g.postName} POSTS (${G.posts.length})`, [g.postsX[0], yb + g.post / 2, G.zPostTop / 2], right * 0.92, fy * 0.8, { kind: 'N', side: 'l' });
    iso.label(foot ? '(N) CONCRETE FOOTINGS' : 'FOOTINGS: SIZE BY ENGINEER', [g.postsX[1], yb + g.footingDia / 2, I(1)], right * 0.5, fy + I(9), { kind: foot ? 'N' : 'R', side: 'l' });
    iso.label(`(N) ${g.beamName} BEAMS`, [L, yb, G.zBeamTop - g.beamDepth / 2], fx - I(40), fy + I(14), { kind: 'N', side: 'l' });
  },
  stepPicture: (P, G, step, k) => isoScene(P, G, { den: Math.ceil((P.geometry.L + P.geometry.D + I(40)) * 0.866 / UPI / 2.9), id: 'st' + k, quiet: true, mode: Object.assign({ deckAs: 'new' }, STEP_PICTURES[step.pic] || STEP_PICTURES.all) }).svg(),
  field: {
    pictureNote: 'Decking shown cut away',
    planHeight: 9.1,   // inches of the middle column given to the plan; the section takes the rest
    pictureDen: (P, G) => Math.ceil(((P.geometry.L + P.geometry.D) / UPI + 40) * 0.866 / 7.6),   // the picture panel is 8.6 in wide
    coverDen: (P, G) => Math.ceil(((P.geometry.L + P.geometry.D) / UPI + 40) * 0.866 / 6.6),      // the cover's is narrower
    plan:    { title: 'Framing plan', den: 24, draw: viewPlan },
    section: { title: 'Section along the joists', den: 16, draw: viewSection },
    details: [
      { title: 'Post base and footing', den: 4, draw: detailBase, note: (P, G) => 'Typical of ' + G.posts.length },
      { title: 'Joist, beam and post', den: 6, draw: detailBeam, note: 'Typical' },
    ],
  },
};
