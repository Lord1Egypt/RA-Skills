# 模块文档 subagent prompt 模板

subagent 类型：`general-purpose`

```
分析以下模块的源码，生成技术文档，通过 Write 工具写入文件。

项目语言: <language>
项目框架: <framework>
<如果是合并任务>
本次为多个模块各自生成独立文档：
- 模块 "<module-A>": 文件 [<路径>], 输出 docs/modules/<module-A>.md
- 模块 "<module-B>": 文件 [<路径>], 输出 docs/modules/<module-B>.md
<如果是单模块任务>
模块名称: <module-name>
源码文件: <逐行列出绝对路径>
输出路径: docs/modules/<module-name>.md
<如果是大模块>
文件较多，优先读取入口文件和 API 定义，跳过测试和生成代码。

步骤：
1. 读取源码，分析模块功能
2. 用 Bash 创建目录：mkdir -p docs/modules
3. 用 Write 工具写入文档到 docs/modules/<name>.md

文档章节：概述、架构设计（ASCII 图）、核心接口（参数+返回值+示例）、数据模型（表格）、配置说明、依赖关系、实现细节。不适用的章节省略。
中文编写，术语保留英文。基于实际代码，绝不编造。

**返回值只需一行摘要**：
"已写入 docs/modules/<name>.md（N 章节，M 接口）"
绝不在返回值中包含文档全文。
```
