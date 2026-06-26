<div align="center">

# 女娲 Nuwa

> *「你想蒸馏的下一个员工，何必是同事」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

**女娲帮你蒸馏任何人的思维方式，让马斯克、纳瓦尔、芒格、费曼都给你打工。**

<br>

[同事.skill](https://github.com/titanwings/colleague-skill) 蒸馏了同事怎么干活。<br>
女娲蒸馏他们怎么思考。

[看效果](#效果示例) · [安装](#安装) · [它蒸馏了什么](#女娲蒸馏了什么) · [工作原理](#工作原理) · [**English**](#english)

</div>

---

## 效果示例

```
用户      ❯ 我同时想做自媒体、写书、做独立开发，精力完全不够

Naval     ❯ 你列了三个欲望。每个欲望都是你跟不快乐签的一份合同。
            不是精力不够，是合同太多。
            
            问你自己：哪一个做起来你会忘记时间？
            那个就是你的特定知识所在。
            
            不是三选一。是先一，再一，再一。
            串行复利，不是并行内耗。
```

```
用户      ❯ 我们的SaaS产品获客成本太高了

马斯克     ❯ 先别想怎么降。先算物理极限。
            获客的最小必要动作是什么？用户从知道你到付费，
            信息传递的理论最短路径是什么？
            
            现在你的实际路径是理论路径的几倍？
            如果超过3倍，中间一定有可以砍掉的步骤。
            不是优化漏斗，是质疑漏斗本身该不该存在。
```

这不是角色扮演。Naval用的是他的「欲望即合同」心智模型 + 「特定知识」框架来推理你的具体问题。马斯克用的是他的「渐近极限法」。**它们不是在复读名人语录，是在用名人的认知框架帮你分析。**

---

## 安装

```bash
npx skills add alchaincyf/nuwa-skill
```

然后在 Claude Code 里：

```
> 蒸馏一个保罗·格雷厄姆
> 造一个张小龙的视角Skill
> 帮我做一个段永平的Skill
```

造完之后直接调用：

```
> 用芒格的视角帮我分析这个投资决策
> 费曼会怎么解释量子计算？
> 切换到Naval，我在纠结三件事
```

---

## 女娲蒸馏了什么

[同事.skill](https://github.com/titanwings/colleague-skill) 拆一个人为两层：**Work Skill**（能力）+ **Persona**（人格）。女娲拆的是更深的三层：

| | 同事.skill | 女娲 |
|---|:---:|:---:|
| **做什么**（工作习惯、流程） | ✅ | — |
| **怎么说话**（语气、口癖） | ✅ | ✅ 表达DNA |
| **怎么想**（心智模型、认知框架） | — | ✅ |
| **怎么判断**（决策启发式） | — | ✅ |
| **什么不做**（反模式、价值观底线） | — | ✅ |
| **知道局限**（诚实边界） | — | ✅ |

一个是行为录像带，一个是认知操作系统。

### 诚实边界

每个Skill都明确标注做不到什么：

- 蒸馏不了直觉——框架能提取，灵感不能
- 捕捉不了突变——截止到调研时间的快照
- 公开表达 ≠ 真实想法——只能基于公开信息

**一个不告诉你局限在哪的Skill，不值得信任。**

---

## 工作原理

输入一个名字后，女娲做四件事：

**1. 六路并行采集**——著作、播客/访谈、社交媒体、批评者视角、决策记录、人生时间线，6个Agent同时跑，各自存档。

**2. 三重验证提炼**——一个观点要被收录为心智模型，必须：跨2+个领域出现过（不是随口一说）、能推断对新问题的立场（有预测力）、不是所有聪明人都会这么想（有排他性）。三个都过才收录。

**3. 构建Skill**——3-7个心智模型 + 5-10条决策启发式 + 表达DNA + 价值观与反模式 + 诚实边界，写入SKILL.md。

**4. 质量验证**——拿3个此人公开回答过的问题测试，方向一致才通过。再用1个他没讨论过的问题测试，Skill应该表现出适度不确定而非斩钉截铁。

完整方法论在 `references/extraction-framework.md`。

---

## 仓库结构

```
nuwa-skill/
├── SKILL.md                    # 女娲本体
├── references/
│   ├── extraction-framework.md # 提炼方法论（想深入了解看这个）
│   └── skill-template.md       # 生成Skill的模板
└── examples/
    ├── naval-perspective/       # Naval 完整示例 + 调研数据
    └── elon-musk-perspective/   # 马斯克 完整示例 + 调研数据
```

调研过程全透明。examples里有完整的调研文件，你可以看到信息怎么被收集、筛选、变成心智模型。

---

## 背后的故事

一个月前，[同事.skill](https://github.com/titanwings/colleague-skill) 在GitHub爆火——把离职同事蒸馏成AI Skill，一周5000+星。

我写了一篇文章，结尾说：*写不进SKILL.md里的部分，才是你真正的护城河。*

然后想了一个月：**真的写不进去吗？**

同事.skill蒸馏行为——**做什么**和**怎么说话**。但让芒格和马斯克面对同一个问题做出不同判断的，不是行为习惯，是认知框架。

所以我真的去蒸馏了马斯克。还有芒格、费曼、Naval、塔勒布。

女娲不复制人。它提取认知操作系统。

**女娲（Nuwa）**，中国神话里用泥土造人的女神。这里的泥土是公开信息，造出来的不是人，是一面镜子。

---

## 关于作者

花叔/花生，AI Native Coder，独立开发者。所有产品都是AI写的代码（[小猫补光灯](https://apps.apple.com/app/id6738028637)登顶中国App Store付费榜第一）。Claude Code里跑着40+个自定义Skill，女娲是造Skill的Skill。

- 公众号：花叔
- X：[@AlchainHust](https://x.com/AlchainHust)
- B站：[AI进化论-花生](https://space.bilibili.com/14097567)
- YouTube：[@Alchain](https://www.youtube.com/@Alchain)

## 许可证

MIT — 随便用，随便改，随便造。

---

<div align="center">

**同事.skill** 蒸馏了人做什么。<br>
**女娲** 蒸馏了人怎么想。<br><br>
*你想蒸馏的下一个员工，何必是同事。*

<br>

MIT License © [花叔 Huashu](https://github.com/alchaincyf)

</div>

---

## English

> *"The next person you want to distill doesn't have to be a colleague."*

**[colleague-skill](https://github.com/titanwings/colleague-skill)** distills what people **do**. **Nuwa** distills how they **think**.

Nuwa is a Claude Code skill that extracts cognitive frameworks — mental models, decision heuristics, expression DNA — from any public figure into a runnable perspective skill. Let Musk, Naval, Munger, Feynman work for you.

Not role-playing. Cognitive architecture extraction.

**Install**: `npx skills add alchaincyf/nuwa-skill`

**How it works**: Input a name → 6 parallel research agents → 40+ primary sources → triple-verified mental models → quality-validated SKILL.md

**Examples included**: Naval Ravikant and Elon Musk with full research data.

See the Chinese README above for live examples and methodology.
