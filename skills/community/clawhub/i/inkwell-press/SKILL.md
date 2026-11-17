---
name: 公众号排版 / 小红书封面
description: >-
  公众号排版 / 小红书封面 / 内容一键发布。全链路内容发布工具（Inkwell）。Markdown 转公众号 HTML、
  生成杂志封面、生成小红书社交卡片、发布到剪贴板或公众号草稿箱。一条命令从选题到发布，不只是排版。
  触发词：公众号排版、公众号发布、小红书封面、小红书卡片、Markdown 转 HTML、内容发布、文章配图、封面生成。
version: 1.0.5
metadata:
  openclaw:
    requires:
      bins: [pip3, python3]
    primaryEnv: ""
    emoji: "🖋️"
    homepage: https://github.com/lijinhongucl-pixel/inkwell
    os: [macos, linux, windows]
    install:
      - kind: pip
        package: inkwell-press==0.8.1
        bins: [inkwell]
---

# Inkwell — 从 Markdown 到发布的一条命令流水线

Inkwell 把写完文章之后最耗时的机械活一次做完：排版成能粘进公众号的 HTML、压缩上传配图、
生成杂志封面与社交卡片，最后推送到剪贴板或公众号草稿箱。一条 `inkwell run article.md`
产出的 HTML 可直接粘进公众号编辑器。

## ⚠️ Safety & Data Handling — Read Before Use

Inkwell 是一个**会对外传输数据**的工具，不是一个纯本地格式化器。在执行以下操作前，
Agent **必须先告知用户数据去向**并征得确认：

| 操作 | 数据去向 | 风险 |
|------|---------|------|
| `run`（配了 CDN） | 本地图片 → **GitHub Contents API** 上传 → **jsDelivr CDN** 公开可访问 | 未发布的图片会变成公网可访问的 URL |
| `run`（正文含外链图，默认行为） | 外链图被**下载**到本地再内嵌进本地预览版 | 下载行为会产生出网请求；在离线/内网/敏感环境加 `--no-embed-external` 禁止 |
| `publish --target clipboard` | 富文本写入**系统剪贴板** | 会**覆盖**剪贴板当前内容；粘贴到错误目的地会泄露文章 |
| `publish --target wechat` | 文章内容 + 图片 → **微信服务器** | 草稿会出现在公众号后台；图片转存到微信图床 |

**Agent 行为约定**：
1. 首次执行 `publish` 前，明确告知用户「内容将被发送到 GitHub / 微信 / 剪贴板」并等待确认
2. 不要对用户未明确要求发布的草稿执行 `publish`
3. `run` 命令默认只在本地处理；只有用户提供了 `GITHUB_TOKEN` 等凭证时才会上传图片
4. 不加 `--no-embed-external` 时，外链图会被下载 —— 在离线/内网环境告知用户

## When to Trigger

**仅在用户明确要求公众号排版或内容发布时触发**。不要在用户只是写 Markdown、
聊 AI、讨论内容策略时自动激活。

明确触发场景：
- 用户说「帮我排版这篇 Markdown 成公众号文章」「把这篇文章转成公众号 HTML」
- 用户说「帮我做封面图」「生成小红书图文」「出社交卡片」
- 用户说「把这篇文章发布到公众号草稿箱」「复制排版结果到剪贴板」
- 用户说「检查这篇文章有没有公众号禁忌写法 / 敏感词」
- 用户提到 Inkwell 并要求执行上述任一操作

**不应触发的场景**：
- 用户只是写 Markdown，没有提到公众号 / 排版 / 发布
- 用户在讨论内容选题但没有要求执行排版或发布操作
- 用户使用其他排版工具（doocs/md、mdnice 等）

## Installation

### 推荐：固定版本安装（供应链安全）

```bash
# 固定到已审查的版本，避免上游变更引入未审查代码
pip3 install "inkwell-press==0.8.1"
```

### 带哈希校验安装（最高安全性）

```bash
# requirements.txt 中固定版本 + 哈希
pip3 install --require-hashes -r requirements.txt
```

（`requirements.txt` 随本 Skill 打包，包含版本号和 SHA256 哈希）

### 从源码安装（审查后固定 commit）

```bash
git clone https://github.com/lijinhongucl-pixel/inkwell.git
cd inkwell
# 固定到已审查的 commit，不跟默认分支漂移
git checkout --detach d1842ba
pip3 install .
```

### 供应链审计与可复现构建

本 Skill 包含 `SUPPLY_CHAIN.md`，提供：

- **可复现构建**：从 pinned commit `d1842ba` 构建 wheel，验证 SHA-256 与 `requirements.txt` 一致
- **SBOM**：直接依赖 + 传递依赖锁定方法（pip-tools --generate-hashes）
- **npm 锁文件**：ClawHub CLI 的 project-local 安装 + integrity 校验
- **审计清单**：安装前逐项核对

审查者应在安装前阅读 `SUPPLY_CHAIN.md` 并复现 wheel 哈希。

⚠️ 发行名是 `inkwell-press`，**不是** `inkwell`（那是无关的 Qt 深色主题包）。

### 安全安装建议

- 在**隔离的虚拟环境**（venv / conda）中安装，不要装到系统 Python
- 不要以 root / 管理员身份安装
- 仅为需要的功能提供凭证：不传 `GITHUB_TOKEN` 就不会上传图片；
  不传 `WECHAT_APP_ID` 就不会推送到微信
- 怀疑依赖被篡改时立即轮换所有已暴露的凭证
- **锁定传递依赖**：使用 `pip-compile --generate-hashes` 生成完整的哈希锁文件
  （见 `SUPPLY_CHAIN.md` Section 2），而非仅锁定顶层包
- **审计上游实现**：本 Skill 包只含文档，实现在 `inkwell-press` 包中 ——
  安装前请按 `SUPPLY_CHAIN.md` 的审计清单复现 wheel 哈希并检查源码

## 核心能力（十三大命令）

| 命令 | 用途 |
|------|------|
| `run` | Markdown → 公众号 HTML 排版 + 图片处理 + 校验（文字节点自动包 `<span leaf="">`） |
| `publish` | 发布到剪贴板（富文本）或公众号草稿箱（封面与正文图自动转存微信图床） |
| `cover` | 生成杂志风封面（21:9 主封面 + 1:1 方图，可选 PNG 截图） |
| `card` | 生成社交卡片（小红书 3:4 轮播等 11 个平台） |
| `generate` | 根据主题生成 Markdown 草稿（5 种风格骨架） |
| `search` | 内容搜索（GitHub 热门项目、自定义后端） |
| `advise` | 封面设计建议（6 种高转化模式智能推荐） |
| `audit` | 三门设计质量审计 |
| `wordcheck` | 敏感词 / 合规检测（广告法极限词 + 平台违规词 + 通用敏感词） |
| `stats` | 字数统计 + 阅读时间 + 结构分析 |
| `toc` | 自动生成文章目录卡片（H2/H3 提取 + 编号） |
| `validate` | 检查 HTML 是否有公众号禁忌写法（含 `<span leaf>` 硬门槛） |
| `themes` | 列出所有排版主题 |

## Usage

### 场景一：排版文章

```bash
inkwell run article.md --theme graphite-minimal
```

产出在 `./output/`，含**两版**：

- `xxx_预览.html` —— 发布版，图片走 CDN 外链（需配置），用于复制到公众号
- `xxx_预览_本地版.html` —— 图片内嵌 base64，用于 IDE 预览等离线环境

**出网行为说明**：
- 不传 `GITHUB_TOKEN` 时，本地图片降级为 base64，不会上传
- ⚠️ 但如果正文里**包含外链图片**（`http://` / `https://`），`run` **默认会下载**这些图片以生成
  本地预览版 —— 这会产生出网请求。在离线/内网/敏感环境，加 `--no-embed-external` 禁止下载：
  ```bash
  inkwell run article.md --theme graphite-minimal --no-embed-external
  ```

### 场景二：完整流水线（涉及数据外传，需用户确认）

```bash
# 1. 搜索素材（出网请求到 GitHub API）
inkwell search "X" --source github --limit 10 --markdown

# 2. 生成草稿骨架（纯本地）
inkwell generate "X" --style tutorial -o draft.md

# 3. 排版（若配了 CDN 则上传图片到 GitHub；否则纯本地）
#    ⚠️ 若正文含外链图，默认会下载 —— 加 --no-embed-external 可禁止
inkwell run draft.md --theme moyu-green -o ./output

# 4. 生成封面（纯本地 HTML；--png 会调用 Playwright 截图）
inkwell cover --title "X" --kicker "开源" -o ./covers/

# 5. 发布到剪贴板 ⚠️ 会覆盖剪贴板内容
inkwell publish ./output/draft_预览.html --target clipboard
```

### 场景三：做一套小红书图文（纯本地）

```bash
inkwell card --platform xhs --style editorial --pages 5 \
  --titles "封面" "要点1" "要点2" "要点3" "总结" -o ./cards/
```

### 场景四：推进公众号草稿箱 ⚠️ 数据发送到微信服务器

```bash
export WECHAT_APP_ID=wx****************
export WECHAT_APP_SECRET=****************

inkwell publish ./output/xxx_预览.html \
  --target wechat --title "标题" --author "作者" \
  --thumb-image ./covers/cover_01_21x9.png
```

**执行前告知用户**：文章内容和图片将被发送到微信服务器，草稿会出现在公众号后台。

## 主题选择指南（15 套）

| 题材 | 推荐主题 |
|------|---------|
| 教程、测评、工具盘点 | `moyu-green` 摸鱼绿 |
| 深度分析、观点 | `red-white` 红白色系 |
| 设计、科技评论 | `graphite-minimal` 石墨极简 |
| 禅意、极简生活 | `zen-whitespace` 留白禅意 |
| 工具对比、评测 | `moyu-ticket` 摸鱼票据 |
| 内刊手记、案例复盘 | `olive-journal` 橄榄手记 |
| 深度长文 | `classic-serif` 经典衬线 |
| 科技、AI、编程 | `cyber-neon` 赛博霓虹 |
| 生活、美食、旅行 | `coffee-mocha` 咖啡摩卡 |
| 商务、财经、职场 | `ocean-blue` 海洋蓝 |
| 品牌、生活方式、情感 | `sunset-warm` 日落暖橙 |
| 传统文化、诗词、人文 | `ink-wash` 水墨山水 |
| 环保、自然、健康 | `forest-deep` 森林深绿 |
| 创意、设计、艺术 | `royal-purple` 皇家紫 |
| 时尚、美妆、穿搭 | `sakura-pink` 樱花粉 |

## 公众号兼容铁律

| 禁用 | 替代方案 |
|------|---------|
| `display:flex` / `grid` | `<table>` + `<td width>` 均分布局 |
| `display:inline-block` 自制图形 | `●` 字符圆点、`→` 字符箭头 |
| `linear-gradient` 渐变 | 实色背景 |
| `<svg>` 装饰 | CSS border 或字符 |
| `data:image;base64` 内嵌图（发布版） | CDN 外链图片 |

**必须做**：正文每个文字节点包在 `<span leaf="">` 里 —— 公众号编辑器只保留 leaf 内的文字样式，
漏包粘贴后样式大面积丢失。Inkwell 输出的每一段文字自动包裹。

## Environment

Inkwell 本身只需 `pip3 install "inkwell-press==0.8.1"`，以下环境变量**可选**：

| 变量 | 用途 | 必需性 | 数据影响 |
|------|------|--------|---------|
| `GITHUB_TOKEN` | 图片上传 GitHub Contents API → jsDelivr CDN | 仅 CDN 外链需要 | 配了此变量，图片会**上传到公网** |
| `WECHAT_APP_ID` | 公众号草稿箱 API | 仅 `publish --target wechat` 需要 | 配了此变量，内容会**发送到微信** |
| `WECHAT_APP_SECRET` | 公众号草稿箱 API | 仅 `publish --target wechat` 需要 | 同上 |
| `INKWELL_GITHUB_REPO` | 图片仓库 `owner/repo` | 可选 | — |
| `INKWELL_CDN_BASE` | 图片外链前缀 | 可选 | — |

**不配置任何环境变量时，Inkwell 不会上传图片或推送草稿** —— 但注意，
如果正文里**包含外链图片**（`http://`/`https://`），`run` 默认会下载这些图片以生成本地预览版，
这会产生出网请求。加 `--no-embed-external` 可彻底禁止所有出网行为。

### 公众号草稿箱前提

- 仅**服务号**可用（订阅号无草稿箱接口权限）
- 调用方**出口 IP 必须在公众号后台 IP 白名单**里，否则 40164
- 使用最小权限凭证，避免继承不相关密钥

## Errors

| 症状 | 原因 / 修复 |
|------|------------|
| `pip install inkwell` 装到了 Qt 主题包 | 改用 `pip install inkwell-press` |
| 图片全是 base64、没有 CDN 外链 | 三项配置（token + repo + cdn-base）缺一，CLI 会提示缺哪项 |
| 粘贴到公众号后图片变乱码 | 不要直接粘含 base64 的 HTML，打开 `_预览.html` 在浏览器里全选复制 |
| 公众号草稿推送报 40164 | 出口 IP 不在白名单，到公众号后台添加当前 IP |
| `validate` 报「无 `<span leaf>` 包裹」 | 用 Inkwell ≥ 0.8.1 重新生成 |

## 与同类工具的区别

| 工具 | 覆盖环节 |
|------|---------|
| doocs/md、mdnice | 仅排版 |
| xiaohu-wechat-format | 仅排版 |
| **Inkwell** | **排版 + 图片 + 封面 + 卡片 + 合规 + 草稿发布**（全链路） |
