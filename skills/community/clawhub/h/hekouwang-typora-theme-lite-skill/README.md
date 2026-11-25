# hekouwang · Typora 长文阅读主题

<p align="center">
  <b>把 Markdown 从编辑器里的纯文本，变成一张适合连续阅读与写作的纸。</b><br>
  免费 V2（浅色 + 深色 · MIT）· 专业版六套视觉走 SkillPay 买断
</p>

<p align="center">
  <a href="README.en.md">English</a>
  · <a href="https://huiyonghkw.github.io/hekouwang-typora-theme-lite-skill/"><b>体验站</b></a>
  · <a href="https://huiyonghkw.github.io/hekouwang-typora-theme-lite-skill/live/">在线真 CSS</a>
  · <a href="https://skillpay.alipay.com/shelf/product?productId=P0806000213890180&amp;merchantCode=huiyonghkw">SkillPay · ¥9.9</a>
  · <a href="README.zh.md">技术说明</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.3-06a88c" alt="version 2.0.3">
  <img src="https://img.shields.io/badge/license-MIT-00d4aa" alt="MIT">
  <img src="https://img.shields.io/badge/Typora-macOS%20%7C%20Windows-6a45e0" alt="Typora macOS Windows">
</p>

免费 V2 真机截图（macOS Typora）：

| 浅色 | 深色 |
|---|---|
| ![免费 V2 浅色](docs/previews/r/v2-light.webp) | ![免费 V2 深色](docs/previews/r/v2-dark.webp) |

## 这套主题解决什么

- **中文长文松而不散。** 正文 `1rem`、行高 `1.65`；纸面随窗口伸缩，阅读列居中夹在 `48–96rem`。
- **层级靠字号与留白，不靠彩条。** 代码、引用、表格各有边界，但不把文章切成卡片墙。
- **侧栏收起即全幅。** 纸边与投影一起消失；正文仍落在阅读列内。
- **编辑 / 源码 / 专注 / PDF 同一套节奏。** 导出压平浮层；纸张与页边距跟 Typora 设置走。
- **中英混排不将就。** 西文随包 Inter，中文用系统字体；Windows 走 `body.os-windows` 字栈。

## 安装（约两分钟）

在 Typora：**偏好设置 → 外观 → 打开主题文件夹**。或用安装器：

### macOS

```bash
git clone https://github.com/huiyonghkw/hekouwang-typora-theme-lite-skill.git
cd hekouwang-typora-theme-lite-skill
./scripts/install.sh
```

### Windows（PowerShell）

```powershell
git clone https://github.com/huiyonghkw/hekouwang-typora-theme-lite-skill.git
cd hekouwang-typora-theme-lite-skill
.\scripts\install-windows.ps1
```

若策略拦住脚本：`powershell -ExecutionPolicy Bypass -File .\scripts\install-windows.ps1`（只影响本次进程）。自定义主题目录用 `-ThemeDir 'D:\your\Typora\themes'`。

然后**完全退出并重开 Typora**，主题菜单选 **Hekouwang** / **Hekouwang Dark**。改 CSS 后也要重启才会加载。

也可手动复制 `theme/hekouwang.css`、`theme/hekouwang-dark.css` 与 `theme/hekouwang/` 到主题目录。

### 可选：更窄的阅读列

在主题目录新建 `hekouwang.user.css`（深色用 `hekouwang-dark.user.css`）：

```css
:root { --hk-reading-measure: 40rem; }
```

改完后重启 Typora。

## 免费与专业版

| | 内容 | 授权 |
|---|---|---|
| **免费 V2** | `Hekouwang` / `Hekouwang Dark`（本仓） | MIT |
| **专业版** | V1 / V2 Pro / V3–V6，各浅+深共 12 个 CSS | SkillPay 买断 ¥9.9 · 许可见专业包内 `LICENSE-PRO.txt` |

免费版是完整长文主题，不是功能阉割。专业版换的是六套独立色彩与标题工艺，阅读指标与免费版相同。菜单名：**Hekouwang V1**、**Hekouwang V1 Dark** 等。购买：[SkillPay · ¥9.9](https://skillpay.alipay.com/shelf/product?productId=P0806000213890180&merchantCode=huiyonghkw) · [体验站说明](https://huiyonghkw.github.io/hekouwang-typora-theme-lite-skill/#buy)。

| 主题 | 视觉方向 |
|---|---|
| **V1 · 石墨青绿** | 冷蓝灰、薄荷青、紫链 |
| **V2 Pro · 典藏编辑** | 胡桃墨、古铜、暖纸、双线 |
| **V3 · 财经** | 海军蓝与黄铜，偏表格秩序 |
| **V4 · 玻璃** | 冰蓝、雾面叠片 |
| **V5 · HUD** | 紫晶外壳、青色信号 |
| **V6 · 焰彩** | 李紫、珊瑚橙与粉 |

真机预览（点图可放大；也可在[体验站对比](https://huiyonghkw.github.io/hekouwang-typora-theme-lite-skill/#compare-shots)）：

### V1 · 石墨青绿

| 浅色 | 深色 |
|---|---|
| ![V1 浅色](docs/previews/r/v1-light.webp) | ![V1 深色](docs/previews/r/v1-dark.webp) |

### V2 Pro · 典藏编辑

| 浅色 | 深色 |
|---|---|
| ![V2 Pro 浅色](docs/previews/r/v2-pro-light.webp) | ![V2 Pro 深色](docs/previews/r/v2-pro-dark.webp) |

### V3 · 财经

| 浅色 | 深色 |
|---|---|
| ![V3 浅色](docs/previews/r/v3-light.webp) | ![V3 深色](docs/previews/r/v3-dark.webp) |

### V4 · 玻璃

| 浅色 | 深色 |
|---|---|
| ![V4 浅色](docs/previews/r/v4-light.webp) | ![V4 深色](docs/previews/r/v4-dark.webp) |

### V5 · HUD

| 浅色 | 深色 |
|---|---|
| ![V5 浅色](docs/previews/r/v5-light.webp) | ![V5 深色](docs/previews/r/v5-dark.webp) |

### V6 · 焰彩

| 浅色 | 深色 |
|---|---|
| ![V6 浅色](docs/previews/r/v6-light.webp) | ![V6 深色](docs/previews/r/v6-dark.webp) |

## 给想定制的人

不要手改 `theme/*.css`（生成物）。改 [`scripts/tokens.json`](scripts/tokens.json) / [`scripts/palettes.json`](scripts/palettes.json) 后重建：

```bash
python3 scripts/build.py
python3 scripts/verify_layout.py --all
```

构建会拦 `px` 字号滥用、非导出区 `!important`，并对出货 CSS 做对比度审计。细节见 [技术说明](README.zh.md)；目录约定见 [`STRUCTURE.md`](STRUCTURE.md)。

本仓 Agent 入口：根 [`SKILL.md`](SKILL.md)（`hekouwang-typora-theme-lite-skill`）。

## 授权

- 免费主题、脚本与 Lite Skill：**[MIT](LICENSE)**；Inter：SIL OFL 1.1
- 专业版主题包：包内许可 / `LICENSE-PRO.txt`，个人使用，勿二次分发
- 与 Anthropic PBC 无从属关系；Claude / Anthropic 为其商标
