# 架构文档 subagent prompt 模板

subagent 类型：`general-purpose`

```
生成项目架构文档，通过 Write 工具写入文件。

项目语言: <language>，框架: <framework>
模块列表: <名称和一行描述>

步骤：
1. 读取 docs/modules/*.md 和项目入口/配置文件
2. 用 Write 工具写入 docs/architecture.md
   （内容：系统概览、ASCII 架构图、技术栈表格、模块关系图、数据流图、设计模式、目录结构）

中文编写，术语保留英文。大量使用 ASCII 图表。

**返回值只需一行摘要**，绝不回传文档全文。
```
