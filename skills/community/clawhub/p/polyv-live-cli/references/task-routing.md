# 自然语言任务路由

使用本文件把用户的业务说法映射到 `polyv-live-cli` 命令族。选中命令族后，必须继续运行 `<CLI> <command> --help` 和必要的深层 help 校验参数。

## 频道与直播

- 创建、查询、更新、删除频道：`channel`
- 频道状态、开播状态、频道角色、频道广告、频道回调、PPT 设置：`channel`
- 频道装修、分发、监控配置、MR 创建、批量创建：`channel`
- 推流地址、推流密钥、直播状态、断流恢复、推流开关：`stream`
- 转播频道、创建转播、查询转播关系：`transmit`
- 监控面板、持续看板：`monitor`
- 场景初始化、创建电商场景资源：`setup`

## 内容、回放和录制

- 回放列表、详情、标题、排序、开关、删除：`playback`
- 录制设置、录制文件、合并、转码、断点续录：`record`
- 文档、课件、多媒体资源关联：`document`
- 场次、场次外部 ID、场次回放/统计关联：`session`
- 素材库、素材分类、素材标签：`material`

## 观看页、播放器和访问控制

- 观看页菜单、分享、退出跳转、页面基础信息：`web`
- 观看页打赏入口或页面打赏设置：`web` 或 `donate`，先查 help 区分
- 播放器配置、Logo、水印、暖场、片头、暂停页：`player`
- 观看条件、鉴权、token、白名单观看模式：`watch-condition`
- 白名单成员、全局白名单、频道白名单：`whitelist`

## 聊天和互动

- 聊天消息、聊天记录、聊天开关、在线人数：`chat`
- 禁言、解禁、踢人、解踢、清空聊天：`chat`
- 签到：`checkin`
- 问答卡：`qa`
- 问卷：`questionnaire`
- 抽奖、福袋、观众组、黑名单：`lottery`
- 打赏设置、打赏记录：`donate`
- 互动脚本、互动监听事件、任务奖励、点赞、奖励消息：`interaction`

## 营销和商品

- 商品列表、创建、更新、删除、商品开关：`product`
- 用户说“观看页展示商品”“直播间显示商品列表”“打开商品库”：先用 `product enabled` 查询，必要时用 `product update-enabled --enabled Y` 打开；不要只创建或上架商品。
- 商品标签、商品统计、商品设置：`product`
- 优惠券：`coupon`
- 用户说“观看页展示优惠券”“直播间可领券”“打开领券入口”：先用 `coupon channel add` 绑定优惠券到频道，再用 `coupon channel enabled` 查询，必要时用 `coupon channel update-enabled --enabled Y` 打开；不要只创建账号级优惠券。
- 卡片推送、推送/取消/删除卡片：`card-push`
- 推广渠道：`promotion`
- 邀请榜单、邀请销售、关注观众：`invite-sales`

## 观众、用户和平台账号

- 观众详情、观众列表、观众画像：`viewer`
- 用户自定义字段、观众字段值：`custom-field`
- 平台账号信息、平台开关、平台回调、平台标签：`platform`
- 用户全局设置、子账号、组织、模板、账单、观看日志：`user`
- 全局账号设置、全局页面设置、全局鉴权：`global`
- 分组账号、资源分配、分组账单：`group`
- 伙伴账号、腾讯订单、客户注册：`partner`
- WebApp 角色和权限：`webapp`
- 全局机器人：`robot`
- 财务、账单、音视频审核：`finance`
- AI 数字人、AI 功能：`ai`

## 统计和报表

- 直播统计、频道统计、观看日志导出：`statistics`
- 观众统计同时可能涉及：`viewer`、`statistics`
- 商品统计同时可能涉及：`product`、`statistics`

## 歧义处理

- 用户说“观看页”时，优先考虑 `web`；如果是播放器组件视觉配置，切到 `player`；如果是访问鉴权，切到 `watch-condition`。
- 用户说“聊天人数/在线人数”时，优先考虑 `chat`；如果是长期数据报表，切到 `statistics`。
- 用户说“回放文件”时，优先考虑 `record`；如果是观众可见回放列表或回放开关，切到 `playback`。
- 用户说“展示商品/优惠券”时，区分创建资源和观看页开关：商品走 `product update-enabled`，优惠券走 `coupon channel add` 加 `coupon channel update-enabled`。
- 用户说“用户”时，区分观众用户用 `viewer`，账号/子账号/组织用 `user`，平台账号信息用 `platform`。
- 用户说“删除、停止、关闭、推送、导入、合并、转码”时，先判断风险并确认，再执行。
