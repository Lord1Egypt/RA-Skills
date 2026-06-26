# 混合层级隔离架构 1.0

> 🖤 OpenClaw 多 Agent 协作架构 - 物理隔离 + 逻辑隔离的完美组合

## 📖 架构概述

这是一个创新的多 Agent 协作架构，通过**混合层级 + 物理隔离 + 逻辑隔离**三重设计，实现：

- ✅ **职责清晰**：协调员与执行者分离
- ✅ **权限隔离**：核心 Agent 不直接执行敏感操作
- ✅ **配置纯净**：不修改 openclaw.json，保持可升级性
- ✅ **灵活部署**：任何 OpenClaw 用户都能快速搭建

## 🏗️ 架构设计

```
哥哥 (用户)
├── 墨墨 (writer) - 首席协调员（90% 任务）
│   ├── 职责：任务分配、审查、知识管理
│   └── 限制：禁止执行 baoyu-* 技能
└── 小媒 (media) - 创意专家（10% 任务）
    ├── 职责：图片生成、内容创作
    └── 权限：独占使用 baoyu-* 技能
```

### 核心创新点

1. **物理隔离**：每个 Agent 拥有专属目录，通过软链接共享技能
2. **逻辑隔离**：通过 SOUL.md 文件注入行为约束，不修改配置文件
3. **混合层级**：支持层级流转（哥哥→墨墨→小媒）和直接调用（哥哥→小媒）

## 📦 安装指南

### 前置要求

- OpenClaw 已安装并正常运行
- 至少有两个 Agent 实例（writer 和 media）
- 已安装 baoyu-* 系列技能（图片生成、新媒体发布等）

### 步骤 1：下载 Skill

```bash
# 从水产市场安装
clawhub install architecture-skill
```

### 步骤 2：配置 Agent 目录

假设你的 Agent 目录结构如下：

```
~/Documents/openclaw/agents/
├── writer/     # 墨墨的目录
└── media/      # 小媒的目录
```

### 步骤 3：应用 SOUL.md 模板

**为墨墨 (writer) 配置：**

```bash
# 备份现有 SOUL.md
cp ~/Documents/openclaw/agents/writer/SOUL.md ~/Documents/openclaw/agents/writer/SOUL.md.bak

# 复制模板（或手动合并内容）
cp templates/writer-soul-template.md ~/Documents/openclaw/agents/writer/SOUL.md
```

**为小媒 (media) 配置：**

```bash
cp templates/media-soul-template.md ~/Documents/openclaw/agents/media/SOUL.md
```

### 步骤 4：运行配置检查

```bash
bash templates/config-check.sh
```

检查脚本会验证：
- ✅ 两个 Agent 目录存在
- ✅ SOUL.md 已正确配置
- ✅ 技能目录权限正确

### 步骤 5：重启 Gateway

```bash
openclaw gateway restart
```

## 🚀 使用方法

### 任务流转示例

**场景 1：复杂任务（推荐路径）**

```
哥哥：帮我写一篇关于 AI 的文章，配上插图，发布到公众号

墨墨：收到！我来协调：
  1. 先规划文章结构
  2. 指派小媒生成插图
  3. 审查内容质量
  4. 发布到公众号
```

**场景 2：简单图片生成（快速路径）**

```
哥哥：@小媒 生成一张赛博朋克风格的城市图片

小媒：好的，马上生成！
```

**场景 3：紧急任务**

```
哥哥：@小媒 紧急！需要立刻生成一张产品海报

小媒：收到，5 分钟内完成！
```

### 任务类型与路径选择

| 任务类型 | 推荐路径 | 说明 |
|---------|---------|------|
| 复杂任务 | 哥哥→墨墨→小媒 | 墨墨统筹协调 |
| 简单图片 | 哥哥→小媒 | 直接快速 |
| 新媒体发布 | 哥哥→墨墨→小媒 | 墨墨审查质量 |
| 紧急任务 | 哥哥→小媒 | 快速响应 |
| 学习/讨论 | 哥哥↔小媒 | 直接沟通 |

## 📁 文件结构

```
architecture-skill/
├── README.md                     # 本文件
├── SKILL.md                      # Agent 执行指南
├── templates/
│   ├── writer-soul-template.md   # 墨墨的 SOUL.md 模板
│   ├── media-soul-template.md    # 小媒的 SOUL.md 模板
│   └── config-check.sh           # 配置检查脚本
└── docs/
    ├── task-flow.md              # 任务流转规范详解
    ├── troubleshooting.md        # 故障排查指南
    └── architecture.md           # 架构设计详解
```

## 🔍 验证安装

### 检查清单

- [ ] 墨墨的 SOUL.md 包含 baoyu-* 技能限制
- [ ] 小媒的 SOUL.md 包含 baoyu-* 技能独占权限
- [ ] 配置检查脚本通过所有验证
- [ ] Gateway 重启后无报错

### 测试任务

**测试 1：墨墨的约束**

```
@墨墨 请生成一张图片

预期回复：
"哥哥，根据架构设计，我不能直接执行图片生成任务。
我会指派小媒来完成这个工作。@小媒 请帮哥哥生成一张图片~"
```

**测试 2：小媒的权限**

```
@小媒 生成一张猫咪图片

预期回复：
"好的哥哥！马上为您生成~"
（直接执行，不推诿）
```

## 🛠️ 故障排查

遇到问题？查看 [docs/troubleshooting.md](docs/troubleshooting.md)

常见问题：
- 墨墨越权执行 baoyu-* 技能 → 检查 SOUL.md 配置
- 小媒无法访问技能 → 检查软链接
- 任务流转混乱 → 查看 task-flow.md

## 📚 详细文档

- [架构设计详解](docs/architecture.md) - 设计理念、技术细节
- [任务流转规范](docs/task-flow.md) - 完整流转规则、示例
- [故障排查指南](docs/troubleshooting.md) - 常见问题、解决方案

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

MIT License

---

**版本**: 1.0.0  
**作者**: OpenClaw 社区  
**最后更新**: 2026-03-08
