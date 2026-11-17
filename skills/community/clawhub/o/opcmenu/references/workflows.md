# 合作、链位与全景工作流

## 合作与私信

公开发现从 `list_needs_feed` / `search_needs` / `search_people` 开始。`get_need` 看清单条需求，结合用户已提供的能力判断匹配，不为了推荐先读完整私信或联系方式。

用户授权发起联系后，`contact_need` 返回 `conversationId`；再用该 id 调 `get_conversation_needs` 补全双方需求上下文，并用 `send_message` 发送获授权的内容。直接找人可用 `start_conversation`。不要在尚无会话 id 时先调会话工具。

发布需求用 `create_need`，更新用 `update_need`；用 `get_need_recommendations` 查看自己需求的候选。合作完成时，`complete_need` 需要双方分别确认，不能替另一方确认。

收件箱用 `list_my_conversations` → `read_messages` → 草拟回复；只有用户明确要求发送的会话与内容才发出。额度不足先读错误出口，`get_my_invite` 可提供邀请入口，`redeem_chat_quota` 则需要明确的积分花费授权，不能自动换额度。

## 产业链与定位

`get_chain_anchor` 不传锚点时定位本人；可先用 `metadataOnly=true` 探索环数，再用 `list_chain_group_members` 查看相关一环，游标原样透传。链上成员 id 可继续作为下一跳锚点，选中人后再看 `get_creator`。

尚未归位时，可以根据用户明确提供的介绍准备 `set_my_chain_position` 的 describe；这会更新实际链位，不能把“帮我理解产业链”视作已授权改资料。

`get_my_positioning` 的 `nextUp` 含建议动作和 `suggestedTool`。只执行用户选择或授权的事项，先核对工具在实时清单里；`mark_positioning_task` 用于用户确认已完成的线下事项，不能为了涨分虚报注册公司、商标或收入。

融资与角色资料用 `set_my_role_profile`，其子树整体替换，修改前读取并保留已填写字段。`list_funding` 的 investor / project 方向按实时入参选择；别人的 BP 文件不会因为出现 `hasBp` 就对当前用户可下载。

## 今日简报

`get_my_brief` 汇总未读消息、近期关注、开聊额度、即将截止的报名、定位待办和本人活动待审事项。根据用户问题选最相关的部分，再按需展开：

- 未读：会话列表 → 消息 → 草稿。
- 即将截止：报名机会 → 合并缺口 → 用户选择的报名。
- 待审：主办方名单 → 预览处置。
- 定位：读取建议动作，按已授权范围处理。
- 近期关注：`list_recent_attention` 只描述返回的具名访客；匿名计数不能编成人名。浏览主页不等于用户授权主动搭话。

## 数据卡与分享

`get_my_card` 返回本人的结构化资料。填入其他服务时仅传用户要求的字段，尤其注意联系方式与链接可见性。`get_share_card_manifest` 返回可分享的文字和链接，但它不代表已经发送；`send_share_card` 才是会话发送动作。

若宿主支持 MCP resources / prompts，可按需发现 `me/card`、`me/brief`、`me/signups` 等 resources，或 `signup_sweep`、`organizer_triage`、`check_my_inbox` 等 prompts。以服务端当次清单为准，不假设每个宿主都有相同的快捷命令。
