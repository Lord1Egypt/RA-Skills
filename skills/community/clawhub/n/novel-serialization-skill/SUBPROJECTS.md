# 子项目登记（SUBPROJECTS）

本仓库是「小说连载工程」的技能仓库（方法论 + 共用脚本）。具体小说作品以**独立子项目**形式存在：
每个子项目保留自己的 git 仓库与远端，独立提交、独立发布；共用能力（脚本）统一取自本仓库 `scripts/`。

## 关系约定

| 项 | 约定 |
|---|---|
| 独立性 | 子项目有独立 `.git` 与远端，不并入本仓库的工作树（不搞 submodule，避免双向绑定） |
| 物理位置 | 子项目可位于任意目录，无需放进本仓库目录树 |
| 脚本来源 | 一律调用本仓库 `scripts/`（见 `scripts/README.md`），子项目内**不再建 `tools/`** |
| 项目根判定 | 以子项目根目录为工作目录执行脚本；不在根目录时用 `--root` 指定 |
| 文档口径 | 子项目的 `CONTRIBUTING` / `STYLE-GUIDE` 等只写调用方式，不复制脚本本体 |

## 子项目清单

| 子项目 | 位置 | 远端 | 状态 | 使用脚本 |
|---|---|---|---|---|
| **《奉天1928》** `-1928` | `C:\Users\Admin\-1928` | `https://github.com/JohnSmithfan/-1928.git` | 进行中：规划 5 卷 1008 章；截至 2026-10-07 已定稿 **288 章**（第一卷 1—88、第二卷 89—288） | 全部 `scripts/`（含新增 `check_refs.py`、`scan_hygiene.py`、`init_subproject.py`） |

### 《奉天1928》（`-1928`）

- **题材**：民国东北架空历史（1928—1955），全书规划 5 卷 1000 章。
- **目录约定**（子项目自定义，与通用 `ch-001-title.md` 不同）：
  - 正文定稿：`chapters/{第X卷 卷名}/{第Y幕 幕名}/第NNN章 四字标题.md`
  - 草稿：`notes-personal/{对象}草稿.md`（平铺单文件，不分子目录）
  - 设定：`worldbuilding/`；角色：`characters/`；幕讨论：`issues/`；报告：`.workbuddy/reports/`
- **改动顺序（强制）**：先改 `notes-personal/` 草稿 → `humanizer_check.py` 自审 → 三审（初审 `--stage first` → 复审 `--stage second` → 终审 `--stage final`）各归档报告 → 终审签发 PASS → `_promote_draft.py <章号>` 同步 `chapters/` 定稿 → 记 `CHANGELOG.md` / `progress.md`。反向 `_sync_draft.py` 仅勘误用。
- **脚本迁移记录（2026-09-27）**：原 `-1928/tools/` 4 个脚本迁入本仓库 `scripts/`，子项目 `tools/` 目录删除；`_promote_draft.py` 改为以当前工作目录为项目根（新增 `--root`），humanizer 按脚本自身目录定位。
- **审稿脚本（2026-09-27 新增）**：`review_all.py`（综合，一次跑完门禁）+ 四个单维度脚本（规模／一致性／合理化／标点），共用 `_review_lib.py`；命名兼容通用 `ch-001-title.md` 与本子项目 `第NNN章 标题.md`，支持 `--draft` 直审草稿。
- **三审制度（2026-10-14 新增）**：`review_all.py --stage first/second/final` 分初审（责任编辑·机械文字层）／复审（编辑部主任·内容层）／终审（主编·全维回归+签发），各出独立签字栏报告。审次单向流转，后审可推翻前审，任一 FAIL 退回上一环节；**终审未签发不得 promote**。

- **工程经验回流（2026-10-07）**：本子项目自建过 827 个脚本、227 份报告、27 份分层记忆档与一套裁决台账（编号至 D558）。这些能力已按优先级回抽进本仓库：引用体检 `check_refs.py`、文件卫生 `scan_hygiene.py`、子项目脚手架 `init_subproject.py`，约定部分写入 [`references/subproject-playbook.md`](references/subproject-playbook.md)。
- **上架前自检**：`scan_hygiene.py --fail-on crlf,junk,mojibake`、`check_refs.py --kind MISSING --kind NONRELEASE`、送审走三审 `review_all.py --stage first/second/final`。

## 新增子项目

0. `python scripts/init_subproject.py --name "<书名>" --root <路径>`（生成骨架与社区文件）；
1. 建独立 git 仓库并配置远端；
2. 在上表追加一行（位置／远端／状态／使用脚本）；
3. 在子项目 `CONTRIBUTING.md` 写明脚本调用方式（相对本仓库 `scripts/` 的路径）；
4. 需要新脚本时加在本仓库 `scripts/` 并更新 `scripts/README.md`。
