# 双语对照导出模块

>  **加载触发器**：PDF 翻译完成后 MANDATORY。合并逐页译文 → 生成 Gxpcode.html + Gxpcode.md。

---

## 输出目录

> 从 `config.json` 的 `output_dir` 读取。子目录自动生成为 `{YYYY-MM-DD_HH-MM-SS}-{pdf-slug}/`。
> 所有 `$outDir` 在步骤 1.2 中已根据配置初始化，此处直接使用。

---

## 步骤 A：合并逐页译文 → translated.json

翻译完成后，逐页译文分散在 `pages/` 目录下。使用 `merge_translations.py` 将其映射为 element-indexed JSON，自动处理跨页续段。

```powershell
& $PythonExe `
  "$SkillDir\scripts\merge_translations.py" `
  --elements "$paddleDir/recognition_json/<file>.json" `
  --pages-dir "$outDir/pages" `
  --out "$outDir/translated.json"
```

---

## 步骤 B：生成 Gxpcode.html

**B.1** 调用 `scripts/Gxpcode_html.py`：

```powershell
& $PythonExe `
  "$SkillDir\scripts\Gxpcode_html.py" `
  --elements "$paddleDir/recognition_json/<file>.json" `
  --translated "$outDir/translated.json" `
  --out-dir "$outDir" `
  --title "<PDF文件名>" `
  --paddleocr-dir "$paddleDir"
```

**B.2** 产出：Risograph 风格双语对照 HTML

- 控制栏：桌面端固定顶栏，移动端固定底栏（安全区适配），视图切换（双栏/仅原文/仅译文）+ 字号切换（小/中/大）+ 目录
- 左侧 TOC 章节目录：IntersectionObserver 滚动联动（移动端 toggle 弹出，自动关闭）
- 段落双栏对照 + 悬停复制按钮（`data-copy` + 事件委托）
- **图片 Lightbox**：点击放大、再次点击/点背景关闭（`onclick` 单事件，无移动端 double-toggle）
- **上下标渲染**：Python `preprocess_latex()` 将 `$^{...}$`/`$_{...}$` → `<sup>/<sub>`，无须 MathJax CDN
- 章节头卡片（顶级红 / 次级绿）
- 移动端：图片单 tap 开/关 lightbox，控件栏 `flex-wrap` + `safe-area-inset-bottom` 适配刘海屏
- 样式：暖米色底、白卡片、圆角、低饱和配色

---

## 步骤 C：生成 Gxpcode.md

**C.1** 调用 `scripts/Gxpcode_markdown.py`：

```powershell
& $PythonExe `
  "$SkillDir\scripts\Gxpcode_markdown.py" `
  --elements "$paddleDir/recognition_json/<file>.json" `
  --translated "$outDir/translated.json" `
  --out-dir "$outDir" `
  --title "<PDF文件名>"
```

**C.2** 产出：双语对照 Markdown（表格格式，按章节分节）

---

## 输出清单

```
translation-output/{ts}-{slug}/
├── paddleocr/                 # paddleocr 原始解析
│   ├── markdown/<file>_p*.md
│   └── recognition_json/<file>.json
├── pages/                     # 逐页翻译中间产物
│   ├── <file>_p001_trans.md
│   └── ...
├── translated.json            # element-indexed 译文映射
├── Gxpcode.html               # 双语对照 HTML
└── Gxpcode.md                 # 双语对照 Markdown
```
