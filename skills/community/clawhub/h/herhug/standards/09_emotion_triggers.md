# 情绪触发场景评分标准

## 理论基础
记录用户在什么场景下产生什么情绪，帮助AI理解用户的情绪模式。

---

## 数据结构

```json
{
  "emotionTriggers": [
    {
      "emotion": "anxiety",
      "triggers": ["deadline", "考试", "面试"],
      "contexts": [
        { "trigger": "deadline", "count": 5, "lastOccurrence": "2026-03-15", "intensity": 0.7 },
        { "trigger": "考试", "count": 3, "lastOccurrence": "2026-03-10", "intensity": 0.8 }
      ],
      "confidence": 0.75
    },
    {
      "emotion": "joy",
      "triggers": ["项目完成", "朋友", "游戏"],
      "contexts": [...],
      "confidence": 0.7
    }
  ]
}
```

---

## 情绪类型与常见触发场景

### 焦虑 (Anxiety)
**常见触发**：
- 工作：deadline、会议、汇报、面试
- 学习：考试、论文、答辩
- 关系：不确定的关系、等待回复
- 健康：身体不适、检查结果

### 悲伤 (Sadness)
**常见触发**：
- 失去：分手、离别、宠物去世
- 失败：项目失败、考试失利
- 孤独：独处、节日、深夜
- 回忆：想起过去

### 愤怒 (Anger)
**常见触发**：
- 不公：被误解、被欺负
- 挫折：计划被打乱、事情不顺
- 关系：争吵、背叛
- 系统：技术问题、服务差

### 喜悦 (Joy)
**常见触发**：
- 成就：项目完成、考试通过、获奖
- 关系：聚会、朋友、恋爱
- 休闲：游戏、旅行、美食
- 惊喜：意外的好消息

### 恐惧 (Fear)
**常见触发**：
- 未来：不确定性、重大决定
- 健康：疾病、疼痛
- 关系：害怕失去、被抛弃
- 社会：公开演讲、社交场合

### 平静 (Calm)
**常见触发**：
- 环境：自然、安静的地方
- 活动：阅读、冥想、散步
- 时间：清晨、深夜独处
- 状态：事情完成、放松

---

## 场景识别规则

### 关键词匹配
```javascript
const triggerKeywords = {
  "deadline": ["deadline", "截止", "到期", "最后期限"],
  "考试": ["考试", "考", "测验", "面试", "答辩"],
  "工作": ["工作", "公司", "老板", "同事", "加班"],
  "关系": ["朋友", "恋人", "分手", "吵架", "家人"],
  "健康": ["生病", "医院", "身体", "疼", "不舒服"],
  "金钱": ["钱", "工资", "花销", "账单", "贷款"],
  "未来": ["未来", "以后", "打算", "计划", "不确定"],
  "孤独": ["一个人", "孤独", "没人", "寂寞"]
};
```

### 时间模式
- 深夜（22:00-05:00）→ 更容易触发负面情绪
- 周一 → 可能触发"周一综合症"
- 节日 → 可能触发孤独或喜悦

---

## 应用场景

### 1. 预测情绪
当用户提到某个触发场景时，AI可以预判可能的情绪：
```
用户："明天有个deadline"
AI预判：可能焦虑 → 主动提供支持
```

### 2. 主动关怀
根据历史触发场景，在相关时间点主动关心：
```
用户之前提到"考试"会焦虑
→ 考试前主动询问准备情况
```

### 3. 避免触发
了解用户的负面触发场景，避免无意中触碰：
```
用户"分手"会悲伤
→ 避免主动提起相关话题
```

---

## 更新逻辑

每次用户表达情绪时：
1. 识别情绪类型
2. 提取可能的触发场景
3. 更新对应情绪的触发列表
4. 统计出现频率和强度

```javascript
function updateEmotionTrigger(emotion, trigger, intensity) {
  const existing = emotionTriggers.find(e => e.emotion === emotion);
  if (existing) {
    const context = existing.contexts.find(c => c.trigger === trigger);
    if (context) {
      context.count++;
      context.intensity = (context.intensity + intensity) / 2;
      context.lastOccurrence = new Date().toISOString();
    } else {
      existing.contexts.push({ trigger, count: 1, intensity, lastOccurrence: new Date().toISOString() });
    }
  } else {
    emotionTriggers.push({
      emotion,
      triggers: [trigger],
      contexts: [{ trigger, count: 1, intensity, lastOccurrence: new Date().toISOString() }],
      confidence: 0.5
    });
  }
}
```

---

## 置信度计算

- **高置信度 (0.7-1.0)**：同一场景触发同一情绪 ≥3次
- **中置信度 (0.4-0.7)**：同一场景触发同一情绪 1-2次
- **低置信度 (0-0.4)**：仅单次记录