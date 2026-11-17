---
name: life-money-skill
description: "当用户要做职业变现/搞钱诊断、梳理隐藏技能、规划副业收入或 90 天计划时使用。访谈建档 → 7 轮分析 → HTML 报告。"
version: 1.0.0
---

# Life Money Skill — 路由中枢

> 人生搞钱：职业变现诊断。建档 → 7 轮分析 → 单文件 HTML 报告。

## 路由决策树

```
用户需求
  │
  ├─ "帮我搞钱 / 职业变现 / 收入诊断 / 副业规划"（完整管线）
  │    → §管线（首次运行）
  │
  ├─ "继续上次分析 / 改目标重跑"（已有 projects/<run>/）
  │    → 读 profile.json → 从对应分析维度续跑
  │
  └─ "重新生成报告 / 换版式"
       → scripts/render_report.py
```

## 管线（4 阶段 + 3 道门禁）

```
L1 建档 ─门禁1─▶ L2 分析（含门禁2/3）─▶ L3 渲染 ─▶ L4 验证交付
```

| 阶段 | 动作 | 资源 |
|---|---|---|
| L1 建档 | 请用户提供材料（简历 / 项目报告 / 作品集等）+ 访谈补全 → profile.json | `references/interview-guide.md` |
| **门禁 1** | 材料与信息确认（缺项追问，不猜测） | `interview-guide.md` |
| L2 分析 1 | 发现隐藏技能 | `references/analysis-specs.md` · `references/seven-prompts.md` |
| **门禁 2** | 用户选每月额外赚取目标（默认 1000-3000 元/月） | `analysis-specs.md` |
| L2 分析 2-5 | 收入机会 → 变现路径 → 最大杠杆 → 高薪方向 | 同上 |
| **门禁 3** | 用户填每周启动可投入时间（默认 6 小时） | `analysis-specs.md` |
| L2 分析 6-7 | AI 副业服务 → 90 天计划 → analysis.json | 同上 |
| L3 渲染 | 校验 analysis.json → report.html | `scripts/render_report.py` |
| L4 验证 | 读回 + 截图 QA → 交付 `projects/<YYYY-MM-DD>-<slug>/` | `references/report-design.md` |

## 按需加载

| 时机 | 加载 |
|---|---|
| 激活即读 | `CONSTITUTION.md` |
| 建档 | `references/interview-guide.md` |
| 分析全程 | `references/analysis-specs.md` + `references/seven-prompts.md` |
| 市场校准（可选） | `references/data-calibration.md` |
| 渲染 / QA | `references/report-design.md` |

## 禁止事项

- ❌ 7 个维度不增删、不改名、不合并（忠实源方法论）
- ❌ 不跳过 3 道门禁；不编造 profile 之外的经历 / 数字
- ❌ 不接外部 LLM API；不把用户数据提交进 git（`projects/` 全程 gitignored）
- ❌ 不手写 HTML——必须经 render 脚本渲染
- ❌ 不自动对外发布

## 下游对接

| 产出 | 下游 |
|---|---|
| report.html | 浏览器打开 / 打印 PDF |
| analysis.json | 信息图 / 分享卡（后续 Skill 可消费） |

## 产出验证

1. profile.json / analysis.json 通过 Schema 校验
2. report.html 七章 + 附录齐全、无空卡
3. 截图 QA 通过（字体 / 版式 / 溢出检查）
4. 敏感数据未入 git（git status 检查）
