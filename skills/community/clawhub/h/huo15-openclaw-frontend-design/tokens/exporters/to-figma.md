# tokens.json → Figma（Tokens Studio v2 兼容）

> [Tokens Studio](https://tokens.studio/)（前 Figma Tokens Plugin）的 v2.x JSON 与本 skill tokens 几乎 1:1 对应。

## 转换规则

| 本 skill 字段 | Tokens Studio v2 |
|---|---|
| `color.<key>: "oklch(...)"` | `{ value: "oklch(...)", type: "color" }` |
| `colorHex.<key>: "#hex"` | （fallback，Figma 不支持 oklch 时使用）`{ value: "#hex", type: "color" }` |
| `spacing.<key>: 16` | `{ value: "16px", type: "spacing" }` |
| `radius.<key>: 14` | `{ value: "14px", type: "borderRadius" }` |
| `shadow.<key>: "..."` | `{ value: "...", type: "boxShadow" }` |
| `typography.display: "Manrope 800"` | 拆为 `fontFamilies.display` + `fontWeights.display` 两个 set |
| `motion.duration.<key>: 200` ⭐v4.5 | `{ value: "200ms", type: "duration" }` |
| `motion.easing.<key>: "cubic-bezier(...)"` ⭐v4.5 | `{ value: "[0.2, 0, 0, 1]", type: "cubicBezier" }`（拆为 4 元数组） |
| `motion.stagger.<key>: 80` ⭐v4.5 | Figma 无原生概念；导出为 `{ value: "80ms", type: "duration" }` 给 Smart Animate 单独引用 |

## jq 转换（hex fallback 版，Figma 实际可用）

```bash
jq '{
  ($SLUG | tostring): {
    color: (.colorHex | with_entries({
      key: .key,
      value: { value: .value, type: "color" }
    })),
    spacing: (.spacing | with_entries({
      key: .key,
      value: { value: "\(.value)px", type: "spacing" }
    })),
    borderRadius: (.radius | with_entries({
      key: .key,
      value: {
        value: (if (.value | type) == "number" then "\(.value)px" else .value end),
        type: "borderRadius"
      }
    })),
    boxShadow: (.shadow | with_entries({
      key: .key,
      value: { value: .value, type: "boxShadow" }
    }))
  }
}' --arg SLUG bold-minimal tokens/bold-minimal.json > generated/figma/bold-minimal.tokens.json
```

## 在 Figma 里使用

1. 安装 [Tokens Studio plugin](https://www.figma.com/community/plugin/843461159747178978/tokens-studio-for-figma)
2. 打开 plugin → 文件菜单 → **Import** → JSON
3. 上传上一步生成的 JSON
4. 一键应用到 Figma styles（自动建 color styles / text styles / effect styles）

## 限制

- **Figma 不支持 oklch**（截至 2026-04），plugin 默认用 hex fallback；本 skill 的 token 文件已为每个 color 提供 `colorHex`
- **Figma 不支持 cubic-bezier 字符串**直接，需拆成 4 元数组 `[x1, y1, x2, y2]`；jq 转换时用 `gsub("cubic-bezier\\("; "[") | gsub("\\)"; "]")` 简单替换可工作
- **stagger** 在 Figma 无原生概念，Smart Animate 只能逐对象设 delay；本 skill 把 stagger 导出为 duration 给 Figma 单独使用
- **不规则圆角**（organic 的 `48% 52% 55% 45%`）Figma 不支持，需手画 ellipse 或 vector
- **rpx**（小程序单位）转 Figma 需 ×2 → px（750rpx 屏宽对应 Figma 375px design board）
- **typography 字符串拆分**：`"Manrope 800"` → 需手动拆成 `fontFamilies.display = "Manrope"` 和 `fontWeights.display = 800`，jq 单行不够智能（用 awk 或 Node 脚本兜底）
