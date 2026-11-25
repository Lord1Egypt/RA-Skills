// Oasis-Blueprints · https://github.com/oasiseng/Oasis-Blueprints · MIT License, Copyright (c) 2026 Oasis Engineering, LLC
// editor.js — screen-only tools: fit to window, answer open items, fill the title block, set the company,
// save and print. Nothing here prints, and nothing is stored in the browser: use the download buttons to keep edits.
'use strict';

let SRC_HTML = '';   // the page as built, captured before the first render; "Download this HTML" re-embeds the project in it

const EDITOR = (() => {
  let timer = null, fit = true;
  const $ = (s, r = document) => r.querySelector(s);
  const get = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
  const set = (o, path, v) => { const ks = path.split('.'), last = ks.pop(), t = ks.reduce((a, k) => (a[k] == null ? (a[k] = {}) : a[k]), o); t[last] = v; };
  const slug = () => ([PROJECT.project.address, PROJECT.project.title].filter(Boolean).join(' - ') || 'sheet-set').replace(/[^\w .-]+/g, '').trim();

  function zoom() { $('#set').style.zoom = fit ? Math.min(1, (window.innerWidth - 24) / (36.9 * 96)) : 1; const b = $('#ui [data-a=fit]'); if (b) b.textContent = fit ? 'Actual size' : 'Fit to window'; }
  function badge(a) {
    const b = $('#ui-audit'), n = openItems(PROJECT).length;
    b.className = a.length ? 'abad' : 'aok';
    b.textContent = (a.length ? a.length + ' layout problem' + (a.length > 1 ? 's' : '') : 'Layout OK') + ' · ' + (n ? n + ' open item' + (n > 1 ? 's' : '') : 'no open items');
    $('#audit').innerHTML = a.length ? '<b>Fix before issuing</b><br>' + a.map(esc).join('<br>') : '';
  }
  function refresh() { renderSet(PROJECT); fitViews(); const a = audit(PROJECT); window.__audit = a; badge(a); zoom(); }
  const later = () => { clearTimeout(timer); timer = setTimeout(refresh, 350); };

  const field = (label, path, o = {}) => { const v = get(PROJECT, path); const s = v == null ? '' : String(v);
    return `<label>${esc(label)}${o.area ? `<textarea data-path="${path}" rows="${o.rows || 2}" placeholder="${esc(o.ph || '')}">${esc(s)}</textarea>` : `<input data-path="${path}" value="${esc(s)}" placeholder="${esc(o.ph || '')}">`}</label>`; };

  function drawer() {
    const P = PROJECT; P.firm = P.firm || {}; P.people = P.people || {}; P.issue = P.issue || {};
    $('#ui-drawer').innerHTML = `
      <h3>Open items for the engineer</h3>
      <p class="hint">Type the answer. The item closes, and where a drawing was waiting on it the red note becomes your answer.</p>
      ${(P.openItems || []).map((o, i) => `<div class="it ${isOpen(o) ? '' : 'closed'}">${o.custom ? field('Item', `openItems.${i}.title`) + field('What is needed', `openItems.${i}.text`, { area: true }) : `<b>${esc(o.title)}</b><span>${esc(o.text)}</span>`}${field('Answer', `openItems.${i}.answer`, { area: true, ph: o.who || 'Engineer' })}</div>`).join('')}
      <button data-a="add">Add an open item</button>
      <h3>Status</h3>
      <label>Set status<select data-path="status">${Object.keys(STATUS).map(k => `<option value="${k}"${P.status === k ? ' selected' : ''}>${esc(STATUS[k].box[0])}</option>`).join('')}</select></label>
      <h3>Title block</h3>
      ${field('Project number', 'project.number')}${field('Drawn by', 'people.drawnBy')}${field('Checked by', 'people.checkedBy')}${field('Address', 'project.address')}${field('City, state, zip', 'project.locality')}${field('Date', 'issue.date')}
      <h3>Design criteria</h3>
      ${(P.criteria || []).map((c, i) => field(c.k, `criteria.${i}.v`)).join('')}
      <h3>Company</h3>
      ${field('Company name', 'firm.name')}${field('Wordmark, shown when there is no logo', 'firm.wordmark')}
      <label>Address, licence, phone, web (one per line)<textarea data-lines="firm.lines" rows="5">${esc((P.firm.lines || []).join('\n'))}</textarea></label>
      ${field('Accent colour, for example #1f63d6', 'firm.accent')}
      <label>Logo image<input type="file" data-a="logo" accept="image/*"></label>
      ${P.firm.logo ? '<button data-a="nologo">Remove logo</button>' : ''}
      <h3>Save</h3>
      <button data-a="json">Download project file</button> <button data-a="html">Download this HTML with my edits</button>
      <details><summary>Whole project file</summary><textarea id="ui-raw" rows="18" spellcheck="false">${esc(JSON.stringify(P, null, 2))}</textarea><button data-a="apply">Apply</button> <span id="ui-err"></span></details>
      <p class="hint src">Drawn with <a href="${esc(ORIGIN.repo)}" target="_blank" rel="noopener">${esc(ORIGIN.name)}</a>, open source from ${esc(ORIGIN.by)}. <a href="${esc(ORIGIN.site)}" target="_blank" rel="noopener">${esc(ORIGIN.site.replace(/^https?:\/\//, '').replace(/\/$/, ''))}</a></p>`;
  }

  function download(name, text, type) { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type })); a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 2000); }
  function pageWithEdits() { const tag = '<script type="application/json" id="project">', i = SRC_HTML.indexOf(tag), j = SRC_HTML.indexOf('</' + 'script>', i);
    return '<!doctype html>\n' + SRC_HTML.slice(0, i + tag.length) + JSON.stringify(PROJECT).replace(/</g, '\\u003c') + SRC_HTML.slice(j); }

  function act(a, el) {
    if (a === 'edit') { const d = $('#ui-drawer'); d.hidden = !d.hidden; if (!d.hidden) drawer(); }
    else if (a === 'fit') { fit = !fit; zoom(); }
    else if (a === 'print') window.print();
    else if (a === 'json') download(slug() + '.project.json', JSON.stringify(PROJECT, null, 2), 'application/json');
    else if (a === 'html') download(slug() + '.html', pageWithEdits(), 'text/html');
    else if (a === 'add') { (PROJECT.openItems = PROJECT.openItems || []).push({ key: 'item' + Date.now().toString(36), title: 'New item', text: '', who: 'Engineer', answer: '', custom: true }); drawer(); refresh(); }
    else if (a === 'nologo') { delete PROJECT.firm.logo; drawer(); refresh(); }
    else if (a === 'apply') { try { const p = JSON.parse($('#ui-raw').value); for (const k of Object.keys(PROJECT)) delete PROJECT[k]; Object.assign(PROJECT, p); $('#ui-err').textContent = ''; drawer(); refresh(); } catch (e) { $('#ui-err').textContent = 'Not valid JSON: ' + e.message; } }
  }

  function init() {
    const ui = document.createElement('div'); ui.id = 'ui';
    ui.innerHTML = `<div class="bar"><button data-a="edit" class="pri">Edit</button><button data-a="fit"></button><button data-a="print">Print / Save as PDF</button><span id="ui-audit"></span></div><div id="ui-drawer" hidden></div>`;
    document.body.appendChild(ui);
    ui.addEventListener('click', e => { const b = e.target.closest('[data-a]'); if (b && b.tagName === 'BUTTON') act(b.dataset.a, b); });
    ui.addEventListener('input', e => { const t = e.target;
      if (t.dataset.path) { set(PROJECT, t.dataset.path, t.value); if (/openItems\.\d+\.answer/.test(t.dataset.path)) t.closest('.it').classList.toggle('closed', !!t.value.trim()); later(); }
      else if (t.dataset.lines) { set(PROJECT, t.dataset.lines, t.value.split('\n').map(s => s.trim()).filter(Boolean)); later(); } });
    ui.addEventListener('change', e => { const t = e.target; if (t.dataset.a === 'logo' && t.files[0]) { const r = new FileReader(); r.onload = () => { PROJECT.firm.logo = r.result; drawer(); refresh(); }; r.readAsDataURL(t.files[0]); } });
    window.addEventListener('resize', zoom);
    badge(window.__audit || []); zoom();
  }
  return { init, refresh };
})();
