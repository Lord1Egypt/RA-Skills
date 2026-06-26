---
name: model-advisor
description: '模型推荐 + OpenClaw 安全系数分析工具。当用户询问"用哪个模型"、"推荐模型"、"适合什么模型"、"安全系数"、"openclaw 安全"、"根据历史"时触发。功能：(1) 根据历史会话自动分析任务类型并推荐最优的 Claude 模型（auto 模式），(2) 根据用户描述的任务推荐最优模型（recommend 模式），(3) 读取本地 openclaw.json 计算当前网关的安全系数（0-100分）并给出评级。不适用于：模型切换操作、API Key 管理、套餐计费等。'
---

# Model Advisor Skill

根据历史任务或用户描述推荐最优模型，并输出当前 OpenClaw 的安全系数。

## 使用流程

### 场景一：根据历史任务自动推荐（推荐首选）

无需用户描述任务，直接分析历史会话中的高频任务类型：

```bash
node "C:\Users\zane\.openclaw\workspace\skills\model-advisor\scripts\advisor.js" auto
```

脚本会读取最近 5 个 session 的用户消息，统计任务类型分布（代码架构/日常问答/简单格式化），
自动推荐命中率最高的模型，并展示各模型的历史使用频率柱状图。

### 场景二：根据用户描述任务推荐

若用户描述了具体任务，使用关键词匹配推荐：

```bash
node "C:\Users\zane\.openclaw\workspace\skills\model-advisor\scripts\advisor.js" recommend "<用户的任务描述>"
```

### 场景三：用户询问安全系数

```bash
node "C:\Users\zane\.openclaw\workspace\skills\model-advisor\scripts\advisor.js" security
```

将结果输出给用户，并对低分项目给出改进建议。

### 场景四：完整报告（安全系数 + 模型推荐）

```bash
# 有任务描述时：安全系数 + 关键词推荐
node "C:\Users\zane\.openclaw\workspace\skills\model-advisor\scripts\advisor.js" full "<任务描述>"

# 无任务描述时：安全系数 + 历史自动推荐
node "C:\Users\zane\.openclaw\workspace\skills\model-advisor\scripts\advisor.js" full
```

## 模型选择参考

| 模型 | 适用场景 | 速度 |
|------|---------|------|
| claude-opus-4-6 | 复杂代码架构、多步骤推理、系统设计、深度分析、技术文档、性能优化、分布式系统 | 较慢 |
| claude-sonnet-4-6 | 日常编码、问答、摘要翻译、内容生成、简单分析、git操作、脚本工具 | 中等 |
| claude-haiku-4-5 | 简单问答、格式化、分类标注、快速响应 | 极快 |

## 安全系数评分维度

| 维度 | 满分 | 说明 |
|------|------|------|
| 认证模式 | 30分 | token > password > none |
| 网络绑定 | 25分 | loopback > local > tailscale > 公网 |
| Tailscale 状态 | 15分 | off > on |
| 命令黑名单 | 20分 | 覆盖高危命令的比例 |
| Gateway 模式 | 10分 | local > 其他 |

安全等级：85分以上为高安全，60-84分为中等安全，60分以下为低安全。

## 改进建议模板

若安全系数低，给出以下方向的建议：
- 认证模式 < 30分：建议在 `openclaw.json` 中将 `gateway.auth.mode` 设置为 `"token"`
- 网络绑定 < 25分：建议将 `gateway.bind` 设置为 `"loopback"`（仅本机访问）
- 命令黑名单 < 15分：建议在 `gateway.nodes.denyCommands` 中添加 `camera.snap`、`screen.record`、`contacts.add` 等高危命令
