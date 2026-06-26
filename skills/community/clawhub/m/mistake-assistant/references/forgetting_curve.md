# 艾宾浩斯遗忘曲线复习算法

## 原理

艾宾浩斯遗忘曲线描述了人类记忆的遗忘规律：学习后遗忘立即开始，且遗忘速度先快后慢。

## 标准复习间隔

基于艾宾浩斯研究，推荐复习间隔：

```
第1次复习：学习后 20分钟
第2次复习：学习后 1小时
第3次复习：学习后 9小时
第4次复习：学习后 1天
第5次复习：学习后 2天
第6次复习：学习后 6天
第7次复习：学习后 1个月
第8次复习：学习后 3个月
```

## 实用简化版（每日提醒）

考虑到实际学习场景，采用简化版本：

| 复习次数 | 间隔天数 | 记忆保持率 |
|---------|---------|-----------|
| 第1次   | 1天     | ~80%      |
| 第2次   | 2天     | ~85%      |
| 第3次   | 4天     | ~90%      |
| 第4次   | 7天     | ~93%      |
| 第5次   | 15天    | ~95%      |
| 第6次   | 30天    | ~98%      |

## 算法实现

### 计算下次复习日期

```python
from datetime import datetime, timedelta

REVIEW_INTERVALS = [1, 2, 4, 7, 15, 30]

def get_next_review_date(created_date: datetime, review_count: int) -> datetime:
    """
    计算下次复习日期
    
    Args:
        created_date: 错题创建日期
        review_count: 已复习次数
    
    Returns:
        下次复习日期
    """
    if review_count >= len(REVIEW_INTERVALS):
        # 超过预设次数后，每30天复习一次
        interval = 30
    else:
        interval = REVIEW_INTERVALS[review_count]
    
    return datetime.now() + timedelta(days=interval)
```

### 动态调整

根据掌握状态调整间隔：

- **已掌握**：间隔延长50%（下次复习时间推后）
- **仍需强化**：间隔缩短50%（加快复习频率）
- **忘记**：重置复习周期，从头开始

```python
def adjust_review_interval(next_review: datetime, status: str) -> datetime:
    """
    根据掌握状态调整复习间隔
    """
    if status == "已掌握":
        # 延长间隔
        delta = next_review - datetime.now()
        return datetime.now() + delta * 1.5
    elif status == "仍需强化":
        # 缩短间隔
        delta = next_review - datetime.now()
        return datetime.now() + delta * 0.5
    elif status == "忘记":
        # 重置到第1次复习
        return datetime.now() + timedelta(days=1)
    return next_review
```

## 复习优先级

当有多道错题需要复习时，按以下优先级排序：

1. **超期未复习**：当前日期 > 应复习日期
2. **今日到期**：当前日期 = 应复习日期
3. **错误次数多**：按错误次数降序
4. **难度高**：困难 > 中等 > 简单

```python
def sort_mistakes_for_review(mistakes: list) -> list:
    """
    为错题排序，确定复习优先级
    """
    def priority_score(m):
        score = 0
        # 超期加分
        if m['next_review'] < datetime.now():
            score += 1000
        # 错误次数加分
        score += m.get('error_count', 0) * 10
        # 难度加分
        difficulty_scores = {'困难': 5, '中等': 3, '简单': 1}
        score += difficulty_scores.get(m.get('difficulty'), 3)
        return score
    
    return sorted(mistakes, key=priority_score, reverse=True)
```

## 学习建议

基于统计数据，提供个性化学习建议：

1. **遗忘曲线陡峭**：科目/知识点需要增加复习频率
2. **错误集中**：重点攻克薄弱知识点
3. **长期未掌握**：考虑重新学习基础概念
4. **掌握率过低**：建议寻求老师/同学帮助

## 数据结构

```json
{
  "id": "math-2024-001",
  "subject": "数学",
  "topic": "二次函数",
  "created_at": "2024-01-15T10:30:00",
  "review_history": [
    {
      "date": "2024-01-16T09:00:00",
      "status": "仍需强化",
      "note": "又忘记配方了"
    },
    {
      "date": "2024-01-17T15:30:00",
      "status": "已掌握",
      "note": "这次做对了"
    }
  ],
  "review_count": 2,
  "next_review": "2024-01-21T00:00:00",
  "mastered": false
}
```
