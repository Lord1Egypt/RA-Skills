# 消息与群组 API（IM）

## 快速调用

# 发送文本消息
python3 /workspace/skills/lark-skill/lark_mcp.py send oc_90845b3c4545b7ed0a3353f53df6eec4 "测试消息"

# 发送富文本
python3 /workspace/skills/lark-skill/lark_mcp.py call im_v1_message_create '{"receive_id_type":"chat_id","receive_id":"oc_xxx","msg_type":"post","content":"{\"zh_cn\":{\"title\":\"标题\",\"content\":[[{\"tag\":\"text\",\"text\":\"正文\"}]]}"}'

## 消息类型（msg_type）

text / post（富文本） / image / file / audio / video / sticker / interactive（卡片） / share_chat / share_user

## API 分类

发送消息：im_v1_message_create message_v4_batch_send
查询消息：im_v1_chat_list im_v1_message_list
编辑撤回：im_v1_message_update im_v1_message_delete
群管理：im_v1_chat_create chatMembers_invite chatMembers_kick
表情/Pin：im_v1_message_reaction_create im_v1_pin_create
图片上传：im_v1_image_create im_v1_file_create

## 权限 Scope

im:message - 基础消息读写
im:message:send_as_bot - 以机器人身份发消息
im:message:recall - 撤回消息
im:chat - 群管理
im:resource - 上传图片/文件

## 常见错误

99991700 - 机器人不在该群中
99991403 - 权限不足
99991140 - 接口频率超限
