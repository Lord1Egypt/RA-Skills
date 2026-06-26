# File Structure

## 1. Goal

Use a stable, reusable project structure for every novel project.

The project should not exist only in chat output.  
It should exist as a clean local file tree that supports:
- planning
- drafting
- revision
- proofreading
- final delivery
- optional Feishu sync

Execution packages used for drafting, polishing, or proofreading are runtime-only inline payloads.
They are not canonical project artifacts and should not be persisted as part of the project file tree.

---

## 2. Root project directory

Default root:

`/root/.openclaw/novels/[小说名称]/`

Use the confirmed novel title or a normalized project title as the project folder name.

Prefer a stable name once the title is confirmed.  
Avoid renaming the project directory repeatedly after downstream files already exist.

---

## 3. Canonical project layout

Use this layout by default:

```text
/root/.openclaw/novels/[小说名称]/
├── 00A_热点扫描.md
├── 00B_用户偏好.md
├── 00C_底盘与切口决策.md
├── 00_选题报告.md
├── 01_想法.md
├── 01A_风格圣经.md
├── 01B_总主线与卷级推进.md
├── 02_大纲.md
├── 03_人物小传.md
├── 04_章节骨架.md
├── 04A_开篇设计.md
├── 05_前情回顾.md
├── 05A_本轮校对报告.md
├── 05_本轮章节规划.md
├── 05B_世界规则账本.md
├── 05C_伏笔回收台账.md
├── 05D_关系状态表.md
├── 05E_能力与资源变化表.md
├── 05F_时间与事件图谱.md
├── 05G_伏笔三元组账本.md
├── 05H_角色认知与误判表.md
├── 05I_证据链与矛盾对照表.md
├── 06_反馈与修订.md
├── 07_终审报告.md
├── characters/
│   ├── [角色名].md
│   └── ...
├── staging/
│   └── [stage]/[branch-id]/
│       ├── 00_脑暴任务卡.md
│       ├── 01_直觉俗套清单.md
│       ├── 02_反驳与否认.md
│       ├── 03_变异候选.md
│       ├── 04_保留候选.md
│       └── 05_定稿结论.md
└── manuscript/
    ├── [章节文件].md
    └── ...
```

Optional extra files may exist when needed, but do not break the core structure.

---

## 4. Required top-level files

### 4.1 `00A_热点扫描.md`
Purpose:
- store discovery-stage hot-search and trend-scan output
- preserve the external market signal snapshot that informed topic selection

Update timing:
- create or refresh during discovery before final topic recommendation

### 4.2 `00B_用户偏好.md`
Purpose:
- store the user preference capture for genre, platform, tone, constraints, and priorities
- preserve the explicit intake record that shapes the discovery recommendation

Update timing:
- create during discovery after user discussion
- revise when the user materially changes discovery constraints

### 4.3 `00C_底盘与切口决策.md`
Purpose:
- store the approved market-facing lane decision
- record primary track, optional secondary flavor, platform mode, and anti-template guardrails
- explain why this lane can sustain conflict and where it most often collapses

### 4.4 `00_选题报告.md`
Purpose:
- store topic research
- store title recommendation logic
- store final title confirmation
- store audience and market positioning

### 4.5 `01A_风格圣经.md`
Purpose:
- store the locked style contract for the project
- record narration distance, rhythm density, dialogue ratio, platform mode, and forbidden drift directions

### 4.6 `01B_总主线与卷级推进.md`
Purpose:
- store the total-story engine and volume-level propulsion
- record the mainline sentence, escalation logic, and cost structure that must survive long serialization

### 4.7 Core planning files
These files remain required and should stay canonical:
- `01_想法.md`
- `02_大纲.md`
- `03_人物小传.md`
- `04_章节骨架.md`
- `04A_开篇设计.md`

Use them for:
- story concept expansion
- outline structure
- character package summary
- chapter-level skeleton
- opening-gate approval before first-batch prose drafting

### 4.8 `05_前情回顾.md`
Purpose:
- store continuity-critical recap context after a batch closes
- support later-batch restoration without relying on chat memory

Update timing:
- update only after the current batch passes downstream review and closes

### 4.9 `05_本轮章节规划.md`
Purpose:
- store the approved chapter-plan package for the current drafting batch
- define batch scope, chapter objectives, hooks, and local climaxes before prose drafting

Ownership:
- parent workflow produces and revises this file before drafting delegation
- drafting subagents do not modify this planning artifact during execution

Update timing:
- create before drafting prose generation begins for the current batch
- revise only during chapter-plan review within the drafting stage

### 4.10 `05A_本轮校对报告.md`
Purpose:
- store the current canonical proofreading result for the active batch
- provide the formal proofreading artifact before final review

Update timing:
- overwrite on each accepted proofreading pass for the active batch
- use this file, not chat output, as the formal proofreading artifact

### 4.11 Ledger set
These four files are mandatory once the project enters prose drafting:
- `05B_世界规则账本.md`
- `05C_伏笔回收台账.md`
- `05D_关系状态表.md`
- `05E_能力与资源变化表.md`

Purpose:
- prevent long-form drift
- keep world rules, foreshadow, relationships, and resources file-backed
- give polishing and proofreading a stable baseline beyond chat memory

### 4.12 Narrative-intelligence set
These four files are parent-owned derived support artifacts:
- `05F_时间与事件图谱.md`
- `05G_伏笔三元组账本.md`
- `05H_角色认知与误判表.md`
- `05I_证据链与矛盾对照表.md`

Purpose:
- keep timeline / CFPG / ToM / evidence-chain views file-backed
- give proofreading and final review a canonical consistency surface beyond chat memory
- preserve parent-owned checker output without changing drafting / polishing / proofreading child contracts

Update timing:
- initialize after planning approval
- refresh after accepted drafting / polishing / proofreading results
- treat these as canonical derived artifacts, but not as new user-approval gates in this slice

### 4.13 `06_反馈与修订.md`
Purpose:
- store the current active formal revision
- store affected scope and revision plan
- store the latest closed formal revision result

### 4.14 `07_终审报告.md`
Purpose:
- store the latest final-review decision
- store delivery readiness judgment
- store final-review strengths, major issues, blockers, and next action
- provide the canonical final-review artifact for completion checks

---

## 5. Character directory rules

Directory:

`characters/`

### 5.1 Purpose
Store detailed individual character files.

### 5.2 File granularity
Default: one important character per file.

Use separate files for:
- protagonist
- major supporting characters
- major antagonists
- structurally important recurring roles

### 5.3 Naming rules
Preferred:
- `[角色名].md`

Optional if ordering matters:
- `[编号]_[角色名].md`

Choose one style and keep it stable within the same project.

### 5.4 Content expectations
Each character file should ideally include:
- basic profile
- personality core
- motivation
- conflict
- growth arc
- relationships
- key plot function
- emotional or visual highlight potential

---

## 6. Manuscript directory rules

Directory:

`manuscript/`

---

## 7. Staging directory rules

`staging/` is not a generic scratchpad.

- only explicit brainstorming mode may write to `staging/`
- keep branches under `staging/<stage>/<branch-id>/`
- when a Cliche Exhaustion branch exists, use `00_脑暴任务卡.md` through `05_定稿结论.md` as the default artifact layout
- use the authoritative branch filenames `00_脑暴任务卡.md`, `01_直觉俗套清单.md`, `02_反驳与否认.md`, `03_变异候选.md`, `04_保留候选.md`, and `05_定稿结论.md`
- only `05_定稿结论.md` may authorize canonical backfill from that branch
- after one branch is promoted, copy selected content back into canonical files
- after promotion, delete sibling branches and stale branch files immediately

### 6.1 Purpose
Store draft or refined chapter text.

### 6.2 Naming rules
Preferred:
- `第X章_[标题].md`

If one chapter is split into parts:
- `第X章_01_[标题].md`
- `第X章_02_[标题].md`

### 6.3 Stability rule
Do not rename chapter files casually after downstream review or sync has happened.

If chapter names must change, preserve numbering consistency.

### 6.4 Batch writing compatibility
This structure supports:
- one chapter per file
- one chapter split into multiple files
- multi-file batches

But the visible chapter order should still remain obvious from filenames.

---

## 7. Naming discipline

### 7.1 Be consistent
Use one naming convention for:
- character files
- chapter files
- top-level planning files

### 7.2 Avoid unstable filenames
Do not keep renaming files across stages unless the user explicitly changes structure.

### 7.3 Prefer readability
Names should be readable by humans and easy to map into Feishu Wiki.

---

## 8. Minimal file completeness standard

A project is minimally structured when it has:
- a root project directory
- `00A_热点扫描.md`
- `00B_用户偏好.md`
- `00C_底盘与切口决策.md`
- `00_选题报告.md`
- `01_想法.md`
- `01A_风格圣经.md`
- `01B_总主线与卷级推进.md`
- `02_大纲.md`
- `04A_开篇设计.md`
- `characters/`
- `manuscript/`

A project is strongly structured when it also has:
- `03_人物小传.md`
- `04_章节骨架.md`
- `05_本轮章节规划.md`
- `05_前情回顾.md`
- `05B_世界规则账本.md`
- `05C_伏笔回收台账.md`
- `05D_关系状态表.md`
- `05E_能力与资源变化表.md`
- `05F_时间与事件图谱.md`
- `05G_伏笔三元组账本.md`
- `05H_角色认知与误判表.md`
- `05I_证据链与矛盾对照表.md`
- `06_反馈与修订.md`
- `07_终审报告.md`
- major character files
- stable chapter files

---

## 9. Stage-to-file mapping

### Intake / topic stage
- populate `00A_热点扫描.md`
- populate `00B_用户偏好.md`
- populate `00C_底盘与切口决策.md`
- populate `00_选题报告.md`

### Idea expansion stage
- populate `01_想法.md`
- populate `01A_风格圣经.md`
- populate `01B_总主线与卷级推进.md`

### Outline stage
- populate `02_大纲.md`
- optionally populate `04_章节骨架.md`

### Character stage
- populate `03_人物小传.md`
- populate `characters/*.md`

### Opening gate
- populate `04A_开篇设计.md`
- do not enter first-batch prose drafting until this file is approved

### Drafting stage
- populate `05_本轮章节规划.md`
- populate `manuscript/*.md`
- maintain `05B_世界规则账本.md`
- maintain `05C_伏笔回收台账.md`
- maintain `05D_关系状态表.md`
- maintain `05E_能力与资源变化表.md`
- parent may refresh `05F_时间与事件图谱.md`
- parent may refresh `05G_伏笔三元组账本.md`
- parent may refresh `05H_角色认知与误判表.md`

### Revision stage
- populate or update `06_反馈与修订.md`

### Proofreading / final-review handoff
- accepted proofreading may refresh `05I_证据链与矛盾对照表.md`
- final review consumes `05I` / `narrativeIntelligence.consistency.openCriticalIssues` as blocker input

### Later stages
- revise existing files rather than fragmenting into many inconsistent duplicates

---

## 10. Revision discipline

When refining work:
- prefer updating canonical files
- avoid creating random suffix copies unless versioning is truly required

Avoid uncontrolled file sprawl such as:
- `大纲_最终版_再改版.md`
- `大纲_最终版2.md`
- `大纲_最终版2_真的最终.md`

---

## 11. Delivery discipline

At delivery time, the project should be:
- structurally complete
- navigable
- stable in naming
- ready for archive or Feishu sync

The file tree should tell the project story clearly even without chat history.
