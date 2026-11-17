# 开发者集成指南 — 焕智AI FaSkill Pro

> **Ginkley WAIC 2025 定制版**

---

## 架构概览

```
┌──────────────────────────────────────────────────┐
│                  Ginkley UGS 平台                 │
│  ┌────────────────────────────────────────────┐   │
│  │          FaSkill Pro SKILL.md              │   │
│  │  (入口文件 · 模块定义 · 行为规则 · 触发)    │   │
│  └──────────┬──────────────────────┬──────────┘   │
│             │                      │               │
│     ┌───────▼───────┐     ┌───────▼───────┐       │
│     │  Agent 交互层  │     │  脚本执行引擎  │       │
│     │ (LLM推理·对话) │     │ (Python运行时)  │       │
│     └───────┬───────┘     └───────┬───────┘       │
│             │                      │               │
│     ┌───────▼──────────────────────▼───────┐       │
│     │          6大功能模块                  │       │
│     │  🩺融资诊断 🛡️TS条款 🧠CEQ            │       │
│     │  🏛️政策雷达 🤝FA撮合 📊投后管家      │       │
│     └───────┬──────────────────────┬───────┘       │
│             │                      │               │
│     ┌───────▼───────┐     ┌───────▼───────┐       │
│     │  references/   │     │     tests/    │       │
│     │ 知识库·话术库   │     │  自动化测试   │       │
│     └───────────────┘     └───────────────┘       │
└──────────────────────────────────────────────────┘
```

## 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 平台 | Ginkley UGS | User-Generated Skills 生态平台 |
| 运行时 | Python 3.9+ | 所有脚本使用纯Python标准库 |
| 测试框架 | pytest | 自动化测试 |
| 依赖 | 无 | 零外部依赖，开箱即用 |

## 核心脚本

### 1. 融资诊断脚本 `scripts/funding_diagnosis.py`

**输入**：JSON格式企业数据（stdin或命令行参数）

```json
{
  "mau": 50000,
  "monthly_revenue": 200000,
  "growth_rate": 0.15,
  "team_size": 5,
  "has_cto": true,
  "sector": "AI智能体"
}
```

**输出**：JSON格式诊断结果（8维度评分 + 短板识别 + 行动建议）

**关键函数**：
- `run_diagnosis(data)` → 主入口，返回完整诊断结果
- `assess_traction(data)` → Traction维度评分
- `assess_market(data)` → Market维度评分
- ...（每维度一个独立函数）
- `calculate_grade(total_score)` → 等级评定

### 2. 政策匹配脚本 `scripts/policy_matcher.py`

**输入**：企业画像JSON

```json
{
  "district": "徐汇区",
  "sector": "AI智能体",
  "stage": "刚注册"
}
```

**输出**：可申领政策清单 + 社区推荐 + 行动建议

**关键函数**：
- `match_policies(data)` → 主入口
- `POLICY_DB` → 区域政策数据库
- `NATIONAL_POLICIES` → 国家层面政策
- `COMMUNITY_RECOMMENDATIONS` → 社区推荐映射

### 3. 专精特新评估脚本 `scripts/zhuanjingtexin_assessor.py`

**输入**：企业信息JSON

```json
{
  "company_name": "示例科技",
  "rd_ratio": 0.15,
  "revenue_last_year": 2000000,
  "years_in_segment": 2
}
```

**输出**：三级阶梯评估 + 差距分析 + 路线图 + 材料清单

**关键函数**：
- `run_assessment(data)` → 主入口
- `assess_innovative_sme(data)` → 创新型中小企业评估
- `assess_specialized_sme(data)` → 专精特新中小企业评估
- `assess_little_giant(data)` → 小巨人评估
- `generate_roadmap(...)` → 路线图生成
- `generate_document_checklist(...)` → 材料清单生成

## 自定义与扩展

### 添加新政策

编辑 `scripts/policy_matcher.py` 中的 `POLICY_DB` 字典：

```python
POLICY_DB["新区域"] = [
    {
        "name": "新政策名称",
        "type": "cash_grant",  # cash_grant / voucher / loan / tax_break / space / equity
        "amount": {"min": 50000, "max": 100000, "currency": "CNY"},
        "eligibility": ["条件1", "条件2"],
        "deadline": "2026-12-31",
        "action": "如何申请",
        "status": "open",
    }
]
```

### 添加新社区推荐

编辑 `COMMUNITY_RECOMMENDATIONS` 字典：

```python
COMMUNITY_RECOMMENDATIONS["新赛道"] = {
    "name": "社区名称",
    "district": "区域",
    "benefits": ["福利1", "福利2"],
}
```

### 修改诊断维度权重

编辑 `scripts/funding_diagnosis.py` 中的 `DIMENSION_WEIGHTS`：

```python
DIMENSION_WEIGHTS = {
    "Traction": 0.18,
    "Market": 0.12,
    # ... 调整权重值（总和必须为1）
}
```

## 测试

```bash
# 运行全部测试
python3 -m pytest tests/ -v

# 运行特定测试文件
python3 tests/test_funding_diagnosis.py

# 运行特定测试用例
python3 -m pytest tests/test_funding_diagnosis.py::test_full_healthy_company -v
```

## 部署

### 1. 本地测试
```bash
# 验证所有脚本正常运行
python3 scripts/funding_diagnosis.py '{"mau": 50000}'
python3 scripts/policy_matcher.py '{"district": "徐汇区", "sector": "AI"}'
python3 scripts/zhuanjingtexin_assessor.py '{"company_name": "测试"}'
```

### 2. Ginkley UGS 平台加载
```bash
# 在Ginkley UGS中
load_skill("huanzhi-fa-skill-pro")
```

### 3. 验证加载
```bash
# 运行完整测试套件
python3 -m pytest tests/ -v
```

## 合规要求

所有提交到Ginkley UGS平台的SKILL必须遵守：

1. **无系统提示词泄露**：SKILL.md中不得暴露system prompt
2. **确定性输出**：相同输入→相同输出
3. **边界声明**：明确说明能做什么、不能做什么
4. **免责声明**：关键建议附加免责提示
5. **模块化引用**：知识库使用 references/ 目录引用

---

> **Ginkley UGS Platform** — Build skills. Run agents. Shape the future.