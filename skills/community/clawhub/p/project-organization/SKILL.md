---
name: project-organization
description: >
  大项目组织方法论 + 可执行脚手架（跨机跨系统）。当用户开始一个会长期演进、多阶段/多子任务的项目，
  需要按研究/业务主题分层组织文件、或项目文件已散落在根目录需归整时使用。
  核心是"大项目制 + 按语义分层 + agent 自动判断归属 + .trash 软删除"。
  提供新建大项目/子项目骨架、结构自检、结构安全删除（.trash）脚本与模板。
  含项目根下的「缓冲区 / buffer」——人类把文件丢进 `buffer/`，AI 说"读取 buffer"即按语义归位到 projects/。
  触发词：组织项目、项目结构、大项目、项目管理、目录整理、项目化、分层结构、新建项目、归档项目、
  读取 buffer、处理 buffer、缓冲区、把文件丢进 buffer、buffer 归位。
  Use ONLY for long-lived / multi-phase projects；一次性临时任务走 `temp-workspace`，不要用本 skill。
  所有大项目根**必须配备 git**（`scripts/git_setup.py`；改动前先 commit）。
version: 2.6.3
---

# Project Organization — 大项目组织方法论

把"组织大项目"固化为**方法论 + 可执行脚手架**。很多任务开始时很小，但会长成庞然大物。
本 skill 提供一套**从第一天就用**的层级结构、归属判断规则，以及一组跨机跨系统的落地脚本。

> **本 SKILL = 给 AI 的规范。给人看的「操作手册」**见 [`references/ops-manual.md`](references/ops-manual.md)
> （5 分钟上手 / 常用命令 / 排错 / 三条铁律）。

> 适用：任何会长期演进、有多阶段/多子任务的工程、研究、写作、开发项目。
>
> **★ 强制（2026-10-10 起）**：每个大项目根**必须配备 git**（`scripts/git_setup.py init`），
> 且**任何改动前先 commit**。缘由：本项目曾因「手改被覆盖 + 无版本控制 + Syncthing 版本功能关闭」**不可逆丢稿**。
> 详见 **§十三、版本控制（git，强制）**。
>
> **另（顺序铁律）**：`git init` 必须在 OpenCode **第一次打开该目录之前**完成；否则会出现
> 「同目录两条 project、该文件夹 session 列表变空」（会话没丢）。检测/修复见 §十三 与 `scripts/oc_project_link.py`。

---

## 一、边界：和 temp-workspace 的分工

| 场景 | 用哪个 skill | 建在哪 |
|------|--------------|--------|
| **会长期成长**、有多个阶段/子项目、需归档 | **本 skill** | 大项目根（`projects/` 分层） |
| **一次性**分析报告 / 临时小实验，用完即弃 | `temp-workspace` | `$OPENCODE_SCRATCH_DIR/<日期>_<主题>/` |

一句话：**"要不要为它建 `projects/` 分层"是分水岭**。只是临时跑一下 → `temp-workspace`；
预期会攒东西、要给人交付、要归档 → 本 skill。

### 与 temp-workspace 的交接协议（晋升 / 降级）

两个 skill 是同一根生命周期的两端，**不是二选一就结束**——项目可随体量在两者间迁移：

| 方向 | 触发 | 工具 |
|------|------|------|
| scratch → 大项目（**晋升 promote**） | 临时项目长大：出现多阶段/子任务、要交付、要归档 | `temp-workspace/scripts/promote.py`（内部调用本 skill 的 `new_subproject.py` + `trash.py`）|
| 大项目 → scratch（**降级 demote**） | 大项目里冒出一段纯一次性实验，不值得建子项目 | `temp-workspace/scripts/new_project.py` |

- `promote.py` 会：建子项目骨架 → 把 scratch 的 `data/src/output/results` 按语义映射进来（`src→scripts`）
  → 用本 skill 的 `trash.py` 把空壳**软删除**进 `.trash/`（不硬删）→ 重建 scratch 索引。
- 因此**接收晋升项目无需额外操作**：子项目天然落在 `projects/<名>/`，且已登记索引。
- 判据仍是一句话：**"要不要为它建 `projects/` 分层"**——不确定时先在 scratch 起，长大后 `promote.py` 过来即可。

---

## 二、大项目根放在哪（接 AGENTS 项目目录规范）

大项目根的**父目录**按 AGENTS.md「本地项目目录规范」四类归属，全部走环境变量：

| 项目类别 | base 根 | 脚本 `--kind` |
|----------|---------|---------------|
| 清华 / 学习 / 校园 | `$OPENCODE_THU_DIR/` | `thu` |
| 腾讯云 / VPS 相关 | `$OPENCODE_TEMP_DIR/tencentcloud-ops/` | `tencent` |
| 跨机共享数据 / 项目 | `$OPENCODE_TEMP_DIR/` | `shared` |
| opencode 临时小项目 | `$OPENCODE_SCRATCH_DIR/` | `scratch` |
| 其它（用户已有目录等） | 显式 `--root` / `--path` | `custom` |

> 例：`--kind thu --name "my-research"` → `$OPENCODE_THU_DIR/ALS-Program/`。
> **不写死盘符**：脚本读环境变量，三端（Windows/Linux/macOS）通用。

---

## 三、推荐的层级结构（hierarchical layout）

```
<大项目根>/                     # 含 .bigproject.json 标记
├── README.md                  # 顶层唯一允许的 .md（目的/结构/子项目清单索引）
├── .bigproject.json           # 由脚手架写入的根标记（供脚本自动定位）
├── .git/  +  .gitignore       # ★ 强制：git 版本库（改动前先 commit；见 §十三）
├── projects/                  # ★ 所有子项目/阶段，每个一个子文件夹
│   ├── _index.md              # 子项目索引（脚本自动维护）
│   └── <项目名>/
│       ├── README.md          # 强制：目的/进展/结果/脚本讲解（无 README 视为未完成）
│       ├── scripts/           # 该项目脚本
│       ├── data/              # 输入数据
│       ├── results/           # 中间结果
│       ├── output/            # 最终产出（报告/图/PPT）
│       └── task/ 或 workplan/ # 任务表/任务书（可选，--with-task 生成）
├── shared/                    # 跨项目共享（只读引用；★ 唯一例外：registry/ 可写）
│   ├── registry/              # ★ 唯一事实源（datasets/methods/… 的**写入区**）+ 状态速查
│   └── references/ models/ config/ templates/ pipeline/ …
├── buffer/                    # ★ 人类 ⇄ AI 交换区（见 §四 缓冲区）
│   └── <文件/目录>            # 扁平：人 → AI 投递 + AI → 人 交付（直接放这里）
│   └── README.md
├── archive/                   # 已结束项目归档（含 README.md 索引）
├── .tools/                    # 本项目**机器流水**：操作日志（journal.jsonl / _log.md）；不放业务产物
└── .trash/                    # 软删除暂存（**压缩包 + _index.json**，见 §六）
```

**关键点**
- 子项目名用英文短横线（`data-analysis`、`literature-review`），阶段用 `--type stage` 或子文件夹区分。
- 子项目根目录**只有 README.md**，其余内容进子目录。
- 任务表/任务书归入所属项目的 `task/`，**不留在根目录**。
- 顶层只允许 `README.md` / `AGENTS.md` / `MEMORY.md` / `.bigproject.json` / `.gitignore` / `.gitattributes`、目录 `.git/` 与上述目录（含 `buffer/`），其余一律视为散落物（`audit_project.py` 会报）。**例外**：项目若确有合法根级扩展，可在 `.bigproject.json` 的 `root_extensions`（`{"files":[...],"dirs":[...]}`）中声明，`audit_project.py` 会并入允许集（见 §十 `audit_project.py`）。
- ★ **每个大项目根必须配备 git**（`git_setup.py init` 自动建库 + 首次提交）；**改动任何文件前先 `git commit`**，之后可 `git diff` / `git checkout` 找回。`audit_project.py` 会把「未配备 git」报为 **high**（见 §十三）。

### 3.1 外部代码仓子项目（code-repo）——「父项目里挂一个别人的 git 仓」

**场景**：子项目本身是一个**有独立远端**的代码仓（GitHub / GitLab / 华为云 CodeArts / Gitee…），
用 `git clone` 拉进 `projects/<名>/`。它与大项目根**各自是独立版本库**；处理不当会产生
「嵌套版本库 / 半吊子 submodule」——父仓库 `git add` 一个含 `.git` 的目录时，会把它记成一个 gitlink，两边状态互相打架。

**约定（就 4 条）**

1. **位置**：`projects/<名>/`（仍是子项目，按 §四 归属）。
2. **父仓库忽略它**：根 `.gitignore` 加 `/projects/<名>/`——**父 git 不追踪代码**，代码的版本控制**完全交给它自己的远端**。
   `audit_project.py` 对「含 `.git` 但未被父仓库忽略」的子项目报 **medium（`nested_repo_not_ignored`）**。
3. **不套骨架**：code-repo **不建** `scripts/data/results/output`；仓库自带的 `README.md` 即子项目说明，布局以仓库自身为准。
4. **同步纪律**：所有 git 操作都用 `git -C projects/<名> …`，别让父仓库的命令误作用到子仓。

**登记（推荐用脚本）**

```bash
python scripts/new_subproject.py --name <名> --type code-repo --repo <远端URL>
# → 不建骨架、不覆盖已有 README、自动写父 .gitignore(忽略 /projects/<名>/)、索引类型记为 code-repo
```

**AI 开发约定（代码仓通用，属"人机协同"护栏）**
- 开工先同步主线：`git -C projects/<名> fetch --all --prune && git -C projects/<名> switch main && git -C projects/<名> pull`；
- **只在专属分支干活**（前缀如 `agent/`），**禁止直推 `main`**；合并走平台 **MR**，由人 review / 合入；
- 建议把 `main` 设成平台**保护分支**（允许推送仅留本人），做到"约定式轻隔离"；要平台级强制隔离则给 AI 单独子账号；
- 平台**接入方法**（账户级 SSH 密钥、克隆地址取法、MR）见对应平台 skill；主机名 / 密钥登记在 `ssh-mesh`（唯一权威）。

### 3.2 文件职责与命名（谁给谁看、写什么）

| 文件 | 给谁 | 性质 | 写什么 | 更新方式 |
|---|---|---|---|---|
| `README.md` | **人**（+AI 初读） | 描述 | 这东西**是什么**、结构、怎么用、入口 | 结构变才改 |
| `AGENTS.md` | **AI**（每次会话**自动加载**） | **指令/规范** | **必须怎么做**：约束、映射、禁区、触发词 | 规则定了少改 |
| `MEMORY.md` | AI | **历史/教训** | 发生过什么 + 学到的规则（带时间戳+源） | **只增**（append） |
| `STATE.md`（项目级） | AI（接手先读） | **当前基线** | **现在以什么为准** + 已被取代 | 就地改写 |
| `INDEX.md` | AI | 登记 | 项目 ↔ 四工具映射 / 项目清单 | 增删项目时 |
| `TODO.md` | 人+AI | 滚动待办 | 最新在上 | 频繁 |
| `.tools/journal.jsonl` | 机器/审计 | 操作流水 | 谁·何时·做了什么 | append-only |

> 一句话：**README 描述「是什么」、AGENTS 下「必须怎么做」、MEMORY 记「曾发生+教训」、STATE 定「现在以什么为准」。**

### 3.3 子项目内部标准布局

```
projects/<项目>/
├── README.md      # 强制：目的/进展/结果/脚本讲解
├── STATE.md       # ★ 当前基线（AI 接手先读）
├── scripts/       # 脚本（只留**可复用**的；一次性脚本用完即弃）
├── data/          # 输入
├── results/       # 中间结果
├── output/        # 最终产出（非 git 项目另设 versions/<时间戳>/ 快照）
├── handoff/       # （人机协作）每轮交接单
├── tmp/           # 仅临时中间件；**任务结束即清**
└── task/|workplan/  # 可选：任务表 / 任务书
```
- `chats/`（research-ops 约定）放组根或项目内均可。
- **`tmp/` 铁律**：只放**可随时删**的中间件，**用完即清**；**不把 `tmp/` 当工作区**。

### 3.4 子代理 / 大模型的中间文件与日志

> 子代理（如 `draw`）跑图/跑数会产出一大堆中间件——统一规矩，**别污染成果区**：
- **中间件一律进 `<项目>/tmp/`**（**不是** `output/`、**不是**根目录、**不是** skill 目录），命名带前缀（`_draft_*` / `_probe*` / `_check*` / `_rt*`）。
- **只有可复用的**进 `scripts/`，**最终产物**进 `output/`；其余**收尾即清**（走 `trash.py put --apply`）。
- **日志**：脚本日志写**项目 `tmp/`**；操作流水写 `.tools/journal.jsonl`（机器流水，非业务产物）。
- **收尾自检**：任务结束时 `tmp/` 清空（或已 `trash.py` 化），`output/` 只留成果。

---

## 四、agent 判断归属规则

每次来新任务，先判断（**语义判断，不是关键词匹配**）：

| 情形 | 动作 |
|------|------|
| 新任务与现有项目无重叠、有独立目标/产出 | **新建** `projects/<项目名>/`（`new_subproject.py`） |
| 子项目是**有独立远端的代码仓**（clone 进来的） | 走 **code-repo**：`projects/<名>/` + 父 `.gitignore` 忽略 + 不套骨架（`--type code-repo`，见 §3.1） |
| 任务属于某项目内已有阶段/子任务 | **复用**，直接在该项目子文件夹内工作，不新建 |
| 项目目标达成、不再推进 | **归档** 到 `archive/<YYYY-MM-DD>_<项目名>/` |
| 多个项目共享的资源 | 放 `shared/`（不属任何单一项目） |
| 一次性、用完即弃 | 不属于本 skill → 走 `temp-workspace` |

- 看任务的**目标/产出**是否与某项目一致，而非看关键词。
- 不确定时**倾向复用**（避免项目碎片化）；目标确实独立时果断新建。

### 4.1 缓冲区（buffer）——**人 ⇄ AI 的唯一交换口 ★**

> **为什么值钱**：它把"人 ⇄ AI 交接文件"收敛成**一句口令**——用户**不用学任何东西**：
> **丢进 `buffer/` + 说「读取 buffer」**即可。**双向**（人→AI 投递 ｜ AI→人 交付）、
> **可追溯**（每步记 journal）、**安全**（覆盖不硬删、进暂存）。
> 它是本 skill 里**唯一**要求"人能独立操作"的入口 → **越简单越好**。

```
<大项目根>/buffer/        # ★ 扁平：直接放（无 inbox/outbox）
├── <文件/目录>          # 人 → AI（投递）＋ AI → 人（交付）
└── README.md
```

**「读取 buffer」= 4 步**：① `buffer.py list`（进入前**自动 TTL 检查**）→ ② **语义归属判断**（§四）→
③ **出「归属方案」（源→目标）→ 等用户确认** → ④ 执行：`take`（归位）/ `deliver`（AI 交付）/ `new_subproject.py`（新建）；`take/deliver/discard` 自动写 journal。

**规则（就 5 条）**
- ★★ **TTL 2 天 = 强制清理**：进入 buffer（任何子命令）**先自动检查**，**超期一律清掉**（软删进 `.trash/`，可恢复；`--hard` 真删，`--no-purge` 跳过）；`audit` 报 `buffer_expired`。**buffer 只做中转，不是存储区。**
- ★★ **一一对应**（判定 = **同名或内容一致**，允许改名）：**buffer 里的每一项都必须在 `projects/`（或 `shared/`/`archive/`）有归宿**——要么等 `take` 归位，要么是项目 `output/` 的**交付副本**（`deliver` **默认 copy → 项目保留原件**）；**禁止把 buffer 当唯一副本 / 长期存放**。
- **先预演后执行**（`--apply`）；覆盖同名旧物**进暂存**（`.trash/` 或 `buffer/.replaced/`），**不硬删**。
- ★★ **只留最新一版（禁版本堆积）**：**同一交付物的新一轮交付 = 取代旧版**——`deliver` **默认自动**把同族旧版（如 `x_v3.png` 之于 `x_v5.png`）**软删进 `.trash/`**（`--no-supersede` 可关）；**禁止 `v1/v2/v3…` 堆在 buffer**。存量用 `buffer.py tidy --apply` 一把收拢；`audit` 报 `buffer_version_pileup`。
- ⭐ **任务文件归位**（AGENTS 规则 8）：用户丢来的输入 + 本任务的中间/结果件，**收尾必须归进对应子项目**；同名不覆盖（`name.1.ext`）；**`take` 归位后才算完**。

---

## 五、快速开始

```bash
PO="$HOME/.config/opencode/skills/project-organization/scripts"

# 0) ★ 版本控制（每个大项目根必备；new_big_project 会自动建库，老项目补做）
python "$PO/git_setup.py" init --root .                      # git init + .gitignore + 首次提交
python "$PO/git_setup.py" commit -m "改前打点：<说明>"         # 每次改动前/后各 commit 一次
python "$PO/git_setup.py" status                             # 看是否脏 / 分支 / HEAD

# 1) 建大项目根（自动含 git init + 首次提交）
python "$PO/new_big_project.py" --name "my-research" --kind thu

# 2) 进大项目后建子项目（自动向上查找 .bigproject.json 定位根）
python "$PO/new_subproject.py" --name analysis --description "结果分析"

# 2.5) 缓冲区（扁平）：用户把文件丢进 buffer/ 后，AI 读 buffer 并归位
python "$PO/buffer.py" init --root .                 # 建缓冲区（幂等；new_big_project 已自带）
python "$PO/buffer.py" list                          # 列 buffer/（自动 TTL 检查）→ 出归属方案 → 用户确认
python "$PO/buffer.py" take --item 数据.csv --subproject analysis --subdir data --apply
python "$PO/buffer.py" deliver --file output/报告.pdf --apply   # ★ AI 交付 → buffer/

# 3) 结构自检
python "$PO/audit_project.py" --root "<大项目根>"

# 4) 归整时"删除"旧目录 → 软删除进 .trash（默认只预演）
python "$PO/trash.py" put "<旧目录>" --reason "迁移到 projects/xxx" 
python "$PO/trash.py" put "<旧目录>" --reason "迁移到 projects/xxx" --apply

# 5) 看操作日志（谁在何时创建/删除/归档了什么）
python "$PO/journal.py" --tail 20
```

> 所有脚本均**先预演、后执行**（默认 dry-run，需 `--apply` 才落盘/移动）；输出 stdout 为 JSON。

---

## 六、删除 = 软删除（.trash 机制，**压缩 · 可精确还原**）

**任何"删除"都先移入 `<大项目根>/.trash/`，不得直接硬删**（AGENTS.md「文件删除铁律」的工具化）。

- **条目 = 一个压缩包**：`.trash/<时间戳>__<名>.tar.<algo>`（默认 **zstd**；可选 `gz`/`xz`/`bz2`）。
  包内含 `_manifest.json`，**路径一律「相对大项目根」（正斜杠）** → **跨机可精确还原**。
- **中央索引**：`.trash/_index.json`（条目 / 时间 / 原因 / 相对路径 / 原始与压缩后大小）→ `list`/`status` **不必解包**。
- 子命令：`put`（压缩入）· `list` · `restore`（**按相对路径还原，逐字节一致**）· `purge`（唯一硬删）· `compress`（把旧「目录式」条目补压成包）· `status`（含**压缩比**）。
- **`purge` 是唯一硬删路径**，必须 `--confirm`，且执行前仍须按 AGENTS 铁律**列清单并经用户确认**。
- **压缩事实**：文本/代码 ~5–15×；已压缩的（png/jpg/zip/pdf）几乎不缩（**正常**，不报错）。
- **一个条目一个包**（不是一个大 tar）：Syncthing **不做包内增量**，一包一条目 → 只同步**新增的包**。
- `.trash/` 是可恢复区，长期留存；无用条目由用户决定何时 `purge`。

```bash
python scripts/trash.py put "<旧目录>" --reason "迁移" --apply          # 压缩入（默认 zstd）
python scripts/trash.py put "<旧目录>" --reason "迁移" --algo xz --apply
python scripts/trash.py list                                            # 看条目（读 _index.json）
python scripts/trash.py restore --id <时间戳>__<名> --apply              # 按相对路径还原
python scripts/trash.py compress --apply                                # 旧目录式条目 → 压缩包
python scripts/trash.py status                                          # 条目数 / 压缩比
python scripts/trash.py purge --older-than 30 --confirm                  # 唯一硬删（须确认）
```

---

## 七、操作日志（journal）

每个大项目根自带一份**追加式操作日志**，记录"谁在何时做了什么"，与 `.trash` 互为印证。

- **存储**：`<大项目根>/.tools/journal.jsonl`（append-only，每行一个事件 JSON）。
- **事件字段**：`{ts, actor, event, target, ...extra}`；`actor` 取 `OPENCODE_ACTOR` → 系统用户名。
- **覆盖事件**：`root.created` / `subproject.created` / `trash.put` / `trash.restore` / `trash.purge` / `audit.run`。
- **查看**：`journal.py`（`--tail` / `--since` / `--event` / `--actor` 过滤，默认输出 JSON）。
- **派生可读版**：`journal.py --render` 生成 `.tools/_log.md`（Markdown 表格）。
- 日志写入**不阻断主流程**（失败仅静默返回 None）；`.tools/` 不被 `audit_project.py` 视为散落物。

---

## 八、本地 ↔ 远程/集群对应

- 本地 = 主项目（脚本/文档/报告），远程 = 工作区（数据/计算/产物）。
- 在本地子项目的 README 里写明远程工作区路径与对应关系。
- **禁止在远程根目录散落脚本/数据/log**——同样按项目归入远程子文件夹。
- 本地与远程目录名尽量一致，便于对照。
- 访问远程机器一律走 `ssh-mesh` 别名（见 `skill-spec` §5.1），不在本 skill 内拼 ssh。

---

## 九、迁移落地流程（把已混乱的项目归整）

1. **全面探查**：列出根目录所有目录/文件，理解每个的语义归属。
2. **设计映射**：把每个平级目录/散落文件映射到目标子项目的子目录。
3. **先建结构 + 建 git**：`new_big_project.py` / `new_subproject.py` 建骨架（自动 `git init`）；
   老项目用 `git_setup.py init` 补建版本库——**必须**；整理过程中**每步先 commit**。
4. **归任务文件**：把根目录任务表/任务书归入所属项目的 `task/`。
5. **归报告/产物**：把平铺的 `output/` 报告按项目归入各子项目 `output/`。
6. **迁移共享**：把跨项目的 `pipeline/` `references/` `models/` 等移入 `shared/`。
7. **写 README**：为每个项目补 README（无 README 视为未完成）。
8. **旧物入 .trash**：旧的空壳/废弃目录用 `trash.py put --apply` 移入 `.trash/`（不硬删）。
9. **更新规范**：更新根 README/AGENTS 反映新结构；历史文档顶部加迁移说明。
10. **验证**：`audit_project.py` 确认无散落物、每个子项目有 README。

> **安全铁律**：任何删除/移动前，先列完整清单 + 等用户确认；**删除一律走 `.trash/`**。

---

## 十、脚本

> 全部为 Python 标准库实现，跨 Windows/Linux/macOS；stdout 输出 JSON，日志走 stderr。
> `<PO>` = 本 skill 的 `scripts/` 目录。

### `scripts/common.py`
公共库（JSON 输出、根目录标记定位、环境变量解析、模板渲染）。被其余脚本 import，不单独调用。

### `scripts/new_big_project.py`
用途：建立大项目根骨架（含 `projects/ shared/ archive/ .tools/ .trash/` 与索引、根标记）。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--name` | 大项目名（用于目录名与 README） | ✅ |
| `--kind` | `thu\|tencent\|shared\|scratch\|custom`，按 AGENTS 规范解析 base 根 | 否（默认 custom） |
| `--root` | base 根目录（在其下建 `<name>/`） | custom 时 ✅ |
| `--path` | 直接指定大项目根完整路径（优先） | 否 |
| `--force` | 目录已存在且非空时复用 | 否 |
| `--dry-run` | 只预演，不落盘 | 否 |

示例：`python scripts/new_big_project.py --name "my-research" --kind thu`
输出：`{"status":"ok","root":...,"marker":...,"created":[...],"git":{...}}`

### `scripts/git_setup.py`
用途：大项目**强制**的 git 版本控制（`init` / `commit` / `status` / `log`）。
| 子命令 | 关键参数 | 说明 |
|--------|----------|------|
| `init` | `--root` `--message` `--force` | `git init` + 写 `.gitignore`（缺失时）+ **首次提交**；幂等 |
| `commit` | `--root` `-m MESSAGE` | `git add -A` 并提交（**改动前/后打点**）；无改动返回 `nothing_to_commit` |
| `status` | `--root` | 是否 git 仓库 / 分支 / 是否脏 / HEAD |
| `log` | `--root` `-n N` | 最近 N 条提交 |
| `tag` | `--root` `NAME` `-m MSG` | 给当前 HEAD 打标签（版本 / 确认 / 冻结打点） |
| `snapshot` | `--root` `-m MSG` `--tag NAME` | ★ **覆盖 / 重跑 / 批量替换前的安全绳**：commit（可再 tag） |

示例：`python scripts/git_setup.py init --root .` ／ `python scripts/git_setup.py commit -m "改前打点"` ／
`python scripts/git_setup.py snapshot -m "重跑生成器前" --tag pre-run-20261010-0630`
输出：`{"status":"ok","root":...,"created":true,"committed":true,"head":"a1b2c3d"}`
> `new_big_project.py` 会**自动**调用 `init`；`audit_project.py` 对未配备 git 的项目报 `high`。

### `scripts/oc_project_link.py`
用途：检查/修复 **OpenCode 对「本大项目根」的 project 记录**（同目录两条 → 该文件夹 session 列表变空）。
| 子命令 | 关键参数 | 说明 |
|--------|----------|------|
| `status` | `--root` `--db` | 列出该目录所有 project 行、哪条有会话、解析器倾向取哪条（最早） |
| `fix` | `--root` `--db` `--hub` `--ssh` `--hub-root` `--dry-run` | 删掉 **0 会话**的冗余行，保留下有会话的那条；`--hub` 一并清 NAS 中枢 |

- **安全底线**：绝不删除任何**有会话**的 project 行；删前把该行导出成 JSON 存底。
- **DB 定位**：`--db` → `$OPENCODE_DATA_DIR/opencode.db` → `opencode debug paths db` → 默认路径。
- `--hub`：经 `ssh <别名>`（默认取 `$OC_SYNC_SSH`）删中枢 `<hub-root>/tables/project.json`（默认取 `$OC_SYNC_ROOT`）中同 id 的行（防 oc-sync 回灌）；未配置时**自动跳过**。

示例：`python scripts/oc_project_link.py status` ／ `python scripts/oc_project_link.py fix --hub`
输出：`{"status":"ok","duplicates":true,"stale":[...],"deleted":[...],"warnings":[...]}`

> **修复后必须**：① 重启 OpenCode 后台服务（项目缓存启动时加载）；② 其他机器若有同一 id，各自清一次。详见 §十三。

### `scripts/new_subproject.py`
用途：在大项目根下新建子项目/阶段骨架，并登记到 `projects/_index.md`。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--name` | 子项目名（英文短横线） | ✅ |
| `--root` | 大项目根（默认从 cwd 向上查找 `.bigproject.json`） | 否 |
| `--type` | `project\|stage\|code-repo`（`code-repo`=外部代码仓：不建骨架、不覆盖 README、自动父仓忽略） | 否（默认 project） |
| `--repo` | code-repo 的远端 URL（写入索引备注） | 否 |
| `--with-task` | 额外建 `task/`（任务表/任务书） | 否 |
| `--description` | 项目目的（写入 README 与索引） | 否 |
| `--force` / `--dry-run` | 复用已存在目录 / 只预演 | 否 |

示例：`python scripts/new_subproject.py --name analysis --description "结果分析"`
示例：`python scripts/new_subproject.py --name evorag --type code-repo --repo git@host:g/evorag.git`
输出：`{"status":"ok","root":...,"project":...,"created":[...],"type":...,"gitignore_rule":...}`

### `scripts/buffer.py`
用途：人类 ⇄ AI 交换缓冲区（`<大项目根>/buffer/`，**扁平 · 2 天 TTL**）——`init` / `list` / `take` / `deliver` / `add` / `purge` / `discard` / **`tidy`**。
| 子命令 | 关键参数 | 说明 |
|--------|----------|------|
| `init` | `--root` `--force` | 建缓冲区骨架 + README；**幂等、直接落盘**（纯新增） |
| `list` | `--root` `--days` `--hard` `--no-purge` | 列 `buffer/`（**进入前自动 TTL 检查**） |
| `take` | `--item NAME...` `--dest DIR` \| `--subproject NAME [--subdir SUB]` `--mkdir` `--overwrite` `--reason` `--apply` `--days` `--hard` | 把 buffer 项移动到目标目录；**默认预演** |
| `deliver` | `--file FILE` `--name` `--move` `--overwrite` **`--no-supersede`** `--apply` | ★ AI 把交付物放进 `buffer/`（默认复制）；**默认自动把同族旧版软删进 `.trash/`（只留最新一版）** |
| `add` | `--file FILE...` `--move` `--overwrite` `--apply` | 把外部文件放进 `buffer/`（人→AI） |
| `purge` | `--days N` `--hard` `--apply` | 清掉超期项（默认 2 天；默认软删进 `.trash/`） |
| `discard` | `--item NAME...` `--reason` `--apply` | 把 buffer 项立即弃入暂存区（`.trash/` 或 `buffer/.replaced/`） |
| **`tidy`** | `--apply` `--days` `--hard` | ★ **同一交付物只留最新一版**：同族旧版一把软删进 `.trash/`（保持 buffer 简洁） |

根定位：`--root` → cwd 向上找 `.bigproject.json` → 回退到含 `projects/`+`README.md` 的目录。
覆盖同名旧物**不硬删**：大项目根进 `.trash/`，否则进 `buffer/.replaced/`。
日志：大项目根写标准 journal；否则写 `buffer/_buffer_log.jsonl`。

示例：`python scripts/buffer.py take --item 数据.csv --subproject analysis --subdir data --apply`
输出：`{"status":"ok","dry_run":false,"dest":...,"moves":[{"from":...,"to":...,"overwrote":false}]}`

### `scripts/trash.py`
用途：`.trash` 软删除暂存（**压缩 · 可精确还原**）——`put` / `list` / `restore` / `purge` / `compress` / `status`。
条目 = `<时间戳>__<名>.tar.<algo>`（默认 **zstd**），内含 `_manifest.json`（**相对大项目根**的路径）；索引 `.trash/_index.json`。
| 子命令 | 关键参数 | 说明 |
|--------|----------|------|
| `put` | `paths...` `--reason` `--algo zst\|gz\|xz\|bz2` `--root` `--apply` | **压缩**入暂存；**默认预演**，`--apply` 才执行 |
| `list` | `--root` | 列出条目（读 `_index.json`；**兼容旧「目录式」**） |
| `restore` | `--id` `--root` `--apply` `--force` | **按相对路径还原**（逐字节一致）；默认预演 |
| `purge` | `--id` \| `--all` \| `--older-than DAYS` `--confirm` `--root` | **唯一硬删**；必须 `--confirm` |
| `compress` | `--algo` `--root` `--apply` | 把旧「目录式」条目**补压**成压缩包（一次性迁移） |
| `status` | `--root` | 条目数 / 原始 / 压缩后 / **压缩比** |

示例：`python scripts/trash.py put "old/" --reason "迁移" --apply` ／ `python scripts/trash.py put "old/" --algo xz --apply`
输出：`{"status":"ok","entry":"...tar.zst","id":...,"algo":"zst","orig_bytes":...,"packed_bytes":...}`

### `scripts/audit_project.py`
用途：大项目「层级结构」自检（顶层散落物、子项目 README、必备目录、.trash）。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--root` | 大项目根（默认从 cwd 向上查找标记） | 否 |
| `--strict` | 存在 high 问题时退出码 1 | 否 |

示例：`python scripts/audit_project.py --root "<大项目根>"`
输出：`{"status":"ok","root":...,"summary":{"by_severity":...},"issues":[...]}`

**根级扩展（`root_extensions`，可选，向后兼容）**：某些项目在通用约定外确有合法根级文件/目录
（例：研究组沿用 `research-ops` 的 `INDEX.md` / `TODO.md` / `chats/`）。在 `.bigproject.json` 中声明即可，
`audit_project.py` 不再报为散落物（缺省 = 空，行为不变）：

```json
{ "name": "...", "kind": "thu", "version": 1,
  "root_extensions": { "files": ["INDEX.md", "TODO.md"], "dirs": ["chats", ".login_tools"] } }
```

### `scripts/journal.py`
用途：查看/渲染操作日志（源 `.tools/journal.jsonl`）。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--root` | 大项目根（默认从 cwd 向上查找标记） | 否 |
| `--tail N` | 只显示最近 N 条 | 否 |
| `--since` | 起始时间（`YYYY-MM-DD` 或 ISO） | 否 |
| `--event` / `--actor` | 事件 / 操作者过滤（子串） | 否 |
| `--render` | 生成 `.tools/_log.md`（Markdown） | 否 |
| `--out` | `--render` 的输出路径 | 否 |

示例：`python scripts/journal.py --tail 20` ／ `python scripts/journal.py --render`
输出：`{"status":"ok","root":...,"count":N,"records":[...]}`

---

## 十一、与现有系统的关系

- 本 skill 定义**组织方法论 + 通用脚手架**，不含领域逻辑；领域结构以项目自身 AGENTS.md/README 为准。
- 进行中的在 `projects/`，结束移入 `archive/`；共享资源进 `shared/`。
- 访问远程/集群走 `ssh-mesh`；临时小项目走 `temp-workspace`。
- 不新建/下载额外 skill 来"管项目"——本 skill 已是该能力。

---

## 十二、真实案例（匿名）

一个大项目根从散落状态归整为：

```
projects/
├── data-analysis/     # 主题 A 结果分析（task/ 放任务表 csv）
├── structure-review/  # 主题 B 结构复核
├── cohort-a/          # 批次 A 的整理
├── literature-review/ # 文献下载与归档
├── knowledge-base/    # 知识库（workplan/ 放任务书）
└── ops-monitor/       # 运维/审计 Agent
shared/
├── references/  models/  config/  templates/  pipeline/
```

每个项目一个 README；外部同步项目化（根目录散落文件归入 `literature-review/`）；
归整过程中废弃的旧目录一律经 `.trash/` 暂存，未硬删。

---

## 十三、版本控制（git，强制 · 2026-10-10）

> **规则**：所有 `project-organization` 大项目根**必须**是 git 仓库；**动文件之前先 commit**。

### ⚠️ 别在 OpenCode 已登记后「重写历史」（2026-10-17 实测）
OpenCode 按 **(worktree, vcs, 登记时的 commit)** 记 project 行。当目录**变成 git 仓**（`git init`）或**重写历史**（`amend` / `rebase` / 重建库，HEAD sha 变了）时，会**再生一条新行**，老会话留在旧行 → 该文件夹 session 列表看似"空 / 不全"（**会话没丢**）。
- ⇒ `git init` 应在 OpenCode **第一次打开该目录之前**完成（顺序铁律）；
- ⇒ **已登记之后，别为了"清历史"反复 `amend` / 重建库**（会多条）；确实要重写时，重写完跑 `oc_project_link.py status` 复查，多出来的 **0 会话行**用 `fix` 清掉。
- 实测佐证：`project.id` **直接等于登记时的 commit sha**（如 `d123897b4beee693f97bb30474209311da56d032`）。
- 修复流程：`status` → `fix`（只删 **0 会话**行，自动导出 JSON 存底）→ **重启 OpenCode 服务** → `status` 复查。

### 为什么（事故背景）
某项目里用户**手工改了 SVG**，随后被「重跑生成器」**覆盖**；而该目录**没有 git**、
Syncthing 的文件夹**版本功能又没开**、回收站为空 → **改动不可逆丢失**。
**有 git，就一条命令 `git checkout -- <file>` 找回。**

### 怎么做
```bash
PO="$HOME/.config/opencode/skills/project-organization/scripts"

# 建库（幂等）：git init + 写 .gitignore + 首次提交
python "$PO/git_setup.py" init --root "<大项目根>"

# ★ 纪律：改动前先打点（人/AI 手动操作之前都先跑一次）
python "$PO/git_setup.py" commit -m "改前打点：<说明>"

# ★★ 覆盖 / 重跑生成器 / 批量替换之前 —— 一条命令打点 + 打标签（安全绳）
python "$PO/git_setup.py" snapshot -m "重跑生成器前" --tag pre-run-<时间戳>

# 版本 / 确认 / 冻结打点
python "$PO/git_setup.py" tag v3-答辩 -m "第三版（用户已确认封面）"

# 看状态 / 历史
python "$PO/git_setup.py" status
python "$PO/git_setup.py" log -n 20
```

> 配套：`deck-authoring` skill 也有同语义的 snapshot（供「人+AI 共创交付物」流程独立调用）。

### 硬性约束
- `new_big_project.py` 建新项目时**自动**执行 `git_setup.py init`。
- `audit_project.py` 对**未配备 git** 的项目报 **high**（`--strict` 退出码 1）。
- `.gitignore` 默认忽略 `__pycache__/`、`.trash/`、系统杂物；大体积产物（`*.pptx` 等）按需开启。
- **AI 必须遵守**：任何「移动 / 覆盖 / 删除 / 重跑生成器」之前，**先 `git_setup.py commit`**；
  覆盖前若目标**不是本会话产出**，**先备份或先问用户**，绝不直接覆盖。

### `git init` 先于 OpenCode 打开目录（一句话规则）

> **建项目的第一个动作就是 `git init`**，且必须在 OpenCode **首次打开该目录之前**完成。

oc 用「git 仓库根」当项目边界；若目录**先**被 oc 认成项目、**之后**才 `git init`，会为同一目录
留下**两条 project**（会话没丢，但该文件夹 session 列表变空）。

**已经晚了**（出现「两条 project / session 列表空」）就走兜底，然后**重启 oc 后台服务**：
```bash
python scripts/oc_project_link.py status        # 先看（哪条有会话、解析器取向）
python scripts/oc_project_link.py fix --hub     # 只删 0 会话冗余行 + 清 NAS 中枢
```
其他机器若也有同一条，需各自清一次（否则 oc-sync 回灌）。自动兜底：`git_setup.py init` 输出
`oc_project_warning`；`audit_project.py` 报 `oc_project_dup`（high）。

### 与 `.trash/` 的分工
- `.trash/` = **删除**的软回收（本项目内，随项目走）；
- `git` = **全部变更**的历史（含覆盖 / 重写），是**唯一能找回「被覆盖内容」**的机制。
- 两者并用：删除先进 `.trash/` 并提交；覆盖 / 重写靠 git 历史。

> ⚠️ 注意：若项目目录处在 Syncthing 同步内，`.git/` 会一并同步。如不想同步 `.git`，
> 可在该文件夹的 `.stignore` 加 `.git/`（各端一致即可）。

---

## 十四、脚本设计补充：**可续跑 + 可看进度（高分辨率）**（2026-10-16，强制）

> 触发：写**任何长任务脚本**（批量下载 / 批量推理 / 多轮实验 / 多局对局 / 爬取 …）。
> 缘由（事故）：狼人杀 Elo 实验脚本跑 8 局、**98 分钟**，**只在最后才输出结果**，中途**完全看不到进度**；
> 一旦服务重启 / 被 kill → **全部重来**。用户问"进度百分之多少"时答不上来。

**① 断点续跑（checkpoint / resume）——长任务必须**
- **逐单元落盘**：每个单元（item / game / batch / 文件）完成即写（append-only `progress.jsonl`，或 `runs/<task>/items/<id>.json`）；
  **禁止**只在全局结束时一次性写。
- **启动即续跑**：启动时扫描已有结果、**跳过已完成单元**（幂等）；单元有**稳定 ID**。默认行为就是 resume。
- **崩溃不丢**：进程被 kill / 服务重启 / 超时后重跑，只补未完成的。
- 目录约定：`runs/<task>/{manifest.json, items/<id>.json, progress.jsonl}`。

**② 进度可视（"高分辨率" = 细颗粒 + 及时）**
- **每完成一个单元立刻报一行**，含 `i/N`、百分比、已用时、ETA：`[12/50] 24% t=180s eta=570s`。
- **细颗粒**：做到**逐单元**，不是每 10% / 每若干分钟才报一次。
- **输出走 stderr 或日志文件**（stdout 留给最终 JSON，遵守"脚本设计铁律"）；**禁用缓冲**：
  `print(..., file=sys.stderr, flush=True)`，或 `PYTHONUNBUFFERED=1`。
- ⚠️ **别被管道缓冲坑**：`python x.py | tail` 会把输出（含 stderr）**缓冲到结束**才吐 → 进度写**日志文件**，
  或 `python x.py > run.log 2>&1` 后再 `tail -f run.log`。

**③ 图表分辨率**：脚本产图用 **高 DPI（≥150–200）**（matplotlib 默认 100 偏低会糊）。

**④ 外部服务并发纪律（2026-10-17 加 · 强制）**
> 触发：长任务脚本会**批量调用某个外部服务**（LLM 端点 / 中转站 / 内网推理服务 / 抓取目标 …）。
> 缘由（事故）：某 CAD 基准以 `MAD_CONC 3~8` 打**清华 MAD**（真实并发上限 ≈3）→ `RATE_LIMIT` → 位点被**中转站封禁** → **全体客户端一起 503 / 流式 `Decode error (200 POST)`**。
> **"我脚本跑得欢"的代价是"所有人的服务一起挂"。**

- **先问上限，再定并发**：调用前先查该服务**声明的并发/配额**（文档、`/v1/limits`、`/api/limits` 之类的端点）。
  - 经 llm-proxy 的模型（`deepseek-flash`/`deepseek-exp`/`gpt`）：`python <skills>/llm-proxy/scripts/proxy.py limits`
    → 看目标上游的 `max_concurrent`（如 `mad=3`、`modelbest=6`）；**并发度 ≤ max_concurrent**（`inflight ≥ max` 即"正忙"，应退避）。
- **并发必须可调**：把并发度做成 CLI 参数（`--conc N`）+ **默认取保守值**；禁止硬编码一个"能跑满"的数。
- **退避重试**：见到 `429` / `503` / `code=upstream_busy` / `RATE_LIMIT` → **指数退避**（带抖动），**不要**立刻重试、更不要提高并发。
- **别绕过中间层**：走中转站的请求受**代理侧硬闸**保护；**直连上游**（自己拿 token 打内网服务）绕不过闸 → 这时**只能靠自己**压并发。
- **共享/免费资源**：校内 / 内网 / 免费额度服务一律按"**共享**"对待，留余量（宁可慢，不要封）。

**交付前检查清单**：□ 逐单元落盘？ □ 启动跳过已完成（幂等）？ □ 每单元实时进度（i/N、%、ETA）？
□ flush / 无缓冲？ □ `stdout=JSON / stderr=进度` 分离？ □ 图 DPI ≥150？ □ **并发度参数化且 ≤ 上游上限？** □ **429/503 有退避？**

**最小模板（Python）**：
```python
import json, os, sys, time
OUT = "runs/task"; os.makedirs(OUT + "/items", exist_ok=True)
items = [...]                                   # 单元列表，每个有稳定 id
done = {f[:-5] for f in os.listdir(OUT + "/items") if f.endswith(".json")}
todo = [x for x in items if str(x["id"]) not in done]
t0 = time.time()
for i, x in enumerate(todo, 1):
    r = do_one(x)                               # 单元计算
    json.dump(r, open(f'{OUT}/items/{x["id"]}.json', "w", encoding="utf-8"), ensure_ascii=False)
    el = time.time() - t0; eta = el / i * (len(todo) - i)
    print(f"[{i}/{len(todo)}] {i/len(todo)*100:.0f}% t={el:.0f}s eta={eta:.0f}s", file=sys.stderr, flush=True)
print(json.dumps({"status": "ok", "total": len(items), "done": len(done) + len(todo)}, ensure_ascii=False))
```

> 与 `AGENTS.md`「脚本设计铁律」互补：那条讲"非阻塞 / 参数化 / JSON / stderr"；
> 本条补"**长了怎么不死、怎么看得见**"。二者一起才算合格的长任务脚本。

---

## 最新版

本技能**开源**，**最新版以这两处为准**：

- **GitHub**：https://github.com/TOMUIV/project-organization-skill
- **ClawHub**：`project-organization`（`clawhub install project-organization`）

> 版本对不上、想看改了什么 → 去上面任一渠道查。
