---
name: kes-app-builder
name_for_command: kes-app-builder
description: KingbaseES 应用构建编排器。当用户提到"帮我构建应用"、"从零开发"、"项目脚手架"、"技术栈选择"、"快速开始"、"完整项目"时，必须使用此技能。本技能是纯编排器，通过触发其他技能完成工作。
---

# KingbaseES 应用构建编排器

本技能是纯编排器，**不承载知识**，通过触发其他技能完成从需求到部署的完整流程。

## 流程

```
1. 需求收集 → 2. 技术栈确认 → 3. 环境检查 → 4. 任务规划 → 5. 执行开发 → 6. 部署
```

## 1. 需求收集

了解用户要做什么：
- Web API？数据导入？管理后台？报表系统？微服务？
- 数据量级？并发要求？

## 2. 技术栈确认

| 场景 | 推荐栈 | 触发技能 |
|------|--------|---------|
| 企业应用（默认） | Java + Spring Boot + MyBatis | `kes-java` + `kes-hibernate` |
| Go 服务 | Go + Gin/Gorm | `kes-go` |
| Python 数据科学 | Python + FastAPI + SQLAlchemy | `kes-python` + `kes-sqlalchemy` |
| Node.js 前端全栈 | Node.js + kb | `kes-nodejs` |
| .NET 企业应用 | C# + EF Core | `kes-dotnet` |
| PHP 快速开发 | PHP + PDO | `kes-php` |
| Qt 桌面应用 | Qt + qkingbase | `kes-qt` |

**默认栈**：Java + Spring Boot + MyBatis（KingbaseES 用户以政企为主，Java 生态占绝对主导）

## 3. 环境检查

根据技术栈检查：
- JDK/Go/Python/Node.js/.NET 版本
- 数据库可达性（`ksql -U SYSTEM -d test -h host -p port`）
- 网络连通性

## 4. 任务规划

根据需求分解为具体任务，每个任务对应一个已有技能：
- 连接配置 → 对应语言技能
- ORM 集成 → 对应框架技能
- SQL 编写 → `kes-core` / `kes-plsql`
- 性能优化 → `kes-sql-tuning` / `kes-index-design`
- 部署 → `kes-deploy` / `kes-docker`

## 5. 执行开发

按规划逐步触发对应技能，完成开发。

## 6. 部署

根据部署目标触发对应技能：
- ISO 安装 → `kes-deploy`
- Docker 容器化 → `kes-docker`
- 高可用集群 → `kes-ha`
- 备份恢复 → `kes-backup`

## 项目布局参考

| 语言 | 参考文件 |
|------|---------|
| Java | `ref/project-layout-java.md` |
| Go | `ref/project-layout-go.md` |
| Python | `ref/project-layout-python.md` |

## 关键原则

1. **不重复造轮子** — 所有具体知识在其他技能中
2. **引导式交互** — 逐步确认需求，不一次性输出所有信息
3. **默认 Java** — 用户未指定时，推荐 Java + Spring Boot
4. **部署优先** — 先确保环境可用，再开始开发

## 参考文档

```
kes-app-builder/
├── SKILL.md                         # 本文件
├── ref/
│   ├── project-layout-java.md       # Java 项目结构参考
│   ├── project-layout-go.md         # Go 项目结构参考
│   └── project-layout-python.md     # Python 项目结构参考
└── test-cases.md
```
