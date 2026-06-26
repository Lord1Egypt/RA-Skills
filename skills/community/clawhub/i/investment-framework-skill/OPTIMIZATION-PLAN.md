# investment-framework-skill 优化计划

**检查时间**：2026-03-19 14:45  
**检查标准**：SKILL-STANDARD-v2.md  
**优化目标**：深度优化 33 个技能（现有 27 个 + 待补充 6 个），统一格式、补充坑点章节、优化示例  
**完成时间**：今天内  
**禁忌**：不改变核心功能逻辑，保持向后兼容

**注**：现有 27 个 SKILL.md，根据 FINAL_SUMMARY.md 设计应有 33 个（13 核心 +12 中国大师 +6 进阶 +1 主技能 +1 future-forecaster）

---

## 📊 技能清单（27 个）

### 主技能（1 个）

| # | 技能 | 版本 | 状态 | 优先级 |
|---|------|------|------|--------|
| 1 | SKILL.md（主技能） | - | ❌ 需重构 | P0 |

### 核心技能（16 个）

| # | 技能 | 版本 | Front Matter | 坑点章节 | 示例 | 优先级 |
|---|------|------|-------------|---------|------|--------|
| 2 | asset-allocator | v2.0.0 | ✅ | ❌ | ⚠️ | P1 |
| 3 | bias-detector | - | ❌ | ❌ | ⚠️ | P1 |
| 4 | cycle-locator | - | ❌ | ❌ | ⚠️ | P1 |
| 5 | decision-checklist | - | ❌ | ❌ | ⚠️ | P1 |
| 6 | future-forecaster | - | ❌ | ❌ | ⚠️ | P1 |
| 7 | global-allocator | - | ❌ | ❌ | ⚠️ | P1 |
| 8 | industry-analyst | - | ❌ | ❌ | ⚠️ | P1 |
| 9 | intrinsic-value-calculator | - | ❌ | ❌ | ⚠️ | P1 |
| 10 | moat-evaluator | - | ❌ | ❌ | ⚠️ | P1 |
| 11 | portfolio-designer | - | ❌ | ❌ | ⚠️ | P1 |
| 12 | second-level-thinker | - | ❌ | ❌ | ⚠️ | P1 |
| 13 | simple-investor | - | ❌ | ❌ | ⚠️ | P1 |
| 14 | stock-picker | - | ❌ | ❌ | ⚠️ | P1 |
| 15 | value-analyzer | - | ❌ | ❌ | ⚠️ | P1 |

### 中国大师系列（10 个）

| # | 技能 | 版本 | Front Matter | 坑点章节 | 示例 | 优先级 |
|---|------|------|-------------|---------|------|--------|
| 16 | china-masters/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 17 | china-masters/duan-yongping/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 18 | china-masters/duan-yongping/culture-analyzer/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 19 | china-masters/duan-yongping/longterm-checker/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 20 | china-masters/li-lu/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 21 | china-masters/li-lu/civilization-analyzer/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 22 | china-masters/li-lu/china-opportunity/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 23 | china-masters/qiu-guolu/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 24 | china-masters/qiu-guolu/valuation-analyzer/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 25 | china-masters/qiu-guolu/quality-analyzer/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 26 | china-masters/wu-jun/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 27 | china-masters/wu-jun/ai-trend-analyzer/SKILL.md | - | ❌ | ❌ | ❌ | P2 |
| 28 | china-masters/wu-jun/data-driven-investor/SKILL.md | - | ❌ | ❌ | ❌ | P2 |

**注**：实际 27 个 SKILL.md（主技能 1+ 核心 14+ 中国大师 12=27）

---

## 🔍 v2.0 标准检查清单

### 必需项（所有技能）

| 检查项 | 标准 | 当前状态 |
|--------|------|---------|
| **Front Matter** | name/version/author/created/updated/skill_type/related_skills/tags | ⚠️ 部分有 |
| **description** | 触发说明式（"［何时使用］当用户...时"） | ⚠️ 部分有 |
| **skill_type** | 核心🔴/通用🟡/内部🟢 | ❌ 缺失 |
| **related_skills** | 说明技能组合关系 | ⚠️ 部分有 |
| **📋 功能描述** | 适用场景/边界条件 | ⚠️ 部分有 |
| **⚠️ 常见错误** | 5-7 个坑点，从失败案例提炼 | ❌ 大部分缺失 |
| **🔗 相关资源** | references/examples/templates 渐进式披露 | ✅ 目录存在，内容待检查 |
| **📊 输入参数** | JSON Schema 标准化 | ❌ 大部分缺失 |
| **📤 输出格式** | JSON Schema 标准化 | ❌ 大部分缺失 |
| **🧪 使用示例** | 2-5 个完整示例（输入 + 输出） | ⚠️ 部分有 |
| **📚 核心理念** | 健康公式 | ⚠️ 部分有 |
| **🔗 相关文件** | 文件路径说明 | ❌ 大部分缺失 |
| **更新日志** | 版本历史 | ⚠️ 部分有 |

---

## 📁 目录结构检查

### 现有结构
```
investment-framework-skill/
├── SKILL.md（主技能）
├── asset-allocator/
│   ├── SKILL.md
│   ├── examples/
│   ├── references/
│   └── templates/
├── bias-detector/
│   └── ...
...
└── china-masters/
    ├── duan-yongping/
    ├── li-lu/
    ├── qiu-guolu/
    └── wu-jun/
```

### 需要补充的内容

| 目录 | 当前状态 | 需要补充 |
|------|---------|---------|
| `examples/` | ✅ 目录存在 | 内容待检查/补充 |
| `references/` | ✅ 目录存在 | 内容待检查/补充 |
| `templates/` | ✅ 目录存在 | 内容待检查/补充 |
| `scripts/` | ❌ 缺失 | 计算脚本/工具代码 |
| `calculators/` | ❌ 缺失 | 计算公式/在线工具 |

---

## 🚀 优化计划

### 阶段 1：主技能重构（P0）
**文件**：`SKILL.md`  
**时间**：1-2 小时  
**内容**：
- 添加完整 Front Matter
- description 改为触发说明式
- skill_type 标注
- related_skills 说明（26 个子技能关系）
- 添加技能关系图
- 添加组合使用流程
- 添加常见错误（7-10 个）
- 标准化输入输出格式

### 阶段 2：核心技能重构（P1，14 个）
**文件**：asset-allocator, bias-detector, cycle-locator, decision-checklist, future-forecaster, global-allocator, industry-analyst, intrinsic-value-calculator, moat-evaluator, portfolio-designer, second-level-thinker, simple-investor, stock-picker, value-analyzer

**时间**：14 个 × 1 小时 = 14 小时  
**每个技能内容**：
- 完善 Front Matter
- description 改为触发说明式
- skill_type 标注
- related_skills 说明
- 添加 5-7 个常见错误（从失败案例提炼）
- 标准化输入输出格式（JSON Schema）
- 优化示例（2-5 个完整示例）
- 添加健康公式
- 补充相关文件路径

### 阶段 3：中国大师系列重构（P2，12 个）
**文件**：china-masters 下 12 个技能

**时间**：12 个 × 0.5 小时 = 6 小时  
**每个技能内容**：
- 添加 Front Matter
- description 改为触发说明式
- skill_type 标注（通用🟡）
- related_skills 说明
- 添加 3-5 个常见错误
- 添加 1-2 个示例
- 添加健康公式

### 阶段 4：资源文件补充（P3）
**内容**：
- 检查每个技能的 examples/ 内容
- 检查每个技能的 references/ 内容
- 检查每个技能的 templates/ 内容
- 创建 scripts/ 目录（计算脚本）
- 创建 calculators/ 目录（计算公式）

**时间**：4-6 小时

### 阶段 5：整合测试（P4）
**内容**：
- 检查所有技能格式一致性
- 测试组合使用流程
- Git 提交
- 推送到 GitHub

**时间**：1-2 小时

---

## ⏰ 时间估算

| 阶段 | 内容 | 时间 |
|------|------|------|
| 阶段 1 | 主技能重构 | 1-2h |
| 阶段 2 | 14 个核心技能 | 14h |
| 阶段 3 | 12 个中国大师技能 | 6h |
| 阶段 4 | 资源文件补充 | 4-6h |
| 阶段 5 | 整合测试 | 1-2h |
| **总计** | | **26-30h** |

**今天完成可行性**：⚠️ 紧张但可行（需高效执行）

---

## 📋 执行策略

### 批量处理
1. **Front Matter 批量添加**：用脚本批量处理
2. **坑点章节模板**：创建通用模板，逐个定制
3. **示例批量优化**：统一格式，补充输入输出

### 优先级调整
- **今天必须完成**：P0 + P1（主技能 +14 个核心技能）
- **明天完成**：P2 + P3 + P4（中国大师系列 + 资源文件）

### 质量保证
- 每个技能提交前检查 v2.0 清单
- 保持向后兼容（不改变核心功能）
- 示例必须可运行/可验证

---

## 🎯 下一步行动

**请确认**：
1. 技能数量是否正确（27 个）？
2. 优先级划分是否合理？
3. 是否按此计划执行？
4. 今天是否必须完成全部（还是可分 2 天）？

**确认后我将**：
1. 从 P0 主技能开始重构
2. 每完成一个技能提交一次
3. 实时汇报进度

---

*检查完成时间：2026-03-19 14:40*
