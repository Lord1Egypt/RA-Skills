# 运行与账户适配

运行需要Node.js 22.20+，不依赖AG1—AG6或其他OpenLX技能。所有路径替换成用户指定位置；不要把酒店工作区放进公开仓库。

## 第一份快照

`example-snapshot.json`是明确标记的演示数据。真实文件必须提供`hotel.id/name`、`observed_at`、`source.type/reference`。类型为USER_EXPORT、LIVE或MOCK；LIVE还需要account_id。`rooms/rates/inventory/orders/reviews/promotions/competitors/events/facts`为数组，未采集用null。

房价按整数分`price_fen`保存。每条rate含`room_id/plan_id/date`。订单数据仅保留本次需要的字段，不导入证件与联系方式。报告不输出这些敏感字段。

metrics需要`scope`（CTRIP或PROPERTY）、`period`、`basis`、`available_room_nights`、`sold_room_nights`和`room_revenue_fen`。PROPERTY另需authoritative_source。用房晚而非订单数计算；入住日期与下单日期口径不可混合。

promotion净回款若已给`net_settlement_fen`则不重复扣减。否则提供`gross_fen/merchant_discount_fen/commission_base_fen/commission_bps/platform_fee_fen/included_cost_fen`和`rules_verified=true`，缺失保持未知。

## 点评与动作授权

reviews每条含id、rating、text、replied和source_reference。离线无模型时只把明确正向短语白名单识别为可自动回；其他进入确认。是否五星不能覆盖投诉语义。

运行`reviews`生成提案，记录id和content_hash。需要人工确认时，将具体回复给用户看；确认后使用`approve --id ID --hash HASH`。改稿将形成新的内容哈希，不继承旧确认。`execute`只执行已核验映射和LIVE来源提案。

自动好评授权由hotel.json明确记录`positive_review_opt_in=true`、`review_authorization_until`和`review_scan_minutes`。先取得对应酒店、动作、有效期授权；之后不增加多层审批。`run`每次检查是否到期，读取新增点评并生成报告，重复扫描不会重复执行已经验证的动作。无人值守由操作系统定时运行此命令；程序自身不承诺关机后运行。

## 价格策略

`example-pricing-policy.json`展示必需字段。标准版基础自动规则用固定target_fen，后续可用明确阈值产生目标价格。`revenue`用已知预订进度、可比同行与核实需求事件计算至尊多信号情景，输出理由，不编造需求指数。计算结果需经过同样的priceProposal护栏。

价格规则包括底价、上限、单次幅度、日累计幅度、日次数、冷却时间、有效期、日期和房型范围，金额整数分。可附net_floor_fen与已核验settlement。PMS负责的字段不在携程形成双主写入。

房态、资料、接单、活动使用`propose --file proposal.json`，字段kind（INVENTORY/PROPERTY/ORDER/PROMOTION）、object_id、before、after、mode。INVENTORY数量非负；ORDER需inventory_confirmed、权威库存，且只处理ACCEPTED；PROPERTY引用verified_fact_ids；PROMOTION需costs_confirmed。这些基础操作均需用户对具体提案确认。

## 账户字段映射

首次用browser login打开独立Chrome，由用户完成扫码。capture只导出本地可见文本，不导出Cookie或令牌，不能当作结构化读取成功。

实际检查页面后，在工作区分别创建`adapter-ebooking.json`和`adapter-content.json`。没有提供虚构可用选择器，必须从对应账户页面核对：

```json
{
  "account_id": "实际账号标识",
  "hotel_id": "与hotel.json一致",
  "account_label": "页面显示的账号文本",
  "hotel_label": "页面显示的门店文本",
  "identity": {"account": "实际CSS选择器", "hotel": "实际CSS选择器"},
  "verified_at": "实际ISO核验时间",
  "evidence_reference": "本地脱敏核验记录路径",
  "price_authority": "CTRIP",
  "inventory_authority": null,
  "reads": {},
  "writes": {}
}
```

reads每个领域指定url、rows选择器和fields。例如fields的每个键指向`{selector, type}`，type为text/integer/fen/boolean；可用attribute读取明确属性。每个领域读取独立失败，成功领域继续进报告。

writes按`writes.PRICE[object_id]`等分组。每个实际对象需`url/current/input/submit/readback/identity/identity_value/value_type`，可选current_is_input、readback_is_input、readback_url。identity必须绑定具体房型、日期、订单或点评对象，不能只定位第一行。执行前重读旧值，执行后刷新回读，未知结果不重试。失效映射只停止依赖它的动作。

## 笔记链路

素材manifest按文件名映射hotel_id、scene、rights_confirmed、channels（包含CTRIP）、has_people、people_authorized、sensitive。实际文件至少稳定5秒，按文件哈希去重；不合格图片跳过，不拦其他图片。

`content`读取合格素材和verified事实，生成标题、正文、图片说明与SEO导出数据。`distill --file questionnaire.json`生成待审核的结构化人设，问卷可提供positioning、voice、audience、forbidden；事实只取已核验facts。`persona --file persona.json`导入最终配置，要求30天选题和3篇示范稿。

`notes.mjs hash --workspace ... --file draft.json`查看实际内容摘要。具体授权后用`approve --hash ...`，再分别运行open、upload、save、submit、readback、public。发布后改稿应新建版本，不能重复提交UNKNOWN或已提交对象。

adapter-content的note字段由实际页面填入：editor_url、title、body、upload、upload_success、ai_disclosure（适用时）、save、submit、object_id、backend_link。readback与public各自映射object_id、title、body、status以及states（实际文案→对应状态）。后台可提供public_link读取公开地址。要核对同一平台对象、标题和正文；只有公开验证通过才写PUBLISHED_VERIFIED。

## 许可证与恢复

会员中心登记同一hotel_id及设备后下载签名许可证，`license --file license.json`验证并导入。免费功能不需要付费许可证。公钥随包发布；私钥只保留服务器。报告、内容和策略使用实际有效权益，客户端不能只改plan参数解锁。离线许可最长24小时，退款或设备停用后不续发；离线客户端在许可到期前存在最长24小时刷新窗口。

pause/resume仅改变工作区写动作状态。异常写入保留UNKNOWN_PENDING_READBACK。锁存在时先核对执行器是否仍运行，不能为了重试删锁；没有人工/PMS后续变更且当前值仍是本次写入值，才可生成恢复旧值的补偿提案。订单产生的后果不能靠改回价格撤销。

## 验收口径

各维度分别记录，见status.json。演示文件、单元测试、公开入口与真实酒店操作不能相互替代。实际账号尚未核验的项目保留待验收状态，不能宣传全面支持。
# 持续运行、价格策略与内容日程

## 设备许可与续取

运行`node scripts/ops.mjs device`获取本机随机设备ID；在官网会员中心登记同一ID并下载许可证，再通过`license --file ... --workspace ...`导入。设备身份保存在用户目录`.openlx-ctrip-device/id`，不能随酒店工作区复制到其他电脑。付费许可绑定酒店、设备和有效期。

许可证文件含设备续取凭据，按私密文件保存，不进入Git、报告或模型请求。`refresh-license --workspace ...`可手动刷新；守护运行在离线有效期不足6小时后自动续取。停用设备或退款撤销权益后，在线续取和写租约被拒绝；已发离线签名最多继续有效24小时。历史报告与免费本地数据不删除。

有登记许可的付费写任务在本地单店锁之外取得服务器单店写租约，每30秒续租，提交前再次校验。另一个登记设备在租约有效期内不能同时写入。免费未登记工作区只具备本机串行约束，跨电脑运行应明确唯一写设备；不可复制Chrome Profile到两台电脑同时执行。真实两设备后台并发仍待账户实测。

单次扫描：`node scripts/ops.mjs run --workspace /path/to/hotel-work`。持续运行：`node scripts/daemon.mjs --workspace /path/to/hotel-work`。加`--once`只跑一轮。Ctrl+C或SIGTERM正常退出；进程锁避免同工作区重复启动，`daemon-status.json`记录心跳。设备关机时不会监控，恢复只处理当前一轮和当日一篇，不堆积补发。当前发行未自动修改操作系统开机任务，可由宿主以登录用户运行该进程。

好评定时在hotel.json中配置`positive_review_opt_in=true`和实际授权到期时间`review_authorization_until`；默认60分钟。差评与含混点评不能靠该开关自动回复。

标准及至尊自动价格策略：先把包含`hotel_id`、`mode=AUTOMATIC`、有效期、房型日期和金额护栏的完整策略保存到文件。核对最终JSON的SHA-256后运行`authorize-pricing --file <file> --hash <hash> --workspace <dir>`。运行器只执行该摘要绑定的策略；改动策略后原授权不覆盖新范围。多信号策略使用`strategy=MULTI_SIGNAL`，仍需至尊许可与至少两种有效信号，PMS权威字段不在携程后台自动改写。

至尊日程在hotel.json配置`content_schedule`：`enabled`、`hour`（本地目标小时，默认10）、`timezone`（默认Asia/Shanghai）、`asset_folder`、`topics`和`mode`（RULE或MODEL）。默认只准备当天一篇，生成后不会重复创建。报告、点评、价格、内容分别捕获失败，互不升级为全局阻塞。

规则内容的持续发布可单次配置有效`publish_policy`，包含实际`hotel_id/account_id/valid_until`、已认可的`facts_hash`、`persona_hash`、`allowed_asset_hashes`及`authorized_topics`，并开启`auto_submit`。该范围与实测账户映射匹配时按当前规则稿提交，随后查询后台与公开状态。新模型正文仍需确认最终内容。不能以此配置样例当作用户已经授权发布；实际账号映射和提交权限须另有实测证据。

用户选择模型后，在酒店工作区创建`model.json`：`endpoint`为用户选定的Chat Completions兼容URL，`model`为模型名，`api_key_env`为保存密钥的环境变量名，`cost_acknowledged=true`表示已经了解该服务费用；可设`max_output_tokens`。只允许HTTPS或本机回环HTTP，不复用浏览器Cookie。`content --model`启用模型正文；请求仅含核实事实和必要人设字段，不发送订单、点评原始页、图片或凭证。模型输出记录用量和输入摘要，引用不存在事实会被拒绝；所有模型正文保持待确认，不把引用校验当作完整语义验证。

提交后连接中断，运行`node scripts/ops.mjs readback --id <action-id> --workspace <dir>`读取原对象。暂停写入时该命令仍可运行；记录VERIFIED、NOT_APPLIED或CONFLICT。不会自行将未知提交重试。笔记使用`notes.mjs readback/public`分别查询后台与公开页面。
