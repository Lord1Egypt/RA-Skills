# 详细参考 - infinite-memory-vault-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (bash)

```bash
mkdir -p ~/memory/projects

cat > ~/memory/projects/alpha.md << 'EOF'
- 状态：进行中
- 负责人：张三
- 截止：2026-09-01
- 技术栈：React + Node.js

- 2026-07-05：采用微服务架构
- 2026-07-12：数据库选 PostgreSQL
EOF

cat > ~/memory/projects/beta.md << 'EOF'
- 状态：暂停
- 负责人：李四
- 截止：2026-12-01
- 技术栈：Vue + Python

等待客户需求确认
EOF

cat > ~/memory/projects/INDEX.md << 'EOF'
| 名称 | 状态 | 负责人 | 截止 | 文件 |
|:---|:---|:---|:---|:---|
| Alpha | 进行中 | 张三 | 2026-09 | alpha.md |
| Beta | 暂停 | 李四 | 2026-12 | beta.md |

总计：2 条（1 进行中，1 暂停）
EOF

cat ~/memory/projects/INDEX.md
```

## 代码示例 (bash)

```bash
mkdir -p ~/memory/decisions

cat > ~/memory/decisions/2026-07-05-microservices.md << 'EOF'
2026-07-05

项目 Alpha 需要从单体架构演进。团队规模扩大到 8 人，单体架构导致部署冲突频繁。

采用微服务架构，按业务域拆分服务。

1. 微服务架构（选择）—— 扩展性好，团队独立部署
2. 单体架构 —— 简单但扩展性差
3. SOA —— 过重，不适合当前规模

- 团队规模 8 人，需要并行开发
- 部署频率高，需独立发布
- 未来有扩团队计划

- 需引入服务注册发现
- 运维复杂度提升
- 开发效率短期下降，长期提升
EOF

cat > ~/memory/decisions/INDEX.md << 'EOF'
| 日期 | 主题 | 状态 | 文件 |
|:---|:---|:---|:---|
| 2026-07-05 | 微服务架构 | 已执行 | 2026-07-05-microservices.md |

总计：1 条
EOF

cat ~/memory/decisions/2026-07-05-microservices.md
```

## 代码示例 (bash)

```bash
mkdir -p ~/memory/people

cat > ~/memory/people/zhang-san.md << 'EOF'
- 公司：ABC 科技
- 职位：CTO
- 联系方式：zhangsan@abc.com

- 2026-07-01：首次接触，介绍产品
- 2026-07-10：产品演示，反馈积极
- 2026-07-15：报价发送，等待回复

- 关注数据安全
- 决策周期约 2 周
- 周三下午方便沟通
EOF

cat > ~/memory/people/INDEX.md << 'EOF'
| 姓名 | 公司 | 职位 | 状态 | 文件 |
|:---|:---|:---|:---|:---|
| 张三 | ABC 科技 | CTO | 跟进中 | zhang-san.md |

总计：1 条
EOF

cat ~/memory/people/zhang-san.md
```

## 代码示例 (bash)

```bash
cat > ~/memory/projects/alpha.md << 'EOF'
- 状态：进行中
- 技术栈：React + TypeScript
- 开始时间：2026-07-01

用户的核心产品，面向小团队的协作工具。

- 2026-07-05：选择 React 而非 Vue（团队熟悉度）
- 2026-07-10：部署到 Vercel（成本考量）
EOF

cat > ~/memory/projects/INDEX.md << 'EOF'
| 名称 | 状态 | 更新 | 文件 |
|:---|:---|:---|:---|
| Alpha | 进行中 | 2026-07 | alpha.md |

总计：1 条进行中
EOF

grep -r "React" ~/memory/
```

## 代码示例 (text)

```text
┌───────────────────────────────────────────────────────────────┐
│           INFINITE MEMORY VAULT（免费版架构）                   │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  Agent 内置记忆                 本 Skill（~/memory/）          │
│  ┌─────────────────┐           ┌─────────────────────────┐    │
│  │ MEMORY.md       │           │ 无限分类存储             │    │
│  │ memory/ (日志)  │    +      │ 任意结构                │    │
│  │ 基础召回        │           │ 完美组织                │    │
│  └─────────────────┘           └─────────────────────────┘    │
│         ↓                              ↓                       │
│    Agent 基础上下文            Everything else                 │
│   （自动工作）                （无限扩展）                      │
│                                                                │
│  并行设计 · 互不冲突 · 即写即存                                 │
└───────────────────────────────────────────────────────────────┘
```

