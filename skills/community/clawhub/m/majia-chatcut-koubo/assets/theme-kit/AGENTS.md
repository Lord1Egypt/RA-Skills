# AGENTS.md

## 设计数据源

- 开始任何 UI 修改前，先读取 `tokens/themes.json`、`tokens/layouts.json` 和 `docs/layout-spec.md`。
- 不在组件中硬编码十六进制颜色；只使用 `tokens/themes.css` 的 CSS 变量，或从 JSON/TS token 读取。
- 不修改 `sourcePalette` 中的 4 个原始色值；新增衍生色只能写入 `semantic`。

## 画布与内容规则

- 画布固定为 1080 × 1920，比例 9:16。
- 标题最多 2 行，强调词最多 1 行；先删字，再缩字号，禁止横向压缩文字。
- 关键文案必须位于安全区内；底部 180px 不放按钮或关键信息。
- 人物素材优先使用透明背景视频或 PNG；普通视频必须置于 `.talk-card__speaker` 中。
- SVG 底图只做氛围和结构，不承载不可替换的业务文字。

## 改动联动

- 新增或改主题时，同步更新：`tokens/themes.json`、`tokens/themes.css`、`tokens/themes.ts`、`manifest.json` 和对应 SVG/PNG 底图。
- 新增或改布局时，同步更新：`tokens/layouts.json`、`components/portrait-talk-card.css` 和预览页。
- 修改后运行 `node scripts/check-contrast.mjs`，并打开 `index.html` 检查 8 套主题无溢出、无遮挡。

## 交付标准

- 保持零运行时依赖的 HTML/CSS/JS 基础版本。
- React 示例可以调整，但不能成为唯一实现。
- 不引入字体文件；使用项目定义的中文系统字体栈。
