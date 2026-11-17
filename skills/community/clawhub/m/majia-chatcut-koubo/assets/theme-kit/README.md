# 9:16 口播视频配色与底图系统

这是一套面向 1080 × 1920 竖屏口播内容的设计资产包。8 套配色均已拆成原始色板、语义色、SVG 底图、布局坐标和可运行的 HTML/CSS/JS 组件；PNG 与海报属于本地生成物，不随 source 包预生成。

## 先看什么

1. 直接打开 `index.html`：查看 8 套主题总览。
2. 打开 `examples/single.html`：切换主题、布局、文案和安全区。
3. Codex 开始改代码前先读取根目录 `AGENTS.md`。
4. 颜色以 `tokens/themes.json` 为唯一数据源，布局以 `tokens/layouts.json` 为唯一数据源。

## 快速接入

```html
<link rel="stylesheet" href="tokens/themes.css">
<link rel="stylesheet" href="components/portrait-talk-card.css">
<div id="card"></div>
<script src="components/portrait-talk-card.js"></script>
<script>
  PortraitTalkThemeKit.mount("#card", {
    theme: "sea-salt-cyan",
    layout: "fresh-frame",
    showSubtitle: true,
    copy: {
      title: "会员不是折扣人群，\n而是经营资产",
      emphasis: "经营资产",
      footer: "先理解用户，再设计权益"
    }
  });
</script>
```

组件画布固定为 1080 × 1920。预览时可以使用 CSS `transform: scale(...)` 缩放，导出时按原尺寸截图或录制。

## 替换口播人物

组件内 `.talk-card__speaker` 是人物安全区。透明背景视频建议加 `is-cutout`：

```html
<div class="talk-card__speaker is-cutout">
  <video class="talk-card__speaker-media" src="speaker.webm" autoplay muted loop playsinline></video>
</div>
```

普通矩形视频去掉 `is-cutout`，组件会按主题自动加底色、边框和圆角。

## 文件结构

- `AGENTS.md`：给 Codex 的项目级约束。
- `tokens/themes.json`：8 套主题、原始色板和语义色。
- `tokens/layouts.json`：8 个布局的 1080 × 1920 坐标。
- `tokens/themes.css` / `tokens/themes.ts`：前端可直接使用的变量与类型。
- `assets/backgrounds/*.svg`：可编辑矢量底图。
- `assets/backgrounds-png/*.png`：运行 `scripts/render-backgrounds.py` 后生成的 1080 × 1920 纯底图（可选，不随 source 包提交）。
- `assets/demo-posters/*.png`：可选的本地成品预览输出，不是 release 必需资产。
- `assets/overlays/safe-area.svg`：字幕和底部 UI 保护区参考。
- `components/portrait-talk-card.*`：无依赖 HTML 组件。
- `examples/PortraitTalkCard.tsx`：React 示例。
- `scripts/check-contrast.mjs`：检查关键文字与按钮对比度。

## 主题选择

| 主题 | 适合内容 | 默认布局 |
|---|---|---|
| 深空蓝 | 数据、技术、AI、方法论 | 斜切科技 |
| 墨绿金 | 业务复盘、经营、策略 | 商务分栏 |
| 暖灰橙 | 干货、培训、日常表达 | 居中编辑 |
| 午夜紫 | 趋势、创新、产品发布 | 轨道聚焦 |
| 极简黑白 | 知识卡片、观点、问答 | 极简长栏 |
| 海盐青 | 用户运营、会员增长、服务 | 清新框景 |
| 大地棕 | 商业思考、案例、品牌故事 | 大地带状 |
| 活力青柠 | 活动、会员日、上新传播 | 轻快角落 |

## 校验

```bash
node scripts/check-contrast.mjs
python3 -m http.server 8000
```

然后访问本地的 `index.html` 和 `examples/single.html`。
