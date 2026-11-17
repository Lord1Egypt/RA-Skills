---
name: json-param-parser
description: "JSON层级解析：输入JSON+参数名，输出参数完整层级路径、枚举值、格式化JSON及SQL提取建议（get_json_object写法）。"
---

# json字段解析 - 使用说明

## 功能概述

输入一段 JSON + 需要查找的参数名，输出：
1. 参数在 JSON 中的完整层级路径
2. 参数的枚举值
3. 格式化后的 JSON
4. SQL 提取建议（get_json_object 写法）

## 触发词

`json字段解析`、`json层级解析`、`json参数解析`、`json解析`

## 使用方式

### 方式1：直接传参
```bash
python3 json_param_parser.py '{"key":"value"}' 参数名
```

### 方式2：从文件读
```bash
python3 json_param_parser.py "$(cat log.json)" 参数名
```

### 方式3：管道输入
```bash
cat log.json | python3 json_param_parser.py 参数名
```

## 输出示例

查找参数 `reply_id`，输出内容：

```python
查找参数: reply_id
找到参数 'reply_id'，共 4 处匹配:
   action_data.reply_id      = "153694391623"
   action_data.request_params.reply_id      = "153694391623"
   reply_id      = "153694391623"
   request_params.reply_id      = "153694391623"
```

格式化 JSON 及 SQL 提取建议 (get_json_object)：
```python
-- action_data.reply_id
get_json_object(get_json_object(bhv_ext, '$.action_data'), '$.reply_id')
get_json_object(bhv_ext, '$.action_data.reply_id')

-- action_data.request_params.reply_id
get_json_object(get_json_object(get_json_object(bhv_ext, '$.action_data'), '$.request_params'), '$.reply_id')
get_json_object(bhv_ext, '$.action_data.request_params.reply_id')

-- reply_id
get_json_object(bhv_ext, '$.reply_id')

-- request_params.reply_id
get_json_object(get_json_object(bhv_ext, '$.request_params'), '$.reply_id')
get_json_object(bhv_ext, '$.request_params.reply_id')
```

## 核心能力

- 自动修复多层转义 JSON（双转义、截断补全）
- 自动匹配 snake_case / camelCase / 去下划线命名
- 递归搜索内嵌 JSON 字符串
- 正则兜底查找
- 模糊匹配提示

## 脚本下载

脚本文件：`json_param_parser.py`
功能：解析 JSON 日志中的参数层级，输出路径、枚举值及 SQL 提取建议。
安装方式：`openclaw skills install json-param-parser`

## Workflow

1. 用户提供 JSON 内容（直接粘贴、文件路径或管道输入）+ 目标参数名
2. 运行 `scripts/json_param_parser.py` 解析
3. 输出层级路径、枚举值、SQL 提取建议
