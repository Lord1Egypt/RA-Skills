/*!
 * HTML Mark — drop-in click-to-annotate overlay for HTML prototypes.
 *
 * Click any element to drop a numbered pin, then write what you'd change.
 * Copy out as Markdown / Plain / JSON for review handoff.
 *
 * Keyboard:
 *   M           toggle mark mode (when not typing)
 *   Esc         exit mark mode / close note popup
 *   Backspace   delete last pin (when not typing)
 *   Enter       save note  ·  Shift+Enter = newline
 *
 * Optional attribute: `data-mm-label="My Card"` on any element.
 */
(function () {
  'use strict';
  if (window.__markModeLoaded) return;
  window.__markModeLoaded = true;

  let markMode = false;
  let annotations = [];
  let nextId = 1;
  let activePinId = null;
  let lastHlEl = null;
  let notePop = null;

  // ---------- Styles ----------
  const css = `
.mm-ui, .mm-ui *, .mm-pin, .mm-pin *, .mm-note-pop, .mm-note-pop * {
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
}
body.mm-on, body.mm-on * { cursor: crosshair !important; }
body.mm-on .mm-ui, body.mm-on .mm-ui *,
body.mm-on .mm-note-pop, body.mm-on .mm-note-pop * { cursor: default !important; }
body.mm-on .mm-note-pop textarea { cursor: text !important; }
body.mm-on .mm-pin { cursor: pointer !important; }

.mm-target-hl {
  outline: 2px solid rgba(255,141,107,0.85) !important;
  outline-offset: 2px !important;
  box-shadow: 0 0 0 6px rgba(255,141,107,0.14) !important;
  transition: outline 0.15s ease, box-shadow 0.15s ease !important;
}

/* ---------- Toggle: glass pill ---------- */
.mm-toggle {
  position: fixed; top: 14px; right: 14px; z-index: 2147483600;
  display: inline-flex; align-items: center; gap: 8px;
  padding: 9px 16px;
  background: linear-gradient(155deg, rgba(48,38,32,0.86) 0%, rgba(38,30,26,0.74) 100%);
  color: #fff;
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 999px;
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  font-size: 12.5px; font-weight: 600; letter-spacing: 0.02em;
  cursor: pointer; user-select: none;
  box-shadow:
    0 8px 24px rgba(0,0,0,0.3),
    0 1px 2px rgba(0,0,0,0.14),
    inset 0 1px 0 rgba(255,255,255,0.2),
    inset 0 0 0 1px rgba(255,255,255,0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}
.mm-toggle:hover {
  transform: translateY(-1px);
  background: linear-gradient(155deg, rgba(62,50,42,0.94) 0%, rgba(50,40,34,0.84) 100%);
  box-shadow:
    0 14px 32px rgba(0,0,0,0.35),
    0 1px 2px rgba(0,0,0,0.16),
    inset 0 1px 0 rgba(255,255,255,0.24),
    inset 0 0 0 1px rgba(255,255,255,0.08);
}
.mm-toggle-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: #d0c8be;
  transition: background 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
}
.mm-toggle.on .mm-toggle-dot {
  background: linear-gradient(135deg, #ff8d6b 0%, #ffaf7a 50%, #ffd29c 100%);
  box-shadow: 0 0 14px rgba(255,141,107,0.95), 0 0 5px rgba(255,200,144,0.7);
  transform: scale(1.15);
}
.mm-toggle.on .mm-toggle-txt {
  color: #ffd29c;
  text-shadow: 0 0 10px rgba(255,141,107,0.55);
}

/* ---------- Pin: gradient orb ---------- */
@keyframes mm-pin-in {
  0%   { opacity: 0; transform: scale(0); }
  55%  { opacity: 1; transform: scale(1.22); }
  100% { opacity: 1; transform: scale(1); }
}
.mm-pin {
  position: absolute;
  width: 22px; height: 22px;
  background: linear-gradient(135deg, #ff8d6b 0%, #ffaf7a 55%, #ffc890 100%);
  color: #fff;
  border: 2px solid rgba(255,255,255,0.95);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 11.5px; font-weight: 700; line-height: 1;
  z-index: 2147483500;
  box-shadow:
    0 4px 12px rgba(255,141,107,0.45),
    0 1px 2px rgba(255,141,107,0.25),
    inset 0 1px 0 rgba(255,255,255,0.55);
  transition: transform 0.18s cubic-bezier(0.22,1,0.36,1), box-shadow 0.18s ease, border-color 0.18s ease;
  user-select: none;
  text-shadow: 0 1px 1px rgba(180,80,40,0.3);
  animation: mm-pin-in 0.42s cubic-bezier(0.22,1,0.36,1);
}
.mm-pin:hover, .mm-pin.mm-pin-hl {
  transform: scale(1.22);
  box-shadow:
    0 6px 18px rgba(255,141,107,0.55),
    0 1px 2px rgba(255,141,107,0.3),
    inset 0 1px 0 rgba(255,255,255,0.65);
}
.mm-pin.mm-pin-active {
  box-shadow:
    0 0 0 4px rgba(255,141,107,0.32),
    0 6px 16px rgba(255,141,107,0.5),
    inset 0 1px 0 rgba(255,255,255,0.65);
}
.mm-pin.mm-has-note::after {
  content: ''; position: absolute; top: -3px; right: -3px;
  width: 9px; height: 9px; border-radius: 50%;
  background: linear-gradient(135deg, #ffd29c, #ffaf7a);
  border: 1.5px solid #fff;
  box-shadow: 0 0 6px rgba(255,175,122,0.75);
}
.mm-pin-del {
  position: absolute; top: -7px; right: -7px;
  width: 16px; height: 16px;
  background: #1f1c1a; color: #fff;
  border-radius: 50%;
  display: none;
  align-items: center; justify-content: center;
  font-size: 10px; line-height: 1;
  border: 1.5px solid #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}
.mm-pin:hover .mm-pin-del { display: flex; }

/* ---------- Note popup: glass + gradient highlight ---------- */
@keyframes mm-pop-in {
  from { opacity: 0; transform: scale(0.94) translateY(-2px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
.mm-note-pop {
  position: absolute;
  width: 300px;
  background: linear-gradient(155deg, rgba(255,255,255,0.72) 0%, rgba(255,240,225,0.46) 100%);
  border: 1px solid rgba(255,255,255,0.78);
  border-radius: 14px;
  backdrop-filter: blur(24px) saturate(160%);
  -webkit-backdrop-filter: blur(24px) saturate(160%);
  box-shadow:
    0 18px 48px rgba(255,141,107,0.22),
    0 2px 4px rgba(255,141,107,0.08),
    inset 0 1px 0 rgba(255,255,255,0.95),
    inset 0 0 0 1px rgba(255,255,255,0.1);
  padding: 12px;
  z-index: 2147483520;
  display: flex; flex-direction: column; gap: 8px;
  overflow: hidden;
  transform-origin: top left;
  animation: mm-pop-in 0.22s cubic-bezier(0.22,1,0.36,1);
}
.mm-note-pop::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,141,107,0.7), rgba(255,210,156,0.7), transparent);
  pointer-events: none;
}
.mm-note-pop > * { position: relative; z-index: 1; }
.mm-note-pop-head {
  display: flex; align-items: center; gap: 8px;
  font-size: 10px; font-weight: 600; letter-spacing: 0.08em;
  color: #6f6864; text-transform: uppercase;
}
.mm-note-pop-head b { color: #1f1c1a; font-weight: 700; letter-spacing: 0.04em; }
.mm-note-pop-head .mm-np-text {
  flex: 1; text-align: right; text-transform: none;
  letter-spacing: 0; font-weight: 500;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  color: #8a847e;
}
.mm-note-pop textarea {
  width: 100%; min-height: 68px; max-height: 200px;
  resize: vertical;
  background: rgba(255,255,255,0.88);
  border: 1px solid rgba(255,200,170,0.45);
  border-radius: 8px;
  padding: 9px 11px;
  font-size: 13px; line-height: 1.5;
  color: #1f1c1a;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  font-family: inherit;
}
.mm-note-pop textarea:focus {
  border-color: rgba(255,141,107,0.7);
  background: rgba(255,255,255,0.98);
  box-shadow: 0 0 0 3px rgba(255,141,107,0.14);
}
.mm-note-pop textarea::placeholder { color: #b8b0a8; }
.mm-note-pop-hint {
  font-size: 10.5px; color: #8a847e;
  display: flex; justify-content: space-between; align-items: center;
}
.mm-note-pop-hint kbd {
  font-family: ui-monospace, 'JetBrains Mono', monospace;
  background: rgba(255,255,255,0.7); color: #6f6864;
  padding: 1px 5px; border-radius: 3px;
  font-size: 10px;
  border: 1px solid rgba(255,255,255,0.9);
  box-shadow: 0 1px 1px rgba(0,0,0,0.03);
}

/* ---------- Panel: glass with gradient highlight ---------- */
.mm-panel {
  position: fixed; right: 20px; bottom: 20px;
  width: 348px; max-height: 60vh;
  background: linear-gradient(155deg, rgba(255,255,255,0.72) 0%, rgba(255,240,225,0.42) 100%);
  border: 1px solid rgba(255,255,255,0.78);
  border-radius: 16px;
  backdrop-filter: blur(28px) saturate(160%);
  -webkit-backdrop-filter: blur(28px) saturate(160%);
  box-shadow:
    0 20px 56px rgba(255,141,107,0.18),
    0 2px 4px rgba(255,141,107,0.06),
    inset 0 1px 0 rgba(255,255,255,0.95),
    inset 0 0 0 1px rgba(255,255,255,0.08);
  z-index: 2147483550;
  display: none;
  flex-direction: column;
  overflow: hidden;
  color: #1f1c1a;
}
.mm-panel::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,141,107,0.7), rgba(255,210,156,0.7), transparent);
  pointer-events: none; z-index: 2;
}
.mm-panel.show { display: flex; }
.mm-panel.collapsed { width: auto; max-height: none; }
.mm-panel.collapsed .mm-panel-body { display: none; }
.mm-panel.collapsed .mm-panel-head { border-bottom: none; padding: 7px 14px; }

.mm-panel-head {
  display: flex; align-items: center; gap: 8px;
  padding: 11px 14px;
  border-bottom: 1px solid rgba(255,255,255,0.5);
  cursor: grab;
  user-select: none;
  position: relative;
}
.mm-panel-head.dragging { cursor: grabbing; }
.mm-panel-title {
  flex: 1;
  font-size: 11px; font-weight: 700; letter-spacing: 0.08em;
  color: #1f1c1a; text-transform: uppercase;
  display: inline-flex; align-items: center;
}
.mm-panel-count {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 18px; height: 18px; padding: 0 5px;
  background: linear-gradient(135deg, #e8633c 0%, #f08d4f 100%);
  color: #fff;
  border-radius: 9px;
  font-size: 10px; font-weight: 700;
  margin-left: 8px;
  letter-spacing: 0;
  box-shadow: 0 2px 6px rgba(232,99,60,0.5), inset 0 1px 0 rgba(255,255,255,0.4);
}
.mm-panel-iconbtn {
  width: 26px; height: 26px;
  background: transparent; color: #6f6864;
  border: 1px solid transparent;
  border-radius: 7px;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 14px; line-height: 1; font-weight: 700;
  cursor: pointer;
  transition: color 0.15s ease, background 0.15s ease;
}
.mm-panel-iconbtn:hover {
  color: #e8633c;
  background: rgba(255,255,255,0.55);
}

.mm-panel-body {
  display: flex; flex-direction: column;
  flex: 1; min-height: 0;
}
.mm-list {
  padding: 10px;
  overflow-y: auto;
  flex: 1; min-height: 60px;
  max-height: calc(60vh - 110px);
}
.mm-list::-webkit-scrollbar { width: 6px; }
.mm-list::-webkit-scrollbar-thumb { background: rgba(255,141,107,0.3); border-radius: 3px; }
.mm-list::-webkit-scrollbar-thumb:hover { background: rgba(255,141,107,0.5); }

.mm-item {
  display: flex; gap: 10px;
  padding: 10px 12px;
  background: rgba(255,255,255,0.65);
  border: 1px solid rgba(255,255,255,0.65);
  border-radius: 10px;
  margin-bottom: 7px;
  font-size: 12.5px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: background 0.18s ease, border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;
}
.mm-item:hover {
  background: rgba(255,255,255,0.88);
  border-color: rgba(255,255,255,0.88);
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(255,141,107,0.15);
}
.mm-item.active {
  border-color: rgba(255,141,107,0.55);
  background: rgba(255,255,255,0.94);
  box-shadow: 0 0 0 2px rgba(255,141,107,0.18);
}
.mm-item.has-note::before {
  content: ''; position: absolute; left: 0; top: 0; bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, #ff8d6b, #ffd29c);
}
.mm-item-num {
  width: 22px; height: 22px;
  background: #1a1612; color: #fff;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font: 700 11px/1 inherit;
  flex-shrink: 0;
  box-shadow: 0 2px 5px rgba(0,0,0,0.22), inset 0 1px 0 rgba(255,255,255,0.18);
}
.mm-item.has-note .mm-item-num {
  background: linear-gradient(135deg, #e8633c 0%, #f08d4f 100%);
  box-shadow: 0 2px 6px rgba(232,99,60,0.55), inset 0 1px 0 rgba(255,255,255,0.35);
}
.mm-item-body { flex: 1; min-width: 0; }
.mm-item-note {
  font-size: 13px; font-weight: 500; color: #1f1c1a;
  line-height: 1.45;
  margin-bottom: 3px;
  white-space: pre-wrap;
  word-break: break-word;
}
.mm-item-note-empty {
  font-size: 12px; color: #b8b0a8; font-style: italic;
  margin-bottom: 3px;
}
.mm-item-meta {
  font-size: 11px; color: #8a847e;
  line-height: 1.4;
  word-break: break-word;
}
.mm-item-meta b { color: #6f6864; font-weight: 600; }
.mm-item-del {
  width: 22px; height: 22px;
  background: transparent; color: #b8b0a8;
  border: none;
  border-radius: 5px;
  font-size: 15px; line-height: 1;
  cursor: pointer;
  flex-shrink: 0;
  align-self: flex-start;
  display: none;
  padding: 0;
  transition: color 0.15s ease, background 0.15s ease;
}
.mm-item:hover .mm-item-del { display: block; }
.mm-item-del:hover {
  color: #e8633c;
  background: rgba(255,141,107,0.1);
}

.mm-empty {
  padding: 30px 16px; text-align: center;
  color: #8a847e; font-size: 12.5px;
  line-height: 1.7;
}
.mm-empty kbd {
  font-family: ui-monospace, 'JetBrains Mono', monospace;
  background: rgba(255,255,255,0.7); color: #6f6864;
  padding: 1px 6px; border-radius: 3px;
  font-size: 10.5px;
  border: 1px solid rgba(255,255,255,0.9);
  margin: 0 2px;
}

/* ---------- Panel footer ---------- */
.mm-panel-foot {
  display: flex; gap: 7px;
  padding: 10px 12px;
  border-top: 1px solid rgba(255,255,255,0.5);
  background: rgba(255,255,255,0.32);
  flex-shrink: 0;
}
.mm-fmt-select {
  background: rgba(255,255,255,0.82);
  border: 1px solid rgba(255,255,255,0.88);
  border-radius: 7px;
  padding: 0 8px;
  font-size: 11px;
  color: #6f6864;
  height: 32px;
  cursor: pointer;
  outline: none;
  font-family: inherit;
  transition: border-color 0.15s ease, background 0.15s ease;
}
.mm-fmt-select:focus, .mm-fmt-select:hover { border-color: rgba(255,141,107,0.5); background: rgba(255,255,255,0.98); }
.mm-btn {
  height: 32px; padding: 0 14px;
  border-radius: 7px;
  font-size: 11.5px; font-weight: 600;
  cursor: pointer;
  border: 1px solid rgba(255,255,255,0.88);
  background: rgba(255,255,255,0.82); color: #6f6864;
  transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease;
  font-family: inherit;
}
.mm-btn:hover {
  color: #1f1c1a;
  background: rgba(255,255,255,0.98);
  border-color: rgba(255,141,107,0.4);
}
.mm-btn.primary {
  background: linear-gradient(135deg, #ff8d6b 0%, #ffaf7a 55%, #ffd29c 100%);
  color: #fff;
  border-color: transparent;
  flex: 1;
  box-shadow: 0 4px 14px rgba(255,141,107,0.32), inset 0 1px 0 rgba(255,255,255,0.35);
  text-shadow: 0 1px 1px rgba(180,80,40,0.2);
}
.mm-btn.primary:hover {
  background: linear-gradient(135deg, #ff7a55 0%, #ff9c64 55%, #ffc890 100%);
  color: #fff;
  box-shadow: 0 6px 20px rgba(255,141,107,0.45), inset 0 1px 0 rgba(255,255,255,0.4);
  border-color: transparent;
}

/* ---------- Toast: glass dark ---------- */
.mm-toast {
  position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
  background: linear-gradient(155deg, rgba(31,28,26,0.9) 0%, rgba(50,40,35,0.86) 100%);
  color: #fff;
  padding: 10px 20px;
  border-radius: 999px;
  font-size: 12.5px; font-weight: 500;
  z-index: 2147483640;
  opacity: 0;
  transition: opacity 0.2s ease, transform 0.2s ease;
  pointer-events: none;
  box-shadow:
    0 12px 32px rgba(0,0,0,0.22),
    inset 0 1px 0 rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.08);
  letter-spacing: 0.01em;
  backdrop-filter: blur(14px) saturate(140%);
  -webkit-backdrop-filter: blur(14px) saturate(140%);
}
.mm-toast.show { opacity: 1; transform: translate(-50%, -4px); }

@media (prefers-reduced-motion: reduce) {
  .mm-pin, .mm-toggle, .mm-item, .mm-btn, .mm-panel-iconbtn, .mm-toast,
  .mm-note-pop, .mm-note-pop textarea, .mm-toggle-dot, .mm-target-hl {
    transition: none !important;
    animation: none !important;
  }
}
`;

  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  // ---------- Build UI ----------
  const toggle = document.createElement('button');
  toggle.className = 'mm-toggle mm-ui';
  toggle.innerHTML = '<span class="mm-toggle-dot"></span><span class="mm-toggle-txt">Mark</span>';
  toggle.title = 'Toggle mark mode · M to toggle · Esc to exit';

  const panel = document.createElement('div');
  panel.className = 'mm-panel mm-ui';
  panel.innerHTML =
    '<div class="mm-panel-head" id="mm-head">' +
    '  <div class="mm-panel-title">Annotations<span class="mm-panel-count" id="mm-count">0</span></div>' +
    '  <button class="mm-panel-iconbtn" id="mm-collapse" title="Collapse">−</button>' +
    '</div>' +
    '<div class="mm-panel-body">' +
    '  <div class="mm-list" id="mm-list"></div>' +
    '  <div class="mm-panel-foot">' +
    '    <select class="mm-fmt-select" id="mm-fmt" title="Export format">' +
    '      <option value="md">Markdown</option>' +
    '      <option value="txt">Plain</option>' +
    '      <option value="json">JSON</option>' +
    '    </select>' +
    '    <button class="mm-btn" id="mm-clear">Clear</button>' +
    '    <button class="mm-btn primary" id="mm-copy">Copy all</button>' +
    '  </div>' +
    '</div>';

  const toast = document.createElement('div');
  toast.className = 'mm-toast mm-ui';

  function init() {
    document.body.appendChild(toggle);
    document.body.appendChild(panel);
    document.body.appendChild(toast);

    toggle.addEventListener('click', toggleMarkMode);
    document.getElementById('mm-clear').addEventListener('click', clearAll);
    document.getElementById('mm-copy').addEventListener('click', copyAll);
    document.getElementById('mm-collapse').addEventListener('click', togglePanelCollapse);

    setupPanelDrag();
    document.addEventListener('click', handleClick, true);
    document.addEventListener('keydown', handleKey);
    render();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // ---------- Behavior ----------
  function toggleMarkMode() {
    markMode = !markMode;
    document.body.classList.toggle('mm-on', markMode);
    panel.classList.toggle('show', markMode);
    toggle.classList.toggle('on', markMode);
    toggle.querySelector('.mm-toggle-txt').textContent = markMode ? 'Marking' : 'Mark';
    if (!markMode) closeNotePop();
  }

  function togglePanelCollapse() {
    const collapsed = panel.classList.toggle('collapsed');
    document.getElementById('mm-collapse').textContent = collapsed ? '+' : '−';
  }

  function describeElement(el) {
    let cur = el;
    while (cur && cur !== document.body && cur !== document.documentElement) {
      if (cur.getAttribute && cur.getAttribute('data-mm-label')) {
        return { label: cur.getAttribute('data-mm-label'), selector: '[data-mm-label]', text: textOf(cur), target: cur };
      }
      if (cur.id) return { label: '#' + cur.id, selector: '#' + cur.id, text: textOf(cur), target: cur };
      if (cur.getAttribute && cur.getAttribute('aria-label')) {
        return { label: cur.getAttribute('aria-label'), selector: cur.tagName.toLowerCase(), text: textOf(cur), target: cur };
      }
      if (cur.matches) {
        if (cur.matches('button, [role="button"]')) return { label: 'Button', selector: 'button', text: textOf(cur), target: cur };
        if (cur.matches('a[href]')) return { label: 'Link', selector: 'a', text: textOf(cur), target: cur };
        if (cur.matches('input, select, textarea')) {
          const v = cur.placeholder || cur.value || '';
          return { label: cur.tagName.toLowerCase(), selector: cur.tagName.toLowerCase(), text: v.slice(0, 80), target: cur };
        }
        if (cur.matches('h1, h2, h3, h4, h5, h6')) {
          return { label: cur.tagName.toLowerCase(), selector: cur.tagName.toLowerCase(), text: textOf(cur), target: cur };
        }
      }
      cur = cur.parentElement;
    }
    const tag = el.tagName ? el.tagName.toLowerCase() : 'unknown';
    const cls = (el.className && typeof el.className === 'string') ? el.className.split(' ').filter(Boolean)[0] : '';
    const sel = tag + (cls ? '.' + cls : '');
    return { label: sel, selector: sel, text: textOf(el), target: el };
  }

  function textOf(el) {
    return (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80);
  }

  function getContext() {
    const url = location.pathname + (location.hash || '');
    const title = document.title || '';
    return title ? title + ' (' + url + ')' : url;
  }

  function handleClick(e) {
    if (!markMode) return;
    if (e.target.closest('.mm-ui')) return;
    if (e.target.closest('.mm-pin')) return;
    if (e.target.closest('.mm-note-pop')) return;

    e.preventDefault();
    e.stopPropagation();

    const desc = describeElement(e.target);
    const ctx = getContext();
    const id = nextId++;

    const pin = document.createElement('div');
    pin.className = 'mm-pin';
    pin.dataset.id = id;
    pin.style.left = (e.pageX - 11) + 'px';
    pin.style.top = (e.pageY - 11) + 'px';

    pin.appendChild(document.createTextNode(String(id)));

    const del = document.createElement('span');
    del.className = 'mm-pin-del';
    del.textContent = '×';
    del.addEventListener('click', function (ev) {
      ev.stopPropagation();
      removeAnn(parseInt(pin.dataset.id, 10));
    });
    pin.appendChild(del);

    pin.addEventListener('click', function (ev) {
      ev.stopPropagation();
      if (ev.target === del) return;
      const aid = parseInt(pin.dataset.id, 10);
      const ann = annotations.find(function (a) { return a.id === aid; });
      if (ann) openNotePop(ann);
    });

    document.body.appendChild(pin);
    const ann = {
      id: id, ctx: ctx,
      label: desc.label, selector: desc.selector, text: desc.text,
      note: '', pinEl: pin, targetEl: desc.target
    };
    annotations.push(ann);
    render();
    openNotePop(ann);
  }

  // ---------- Note popup ----------
  function openNotePop(ann) {
    closeNotePop();
    activePinId = ann.id;
    ann.pinEl.classList.add('mm-pin-active');
    document.querySelectorAll('.mm-item').forEach(function (it) {
      it.classList.toggle('active', parseInt(it.dataset.id, 10) === ann.id);
    });

    notePop = document.createElement('div');
    notePop.className = 'mm-note-pop';
    notePop.innerHTML =
      '<div class="mm-note-pop-head">' +
      '  <span><b>#' + ann.id + '</b> · ' + esc(ann.label) + '</span>' +
      '  <span class="mm-np-text">' + (ann.text ? esc(ann.text) : '') + '</span>' +
      '</div>' +
      '<textarea placeholder="What should change here? (optional)"></textarea>' +
      '<div class="mm-note-pop-hint">' +
      '  <span><kbd>↵</kbd> save · <kbd>⇧↵</kbd> newline · <kbd>Esc</kbd> close</span>' +
      '  <span style="color:#b8b0a8">' + (ann.note ? 'editing' : 'new') + '</span>' +
      '</div>';

    document.body.appendChild(notePop);

    const pinRect = ann.pinEl.getBoundingClientRect();
    const popW = notePop.offsetWidth;
    const popH = notePop.offsetHeight;
    let popX = pinRect.right + 10 + window.scrollX;
    let popY = pinRect.top + window.scrollY;
    if (popX + popW > window.scrollX + window.innerWidth - 8) {
      popX = pinRect.left - popW - 10 + window.scrollX;
    }
    if (popX < window.scrollX + 8) popX = window.scrollX + 8;
    if (popY + popH > window.scrollY + window.innerHeight - 8) {
      popY = window.scrollY + window.innerHeight - popH - 8;
    }
    if (popY < window.scrollY + 8) popY = window.scrollY + 8;
    notePop.style.left = popX + 'px';
    notePop.style.top = popY + 'px';

    const ta = notePop.querySelector('textarea');
    ta.value = ann.note || '';
    ta.focus();
    ta.setSelectionRange(ta.value.length, ta.value.length);

    ta.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' && !ev.shiftKey) {
        ev.preventDefault();
        ann.note = ta.value.trim();
        closeNotePop();
        render();
      } else if (ev.key === 'Escape') {
        ev.preventDefault();
        closeNotePop();
      }
    });

    setTimeout(function () {
      document.addEventListener('mousedown', outsideHandler, true);
    }, 0);

    function outsideHandler(ev) {
      if (!notePop) {
        document.removeEventListener('mousedown', outsideHandler, true);
        return;
      }
      if (notePop.contains(ev.target)) return;
      if (ev.target.closest && ev.target.closest('.mm-pin')) return;
      const val = ta.value.trim();
      if (val !== (ann.note || '')) { ann.note = val; render(); }
      closeNotePop();
      document.removeEventListener('mousedown', outsideHandler, true);
    }
  }

  function closeNotePop() {
    if (notePop) { notePop.remove(); notePop = null; }
    if (activePinId !== null) {
      const a = annotations.find(function (x) { return x.id === activePinId; });
      if (a && a.pinEl) a.pinEl.classList.remove('mm-pin-active');
      document.querySelectorAll('.mm-item.active').forEach(function (it) { it.classList.remove('active'); });
      activePinId = null;
    }
  }

  // ---------- Keyboard ----------
  function handleKey(e) {
    const inField = e.target.matches && e.target.matches('input, textarea, [contenteditable="true"]');
    if (!inField && (e.key === 'm' || e.key === 'M') && !e.metaKey && !e.ctrlKey && !e.altKey) {
      e.preventDefault();
      toggleMarkMode();
      return;
    }
    if (e.key === 'Escape') {
      if (notePop) return;
      if (markMode) toggleMarkMode();
      return;
    }
    if (markMode && e.key === 'Backspace' && !inField) {
      if (annotations.length > 0) {
        e.preventDefault();
        removeAnn(annotations[annotations.length - 1].id);
      }
    }
  }

  // ---------- Mutations ----------
  function removeAnn(id) {
    if (activePinId === id) closeNotePop();
    const a = annotations.find(function (x) { return x.id === id; });
    if (a && a.pinEl) a.pinEl.remove();
    annotations = annotations.filter(function (x) { return x.id !== id; });
    annotations.forEach(function (a, i) {
      const n = i + 1;
      a.pinEl.firstChild.nodeValue = String(n);
      a.pinEl.dataset.id = n;
      a.id = n;
    });
    nextId = annotations.length + 1;
    render();
  }

  function clearAll() {
    closeNotePop();
    annotations.forEach(function (a) { a.pinEl && a.pinEl.remove(); });
    annotations = [];
    nextId = 1;
    render();
  }

  // ---------- Render ----------
  function render() {
    document.getElementById('mm-count').textContent = annotations.length;
    const list = document.getElementById('mm-list');
    if (annotations.length === 0) {
      list.innerHTML =
        '<div class="mm-empty">' +
        'Click anywhere to drop a pin.<br/>' +
        '<kbd>M</kbd> toggle · <kbd>Esc</kbd> exit · <kbd>⌫</kbd> undo' +
        '</div>';
      return;
    }
    list.innerHTML = annotations.map(function (a, i) {
      const hasNote = !!a.note;
      const n = i + 1;
      return '<div class="mm-item ' + (hasNote ? 'has-note' : '') + '" data-id="' + a.id + '">' +
        '<div class="mm-item-num">' + n + '</div>' +
        '<div class="mm-item-body">' +
          (hasNote
            ? '<div class="mm-item-note">' + esc(a.note) + '</div>'
            : '<div class="mm-item-note-empty">No note · click to add</div>') +
          '<div class="mm-item-meta">' +
            '<b>' + esc(a.label) + '</b>' +
            (a.text ? ' · ' + esc(a.text).slice(0, 50) : '') +
          '</div>' +
        '</div>' +
        '<button class="mm-item-del" data-del="' + a.id + '" title="Delete">×</button>' +
      '</div>';
    }).join('');

    list.querySelectorAll('.mm-item').forEach(function (it) {
      const id = parseInt(it.dataset.id, 10);
      const ann = annotations.find(function (a) { return a.id === id; });
      if (!ann) return;
      it.addEventListener('click', function (e) {
        if (e.target.matches('[data-del]')) return;
        if (ann.pinEl) ann.pinEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        setTimeout(function () { openNotePop(ann); }, 80);
      });
      it.addEventListener('mouseenter', function () {
        if (ann.pinEl) ann.pinEl.classList.add('mm-pin-hl');
        if (ann.targetEl && ann.targetEl !== document.body && document.body.contains(ann.targetEl)) {
          lastHlEl = ann.targetEl;
          ann.targetEl.classList.add('mm-target-hl');
        }
      });
      it.addEventListener('mouseleave', function () {
        if (ann.pinEl) ann.pinEl.classList.remove('mm-pin-hl');
        if (lastHlEl) { lastHlEl.classList.remove('mm-target-hl'); lastHlEl = null; }
      });
    });
    list.querySelectorAll('[data-del]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        removeAnn(parseInt(btn.dataset.del, 10));
      });
    });

    annotations.forEach(function (a) {
      if (a.pinEl) a.pinEl.classList.toggle('mm-has-note', !!a.note);
    });
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // ---------- Copy ----------
  function copyAll() {
    if (annotations.length === 0) {
      showToast('Nothing to copy yet — drop a pin first.');
      return;
    }
    const fmt = document.getElementById('mm-fmt').value;
    const ctx = getContext();
    let txt = '';

    if (fmt === 'md') {
      txt = '# Annotations — ' + ctx + '\n\n' + annotations.map(function (a, i) {
        const n = i + 1;
        const note = a.note || '_(no note)_';
        const meta = a.label + (a.text ? ' · "' + a.text + '"' : '') + ' · `' + a.selector + '`';
        return '**' + n + '.** ' + note + '\n   <sub>' + meta + '</sub>';
      }).join('\n\n');
    } else if (fmt === 'json') {
      txt = JSON.stringify({
        context: ctx,
        annotations: annotations.map(function (a, i) {
          return {
            id: i + 1,
            note: a.note,
            label: a.label,
            text: a.text,
            selector: a.selector
          };
        })
      }, null, 2);
    } else {
      txt = annotations.map(function (a, i) {
        const n = i + 1;
        const noteStr = a.note ? ': ' + a.note : '';
        return n + '. [' + a.label + (a.text ? ' "' + a.text + '"' : '') + ']' + noteStr;
      }).join('\n') + '\n\n@ ' + ctx;
    }

    navigator.clipboard.writeText(txt).then(function () {
      const n = annotations.length;
      showToast('✓ ' + n + ' annotation' + (n > 1 ? 's' : '') + ' copied as ' + fmt.toUpperCase());
    }).catch(function () {
      showToast('Failed to copy — check clipboard permission.');
    });
  }

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(function () { toast.classList.remove('show'); }, 2000);
  }

  // ---------- Panel drag ----------
  function setupPanelDrag() {
    const head = document.getElementById('mm-head');
    let dragging = false, sx = 0, sy = 0, sl = 0, st = 0;
    head.addEventListener('mousedown', function (e) {
      if (e.target.closest('.mm-panel-iconbtn')) return;
      dragging = true;
      head.classList.add('dragging');
      const r = panel.getBoundingClientRect();
      sx = e.clientX; sy = e.clientY;
      sl = r.left; st = r.top;
      panel.style.right = 'auto'; panel.style.bottom = 'auto';
      panel.style.left = sl + 'px'; panel.style.top = st + 'px';
      e.preventDefault();
    });
    document.addEventListener('mousemove', function (e) {
      if (!dragging) return;
      const w = panel.offsetWidth, h = panel.offsetHeight;
      const nx = Math.max(4, Math.min(window.innerWidth - w - 4, sl + (e.clientX - sx)));
      const ny = Math.max(4, Math.min(window.innerHeight - 40, st + (e.clientY - sy)));
      panel.style.left = nx + 'px';
      panel.style.top = ny + 'px';
    });
    document.addEventListener('mouseup', function () {
      if (dragging) { dragging = false; head.classList.remove('dragging'); }
    });
  }
})();
