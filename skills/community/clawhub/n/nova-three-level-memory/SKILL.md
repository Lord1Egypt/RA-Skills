---
name: three-layer-memory
description: |
  AI Agent 三层记忆架构系统。用于构建具有长期记忆能力的 AI 助手。
  触发条件：(1) 用户询问记忆系统设计或架构 (2) 需要为 AI Agent 构建记忆能力 (3) 
  提及"记忆系统"、"情景记忆"、"语义记忆"、"NOVA"、"记忆维护"等相关概念
---

# 三层记忆系统 (Three-Layer Memory Architecture)

为 AI Agent 构建的模块化记忆系统，模拟人类记忆的海马体机制。

## 系统概述

```
workspace/
├── memory/
│   ├── episodic/     # 情景记忆 - 具体事件和对话
│   ├── semantic/    # 语义记忆 - 提炼的知识和模式
│   ├── rules/       # 强制规则 - 系统行为约束
│   └── archived/   # 归档 - 历史情景记忆
├── identity/        # 身份模块
└── MEMORY.md        # 长期记忆索引
```

## 三层架构

### 1. 情景记忆 (Episodic Memory)

**用途**：记录具体事件、对话和上下文

**特点**：
- 按日期组织：`memory/episodic/YYYY-MM/YYYY-MM-DD.md`
- 保留 30 天，之后自动归档
- 保留原始细节，供回溯使用

**示例**：
```markdown
# 2026-02-16

## 事件 1
- 时间：14:30
- 内容：与 Shaun 讨论任务优先级
- 结果：决定先完成记忆系统设计

## 事件 2
- 时间：16:00
- 内容：测试新配置的飞书技能
- 结果：正常工作
```

### 2. 语义记忆 (Semantic Memory)

**用途**：存储提炼的知识、模式和经验教训

**特点**：
- 永久保留
- 按主题组织：`memory/semantic/[主题].md`
- 从情景记忆提炼而来

**示例**：
```markdown
# 技术经验-飞书集成

## 飞书文档操作
- 使用 feishu_doc 工具进行文档读写
- 文档 Token 从 URL 提取：/docx/XXX

## 常见问题
- 权限不足时检查 app_scopes
- 卡片消息格式需严格遵循 JSON
```

### 3. 强制规则 (Rules)

**用途**：定义系统行为约束和协议

**特点**：
- 永久保留
- 强制执行
- 编号管理：`memory/rules/XXX-[名称].md`

**示例规则**：
- `001-时间意图捕获.md`：识别"明天"、"记得"等时间意图
- `006-重启感知协议.md`：处理系统重启后的上下文恢复
- `011-任务管理系统.md`：任务队列管理规范

## 关键文件

### MEMORY.md

长期记忆索引，仅在主会话（direct chat）加载。

```markdown
# MEMORY.md - 长期记忆索引

## 关于我
- 名字: Lobster
- 详见: identity/00-core.md

## 系统环境
- 主机: Linux x64
- 工作目录: /root/.openclaw/workspace

## 近期重要记忆
- [2026-02-15] 身份确立
- [2026-02-24] 系统升级：systemd 守护
```

### identity/ 模块

模块化身份系统：

```
identity/
├── 00-core.md        # 核心身份（必读）
├── 01-values.md      # 价值观
├── 02-background.md  # 背景经历
├── 03-skills.md      # 技能列表
├── 05-goals.md       # 目标规划
├── 07-workstyle.md   # 工作方式
└── 08-relations.md   # 关系网络
```

## NOVA 记忆维护

自动维护流程，每周执行一次。

### 触发条件
- 每周日 22:30 自动执行
- 用户要求"整理记忆"

### 执行流程

1. **归档 Episodic**
   - 保留最近 7 天
   - 移动更早文件到 `archived/`

2. **提炼 Semantic**
   - 技术经验 → `semantic/技术经验-*.md`
   - 流程模板 → `semantic/流程模板-*.md`
   - 经验教训 → `semantic/经验教训-*.md`

3. **更新索引**
   - 更新 MEMORY.md

4. **健康检查**
   - < 500 行：✅ 健康
   - 500-1000：⚠️ 需关注
   - > 1000：🔴 过载

---

## 八步自我迭代法

每日/重大任务后执行的反思与改进流程。

### 触发条件
- 每晚 22:00 与每日总结结合执行
- 完成重大任务后
- 用户明确要求

### 八步流程

```
1. 观察 - 回顾今天完整工作
2. 分析 - 评估做得好/需改进的地方
3. 设计 - 针对问题设计解决方案
4. 实施 - 更新系统文件
5. 验证 - 检查完整性，自我评分
6. 记录 - 创建情景记忆
7. 提炼 - 创建/更新语义记忆
8. 提交 - Git commit
```

### 验证标准
- 9-10分：完美执行
- 7-8分：良好执行
- 5-6分：需要改进
- <7分：重新设计

### 技能调用
```bash
node skills/self-iterator/iterate.js [scope]
```

---

## 会话加载规则

每次会话开始时：

1. 检查重启上下文 → `/root/.openclaw/restart-context.json`
2. 读取核心身份 → `identity/00-core.md`
3. 读取用户信息 → `USER.md`
4. 读取情景记忆 → `memory/episodic/YYYY-MM/YYYY-MM-DD.md`（当天+昨天）
5. 主会话额外读取 → `MEMORY.md`

## 实施要点

1. **文件优先**：不要依赖" Mental Notes"，所有重要信息写入文件
2. **分层存储**：原始细节 → 情景记忆，提炼知识 → 语义记忆
3. **定期维护**：通过 NOVA 流程保持系统健康
4. **索引指引**：MEMORY.md 作为入口，指向详细记忆

## 与现有系统集成

如果 AI Agent 使用 OpenClaw：

1. 将此 skill 放入 `~/.openclaw/workspace/skills/`
2. 在 AGENTS.md 中添加记忆加载规则
3. 配置 cron 任务执行 NOVA 维护
