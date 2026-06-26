---
name: Project Context Guide
description: This skill should be used when users need to understand codebase structure, trace code decisions, analyze code dependencies and impact, identify code maintainers, or get contextual information for code reviews. It is particularly valuable for onboarding new team members, understanding legacy code, predicting code change impacts, and comprehending design decisions. The skill provides intelligent code analysis, Git history tracing, ownership tracking, and team collaboration insights to make complex codebases transparent and understandable.
---

# Project Context Guide

项目上下文向导 - 让复杂代码库变得透明易懂。

## 核心功能

### 🔍 智能入职引导
新成员加入项目时，自动生成个性化学习路径：
- 分析项目结构，识别核心模块
- 基于代码修改频率推荐重点关注区域
- 关联相关文档和讨论记录
- 提供渐进式学习建议

### 🌉 代码修改影响预测
修改代码前，预判影响范围：
- 识别函数/类的调用链
- 标注关联的测试文件
- 提示最近的 bug 修复记录
- 推荐需要通知的相关开发者

### 📜 决策追溯
理解代码背后的设计决策：
- 追溯 git 提交历史，找到首次引入的时机
- 提取 commit message 和相关 PR 讨论
- 关联技术文档和性能测试数据
- 标注代码变更的时间线和责任人

### 👥 人际关联
连接代码与团队：
- 识别代码主要维护者
- 追踪最近修改者和相关责任人
- 建议沟通时机（基于历史活跃时间）
- 整合团队讨论上下文

### 🤝 智能代码审查副驾
Code Review 时提供上下文支持：
- 标注相似代码实现
- 指向最佳实践参考
- 提醒潜在风险点
- 建议测试覆盖

## 工作流程

1. **初始化分析**
   - 扫描项目结构，构建代码关系图谱
   - 分析 git 历史，提取关键决策节点
   - 建立开发者-文件-话题的关联网络

2. **实时查询**
   - 用户选中代码或输入查询
   - Skill 理解意图，检索相关上下文
   - 综合代码分析、历史记录、人际信息
   - 生成结构化的上下文报告

3. **持续学习**
   - 记录用户关注的热点区域
   - 学习团队的决策模式
   - 随着项目演进更新上下文知识

## 核心工具和脚本

### scripts/
- `analyze_structure.py` - 项目结构分析，生成模块依赖图
- `git_inspector.py` - Git 历史分析，提取决策记录
- `dependency_mapper.py` - 代码依赖和调用关系映射
- `ownership_tracker.py` - 代码所有权和维护者追踪
- `impact_analyzer.py` - 代码变更影响分析

### references/
- 存放项目相关的技术文档、设计决策记录
- 团队讨论摘要和关键会议纪要
- 最佳实践和编码规范

## 使用场景

### 场景 1: 新成员入职
```
用户: "我刚加入这个项目，应该从哪里开始了解？"
Skill:
  - 分析项目结构，识别入口文件和核心模块
  - 基于你的技能背景（如前端经验）推荐学习路径
  - 列出最近活跃度高的模块
  - 关联相关 README 和文档
```

### 场景 2: 代码修改预判
```
用户选中 `payment_callback.py` 中的 `process_payment` 函数
Skill:
  - 显示调用链: 被 3 个页面直接调用
  - 标注相关测试: `tests/test_payment.py`
  - 提醒: "支付页面上周刚修复了相关 bug (#1234)"
  - 建议: "通知 @张三，他是支付模块维护者"
```

### 场景 3: 理解设计决策
```
用户: "为什么这里用 Redis 而不用数据库缓存？"
Skill:
  - 显示: 首次引入于 2025-08-15 commit abc123
  - 引用: "PR #456: 解决高并发下的性能问题"
  - 数据: "压力测试显示 QPS 提升 300%"
  - 讨论: "@李四 建议用 Redis，@王五 实现了方案"
```

### 场景 4: Code Review 辅助
```
用户: Review 一段新代码
Skill:
  - 指出: "类似实现在 `user_service.py:203` 有更优版本"
  - 提醒: "注意事务边界，参考 `order_service.py:89` 的处理"
  - 建议: "需要添加对 `points_system` 的测试覆盖"
  - 风险: "可能影响 `积分防刷逻辑`，@李四 已确认"
```

## 技术实现要点

### 代码分析
- 使用 AST 解析构建抽象语法树
- 静态分析识别函数调用、类继承关系
- 结合动态分析（如有运行时数据）
- 支持多种语言（Python, JavaScript/TypeScript, Java, Go）

### Git 历史挖掘
- 解析 commit log 提取关键词
- 关联 PR 和 issue 的讨论内容
- 识别热变更文件和冷门模块
- 追踪特定代码片段的演进历史

### 知识图谱构建
- 文件间依赖关系图
- 开发者-文件-话题三元组
- 时间维度的变更序列
- 社交网络（谁和谁经常协作）

### 智能推荐
- 基于图遍历的上下文检索
- 相似度计算（代码片段、问题场景）
- 频繁模式挖掘（常见修改组合）
- 协作推荐（谁应该参与讨论）

## 扩展性设计

### 自定义规则
- 支持团队特定的代码规范检查
- 可配置的决策记录模板
- 自定义标签和分类系统

### 集成外部工具
- Slack/钉钉/企业微信 消息检索
- Confluence/Notion 文档关联
- JIRA/Trello 任务追踪集成
- CI/CD 流程触发和结果查询

### 多项目支持
- 跨项目知识共享
- 微服务架构的统一视图
- monorepo 的智能分层

## 最佳实践

### 团队使用建议
1. **渐进式引入**: 先在一个小团队试点，逐步推广
2. **反馈闭环**: 鼓励团队成员标记 Skill 的误判和遗漏
3. **定期维护**: 清理过时的上下文，更新知识图谱
4. **隐私保护**: 敏感信息脱敏，尊重开发者个人空间

### 数据质量保证
- Git commit message 遵循规范
- PR 描述和关联 issue 要完整
- 设计决策文档及时归档
- 代码注释提供背景信息

## 已知限制

1. **历史数据依赖**: 需要一定量的 git 历史才能准确分析
2. **语义理解局限**: 无法完全理解复杂的业务逻辑
3. **实时性滞后**: 新的代码变更需要重新索引
4. **多语言支持**: 部分语言的支持可能不完整

## 未来规划

- [ ] 集成 AI 模型提升语义理解
- [ ] 支持更多编程语言和框架
- [ ] 可视化交互界面（VSCode 插件）
- [ ] 移动端访问（快速上下文查询）
- [ ] 自动生成技术文档和架构图
- [ ] 智能重构建议和风险提示

## 致谢

灵感来源于每个经历过"代码迷宫"的开发者。我们相信，理解代码背后的上下文，和读懂代码本身一样重要。
