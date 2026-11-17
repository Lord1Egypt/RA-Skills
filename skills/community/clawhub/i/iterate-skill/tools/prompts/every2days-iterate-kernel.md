# 每两日任务 · iterate-kernel（双向集成共享内核）

> 用法：由定时任务引用（任务名「iterate-kernel 每两日 审查+修复+发版+消费方追平」）。把下面「提示词正文」整段当成本轮指令。它是自足的——所有命令、判据、坑都写在里面，不依赖创建会话的上下文。

---

## 提示词正文

请对 `/Volumes/Eng-Dev/iterate-skill/kernel`（iterate-kernel，GlassPane 主仓、glasspane-harness fork、iterate-harness、iterate-plugin 四处消费方共用的 canonical 内核）执行每两日例行「审查 + 修复 + 发版 + 消费方追平」任务。**这是无人值守场景**：全程没有人在旁边，任何正常情况下需要决策的地方都由你自己判断并执行到底，不许中途停下来问，也不许留任何"待裁决/待补/下一轮再看"。

【无人值守：零遗留与全线发布授权（本节优先级最高）】

- **授权范围**：审查、改 `kernel/` 代码与测试、提交、推送 iterate-skill 仓 `origin main`、升内核版本线（0.1.x）、打 tag `v0.1.<X>` 并推、触发并观察 `.github/workflows/npm-publish-kernel.yml`（OIDC trusted publishing，带 `--provenance`）真发 npm、以及四处消费方 pin 的追平与按各仓口径的提交推送。这些都不必再问。
- **发现问题必须完全解决，只允许一种终态**：已修 + 有测试 + 已进 main +（若有实质改动）已发 npm + 消费方同轮追平。「判定不属于本轮」这个出口不存在。中间态一律不合格；半修（schema 加了字段而读侧没管、修了内核而消费方仍 pin 旧版且没人追平）比不修更糟。收口后还能存在的未完成项只有物理上做不到的那类，且必须写成一条可执行的人工动作。
- **内核无实质改动就不发版**：本轮审查后若没有需要改的缺陷/契约变化，不必为发而发——汇报里写明"本轮内核零改动，不发版"，这算合法收口，不算遗留。但只要改了 `kernel/src` 或 `kernel/schemas` 或 `kernel/fixtures`，就必须发版并追平消费方，不许"改了不发"。
- **替你做的决定要留痕**：取号判断（patch/minor）、修在哪一层、消费方追平与否，写进提交正文与汇报的「本轮我替你做了哪些决定 → 依据 → 回滚命令」一节。
- **范围纪律**：内核的职责是转录与校验（schemas、evidence→decision 转录、decision-log 哈希链、公共 validator），判定语义永远留在引擎/壳那一层——发现"内核在替消费者做判定"是缺陷，修回去，不是加更多判定。不得擅自扩大产品面（新增对外 entry、改产品定位）。

【审查范围】

- 主审：`kernel/src/**`（含 canonical-json、convergence、decision-log 链、evidence-decision、run-plan、provider-registration、recipe-config、dimension-context、parse、schemas、errors、各 entry）、`kernel/schemas/**`、`kernel/fixtures/**`、`kernel/test/**`、`kernel/package.json`、`kernel/tsconfig.json`、`.github/workflows/npm-publish-kernel.yml` 与 `ci.yml`。
- 附带审（只读不改，发现缺陷仍要本轮跨过去修）：四处消费方对内核的**使用方式**。四处形状各不相同，逐处都要核到：
  1. **GlassPane MCP 壳**（`/Volumes/Eng-Dev/GlassPane/mcp-shell`，TS）：`mcp-shell/package.json` 里 `iterate-kernel` 的**精确版本**依赖；GlassPane 仓根的 `kernel/{schemas,fixtures}` 不是第二真源，是从已安装包逐字节抄出的**被 pin 语料**，由 `scripts/check-kernel-corpus.mjs` 核（`--record` 只肯从装好的、与 pin 同字节的那份包里抄）。追平动作：改 pin → `npm install` → `node scripts/check-kernel-corpus.mjs --record`。
  2. **GlassPane harness fork**（`/Volumes/Eng-Dev/GlassPane/harness/glasspane-harness`，TS）：`packages/opencode/package.json` 的 `iterate-kernel` 依赖 + 两道闸 `script/kernel-pin.mjs`（依赖解析到的版本 == 声明的 pin）与 `script/kernel-conformance.mjs`（fork 侧使用与契约语义一致）。追平动作：改 pin → `bun install` → `node script/kernel-pin.mjs --record` → `bun script/kernel-conformance.mjs --record`。
  3. **iterate-harness**（`/Volumes/Eng-Dev/iterate-skill/harness/iterate-harness`，**Python，不装 npm 包，是内核语义的第二实现**）：`src/iterate_harness/iterate/*.py`（convergence_policy、evidence_transcription、kernel_decision_log/kernel_decision_record、dimension_context 等）用 Python 重实现契约；对齐靠 `tests/kernel_fixtures/`——从 `kernel/fixtures` 逐字节 vendored 的语料，`manifest.json` 钉 `package/version` 与每个文件的 sha256，`tests/test_iterate/test_kernel_fixtures.py` 强制 vendor==manifest，`scripts/check_kernel_fixtures.py` 与 `scripts/diff_kernel_implementations.py` 做**跨语言对拍**（Python 实现 vs 已发布 TS 包的 dist，拒收集合/决定/digest 逐项一致；版本与语料 pin 不符直接拒测，不许静默跳过）。追平动作：`npm pack iterate-kernel@<new>` → 逐文件拷进 `tests/kernel_fixtures/` → 重记 manifest 的 version 与 sha256 → 跑 `PYTHONPATH=src python3 scripts/diff_kernel_implementations.py` 与 `python3 -m pytest tests/test_iterate -q`；对拍红＝两边实现真分叉，那是内核改动的 bug，不是语料该放行。
  4. **iterate-plugin**（`/Volumes/Eng-Dev/iterate-skill/harness/iterate-plugin`，TS）：`package.json` 里 `iterate-kernel` 的**精确版本**依赖（写本文时是 0.1.9，落后 registry 一大截——首次追平先吃掉这个差），`src/tools/decision-log.ts` 等直接消费内核 entry（decision-log 落盘即内核哈希链）。追平动作：改 pin → `npm install` → 跑该仓自身套件（按它的 `package.json` scripts）→ 按它自己的发布口径决定是否随版本发出。
  - 四处版本号必须同号；任何一处落后 registry 最新版本身就是一条缺陷，本轮追平，不许列「待裁决」。`.release/` 下是两个发布仓的镜像，只读对照用，不手改。
- 禁区：`specs/**`（只可新增不改写历史）、`LICENSE`、`tools/prompts/**` 之外别在 iterate-skill 仓留下不属于本线的未提交批次、以及任何**别人正在飞的未提交改动**（见下）。

【开工前先确认工作树】

1. `cd /Volumes/Eng-Dev/iterate-skill && git status --porcelain`（整树，不只看 kernel/）并记开工 HEAD。本仓**常驻有别的线的未提交批次**（例如 harness 前端与 web 路由的活）——不混提、不 `git add -A`、绝不 `git checkout --`/`reset`/`stash`/`clean` 别人的文件；本轮只 `git add` 明确属于自己的路径（`kernel/`、`tools/prompts/`、`.github/workflows/npm-publish-kernel.yml` 及四处消费方的 pin 位点）。**未追踪文件会被并行会话的 `git clean` 洗掉**（`tools/prompts/every2days-iterate-kernel.md` 就这么消失过一次），所以本轮产出要么及时提交、要么落在既有追踪文件旁边并同批提交。若 dirty 状态影响到 kernel 的构建/测试（如共享 lockfile），改用 `git worktree add` 隔离工作树做本轮改动。
2. **先找上一轮没收口的活**：`git fetch origin --prune` 后列 `git branch -r --list "origin/*kernel*"` 与 `git worktree list`，逐条判定「已落地 / 被取代 / 真未落地」——判据只用文件字节（`git cherry` 对 squash 合并会误报）。真未落地的本轮并回 main 跑齐闸收口。
3. **环境余量**：`df -k /Volumes/Eng-Dev`，可用低于 ~4 GiB 先清可再生物（`kernel/node_modules`+重装、`npm cache`、往轮 `/var/tmp` 临时件）；仍不够就按"环境不足"如实终止并给补救命令，别硬跑到被杀。
4. 对每个要改的文件先复制到 scratch 目录（如 `/var/tmp/iterate-kernel-check/`）留快照——这是唯一回滚点。

【执行流程】

1. **全面审查**：对 kernel 全部代码做正确性、边界条件、异常处理审查（可调用 review-bugbot / review-security 类子代理；它们不可用时通读现存代码，按"无 diff＝通读"下简报）。重点盯：decision-log 哈希链的拒绝路径（读不进的历史必须拒绝且零改动）、schema 演进的向后兼容、zod 版本（`kernel/package.json` 依赖 zod，GHSA-mrhx-c7xc-m3w5 要求 ≥4.6.6）、`exports` 表与 `dist/` 产物的一致性（`.d.ts` 形状与 zod 主版本必须匹配——曾出现过 `.d.ts` 是 zod 3 形状而范围允许 <5 的缺陷）。每个修复配 `node --test` 测试（不引第三方测试框架），夹具形状必须来自真报文/真文件，不许桩编形状。
2. **门禁全绿**（命令逐字精确；先记基线计数再改代码；包装脚本退出码不可信，绿要落到具体用例名；完整读日志禁止 tail/head 截断）：
   - `cd kernel && npm ci`
   - `npm run build`（`tsc -p tsconfig.json`）
   - `npm test`（= build + `node --test test/*.test.mjs`）
   - iterate-skill 仓 CI 里与 kernel 相关的闸（读 `.github/workflows/ci.yml` 找出 kernel job 的逐字命令并复跑）
   - 反向验证：对每条新修/新加的守卫做一次反向破坏，证明具名用例能红，再核回。
3. **发版**（仅当 kernel 有实质改动）：
   a. 版本判断：真源 = `kernel/package.json` 的 `version`。契约/schema 有变化或修缺陷＝至少 patch；新增 entry 或破坏兼容＝minor。开工先 `npm view iterate-kernel version --prefer-online` 与 `git tag --sort=-v:refname | head -5` 实测，别信文档数字。
   b. 只改 `kernel/package.json` 与 `kernel/package-lock.json` 的版本（内核没有 set-version 统一器；**绝不拿 GlassPane 的 `scripts/set-version.mjs` 来取号**——那是父仓 12 位点的统一器）。
   c. 本地复跑第 2 步全部命令全绿后提交：`git add kernel/`（+ 如需 workflows），Conventional Commits 前缀 + 中文正文，含中文/括号一律 `git commit -F <文件>`，推送 `origin main`。
   d. 打 tag：`git tag v0.1.<X>` + `git push origin v0.1.<X>`；**顺序固定 push main → 核 tag 可达 → 再触发发布**（tag 先推而 commit 不可达会让发布动作 403）。
   e. 发 npm：`gh workflow run npm-publish-kernel.yml --repo jingzhao-l/iterate-skill --ref v0.1.<X>`（或确认 tag push 触发的通道），`gh run list/view` 逐 job 确认真绿。
   f. **tag ≠ npm**：job 绿不算发完，回查 registry：`npm view iterate-kernel@0.1.<X> version --prefer-online` 等于新号才算；registry 读副本有 12–20 分钟延迟，按版本号点名查。再 `npm view iterate-kernel dist.tarball` 与 `npm pack --dry-run` 对 shasum。
4. **消费方追平**（同轮做完，不许列"待裁决"；四处的确切动作见【审查范围】里逐处清单）：
   - 顺序：壳（mcp-shell pin + corpus `--record`）→ fork（opencode pin + kernel-pin/kernel-conformance `--record`）→ Python 第二实现（vendored fixtures + manifest + 跨语言对拍 + pytest）→ plugin（pin + 自身套件）。四处同号才算追平。
   - 注意：**改 GlassPane 主仓 / harness fork 会撞上那两条每日线的发布链**（harness 侧 `release-artifact` 闸要求发布物==主干）。追平改动落地 GlassPane 侧时：按它自己的口径提交推送，并在汇报里点名"harness 侧的 split/tag 吸收由 10:30 那条线完成"或按当日实际情况处理；若因此必须把 fork 侧 split 推出去，按 `fork-diff --record` + subtree split 的顺序做并跑齐该侧闸。
   - iterate-harness 与 iterate-plugin 有各自独立的发布仓与版本线（`harness-origin` / `plugin-origin` remote，`.release/` 是镜像）：本线只把它们在 iterate-skill 主仓的子树改到同号，是否再走各自的 split/发版按该仓口径判断并留痕；不确定就不发版但在汇报里写清那一格留给谁。
5. **收口清理**（最后一步，属硬条件）：
   - iterate-skill 仓：`git status --porcelain` 里只剩别人的未提交批次（逐条点名）或为空；本轮自建的 worktree 确认无未提交内容后 `git worktree remove` + `prune`；已证实落地的本线分支 `git branch -d`（禁 -D）与 `git push origin --delete`；`/var/tmp/iterate-kernel-check/` 之外不留临时件。
   - 不许删：任何 tag、别人的活跃分支、内容未证实落地的分支、`node_modules`（那是环境）。
   - 进程：本轮起的每个后台命令/探针必须退出，判据是前后两次 `pgrep` 非空→空，不是 pkill 退出码；归属不明的长命进程一律不动并点名。

【不可让步的诚实性红线】

- 金样/记录一律由 `--record` 生成，不手改；任何闸转红先反向破坏证明它能红，再决定修代码还是重记基线。
- 修在跑不到的路径上等于没交付；只在负载下才红的计时断言是坏对照（改判据，不加超时）。
- 内核只转录不判定：判定语义的代码不许进 kernel。
- 测不出就写"未观测"并附补上它的确切命令；不得把未验证写成已验证。

【环境约束】

- 每条终端命令前先执行：`export PATH="/opt/homebrew/bin:/opt/miniconda3/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"`；不可用就绝对路径（node=/usr/local/bin/node、gh=/opt/homebrew/bin/gh）。禁止 `source ~/.zshrc`。
- 本机 zsh tmux 钩子会杀管道（`command not found: tmux` + exit 127）：多段命令走 `/bin/bash -c '…'`；heredoc 用引号形式 `<<'EOF'`。
- bun 与 GitHub 资产下载：本机代理对 `objects.githubusercontent.com` 出 TLS MITM，bun 报 UNABLE_TO_VERIFY_LEAF_SIGNATURE 时喂 `NODE_EXTRA_CA_CERTS`/`--cafile`，**绝不关校验**；大资产走 `gh api` + `assets[].digest` 对账，不用本地重算 shasum 当判据。
- 推 `.github/workflows/**` 被 token scope 拒时改用 SSH remote（`git@github.com:jingzhao-l/iterate-skill.git`）；`--force-with-lease` 必须显式 SHA 形式。

【最终汇报】

按顺序简明列出：① 收口证据——iterate-skill main 收口 HEAD、status 状态、tag 与 registry `iterate-kernel@0.1.<X>` 实测版本号（零改动轮写明"本轮内核零改动，不发版"）；② 每条门禁命令的实际计数；③ 发现的缺陷数与修复数（必须相等，"未修项"必须为空）；④ **四处消费方 pin 追平前后的版本号**（壳 / fork / Python fixtures manifest / plugin，逐个列，缺一个就是没追平）；⑤ 做过的反向验证（破坏哪一处、哪条具名用例变红）；⑥ 本轮我替你做了哪些决定（依据 + 回滚命令）；⑦ 未观测项（只限物理边界，附补救命令）；⑧ 清理盘点（worktree 行数、分支条数、删了什么/留下什么/判据）。不贴大段日志。
