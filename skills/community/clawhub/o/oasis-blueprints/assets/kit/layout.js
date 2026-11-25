// Oasis-Blueprints · https://github.com/oasiseng/Oasis-Blueprints · MIT License, Copyright (c) 2026 Oasis Engineering, LLC
// layout.js — builds the sheets from PROJECT. Nothing here knows about a job type: the drawings come from JOB (see views/).
'use strict';

const STATUS = {
  draft:        { band: 'Draft · for engineer review · not for construction', box: ['Draft', 'For engineer review', 'Not for construction'], cls: 'st-draft', issue: false },
  review:       { band: 'Released for review · not for construction', box: ['Released for review', '', 'Not for construction'], cls: 'st-draft', issue: false },
  permit:       { band: '', box: ['Issued for permit', '', ''], cls: 'st-ok', issue: true },
  construction: { band: 'Released for construction', bandCls: 'rel', box: ['Released for construction', '', ''], cls: 'st-ok', issue: true },
};
// View numbers on the field sheet. Set while that sheet is laid out, so a note can say `SEE ${REF.d1}/${REF.sheet}`.
let REF = {};

// ---- open items: things the engineer still owes. An item with an answer is closed.
const isOpen = o => !String(o.answer || '').trim();
function answer(P, key) { const o = (P.openItems || []).find(o => o.key === key); return o ? String(o.answer || '').trim() : ''; }
function openItems(P) {
  const list = (P.openItems || []).filter(isOpen), p = P.project || {}, blank = [];
  if (!p.number) blank.push('project number'); if (!(P.people || {}).drawnBy) blank.push('drawn by'); if (!p.locality) blank.push('city, state and zip');
  if (blank.length) list.push({ title: 'Title block', text: 'Still blank: ' + blank.join(', ') + '.', who: 'Office', auto: true });
  const missingCriteria = (P.criteria || []).filter(c => c.v == null || !String(c.v).trim());
  if (missingCriteria.length && !list.some(o => o.key === 'criteria'))
    list.push({ title: 'Design criteria', text: 'Complete the blank design criteria fields before issue.', who: 'Engineer', auto: true });
  return list;
}
const closedItems = P => (P.openItems || []).filter(o => !isOpen(o));

const val = (x, what) => x ? esc(x) : `<span class="blank">${esc(what || 'to fill')}</span>`;
const chip = (k, t) => `<span class="chip ${k}">${esc(t)}</span>`;
// Text in the project file may use: **bold**, [N] [E] [HOLD] chips, {permit} {relatedPermit},
// and {key}: the answer to the open item with that key, or a red "Engineer" chip while it is open.
function rich(s, P) {
  return esc(s || '').replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\[N\]/g, chip('n', 'New')).replace(/\[E\]/g, chip('e', 'Existing')).replace(/\[EOR\]/g, chip('r', 'Engineer')).replace(/\[HOLD\]/g, chip('h', 'Hold'))
    .replace(/\{(\w+)\}/g, (m, k) => k === 'permit' ? esc(P.project.permit || '') : k === 'relatedPermit' ? esc(P.project.relatedPermit || '') : k in REF ? esc(REF[k])
      : answer(P, k) ? `<b class="ans">${esc(answer(P, k))}</b>` : chip('r', 'Engineer'));
}

function logoHtml(P) {
  const f = P.firm || {};
  if (f.logo) return `<img class="logo" src="${esc(f.logo)}" alt="${esc(f.name || '')}">`;
  const w = String(f.wordmark || f.name || 'Your Company').trim().split(/\s+/);
  const pt = Math.round(38 * Math.min(1, 7 / w[0].length));   // long first words shrink to stay inside the title block
  return `<div class="wm" style="font-size:${pt}pt">${esc(w[0])}</div>${w.length > 1 ? `<div class="wm2">${esc(w.slice(1).join(' '))}</div>` : ''}`;
}

function titleBlock(P, sh, i, n) {
  const p = P.project, f = P.firm || {}, st = STATUS[P.status] || STATUS.draft, open = openItems(P).length, revs = ((P.issue || {}).revisions || []).concat([{}, {}, {}, {}]).slice(0, 4);
  return `<aside class="tb">
  <div class="tb-logo">${logoHtml(P)}<div class="firm">${[f.name].concat(f.lines || []).filter(Boolean).map(esc).join('<br>')}</div></div>
  <div class="tb-proj"><label>Project</label><div class="pt">${esc(p.title)}</div><div class="ps">${esc(p.subtitle || '')}</div><div class="pa">${val(p.address, 'address')}</div><div class="pl">${val(p.locality, 'city, state, zip')}</div>
    <dl>${p.permit ? `<dt>Permit</dt><dd>${esc(p.permit)}</dd>` : ''}${p.relatedPermit ? `<dt>Related</dt><dd>${esc(p.relatedPermit)}${p.relatedScope ? ' · ' + esc(p.relatedScope) : ''}</dd>` : ''}</dl></div>
  <div class="tb-status ${st.cls}"><b>${esc(st.box[0])}</b>${st.box[1] ? `<span>${esc(st.box[1])}</span>` : ''}${st.box[2] ? `<span>${esc(st.box[2])}</span>` : ''}</div>
  ${open ? `<div class="tb-open"><b>${open}</b><span>open item${open > 1 ? 's' : ''} for the engineer.<br>Listed on ${esc(P.sheets[0].no)}. Must be 0 to issue.</span></div>` : ''}
  <div class="tb-seal"><label>Engineer of record · seal, signature, date</label></div>
  <div class="tb-rev"><label>Revisions</label><table><tr><th>No.</th><th>Description</th><th>Date</th></tr>${revs.map(r => `<tr><td>${esc(r.no || '')}</td><td>${esc(r.text || '')}</td><td>${esc(r.date || '')}</td></tr>`).join('')}</table></div>
  <div class="tb-fields"><div><label>Project no.</label>${val(p.number)}</div><div><label>Date</label>${esc((P.issue || {}).date || '')}</div><div><label>Drawn by</label>${val((P.people || {}).drawnBy)}</div><div><label>Checked by</label>${val((P.people || {}).checkedBy)}</div></div>
  <div class="tb-name"><label>Sheet name</label><div>${esc(sh.name)}</div></div>
  <div class="tb-no"><label>Sheet number</label><div class="no">${esc(sh.no)}</div><div class="of">Sheet ${i + 1} of ${n}</div></div>
  <div class="tb-chk"><i></i><span>Full size 24 × 36 in.<br>This square is 1 in × 1 in.</span></div>
</aside>`;
}

function band(P) {
  const st = STATUS[P.status] || STATUS.draft, open = openItems(P).length;
  return st.band ? `<div class="band ${st.bandCls || ''}">${esc(st.band)}${open ? ` · ${open} open item${open > 1 ? 's' : ''}` : ''}</div>` : `<div class="band quiet">${esc(P.project.title)}${P.project.address ? ' · ' + esc(P.project.address) : ''}</div>`;
}
function panel(num, title, den, svg, o = {}) {
  const scale = o.scale || (den ? 'Scale ' + scaleText(den) : '');
  return `<section class="panel ${o.cls || ''}"${o.style ? ` style="${o.style}"` : ''}>${o.top || ''}<div class="view">${svg}</div><footer class="vt"><span class="vb">${num}</span><span class="vn">${esc(title)}</span>${o.note ? `<span class="vx">${esc(o.note)}</span>` : ''}<span class="vs">${esc(scale)}</span>${den && !o.scale ? scaleBar(den) : ''}</footer></section>`;
}
// "credit": true in the project file prints one small grey line in the bottom margin, outside the border. Off unless asked for.
const creditLine = P => P.credit === true && typeof ORIGIN !== 'undefined' ? `<div class="credit">Drawn with ${esc(ORIGIN.name)} · ${esc(String(ORIGIN.site).replace(/^https?:\/\//, '').replace(/\/$/, ''))}</div>` : '';
function sheet(P, sh, i, n, bodyCls, body) {
  return `<article class="sheet" data-sheet="${esc(sh.no)}"><div class="frame"><div class="body ${bodyCls}">${band(P)}${body}</div>${titleBlock(P, sh, i, n)}</div>${creditLine(P)}</article>`;
}

function legendHtml(P) {
  return `<div class="lg">
    <div><i class="sw n"></i><b>(N) New</b><span>${P.project.permit ? 'Work under permit ' + esc(P.project.permit) + '.' : 'New work.'} Blue on every view.</span></div>
    <div><i class="sw e"></i><b>(E) Existing</b><span>Stays in place. Grey on every view.</span></div>
    ${(STATUS[P.status] || {}).issue ? '' : `<div><i class="tri"></i><b>Engineer</b><span>A value or decision the engineer still owes. Do not build from it until it is filled in.</span></div>`}
    <div><i class="hd">Hold</i><b>Hold point</b><span>Stop and get the answer or inspection before going on.</span></div>
    <div><i class="pm">±</i><b>Not confirmed</b><span>Scanned, scaled or assumed. Verify in field (V.I.F.) before cutting.</span></div>
  </div>`;
}
const legendStrip = P => `<div class="lgs"><span><i class="sw n"></i>(N) New work</span><span><i class="sw e"></i>(E) Existing, stays</span>${P && (STATUS[P.status] || {}).issue ? '' : '<span><i class="tri"></i>Engineer still owes this</span>'}<span><i class="hd">Hold</i>Stop and ask</span><span><i class="pm">±</i>Verify in field</span></div>`;

// ---------------------------------------------------------------- the field sheet: picture, steps, plan, section, details
function sheetField(P, G, sh, i, n) {
  const F = JOB.field, dets = F.details || [];
  const num = v => typeof v === 'function' ? v(P, G) : v, S = P.scales || {};
  const pic = JOB.picture(P, G, { den: S.picture || num(F.pictureDen) || 52, id: 'iso' }); if (JOB.labels) JOB.labels(P, G, pic);
  // A view is drawn at the scale in the project file ("scales": { plan, section, side, details, d1.. }) or else the job type's own.
  const view = (spec, key, o = {}) => { const den = S[key] || (key[0] === 'd' && S.details) || spec.den;
    return panel(REF[key], spec.title, den, spec.draw(P, G, den), Object.assign({ note: typeof spec.note === 'function' ? spec.note(P, G) : spec.note }, o)); };
  const facts = (P.facts || []).map(f => `<div class="fact"><div class="k">${esc(f.k)} ${f.tag === 'N' ? chip('n', 'New') : f.tag === 'E' ? chip('e', 'Existing') : f.tag ? chip('o', f.tag) : ''}</div><div class="v ${f.tag === 'N' ? 'vn' : ''}">${esc(f.v)}</div><div class="s">${rich(f.s, P)}</div></div>`).join('');
  const steps = (P.steps || []).map((s, j) => `<div class="step"${JOB.stepPicture ? '' : ' style="grid-template-columns:0.4in 1fr"'}><div class="num">${j + 1}</div>${JOB.stepPicture ? `<div class="pic">${JOB.stepPicture(P, G, s, j)}</div>` : ''}<div class="tx" data-fit><h4>${esc(s.title)}</h4><p>${rich(s.text, P)}</p>${s.hold ? `<p class="hold">${chip('h', 'Hold')} ${rich(s.hold, P)}</p>` : ''}${s.ref ? `<p class="ref">${rich(s.ref, P)}</p>` : ''}</div></div>`).join('');
  const body = `
  <div class="head"><div class="job" data-fit><label>The job</label><h2>${esc(P.summary.headline)}</h2><p>${esc(P.summary.text)}</p></div><div class="facts" style="grid-template-columns:repeat(${Math.max(1, (P.facts || []).length)},1fr)">${facts}</div></div>
  <div class="main">
    <div class="col">
      ${panel('', 'What you are building', 0, pic.svg(), { cls: 'p-iso' + (F.side ? '' : ' grow'), top: legendStrip(P), note: F.pictureNote || '', scale: 'Isometric · not to scale', style: F.side ? `flex:0 0 ${F.pictureHeight || 10.2}in` : '' })}
      ${(F.extras || []).length ? `<div class="xrow" style="flex:0 0 ${F.extrasHeight || 3.7}in;grid-template-columns:${F.extras.map(x => (x.flex || 1) + 'fr').join(' ')}">${F.extras.map((x, j) => view(x, 'x' + (j + 1), x.nts ? { scale: 'Not to scale' } : {})).join('')}</div>` : ''}
      ${F.side ? view(F.side, 'side', { cls: 'grow' }) : ''}
    </div>
    <div class="col">
      ${view(F.plan, 'plan', { style: `flex:0 0 ${F.planHeight || 10}in` })}
      ${view(F.section, 'section', { cls: 'grow' })}
    </div>
    <div class="col">
      <section class="panel grow"><div class="ph">How the job goes</div><div class="steps">${steps}</div><div class="fine" data-fit>${esc(P.summary.sequenceNote || '')}</div></section>
    </div>
  </div>
  <div class="dets" style="grid-template-columns:repeat(${Math.max(1, dets.length)},1fr)">${dets.map((d, j) => view(d, 'd' + (j + 1))).join('')}</div>`;
  return sheet(P, sh, i, n, 's-field', body);
}

// ---------------------------------------------------------------- optional cover blocks: property record, maps, general notes
// "property": { rows: [[label, value]], source, maps: [{ src, title, credit }] }   adds a fifth column to the cover.
function propertyHtml(P) {
  const pr = P.property; if (!pr) return '';
  const rows = (pr.rows || []).map(r => `<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td></tr>`).join('');
  const figs = (pr.maps || []).filter(m => m.src).map(m => `<section class="panel fig"><div class="view"><img src="${esc(m.src)}" alt="${esc(m.title || '')}"></div><footer class="vt"><span class="vn">${esc(m.title || '')}</span><span class="vs">${esc(m.credit || '')}</span></footer></section>`).join('');
  return `<div class="col" data-fit data-name="Property column"><section class="panel grow"><div class="ph">Property</div><div class="pad" data-fit><table class="kv pk">${rows}</table>${pr.source ? `<p class="src">${esc(pr.source)}</p>` : ''}</div></section>${figs}</div>`;
}
// "generalNotes": [{ title, text?, items?: [string | { text, sub?: [string], table?: { head?, rows }, after? }], bullets?, after? }]
// fills the band at the bottom of the cover, set in narrow columns.
function generalNotesHtml(P) {
  const tbl = t => `<table class="gt">${t.head ? `<tr>${t.head.map(h => `<th>${esc(h)}</th>`).join('')}</tr>` : ''}${t.rows.map(r => `<tr>${r.map(c => `<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</table>`;
  const item = it => typeof it === 'string' ? `<li>${rich(it, P)}</li>` : `<li>${rich(it.text, P)}${it.sub ? `<ol type="a">${it.sub.map(x => `<li>${rich(x, P)}</li>`).join('')}</ol>` : ''}${it.table ? tbl(it.table) : ''}${it.after ? `<p>${rich(it.after, P)}</p>` : ''}</li>`;
  return (P.generalNotes || []).map(g => `<h4>${esc(g.title)}</h4>${g.text ? `<p>${rich(g.text, P)}</p>` : ''}${g.items ? `<ol>${g.items.map(item).join('')}</ol>` : ''}${g.bullets ? `<ul>${g.bullets.map(b => `<li>${rich(b, P)}</li>`).join('')}</ul>` : ''}${g.after ? `<p>${rich(g.after, P)}</p>` : ''}${g.image && g.image.src ? `<img class="gimg" src="${esc(g.image.src)}" style="width:${+g.image.width || 1.6}in" alt="${esc(g.image.alt || g.title || '')}">` : ''}`).join('');
}

// ---------------------------------------------------------------- the office sheet: scope, notes, criteria, open items
function sheetCover(P, G, sh, i, n, sheets) {
  const F = JOB.field || {}, cd = (P.scales || {}).cover || (typeof F.coverDen === 'function' ? F.coverDen(P, G) : F.coverDen) || 56, pic = JOB.picture(P, G, { den: cd, id: 'cov' }), st = STATUS[P.status] || STATUS.draft;
  const scope = (P.scope || []).map(s => `<div class="sc ${s.kind}"><div class="sk1">${s.kind === 'n' ? chip('n', 'New') : s.kind === 'e' ? chip('e', 'Existing') : chip('o', s.tag || 'Separate permit')}</div><div><b>${esc(s.item)}</b><span>${rich(s.text, P)}</span></div></div>`).join('');
  const notes = (P.notes || []).map(grp => `<h4>${esc(grp.title)}</h4><ol start="${grp.start || 1}">${grp.items.map(t => `<li>${rich(t, P)}</li>`).join('')}</ol>`).join('');
  const openL = openItems(P), closed = st.issue ? [] : closedItems(P);
  const open = openL.map((o, j) => `<div class="oi"><i class="tri"><b>${j + 1}</b></i><div><b>${esc(o.title)}</b><span>${rich(o.text, P)}</span><em>${esc(o.who || 'Engineer')}</em></div></div>`).join('');
  const done = closed.map(o => `<div class="oi done"><i class="ok"><svg viewBox="0 0 16 16"><path d="M3 8.6l3.2 3L13 4.6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></i><div><b>${esc(o.title)}</b><span>${esc(o.answer)}</span></div></div>`).join('');
  const crit = (P.criteria || []).map(c => `<tr><td>${esc(c.k)}</td><td>${c.v != null && String(c.v).trim() ? esc(c.v) : chip('r', 'Engineer')}</td></tr>`).join('');
  const S0 = P.summary || {};
  const idx = sheets.map(s => `<tr><td><b>${esc(s.no)}</b></td><td>${esc(s.name)}</td><td>${esc(s.what || '')}</td></tr>`).join('');
  const body = `
  <div class="cover${P.property ? ' c5' : ''}${st.issue && !openL.length ? ' noopen' : ''}">
    <div class="ctop"${S0.coverTop ? ` style="flex-basis:${+S0.coverTop}in"` : ''}>
      <div class="col">
        <section class="panel"><div class="pad job big" data-fit><label>The job</label><h2>${esc(P.summary.headline)}</h2><p>${esc(P.summary.text)}</p>${P.project.use ? `<p class="use">${esc(P.project.use)}</p>` : ''}</div></section>
        ${panel('', 'What this set covers', 0, pic.svg(), { cls: 'p-iso grow', note: 'Blue is new work', scale: 'Isometric · not to scale' })}
        <section class="panel"><div class="ph">How to read this set</div><div class="pad" data-fit>${legendHtml(P)}<p class="how">${esc(P.summary.howToRead || '')}</p></div></section>
      </div>
      <div class="col">
        <section class="panel"><div class="ph">Scope</div><div class="pad" data-fit>${scope}</div></section>
        <section class="panel"><div class="ph">Design criteria</div><div class="pad" data-fit><table class="kv">${crit}</table></div></section>
        <section class="panel grow"><div class="ph">Sheet index</div><div class="pad" data-fit><table class="idx">${idx}</table></div></section>
      </div>
      <div class="col">
        <section class="panel grow"><div class="ph">${esc(S0.notesTitle || 'Notes for this job')}</div><div class="pad notes${S0.notesSize ? ' fs' : ''}" data-fit${S0.notesSize ? ` style="font-size:${+S0.notesSize}pt"` : ''}>${notes}</div></section>
      </div>
      ${st.issue && !openL.length ? '' : `      <div class="col">
        <section class="panel grow"><div class="ph ${openL.length ? 'red' : ''}">Open items for the engineer · ${openL.length || 'none'}</div><div class="pad" data-fit>${open}${openL.length ? `<p class="how">The set cannot be issued for permit or construction while this list has entries. Each item also shows in red where it applies on the drawings.</p>` : ''}${done ? `<h4 class="oih">Recorded answers</h4>${done}` : ''}</div></section>
      </div>`}
      ${propertyHtml(P)}
    </div>
    ${(P.generalNotes || []).length
      ? `<section class="panel gnotes"><div class="ph">${esc(S0.generalNotesTitle || 'General notes')}</div><div class="pad gn" data-fit style="columns:${+S0.generalNotesColumns || 8}${S0.generalNotesSize ? `;font-size:${+S0.generalNotesSize}pt` : ''}">${generalNotesHtml(P)}</div></section>`
      : `<section class="panel reserved"><div class="ph">${esc(S0.reservedTitle || "Reserved: engineer's general structural notes")}</div><div class="pad" data-fit><p>${esc(S0.reserved || '')}</p></div></section>`}
  </div>`;
  return sheet(P, sh, i, n, 's-cover', body);
}

// ---------------------------------------------------------------- a reserved sheet (site plan by others, etc.)
function sheetReserved(P, G, sh, i, n) {
  return sheet(P, sh, i, n, 's-res', `<div class="resv"><div><h2>${esc(sh.name)}</h2><p>${esc(sh.what || '')}</p></div></div>`);
}

// ---------------------------------------------------------------- a sheet of figures: reference details supplied as images
// sheet: { type: "figures", intro?, ppi?, figures: [{ src, title, note?, scale? }] }. Each image is shown at `ppi` pixels per inch
// (72 by default) so screenshots are not blown up, and numbered 1, 2, 3 on this sheet.
function sheetFigures(P, G, sh, i, n) {
  const figs = (sh.figures || []).filter(f => f.src), zoom = 96 / (+sh.ppi || 72);
  const body = `${sh.intro ? `<div class="figintro" data-fit>${rich(sh.intro, P)}</div>` : ''}
  <div class="figs" data-fit data-name="Figures" style="--figzoom:${zoom.toFixed(4)}">${figs.map((f, j) => `<section class="panel figp"><div class="view"><img src="${esc(f.src)}" alt="${esc(f.title || '')}"></div><footer class="vt"><span class="vb">${j + 1}</span><span class="vn">${esc(f.title || '')}</span>${f.note ? `<span class="vx">${esc(f.note)}</span>` : ''}<span class="vs">${esc(f.scale || 'Not to scale')}</span></footer></section>`).join('')}</div>`;
  return sheet(P, sh, i, n, 's-figs', body);
}

// ---------------------------------------------------------------- a sheet of library details
// sheet: { type: "details", details: ["id", { id, title?, note? }], intro? }. The details come from the library the project
// names ("library": "<folder>"); build.py embeds the ones used under P.library.details. Each is drawn at its own scale and
// numbered 1, 2, 3 on this sheet. Rows fill left to right in the order given; a detail that does not fit starts the next row.
function libDetail(P, ref) { const r = typeof ref === 'string' ? { id: ref } : ref || {}, D = ((P.library || {}).details || {})[r.id]; return D ? { D, title: r.title || D.title, note: r.note || '' } : { missing: r.id || '?' }; }
function sheetDetails(P, G, sh, i, n) {
  const W = 31.8, GAP = 0.12, rows = [[]]; let x = 0, k = 0;
  for (const it of (sh.details || []).map(r => libDetail(P, r))) { const D = it.D; it.w = Math.min(W, D ? Math.max(4.4, (D.box[2] - D.box[0]) / D.den + 0.5) : 4.4); it.h = D ? (D.box[3] - D.box[1]) / D.den + 1.15 : 2;
    if (rows[rows.length - 1].length && x + it.w > W + 1e-6) { rows.push([]); x = 0; } rows[rows.length - 1].push(it); x += it.w + GAP; }
  const cell = it => { k++; return it.D ? panel(k, it.title, it.D.den, libSvg(it.D, { key: String(sh.no).replace(/\W/g, '') + 'n' + k }), { style: `flex:${r3(it.w)} 1 0`, note: it.note, scale: it.D.nts ? 'Not to scale' : it.w < 6.6 ? 'Scale ' + scaleText(it.D.den) : '' })
    : `<section class="panel" style="flex:4.4 1 0"><div class="view"><p class="miss">Detail ${esc(it.missing)} is not in the library</p></div><footer class="vt"><span class="vb">${k}</span><span class="vn">Missing detail</span></footer></section>`; };
  const body = `${sh.intro ? `<div class="figintro" data-fit>${rich(sh.intro, P)}</div>` : ''}<div class="libs">${rows.filter(r => r.length).map(r => `<div class="lrow" style="flex:${r3(Math.max(...r.map(it => it.h)))} 1 0">${r.map(cell).join('')}</div>`).join('')}</div>`;
  return sheet(P, sh, i, n, 's-libs', body);
}

// View numbers: plan 1, section 2, then the optional side view, then the details in order.
function setRefs(P) {
  const F = JOB.field, fs = (P.sheets || []).find(s => s.type === 'field') || {};
  REF = { sheet: fs.no || '', plan: 1, section: 2 }; let k = 3; if (F.side) REF.side = k++; (F.details || []).forEach((d, j) => { REF['d' + (j + 1)] = k++; });
  (F.extras || []).forEach((d, j) => { REF['x' + (j + 1)] = k++; });   // small extra views under the picture: x1, x2 ...
}

function renderSet(P) {
  setUnits((P.geometry || {}).units); setRefs(P);
  const G = JOB.derive(P), sheets = P.sheets, n = sheets.length, set = document.getElementById('set');
  const make = Object.assign({ cover: sheetCover, reserved: sheetReserved, field: sheetField, figures: sheetFigures, details: sheetDetails }, typeof SHEET_TYPES !== 'undefined' ? SHEET_TYPES : {});   // a job file may add sheet types
  set.innerHTML = sheets.map((sh, i) => make[sh.type](P, G, sh, i, n, sheets)).join('');
  if ((P.firm || {}).accent) set.style.setProperty('--brand', P.firm.accent); else set.style.removeProperty('--brand');
  document.title = [P.project.address, P.project.title].filter(Boolean).join(' · ');
}

// Fit every drawing to its real extents (this keeps true scale), then check nothing spills out of its box.
// The isometric picture is not to scale, so if it is too big for its box it is shrunk to fit (the audit says so if text gets small).
function fitViews() {
  const set = document.getElementById('set'), zoom = set.style.zoom; set.style.zoom = 1;   // measure at full size
  for (const s of document.querySelectorAll('svg.sk')) {
    const k = +s.dataset.den * UPI, b = s.getBBox(), p = 4 * k / 72; let w = (b.width + 2 * p) / k, h = (b.height + 2 * p) / k;
    s.setAttribute('viewBox', [b.x - p, b.y - p, b.width + 2 * p, b.height + 2 * p].map(v => Math.round(v * 1000) / 1000).join(' '));
    const box = s.classList.contains('iso') && s.closest('.view, .pic');
    if (box) { const r = box.getBoundingClientRect(), f = Math.min(1, (r.width - 2) / 96 / w, (r.height - 2) / 96 / h); s.dataset.shrunk = f.toFixed(3); w *= f; h *= f; }
    s.setAttribute('width', w.toFixed(4) + 'in'); s.setAttribute('height', h.toFixed(4) + 'in');
  }
  set.style.zoom = zoom;
}
function audit(P) {
  const set = document.getElementById('set'), zoom = set.style.zoom; set.style.zoom = 1;   // measure at full size
  const out = [], name = el => (el.closest('.sheet')?.dataset.sheet || '?') + ' · ' + (el.dataset.name || el.closest('.panel')?.querySelector('.vn, .ph')?.textContent || el.className);
  for (const v of document.querySelectorAll('.view')) { const s = v.querySelector('svg'); if (!s) continue; const a = v.getBoundingClientRect(), b = s.getBoundingClientRect();
    const dx = Math.max(a.left - b.left, b.right - a.right), dy = Math.max(a.top - b.top, b.bottom - a.bottom);
    if (dx > 1 || dy > 1) out.push(`${name(v)}: drawing is ${(Math.max(dx, 0) / 96).toFixed(2)} in too wide, ${(Math.max(dy, 0) / 96).toFixed(2)} in too tall for its box`); }
  for (const s of document.querySelectorAll('svg.sk:not(.iso)')) { const w = s.viewBox.baseVal.width / (+s.dataset.den * UPI), r = s.getBoundingClientRect().width / 96;
    if (Math.abs(r - w) / w > 0.003) out.push(`${name(s)}: drawn at ${(100 * r / w).toFixed(1)}% of its stated scale`); }
  for (const s of document.querySelectorAll('.p-iso svg.iso')) if (+s.dataset.shrunk < 0.8) out.push(`${name(s)}: the picture had to be shrunk to ${Math.round(100 * s.dataset.shrunk)}% to fit, so its labels are small. Raise pictureDen (or coverDen) or move the labels in`);
  for (const e of document.querySelectorAll('[data-fit]')) if (e.scrollHeight > e.clientHeight + 1 || e.scrollWidth > e.clientWidth + 1) out.push(`${name(e)}: text overflows its box by ${(Math.max(e.scrollHeight - e.clientHeight, e.scrollWidth - e.clientWidth) / 96).toFixed(2)} in`);
  for (const sh of document.querySelectorAll('.sheet')) { const f = sh.querySelector('.frame').getBoundingClientRect(), bd = sh.querySelector('.body'), tb = sh.querySelector('.tb');
    let low = 0; for (const c of bd.children) low = Math.max(low, c.getBoundingClientRect().bottom);
    if (low > f.bottom + 1) out.push(`${sh.dataset.sheet}: drawing area is ${((low - f.bottom) / 96).toFixed(2)} in taller than the sheet`);
    let tlow = 0; for (const c of tb.children) tlow = Math.max(tlow, c.getBoundingClientRect().bottom);
    if (tlow > f.bottom + 1) out.push(`${sh.dataset.sheet}: title block is ${((tlow - f.bottom) / 96).toFixed(2)} in taller than the sheet`); }
  for (const m of document.querySelectorAll('.miss')) out.push(`${name(m)}: ${m.textContent}`);
  const open = openItems(P).length;
  if ((STATUS[P.status] || STATUS.draft).issue && open) out.push(`status is "${P.status}" but ${open} open item${open > 1 ? 's' : ''} remain`);
  set.style.zoom = zoom;
  return out;
}
