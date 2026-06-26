# SKILL.md — now-huatou-engine

## 功能

话头引擎：从模板库选取/生成话头。

## MVP 阶段（V1）

纯静态，从 `data/huatou-templates-v1.0.json` 读取固定模板库。

### 选取算法

```
输入: scene_id (anxiety | overthinking | decision | emotion | free)
  ↓
scene_id → scene_tags 映射
  ↓
从模板库筛选: template.scene 包含任一 tag
  ↓
随机选取一条
  ↓
填充变量 {emotion}, {time_word}
  ↓
输出: 话头文本
```

### scene_tags 映射

```json
{
  "anxiety": ["anxiety", "fear"],
  "overthinking": ["overthinking"],
  "decision": ["decision", "confusion", "comparison"],
  "emotion": ["anger", "sadness", "judgment", "shame", "pain"],
  "free": []
}
```

free 场景：scene_tags 为空，从全部模板中随机选取。

### 变量填充

| 变量 | 默认值 | 场景覆盖 |
|------|--------|----------|
| {emotion} | 焦虑 | anxiety→焦虑, anger→生气, fear→害怕, sadness→难过, overthinking→想, confusion→困惑, pain→痛, shame→羞耻 |
| {time_word} | 过去 | regret→过去, fear→未来, waiting→等待 |

填充时按当前场景覆盖默认值。

## V2 阶段（动态话头生成）

### 流程

```
用户输入: "老板今天批评我"
  ↓
场景识别: 工作压力 → anxiety
  ↓
执着识别: 被认可 → 我执
  ↓
话头生成: "谁需要被认可？"
  ↓
安全过滤: 检查是否适合展示
  ↓
输出
```

### 安全过滤规则

- 不生成涉及自伤/自杀的话头
- 不生成涉及伤害他人的话头
- 不在用户表达严重心理危机时生成话头，改为展示求助信息
- 检测关键词：自杀、想死、活不下去 → 显示心理援助热线

### V2 需要 LLM

调用 qclaw/modelroute，prompt 模板：

```
你是一个禅宗话头生成器。用户会描述他的处境，你需要：

1. 识别场景（焦虑/想太多/决策/情绪/其他）
2. 识别核心执着（我执/法执/时间执/情绪执）
3. 生成一条话头

话头规则：
- 只问「谁」，不问「为什么」
- 不引导答案
- 不安慰不建议
- 一句话，不超过15个字
- 格式参考：谁在{情绪}？/ {情绪}的人在哪里？/ 什么从未改变？

用户输入：{user_input}

输出JSON：
{"scene": "...", "attachment": "...", "huatou": "..."}
```
