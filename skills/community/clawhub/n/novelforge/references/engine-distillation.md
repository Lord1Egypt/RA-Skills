# Narrative Engine Distillation (叙事引擎提炼与构建规范)

本规范定义从小说或文章语料中提炼因果规律与技法体系的**叙事引擎 (Narrative Engine) 提炼与构建标准**。

## 核心理念 (Core Philosophy)

> **提炼的是 HOW they think / write（叙事操作系统），而不是 WHAT they said（表层词句模仿）。**

一个合规的叙事引擎是一套可插拔、状态感知的叙事推理卡片库：
- 它用什么**心智模型**驱动故事的因果与世界？（镜片与核心动力）
- 它在具体场景下用什么**技法卡**把控节奏与张力？（微观启发式）
- 它的**适用条件**是什么？（在什么阶段、场景类型下激活）
- 它的**诚实边界与反模式**是什么？（绝对不能做什么、何处不适用）

---

## 五步蒸馏标准作业程序 (5-Step SOP)

当用户通过自然语言提出引擎生成需求（如「参考这几篇科幻小说蒸馏一个硬科幻引擎」）时，Agent 按以下五步闭环执行：

### Step 1: 语料摄入与叙事采样 (Source Ingestion)
1. **收集参考样本**：读取用户提供的多篇代表性章节、创作谈、深度长评或写作随笔。
2. **结构化提取**：
   - 寻找反复出现的因果推动逻辑（如关键转折来自何种动机？）。
   - 提取张力营造与释放方式（动作、道具、对白停顿、场景反差）。
   - 统计视角偏好、段落节奏与留白模式。

### Step 2: 叙事心智模型提炼 (Mental Models, 3-7个)
对候选论点执行**三重检验**：
- **跨场景复现**：在不同场景或章节中反复出现，体现真切的创作信念；
- **推演生成力**：面对全新的未写剧情，能指导角色做出符合该逻辑的选择；
- **非平庸排他性**：不是“写得生动”这种放之四海而皆准的套话，而是具有独特取向的思考方式（例如“人物因果优于巧合降神”、“技术逻辑决定生死代价”）。

输出结构写入 `cards/models.json`：
```json
{
  "id": "ENG-M1",
  "kind": "model",
  "name": "character-driven causality",
  "when": {"phase": ["outline", "scene", "review"]},
  "requires": ["character"],
  "hardness": "required",
  "prompt": "让关键剧情转折来自人物真实的选择与代价，拒绝机械降神或外部作者意志强推。"
}
```

### Step 3: 场景技法卡提炼 (Technique Cards, 5-10条)
将具体写作直觉转化为明确的“情境-动作”启发式卡片，必须声明触发谓词：
- `when.phase`: `["outline", "scene", "draft", "review", "settlement"]`
- `when.scene_types`: `["conflict", "relationship", "choice", "loss", "transition"]`
- `requires`: 依赖的角色、关系、伏笔等前置状态
- `hardness`: `required` (硬性门禁), `recommended` (推荐遵循), `optional` (视情选用)

输出结构写入 `cards/techniques.json`：
```json
{
  "id": "ENG-T1",
  "kind": "technique",
  "name": "unresolved tension hook",
  "when": {"phase": ["outline", "draft", "review"], "requires": ["chapter_boundary"]},
  "hardness": "required",
  "prompt": "章节结尾留下清晰的情节悬念、认知错位或行动代价，驱动后续章节。"
}
```

### Step 4: 适用条件与诚实边界 (Applicability & Limits)
- **适用条件 (`applicability.md`)**：说明该引擎的优势区间（如擅长宏大推演、硬核博弈，还是细腻情感），强调方法卡只在状态匹配时激活。
- **诚实边界与反模式 (`limits.md`)**：
  - 严禁机械模仿作者语言风格或词汇；
  - 严禁借引擎名义凭空脑补未登记的设定；
  - 明确指出何种场景应主动禁用该引擎方法。

### Step 5: 打包构建与闭环验真 (Build & Verification)
Agent 自动调用底层构建命令完成文件生成与哈希验真：
```bash
python3 scripts/novelforgectl.py engine distill <source-path> --id <engine-id> [--label <label>] [--output <dir>]
```
构建器会自动计算 `manifest.json` 并通过 `load_engine` 校验。校验通过后，引擎即可通过 `novelforgectl engine install` 和 `engine use` 在任意小说项目中即插即用。

