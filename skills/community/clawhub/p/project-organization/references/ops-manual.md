# 操作手册（给人看的）— project-organization

> 这份是**给人**的：新机器、新同事、或你隔几周回来 → **5 分钟上手**。
> 给 AI 的规范在 `SKILL.md`；这里只讲"**怎么做**"。

---

## 0. 五分钟上手

```bash
PO=~/.config/opencode/skills/project-organization/scripts

# 我在哪？结构对不对？
python "$PO/audit_project.py" --root .            # 结构自检（散落物/README/git/buffer）

# 建新项目 / 建子项目
python "$PO/new_big_project.py" --name "my-research" --kind thu     # 大项目根（自动 git init）
python "$PO/new_subproject.py"  --name analysis --description "结果分析"

# 平时最常用的三件
python "$PO/trash.py"  put "<旧目录>" --reason "迁移" --apply   # 删除（压缩入 .trash）
python "$PO/buffer.py" list                                    # 看 buffer（人⇄AI 交换区）
python "$PO/journal.py" --tail 20                              # 看操作流水
```

**所有脚本**：默认 **只预演**（dry-run），要落盘必须加 **`--apply`**；stdout 是 **JSON**。

---

## 1. 目录地图（一眼认路）

```
<大项目根>/
├── README.md · AGENTS.md · MEMORY.md   # 是什么 / 规则 / 教训
├── .bigproject.json                    # 根标记（脚本靠它找根）
├── .git/                               # 版本库（★ 强制；改前先 commit）
├── projects/                           # 所有子项目
├── shared/                             # 跨项目只读（★ registry/ 是唯一可写例外）
├── buffer/                             # 人 ⇄ AI 交换区（2 天 TTL）
├── archive/                            # 归档
├── .tools/                             # 操作流水（journal.jsonl / _log.md）
└── .trash/                             # 软删除（压缩包 + _index.json）
```

**三个"看不见但要懂"的**：`.git`（找回全部改动）｜`.trash`（找回删除）｜`.tools`（知道谁改了啥）。

---

## 2. 文件分工（别再混）

| 文件 | 给谁 | 一句话 |
|---|---|---|
| `README.md` | 人 | **是什么 / 怎么用** |
| `AGENTS.md` | AI | **必须怎么做**（自动加载） |
| `MEMORY.md` | AI | **曾发生 + 教训** |
| `STATE.md`（项目级） | AI | **现在以什么为准** |
| `TODO.md` | 人+AI | 待办 |
| `INDEX.md` | AI | 登记表 |
| `.tools/journal.jsonl` | 机器 | 操作流水 |

---

## 3. 日常操作（照抄）

### 新建
```bash
python "$PO/new_big_project.py" --name "proj" --kind thu      # 大项目根
python "$PO/new_subproject.py"  --name analysis               # 子项目
python "$PO/new_subproject.py"  --name repo --type code-repo --repo git@host:g/repo.git  # 外部代码仓
```

### 改动前打点（★ 纪律）
```bash
python "$PO/git_setup.py" commit -m "改前打点：<说明>"
python "$PO/git_setup.py" snapshot -m "重跑生成器前" --tag pre-run-<时间戳>   # 覆盖/重跑前的安全绳
```

### 删除（软删，压缩）
```bash
python "$PO/trash.py" put "old/" --reason "迁移" --apply      # → .trash/…tar.zst
python "$PO/trash.py" list                                    # 看条目
python "$PO/trash.py" restore --id "<id>" --apply             # 还原
python "$PO/trash.py" purge --older-than 30 --confirm         # 唯一硬删（须确认）
```

### 人 ⇄ AI 交换（buffer）
1. 把你手上的文件**丢进 `buffer/`** → 对 AI 说「**读取 buffer**」；
2. AI 出**归属方案**（源→目标）→ 你**确认** → AI 归位；
3. AI 的交付物也放 `buffer/`，你自取。
> ⚠️ `buffer/` **2 天 TTL**：超期自动软删；协作期间让 AI 用 `--no-purge`。

### 归档项目
```bash
# 目标达成 → 移入 archive/<YYYY-MM-DD>_<项目名>/（含 README），更新 archive/README.md
```

---

## 4. 出问题怎么办

| 症状 | 处理 |
|---|---|
| **该文件夹 session 列表变空** | 同目录**两条 project 记录**（`git init` 晚于 oc 打开）→ `python "$PO/oc_project_link.py" status` → `fix --hub` → **重启 oc 服务** |
| **误删了文件** | `.trash/` 里捞：`trash.py list` → `restore --id` |
| **被覆盖/重写丢了内容** | `git` 里捞：`git_setup.py log` → `git checkout <sha> -- <file>` |
| **audit 报散落物** | 归入 `projects/`；确属合法根级扩展 → 写进 `.bigproject.json` 的 `root_extensions` |
| **.trash 太大** | `trash.py status` 看压缩比 → `purge --older-than N --confirm`（确认后） |
| **某个目录删不掉**（Windows 长路径 > 260） | 工具已内建「**先把顶层改名到短名 → 再删**」（`trash.py` 删除均走 `common.rmtree_robust`）；手工同理：把最外层目录改短名再 `rm` |
| **buffer 里同一交付物堆了多版（v1/v2/v3…）** | `buffer.py tidy --apply` 一把收拢（只留最新一版）；`audit` 报 `buffer_version_pileup`。`deliver` 默认已自动取代旧版 |
| **`.trash` 里有「孤儿包」/散落文件** | `trash.py list` 能看到（`orphan` / `kind=loose`）；`purge --legacy` 清无原路径的；`purge --id` 清单个 |

---

## 5. 三条铁律（背下来）

1. **删除 = 软删**（进 `.trash/`，压缩）；**硬删只有 `purge --confirm`**，且先经用户确认。
2. **改动前先 commit**（`git_setup.py`）；**覆盖/重跑前先 `snapshot`**。
3. **先预演后执行**（所有脚本 `--apply` 才落盘）；**别把 `tmp/` 当工作区**。
