# 依赖 + 部署文档 subagent prompt 模板

subagent 类型：`general-purpose`

```
分析项目依赖和部署配置，生成两份文档，通过 Write 工具写入文件。

项目语言: <language>
项目框架: <framework>
项目元数据: <依赖列表摘要>
模块列表: <所有模块名称>

步骤：
1. 读取依赖配置文件（pyproject.toml / package.json / go.mod 等）
2. 读取 Dockerfile、docker-compose.yml、Makefile 等（如有）
3. 扫描 import/require 语句分析模块间依赖
4. 用 Write 工具写入：
   - docs/dependencies.md（内容：第三方依赖表格、内部模块依赖图、依赖层级）
   - docs/deployment.md（内容：环境要求、安装步骤、配置表格、构建发布、常见问题）

中文编写，术语保留英文。

**返回值只需一行摘要**：
"已写入 docs/dependencies.md + docs/deployment.md"
绝不在返回值中包含文档全文。
```
