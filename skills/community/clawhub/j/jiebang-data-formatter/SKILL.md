---
name: jiebang-data-formatter
description: 开发者数据格式转换工具 - JSON/YAML互转、XML格式化、SQL格式化、进制转换、HTML实体编解码、Cron表达式解析。当用户提到JSON转YAML、YAML转JSON、XML格式化、SQL美化、进制转换、HTML编码解码、Cron表达式解析等需求时使用此技能。
---

# 捷帮数据格式化

开发者常用的数据格式转换与处理工具集。

## 核心能力

### 1. JSON/YAML互转 (json-yaml)
- JSON → YAML
- YAML → JSON
- 支持大文件处理
- 保留注释（如源文件有）

### 2. XML格式化 (xml-format)
- XML 美化/格式化
- XML 压缩
- XML 验证
- XML → JSON 转换

### 3. SQL格式化 (sql-format)
- SQL 语句美化
- 关键字大写
- 缩进格式化
- 支持 SELECT/INSERT/UPDATE/DELETE

### 4. 进制转换 (base-convert)
- 二进制 ↔ 十进制
- 十进制 ↔ 十六进制
- 二进制 ↔ 八进制
- 任意进制转换（2-36）

### 5. HTML实体编解码 (html-entity)
- HTML实体编码（将 < > & 等转换为 &lt; &gt; &amp;）
- HTML实体解码（反向操作）
- Unicode编码支持

### 6. Cron表达式解析 (cron-parse)
- 解析Cron表达式含义
- 计算下次执行时间
- 验证Cron表达式格式
- 生成可读描述

## 输入参数

### JSON/YAML互转
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| data | string | 是 | 要转换的数据 |
| direction | string | 是 | 转换方向 (json_to_yaml / yaml_to_json) |
| indent | int | 否 | 缩进空格数，默认2 |

### XML格式化
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| data | string | 是 | XML内容 |
| action | string | 是 | 操作 (format / minify / validate) |

### SQL格式化
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sql | string | 是 | SQL语句 |
| keyword_upper | bool | 否 | 关键字大写，默认true |
| indent | int | 否 | 缩进，默认2 |

### 进制转换
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| value | string | 是 | 要转换的数值 |
| from_base | int | 是 | 源进制 |
| to_base | int | 是 | 目标进制 |

### HTML实体编解码
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| data | string | 是 | 要处理的内容 |
| action | string | 是 | 操作 (encode / decode) |

### Cron表达式解析
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| expression | string | 是 | Cron表达式 |
| next_runs | int | 否 | 返回下次执行次数，默认5 |

## 输出格式

### 格式化结果
```json
{
  "success": true,
  "data": {
    "result": "格式化后的结果",
    "original_length": 100,
    "result_length": 150
  }
}
```

### Cron解析结果
```json
{
  "success": true,
  "data": {
    "expression": "0 0 * * *",
    "description": "每天午夜执行",
    "next_runs": ["2024-01-01 00:00", "2024-01-02 00:00"],
    "is_valid": true
  }
}
```

## 使用示例

**示例1：JSON转YAML**
```
输入：将 {"name": "test", "value": 123} 转为YAML
输出：
name: test
value: 123
```

**示例2：SQL格式化**
```
输入：SELECT id,name from users where id=1
输出：
SELECT id, name 
FROM users 
WHERE id = 1
```

**示例3：进制转换**
```
输入：将 255 从十进制转为十六进制
输出：FF
```

**示例4：Cron解析**
```
输入：解析 0 0 * * *
输出：每天午夜 00:00 执行
```

## 注意事项

- 输入数据需符合对应格式规范
- Cron表达式支持标准5段式格式
- 进制转换支持2-36进制
- HTML编解码支持命名实体和数字实体
