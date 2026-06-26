# Package Version Tracker

> 快速查询 npm/pypi 包版本信息，追踪最新版本和历史版本。

## 功能

- **npm 包版本查询**：查询 npm 包的最新版本、发布时间、所有版本列表
- **pypi 包版本查询**：查询 PyPI 包的最新版本、发布历史
- **版本比较**：比较两个版本号大小
- **多包批量查询**：一次查询多个包

## 触发词

- "查一下 npm 包版本"
- "pypi 版本"
- "package version"
- "包版本查询"
- "npm latest"
- "pip show"

## 使用方法

### 命令格式

```
/version npm <package_name>
/version pypi <package_name>
/version compare <version1> <version2>
```

### 示例

```
/version npm react
/version pypi pandas
/version compare 2.0.0 1.9.0
```

## 输出格式

返回包的详细信息：
- 包名
- 最新版本
- 发布日期
- 版本数量
- 依赖信息
- 历史版本列表（最近5个）

## 限制

- 无需 API key，直接使用公共 registry API
- 速率限制：每秒最多 5 次请求
- 批量查询最多 10 个包
