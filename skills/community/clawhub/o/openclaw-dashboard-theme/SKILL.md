---
name: openclaw-dashboard-theme
slug: openclaw-dashboard-theme
version: 2.0.0
description: Change OpenClaw Dashboard accent color with one sentence. Dynamically finds CSS/JS files and updates all accent CSS variables.
---

# Dashboard Theme Changer Skill v2

用一句话修改 OpenClaw Dashboard 的主题颜色。支持任意 `#RRGGBB` 色值，自动计算所有 hover/muted/glow 变体，鲁棒地处理文件路径变化。

## 触发条件

匹配以下任一说法时调用：
- "修改 Dashboard 颜色"、"换主题色"、"改变 dashboard 颜色"
- "把 Dashboard 改成 [颜色]"、"把主题换成 [颜色]"
- "Dashboard 换成 [颜色名]"

## 输入

- `color`（必填）：目标十六进制颜色，如 `#2775b6`、`#fcd337`、`#5865F2`

也支持直接说颜色名，自动映射：
- 蓝色 `#2775b6`、紫色 `#5865F2`、绿色 `#22c55e`
- 橙色 `#f59e0b`、青色 `#14b8a6`、粉色 `#ec4899`
- 黄色 `#fcd337`、红色 `#ef4444`

## 工作原理

1. **动态定位文件** — 自动在 OpenClaw 安装目录找到当前版本的 CSS 和 JS 文件（不受文件名 hash 影响）
2. **更新 CSS 变量** — 替换所有 `--accent` 相关变量（dark mode、light mode、openknot、dash 等全部主题）
3. **更新 JS Bundle** — 替换 JS 里硬编码的 accent 色值
4. **自动计算变体** — hover / muted / subtle / glow 颜色根据主色自动推导

## 操作步骤

### 执行脚本

```bash
SKILL_DIR=~/.openclaw/workspace/skills/dashboard-theme
bash "$SKILL_DIR/change-theme.sh" "#fcd337"
```

### 色值校验规则

脚本会自动校验输入：
- 格式必须为 `#RRGGBB`（6位 hex）
- 字母大小写均可
- 已有 `#` 或无 `#` 都能识别

### CSS 变量覆盖范围

脚本会替换以下 CSS 变量（在所有主题块中）：

| 变量 | 用途 |
|------|------|
| `--accent` | 主强调色 |
| `--primary` | 主按钮色 |
| `--ring` | 焦点环 |
| `--accent-hover` | 悬停加深色 |
| `--accent-muted` | 次要强调 |
| `--accent-subtle` | 背景浅色（10% opacity） |
| `--accent-glow` | 发光效果（20% opacity） |
| `--focus` | 焦点高亮 |

### JS Bundle 处理

OpenClaw 的 UI bundle（`index-*.js`）中包含硬编码的 accent 颜色。脚本会：
- 扫描 JS 中的高频出现颜色（排除标准色板：#007bff、#00e5cc、#f59e0b 等）
- 将上一个 accent 颜色替换为新颜色
- 保留 danger 色（`#ef4444` 类）不变

### 验证

运行后脚本自动验证：
- `✅ CSS --accent` 值是否正确
- `✅ 是否消除了旧红色 accent 值`

手动验证：强制刷新浏览器，确认主题色已更新。

## 示例

**用户：** "把 Dashboard 改成明黄色 #fcd337"
**助手：** 运行 `change-theme.sh "#fcd337"`，回复"已改为 #fcd337，强制刷新浏览器生效 🎨"

**用户：** "换成紫色"
**助手：** 运行 `change-theme.sh "#5865F2"`，回复"已改为紫色 #5865F2 🟣"

## 注意事项

- ⚠️ 升级 OpenClaw 后会被覆盖，重新运行命令即可
- ⚠️ **不要**修改 `change-theme.sh` 以外的文件
- ✅ 支持 idempotent（重复运行安全，不会累积替换）
- ✅ 自动适配文件名 hash 变化（v2.0 新增）
- 无需重启 Gateway，强制刷新浏览器即可
