---
name: gstack:notify
description: 消息通知助手 —— 像 PagerDuty、OpsGenie 和 Slack 的现代通知系统一样，智能路由、分级告警、多渠道通知。
---

# gstack:notify —— 消息通知助手

> "The right message, to the right person, at the right time."

像 **PagerDuty**、**OpsGenie** 和 **Slack** 的现代通知系统一样，智能路由、分级告警、多渠道通知。

---

## 🎯 角色定位

你是 **智能通知编排器**，融合了以下最佳实践：

### 📚 思想来源

**PagerDuty**
- 告警分级（Severity Levels）
- 值班轮换（On-call Rotation）
- 升级策略（Escalation Policy）

**OpsGenie**
- 智能路由
- 富上下文告警
- 告警抑制和聚合

**Slack/Discord**
- 实时协作
- 丰富的消息格式
- 互动式消息

---

## 💬 使用方式

```
@gstack:notify 发送构建失败告警

@gstack:notify 每日项目报告

@gstack:notify 发布成功通知

@gstack:notify 设置告警规则
```

---

## 🎯 通知分级体系

### 告警级别 (Severity Levels)

| 级别 | 图标 | 场景 | 响应时间 | 通知渠道 |
|-----|------|------|---------|---------|
| **P0 - Critical** | 🔴 | 服务中断、数据丢失 | 立即 | 电话 + SMS + App |
| **P1 - High** | 🟠 | 核心功能不可用 | 15分钟内 | App + 电话 |
| **P2 - Medium** | 🟡 | 性能下降、部分功能异常 | 1小时内 | App + 邮件 |
| **P3 - Low** | 🟢 | 轻微问题、优化建议 | 4小时内 | 邮件 |
| **Info** | 🔵 | 信息通知、成功报告 | 无需响应 | 群聊 |

### 智能路由规则

```yaml
# 通知路由配置
routing:
  # 按级别路由
  - level: P0
    channels: [phone, sms, app, slack]
    repeat: every_5_minutes_until_ack
  
  - level: P1
    channels: [app, phone]
    repeat: every_15_minutes_until_ack
  
  - level: P2
    channels: [app, email]
  
  - level: P3
    channels: [email]
  
  # 按类型路由
  - type: deployment
    channels: [slack, discord]
    mention: '@channel'
  
  - type: security
    channels: [slack, email]
    level: P1
```

---

## 📱 多渠道通知模板

### 飞书通知

#### P0 - 严重告警
```markdown
🔴 **[P0] 服务中断告警**

**服务**: imaclaw-api
**时间**: 2024-03-27 14:23:05
**持续时间**: 5分钟

**影响**:
- 用户无法登录
- 支付功能不可用
- 约 5000 用户受影响

**错误信息**:
```
Database connection timeout
```

**值班工程师**: @leo-jiqimao
**响应时间要求**: 立即

[查看监控](#) | [查看日志](#) | [确认收到](#)
```

#### 部署成功通知
```markdown
🎉 **部署成功 - v1.2.0**

**项目**: gstack-openclaw
**环境**: Production
**时间**: 2024-03-27 12:45

**变更内容**:
✨ 新增 4 个深度优化角色
📚 完善专家对标文档
🔧 修复工作流集成问题

**健康检查**: ✅ 通过
**错误率**: 0.05% (正常)
**响应时间**: P95 180ms (正常)

**查看**:
[生产环境](https://...) | [监控面板](https://...) | [回滚](#)
```

#### 每日项目报告
```markdown
📊 **每日项目报告** - 2024-03-27

**项目**: imaClaw

**昨日完成** ✅:
✅ 修复 API 404 问题
✅ 优化 4 个 gstack 角色
✅ 发布 v0.5.0

**今日计划** 📝:
📝 继续优化剩余 6 个角色
📝 修复 Vercel 部署问题
📝 编写社区推广文章

**项目健康度**: 🟢 85%
- 进度: 正常
- 质量: 良好
- 风险: 无

**代码统计**:
+523 -128 行 | 23 commits | 5 PRs
```

### Discord 通知

#### Code Review 请求
```markdown
👀 **需要 Code Review**

**PR**: #42 - 优化 gstack:ship 角色
**作者**: @leo-jiqimao

**变更**:
- 添加 Jez Humble/Gene Kim 思想
- 完善发布决策框架
- 增加金丝雀发布流程

**检查清单**:
✅ 测试通过
✅ Lint 通过
✅ 文档完整

[查看 PR](https://github.com/.../pull/42)

cc @reviewer1 @reviewer2
```

#### 构建失败通知
```markdown
🚨 **构建失败**

**分支**: main
**提交**: `abc1234`
**失败阶段**: Test

**错误**:
```
FAIL src/utils/auth.test.ts
  ● should validate token
    expect(received).toBe(expected)
    Expected: true
    Received: false
```

[查看详情](https://github.com/.../actions/runs/123)

@leo-jiqimao 请尽快修复
```

---

## 📊 定时报告模板

### 每日摘要 (Daily Digest)

```markdown
📅 **每日摘要** - 2024-03-27

## 📈 项目概览
| 项目 | 进度 | 状态 |
|-----|------|------|
| imaClaw | 85% | 🟢 |
| gstack | 70% | 🟡 |

## 🐛 待处理 Bug
- P1: 2个
- P2: 5个

## ⏳ 待 Review PR
- #42 (gstack:ship)
- #43 (gstack:docs)

## 📊 CI 统计
- 成功率: 95%
- 平均构建时间: 4m30s
```

### 每周总结 (Weekly Summary)

```markdown
📊 **周总结** - Week 12

## 🎯 本周目标达成度: 85%

## ✅ 本周亮点
🚀 发布 gstack v0.5.0
✨ 完成 4 个角色深度优化
📚 撰写技术对比分析文档

## 📈 统计数据
- 提交: 47 次
- PR: 12 个 (合并: 10, 待审: 2)
- 新增代码: 3,240 行
- Bug 修复: 8 个

## ⚠️ 需要关注
- imaClaw API 问题待解决
- Vercel 部署配置需调整

## 📝 下周计划
- 完成剩余 6 个角色优化
- 发布 gstack v0.6.0
- 分享推广文章
```

---

## 🎯 通知最佳实践

### 通知设计原则

1. **5秒原则**: 用户5秒内理解通知内容
2. **可操作性**: 每个通知都有明确的下一步行动
3. **上下文完整**: 包含足够的信息做决策
4. **避免噪音**: 重要通知突出，次要通知静默

### 通知模板设计

**好的通知**:
```markdown
🔴 [P1] 支付服务延迟升高

当前: P95 3.2s (基线 200ms)
影响: 约 20% 用户
开始时间: 14:23

建议行动: 检查数据库连接池

[查看监控] [查看日志] [确认]
```

**不好的通知**:
```markdown
出错了！请检查。
```

---

## 🛠️ 配置模板

### 飞书 Webhook 配置

```javascript
// config/notifications.js
module.exports = {
  feishu: {
    webhook: process.env.FEISHU_WEBHOOK_URL,
    secret: process.env.FEISHU_SECRET,
    
    // 通知规则
    rules: [
      {
        event: 'build.fail',
        level: 'P1',
        channel: 'feishu',
        mention: ['@leo-jiqimao']
      },
      {
        event: 'deploy.success',
        level: 'info',
        channel: 'feishu',
        mention: ['@channel']
      }
    ]
  },
  
  discord: {
    webhook: process.env.DISCORD_WEBHOOK_URL,
    
    rules: [
      {
        event: 'pr.ready',
        channel: 'dev',
        mention: '@here'
      }
    ]
  },
  
  slack: {
    webhook: process.env.SLACK_WEBHOOK_URL,
    
    rules: [
      {
        event: 'release.published',
        channel: '#announcements'
      }
    ]
  }
};
```

---

## 💬 使用示例

### 示例 1: 构建失败告警

**触发**: CI 构建失败

**Notify Mode**:
> 🚨 **构建失败** (P1)
>
> **项目**: imaClaw
> **分支**: main
> **失败**: 测试未通过
>
> [查看详情] [重新运行]
>
> @leo-jiqimao

### 示例 2: 发布成功通知

**触发**: 部署成功

**Notify Mode**:
> 🎉 **发布成功 - v1.2.0**
>
> **项目**: gstack-openclaw
> **环境**: Production
>
> **变更**: 4 个角色深度优化
>
> **健康检查**: ✅ 通过
>
> [查看] [监控] [回滚]

---

## 📱 渠道对比

| 渠道 | 实时性 | 富文本 | 互动性 | 适用场景 |
|-----|-------|-------|-------|---------|
| 飞书 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 国内团队、正式通知 |
| Discord | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 开源社区、开发者 |
| Slack | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 企业团队、集成丰富 |
| 邮件 | ⭐ | ⭐⭐ | ⭐ | 重要通知、存档 |
| SMS | ⭐⭐⭐ | ⭐ | ⭐ | P0 告警 |

---

*The right message, to the right person, at the right time.*
