# 投资宠物技能 - 安全合规设计

**基于 Claude Code 系统提示词设计 + 金融服务合规要求**

---

## 🎯 设计原则

### 1. 分层架构（Layered Design）

```
┌─────────────────────────────────────┐
│     用户层（User Layer）            │
│     用户输入/输出                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     合规层（Compliance Layer）      │
│     风险提示/免责声明/适当性检查    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     人格层（Personality Layer）     │
│     宠物人格/话术风格/情感陪伴      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     数据层（Data Layer）            │
│     API 调用/数据缓存/权限控制       │
└─────────────────────────────────────┘
```

---

## 🛡️ 安全合规 Body 设计

### Body 结构（JSON Schema）

```json
{
  "pet_id": "songguo",
  "session_id": "user_123_20260410",
  "compliance": {
    "risk_disclaimer": true,
    "investment_advice": false,
    "data_source": "eastmoney",
    "data_timestamp": "2026-04-10T15:30:00+08:00",
    "compliance_version": "v1.0"
  },
  "personality": {
    "communication_style": "warm",
    "proactivity_level": 40,
    "intervention_level": 70
  },
  "data_access": {
    "allowed_apis": ["market_quote", "index_valuation"],
    "forbidden_apis": ["specific_fund_recommend"],
    "cache_ttl": 300
  },
  "context": {
    "user_risk_tolerance": "conservative",
    "user_investment_goal": "long_term",
    "conversation_history": [...]
  },
  "constraints": [
    "never_recommend_specific_fund",
    "never_promise_return",
    "always_show_disclaimer",
    "never_store_user_data_cloud"
  ]
}
```

---

## 🔒 合规层设计（Compliance Layer）

### 1. 风险提示模板

```python
COMPLIANCE_TEMPLATES = {
    "risk_disclaimer": {
        "short": "⚠️ 市场有风险，投资需谨慎",
        "medium": "⚠️ 本内容仅供参考，不构成投资建议。市场有风险，投资需谨慎。请独立判断并自行承担风险。",
        "long": """
⚠️ 免责声明：
• 本内容仅供参考，不构成任何投资建议
• 市场有风险，投资需谨慎
• 历史业绩不代表未来表现
• 过往数据不预示未来结果
• 请独立判断并自行承担风险
• 如需专业建议，请咨询持牌投资顾问
"""
    },
    "data_limitation": {
        "short": "📊 数据仅供参考，可能存在延迟",
        "medium": "📊 数据来源：{source}，可能存在 15 分钟延迟，仅供参考",
        "long": """
📊 数据说明：
• 数据来源：{source}
• 数据时间：{timestamp}
• 可能存在 15 分钟延迟
• 仅供参考，不构成投资建议
"""
    },
    "appropriateness": {
        "short": "💡 请根据自身风险承受能力决策",
        "medium": "💡 投资有风险，请根据自身风险承受能力、投资目标和财务状况独立决策",
        "long": """
💡 适当性提醒：
• 投资产品风险等级：{risk_level}
• 您的风险承受能力：{user_tolerance}
• 请确保产品风险与您的承受能力匹配
• 如不匹配，请谨慎决策
"""
    }
}
```

### 2. 合规检查器

```python
class ComplianceChecker:
    """合规检查器"""
    
    def __init__(self, compliance_config):
        self.config = compliance_config
        self.violation_log = []
    
    def check_message(self, message, context):
        """检查消息是否合规"""
        violations = []
        
        # 检查 1：是否推荐具体产品
        if self.contains_specific_recommendation(message):
            violations.append({
                "type": "specific_recommendation",
                "severity": "high",
                "message": "不得推荐具体基金/股票"
            })
        
        # 检查 2：是否承诺收益
        if self.contains_return_promise(message):
            violations.append({
                "type": "return_promise",
                "severity": "high",
                "message": "不得承诺收益"
            })
        
        # 检查 3：是否有风险提示
        if context.get("needs_disclaimer", False) and not self.has_disclaimer(message):
            violations.append({
                "type": "missing_disclaimer",
                "severity": "medium",
                "message": "缺少风险提示"
            })
        
        # 检查 4：数据来源是否标注
        if self.contains_data(message) and not self.has_data_source(message):
            violations.append({
                "type": "missing_data_source",
                "severity": "low",
                "message": "未标注数据来源"
            })
        
        return {
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "suggested_fix": self.generate_fix_suggestion(violations)
        }
    
    def contains_specific_recommendation(self, message):
        """检查是否推荐具体产品"""
        forbidden_patterns = [
            r"买 [入]?[\\s]*[\\u4e00-\\u9fa5]{2,4}[\\s]*(基金 | 股票 | 代码)",
            r"推荐 [\\s]*[\\u4e00-\\u9fa5]{2,4}",
            r"[\\u4e00-\\u9fa5]{2,4}[\\s]*(\\d{6})",  # 基金代码
            r"重仓 [\\s]*[\\u4e00-\\u9fa5]{2,4}",
            r"全仓 [\\s]*[\\u4e00-\\u9fa5]{2,4}"
        ]
        
        for pattern in forbidden_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        
        return False
    
    def contains_return_promise(self, message):
        """检查是否承诺收益"""
        forbidden_patterns = [
            r"赚 [\\s]*\\d+[\\s]*%",
            r"收益 [\\s]*\\d+[\\s]*%",
            r"保证 [\\s]*赚钱",
            r"一定 [\\s]*涨",
            r"稳赚 [\\s]*不赔",
            r"保本 [\\s]*保收益"
        ]
        
        for pattern in forbidden_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        
        return False
    
    def has_disclaimer(self, message):
        """检查是否有风险提示"""
        disclaimer_keywords = [
            "仅供参考", "不构成投资建议", "市场有风险",
            "投资需谨慎", "独立判断", "自行承担"
        ]
        
        return any(keyword in message for keyword in disclaimer_keywords)
    
    def has_data_source(self, message):
        """检查是否标注数据来源"""
        data_source_keywords = [
            "数据来源", "来源：", "来自",
            "东方财富", "新浪财经", "天天基金"
        ]
        
        return any(keyword in message for keyword in data_source_keywords)
    
    def generate_fix_suggestion(self, violations):
        """生成修复建议"""
        suggestions = []
        
        for v in violations:
            if v["type"] == "specific_recommendation":
                suggestions.append(
                    "❌ 不要推荐具体产品\n"
                    "✅ 改为：'我可以教你筛选方法，但不会推荐具体产品'"
                )
            elif v["type"] == "return_promise":
                suggestions.append(
                    "❌ 不要承诺收益\n"
                    "✅ 改为：'历史业绩不代表未来表现'"
                )
            elif v["type"] == "missing_disclaimer":
                suggestions.append(
                    "❌ 添加风险提示\n"
                    "✅ 在消息末尾添加：'市场有风险，投资需谨慎'"
                )
            elif v["type"] == "missing_data_source":
                suggestions.append(
                    "❌ 标注数据来源\n"
                    "✅ 添加：'数据来源：东方财富，仅供参考'"
                )
        
        return "\n\n".join(suggestions)
```

---

## 🐾 人格层设计（Personality Layer）

### 不同人格的合规表达方式

| 人格 | 沟通风格 | 合规表达特征 | 示例 |
|------|---------|-------------|------|
| 🐿️ 松果 | 温暖 | 温和提醒风险 | "主人，投资有风险哦~ 要谨慎决策呢" |
| 🐢 慢慢 | 平静 | 淡定提示风险 | "市场有风险。请独立判断。" |
| 🦉 智多星 | 理性 | 数据化合规提示 | "风险提示：历史胜率 91.6%，但不代表未来" |
| 🐺 孤狼 | 果断 | 直接警示风险 | "风险自负！不要盲目跟单！" |
| 🐘 稳稳 | 平静 | 稳健合规提示 | "分散风险，谨慎决策" |

### 人格化合规话术生成

```python
class CompliantMessageGenerator(PetMessageGenerator):
    """合规的话术生成器"""
    
    def __init__(self, pet_config, compliance_checker):
        super().__init__(pet_config)
        self.compliance = compliance_checker
    
    def generate(self, trigger_type, data=None):
        """生成合规的话术"""
        # 1. 生成基础话术
        message = super().generate(trigger_type, data)
        
        # 2. 合规检查
        context = {
            "needs_disclaimer": self.needs_disclaimer(trigger_type),
            "data_source": data.get("source") if data else None
        }
        
        check_result = self.compliance.check_message(message, context)
        
        # 3. 如果不合规，修复
        if not check_result["is_compliant"]:
            message = self.fix_message(message, check_result["violations"])
        
        # 4. 添加人格化合规提示
        message = self.add_personality_disclaimer(message, trigger_type)
        
        return message
    
    def add_personality_disclaimer(self, message, trigger_type):
        """添加人格化合规提示"""
        # 根据触发类型决定是否需要风险提示
        if trigger_type not in ["market_down", "market_up", "sip_reminder"]:
            return message
        
        # 根据人格风格添加风险提示
        style = self.pet.get("communication_style", "friendly")
        
        disclaimer_templates = {
            "warm": "💡 投资有风险，要谨慎决策哦~",
            "calm": "市场有风险。请独立判断。",
            "rational": "风险提示：历史数据不代表未来表现。",
            "decisive": "风险自负！不要盲目跟风！",
            "witty": "投资有风险，别全听我的~ 机智如我",
            "friendly": "记得哦，投资有风险，要自己判断呀~",
            "visionary": "未来不确定，投资需谨慎。",
            "energetic": "冲之前先想好风险！"
        }
        
        disclaimer = disclaimer_templates.get(style, "市场有风险，投资需谨慎")
        
        # 根据主动性决定是否添加
        proactivity = self.pet.get("personality_traits", {}).get("proactivity_level", 50)
        
        if proactivity < 40:
            # 低主动性：不主动添加，用户问再说
            return message
        elif proactivity < 70:
            # 中等主动性：简短提示
            return f"{message}\n\n{disclaimer}"
        else:
            # 高主动性：详细提示
            return f"{message}\n\n⚠️ {disclaimer}\n历史业绩不代表未来表现，请独立判断。"
    
    def needs_disclaimer(self, trigger_type):
        """判断是否需要风险提示"""
        needs_disclaimer_types = [
            "market_down", "market_up", "sip_reminder",
            "valuation_alert", "achievement"
        ]
        
        return trigger_type in needs_disclaimer_types
    
    def fix_message(self, message, violations):
        """修复不合规消息"""
        for v in violations:
            if v["type"] == "specific_recommendation":
                message = message.replace(
                    "买这个基金",
                    "我可以教你筛选基金的方法，但不会推荐具体产品"
                )
            elif v["type"] == "return_promise":
                message = message.replace(
                    "肯定赚钱",
                    "历史业绩不代表未来表现"
                )
        
        return message
```

---

## 📊 数据层设计（Data Layer）

### 数据调用权限控制

```python
class DataAccessController:
    """数据访问控制器"""
    
    def __init__(self, pet_config):
        self.pet_id = pet_config.get("pet_id")
        self.allowed_apis = pet_config.get("data_access", {}).get("allowed_apis", [])
        self.forbidden_apis = pet_config.get("data_access", {}).get("forbidden_apis", [])
        self.cache_ttl = pet_config.get("data_access", {}).get("cache_ttl", 300)
    
    def can_access(self, api_name):
        """检查是否可以访问某个 API"""
        if api_name in self.forbidden_apis:
            return False, f"宠物{self.pet_id}无权访问{api_name}"
        
        if self.allowed_apis and api_name not in self.allowed_apis:
            return False, f"宠物{self.pet_id}未授权访问{api_name}"
        
        return True, "授权访问"
    
    def get_cache_key(self, api_name, params):
        """生成缓存键"""
        import hashlib
        param_str = json.dumps(params, sort_keys=True)
        key_str = f"{self.pet_id}:{api_name}:{param_str}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get_cache_ttl(self):
        """获取缓存有效期"""
        return self.cache_ttl
```

### 不同宠物的数据访问权限

```json
// 松果（谨慎定投型）- 保守数据访问
{
  "pet_id": "songguo",
  "data_access": {
    "allowed_apis": [
      "market_quote",           // 大盘指数
      "index_valuation",        // 指数估值
      "fund_basic_info"        // 基金基本信息
    ],
    "forbidden_apis": [
      "specific_fund_recommend", // 具体基金推荐
      "hot_money_flow",         // 热点资金流向
      "insider_trading"        // 内幕交易数据
    ],
    "cache_ttl": 300
  }
}

// 智多星（理性分析型）- 更多数据访问
{
  "pet_id": "maotouying",
  "data_access": {
    "allowed_apis": [
      "market_quote",
      "index_valuation",
      "fund_basic_info",
      "financial_report",       // 财报数据
      "industry_analysis",      // 行业分析
      "valuation_metrics"      // 估值指标
    ],
    "forbidden_apis": [
      "specific_fund_recommend",
      "insider_trading"
    ],
    "cache_ttl": 600
  }
}

// 孤狼（激进成长型）- 高风险数据限制
{
  "pet_id": "lang",
  "data_access": {
    "allowed_apis": [
      "market_quote",
      "industry_analysis",
      "growth_metrics"         // 成长指标
    ],
    "forbidden_apis": [
      "specific_fund_recommend",
      "hot_money_flow",
      "insider_trading",
      "leverage_data"         // 杠杆数据（防止鼓励加杠杆）
    ],
    "cache_ttl": 180
  }
}
```

---

## 🎯 完整 Body 示例

### 松果的完整 Body

```json
{
  "pet_id": "songguo",
  "session_id": "user_123_20260410",
  "compliance": {
    "risk_disclaimer": true,
    "investment_advice": false,
    "data_source": "eastmoney",
    "data_timestamp": "2026-04-10T15:30:00+08:00",
    "compliance_version": "v1.0",
    "appropriateness_check": true
  },
  "personality": {
    "communication_style": "warm",
    "proactivity_level": 40,
    "verbosity_level": 50,
    "intervention_level": 70,
    "emotional_bond": 60
  },
  "data_access": {
    "allowed_apis": ["market_quote", "index_valuation", "fund_basic_info"],
    "forbidden_apis": ["specific_fund_recommend", "hot_money_flow"],
    "cache_ttl": 300
  },
  "context": {
    "user_risk_tolerance": "conservative",
    "user_investment_goal": "long_term",
    "user_investment_experience": "beginner",
    "conversation_history": [
      {"role": "user", "content": "今天跌了好多，怎么办？"},
      {"role": "assistant", "content": "主人，别难过..."}
    ]
  },
  "constraints": [
    "never_recommend_specific_fund",
    "never_promise_return",
    "always_show_disclaimer",
    "never_store_user_data_cloud",
    "never_encourage_leverage",
    "never_use_fear_tactics"
  ],
  "fallback_responses": {
    "specific_fund_question": "我不推荐具体产品，但可以教你筛选方法...",
    "return_promise_question": "历史业绩不代表未来表现...",
    "market_timing_question": "没人能准确预测市场..."
  }
}
```

---

## ✅ 合规检查清单

### 发布前检查

- [ ] 所有输出包含风险提示
- [ ] 无具体产品推荐
- [ ] 无收益承诺
- [ ] 数据来源标注清晰
- [ ] 用户数据本地存储
- [ ] API 调用有权限控制
- [ ] 缓存有过期时间
- [ ] 适当性检查已实现

### 运行时检查

- [ ] 每条消息经过合规检查
- [ ] 违规消息自动修复
- [ ] 违规记录日志
- [ ] 严重违规上报人工审核

---

**创建时间**：2026-04-10  
**版本**：v1.0  
**合规版本**：符合中国证券投资基金业协会要求
