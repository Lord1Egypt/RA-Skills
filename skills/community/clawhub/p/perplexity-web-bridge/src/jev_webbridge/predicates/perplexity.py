"""Site override: generic probe + submit-icon idle + answer-QA probe (thin, last resort)."""
from jev_webbridge.predicates.generic import settled

WHY_OVERRIDE = ("generic cannot see the submit icon morph (arrow-up vs stop) nor the answer "
                "provenance/citation markers; disabled-flag cannot express 'streaming but paused'")
CAP_MS = 2000

PROBE_JS = r"""(() => {
  const now = Date.now();
  if (!window.__jw) { window.__jw = {lastMut: now}; new MutationObserver(() => { window.__jw.lastMut = Date.now(); }).observe(document.body, {subtree:true, childList:true, characterData:true}); }
  const textLen = document.body ? document.body.innerText.length : 0;
  let iconIdle = true;
  for (const u of document.querySelectorAll('button svg use')) { const href = u.getAttribute('href') || u.getAttribute('xlink:href') || ''; if (href.includes('arrow-up')) { iconIdle = true; break; } if (href.includes('stop') || href.includes('square')) iconIdle = false; }
  return JSON.stringify({text_len: textLen, quiet_ms: Date.now() - window.__jw.lastMut, extra: {icon_idle: iconIdle}});
})()"""

POST_FILL_JS = ("(() => { const el = (document.activeElement && document.activeElement.isContentEditable) ? document.activeElement : document.querySelector('[contenteditable=\"true\"]'); if (!el) return 'nosync'; el.focus(); "
                "el.dispatchEvent(new InputEvent('input', {bubbles: true, data: el.textContent, inputType: 'insertText'})); return 'synced'; })()")

POST_EXTRACT_JS = ("(() => { const m = document.querySelector('main') || document.body; const t = m.innerText;"
                   " const cited = new Set((t.match(/\\[\\d+\\]/g) || []).map(s => +s.slice(1, -1)));"
                   " const links = new Set(Array.from(m.querySelectorAll('a')).map(a => a.href).filter(h => h.startsWith('http')));"
                   " const lab = (t.match(/Prepared using[^\\n]{0,40}/i) || [])[0] || null;"
                   " return JSON.stringify({model_label: lab, sources_listed: links.size, markers_used: cited.size}); })()")

def predicate() -> dict:
    return {"name": "perplexity", "probe_js": PROBE_JS, "post_fill_js": POST_FILL_JS,
            "post_extract_js": POST_EXTRACT_JS, "cap_ms": 2000,
            "poll_ms": 100, "settled": settled, "why_override": WHY_OVERRIDE}
