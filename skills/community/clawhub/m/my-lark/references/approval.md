# 审批 API（Approval）

## 快速调用

# 查询审批实例
python3 /workspace/skills/lark-skill/lark_mcp.py call approval_v4_instances_list '{"approval_code":"审批定义code"}'

# 提交审批
python3 /workspace/skills/lark-skill/lark_mcp.py call approval_v4_instances_create '{"approval_code":"xxx","form":"[{\"value\":\"内容\"}]"}'

## API 分类

approval_v4_instances_create - 提交审批
approval_v4_instances_get / approval_v4_instances_list - 查询详情
approval_v4_tasks_list - 获取待审批列表
approval_v4_approvers_record / approval_v4_instance_cancel - 审批操作
approval_v4_approval_info - 审批定义
