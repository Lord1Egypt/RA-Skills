***

name: herhug-sk
description: 心理学评分引擎 - 让AI从专业角度理解用户，越用越懂你
metadata: {
"openclaw": {
"emoji": "🤗",
"homepage": "[https://github.com/xinqimiao/herHug-sk.git](https://github.com/your-username/herHug-sk)",
"requires": {
"bins": \["node"],
"env": \["OPENCLAW\_DATA\_DIR"]
}
}
}
-

# herHug - 心理学评分引擎

## 🤗 她懂你

herHug 不直接生成回复，而是提供**心理学评分标准**和**用户状态数据**，让大模型基于这些数据生成真正懂你的回复。

## 📊 核心功能

### 1. 获取评分标准

const standards = await openclaw\.skills.run('herHug', 'get-scoring-standards');

### 2. 保存用户评分

await openclaw\.skills.run('herHug', 'save-score', {
scoreData: {
timestamp: new Date().toISOString(),
content: userInput,
ocean: { ... },
emotion: { ... },
flexibility: { ... },
coping: { ... },
confidence: 0.7
}
});

### 3. 获取当前状态

const state = await openclaw\.skills.run('herHug', 'get-current-state');

### 4. 每日情绪节律分析

const rawData = await openclaw\.skills.run('herHug', 'get-daily-rhythm-data');
await openclaw\.skills.run('herHug', 'save-daily-rhythm', {
rhythmAnalysis: analysisResult
});
🧠 心理学维度
维度	文件	说明
OCEAN+HEXACO	01\_ocean\_hexaco.md	人格骨架
情绪节律	02\_emotional\_rhythm.md	时间模式（日/周/恢复力）
心理灵活性	03\_psychological\_flexibility.md	适应能力
应激应对	04\_stress\_coping.md	压力反应
置信度	05\_confidence\_scoring.md	可信程度
⚠️ 置信度原则
≥0.7：可完全信任，用于调整回复风格
0.4-0.7：谨慎参考，多用询问确认
<0.4：忽略，用默认策略

📁 数据存储
所有用户数据保存在 \~/.openclaw/data/herHug/<userId>/ 目录下：
raw\_scores.jsonl：原始评分（时间序列）
daily\_rhythm.json：每日情绪节律
current\_state.json：当前状态（含置信度加权）
emotion\_tracker.json：主动关怀待办
confidence\_report.json：置信度报告

🔄 完整工作流程
每次对话后：大模型分析输入 → 生成评分 → 调用 save-score
每天一次：调用 get-daily-rhythm-data → 大模型分析 → 调用 save-daily-rhythm
每次回复前：调用 get-current-state → 根据状态生成回复
