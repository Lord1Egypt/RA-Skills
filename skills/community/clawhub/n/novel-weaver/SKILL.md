---
name: novel-weaver
slug: novel-weaver
displayName: Novel Weaver
version: 1.35.2
author: wUwproject
license: MIT
description: 结构化小说写作辅助技能。场景配置→大纲生成→因果链双重验证→pipeline 流程门禁→子结构先行规划→情绪混合系统→文风约束→人格驱动→分段写作→连通性补充→风格校验+逻辑检查(含实体状态+关系链)+大纲忠实度+结尾收束验证+实体关系追踪+角色别名识别+跨章行为摘要。全流程硬约束+门禁跟踪。
sensitive_access: false
critical_write: false
permission_weight: MEDIUM
data_dir: ../.standardization/novel-weaver/projects
tags: ['novel', 'writing', 'story', 'outline', 'scene-setting', 'character', 'personality', 'emotion', 'writing-style', 'narrative', 'workflow']
trigger: 写小说/写故事/写文章/长文写作/故事大纲/场景配置/我想写个故事
trigger_negative: 翻译/改写/润色/校对/简洁回答/做 PPT/画图
h1_position: true
meta_field_sync: true
create_permissions_md: true
trigger_quality: add_triggers
faq_unparsable: reformat
antipattern_count: add_examples
external_data_dir: true
---
# novel-weaver — 结构化小说写作辅助技能

> 本文档由 skill-standardization 自动化审计与维护。

## 约束

- **[强制] 新会话第一步：查看项目** — 不要猜路径，先运行以下命令查看已有的项目：
  ```bash
  python scripts/novel_workflow_engine.py list-projects
  ```
  如果无项目则创建新项目，有项目则记录 state_path 供后续命令使用。
- **[强制] 流程门禁系统** — 在阶段转换时自动 require 前置门禁：→writing 检查 outline_causality + sub_causality；→stage3_ready 检查 fidelity + ending_verify。门禁状态查看：`python novel_pipeline_gate.py status <state_path>`
- **[强制] 核心规划字段保护 + 串行阻断** — `novel_state_manager.py` 对核心字段做 MD5 指纹校验，LLM 不可更新。context_loader 检测上一子结构是否为 completed，否则 HOOK-BLOCK 阻断。串行写入，一次只改一个子结构
- **[强制] 串行阻断** — context_loader 加载子结构上下文时检测上一子结构 state 是否为 completed。若为 pending 则输出 HOOK-BLOCK 并给出 write-sub 修复命令，强制走管道完成标记后才能继续。子结构写作必须串行
- **[必须] 先确认+规划再写作** — 场景配置和大纲必须经用户确认，每章先 `plan-chapter`（含必填 writing_prompt + 情绪 tone + 可选 emotions）→ 因果链验证 → 通过串行阻断检查，才可开始写作
- **[必须] 写作规范** — 每段 ≤200行（自然段落结束），atomic write 逐行 fsync，正文禁止 `L##S##` 标记行（会被阻断）
- **[强制] 写作中登记** — 新角色出场时 `novel_state_manager.py add-char`。**plan-chapter 已加硬阻断**：sub_structures 中出现未登记角色名时 HOOK-BLOCK，必须先 add-char 才能写入。
- **[强制] 每章六检 + 自动完结** — 写完所有子结构后 **write-sub 自动触发 finalize-chapter**（不再需手动执行）：章内连通性 → 跨章承诺链 → 风格校验 → 逻辑检查 → **语义检查** → **推理审核** → 聚合硬性问题并阻断。通过后自动推进 phase。
- **[必须] 全文三检** — 全文完成后必须：`novel_fidelity.py`（大纲忠实度）+ `verify-ending`（结尾收束验证）+ `set-phase stage3_ready`

### 数据目录

⚠️ **LLM 禁止手工拼写路径！禁止去 Read memory/ 目录下的文件！** 
所有项目数据只能通过以下途径获取：

**列出所有项目（新会话第一件事）：**
```bash
python scripts/novel_workflow_engine.py list-projects
```
或
```python
import sys; sys.path.insert(0, 'scripts')
from _path_utils import list_projects, resolve_state_path, DATA_DIR
projects = list_projects()
# DATA_DIR = ~/.workbuddy/skills/.standardization/novel-weaver/projects/
```

**获取单个项目 state 路径：**
```python
from _path_utils import resolve_state_path
state_path = resolve_state_path()       # 自动从 .project 缓存读取
# 或传入项目名: resolve_state_path("赛博搏杀记")
```

**读取项目状态：**
```python
state_path = resolve_state_path()
if state_path:
    import json; state = json.loads(open(state_path, encoding='utf-8').read())
from _path_utils import DATA_DIR
proj = DATA_DIR / '项目名' / 'data' / 'novel_state.json'
```

**目录结构（代码推导，仅供理解）：**
```text
{DATA_DIR}/<项目名>/
├── data/novel_state.json          ← 状态文件
├── data/.workbuddy/gate_state.json ← 门禁状态
├── data/reports/                   ← 检查报告
├── chapters/L##/S##.txt          ← 章节正文
└── .project                       ← 路径缓存

模型文件存储在：
  ~/.workbuddy/skills/.standardization/novel-weaver/models/
  ├── bge-small-zh/                 ← BERT 33MB（可选）
  └── ds-r1-distill-qwen-1.5b/     ← DeepSeek-R1-Distill-Qwen-1.5B ~1GB（CPU 可跑）
```
数据目录由 `_path_utils.py` 统一管理。

## 触发条件

**正向触发：**
- 「我想写个故事/小说/文章」→ 触发完整流程
- 「帮我生成故事大纲和场景配置」→ 触发阶段1
- 「根据大纲写下一章」→ 触发阶段2（续写模式）
- 「帮我检查文章前后是否一致」→ 触发风格校验
- 「把这几段串起来」→ 触发连通性补充
- 「检查文章是否偏离了大纲」→ 触发大纲忠实度报告
- 「安装模型/下载模型/装 BERT/装推理模型」→ 触发模型安装流程：安装 sentence-transformers + 下载 bge-small-zh 或安装 transformers + 下载推理审核模型

**否定条件：**
- 用户只是说「改写/润色」——不是本技能范畴
- 用户要求翻译/简洁回答——不触发

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

本技能采用渐进式 MD 体系，SKILL.md 为入口（≤230行），详细内容拆分到 references/。

| 文件 | 内容 |
| ------ |------|
| references/execution_standards.md | 字数管理 / 文体规范 / novel_state.json 结构 / 子结构文件格式 / 章节输出 / 时间线 / 角色表 / 结尾收束 / 实体关系追踪 |
| references/hooks.md | 参考文档 | 全量流程钩子 + 门禁系统一览（类型/行为/脚本） |
| references/antipatterns.md | 常见反模式与正确做法 |
| references/faq.md | 常见问题与排除 |
| references/changelog.md | 版本更新日志 |
| references/examples.md | 使用示例 |
| references/permissions.md | 权限说明 |
| references/LICENSE.md | MIT 许可证 |

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
| -------- |------| ---------- |----------|
| `references/LICENSE.md` | 许可协议 | 开源许可证声明（MIT）。包含：MIT 许可证完整文本。 | R-26 |
| `references/antipatterns.md` | 规范指南 | skill 编写中的常见反模式。包含：错误做法示例、正确做法示例、避坑指引。 | R-18 |
| `references/changelog.md` | 版本管理 | 版本更新日志。包含：版本号、更新类型、修复项、升级说明。 | R-24 |
| `references/examples.md` | 使用示例 | 各场景完整执行示例。包含：CLI 命令、执行过程、输出结果。 | R-25 C-17 |
| `references/execution_standards.md` | 参考文档 | 字数目标在**规划、写作、检查**三个阶段使用同一套标准，不允许 AI 自行配置或偏离。 | 无 |
| `references/faq.md` | 常见问题 | 常见疑问与解答。包含：问题分类、原因分析、解决方案。 | R-19, R-25 C-19 |
| `references/hooks.md` | 参考文档 | 门禁状态查看：`python novel_pipeline_gate.py status <state_path>` | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描说明与测试结论。包含：风险等级、高权限操作说明、测试概览、计时统计。 | R-15, R-16 |
## 工作流程

### 写作流程

1. **LLM 生成场景配置** → 输入 用户模糊想法 → 输出 novel_info/setting — 生成人物/时代/地点/风土人情/核心冲突
2. **LLM 生成一级大纲** → 输入 场景配置 → 输出 chapters[] title/overview — L01-L15编号+标题+每章概述
3. **因果链验证(outline)** → 输入 chapters[] overview → 输出 outline_causality 门禁 — 逐链节检查L01→L02→...因果递进
4. **用户确认** → 输入 大纲 → 输出 确认/修正 — 钩子阻断式，未确认不得进入阶段2
5. **初始化 novel_state.json** → 输入 大纲 → 输出 novel_state.json — chapters/characters/timeline 骨架
6. **规划章子结构** → 输入 章节标题+概述 → 输出 sub_structures[] JSON — S01-S05+标题+概述+tone+**必填 writing_prompt(≥50字符)**+可选 emotions。缺失 writing_prompt 则 plan-chapter HOOK-BLOCK
7. **注册子结构到 state** → 输入 subs_json → 输出 novel_state 更新 — MD5指纹锁定+自动字数目标+标记 is_ending/is_hook。**新角色检测+HARD-BLOCK**：sub_structures 中出现未登记角色名时阻断并提示 add-char 命令
8. **子结构因果链验证** → 输入 sub_structures → 输出 sub_causality 门禁 — 逐子结构因果递进检查
9. **set-phase writing** → 输入 outline+sub 门禁 → 输出 phase=writing — require 双门禁，不通过则阻断
10. **加载上下文（context_loader）** → 输出 4区块优先级排列：A(标识+硬性字数/文风/署名约束+写作命题框) → B(末3行+人物+人格+实体+轨迹+节奏) → C(收尾+钩子+输出模板)。无预编命题时自动从概述合成 fallback
11. **LLM 写作 → 系统组装写入** → LLM 只输出纯正文（末尾可带可选【别名】行）→ write-sub 自动组装标题行+别名行+标记行 → atomic_writer.v4 校验正文合法性。无别名行时系统自动补【别名】无
12. **重复10-11** → 输入 下一子结构 → 输出 全部子结构完成 — 直到该章全部子结构写完
13. **完结一章(finalize-chapter)** → 输入 章内容 → 输出 六合⼀检查报告 — **自动触发**（最后一个子结构写入后自动运行），无需手动执行
14. **全文整合(fidelity)** → 输入 全部章节 → 输出 大纲忠实度报告 — 检查是否偏离大纲
15. **结尾收束验证** → 输入 末章末子结构 → 输出 ending_report.md — 封闭式/开放式/悬停式三选一验证

### 检查系统

finalize-chapter 是章节质量的核心关卡，聚合执行 6 步检查链：

| 步骤 | 名称 | 脚本 | 作用 | 等级 |
| ------ |------| ------ |------| ------ |
| 1 | 章内连通性 | `novel_continuity.py` | 检测子结构间时间/角色是否断裂 | SOFT |
| 2 | 跨章承诺链 | `novel_continuity.py` | 检测上章尾与下章头的关键词续接 | SOFT |
| 3 | 风格校验 | `novel_style_check.py` | 禁用词/末行标记/超200行检测 | HARD |
| 4 | 逻辑检查 | `novel_logic_check.py` | 角色一致性+时间线+概述关键词命中率 | HARD |
| 5 | 语义检查(BERT) | `novel_semantic_check.py` | overview-vs-content 对齐+子结构间语义跳跃（有模型时） | HARD |
| 6 | 推理审核(DeepSeek-R1) | `novel_reasoning_check.py` | 因果合理/人格一致/情绪弧/对话/论证（有模型时） | HARD/SOFT |

步骤 1-4 由 Python 刚性规则驱动，**无外部依赖**。步骤 5-6 需本地已缓存的模型，**无模型时自动跳过（绝不联网）**。有 HARD 问题则阻断（不标记门禁），写入 `_fixes.json`；全部通过则标记 `chapter_finalized` 门禁。

> ⚠️ **GPU 安全**：步骤 5-6 强制 CPU 运行（`CUDA_VISIBLE_DEVICES=-1`），避免与 LM Studio 等 GPU 应用冲突。模型推理全程使用系统内存。

### 模型安装（可选，仅步骤5-6需要）

步骤 5-6 只在本地已有模型缓存时运行。无模型时静默跳过，按需安装：

BERT 语义检查（92MB，纯 CPU 可跑，第5步）：
```bash
pip install sentence-transformers -i https://mirrors.aliyun.com/pypi/simple/
HF_ENDPOINT=https://hf-mirror.com python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-zh-v1.5')"
```

DeepSeek-R1-Distill-Qwen-1.5B 推理审核（~3.7GB，CPU 可跑，第6步）：

安装 transformers + torch + accelerate，有 prebuilt wheel：

```bash
# 1. 装 transformers + torch + accelerate
pip install transformers torch accelerate -i https://mirrors.aliyun.com/pypi/simple/

# 2. 下载 DeepSeek-R1-Distill-Qwen-1.5B 模型（~3.7GB，hf-mirror）
HF_ENDPOINT=https://hf-mirror.com python -c "from transformers import AutoModel; AutoModel.from_pretrained('deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', trust_remote_code=True)"
```

