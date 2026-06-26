# 示例 1：宠物匹配

**场景**: 用户第一次使用，想领只宠物

---

## 用户触发

```
用户：我想领只宠物
```

---

## Skill 执行流程

### Step 1: 告知用户有 12 只宠物可选

```
🐿️ 小蚂蚁：好的！我们有 12 只投资宠物，每只有不同的投资风格和性格~ 🐾

先做个投资性格测试吧（10 道题），帮你找到最适合的宠物！
```

### Step 2: 引导用户做测试

```
第 1 题：市场跌了 20%，你的第一反应是？
A. 赶紧卖出，止损
B. 继续持有，不操作
C. 加仓，这是机会
D. 很焦虑，但不知道怎么办
```

### Step 3: 计算匹配度

```bash
# 后台执行
python scripts/pet_match.py --user-id user_001 --answers "[1,2,3,4,5,6,7,8,9,10]"
```

**输出**:
```json
{
  "top_pets": [
    {"pet_type": "songguo", "match_score": 92},
    {"pet_type": "wugui", "match_score": 85},
    {"pet_type": "haitun", "match_score": 78}
  ]
}
```

### Step 4: 推荐 Top 3 宠物

```
✅ 测试结果出来啦！

🥇 Top 1: 🐿️ 松果（匹配度 92%）
性格：谨慎、爱囤积、安全感第一
策略：极简定投，自动储蓄
口头禅："慢慢来，比较快"

🥈 Top 2: 🐢 慢慢（匹配度 85%）
性格：耐心、长期主义
策略：买入持有，时间复利
口头禅："时间会奖励耐心"

🥉 Top 3: 🐬 豚豚（匹配度 78%）
性格：友好、被动投资
策略：指数定投，分散风险
口头禅："跟着市场走"

你想选哪只宠物？
```

### Step 5: 用户选择后告知激活方法

```
用户：松果

🐿️ 小蚂蚁：好的！你的本命宠物是🐿️ 松果！

📥 激活方法：
1. 安装技能：/clawhub install investment-buddy-pet
2. 启动宠物：python scripts/heartbeat_engine.py start --pet-type songguo

要我帮你复制链接吗？
```

---

## 关键代码

```python
# scripts/pet_match.py
def run_test(user_id: str, answers: List[int]) -> Dict:
    """
    运行宠物匹配测试
    
    Args:
        user_id: 用户 ID
        answers: 用户答案列表 [1,2,3,4,5,6,7,8,9,10]
    
    Returns:
        {
            "top_pets": [...],
            "user_profile": {...}
        }
    """
    # 计算五维评分
    scores = calculate_personality_scores(answers)
    
    # 计算与 13 只宠物的匹配度
    pet_scores = []
    for pet_type in PET_TYPES:
        score = calculate_pet_match(scores, pet_type)
        pet_scores.append({"pet_type": pet_type, "match_score": score})
    
    # 排序返回 Top 3
    pet_scores.sort(key=lambda x: x['match_score'], reverse=True)
    
    return {
        "top_pets": pet_scores[:3],
        "user_profile": scores
    }
```

---

## 合规检查点

- ✅ 测试结果标注"仅供参考"
- ✅ 不承诺宠物能带来收益
- ✅ 提供风险提示

---

**文件位置**: `examples/01-pet-match.md`  
**创建时间**: 2026-04-14
