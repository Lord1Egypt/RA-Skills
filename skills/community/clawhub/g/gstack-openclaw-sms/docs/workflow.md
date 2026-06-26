# gstack 完整工作流指南

> 如何像 YC 团队一样高效协作

---

## 🔄 标准开发流程

### Phase 1: 启动 (Day 1)

```
@gstack:office  # 澄清需求，对齐方向
```
**目标**: 确定要解决什么问题，为谁解决

**输出**:
- 问题定义
- 目标用户画像
- 成功标准

---

### Phase 2: 规划 (Day 1-2)

```
@gstack:ceo     # 产品规划
@gstack:eng     # 技术架构
```

**CEO 输出**:
- PRD (产品需求文档)
- 功能优先级
- MVP 范围

**Eng 输出**:
- 技术架构图
- 数据模型
- API 设计
- 技术选型

---

### Phase 3: 开发 (Day 3-5)

**编码过程中**:
```
@gstack:review  # 代码审查（每完成一个模块）
```

**关键点**:
- 小步快跑，频繁 commit
- 每个功能完成后立即 review
- 保持代码质量

---

### Phase 4: 测试 (Day 6)

```
@gstack:qa      # 设计测试用例
@gstack:browse  # 浏览器测试（如有 UI）
```

**QA 输出**:
- 测试计划
- 测试用例
- Bug 报告

---

### Phase 5: 发布 (Day 7)

```
@gstack:ship    # 发布准备
```

**Ship 输出**:
- 发布检查清单
- Changelog
- 回滚方案
- 发布后监控

---

### Phase 6: 复盘 (发布后 1 周)

```
@gstack:retro   # 项目复盘
```

**Retro 输出**:
- 做得好的
- 学到什么
- 缺少什么
- 改进计划

---

## 🎯 不同场景的工作流

### 场景 1: 快速原型 (1-2 天)

适合验证想法，快速出 Demo：

```
@gstack:office  # 快速对齐
@gstack:ceo     # 极简 PRD（1 页纸）
【开发 MVP】
@gstack:ship    # 简单检查就发
```

---

### 场景 2: 新功能开发 (1-2 周)

标准流程：

```
Day 1:  @gstack:office + @gstack:ceo
Day 2:  @gstack:eng
Day 3-8: 开发 + @gstack:review
Day 9:  @gstack:qa
Day 10: @gstack:ship
Day 17: @gstack:retro
```

---

### 场景 3: Bug 修复 (几小时到 1 天)

快速响应：

```
@gstack:office  # 快速了解问题（可选）
【修复代码】
@gstack:review  # 审查修复
@gstack:qa      # 验证修复（可选）
@gstack:ship    # 发布修复
```

---

### 场景 4: 技术重构 (1-2 周)

谨慎进行：

```
@gstack:office  # 为什么需要重构
@gstack:eng     # 重构方案
@gstack:qa      # 回归测试策略
【重构开发 + @gstack:review】
@gstack:ship    # 分阶段发布
@gstack:retro   # 重构效果评估
```

---

## 💡 使用技巧

### 1. 上下文管理

在 `GSTACK.md` 中记录项目信息，每次对话前让 AI 阅读：

```
请阅读 GSTACK.md 了解项目背景

@gstack:ceo 帮我分析一下...
```

### 2. 多角色协作

复杂问题可以让多个角色"讨论"：

```
先以 CEO 视角分析：
@gstack:ceo 这个功能的产品价值是什么？

然后以 Eng 视角分析技术可行性：
@gstack:eng 实现这个的技术方案？

最后综合判断
```

### 3. 渐进式细化

不要一次问太复杂的问题，逐步细化：

```
# 第一轮：方向
@gstack:office 这个方向对吗？

# 第二轮：范围
@gstack:ceo MVP 应该包含什么？

# 第三轮：技术
@gstack:eng 技术方案怎么设计？
```

---

## ⚠️ 常见误区

### ❌ 过度规划
不要试图一次规划完所有事情。先做 MVP，然后迭代。

### ❌ 跳过 Review
即使是小改动，也建议走一遍 review，养成好习惯。

### ❌ 忽视 Retro
复盘是进步的源泉，不要发完版就结束。

### ✅ 保持灵活
工作流是指导，不是枷锁。根据实际情况调整。

---

## 🚀 进阶用法

### 自定义技能

如果标准技能不满足需求，可以创建自己的：

```bash
# 创建新技能
mkdir ~/.openclaw/skills/gstack-custom
cat > ~/.openclaw/skills/gstack-custom/SKILL.md << 'EOF'
# gstack:custom —— 自定义技能

[你的自定义 prompt]
EOF
```

### 组合技能

把多个技能组合成工作流脚本：

```bash
#!/bin/bash
# new-feature.sh - 新功能开发工作流

echo "🚀 启动新功能开发流程"

echo "📋 Phase 1: 需求澄清"
# @gstack:office

echo "📋 Phase 2: 产品规划"
# @gstack:ceo

echo "📋 Phase 3: 技术设计"
# @gstack:eng

echo "✅ 准备就绪，可以开始开发"
```

---

## 📚 参考资源

- [Garry Tan 的 gstack](https://github.com/garrytan/gstack)
- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [ClawHub 技能商店](https://clawhub.ai)

---

*工作流是活的，不断调整和优化，找到最适合你的节奏*
