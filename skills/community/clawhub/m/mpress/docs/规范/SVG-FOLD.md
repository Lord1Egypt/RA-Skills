# 公众号 SVG 折叠块：唯一实现说明

> 状态：2026-11-15 更新为 v4 紧凑版。双层裁切结构曾于 2026-11-13 真机确认可以正常弹开；v4 的展开、收起尚未单独做真机复测。  
> 适用范围：微信公众号图文正文里的「点一下展开 / 点一下收回」折叠块。  
> 一句话：**外层 `svg` 只负责高度动画和裁切，内层 `svg` 用固定比例承载内容；绝不能让内容跟着被改高度的视口重新缩放。**

---

## 0. 先看结论

正确的结构只有一种：

```text
外层 svg：无 viewBox，width:100%，height 从折叠高度动到展开高度，overflow:hidden
  └─ 内层 svg：width:100%，height = viewBox 高 ÷ viewBox 宽 × 100（单位 vw），viewBox 承载内容
```

错误的结构也只有一种典型：

```text
根 svg：带 viewBox，直接 animate height
```

后者在浏览器里可能看起来正常，但在真机微信里会退化成「整块图放大 / 缩小」，因为微信不认 `preserveAspectRatio`，高度一变就按默认 `meet` 重算整个 `viewBox` 的缩放。

---

## 1. 机制

### 1.1 为什么必须拆两层

旧写法：

```html
<svg viewBox="0 0 686 860" preserveAspectRatio="xMinYMin slice"
     style="width:100%;height:28vw;">
  <animate attributeName="height" begin="focusin" values="28vw;114.4vw" .../>
  <!-- 正文 -->
</svg>
```

它把「视口高度」和「内容坐标系」绑在同一个 `svg` 上。浏览器会按 `preserveAspectRatio="xMinYMin slice"` 保持内容比例，所以看起来是「多露一点」；真机微信表现上等价于这个属性不存在，默认 `meet` 会随着高度变化重新缩放整个 `viewBox`，于是变成了缩放。

新写法：

```html
<!-- 外层：只做高度动画和裁切，没有 viewBox -->
<svg tabindex="0"
     style="display:block;width:100%;height:28vw;overflow:hidden;background:#eef4f4;">
  <animate attributeName="height" begin="focusin"  values="28vw;125.4vw" .../>
  <animate attributeName="height" begin="focusout" values="125.4vw;28vw" .../>

  <!-- 内层：固定 width/height 比例 + viewBox，内容坐标系独立 -->
  <svg x="0" y="0" width="100%" height="125.4vw"
       viewBox="0 0 686 860">
    <rect width="686" height="860" fill="#eef4f4"/>
    <!-- 正文，按 686×860 的坐标排 -->
  </svg>
</svg>
```

- 外层没有 `viewBox`，高度变化不会被用来重算内容缩放。
- 内层 `width="100%"`、`height="125.4vw"` 固定了它自己的渲染尺寸；`viewBox` 只负责把 686×860 的坐标映射到这个固定尺寸。
- 外层 `overflow:hidden` 裁掉超出当前高度的部分；展开时只是把已经画好的内容多露出来。

### 1.2 关键约束

- 外层 `svg` **不能**有 `viewBox`。
- 内层 `svg` 的 `width/height` 比例必须和 `viewBox` 比例一致；否则 `meet` 会在内层再缩放一次。
- 内容只放在内层；不要在外层再放正文。
- 不要试图用 `animate attributeName="viewBox"` 来做折叠：草稿回读实测这个动画会被微信删掉（见 §6）。
- 不要用 `height:auto !important` 之类会覆盖外层高度的样式；发布态如果被微信补上 `!important`，高度动画会被压掉（见 §4、§7）。

---

## 2. 参数换算

### 2.1 公式

```text
展开高度（vw） = 内层 viewBox 高 ÷ 内层 viewBox 宽 × 100
折叠高度（vw） = 你希望折叠态露出的高度，建议落在两行文字之间
```

内层 `height` 也直接用这个展开高度：

```text
内层 height = 展开高度（vw）
```

### 2.2 算例

内容按 `viewBox="0 0 686 860"` 排：

```text
展开高度 = 860 ÷ 686 × 100 = 125.36 ≈ 125.4vw
内层 height = 125.4vw
折叠高度 = 28vw（示例；按你的首屏设计改）
```

在 390px 宽的 iPhone 上：

```text
展开高度 = 390 × 1.254 = 489px
折叠高度 = 390 × 0.28  = 109px
```

> 这里的 `vw` 以「移动端正文宽度 ≈ 视口宽度」为前提。微信正文如果有左右内边距，内层宽高比会有微小偏差；若展开后底部出现细白边，按正文实际宽度微调 `EXPANDED_VW`，或在目标客户端复测内层 `height:auto` 的写法。

如果内容改成 `viewBox="0 0 750 1200"`：

```text
展开高度 = 1200 ÷ 750 × 100 = 160vw
内层 height = 160vw
```

### 2.3 折叠高度怎么选

折叠高度决定「第一屏露到哪」。建议：

- 让裁切线落在两行文字之间，不要切在字形中间。
- 先排好内层文字，再量最后一行完全可见的 `y`，换算成 `vw` 后向上取整。
- 例：标题在 `y=120`、副标题在 `y=200`，`viewBox` 宽 686，则副标题底部约 `(200+30)/686×100 ≈ 33.5vw`，折叠高度取 `34vw` 更稳。

---

## 3. 触发源：焦点，不是 click

### 3.1 标准写法

- 外层 `svg` 加 `tabindex="0"`：点卡片 → `focusin` → 展开。
- 卡片下方放一行可聚焦的小字：`<p tabindex="0">点这一行收起</p>`；点它 → 卡片 `focusout` → 收起。
- 两个 `animate` 都绑在**外层 `svg`** 上：

```html
<animate attributeName="height" begin="focusin"
         values="28vw;125.4vw" dur="0.42s" fill="freeze" restart="whenNotActive"/>
<animate attributeName="height" begin="focusout"
         values="125.4vw;28vw" dur="0.30s" fill="freeze" restart="whenNotActive"/>
```

### 3.2 为什么不用 click 做同元素 toggle

微信会删 `id`，所以跨元素触发 `begin="otherId.click"` 直接不可用。没有跨元素引用时，同一个元素上的 `click` 只能做**单向**动画：

- `begin="click"`：第一次点展开，之后再点不会收回。
- `begin="click" end="click"`：同一次点击同时满足 begin 和 end，动画区间为零；WebKit 实测高度保持 `70→70`，等于没动。
- `<set begin="click" end="click">` 也一样，同一次点击立即结束。

焦点天然提供两个不同事件：`focusin` 和 `focusout`；再配一个可聚焦的收起目标，就能在不依赖 `id` 的情况下做同元素双向。代价是收起目标必须真的能获得焦点（必须是 `tabindex` 元素），否则 `focusout` 不触发。

> 触发源的可移植性：本次真机（用户手机）已确认 `focusin/focusout` 能触发；Android 未验证。如果 Android 上焦点不可靠，可以换成 135 的 `click` + `touchstart` + `<set visibility>` 冷却状态机，但**§1 的裁切几何不要变**。135 组件 129 的真实发布代码就是这套触发方式，可作为兜底参考（见 §9）。

---

## 4. 失败模式清单

对着现象查，不要先怀疑清洗。

| 现象 | 最可能的原因 | 怎么确认 | 修法 |
|---|---|---|---|
| 点下去整块图放大 / 缩小，高度数字也变了 | 根 `svg` 带 `viewBox`，直接 animate `height`；微信不认 `preserveAspectRatio`，按默认 `meet` 重算缩放 | 量隐藏区文字的 `getBoundingClientRect()`：折叠态和展开态的字号/坐标是否变化 | 改成 §1 的两层结构：外层无 `viewBox` 只裁切，内层固定比例 |
| 只能开一次，第二次点没反应 | 用了单向 `begin="click"`，没有收起触发 | 看有没有 `focusout` 或第二套收起动画 | 加 `tabindex` 收起目标 + `focusout` 动画；或换 135 双触发状态机 |
| 点了完全没反应 | 外层或收起目标没有 `tabindex`；`animate` 被删（例如 `attributeName="viewBox"`）；SVG 嵌套写错 | 草稿回读看 `animate`、`tabindex` 是否还在；浏览器里看 `focusin` 是否触发 | 只 animate `height/width/opacity/transform`；两个可点元素都加 `tabindex` |
| 展开后下方露出白板 | 外层展开高度 > 内层内容高度；内层 `height` 算小了 | 量内层 `getBoundingClientRect().height` 和外层展开高度 | 内层 `height` 用 `viewBoxH / viewBoxW × 100`（单位 vw），和外层展开高度一致 |
| 展开后正文被裁掉一截 | 外层展开高度 < 内层内容高度；比例四舍五入取小了 | 看最后一行是否完整 | 展开高度向上取整，或内层 `height` 直接用同一个值 |
| 折叠态文字被切一半 | 折叠高度落在字形中间 | 看裁切线是否穿过文字 | 折叠高度取两行之间，按 §2.3 重新算 |
| 收起后整块消失 / 留白 | 收起目标不可聚焦，`focusout` 没触发；或收起后外层高度为 0 | 看 `document.activeElement` 是否真的离开外层 `svg` | 收起目标必须是 `tabindex` 元素；给外层保留最小高度 |
| 发布后不折叠，草稿预览正常 | 发布态给外层 `svg` 补了 `height:auto !important`，高度动画被覆盖 | 对比草稿回读和已发布文章的外层 `style`；受控测试里 `height:70px !important` 会让 `animate height` 完全失效 | 避免依赖会被 `!important` 覆盖的高度；改用 135 的 `width`/`visibility` 状态机，或把高度动画放到不会被补样式的层级 |
| 微信里整个块不见 | 内层 `svg` 的 `width/height` 无效；外层没有高度；`style` 被清 | 草稿回读看 `svg`、`style`、`height` 是否在 | 用内联 `style`；内层给明确 `width="100%"` 和 `height="…vw"` |
| `preserveAspectRatio` 写了也没用 | 微信把属性名小写化，渲染链路不还原 / 不生效 | 草稿回读看到 `preserveaspectratio`；真机表现等价于默认 `meet` | 不依赖它：按 §1 拆两层 |

---

## 5. 验收判据

### 5.1 唯一判据：量内容元素，不量容器

在折叠态、展开态、再折叠态三次，取**隐藏区里的一行文字**（不是容器），记录：

```js
const r = el.getBoundingClientRect();
// 记录 x / y / width / height
```

通过条件：

- 三次的 `width`、`height`、`x`、`y` 完全一致（容差 ≤ 0.5px）。
- 折叠态截图里这行文字不可见；展开态可见；再折叠又不可见。
- 容器高度可以变，页面总高可以变，但**内容盒不能变**。

不通过的典型：

- 容器高度对了，文字盒从 `56.4×4.7` 变成 `230.6×18.7` —— 这是缩放，不是折叠。
- 浏览器/WebKit 里文字盒不变，真机变了 —— 说明模拟环境还原了 `preserveAspectRatio`，不能作为验收。

### 5.2 本次真实数值（样本）

WebKit iPhone 13 模拟，取展开区一行文字 `t4`：

| 状态 | 外层高度 | 文字盒 `w×h` | 文字 `x / y` |
|---|---|---|---|
| 折叠 | 109.2 | 254.7×20.3 | 22.7 / 407.8 |
| 展开 | 489.0 | 254.7×20.3 | 22.7 / 407.8 |
| 再折叠 | 109.2 | 254.7×20.3 | 22.7 / 407.8 |

Chrome（同一页面、同一坐标）：

| 状态 | 外层高度 | 文字盒 `w×h` | 文字 `x / y` |
|---|---|---|---|
| 折叠 | 109.2 | 255.5×24 | 22.7 / 405.1 |
| 展开 | 489.0 | 255.5×24 | 22.7 / 405.1 |
| 再折叠 | 109.2 | 255.5×24 | 22.7 / 405.1 |

失败样本（旧结构，去掉 `preserveAspectRatio` 模拟微信）：

| 状态 | 外层高度 | 文字盒 `w×h` |
|---|---|---|
| 折叠 | 109.2 | 56.4×4.7 |
| 展开 | 446.2 | 230.6×18.7 |

这就是「高度数字全对，肉眼是缩放」的量化样子。

### 5.3 截图

原截图（`design/2026-11-13/wechat-svg-toggle/work/fold-clip-*.png`）已丢失，仓库内没有现存副本，不再保留链接；数值结论见 §5.2。

### 5.4 可复跑的量测

原量测脚本与可交互原型（同目录下的 `fold-clip-focus*.cjs` / `fold-clip-focus.html`）已丢失。需要复核时按 §5.1 重新量隐藏区文字：分别在折叠、展开、再折叠三态取 `getBoundingClientRect()`，内容盒的 `x / y / width / height` 必须不变。

---

## 6. 微信清洗后保留什么、删什么

以下分「草稿回读实测」和「行为推断」，不要把推断写成实测。

### 6.1 草稿回读实测：保留

- `tabindex`（外层 `svg` 和收起 `p` 都保留）
- `begin="focusin"` / `begin="focusout"`
- `<animate attributeName="height">`（`attributename`/`attributetype` 会被小写化，但动画保留）
- `vw` 数值（如 `125.4vw`）
- 内联 `style` 里的 `display/width/height/overflow/background/outline`
- `overflow:hidden`
- 嵌套 `<svg>` 结构和内层 `viewBox`（`viewbox` 小写化，但保留）

实测文件的原始回读（`design/2026-11-13/wechat-svg-toggle/work/probe*.html`）已丢失，不再保留链接。现存可查的证据是 `.generated/wechat-publisher/chaodraft/`（「抄」草稿回读）和样例稿的最近一次渲染结果。

### 6.2 草稿回读实测：删掉 / 失效

- `id`：被删；`url(#...)` 会变成断引用
- `href="#..."`：被删；`draft/add` 会返回 45166
- `<style>`：整段消失
- `<details>`：被剥成裸 `<summary>`，展开语义消失
- `<input>`：被删；`label` 还在但没有作用对象
- `<button>`：被剥成纯文本
- `<textarea>`：被删
- 事件属性：`onclick` 等被删
- `<animate attributeName="viewBox">`：被删（普通写法和自闭合写法都删）

### 6.3 实测的属性名变化

草稿回读里 SVG 属性名会被统一小写：

```text
viewBox              → viewbox
preserveAspectRatio  → preserveaspectratio
attributeName        → attributename
attributeType        → attributetype
```

浏览器 HTML 解析会按规范还原 camelCase；微信的渲染链路没有让它生效——这是**行为推断**，证据是真机表现等价于默认 `meet`，以及回读里属性名小写化。不要把它写成「微信源码里确认删除了这个属性」。

### 6.4 发布态风险（未完全验证）

已发布文章的 HTML 里能看到微信给部分 `svg`/图片补：

```text
max-width:100% !important;
height:auto !important;
```

受控测试里，`height:70px !important` 会让 `animate height` 完全失效（高度保持 70）。本次真机测试的高度能变，说明这一版没有被补上；但发布态是否补、补在哪个层级，仍需用真实发布文章确认。若被补上，§4 的「发布后不折叠」就是对应失败模式。

---

## 7. 真机验证记录

- **日期**：2026-11-13
- **设备**：用户真机（本次记录未标注具体型号 / 系统；下次预览时补记机型、系统版本、微信版本）
- **旧结构结论**：根 `svg` + `viewBox` + `preserveAspectRatio` + `vw` 高度 + `focusin/focusout`，真机点下去是**整块图放大又缩小**，高度数字 `109 → 446 → 109`，但视觉不是折叠。说明触发可用，几何不可用。
- **新结构结论**：用户真机确认**可以正常弹开**。
- **本次未单独复述的部分**：新结构的「再点收起」动作未在真机上单独记录；收起使用同一个 `focusout` 机制，旧版真机收起是正常的，下次预览时顺手确认。
- **对比稿**：草稿箱标题「【真机对比】旧缩放 vs 新裁切折叠（请勿群发）」，`media_id`：

```text
G-yr1Pkv1u1PH3jQbF_O_WFPpo5Kg0AeKu6QgGn9MA98254wimoZf0v-GFh8cUcY
```

### 未验证

- Android 微信（焦点触发、`vw`、嵌套 SVG 的渲染差异）。
- 桌面微信宽窗口（宽度变化时 `125.4vw` 的比例是否仍成立）。
- 发布态样式归一化（`height:auto !important` 是否补到外层 `svg`）。
- 不同字号、行高、超长正文、图片混排下的折叠高度取整。
- 快速连点、滚动中点击、键盘弹出/收起对焦点的影响。

---

## 8. 最小可复用片段

片段文件：

[../../../skills/wechat-article/assets/wechat-svg-fold.html](../../../skills/wechat-article/assets/wechat-svg-fold.html)

片段里用占位符标出必须替换的位置，并在注释里写了公式和验收提醒。生成文章时直接复制，替换：

- `{{VIEWBOX_W}}` / `{{VIEWBOX_H}}`
- `{{EXPANDED_VW}}` / `{{COLLAPSED_VW}}`
- `{{TITLE}}` / `{{EXPAND_LABEL}}`
- `{{SUMMARY_LINE}}`：details 替换为空；fold 有摘要时才注入一行
- `{{BODY_LINES}}`

颜色、字号、双热区和收起提示已经固定在模板与 `theme.css` 中，不另开占位符。

---

## 9. 参考

- [135 组件 129：无限点击展开+点击收回（首图变化）](https://www.135editor.com/svg_templates/lists.json?id=129)
- [135 组件 129 的真实案例文章](https://mp.weixin.qq.com/s/Y3BzLcnQ3LZuX0qM52UmZg)

> 原「96 编辑器说明、旧结构复现页、clip 原型、三份草稿回读」的本地文件已丢失，链接已移除。需要复现时按 §1 的结构和 §5.1 的判据重新搭。

---

## 10. 「抄」草稿的结构记录（2026-11-13）

「抄」是**草稿**，不是已发布文章；先前「抄」「抄2」两篇在清空草稿箱时被删且不可恢复，用户随后重新存了一篇同名「抄」。以下只记录 `draft/get` 回读到的原文，不做推断。

- 来源：`draft/batchget` + `draft/get`，media_id `G-yr1Pkv1u1PH3jQbF_O_a0wC3TtbaGZ04LTYAq3GSWkHhhOuSlkF4sjNvXGvYXL`
- 落盘：`.generated/wechat-publisher/chaodraft/article-0.html`（8009 字符）
- 规模：6 个 `<svg>`、4 个 `<animate>`、1 个 `<set>`、0 个 `id`、0 个 `<style>`

### 10.1 原文里真实写着的属性

| 项 | 原文 |
| --- | --- |
| 外层承载 | HTML `<section style="display:inline-block;width:100%;overflow:hidden">`；内层 `height:0px;overflow:visible` |
| 动画元素 | 主 `<svg viewbox="0 0 1022 216" style="pointer-events:none">`，无 height 属性 |
| 展开 | `opacity` 1→0，`begin="click"`，0.1s；`width` 100%→612.7453824581763%，`begin="click + 0.1s"`，0.4s，均 `fill="freeze"` |
| 收起 | `width` 612.745…%→100%，`begin="touchstart"`，0.4s；`opacity` 0→1，`begin="touchstart+0.4s"`，0.1s |
| 热区 | `<g opacity="0">` 内两块 `rect pointer-events="visible"`：全幅一块；小热区 `x=106.21% y=84.7% w=3.9% h=15.13%`（在 1022 宽视口之外） |
| 第二次点击 | 两条 `animatetransform type="translate"`：`begin="click"` 时 `values="-9999 0; -9999 0; -1022 0"`，`begin="touchstart"` 时 `values="-9999 0; -9999 0; 0 0"`；均 `dur=0.4/0.5s`、`fill="freeze"`、`keytimes="0;0.99;1"`、`calcmode="discrete"`，即整组热区被移出命中范围再移回 |
| 状态互斥 | 另有一个 `opacity="0" pointer-events:none` 的叠层 svg，`<g>` 内有 `<set attributename="visibility" to="hidden" begin="touchstart" dur="0.21s" fill="remove">` 与一条 `values="20000 20000;20000 20000" begin="touchstart" dur="0.21s" fill="remove" restart="always"` |
| pointer-events | 命中层 `pointer-events="visible"`；根 svg、图片层、foreignObject 全部 `pointer-events:none` |
| 清洗结果 | 属性名小写：`animatetransform` / `attributename` / `keytimes` / `calcmode` / `viewbox` / `foreignobject` |

### 10.2 与本站实现的差异

1. 它展开的是 **width**，内容是 `foreignObject` 里 `background-image` 的预渲染 PNG 海报；本站要放可选中的真文字，只能动 **height** 并用两层裁切。
2. 它的外层是 HTML section 的 `overflow:hidden` + `height:0/visible`；本站沿用 §1 的外层 svg 无 viewBox + 内层固定比例。
3. 它把开/关分别绑在 click / touchstart 上，但两者都挂在同一个主 svg 上，靠两块热区 + 热区平移做路由；height 只能挂在外层 svg 上，click 与 touchstart 在同一次点击里都会冒泡到同一个元素，无法做出可反复的双向。
4. 因此本站保留它的**双热区**模型（这点是它能用的原因，不是代价），触发改用真机已验证的 `focusin` / `focusout`：热区 A = 卡片，热区 B = 卡片底部一行。单点焦点合并做不到反复，不要再往那个方向改。
5. 样式约束（用户 2026-11-13 补充）：**圆角按主题保留**，折叠块用 6px（与 `theme.css` 的 `pre` 同半径），不要照搬「抄」的直角。
6. vw 换算补了正文宽度系数：`EXPANDED_VW = H ÷ W × 100 × 0.92`，`COLLAPSED_VW = collapsedHeight ÷ W × 100 × 0.92`；v4 中 details 的 `collapsedHeight=64`，有摘要的 fold 为 `100`。0.92 是「正文宽 ÷ 视口宽」的近似，避免展开后底部留白或多露一行。
7. CSS 内联工具会用根选择器覆盖元素上的行内样式：折叠块的收起行和 svg 必须挂类名（`.wx-fold-hint` / `.wx-fold-outer` / `.wx-fold-inner`），样式写在 `theme.css`；高度只写在 `height` 属性上，由 `restoreSvgHeight` 去掉内联的 `height:auto`。

### 10.3 已推送的完整样例稿

- 标题：`把长文排成一张纸`（同一篇草稿，`draft/update`，未新建）
- media_id：`G-yr1Pkv1u1PH3jQbF_O_f2B-l9M4-irHW-D7XR-WbreLpQ7zvBFw_vLEcDB3kk6`
- 覆盖：篇章标题 H1、章节页签 H2、小节 H3、导语、正文与强调、有序/无序/嵌套列表、四种提示块（TIP / NOTE / WARNING / IMPORTANT）、短引与带出处长引、行内代码、带语言标签的代码块、表格、通栏图与图注、分割线、3 个折叠块、收束块、签名。
- 回读确认：6 个 svg、6 个 animate、6 个 tabindex、0 个 id；组件样式随类名内联后仍然存在。
- 实现备忘：原生 `<pre>` 在部分渲染器中会被注入额外色块，代码块统一改用 `<section class="wx-pre">` + 每行一个 `<p class="wx-pre-line">`；`<p>` 与 `<svg>` 上的行内样式会被根规则覆盖，组件样式必须挂在类名上写进 `theme.css`。

---

## 11. 折叠块 v4 规格（2026-11-15 紧凑化）

v4 的目标是减少收起态占高，并让两个提示贴近各自的动作区域。双层 SVG、双热区和 `focusin/focusout` 机制不变。

### 11.1 details 与 fold 的内容边界

1. **`:::details[标题]` 只保留粗标题和正文**：不生成空摘要，不收起态第二行，不加竖条、发丝线、编号或行数。
2. **` ```fold 标题｜摘要 ` 可以保留摘要**：只有源稿确实给出摘要时，才在标题下显示第二行。
3. 正文只在内层 SVG 中按固定行高排布；收起时由外层裁切，展开时不重新缩放文字。

### 11.2 两处提示的位置与样式

- **点击展开 ↓**：放在标题同一行的最右侧，20 号 / `#007275`，右对齐到 x=662。不再独占一行。
- **点击收起 ↑**：放在卡片正文之后的 HTML 收起行，11px / `#007275`，右对齐，底内边距 10px，不描边、不加图标或独立大色块。
- 两个提示使用方向相反的箭头，动作只讲一件事。禁止「点开阅读全文」、行数计数和一行同时解释两个热区。
- 双热区仍是卡片与底部收起行。底部 p 是第二个焦点目标，当前机制下常驻；只用小字号和右对齐降低存在感，不新增未经微信验证的显隐方案。
- SMIL 的 `focusin` 不能可靠驱动子元素显隐，因此卡片内的展开提示也不做显隐动画。

### 11.3 几何与公式（v4）

| 项 | details | 有摘要的 fold |
| --- | ---: | ---: |
| 标题基线 / 字号 / 字重 | 44 / 30 / 700 | 44 / 30 / 700 |
| 展开提示基线 / 字号 | 42 / 20 | 42 / 20 |
| 摘要基线 / 字号 | 不生成 | 84 / 24 |
| 正文首行基线 `firstY` | 106 | 142 |
| 正文行高 / 字号 | 44 / 27 | 44 / 27 |
| 收起高度 `collapsedHeight` | 64 | 100 |
| 内层高度 `viewBoxH` | `106 + (行数 - 1) × 44 + 30` | `142 + (行数 - 1) × 44 + 30` |

换算统一为：

```text
EXPANDED_VW = viewBoxH ÷ 686 × 100 × 0.92
COLLAPSED_VW = collapsedHeight ÷ 686 × 100 × 0.92
```

details 的裁切线 64 位于标题之下、正文首行字顶之前；fold 的裁切线 100 位于摘要之下、正文首行字顶之前。替换占位符后必须过滤空行，否则空摘要会截断 Markdown 的 HTML 块。

### 11.4 落盘位置

- 模板：`skills/wechat-article/assets/wechat-svg-fold.html`
- 样式：`skills/wechat-article/assets/theme.css`（`.wx-fold-outer` / `.wx-fold-inner` / `.wx-fold-hint`）
- 视觉规范：`docs/wechat/规范/VISUAL-SYSTEM.md` C13
- 本文件 §1–§9 是结构原理，§11 是 v4 的可执行规格；两者冲突时以 §11 为准。
