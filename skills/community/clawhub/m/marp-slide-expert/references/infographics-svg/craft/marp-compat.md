# marp 兼容层 — 内联 SVG 的前置条件与静默失败模式

> **本文件自足**：§1–§3 是把 SVG 放进 marp 的全部硬约束，§4 是渲染器矩阵，§5 是陷阱速查。画图前读一次，之后按 §5 排查。

## 1. 什么必须加 `--html`，什么不用

marp 默认转义内联 HTML，但**转义的范围只包含 `<svg>` 这类需要 HTML 解析器介入的标签**。实测（marp-cli v4.5.1）：

| 元素 | 不加 `--html` | 加 `--html` |
|---|---|---|
| 内联 `<svg>` | ❌ 被转义成 `&lt;svg` 源码，整页变成代码 | ✅ 原样输出 |
| 块级 `<div>` 包裹的分栏 | ✅ 正常渲染 | ✅ 正常渲染 |

所以：

- **deck 里有内联 SVG → 必须** `marp deck.marp.md --html --pdf --allow-local-files`。把这条命令写进 deck 顶部（frontmatter 之后的注释里），避免下次渲染忘。
- **纯文字 / 表格 / div 分栏的 deck → 不需要** `--html`。这类 deck 保持默认渲染路径，Obsidian 内置导出也能用。

> 早先版本的本 skill 写过「不用 `--html` 时 marp 不支持 div 布局」，这在 marp-cli v4.x 上不成立。div 两种模式都渲染，只有 SVG 需要开关。

## 2. SVG 三条铁律

这三条违反了都是**静默失败**——不报错，图就是不出来或变形。

| 铁律 | 后果 |
|---|---|
| **SVG 内部不能有空行** | markdown 在第一个空行处把 HTML 块切断，图形直接消失 |
| **每张图的 `marker` / `clipPath` id 必须唯一** | 导出合并 HTML（`--html` 单文件）时所有 SVG 共享一个 DOM，后面的 marker 全串到第一个定义上，箭头统一变成第一种颜色 |
| **SVG 内不写 `---`** | 仍被解析为分页符，这页裂成两页 |

**id 命名约定**：`a1` / `a2` / `a3`… 第 N 张图用第 N 组前缀。全文唯一即可。写图之前先数一下这是第几张。

## 3. 内联 SVG 的书写纪律

- **字号走 class，不写 `font-size` 属性。** deck frontmatter 的 `style:` 块已经定义了 `svg .t / .tb / .sm / .qt / .lbl`，改一处全篇图形同步缩放。写死 `font-size="26"` 就锁死了。完整 CSS 见 [../../style-bootstrap.md](../../style-bootstrap.md)。
- **贴底的图加 `<!-- _class: diagram -->`。** X 轴标题、图例、注脚很容易压到 footer（footer 绝对定位在 `bottom: 25px`）。`style-bootstrap` 里已含 `section.diagram footer { display: none; }`。
- **不要用 div 做图形布局。** 几何关系用 SVG 表达更直接；`--html` 之下 div 虽可用，但混用两套定位模型只会更难排查。
- **节点 ≤ 7。** 超过就拆页、聚合，或降级成表格。

## 4. 渲染器矩阵：谁能把内联 SVG 渲染进 PDF

内联 SVG 的可移植性**只取决于渲染器，不取决于文件**。同一份 `.md`，换个导出器结果就不同：

| 渲染器 | 屏幕 | 导出 PDF |
|---|---|---|
| Marp CLI + `--html` | ✅ | ✅ 矢量（标准路径） |
| Marp CLI 不加 `--html` | ❌ 整页源码 | ❌ |
| Obsidian 阅读模式 | ✅ | — |
| **Obsidian 内置 Export to PDF** | ✅ | **❌ 变成源码** |
| Obsidian + **Enhanced PDF Export** 插件 | ✅ | ✅ |
| 浏览器（导出 HTML 后 Ctrl+P） | ✅ | ✅ |

**如果 deck 在 Obsidian 里写、又用 Obsidian 内置导出，图形会变源码**——这是 Obsidian 导出器拍平 inline HTML 的已知问题，不是 deck 写错了。两个出路：

1. **继续用 Marp CLI 导出**（`--html --pdf`）。这是本 skill 面向的场景，源文件保持单文件内联。
2. **在 Obsidian 里换导出器**：[Enhanced PDF Export](https://github.com/cygnusyang/obsidian-enhanced-pdf-export)，它先经 preview renderer 渲染再打印，明确保留 inline SVG。源文件同样不用拆。

**不要**为了迁就某个导出器就把 SVG 拆成独立 `.svg` 文件——那会失去「源码和 Markdown 在一起」的最大好处（可搜索、可 diff、改一处全篇同步），而插件方案能保留它。

### 4.1 Obsidian 的 Marp 插件：导出命令缺 `--html`

Obsidian 的 [Marp 插件](https://github.com/JichouP/obsidian-marp)（v1.5.0）内置的三个导出动作（PDF / PPTX / HTML）**都不会传 `--html`**，所以内联 SVG 必然变源码。

插件的预览是好的（内置 `html = {br:[]}`，truthy），但导出时它把原始 markdown 写到 `~/Downloads/<name>.tmp`，再 shell out 给 marp-cli：

```bash
npx -y @marp-team/marp-cli@latest --stdin false --allow-local-files \
    --bespoke.transition -o ~/Downloads/<name>.pdf \
    --engine ~/Downloads/engine.js -- ~/Downloads/<name>.tmp
    #                                 ↑ 这里没有 --html
```

**修法：给这两处命令各加一个 `--html`。** 补丁点在 `.obsidian/plugins/marp/main.js` 的 `il()` 函数里，只有两处：

```bash
cd "<vault>/.obsidian/plugins/marp"
cp main.js main.js.bak                                    # 先备份
python3 - <<'EOF'
p = 'main.js'
s = open(p, encoding='utf-8', errors='surrogateescape').read()
s = s.replace('@marp-team/marp-cli@latest --',
              '@marp-team/marp-cli@latest --html --')
open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
EOF
node --check main.js && echo "syntax OK"                # 语法自检
```

改完**必须重载 Obsidian**（`Cmd+Shift+R`，或在插件设置里禁用再启用）才生效。

三点注意：

- `<!-- marp html: true -->` 全局指令和 frontmatter 里的 `html: true` **都无效**——`html` 是引擎构造参数，在解析 markdown 之前就定死了，只有命令行开关能用。
- 插件升级会覆盖补丁。每次升级后如果又变源码，重新打一次即可。
- 补丁文件若在坚果云 / iCloud 等同步目录里，会同步到其他机器；不想同步就把 `main.js.bak` 和补丁后的 `main.js` 排除掉，或改用 CLI 直接导出。

## 5. 陷阱速查

| 现象 | 原因 |
|---|---|
| 整页显示 SVG 源码 | 渲染命令漏了 `--html` |
| 图形完全消失 | SVG 内部有空行，HTML 块被切断 |
| 一页裂成两页 | SVG 内部写了 `---` |
| 所有图的箭头颜色一样 | `marker id` 重复，合并成单个 HTML 时全部串到第一个 |
| SVG 文字不认 CSS 类 | 类名写在了 SVG 内部 `<style>`；应写在 deck frontmatter `style:` 块里 |
| 改了字号四张图没同步 | SVG 里写死了 `font-size` 属性；应只用 class |
| X 轴标题 / 图例压住 footer | 给该页加 `<!-- _class: diagram -->` |
| 文字看不见（白字浮在空白处） | 箭头画成了空心 `>` 形，文字落在镂空区（见 [../skeletons/linear-sequence.md](../skeletons/linear-sequence.md)） |
| 箭头串文字整体偏移 | 按整个外框居中，应该按矩形部分居中（`x + 81` 而非 `x + 98`） |
| 图例不随图配色变 | 图例用了固定色值，没引用本图的主色 token |

## 6. 交付前必跑

```bash
node scripts/svg-lint.mjs deck.marp.md      # 确定性合规检查
marp deck.marp.md --html --images png -o check   # 渲染 PNG，肉眼逐页看
```

lint 抓「必然错」的（空行、`---`、id 冲突、坐标越界），PNG 抓「看起来对不对」的（重叠、错位、留白）。两步都不能省——**不要相信代码看起来对**。详见 [qa.md](qa.md)。
