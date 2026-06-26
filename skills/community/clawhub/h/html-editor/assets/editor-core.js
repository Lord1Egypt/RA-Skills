/* ========================================================
   html-visual-editor - Editor core runtime
   Inject INSIDE a script block near the end of the body

   REQUIRED customizations in the target HTML:
   1. Define PAGE_ELEMENT_TO_PANEL mapping (see below)
   2. Define PRESETS (theme objects)
   3. Define DEFAULT_COLORS (for reset)
   4. Define SIZE_BOUNDS (clamp min/max for each size var)

   NOTE: never mix single-line and block comments in the same area.
   A bare-text line after a single-line-comment line crashes the
   script in the browser. See MEMORY 2026-05-07.
   ======================================================== */

/* =====================================================
   CORE PRESENTATION SCRIPTS
   ===================================================== */

const slides = document.querySelectorAll('.slide');
const reveals = document.querySelectorAll('.reveal');
const dots = document.querySelectorAll('.nav-dot');

function updateVisibility() {
    try {
        const trigger = window.innerHeight * 0.85;
        reveals.forEach(el => {
            if (el.getBoundingClientRect().top < trigger) el.classList.add('visible');
        });

        let current = 0;
        slides.forEach((s, i) => {
            const rect = s.getBoundingClientRect();
            if (rect.top <= 0 && rect.bottom > 0) current = i;
        });
        dots.forEach((d, i) => d.classList.toggle('active', i === current));
    } catch(err) {
        console.warn('[updateVisibility]', err);
    }
}

/* === 立即让所有 reveal 元素可见 ===
   不等滚动触发——页面一打开就显示全部内容，
   动画效果仅在首次滚动时生效 */
function revealAllNow() {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
}

window.addEventListener('scroll', updateVisibility, { passive: true });
window.addEventListener('load', () => {
    try {
        updateVisibility();
        revealAllNow();
        if (slides[0]) slides[0].scrollIntoView();
        if (typeof loadFromStorage === 'function') loadFromStorage();
        if (typeof _initToolbarDrag === 'function') _initToolbarDrag();
        if (typeof _initI18n === 'function') _initI18n();
    } catch(err) {
        console.warn('[load handler]', err);
    }
});

/* ====== i18n (todo20) ====== */
var I18N_STRINGS = {
    zh: {
        edit: '编辑', exit_edit: '退出编辑',
        preview: '预览', preview_sub: '仅限当前窗口',
        undo: '撤销',
        export: '导出干净版', export_sub: '去掉编辑器，留下你的改动',
        reset: '重置',
        saved: '已保存 ✓',
        panel_title: '样式面板',
        tab_colors: '颜色', tab_presets: '风格', tab_layout: '布局', tab_size: '字号',
        style_prompt: '风格 Prompt',
        style_prompt_hint: '点击复制风格 Prompt 给 AI',
        style_card_flow_hint: '复制后 → 粘贴到 AI 对话 → AI 会改写 CSS',
        toast_prompt_copied: '✓ 风格 prompt 已复制，去粘贴给 AI',
        toast_copy_failed: '复制失败，请手动复制',
        autosave_hint: '✓ 修改自动保存到当前浏览器（导出请用顶部工具栏）',
        reset_default: '🔄 恢复默认设置',
        tooltip_pinned: '📌 已固定 · 点击下方跳转面板',
        tooltip_hover: '↖ 此处可调整：',
        tooltip_pin_hint: 'P 键固定',
        preset_name_cloud_native: '云原生企业',
        preset_name_swiss_grid: '瑞士网格',
        preset_name_editorial_magazine: '杂志编辑',
        preset_name_sunlit_warmth: '阳光手账',
        preset_name_terminal_hacker: '终端骇客',
        preset_name_y2k_kawaii: 'Y2K 可爱数字',
    },
    en: {
        edit: 'Edit', exit_edit: 'Exit',
        preview: 'Preview', preview_sub: 'Current window only',
        undo: 'Undo',
        export: 'Export Clean', export_sub: 'Strip editor, keep your edits',
        reset: 'Reset',
        saved: 'Saved ✓',
        panel_title: 'Style Panel',
        tab_colors: 'Colors', tab_presets: 'Styles', tab_layout: 'Layout', tab_size: 'Size',
        style_prompt: 'Style Prompts',
        style_prompt_hint: 'Click to copy a style prompt for AI',
        style_card_flow_hint: 'Copy → paste into your AI chat → AI rewrites CSS',
        toast_prompt_copied: '✓ Style prompt copied — paste into your AI',
        toast_copy_failed: 'Copy failed, please copy manually',
        autosave_hint: '✓ Edits auto-saved to this browser (use top toolbar to export)',
        reset_default: '🔄 Restore Defaults',
        tooltip_pinned: '📌 Pinned · Click below to jump to panel',
        tooltip_hover: '↖ Adjustable here:',
        tooltip_pin_hint: 'Press P to pin',
        preset_name_cloud_native: 'Cloud Native',
        preset_name_swiss_grid: 'Swiss Grid',
        preset_name_editorial_magazine: 'Editorial Magazine',
        preset_name_sunlit_warmth: 'Sunlit Warmth',
        preset_name_terminal_hacker: 'Terminal Hacker',
        preset_name_y2k_kawaii: 'Y2K Kawaii',
    }
};

function _initI18n() {
    var saved = null;
    try { saved = localStorage.getItem('hve_lang'); } catch(_) {}
    var lang = saved;
    if (!lang) {
        var navLang = (navigator.language || 'en').toLowerCase();
        lang = navLang.indexOf('zh') === 0 ? 'zh' : 'en';
    }
    window.__hveLang = lang;
    _applyI18n(lang);
}

function _applyI18n(lang) {
    var dict = I18N_STRINGS[lang] || I18N_STRINGS.zh;
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
        var key = el.getAttribute('data-i18n');
        if (dict[key] != null) el.textContent = dict[key];
    });
    var lbl = document.getElementById('langLabel');
    if (lbl) {
        // v1.8.3 todo59: 双显 "中 / EN"，激活态 class
        if (lbl.classList.contains('lang-pair')) {
            lbl.classList.toggle('zh-active', lang === 'zh');
            lbl.classList.toggle('en-active', lang === 'en');
        } else {
            lbl.textContent = (lang === 'zh') ? '中' : 'EN';
        }
    }
    // If currently in edit mode, the toggle button text should be "exit_edit"
    var btnEdit = document.getElementById('btnEditText');
    if (btnEdit && document.body.classList.contains('edit-mode')) {
        btnEdit.textContent = dict.exit_edit;
    }
}

function switchLang() {
    var cur = window.__hveLang || 'zh';
    var next = (cur === 'zh') ? 'en' : 'zh';
    window.__hveLang = next;
    try { localStorage.setItem('hve_lang', next); } catch(_) {}
    _applyI18n(next);
}

/* ====== Toolbar drag (todo19) ====== */
function _initToolbarDrag() {
    var toolbar = document.getElementById('editToolbar');
    var handle = document.getElementById('toolbarDragHandle');
    if (!toolbar || !handle) return;

    // Restore saved position
    try {
        var saved = JSON.parse(localStorage.getItem('hve_toolbar_pos') || 'null');
        if (saved && typeof saved.left === 'number' && typeof saved.top === 'number') {
            _setToolbarPos(toolbar, saved.left, saved.top);
        }
    } catch(_) {}

    var dragState = null;
    handle.addEventListener('mousedown', function(e) {
        e.preventDefault();
        var rect = toolbar.getBoundingClientRect();
        dragState = { dx: e.clientX - rect.left, dy: e.clientY - rect.top, w: rect.width, h: rect.height };
        toolbar.classList.add('dragging');
    });
    document.addEventListener('mousemove', function(e) {
        if (!dragState) return;
        var left = e.clientX - dragState.dx;
        var top  = e.clientY - dragState.dy;
        // Clamp to viewport
        var maxL = window.innerWidth  - dragState.w - 4;
        var maxT = window.innerHeight - dragState.h - 4;
        left = Math.max(4, Math.min(maxL, left));
        top  = Math.max(4, Math.min(maxT, top));
        _setToolbarPos(toolbar, left, top);
    });
    document.addEventListener('mouseup', function() {
        if (!dragState) return;
        dragState = null;
        toolbar.classList.remove('dragging');
        var r = toolbar.getBoundingClientRect();
        try { localStorage.setItem('hve_toolbar_pos', JSON.stringify({ left: r.left, top: r.top })); } catch(_) {}
    });

    // Re-clamp on resize
    window.addEventListener('resize', function() {
        var r = toolbar.getBoundingClientRect();
        if (r.right > window.innerWidth || r.bottom > window.innerHeight) {
            var left = Math.min(r.left, window.innerWidth - r.width - 4);
            var top  = Math.min(r.top,  window.innerHeight - r.height - 4);
            _setToolbarPos(toolbar, Math.max(4, left), Math.max(4, top));
        }
    });
}

function _setToolbarPos(toolbar, left, top) {
    toolbar.style.left = left + 'px';
    toolbar.style.top  = top  + 'px';
    toolbar.style.right = 'auto';  // override CSS default
}
// Run immediately too (in case load fires before this runs)
revealAllNow();
updateVisibility();

/* FAILSAFE: 1.5s 后如果仍有 .reveal 元素不可见，启用 CSS 兜底 */
setTimeout(() => {
    const invisible = [...document.querySelectorAll('.reveal')].filter(el => !el.classList.contains('visible'));
    if (invisible.length > 0) {
        console.warn(`[failsafe] ${invisible.length} .reveal elements still hidden, enabling CSS fallback`);
        document.documentElement.classList.add('reveal-fallback');
    }
}, 1500);

/* Keyboard nav + E key for edit mode */
document.addEventListener('keydown', e => {
    // Edit mode shortcuts
    if ((e.metaKey || e.ctrlKey) && e.key === 's') {
        e.preventDefault();
        saveToStorage();
        return;
    }
    if (e.key.toLowerCase() === 'e' && !e.metaKey && !e.ctrlKey && !e.altKey) {
        // Don't toggle if user is typing in a contenteditable element
        if (document.activeElement.getAttribute('contenteditable') !== 'true') {
            toggleEditMode();
        }
        return;
    }
    // Navigation (only when not editing text)
    if (document.activeElement.getAttribute('contenteditable') !== 'true') {
        if (e.key === 'ArrowDown' || e.key === ' ' || e.key === 'PageDown') {
            e.preventDefault();
            const idx = [...slides].findIndex(s => s.getBoundingClientRect().top >= -1 && s.getBoundingClientRect().bottom > 1);
            if (idx < slides.length - 1) slides[idx + 1].scrollIntoView({ behavior: 'smooth' });
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
            e.preventDefault();
            const idx = [...slides].findIndex(s => s.getBoundingClientRect().top >= -1 && s.getBoundingClientRect().bottom > 1);
            if (idx > 0) slides[idx - 1].scrollIntoView({ behavior: 'smooth' });
        }
    }
});


/* =====================================================
   EDIT MODE ENGINE
   ===================================================== */

/* STORAGE_KEY: 必须每个 HTML 文件**唯一**，否则不同 html 之间会通过 localStorage
   互相污染（尤其是 file:// 协议下所有本地 html 共享同一个 origin）。
   策略：用 location.pathname + document.title 哈希，每个文件天然隔离。
   ⚠️ 已知限制：Safari 对 file:// 协议的每个标签页分配独立 origin，
   导致同一文件在不同标签页间 localStorage 不共享。"导出 .html"（todo13）
   是跨标签页/设备持久化的唯一可靠手段。 */
function _editorStorageKey() {
    // decodeURIComponent 确保 WorkBuddy(空格) 和 Chrome(%20) 生成同一 key
    const raw = decodeURIComponent(location.pathname || '') + '|' + (document.title || '');
    // 简单 djb2 哈希
    let h = 5381;
    for (let i = 0; i < raw.length; i++) {
        h = ((h << 5) + h + raw.charCodeAt(i)) | 0;
    }
    return 'html-visual-editor::' + (h >>> 0).toString(36) + '::' + (raw.length & 0xffff).toString(36);
}
const STORAGE_KEY = _editorStorageKey();

/* =====================================================
   UNDO / HISTORY SYSTEM
   Captures snapshot before each meaningful change.
   Up to 30 steps (can increase if needed).
   ===================================================== */
const history = [];          // array of { type, data } snapshots
const MAX_HISTORY = 30;

function pushHistory(type, data) {
    // Deduplicate: skip if same as last entry
    const last = history[history.length - 1];
    if (last && last.type === type && JSON.stringify(last.data) === JSON.stringify(data)) return;
    history.push({ type, data });
    if (history.length > MAX_HISTORY) history.shift();
    updateUndoBtn();
}

function updateUndoBtn() {
    const btn = document.getElementById('btnUndo');
    if (btn) btn.disabled = history.length === 0;
}

/** Lightweight toast notification */
function showToast(msg, duration = 2000) {
    let toast = document.getElementById('editHint');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'editHint';
        toast.style.cssText = 'position:fixed;bottom:3rem;left:50%;transform:translateX(-50%);z-index:9997;padding:7px 18px;background:rgba(0,0,0,0.85);border:1px solid rgba(255,255,255,0.15);border-radius:100px;font-family:var(--font-body,system-ui);font-size:12px;color:#fff;pointer-events:none;white-space:nowrap;opacity:0;transition:opacity 0.3s';
        document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.opacity = '1';
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => { toast.style.opacity = '0'; }, duration);
}

function undoLast() {
    if (history.length === 0) return;
    const { type, data } = history.pop();
    updateUndoBtn();

    if (type === 'color') {
        document.documentElement.style.setProperty(data.varName, data.oldVal);
        // Sync UI
        document.querySelectorAll(`.color-row input[data-var="${data.varName}"]`).forEach(input => {
            const row = input.closest('.color-row');
            row.querySelector('.color-hex').value = data.oldVal.toUpperCase();
            row.querySelector('.color-swatch').style.background = data.oldVal;
            if (input.type === 'color') input.value = data.oldVal;
        });
    } else if (type === 'text') {
        const el = document.querySelector(`[data-editable="${data.id}"]`) ||
                   document.querySelectorAll('[data-editable]')[data.idx];
        if (el) {
            el.innerHTML = data.oldText;
            el.normalize();
        }
    } else if (type === 'size') {
        document.documentElement.style.setProperty(data.varName, data.oldVal);
        const slider = document.querySelector(`[data-var="${data.varName}"]`);
        if (slider) {
            const match = data.oldVal.match(/clamp\([^,]+,\s*([^,]+)/);
            if (match) slider.value = parseFloat(match[1]);
        }
    } else if (type === 'preset') {
        Object.entries(data.oldStyles).forEach(([v, val]) => {
            document.documentElement.style.setProperty(v, val);
        });
        // Sync all UI controls
        document.querySelectorAll('.color-row').forEach(row => {
            const ci = row.querySelector('input[type="color"]');
            const hi = row.querySelector('.color-hex');
            const sw = row.querySelector('.color-swatch');
            const vn = ci?.dataset.var;
            if (vn && data.oldStyles[vn] !== undefined) {
                const v = data.oldStyles[vn];
                if (ci) ci.value = v.startsWith('#') ? v : '#888888';
                if (hi) hi.value = v.startsWith('#') ? v.toUpperCase() : v;
                if (sw) sw.style.background = v.startsWith('#') ? v : '#888888';
            }
        });
    } else if (type === 'layout') {
        const targets = document.querySelectorAll(data.target);
        targets.forEach((el, i) => {
            const oldVal = data.oldVals[i];
            if (oldVal) {
                el.style.setProperty(data.prop, oldVal);
            } else {
                el.style.removeProperty(data.prop);
            }
        });
    }

    // Brief flash to confirm undo
    document.body.style.transition = 'opacity 0.1s';
    document.body.style.opacity = '0.7';
    setTimeout(() => { document.body.style.opacity = ''; }, 150);
    showToast('↩ 已撤销上一步', 1500);
}

// === applyColor/applyHex/applyPreset defined below with full history support ===
document.addEventListener('focusin', e => {
    if (!e.target.hasAttribute('data-editable') || !e.target.getAttribute('contenteditable')) return;
    if (e.target.dataset._savedText !== undefined) return;
    e.target.dataset._savedText = e.target.innerHTML.trim();
});

/** Capture on blur */
document.addEventListener('blur', e => {
    if (!e.target.hasAttribute('data-editable')) return;
    const saved = e.target.dataset._savedText;
    if (saved !== undefined && saved !== e.target.innerHTML.trim()) {
        const idx = [...document.querySelectorAll('[data-editable]')].indexOf(e.target);
        pushHistory('text', { idx, oldText: saved });
    }
    delete e.target.dataset._savedText;
}, true);

// Default values for reset
/* 默认值——host HTML 可在 editor-core.js 之后用
   Object.assign(DEFAULT_COLORS, { ...你的色板... }); 覆盖
   或直接重新赋值 window.DEFAULT_COLORS = { ... }; */
var DEFAULT_COLORS = window.DEFAULT_COLORS = window.DEFAULT_COLORS || {
    '--accent': '#FF5722',
    '--card-bg': '#FF5722',
    '--bg-primary': '#1a1a1a',
    '--text-primary': '#ffffff',
    '--text-secondary': '#b0b0b0',
    '--text-on-card': '#1a1a1a',
    '--safe-green': '#00E676',
    '--warn-yellow': '#FFD600',
    '--danger-red': '#FF1744'
};

var PRESETS = window.PRESETS = window.PRESETS || {
    'bold-signal': {
        '--accent': '#FF5722', '--card-bg': '#FF5722', '--card-alt': '#FF7043',
        '--bg-primary': '#1a1a1a', '--bg-gradient': 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a2e 100%)',
        '--text-primary': '#ffffff', '--text-on-card': '#1a1a1a', '--text-secondary': '#b0b0b0',
        '--accent-glow': 'rgba(255, 87, 34, 0.25)',
        '--safe-green': '#00E676', '--warn-yellow': '#FFD600', '--danger-red': '#FF1744'
    },
    'ocean-blue': {
        '--accent': '#3B82F6', '--card-bg': '#2563EB', '--card-alt': '#3B82F6',
        '--bg-primary': '#0c1929', '--bg-gradient': 'linear-gradient(135deg, #0c1929 0%, #1a2744 50%, #0f172a 100%)',
        '--text-primary': '#e2e8f0', '--text-on-card': '#ffffff', '--text-secondary': '#94a3b8',
        '--accent-glow': 'rgba(59, 130, 246, 0.25)',
        '--safe-green': '#34D399', '--warn-yellow': '#FBBF24', '--danger-red': '#F87171'
    },
    'forest': {
        '--accent': '#22C55E', '--card-bg': '#16A34A', '--card-alt': '#22C55E',
        '--bg-primary': '#0a1612', '--bg-gradient': 'linear-gradient(135deg, #0a1612 0%, #142319 50%, #0d1a14 100%)',
        '--text-primary': '#ecfdf5', '--text-on-card': '#ffffff', '--text-secondary': '#86efac',
        '--accent-glow': 'rgba(34, 197, 94, 0.25)',
        '--safe-green': '#4ADE80', '--warn-yellow': '#FACC15', '--danger-red': '#FB7185'
    },
    'royal-purple': {
        '--accent': '#A78BFA', '--card-bg': '#8B5CF6', '--card-alt': '#A78BFA',
        '--bg-primary': '#131026', '--bg-gradient': 'linear-gradient(135deg, #131026 0%, #1e1a3d 50%, #0f0d1a 100%)',
        '--text-primary': '#ede9fe', '--text-on-card': '#ffffff', '--text-secondary': '#c4b5fd',
        '--accent-glow': 'rgba(167, 139, 250, 0.25)',
        '--safe-green': '#34D399', '--warn-yellow': '#FBBF24', '--danger-red': '#FB7185'
    },
    'rose-gold': {
        '--accent': '#F472B6', '--card-bg': '#EC4899', '--card-alt': '#F472B6',
        '--bg-primary': '#1a1216', '--bg-gradient': 'linear-gradient(135deg, #1a1216 0%, #2d1a24 50%, #1a1218 100%)',
        '--text-primary': '#fce7f3', '--text-on-card': '#ffffff', '--text-secondary': '#f9a8d4',
        '--accent-glow': 'rgba(244, 114, 182, 0.25)',
        '--safe-green': '#34D399', '--warn-yellow': '#FCD34D', '--danger-red': '#FCA5A5'
    },
    'mono-dark': {
        '--accent': '#e5e5e5', '--card-bg': '#404040', '--card-alt': '#525252',
        '--bg-primary': '#0a0a0a', '--bg-gradient': 'linear-gradient(135deg, #0a0a0a 0%, #171717 50%, #0d0d0d 100%)',
        '--text-primary': '#fafafa', '--text-on-card': '#fafafa', '--text-secondary': '#a3a3a3',
        '--accent-glow': 'rgba(229, 229, 229, 0.15)',
        '--safe-green': '#aaaaaa', '--warn-yellow': '#999999', '--danger-red': '#888888'
    }
};

/** Toggle edit mode on/off */
function toggleEditMode() {
    const isEdit = !document.body.classList.contains('edit-mode');
    document.body.classList.toggle('edit-mode', isEdit);

    // Toggle contenteditable on all marked elements
    document.querySelectorAll('[data-editable]').forEach(el => {
        el.setAttribute('contenteditable', isEdit ? 'true' : 'false');
    });

    // Update toolbar button state
    const btn = document.getElementById('btnToggleEdit');
    if (btn) btn.classList.toggle('active', isEdit);
    /* todo20: use i18n dict */
    var lang = window.__hveLang || 'zh';
    var dict = (window.I18N_STRINGS && window.I18N_STRINGS[lang]) || { edit: '编辑', exit_edit: '退出编辑' };
    document.getElementById('btnEditText').textContent = isEdit ? dict.exit_edit : dict.edit;

    // Show/hide hint
    const hint = document.getElementById('editHint');
    hint.classList.toggle('visible', isEdit);
    setTimeout(() => hint.classList.remove('visible'), 3500);

    // Auto-focus first editable element for immediate typing
    if (isEdit) {
        setTimeout(() => {
            const firstEditable = document.querySelector('[data-editable]');
            if (firstEditable) {
                firstEditable.focus();
                // Place cursor at end of existing text
                const range = document.createRange();
                const sel = window.getSelection();
                range.selectNodeContents(firstEditable);
                range.collapse(false);
                sel.removeAllRanges();
                sel.addRange(range);
            }
        }, 100);
    }
}

/** Apply color from color picker */
function applyColor(input) {
    const val = input.value;
    const varName = input.dataset.var;

    // Record old value for undo (todo25-B1)
    let oldVal = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
    if (!oldVal && window.DEFAULT_COLORS && window.DEFAULT_COLORS[varName]) {
        oldVal = window.DEFAULT_COLORS[varName];
    }
    if (typeof pushHistory === 'function') {
        pushHistory('color', { varName, oldVal });
    }

    document.documentElement.style.setProperty(varName, val);

    // Update sibling hex input and swatch
    const row = input.closest('.color-row');
    const hexInput = row.querySelector('.color-hex');
    const swatch = row.querySelector('.color-swatch');
    if (hexInput) hexInput.value = val.toUpperCase();
    if (swatch) swatch.style.background = val;

    // Sync related variables
    syncRelatedVars(varName, val);
}

/** Preview color on drag (before releasing) */
function previewColor(input) {
    applyColor(input);
}

/** Apply color from hex text input */
function applyHex(input) {
    let val = input.value.trim();
    if (!val.startsWith('#')) val = '#' + val;
    if (/^#[0-9A-Fa-f]{6}$/.test(val)) {
        const varName = input.dataset.var;

        // Record old value for undo (todo25-B1)
        let oldVal = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
        if (!oldVal && window.DEFAULT_COLORS && window.DEFAULT_COLORS[varName]) {
            oldVal = window.DEFAULT_COLORS[varName];
        }
        if (typeof pushHistory === 'function') {
            pushHistory('color', { varName, oldVal });
        }

        document.documentElement.style.setProperty(varName, val.toUpperCase());
        const row = input.closest('.color-row');
        const colorInput = row.querySelector('input[type="color"]');
        const swatch = row.querySelector('.color-swatch');
        if (colorInput) colorInput.value = val;
        if (swatch) swatch.style.background = val;
        syncRelatedVars(varName, val.toUpperCase());
    }
}

/** Sync accent → card-bg / accent-glow etc. */
function syncRelatedVars(varName, val) {
    if (varName === '--accent') {
        document.documentElement.style.setProperty('--card-bg', val);
        document.documentElement.style.setProperty('--accent-glow', val + '40'); // rough alpha
        // Also update card-bg UI
        const cbRow = document.querySelector('[data-var="--card-bg"]?.closest(".color-row")');
        if (cbRow) {
            cbRow.querySelector('.color-swatch').style.background = val;
            cbRow.querySelector('input[type="color"]').value = val;
            cbRow.querySelector('.color-hex').value = val.toUpperCase();
        }
    }
    if (varName === '--bg-primary') {
        // Rebuild gradient from new bg
        const grad = `linear-gradient(135deg, ${val} 0%, ${lighten(val, 20)} 50%, ${lighten(val, 10)} 100%)`;
        document.documentElement.style.setProperty('--bg-gradient', grad);
    }

    // v1.7.0 todo25/26: 收敛后的"同组联动"
    // HVE_COLOR_GROUP: {anyVar: representativeVar}
    // 当用户修改 representative 时，把所有指向该 representative 的 alias 一并更新
    try {
        const group = window.HVE_COLOR_GROUP || {};
        // 把所有 alias 找出来
        const aliases = Object.keys(group).filter(k => group[k] === varName && k !== varName);
        aliases.forEach(alias => {
            document.documentElement.style.setProperty(alias, val);
        });
    } catch (e) { /* noop */ }
}

/** Simple color lightener helper */
function lighten(hex, pct) {
    let r = parseInt(hex.slice(1,3), 16);
    let g = parseInt(hex.slice(3,5), 16);
    let b = parseInt(hex.slice(5,7), 16);
    r = Math.min(255, Math.floor(r + (255 - r) * pct / 100));
    g = Math.min(255, Math.floor(g + (255 - g) * pct / 100));
    b = Math.min(255, Math.floor(b + (255 - b) * pct / 100));
    return '#' + [r,g,b].map(x => x.toString(16).padStart(2,'0')).join('');
}

/** Check if a hex color is dark (for contrast decisions) */
function _isColorDarkJS(hex) {
    if (!hex || !hex.startsWith('#')) return true;
    hex = hex.replace('#', '');
    if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
    if (hex.length < 6) return true;
    var r = parseInt(hex.substring(0,2), 16) / 255;
    var g = parseInt(hex.substring(2,4), 16) / 255;
    var b = parseInt(hex.substring(4,6), 16) / 255;
    return (0.299 * r + 0.587 * g + 0.114 * b) < 0.5;
}

/**
 * v1.3: After a preset is applied, dynamically inject <style> to override
 * banner/footer hardcoded text colors based on the current banner background.
 * This fixes the "banner doesn't change with theme" issue (todo16B).
 */
function _applyBannerFooterContrast() {
    /* Get the effective banner background color from --banner-bg-2 (the first gradient stop) */
    var bannerBg = getComputedStyle(document.documentElement).getPropertyValue('--banner-bg-2').trim();
    /* Fallback: try to detect from .banner element's computed background */
    if (!bannerBg || !bannerBg.startsWith('#')) {
        var bannerEl = document.querySelector('.banner');
        if (bannerEl) {
            var bgComputed = getComputedStyle(bannerEl).backgroundColor;
            /* Parse rgb(r,g,b) → hex */
            var rgbMatch = bgComputed.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
            if (rgbMatch) {
                bannerBg = '#' + [rgbMatch[1], rgbMatch[2], rgbMatch[3]].map(function(x) {
                    return parseInt(x).toString(16).padStart(2, '0');
                }).join('');
            }
        }
    }
    if (!bannerBg || !bannerBg.startsWith('#')) return;

    var isDark = _isColorDarkJS(bannerBg);
    var textColor = isDark ? '#ffffff' : '#1a1a1a';
    var subColor = isDark ? 'rgba(255,255,255,0.65)' : 'rgba(0,0,0,0.55)';
    var tagBg = isDark ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.06)';
    var tagBorder = isDark ? 'rgba(255,255,255,0.22)' : 'rgba(0,0,0,0.12)';
    var pillBg = isDark ? 'rgba(255,255,255,0.10)' : 'rgba(0,0,0,0.05)';
    var pillBorder = isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.10)';

    var styleEl = document.getElementById('html-visual-editor-banner-override');
    if (!styleEl) {
        styleEl = document.createElement('style');
        styleEl.id = 'html-visual-editor-banner-override';
        document.head.appendChild(styleEl);
    }
    styleEl.textContent =
        '.banner h1, .banner h2, .banner h3 { color: ' + textColor + ' !important; }' +
        '.banner-sub, .banner p, .banner .banner-sub { color: ' + subColor + ' !important; }' +
        '.banner-tag { background: ' + tagBg + ' !important; border-color: ' + tagBorder + ' !important; color: ' + textColor + ' !important; }' +
        '.footer-left, .footer p, .footer span { color: ' + subColor + ' !important; }' +
        '.footer-pill, .footer .pill { background: ' + pillBg + ' !important; border-color: ' + pillBorder + ' !important; color: ' + subColor + ' !important; }';
}

/**
 * v1.3: General contrast correction pass after preset application.
 * Scans text elements, checks WCAG 4.5:1 contrast ratio against
 * their computed background, and auto-flips text color if needed.
 */
function _applyContrastCorrection() {
    /* Collect text elements: data-editable + common text containers */
    /* todo22-C: First, clear any previous inline color corrections so we re-evaluate from scratch */
    document.querySelectorAll('[data-hve-corrected="1"]').forEach(function(el) {
        el.style.removeProperty('color');
        el.removeAttribute('data-hve-corrected');
    });

    var targets = document.querySelectorAll(
        '[data-editable], h1, h2, h3, h4, h5, h6, p, li, th, td, span, .stat-card .number, .stat-card .label, [style*="color"]'
    );
    var fixes = [];  /* {selector, color} pairs to inject */

    targets.forEach(function(el) {
        /* Skip editor UI elements */
        if (el.closest('.edit-toolbar') || el.closest('.edit-panel') || el.closest('.edit-hint')) return;
        if (el.closest('.nav-dots') || el.closest('.keyboard-hint')) return;

        var fgRaw = getComputedStyle(el).color;
        var fg = _rgbaToHex(fgRaw);  /* todo22-C: convert rgb() → hex first */
        var bg = _getEffectiveBackground(el);
        if (!fg || !bg || !fg.startsWith('#') || !bg.startsWith('#')) return;

        var ratio = _contrastRatio(fg, bg);
        if (ratio < 4.5) {
            /* Low contrast — flip based on background brightness */
            var isDarkBg = _isColorDarkJS(bg);
            var newColor = isDarkBg ? '#ffffff' : '#1a1a1a';
            /* Use inline style for precise targeting; mark for cleanup on next pass */
            el.style.setProperty('color', newColor, 'important');
            el.setAttribute('data-hve-corrected', '1');
        }
    });
}

/**
 * Get the effective background color of an element by walking up the DOM
 * until a non-transparent background is found.
 */
function _getEffectiveBackground(el) {
    var current = el;
    while (current && current !== document.body) {
        var bg = getComputedStyle(current).backgroundColor;
        if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
            return _rgbaToHex(bg);
        }
        current = current.parentElement;
    }
    /* Fallback: body or html background */
    var bodyBg = getComputedStyle(document.body).backgroundColor;
    if (bodyBg && bodyBg !== 'rgba(0, 0, 0, 0)' && bodyBg !== 'transparent') {
        return _rgbaToHex(bodyBg);
    }
    return '#ffffff';  /* default white */
}

/** Convert rgb/rgba string to hex */
function _rgbaToHex(rgb) {
    var match = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
    if (!match) return rgb;
    return '#' + [match[1], match[2], match[3]].map(function(x) {
        return parseInt(x).toString(16).padStart(2, '0');
    }).join('');
}

/**
 * Calculate WCAG 2.0 contrast ratio between two colors.
 * Both fg and bg should be hex strings like '#1a1a1a'.
 */
function _contrastRatio(fg, bg) {
    var l1 = _relativeLuminance(fg);
    var l2 = _relativeLuminance(bg);
    var lighter = Math.max(l1, l2);
    var darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
}

/** WCAG relative luminance */
function _relativeLuminance(hex) {
    if (!hex || !hex.startsWith('#')) return 0;
    hex = hex.replace('#', '');
    if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
    if (hex.length < 6) return 0;
    var r = parseInt(hex.substring(0,2), 16) / 255;
    var g = parseInt(hex.substring(2,4), 16) / 255;
    var b = parseInt(hex.substring(4,6), 16) / 255;
    r = r <= 0.03928 ? r / 12.92 : Math.pow((r + 0.055) / 1.055, 2.4);
    g = g <= 0.03928 ? g / 12.92 : Math.pow((g + 0.055) / 1.055, 2.4);
    b = b <= 0.03928 ? b / 12.92 : Math.pow((b + 0.055) / 1.055, 2.4);
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/** todo23: Apply a preset — simplified, only supports 'original' (used by Reset button) */
function applyPreset(name) {
    if (name !== 'original') {
        console.warn('[html-visual-editor] applyPreset only supports "original" since todo23. Use copyStylePrompt() for style themes.');
        return;
    }
    const original = (window.PRESETS && PRESETS['original']) || {};
    if (!Object.keys(original).length) {
        console.warn('[html-visual-editor] PRESETS.original is empty.');
        return;
    }

    // Capture current state for undo
    const oldStyles = {};
    Object.keys(original).forEach(v => {
        oldStyles[v] = getComputedStyle(document.documentElement).getPropertyValue(v).trim();
    });
    if (typeof pushHistory === 'function') pushHistory('preset', { oldStyles });

    // Reset all vars to original
    Object.entries(original).forEach(([varName, val]) => {
        document.documentElement.style.setProperty(varName, val);
    });

    // Sync color-row UI back to original values
    document.querySelectorAll('.color-row').forEach(row => {
        const colorInput = row.querySelector('input[type="color"]');
        const hexInput = row.querySelector('.color-hex');
        const swatch = row.querySelector('.color-swatch');
        const varName = colorInput?.dataset.var;
        if (!varName) return;
        const v = (original[varName] || '').trim();
        if (v) {
            if (colorInput) colorInput.value = v.startsWith('#') ? v : '#888888';
            if (hexInput) hexInput.value = v.startsWith('#') ? v.toUpperCase() : v;
            if (swatch) swatch.style.background = v.startsWith('#') ? v : '#888888';
        }
    });

    // Apply banner/footer contrast correction + general contrast correction
    _applyBannerFooterContrast();
    _applyContrastCorrection();
}

/* ====== todo23: Style prompt copy ====== */
var TPL_PROMPT_ZH = [
    '请按以下风格重新设计这个 HTML 的视觉样式（保留结构、只改 CSS）：',
    '',
    '风格名：{name_zh}（{name_en}）',
    '氛围：{vibe_zh}',
    '关键色（参考，可微调以保证对比度）：',
    '- 背景 bg：{palette.bg}',
    '- 主色 accent：{palette.accent}',
    '- 次色 secondary：{palette.secondary}',
    '- 主文字 text：{palette.text}',
    '- 辅文字 text-soft：{palette.text_soft}',
    '- 分割线 line：{palette.line}',
    '',
    '硬约束：',
    '1. 保留所有 data-editable 标记，不要删改任何元素属性。',
    '2. 保留所有 class 名与 id，不改 HTML 结构。',
    '3. 只修改 <style> 块（或 :root 中的 CSS 变量）；不要新增 <script>。',
    '4. 文字与背景对比度需通过 WCAG AA；若色板对比度不足，请就近微调。',
    '5. 不要引入外部字体/CDN/图片资源。'
].join('\n');

var TPL_PROMPT_EN = [
    'Please restyle this HTML in the following aesthetic (keep the structure, only change CSS):',
    '',
    'Style: {name_en} ({name_zh})',
    'Vibe: {vibe_en}',
    'Key palette (reference, tweak slightly for contrast if needed):',
    '- bg:        {palette.bg}',
    '- accent:    {palette.accent}',
    '- secondary: {palette.secondary}',
    '- text:      {palette.text}',
    '- text-soft: {palette.text_soft}',
    '- line:      {palette.line}',
    '',
    'Hard constraints:',
    '1. Preserve every data-editable attribute and element attribute.',
    '2. Keep all class names and ids; do not change HTML structure.',
    '3. Only modify the <style> block (or :root CSS variables); do not add <script>.',
    '4. Ensure WCAG AA contrast; nudge colors locally if the palette falls short.',
    '5. No external fonts / CDNs / images.'
].join('\n');

function copyStylePrompt(id) {
    var data = (window.HVE_STYLE_PRESETS || {})[id];
    var lang = window.__hveLang || 'zh';
    var dict = (window.I18N_STRINGS || {})[lang] || {};
    if (!data) {
        showToast('Style preset not found: ' + id);
        return;
    }

    var tpl = (lang === 'zh') ? TPL_PROMPT_ZH : TPL_PROMPT_EN;
    var prompt = tpl
        .replace(/\{name_zh\}/g,         data.name_zh || '')
        .replace(/\{name_en\}/g,         data.name_en || '')
        .replace(/\{vibe_zh\}/g,         data.vibe_zh || '')
        .replace(/\{vibe_en\}/g,         data.vibe_en || '')
        .replace(/\{palette\.bg\}/g,        (data.palette && data.palette.bg)        || '')
        .replace(/\{palette\.accent\}/g,    (data.palette && data.palette.accent)    || '')
        .replace(/\{palette\.secondary\}/g, (data.palette && data.palette.secondary) || '')
        .replace(/\{palette\.text\}/g,      (data.palette && data.palette.text)      || '')
        .replace(/\{palette\.text_soft\}/g, (data.palette && data.palette.text_soft) || '')
        .replace(/\{palette\.line\}/g,      (data.palette && data.palette.line)      || '');

    _copyToClipboard(prompt).then(function(ok) {
        showToast(ok ? (dict.toast_prompt_copied || '✓ Copied') : (dict.toast_copy_failed || 'Copy failed'), 2500);
    });
}

function _copyToClipboard(text) {
    // Primary: async Clipboard API (requires secure context)
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text)
            .then(function() { return true; })
            .catch(function() { return _execCopy(text); });
    }
    // Fallback for file:// / older Safari
    return Promise.resolve(_execCopy(text));
}

function _execCopy(text) {
    try {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.cssText = 'position:fixed;left:-9999px;top:0;opacity:0;';
        document.body.appendChild(ta);
        ta.select();
        var ok = document.execCommand('copy');
        document.body.removeChild(ta);
        return ok;
    } catch (e) {
        console.warn('[copyStylePrompt] fallback failed', e);
        return false;
    }
}

/** Known safe clamp bounds for each size variable
    v16: 完全由 Python 动态生成并通过 window.SIZE_BOUNDS 注入 */
var SIZE_BOUNDS = window.SIZE_BOUNDS = window.SIZE_BOUNDS || {};

// =====================================================
//    ✦✦✦  REVERSE MAPPING: PAGE ELEMENT → PANEL CONTROL  ✦✦✦
//    Hover/click a page element → show tooltip pointing to panel
// =====================================================

/**
 * Page element class → list of panel controls (multiple dimensions per element)
 * v16: 硬编码金版 PEM 已移除，完全由 Python 动态生成并通过 window.PAGE_ELEMENT_TO_PANEL 注入
 * 如果 Python 未注入（极罕见），使用空对象
 */
var PAGE_ELEMENT_TO_PANEL = window.PAGE_ELEMENT_TO_PANEL = window.PAGE_ELEMENT_TO_PANEL || {};

/** Page element hover tooltip (reverse mapping) */
let _pageTooltip = null;
let _pinnedTooltip = false;     // 用户点击后被"固定"
let _pinnedSourceEl = null;     // 当前固定tooltip绑定的页面元素

/** Tab name → tab id 映射（支持中英双语） */
const TAB_NAME_TO_ID = {
    '颜色': 'colors', 'Colors': 'colors',
    '预设': 'presets', 'Styles': 'presets', 'Style': 'presets',
    '布局': 'layout', 'Layout': 'layout',
    '字号': 'size', 'Size': 'size',
};

/** Tab name → 颜色编码（支持中英双语） */
const TAB_COLORS = {
    '颜色': '#FF7043', 'Colors': '#FF7043',
    '预设': '#BA68C8', 'Styles': '#BA68C8', 'Style': '#BA68C8',
    '布局': '#81C784', 'Layout': '#81C784',
    '字号': '#64B5F6', 'Size': '#64B5F6',
};

/** i18n helper for runtime translation (todo25-B4) */
function _t(key) {
    const lang = window.__hveLang || 'zh';
    const dict = I18N_STRINGS[lang] || I18N_STRINGS['zh'];
    return dict[key] || key;
}

/** Translate tab name to display text based on current language */
function _translateTab(tabName) {
    const tabId = TAB_NAME_TO_ID[tabName];
    if (!tabId) return tabName;
    return _t('tab_' + tabId) || tabName;
}

/** Get safe tooltip max-right bound (accounts for panel width) */
function _getTooltipMaxRight() {
    const panel = document.querySelector('.edit-panel');
    if (panel) {
        return panel.offsetLeft - 10;
    }
    return window.innerWidth - 10;
}
function findPanelControl(tabName, rowName) {
    const tabId = TAB_NAME_TO_ID[tabName];
    if (!tabId) return null;
    const tabContent = document.getElementById('tab-' + tabId);
    if (!tabContent) return null;

    // 颜色tab：根据 .color-label 文本匹配
    const colorRows = tabContent.querySelectorAll('.color-row');
    for (const row of colorRows) {
        const label = row.querySelector('.color-label');
        if (label && label.textContent.trim() === rowName) return row;
    }

    // 字号/布局tab：根据 .slider-name 文本匹配
    const sliderRows = tabContent.querySelectorAll('.slider-row');
    for (const row of sliderRows) {
        const name = row.querySelector('.slider-name');
        if (name && name.textContent.trim() === rowName) return row;
    }

    return null;
}

/** 跳到指定面板控件：切换tab + 滚动到位 + 临时高亮 */
function jumpToPanelControl(tabName, rowName) {
    const tabId = TAB_NAME_TO_ID[tabName];
    if (tabId && typeof switchPanelTab === 'function') {
        switchPanelTab(tabId);
    }
    // 等tab切换动画后再滚动
    setTimeout(() => {
        const ctrl = findPanelControl(tabName, rowName);
        if (!ctrl) return;
        ctrl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        // 临时高亮3秒
        ctrl.style.transition = 'background 0.3s, box-shadow 0.3s';
        const oldBg = ctrl.style.background;
        const oldShadow = ctrl.style.boxShadow;
        ctrl.style.background = 'rgba(255, 200, 50, 0.18)';
        ctrl.style.boxShadow = '0 0 0 2px rgba(255, 200, 50, 0.6), 0 0 16px rgba(255,200,50,0.4)';
        ctrl.style.borderRadius = '8px';
        setTimeout(() => {
            ctrl.style.background = oldBg;
            ctrl.style.boxShadow = oldShadow;
        }, 2400);
    }, 60);
}

/** v1.8.2 todo31: build small extras (color swatch / hex / px value) for a tooltip row */
function _buildRowExtras(info, el) {
    let swatchHtml = '';
    let valueHtml = '';
    try {
        if (info.tab === '颜色' || info.tab === 'color' || info.tab === 'Color') {
            // 尝试找该 row 对应的面板控件，取其当前值
            const inputs = document.querySelectorAll('#tab-colors input[type="color"]');
            let hex = '';
            for (const inp of inputs) {
                const labelEl = inp.closest('.color-row')?.querySelector('.color-label');
                if (labelEl && labelEl.textContent.trim() === info.row.trim()) {
                    hex = (inp.value || '').toUpperCase();
                    break;
                }
            }
            if (hex) {
                swatchHtml = `<span style="display:inline-block;width:14px;height:14px;background:${hex};border-radius:3px;border:1px solid rgba(255,255,255,0.2);flex-shrink:0;"></span>`;
                valueHtml = `<span style="font-family:monospace;color:rgba(255,255,255,0.5);font-size:10.5px;flex-shrink:0;">${hex}</span>`;
            }
        } else if (info.tab === '字号' || info.tab === 'size' || info.tab === 'Size') {
            // 找对应 slider 取当前 px 值
            const sliders = document.querySelectorAll('#tab-size input[type="range"]');
            for (const sl of sliders) {
                const nameEl = sl.closest('.slider-row')?.querySelector('.slider-name');
                if (nameEl && nameEl.textContent.trim() === info.row.trim()) {
                    const unit = sl.dataset.unit || 'px';
                    valueHtml = `<span style="font-family:monospace;color:rgba(255,255,255,0.5);font-size:10.5px;flex-shrink:0;">${sl.value}${unit}</span>`;
                    break;
                }
            }
        } else if (info.tab === '布局' || info.tab === 'layout' || info.tab === 'Layout') {
            const sliders = document.querySelectorAll('#tab-layout input[type="range"]');
            for (const sl of sliders) {
                const nameEl = sl.closest('.slider-row')?.querySelector('.slider-name');
                if (nameEl && nameEl.textContent.trim() === info.row.trim()) {
                    const unit = sl.dataset.unit || '';
                    valueHtml = `<span style="font-family:monospace;color:rgba(255,255,255,0.5);font-size:10.5px;flex-shrink:0;">${sl.value}${unit}</span>`;
                    break;
                }
            }
        }
    } catch (e) { /* noop */ }
    return { swatchHtml, valueHtml };
}

/** v1.8.2 todo31: detect colors used on this element that are NOT in the panel; show alert + extract button */
function _buildMissingColorAlert(el) {
    if (!el || !el.nodeType) return '';
    try {
        const panelHexes = new Set();
        document.querySelectorAll('#tab-colors input[type="color"]').forEach(inp => {
            panelHexes.add((inp.value || '').toUpperCase());
        });

        const cs = getComputedStyle(el);
        const candidates = [];
        const fg = _rgbToHex(cs.color);
        const bg = _rgbToHex(cs.backgroundColor);
        if (fg && !panelHexes.has(fg)) candidates.push({ role: 'text', hex: fg });
        if (bg && !panelHexes.has(bg)) candidates.push({ role: 'bg', hex: bg });

        if (!candidates.length) return '';

        const lang = (typeof _currentLang === 'function') ? _currentLang() :
                     (localStorage.getItem('hve_lang') || (navigator.language||'en').toLowerCase().indexOf('zh') >= 0 ? 'zh' : 'en');
        const isZh = lang === 'zh';
        const itemsHtml = candidates.map(c => {
            const roleLabel = isZh
                ? (c.role === 'text' ? '文字色' : c.role === 'bg' ? '背景色' : '边框色')
                : (c.role === 'text' ? 'Text color' : c.role === 'bg' ? 'Bg color' : 'Border color');
            // v1.8.3.1: 提前判断 A 类 / 非 A 类，按钮分两种
            const inlineProp = _findInlineColorProp(el, c.hex);
            const isA = !!inlineProp;
            const btnLabel = isA
                ? (isZh ? '+ 一键提取为变量' : '+ Extract as variable')
                : (isZh ? '📋 复制提示让 AI 改' : '📋 Copy prompt for AI');
            const btnClass = isA ? 'tt-extract-btn' : 'tt-ai-hint-btn';
            const btnStyle = isA
                ? 'background:rgba(255,169,64,0.15);border:1px solid rgba(255,169,64,0.5);color:#FFA940;'
                : 'background:rgba(120,160,255,0.15);border:1px solid rgba(120,160,255,0.5);color:#7AA3FF;';
            return `
            <div style="display:flex;align-items:center;gap:8px;margin-top:6px;">
                <span style="display:inline-block;width:14px;height:14px;background:${c.hex};border-radius:3px;border:1px solid rgba(255,255,255,0.2);flex-shrink:0;"></span>
                <span style="font-size:11px;color:rgba(255,255,255,0.75);">${roleLabel}</span>
                <span style="font-family:monospace;color:rgba(255,255,255,0.55);font-size:10.5px;">${c.hex}</span>
                <button class="${btnClass}" data-hex="${c.hex}" data-role="${c.role}"
                    style="margin-left:auto;${btnStyle}font-size:10.5px;padding:3px 8px;border-radius:4px;cursor:pointer;flex-shrink:0;">
                    ${btnLabel}
                </button>
            </div>`;
        }).join('');

        const headLabel = isZh ? '⚠️ 检测到面板没有的颜色' : '⚠️ Colors not in the panel';
        return `
        <div style="margin-top:10px;padding:8px 10px;background:rgba(255,255,255,0.04);border-left:2px solid #FFA940;border-radius:4px;">
            <div style="font-size:11px;color:rgba(255,255,255,0.7);">${headLabel}</div>
            ${itemsHtml}
        </div>`;
    } catch (e) { return ''; }
}

/** Convert rgb()/rgba() string to #RRGGBB, or '' on failure */
function _rgbToHex(s) {
    if (!s) return '';
    const m = s.match(/rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)(?:[\s,]+([\d.]+))?\s*\)/);
    if (!m) {
        if (/^#[0-9a-fA-F]{6}$/.test(s)) return s.toUpperCase();
        return '';
    }
    const a = m[4] !== undefined ? parseFloat(m[4]) : 1;
    if (a < 0.05) return ''; // 透明，忽略
    const r = parseInt(m[1]); const g = parseInt(m[2]); const b = parseInt(m[3]);
    return '#' + [r,g,b].map(x => x.toString(16).padStart(2,'0').toUpperCase()).join('');
}

/** v1.8.2 todo31: one-click "extract this hex into a new CSS var and add it to the panel" */
/** v1.8.3 todo61: smart name from hex - returns 'purple' / 'blue' / 'mint' etc */
function _hueNameFromHex(hex) {
    try {
        const h = hex.replace('#', '');
        const r = parseInt(h.slice(0,2),16) / 255;
        const g = parseInt(h.slice(2,4),16) / 255;
        const b = parseInt(h.slice(4,6),16) / 255;
        const mx = Math.max(r,g,b), mn = Math.min(r,g,b);
        const l = (mx + mn) / 2;
        if (mx - mn < 0.05) {
            if (l > 0.92) return 'white';
            if (l < 0.12) return 'black';
            return 'gray';
        }
        const d = mx - mn;
        let hue;
        if (mx === r) hue = ((g - b) / d) % 6;
        else if (mx === g) hue = (b - r) / d + 2;
        else hue = (r - g) / d + 4;
        hue = (hue * 60 + 360) % 360;
        if (hue < 15 || hue >= 345) return 'red';
        if (hue < 45) return 'orange';
        if (hue < 65) return 'amber';
        if (hue < 90) return 'lime';
        if (hue < 165) return 'green';
        if (hue < 195) return 'teal';
        if (hue < 230) return 'sky';
        if (hue < 265) return 'blue';
        if (hue < 295) return 'purple';
        if (hue < 330) return 'pink';
        return 'red';
    } catch (e) { return 'color'; }
}

/** v1.8.3 todo61: 判断 hex 是否来自 element 的 inline style（A 类）。
 *  返回 inline style 中匹配该 hex 的 property（color/background-color/border-color）或 ''。
 */
function _findInlineColorProp(el, hex) {
    if (!el || !el.getAttribute) return '';
    const style = el.getAttribute('style') || '';
    const target = hex.toUpperCase().replace('#','');
    for (const decl of style.split(';')) {
        if (!decl.includes(':')) continue;
        const [k, v] = decl.split(':');
        const prop = k.trim().toLowerCase();
        const val = (v || '').trim();
        if (!/color/i.test(prop) && !/background/i.test(prop) && !/border/i.test(prop)) continue;
        const hexMatch = val.match(/#([0-9a-fA-F]{3,8})/);
        if (hexMatch) {
            let mh = hexMatch[1];
            if (mh.length === 3) mh = mh.split('').map(c => c+c).join('');
            if (mh.slice(0,6).toUpperCase() === target) return prop;
        }
        const rgbMatch = val.match(/rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/);
        if (rgbMatch) {
            const rh = [rgbMatch[1], rgbMatch[2], rgbMatch[3]]
                .map(x => parseInt(x).toString(16).padStart(2,'0')).join('').toUpperCase();
            if (rh === target) return prop;
        }
    }
    return '';
}

/** v1.8.3 todo62: best CSS selector for an element (mirror of scan_dom heuristic) */
function _bestSelectorFor(el) {
    if (!el || !el.nodeType) return '';
    if (el.id) return '#' + el.id;
    const cls = (el.className || '').toString().trim().split(/\s+/).filter(c => c && !c.startsWith('reveal-') && c !== 'pinned-page-el');
    if (cls.length) return el.tagName.toLowerCase() + '.' + cls[0];
    // path-based fallback (2 levels)
    let path = el.tagName.toLowerCase();
    if (el.parentElement && el.parentElement.tagName) {
        const p = el.parentElement;
        const pcls = (p.className || '').toString().trim().split(/\s+/).filter(c => c && !c.startsWith('reveal-'))[0];
        if (pcls) path = p.tagName.toLowerCase() + '.' + pcls + ' ' + path;
    }
    return path;
}

function _extractColorToVar(hex, role, sourceEl) {
    try {
        hex = (hex || '').toUpperCase();
        if (!/^#[0-9A-F]{6}$/.test(hex)) return;

        // v1.8.3 todo61: A 类检测 —— 只有 inline style 写死的才能直改 DOM 拿到画面联动
        const el = sourceEl || _pinnedSourceEl;
        const inlineProp = el ? _findInlineColorProp(el, hex) : '';
        const isAClass = !!inlineProp;

        const lang = (typeof _currentLang === 'function') ? _currentLang()
            : (localStorage.getItem('hve_lang') || ((navigator.language||'en').toLowerCase().indexOf('zh') >= 0 ? 'zh' : 'en'));
        const isZh = lang === 'zh';

        if (!isAClass) {
            // B/C/D/E 类：不擅自改 DOM，给提示
            const msg = isZh
                ? `该颜色 ${hex} 来自 CSS 规则、父级继承或复杂表达式，不在 inline 写死。\n\n直接改样式有风险，建议：去 "风格" tab 复制一份 Style Prompt，让 AI 帮你重塑 CSS。`
                : `${hex} comes from a CSS rule, inherited from a parent, or a complex expression — not an inline style.\n\nDirect rewriting is risky. Tip: open the "Styles" tab, copy a Style Prompt, and let an AI rewrite your CSS.`;
            alert(msg);
            return;
        }

        // ===== A 类：直改 =====

        // 1) 智能默认变量名 + 让用户改名
        const roleShort = { text: 'text', bg: 'bg', border: 'border' }[role] || 'color';
        const hue = _hueNameFromHex(hex);
        let baseName = `--${roleShort}-${hue}`;
        // 避免冲突，加序号
        let varName = baseName;
        let n = 2;
        while (window.DEFAULT_COLORS && window.DEFAULT_COLORS[varName]) {
            varName = baseName + '-' + n;
            n += 1;
        }
        const promptMsg = isZh
            ? `提取 ${hex} 为变量。\n变量名（可改）：`
            : `Extract ${hex} as a variable.\nVariable name (editable):`;
        const userInput = prompt(promptMsg, varName);
        if (userInput == null) return;  // 用户取消
        let finalVar = userInput.trim();
        if (!finalVar.startsWith('--')) finalVar = '--' + finalVar.replace(/^-+/, '');
        if (!/^--[a-zA-Z_][\w-]*$/.test(finalVar)) {
            alert(isZh ? '变量名不合法（应为 --xxx 格式）' : 'Invalid variable name (use --xxx format)');
            return;
        }

        // 2) 写 :root inline
        document.documentElement.style.setProperty(finalVar, hex);
        if (window.DEFAULT_COLORS) window.DEFAULT_COLORS[finalVar] = hex;

        // 3) 改 element inline style，把 hex 换成 var()
        const oldStyle = el.getAttribute('style') || '';
        const re = new RegExp(`(#${hex.slice(1)}|#${hex.slice(1,4)})\\b`, 'gi');
        const newStyle = oldStyle.replace(re, `var(${finalVar})`);
        el.setAttribute('style', newStyle);

        // 4) 注入一行 .color-row 到面板
        const tabColors = document.querySelector('#tab-colors');
        if (tabColors) {
            const roleTitleMap = { text: '文字 Text', bg: '背景 Background', border: '边框 / 分割线 Border' };
            let section = null;
            const sections = tabColors.querySelectorAll('.panel-section');
            for (const s of sections) {
                const t = s.querySelector('.panel-section-title');
                if (t && t.textContent.trim() === roleTitleMap[role]) { section = s; break; }
            }
            if (!section) {
                section = document.createElement('div');
                section.className = 'panel-section';
                section.innerHTML = `<div class="panel-section-title">${roleTitleMap[role]}</div>`;
                tabColors.appendChild(section);
            }
            const row = document.createElement('div');
            row.className = 'color-row';
            const labelText = isZh ? '提取 Extracted' : 'Extracted';
            row.innerHTML = `
                <span class="color-label">${labelText} (${finalVar})</span>
                <div class="color-swatch" style="background:${hex};"><input type="color" value="${hex}" data-var="${finalVar}" onchange="applyColor(this)" oninput="previewColor(this)"></div>
                <input type="text" class="color-hex" value="${hex}" data-var="${finalVar}" onchange="applyHex(this)">`;
            section.appendChild(row);
        }

        // 5) v1.8.3 todo62: 注册 PEM + CVE，让 hover 提示工作
        try {
            const sel = _bestSelectorFor(el);
            if (sel) {
                window.CSS_VAR_TO_ELEMENTS = window.CSS_VAR_TO_ELEMENTS || {};
                const old = window.CSS_VAR_TO_ELEMENTS[finalVar] || '';
                window.CSS_VAR_TO_ELEMENTS[finalVar] = old ? (old + ', ' + sel) : sel;

                window.PAGE_ELEMENT_TO_PANEL = window.PAGE_ELEMENT_TO_PANEL || {};
                const items = window.PAGE_ELEMENT_TO_PANEL[sel] || [];
                const rowLabel = (isZh ? '提取 Extracted' : 'Extracted') + ' (' + finalVar + ')';
                if (!items.some(it => it.tab === '颜色' && it.row === rowLabel)) {
                    items.push({ tab: '颜色', row: rowLabel });
                }
                window.PAGE_ELEMENT_TO_PANEL[sel] = items;
            }
        } catch (e) { /* noop */ }

        // 6) toast
        if (typeof showToast === 'function') {
            showToast((isZh ? '✓ 已提取为 ' : '✓ Extracted as ') + finalVar, 2500);
        }
    } catch (e) { console.warn('[extract] failed', e); }
}

/** Render multi-line tooltip showing all adjustable dimensions */
function showPageElementTooltip(el, infoList, x, y, opts = {}) {
    // 如果已有固定tooltip，且不是正在创建固定tooltip，则不覆盖
    if (_pinnedTooltip && !opts.replacePinned) return;

    clearPageTooltip();

    const tip = document.createElement('div');
    tip.className = 'panel-highlight-tooltip';
    tip.dataset.pinned = opts.pinned ? '1' : '0';

    // Header (todo25-B4: i18n)
    const headerHtml = `
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,0.08);">
            <span style="font-size:11px;color:rgba(255,200,50,0.85);font-weight:600;letter-spacing:0.04em;">
                ${opts.pinned ? _t('tooltip_pinned') : _t('tooltip_hover')}
            </span>
            ${opts.pinned ? '<button class="tt-close-btn" style="background:none;border:none;color:rgba(255,255,255,0.5);cursor:pointer;font-size:14px;padding:0 4px;line-height:1;">✕</button>' : '<span style="font-size:10px;color:rgba(255,200,50,0.55);">' + _t('tooltip_pin_hint').replace(/P/g, '<kbd style="background:rgba(255,255,255,0.1);padding:1px 5px;border-radius:3px;font-family:monospace;">P</kbd>') + '</span>'}
        </div>`;

    // Rows — each clickable, jumps to panel
    // v1.8.2 todo31: 每行加色块/数值 + 漏色检测
    const rowsHtml = infoList.map((info, i) => {
        const tagColor = TAB_COLORS[info.tab] || 'rgba(255,200,50,0.9)';
        const tabDisplay = _translateTab(info.tab);
        const extras = _buildRowExtras(info, el);
        return `
        <div class="tt-row" data-tab="${info.tab}" data-row="${info.row.replace(/"/g, '&quot;')}"
             style="display:flex;align-items:center;gap:8px;padding:6px 8px;margin:2px -4px;border-radius:6px;cursor:${opts.pinned ? 'pointer' : 'default'};transition:background 0.15s;">
            <span style="display:inline-block;padding:2px 8px;border-radius:4px;background:${tagColor}22;border:1px solid ${tagColor}88;color:${tagColor};font-size:10.5px;font-weight:600;flex-shrink:0;">${tabDisplay}</span>
            ${extras.swatchHtml}
            <span style="color:rgba(255,255,255,0.88);font-size:12px;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${info.row}</span>
            ${extras.valueHtml}
            ${opts.pinned ? '<span style="margin-left:6px;color:rgba(255,200,50,0.6);font-size:11px;flex-shrink:0;">→</span>' : ''}
        </div>`;
    }).join('');

    // v1.8.2 todo31: 漏色提示 + 一键提取按钮（只在 pinned 模式显示）
    const missingHtml = opts.pinned ? _buildMissingColorAlert(el) : '';

    tip.innerHTML = headerHtml + rowsHtml + missingHtml;

    tip.style.cssText = `
        position: fixed;
        z-index: 10002;
        background: rgba(20, 20, 20, 0.97);
        border: 1px solid ${opts.pinned ? 'rgba(255, 200, 50, 0.7)' : 'rgba(255, 200, 50, 0.4)'};
        border-radius: 10px;
        padding: 10px 14px;
        font-family: var(--font-body, sans-serif);
        color: rgba(255, 255, 255, 0.9);
        pointer-events: ${opts.pinned ? 'auto' : 'none'};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.5)${opts.pinned ? ', 0 0 0 3px rgba(255,200,50,0.15)' : ''};
        line-height: 1.4;
        min-width: 200px;
        max-width: 320px;
    `;

    document.body.appendChild(tip);
    _pageTooltip = tip;

    // 固定模式下绑定行点击事件
    if (opts.pinned) {
        tip.querySelectorAll('.tt-row').forEach(row => {
            row.addEventListener('mouseenter', () => row.style.background = 'rgba(255,255,255,0.06)');
            row.addEventListener('mouseleave', () => row.style.background = '');
            row.addEventListener('click', () => {
                jumpToPanelControl(row.dataset.tab, row.dataset.row);
            });
        });
        // v1.8.2 todo31: 一键提取按钮（A 类）
        tip.querySelectorAll('.tt-extract-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                _extractColorToVar(btn.dataset.hex, btn.dataset.role, el);
                btn.parentElement.style.opacity = '0.5';
                btn.disabled = true;
            });
        });
        // v1.8.3.1: B/C/D/E 类——复制提示让 AI 改 CSS（不动 DOM）
        tip.querySelectorAll('.tt-ai-hint-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const hex = btn.dataset.hex;
                const role = btn.dataset.role;
                const lang = (typeof _currentLang === 'function') ? _currentLang()
                    : (localStorage.getItem('hve_lang') || ((navigator.language||'en').toLowerCase().indexOf('zh') >= 0 ? 'zh' : 'en'));
                const isZh = lang === 'zh';
                const sel = _bestSelectorFor(el);
                const promptText = isZh
                    ? `请帮我修改这份 HTML 的 CSS：把 ${role === 'text' ? '文字' : role === 'bg' ? '背景' : '边框'}颜色 ${hex}（出现在 ${sel} 上）提取为一个 CSS 变量并替换所有引用，方便我之后统一调整。要求：变量名要语义化，例如 --text-brand 或 --bg-accent。`
                    : `Please refactor this HTML's CSS: extract the ${role} color ${hex} (used on ${sel}) into a CSS variable and replace all references so I can tweak it centrally. Use a semantic variable name like --text-brand or --bg-accent.`;
                // 复制到剪贴板
                const copy = (txt) => {
                    if (navigator.clipboard && navigator.clipboard.writeText) {
                        return navigator.clipboard.writeText(txt);
                    }
                    const ta = document.createElement('textarea');
                    ta.value = txt; document.body.appendChild(ta); ta.select();
                    try { document.execCommand('copy'); } catch(_) {}
                    document.body.removeChild(ta);
                };
                Promise.resolve(copy(promptText)).then(() => {
                    if (typeof showToast === 'function') {
                        showToast(isZh ? '✓ 已复制提示，去粘贴给 AI（不要忘了附上 HTML 源码）' : '✓ Prompt copied — paste it to your AI together with the HTML', 3500);
                    }
                });
                btn.disabled = true;
                btn.style.opacity = '0.5';
            });
        });
        const closeBtn = tip.querySelector('.tt-close-btn');
        if (closeBtn) closeBtn.addEventListener('click', () => {
            _pinnedTooltip = false;
            _pinnedSourceEl = null;
            clearPageTooltip();
            // 同时清除页面元素的固定高亮
            document.querySelectorAll('.pinned-page-el').forEach(el => el.classList.remove('pinned-page-el'));
        });
    }

    // 测量真实尺寸再定位 (todo25-B2: 避开右侧面板)
    const rect = tip.getBoundingClientRect();
    const tipW = rect.width;
    const tipH = rect.height;
    const maxRight = _getTooltipMaxRight();
    let posX = x + 18;
    let posY = y - 10;
    if (posX + tipW > maxRight) posX = x - tipW - 18;
    if (posX < 10) posX = 10;
    if (posY < 10) posY = 10;
    if (posY + tipH > window.innerHeight - 10) posY = window.innerHeight - tipH - 10;
    tip.style.left = posX + 'px';
    tip.style.top = posY + 'px';
}

function clearPageTooltip() {
    if (_pageTooltip) {
        _pageTooltip.remove();
        _pageTooltip = null;
    }
}

/** Find ALL panel control info applicable to this element (collect from element + ancestors) */
function findPanelInfo(el) {
    const collected = [];
    const seenKeys = new Set();
    let current = el;

    while (current && current !== document.body) {
        for (const selector of Object.keys(PAGE_ELEMENT_TO_PANEL)) {
            try {
                if (current.matches && current.matches(selector)) {
                    const items = PAGE_ELEMENT_TO_PANEL[selector];
                    // Support both single-object (legacy) and array forms
                    const list = Array.isArray(items) ? items : [items];
                    list.forEach(item => {
                        const key = (item.tab || '') + '|' + (item.row || '');
                        if (!seenKeys.has(key)) {
                            seenKeys.add(key);
                            collected.push(item);
                        }
                    });
                }
            } catch(_) { /* invalid selector — skip */ }
        }
        current = current.parentElement;
    }

    return collected.length > 0 ? collected : null;
}

/** Init reverse mapping: page element hover → show panel hint */
function initPageElementHighlights() {
    // 触发热区：所有 PAGE_ELEMENT_TO_PANEL 里的选择器 + data-editable 元素
    // 这样不管 host HTML 是 slides 结构还是单页文档结构都能工作
    const selectors = new Set();
    selectors.add('[data-editable]');  // 所有可编辑元素都该能触发
    Object.keys(PAGE_ELEMENT_TO_PANEL || {}).forEach(sel => selectors.add(sel));
    const selectorString = [...selectors].join(', ');

    let targets;
    try {
        targets = document.querySelectorAll(selectorString);
    } catch(err) {
        console.warn('[html-visual-editor] selector error, using fallback:', err);
        targets = document.querySelectorAll('[data-editable]');
    }

    // 记录鼠标当前悬停的目标和坐标，供 P 键固定使用
    let _hoverTarget = null;
    let _hoverX = 0, _hoverY = 0;

    targets.forEach(el => {
        if (el.closest('.edit-panel') || el.closest('.edit-toolbar')) return;

        // hover → 临时显示
        el.addEventListener('mouseover', (e) => {
            if (!document.body.classList.contains('edit-mode')) return;
            if (_pinnedTooltip) return;
            _hoverTarget = e.target;
            _hoverX = e.clientX; _hoverY = e.clientY;
            const infoList = findPanelInfo(e.target);
            if (infoList && infoList.length > 0) {
                showPageElementTooltip(e.target, infoList, e.clientX, e.clientY);
            }
        });

        // mousemove → 跟随鼠标 (todo25-B2: 避开右侧面板)
        el.addEventListener('mousemove', (e) => {
            _hoverTarget = e.target;
            _hoverX = e.clientX; _hoverY = e.clientY;
            if (_pinnedTooltip) return;
            if (_pageTooltip && !_pageTooltip.contains(e.target)) {
                const rect = _pageTooltip.getBoundingClientRect();
                const tipW = rect.width;
                const tipH = rect.height;
                const maxRight = _getTooltipMaxRight();
                let posX = e.clientX + 18;
                let posY = e.clientY - 10;
                if (posX + tipW > maxRight) posX = e.clientX - tipW - 18;
                if (posX < 10) posX = 10;
                if (posY < 10) posY = 10;
                if (posY + tipH > window.innerHeight - 10) posY = window.innerHeight - tipH - 10;
                _pageTooltip.style.left = posX + 'px';
                _pageTooltip.style.top = posY + 'px';
            }
        });

        // mouseout → 清除（仅当没固定时）
        el.addEventListener('mouseout', (e) => {
            if (_pinnedTooltip) return;
            if (!_pageTooltip || !_pageTooltip.contains(e.relatedTarget)) {
                clearPageTooltip();
            }
        });
    });

    // 全局 P 键监听 → 固定/解锁当前tooltip
    document.addEventListener('keydown', (e) => {
        if (!document.body.classList.contains('edit-mode')) return;
        // 不在文字编辑时
        if (document.activeElement && document.activeElement.getAttribute('contenteditable') === 'true') return;
        if (e.metaKey || e.ctrlKey || e.altKey || e.shiftKey) return;
        if (e.key.toLowerCase() !== 'p') return;

        e.preventDefault();
        e.stopPropagation();

        if (_pinnedTooltip) {
            // 解锁
            _pinnedTooltip = false;
            _pinnedSourceEl = null;
            clearPageTooltip();
            document.querySelectorAll('.pinned-page-el').forEach(p => p.classList.remove('pinned-page-el'));
            return;
        }

        // 固定当前 hover
        if (_hoverTarget) {
            const infoList = findPanelInfo(_hoverTarget);
            if (infoList && infoList.length > 0) {
                _pinnedTooltip = true;
                _pinnedSourceEl = _hoverTarget;
                document.querySelectorAll('.pinned-page-el').forEach(p => p.classList.remove('pinned-page-el'));
                _hoverTarget.classList.add('pinned-page-el');
                showPageElementTooltip(_hoverTarget, infoList, _hoverX, _hoverY, { pinned: true, replacePinned: true });
            }
        }
    });

    // 点击 tooltip 外部（且非面板）→ 取消固定
    document.addEventListener('click', (e) => {
        if (!_pinnedTooltip) return;
        if (_pageTooltip && _pageTooltip.contains(e.target)) return;
        if (e.target.closest('.edit-panel') || e.target.closest('.edit-toolbar')) return;
        // 点其它有映射的元素 → 重新固定到那里
        // v16 修复: 动态生成 PEM 选择器列表，替代硬编码
        const pemSelectors = Object.keys(PAGE_ELEMENT_TO_PANEL || {}).join(', ');
        const mapped = e.target.closest('[data-editable]' + (pemSelectors ? ', ' + pemSelectors : ''));
        if (mapped) {
            const infoList = findPanelInfo(e.target);
            if (infoList && infoList.length > 0) {
                document.querySelectorAll('.pinned-page-el').forEach(p => p.classList.remove('pinned-page-el'));
                _pinnedSourceEl = e.target;
                e.target.classList.add('pinned-page-el');
                showPageElementTooltip(e.target, infoList, e.clientX, e.clientY, { pinned: true, replacePinned: true });
            }
            return;
        }
        // 否则取消固定
        _pinnedTooltip = false;
        _pinnedSourceEl = null;
        clearPageTooltip();
        document.querySelectorAll('.pinned-page-el').forEach(p => p.classList.remove('pinned-page-el'));
    });
}

/* =====================================================
   ✦✦✦  PANEL → PAGE ELEMENT MAPPING  ✦✦✦
   Hover a panel row → the page elements it controls glow
   ===================================================== */

/**
 * CSS var → page element selectors
 * Used for hover/click highlighting
 * v16: 完全由 Python 动态生成并通过 window.CSS_VAR_TO_ELEMENTS 注入
 */
var CSS_VAR_TO_ELEMENTS = window.CSS_VAR_TO_ELEMENTS = window.CSS_VAR_TO_ELEMENTS || {};

/**
 * Layout slider target → human-readable label
 * v16: 完全由 Python 动态生成
 */
var LAYOUT_TARGET_LABELS = window.LAYOUT_TARGET_LABELS = window.LAYOUT_TARGET_LABELS || {};

/* Track active highlight + tooltip */
let _activeHighlightEls = [];
let _activeTooltip = null;
let _lastHighlightedControl = null;

/** Highlight page elements controlled by a panel row */
function highlightPageElements(els, label) {
    clearHighlights();

    els.forEach(el => {
        if (el) el.classList.add('panel-highlight');
    });
    _activeHighlightEls = els;

    // Show tooltip near cursor area (slide viewport center)
    showHighlightTooltip(label);
}

/** Clear all active highlights */
function clearHighlights() {
    _activeHighlightEls.forEach(el => {
        if (el) el.classList.remove('panel-highlight');
    });
    _activeHighlightEls = [];
    if (_activeTooltip) {
        _activeTooltip.remove();
        _activeTooltip = null;
    }
}

/** Show a tooltip near the panel row */
function showHighlightTooltip(text) {
    if (_activeTooltip) _activeTooltip.remove();
    const tip = document.createElement('div');
    tip.className = 'panel-highlight-tooltip';
    tip.textContent = text;
    document.body.appendChild(tip);
    _activeTooltip = tip;

    // Position: right of panel, vertically centered in viewport
    const panel = document.getElementById('editPanel');
    const panelRect = panel ? panel.getBoundingClientRect() : { right: 310, top: 0, height: window.innerHeight };
    const viewH = window.innerHeight;

    // Place tooltip to the left of the panel (inside panel area would overlap controls)
    // Position it at the right edge of panel, vertically centered
    tip.style.right = (window.innerWidth - panelRect.right + 8) + 'px';
    tip.style.top = Math.max(10, Math.min(window.innerHeight - 40, viewH / 2 - 15)) + 'px';
}

/** Get target elements for a given CSS var name */
function getTargetsForVar(varName) {
    const selector = CSS_VAR_TO_ELEMENTS[varName];
    if (!selector) return [];
    return [...document.querySelectorAll(selector)].filter(el =>
        !el.closest('.edit-toolbar') && !el.closest('.edit-panel') && !el.closest('.nav-dots') && !el.closest('.keyboard-hint')
    );
}

/** Init panel highlight bindings — call once on load */
function initPanelHighlights() {
    // Color rows: hover → highlight, leave → clear
    document.querySelectorAll('.color-row').forEach(row => {
        const varName = row.querySelector('[data-var]')?.dataset.var;
        if (!varName) return;

        row.addEventListener('mouseover', () => {
            const labelEl = row.querySelector('.color-label');
            const label = labelEl ? labelEl.textContent.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '').trim() : varName;
            const els = getTargetsForVar(varName);
            highlightPageElements(els, label + ' ← 当前行控制');
            _lastHighlightedControl = row;
        });

        row.addEventListener('mouseout', (e) => {
            // Only clear if mouse actually left the row (not entering a child)
            if (!row.contains(e.relatedTarget)) {
                clearHighlights();
                _lastHighlightedControl = null;
            }
        });
    });

    // Layout sliders: hover → highlight data-target elements
    document.querySelectorAll('.slider-row input[type="range"]').forEach(slider => {
        const target = slider.dataset.target;
        if (!target) return;

        slider.closest('.slider-row').addEventListener('mouseover', () => {
            const labelEl = slider.closest('.slider-row').querySelector('.slider-name');
            const label = labelEl ? labelEl.textContent.trim() : target;
            const els = [...document.querySelectorAll(target)].filter(el =>
                !el.closest('.edit-panel') && !el.closest('.edit-toolbar')
            );
            highlightPageElements(els, label + ' ← 当前行控制');
        });

        slider.closest('.slider-row').addEventListener('mouseout', (e) => {
            if (!slider.closest('.slider-row').contains(e.relatedTarget)) {
                clearHighlights();
            }
        });
    });

    // Size sliders: hover → highlight elements using the CSS var
    document.querySelectorAll('.slider-row input[data-var]').forEach(slider => {
        const varName = slider.dataset.var;
        if (!varName || slider.dataset.target) return; // skip layout sliders (already handled above)

        slider.closest('.slider-row').addEventListener('mouseover', () => {
            const labelEl = slider.closest('.slider-row').querySelector('.slider-name');
            const label = labelEl ? labelEl.textContent.trim() : varName;
            // v16: 优先使用 Python 注入的 CSS_VAR_TO_ELEMENTS，fallback 到通用选择器
            const selector = CSS_VAR_TO_ELEMENTS[varName] || 'p, span, div';
            const els = [...document.querySelectorAll(selector.split(', '))].filter(el =>
                !el.closest('.edit-panel') && !el.closest('.edit-toolbar')
            );
            highlightPageElements(els, label + ' ← 当前行控制');
        });

        slider.closest('.slider-row').addEventListener('mouseout', (e) => {
            if (!slider.closest('.slider-row').contains(e.relatedTarget)) {
                clearHighlights();
            }
        });
    });
}

/** Apply size slider change */
function applySize(slider, displayId, unit) {
    const val = parseFloat(slider.value);
    const varName = slider.dataset.var;
    // Build new clamp() using known bounds — never rely on getComputedStyle regex
    const bounds = SIZE_BOUNDS[varName];
    if (bounds) {
        const newVal = `clamp(${bounds.min}, ${val}${unit}, ${bounds.max})`;
        document.documentElement.style.setProperty(varName, newVal);
    } else {
        // Fallback: simple vw-only value
        document.documentElement.style.setProperty(varName, `${val}${unit}`);
    }
    document.getElementById(displayId).textContent = `${val} ${unit}`;
}

/** Switch panel tabs */
/** Apply layout slider (width/padding) to target elements */
function applyLayout(slider, displayId) {
    const val = parseInt(slider.value);
    const unit = slider.dataset.unit || 'px';
    const prop = slider.dataset.prop || 'max-width';
    const targets = document.querySelectorAll(slider.dataset.target);

    // Push undo history (debounced: once per interaction burst) (todo25-B1)
    if (!slider._undoPushed) {
        const oldVals = [];
        targets.forEach(el => {
            oldVals.push(el.style.getPropertyValue(prop) || '');
        });
        if (typeof pushHistory === 'function') {
            pushHistory('layout', {
                target: slider.dataset.target,
                prop: prop,
                oldVals: oldVals,
                unit: unit
            });
        }
        slider._undoPushed = true;
        clearTimeout(slider._undoTimer);
        slider._undoTimer = setTimeout(() => { slider._undoPushed = false; }, 400);
    }

    targets.forEach(el => {
        el.style.setProperty(prop, `${val}${unit}`);
    });
    document.getElementById(displayId).textContent = `${val}${unit}`;
}

function switchPanelTab(tabName) {
    document.querySelectorAll('.panel-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tabName));
    document.querySelectorAll('.panel-tab-content').forEach(c => c.classList.toggle('active', c.id === 'tab-' + tabName));
}

/** Save state to localStorage */
function saveToStorage() {
    // Collect all CSS custom property overrides — 遍历面板中所有 .color-row 的 data-var
    // v16 修复: 不再依赖 DEFAULT_COLORS keys，而是动态收集面板中实际存在的颜色变量
    const styles = {};
    const varsToSave = [];
    document.querySelectorAll('.color-row input[type="color"]').forEach(ci => {
        if (ci.dataset.var) varsToSave.push(ci.dataset.var);
    });
    // Fallback: 如果面板还没渲染完，用 DEFAULT_COLORS
    if (varsToSave.length === 0 && typeof DEFAULT_COLORS === 'object' && DEFAULT_COLORS) {
        varsToSave.push(...Object.keys(DEFAULT_COLORS));
    }
    varsToSave.forEach(v => {
        const val = getComputedStyle(document.documentElement).getPropertyValue(v).trim();
        if (val) styles[v] = val;
    });

    // Collect all edited text content
    const texts = {};
    const editables = document.querySelectorAll('[data-editable]');
    editables.forEach((el, i) => {
        texts['el_' + i] = el.innerHTML.trim();
    });

    // Page signature: 用于 load 时校验"是不是同一份文档"
    // 由元素总数 + 各元素的 class 列表组成（结构指纹）
    const signature = {
        editableCount: editables.length,
        // 取前16个元素的 class 名作为结构指纹（够用且不大）
        classFingerprint: [...editables].slice(0, 16).map(el => el.className || '').join('|'),
        title: document.title || '',
        path: location.pathname || '',
    };

    // v16 新增: Collect size/layout slider states
    const sliders = {};
    document.querySelectorAll('.slider-row input[type="range"]').forEach(slider => {
        const key = slider.dataset.target + '|' + slider.dataset.prop + '|' + (slider.dataset.var || '');
        if (slider.value !== slider.defaultValue) {
            sliders[key] = {
                value: slider.value,
                target: slider.dataset.target || '',
                prop: slider.dataset.prop || '',
                unit: slider.dataset.unit || '',
                varName: slider.dataset.var || '',
                displayId: (slider.closest('.slider-row').querySelector('.slider-val') || {}).id || '',
            };
        }
    });

    const state = { signature, styles, texts, sliders, savedAt: new Date().toISOString(), version: 3 };
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        showSaveIndicator(true);
    } catch(e) {
        alert('保存失败：localStorage 可能已满或不可用');
    }
}

/** Load state from localStorage */
function loadFromStorage() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) return;
        const state = JSON.parse(raw);

        // ⚠️  防污染校验：只有在文档"指纹"基本匹配时才恢复内容
        // 放宽策略：editableCount 差异 ≤ 3 仍恢复（部分恢复），避免微小变动导致整个 localStorage 被丢弃
        const editables = document.querySelectorAll('[data-editable]');
        const sig = state.signature;
        if (sig) {
            const currentFingerprint = [...editables].slice(0, 16).map(el => el.className || '').join('|');
            const countDiff = Math.abs(sig.editableCount - editables.length);
            const titleMismatch = sig.title && sig.title !== document.title;
            const fingerprintMismatch = sig.classFingerprint !== currentFingerprint;

            if (titleMismatch || countDiff > 3) {
                console.warn('[html-visual-editor] localStorage 与当前文档不匹配，跳过恢复以防内容污染。',
                    { saved: sig, current: { editableCount: editables.length, title: document.title } });
                try { localStorage.removeItem(STORAGE_KEY); } catch(_) {}
                return;
            }

            if (fingerprintMismatch && countDiff > 0) {
                console.warn('[html-visual-editor] 指纹不匹配但元素数量差异在容差内，尝试恢复。',
                    { saved: sig, current: { editableCount: editables.length, title: document.title } });
                // 继续恢复，但可能部分 editable 索引错位
            }
        } else {
            // 旧版本（v1）没有 signature，直接拒绝恢复并清掉
            console.warn('[html-visual-editor] 旧版本 localStorage 数据，跳过恢复。');
            try { localStorage.removeItem(STORAGE_KEY); } catch(_) {}
            return;
        }

        // Restore colors
        if (state.styles) {
            Object.entries(state.styles).forEach(([v, val]) => {
                document.documentElement.style.setProperty(v, val);
            });
            // Update UI controls
            document.querySelectorAll('.color-row').forEach(row => {
                const ci = row.querySelector('input[type="color"]');
                const hi = row.querySelector('.color-hex');
                const sw = row.querySelector('.color-swatch');
                const vn = ci?.dataset.var;
                if (vn && state.styles[vn]) {
                    const v = state.styles[vn];
                    if (ci) ci.value = v.startsWith('#') ? v : '#888888';
                    if (hi) hi.value = v.startsWith('#') ? v.toUpperCase() : v;
                    if (sw) sw.style.background = v.startsWith('#') ? v : '#888888';
                }
            });
        }

        // Restore texts
        if (state.texts) {
            editables.forEach((el, i) => {
                if (state.texts['el_' + i] !== undefined) {
                    el.innerHTML = state.texts['el_' + i];
                }
            });
        }

        // v16 新增: Restore size/layout slider states
        if (state.sliders) {
            Object.values(state.sliders).forEach(s => {
                // 如果是 CSS 变量方式 (varName 存在)
                if (s.varName) {
                    document.documentElement.style.setProperty(s.varName, s.value + (s.unit || ''));
                }
                // 如果是直接元素方式 (target + prop)
                if (s.target) {
                    const el = document.querySelector(s.target);
                    if (el) {
                        el.style[s.prop] = s.value + (s.unit || '');
                    }
                }
                // 更新面板中的 slider 显示值
                if (s.displayId) {
                    const displayEl = document.getElementById(s.displayId);
                    if (displayEl) displayEl.textContent = s.value + (s.unit || '');
                }
            });
            // 同步所有 slider input 的值
            document.querySelectorAll('.slider-row input[type="range"]').forEach(slider => {
                const key = slider.dataset.target + '|' + slider.dataset.prop + '|' + (slider.dataset.var || '');
                if (state.sliders[key]) {
                    slider.value = state.sliders[key].value;
                }
            });
        }
    } catch(e) {
        console.warn('Failed to load saved state:', e);
    }
}

/** Show save indicator briefly */
function showSaveIndicator(ok) {
    const el = document.getElementById('saveIndicator');
    el.textContent = ok ? '已保存 ✓' : '保存失败';
    el.classList.add('show');
    setTimeout(() => el.classList.remove('show'), 2000);
}

/** Export current HTML as downloadable file */
function exportHTML() {
    // Collect current state
    const clone = document.documentElement.cloneNode(true);

    // 1) 同步 inline CSS 变量值到 <style> 块
    //    cloneNode(true) 会复制 inline style，但 <style> 块中的 CSS 变量声明仍是旧值
    //    需要把当前计算值写回 <style id="html-visual-editor-vars"> 块
    const varsStyleEl = clone.querySelector('style#html-visual-editor-vars');
    if (varsStyleEl) {
        // 从 clone 的 inline style 收集所有已覆盖的 CSS 变量
        const rootEl = clone.querySelector(':root') || clone;
        const inlineStyle = rootEl.getAttribute('style') || '';
        // 构建新的 :root 块
        const varOverrides = {};
        inlineStyle.split(';').forEach(decl => {
            const [prop, ...valParts] = decl.split(':');
            if (prop && prop.trim().startsWith('--')) {
                varOverrides[prop.trim()] = valParts.join(':').trim();
            }
        });
        if (Object.keys(varOverrides).length > 0) {
            // 替换 vars style 块中的声明
            let newCSS = varsStyleEl.textContent;
            Object.entries(varOverrides).forEach(([prop, val]) => {
                // 替换已有声明
                const re = new RegExp(prop.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*:\\s*[^;]+', 'g');
                if (re.test(newCSS)) {
                    newCSS = newCSS.replace(re, `${prop}: ${val}`);
                } else {
                    // 在 :root { ... } 块内追加
                    newCSS = newCSS.replace(/:root\s*\{/, `:root {\n  ${prop}: ${val};`);
                }
            });
            varsStyleEl.textContent = newCSS;
        }
    }

    // Remove edit UI elements from export
    // v1.8.2 todo58: 增补 .panel-highlight-tooltip（pinned 弹窗）和 .pinned-page-el class 残留
    clone.querySelectorAll('.edit-toolbar, .edit-panel, .edit-hint, .panel-highlight-tooltip').forEach(el => el.remove());
    clone.querySelectorAll('.pinned-page-el').forEach(el => el.classList.remove('pinned-page-el'));
    // Remove contenteditable attributes (但保留 data-editable —— 方案 B：日后可再次 adapt)
    clone.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
    // v1.7.0 todo35: 保留 data-editable（用户选方案 B）
    // Remove reveal animation delays (optional cleanup)
    clone.querySelectorAll('[class*="reveal-delay"]').forEach(el => {
        el.className = el.className.replace(/\s*reveal-delay-\d/g, '');
    });

    // v1.8.3 todo63: ε 方案——把 inline style 中所有 var(--xxx) 还原成当前 computed hex
    // 这样导出 HTML 剪贴到 Notion/邮件/微信也能保留颜色
    try {
        const rootStyle = getComputedStyle(document.documentElement);
        clone.querySelectorAll('[style*="var(--"]').forEach(el => {
            let style = el.getAttribute('style') || '';
            style = style.replace(/var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)/g, (_, varName) => {
                const v = rootStyle.getPropertyValue(varName).trim();
                if (!v) return _;  // 找不到值就保留 var()
                // 归一化为 #RRGGBB
                const m = v.match(/^#([0-9a-fA-F]{3,8})$/);
                if (m) {
                    let h = m[1];
                    if (h.length === 3) h = h.split('').map(c => c+c).join('');
                    return '#' + h.slice(0,6).toUpperCase();
                }
                return v;
            });
            el.setAttribute('style', style);
        });
    } catch (e) { console.warn('[exportHTML] var→hex inline failed', e); }

    // Remove editor-injected script/style markers
    clone.querySelectorAll('script[id^="html-visual-editor"]').forEach(el => el.remove());
    // v1.8.3 todo63: vars-style 块保留是双保险（host CSS 中其它 var(--x) 引用仍依赖它），
    // 因为 inline 已还原 hex，剪贴到 Notion 等场景也不影响；但完整网页仍需 vars 块支撑 host CSS rule
    clone.querySelectorAll('style[id^="html-visual-editor"]:not(#html-visual-editor-vars)').forEach(el => el.remove());

    const htmlStr = '<!DOCTYPE html>\n' + clone.outerHTML;

    // 2) 优先用 File System Access API（Chromium 浏览器支持）
    if (window.showSaveFilePicker) {
        (async () => {
            try {
                // 推断默认文件名：用当前页面标题或原文件名
                const defaultName = (document.title || 'edited').replace(/[^\w\u4e00-\u9fa5\-]/g, '_') + '.html';
                const handle = await window.showSaveFilePicker({
                    suggestedName: defaultName,
                    types: [{
                        description: 'HTML 文件',
                        accept: { 'text/html': ['.html'] },
                    }],
                });
                const writable = await handle.createWritable();
                await writable.write(htmlStr);
                await writable.close();
                showSaveIndicator(true);
                showToast('✓ 已导出到 ' + handle.name, 3000);
            } catch (err) {
                // 用户取消选择器 → 不做任何事
                if (err.name === 'AbortError') return;
                // 其他错误 → fallback 到 Blob
                console.warn('[exportHTML] showSaveFilePicker failed, fallback to Blob:', err);
                _exportViaBlob(htmlStr);
            }
        })();
    } else {
        // 3) Safari/Firefox fallback → Blob 下载
        _exportViaBlob(htmlStr);
    }
}

/** Blob 下载 fallback (Safari/Firefox) */
function _exportViaBlob(htmlStr) {
    const blob = new Blob([htmlStr], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = (document.title || 'edited').replace(/[^\w\u4e00-\u9fa5\-]/g, '_') + '.html';
    a.style.display = 'none';
    document.body.appendChild(a);
    try {
        var evt = new MouseEvent('click', { view: window, bubbles: true, cancelable: true });
        a.dispatchEvent(evt);
    } catch (e) {
        var win = window.open(url, '_blank');
        if (win) {
            win.focus();
            setTimeout(() => { alert('请在新窗口中按 ⌘S / Ctrl+S 保存为 .html 文件'); }, 500);
        }
    }
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 10000);
    showSaveIndicator(true);
}

/** Reset everything to defaults */
function resetAll() {
    if (!confirm('确定要恢复所有默认设置吗？（颜色和文字都会重置）')) return;

    // Reset CSS variables (remove overrides → CSS defaults restored)
    Object.entries(DEFAULT_COLORS).forEach(([v, val]) => {
        document.documentElement.style.removeProperty(v);
    });
    // Also remove size overrides
    ['--title-size','--h2-size','--h3-size','--body-size','--small-size','--bg-gradient','--accent-glow'].forEach(v => {
        document.documentElement.style.removeProperty(v);
    });

    // Update color UI controls back to defaults
    document.querySelectorAll('.color-row').forEach(row => {
        const ci = row.querySelector('input[type="color"]');
        const hi = row.querySelector('.color-hex');
        const sw = row.querySelector('.color-swatch');
        const vn = ci?.dataset.var;
        if (vn && DEFAULT_COLORS[vn]) {
            ci.value = DEFAULT_COLORS[vn];
            hi.value = DEFAULT_COLORS[vn];
            sw.style.background = DEFAULT_COLORS[vn];
        }
    });

    // Reset size slider UI
    const sizeSliders = {
        'val-title':  { slider: document.querySelector('[data-var="--title-size"]'), val: 6 },
        'val-h2':     { slider: document.querySelector('[data-var="--h2-size"]'),    val: 3.5 },
        'val-body':   { slider: document.querySelector('[data-var="--body-size"]'), val: 1.5 },
        'val-small':  { slider: document.querySelector('[data-var="--small-size"]'), val: 1 },
        'val-stat':   { slider: document.querySelector('[data-var="--stat-size"]'), val: 4 },
        'val-hero':   { slider: document.querySelector('[data-var="--hero-size"]'), val: 8 },
    };
    Object.entries(sizeSliders).forEach(([id, { slider, val }]) => {
        if (slider) slider.value = val;
        const el = document.getElementById(id);
        if (el) el.textContent = val + ' rem';
    });

    // Reload page to fully reset text content
    location.reload();
}

/** Init highlight bindings on load */
document.addEventListener('DOMContentLoaded', () => {
    initPanelHighlights();
    initPageElementHighlights();
});
