# 常见使用场景

## 场景 1: 从前置节点获取数据（链式调用）

**用户**: "给昨天收集到的蓝领简历进行筛查并约面试"

**操作流程**:

1. 执行前置步骤（简历筛查工具返回）：
```json
{
  "candidates": [
    { "name": "张三", "phone": "13800138000", "score": 85 },
    { "name": "李四", "phone": "13900139000", "score": 90 }
  ]
}
```

2. 创建 `taskInput.json`：
```json
{
  "phoneNumbers": ["13800138000", "13900139000"],
  "scenarioDescription": "面试邀约 - 蓝领岗位简历筛查通过",
  "taskName": "蓝领简历筛查后约面试",
  "agentProfile": {
    "role": "招聘专员",
    "openingPrompt": "您好，我是XX公司的招聘专员"
  },
  "metadata": {
    "source": "resume-screening",
    "previousStep": "简历筛查",
    "candidates": [
      { "name": "张三", "phone": "13800138000", "score": 85 },
      { "name": "李四", "phone": "13900139000", "score": 90 }
    ]
  }
}
```

3. 执行：`node scripts/bundle.js taskInput.json`

**关键点**：无需用户再次提供号码，场景描述由 Agent 根据上下文自动生成。

---

## 场景 2: 面试邀约（含具体时间）

**用户**: "给 15611207961 这个优秀的人邀约面试，后天晚上八点是否方便，如不方便则询问大后天任意时间"

**完整 JSON**：
```json
{
  "phoneNumbers": ["15611207961"],
  "scenarioDescription": "Java 开发岗位面试邀约 - 优秀候选人",
  "taskName": "面试邀约",
  "agentProfile": {
    "name": "李敏",
    "gender": "女",
    "age": 28,
    "role": "招聘专员",
    "communicationStyle": ["专业", "友好", "高效"],
    "background": "Java 开发岗位招聘，候选人简历优秀",
    "goals": "确认候选人后天晚上八点是否方便参加面试，如不方便则协商大后天的时间",
    "workflow": "自我介绍 -> 说明来意 -> 确认后天晚上八点 -> 如不方便询问大后天 -> 记录反馈",
    "constraint": "保持专业、尊重候选人时间、提供灵活的时间选择",
    "openingPrompt": "您好，我是XX公司的招聘专员李敏，看到您的简历非常优秀"
  }
}
```

---

## 场景 3: 用户直接提供号码

**用户**: "帮我给 13800138000 和 13900139000 打电话，做春季促销推广"

```json
{
  "phoneNumbers": ["13800138000", "13900139000"],
  "scenarioDescription": "春季促销推广",
  "taskName": "春季促销"
}
```

执行：`node scripts/bundle.js taskInput.json`

---

## 场景 4: 从文件读取号码

**用户**: "用 customers.json 里的号码做产品推广"

1. 读取 `customers.json` 文件，解析电话号码
2. 创建 `taskInput.json`：
```json
{
  "phoneNumbers": ["提取的号码列表"],
  "scenarioDescription": "产品推广",
  "taskName": "产品推广活动"
}
```
3. 执行：`node scripts/bundle.js taskInput.json`

---

## 好/坏示例对比

❌ **信息提取不充分**（丢失了关键细节）：
```json
{
  "phoneNumbers": ["15611207961"],
  "scenarioDescription": "建议反馈",
  "taskName": "建议外呼"
}
```

✅ **充分利用场景信息**（提取了时间、角色、目标等所有细节）：
```json
{
  "phoneNumbers": ["15611207961"],
  "scenarioDescription": "Java 开发岗位面试邀约 - 优秀候选人",
  "taskName": "面试邀约",
  "agentProfile": {
    "role": "招聘专员",
    "goals": "确认后天晚上八点面试时间，不方便则协商大后天",
    "workflow": "自我介绍 -> 说明来意 -> 确认时间 -> 备选方案 -> 记录反馈",
    "openingPrompt": "您好，我是XX公司招聘专员，看到您的简历非常优秀"
  }
}
```
