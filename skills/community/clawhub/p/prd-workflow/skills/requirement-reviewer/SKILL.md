---
name: requirement-reviewer
description: "PRD/requirement document reviewer with plugin architecture. Supports auto scenario detection (default/financial/internet). Core checkers for all scenarios, domain-specific plugins for specialized validation."
---

## 环境要求

- **Python**: >= 3.7（必需，类型注解支持）
- **python-docx**: >= 0.8.11（可选，Word文档格式检查）

## 安装

### 自动安装（推荐）

技能安装后会自动检测并安装依赖：

```bash
# ClawHub 安装
clawhub install requirement-reviewer

# 或手动安装
tar -xzf requirement-reviewer.tar.gz -C ~/.openclaw/skills/
cd ~/.openclaw/skills/requirement-reviewer
npm run postinstall  # 触发依赖安装
```

### 手动安装

如果自动安装失败，可手动安装依赖：

```bash
# 安装 Python 依赖
pip3 install --break-system-packages python-docx

# 或使用 requirements.txt
pip3 install -r requirements.txt
```

### 验证安装

```bash
# 方式1：使用环境检测工具
cd ~/.openclaw/skills/requirement-reviewer/engines
python3 check_environment.py

# 方式2：运行测试
python3 review_engine.py --check-env

# 方式3：测试评审引擎
python3 review_engine.py --test
```

## 依赖说明

| 依赖 | 版本 | 类型 | 用途 |
|------|------|------|------|
| Python | >= 3.7 | 必需 | 类型注解支持 |
| python-docx | >= 0.8.11 | 可选 | Word文档格式检查 |

**优雅降级**：python-docx 为可选依赖，未安装时：
- ✅ 核心评审功能正常使用
- ⚠️ Word 文档格式检查功能自动跳过
- 💡 系统会提示用户安装以获得完整功能

---

# Requirement Reviewer（需求评审专家）

**版本**: v3.1
**定位**: PRD/需求文档自动评审专家（插件式架构）
**能力**: 自动场景识别 + 场景模式 + 插件式评审器 + 迭代优化

---

## 🎯 核心能力

### 架构设计 v3.1

```
requirement-reviewer/
├── engines/
│   ├── review_engine.py          # 主评审引擎（支持场景模式 + 自动识别）
│   ├── plugin_manager.py         # 插件管理器
│   ├── core/                     # 核心评审器（通用）
│   │   ├── completeness_checker.py
│   │   ├── consistency_checker.py
│   │   ├── terminology_checker.py
│   │   └── acceptance_criteria_checker.py
│   └── plugins/
│       └── financial/            # 金融插件（领域专属）
│           ├── compliance_checker.py
│           ├── business_rule_checker.py
│           ├── edge_case_checker.py
│           └── risk_checker.py
```

### 场景模式

| 场景 | 适用场景 | 加载评审器 | 评审规则 |
|-----|---------|-----------|---------|
| **default** | 通用产品/互联网产品 | 4 个核心评审器 | 通用规则 |
| **financial** | 金融产品/理财产品 | 8 个评审器（4 核心 +4 金融） | 金融专属规则 |
| **internet** | 互联网产品/APP | 4 个核心评审器 | 通用规则（可扩展） |

### 🆕 自动场景识别（v3.1 新增）

**无需手动指定场景**，系统会根据 PRD 内容自动识别：

| 识别特征 | 匹配场景 | 关键词示例 |
|---------|---------|-----------|
| 金融关键词 ≥ 3 个 | financial | 基金、私募、信托、理财、认购、申购、赎回、净值、合格投资者、风险测评 |
| 互联网关键词 ≥ 3 个 | internet | APP、小程序、支付、订单、购物车、DAU、QPS、UI/UX |
| 其他 | default | 不满足以上条件 |

---

## 📦 核心评审器（所有场景通用）

| 评审器 | 检查内容 | 输出 |
|-------|---------|------|
| **completeness** | 章节完整性（P0/P1 章节） | 缺失章节清单 |
| **consistency** | 前后文一致性（风险/费率/数字） | 矛盾点清单 |
| **terminology** | 术语准确性 | 术语错误清单 |
| **acceptance_criteria** | 验收标准格式和内容 | 验收标准问题 |

---

## 🔌 领域插件（按需加载）

### financial 插件

| 评审器 | 检查内容 | 适用场景 |
|-------|---------|---------|
| **compliance** | 金融合规检查（15+ 检查点） | 基金/私募/信托/理财 |
| **business_rules** | 业务规则（风险匹配/适当性/冷静期） | 金融产品销售 |
| **edge_case** | 边界场景（交易/数据/系统异常） | 金融交易系统 |
| **risk** | 风险揭示（7 类风险） | 金融产品 PRD |

---

## 🔧 使用方式

### Python API

#### 方式 1：自动场景识别（推荐）⭐

```python
from review_engine import PRDReviewer

# 自动识别场景（推荐）
reviewer = PRDReviewer(scenario=None, auto_detect=True)
result = reviewer.review(prd_content)

print(f"识别场景：{result['scenario']}")
print(f"得分：{result['overall_score']}/100")
```

**适用场景**：
- 不确定 PRD 类型
- 需要评审多种类型的 PRD
- openclaw/skill 直接调用（无用户交互）

#### 方式 2：手动指定场景

```python
# 通用场景（互联网/电商/SaaS）
reviewer = PRDReviewer(scenario="default")
result = reviewer.review(prd_content)

# 金融场景（基金/私募/信托/理财）
reviewer = PRDReviewer(scenario="financial", product_type="fund", risk_level="R3")
result = reviewer.review(prd_content)

# 互联网场景（同 default）
reviewer = PRDReviewer(scenario="internet")
result = reviewer.review(prd_content)
```

**适用场景**：
- 明确知道 PRD 类型
- 需要覆盖自动识别结果
- 特定场景的专项评审

#### 方式 3：自定义评审器组合

```python
# 只检查完整性和一致性
reviewer = PRDReviewer(custom_checkers=["completeness", "consistency"])
result = reviewer.review(prd_content)
```

#### 迭代评审

```python
from review_engine import IterativeReviewer

# 迭代评审（支持自动场景识别）
iterative = IterativeReviewer(scenario=None, auto_detect=True, max_loops=3)
result = iterative.review_with_iteration(prd_content)

print(f"迭代轮数：{result['loop_count']}")
print(f"最终得分：{result['final_report']['overall_score']}")
```

### 命令行

```bash
cd requirement-reviewer/engines

# 运行测试（对比 default vs financial 场景）
python3 review_engine.py
```

---

## 📊 评审报告结构

### 报告模板

```markdown
# PRD 评审报告

## 📊 评审概览
- **文档名称**: XXX
- **评审时间**: YYYY-MM-DD
- **评审场景**: default / financial
- **加载评审器**: completeness, consistency, ...
- **总体评分**: XX/100

## ✅ 通过项
- [x] 检查项 1
- [x] 检查项 2

## ⚠️ 待改进项

### 1. 完整性问题
- [ ] 缺失章节：XXX
- [ ] 建议补充：XXX

### 2. 一致性问题
- [ ] 矛盾点：XXX
- [ ] 建议修正：XXX

### 3. 术语问题
- [ ] 错误术语：XXX
- [ ] 正确用法：XXX

### 4. 验收标准问题
- [ ] 格式问题：XXX
- [ ] 内容问题：XXX

## 📈 改进建议
1. 优先修复：XXX
2. 建议补充：XXX
3. 可选优化：XXX

## 🎯 评审结论
□ 通过，可提交
□ 需改进，改进后复审
□ 不通过，需重大修改
```

---

## 🆕 版本历史

### v3.0 (2026-03-11) - 插件式架构

**核心变更**:
- 重构为插件式架构，支持场景模式
- 核心评审器与领域插件分离
- 解决金融规则对非金融场景评分过严的问题

**新增**:
- `plugin_manager.py` - 插件加载管理
- `core/` - 核心评审器目录
- `plugins/financial/` - 金融领域插件
- `scenario` 参数支持（default/financial/internet）

**使用示例**:
```python
# 通用场景（不受金融规则影响）
reviewer = PRDReviewer(scenario="default")

# 金融场景（启用金融专属规则）
reviewer = PRDReviewer(scenario="financial")
```

### v2.0 (2026-03-10) - 9 合 1 评审引擎

**新增检查引擎**:
- `business_rule_checker` - 业务规则检查
- `edge_case_checker` - 边界案例检查
- `acceptance_criteria_checker` - 验收标准检查
- `iterative_reviewer` - 迭代评审控制器

**评审流程**:
```
PRD → 9 项检查 → 生成报告 → 迭代优化 (2-3 轮) → 交付
```

### v1.0 - 基础评审引擎

**核心检查器**:
- `completeness_checker` - 完整性检查
- `consistency_checker` - 一致性检查
- `compliance_checker` - 合规检查
- `terminology_checker` - 术语检查
- `risk_checker` - 风险检查

---

## 📝 场景选择指南

| 产品类型 | 推荐场景 | 说明 |
|---------|---------|------|
| 互联网 APP | default | 无需金融专属规则 |
| 电商平台 | default | 通用业务规则 |
| 基金/私募 | financial | 需要合规检查 |
| 银行理财 | financial | 需要金融监管规则 |
| 信托产品 | financial | 需要合格投资者/冷静期检查 |
| 物联网/硬件 | default | 通用业务规则 |
| SaaS 平台 | default | 通用业务规则 |

---

## ⚠️ 注意事项

### 评分差异说明

同一份 PRD 在不同场景下得分可能不同：

| 场景 | 得分示例 | 说明 |
|-----|---------|------|
| default | 75/100 | 只检查通用规则 |
| financial | 55/100 | 额外检查金融合规规则 |

**这不是 Bug**，而是因为：
1. financial 场景加载了更多评审器
2. 金融专属规则（合规/业务规则/风险揭示）更严格
3. 非金融产品不需要满足金融监管要求

### 正确选择场景

- 如果 PRD 是**通用产品** → 使用 `scenario="default"`
- 如果 PRD 是**金融产品** → 使用 `scenario="financial"`
- 如果不确定 → 先用 `default`，再根据建议选择

---

## 🆕 v4.0 内容检查层（新增）

### 分层架构

```
评审流程：
  ├─ 形式检查层（规则匹配，秒级，无成本）
  │     ↓ 发现问题
  │   自动修补 → 重新检查 → 通过
  │
  └─ 内容检查层（AI理解，分钟级，有成本）
        ↓ 发现问题
      问答引导用户修补
        ↓
      生成评审报告
```

### 13项内容检查

#### 核心建议（必须处理）
| ID | 检查项 | 对应章节 |
|----|-------|---------|
| C001 | 流程描述 | 业务流程 |
| C002 | 异常处理 | 功能需求 |

#### 完善建议（建议处理）
| ID | 检查项 | 对应章节 |
|----|-------|---------|
| C003 | 改造内容标注 | 全文 |
| C004 | 元素完整性 | 功能需求 |
| C005 | 交互逻辑 | 功能需求 |
| C006 | 算法公式 | 功能需求 |
| C007 | 查询关联 | 数据需求 |
| C008 | GWT验收标准 | 验收标准 |
| C009 | 系统对接描述 | 系统对接 |

#### 优化建议（可选处理）
| ID | 检查项 | 对应章节 |
|----|-------|---------|
| C010 | 分项描述 | 全文 |
| C011 | 界面细节 | 界面设计 |
| C012 | 改造类型 | 全文 |
| C013 | 原型附件 | 界面设计/附录 |

### 内容检查交互流程

**OpenClaw AI 执行内容检查后，按优先级逐个引导用户修补：**

```
┌─────────────────────────────────────┐
│ 【核心问题】第 1/2 项                        │
├─────────────────────────────────────┤
│ 问题：流程描述不完整                         │
│ 章节：业务流程                               │
│ 说明：缺少异常分支说明（超时处理、失败重试）      │
├─────────────────────────────────────┤
│ 请选择：                                     │
│   1. AI 自动修补                             │
│   2. 告诉 AI 怎么修补                        │
│   3. 误判，可忽略                            │
└─────────────────────────────────────┘
```

**三种选项的处理**：

| 选项 | 用户操作 | 系统行为 |
|------|---------|---------|
| 1. AI 自动修补 | 无需输入 | AI 生成修补内容，自动更新 PRD |
| 2. 告诉 AI 怎么修补 | 输入修补描述 | AI 按用户描述生成内容，更新 PRD |
| 3. 误判，可忽略 | 无需输入 | 标记忽略，记入报告，不修补 |

### 命令行调用

```bash
# 执行内容检查
python3 content_check_cli.py --prd /path/to/prd.md --format json

# 指定 API
python3 content_check_cli.py --prd /path/to/prd.md --api-key $OPENAI_API_KEY
```

### Python API

```python
from semantic import AIContentChecker, SectionMatcher

# 解析章节
matcher = SectionMatcher()
tasks = matcher.get_all_tasks(prd_content)

# 执行检查
checker = AIContentChecker()
issues = checker.check_all(tasks)

# 按优先级分组
from semantic.check_items import Priority
core_issues = [i for i in issues if i.priority == Priority.CORE]
```

---

*Requirement Reviewer v4.0 - 形式检查 + 内容检查，让 PRD 质量更上一层*
