// Oasis-Blueprints · https://github.com/oasiseng/Oasis-Blueprints · MIT License, Copyright (c) 2026 Oasis Engineering, LLC
// kit.js — scale-true SVG drawing kit.
// Model units are inches with y up. A view has a scale denominator `den` (model inches per sheet inch):
// ½" = 1'-0" is den 24. Text and line weights are given in sheet points and converted, so they print
// the same size on every view whatever its scale.
'use strict';

const PAL = {
  ink: '#16213a', muted: '#56637a', rule: '#b9c2d0', paper: '#ffffff',
  new: '#1f63d6', newFill: '#cfe0fb', newSolid: '#3b7be0',
  exist: '#6f7a8c', existFill: '#eceff3', existSolid: '#b4bcc9',
  slab: '#d5d9df', wall: '#e9ebee', glass: '#cfe6f5', ghost: '#e6e9ee',
  check: '#f0a928', shore: '#f08c2e', hold: '#e8730c', eor: '#c81d25', steel: '#2b3345',
};

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const r3 = v => Math.round(v * 1000) / 1000;

// 254 -> 21'-2"    257.5 -> 21'-5½"
function ftin(v, approx) {
  const s = Math.round(v * 2) / 2, f = Math.floor(s / 12), i = s - f * 12, w = Math.floor(i), h = i - w > 0;
  return (f ? f + "'-" : '') + w + (h ? '½' : '') + '"' + (approx ? ' ±' : '');
}

// Units. Model geometry is in inches (default) or millimetres. UPI = model units per inch.
// den is what the drafter would say: 24 for ½" = 1'-0", 50 for 1:50.
let UPI = 1, FMT = ftin;
function setUnits(u) { UPI = u === 'mm' ? 25.4 : 1; FMT = u === 'mm' ? ((v, approx) => String(Math.round(v)) + (approx ? ' ±' : '')) : ftin; }
const SCALE_LABEL = { 4: '3" = 1\'-0"', 6: '2" = 1\'-0"', 8: '1½" = 1\'-0"', 12: '1" = 1\'-0"', 16: '¾" = 1\'-0"', 24: '½" = 1\'-0"', 32: '3/8" = 1\'-0"', 48: '¼" = 1\'-0"', 96: '1/8" = 1\'-0"' };
const scaleText = den => UPI === 1 && SCALE_LABEL[den] ? SCALE_LABEL[den] : '1:' + den;
// graphic scale bar, so a print at any size can still be measured
function scaleBar(den) {
  let spec;
  if (UPI === 1) spec = { 4: [[0, '0'], [3, '3"'], [6, '6"'], [12, "1'"]], 6: [[0, '0'], [3, '3"'], [6, '6"'], [12, "1'"]], 8: [[0, '0'], [6, '6"'], [12, "1'"], [24, "2'"]], 12: [[0, '0'], [6, '6"'], [12, "1'"], [24, "2'"]], 16: [[0, '0'], [12, "1'"], [24, "2'"], [36, "3'"]], 24: [[0, '0'], [12, "1'"], [24, "2'"], [48, "4'"]], 32: [[0, '0'], [24, "2'"], [48, "4'"], [72, "6'"]], 48: [[0, '0'], [24, "2'"], [48, "4'"], [96, "8'"]], 96: [[0, '0'], [48, "4'"], [96, "8'"], [192, "16'"]] }[den];
  else { const L = [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000].filter(v => v / (den * UPI) <= 2.4).pop(), t = v => v >= 1000 ? (v / 1000) + ' m' : v + ' mm'; if (L) spec = [[0, '0'], [L / 4, t(L / 4)], [L / 2, t(L / 2)], [L, t(L)]]; }
  if (!spec) return '';
  const k = den * UPI, L = spec[spec.length - 1][0] / k, h = 0.06; let s = '';
  for (let i = 0; i < spec.length - 1; i++) { const a = spec[i][0] / k, b = spec[i + 1][0] / k; s += `<rect x="${r3(a)}" y="0" width="${r3(b - a)}" height="${h}" fill="${i % 2 ? '#fff' : PAL.ink}" stroke="${PAL.ink}" stroke-width="0.008"/>`; }
  for (const [v, t] of spec) s += `<text x="${r3(v / k)}" y="${h + 0.115}" font-size="0.1" text-anchor="middle" fill="${PAL.muted}" font-weight="600">${esc(t)}</text>`;
  return `<svg class="sbar" width="${r3(L + 0.5)}in" height="0.22in" viewBox="-0.25 -0.01 ${r3(L + 0.5)} 0.22" xmlns="http://www.w3.org/2000/svg">${s}</svg>`;
}

const TEXT_PT = { t: 10.5, ts: 9, tb: 11.5, th: 13.5, td: 10, tN: 10.5, tR: 10.5, tm: 9 };

class View {
  constructor(den, id) { this.den = den; this.id = id; this.u = den * UPI / 72; this.out = []; this.defs = []; this.bb = [1e9, 1e9, -1e9, -1e9]; this.pats = {}; }
  pt(n) { return n * this.u; }
  ext(x, y) { const b = this.bb; if (x < b[0]) b[0] = x; if (y < b[1]) b[1] = y; if (x > b[2]) b[2] = x; if (y > b[3]) b[3] = y; }
  _st(o) { return o && o.fill ? ` style="fill:${o.fill}"` : ''; }
  line(x1, y1, x2, y2, cls = 'o') { this.ext(x1, y1); this.ext(x2, y2); this.out.push(`<line class="${cls}" x1="${r3(x1)}" y1="${r3(-y1)}" x2="${r3(x2)}" y2="${r3(-y2)}"/>`); return this; }
  poly(pts, cls = 'o', close = true, o) { for (const p of pts) this.ext(p[0], p[1]); this.out.push(`<${close ? 'polygon' : 'polyline'} class="${cls}${close ? '' : ' nf'}" points="${pts.map(p => r3(p[0]) + ',' + r3(-p[1])).join(' ')}"${this._st(o)}/>`); return this; }
  rect(x0, y0, x1, y1, cls = 'o', o) { return this.poly([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], cls, true, o); }
  circle(x, y, r, cls = 'o') { this.ext(x - r, y - r); this.ext(x + r, y + r); this.out.push(`<circle class="${cls}" cx="${r3(x)}" cy="${r3(-y)}" r="${r3(r)}"/>`); return this; }
  arc(cx, cy, r, a0, a1, cls = 'o') { // degrees, counter-clockwise
    const p = a => [cx + r * Math.cos(a * Math.PI / 180), cy + r * Math.sin(a * Math.PI / 180)], s = p(a0), e = p(a1);
    this.ext(s[0], s[1]); this.ext(e[0], e[1]);
    this.out.push(`<path class="${cls} nf" d="M${r3(s[0])} ${r3(-s[1])}A${r3(r)} ${r3(r)} 0 ${a1 - a0 > 180 ? 1 : 0} 0 ${r3(e[0])} ${r3(-e[1])}"/>`); return this; }
  // lumber cut in section: outline plus the X
  lumber(x0, y0, x1, y1, cls) { this.rect(x0, y0, x1, y1, cls); this.line(x0, y0, x1, y1, cls + ' xx'); this.line(x0, y1, x1, y0, cls + ' xx'); return this; }
  text(s, x, y, o = {}) {
    const cls = o.cls || 't', size = this.pt(o.size || TEXT_PT[cls] || 10.5), lines = String(s).split('\n'), lh = (o.lh || 1.2) * size, anchor = o.anchor || 'start', rot = o.rot || 0;
    this.ext(x, y); this.ext(x, y - (lines.length - 1) * lh);
    const tr = rot ? ` transform="rotate(${-rot} ${r3(x)} ${r3(-y)})"` : '';
    this.out.push(`<text class="${cls}" font-size="${r3(size)}" x="${r3(x)}" y="${r3(-y)}" text-anchor="${anchor}"${tr}>${lines.map((l, i) => `<tspan x="${r3(x)}" dy="${i ? r3(lh) : 0}">${esc(l)}</tspan>`).join('')}</text>`); return this; }
  arrow(tx, ty, fx, fy, cls = 'dot') { // filled arrowhead at (tx,ty) pointing away from (fx,fy)
    const a = Math.atan2(ty - fy, tx - fx), L = this.pt(6), w = this.pt(1.9), bx = tx - L * Math.cos(a), by = ty - L * Math.sin(a);
    return this.poly([[tx, ty], [bx - w * Math.sin(a), by + w * Math.cos(a)], [bx + w * Math.sin(a), by - w * Math.cos(a)]], cls); }
  // horizontal dimension: dim line at y, extension lines rising from yo
  dimH(x1, x2, y, yo, o = {}) {
    const d = y >= yo ? 1 : -1, g = this.pt(2.5), e = this.pt(3.5), t = this.pt(3);
    for (const x of [x1, x2]) { this.line(x, yo + d * g, x, y + d * e, 'dm'); this.line(x - t, y - t, x + t, y + t, 'dmt'); }
    this.line(x1, y, x2, y, 'dm');
    return this.text(o.text != null ? o.text : FMT(Math.abs(x2 - x1), o.approx), (x1 + x2) / 2, y + this.pt(3), { cls: 'td', anchor: 'middle' }); }
  dimV(y1, y2, x, xo, o = {}) {
    const d = x >= xo ? 1 : -1, g = this.pt(2.5), e = this.pt(3.5), t = this.pt(3);
    for (const y of [y1, y2]) { this.line(xo + d * g, y, x + d * e, y, 'dm'); this.line(x - t, y - t, x + t, y + t, 'dmt'); }
    this.line(x, y1, x, y2, 'dm');
    return this.text(o.text != null ? o.text : FMT(Math.abs(y2 - y1), o.approx), x - this.pt(3), (y1 + y2) / 2, { cls: 'td', anchor: 'middle', rot: 90 }); }
  // leader note. kind: undefined (ink), 'N' (new work, blue), 'R' (engineer still owes this, red + triangle)
  note(s, tx, ty, ex, ey, o = {}) {
    const side = o.side || (ex >= tx ? 'r' : 'l'), k = side === 'r' ? 1 : -1, kind = o.kind || '', cls = kind === 'N' ? 'tN' : kind === 'R' ? 'tR' : 't';
    const size = this.pt(TEXT_PT[cls]), sh = this.pt(9) * k;
    this.poly([[tx, ty], [ex, ey], [ex + sh, ey]], 'ld' + (kind === 'R' ? ' ldR' : ''), false);
    if (o.mark !== 'none') this.circle(tx, ty, this.pt(1.5), 'dot' + (kind === 'R' ? ' dotR' : ''));
    let x = ex + sh + this.pt(3) * k;
    if (kind === 'R') { const w = this.pt(9), h = this.pt(8.5), x0 = side === 'r' ? x : x - w, yb = ey - h * 0.45;
      this.poly([[x0, yb], [x0 + w, yb], [x0 + w / 2, yb + h]], 'eorT'); this.text('!', x0 + w / 2, yb + h * 0.14, { cls: 'eorX', size: 7.5, anchor: 'middle' }); x += (w + this.pt(3)) * k; }
    return this.text(s, x, ey - size * 0.34, { cls, anchor: side === 'r' ? 'start' : 'end' }); }
  // elevation datum: target symbol with a level line and a two-line label
  datum(s, x, y, toX) {
    const r = this.pt(4.5), k = toX >= x ? 1 : -1;
    this.line(x + r * k, y, toX, y, 'dm'); this.circle(x, y, r, 'o2'); this.line(x - r * 1.5, y, x + r * 1.5, y, 'o2'); this.line(x, y - r * 1.5, x, y + r * 1.5, 'o2');
    this.out.push(`<path class="dot" d="M${r3(x)} ${r3(-y)}L${r3(x + r)} ${r3(-y)}A${r3(r)} ${r3(r)} 0 0 0 ${r3(x)} ${r3(-y - r)}Z"/><path class="dot" d="M${r3(x)} ${r3(-y)}L${r3(x - r)} ${r3(-y)}A${r3(r)} ${r3(r)} 0 0 0 ${r3(x)} ${r3(-y + r)}Z"/>`);
    const lines = String(s).split('\n'), size = this.pt(TEXT_PT.ts);
    return this.text(s, x - k * this.pt(9), y + size * (lines.length - 1) * 1.2 + this.pt(3), { cls: 'ts', anchor: k > 0 ? 'end' : 'start' }); }
  // detail / section reference bubble: number over sheet
  bubble(x, y, num, sheet) {
    const r = this.pt(11); this.circle(x, y, r, 'bub'); this.line(x - r, y, x + r, y, 'o2');
    this.text(num, x, y + this.pt(2.2), { cls: 'tb', size: 9.5, anchor: 'middle' }); return this.text(sheet, x, y - this.pt(8.2), { cls: 'tm', size: 7, anchor: 'middle' }); }
  pat(name) {
    if (this.pats[name]) return this.pats[name];
    const id = name + '-' + this.id, u = this.u, f = r3; let d = '';
    if (name === 'wall') { const s = 5.5 * u; d = `<pattern id="${id}" width="${f(s)}" height="${f(s)}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="${f(s)}" height="${f(s)}" fill="#f1f3f5"/><line x1="0" y1="0" x2="0" y2="${f(s)}" stroke="${PAL.exist}" stroke-width="${f(0.7 * u)}"/></pattern>`; }
    if (name === 'conc') { const s = 44 * u, c = (x, y, r) => `<circle cx="${f(x * u)}" cy="${f(y * u)}" r="${f(r * u)}"/>`, t = (x, y) => `<path d="M${f(x * u)} ${f(y * u)}l${f(4 * u)} ${f(1 * u)}l${f(-3 * u)} ${f(3 * u)}z"/>`;
      d = `<pattern id="${id}" width="${f(s)}" height="${f(s)}" patternUnits="userSpaceOnUse"><rect width="${f(s)}" height="${f(s)}" fill="${PAL.slab}"/><g fill="${PAL.ink}" opacity=".5">${c(5, 7, .8)}${c(19, 4, .6)}${c(33, 11, .8)}${c(40, 27, .6)}${c(12, 22, .7)}${c(25, 30, .8)}${c(7, 38, .6)}${c(36, 40, .7)}${c(21, 41, .6)}${c(28, 17, .5)}</g><g fill="none" stroke="${PAL.ink}" stroke-width="${f(.5 * u)}" opacity=".5">${t(14, 11)}${t(33, 31)}${t(8, 28)}</g></pattern>`; }
    this.defs.push(d); return (this.pats[name] = `url(#${id})`); }
  svg(o = {}) {
    const p = this.pt(o.pad == null ? 4 : o.pad), [x0, y0, x1, y1] = this.bb, W = x1 - x0 + 2 * p, H = y1 - y0 + 2 * p;
    return `<svg class="sk" data-den="${this.den}" style="--u:${r3(this.u)}" width="${r3(W / (this.den * UPI))}in" height="${r3(H / (this.den * UPI))}in" viewBox="${r3(x0 - p)} ${r3(-y1 - p)} ${r3(W)} ${r3(H)}" xmlns="http://www.w3.org/2000/svg"><defs>${this.defs.join('')}</defs>${this.out.join('')}</svg>`; }
}

// ---- library details: drawings converted from CAD and kept as data (schema oasis-blueprints/detail/0.1) ----
// D.prims holds, in inches from the detail's own origin: P polylines, W wide lines (rebar), C circles, F filled shapes,
// H hatches, R leader arrowheads and T text (already broken into lines, each with the width it was drawn at).
// D.st is the pen table [pen in 1/100 mm, dash, grey]; D.pats the hatch patterns. libSvg draws one detail at its own
// scale, D.den, with the kit's pens and fonts. Nothing here is a size or a value: it redraws what the source drawing shows.
// Hatches are drawn as real lines clipped to their boundary (no pattern fills), so the PDF stays small and sharp.
const LIB_DASH = { h: [4, 2.5], c: [13, 3, 3, 3], d: [7, 3.5], p: [15, 3, 3, 3, 3, 3], t: [0.6, 2.6] };
function libSvg(D, o = {}) {
  const v = new View(D.den, 'lib' + (o.key || D.id)), u = v.u, K = UPI, q = u / K, f = n => r3(n * K), Y = y => r3(-y * K), col = g => g === 1 ? PAL.exist : g === 2 ? PAL.existSolid : PAL.ink;
  const pen = s => Math.max(0.4, Math.min(2.1, s[0] * 0.0283 * 1.05));   // 1/100 mm -> points
  const hat = [], fill = [], wide = [], path = {}, arrows = [], text = [];
  const run = (p, i0, close) => { let d = ''; for (let i = i0; i < p.length; i += 2) { v.ext(p[i] * K, p[i + 1] * K); d += (i === i0 ? 'M' : 'L') + f(p[i]) + ' ' + Y(p[i + 1]); } return d + (close ? 'Z' : ''); };
  // one family of parallel hatch lines across a box: every line starts from the family's base point, dashes staggered line by line
  const famLines = (fm, g, bb) => { const c = Math.cos(fm.a), s = Math.sin(fm.a); let sp = fm.s; if (!(sp > 1e-9)) return ''; const m = Math.max(1, Math.ceil(1.7 * q / sp)); sp *= m; const dl = -fm.sh * m;   // never closer than 1.7 pt on paper
    const cs = [[bb[0], bb[1]], [bb[2], bb[1]], [bb[2], bb[3]], [bb[0], bb[3]]].map(([x, y]) => [(x - fm.bx) * c + (y - fm.by) * s, -(x - fm.bx) * s + (y - fm.by) * c]);
    const t0 = Math.min(...cs.map(z => z[0])), t1 = Math.max(...cs.map(z => z[0])), n0 = Math.ceil(Math.min(...cs.map(z => z[1])) / sp), n1 = Math.floor(Math.max(...cs.map(z => z[1])) / sp); if (n1 - n0 > 2500) return '';
    const dash = fm.dash || [], L = dash.reduce((a, b) => a + Math.abs(b), 0), P = (t, n) => f(fm.bx + t * c - n * s) + ' ' + Y(fm.by + t * s + n * c); let d = '', dots = '', count = 0;
    for (let j = n0; j <= n1; j++) { const n = j * sp, X0 = fm.bx - n * s, Y0 = fm.by + n * c; let ta = t0, tb = t1;   // keep each line inside the box, so the drawing's extents stay true
      if (Math.abs(c) > 1e-9) { const a = (bb[0] - X0) / c, b = (bb[2] - X0) / c; ta = Math.max(ta, Math.min(a, b)); tb = Math.min(tb, Math.max(a, b)); } else if (X0 < bb[0] || X0 > bb[2]) continue;
      if (Math.abs(s) > 1e-9) { const a = (bb[1] - Y0) / s, b = (bb[3] - Y0) / s; ta = Math.max(ta, Math.min(a, b)); tb = Math.min(tb, Math.max(a, b)); } else if (Y0 < bb[1] || Y0 > bb[3]) continue;
      if (!(tb > ta)) continue; if (!dash.length || L < 1e-9) { d += 'M' + P(ta, n) + 'L' + P(tb, n); continue; }
      let t = ta - ((((ta - j * dl) % L) + L) % L);
      while (t < tb && count < 15000) for (const z of dash) { if (z > 0) { if (t + z > ta && t < tb) { d += 'M' + P(Math.max(t, ta), n) + 'L' + P(Math.min(t + z, tb), n); count++; } t += z; } else if (z === 0) { if (t >= ta && t <= tb) { dots += 'M' + P(t, n) + 'h0'; count++; } } else t -= z; } }
    return (d ? `<path d="${d}" fill="none" stroke="${col(g)}" stroke-width="${r3(0.38 * u)}"/>` : '') + (dots ? `<path d="${dots}" fill="none" stroke="${col(g)}" stroke-width="${r3(0.9 * u)}" stroke-linecap="round"/>` : ''); };
  // stipple for concrete and sand, sized on paper so it reads the same at every scale
  const stipple = (kind, bb) => { const T = 44 * q, A = [[5, 7], [33, 11], [25, 30], [12, 22], [36, 40]], B = [[19, 4], [40, 27], [7, 38], [21, 41], [28, 17]], TR = [[14, 11], [33, 31], [8, 28]]; let a = '', b = '', t = '';
    const i0 = Math.floor(bb[0] / T), i1 = Math.floor(bb[2] / T), j0 = Math.floor(bb[1] / T), j1 = Math.floor(bb[3] / T); if ((i1 - i0 + 1) * (j1 - j0 + 1) > 1200) return '';
    for (let i = i0; i <= i1; i++) for (let j = j0; j <= j1; j++) { const ox = i * T, oy = j * T; const inb = (x, y, m) => x >= bb[0] + m && x <= bb[2] - m && y >= bb[1] + m && y <= bb[3] - m;   // only what lies inside the box
      for (const [x, y] of A) if (inb(ox + x * q, oy + y * q, 0)) a += `M${f(ox + x * q)} ${Y(oy + y * q)}h0`; for (const [x, y] of B) if (inb(ox + x * q, oy + y * q, 0)) b += `M${f(ox + x * q)} ${Y(oy + y * q)}h0`;
      if (kind === 'conc') for (const [x, y] of TR) if (inb(ox + x * q, oy + y * q, 4 * q)) t += `M${f(ox + x * q)} ${Y(oy + y * q)}l${r3(4 * u)} ${r3(-u)}l${r3(-3 * u)} ${r3(-3 * u)}z`; }
    return `<g fill="none" stroke="${PAL.ink}" opacity=".55" stroke-linecap="round"><path d="${a}" stroke-width="${r3(1.5 * u)}"/><path d="${b}" stroke-width="${r3(1.1 * u)}"/>${t ? `<path d="${t}" stroke-width="${r3(0.5 * u)}" stroke-linejoin="round"/>` : ''}</g>`; };
  let hn = 0;
  for (const p of D.prims || []) { switch (p[0]) {
    case 'P': { (path[p[1]] || (path[p[1]] = [])).push(run(p, 3, p[2])); break; }
    case 'C': { const x = p[2], y = p[3], r = p[4]; v.ext((x - r) * K, (y - r) * K); v.ext((x + r) * K, (y + r) * K); (path[p[1]] || (path[p[1]] = [])).push(`M${f(x - r)} ${Y(y)}a${f(r)} ${f(r)} 0 1 0 ${f(2 * r)} 0a${f(r)} ${f(r)} 0 1 0 ${f(-2 * r)} 0`); break; }
    case 'W': { const s = D.st[p[1]] || [25, '', 0]; wide.push(`<path d="${run(p, 4, p[3])}" fill="none" stroke="${col(s[2])}" stroke-width="${r3(Math.max(p[2] * K, 0.6 * u))}" stroke-linejoin="round"/>`); break; }
    case 'F': fill.push(`<path d="${run(p, 2, true)}" fill="${col(p[1])}" stroke="none"/>`); break;
    case 'H': { const z = D.pats[p[1]] || {}, d = p[2].map(r => run(r, 0, true)).join('');
      if (z.solid) { hat.push(`<path d="${d}" fill-rule="evenodd" fill="${z.g === 1 ? '#aab1bd' : z.g === 2 ? '#d8dce2' : z.ink ? PAL.ink : '#c2c8d1'}" stroke="none"/>`); break; }
      const bb = [1e9, 1e9, -1e9, -1e9]; for (const r of p[2]) for (let i = 0; i < r.length; i += 2) { bb[0] = Math.min(bb[0], r[i]); bb[1] = Math.min(bb[1], r[i + 1]); bb[2] = Math.max(bb[2], r[i]); bb[3] = Math.max(bb[3], r[i + 1]); }
      const inner = /CONC/.test(z.name) ? stipple('conc', bb) : /SAND|STUCCO|GROUT|CORK|GRAVEL/.test(z.name) || (z.fam || []).length > 6 ? stipple('sand', bb) : (z.fam || []).map(fm => famLines(fm, z.g || 0, bb)).join('');
      if (!inner) break; const id = `hc${hn++}-${v.id}`; v.defs.push(`<clipPath id="${id}"><path d="${d}" clip-rule="evenodd"/></clipPath>`); hat.push(`<g clip-path="url(#${id})">${inner}</g>`); break; }
    case 'R': { const L = 7 * u, w = 1.3 * u, x = p[2] * K, y = p[3] * K, c = Math.cos(p[4]), s = Math.sin(p[4]), bx = x - L * c, by = y - L * s; v.ext(x, y);
      arrows.push(`<path d="M${r3(x)} ${r3(-y)}L${r3(bx - w * s)} ${r3(-(by + w * c))}L${r3(bx + w * s)} ${r3(-(by - w * c))}Z" fill="${col(p[1])}" stroke="none"/>`); break; }
    case 'T': { const x = p[2] * K, y = p[3] * K, h = p[4] * K, rot = p[5], an = p[6] || 'sl', lines = p[7] || [], ws = p[8] || [], LS = h * (p[10] || 1.72), n = lines.length, H = h + (n - 1) * LS;
      const y0 = an[0] === 't' ? h : an[0] === 'm' ? h - H / 2 : an[0] === 'b' ? -0.25 * h - (n - 1) * LS : 0, ta = an[1] === 'r' ? 'end' : an[1] === 'c' ? 'middle' : 'start', size = r3(h / 0.7), c = Math.cos(rot), s = Math.sin(rot);
      const W = Math.max(0, ...ws) * K, xa = an[1] === 'r' ? -W : an[1] === 'c' ? -W / 2 : 0; for (const [a, b] of [[xa, -(y0 - h)], [xa + W, -(y0 - h)], [xa, -(y0 + (n - 1) * LS + 0.3 * h)], [xa + W, -(y0 + (n - 1) * LS + 0.3 * h)]]) v.ext(x + a * c - b * s, y + a * s + b * c);
      const tr = `translate(${r3(x)} ${r3(-y)})` + (Math.abs(rot) > 1e-4 ? ` rotate(${r3(-rot * 180 / Math.PI)})` : ''), sty = (p[9] ? '' : 'font-family:var(--f-body);') + (p[1] ? `fill:${col(p[1])};` : '');
      lines.forEach((l, i) => { if (!l) return; const w = (ws[i] || 0) * K; text.push(`<text class="t" transform="${tr}" font-size="${size}" text-anchor="${ta}" y="${r3(y0 + i * LS)}"${l.length > 1 && w > 0 ? ` textLength="${r3(w)}" lengthAdjust="spacingAndGlyphs"` : ''}${sty ? ` style="${sty}"` : ''}>${esc(l)}</text>`); }); break; }
  } }
  const strokes = Object.keys(path).map(k => { const s = D.st[k] || [25, '', 0], w = pen(s), da = LIB_DASH[s[1]]; return `<path d="${path[k].join('')}" fill="none" stroke="${col(s[2])}" stroke-width="${r3(w * u)}" stroke-linecap="${s[1] === 't' ? 'round' : 'butt'}" stroke-linejoin="round"${da ? ` stroke-dasharray="${da.map(x => r3(x * u)).join(' ')}"` : ''}/>`; });
  v.out.push(hat.join(''), fill.join(''), wide.join(''), strokes.join(''), arrows.join(''), text.join(''));
  return v.svg();
}

// ---- isometric (30° axonometric). x runs left-down, y runs right-down, z is up. Viewer sits at +x, +y, +z. ----
function shade(hex, f) { // f > 0 lightens toward white, f < 0 darkens toward black
  const n = parseInt(hex.slice(1), 16), c = [n >> 16, (n >> 8) & 255, n & 255].map(v => Math.round(f >= 0 ? v + (255 - v) * f : v * (1 + f)));
  return '#' + c.map(v => v.toString(16).padStart(2, '0')).join(''); }

class Iso {
  constructor(den, id) { this.den = den; this.id = id; this.u = den * UPI / 72; this.items = []; this.over = []; }
  pt(n) { return n * this.u; }
  p(x, y, z) { return [(y - x) * 0.8660254, (x + y) * 0.5 - z]; }
  // box or sloped prism: zb / zt may be numbers or functions of y. order = paint layer; within a layer far paints first.
  solid(x0, x1, y0, y1, zb, zt, color, o = {}) { this.items.push({ k: 's', x0, x1, y0, y1, zb, zt, color, order: o.order || 0, key: (x0 + x1 + y0 + y1) / 2, o }); return this; }
  quad(pts, color, o = {}) { this.items.push({ k: 'q', pts, color, order: o.order || 0, key: pts.reduce((a, p) => a + p[0] + p[1], 0) / pts.length, o }); return this; }
  line3(a, b, cls) { const p = this.p(...a), q = this.p(...b); this.over.push(`<line class="${cls}" x1="${r3(p[0])}" y1="${r3(p[1])}" x2="${r3(q[0])}" y2="${r3(q[1])}"/>`); return this; }
  poly3(pts, cls) { this.over.push(`<polygon class="${cls}" points="${pts.map(a => this.p(...a).map(r3).join(',')).join(' ')}"/>`); return this; }
  label(s, at, ex, ey, o = {}) { // leader from a 3D point to an elbow given in screen units; text runs to o.side ('r' or 'l')
    const p = this.p(...at), k = (o.side || (ex >= p[0] ? 'r' : 'l')) === 'r' ? 1 : -1, sh = this.pt(8) * k, cls = o.kind === 'N' ? 'tN' : o.kind === 'R' ? 'tR' : 't', size = this.pt(o.size || 10.5), lines = String(s).split('\n');
    const x = ex + sh + this.pt(3) * k, y = ey + size * 0.34;
    this.over.push(`<polyline class="ld nf" points="${r3(p[0])},${r3(p[1])} ${r3(ex)},${r3(ey)} ${r3(ex + sh)},${r3(ey)}"/><circle class="dot" cx="${r3(p[0])}" cy="${r3(p[1])}" r="${r3(this.pt(1.6))}"/>` +
      `<text class="${cls}" font-size="${r3(size)}" x="${r3(x)}" y="${r3(y)}" text-anchor="${k > 0 ? 'start' : 'end'}">${lines.map((l, i) => `<tspan x="${r3(x)}" dy="${i ? r3(size * 1.2) : 0}">${esc(l)}</tspan>`).join('')}</text>`); return this; }
  svg() {
    const f = (v, y) => typeof v === 'function' ? v(y) : v, sw = r3(this.pt(0.45)), out = [];
    const face = (pts, fill, stroke, op) => `<polygon points="${pts.map(a => this.p(...a).map(r3).join(',')).join(' ')}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round"${op != null ? ` fill-opacity="${op}"` : ''}/>`;
    for (const it of this.items.slice().sort((a, b) => a.order - b.order || a.key - b.key)) {
      const c = it.color, st = it.o.stroke || shade(c, -0.45);
      if (it.k === 'q') { out.push(face(it.pts, c, st, it.o.op)); continue; }
      const { x0, x1, y0, y1 } = it, b0 = f(it.zb, y0), b1 = f(it.zb, y1), t0 = f(it.zt, y0), t1 = f(it.zt, y1);
      out.push(face([[x0, y0, t0], [x1, y0, t0], [x1, y1, t1], [x0, y1, t1]], shade(c, 0.32), st, it.o.op));          // top
      out.push(face([[x1, y0, b0], [x1, y1, b1], [x1, y1, t1], [x1, y0, t0]], shade(c, -0.14), st, it.o.op));         // +x side
      out.push(face([[x0, y1, b1], [x1, y1, b1], [x1, y1, t1], [x0, y1, t1]], c, st, it.o.op));                        // +y side
    }
    return `<svg class="sk iso" data-den="${this.den}" style="--u:${r3(this.u)}" xmlns="http://www.w3.org/2000/svg">${out.join('')}${this.over.join('')}</svg>`; }
}

// wrap a long note to lines of about n characters
function wrap(s, n = 36) { const out = []; for (const para of String(s).split('\n')) { let line = ''; for (const w of para.split(/\s+/)) { if (line && (line + ' ' + w).length > n) { out.push(line); line = w; } else line = line ? line + ' ' + w : w; } out.push(line); } return out.join('\n'); }

if (typeof module !== 'undefined') module.exports = { PAL, esc, r3, ftin, setUnits, scaleText, scaleBar, TEXT_PT, View, Iso, shade, wrap, libSvg };
