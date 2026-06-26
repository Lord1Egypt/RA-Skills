# OpenClaw Ops Skills Pack
# OpenClaw 运维技能包

> **Production-ready skills for autonomous agent operations**
> **生产级自主代理运维技能**

> **Transform your agent from chatbot to infrastructure**
> **将您的代理从聊天机器人转变为基础设施**

---

## Table of Contents / 目录

- [Overview / 概述](#overview--概述)
- [Key Features / 核心功能](#key-features--核心功能)
- [Skills Breakdown / 技能详解](#skills-breakdown--技能详解)
- [Installation / 安装](#installation--安装)
- [Configuration / 配置](#configuration--配置)
- [Usage Guide / 使用指南](#usage-guide--使用指南)
- [Best Practices / 最佳实践](#best-practices--最佳实践)
- [FAQ / 常见问题](#faq--常见问题)

---

## Overview / 概述

### English

The OpenClaw Ops Skills Pack is a comprehensive collection of 14 production-ready skills designed to transform OpenClaw from a simple chatbot into reliable autonomous infrastructure. Based on 1.4+ billion tokens of real-world testing, these skills provide the guardrails, workflows, and best practices needed for autonomous agent operations that work while you sleep.

### 中文

OpenClaw 运维技能包是一套包含 14 个生产级技能的全面集合，旨在将 OpenClaw 从简单的聊天机器人转变为可靠的自主基础设施。基于超过 14 亿 token 的真实世界测试，这些技能为自主代理操作提供了防护栏、工作流程和最佳实践，让代理在您睡眠时也能正常工作。

---

## Key Features / 核心功能

### 🎯 Cost Optimization / 成本优化

**English**: Reduce token costs by up to 80% through intelligent model routing. Use Sonnet 4.6 for daily operations (95% of Opus capability at 20% cost) and budget models like Kimi K2.5 for routine tasks.

**中文**: 通过智能模型路由减少高达 80% 的 token 成本。日常操作使用 Sonnet 4.6（拥有 Opus 95% 的能力，成本仅为 20%），常规任务使用 Kimi K2.5 等预算模型。

---

### 🤖 True Autonomy / 真正的自主性

**English**: Self-expanding task lists that grow organically as work progresses. Agent discovers subtasks, adds them to Todo.md, and continues work without human intervention.

**中文**: 自我扩展的任务列表随着工作进展有机增长。代理发现子任务，将其添加到 Todo.md，并在无需人工干预的情况下继续工作。

---

### 🧠 Persistent Memory / 持久化记忆

**English**: File-based memory system survives session compression. Critical decisions, learned patterns, and user preferences persist across sessions.

**中文**: 基于文件的记忆系统在会话压缩后仍然存在。关键决策、学习到的模式和用户偏好在会话之间持久保存。

---

### 📊 Complete Visibility / 完全可见性

**English**: Comprehensive progress logs replace the need to scroll through chat history. Wake up to a clear morning briefing of overnight work.

**中文**: 全面的进度日志取代了滚动浏览聊天记录的需要。醒来后即可看到清晰的隔夜工作晨间简报。

---

### 🔒 Security Hardening / 安全加固

**English**: Built-in security practices protect against credential exposure, unauthorized access, and malicious skill installation.

**中文**: 内置的安全实践可防止凭据泄露、未经授权的访问和恶意技能安装。

---

## Skills Breakdown / 技能详解

### Core Infrastructure Skills / 核心基础设施技能

#### 1. Model Routing / 模型路由

**English**:
- **Purpose**: Optimize model selection for cost-effectiveness
- **Key Features**:
  - Sonnet 4.6 for daily operations (default)
  - Opus 4.6 fallback for complex reasoning
  - Budget models for routine tasks
  - Automatic escalation and downgrade logic

**中文**:
- **用途**: 优化模型选择以提高成本效益
- **主要功能**:
  - Sonnet 4.6 用于日常操作（默认）
  - Opus 4.6 作为复杂推理的后备
  - 预算模型用于常规任务
  - 自动升级和降级逻辑

**Cost Comparison / 成本对比**:

| Model / 模型 | Cost (per 1M tokens) | Use Case / 使用场景 |
|--------------|---------------------|---------------------|
| Opus 4.6 | $15/$75 | Complex reasoning / 复杂推理 |
| Sonnet 4.6 | $3/$15 | Daily operations / 日常操作 ⭐ |
| Kimi K2.5 | $0.60/$2 | Budget tasks / 预算任务 |
| MiniMax M2.5 | $0.30/$1.20 | High-volume / 高吞吐量 |

---

#### 2. Execution Discipline / 执行纪律

**English**:
- **Purpose**: Build → Test → Document → Decide cycle
- **Key Features**:
  - Smallest meaningful change per iteration
  - Mandatory testing before proceeding
  - Progress logging after each cycle
  - Maximum 3 iterations before re-planning

**中文**:
- **用途**: 构建 → 测试 → 记录 → 决策循环
- **主要功能**:
  - 每次迭代最小的有意义的更改
  - 继续之前必须进行测试
  - 每个循环后记录进度
  - 重新规划前最多 3 次迭代

---

#### 3. Docs-First / 文档优先

**English**:
- **Purpose**: Never touch code without reading documentation first
- **Key Features**:
  - Mandatory reconnaissance phase
  - Documentation search protocol
  - Existing solution identification
  - Recon file creation before building

**中文**:
- **用途**: 在不先阅读文档的情况下绝不触碰代码
- **主要功能**:
  - 强制侦察阶段
  - 文档搜索协议
  - 现有解决方案识别
  - 构建前创建侦察文件

---

#### 4. Scope Control / 范围控制

**English**:
- **Purpose**: Define and enforce operational boundaries
- **Key Features**:
  - Pre-task scope declaration
  - File system boundaries
  - Change type restrictions
  - Scope creep detection

**中文**:
- **用途**: 定义和执行操作边界
- **主要功能**:
  - 任务前范围声明
  - 文件系统边界
  - 更改类型限制
  - 范围蔓延检测

---

#### 5. Task Autonomy / 任务自主性

**English**:
- **Purpose**: Self-expanding task management
- **Key Features**:
  - Task decomposition
  - Discovery during execution
  - Self-task selection
  - Automatic dependency resolution

**中文**:
- **用途**: 自我扩展的任务管理
- **主要功能**:
  - 任务分解
  - 执行期间发现
  - 自我任务选择
  - 自动依赖解析

---

#### 6. Progress Logging / 进度日志

**English**:
- **Purpose**: Comprehensive, searchable logs
- **Key Features**:
  - Chronological execution records
  - Test results with evidence
  - Morning briefing generation
  - Daily summary creation

**中文**:
- **用途**: 全面的可搜索日志
- **主要功能**:
  - 按时间顺序的执行记录
  - 带证据的测试结果
  - 晨间简报生成
  - 每日摘要创建

---

### Operational Skills / 运维技能

#### 7. Memory Persistence / 记忆持久化

**English**:
- **Purpose**: Maintain critical state across sessions
- **Key Features**:
  - MEMORY.md for facts and decisions
  - USER.md for preferences
  - LESSONS.md for learned patterns
  - STATE.md for session recovery

**中文**:
- **用途**: 在会话间维护关键状态
- **主要功能**:
  - MEMORY.md 用于事实和决策
  - USER.md 用于偏好
  - LESSONS.md 用于学习的模式
  - STATE.md 用于会话恢复

---

#### 8. Cron Orchestration / 定时编排

**English**:
- **Purpose**: Scheduled task management
- **Key Features**:
  - Overnight work cycles
  - Wake-up scheduling
  - Session recovery
  - Morning briefing automation

**中文**:
- **用途**: 定时任务管理
- **主要功能**:
  - 隔夜工作周期
  - 唤醒调度
  - 会话恢复
  - 晨间简报自动化

---

#### 9. Error Recovery / 错误恢复

**English**:
- **Purpose**: Graceful failure handling
- **Key Features**:
  - Error classification
  - Recovery strategies
  - Escalation protocols
  - Learning from failures

**中文**:
- **用途**: 优雅的失败处理
- **主要功能**:
  - 错误分类
  - 恢复策略
  - 升级协议
  - 从失败中学习

---

#### 10. Security Hardening / 安全加固

**English**:
- **Purpose**: Security best practices
- **Key Features**:
  - Credential management
  - Skill validation protocol
  - Audit trail requirements
  - Incident response procedures

**中文**:
- **用途**: 安全最佳实践
- **主要功能**:
  - 凭据管理
  - 技能验证协议
  - 审计跟踪要求
  - 事件响应程序

---

#### 11. Cost Optimization / 成本优化

**English**:
- **Purpose**: Token waste prevention
- **Key Features**:
  - Usage monitoring
  - Efficiency metrics
  - Cost-saving techniques
  - ROI calculation

**中文**:
- **用途**: Token 浪费预防
- **主要功能**:
  - 使用监控
  - 效率指标
  - 成本节省技术
  - ROI 计算

---

#### 12. Testing Protocol / 测试协议

**English**:
- **Purpose**: Quality assurance standards
- **Key Features**:
  - Test coverage requirements
  - TDD support
  - Quality gates
  - Test documentation

**中文**:
- **用途**: 质量保证标准
- **主要功能**:
  - 测试覆盖率要求
  - TDD 支持
  - 质量门控
  - 测试文档

---

#### 13. Communication / 通信

**English**:
- **Purpose**: Clear, structured updates
- **Key Features**:
  - Update templates
  - Status indicators
  - Escalation formats
  - Morning briefings

**中文**:
- **用途**: 清晰的结构化更新
- **主要功能**:
  - 更新模板
  - 状态指示器
  - 升级格式
  - 晨间简报

---

#### 14. Integration Guide / 集成指南

**English**:
- **Purpose**: Safe third-party connections
- **Key Features**:
  - Pre-integration checklist
  - Security considerations
  - Testing protocols
  - Rollback procedures

**中文**:
- **用途**: 安全的第三方连接
- **主要功能**:
  - 集成前检查清单
  - 安全考虑
  - 测试协议
  - 回滚程序

---

## Installation / 安装

### Quick Install / 快速安装

**English**:

```bash
# Clone or download the repository
git clone https://github.com/yourusername/openclaw-ops-skills.git
cd openclaw-ops-skills

# Copy skills to your OpenClaw workspace
cp skills/*.md ~/.openclaw/workspace/skills/

# Verify installation
ls ~/.openclaw/workspace/skills/
# You should see: model-routing.md, execution-discipline.md, etc.
```

**中文**:

```bash
# 克隆或下载仓库
git clone https://github.com/yourusername/openclaw-ops-skills.git
cd openclaw-ops-skills

# 将技能复制到 OpenClaw 工作区
cp skills/*.md ~/.openclaw/workspace/skills/

# 验证安装
ls ~/.openclaw/workspace/skills/
# 您应该看到: model-routing.md, execution-discipline.md 等
```

---

### Workspace Setup / 工作区设置

**English**:

```bash
# Copy workspace templates
cp templates/workspace-setup.md ~/.openclaw/workspace/

# Create individual workspace files
cd ~/.openclaw/workspace

# Create and edit USER.md
cat > USER.md << 'EOF'
# User Profile
**Name**: Your Name
**Role**: Developer
**Timezone**: Your TZ
[Fill in more details...]
EOF

# Create other necessary files
touch MEMORY.md Todo.md progress-log.md SOUL.md
```

**中文**:

```bash
# 复制工作区模板
cp templates/workspace-setup.md ~/.openclaw/workspace/

# 创建单独的工作区文件
cd ~/.openclaw/workspace

# 创建并编辑 USER.md
cat > USER.md << 'EOF'
# User Profile
**Name**: 您的姓名
**Role**: 开发者
**Timezone**: 您的时区
[填写更多详细信息...]
EOF

# 创建其他必要的文件
touch MEMORY.md Todo.md progress-log.md SOUL.md
```

---

## Configuration / 配置

### Model Routing Configuration / 模型路由配置

**English**:

Edit `~/.openclaw/config.json`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-6",
        "fallbacks": [
          "anthropic/claude-opus-4-6",
          "openrouter/moonshotai/kimi-k2.5"
        ],
        "auto_escalation": true,
        "escalation_threshold": 2
      }
    }
  }
}
```

**中文**:

编辑 `~/.openclaw/config.json`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-6",
        "fallbacks": [
          "anthropic/claude-opus-4-6",
          "openrouter/moonshotai/kimi-k2.5"
        ],
        "auto_escalation": true,
        "escalation_threshold": 2
      }
    }
  }
}
```

---

### Cron Job Setup / 定时任务设置

**English**:

```bash
# Early night check (2 AM)
openclaw cron add \
  --name "overnight-2am" \
  --cron "0 2 * * *" \
  --message "Check Todo.md. Pick up incomplete tasks. Update progress-log."

# Mid night continuation (4 AM)
openclaw cron add \
  --name "overnight-4am" \
  --cron "0 4 * * *" \
  --message "Continue working through Todo.md. Update progress-log."

# Morning briefing (6 AM)
openclaw cron add \
  --name "overnight-6am" \
  --cron "0 6 * * *" \
  --message "Final check. Summarize all overnight work."

# List cron jobs
openclaw cron list
```

**中文**:

```bash
# 早期夜间检查（凌晨 2 点）
openclaw cron add \
  --name "overnight-2am" \
  --cron "0 2 * * *" \
  --message "检查 Todo.md。接手未完成的任务。更新进度日志。"

# 午夜继续（凌晨 4 点）
openclaw cron add \
  --name "overnight-4am" \
  --cron "0 4 * * *" \
  --message "继续处理 Todo.md。更新进度日志。"

# 晨间简报（凌晨 6 点）
openclaw cron add \
  --name "overnight-6am" \
  --cron "0 6 * * *" \
  --message "最终检查。总结所有隔夜工作。"

# 列出定时任务
openclaw cron list
```

---

## Usage Guide / 使用指南

### Basic Workflow / 基本工作流程

**English**:

1. **Assign a task** at any time
2. **Agent decomposes** it into subtasks in Todo.md
3. **Agent executes** following execution-discipline.md
4. **Agent discovers** new tasks and adds them to Todo.md
5. **Cron jobs wake** agent to continue work overnight
6. **Wake up to** a complete morning briefing

**中文**:

1. **随时分配任务**
2. **代理将其分解**为 Todo.md 中的子任务
3. **代理执行**遵循 execution-discipline.md
4. **代理发现**新任务并将其添加到 Todo.md
5. **定时任务唤醒**代理继续隔夜工作
6. **醒来后查看**完整的晨间简报

---

### Example: Overnight Work / 示例：隔夜工作

**English**:

```
10:00 PM - You assign: "Add user authentication"
10:01 PM - Agent decomposes into 6 subtasks
10:05 PM - Agent begins work

2:00 AM - Cron wakes agent
2:01 AM - Agent resumes work, completes 2 tasks

4:00 AM - Cron wakes agent
4:01 AM - Agent continues, completes 2 more tasks

6:00 AM - Cron wakes agent
6:30 AM - All tasks complete, morning briefing generated

8:00 AM - You wake to complete authentication system
```

**中文**:

```
晚上 10:00 - 您分配任务："添加用户认证"
晚上 10:01 - 代理将其分解为 6 个子任务
晚上 10:05 - 代理开始工作

凌晨 2:00 - 定时任务唤醒代理
凌晨 2:01 - 代理恢复工作，完成 2 个任务

凌晨 4:00 - 定时任务唤醒代理
凌晨 4:01 - 代理继续，再完成 2 个任务

凌晨 6:00 - 定时任务唤醒代理
凌晨 6:30 - 所有任务完成，晨间简报已生成

早上 8:00 - 您醒来看到完整的认证系统
```

---

### Verifying Operation / 验证运行

**English**:

```bash
# Check skills are loaded
openclaw skills list

# Check progress log
cat ~/.openclaw/workspace/progress-log.md

# Check task list
cat ~/.openclaw/workspace/Todo.md

# Review overnight work
openclaw progress overnight
```

**中文**:

```bash
# 检查技能是否已加载
openclaw skills list

# 检查进度日志
cat ~/.openclaw/workspace/progress-log.md

# 检查任务列表
cat ~/.openclaw/workspace/Todo.md

# 查看隔夜工作
openclaw progress overnight
```

---

## Best Practices / 最佳实践

### DO ✅ / 应该做

**English**:

1. **Start with core skills first** - Add operational skills gradually
2. **Test before trust** - Verify with simple tasks first
3. **Monitor overnight runs** - Check logs for first few nights
4. **Update memory regularly** - Keep MEMORY.md and LESSONS.md current
5. **Review costs weekly** - Optimize based on usage patterns

**中文**:

1. **首先从核心技能开始** - 逐步添加运维技能
2. **测试后再信任** - 首先用简单任务验证
3. **监控隔夜运行** - 前几天检查日志
4. **定期更新记忆** - 保持 MEMORY.md 和 LESSONS.md 最新
5. **每周审查成本** - 根据使用模式优化

---

### DON'T ❌ / 不应该做

**English**:

1. **Don't install all skills at once** - Add incrementally
2. **Don't skip workspace setup** - Templates are essential
3. **Don't ignore escalations** - Agent needs your input
4. **Don't forget security** - Run regular audits
5. **Don't set and forget** - Monitor and adjust

**中文**:

1. **不要一次安装所有技能** - 逐步添加
2. **不要跳过工作区设置** - 模板至关重要
3. **不要忽略升级请求** - 代理需要您的输入
4. **不要忘记安全** - 定期运行审计
5. **不要设置后就忘记** - 监控和调整

---

## FAQ / 常见问题

### Q: How much can I save on costs? / 成本能节省多少？

**English**: Users typically see 60-80% cost reduction through intelligent model routing alone. Additional savings come from reduced looping and better context management.

**中文**: 仅通过智能模型路由，用户通常可以看到 60-80% 的成本降低。额外节省来自减少的循环和更好的上下文管理。

---

### Q: Will this work with any project? / 这适用于任何项目吗？

**English**: Yes, these skills are project-agnostic. They provide meta-patterns for how the agent should work, regardless of your specific tech stack.

**中文**: 是的，这些技能与项目无关。它们提供了代理应如何工作的元模式，无论您的具体技术栈如何。

---

### Q: How do I know the agent is working overnight? / 我怎么知道代理在隔夜工作？

**English**: Check `progress-log.md` in the morning. Each cycle is logged with timestamps, test results, and decisions. The morning briefing summarizes all overnight activity.

**中文**: 早上检查 `progress-log.md`。每个循环都记录有时间戳、测试结果和决策。晨间简报总结了所有隔夜活动。

---

### Q: What if the agent makes a mistake? / 如果代理犯了错误怎么办？

**English**: The execution-discipline skill requires testing before marking anything complete. Errors are logged in LESSONS.md to prevent recurrence. You can always review and revert changes.

**中文**: execution-discipline 技能要求在标记任何内容完成之前进行测试。错误记录在 LESSONS.md 中以防止再次发生。您可以随时审查和恢复更改。

---

### Q: Can I customize the skills? / 我可以自定义技能吗？

**English**: Absolutely! These are starting points. Edit them to match your preferences, tech stack, and working style. Your customizations are preserved in your workspace.

**中文**: 当然可以！这些只是起点。编辑它们以匹配您的偏好、技术栈和工作风格。您的自定义将保存在您的工作区中。

---

## Support & Community / 支持与社区

**English**:

- **Author**: Eric Jie <jxmerich@mail.com>
- **GitHub**: https://github.com/Erich1566/openclaw-ops-skills
- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share experiences
- **Documentation**: See README.md for detailed guides

**中文**:

- **作者**: Eric Jie <jxmerich@mail.com>
- **GitHub**: https://github.com/Erich1566/openclaw-ops-skills
- **Issues**: 报告错误和请求功能
- **Discussions**: 提出问题并分享经验
- **文档**: 详见 README.md 获取详细指南

---

## License / 许可证

**English**: MIT License - Free to use, modify, and distribute.

**中文**: MIT 许可证 - 可自由使用、修改和分发。

---

## Author / 作者

**Eric Jie** <jxmerich@mail.com>

---

## Summary / 总结

### English

The OpenClaw Ops Skills Pack transforms autonomous agent operations from experimental to production-ready. By implementing these 14 skills, you gain:

- 80% cost reduction through optimized model routing
- True autonomy with self-expanding task lists
- Persistent memory across sessions
- Complete visibility into overnight work
- Security hardening and error recovery
- Professional-grade execution discipline

Your agent will work while you sleep, leaving you with completed tasks, comprehensive logs, and a morning briefing of what was accomplished.

### 中文

OpenClaw 运维技能包将自主代理操作从实验性转变为生产就绪。通过实施这 14 个技能，您将获得：

- 通过优化的模型路由实现 80% 的成本降低
- 具有自我扩展任务列表的真正自主性
- 跨会话的持久记忆
- 对隔夜工作的完全可见性
- 安全加固和错误恢复
- 专业级的执行纪律

您的代理将在您睡眠时工作，为您留下已完成的任务、全面的日志以及关于已完成工作的晨间简报。

---

**Ready to transform your agent? / 准备好转变您的代理了吗？**

**Start with QUICKSTART.md for a 15-minute setup! / 从 QUICKSTART.md 开始，15 分钟即可完成设置！**

**Let's build something amazing while you sleep. / 让我们在您睡眠时构建令人惊叹的东西。** 🚀
