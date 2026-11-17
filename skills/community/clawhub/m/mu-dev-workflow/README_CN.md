<p align="center">
  <picture>
    <img alt="mu-dev-workflow" src="assets/default-banner.png" width="100%">
  </picture>
</p>

# 🔄 mu-dev-workflow · 人虾协作开发工作流

> 面向技术小白的 Skill/代码开发协作流程，别让 Agent 没对齐需求就乱做浪费 Token。

[English](README.md) | **中文** | [🌐 在线主页](https://muippt.github.io/mu-dev-workflow/)

[![微信公众号](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![小红书](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![书籍](https://img.shields.io/badge/书籍-图解团队管理-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skill集合](https://img.shields.io/badge/mu--skill集合-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-dev-workflow)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-dev-workflow)](https://github.com/muippt/mu-dev-workflow/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-dev-workflow)](https://github.com/muippt/mu-dev-workflow/stargazers)

---

### 💡 使用场景示例

1. 🆕 **从零创建新 Skill** — Agent 先问 5 个澄清问题，输出 Intent Brief 确认后才动笔写代码
2. 🐛 **修一个 bug** — 快捷模式：确认问题 → 修复 → 用实际命令输出验证（禁止"应该好了"）
3. 🏗️ **开发新功能** — 完整 5 阶段流程，含设计文档、架构模式选择、双阶段 Review
4. 🔄 **重构现有代码** — 仅走阶段 1-3，明确防止过度重构
5. 📋 **输出方案/计划** — 批判性三问自检（真问题？造轮子？边界案例？）确保交付质量
6. 🤖 **多 Agent 任务委派** — 双阶段 Review（规格审查 + 质量审查）+ Monitor 机制监控长任务
7. 🚫 **防止 Agent 浪费 Token** — 硬门控物理阻断：需求不清时 Agent 无法开始写代码
8. 📝 **Skill 质量审计** — 集成 `skill-audit.sh`，对 Skill 文件进行 23 项自动化质量扫描

---

### ✨ 核心亮点

#### 🚧 五阶段硬门控工作流

整个开发生命周期被切分为五个阶段，每阶段有明确的入口条件和出口条件。任何阶段都不可跳过——阶段 1（需求澄清）未完成时，Agent 物理上无法开始写代码。

| 阶段 | 名称 | 入口条件 | 出口条件 |
|------|------|----------|----------|
| 1 | 需求澄清 | 收到开发/Skill 需求 | 需求类型明确 + 方案选项已给出 + 木老师已确认 |
| 2 | 设计确认 | 阶段1完成，方向已确认 | 方案含批判性自检 + 木老师说"可以"/"开始吧" |
| 2.5 | Skill 质量门控 | （仅 Skill 开发）阶段2完成 | mu-skill-creator 流程完成 + 安全检查通过 |
| 3/4 | 计划与执行 | 阶段2完成 | 任务执行完毕，子Agent返回结果，核心功能可运行 |
| 5 | 验收收尾 | 阶段3/4完成 | Checklist 全绿 + 已 commit + 已报告木老师 |

#### 🧠 批判性三问自检

任何方案/建议/策略输出前必须包含「批判性自检」章节，与方案一体输出。无自检 = 方案不完整，禁止提交给木老师确认。

| # | 自检问题 | 开发场景 | 招聘/HR场景 | 管理/规划场景 |
|---|---------|---------|------------|-------------|
| 1 | **真问题？有没有更简单的解法？** | 方案是否 over-engineering | 策略是否瞄准真正瓶颈 | 目标是真需求还是惯性延续 |
| 2 | **造轮子？已有资源能否复用？** | 现有 Skill/工具能否 cover | 现成流程/团队有没有在做 | 上下游有没有类似目标可协同 |
| 3 | **边界案例？极端情况怎么兜底？** | references 是否完备、降级链 | 候选人放鸽子/HC冻结/JD变更 | 资源不足/方向变化/人不齐 |

#### 🎯 Skill 意图澄清协议

创建任何 Skill 之前，Agent 必须依次提出最多 5 个针对性问题（一次只问一个），厘清 Skill 的核心价值、边界和风险模式。输出一份 **Skill Intent Brief**，经木老师确认后方可进入设计阶段。

| # | 问题 | 目的 |
|---|------|------|
| 1 | 这个 Skill 只做一件事，它必须消除用户的什么认知负担？ | 定位核心价值 |
| 2 | 你最不希望它被误解成什么？ | 定义边界 |
| 3 | 它最危险的失败模式是什么：问太多、问太少、执行太早，还是变成总结机器？ | 识别风险 |
| 4 | 它的输出应该改变谁的行为？ | 明确受益方 |
| 5 | 如果它跑通了，哪个现有工作流会变得多余或变轻？ | 评估影响范围 |

#### 🛡️ 防跳步借口表

6 条常见跳步借口及其现实对照，预注册为反模式。Agent 遇到任何借口时，强制停下来完成阶段 1 再继续。

| 常见借口 | 现实 |
|---------|------|
| "需求很简单，不用设计" | 简单需求同样有隐藏依赖，30分钟设计省去3小时返工 |
| "我已经知道怎么做了" | 知道怎么做 ≠ 木老师知道你要做什么，设计文档是对齐工具 |
| "改一行代码而已" | 一行代码可以影响十个调用方，改之前先看影响范围 |
| "来不及，先做再说" | 先做的代码往往成为技术债，设计时间最多5分钟 |
| "这个功能之前做过" | 之前的上下文可能已变，复用前先确认接口兼容 |
| "木老师催了，跳过设计" | 木老师催的是结果，不是过程；慢就是快 |

#### 🔄 ICE-5 事故闭环

当触发条件满足时（同类失败第二次出现 / 首次造成对外交付或发布事故 / 不可逆或外部依赖存在静默降级风险），五个字段必须嵌入执行路径本身——不是写在独立的 memory 或 issue 里。

| 字段 | 说明 |
|------|------|
| **触发步骤** | 什么动作序列会触发该失败 |
| **强制点** | 门控具体放在代码/脚本/Checklist 的哪个位置 |
| **失败行为** | 门控触发时发生什么 |
| **运行证据** | 强制点处的实际命令输出或审计证据 |
| **失败后动作** | 门控触发后 Agent 必须做什么 |

#### 🤖 子 Agent 双阶段 Review

复杂任务委派给子 Agent 时，强制执行两阶段审查流水线。Monitor Agent 监控长时任务并上报异常。任务体积约束防止上下文截断。

| 阶段 | 审查者 | 检查内容 |
|------|--------|----------|
| 规格审查 | 规格审查 Agent | 设计要求的功能是否全部实现？有无遗漏？有无多余？ |
| 质量审查 | 质量审查 Agent | 可读性、简洁性、健壮性、一致性 |
| 监控（长任务） | Monitor Agent | 每5分钟读取任务看板，发现 blocked/超时立即通知主 Agent |

#### 🏗️ 架构模式库

六大架构模式 + 设计决策树 + 高频共通组件清单，让每个新 Skill 从成熟结构出发，而非从零摸索。

| 模式 | 名称 | 适用场景 |
|------|------|----------|
| A | 路由分发 | 多场景覆盖 |
| B | 线性流水线 | 固定步骤文档产出 |
| C | 双模式交互 | 用户可能已有部分信息 |
| D | 能力模块 | 多功能复合型 Skill |
| E | 规则引擎 | 质量扫描/安全检查/格式修正 |
| F | 三级分层 | 必须做 vs 可以做分离 |

---

### 📌 与同类工具对比

| 维度 | 🧭 mu-dev-workflow | 裸开发 | Superpowers |
|------|-------------------|--------|-------------|
| 结构 | 1 文件 + 3 引用文件，自包含 | 无 | 14 个内置 Skill，颗粒度细 |
| 目标用户 | 技术小白 | 无门槛 | 有经验的开发者 |
| 适用范围 | Skill 开发 + 代码开发 | 任意 | 通用软件工程 |
| 事故闭环 | ICE-5 五字段机制 | 无 | 无 |
| 防跳步 | 显式借口表 + 现实对照 | 无 | 流程中隐式约束 |
| 架构指导 | 6 模式 + 决策树 | 无 | 无 |
| Skill 创建 | 意图澄清 + 4 种类型模板 | 无 | 无 |
| 子 Agent 审查 | 双阶段 + Monitor + 体积约束 | 无 | 有子 Agent 机制 |
| 平台 | Agent 无关（适配任意 AI Agent） | 任意 | Claude Code 原生 |
| 许可证 | MIT | N/A | MIT |

---

### 🚀 四大工作流

| 工作流 | 场景 | 触发方式 |
|--------|------|----------|
| 完整 5 阶段 | 新 Skill 开发、大型功能 | "开发"/"写代码"/"新功能"/"新skill" |
| 快捷模式 | Skill 创建 <1500 行 | 按规模估算自动触发 |
| Bug 修复捷径 | 小 bug（<30 分钟） | "修bug"/"fix" |
| 非开发自检 | 方案、计划、策略 | "方案自检"/"三问自检" |

---

### ⚙️ 技术规格

| 项目 | 说明 |
|------|------|
| 类型 | AI Agent 方法论框架（Markdown 规则） |
| 依赖 | 无（纯 Markdown，无运行时） |
| 兼容环境 | 任何支持自定义指令/Skill 的 AI Agent（Claude Code、Cursor、CatPaw 等） |
| 包体积 | ~30KB（4 个 Markdown 文件） |
| 文件结构 | SKILL.md + references/（3 个文件） |
| 输入支持 | 自然语言触发 |
| 输出格式 | 设计文档、代码、验收报告 |
| 语言 | 中文（主），英文（README） |
| 版本 | 2.1.0 |
| 许可证 | MIT |

---

### 🛠️ 快速开始

**1. 安装**

```bash
git clone https://github.com/muippt/mu-dev-workflow.git ~/.claude/skills/mu-dev-workflow
```

> 其他 Agent（Cursor、CatPaw 等）可使用各自的 Skill 目录或项目级 `.claude/skills/mu-dev-workflow`。

**2. 验证**

重启 Agent 后，输入：

```
列出我当前可用的 Skills
```

**3. 使用**

```
帮我开发一个新功能
```

也可以直接进入指定工作流：

```
帮我创建一个新的 Skill
```

```
帮我做方案自检，用三问自检
```

---

### 🔒 安全与隐私

- 100% 本地执行，无网络调用
- 无遥测，无数据收集
- 纯 Markdown 文件，无可执行代码
- 无需 API 密钥或凭证

---

### ⭐ Star 趋势

如果 mu-dev-workflow 帮你省下了 Token，欢迎点个 Star！

[![Star History Chart](assets/star-history.png)](https://www.star-history.com/?repos=muippt%2Fmu-dev-workflow&type=date)

> 面向技术小白的 Skill/代码开发协作流程，别让 Agent 没对齐需求就乱做浪费 Token。

---

### 👤 作者简介

🎓 清华大学出版社签约作家 / 2026 当当影响力作家 / 某互联网大厂 AI 大模型业务 HR 砖家 / 一级人力资源管理师 / 二级心理咨询师 / 野生设计师

📚 著有[《图解团队管理》](https://item.m.jd.com/product/14547345.html)，服务客户有字节跳动、腾讯、百度、中国移动、SMG、BOE…

💡 [微信公众号](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [小红书](https://xhslink.com/m/ESxtgUNMdl)：muippt

### 📄 许可证与致谢

[MIT](LICENSE) © 2026 木先生 (muippt)

本项目灵感来源于 [Superpowers](https://github.com/obra/superpowers)（Jesse Vincent）。批判性思维框架参考《学会提问》（Browne & Keeley）。

> 声明：本项目大部分内容由 AI 辅助完成。如您认为您的作品被使用但未获得适当署名，请提交 issue。
