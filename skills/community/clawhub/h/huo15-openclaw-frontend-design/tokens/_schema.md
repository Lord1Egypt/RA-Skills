# tokens.json Schema · v4.0

> 每个流派一份 `<slug>.json`，扁平 1 层结构便于 jq 转换。

## 字段约定

```jsonc
{
  "name": "bold-minimal",                     // 必须等于文件名（无 .json）
  "displayName": "BOLD-MINIMAL · 勇敢极简",   // SKILL.md §三 流派表对应名
  "version": "1.0.0",                         // 流派 token 自身版本
  "color":    { "<token>": "oklch(...)" },   // oklch 首选
  "colorHex": { "<token>": "#hex" },         // 1:1 对应 color，给不支持 oklch 环境
  "typography": {
    "display": "<Family> <Weight> [italic]",
    "body":    "<Family> <Weight>"
  },
  "spacing": { "xs": 4, "sm": 8, ..., "2xl": 128 },   // 单位 px；小程序按 rpx ×2 换算
  "radius":  { "none": 0, "sm": 2, ..., "pill": 999 },
  "shadow":  { "subtle": "...", "card": "...", "modal": "..." },
  "examplePath": "../examples/<dir>/index.html",     // 对应 starter 文件
  "redLineWaiver": ["..."],                           // 可选；说明本流派对哪条红线有合规豁免
  "motion": {                                         // ⭐v4.5 动效 tokens
    "duration": { "fast": 200, "normal": 300, ... },  // 单位 ms
    "easing":   { "<name>": "cubic-bezier(...) | linear | steps(...)" },
    "stagger":  { "tight"|"normal"|"loose": 50|80|120 },  // 列表级联出场延迟（ms）
    "philosophy": "<一句话流派动效原则>"
  }
}
```

## 硬约束

- `color` 与 `colorHex` 必须**键名 1:1 对应**（同 key、同顺序）
- `color` 必填 oklch；颜色硬规则见 [`../references/colors.md`](../references/colors.md)
- `typography` 字体不能命中红线 #1（Inter / Roboto / Arial / system-ui）；**小程序场景豁免**（PingFang SC 等中文字体允许）
- 任何字段缺失 → 视作"沿用 colors.md / typography.md 中通用约束"
- **不要嵌套**对象（如 `color.brand.primary`）— 保持扁平 1 层，jq 一行能转

## 导出器

- [`exporters/to-css-vars.md`](exporters/to-css-vars.md) — jq → CSS variables
- [`exporters/to-tailwind.md`](exporters/to-tailwind.md) — jq → tailwind.config.js extend
- [`exporters/to-figma.md`](exporters/to-figma.md) — Tokens Studio v2 兼容格式

所有导出器**只返回 jq / shell 命令给用户执行**，不在 skill 内部 spawn（延续 enhance "禁 child_process" 铁律）。
