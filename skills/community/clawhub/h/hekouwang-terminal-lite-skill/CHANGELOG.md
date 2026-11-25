# 更新日志

> 公开版更新日志：只记**你用得到的变化**。
> 付费包另有一份完整版，逐条记着每个坑是怎么调出来的。

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

> **路径说明**：2.x 起脚本移入 `scripts/`；下面旧条目里的 `./theme.sh` 等路径按当时布局书写，勿照抄。

---

## [3.0.6] · 审核披露对齐（2026-11-19）

### 变更

- description：写明全量 doctor 为测启动耗时会多次以交互式 zsh 加载 `~/.zshrc`；`--status` 跳过该段；`--profile` 改为「临时 ZDOTDIR 的交互式 zsh + zprof」，不再写「登录 shell」

---

## [3.0.5] · 审核安全项收尾（2026-11-18）

### 修复

- 卸载：所有删除/还原项在交互模式下先询问（Apple Terminal Profile、`~/.gitconfig`、`~/.tmux.conf`、动态 Profile、运行时、Ghostty/bat/VS Code 主题等）；`--yes` 跳过确认执行默认档
- `sync.sh --export` 改用 `mktemp` 临时清单（600 权限），不再使用固定 `/tmp/.hkw-files.z`
- `transaction.py` 回滚只允许管理目录内的路径，manifest 被篡改也无法越界删文件；路径统一 `expanduser`
- 免费包不再包含 launch agent 清理块

### 变更

- description 写明 `doctor --profile` 会加载 `~/.zshrc` 取样；卸载改为「交互模式先询问」
- SkillPay 计费周期改为每季度 ¥14.9（平台不支持年付；约 ¥59.6/年，不自动续费）

---

## [3.0.4] · 审核一致性收尾（2026-11-18）

- 卸载：先快照安装清单再删运行时，brew 包现在真按清单卸；删 `~/.config/starship.toml` 前先还原安装时的最新备份
- description 补全：Shell Integration 未执行会继续后续步骤、`update.sh` 的 git fetch/pull、Ghostty `ssh-terminfo` 的远端 terminfo、卸载的完整范围
- Lite 文档统一改称「换机迁移」；免费版文档不再出现专业版跟随系统命令
- metadata 补 `git` 依赖

---

## [3.0.3] · 声明与行为对齐（2026-11-18）

- `sync --pull` 与 `update` 覆盖 starship.toml 前做时间戳备份
- 安装记录 brew 清单，卸载只删清单内的包
- oh-my-zsh 未执行时停止；Shell Integration 未执行时保留下载文件
- atuin 历史导入改为 `HKW_ATUIN_IMPORT=1`
- 免费包移除跟随系统，该能力保留在专业版

---

## [3.0.2] · 声明与行为对齐（2026-11-18）

- 远程安装改为「下载 → 打印 SHA-256 → `HKW_ASSUME_YES=1` 才执行」
- `setup-cli` 改为 `--config` 显式传入，不再探测 CLI 配置目录
- 卸载只删 `find` 命中目录；starship 覆盖前先备份

---

## [3.0.1] · 安全审查修复（2026-11-18）

- 免费包剔除站点资产与维护者工具：108 → 90 个文件，安装后不再带官网页面、测试和发版脚本
- SKILL 描述如实声明可选能力：专业版包安装、换肤回滚、P3 广色域、只读检测 AI CLI 设置
- 下载脚本改为「先保存到文件、确认后再执行」，不再下载即执行
- 脚本引用统一加 `scripts/` 前缀；功能不变

---

## [3.0.0] · 专业版首发

- 专业版走平台购买：支付宝 SkillPay 按年（¥59.9/年，不自动续费）、腾讯 SkillHub 按次（¥2.99/次）
- 购买入口改为平台渠道，不再以微信发货为主路径
- 免费版更名为 Lite（`hekouwang-terminal-lite-skill`）
- 官网重设计：能力对照表 + 场景故事，说清免费版与专业版差异

---

## [2.13.0] · 视觉层与 P3（2026-11-13）

- 品牌主题改用英文名：Ember（暖黑暗）、Voltage（霓虹科技黑）、Parchment（暖纸亮）、Ledger（财经白）；旧名仍作为别名可用
- 视觉审计新增选区 / 搜索命中 / 光标 / 亮底中性槽 / 暗字 / 色相区分度：不再只审 16 个 ANSI 槽
- 视觉审计新增 diff 新增/删除底的明度差与红绿色盲分离度；diff 底改成 19%/10% 不对称配方，灰度/色盲下也能分开
- iTerm2 Triggers 改用语义表面：error / warn / success 的背景按主题解算，文字 ≥4.5:1，不再直接拿 raw ANSI 红黄绿当底
- 中性梯：`neutral_ramp` 解出 surface / overlay / border / muted 四档，预览标题栏和代码块改用设计过的 surface；审计新增 `neu` 列
- iTerm2 Cursor Guide 启用，颜色取中性梯 `border`；daily / focus / remote 开，present / record 关
- 社区主题补签名 accent：Catppuccin peach、Gruvbox orange、Rose Pine rose、Tokyo cyan；cursor / badge / tab 不再等于前景色
- P3 广色域：`./theme.sh <主题> --p3` 把 iTerm2 Profile 转成 Display P3；彩色槽扩彩度，背景/前景/中性色只做 P3 等价表示
- 审计新增「语法色 × diff 行底」≥3:1 检查（comment 除外）；新增 `tests/test-p3.sh` 覆盖打开/回退
- Ember 取消专用字体覆盖，九套主题统一按 `font.conf` 优先级取字体
- 9 套色板提彩：只放大 OKLab 彩度、不动色相，主题列表和投屏里更容易一眼分开
- `claude-code-light` 的 ANSI 7 从 1.19:1 提到 3.04:1，ANSI 0 与 15 不再是同一个颜色
- 亮色主题选区从 1.19–1.29 提到 1.40 左右；v1 / tokyo 选区也补到 1.5
- 搜索命中改成按「对背景可见、对正文可读」解算，catppuccin / tokyo 的 3.07 / 3.81 提到 4.5+
- `./setup-cli.sh`：检查 CodeBuddy / Claude Code 是否在用 ANSI 主题，并可带备份切到非 ANSI 的 Dark / Light
- `./setup-gui.sh` 新增复制即选、三击选折行、标签页新输出指示

---

## [2.12.0] · 色板视觉地板

- 社区色板生成时统一过视觉地板：只调 OKLab 明度、保住色相，catppuccin-mocha 与 tokyo-night 各 6 对 normal / bright 同色已分开，`ls` 与 `git diff` 的强调层恢复可辨
- gruvbox-dark 的 red 从 2.69:1 提到 4.55:1，错误提示不再糊在背景里
- 新增 `./theme.sh --audit`：只读体检对比度地板 / 明暗分档 / 暗字槽，换肤前先看色板站不站得住；`./doctor.sh --status` 与 `./release.sh --check` 同步接入
- `./setup-gui.sh` 补上 iTerm2 全局窗格边距——左右 10pt / 上下 8pt，运行前需先退出 iTerm2
- 付费档同期：光学档新增 CJK 等宽层（中文与图标同字号，CJK 正好两格），`font.sh verify` 按真实字体度量打分；场景补 Ghostty 窗口内边距，自动补全的幽灵文字改跟主题暗字槽

---

## [2.11.0] · 换肤可回滚、结果可验收

- 换肤前可用 `--plan` 看管理范围；正式切换自动留快照，失败自动恢复
- `--rollback / --history` 可恢复或查看最近 5 次换肤快照
- `doctor.sh --parity` 对照源主题验收 iTerm2；付费版扩展到六终端与工具链
- 付费 zip 更新增加版本门、更新前快照与失败恢复

---

## [2.10.8] · 六终端说明页（公开可见）

文档站「四终端」升格为「六终端」：对照表与落地页标明付费档同步 iTerm2 · Ghostty · Warp · cmux · Tabby · 自带终端。开源版仍只同步 iTerm2。

## [2.10.7] · README 主 CTA 指向产品主页（公开可见）

仓库 README 顶栏主链改为产品主页；文档站退为次链。产品叙事以 Pages 主页为准。

## [2.10.6] · 标题字重对齐（公开可见）

文档站重跑字体子集（含拉丁）；标题中英同族，Hero 渐字不再比黑字细。

## [2.10.5] · 落地页徽章归位（公开可见）

Hero 预览卡上的 `1 palette` 收到标题栏右侧。

## [2.10.4] · 落地页 Hero + 功能卡（公开可见）

主页改成左文案 / 右预览 + 六格卖点卡（结构参考常见产品站，仍用 OneLook V1 色板）。

## [2.10.3] · README 对齐文档站简介（公开可见）

仓库 README 开头与文档站「为什么是 OneLook」同文案：文档地图 + 开源/付费分界，并链到 Pages。

## [2.10.2] · 四终端说明进文档（公开可见）

新增「四终端」文档页：iTerm2 · Ghostty · Warp · 自带终端，开源/付费各拿到什么、什么仍是 iTerm2 独家。

## [2.10.1] · 选肤预览进文档（公开可见）

文档站展示 `./theme.sh` 的 fzf + ANSI 选肤界面截图（换肤页 / 画廊 / CLI）。

## [2.10.0] · 体验小改（公开可见）

- `./theme.sh`：fzf 模糊选 + ANSI 预览（无 fzf 仍出画廊）
- `./doctor.sh --fix`：按组问修
- `./sync.sh --state-export` / `--state-import`：换机钉住状态

## [2.9.4] · 脚本完整操作手册（公开可见）

文档站「CLI 与脚本」页：每个开源脚本的完整用法（含 dry-run / 撤回）；付费脚本只写命令形态。

## [2.9.3] · 文档站语言跟链（公开可见）

中文模式下点侧栏不再闪回英文；链接带 `?lang=`。安装行为不变。

## [2.9.2] · 文档站导航修复（公开可见）

文档页顶栏不再塞满子链；侧栏 + 语言切换恢复。安装行为不变。

## [2.9.1] · 货架名 OneLook（公开可见）

产品展示名：**OneLook**（把「同色」做成「同观感」）。  
仓库仍叫 `hekouwang-terminal-kit`；落地页与 README 标题已换。安装 / 卸载行为不变。

## [2.9.0] · 语义交互层 v1 · doctor 状态机（公开版可见的变化）

**语义交互层 v1（随 Profile 交付）**  
换肤后**新开 tab**：Cmd-click `path:line`、Git SHA、`localhost:port`；四击按 Smart Selection 选中。  
Semantic History 走本机最佳编辑器。

**doctor 状态机仪表盘**

```bash
./doctor.sh --status
```

一眼看：theme / auto / node / optical·scene（付费才有值）/ semantic / Ghostty 是否需重载。

## [2.8.0] · Node 自选 · 跟随系统默认关 · 备份归目录（公开版可见的变化）

开源版与付费版共用这三条（不涉及付费档能力）：

**Node 管理器四选一**  
装机可选 `fnm`（默认）/ `nvm` / `brew` / `vfox`，或装完跑 `./node-mgr.sh <名字>`。  
选择写在 `~/.config/hekouwang-terminal/node.sh`，`.zshrc` 只 source 那一份；**只留一套，别混用**。

```bash
./install.sh --node vfox
./node-mgr.sh fnm
```

**跟随系统深浅色：默认关，现为专业版能力**  
2.x 曾默认关闭但可用；3.0 起只在专业版提供，免费版没有这个命令。手动 `./theme.sh <主题>` 会钉住该主题，避免「配了黑色被系统浅色顶回白色」。

**.zshrc 备份进专用目录**  
不再往家目录根丢 `~/.zshrc.bak.*`。统一进 `~/.hekouwang-terminal-backups/`；装机时会把旧散落文件收进去。卸载不会误删这份还原历史。

## [2.7.1] · 窗口水印可自定义（公开版可见的变化）

- 付费档场景引擎新增 `./scene.sh badge <文字>`：iTerm2 窗口右上角的水印写自己的名字或项目名，
  钉住之后跨场景、跨换肤都跟着走，`off` 清掉
- 开源版行为不变：`scene.sh` / `config/scenes/` 仍只在付费包里

## [2.7.0] · 场景美学引擎（公开版可见的变化）

- 付费第二柱落地：**场景美学引擎**（`./scene.sh`）  
  日常 / 专注 / 投屏 / 录屏 / 远程一键切气质；开源版行为不变
- 开源版不包含 `scene.sh` / `config/scenes/`（与 `font.sh` 同分档）

## [2.6.0] · 产品三柱定位（公开版可见的变化）

- 付费产品正式立名三柱：**终端光学校准引擎**、**场景美学引擎**、**语义交互层**  
  总定位：把「同色」做成「同观感」
- 开源版行为：仍是完整 iTerm2 换肤；光学校准 / `font.sh` / 光学档目录只在付费包
- 主题生成器与社区三套默认视觉不变

## Docs · README 主路径 + manual 进阶（无版本号变更）

- 仓根 README（中/英）恢复完整主故事：对比图 → 痛点 → 差异 → 分档 → 安装 → 颜值 → 日常命令 → 换肤 → 维护（约 280–320 行）
- `docs/manual*` 保留进阶、FAQ、设计原则、文件级分档与长说明；不再要求路人先读手册
- 付费实现（Skill / 品牌色板 / 多终端生成器等）仍不进公开仓

## [2.5.1] · 主题生成器支持状态层字段

- 色板可选 `bold` / `matchbg` / `faint_text_alpha` / `surfaces`：自定义主题可单独定粗体、搜索命中、弱化字透明度、diff 表面色
- 社区三套默认视觉不变；品牌主题的可读性微调在付费包

## [2.5.0] · 标签页改成「一块画布 + 一个圆点」

- **变更：标签页不再按项目染底色**，改成在标题前挂一个彩色圆点（像 VS Code / Zed
  的项目色点）。一整条顶栏被刷成高饱和色块，跟窗体明显不是一家；现在顶栏永远跟
  窗口底色走，也就是 Minimal 主题本来的「整窗一块画布」。常驻项目可以在
  `~/.zshrc` 的 `HKW_TAB_DOT` 里钉死圆点，没钉的按仓库根路径哈希取一个 ——
  同一个仓永远同一个点
  - ⚠️ **升级不会动你已有的 `~/.zshrc`**（安装脚本从不覆盖你的配置）。想要这个效果，
    照 `config/zshrc.template` 里的 `_hkw_title` 手工换一下那一段
  - ⚠️ 换完之后，已经染过色的标签页要**再画一次提示符**才会恢复（回车一下或新开标签）：
    标签色是 iTerm2 的**会话级状态**，光把染色代码删掉，旧颜色会一直挂着
- 🐞 修：安装那一节的 `doctor.sh` 截图拍的是**付费档**的机器（第 5 节「全生态同色」
  八行全绿），而开源版那一节本来就不会全绿。已在图下写明，免得你以为自己装坏了
- 🐞 修：安装流程那行写着「主题与**全生态配色**」—— 全生态同色是付费能力，
  开源版只同步 iTerm2。跟当初 `install.sh` 收尾吹「连 bat/fzf/git diff 一起换」同一个错
- 剔掉一张公开仓用不上的截图（付费功能的项目工作区图，只有付费版首页在用）
- 顶部两个 badge（四终端 / 一份色板管全工具链）改成明标「付费档」，
  并补一个「开源版＝配好的 iTerm2 · MIT」的绿标 —— 第一屏就该看得出哪句属于哪档
- 付费包 zip 现在把 `VERSION` 一并打进去：以前老版本免费仓解压新付费包之后，
  树里根本没有 VERSION，`update.sh` 会静默打「版本未知」。`unlock.sh` 另加一句提醒：
  本地版本与包里版本不一致时告诉你先 `git pull`
- 发版脚本新增 `--release`：GitHub Release 的发布说明直接取自这份更新日志的同名小节，
  不另写一份对外文案。公开仓的 Release 页以前也是手发的，2.3.0 / 2.4.0 都漏了

## [2.4.0] · Claude Code Skill 归付费档

- 发版脚本新增 `--tag`：版本号从 `VERSION` 取，母版与两个子仓一条命令打齐并推送。
  以前 tag 是手打的，2.3.0 / 2.4.0 连着两版都没人记得打（线上最后一个 tag 停在 2.2.0），
  已回补 v2.3.0
- **变更：Claude Code Skill 归付费档。** 开源版不再带 `SKILL.md`，
  「装进 `~/.claude/skills/` 让 AI 驱动整套」从这一版起属于付费包。
  **开源版没有任何功能因此少掉**：脚本一个不少、参数一个不改，
  只是由你自己敲 `./theme.sh` / `./doctor.sh` / `./migrate.sh`，而不是让 AI 替你挑
- 新增仓根 `VERSION` 文件当版本号唯一真相源。以前版本号读的是 `SKILL.md` 的
  frontmatter，那个文件走了之后 `update.sh` 会安静地打「版本未知」——
  功能没坏、也没有任何报错，但你看不出自己在哪一版。已连同一道校验门一起补上

## [2.3.0] · 项目主页与「怎么买」

- 新增项目主页 <https://huiyonghkw.github.io/hekouwang-terminal-kit/>：
  免费/付费对比图、分档表、怎么买、七天退款、能力边界，中英双语。
  支持微信支付与支付宝；页面零 CDN，中文字体是自托管子集（102 KB），墙内也能瞬间打开
- 🐞 修：主页中文标题字重是假的 —— 系统的 PingFang SC 最粗只到 Semibold，
  `font-weight:900` 在它身上不成立，标题一律发虚。已换成带完整字重轴的自托管字体
- `theme.sh` / `doctor.sh` / `install.sh` 在开源版下各多打一行，说明付费档在哪儿。
  只有一行、只在付费件缺席时打；装了付费包之后一句都不会出现
- 🐞 修：发版脚本 `--update` 用的 `rsync -a` 会静默漏发**等长**改动
  （版本号升位、改一个字符的 typo），已改成按校验和比对
- 🐞 修：**这份更新日志以前根本没进过公开仓**（导出脚本的 `.gitignore` 把它自己
  生成的这份忽略掉了，全程零报错）。所以 2.3.0 之前没有历史记录，不是没改过
- 🐞 修：`install.sh` 装完的收尾写着「换肤（连 bat/fzf/git diff 一起换）」，
  但开源版只同步 iTerm2，工具链同色是付费能力。这行文案说的不是开源版能做到的事，
  已改成「换肤：./theme.sh」

## [2.2.0]

**语言：默认英文，可切中文**

- 全线脚本、生成器、模板的对外文案默认英文；`--lang zh` 或 `HKW_LANG=zh` 切中文
- `install.sh` 首次交互安装时问一次语言并记住（`~/.config/hekouwang-terminal/lang`），
  之后所有命令跟着走；非交互运行永远不卡在这个问题上
- 文档双语并列：`README.md` / `README.zh-CN.md`、`SKILL.md` / `SKILL.zh-CN.md`
- `.zshrc` 模板分语言（`config/zshrc.template` / `.zh`），落进你家目录的注释是你选的那种语言
- 主题显示名分中英两套：产物里烧英文名，中文名在部署那一刻注入 ——
  两种语言共用同一套生成产物，不会有两份互相漂的 JSON
- 英文版模板里的 Homebrew 国内镜像改为默认注释掉（在国外网络上它只会更慢）

**修复**

- `migrate.sh` 自动回滚现在真的还原 `~/.zshrc.local`：以前 `$LOCAL_BAK` 从没被赋值，
  追加进去的内容永远留着，回滚是假的
- `uninstall.sh --dry-run` 不再谎报「已还原 ~/.zshrc」——它一个字节都没动
- `uninstall.sh` / `install.sh` 认 Ghostty config 与自带终端 Profile 时中英两种标记都认，
  换语言重装后不会漏删、也不会每次多备份一份
- `install.sh` 里 `setup-gui.sh` 失败不再把整个安装带走

---

## [2.1.0]

**换肤**

- 换肤回执改成分组（终端 / 工具链），一眼看清哪些真生效了、哪些跳过了
- `./theme.sh --preview <名字>` 出一整块「假终端」：提示符、文件列表、git diff、
  语法高亮、ERROR/WARN 标色都在一张图里，不用真换肤就能挑
- `./theme.sh --gallery` 把全部主题挨个渲一遍
- 标题栏默认与背景同色，整窗一块画布

**主题**

- 主题生成器新增旧产物清理：移除一套色板后，它留下的文件会一并清掉，
  不再永远赖在目录里

**修**

- 修 iTerm2 在 GUI 里编辑过 Dynamic Profile 后，文件被回写成存根导致换肤失效
- 修 `Send text at start` 被 GUI 手滑写入后，每开一个 tab 都自动敲一行命令，
  换肤/重装都清不掉（Dynamic Profile 只覆盖 JSON 里出现过的键，现已显式声明为空）

## [2.0.0]

**这一版把「一台配好的 iTerm2」做完整了。**

- **Minimal 窗口形态**：无标题栏 · 无边框 · 无滚动条 · 无限回滚
- **配色**：3 套社区主题（catppuccin-mocha / tokyo-night / gruvbox-dark），
  走同一份色板生成，改色只改一个文件
- **质感层**：毛玻璃 · 透明度 · 光标形态
- **Triggers**（随 Profile 交付，不用手点 GUI）：ERROR / WARN / SUCCESS 自动标色，
  密码提示自动弹密码管理器
- **`Shift+Enter` 换行不提交**：给 AI CLI 写多行 prompt 用
- **现代 CLI 全家桶**：eza / bat / fzf / fd / zoxide / ripgrep / atuin / delta
- **`./migrate.sh`**：接管已有 `.zshrc`（搬进 `.zshrc.local`，**不是覆盖**）。
  按段落判定，写入前 `zsh -n` 验语法，写完真起一个 shell 验，起不来自动回滚
- **`./doctor.sh`**：只读自检；`--fix` 逐项修；`--profile` 用 zprof 点名慢插件
- **`./uninstall.sh`**：一键还原，`--dry-run` 先看清单。
  `.zshrc` 从备份**还原**而不是删掉；GUI 设置用 `defaults delete` 回出厂默认
- 全部写操作都能 `--dry-run` 预演

⚠️ **字体**：1.x 曾从第三方仓库拉 Operator Mono（商业字体）—— 自用是灰色地带，
随产品分发就是侵权。2.0 已移除，默认改用 Maple Mono NF CN（SIL OFL，可商用可分发）。

## [1.3.1] 及更早

早期版本的迭代记录（安装脚本、主题生成器、`.zshrc` 模板成型的过程）不在公开版列出。
从 2.0.0 开始是当前形态。
