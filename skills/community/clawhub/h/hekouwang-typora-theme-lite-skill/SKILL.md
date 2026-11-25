---
name: hekouwang-typora-theme-lite-skill
slug: hekouwang-typora-theme-lite-skill
displayName: Typora 主题工程 · Lite（hekouwang）
summary: Typora theme engineering / CJK long-form markdown — tokens.json CSS build, color sampling, contrast/layout audits, font probe. Free V2 light+dark.
license: MIT
homepage: https://github.com/huiyonghkw/hekouwang-typora-theme-lite-skill
version: 2.0.4
description: "当需要改 Typora 主题配色/字号/行高、用 tokens 生成 CSS、采样真实色值、排查主题不生效或发布主题库时使用"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Typora 主题工程（Lite）

本文件是仓库根上的 **Lite** Skill 入口（`hekouwang-typora-theme-lite-skill`）。
clone / 打开本仓后直接读根 `SKILL.md` 即可；本仓不维护 `.claude/skills` / `.cursor/skills` 项目内软链。
工作区：`scripts/`、`theme/`、`demo/`。目录约定见 [`STRUCTURE.md`](STRUCTURE.md)。

**授权：** Lite Skill 文本与免费主题 / 脚本均为 **MIT**（根 `LICENSE`；说明见 [LICENSE.txt](LICENSE.txt)）。
专业版六套走私有仓 / SkillPay zip（`hekouwang-typora-theme-skill`），本仓不含付费源码。

> **从 ClawHub / SkillHub 安装的**：平台包可能不含完整 `scripts/` 工作区。
> 先 `git clone https://github.com/huiyonghkw/hekouwang-typora-theme-lite-skill.git`，下文命令均在仓库根执行。

## 30 秒速览

- **主题产物（本仓 · 免费）**：`theme/hekouwang.css` + `hekouwang-dark.css`（= V2 编辑）
- **付费六套**（V1/V2 Pro/V3–V6）：专业版 zip / 私有仓；`./scripts/unlock.sh 包.zip`。付费 V2 Pro ≠ 免费 V2。
- **别手改 CSS**，它是生成物。
- **改哪个文件**（⚠️ 改错 = 静默失败，全绿但不生效）：
  - 改**排版**（行高 / 字号 / 段距 / 栏宽 / 断点）→ `scripts/tokens.json` 的 `_presets.work`
  - 改**配色 / 纸感 / 圆角 / 语法色** → `scripts/palettes.json`
- **开源仓库**：https://github.com/huiyonghkw/hekouwang-typora-theme-lite-skill （免费 V2 · MIT）
- **专业版购买**：支付宝 SkillPay · https://skillpay.alipay.com/shelf/product?productId=P0806000213890180&merchantCode=huiyonghkw （说明见落地页 `#buy`）

## 常用命令

```bash
python3 scripts/build.py --tier free        # → 仅免费 V2
python3 scripts/build.py                    # → 同 free（本仓无 edition）
python3 scripts/test_contrast_check.py     # → 7 个单测（对比度数学 + 出货 CSS）
python3 scripts/verify_layout.py --all      # → 免费 2 + 付费 12 套 × 7 档窗口、窄屏与表格预检
python3 scripts/verify_export_pdf.py        # → A4/A5、长代码与长表 PDF 预检
./scripts/install.sh                        # 装进 Typora（有 edition 时顺带付费 12 套；--free-only / --paid）
python3 scripts/verify_render.py --css theme/hekouwang.css \
  --fonts "Hekouwang Sans,Hekouwang Sans Fb" --vars bg-color,text-color
```

**依赖**：`python3`（必需）、`google-chrome`（两个 verify 脚本要）、
`pillow`（只有 `sample_colors.py` 读图要；`--solve-alpha` 不需要）。

## 铁律（这几条踩过，全是静默失败）

1. **改完 CSS 必须 `Cmd+Q` 完全退出 Typora 再重开。** 切换主题**不会**重新加载被修改的
   CSS 文件。不这么做，你会在一个用户根本没看到的版本上反复调参数。
2. **备份绝不能留在 themes 根目录。** Typora 把根目录下任何文件名含 `.css` 的文件都列进
   主题菜单，**包括 `.` 开头的隐藏文件**。安装脚本现在不自动备份；如需自己留副本，必须进子目录。
3. **编辑区零 `!important`**。常规规则靠 `#write` 特异性；仅导出段为覆盖 Typora 的打印基础样式而使用。构建时断言。
4. **除根字号外零 `px` 字号**，否则 Typora 偏好里的字号调节失效。构建时断言。
5. **配色基色不许猜，要采样。** 构建会对承担文字和控件信息的颜色做最小对比度校正，并审计所有生成变体。
6. **headless 全绿 ≠ Typora 里对。** 系统 Chrome 比 Typora 内嵌的 Chromium 新得多，
   最终验收必须在 Typora 里肉眼看。
7. **改完确认"你改的字段真被用上了"。** 构建全绿不代表改动生效——历史上
   `tokens.json` 顶层的 color / paper / type / layout 会被 palette 整体覆盖，
   改了不生效而构建全绿、断言全过。现在顶层放错段会被构建直接拦下，
   但"改了个存在却没被用的字段"仍要自查：

   ```bash
   python3 scripts/build.py >/dev/null && grep -o '你的新值' theme/hekouwang.css | head -1
   ```

   grep 不到 = 改错地方了。
8. **`:has()` 不能嵌套。** `a:has(.x):not(:has(> p:not(:has(.x))))` 这类写法
   会被浏览器**整条丢弃**（实测：嵌套写法 parsed=false，平坦写法 parsed=true），
   页面照常渲染、只是那条规则凭空消失。2.0.1 修过一处这种写法。写 `:has()` 用平坦写法。

## 采样，不要猜配色

做浅色版时我笃定页面底色是品牌米色 `#faf9f5`，采样后发现对话区是 `#fdfdfc` ——
`#faf9f5` 是**窗口/侧边栏**色，两者角色搞反了。深色版更极端：**深色下侧边栏比正文区更亮**，
与浅色模式的关系完全相反，靠"把浅色取反"推演一定会做错。

```bash
python3 scripts/sample_colors.py 参照截图.png                      # 按常见布局给候选
python3 scripts/sample_colors.py 图.png --box 700,640,1700,700 --label 正文背景
python3 scripts/sample_colors.py 图.png --text-box 690,300,1500,345 --label 正文文字
# 反解叠加色：底色 结果色 候选色 —— 三通道 alpha 一致的那个才是真的
python3 scripts/sample_colors.py --solve-alpha 1f1f1e 272725 ffffff,d97757
```

最后那条是判断"某个底色是品牌色浅铺还是中性叠加"的可靠办法。实测深色行内代码底：
白色叠加解出 0.036/0.036/0.031（一致 ✅），品牌橙解出 0.043/0.091/0.123（不一致 ❌）。

## 验证字体是否真的上屏

字体不生效**不会报错**，页面照常渲染、只是悄悄换成系统字体。判据必须带 fallback 基准：
量一个**不存在的字体**得到基准宽度，任何字体只要等于基准就说明它没生效。

```bash
python3 scripts/verify_render.py --css theme/hekouwang.css \
  --fonts "Hekouwang Sans,Hekouwang Sans Fb,Hekouwang Mono"
```

字体没生效的三个常见原因（都遇到过）：`format()` 用了 `truetype-variations` 这类非标准值导致
整条 `src` 被丢弃 / 字体栈里的族名与 `@font-face` 的 `font-family` 不一致（**改名时最常见**）/
`src` 相对路径写错（基准是 CSS 文件所在目录）。

## 按需展开

| 要做什么 | 读哪份 |
|---|---|
| 改配色 / 字号 / 行高 / 紧凑度（先看"改哪个文件"表） | [references/tokens.md](references/tokens.md) |
| Typora 选择器地图、官方规范、七个静默坑 | [references/typora-spec.md](references/typora-spec.md) |
| 字体策略、授权红线、三级降级 | [references/fonts.md](references/fonts.md) |
| 做一套全新主题 / 加变体 / 发布到主题库 | [references/workflow.md](references/workflow.md) |
| 目录与 Pro / Lite 边界 | [STRUCTURE.md](STRUCTURE.md) |

## 目录

```
SKILL.md                 本文件（Lite 入口；仓库根）
references/              渐进披露
scripts/tokens.json      阅读指标真源（_presets.work）+ 字体栈 + 透明度阶
scripts/palettes.json    免费 V2 配色真源
edition/scripts/         付费色板 + craft（本地仓；不进公开 git）
scripts/build.py         默认：有 edition 则 free+paid；公开 CI 用 --tier free
scripts/pack.sh          打专业版 zip → dist/<version>/…-paid.zip
scripts/unlock.sh        买家装付费 zip；开发树同步回 edition/
scripts/install.sh       装进 Typora
scripts/sample_colors.py 从截图采样真实色值
scripts/contrast_check.py / test_contrast_check.py
scripts/verify_layout.py / verify_export_pdf.py / verify_render.py
theme/                   成品 CSS 与随包字体（Inter, OFL）
demo/                    验收样张
docs/                    GitHub Pages
materials/               本机运营物料（不入库、不进安装包）
```
