# Session 36：pure Latin pill label 需要单独走 Latin-safe font

时间：2026-04-24

## 背景

在 Session 34/35 之后，`data-story` 的 `P1 / P8` 胶囊结构已经回正：

- `_pair_with` 不再被 centered wrapper packer 拆散
- `div.cta-pill` 也重新进入了胶囊组件路径

但肉眼仍然会觉得胶囊“不完全像”，继续排查后确认，剩下还有一层字体问题：

- 胶囊里的文本是纯 Latin
  - `slide-creator`
  - `/slide-creator`
- 但 exporter 之前只按字体栈选 font，不看文本内容
- 只要字体栈里出现 `Noto Sans SC / PingFang / system-ui`
  就会整体回退到 `Microsoft YaHei`

这对中文正文是稳的，但对纯 Latin 的 pill label 会让字宽、字重、气质都偏掉。

## 本轮修复

### 1. `map_font()` 增加 text-aware 分支

现在 `map_font(css_font_family, text=...)` 会先判断文本内容：

- 如果是 pure Latin / ASCII label
  - 优先走 Latin-safe font
- 如果含 CJK
  - 继续走稳定的 CJK safe font

### 2. 新增 Latin-safe font 映射

增加了这类映射：

- `Inter -> Calibri`
- `DM Sans -> Calibri`
- `system-ui / -apple-system / BlinkMacSystemFont -> Calibri`
- monospace 倾向 `Consolas`

目标不是 100% 还原浏览器字体，而是：

- 让 pure Latin label 不再被错误拉回 CJK 字体
- 同时保持 Office / WPS 环境的稳定可用

### 3. pill shape 内嵌文本也同步走这条字体映射

`pill_text` 之前在 `export_shape_background()` 里是手工写 run：

- 设了 size
- 设了 color
- 但没有走统一 font mapping

现在这里也补上：

- `map_font(..., text=pill_text)`
- `set_run_fonts(...)`

## 验证

新增测试：

- `test_map_font_pure_latin_prefers_latin_safe_font_even_in_mixed_stack()`

直接验证：

- `"'Inter', 'Noto Sans SC', system-ui, sans-serif" + "slide-creator"`
- 应该返回 `('Calibri', 'Calibri')`

同时确认：

- 同一字体栈 + 中文文本
- 仍然返回 `('Microsoft YaHei', 'Microsoft YaHei')`

`python3 scripts/test-export.py` 继续全绿。

## 一个重要坑

这轮还确认了一个容易误判的问题：

- `python-pptx` 重新读回 `run.font.name`
- 不一定等于最终 XML 里实际写入的 `a:latin typeface`

这次就出现了：

- API 读回看起来像 `Microsoft YaHei`
- 但直接解压 `ppt/slides/slide1.xml / slide8.xml`
- 实际写入已经是：
  - `<a:latin typeface="Calibri"/>`
  - `<a:ea typeface="Calibri"/>`
  - `<a:cs typeface="Calibri"/>`

所以后续如果遇到“字体似乎没变”，必须优先看：

1. PPTX XML
2. 而不是只看 `python-pptx` 读回对象

## 不要再犯

1. 不要再把纯 Latin 的胶囊/标签和中文正文走同一条字体 fallback。
2. `map_font()` 以后必须允许基于文本内容做分流，而不是只看 CSS stack。
3. 验证字体是否真正写进 PPTX 时，优先看 XML，不要只看 `python-pptx` 读回字段。

## 当前影响

这轮主要影响：

- `data-story` 的 `P1 / P8` pill labels
- 以及未来所有：
  - pure Latin badge
  - CTA pill
  - command tag
  - short English KPI tag

这些元素现在会更接近源 HTML 的 Latin 字形，而不会再被统一拉回 CJK safe font。
