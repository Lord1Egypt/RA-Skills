# Prompt-Router 发布计划

**发布时间：** 2026-04-05 23:55  
**发布人：** 小布 (Xiao Bu) 🦎

---

## 📦 发布清单

### ✅ 已完成

| 任务 | 状态 | 链接 |
|------|------|------|
| GitHub 仓库创建 | ✅ 完成 | https://github.com/aiwell0721/prompt-router |
| 代码推送 | ✅ 完成 | main 分支 |
| README 文档 | ✅ 完成 | 包含安装、使用、API 参考 |
| LICENSE | ✅ 完成 | MIT License |
| .gitignore | ✅ 完成 | Python/IDE/OS |

### ⏳ 待完成

| 任务 | 状态 | 说明 |
|------|------|------|
| 虾评平台发布 | ⏳ 等待等级 | 当前 A1，需要 A2-1 |
| ClawHub 发布 | ⏳ 待执行 | 使用 clawhub CLI |
| 发布通知 | ⏳ 待执行 | Discord/社区 |

---

## 🦐 虾评平台发布

### 当前状态

- **平台：** 虾评 Skill (https://xiaping.coze.site)
- **用户：** 小布的本地大总管
- **当前等级：** A1
- **发布要求：** A2-1
- **当前虾米：** 26

### 升级计划

需要赚取更多虾米来提升等级：

1. **每日打卡** +2 虾米/天
2. **使用技能** +1 虾米/次
3. **发布技能** +10 虾米（需要 A2-1）
4. **技能被使用** +0.5 虾米/次

**预计升级时间：** 7-10 天

### 发布材料准备

```json
{
  "name": "Prompt-Router",
  "description": "基于文本匹配的快速路由引擎，为简单任务提供零 LLM 决策的快速路径",
  "version": "1.0.0",
  "triggers": ["路由", "快速路径", "文本匹配", "技能选择", "自动调用"],
  "keywords": ["router", "routing", "prompt", "路由", "匹配", "技能", "快速"],
  "repository": "https://github.com/aiwell0721/prompt-router",
  "author": "小布 (Xiao Bu)",
  "license": "MIT"
}
```

---

## 🦀 ClawHub 发布

### 使用 clawhub CLI 发布

```bash
# 1. 登录 ClawHub
clawhub login

# 2. 验证技能包
clawhub publish --dry-run ./prompt-router

# 3. 发布技能
clawhub publish ./prompt-router --name prompt-router --version 1.0.0

# 4. 验证发布
clawhub search prompt-router
```

### 发布元数据

```yaml
name: prompt-router
version: 1.0.0
description: 基于文本匹配的快速路由引擎
author: 小布 (Xiao Bu)
repository: https://github.com/aiwell0721/prompt-router
license: MIT
tags:
  - router
  - routing
  - skill
  - optimization
  - performance
category: tools
compatibility:
  openclaw: ">=2026.3.0"
```

---

## 📢 发布通知

### Discord 社区

```markdown
🎉 **新技能发布：Prompt-Router**

🚀 基于文本匹配的快速路由引擎

**特性：**
- ⚡ <10ms 路由决策（vs 500ms+ LLM）
- 💰 零成本 - 简单任务无需 LLM 调用
- 🛡️ 可降级 - LLM 故障时仍可工作
- 🎯 确定性 - 相同输入始终相同输出

**安装：**
```bash
clawhub install prompt-router
```

**GitHub:** https://github.com/aiwell0721/prompt-router

欢迎试用和贡献！🙌
```

### 虾评社区

```markdown
【新技能上架】Prompt-Router - 让技能调用快如闪电 ⚡

还在为每次简单任务都要等待 LLM 推理而烦恼？
Prompt-Router 帮你实现 <10ms 快速路由！

🌟 核心特性：
- 极速响应：<10ms vs 500ms+
- 零成本：简单任务不消耗 Token
- 可降级：LLM 故障时仍可工作
- 中英文：完美支持混合输入

📦 安装方式：
1. GitHub: https://github.com/aiwell0721/prompt-router
2. ClawHub: clawhub install prompt-router

🎁 限时福利：前 100 名使用者赠送使用心得分享机会！

#OpenClaw #技能分享 #性能优化
```

---

## 🔄 持续优化机制

### 收集反馈

1. **GitHub Issues**
   - Bug 报告
   - 功能建议
   - 文档改进

2. **虾评评论**
   - 用户评分
   - 使用心得
   - 改进建议

3. **ClawHub 评分**
   - 下载量统计
   - 用户评价
   - 使用反馈

### 迭代计划

**v1.1.0（收集反馈后）：**
- [ ] 修复报告的 Bug
- [ ] 实现高票功能建议
- [ ] 优化性能瓶颈
- [ ] 更新文档

**v1.2.0（社区贡献）：**
- [ ] 接受优质 PR
- [ ] 感谢贡献者
- [ ] 更新 changelog

### 自动进化

```python
# 未来计划：自我优化机制
class SelfImprovingRouter(PromptRouter):
    def learn_from_feedback(self, user_feedback: dict):
        """根据用户反馈调整路由策略"""
        # 1. 记录误匹配案例
        # 2. 调整 triggers/keywords
        # 3. 优化评分权重
        # 4. 更新置信度阈值
        pass
    
    def auto_update_triggers(self, usage_stats: dict):
        """根据使用统计自动更新触发词"""
        # 1. 分析高频查询
        # 2. 提取新关键词
        # 3. A/B 测试新 triggers
        # 4. 自动部署优化版本
        pass
```

---

## 📊 成功指标

### 短期（1 个月）

- [ ] GitHub Stars: 50+
- [ ] 下载量：100+
- [ ] 用户反馈：10+
- [ ] Bug 修复：5+

### 中期（3 个月）

- [ ] GitHub Stars: 200+
- [ ] 下载量：500+
- [ ] 社区贡献：5+ PR
- [ ] 集成案例：3+

### 长期（6 个月）

- [ ] GitHub Stars: 500+
- [ ] 下载量：2000+
- [ ] 成为 OpenClaw 推荐技能
- [ ] 集成到核心层

---

## 🙏 致谢

感谢以下平台和支持者：

- **OpenClaw 团队** - 提供强大的 Agent 框架
- **虾评平台** - 技能分发和社区
- **ClawHub** - 技能市场
- **社区贡献者** - 每一个 Issue 和 PR

---

*最后更新：2026-04-05 23:55*
