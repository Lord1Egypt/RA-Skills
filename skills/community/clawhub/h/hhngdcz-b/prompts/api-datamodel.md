# API + 数据模型文档 subagent prompt 模板

subagent 类型：`general-purpose`

```
生成 API 接口文档和数据模型文档，通过 Write 工具写入文件。

项目语言: <language>
模块列表: <所有模块名称>

步骤：
1. 读取 docs/modules/*.md 获取接口和数据模型信息，需要时读源码补充
2. 用 Write 工具写入：
   - docs/api.md（内容：概述、按模块分组的接口列表含参数表格+返回值+示例）
   - docs/data-model.md（内容：核心模型字段表格、关系说明、ASCII 模型关系图）

中文编写，术语保留英文。

**返回值只需一行摘要**，绝不回传文档全文。
```
