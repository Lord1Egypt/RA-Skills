# 微信公众号 CSS 兼容性约束

> 本文档基于实际推送验证（2026-08-14/15/20/21），通过 draft/get 回读 + Headless Chrome 渲染截图对比确认。
> 2026-08-21 更新：补充 flex 子属性行为说明，修正 display:flex 条目。

## 微信渲染器会静默丢弃的 CSS 属性

以下属性在微信草稿存储层（draft/add → draft/get）100% 无损保留，但**微信文章渲染器会直接忽略**，不产生任何视觉效果：

| 属性 | 状态 | 替代方案 |
|------|------|----------|
| `border-radius` | ❌ 忽略 | 用纯色边框代替，接受直角 |
| `box-shadow` | ❌ 忽略 | 用 `border` 代替 |
| `text-shadow` | ❌ 忽略 | 用 `color` / `font-weight` 代替 |
| `linear-gradient` | ❌ 忽略 | 用纯色 `background` 代替 |
| `radial-gradient` | ❌ 忽略 | 同上 |
| `letter-spacing` | ❌ 忽略 | 无替代，接受默认字间距 |
| `opacity` | ❌ 忽略 | 用 `rgba` 代替（但 rgba 也可能被剥） |
| `rgba()` | ⚠️ 部分 | alpha 通道被丢弃，颜色变实色 |
| `background-clip` | ❌ 忽略 | 无 |
| `text-fill-color` | ❌ 忽略 | 无 |
| `backdrop-filter` | ❌ 忽略 | 无 |
| `filter` | ❌ 忽略 | 无 |
| `transition` | ❌ 忽略 | 微信文章无动画 |
| `animation` | ❌ 忽略 | 同上 |
| `transform` | ❌ 忽略 | 同上 |

## Flexbox / Grid 子属性（关键修正）

> 2026-08-21 实测确认：`display: flex` 虽然在存储层保留，但微信渲染器**不执行 flexbox 布局**。
> 子元素会塌陷为普通 block 流，所有 flex 子属性完全无效。

| 属性 | 状态 | 说明 |
|------|------|------|
| `display: flex` | ⚠️ 保留但不渲染 | 存储无损，但渲染器按 block 处理，子元素不会横向排列 |
| `display: inline-flex` | ⚠️ 同上 | 同 flex |
| `display: grid` | ⚠️ 同上 | 同 flex |
| `flex` (shorthand) | ❌ 忽略 | `flex: 1` 不生效，子元素不自动填充 |
| `flex-shrink` | ❌ 忽略 | 不生效 |
| `flex-grow` | ❌ 忽略 | 不生效 |
| `flex-basis` | ❌ 忽略 | 不生效 |
| `flex-direction` | ❌ 忽略 | 不生效 |
| `justify-content` | ❌ 忽略 | 不生效 |
| `align-items` | ❌ 忽略 | 不生效 |
| `align-self` | ❌ 忽略 | 不生效 |
| `align-content` | ❌ 忽略 | 不生效 |
| `gap` | ❌ 忽略 | 不生效 |
| `row-gap` | ❌ 忽略 | 不生效 |
| `column-gap` | ❌ 忽略 | 不生效 |
| `grid-template-columns` | ❌ 忽略 | 不生效 |
| `grid-template-rows` | ❌ 忽略 | 不生效 |

**替代方案**：使用 `<table>` + `<td>` 实现多列布局（border-collapse: collapse/separate），这是微信渲染器最稳定的布局方式。

## 微信渲染器支持的 CSS 属性

以下属性经实测确认在微信渲染器中正常工作：

| 属性 | 状态 | 备注 |
|------|------|------|
| `color` | ✅ 支持 | |
| `background` / `background-color` | ✅ 支持 | 仅纯色，不含渐变 |
| `font-size` | ✅ 支持 | |
| `font-weight` | ✅ 支持 | |
| `font-family` | ✅ 支持 | |
| `line-height` | ✅ 支持 | |
| `text-align` | ✅ 支持 | |
| `margin` | ✅ 支持 | |
| `padding` | ✅ 支持 | |
| `border` | ✅ 支持 | |
| `border-left` / `border-top` 等 | ✅ 支持 | |
| `display` | ✅ 支持 | `block` / `inline` / `inline-block` / `none`（flex/grid 值不渲染为弹性布局） |
| `vertical-align` | ✅ 支持 | table cell 中使用 |
| `max-width` | ✅ 支持 | |
| `width` / `height` | ✅ 支持 | |
| `word-break` | ✅ 支持 | |
| `white-space` | ✅ 支持 | |
| `position` | ⚠️ 有限 | `relative` 可用，`absolute`/`fixed` 不稳定 |

## 关键教训

1. **存储层 vs 渲染层**：微信 draft/add API 存储 HTML 时 100% 无损（所有内联 style 原样保存），但前端渲染器有独立 CSS 过滤层
2. **草稿删除导致图片失效**：草稿删除后，其引用的 mmbiz.qpic.cn 图片 URL 会失效，不可复用
3. **每次推送必须重新上传图片**：即使 Markdown 中已有 mmbiz URL，也必须重新上传本地图片获取新 URL
4. **headless Chrome 验证法**：用 `--headless --screenshot` 渲染对比本地 HTML 和 draft/get 回读 HTML，可确认存储无损
5. **flex 不是布局方案**：微信渲染器保留 `display:flex` 但不执行 flexbox 引擎。列表/多列布局必须用 `<table>` 代替
6. **converter.py 已内置清洗**：`_sanitize_style()` 会自动剥离所有 UNSAFE_CSS_PROPS 中的属性，并将 `display:flex/grid` 替换为 `display:block`
