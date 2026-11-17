# Figure Rendering / 图形渲染规范（SVG 展示在 HTML 报告中）

> ⚠️ **2026-08-26 修订：内联 `show_widget` 渲染已取消**。所有 `figures[].svg` 一律展示在 `run_analysis` 生成的**聚合 HTML 报告**里（agent 用 `present_files` 打开预览），不再内联进对话流。本文档原"内联优先"原则废止；保留其中的 SVG 净化 / viewBox / 宽度处理技术细节，供 HTML 报告渲染链（`adapters/rendering.py` 的 `build_figure_widget` / `render_html_report`）复用。
> 生效：2026-08-19（v1.9.5+）｜ 范围：meta-analysis 分析结果的所有 `figures[].svg`。**唯一展示面 = HTML 报告**，同时另存 `output/` 供下载/编辑。

## 1. 原则

| 原则 | 要求 |
|---|---|
| **HTML 报告唯一面** | 图的 `figures[].svg` 一律嵌入 HTML 报告展示（agent 用 `present_files` 打开），**不再内联 widget** |
| **矢量可编辑** | 所有图保持 `<text>` 文本元素，禁止转位图；编辑工具见 `references/svg_editing.md` |
| **原尺寸保真 · 不放大** | 图**保持自然内容尺寸，绝不放大到固定画幅**（如 680px）。容器装不下即出**横向滚动条**（见 §3）——任何场景都不缩小、也不强制拉伸图 |
| **主题适配** | SVG 内容为深色文字，容器一律浅底（`#fff`）+ 细边框，明暗主题下均清晰 |

## 2. 标准容器模板（HTML fragment）

```html
<!-- 单图容器（figures 数组 → 每图一个，纵向排列） -->
<div style="display:flex;flex-direction:column;gap:16px;font-family:var(--font-sans);">
  <div>
    <div style="font-size:13px;font-weight:500;margin:0 0 6px;color:var(--color-text-primary);">
      森林图 · 新药 X vs 标准治疗（OR）   <!-- 标题：≤24 字，宽容器一行放不下时允许换行 -->
    </div>
    <!-- ★ 横向滚动容器：图固定原尺寸，容器装不下即出横向滚动条（核心规则） -->
    <div style="overflow-x:auto;max-width:100%;background:#fff;
                border:0.5px solid var(--color-border-tertiary);
                border-radius:var(--border-radius-md);">
      <svg viewBox="-140 -8 785 376"  <!-- viewBox = content_bbox 动态值 -->
           style="width:785px;height:auto;display:block;margin:0 auto;">
        …SVG 内部内容（去外层 <svg> 标签后的 inner）…
      </svg>
    </div>
  </div>
</div>
```

## 3. 宽度处理策略（核心）

**问题一：内容超界（更根本）**——svglite 输出固定 viewBox（如 `0 0 504 360`），但内容**可能超出该区域**：meta 包 forest() 把 Study/Events/OR/95%CI/Weight 列画在图形区外（实测 x∈[-140, 644]，实际宽 **785px**）。按原 viewBox 渲染会被浏览器裁剪两侧文字。**必须先扩展 viewBox**。

**问题二：宽度**——任何情况下不缩小图（缩小使文字不可读），也**绝不放大到固定画幅**（如因容器要求 680px 而把 504px 的图拉伸）。始终按 `content_bbox` 算出的自然内容宽度（`max_x - min_x`，森林图约 785px）嵌入，**“提供刚好贴合内容宽度的画幅”**即可，装不下就出横向滚动条。

**策略（默认，`adapters/rendering.py` 已实现）**：

```python
from rendering import build_figure_widget
html = build_figure_widget(figures, ["森林图 · OR", "漏斗图 · Egger"])
```

| 步骤 | 说明 |
|---|---|
| ⓪ `_strip_clip()` | **移除内部 clipPath**（svglite 固定 0..504 裁剪，会裁掉森林图左右文字列——即使外层 viewBox 扩展也无效）；必须在 bbox 之前调用 |
| ① `content_bbox()` | 扫描内容元素（text 含 textLength/text-anchor、transform 文本解析 translate 锚点、rect、line、circle、polyline/polygon）极值 → 实际边界（**x 方向 pad=8 紧凑、y 方向 pad_y=24 留白**，森林图上下保持呼吸空间） |
| ② viewBox | 动态设为 `min_x min_y 宽 高`（森林图 → `-140 -8 785 376`），内容全部可见 |
| ③ 宽度 | SVG 固定为**实际内容宽度**（785px）不缩放 |
| ④ 容器 | 外层 `overflow-x:auto` —— 容器装不下即出横向滚动条（含正常对话窗，只要没显示完就必须滚动而非缩小） |
| ⑤ 居中 | SVG `margin:0 auto` —— 容器比图宽时水平居中；窄容器溢出时 auto 边距归零自动回左对齐出滚动条（**勿用 flex justify-center**：溢出时左侧内容不可滚动到达） |

- 不用 `width:100%`（避免任何隐性缩放）；`max-width:100%` 只约束容器
- 移动端加 `-webkit-overflow-scrolling:touch` 平滑滚动（可选）
- 完整模块：`adapters/rendering.py`（extract_svg / content_bbox / build_figure_widget，标准库零依赖）

**备选模式（非默认，明确需要时启用）**：自适应缩放 `width:100%;min-width:480px`——宽容器放大撑满、窄容器滚动；仅在用户明确要求"图铺满对话窗"时使用。

**可选进阶：缩放控件**（交互式呈现时启用）

```html
<div id="fig1" style="position:relative;">
  <div style="overflow-x:auto;max-width:100%;">
    <svg id="fig1-svg" viewBox="0 0 504 360"
         style="width:504px;height:auto;display:block;transition:width .15s;">
      …inner…
    </svg>
  </div>
  <div style="position:absolute;top:6px;right:6px;display:flex;gap:4px;">
    <button onclick="figZoom('fig1',-50)">−</button>
    <button onclick="figZoom('fig1',0)">适应</button>
    <button onclick="figZoom('fig1',50)">＋</button>
  </div>
</div>
<script>
function figZoom(id, d){ const svg=document.getElementById(id+'-svg');
  let w=parseFloat(svg.style.width)||504;
  if(d===0){svg.style.width='504px';return;}
  w=Math.min(Math.max(w+d, 320), 1200);
  svg.style.width=w+'px'; }
</script>
```

## 4. SVG 嵌入方法（Python，adapters 层消费 figures[].svg）

**直接使用正式模块 `adapters/rendering.py`**（标准库零依赖，已实现全部逻辑）：

```python
from rendering import build_figure_widget, extract_svg, content_bbox

html = build_figure_widget(figures, ["森林图 · OR", "漏斗图 · Egger"])
# 内部步骤：
#   ① extract_svg(fig["svg"])  → (inner, viewbox)     兼容 svglite 单引号属性
#   ② content_bbox(inner)      → (min_x, min_y, max_x, max_y)  扫描内容实际边界
#   ③ viewBox = "min_x min_y 宽 高"（森林图 → "-140 -8 785 376"，解决内容超界裁剪）
#   ④ SVG 固定实际内容宽度（785px）+ 容器 overflow-x:auto（装不下即滚动）
```

如需自定义实现（不依赖模块），核心步骤：

```python
import re
def extract_svg(svg_str: str):
    """返回 (inner, viewbox)。兼容单/双引号属性。"""
    m = re.search(r"<svg[^>]*viewBox=['\"]([^'\"]+)['\"][^>]*>(.*)</svg>", svg_str, re.S)
    if not m:
        m = re.search(r"<svg[^>]*>(.*)</svg>", svg_str, re.S)  # 无 viewBox 兜底
        return (m.group(1), "0 0 504 360") if m else (svg_str, "0 0 504 360")
    return (m.group(2), m.group(1))
```

**内容边界扫描要点（content_bbox）**：
- `text`：`x + textLength`（按 `text-anchor` 的 start/middle/end 修正左右端点）；**transform 文本**（如漏斗图 y 轴旋转标签）解析 `translate(tx,ty)` 锚点并沿 x/y **双向扩展 textLength**（旋转方向不定，保守覆盖保证不裁剪）
- `rect`：跳过 `width=100%` 白底占位；`line`/`circle` 取端点±r；`polyline`/`polygon` 解析 points
- 数值一律 strip `px` 后缀（svglite 的 textLength 是 `39.34px`）
- 未扫描到内容时回退原画布 `0 0 504 360`

**坑**（实测）：
- **内部 clipPath 会裁内容**：svglite 输出固定 `0 0 504 360` 的 clipPath 包裹绘图元素，森林图左右文字列（x∈[-140,644]）被裁——必须 `_strip_clip()` 移除（含定义与引用），且在 content_bbox 之前调用（clip 内 rect 会污染 bbox）
- svglite 的 `<polyline points=…>` 坐标列表可能单行 7000+ 字符 → 读取/渲染前按空白拆行（points 内空白合法）
- SVG 内部 `<style>` 用 CDATA，嵌入 HTML widget 时保留原样即可
- `%` 字符（如 `fill-opacity:0.5` 用 `%` 书写时）→ python 格式化须 `%%` 或 f-string 直接拼接
- **svglite 2.2.2 偶发缺 `</g>`**（实测森林图 `<g>` 开 2 闭 1）→ 浏览器宽容渲染 OK，但 cairosvg 严格 XML 解析报 `mismatched tag`；`_fix_xml()` 用标签栈补齐缺失闭合（仅 PNG 路径使用；内联渲染不需要）

## 5. 多图布局

- 默认：figures 数组顺序 → **每图一行纵向流式**（对话流天然排版，宽图友好）
- 同类型小图（如亚组森林图多张）可 grid 2 列：`display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr))`

## 6. 标题规范

- 简洁 ≤24 字，如 `森林图 · OR`、`漏斗图 · Egger 检验`、`剂量-反应曲线`
- 超长（含研究名）时：主标题 + 冒号省略，如 `森林图（5 研究，OR）`
- 标题文字在窄容器自动换行（默认行为），无需手动截断

## 7. 出图模式与渲染计时（2026-08-19）

`adapters/run_analysis.py` 提供 `render_figures(out, mode, out_dir)`：

| 模式 | 行为 | 适用场景 |
|---|---|---|
| `svg_inline`（默认） | `figures[].svg` 原样保留，agent 用 HTML 报告展示（不再内联 widget） | 普通场景，可编辑文本需求 |
| `png_file` | 本地 cairosvg 转 PNG（同一处理链：strip clip → fix xml → bbox → viewBox → 光栅化）存 `out_dir`，figures 替换为 `{type, format:"png", path}` | SVG 体量超大或嵌入慢时（界面渲染快、不占 LLM 上下文，但变位图） |

**渲染计时（★ 本地渲染阶段，非 coze 计算）**：
- `render_elapsed_seconds` = 拿到 SVG → 处理 → widget/PNG 就绪的秒数
- `render_svg_kb` = 所有 figures SVG 字节合计（KB）—— 界面浏览器渲染无法在 agent 侧计时，用此作代理
- `render_hint`（仅 svg_inline 模式）：当 `render_elapsed_seconds > 30s` 或 `render_svg_kb > 200KB` 时生成中文提示，建议切 `png_file`
- 阈值常量在 `run_analysis.py` 顶部 `RENDER_SVG_THRESHOLD` / `RENDER_SVG_KB_THRESHOLD`
- coze 计算/网络耗时见 `out['coze_elapsed_seconds']`（**仅诊断参考，不参与提示**）

## 8. 与 Output 章节的关系

- **HTML 报告（唯一展示面）**：`run_analysis` 生成的聚合 HTML 报告（`out['html_report']`），agent 用 `present_files` 打开预览（本文档技术细节服务于该渲染链）
- **output/ 落盘**：仍保存原始 `.svg` 文件供下载/编辑/期刊转换（`references/svg_editing.md`）
- 报告=查看，落盘=交付物
