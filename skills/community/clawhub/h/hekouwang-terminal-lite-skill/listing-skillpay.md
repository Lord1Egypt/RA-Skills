# SkillPay 商品文案（仓库副本）

> 本文件只对应支付宝 SkillPay 专业版。ClawHub 是免费版，腾讯 SkillHub 是按次客户端；两者都不使用这份文案。
> 平台商品描述是手写字段，仓库之外没有第二个来源。改版本前先比对这里。
> 本文件与 `materials/` 不随安装包分发。

## 商品名称

会勇禾口王 · 终端工作台（专业版）

## 商品描述（422 字，平台上限 500）

```text
会勇禾口王·终端工作台（专业版）是 macOS 终端观感与效率方案：把 iTerm2、Ghostty、Warp、Tabby、VS Code、bat、fzf、eza、delta、tmux 收束到同一色板，换一次主题全链一起变。专业版含 4 套品牌主题（含 2 亮色）、共 7 套；iTerm2、Ghostty、Terminal.app 覆盖 7/7，Warp、Tabby 5/7。支持多终端与全生态同色、光学校准、5 个场景、项目工作区、色板推导与跟随系统深浅色；换肤可 --plan 预览、--rollback 回滚，doctor 可体检。安装：先装免费版 Lite（3.0.5+），解压覆盖后运行 config/themes/_generate.py，再执行 ./scripts/theme.sh ember。¥14.9/季度，不自动续费，约 ¥59.6/年。适合多终端、投屏、录屏用户；不含后端、密钥与许可证校验，卸载可逐项确认并还原配置。
```

## 补充商品介绍（最多 4 条，3 文字 + 1 图片）

平台弹窗规则：最多 4 条；文字每条 500 字；图片支持 PNG / JPG / WebP，单张不超过 5 MB。

### 材料 1 · 文字（362 字）

```text
会勇禾口王·终端工作台（专业版）解决的是一件事：让 iTerm2、Ghostty、Terminal.app、Warp、Tabby 与 VS Code、bat、fzf、eza、delta、tmux 共用同一份色板。免费版自带 3 套社区主题；专业版再加 ember、voltage、parchment、ledger 4 套品牌主题，合计 7 套。iTerm2、Ghostty、Terminal.app 覆盖 7/7，Warp、Tabby 覆盖 5/7。换一次主题，整条命令行工具链一起变，不会出现终端深色、编辑器旧配色、git diff 另一种绿的割裂感。换肤前可用 --plan 预览改动清单，不满意可 --rollback 回滚到上一份快照；doctor --status 逐项体检主题、字体、Node 管理器与生态配色。
```

### 材料 2 · 图片

`materials/skillpay/01-hero-2880x2000.png`

官网首屏：标题、¥14.9/季度、Voltage 主题终端实景、7 套主题圆点。2880×2000，410 KB。

备选：`materials/skillpay/02-pricing-2880x2000.png`（三档价格同屏，611 KB）。只能占用一个图片位，优先首屏。

### 材料 3 · 文字（242 字）

```text
专业版把「同一字号」升级成「跨终端同一观感」：按字体字格、中文两格宽与 compact / comfortable / present 三档密度，为 iTerm2、Ghostty 分别计算字号、行高与留白。5 个场景一键切换：日常、专注、投屏、录屏、远程；投屏与录屏会去掉透明与模糊、放大字号、隐藏家目录路径、关闭闪烁光标。项目工作区在 cd 进入目录时自动换色并印出项目名，几个 Agent 标签同时跑也不会认错。还能跟随 macOS 深浅色自动切换。所有改动先计划后执行，可回滚。
```

### 材料 4 · 文字（273 字）

```text
安装：先装免费版 Lite 3.0.5 或更新版本，再把专业版压缩包解压覆盖到 Lite 目录，运行 config/themes/_generate.py 重新生成主题，最后执行 ./scripts/theme.sh ember。授权为按季度订阅，¥14.9/季度，不自动续费，约 ¥59.6/年；授权期内可获取版本更新与 GitHub Issues 答疑。包内不含后端服务、密钥或本地许可证校验。卸载为交互式逐项确认，可还原 .zshrc、starship.toml 与 Ghostty 配置。不适合只想要一张静态配色、或不需要终端工具链的人。
```

## 售卖设定

| 项 | 值 |
|---|---|
| 售卖模式 | 订阅制（选定后无法更改） |
| 订阅周期 | 每季度，不支持自动续费 |
| 价格 | ¥14.9/季度（平台允许 8.99–50） |
| 免费试用 | 0 次（不设试用） |

## 发版与上架核对

1. 包内能力有变化 → 先改本文件，再改平台。顺序反了就是拿旧描述送审。
2. **上传新包会重置商品名称与描述**：平台按包内 `SKILL.md` 的 `name`、`description` 覆盖。上传后回基本信息确认名称仍是中文，并重新粘贴商品描述。
3. 只加「补充商品介绍」时不要重传安装包；提交补充材料会重新走一次审核，审核期间商品仍按当前线上版本展示。
4. 描述与补充材料里的每条能力都要在包内找得到落点：主题见 `config/themes/`，光学见 `config/typography/`，场景见 `config/scenes/`，工作区见 `scripts/workspace.sh`，跟随系统见 `scripts/theme.sh --auto`。
5. 价格与周期以平台后台为准，本文件只记录口径。
