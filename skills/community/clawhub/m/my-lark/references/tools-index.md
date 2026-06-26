# 工具完整索引

## 消息与群组（im_v1_*）
im_v1_chat_list - 获取当前用户所在群列表
im_v1_chat_create - 创建群聊
im_v1_chatMembers_get - 获取群成员列表
im_v1_message_create - 发送消息
im_v1_message_list - 查询消息历史
im_v1_message_reply - 回复消息
im_v1_message_update - 编辑消息
im_v1_message_delete - 撤回消息
im_v1_message_forward - 转发消息
im_v1_message_reaction_create - 添加表情回复
im_v1_pin_create - Pin 消息
im_v1_image_create - 上传图片
message_v4_batch_send - 批量发送消息

## 云盘与文件（drive_v1_* / explorer_v2_*）
drive_explorer_v2_root_folder_meta - 获取云盘根目录 token
drive_explorer_v2_fileList - 获取文件夹内文件列表
drive_v1_files_create_folder - 创建文件夹
drive_v1_files_move - 移动文件或文件夹
drive_v1_files_delete - 删除文件或文件夹
drive_v1_permissionMember_create - 添加文件协作者
drive_v1_permissionMember_list - 获取协作者列表

## 知识库（wiki_v1_* / wiki_v2_*）
wiki_v1_node_search - 搜索知识库节点（⚠️ User Token）
wiki_v2_spaces - 获取知识库空间列表
wiki_v2_space_getNode - 获取节点详情（含 obj_token）
wiki_v2_nodes_create - 创建知识库节点
wiki_v2_nodes_delete - 删除节点
wiki_v2_nodes_move - 移动节点

## 云文档（docx_v1_* / docx_builtin_*）
docx_builtin_search - 搜索云文档（⚠️ User Token）
docx_v1_document_rawContent - 读取文档内容（⚠️ User Token）
docx_v1_document_blocks - 获取文档块列表
docx_v1_blocks_create - 在文档中插入块
docx_v1_blocks_update - 更新块内容
docx_builtin_import - 导入文档

## 电子表格（sheets_v2_* / sheets_v3_*）
sheets_v3_spreadsheets_create - 创建电子表格
sheets_v2_spreadsheets_values_get - 读取单元格
sheets_v2_spreadsheets_values_put - 写入单元格
sheets_v2_spreadsheets_values_batch_get - 批量读取范围
sheets_v2_spreadsheets_values_append - 追加数据

## 多维表格（bitable_v1_app*）
bitable_v1_app_list - 列出所有多维表格
bitable_v1_appTable_list - 列出子表
bitable_v1_appTableRecord_create - 新增记录
bitable_v1_appTableRecord_list - 获取记录列表
bitable_v1_appTableRecord_update - 更新记录
bitable_v1_appTableRecord_delete - 删除记录
bitable_v1_appTableField_list - 获取字段配置

## 通讯录（contact_v3_*）
contact_v3_user_batchGetId - 批量获取用户
contact_v3_users - 获取用户详情列表
contact_v3_departments - 获取部门列表

## 日历（calendar_v4_*）
calendar_v4_calendars - 获取日历列表
calendar_v4_events - 创建日程
calendar_v4_events_list - 获取日程列表
calendar_v4_freebusy_query - 查询忙闲状态
calendar_v4_attendees_create - 添加参与者

## 审批（approval_v4_*）
approval_v4_instances_create - 提交审批
approval_v4_instances_get - 获取审批详情
approval_v4_instances_list - 获取审批列表
approval_v4_tasks_list - 获取待审批列表

## 画板（board_v1_*）
board/v1/whiteboards/:id/download_as_image - 下载画板为图片
board/v1/whiteboards/:id/nodes/plantuml - 解析 PlantUML/Mermaid
