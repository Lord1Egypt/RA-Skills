# json-query-tool — JSON 查询工具

## 痛点
- jq 语法复杂，学习成本高
- 只想快速提取 JSON 中的某个字段，却要写一长串表达式
- 需要在 shell 脚本中处理 JSON，但不想引入额外依赖
- 不同格式输出（表格、纯文本）要手动转换

## 场景
- 从 API 响应 JSON 中提取指定字段
- 查询 JSON 配置文件中的某个值
- 日志文件是 JSON Lines 格式，批量提取字段
- 将 JSON 数据导出为易读的表格形式

## 定价
- **免费**：基础路径查询 + JSON/纯文本输出
- **Pro 19元**：表格输出 + 类型过滤 + 通配符支持
- **Team 49元**：批量文件处理 + 管道集成 + 自定义格式

## 指令格式

### 基本用法
```
jsonq <文件> <路径表达式>
```

### 输出格式
```
jsonq <文件> <路径> --format raw|json|table
```

## 查询语法

| 模式 | 说明 | 示例 |
|------|------|------|
| `key` | 对象属性访问 | `users.name` |
| `parent.child` | 嵌套访问 | `user.profile.email` |
| `[n]` | 数组索引 | `users[0]` |
| `[*]` | 全部数组元素 | `users[*]` |
| `*` | 通配符键名 | `users.*.name` |
| `:type` | 类型过滤 | `age:number` |

## 示例

### 示例 JSON
```json
{
  "users": [
    {"name": "Alice", "age": 30, "email": "alice@example.com"},
    {"name": "Bob", "age": 25, "email": "bob@example.com"}
  ],
  "company": {
    "name": "TechCorp",
    "departments": [
      {"name": "Engineering", "head": "Carol"},
      {"name": "Sales", "head": "Dave"}
    ]
  }
}
```

### 查询示例
```bash
# 获取所有用户名
jsonq data.json "users[*].name"
["Alice", "Bob"]

# 获取第一个用户的邮箱
jsonq data.json "users[0].email"
alice@example.com

# 获取部门名称列表
jsonq data.json "company.departments[*].name"
["Engineering", "Sales"]

# 表格形式输出
jsonq data.json "users[*]" --format table
name    age  email
Alice   30   alice@example.com
Bob     25   bob@example.com

# 类型过滤：只取数字字段
jsonq data.json "users[0]" --format json
{"name": "Alice", "age": 30, "email": "alice@example.com"}
```

## 安装

```bash
# 本地安装
pip install -e .

# 或直接使用
chmod +x jsonq
./jsonq data.json "field"
```
