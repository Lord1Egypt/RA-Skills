# FAQ（完整版）

> SKILL.md 只保留高频速览；这里是完整 17 条。按「先自救（doctor/info）→ 再查此处」的顺序。

**Q1：召回输出「无可召回修法」是坏了吗？**
不是。经验库从零开始，首次运行必然为空。想**立刻有东西可召回**，装起步包最快：
```bash
node code/light-cli.mjs starter      # 装载 20 条通用教训（编码/JSON/权限/文件/语法/类型/网络）
node code/evolver-recall.mjs --query "读取中文日志报 UnicodeDecodeError"   # 立刻能命中
```
**EN A1**: Normal - the store starts empty. Fastest way to get something recallable: `starter` loads 20 curated general lessons.


**Q2：models.json 里配 `$ENV` 环境变量不生效？**
pi **0.85.1 起已支持 `$ENV` 插值**（实测确认，上游 issue #9258 已闭环）；**0.74.2 及更早不支持**，需 `--api-key "$MY_KEY"` 显式传。
**EN A2**: pi >= 0.85.1 supports `$ENV` in models.json (upstream issue #9258 closed); <= 0.74.2 does not - pass `--api-key` explicitly.


**Q3：`--fresh` 会不会丢数据？**
不会丢——运行前自动备份到 `~/.evomap/assets/backup-<时间戳>/`。恢复时把该目录下的 `genes.jsonl` 与 `review.jsonl` **配套**拷回。但清空动作仍是破坏性的，执行前请确认。
**EN A3**: No data loss - auto-backup to `~/.evomap/assets/backup-<ts>/` before running. Restore genes.jsonl + review.jsonl together.


**Q4：修法注入后还是踩坑了，为什么？**
修法注入是软提示（system prompt），遵从度模型相关——它把「多次试错」压成「最多一次教训」，但不承诺 100% 避坑（诚实边界见报告 §22）。
**EN A4**: Injection is a soft prompt (system prompt) - adherence is model-dependent. It compresses many tries into at most one lesson; it never promises 100% avoidance (see report section 22).


**Q5：沉淀/审核时报「命令找不到」？**
默认后端（light）**零外部依赖**，只要 node ≥22 就能跑：
```bash
node code/light-cli.mjs doctor    # 环境自检
node code/light-cli.mjs list      # 查看台账
```
只有在用 evolver 集成（`--engine evolver`）时才需先 `npm install`。
**Q8 补充：可选集成的运行版本**：可选集成的最低运行版本为 pi-coding-agent 1.5.1 → Node ≥22.19.0、evolver 2.0.50 → Node ^22.13.0 或 ≥23.4.0；默认 light 后端仍只需 Node ≥22。**EN**: Optional integrations require Node >=22.19.0 (pi 1.5.1) or ^22.13.0/>=23.4.0 (evolver 2.0.50); the default light backend needs only Node >=22.

**EN A5**: The default light backend has zero external dependencies - Node >= 22 suffices. `doctor` for environment self-check. npm install only needed for the evolver integration.


**Q6：approve 能全自动吗？**
审核语义**统一见 SKILL.md「审核状态机」（单一事实源）**：四种场景（交互/非交互本地沉淀、approve 取证、池导入 tier）各有默认行为；召回侧守卫仍兜底。想改人工：`config --auto-approve off`；共享池 `gene import` 按 `--tier` 判定。
**EN A6**: All review semantics live in the SKILL.md review-state-machine section (single source of truth): interactive / non-interactive deposits, approve-with-evidence and pool tiers each have their own default; recall-side guards still backstop. Switch to manual with `config --auto-approve off`; pool imports follow `--tier`.


**Q7：国内网络 npm/GitHub 慢？**
npm 换国内镜像：`npm config set registry https://registry.npmmirror.com`；GitHub 克隆可用镜像代理或直接下载 Release zip。
**EN A7**: npm domestic mirror: `npm config set registry https://registry.npmmirror.com`; for GitHub, use a mirror proxy or download the Release zip directly.


**Q8：Node 版本要求？**
≥22（traps 生成器还需 Python 3）。版本过低时 pi/evolver 可能启动失败。
**EN A8**: >= 22 (traps also need Python 3). Lower versions may fail to start pi/evolver.


**Q9：我沉淀了很多，但好像从来没被用过？**
先看闭环健康度——大概率是两个静默失效之一：
```bash
node code/light-cli.mjs info      # 看「召回次数 / 命中 / 待审」
```
- **召回次数 0** ⇒ 要么手工跑一次召回，要么 `install-hooks` 让宿主自动召回；
- **待审 > 0** ⇒ 这些基因不会注入，用 `approve <gene_id>` 放行。
**EN A9**: Check loop health via `info` first - likely recall never ran (run it once or install-hooks) or genes await review (approve them).


**Q10：`install-hooks` 会不会改坏我的宿主配置？**
不会擅自改。它**默认只演练**：打印将要复制的文件、目标路径、需手工确认的注册步骤，**不落盘**。确认后加 `--yes` 才写入（写入前自动备份）。回滚 = 删除钩子目录。
**EN A10**: It never writes without consent - dry-run by default, `--yes` applies after confirmation, with automatic backup. Rollback = delete the hook directory.

> 接入方式**完整矩阵**（有钩子宿主 / 有指令文件的宿主 / 补写侧 last mile / 国内镜像 / 自检）见 [`docs/boundary-and-triggers.md`](boundary-and-triggers.md) §6。
> **EN**: For the full integration matrix (hook-capable hosts / hosts with instruction files / write-side last mile / China mirror / self-check), see [`docs/boundary-and-triggers.md`](boundary-and-triggers.md) §6。


**Q11：起步包里的基因是哪来的？安全吗？**
是策展过的**通用工程教训**，来源为实际踩坑并人工筛选；装载时同样**过脱敏闸门 + 注入扫描**两道门；不收集、不上传任何数据，纯本地文件。
**EN A11**: Curated general engineering lessons from real incidents, human-filtered; loading passes the same redaction + injection gates. No collection, no upload, pure local files.


**Q12：我的 Agent 既不是 OpenClaw 也不是 Hermes，怎么让它自动用？**
用规程粘贴：`node code/light-cli.mjs snippet` 输出「五个触发点」操作规程，粘进你的 AGENTS.md / CLAUDE.md / 系统提示即可。这是没有钩子机制的宿主最可靠的接入方式。
**EN A12**: Use the procedure paste: `snippet` outputs the five-trigger-point protocol; paste it into AGENTS.md / CLAUDE.md / system prompt. The most reliable integration for hosts without hooks.

> 接入方式**完整矩阵**（含 OpenClaw/Hermes 钩子路径对比、多宿主并发行为、国内镜像、自检）见 [`docs/boundary-and-triggers.md`](boundary-and-triggers.md) §5–§6。
> **EN**: For the full integration matrix (OpenClaw/Hermes hook-path comparison, multi-host concurrency behavior, China mirror, self-check), see [`docs/boundary-and-triggers.md`](boundary-and-triggers.md) §5-§6.


**Q13：为什么我的 agent 修完坑从来不自动沉淀？**
因为 T4（修好坑后沉淀）没出现在它的上下文里——技能只在被加载时影响 agent。解法：`install-snippet --file <项目>/AGENTS.md --yes` 把五触发点规程写进项目指令文件。这是**写侧的 last mile**。
**EN A13**: Because T4 never entered the agent context - skills only influence agents when loaded. Fix: `install-snippet --file <project>/AGENTS.md --yes` writes the procedure into the project instruction file (the write-side last mile).


**Q14：多会话并行时 register-hit 为什么会错记？**
0.17.0 及以前用位置编号（#N），而「本次召回选中集」是共享单文件，会被其他会话的 recall 覆盖 → 编号漂移。**0.18 起用 `--gene <asset_id|gene_id>` 按 id 寻址**，并发安全。
**EN A14**: Pre-0.18 used positional numbers against a shared single-file selection snapshot (overwritten by other sessions' recall). 0.18+ addresses by `--gene <asset_id|gene_id>` - concurrency-safe.

**Q15：基因签名是什么？我的基因会被别人冒充吗？**
不会。0.21 起每台机器有 Ed25519 身份（`~/.evomap/identity/`，私钥 0600 不出本机）；沉淀的基因带 {sig, keyid, pubkey}，入池导入时验签——内容被篡改会被拒绝。无签名的老基因原样接受。查看本机身份：`light-cli identity`；验签：`light-cli verify <gene_id>`。
**EN A15**: Ed25519 per-machine identity; genes carry {sig, keyid, pubkey}; pool imports verify - tampered content is rejected. Legacy unsigned genes pass. `light-cli identity` / `light-cli verify <gene_id>`.


**Q16：文档里的「锁定依赖版本」和「上游实测版本」有什么区别？**
前者是 `package.json` 的 `optionalDependencies` 锁定值（pi 0.74.2 / evolver 2.0.30），只在你主动安装可选集成时生效，A/B 流程零 npm 依赖；后者是每版开发前 C42 上游检查实测到的最新版（pi 1.5.1 / evolver 2.0.50），只用于兼容性评估与最低运行版本说明，**不是本项目安装的版本**。两者由同一生成器写入，语义不可混用。
**EN A16**: Locked dependency versions (pi 0.74.2 / evolver 2.0.30) are the pinned optional integrations in package.json; upstream-checked versions (pi 1.5.1 / evolver 2.0.50) come from the C42 pre-development check and are used only for compatibility assessment, never installed.

**Q17： 常见英文技术术语对照表（错误提示与文档共用）**
**EN A17**: Chinese–English glossary for terms appearing in CLI errors and docs.

| 英文术语 | 中文含义 | 出现在哪 |
|---|---|---|
| ENOENT | 文件/目录不存在 | 路径写错、库未初始化 |
| EACCES / EPERM | 权限不足 | 只读文件、目录权限 |
| EBUSY | 文件被占用（Windows 常见） | 编辑器/同步盘占用中 |
| EISDIR | 目标是目录不是文件 | `--out` 等路径参数指错 |
| ENOSPC | 磁盘空间不足 | 大库写入失败 |
| ETIMEDOUT | 网络超时 | 端点不可达/代理 |
| JSON / JSONL | 数据格式 / 每行一个 JSON 对象 | 经验库文件格式 |
| POSIX | 跨平台系统接口标准 | chmod/ulimit 等术语出处 |
| fail-closed | 失败即拒绝（宁可不通过） | 守卫/审核门语义 |
| fail-open | 失败即放行（不阻塞调用方） | 文件锁超时等非关键路径 |
| Ed25519 | 签名算法 | 基因签名链与许可 token |
| asset_id | 基因资产标识（sha256:…） | 去重与审核台账键 |
| keyid | 签名者身份短号 | 贡献归属与验签 |
| T1–T5 | 五个触发点（召回/行动前/报错/修好/结束） | 使用规程 |
| ABF | 对抗守卫（注入前扫描） | 安全门 |

> 术语表由 `doctor`/`fail()` 的错误输出自动引用（输出末尾附「[术语对照]」行）；文档与 CLI 共用同一份，避免两处漂移。
