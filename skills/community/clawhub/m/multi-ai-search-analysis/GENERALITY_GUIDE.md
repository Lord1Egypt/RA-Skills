# 🌐 通用性说明 - Multi-AI Search Analysis

**版本**：v1.2（通用版）  
**更新日期**：2026-03-16

---

## ✅ 通用化改进

### v1.1 → v1.2 核心变化

| 方面 | v1.1（特定） | v1.2（通用） |
|------|-------------|-------------|
| **默认维度** | 政治、经济、军事、外交 | 无（由用户指定） |
| **问题模板** | 硬编码"局势对油价影响" | 支持自定义模板 |
| **报告模板** | 固定 7 章结构 | 4 种场景模板可选 |
| **适用场景** | 地缘政治分析 | 任意复杂问题分析 |

---

## 📊 支持的场景类型

### 1. 时事分析（原场景）

```bash
python scripts/run.py \
  -t "伊朗局势分析" \
  -d 政治 经济 军事 外交 \
  --follow-up "对油价有什么影响？" "对中国有何影响？"
```

**推荐模板**：`general`（默认）

---

### 2. 技术对比

```bash
python scripts/run.py \
  -t "Python vs Java 性能对比" \
  -d 性能 易用性 生态系统 学习曲线 就业市场 \
  --question-template "请详细对比{topic}，从{dimensions}角度分析，给出具体数据支持"
```

**推荐模板**：`comparison`

---

### 3. 产品评测

```bash
python scripts/run.py \
  -t "iPhone 16 Pro 深度评测" \
  -d 性能 拍照 续航 价格 创新点 \
  --follow-up "值得购买吗？" "适合什么人群？"
```

**推荐模板**：`evaluation`

---

### 4. 市场研究

```bash
python scripts/run.py \
  -t "2026 年 AI 市场趋势分析" \
  -d 技术发展 投资趋势 应用场景 竞争格局 政策环境 \
  --question-template "请分析{topic}，重点关注{dimensions}"
```

**推荐模板**：`trend`

---

### 5. 学术研究

```bash
python scripts/run.py \
  -t "量子计算发展现状" \
  -d 理论基础 技术突破 应用前景 挑战 \
  --follow-up "有哪些关键论文？" "主要研究机构有哪些？"
```

**推荐模板**：`general`

---

### 6. 商业决策

```bash
python scripts/run.py \
  -t "是否应该投资新能源汽车行业" \
  -d 市场空间 竞争态势 政策风险 技术路线 财务回报 \
  --follow-up "最佳入场时机？" "推荐标的？"
```

**推荐模板**：`evaluation`

---

### 7. 学习规划

```bash
python scripts/run.py \
  -t "如何系统学习机器学习" \
  -d 数学基础 编程技能 理论框架 实战项目 资源推荐 \
  --follow-up "学习路径？" "预计耗时？"
```

**推荐模板**：`general`

---

## 🎨 自定义问题模板

### 模板语法

支持占位符：
- `{topic}` - 分析主题
- `{dimensions}` - 维度列表（自动用"、"连接）

### 内置模板

配置文件 `config/ai-platforms.json` 中预定义：

```json
{
  "templates": {
    "general": "请帮我分析一下{topic}，包括{dimensions}等方面的情况。",
    "comparison": "请详细对比{topic}，从{dimensions}等角度进行全面分析。",
    "trend": "请分析{topic}的发展趋势，包括{dimensions}等关键因素。",
    "evaluation": "请评估{topic}，从{dimensions}维度给出详细评价和建议。"
  }
}
```

### 使用方式

```bash
# 使用内置模板
python run.py -t "主题" --question-template "comparison"

# 自定义模板
python run.py -t "主题" \
  --question-template "请从专业角度分析{topic}，重点讨论{dimensions}，要求数据准确、逻辑清晰"
```

---

## 📋 自定义报告模板

### 内置模板类型

| 模板 | 适用场景 | 章节结构 |
|------|----------|----------|
| `general` | 通用分析 | 执行摘要 → 核心观点 → 分维度分析 → 数据对比 → 特色 → 来源 |
| `comparison` | 对比分析 | 对比总结 → 各选项详情 → 维度对比表 → 优劣势 → 推荐 → 评价 |
| `trend` | 趋势分析 | 核心趋势 → 现状 → 驱动因素 → 预测 → 风险机遇 → 数据 |
| `evaluation` | 评测报告 | 评测结论 → 评测维度 → 详细评分 → 优缺点 → 建议 → 观点 |

### 使用方式

```bash
# 指定模板
python run.py -t "产品对比" --report-template "comparison"

# 或在代码中调用
from reporter import generate_report

generate_report(
    topic="iPhone 16 Pro 评测",
    results=results,
    template_name="evaluation"
)
```

---

## 🔧 配置示例

### 完整命令行示例

```bash
# 场景 1：技术选型对比
python scripts/run.py \
  -t "MySQL vs PostgreSQL 选型分析" \
  -p DeepSeek Qwen Kimi \
  -d 性能 功能 易用性 生态 成本 \
  --question-template "请对比{topic}，从{dimensions}角度分析，给出具体场景建议" \
  --follow-up "各自适合什么场景？" "迁移成本如何？" \
  --report-template "comparison" \
  --timeout 150 \
  -o "reports/mysql-vs-pg.md"

# 场景 2：市场趋势分析
python scripts/run.py \
  -t "2026 年跨境电商趋势" \
  -d 市场规模 政策环境 竞争格局 技术创新 消费者行为 \
  --question-template "请分析{topic}，重点关注{dimensions}" \
  --report-template "trend" \
  --mode parallel

# 场景 3：产品评测
python scripts/run.py \
  -t "大疆 Mini 4 Pro 无人机评测" \
  -d 画质 续航 操控 便携性 价格 \
  --follow-up "适合新手吗？" "性价比如何？" \
  --report-template "evaluation"
```

---

## 📊 通用报告结构

### 最小化报告（所有场景通用）

```markdown
# {主题} - 综合分析报告

**生成时间**：{时间}  
**AI 平台**：{平台列表}  
**分析维度**：{维度列表}

---

## 核心结论

[200 字摘要]

## 各 AI 回复原文

### DeepSeek
[完整回复]

### Qwen
[完整回复]

...

## 数据对比表

| 维度 | DeepSeek | Qwen | ... | 共识 |
|------|----------|------|-----|------|
| - | - | - | ... | - |

## 各家特色

- **DeepSeek**: [特色]
- **Qwen**: [特色]
...
```

---

## 🎯 最佳实践

### 1. 选择合适的维度

**好维度**（具体、可衡量）：
- ✅ 性能、价格、续航、生态
- ✅ 技术、市场、投资、政策
- ✅ 优点、缺点、风险、机遇

**避免的维度**（过于宽泛）：
- ❌ 各方面、所有因素、全部

### 2. 设计清晰的问题模板

**好模板**：
```
请分析{topic}，从{dimensions}角度进行详细评估，要求：
1. 提供具体数据支持
2. 给出明确结论
3. 说明适用场景
```

**避免的模板**：
```
请说一下{topic}（过于模糊）
```

### 3. 使用延伸问题

延伸问题能引导 AI 提供更深入的分析：

```bash
--follow-up "有什么风险？" \
            "未来趋势如何？" \
            "对普通人有何影响？" \
            "有哪些具体案例？"
```

### 4. 选择匹配的报告模板

| 场景 | 推荐模板 |
|------|----------|
| 时事/局势分析 | `general` |
| 产品/技术对比 | `comparison` |
| 趋势/预测分析 | `trend` |
| 评测/评估 | `evaluation` |

---

## 🚀 快速上手

### 第一步：确定场景类型

问自己：
- 我是要**对比**多个选项？→ `comparison`
- 我是要**预测**趋势？→ `trend`
- 我是要**评估**某个事物？→ `evaluation`
- 我是要**全面了解**某个主题？→ `general`

### 第二步：设计维度

列出 3-6 个关键维度，例如：
- 技术对比：性能、易用性、生态、成本
- 产品评测：功能、质量、价格、服务

### 第三步：运行命令

```bash
python scripts/run.py \
  -t "你的主题" \
  -d 维度 1 维度 2 维度 3 \
  --report-template "模板类型"
```

### 第四步：查看报告

```bash
# 打开最新报告
python scripts/open-report.py latest
```

---

## 📚 完整示例

### 示例 1：选择编程语言

```bash
python scripts/run.py \
  -t "2026 年 Java vs Python vs Go 选型建议" \
  -d 性能 开发效率 生态系统 学习曲线 就业前景 薪资水平 \
  --question-template "请对比{topic}，从{dimensions}角度分析，给出不同场景的选型建议" \
  --follow-up "各自最适合什么场景？" "未来 5 年趋势如何？" \
  --report-template "comparison" \
  --timeout 150
```

### 示例 2：购房决策

```bash
python scripts/run.py \
  -t "2026 年北京购房时机分析" \
  -d 房价趋势 政策环境 利率水平 供需关系 经济形势 \
  --follow-up "现在是好时机吗？" "推荐哪些区域？" "风险有哪些？" \
  --report-template "evaluation"
```

### 示例 3：学习计划

```bash
python scripts/run.py \
  -t "如何 6 个月内系统学习数据科学" \
  -d 数学基础 编程技能 机器学习 深度学习 实战项目 资源推荐 \
  --follow-up "每天需要多少时间？" "推荐哪些课程？" "如何检验学习效果？" \
  --report-template "general"
```

---

## ✅ 通用性检查清单

设计问题时自检：

- [ ] 主题是否清晰具体？
- [ ] 维度是否适合该主题？（3-6 个为宜）
- [ ] 问题模板是否包含{topic}和{dimensions}？
- [ ] 是否需要延伸问题来引导 AI？
- [ ] 报告模板是否匹配场景类型？
- [ ] 超时时间是否合理？（简单 60s / 中等 120s / 复杂 180s+）

---

## 🎉 总结

**Multi-AI Search Analysis v1.2** 已完全通用化：

- ✅ **任意主题**：时事、技术、产品、市场、学术、商业...
- ✅ **灵活维度**：用户自定义，不再局限于政治/经济
- ✅ **多种模板**：4 种报告模板适配不同场景
- ✅ **自定义问题**：支持模板和延伸问题
- ✅ **易于使用**：简单命令行即可调用

**核心理念**：让工具适应用户，而不是用户适应工具！

---

*维护者：小呱 🐸*  
*版本：v1.2（通用版）*  
*更新时间：2026-03-16 23:45*
