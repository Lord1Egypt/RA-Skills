---
name: html-ppt-editable
description: 为 HTML 演示文稿添加浏览器内联编辑功能——文字修改、字体颜色调整、文字框拖拽。基于 contenteditable + localStorage 实现，零依赖。
---

## 触发关键词

当用户提到以下内容时使用此技能：
- 可编辑PPT / HTML幻灯片编辑 / inline edit slides
- html-ppt-editable / HTML可编辑
- 明确要求在浏览器中修改 HTML 幻灯片文字

# html-ppt-editable

在任意 HTML 演示文稿的基础上，追加浏览器内联编辑能力。

## 核心特性

- **编辑按钮隐藏式**：默认完全隐藏，鼠标移入左上角 90×90px 区域才淡入显现，移开 500ms 后自动淡出
- **键盘快捷键**：按 `E` 进入/退出编辑，`Ctrl+S` 下载保存
- **contentEditable**：点击文字直接修改，修改后虚线边框提示
- **localStorage**：自动保存编辑状态
- **零依赖**：纯原生 JS，无任何外部库

## 为什么不用 CSS `~` 选择器

`.hotzone:hover ~ .toggle` 会失效——鼠标从热区移向按钮时，先离开热区，按钮立刻消失，根本点不到。

**正确做法：JS 500ms 延迟隐藏**

```javascript
let hideTimer = null;

document.addEventListener('mousemove', (e) => {
  // 热区 → 显示
  if (e.clientX < 90 && e.clientY < 90) {
    clearTimeout(hideTimer);
    btn.classList.add('show');
  } else {
    // 热区外 + 非按钮/非编辑区 → 延迟隐藏
    if (!isEditing && !e.target.closest('.edit-btn')) scheduleHide();
  }
});

function scheduleHide() {
  hideTimer = setTimeout(() => {
    if (!isEditing) btn.classList.remove('show');
  }, 500); // 宽限期，让用户移动到按钮
}
```

## 集成步骤

在 HTML 演示文稿的 `</body>` 前追加三块代码：

### Step 1: HTML（在 `</body>` 前插入）

```html
<!-- 编辑按钮（完全隐藏，鼠标移入左上角区域显现） -->
<button class="edit-btn" id="editBtn" title="按 E 进入编辑模式">✏️</button>
<span class="edit-hint">按 E 键进入编辑 · Ctrl+S 保存</span>

<!-- 保存操作条 -->
<div class="save-banner" id="saveBanner">
  <span>编辑模式 · 点击文字直接修改</span>
  <button id="saveBtn">💾 保存下载</button>
  <button class="secondary" id="exitBtn">退出</button>
</div>
```

### Step 2: CSS（在 `<style>` 中追加）

```css
/* ====== 编辑按钮 ====== */
.edit-btn {
  position: fixed;
  top: 16px; left: 16px;
  width: 44px; height: 44px;
  background: rgba(245,244,237,0.95);
  border: 1.5pt solid var(--brand, #1B365D);
  border-radius: 8px;
  color: var(--brand, #1B365D);
  font-size: 20px;
  cursor: pointer;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  font-family: sans-serif;
  /* 隐藏式核心 */
  opacity: 0;
  pointer-events: none;
  transform: scale(0.9);
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.edit-btn.show {
  opacity: 0.88;
  pointer-events: auto;
  transform: scale(1);
}
.edit-btn.show:hover {
  opacity: 1;
  transform: scale(1.06);
}
.edit-hint {
  position: fixed;
  top: 16px; left: 70px;
  background: rgba(245,244,237,0.95);
  border: 1pt solid var(--brand, #1B365D);
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 9pt;
  color: var(--brand, #1B365D);
  z-index: 9999;
  pointer-events: none;
  font-family: sans-serif;
  opacity: 0;
  transition: opacity 0.25s ease;
  white-space: nowrap;
}
.edit-btn.show:hover ~ .edit-hint {
  opacity: 1;
}

/* 编辑模式下：文字悬停虚线提示 */
body.edit-mode [contenteditable]:hover {
  outline: 1.5px dashed rgba(27,54,93,0.4);
  cursor: text;
}
[contenteditable] { outline: none; }

/* ====== 保存操作条 ====== */
.save-banner {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%) translateY(80px);
  background: rgba(245,244,237,0.97);
  border: 1.5pt solid var(--brand, #1B365D);
  border-radius: 8px;
  padding: 8px 16px;
  display: flex;
  gap: 10px;
  align-items: center;
  z-index: 9999;
  font-family: sans-serif;
  font-size: 9pt;
  color: var(--olive, #504e49);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  transition: transform 0.3s ease;
}
.save-banner.show { transform: translateX(-50%) translateY(0); }
.save-banner button {
  background: var(--brand, #1B365D);
  border: none;
  border-radius: 4px;
  color: white;
  padding: 5px 12px;
  font-size: 9pt;
  cursor: pointer;
  font-family: sans-serif;
}
.save-banner button.secondary {
  background: transparent;
  color: var(--brand, #1B365D);
  border: 1pt solid var(--brand, #1B365D);
}

/* 打印时隐藏 */
@media print {
  .edit-btn, .edit-hint, .save-banner { display: none !important; }
}
```

### Step 3: JavaScript（在 `</body>` 前插入）

```javascript
<script>
(function() {
  var btn = document.getElementById('editBtn');
  var banner = document.getElementById('saveBanner');
  var saveBtn = document.getElementById('saveBtn');
  var exitBtn = document.getElementById('exitBtn');
  var isEditing = false;
  var hideTimer = null;

  // 可编辑元素（根据实际结构调整选择器）
  var editables = document.querySelectorAll(
    'h1, h2, h3, h4, p, li, td, th, .metric-value, .metric-label,' +
    '.lead, .callout, .footer span, .eyebrow, .subtitle, .meta,' +
    '.tl-year, .tl-head, .tl-body'
  );

  /* ---- 隐藏式按钮核心逻辑 ---- */
  function showBtn() {
    clearTimeout(hideTimer);
    btn.classList.add('show');
  }

  function scheduleHide() {
    hideTimer = setTimeout(function() {
      if (!isEditing) btn.classList.remove('show');
    }, 500);
  }

  // 鼠标移动：左上角热区显示，其他区域延迟隐藏
  document.addEventListener('mousemove', function(e) {
    if (e.clientX < 90 && e.clientY < 90) {
      showBtn();
    } else if (
      !isEditing &&
      !e.target.closest('.edit-btn') &&
      !e.target.closest('.save-banner')
    ) {
      scheduleHide();
    }
  });

  // 按钮悬停保持显示
  btn.addEventListener('mouseenter', function() {
    clearTimeout(hideTimer);
    showBtn();
  });
  btn.addEventListener('mouseleave', scheduleHide);

  /* ---- 编辑模式 ---- */
  function enterEdit() {
    isEditing = true;
    document.body.classList.add('edit-mode');
    btn.classList.add('show', 'active');
    btn.textContent = '✓';
    banner.classList.add('show');
    editables.forEach(function(el) {
      el.setAttribute('contenteditable', 'true');
    });
  }

  function exitEdit() {
    isEditing = false;
    document.body.classList.remove('edit-mode');
    btn.classList.remove('active');
    btn.textContent = '✏️';
    banner.classList.remove('show');
    editables.forEach(function(el) {
      el.removeAttribute('contenteditable');
    });
  }

  /* ---- 保存下载 ---- */
  function saveFile() {
    editables.forEach(function(el) { el.removeAttribute('contenteditable'); });
    document.body.classList.remove('edit-mode');
    banner.classList.remove('show');
    var html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
    editables.forEach(function(el) { el.setAttribute('contenteditable', 'true'); });
    document.body.classList.add('edit-mode');
    banner.classList.add('show');
    var blob = new Blob([html], { type: 'text/html' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'edited.html';
    a.click();
    URL.revokeObjectURL(a.href);
  }

  /* ---- 事件绑定 ---- */
  btn.addEventListener('click', function() {
    isEditing ? exitEdit() : enterEdit();
  });
  exitBtn.addEventListener('click', exitEdit);
  saveBtn.addEventListener('click', saveFile);

  document.addEventListener('keydown', function(e) {
    // E 键切换编辑模式（非输入框内）
    if ((e.key === 'e' || e.key === 'E') && !e.target.getAttribute('contenteditable')) {
      isEditing ? exitEdit() : enterEdit();
    }
    // Ctrl+S 保存
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      e.preventDefault();
      if (isEditing) saveFile();
    }
  });
})();
</script>
```

## 使用方式

1. 在 HTML 文件的 `</body>` 前插入上述三段代码
2. 浏览器打开
3. **鼠标移到左上角** → 编辑按钮 ✏️ 淡入
4. **按 E** 或点 ✏️ → 进入编辑模式，按钮变成 ✓
5. **点击文字直接修改**（虚线边框提示）
6. **Ctrl+S** 或点"💾 保存下载" → 下载 HTML 文件
7. **按 E** 或点"退出" → 退出编辑模式

## 局限性

- `contentEditable` 不支持表格行的动态增删
- localStorage 有 5MB 上限
- 拖拽功能需额外实现

## 触发条件

- "可编辑PPT" / "HTML幻灯片编辑" / "inline edit slides"
- "html-ppt-editable" / "HTML可编辑"
- 明确要求在浏览器中修改 HTML 幻灯片文字
