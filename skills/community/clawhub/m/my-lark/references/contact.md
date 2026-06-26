# 通讯录 API（Contact）

## 快速调用

# 查询用户（通过 open_id）
python3 /workspace/skills/lark-skill/lark_mcp.py call contact_v3_user_batchGetId '{"user_id_type":"open_id","open_ids":["ou_032ca29de8829b1a71272844465a4df3"]}'

# 查询部门列表
python3 /workspace/skills/lark-skill/lark_mcp.py call contact_v3_departments '{"user_id_type":"open_id"}'

## API 分类

contact_v3_user_batchGetId / contact_v3_users / contact_v3_users_search - 用户查询
contact_v3_departments / contact_v3_department / contact_v3_group_user_list - 部门查询
contact_v3_accounthierarchy - 账号层级
