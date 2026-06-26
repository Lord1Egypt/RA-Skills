# 多维表格 API（Bitable）

## 快速调用

# 列出所有多维表格
python3 /workspace/skills/lark-skill/lark_mcp.py call bitable_v1_app_list '{}'

# 查询记录
python3 /workspace/skills/lark-skill/lark_mcp.py call bitable_v1_appTableRecord_list '{"page_size":100}'

## 资源层次

多维表格 App（app_token）→ 数据表（table_id）→ 字段/记录/视图

## API 分类

bitable_v1_app_list / bitable_v1_app_create - 多维表格 App
bitable_v1_appTable_list / bitable_v1_appTable_create - 数据表
bitable_v1_appTableRecord_create list update delete search - 记录
bitable_v1_appTableField_list create update delete - 字段

## 使用限制

批量操作单次最大记录数：1,000 条
字段数：300 / 视图数：200
写操作并发：同一多维表格建议同时只请求 1 次写操作

批量操作：要么全部成功，要么全部失败，不存在部分成功
