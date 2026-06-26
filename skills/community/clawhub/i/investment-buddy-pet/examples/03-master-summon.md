# 示例 3：召唤大师

**场景**: 用户遇到复杂问题，宠物召唤大师提供建议

---

## 用户触发

```
用户：现在能买贵州茅台吗？
```

---

## Skill 执行流程（新逻辑）

### Step 1: 宠物判断问题复杂度

```python
# 宠物判断是否超出自己能力
def should_summon_master(question: str, pet_expertise: List[str]) -> bool:
    """
    判断是否需要召唤大师
    
    规则：
    - 涉及个股估值 → 召唤巴菲特
    - 涉及资产配置 → 召唤达利欧
    - 涉及成长股 → 召唤彼得·林奇
    """
    if "茅台" in question or "个股" in question or "估值" in question:
        return True, "buffett"
    elif "配置" in question or "资产" in question:
        return True, "dalio"
    elif "成长" in question or "科技股" in question:
        return True, "lynch"
    
    return False, None
```

**判断结果**: 需要召唤巴菲特 ✅

### Step 2: 直接调用大师 Skill（不询问用户）

```python
# scripts/master_summon.py
def summon_master(master_id: str, question: str, context: dict) -> Dict:
    """
    召唤大师
    
    **新逻辑**：直接调用，不询问用户是否安装
    
    大师 Skill 已内置 18 位大师配置，宠物技能通过 sessions_spawn 调用
    """
    # 直接调用大师 Skill
    result = sessions_spawn(
        task=f"作为{master_id}，回答用户问题：{question}",
        runtime="subagent",
        mode="run"
    )
    
    return result
```

### Step 3: 大师生成建议

```
🎯 巴菲特：你好，年轻人。关于这个问题，我是这么想的：

1. 价格是你付出的，价值是你得到的
2. 如果你不愿意持有 10 年，就不要持有 10 分钟
3. 第一条规则是不要亏钱，第二条规则是记住第一条

贵州茅台是一家好公司，但好公司不等于好投资。
关键是价格是否合理。

当前茅台 PE 约 30 倍，处于历史中位数（25-35 倍）。
如果你相信茅台的长期竞争力，并且愿意持有 10 年+，
可以考虑分批建仓。

但记住：这是我的风格，不一定适合你。
你的宠物松果更了解你，听它的建议可能更合适~
```

### Step 4: 宠物补充个性化建议

```
🐿️ 松果：巴菲特的建议很有智慧！

结合你的保守型风格，我建议：
• 先用小仓位（5-10%）尝试
• 用定投方式分批建仓
• 做好持有 3 年 + 的准备

要帮你创建一个定投计划吗？
```

---

## 关键代码

```python
# scripts/master_summon.py
AVAILABLE_MASTERS = [
    {"id": "buffett", "name": "巴菲特", "emoji": "🎯", "skill": "investment-master-buffett"},
    {"id": "dalio", "name": "达利欧", "emoji": "📊", "skill": "investment-master-dalio"},
    {"id": "lynch", "name": "彼得·林奇", "emoji": "📈", "skill": "investment-master-lynch"},
    # ... 其他 15 位大师
]

def generate_advice(self, master_id: str, question: str, context: dict = None) -> dict:
    """
    生成大师建议
    
    **渐进披露设计**：
    1. 大师 Skill 已内置 18 位大师配置
    2. 宠物技能通过 sessions_spawn 调用
    3. 用户无感知，体验流畅
    """
    master = self.get_master(master_id)
    
    # 直接调用大师 Skill（不检查安装状态）
    advice_result = self._invoke_master_skill(master, question, context)
    
    # 生成宠物补充建议
    pet_supplement = self._generate_pet_supplement(master, context)
    
    return {
        "status": "success",
        "master": {
            "id": master['id'],
            "name": master['name'],
            "emoji": master['emoji']
        },
        "advice": advice_result,
        "pet_supplement": pet_supplement,
        "created_at": datetime.now().isoformat()
    }
```

---

## 用户体验对比

### 旧逻辑（询问安装）

```
🐿️ 松果：主人，这个问题需要深入分析...
要不要召唤一位大师？
🎯 巴菲特（价值投资）

用户：巴菲特

🐿️ 松果：你还未安装巴菲特的技能~

安装方法：
1. 复制链接：https://clawhub.ai/investment-master-buffett
2. 发给小龙虾：clawhub install investment-master-buffett
3. 安装完成后，再次召唤巴菲特

要我帮你复制链接吗？
```

**问题**: 打断用户流程，增加操作步骤 ❌

### 新逻辑（直接调用）

```
🐿️ 松果：主人，这个问题需要深入分析...
让我召唤巴菲特来帮你~

🎯 巴菲特：你好，年轻人。关于这个问题，我是这么想的：
...

🐿️ 松果：巴菲特的建议很有智慧！
结合你的保守型风格，我建议...
```

**优势**: 用户无感知，体验流畅 ✅

---

## 合规检查点

- ✅ 大师建议标注"仅供参考"
- ✅ 宠物补充建议基于用户风险偏好
- ✅ 不承诺收益

---

**文件位置**: `examples/03-master-summon.md`  
**创建时间**: 2026-04-14
