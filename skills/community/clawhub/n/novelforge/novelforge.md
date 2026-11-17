---
name: novel-workflow
description: "通用长篇小说创作主流程：项目初始化、结构化大纲、章节蓝图、上下文编译、正文、审查、结算与原生 Wiki 构建。"
---

# Novel workflow

## 语言约定

本 Skill 的人机交互统一使用简体中文。命令、路径、JSON 键名、状态枚举和程序错误码
保持原样，以保证脚本兼容；其余说明、审查、交接和写作建议均用中文输出。

本流程服务于通用小说创作，不预设题材、作者、语言、章节长度或世界观。
项目可以选择一个或多个 Narrative Engine；Engine 的方法只在当前状态满足适用
条件时激活。所有机器状态由 `scripts/novelforgectl.py` 管理。

## 0. SOP 流水线执行模型 (Pipeline Execution Model)

本流程不要求用户记忆或手动触发大量细粒度底层命令。整套创作被组织为**可复用、可中断、可恢复的标准作业程序 (SOP 流水线)**，由系统统一协调并自动推进。

流水线标准阶段流转：

```text
INIT (项目初始化与 Wiki 脚手架创建)
  → BLUEPRINT (蓝图设计与校验)
  → CONTEXT (显式依赖编译与上下文锁定)
  → DRAFT (正文起草)
  → REVIEW (质量质检与引擎审查)
  → SETTLEMENT (事实结算与 Wiki 事实更新)
  → DELIVERY (Wiki 校验与交付)
```

用户只需用自然语言（如「写第1章」「继续写下一章」）发起指令，Agent 通过统一流水线调度器自动推进：

```bash
python3 scripts/novelforgectl.py pipeline advance <project-root> [chapter-id]
```

- **自动执行**：每当创作产物就绪（如蓝图已编写、正文已完成、审查已通过），流水线会自动校验并推进所有确定性门禁，无需人工分步敲击命令。
- **可中断机制 (Interruptibility)**：
  - 当缺少必要创作产物（蓝图缺失、依赖未登记、正文未起草）、质检未通过且补丁耗尽、或用户主动发出暂停指令时，流水线会安全中断，将当前状态与原因持久化保存至 `.novelforge/state/pipeline.json`。
- **可恢复机制 (Resumability)**：
  - 用户随时可以通过自然语言「继续」「恢复」唤醒流水线（执行 `pipeline resume` 或 `pipeline advance`），系统基于文件哈希校验已有阶段产物，精准从中断点继续推进，不重复做功，不丢失进度。
- **状态感知**：
  - 随时可通过 `pipeline status` 获取流水线当前阶段、待办事项与阻塞原因：
    ```bash
    python3 scripts/novelforgectl.py pipeline status <project-root> [chapter-id]
    ```

## 0.1 故事筑基与立项 (Story Genesis & Inception SOP)

对于新书立项或全新故事构建，系统提供专用的**故事筑基 SOP**（详见 [references/story-genesis.md](references/story-genesis.md)）。
在动笔前，Agent 引导作者或根据投喂资料完成：
1. **题材与基调对齐**：37 个主流题材映射与复合题材（7:3 规则）；
2. **规模梯队设定**：短篇 (`short`)、中短篇 (`novella`)、中长篇 (`standard`) 或宏大长篇 (`epic`)；
3. **承载力理性诊断**：
   ```bash
   python3 scripts/novelforgectl.py project assess-capacity --scale <tier> --words <count> [--ranks <r>] [--factions <f>]
   ```
   双向诊断防崩盘：防止动力不足导致“小马拉大车”（中途注水），防止设定过度导致“大马拉小车”（短篇消化不良）。
4. **总纲与项目画像落盘**：
   ```bash
   python3 scripts/novelforgectl.py project init <project-root> --genre <genre> --scale <tier> --words <count>
   ```

## 1. Project initialization

初始化只创建空的文件型状态目录、审计日志、蓝图目录、章节目录和 Wiki 目录，
并把内置 Jin Yong Engine 作为可替换的初始 engine 配置。它不会创建任何人物、
世界观或章节内容。
项目画像可以声明：

- 项目题材和格式。
- 启用的 Engine ID。
- 视角、语言和章节长度。
- 风格检测器及其 `warning` / `blocking` 策略。
- 事实源目录和自定义字段。

用 `engine install` 添加引擎，用 `engine use` 显式切换当前引擎；安装本身不
会改变当前项目的写作状态。

Core 只验证结构；题材规则必须来自项目画像或显式 genre pack。

## 2. Outline and blueprint

每个章节蓝图必须是结构化 JSON，至少包含：

```json
{
  "id": "v01-c001",
  "phase": "scene",
  "dependencies": {
    "entities": [],
    "hooks": [],
    "relations": [],
    "events": []
  },
  "viewpoint": null,
  "scene_types": [],
  "state": {}
}
```

蓝图必须先通过 `blueprint validate`，再进入上下文编译。缺失依赖不能由 Agent
猜测补全。

## 3. Context compilation

`context build` 根据蓝图 ID 读取人物、地点、物品、关系、事件和伏笔文件，生成
带正文哈希、依赖哈希和 Engine Snapshot 的 Context Ticket。只读取显式依赖和
允许的一跳关系；严格按显式声明的依赖精准编译上下文。

## 4. Draft and review

正文 Agent 只能使用有效 Context Ticket，产出章节正文和结构化提交元数据。质量
审查分成两类：

- 结构/事实审查：脚本硬门禁，检查状态、哈希、链接、时间线、关系和伏笔引用。
- 文学/风格审查：Agent 按当前 Engine Snapshot 输出带证据的 JSON；风格检测默认
  只产生 warning。

正文可以使用心理描写、解释、留白或不同语言风格；是否推荐某种表现方式由项目
画像和 Engine 方法卡决定。

## 5. Settlement and memory

只有 `TEXT_PASS` 和 `ENGINE_PASS` 都完成后，才允许提交 Settlement。Settlement
必须引用当前正文哈希，并记录：

- 发生的事件及其来源。
- 实体属性变化。
- 角色心理压力事件（`pressure_event` 累积至阈值后触发性格转变）。
- 关系和立场变化。
- 角色新获得或失去的知识。
- 伏笔的新增、推进、兑现或失效。
- 时间和地点变化。

脚本以原子写入方式更新根目录对应设定分类文件夹（`characters/`, `locations/`, `items/` 等）下的实体 Markdown 文件（前置 YAML 元数据与 Markdown 正文叙事）并重建根目录 `index.md` 索引网络，同时在 `.novelforge/settlements/` 和 `.novelforge/audit.jsonl` 中记录机器账本。绝不进行双份投影。正文或蓝图改变后，相关上下文和 Settlement 自动标记为 `STALE`。

## 6. Engine usage & Distillation

内置 `engines/jin-yong/` 是选择性方法卡集合，详见 [engine-contract.md](references/engine-contract.md)。
它提供人物因果、情感具象化、求变、长线根、道德选择、间接呈现、幻想与人性，
以及伏笔、节奏、双重回响、逆向规划、章末牵引、对话指纹和环境舞台等方法。
每章只接收满足 `phase`、`scene_types` 和 `requires` 的卡片。

用户可通过自然语言指令要求系统参考特定小说或文章生成新引擎。
系统自动提炼因果心智模型与场景技法卡（详见 [engine-distillation.md](references/engine-distillation.md)），
并调用底层构建器打包自校验引擎：

```bash
python3 scripts/novelforgectl.py engine distill <source-path> --id <engine-id> [--label <label>]
```

## 7. Completion gate

交付前必须执行：

```bash
python3 scripts/novelforgectl.py project verify <project-root>
python3 -m unittest discover -s tests -p 'test_*.py'
```

任何结构错误、事实冲突、过期哈希或缺失审查证据都会阻止交付。风格检测只有
在项目画像明确设为 `blocking` 时才阻止交付。
