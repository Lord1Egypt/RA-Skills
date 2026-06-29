#!/usr/bin/env python3
# visual_editor.py — Grid-aware 可视化编辑器 v2.1.2
# 用法:
#   python visual_editor.py --template <template.html> --output <editor.html>
#   python visual_editor.py --type <模板名> --output <editor.html>  (从内置模板生成)

import argparse
import sys
import traceback
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent

sys.path.insert(0, str(SKILL_DIR / "scripts"))
from grid_builder import BUILTIN_TEMPLATES, generate_html, show_error, safe_write_text

OUTPUT_DIR = DATA_DIR / "output"

# ══════════════════════════════════════════════════════
# 增强版编辑器 JS (grid-aware)
# ══════════════════════════════════════════════════════

GRID_EDITOR_JS = r"""
// === Grid-Aware Visual Editor v2 ===
let editorOpen = false;
let selectedCell = null;
let selectedField = null;
let cellSelectorVisible = false;

// Editor state
const EDITOR_STATE = {
    fields: {},
    cells: {},
};

// Initialize editor
function initGridEditor() {
    // Make all [data-field] elements editable
    document.querySelectorAll('[data-field]').forEach(el => {
        el.classList.add('ge-editable');
        el.addEventListener('click', (e) => {
            e.stopPropagation();
            selectField(el);
        });
        el.style.outline = '2px dashed #6C63FF';
        el.style.cursor = 'pointer';
        el.style.padding = '4px 6px';
        el.style.borderRadius = '4px';
        el.style.minHeight = '1.2em';
    });

    // Make all grid cells selectable
    document.querySelectorAll('.grid-cell').forEach(cell => {
        cell.style.outline = '1px solid #d0dae8';
        cell.style.outlineOffset = '2px';
        cell.style.cursor = 'pointer';
        cell.style.position = 'relative';
        cell.addEventListener('click', (e) => {
            if (e.target === cell || e.target.closest('.grid-cell') === cell) {
                selectCell(cell);
                e.stopPropagation();
            }
        });
    });

    // Show cell labels
    document.querySelectorAll('.grid-cell').forEach((cell, idx) => {
        const id = cell.id || 'cell-' + idx;
        if (!cell.querySelector('.ge-cell-label')) {
            const label = document.createElement('div');
            label.className = 'ge-cell-label';
            label.textContent = id.replace('cell-', '');
            label.style.cssText = 'position:absolute;top:-10px;left:4px;background:#6C63FF;color:white;font-size:10px;padding:0 6px;border-radius:4px;z-index:10;opacity:0.7;';
            cell.appendChild(label);
        }
    });

    showGridToolbar();
    editorOpen = true;
    console.log('[Grid Editor] ✅ 网格编辑模式已启动');
    console.log('[Grid Editor] 💡 点击格子编号区域选择格子，点击可编辑内容进行修改');
}

function selectCell(cellEl) {
    // Deselect previous
    if (selectedCell) {
        selectedCell.style.outline = '1px solid #d0dae8';
        selectedCell.style.backgroundColor = '';
    }
    // Select
    selectedCell = cellEl;
    cellEl.style.outline = '3px solid #6C63FF';
    cellEl.style.backgroundColor = 'rgba(108,99,255,0.05)';

    // Update toolbar info
    const id = cellEl.id || 'unknown';
    document.getElementById('ge-cell-id').textContent = '格子: ' + id.replace('cell-', '');
    document.getElementById('ge-cell-id').style.display = 'inline';
    document.getElementById('ge-field-name').textContent = '(未选中字段)';

    // Show cell panel
    showCellPanel(id);
}

function selectField(el) {
    selectedField = el;
    document.getElementById('ge-field-name').textContent = el.getAttribute('data-field') || '(选中字段)';
    el.focus();
}

function showCellPanel(cellId) {
    const panel = document.getElementById('ge-cell-panel');
    if (!panel) return;
    panel.style.display = 'flex';

    // Load cell bg if present
    const cell = document.getElementById(cellId);
    if (cell) {
        const bg = cell.style.backgroundColor || '';
        document.getElementById('ge-cell-bg').value = rgbToHex(bg) || '#ffffff';
    }
}

function rgbToHex(rgb) {
    if (!rgb || rgb === 'transparent') return '#ffffff';
    const match = rgb.match(/\d+/g);
    if (!match || match.length < 3) return '#ffffff';
    return '#' + [0,1,2].map(i => parseInt(match[i]).toString(16).padStart(2,'0')).join('');
}

function applyCellBg() {
    if (!selectedCell) return;
    const color = document.getElementById('ge-cell-bg').value;
    selectedCell.style.backgroundColor = color;
}

function applyCellPadding() {
    if (!selectedCell) return;
    const pad = document.getElementById('ge-cell-pad').value;
    selectedCell.style.padding = pad;
}

function toggleCellSelector() {
    if (cellSelectorVisible) {
        document.getElementById('ge-cell-selector').style.display = 'none';
        cellSelectorVisible = false;
        return;
    }
    // Show grid overview with all cells
    const selector = document.getElementById('ge-cell-selector');
    if (!selector) return;
    selector.style.display = 'block';
    selector.innerHTML = '<div style="font-weight:bold;margin-bottom:8px;">📋 网格概览</div>';
    document.querySelectorAll('.grid-cell').forEach((cell, idx) => {
        const id = cell.id || 'cell-' + idx;
        const btn = document.createElement('button');
        btn.textContent = id.replace('cell-', '');
        btn.style.cssText = 'margin:4px;padding:6px 12px;background:#eef2ff;border:1px solid #6C63FF;border-radius:8px;cursor:pointer;font-size:12px;';
        btn.onclick = () => {
            cell.scrollIntoView({behavior:'smooth', block:'center'});
            selectCell(cell);
            document.getElementById('ge-cell-selector').style.display = 'none';
            cellSelectorVisible = false;
        };
        selector.appendChild(btn);
    });
    cellSelectorVisible = true;
}

// ── 编辑工具栏功能 ──

function applyColor() {
    if (!selectedField) return;
    const c = document.getElementById('ge-color-picker').value;
    selectedField.style.color = c;
}

function applyBgColor() {
    if (!selectedField) return;
    const c = document.getElementById('ge-bg-picker').value;
    selectedField.style.backgroundColor = c;
}

function applyOpacity() {
    if (!selectedField) return;
    const v = document.getElementById('ge-opacity').value;
    selectedField.style.opacity = v;
}

// ── 字体/字重/字号/字色 独立控制 ──

function getActiveEditorEl() {
    const sel = window.getSelection();
    if (sel && sel.rangeCount > 0) {
        let node = sel.getRangeAt(0).startContainer;
        while (node && node.nodeType === 3) node = node.parentNode;
        return node ? node.closest('[data-field]') || node.closest('[contenteditable]') : null;
    }
    return selectedField || null;
}

function applyFontFamily() {
    const el = getActiveEditorEl();
    if (!el) return;
    el.style.fontFamily = document.getElementById('ge-font-family').value;
}

function applyFontWeight() {
    const el = getActiveEditorEl();
    if (!el) return;
    el.style.fontWeight = document.getElementById('ge-font-weight').value;
}

function applyFontSizeVE() {
    const el = getActiveEditorEl();
    if (!el) return;
    el.style.fontSize = document.getElementById('ge-font-size').value;
}

function applyFontColor() {
    const el = getActiveEditorEl();
    if (!el) return;
    el.style.color = document.getElementById('ge-color-picker').value;
}

// ── 导出与预览 ──

function exportFinalHTML() {
    const container = document.querySelector('.grid-card') || document.body;
    const clone = container.cloneNode(true);

    // Remove editor UI elements
    clone.querySelectorAll('.ge-editable, .ge-toolbar, .ge-overlay, .ge-cell-label, #ge-cell-panel, #ge-init-hint, #ge-cell-selector').forEach(el => el.remove());
    clone.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));

    const finalHTML = '<!DOCTYPE html>\n' + clone.outerHTML;
    const blob = new Blob([finalHTML], {type: 'text/html;charset=utf-8'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'final-' + Date.now() + '.html';
    a.click();
    URL.revokeObjectURL(a.href);
    alert('✅ 最终 HTML 已下载！');
}

function previewHTML() {
    const container = document.querySelector('.grid-card') || document.body;
    const clone = container.cloneNode(true);
    clone.querySelectorAll('.ge-editable, .ge-toolbar, .ge-overlay, .ge-cell-label').forEach(el => el.remove());
    const w = window.open('', '_blank');
    w.document.write('<!DOCTYPE html>\n' + clone.outerHTML);
    w.document.close();
}

function closeEditor() {
    document.querySelectorAll('.ge-editable').forEach(el => {
        el.style.outline = '';
        el.style.cursor = '';
        el.style.padding = '';
    });
    document.querySelectorAll('.grid-cell').forEach(el => {
        el.style.outline = '';
        el.style.cursor = '';
    });
    document.getElementById('ge-toolbar').style.display = 'none';
    const panel = document.getElementById('ge-cell-panel');
    if (panel) panel.style.display = 'none';
    const sel = document.getElementById('ge-cell-selector');
    if (sel) sel.style.display = 'none';
    editorOpen = false;
    selectedCell = null;
    selectedField = null;
}

// Drag & drop image support
document.addEventListener('dragover', e => {
    const t = e.target.closest('img');
    if (t && editorOpen) { e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; t.style.outline = '3px solid #00B894'; }
});
document.addEventListener('dragleave', e => {
    const t = e.target.closest('img');
    if (t) t.style.outline = '';
});
document.addEventListener('drop', e => {
    e.preventDefault();
    const t = e.target.closest('img');
    if (!t || !editorOpen) return;
    const f = e.dataTransfer.files[0];
    if (!f || !f.type.startsWith('image/')) { alert('请拖入图片文件'); return; }
    const r = new FileReader();
    r.onload = ev => { t.src = ev.target.result; t.style.outline = ''; };
    r.readAsDataURL(f);
});

// Keyboard shortcuts
document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 'e') { e.preventDefault(); editorOpen ? closeEditor() : initGridEditor(); }
    if (e.ctrlKey && e.key === 's') { e.preventDefault(); exportFinalHTML(); }
});
"""

# ── 增强工具栏 HTML (grid-aware) ──

TOOLBAR_HTML = r"""
<div id="ge-toolbar" style="display:none;position:fixed;top:0;left:0;right:0;z-index:99999;background:#1e1e2e;color:#fff;padding:6px 12px;align-items:center;gap:6px;font-size:12px;box-shadow:0 2px 12px rgba(0,0,0,0.3);max-height:48px;overflow:visible;">
  <div style="display:flex;align-items:center;gap:6px;flex-wrap:nowrap;width:100%;">

    <!-- Field info -->
    <span id="ge-cell-id" style="color:#6C63FF;font-weight:bold;font-size:11px;display:none;white-space:nowrap;"></span>
    <span id="ge-field-name" style="color:#FFD700;font-size:11px;min-width:60px;white-space:nowrap;">(未选中字段)</span>

    <!-- Divider -->
    <div style="width:1px;height:18px;background:#555;flex-shrink:0;"></div>

    <!-- Text formatting -->
    <button onclick="document.execCommand('bold')" title="加粗" style="background:#333;color:#fff;border:1px solid #666;padding:2px 6px;border-radius:4px;cursor:pointer;font-weight:bold;font-size:11px;">B</button>
    <button onclick="document.execCommand('italic')" title="斜体" style="background:#333;color:#fff;border:1px solid #666;padding:2px 6px;border-radius:4px;cursor:pointer;font-style:italic;font-size:11px;">I</button>
    <button onclick="document.execCommand('underline')" title="下划线" style="background:#333;color:#fff;border:1px solid #666;padding:2px 6px;border-radius:4px;cursor:pointer;text-decoration:underline;font-size:11px;">U</button>

    <!-- Font family -->
    <select id="ge-font-family" onchange="applyFontFamily()" title="字体" style="background:#333;color:#fff;border:1px solid #666;padding:1px 4px;border-radius:4px;font-size:10px;max-width:90px;">
      <option value="">字体</option>
      <option value="system-ui, -apple-system, sans-serif">系统默认</option>
      <option value="'Microsoft YaHei', sans-serif">微软雅黑</option>
      <option value="'PingFang SC', sans-serif">苹方</option>
      <option value="SimSun, serif">宋体</option>
      <option value="SimHei, sans-serif">黑体</option>
      <option value="Consolas, monospace">等宽</option>
    </select>

    <!-- Font weight -->
    <select id="ge-font-weight" onchange="applyFontWeight()" title="字重" style="background:#333;color:#fff;border:1px solid #666;padding:1px 4px;border-radius:4px;font-size:10px;width:50px;">
      <option value="">字重</option>
      <option value="100">细</option>
      <option value="400">常规</option>
      <option value="600">半粗</option>
      <option value="700">粗</option>
      <option value="900">超粗</option>
    </select>

    <!-- Font size -->
    <select id="ge-font-size" onchange="applyFontSizeVE()" title="字号" style="background:#333;color:#fff;border:1px solid #666;padding:1px 4px;border-radius:4px;font-size:10px;width:48px;">
      <option value="">字号</option>
      <option value="9px">9</option><option value="11px">11</option><option value="12px">12</option>
      <option value="14px">14</option><option value="15px">15</option><option value="16px">16</option>
      <option value="18px">18</option><option value="20px">20</option><option value="24px">24</option>
      <option value="28px">28</option><option value="32px">32</option><option value="36px">36</option>
    </select>

    <!-- Color & bg -->
    <label style="color:#ccc;font-size:10px;">🎨</label>
    <input type="color" id="ge-color-picker" value="#333333" onchange="applyFontColor()" title="字色" style="width:20px;height:20px;border:none;cursor:pointer;padding:0;">
    <label style="color:#ccc;font-size:10px;">🖌️</label>
    <input type="color" id="ge-bg-picker" value="#ffffff" onchange="applyBgColor()" title="背景色" style="width:20px;height:20px;border:none;cursor:pointer;padding:0;">

    <!-- Opacity -->
    <select id="ge-opacity" onchange="applyOpacity()" title="透明度" style="background:#333;color:#fff;border:1px solid #666;padding:1px 4px;border-radius:4px;font-size:10px;">
      <option value="1">100%</option>
      <option value="0.9">90%</option>
      <option value="0.7">70%</option>
      <option value="0.5">50%</option>
    </select>

    <!-- Grid controls -->
    <div style="width:1px;height:18px;background:#555;flex-shrink:0;"></div>
    <button onclick="toggleCellSelector()" title="网格概览" style="background:#3F51B5;color:#fff;border:none;padding:2px 8px;border-radius:4px;cursor:pointer;font-size:11px;">📋 网格</button>

    <!-- Flex spacer -->
    <div style="flex:1;"></div>

    <!-- Actions -->
    <button onclick="previewHTML()" title="预览" style="background:#3F51B5;color:#fff;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:11px;">👁️ 预览</button>
    <button onclick="exportFinalHTML()" title="生成最终HTML" style="background:#00B894;color:#fff;border:none;padding:4px 12px;border-radius:4px;cursor:pointer;font-weight:bold;font-size:11px;">✅ 导出</button>
    <button onclick="closeEditor()" title="退出" style="background:#E17055;color:#fff;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;font-size:11px;">❌</button>
  </div>
</div>

<!-- Cell property panel (floating) -->
<div id="ge-cell-panel" style="display:none;position:fixed;bottom:60px;right:20px;z-index:99998;background:#1e1e2e;color:#fff;padding:12px 16px;border-radius:12px;font-size:12px;width:200px;box-shadow:0 4px 16px rgba(0,0,0,0.4);">
  <div style="font-weight:bold;margin-bottom:8px;color:#6C63FF;">🟣 格子属性</div>
  <div style="display:flex;flex-direction:column;gap:6px;">
    <label style="font-size:11px;color:#aaa;">底板颜色</label>
    <input type="color" id="ge-cell-bg" value="#ffffff" onchange="applyCellBg()" style="width:100%;height:28px;border:none;cursor:pointer;">
    <label style="font-size:11px;color:#aaa;">内边距</label>
    <select id="ge-cell-pad" onchange="applyCellPadding()" style="background:#333;color:#fff;border:1px solid #666;padding:2px 4px;border-radius:4px;">
      <option value="4px">4px</option>
      <option value="8px">8px</option>
      <option value="12px">12px</option>
      <option value="16px" selected>16px</option>
      <option value="24px">24px</option>
    </select>
  </div>
</div>

<!-- Grid cell selector overlay -->
<div id="ge-cell-selector" style="display:none;position:fixed;bottom:120px;right:20px;z-index:99997;background:#1e1e2e;color:#fff;padding:12px 16px;border-radius:12px;font-size:12px;max-height:200px;overflow-y:auto;min-width:160px;box-shadow:0 4px 16px rgba(0,0,0,0.4);"></div>

<!-- Init hint -->
<div id="ge-init-hint" style="position:fixed;bottom:20px;right:20px;z-index:99996;background:#6C63FF;color:white;padding:10px 18px;border-radius:8px;cursor:pointer;font-size:13px;box-shadow:0 4px 12px rgba(108,99,255,0.4);" onclick="this.style.display='none';initGridEditor();">
  🛠️ 启动网格编辑器
</div>
"""

def inject_editor(html_str):
    """Inject grid-aware editor into HTML string"""
    editor_block = TOOLBAR_HTML + '<script>' + GRID_EDITOR_JS + '</script>'
    if '</body>' in html_str:
        html_str = html_str.replace('</body>', editor_block + '\n</body>', 1)
    else:
        html_str = html_str + editor_block
    return html_str

def generate_standalone_editor(template_path, output_path):
    """Generate a standalone grid editor HTML wrapping the template"""
    tpl = Path(template_path)
    if not tpl.exists():
        show_error("文件错误", f"找不到模板文件: {tpl}", "请确认 --template 参数指向一个已存在的 HTML 文件")
        return None

    try:
        html = tpl.read_text(encoding='utf-8')
    except Exception as e:
        show_error("文件错误", f"读取模板文件失败: {e}", "检查文件编码（应为 UTF-8）")
        return None

    html = inject_editor(html)

    if not safe_write_text(output_path, html, "编辑器 HTML"):
        return None

    print(f'[OK] 网格编辑器已生成: {output_path}')
    print('     浏览器打开后按 Ctrl+E 切换编辑模式')
    return str(output_path)

def generate_from_type(template_type, output_path):
    """Generate editor from built-in template type"""
    if template_type not in BUILTIN_TEMPLATES:
        show_error("模板错误", f"未知模板类型: {template_type}", f"可用类型: {', '.join(BUILTIN_TEMPLATES.keys())}")
        return None

    spec = BUILTIN_TEMPLATES[template_type]
    html = generate_html(spec)
    html = inject_editor(html)

    if not safe_write_text(output_path, html, f"编辑器 HTML ({template_type})"):
        return None

    print(f'[OK] 网格编辑器已生成（来自 "{template_type}"）: {output_path}')
    print('     浏览器打开后按 Ctrl+E 切换编辑模式')
    return str(output_path)

def main():
    try:
        _main_impl()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
    except Exception as e:
        show_error("内部错误", f"程序发生未预期的错误: {type(e).__name__}",
                   "使用 --help 查看参数说明。如持续报错，可查看 FAQ。")
        import traceback
        traceback.print_exc()

def _main_impl():
    ap = argparse.ArgumentParser(description='Grid-aware 可视化编辑器生成器 v2', add_help=True)
    ap.add_argument('--template', help='输入模板 HTML 文件路径')
    ap.add_argument('--type', help='内置模板类型名称（如 harmony-app, promo）')
    ap.add_argument('--output', '-o', required=True, help='输出编辑器 HTML 文件路径')
    ap.add_argument('--debug', action='store_true', help='显示详细错误堆栈')

    args = ap.parse_args()

    if not args.template and not args.type:
        show_error("参数错误", "必须提供 --template 或 --type 参数",
                   "用法: python visual_editor.py --type harmony-app -o data/output/editor.html\n"
                   "  或: python visual_editor.py --template data/output/template.html -o data/output/editor.html")
        return

    if args.type:
        generate_from_type(args.type, args.output)
    elif args.template:
        generate_standalone_editor(args.template, args.output)

if __name__ == '__main__':
    main()
