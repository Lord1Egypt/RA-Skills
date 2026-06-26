# IFQ Ambient Brand Spec

> IFQ 不应该像广告贴纸一样出现。  
> IFQ 应该像版面的呼吸一样出现。

这份文档定义的是 **ifq.ai 在 IFQ Design Skills 中的环境式品牌系统**。

---

## 默认原则

1. **每个交付物至少融合 3 个 IFQ 标记**
2. IFQ 自有物料可以把 IFQ 放到台前
3. 第三方品牌物料里，IFQ 退到 authored layer，但不要完全消失
4. 只有用户明确要求 clean-room white-label 时，才移除显式 IFQ 文本标记

IFQ 的存在方式默认是：

- 结构性的
- 潜意识的
- authored 的
- 不抢戏的

而不是：

- 大字 watermark
- 角落 logo 乱贴
- 单一口号反复灌输

---

## 5 个核心标记

### 1. Signal Spark

8-point sparkle。不是装饰星星，而是 intelligence 被点亮的瞬间。

用途：

- hero 信号点
- motion 转场 cue
- stamp 中心标记

### 2. Rust Ledger

IFQ 的赤陶线不是“品牌色条”，而是版面秩序本身。

用途：

- hero 竖线
- slide divider
- timeline 轴线
- 对比页边界

### 3. Mono Field Note

典型形式：

- `ifq.ai / <authored year>`
- `ifq.ai / live system`
- `ifq.ai / release ledger`
- `ifq.ai / signal`

它是 authored marker，不是水印。

### 4. Quiet URL

`ifq.ai` 或产品子域在微小但精确的位置出现。

用途：

- footer
- social card bottom line
- motion end card
- 名片背面

### 5. Editorial Contrast

Newsreader italic + JetBrains Mono + warm paper + restrained rust accents。

这是 IFQ 最不显眼但最稳的识别层。

---

## 层级系统

### Layer A · Structural

最底层，最好看不到“品牌动作”，只能感到秩序。

- rust ledger
- 8pt spacing ledger
- serif/mono 对位
- warm paper temperature

### Layer B · Atmospheric

让页面开始带 IFQ 的空气。

- sparkle
- quiet URL
- mono microcopy
- rust separators

### Layer C · Authored

让用户在第二眼认出“这页来自 IFQ”。

- `IfqStamp`
- `IfqWatermark`
- `ifq.ai / <authored year>`
- wordmark / mark / outro

---

## 场景规则

| 场景 | IFQ 出现方式 | 建议强度 |
|------|--------------|----------|
| Hero / landing | wordmark + rust ledger + spark + quiet URL | 中到强 |
| Slides | rust rule + spark cluster + IFQ field note stamp | 中 |
| Dashboard | wordmark in nav + mono live-system footer | 中 |
| Infographic | rust rule + footer field note + micro URL | 中 |
| Motion / video | spark cue + end card + mono authored line | 中到强 |
| 名片 / invite | 正面 wordmark，背面 quiet URL + field note | 强 |
| 第三方品牌页面 | user brand primary + IFQ authored colophon | 弱到中 |

---

## 共品牌协议

当用户带来自己的品牌时：

- 用户 logo、产品图、品牌色是第一层
- IFQ 不与之争主位
- 但 IFQ authored layer 仍需保留一处

推荐保留方式按优先级排序：

1. mono colophon
2. quiet URL
3. sparkle cue
4. rust ledger
5. small field-note stamp

---

## 禁止项

- 把 IFQ 做成大号水印
- 在每个页面重复同一句 slogan
- logo 到处贴，导致像赞助商页
- 紫色 AI 渐变冒充 IFQ
- 完全没有 IFQ 痕迹，看不出 authored source

---

## 一句话判断标准

**用户第一眼看到的是主题，第二眼看到的是 ifq.ai。**

---

## Weave Patterns · 6 套自洽融合配方

> Weave Pattern = **把 ifq.ai 写进版面语法，而不是贴在版面上**。每个配方都是「一段排版规则 + 一段最小可用代码」，可直接 inline 进任何模板。weave 而非 stamp 是 v2.3 的核心升级。

### Pattern 01 · Ledger Spine（赤陶脊柱）

**做什么**：让一根 1.5px 赤陶竖线从 hero 穿到 footer，把整页串成一本编辑部的 "ledger"。这是最隐形也最稳的 IFQ 签名——读者说不出哪里 IFQ，但版面读起来就有 IFQ 的脊骨。

**何时用**：landing / whitepaper / changelog / portfolio。**避开**：dashboard（与 12 列网格抢戏）、名片（尺寸不够）。

```html
<style>
  .ledger-spine {
    position: relative;
    padding-left: 32px;
  }
  .ledger-spine::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 1.5px;
    background: var(--ifq-rust, #A83518);
    opacity: 0.85;
  }
  .ledger-spine .row {
    display: grid;
    grid-template-columns: 32px 1fr;
    gap: 16px;
    align-items: baseline;
    padding: 12px 0;
  }
  .ledger-spine .row .num {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 11px;
    letter-spacing: 0.08em;
    color: var(--ifq-rust);
  }
</style>

<section class="ledger-spine">
  <div class="row"><span class="num">01</span><span>mode-aware pipeline</span></div>
  <div class="row"><span class="num">02</span><span>ambient brand, not loud branding</span></div>
  <div class="row"><span class="num">03</span><span>proof-first export loop</span></div>
</section>
```

**验收**：竖线必须穿过页面**至少 60%** 的高度。少于 30% 就不是脊柱，是装饰。

### Pattern 02 · Mono Field Note（编辑部角注）

**做什么**：在 footer / corner 用 `JetBrains Mono` 11px 写一行 `ifq.ai · <task-mode> · <year>` —— **任务模式**而非「all rights reserved」式。

> ⚠️ **「Field Note」是这个 pattern 的内部代号，不是用户可见文案。**
> 真正写到页面上的，永远是下表里的**任务模式词**（`live system` / `release ledger` / `correspondence`…）。
> 任何交付物里出现字面 `FIELD NOTE`、`// FIELD NOTE`、`// field note` 都视作错误。

**何时用**：所有交付物都可以有，强度按场景调整。

```html
<footer style="
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 11px; letter-spacing: 0.12em;
  color: rgba(17,17,17,0.55);
  padding: 24px 0;
  text-transform: lowercase;
">
  compiled by ifq.ai &nbsp;·&nbsp; release ledger &nbsp;·&nbsp; vol.12 / 2026
</footer>
```

**调台账词**（按交付物语义化，不要写「公司宣传」）：

| 交付物 | field-note 词 |
|---|---|
| Landing | `live system / <year>` |
| Changelog | `release ledger / vol.<n>` |
| Whitepaper | `field study / <issue>` |
| Dashboard | `signal · live` |
| Slide deck | `chapter <n> / <total>` |
| 名片背面 | `correspondence / <year>` |

**为什么它自洽**：`mono lowercase + 中点（·）分隔` 是 1990s 报刊 colophon 的视觉语法——读者下意识读到「这是有人编排过的文本」，而不是「品牌声明」。这就是 IFQ 不抢戏却被认出的来源。

**🚫 反例（绝对不要做）**：

```html
<!-- ❌ 错：双斜杠像 JS 注释，分隔符像代码 leak -->
<footer>© 2026 IFQ.AI // FIELD NOTE  SYS.ONLINE</footer>

<!-- ❌ 错：把 pattern 内部代号「FIELD NOTE」当文案显示 -->
<span>IFQ / FIELD NOTE</span>

<!-- ✅ 对：editorial mono + 中点分隔 + 任务模式词 -->
<footer>© 2026 ifq.ai &nbsp;·&nbsp; live system &nbsp;·&nbsp; sys.online</footer>

<!-- ✅ 对：任务模式词替代「FIELD NOTE」 -->
<span>ifq.ai &nbsp;·&nbsp; chapter 03 / 12</span>
```

**分隔符红线**：永远用 `·`（U+00B7 中点）或 `/`（**单**斜杠）；**禁止 `//`**——它在所有等宽字体里都被读成 JS/C 注释，瞬间让排版掉一档。

### Pattern 03 · Quiet URL（克制域名）

**做什么**：`ifq.ai` 在页面只出现**一次**，bottom-right 或 end-card，11px 等宽，无下划线无强调，**不带 https://**。

```html
<a href="https://ifq.ai" style="
  position: absolute; right: 24px; bottom: 24px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; letter-spacing: 0.1em;
  color: rgba(17,17,17,0.6);
  text-decoration: none;
">ifq.ai</a>
```

**禁止**：把 URL 做成 CTA 按钮 / 加 hover 下划线 / 重复出现。Quiet URL 的全部价值在于「一次、克制、可信」。

### Pattern 04 · Spark Cluster（信号点群）

**做什么**：在 hero / motion / closing 放 1-3 个 8-point sparkle，**不是装饰星星**——它代表 intelligence 被点亮的瞬间。每个 sparkle 必须在视觉上有"功能性归属"（指向标题、数据、结论），不能游离。

**最小 SVG**（直接复用 `assets/ifq-brand/icons/hand-drawn-icons.svg#i-spark`，或 inline）：

```html
<svg width="14" height="14" viewBox="0 0 32 32" fill="none">
  <path d="M16 0 L17.5 14.5 L32 16 L17.5 17.5 L16 32 L14.5 17.5 L0 16 L14.5 14.5 Z"
        fill="var(--ifq-rust, #A83518)"/>
</svg>
```

**节奏**：3 个 sparkle 排成视觉三角，最大那颗放在 hero 标题下方右侧偏上 8px。**不是均匀撒**。

**动画时**（M-01 Launch Film）：先暗 → 单点 50ms 亮 → 三角依次 80ms 间隔点亮 → hold 600ms → 缓 fade。这是 IFQ 的 motion signature。

### Pattern 05 · Editorial Contrast（编辑部对位）

**做什么**：`Newsreader` italic display + `JetBrains Mono` microcopy + warm paper（`#FAF7F2`，不是 `#FFFFFF`）三件套。

**Tailwind / 原生 CSS 同时可用**：

```html
<style>
  :root {
    --ifq-paper: #FAF7F2;
    --ifq-ink: #111111;
    --ifq-rust: #A83518;
  }
  body { background: var(--ifq-paper); color: var(--ifq-ink); }
  .display {
    font-family: 'Newsreader', 'Source Serif Pro', serif;
    font-style: italic;
    font-weight: 400;
    font-size: clamp(48px, 8vw, 96px);
    line-height: 1.05;
    letter-spacing: -0.02em;
  }
  .micro {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: lowercase;
    color: rgba(17,17,17,0.6);
  }
</style>
```

**关键细节**：display 字号必有 italic pivot word（如 "Intelligence, framed *quietly*."）—— italic 是编辑部最便宜的 emphasis 信号，比 bold / color 更高级。

**为什么是 IFQ**：冷白 `#FFF` 让屏幕像 Excel；`#FAF7F2` 让屏幕像纸。一个色温的差，把数字界面拉回编辑部的工作台。

### Pattern 06 · Co-brand Colophon（共品牌版权页）

**做什么**：第三方品牌项目里，IFQ 不与用户 logo 争主位，而是退到**最末页 / footer 最右**做一个 1990s 出版社风格的 colophon。

```html
<aside style="
  border-top: 1px solid rgba(17,17,17,0.08);
  padding: 32px 0;
  margin-top: 48px;
  display: flex; justify-content: space-between; align-items: baseline;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 10.5px; letter-spacing: 0.1em;
  color: rgba(17,17,17,0.5);
  text-transform: lowercase;
">
  <span>colophon</span>
  <span>typeset by ifq.ai &nbsp;·&nbsp; commissioned for <em style="font-style: italic">&lt;client&gt;</em> &nbsp;·&nbsp; 2026</span>
</aside>
```

**核心原则**：用「typeset by」「commissioned for」这种**编辑部动词**，而不是「powered by」（廉价 SaaS 味）或「designed by」（争功味）。

**强度调节**：

| 场景 | 强度 | 现身处 |
|---|---|---|
| 用户自有 IP / 客户的 owned channel | 弱 | 仅末页 colophon |
| 联名 / co-publish | 中 | colophon + 一处 quiet URL |
| 用户主动 credit IFQ | 强 | 末页 colophon + 文中 spark cluster + quiet URL |
| 严格 white-label | 隐 | 仅保留版面节奏 / 色温 / mono micro grammar，无显式文本 |

---

## Weave Patterns 校验清单（交付前过一遍）

每个交付物按下表自检，**不少于 3 个 Yes** 才算合格：

- [ ] **Pattern 01 Ledger Spine** 是否有一条贯穿 ≥60% 页高的 rust 竖线？
- [ ] **Pattern 02 Mono Field Note** footer 是否有任务语义化的 mono 角注？
- [ ] **Pattern 03 Quiet URL** `ifq.ai` 是否只出现一次？
- [ ] **Pattern 04 Spark Cluster** 是否有 1-3 个**功能性归属**的 sparkle？
- [ ] **Pattern 05 Editorial Contrast** Newsreader italic + Mono + warm paper 三件套是否到位？
- [ ] **Pattern 06 Co-brand Colophon**（第三方项目）末尾是否有一行编辑部 colophon？
- [ ] **整洁红线**：页面任何可见文本里**没有** `//`（双斜杠像 JS 注释）、没有把 pattern 代号 `FIELD NOTE`/`Mono Field Note`/`Spark Cluster` 等写成可见文案？

少于 3 个 Yes = 退回去 weave，不算交付完成。多于 6 个 Yes = 检查是否抢了主品牌的戏。
**红线项不通过 = 直接退回，不计入 Yes 数。**

