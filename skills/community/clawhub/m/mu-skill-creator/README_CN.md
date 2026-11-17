<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/default-banner.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/default-banner.png">
    <img alt="mu-skill-creator" src="assets/default-banner.png" width="100%">
  </picture>
</p>

# 🦐 mu-skill-creator · Skill创作发明家

> AI Agent 技能的质量守门员 —— 内置 56 项 10 层审计模型、39 条反模式与 8 阶段门控创建工作流。

[English](README.md) | **中文** | [🌐 在线主页](https://muippt.github.io/mu-skill-creator/)

[![微信公众号](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![小红书](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![书籍](https://img.shields.io/badge/书籍-图解团队管理-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skill集合](https://img.shields.io/badge/mu--skill集合-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-skill-creator)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-skill-creator)](https://github.com/muippt/mu-skill-creator/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-skill-creator)](https://github.com/muippt/mu-skill-creator/stargazers)

---

### 💡 使用场景示例

| 场景 | 你说的话 | 实际效果 |
|------|---------|---------|
| 🆕 从零创建新技能 | "创建一个把 Markdown 转排版的 Skill" | 完整 8 阶段门控流程：需求 → 规划 → L1/L2/L3 编写 → 审计 → 交付 |
| 🔍 审计已有技能 | "帮我审计 my-skill 的质量" | 10 层 56 项逐项检查，自动脚本扫描 + 人工判断项 |
| 🚫 修复反模式 | "检查我的 Skill 有没有反模式" | 扫描 AP-1 至 AP-39 反模式目录，逐条标注根因与修复方案 |
| 🎯 优化触发词 | "我的 Skill 总是不被触发，帮我修" | 触发词分析：禁用词扫描、覆盖率测试、Pushy 原则检查 |
| 📊 批量扫描多个技能 | `bash scripts/skill-audit.sh skill-a skill-b` | 一条命令完成多技能结构健康检查 |
| ✂️ 重构臃肿技能 | "我的 SKILL.md 有 400 行，帮我瘦身" | 应用三层模型：L2 控制在 ≤ 300 行，参考资料下沉到 L3 |

---

### ✨ 核心亮点

#### 56 项 10 层审计模型

10 层审计覆盖文档结构、架构一致性、代码质量、跨文件对齐、安全合规、健壮性和内容质量。30 项可通过脚本自动扫描，26 项需人工判断。每条规则都追溯至真实事故——不是抽象建议。

| 层级 | 审计目标 | 项数 | 自动 |
|------|---------|------|------|
| L1 | 文档结构 | 9 | 6 |
| L2 | 架构一致性 | 5 | 2 |
| L3 | 代码质量 | 8 | 6 |
| L4 | 跨文件一致性 | 5 | 1 |
| L5 | 文档↔代码对齐 | 3 | 2 |
| L6 | 依赖完整性 | 3 | 2 |
| L7 | 文件卫生 | 6 | 5 |
| L8 | 安全合规 | 4 | 3 |
| L9 | 健壮性与降级 | 7 | 1 |
| L10 | 内容质量 | 6 | 1 |
| **合计** | | **56** | **30** |

#### 三层架构（L1 / L2 / L3）

上下文感知加载：L1 触发层始终加载（约 100 词），L2 工作流层激活时加载（SKILL.md ≤ 300 行），L3 参考层按需加载。从架构层面控制上下文窗口膨胀——只在需要时加载需要的内容。

#### AP-1 ~ AP-39 反模式目录

39 条反模式，每条追溯到真实事故，关联设计原则，配有具体修复方案。是实战验证的纠正措施，不是抽象建议。每次审计周期自动扫描。

v4.1 新增：AP-35（事故闭环 / ICE-5）、AP-36（附件文件职责重叠）、AP-37（已知局限膨胀——三要素结构 + P/D/E 分类 + ≤3 条 + 三维重要性排序）。

#### 自动化审计脚本

`skill-audit.sh` 一条命令批量扫描，检查 IRON LAW 位置、description 格式、安全风险、行数、代码质量、断链引用等——在每次交付前拦截问题。

#### 停滞检测规则

内置量化信号（stale_count、时间限制、失败阈值），防止迭代或定时任务中的无限循环和静默失败。当进度停滞时，系统切换的是结构——而不只是调参数。

#### 安全优先设计

硬性规则杜绝凭据泄露、人员数据暴露和受限系统访问。自动扫描在交付前拦截违规。`.skillignore` 确保用户态文件不进入版本控制。

---

### 📌 与同类工具对比

| 维度 | mu-skill-creator | 手工编写 | 通用提示模板 | AI Agent 框架 |
|------|-----------------|---------|------------|--------------|
| 审计模型 | 56 项 10 层 | 无 | 无 | 不定 |
| 自动化扫描 | ✅ Shell 脚本 | ❌ | ❌ | 少见 |
| 反模式目录 | 39 条，追溯事故 | 无 | 无 | 较少 |
| 上下文感知加载 | ✅ 三层 L1/L2/L3 | ❌ 单文件 | ❌ | 不定 |
| 门控工作流 | ✅ 8 阶段入口/出口 | ❌ | ❌ | 少见 |
| 停滞检测 | ✅ 量化信号 | ❌ | ❌ | ❌ |
| 安全扫描 | ✅ 交付前 | 仅人工 | ❌ | 不定 |
| 触发词优化 | ✅ 10+10 测试，覆盖率检查 | ❌ | ❌ | ❌ |
| 已知局限标准 | ✅ 三要素 + P/D/E + ≤3 条 | ❌ | ❌ | ❌ |

---

### 🚀 工作流

| 工作流 | 场景 | 触发方式 |
|--------|------|---------|
| 创建新技能 | 从零构建技能 | "创建一个做 X 的 Skill" |
| 审计已有技能 | 交付前质量检查 | "帮我审计 my-skill 的质量" |
| 修复反模式 | 诊断技能退化 | "检查我的 Skill 有没有反模式" |
| 优化触发词 | 技能不被可靠触发 | "我的 Skill 不触发" |
| 重构臃肿技能 | SKILL.md 超过 300 行 | "帮我瘦身 SKILL.md" |
| 批量扫描 | 多技能健康检查 | `bash scripts/skill-audit.sh skill-a skill-b` |
| 交付 | 最终安全扫描 + 打包（发布动作委托专用工具） | "交付 my-skill" |

---

### ⚙️ 技术规格

| 项目 | 说明 |
|------|------|
| 架构 | 三层模型（L1 触发 / L2 工作流 / L3 参考） |
| 审计模型 | 10 层 56 项（30 项自动扫描，26 项人工判断） |
| 反模式 | 39 条，每条关联真实事故与修复方案 |
| 已知局限 | 三要素结构（能力边界→触发条件→降级路径）、P/D/E 分类、≤3 条、三维重要性评估 |
| 工作流阶段 | 8 个主阶段 + 2 个可选阶段（1.5 案例收集、6.5 Eval 测试） |
| 审计脚本 | Bash 脚本，零外部依赖 |
| 技能格式 | Markdown（SKILL.md）+ references/ + scripts/ + assets/ |
| 依赖 | 无——纯 Markdown + Bash |
| 输出格式 | SKILL.md + 参考文档 + 自动审计报告 |
| 行数预算 | L2 ≤ 300 行（官方建议 500，收紧至 300 留余量） |
| IRON LAW | 业务专属约束，上限 6 条 |
| 版本 | v4.1.9 |

---

### 🛠️ 快速开始

**1. 克隆并安装**

```bash
git clone https://github.com/muippt/mu-skill-creator.git
cp -r mu-skill-creator /path/to/your/agent/skills/
```

**2. 创建或审计技能**

告诉你的 AI Agent：

```
"创建一个做 X 的 Skill"            → 完整 8 阶段创建流程
"帮我审计 my-skill 的质量"         → 56 项 10 层审计
```

**3. 运行自动化扫描**

```bash
bash scripts/skill-audit.sh <skill-name>    # 扫描单个技能
bash scripts/skill-audit.sh                  # 扫描全部技能
bash scripts/skill-audit.sh --verbose        # 详细输出
```

---

### 🔒 安全与隐私

- **技能文件禁止包含凭据** —— Token、API Key、密钥不得出现在 SKILL.md、frontmatter 或参考文档中。
- **禁止包含个人数据** —— 姓名、用户 ID、组织信息和敏感人员数据在所有技能文件中均被禁止。
- **受限系统黑名单** —— 技能不得调用 HR、人才管理等敏感内部系统的 API。
- **用户态数据隔离** —— 本地偏好、快照、推荐历史必须通过 `.skillignore` 排除，不随技能包发布。
- **自动化安全扫描** —— `skill-audit.sh` 在每次交付前检查凭据泄露、PII 暴露和受限系统引用。
- **本地运行** —— 一切在本地运行，无遥测、无数据收集、无云端调用。

---

### ⭐ Star 趋势

如果这个项目帮你构建了更好的 AI Agent 技能，给个 star ⭐

[![Star History Chart](assets/star-history.png)](https://www.star-history.com/?repos=muippt%2Fmu-skill-creator&type=date)

> AI Agent 技能的质量守门员 —— 56 项，10 层，39 条反模式，零妥协。

---

### 👤 作者简介

🎓 清华大学出版社签约作家 / 2026 当当影响力作家 / 某互联网大厂 AI 大模型业务 HR 砖家 / 一级人力资源管理师 / 二级心理咨询师 / 野生设计师

📚 著有[《图解团队管理》](https://item.m.jd.com/product/14547345.html)，服务客户有字节跳动、腾讯、百度、中国移动、SMG、BOE…

💡 [微信公众号](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [小红书](https://xhslink.com/m/ESxtgUNMdl)：muippt

---

### 📄 许可证与致谢

[MIT](LICENSE) © 2026 muippt

本项目站在 AI Agent 社区的肩膀上。感谢开源工具、设计模式和真实事故教训对这一框架的塑造。

> 声明：本项目大部分内容由 AI 辅助完成。如您认为您的作品被使用但未获得适当署名，请提交 issue。

---

> **版本**：v4.1.9 · [在线主页](https://muippt.github.io/mu-skill-creator/) · [发布历史](https://github.com/muippt/mu-skill-creator/releases)
>
> **v4.1.9 更新**：脱敏修复——移除 AP-39 事故描述中的内部平台名（quality-gates.md），无功能变更。
