# Java 依赖安全扫描技能文档

本项目是一套用于分析 Java、Maven 或 Spring 生态项目依赖安全风险的技能文档（Skill）。

## 用途

当需要执行以下任务时，使用本文档：

- 扫描项目依赖漏洞
- 核实特定依赖版本是否受影响
- 分析 CVE 影响范围
- 检查传递依赖路径
- 检查第三方 JAR 内嵌依赖
- 生成包含修复建议的依赖安全报告

## 文档结构

```
.
├── README.md                 # 本文件
├── SKILL.md                  # 技能入口文档（从这里开始）
└── references/               # 参考资料目录
    ├── 01-principles.md      # 执行原则与环境
    ├── 02-maven.md           # Maven 项目分析
    ├── 03-gradle.md          # Gradle 项目分析
    ├── 04-tools.md           # 漏洞扫描工具
    ├── 05-commands.md        # 命令示例
    ├── 06-output.md          # 输出与修复模板
    └── 07-reference.md       # 参考与常见问题
```

## 快速开始

1. 首先阅读 [SKILL.md](./SKILL.md) 了解整体工作流程
2. 根据项目类型查阅 [Maven](./references/02-maven.md) 或 [Gradle](./references/03-gradle.md) 分析指南
3. 使用 [命令示例](./references/05-commands.md) 执行扫描
4. 参考 [输出与修复模板](./references/06-output.md) 生成报告

## 核心工作流程

```
收集证据 → 界定范围 → 匹配漏洞 → 输出报告
```

## 适用范围

本文档聚焦 **Java 生态（Maven/Gradle）** 的依赖安全分析。

其他语言项目可复用相同的漏洞分析方法，但需调整：
- 依赖获取命令（npm list, pip freeze 等）
- 锁文件格式（package-lock.json, Pipfile.lock 等）
- 漏洞数据源和 API 接口

## 关键原则

- **先收集证据，再下结论**：优先使用 lockfile 和 dependency:tree
- **双重验证**：扫描器结果只是线索，需人工核实版本和受影响范围
- **明确不确定性**：无法确认的信息要标注"需要验证"或"证据不足"
- **关注运行时**：默认只关注实际进入运行时类路径的依赖

## 许可证

本项目为技能文档，供学习参考使用。
