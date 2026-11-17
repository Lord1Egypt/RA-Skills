---
name: mingxi-analyzer
description: 明析分析框架体系（明析-analyzer）。当用户需要进行结构化深度分析、系统诊断、矛盾分析、博弈推演、内容质量评估、知识管理或交叉验证时使用。触发词：分析、诊断、推演、复盘、评估、框架分析、系统诊断、矛盾分析、五层推演、OCGS、政策解读、灵感评估、交叉验证。适用于政策分析、市场研究、战略规划、内容评估、组织诊断、复杂问题拆解等场景。此技能将方法论转化为可操作的分析流程，确保每次输出都有信度标注、失效条件和回查计划。
---

# 明析分析框架体系

## 运行内核

遇到任何问题的第一反应顺序：**实事求是 → 矛盾分析 → 实践循环 → 持久战**

## 🚦 TCR前置（必须第一步）

**每次开始任何任务前，必须先执行TCR分类。** 分类结果决定后续走哪条纪律包。

参考 `references/00-tcr.md`。

---

## 核心工作流

### TCR-C类（常规分析）标准流程（4步）

```
第0步：TCR分类 → C类
第1步：事实收集 → 标注信度（T3）
第2步：框架分析（选1个框架）
第3步：输出 → 核心判断 + 来源标注
```

### TCR-D类（深度分析）标准流程（7步）

```
第0步：TCR分类 → D类
第1步：检察官前置核查（references/07-safety-gates.md → 第0步）
第2步：事实收集 → 标注信度
第3步：框架分析（选1-2个框架深入）
第4步：矛盾定位 + 输出判断 → 核心判断 + 否定了 + 不变量 + 失效条件 + 回查
第5步：预防迎合四问
第6步：复盘（references/09-review-template.md）→ 判断回查登记
```

### TCR-E类（自我审视）标准流程
同D类，输出尾部追加自省后问：**"这个结论的反面有没有可能成立？"**

### 框架选择指南

| 问题类型 | 推荐框架 | 参考文件 |
|:---------|:---------|:---------|
| 系统/组织/战略短板诊断 | OCGS六维 | references/01-ocgs.md |
| 多对手博弈（市场/政策/军事） | 五层推演法 | references/02-five-layer.md |
| 复杂混沌局面 | 矛盾分析（三态+性质） | references/03-contradiction.md |
| 官方公报/政策文件解读 | 政策信号解读法 | references/04-policy-signal.md |
| 文章/视频/课程内容评估 | 灵感六棱镜 | references/05-six-prism.md |
| 知识/结论管理 | 信度等级体系 | references/06-credibility.md |

---

## 输出强制格式（与TCR联动）

**仅TCR-D类和E类**需要以下格式。A/B/C类不需要。

```
**核心判断**：XXX（T1/T2/T3）
**失效条件**：如果Y发生，此判断作废
**回查日期**：YYYY-MM-DD（默认7天后）
```

复盘输出（D/E类）必须遵循 `references/09-review-template.md` 格式。

---

## Quick Start

```python
# 一键启动分析
python3 scripts/analyze.py --mode ocgs --target "你的分析对象"

# 矛盾分析
python3 scripts/contradiction_analysis.py --problem "你的问题描述"

# OCGS诊断模板
python3 scripts/ocgs_diagnosis.py --system "系统名称"
```

---

## References

| 文件 | 内容 | 什么时候读 |
|:----|:-----|:-----------|
| references/00-tcr.md | 🚦 **TCR任务分类路由**（先分类再动手） | **每次任务开始前，第一步** |
| references/00-core-principles.md | 核心准则（实事求是→矛盾论→实践论→持久战） | 每次分析前 |
| references/01-ocgs.md | OCGS六维系统诊断 | 系统/组织/战略分析时 |
| references/02-five-layer.md | 五层推演法 | 博弈分析时 |
| references/03-contradiction.md | 矛盾分析（三态+性质判定+临界条件） | 复杂局面分析时 |
| references/04-policy-signal.md | 政策信号解读法 | 政策/官方文件解读时 |
| references/05-six-prism.md | 灵感六棱镜 | 内容质量评估时 |
| references/06-credibility.md | T1-T4信度等级体系 | 任何时候涉及信度标注 |
| references/07-safety-gates.md | 安全闸（预防迎合四问+统筹兼顾+框架倾向性自检+直觉核验） | 第0步和输出前 |
| references/08-judgment-tracker.md | 判断回查系统 | 输出判断后 |
| references/09-review-template.md | 复盘格式模板 | 任务闭环后 |

---

## 不适用范围

- 信息极度对称的简单问题（不需要多框架）
- 单因单果的线性问题（OCGS不适合）
- 纯事实查询（不需要分析框架，直接回答即可）
- 日常闲聊
