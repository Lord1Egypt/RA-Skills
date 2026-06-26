# Font Loading Protocol · CN-friendly, GFW-tolerant

> **目标**：让 IFQ Design Skills 的产出在中国大陆、企业内网、离线环境下都能流畅打开，不因为 Google Fonts 被墙就白屏 / 长时间空转 / 字体巨丑。
>
> **核心原则**：Google Fonts 是「锦上添花」，不是「render 前提」。永远先用强健的系统字体栈托底，再异步增强。

---

## 0 · 决策树

```
任务涉及交付 HTML？
├─ 用户在中国大陆 / 内网 / 离线？      → 走「Tier A · 系统字体优先」（可完全去掉 Google Fonts）
├─ 用户在海外 / 不确定网络？           → 走「Tier B · 非阻塞渐进增强」（默认）
└─ 必须像素级匹配 Newsreader/Inter？   → 走「Tier C · 自托管子集」（高级）
```

**默认走 Tier B**。所有 8 个模板与本仓库 demo 都已按 Tier B 改造，agent fork 后**无需再做额外工作**。

---

## 1 · Tier A · 系统字体优先（中国友好 · 零网络依赖）

完全不引入 Google Fonts，靠 `ifq-tokens.css` 里的多语言系统栈。`Noto Serif SC` / `Songti SC` / `PingFang SC` 在 macOS / iOS / 部分 Windows 自带，Linux 多发行版也有 `Noto` 全家桶。

**启用方式**：把 `<link rel="stylesheet" href="https://fonts.googleapis.com/...">` 整段删掉，保留 `ifq-tokens.css` 的 `--ifq-font-*` 变量。

**何时强烈推荐**：

- 用户明确说「我在国内 / 网不好 / 不要外链 CDN」
- 离线 / 内网交付
- VirusTotal / 企业 SOC 审查的纯文本资产
- 印刷物（Tier A 永远更稳）

---

## 2 · Tier B · 非阻塞渐进增强（默认）

页面 render **不等** Google Fonts。如果 CDN 通就 swap 进来；不通就保持系统字体，用户视觉上几乎无感。

**统一片段**（可直接复制进 `<head>`）：

```html
<!-- Tier B · 非阻塞 Google Fonts；GFW / 离线时自动回退到 ifq-tokens.css 系统字体栈 -->
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,700;1,400&family=JetBrains+Mono:wght@400;600&family=Noto+Serif+SC:wght@400;700&display=swap"
      rel="stylesheet"
      media="print"
      onload="this.media='all'">
<noscript>
  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,700;1,400&family=JetBrains+Mono:wght@400;600&family=Noto+Serif+SC:wght@400;700&display=swap">
</noscript>
```

**为什么这套写法安全**：

- `media="print"` 让浏览器把它当打印样式 → 不阻塞首屏 render
- `onload="this.media='all'"` 加载完才提升为正式样式（Filament Group / web.dev 推荐写法）
- 无 `eval` / `Function` / `document.write`，VirusTotal、企业内容安全策略不会告警
- 无 `<script>` 标签，CSP `script-src 'self'` 也兼容
- 失败时**静默回退**到 system stack，没有 console error 也没有空白

**关键搭配**（已在 `ifq-tokens.css` 落地）：

```css
:root {
  --ifq-font-display: "Newsreader", "Noto Serif SC", "Songti SC", Georgia, serif;
  --ifq-font-body:    "Noto Serif SC", "Songti SC", Georgia, "Newsreader", serif;
  --ifq-font-mono:    "JetBrains Mono", "SF Mono", ui-monospace, Menlo, monospace;
}
```

字体栈第一位是 Web 字体，**其余都是各 OS 自带**——任何一台终端打开都不会"豆腐块"。

**`display=swap` 必带**：CSS 端通知浏览器「先用 fallback 渲染，加载完再 swap」。Tier B 的两个保护层：HTML 层非阻塞，CSS 层 swap-FOUT。

---

## 3 · Tier C · 自托管子集（高级 · 可选）

在像素级匹配特定 Web 字体、且离线场景重要时使用。流程：

1. 在 `assets/fonts/` 下放 woff2（已在 smoke-test 允许的二进制白名单内）
2. 用 [pyftsubset](https://fonttools.readthedocs.io/) 或 [glyphhanger](https://github.com/zachleat/glyphhanger) 子集化（中文按 GB2312 常用 6763 字 ≈ 800KB）
3. 在 `<head>` 写 `@font-face`：

```html
<style>
  @font-face {
    font-family: 'Newsreader';
    font-display: swap;
    src: url('assets/fonts/newsreader-subset.woff2') format('woff2');
  }
</style>
```

**注意**：本仓库 ClawHub 版**不预打包字体二进制**——避免 bundle 体积膨胀和版权审查。Tier C 由用户在自己仓库引入。

---

## 4 · 镜像选项（不推荐为默认）

> ⚠️ 镜像稳定性、隐私性、版权状态各异，**不要写进默认模板**。仅在用户主动要求或 Tier B 长期不通时手工切换。

| 镜像 | 用途 | 风险 |
|------|------|------|
| `fonts.loli.net` / `gstatic.loli.net` | 社区维护的 Google Fonts 反代 | 第三方运营，可能停服 |
| `fonts.font.im` | 「字客网」反代 | 同上，速度不稳 |
| 自托管（Tier C） | 完全可控 | 需要打包资源 |

切换方式：把上面 Tier B 片段里的 `fonts.googleapis.com` 替换为镜像域名，**同步替换 preconnect**。不要混用。

---

## 5 · Verification 清单（交付前自检）

- [ ] HTML 里 Google Fonts 的 `<link>` 带 `media="print" onload="this.media='all'"`
- [ ] 配套 `<noscript>` 兜底
- [ ] CSS `--ifq-font-*` 栈第一位之后**至少有 2 个系统字体**（中文资产必须含 `Noto Serif SC` 或 `Songti SC` / `PingFang SC`）
- [ ] CSS `font-display: swap`（Google Fonts URL 自带 `display=swap`）
- [ ] 在断网 / 屏蔽 `fonts.googleapis.com` 的浏览器里打开页面，**5 秒内首屏可读**，不出现「豆腐块」
- [ ] 动画 / 测量代码包在 `document.fonts.ready.then(...)`（避免 swap 时跳变，详见 `references/animation-pitfalls.md`）

---

## 6 · 与本仓库其他规则的关系

- `references/asset-protocol.md` 里「字体」一栏指的是**品牌字体**抽取，本协议讲的是 **Web 字体加载方式**——两者正交
- `references/content-guidelines.md` 反 slop 提到「不要默认用 Inter/Roboto 当 display」——Tier B 默认就给的是 `Newsreader + Noto Serif SC + JetBrains Mono`，已避开
- `references/animation-pitfalls.md` 的 `document.fonts.ready` 守则在 Tier B 下依然必须遵守（swap 进来时会触发 reflow）
