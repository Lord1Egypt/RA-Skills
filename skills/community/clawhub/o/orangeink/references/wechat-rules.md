# 微信公众号合规规则与坑位表（wechat-rules）

> 来源：微信官方《编辑器插件开发规范》+ wechatjs/verify-article-structure-spec（MIT，规则权威定义）。以下为橙墨管线处理的规则摘要，**改样式逻辑前必读**——每条都是实战踩出来的。

## 平台检测规则（会弹「结构异常」）

| 规则 | 官方章节 | 坑与修法 |
|------|----------|----------|
| 行高叠字（旧口径） | 2.3.2 | 行数 = 元素高度 ÷ `parseFloat(line-height)`。无单位 `1.8` 被当 1.8px → 误判。**行高一律输出 px**（`line-height:28.8px`） |
| 行高叠字（实测口径） | 2.3.2 | `Range.getClientRects()` 把**一行里每个行内片段**各算一个矩形 → 段落里有 `**加粗**` 必然误报。**修法：所有直接文本节点包 `<span leaf>`**（官方兜底分支只查「有直接文本子节点」的块）。⚠️ 不要为精简 HTML 删掉 `wrapTextRuns` |
| li 顶层行内拆行 | 实测 | 微信粘贴解析把 li 顶层的行内兄弟节点拆进块级 section → 加粗起头的 li 被强制换行。**修法：纯行内 li 整包 `<section style="margin:0;…">`**（`wrapLiSections`，须在 wrapTextRuns 之前跑） |
| text-align | 2.6 | `start`/`end` 是违禁值。净化时 `start→left`、`end→right`。**只查内联显式设置**（computed 对默认值返回 start，会全量误报） |
| font-family | 4 | 官方白名单只有一条链 `"mp-quote", PingFang SC, system-ui, -apple-system`，**内联 font-family 不以它开头即违规**（连 `serif` 都算）→ 正文完全不输出 font-family |
| 嵌套层级 | 3.1 | 同标签+同样式连续嵌套 ≤15 层（2026-09 从 10 放宽），超了自动删节点 |
| 固定宽度 | 2.4 | width >677px 溢出安全区 |
| pre 滥用 | 2.8 | 普通长段落不用 `<pre>` |
| 空标签剥离 | 实测 | 分割条是无内容的 span，粘贴后被删。**修法：条内塞 `&nbsp;`** + `font-size:4px;line-height:4px;overflow:hidden`（不撑行框、过叠字检测） |
| div 样式剥除 | 实测（2026-10-14，haitang 主题首发回归） | 渲染输出中的 `<div>` 粘贴公众号后样式不可控——顶层 div 被剥样式（刊头全崩），嵌在 section 卡片内的 div 侥幸保留。**修法：渲染输出一律 section/span/p，禁用 div**（判别特征：渲染字符串 div 必带 `style=`，页面 UI 框架 div 不在此列） |
| 复制污染 | 实测 | `execCommand('copy')` 走 annotate-for-interchange 会把页面计算样式（text-align:start、font-family、orphans/widows…）写进剪贴板。**修法：copy 事件里 `clipboardData.setData` 自建 HTML + 先净化**（渲染器输出已是净化后字符串，复制页按钮同样走此路径） |

## 质量规则（不拦发布，自检按 warn 报）

- **WCAG AA 对比度**：文字 vs 最近背景 ≥4.5:1（大字 ≥3:1）。橙墨四主题全过；自造配色必须先算对比度
- **表格列数**：>4 列手机端挤压
- **加粗/斜体未生效**：`**` 紧贴中文标点（引号/书名号/「」/句号）开收失败残留裸星号 → 标点移出标记、`**` 前加空格、或整句独立成行

## 微信粘贴解析的已知行为（写草稿时绕开）

1. `<a href="#anchor">` 锚点被过滤 → 脚注用「上标编号 + 文末参考块」形态
2. 外链图片在 API 路径被过滤（draft/add）；复制粘贴路径会尝试转存
3. CSS `nth-child`/`:last-child` 不可用 → 斑马纹写内联、末元素 margin 在 DOM 里直接清零
4. `#RRGGBBAA` 支持不可控 → 透明度一律输出 `rgba()`
5. flex/grid 不保证 → 模块内部用 table/section 布局

## 官方规则源（跟进规则变化时核对）

- 规范：https://developers.weixin.qq.com/doc/subscription/guide/product/plugin_spec.html （章节号会随改版变化，按规则内容比对）
- 校验仓库：https://github.com/wechatjs/verify-article-structure-spec （基线 0.2.16）
