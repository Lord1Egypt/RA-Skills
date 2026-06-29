# projects.yaml 格式规范

> AI 参考：读写 `~/.myknowledge/config/projects.yaml` 时按此规范操作。

## 文件位置

```
~/.myknowledge/config/projects.yaml
```

## 格式

```yaml
projects:
  - path: "知识库的完整路径"
    name: "项目名称"
    last_access: "YYYY-MM-DD"
    type: "global" | "project"
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `path` | string | 知识库目录的绝对路径（支持 `~` 开头） |
| `name` | string | 项目显示名称（用于向用户展示） |
| `last_access` | string | 最后访问日期，格式 `YYYY-MM-DD` |
| `type` | string | `"global"` = 全局知识库（`~/.myknowledge/global/{name}/`），`"project"` = 项目知识库（`{workspace}/.myknowledge/`） |

## 操作规则

### 追加新项目
```yaml
# 在 projects 列表末尾追加
projects:
  - path: "~/.myknowledge/global/销售数据分析"
    name: "销售数据分析"
    last_access: "2026-06-11"
    type: "global"
```

### 更新 last_access
找到 `path` 匹配的条目，更新 `last_access` 为当前日期。

### 删除项目
找到 `path` 匹配的条目，从列表中移除。

### 列出所有项目
读取整个文件，按 `last_access` 倒序排列后展示给用户。

## 示例

```yaml
projects:
  - path: "~/projects/sales-report"
    name: "销售报表系统"
    last_access: "2026-06-11"
    type: "project"
  - path: "~/.myknowledge/global/爬虫脚本"
    name: "爬虫脚本"
    last_access: "2026-06-10"
    type: "global"
  - path: "~/.myknowledge/global/数据分析"
    name: "数据分析"
    last_access: "2026-06-09"
    type: "global"
```

## 空文件

首次初始化时为空列表：
```yaml
projects: []
```
