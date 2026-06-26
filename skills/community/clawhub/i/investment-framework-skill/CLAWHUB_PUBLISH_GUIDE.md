# ClawHub 发布指南

## 📋 前提条件

1. **ClawHub 账号** - 已有账号（lj22503）
2. **ClawHub CLI** - 已安装
3. **登录状态** - 需要先登录

---

## 🔐 第一步：登录 ClawHub

```bash
clawhub login
```

按提示输入：
- 邮箱/用户名
- 密码/API Token

---

## 📦 第二步：发布技能包

### 方式 1：发布完整技能包

```bash
cd /tmp/investment-framework-skill
clawhub publish . \
  --slug "investment-framework" \
  --name "投资框架技能包" \
  --version "3.0.0" \
  --changelog "v3.0.0 - 35 个技能全部按 v2.0 标准重构" \
  --tags "latest,投资，价值投资，资产配置"
```

### 方式 2：发布单个技能

```bash
# 发布价值分析师
clawhub publish ./value-analyzer \
  --slug "value-analyzer" \
  --name "价值分析师" \
  --version "2.0.0" \
  --changelog "按 v2.0 标准重构" \
  --tags "latest,价值投资，格雷厄姆"

# 发布护城河评估师
clawhub publish ./moat-evaluator \
  --slug "moat-evaluator" \
  --name "护城河评估师" \
  --version "2.0.0" \
  --changelog "按 v2.0 标准重构" \
  --tags "latest,护城河，巴菲特"
```

---

## 📝 第三步：验证发布

访问 ClawHub 主页验证：
- https://clawhub.ai/lj22503/investment-framework

---

## 🚀 发布清单

### 核心技能（14 个）

```bash
# 1. 价值分析师
clawhub publish ./value-analyzer --slug "value-analyzer" --name "价值分析师" --version "2.0.0"

# 2. 护城河评估师
clawhub publish ./moat-evaluator --slug "moat-evaluator" --name "护城河评估师" --version "2.0.0"

# 3. 内在价值计算器
clawhub publish ./intrinsic-value-calculator --slug "intrinsic-value-calculator" --name "内在价值计算器" --version "2.0.0"

# 4. 决策清单
clawhub publish ./decision-checklist --slug "decision-checklist" --name "决策清单" --version "2.0.0"

# 5. 资产配置师
clawhub publish ./asset-allocator --slug "asset-allocator" --name "资产配置师" --version "2.0.0"

# 6. 行业分析师
clawhub publish ./industry-analyst --slug "industry-analyst" --name "行业分析师" --version "2.0.0"

# 7. 未来预测师
clawhub publish ./future-forecaster --slug "future-forecaster" --name "未来预测师" --version "2.0.0"

# 8. 周期定位师
clawhub publish ./cycle-locator --slug "cycle-locator" --name "周期定位师" --version "2.0.0"

# 9. 选股专家
clawhub publish ./stock-picker --slug "stock-picker" --name "选股专家" --version "2.0.0"

# 10. 组合设计师
clawhub publish ./portfolio-designer --slug "portfolio-designer" --name "组合设计师" --version "2.0.0"

# 11. 全球配置师
clawhub publish ./global-allocator --slug "global-allocator" --name "全球配置师" --version "2.0.0"

# 12. 简单投资者
clawhub publish ./simple-investor --slug "simple-investor" --name "简单投资者" --version "2.0.0"

# 13. 认知偏差检测器
clawhub publish ./bias-detector --slug "bias-detector" --name "认知偏差检测器" --version "2.0.0"

# 14. 第二层思维者
clawhub publish ./second-level-thinker --slug "second-level-thinker" --name "第二层思维者" --version "2.0.0"
```

### 中国大师系列（4 个）

```bash
# 15. 邱国鹭投资智慧
clawhub publish ./china-masters/qiu-guolu --slug "qiu-guolu-investor" --name "邱国鹭投资智慧" --version "2.0.0"

# 16. 段永平投资智慧
clawhub publish ./china-masters/duan-yongping --slug "duan-yongping-investor" --name "段永平投资智慧" --version "2.0.0"

# 17. 李录投资智慧
clawhub publish ./china-masters/li-lu --slug "li-lu-investor" --name "李录投资智慧" --version "2.0.0"

# 18. 吴军投资智慧
clawhub publish ./china-masters/wu-jun --slug "wu-jun-investor" --name "吴军投资智慧" --version "2.0.0"
```

---

## 📊 发布统计

| 类别 | 技能数 | 状态 |
|------|--------|------|
| 核心技能 | 14 | ⏳ 待发布 |
| 中国大师 | 4 | ⏳ 待发布 |
| 子技能 | 8 | ⏳ 待发布 |
| **总计** | **26** | ⏳ **待发布** |

---

## ⚠️ 注意事项

1. **登录状态** - 确保已登录 ClawHub
2. **版本号** - 遵循语义化版本（semver）
3. **changelog** - 简要描述变更内容
4. **tags** - 使用逗号分隔的标签
5. **slug** - 唯一标识符，不能重复

---

## 🔗 相关链接

- **ClawHub 主页：** https://clawhub.ai/lj22503
- **龙虾翻译官示例：** https://clawhub.ai/lj22503/lobster-translator
- **GitHub 仓库：** https://github.com/lj22503/investment-framework-skill

---

## 📞 遇到问题？

1. **登录问题：** `clawhub login --help`
2. **发布问题：** `clawhub publish --help`
3. **GitHub Issues：** https://github.com/lj22503/investment-framework-skill/issues

---

*投资很简单，但不容易。简单的是原则，不容易的是执行。* 📚
