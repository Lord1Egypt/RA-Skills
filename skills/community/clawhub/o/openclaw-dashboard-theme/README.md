# 🌈 OpenClaw Dashboard Theme Changer

> Change your OpenClaw Dashboard accent color with **one sentence**.

[🇨🇳 中文](#中文说明) · [🇺🇸 English](#english)

---

## English

### What is this?

A **skill** for [OpenClaw](https://github.com/openclaw/openclaw) that changes the Dashboard's accent color in one sentence. v2.0 is fully robust — it works regardless of OpenClaw version or file hash changes.

### Preview

| Default | Your Color |
|:---:|:---:|
| 🔴 | 💛 🟣 🟢 🔵 |

### Usage

Just tell your OpenClaw assistant:

```
Change my Dashboard to #5865F2
```
```
把 Dashboard 改成明黄色
```

Or pick a color by name:

| Color | Hex |
|:---:|:---:|
| 🔵 Blue | `#2775b6` |
| 🟣 Purple | `#5865F2` |
| 🟢 Green | `#22c55e` |
| 🟠 Orange | `#f59e0b` |
| 🔵 Cyan | `#14b8a6` |
| 💗 Pink | `#ec4899` |
| 💛 Yellow | `#fcd337` |

### How it works (v2.0)

1. Dynamically locates the CSS and JS asset files in the OpenClaw install directory — **no hardcoded paths**
2. Replaces all `--accent` CSS variables across every theme (dark, light, openknot, dash, etc.)
3. Computes all variants automatically: `--accent-hover`, `--accent-muted`, `--accent-subtle`, `--accent-glow`, `--focus`
4. Updates hardcoded accent colors in the JS bundle
5. Idempotent — safe to run multiple times

### Installation

OpenClaw loads skills automatically from:

```
~/.openclaw/workspace/skills/dashboard-theme/SKILL.md
```

Or via [ClawHub](https://clawhub.com):

```bash
openclaw skills install openclaw-dashboard-theme
```

### Requirements

- Bash 4+
- OpenClaw installed via npm (`npm install -g openclaw`)
- No root required

### Notes

- ⚠️ Upgrading OpenClaw will **overwrite** changes — just re-run the command
- No Gateway restart needed — force refresh browser (`Ctrl+Shift+R` / `Cmd+Shift+R`)
- The script validates input and prints clear error messages

---

## 中文说明

### 这是什么？

一个面向 [OpenClaw](https://github.com/openclaw/openclaw) 的 **技能（Skill）**，用一句话修改 Dashboard 的主题颜色。v2.0 完全鲁棒，不受 OpenClaw 版本或文件路径变化影响。

### 效果预览

| 默认 | 自定义 |
|:---:|:---:|
| 🔴 | 💛 🟣 🟢 🔵 |

### 使用方法

直接告诉你的 OpenClaw 助手：

```
把我的 Dashboard 改成 #5865F2
```
```
换成黄色
```

或直接说颜色名：

| 颜色 | 色号 |
|:---:|:---:|
| 🔵 蓝色 | `#2775b6` |
| 🟣 紫色 | `#5865F2` |
| 🟢 绿色 | `#22c55e` |
| 🟠 橙色 | `#f59e0b` |
| 🔵 青色 | `#14b8a6` |
| 💗 粉色 | `#ec4899` |
| 💛 黄色 | `#fcd337` |

### 工作原理（v2.0）

1. **动态定位文件** — 不依赖硬编码路径，自动找到当前版本的 CSS 和 JS 文件
2. **替换所有 CSS 变量** — `--accent`、`--primary`、`--ring`、`--accent-hover`、`--accent-muted`、`--accent-subtle`、`--accent-glow`、`--focus` 在所有主题块中全部更新
3. **自动计算变体** — 根据主色自动推导 hover / muted / subtle / glow 颜色
4. **更新 JS Bundle** — 替换 JS 里硬编码的 accent 颜色
5. **幂等安全** — 可重复运行，不会累积替换

### 安装方式

OpenClaw 会自动从以下路径加载技能：

```
~/.openclaw/workspace/skills/dashboard-theme/SKILL.md
```

或通过 [ClawHub](https://clawhub.com) 安装：

```bash
openclaw skills install openclaw-dashboard-theme
```

### 系统要求

- Bash 4+
- 通过 npm 安装的 OpenClaw（`npm install -g openclaw`）
- 无需 root 权限

### 注意事项

- ⚠️ 升级 OpenClaw 后会被覆盖，重新运行命令即可
- 无需重启 Gateway，强制刷新浏览器即可（`Ctrl+Shift+R` / `Cmd+Shift+R`）
- 脚本会验证输入并输出清晰的错误信息

---

## 文件说明

```
dashboard-theme/
├── SKILL.md          # OpenClaw Skill 定义（触发条件 + 执行逻辑）
├── change-theme.sh   # 核心脚本（v2.0，完全鲁棒）
└── README.md         # 使用文档（中英双语）
```

## License

MIT License
