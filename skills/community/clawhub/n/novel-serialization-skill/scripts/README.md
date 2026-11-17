# scripts/ —— 小说工程共用脚本

> 本目录存放**跨子项目共用**的自动化脚本。脚本属于技能仓库（GitHub Novel Serialization Skill），
> 子项目只消费、不拷贝；子项目内不再自建 `tools/` 目录。

## 调用约定

脚本**不在子项目内**，因此以「子项目根目录」为工作目录执行：

| 项目根判定 | 说明 |
|---|---|
| 默认 | 取**当前工作目录**，须含 `chapters/` 与 `notes-personal/` |
| 显式 | `_promote_draft.py --root <项目根>` |

从子项目根目录调用的相对路径写法（以 `-1928` 为例）：

```bash
cd "C:/Users/Admin/-1928"

# 去 AI 痕迹自检
python "../GitHub Novel Serialization Skill/scripts/humanizer_check.py" chapters/
python "../GitHub Novel Serialization Skill/scripts/humanizer_check.py" notes-personal/正文草稿.md

# 列出待改写命中句
python "../GitHub Novel Serialization Skill/scripts/_list_hits.py" --kind vague --target chapters/

# 草稿 → 定稿同步
python "../GitHub Novel Serialization Skill/scripts/_promote_draft.py" 031 034 036 --dry-run

# 定稿 → 草稿回写（仅勘误）
python "../GitHub Novel Serialization Skill/scripts/_sync_draft.py" 041

# 审稿：一键跑完全部门禁（规模／一致性／合理化／标点／去 AI 痕迹）
python "../GitHub Novel Serialization Skill/scripts/review_all.py" --batch "第9批" \
    --out .workbuddy/reports/草稿审核报告_2026-09-27.md

# 审稿：三审制度分阶段（初审／复审／终审各出报告、各带独立签字栏）
python "../GitHub Novel Serialization Skill/scripts/review_all.py" --stage first  --out .workbuddy/reports/初审_第9批.md
python "../GitHub Novel Serialization Skill/scripts/review_all.py" --stage second --out .workbuddy/reports/复审_第9批.md
python "../GitHub Novel Serialization Skill/scripts/review_all.py" --stage final  --out .workbuddy/reports/终审签发_第9批.md

# 单维度审稿
python "../GitHub Novel Serialization Skill/scripts/review_scale.py" --target 4000
python "../GitHub Novel Serialization Skill/scripts/review_continuity.py"
python "../GitHub Novel Serialization Skill/scripts/review_rationality.py"
python "../GitHub Novel Serialization Skill/scripts/review_punctuation.py"
```

脚本内部依赖按 `Path(__file__).parent` / `sys.executable` 解析，不受调用路径影响；
`_promote_draft.py` 亦按自身目录定位 `humanizer_check.py`。

## 脚本清单

| 脚本 | 用途 | 关键参数 |
|---|---|---|
| `humanizer_check.py` | 去 AI 痕迹自检：AI 腔词密度、结构套话与抽象评价、模糊副词、情绪标签、套路句式、章末升华、成语连用、破折号/省略号/感叹号密度、段长变异系数；按 PASS / WARN / FAIL 分级 | `<文件或目录>`、`--out <报告.md>` |
| `_list_hits.py` | 列出待改写的命中句（人工改写前取句） | `--kind banned/pattern/vague/emotion/idiom/dash`、`--target <路径>`、`--limit N` |
| `_promote_draft.py` | 草稿 → 定稿（release）同步：按章号整块写入、写前快照 `_trash/定稿同步前_<日期>/`、字数前后对比、章标题零差异校验、humanizer 门禁（FAIL 拒绝同步） | `<章号...>`、`--root`、`--draft`、`--dry-run`、`--report`、`--no-check`、`--force` |
| `_sync_draft.py` | 定稿 → 草稿回写（**仅勘误**，不得作常规改动通道） | `<章号...>` |
| `review_all.py` | **综合审稿**：跑门禁并输出审核报告（对象／结论表／问题明细／规模概览／待办清单／签字栏）；`--stage` 按三审制度分阶段（`first` 初审＝humanizer+scale+punctuation／`second` 复审＝continuity+rationality／`final` 终审＝全维回归+签发），各审次出独立签字栏；不带 `--stage` 为一次跑全部（旧行为） | `--batch`、`--stage`、`--chapters`、`--draft`、`--target`、`--skip`、`--out` |
| `review_scale.py` | **规模审查**：每章字数、达标率、缺口、分布区间与缺口 TOP（供分批扩写排序） | `--target`、`--max`、`--chapters`、`--draft`、`--out` |
| `review_continuity.py` | **一致性审稿**：专名异写、角色年龄与档案冲突、时间线倒流、标题与正文不符、timeline 登记缺失、草稿与定稿章标题零差异 | `--min-freq`、`--min-variant`、`--max-variant`、`--min-ent-len`、`--year-tol`、`--out` |
| `review_rationality.py` | **合理化审查**：重复段落（章内／跨章）、超长段与残句、对话占比、序数跳号、视角混用、伏笔未回收、大纲要点偏离 | `--outline`、`--max-para`、`--max-dialogue`、`--min-cover`、`--out` |
| `review_punctuation.py` | **标点审查**：引号错位、半角标点、直引号、繁体混入、英文残留、标点密度、重复与行首标点、书名号配对 | `--max-dash`、`--max-ellipsis`、`--max-excl`、`--out` |
| `_review_lib.py` | 审稿脚本公共库（内部模块，不直接执行）：项目根判定、章节索引、字数口径、报告渲染 | — |
| `check_refs.py` | **引用体检**：八档判定 `OK/LOCAL/TEMPLATE/BARE/PRIVATE_OK/NONRELEASE/MISSING/PRIVATE_MISSING`；**release 文件只引用 release 文件，非 release 文件可引用全部**；反引号路径按仓库根起算、真链接（label 在 `[]`、target 在 `()`）按本文件相对，两套体系分开判。豁免模式写在仓库根 `.refsignore`（本地/pre-commit/CI 三处共用同一份） | `--root`、`--json`、`--kind`、`--fail-on`、`--ignore`、`--ignore-file`、`--out` |
| `scan_hygiene.py` | **文件卫生**：CRLF／乱码／临时垃圾／空文件／缺尾换行／超行数预算；`--fix` 就地改回 LF | `--root`、`--fix`、`--max-lines`、`--allow`、`--json`、`--fail-on`、`--out` |
| `init_subproject.py` | **子项目脚手架**：生成目录骨架、Issue/PR 模板、CODEOWNERS、裁决台账、报告索引、分层记忆入口 | `--name`、`--root`、`--scripts`、`--owner`、`--force`、`--dry-run` |

### 落盘守则（Windows 必读）

`io.open(p, 'w', encoding='utf-8')` 在 Windows 上 `newline` 默认为 `None`：
**读时把 CRLF 归一成 LF，写时又把 LF 转回 CRLF**。任何被 Python 文本模式改过一小段的 md，
整份都会变成 CRLF，`.gitattributes` 拦不住脚本落盘那一笔。

> **凡写文本，一律 `io.open(p, 'w', encoding='utf-8', newline='\n')`。**

自检：`python scripts/scan_hygiene.py --root . --fail-on crlf,junk,mojibake`。

# 引用体检（release 文件不得引用不存在或非 release 的文件）
python "../GitHub Novel Serialization Skill/scripts/check_refs.py" --root . \
    --ignore '^state/|^worldbuilding/|^characters/|^notes-personal/|^issues/'

# 文件卫生（CRLF／乱码／垃圾文件／行数预算）
python "../GitHub Novel Serialization Skill/scripts/scan_hygiene.py" --root . \
    --max-lines 500 --allow "CHANGELOG.md,progress.md" --fail-on crlf,junk,mojibake

# 新建子项目骨架
python "../GitHub Novel Serialization Skill/scripts/init_subproject.py" --name "书名" --root ../新书
```

### 审稿脚本设计约定

1. **命名兼容**：同时支持通用命名 `ch-001-title.md` 与子项目命名 `第001章 标题.md`；草稿按 `## 第N章` 分块。
2. **通用参数**：`--root`（项目根，默认当前工作目录）、`--chapters`（指定章号）、`--draft`（审草稿而非定稿）、`--out`（Markdown 报告落盘）。
3. **判定分级**：`FAIL` 必须修改且不得进定稿；`WARN` 需人工复核（综合结论记 `REVISE`）；`PASS` 达标。
4. **宁可漏报，不可误报**：各检查项均按真实语料校准过阈值（如繁体按词组而非单字扫描、异写只查等长实词差异、年份孤例不判倒流），避免噪声淹没真问题。
5. **只挑可疑处**，最终以人工复核为准；报告自带签字栏。三审制度下签字栏按审次生成（初审＝责任编辑／复审＝编辑部主任／终审＝主编签发）。
6. **三审维度归属**：初审（`first`）管机械与文字层 `humanizer`/`scale`/`punctuation`；复审（`second`）管内容层 `continuity`/`rationality`；终审（`final`）全维回归 + 通读签发。审次单向流转，后审可推翻前审（须写明理由），前审不得推翻后审；任一 `FAIL` 阻断 promote。详见 `SKILL.md` Verification Gates 与 `references/method-patterns-publishing.md` §7。

## 门禁约定

- 改动一律**先进子项目草稿**（`notes-personal/`），草稿 `humanizer_check.py` 通过且审核通过后，才允许用 `_promote_draft.py` 同步进 `chapters/` 定稿。
- 送审走**三审制度**：`review_all.py --stage first`（初审·责任编辑）→ `--stage second`（复审·编辑部主任）→ `--stage final`（终审·主编签发），每审次各出一份带独立签字栏的报告，全部归档到 `.workbuddy/reports/`。审次单向流转，任一 `FAIL` 退回上一环节；**终审未签发（或 FAIL 未清零）不得 promote**。
- `_promote_draft.py` 默认执行 humanizer 自检，FAIL 拒绝同步；`--force` 为例外通道，`--no-check` 不推荐。
- 纯勘误（错别字、标点、繁简、断行）可直改定稿并用 `_sync_draft.py` 回写草稿。

## 新增子项目脚本

1. 脚本放本目录，命名沿用 `_` 前缀表示内部工具；
2. 项目根一律取当前工作目录，禁止写死任何子项目绝对路径；
3. 同步更新本文件清单，并在 `SUBPROJECTS.md` 标注该子项目使用的脚本。
