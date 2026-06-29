---
name: promotion-apply-skills
description: 灵渠 Banner 推广创建、查询、复制、修改、状态修改、创意和关联物料 skill。用户说“配置发现页 banner”“帮我配置发现页banner”“查询/复制/创建/预占/取消预占/状态修改/修改/配置 banner 推广/素材”时使用。
metadata:
  version: 1.0.0
---
# Promotion Apply Skills

## MWS 使用

使用 `mws` 前按以下规则执行：

- 首次使用先 `which mws` 确认命令可用；不要自动执行 `mws update`。只有用户明确要求更新 MWS 时才更新。
- 不熟悉的方法必须先 `mws schema <method>`。
- 写操作先 `--dry-run` 做本地 schema 校验，再执行真实写入。
- NOS 对象存储上传：通过 `mws link backend-nos-token-whalealloc` 拿到 token 后，可按 [references/image-upload-nos.md](references/image-upload-nos.md) 直传到 NOS。
- 需要用 Python 解析 MWS 输出时，不要写 `mws ... | python3 - <<'PY'`，因为 here-doc 会占用 Python stdin，导致管道里的 MWS JSON 丢失。应使用 `mws ... --format json > /tmp/xxx.json` 后让 Python 读文件，或使用 `mws ... --format json | python3 -c '...'`。

如果不确定 MWS 命令语法、鉴权、参数格式或输出处理，参考 [references/mws-shared.md](references/mws-shared.md)。该文档只作为 MWS 通用参考，推广业务流程以本 skill 为准。

## 强制规则

1. 推广新增调用 `mws link promotion-add`，推广查询调用 `mws link promotion-list` / `mws link promotion-detail`，推广复制调用 `mws link promotion-copy`，推广修改调用 `mws link promotion-update`，状态流转调用 `mws link promotion-transition`，物料保存调用 `mws link promotion-update-creative`。
2. 添加创意/素材前必须先获取推广详情里的可投放资源树 `deliveryResourceList` 和已选投放端；投放类型优先取用户本轮已明确选择的资源类型，其次取详情里的 `resourceTypes` / `relatedResourceTypes`。人工创建或历史推广详情缺少 `fullType/resourceTypes/resourceInfo` 时，先把缺失项作为“素材更新前置补问”问用户，不能用 `deliveryResource` 标签、上游 URL 或旧创意反推。不同投放类型、不同端对应不同模板，禁止复用另一端或上一轮的 `templateSchema`。保存素材时必须把投放类型规范化后随 `promotion-update-creative` 一起提交：`resourceType`=二级类型，`resourceTypes`=二维数组，`resourceInfo`=资源 ID 或空字符串。
3. 图片字段必须从模板 `conditionConfig` 解析宽高后做本地像素校验；不要凭经验写死尺寸。
4. 时间必须使用 `yyyy-MM-dd HH:mm:ss`，不要使用 ISO8601 `T` 格式。用户只给日期时按自然日闭区间落时间：开始日 `00:00:00`，结束日 `23:59:59`；例如“0612 到 0613 / 0612 0613 2天”落为 `2026-06-12 00:00:00` 至 `2026-06-13 23:59:59`，不要改成 `2026-06-14 00:00:00`。排期预占只有跨自然日时才可能拆分；同一天内的小时段（例如 8:00-12:00）必须保持 1 条排期，不追问拆分。跨自然日时必须先让用户在“拆分”和“不拆分”两个选项里选择，不能未经确认直接拆，也不能只给建议后默认执行。给用户展示推荐拆分方案时用纯文本换行或列表，不要输出 `<br>` 这类 HTML 字符串。默认推荐首日保留用户开始时间到当天 `23:59:59`，中间日 `00:00:00` 到 `23:59:59`，末日 `00:00:00` 到用户结束时间；用户选择不拆分时按原始连续 `startTime/endTime` 创建 1 条推广。最多 7 个自然日，超过 7 天必须让用户缩短或拆分。`endTime` 必须晚于 `startTime` 且在未来。
5. 机器人/数字员工代创建时，必须在写入前先算好管理员补权限名单，名单 = 本轮真实发起人邮箱前缀 + 群聊里真实被 @ 的协作者邮箱前缀，去重后排除 `grp.` 账号、机器人账号和完整邮箱域。`promotion-add` 成功拿到推广 ID 后，第一件事就是调用 `mws link admin-add` 追加这些人为推广普通管理员；该步骤必须发生在 `promotion-detail`、提取模板、保存素材和成功回复之前。不要等素材保存完成后再补；不要用 `admin-update` 重写管理员列表。如果无法识别真实发起人，创建前就把“真实发起人邮箱前缀”列为缺失项补问，不能写入后跳过。复制推广成功后只补本轮真实被 @ 的协作者：有 @ 人时用新推广 ID 先查管理员，缺谁就 `admin-add` 追加谁；没有 @ 人就跳过。修改推广、状态流转、保存物料或其它非创建/复制写操作都不做 `admin-add`。
6. 群聊里需要 @ 人时，必须使用 POPO 群消息工具真实 @ 能力；不要只写文本形式的邮箱。
7. 创建或修改推广前必须拿到本轮任务的完整业务字段；但能从本轮用户短句、当前登录/会话身份、接口配置和“运营轻量推断规则”高置信推断出的字段，不要再追问用户填一遍。禁止使用示例值、默认测试值、上一轮/记忆里的推广字段或无依据猜测。用户只说“创建推广”且无法推断关键字段时，先列出缺失字段并等待用户补充；用户一次性给齐字段或可推断字段且明确要求执行时，不要重复确认同一批字段。
8. 默认按两阶段执行：第一阶段创建推广并预占，创建入参可以先不包含实际投放资源类型、资源 ID、全量/非全量和人群；这些初始化字段允许在第二阶段配物料前补齐。第二阶段先确认资源类型、资源 ID（标准资源时）、全量/非全量，非全量再确认人群，然后获取资源默认值、提取模板、收集并保存素材。用户明确说“只预占/先占排期/暂不配置物料/素材后补/只做第一步”时，完成创建、预占、管理员补权限和详情核验后即可结束，不强制进入素材引导；回复里说明后续可继续补物料。只有用户一次性给齐“创建推广 + 实际投放资源 + 全量/非全量 + 各端素材”时，才按依赖顺序一次性执行完整链路；不要人为拆成多轮。创建后默认预占，不需要把“是否预占”作为必答项。信息不齐时，只做一次轻量补问：先展示“我已识别/推断”的字段，再只问真正缺的字段；不要把完整字段表一次性丢给运营。四个业务标签只有在缺失且无法推断时才展示完整选项；已经推断或用户已按顺序给出时，只在确认摘要中展示结果。
9. 项目负责人 `projectOwner` 和创建人二级部门 `creatorDept` 的默认值取决于当前执行身份：如果能从当前会话真实发起人或登录态拿到项目负责人邮箱前缀，就直接使用，不再让运营填写。创建人二级部门在“运营审核机器人/龙虾代创建且属于本部门推广”场景默认 `内容运营部`；其它 `grp.` 前缀群组或机器人身份如果不能确认本部门场景，`projectOwner` 必须让用户输入真实项目负责人邮箱前缀，`creatorDept` 也必须让用户输入真实二级部门。只有当前执行身份不是 `grp.` 前缀时，才可以默认当前用户邮箱前缀和当前用户二级部门。
10. 本 skill 禁止使用长期记忆、历史测试记录、上一条推广详情或旧对话里的素材/人群/资源作为当前任务默认值。所有字段只能来自本轮用户明确输入、当前 `promotion-detail`、当前模板接口和本轮 MWS 返回。图片、视频、NOS URL、角标、跳转链接等素材也不能复用上次任务或上一轮对话里的值；只有用户在本轮明确说“这张图所有端共用”“沿用当前推广已有素材”时，才允许在本轮当前推广内复用。用户本轮给的任意图片 URL（包括 NOS、NOSK、`mb-mlbclaw-pub`、`nos-jd`、`p5.music.126.net` 等看起来已上传的地址）都只能当作原始素材，不能直接写入创意 payload；必须先下载到本地，按当前模板校验/裁剪确认，再通过本轮 `backend-nos-token-whalealloc` + NOS 上传得到最终 URL。
11. 环境是独立上下文字段：用户明确预发布时使用 `pre`，用户明确线上或未说明环境时默认 `online`。同一任务里后续 MWS 调用沿用该环境；允许复用的只有同一任务内最近一次明确环境，不允许从长期记忆或其他推广任务复用环境。
12. 真正执行时不能依赖本地前端/后端仓库代码排查。`--dry-run` 只代表 schema 形状通过，不代表物料业务结构正确；物料保存必须先跑本 skill 的 `scripts/validate_update_creative_payload.py`。如果没有当前 `promotion-detail` 文件和预检脚本通过结果，禁止调用 `mws link promotion-update-creative --dry-run` 和真实写入，也禁止对用户说“业务层两种结构都挂/建议后端确认服务状态”。遇到 MWS dry-run 通过但真实调用失败时，先按本 skill 的错误检查表处理；仍无法定位时，报告 MWS 方法、关键入参摘要和错误信息，不要临时翻代码猜字段。禁止绕过 MWS 直连 Link 平台 HTTP 接口；标准资源默认值只能通过 `mws link plan-pack-resource-list` 调用，参数名必须是 `resourceIds`（复数），不能用 `resourceId` 单数。
13. `promotion-update-creative` 是 AI 物料更新接口，path 为 `/api/link/platform/ai/promotion/updateCreative`，已内嵌 `updateCreativeCheck`。当前 schema 接收 `id`、`promotionAliasCreativeList`、`fullType`、`resourceType`、`resourceInfo`、`resourceTypes`、`strategyInfo`、`businessRemark`、`relateTask`。保存物料时必须把第一阶段已确认的投放信息带下来一起传：`fullType/resourceType/resourceInfo/resourceTypes`，非全量再传 `strategyInfo` JSON 字符串。用户在素材阶段修改了资源或投放量，就用修改后的值；没有修改就沿用第一阶段创建/详情里的值直接传上去。人工创建、历史推广或已有预占推广缺失这些字段时，先让用户补齐实际投放资源类型、标准资源 ID（标准资源时）、全量/非全量和非全量人群，再用同一套资源选择/默认值/模板逻辑组包；这是素材更新前置补问，不要直接引导重建或服务端修复，也不要调用 `promotion-update` 后补。关联艺人不是 `promotion-update-creative` 的入参，配物料/更新物料时不要把“关联艺人为空”列为阻塞项；只有创建/修改推广基础信息且当前项目类型配置 `needArtist=true` 时才补问艺人。禁止把空 `fullType`、空 `resourceTypes` 或猜出来的资源类型传给接口。更新/换物料时也必须重新跑标准资源默认值获取和链接校验，不能直接信任上游或旧创意带来的 URL；标准资源必须先调用 `plan-pack-resource-list` 获取默认值，再按每个端调用 `data-template-extract-private`，在模板 `preData` 基础上填充，禁止用资源 ID 手拼 `https://music.163.com/...`。只有 Web 端跳转链接必须是 http/https，缺失时补问用户，禁止用 `orpheus` 兜底；非 Web 端必须使用资源/模板返回的客户端默认链接（如 `composedData.commonComposedData.url`、`orpheus` 或模板 `preData`），缺失时问用户提供端维度链接，不能用 Web 链接兜底。保存前必须把所有折叠端最终跳转链接发给用户确认，用户确认后才运行 `promotion-update-creative`。`resourceType` 是二级类型字符串，例如 `song/activity`；`resourceTypes` 是二维数组，例如 `[["standard","song"]]` / `[["nonstandard","activity"]]`；`resourceInfo` 标准资源传资源 ID，非标通常传空字符串。不要传 schema 不存在的 `op/crowdIds/forceSave` 顶层字段。命中审批码 `31003`（`PROMOTION_UPDATE_CREATIVE`）时，不要再找单独的 check/approval 方法；未传 `businessRemark` 时接口会返回 `needApproval=true`，此时向用户要审批说明后，原物料参数补 `businessRemark` 重试，接口会自动发起 `updateCreativeApproval`。用户本轮明确给了需求单时，可同时传 `relateTask`；不要猜。
14. 全流程禁止使用 `creative-add`。创建创意、添加创意、关联素材、验证创意结构、失败重试都不能调用 `creative-add`，也不能先创建独立创意再关联推广。物料保存只能使用 `mws link promotion-update-creative`，由该接口在推广物料保存时处理创意和素材。如果用户、上游或机器人给出一整段 `mws link promotion-update-creative --json ...`、`{method:"updateCreative",param:[...]}`、`promotionAliasCreativeList`、`promotionCreativeList`、`creativeDetailDataVO` 或 `templateSchema` 成品包，必须视为绕过本 skill 的错误输入：不要原样执行，也不要只补 `name/tenant/resourceInfo` 后继续；必须拆回业务输入，重新查 `promotion-detail`、获取默认值、提模板、下载并重传图片、生成完整创意并跑预检。也禁止把同一个成品包改成“拍平结构/嵌套结构/换 token 接口/换 raw HTTP”轮流试；这种试错本身就是绕过。该方法真实调用返回 404、method not found、未注册或其它环境路由问题时，不能改用 `creative-add`、`promotion-update`、`mws_exec`、`raw_call`、curl/HTTP 直连或任何其它接口绕过；只能检查当前 MWS 方法名、环境、schema 和参数，能修参数就用同一个方法重试，不能修就报告该 MWS 方法在当前环境不可用和原始错误。也不能为了验证创意结构创建一个新的测试推广。
15. 对话输出只说用户需要知道的结论、缺失项、阻塞点和最终结果。不要向用户播报内部流水、参数试错和自我纠错，例如“收到，校验配置和资源”“位置校验无关人群，跳过直接创建”“strategyInfo 需为对象非字符串，修正重试”“创建成功，查详情”。参数修正、重试和详情查询都应在内部完成；只有创建后的必做步骤（尤其是 `admin-add`）完成后，才能说“推广创建完成”；复制推广如果本轮有真实 @ 协作者，必须完成或明确说明管理员追加失败后才能说“推广复制完成”。修改、状态流转、素材保存不触发 `admin-add`。耗时超过 30 秒时可发一句合并进度，但不得暴露内部试错。

16. 如果 `promotion-update-creative` 后端堆栈包含 `Column 'name' cannot be null`、`Music_Link_Creative` 插入失败、`name ... null`，这是 `creative.name` 缺失，不是数据库问题。立即停止原 payload 重试，按 [references/creative-dynamic-material.md](references/creative-dynamic-material.md) 的“创意名称生成”规则重新生成每个折叠端唯一 `creative.name`，并同时确认 `tenant=music`、`dataTemplate.id`、完整 `templateSchema`、完整 `creativeDetailDataVO` 都存在后再预检。

17. 如果 payload 里把 `移动端(iPhone&Android)/荣耀白牌/iPad(新版)/AndroidPad` 拆成多个节点（例如单独提交 `荣耀白牌`、`iPad(新版)`、`AndroidPad`），但当前 `promotion-detail.promotionAliasTemplateList` 只返回折叠后的 `移动端(iPhone&Android)` 节点，必须判定为折叠端错误。保存节点只能等于详情里的折叠端列表，`positionAliasShow` 必须从详情同节点复制，不能是 null。

18. 每次进入配物料、补配物料或换物料，都必须先清空上一轮配置缓存：不要复用浏览器页面中残留的表单物料、旧 `/tmp/promotion-detail.json`、旧模板提取结果、旧 `plan-pack-resource-list`、旧 payload、旧 NOS 上传结果或上一轮裁剪图。为当前推广创建唯一工作目录，例如 `WORKDIR=/tmp/lingqu-banner-${promotionId}-$(date +%Y%m%d%H%M%S)`，所有详情、默认值、模板、图片处理、payload 和预检文件都写在该目录内；第一步重新查当前 `promotion-detail`。如果发现页面上显示了其它人的旧物料，不能据此判断当前配置，也不能沿用，必须重新拉详情并按本轮素材覆盖。

## 当前可用 MWS 方法

```bash
mws schema link.promotion-add
mws schema link.pms-login-status
mws schema link.promotion-list
mws schema link.promotion-copy
mws schema link.promotion-update
mws schema link.promotion-detail
mws schema link.promotion-transition
mws schema link.promotion-update-creative
mws schema link.promotion-position-alias
mws schema link.promotion-admin-info
mws schema link.promotion-tag-config
mws schema link.promotion-type-list
mws schema link.promotion-artist-list
mws schema link.plan-check
mws schema link.admin-get
mws schema link.admin-add
mws schema link.component-code
mws schema link.data-template-extract-private
mws schema link.position-channel-data-template
mws schema link.template-detail-get
mws schema link.plan-pack-resource-list
mws schema link.backend-nos-token-whalealloc
```

常用调用名：

```bash
mws link promotion-add --env ${MWS_ENV} --reason "创建推广" --json '{...}'
mws link pms-login-status --env ${MWS_ENV} --format json
mws link promotion-list --env ${MWS_ENV} --reason "查询推广列表" --json '{...}'
mws link promotion-copy --env ${MWS_ENV} --reason "复制推广" --json '{...}'
mws link promotion-update --env ${MWS_ENV} --reason "修改推广" --json '{...}'
mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000577801"}'
mws link promotion-transition --env ${MWS_ENV} --reason "推广状态流转" --json '{...}'
mws link promotion-update-creative --env ${MWS_ENV} --reason "保存推广物料/创意" --json '{...}'
mws link plan-check --env ${MWS_ENV} --reason "校验人群包" --json '{...}'
mws link admin-get --env ${MWS_ENV} --json '{...}'
mws link admin-add --env ${MWS_ENV} --reason "追加推广管理员" --json '{...}'
```

## 环境

环境必须作为独立信息处理，不能隐式默认。

| 用户说法 | `MWS_ENV` |
|---|---|
| 预发 / 预发布 / pre | `pre` |
| 线上 / online | `online` |

执行任一业务 MWS 命令前，先确定当前任务环境并设置变量：

```bash
export MWS_ENV=pre      # 用户明确选择预发布时
export MWS_ENV=online   # 用户明确选择线上或未说明环境时
```

规则：

- 用户可以直接说“环境预发布”或“环境线上”；同一推广任务后续命令都沿用这个环境。
- 如果用户没说环境，默认 `online`，不要补问。
- 所有示例里的 `${MWS_ENV}` 都代表当前任务环境；未说明时为 `online`。

## 时间拆分确认

跨自然日排期不能自动拆分。创建或修改前必须先向用户确认，并只给两个明确选择：

```text
这个时间跨 3 天，我建议拆成：
- 6/17 00:00:00 至 23:59:59
- 6/18 00:00:00 至 23:59:59
- 6/19 00:00:00 至 23:59:59

请选择：
1. 拆分：按上面 3 条分别创建/预占
2. 不拆分：按 6/17 00:00:00 至 6/19 23:59:59 创建 1 条
```

规则：

- 等用户明确选择后再执行；用户未选择时不能默认拆分或默认不拆分。
- 推荐方案用 Markdown 列表或纯文本换行展示，禁止输出 `<br>` 字符串。
- 用户选择不拆分时，只提交原始连续 `startTime/endTime`。
- 用户选择拆分时，每条按自然日拆成独立时间段；首日保留原开始时刻到当天 `23:59:59`，中间日为整天，末日为 `00:00:00` 到原结束时刻。
- 拆分创建多条推广时，推广名称必须带日期后缀便于区分。后缀插在部门后缀前，例如原名 `【头部/首发/艺粉/单曲】线上测试 –【技术中心】`，拆成单日后分别提交 `【头部/首发/艺粉/单曲】线上测试-6.17 –【技术中心】`、`【头部/首发/艺粉/单曲】线上测试-6.18 –【技术中心】`。如果某条覆盖多日，使用 `-6.17-6.19`。追加后仍必须满足名称长度限制；超长时先让用户确认缩短基础名称。

## 投放端配置

用户只需要感知“投放端”，例如“移动端、PC、Web、荣耀白牌”。内部调用时再把投放端转换为 `relatedPositionCodes`。不要让用户直接填写或确认 `PAGE_DISCOVERY_BANNER@mobile` 这类 code。

Banner 投放端配置来自接口，不要在 skill 中写死，也不要说来源是配置中心。创建、修改、提取模板前必须调用：

```bash
mws link promotion-position-alias --env ${MWS_ENV} --params '{"biz":"banner"}' --format json
```

接口返回是标准 `code/data/message` 结构；真实端配置在 `data[]` 中。每项包含 `positionAlias`、`positionCode`、`channelCode`，用户只选择 `positionAlias`，内部再使用 `positionCode/channelCode`。

当前接口 `data[]` 常见返回如下，仅作说明；真实值以接口返回为准：

| 接口返回 `positionAlias` | 内部 `positionCode` | 内部 `channelCode` |
|---|---|---|
| 移动端(iPhone&Android) | `PAGE_DISCOVERY_BANNER@mobile` | `page_discovery_banner_channel` |
| 荣耀白牌 | `PAGE_DISCOVERY_BANNER@magios` | `page_discovery_banner_channel_magios` |
| PC | `BANNER_PC_V2` | `pc_banner_op_channel` |
| Web | `BANNER_WEB` | `web_banner_op_channel` |
| Mac | `BANNER_MAC` | `mac_banner_op_channel` |
| iPad(新版) | `PAGE_DISCOVERY_BANNER@newIpad` | `page_discovery_banner_channel_new_ipad` |
| AndroidPad | `PAGE_DISCOVERY_BANNER@androidPad` | `page_discovery_banner_channel_android_pad` |
| iPadHD(旧版) | `BANNER_IPAD_HD` | `ipad_hd_banner_op_channel` |

用户给投放端时，先用 `promotion-position-alias` 返回值转换为 `relatedPositionCodes`，用英文逗号拼接。转换失败时停止并提示哪个端没有配置。

默认客户端/投放端是 4 个：移动端(iPhone&Android)、荣耀白牌、PC、Web。用户未明确指定客户端/投放端时，按这 4 个端创建；用户明确指定“全部”或其它端时，以用户本轮选择为准。

默认 4 个客户端/投放端：

```text
移动端(iPhone&Android), 荣耀白牌, PC, Web
```

转换为：

```text
PAGE_DISCOVERY_BANNER@mobile,PAGE_DISCOVERY_BANNER@magios,BANNER_PC_V2,BANNER_WEB
```

## 推广基础字段

`promotion-add` 当前真实 schema 必填：

| 字段 | 规则 |
|---|---|
| `name` | 最终提交推广名称，格式为 `【内容大类/版权类型/战略类型/投放资源标签】推广基础名称 –【二级部门】`，长度不超过 50 |
| `projectName` | 项目名称，使用用户真实项目名 |
| `projectOwner` | 项目负责人邮箱前缀，不传完整邮箱；优先取当前会话真实发起人或当前登录用户。只有 `grp.`/机器人执行且无法确认真实发起人时才问用户 |
| `creatorDept` | AI VO 不直接传该字段；服务端从推广名称末尾 `–【二级部门】` 解析并写入。本部门龙虾/运营审核机器人场景默认 `内容运营部`；非 `grp.` 执行身份可从 `pms-login-status.data.depList[level=2].name` 取。其它 `grp.` 场景无法确认本部门时才问真实二级部门 |
| 投放端 | 用户选择的端，内部转换为 `relatedPositionCodes` |
| `startTime` / `endTime` | `yyyy-MM-dd HH:mm:ss`；只给日期时按自然日闭区间，开始日 00:00:00，结束日 23:59:59；同一天小时段不拆，跨自然日才可能按天拆分，最多 7 天；拆分前必须让用户在“拆分/不拆分”中二选一 |
| `contentCategory` | 内容大类 code |
| `copyrightType` | 版权类型 code，服务端 `@NotNull` |
| `strategyType` | 战略类型 code |
| `deliveryResource` | 投放资源 code |

常用可选字段：

| 字段 | 规则 |
|---|---|
| `biz` | 默认 `banner` |
| `projectType` | 从 `promotion-type-list` 获取，不能猜 code |
| `projectLevel` | 可传 `S+` / `S` / `A` / `B` |
| `projectBackground` | 项目背景，最长 500 |
| `fullType` | 全量传 `full`，非全量传 `nofull`；创建阶段可以不传，配物料/更新物料前必须补齐并随 `promotion-update-creative` 同包提交 |
| `priority` | 默认 0，数值越小优先级越高 |
| `relatedResourceTypes` | 关联资源类型，英文逗号串；用户选择标准/歌曲并给歌曲 ID 时传 `song` |
| `relatedResourceIds` | 关联资源 ID，英文逗号串；标准资源 ID 创建阶段可以不传，配物料/更新标准资源素材前必须补齐并随 `promotion-update-creative` 同包提交 |
| `strategyInfo` / `crowdList` | 非全量人群创建阶段可以不传，配物料/更新物料前必须补齐；`strategyInfo.crowd.op` 使用 `contain/notcontain`，`crowdList[].type` 使用 `include/exclude`；物料保存阶段非全量固定给 `promotion-update-creative` 传 `strategyInfo` JSON 字符串，不传 `crowdList` |
| `promotionAliasCreativeList` | 创建时可附带创意/物料列表 |
| `autoPreoccupy` | 默认创建后自动进入预占；用户明确说不预占时才不传 |
| `promotionArtistList` | 项目类型 `needArtist=true` 时必填，必须是完整艺人对象列表；不能只传 `artistIds` |

保密项目默认“否”。创建/修改入参不传 `secret`。

项目等级选项：

| 展示 | 提交值 |
|---|---|
| S+ | `S+` |
| S | `S` |
| A | `A` |
| B | `B` |

项目类型必须调用 `mws link promotion-type-list` 获取当前配置。常见展示项如下，最终以接口返回的 `type` code 为准：

| 展示名 | 说明 | 关联艺人 |
|---|---|---|
| 歌曲版权宣发 | 常规歌曲宣发/版权合作或回归/内容营收项目/版权合作延伸活动 | 需要 |
| 艺人合作宣发 | 艺人参与的空降翻牌评论区/一起听/乐迷团/笔记/专访/播客等形式站内活动 | 需要 |
| 营收 | 会员促销项目/商业化合作项目 | 按接口 `needArtist` |
| 活动推广 | 品宣类策划/用户参与类玩法/品牌联动/内容征集活动等 | 按接口 `needArtist` |
| 热点 | 常规节日、节气、纪念日及突发文娱类社会热点承接内容 | 按接口 `needArtist` |
| 有声书ip推广 | 有声书 IP 推广 | 按接口 `needArtist` |
| 其他类型 | 政府/GR 指示内容或其他特殊需求 | 按接口 `needArtist` |

### 关联艺人完整信息

项目类型 `needArtist=true` 时，创建和修改都必须提交完整 `promotionArtistList`，不能只提交 `artistIds`。完整对象至少保留前端详情/艺人接口可拿到的字段：

```json
{
  "artistId": 10559,
  "artistName": "张惠妹",
  "score": 831,
  "area": "华语",
  "level": "S",
  "musicianScore": 726
}
```

处理规则：

- 新建时，用户只给艺人 ID 后，必须调用 `promotion-artist-list` 校验并把返回的完整对象写入 `promotionArtistList`。
- 修改已有推广时，先查 `promotion-detail`。如果用户没有修改艺人，沿用详情里的 `promotionArtistList` 完整对象；如果用户修改了艺人 ID，必须重新调用 `promotion-artist-list` 拿完整对象后再提交。
- 入参里可以保留 `artistIds` 作为前端选择辅助，但真正保存必须同时带完整 `promotionArtistList`；MWS/AI 写入时优先以 `promotionArtistList` 为准。
- 如果 `promotion-artist-list` 或详情只返回了部分字段，提交时保留接口返回的全部字段，不要只构造 `{ "artistId": xxx }`；拿不到 `artistName` 等关键信息时停止并说明艺人详情不可用。

业务标签必须给出选择，不能让用户猜 code，也不能在 skill 中硬编码选项。创建或修改推广前必须调用统一配置接口：

```bash
mws link promotion-tag-config --env ${MWS_ENV} --reason "查询推广业务标签配置" --format json
```

该接口返回四组配置：

| 返回字段 | 对应入参 | 展示/提交规则 |
|---|---|---|
| `contentCategoryOptions` | `contentCategory` | `label` 给用户选择，`code` 用于提交 |
| `copyrightTypeOptions` | `copyrightType` | `label` 给用户选择，`code` 用于提交；服务端必填 |
| `strategyTypeOptions` | `strategyType` | `label` 给用户选择，`code` 用于提交 |
| `deliveryResourceOptions` | `deliveryResource` | `label` 给用户选择，`code` 用于提交；这是推广基础里的“投放资源标签”，不是实际投放资源类型 |

如果 `promotion-tag-config` 调用失败、返回为空、或用户选择的中文项不在返回列表中，停止并说明“推广业务标签配置不可用或选项不存在”，不要使用文档里的旧示例值兜底。

示例入参片段：

```json
{
  "contentCategory": "strategy",
  "copyrightType": "exclusive",
  "strategyType": "kpop",
  "deliveryResource": "mv"
}
```

`copyrightType` 是必填字段，不能省略。示例中的 code 只展示提交结构，真实选项必须来自 `promotion-tag-config`。
`deliveryResource` 是推广基础的业务标签，只用于描述这次推广偏 H5/MV/专辑/单曲等标签归类；它不等于后续素材/资源链路里的实际投放资源类型。实际投放资源类型要单独收集，例如“标准/歌曲 + 歌曲 ID”或“非标/活动”。

用户连续给出四个业务标签时，按固定顺序解析为：内容大类、版权类型、战略类型、投放资源标签。轻量模式下不要默认完整展示四组可选项；只有用户不知道怎么填、选项无法匹配、或业务标签缺失且不能推断时，才展示下面的完整选项。真实提交前仍以 `promotion-tag-config` 返回为准：

```text
内容大类：头部 / 战略 / 潜力 / 品牌
版权类型：自制 / 独家 / 首发 / 全网 / 后发
战略类型：艺粉 / Kpop / 嘻哈 / 欧西 / 日音/二次元 / 其他
投放资源标签：H5 / MV / 专辑 / 数字专辑 / 歌单 / 单曲 / 长音频 / 直播 / 其他
```

用户也可以按顺序简写。例如用户说“头部 独家 其他 其他”，表示：

```text
内容大类：头部
版权类型：独家
战略类型：其他
投放资源标签：其他
```

只要四个值都能在 `promotion-tag-config` 返回的选项中匹配，就直接转 code；不要再提示用户补这四项。若只有部分值无法匹配，只提示无法匹配的那几项和可选项，不要整组重问。

## 运营轻量推断规则

面向运营创建推广时，优先按 [references/phase-one-reserve.md](references/phase-one-reserve.md) 从自然语言短句推断字段，减少补问。执行阶段一创建/预占前必须先读该引用文档。

高频规则摘要：

- 运营/申请人必须提供：项目名称、项目等级、时间段。
- 数字员工自动解析：项目类型、投放资源标签、客户端、投放量；推广名称由四个前缀字段和项目核心名生成，不让运营/申请人手工拼完整字符串。
- 项目负责人默认项目申请人 + 王可；如果当前接口只支持单个 `projectOwner`，`projectOwner` 用当前会话真实发起人，王可按后台支持字段或管理员补权限处理。本部门龙虾/运营审核机器人场景创建人二级部门默认 `内容运营部`。
- 歌曲 / 数字专辑 / 数字单曲 / 歌单 / 专辑 / MV 默认全端、全量。
- 空降 / 有票默认非全量，只投移动端、荣耀白牌、iPad(新版)、AndroidPad，并需要人群包 ID。
- H5 活动 / 其他活动（实体专辑）默认移动端、荣耀白牌、PC、Web、iPad(新版)、AndroidPad。
- 只有跨自然日排期才可能拆成逐日排期；同一天 8:00-12:00 这类小时段不拆。跨自然日最多 7 天，必须先给“拆分/不拆分”两个选项并等用户选择；用户可选择推荐拆分、每天同一时段或不拆。
- 笔记类即使说全选，也自动排除荣耀白牌。
- 空降 / 有票四个名称前缀固定为 `潜力 / 全网 / 其他 / 其他`，不要再问运营/申请人。
- 其它资源类型只补问无法推断的内容大类、战略类型、版权类型和必要艺人 ID。

推断后仍必须用 `promotion-tag-config`、`promotion-type-list`、`promotion-position-alias`、`deliveryResourceList` 等接口校验当前配置是否存在，不能跳过接口校验。

轻量补问原则：

1. 已能推断的字段不要再问；只在摘要里展示。
2. 标准资源必须最终拿到资源 ID；如果用户只说“王力宏新歌”但没给歌曲 ID，先提示“我已按标准/歌曲处理，还差歌曲 ID”。如果当前没有搜索资源的 MWS 能力，就只问歌曲 ID。
3. 非全量默认只由“空降/有票”触发；此时只补问人群包 ID 和包含/不包含。
4. 回复尽量控制在一屏内。不要默认输出完整字段表、接口字段名、内部 code、长示例 JSON。
5. 用户要求“看看有哪些选项”“我不知道怎么填”时，才展开完整可选项。

## 创建推广

创建前必须拿到推广基础字段，或能按“运营轻量推断规则”推断出对应值。资源类型、资源 ID、投放量和人群属于物料初始化字段：创建/预占阶段可以没有，配物料、直接修改或换物料提交 `promotion-update-creative` 前必须补齐。

| 字段 | 必填性 | 可选项/默认 | 说明 |
|---|---|---|---|
| 推广基础名称 | 必填 | 用户输入 | 用户只需要填写中间主体，例如 `云打歌企划x限定`；最终提交 `name` 会自动拼成 `【内容大类/版权类型/战略类型/投放资源标签】推广基础名称 –【二级部门】`，长度不超过 50 字 |
| 环境 | 必填，有上下文 | 预发布 / 线上 | 首次必须让用户选择；同一任务后续沿用已确认环境 |
| 项目名称 `projectName` | 必填 | 用户输入 | 使用真实项目名 |
| 项目负责人 `projectOwner` | 必填，可自动 | 优先取当前会话真实发起人邮箱前缀；非 `grp.` 执行身份也可取当前登录用户邮箱前缀；取不到才问 | 不传完整邮箱 |
| 创建人二级部门 `creatorDept` | 必填，可自动 | 运营审核机器人/龙虾本部门场景默认 `内容运营部`；非 `grp.` 执行身份优先从 `pms-login-status.data.depList[level=2].name` 取；其它 `grp.` 场景取不到才问 | `PromotionAiAddVO` 没有独立字段，必须拼到最终推广名称末尾：`推广名称 –【内容运营部】`；服务端从名称解析 |
| 客户端/投放端 | 必填，有默认 | 优先按实际投放资源类型推断；无法推断时默认：移动端(iPhone&Android) / 荣耀白牌 / PC / Web；可选：全部 / Mac / iPad(新版) / AndroidPad / iPadHD(旧版) | 用户只选择端，skill 内部换算 code |
| 起止时间 | 必填 | 用户输入 | `yyyy-MM-dd HH:mm:ss`；只给日期时按自然日闭区间。同一天小时段不拆；跨自然日才可能拆成逐日排期，最多 7 天；拆分前必须让用户在“拆分/不拆分”中二选一，超过 7 天停止并请用户缩短或拆分 |
| 项目等级 `projectLevel` | 必填 | `S+` / `S` / `A` / `B` | 需要让用户选择 |
| 项目类型 `projectType` | 必填 | 调 `promotion-type-list` 返回的选项 | 选择项 `needArtist=true` 时必须收集艺人 ID |
| 保密项目 | 默认确认 | 默认否 | 当前 AI VO 不传 `secret` |
| 内容大类 `contentCategory` | 必填 | 来自 `promotion-tag-config.contentCategoryOptions` | 用户选 `label`，提交 `code` |
| 版权类型 `copyrightType` | 必填 | 来自 `promotion-tag-config.copyrightTypeOptions` | 用户选 `label`，提交 `code`，服务端必填 |
| 战略类型 `strategyType` | 必填 | 来自 `promotion-tag-config.strategyTypeOptions` | 用户选 `label`，提交 `code` |
| 投放资源标签 `deliveryResource` | 必填 | 来自 `promotion-tag-config.deliveryResourceOptions`，常见展示：H5 / MV / 专辑 / 数字专辑 / 歌单 / 单曲 / 长音频 / 直播 / 其他 | 这是推广基础的业务标签，用户选 `label`，提交 `code`；不要和实际投放资源类型混用 |
| 实际投放资源类型 | 第二阶段必填 | 标准/歌曲、标准/专辑、标准/歌单、标准/MV、标准/数字专辑、标准/长音频、标准/直播，或非标/活动 | 创建/预占阶段可以没有；如果创建时已提供可转换为 `relatedResourceTypes`，配物料/更新物料前必须确认 |
| 标准资源 ID | 阶段二条件必填 | 用户输入 | 创建/预占阶段可以没有；配物料、直接修改或换物料前必须提供，用于取资源默认值、提模板和提交 `resourceInfo` |
| 投放量 `fullType` | 第二阶段必填 | 全量 / 非全量 | 创建/预占阶段可以没有；配物料、直接修改或换物料前必须确认并提交 `full` / `nofull` |
| 人群包 | 第二阶段条件必填 | 人群包 ID + 包含/不包含 | 仅非全量必填；创建/预占阶段可以没有，配物料/更新物料前先 `plan-check`，再随 `promotion-update-creative` 提交 `strategyInfo` |
| 关联艺人 ID | 条件必填 | 用户输入 | 项目类型需要艺人时，调用 `promotion-artist-list` 校验并填 `promotionArtistList` |

## 一次性创建、预占、配置素材

用户可能一次性表达完整目标，例如“创建推广、投移动端和 PC、非标活动、全量、这些图片和链接都配上”。也可能先只给创建字段、后给素材。创建推广前可以不拿实际投放资源类型、资源 ID、投放量和人群；这些字段都可以第二阶段再补。进入素材保存、直接修改或换物料前，必须先拿到实际投放资源类型、资源 ID（标准资源时）、全量/非全量，非全量再拿人群，然后获取默认值、提取模板并让用户补模板要求的物料。

1. 先解析用户已给信息，分成三组：
   - 推广基础字段：环境、推广名称、项目名称、项目负责人、创建人二级部门、投放端、起止时间、项目等级、项目类型、四个业务标签（内容大类、版权类型、战略类型、投放资源标签）、关联艺人。先按“运营轻量推断规则”和登录/会话身份自动补齐；环境首次必须让用户选择；投放端未指定时先按实际投放资源类型推断，无法推断再用默认 4 个端；创建后默认预占，不在轻量补问中要求用户确认“是否预占”。同一天小时段不拆；跨自然日排期先给推荐拆分方案和“不拆分”方案，让用户二选一，最多 7 天；超过 7 天不创建，提示用户缩短时间或拆成多次。运营审核机器人/龙虾本部门场景默认创建人二级部门为 `内容运营部`；其它场景能从 `pms-login-status` 取则自动取，取不到才问用户。
   - 实际投放资源与投放量：一级资源类型（标准/非标）、二级资源类型（歌曲/活动等）、标准资源 ID、全量/非全量、非全量人群包 ID 和包含/不包含。这组如果本轮已给可以在 `promotion-add` 创建阶段写入；没给则留到素材阶段前置补问。这里的资源类型不是推广基础里的 `deliveryResource` 标签。
   - 素材字段：按投放端或端分组给出的图片、视频、角标、标题、跳转链接等。
2. 如果三组信息都齐，直接执行完整链路：
   - 查 `promotion-tag-config` / `promotion-type-list` / `promotion-artist-list`，把中文选项转 code。
   - `promotion-add --env ${MWS_ENV}` 创建推广；如果用户已给投放资源/资源 ID/投放量/人群，创建入参同时带 `relatedResourceTypes`、`relatedResourceIds`、`fullType`、`strategyInfo/crowdList`。默认带 `autoPreoccupy`，用户明确说不预占时才不带。跨自然日排期必须先得到用户对“拆分/不拆分”的明确选择；选择拆分后按每日时间片逐条创建/预占，选择不拆分时按用户确认的连续周期提交；不要静默替用户决定拆或不拆。
   - `promotion-add` 返回推广 ID 后，如果是机器人/数字员工环境，立即调用 `admin-add` 追加“真实发起人 + 本轮真实被 @ 协作者”为推广普通管理员；如果创建前无法识别真实发起人，则不应进入创建步骤。非机器人/数字员工环境或确实没有可追加人员时，必须明确记录跳过原因。这个步骤必须发生在查详情、提取模板、保存素材之前。
   - `promotion-detail` 查回推广 ID、状态、投放端和可投放资源树。
   - 校验用户选择的投放资源；标准资源已有资源 ID 时调 `plan-pack-resource-list` 校验资源 ID，并提取默认角标、默认跳转链接、资源名称和作者/艺人。若要继续保存素材但资源 ID 还缺失，先补问资源 ID 后再进入默认值和模板交互。
   - 按每个投放端调用 `data-template-extract-private`。模板提取本身不依赖资源 ID；标准资源已有 `resId` 时传入，非标或确实没有 `resId` 时不传。
   - 从每个模板的 `conditionConfig` 得到启用且必填的素材字段，本地校验图片尺寸，上传图片。
   - 非全量且用户已给人群时先用 `plan-check` 校验人群包；校验通过后，创建阶段可写入 `fullType=nofull`、`strategyInfo/crowdList`。如果未给，留到第二阶段保存物料前补问和校验。
   - 全量且用户已明确时，创建阶段可写入 `fullType=full`；未明确时留到第二阶段保存物料前补问。
   - 保存物料时调用 `promotion-update-creative --env ${MWS_ENV}`，传 `id`、`promotionAliasCreativeList`，并固定带上本轮已确认的 `fullType/resourceType/resourceInfo/resourceTypes`；非全量固定带 `strategyInfo` JSON 字符串。用户在素材阶段补充或修改了资源/投放量/人群就用新值，没改就沿用创建阶段或详情里的值。审批场景再补 `businessRemark/relateTask`。不要传 `op/crowdIds/forceSave` 这类 schema 不存在的顶层字段。
3. 如果只给齐推广基础字段但缺实际投放资源类型、资源 ID、投放量或非全量人群，仍可以创建/预占；但如果用户要求本轮继续配物料/修改物料，则必须在提取默认值和模板前一次性补问这些素材保存前置字段。创建成功并预占后，立即查 `promotion-detail`，按实际投放端和当前详情可用信息提取模板并输出素材填写清单；缺资源 ID、`fullType` 或非全量人群时，清单可以先展示模板字段，但默认角标/跳转链接和最终保存必须等这些字段补齐。
4. 如果信息不齐，不要一项一项追问；只补问一轮“轻量缺失清单”。清单要用用户感知的中文字段，不展示 `positionCode` / `channelCode`。先列“已识别/已推断”，再列“还差”。已推断出的四个业务标签、实际投放资源类型、投放端、投放量、人群不要再问；只有无法推断或和用户说法冲突时才补问。后续收到用户补充后，先完整解析本轮回答，不能因为只解析到部分字段就立刻再次追问同一组内容。

```text
我先按运营规则识别了一版：
- 项目类型：歌曲版权宣发
- 项目等级：S
- 实际投放资源类型：标准/歌曲
- 投放端：全部端
- 投放量：全量
- 起止时间：2026-06-15 08:00:00 至 2026-06-16 23:59:00
- 项目负责人：当前发起人
- 创建人二级部门：内容运营部

还差：
- 歌曲 ID
- 推广名称/项目名称（如果都用“王力宏新歌”也可以直接告诉我）
- 内容大类、版权类型、战略类型（可直接回复：头部/独家/其他）

素材可以创建预占后再给；如果你已经有图，也可以一起发。
```

上面的短模板是默认补问方式。只有用户要求查看完整选项、推断失败、或字段冲突时，才展开完整字段表和完整可选项。

5. 多端素材默认不共用。只有用户明确说“所有端共用同一套素材”，并且每个端模板字段和尺寸要求一致时，才复用同一份上传结果。
6. 多端模板不同或尺寸不同，要按端展示素材矩阵，让用户一次性给齐每端素材：

| 投放端 | 模板 | 必填素材 | 选填素材 |
|---|---|---|---|
| 移动端(iPhone&Android) | banner图片模版 | 大卡图片 1080x607、角标、跳转链接 | 普通图片 1080x420、视频、大卡视频：选填，模板未要求 |
| PC | 以模板返回为准 | 以模板返回为准 | 以模板返回为准 |

7. 给用户素材填写方式时，要支持“通用素材 + 按端覆盖”两种写法，减少重复输入：
   - 通用素材：适用于所有端，字段和尺寸一致时可以共用。
   - 按端覆盖：某个端素材不同，只写这个端特殊的图片、角标、链接、视频等，覆盖通用值。
   - 如果模板显示同一张图要同时用于多个字段，必须分别校验各字段尺寸；尺寸不同不能直接共用。
   - 如果某端没有覆盖，默认使用通用素材；如果没有通用素材，则必须给该端自己的必填素材。
   - 通用素材只在本轮当前推广内生效，不能从上一轮、上次测试、旧推广或旧对话自动带入。
8. 用户提供多张本地图片时，先按端和字段建立映射；无法判断某张图属于哪个端或字段时，只追问这一个映射问题，不要重新询问已确认的推广基础字段。
   不要因为上一次已经上传过同名图片、同尺寸图片或已有 NOS URL，就自动复用；本轮用户给的 NOS/NOSK/外部图片 URL 也不能直接复用，必须下载后按本轮图片流程重传。只有用户明确“沿用当前推广已有素材”且该 URL 来自当前 `promotion-detail` 时才保留。其它情况下，本轮没给图片且当前推广详情里也没有明确要沿用的素材时，必须让用户补图。
9. 一次性链路里任何一步返回强制保存、模板字段缺失或其它需要确认的错误时，停止当前写入链路并把需要用户确认的点列清楚；不要猜额外字段、不要强行复用旧模板。`promotion-update-creative` 返回 `needApproval=true` 时，只补问这次物料更新的 `businessRemark`，用户明确给了需求单再补 `relateTask`，不要改素材整包内容。
10. 创建推广成功并预占后，如果用户明确只做第一阶段或素材后补，在管理员补权限和详情核验完成后可以结束；否则不要只回复“推广已创建，等你给素材”。必须继续进入素材引导，尽量在同一条回复里告诉用户要传什么素材：
   - 先调用 `promotion-detail` 查回当前投放端和推广详情。
   - 使用创建阶段已经写入的实际投放资源类型、标准资源 ID（如有）、投放量和人群信息，校验并提取模板。若这是人工创建/历史推广导致详情缺少这些初始化字段，转入“人工历史推广补齐”分支，补问后继续素材链路。
   - 不要用推广基础里的 `deliveryResource`（投放资源标签）当作实际投放资源类型推断，也不要在预占后再追问资源/投放量/人群。
   - 正常由本 skill 创建的推广也可能只完成预占、尚未写入实际投放资源类型、资源 ID、投放量或人群；这不是异常。若详情缺这些字段，转入素材保存前置补问，拿到实际投放资源类型、标准资源 ID（标准资源时）、全量/非全量和非全量人群后，随 `promotion-update-creative` 同包补齐。
   - 对人工创建/历史推广，缺失同样不视为不可修复：只做一次前置补问，拿到实际投放资源类型、标准资源 ID（标准资源时）、全量/非全量和人群后，随 `promotion-update-creative` 同包补齐。不要因为这些初始化字段缺失就直接让用户重建或找服务端修复。
   - 标准资源校验后，运行 `resource_defaults.py` 提取默认值；如果用户没给角标，就用 `defaultBannerLabel` 并说明。跳转链接必须按端取默认值：只有 Web 优先用 `webDefaultUrl`（顶层 `pcUrl` 或其它 http/https 链接）；移动端、荣耀白牌、PC、Mac、iPad、AndroidPad、iPadHD 等其它端优先用 `clientDefaultUrl`（通常是 `composedData.commonComposedData.url` 或 `orpheus`）。Web 没有 http/https 默认值时必须补问用户，不能用 `orpheus` 兜底。用户显式给的值优先，但 Web 显式链接仍必须是 http/https。资源不存在或未上线时，只提醒无法取默认角标/跳转链接；用户确认强制配置并手工给链接/素材后可以继续。
   - 对每个端运行 `template_field_summary.py`，整理出用户需要填写/上传的素材清单。
   - 回复给用户时先列“通用素材”，再列“各端特殊素材”。只有各端模板字段和尺寸完全一致时，才提示可以共用一套素材；否则明确说明“每个端素材可能不一样，需要分别给”。
   - 素材清单必须包含：字段中文名、是否必填、图片尺寸、文本长度、链接/视频/图片类型、本地文件或 URL 的填写方式。模板未要求的字段写“选填”，不要写“不需要”。不要让用户自己猜要传什么。
   - 如果 `fullType` 或非全量人群在创建阶段没有提交，素材阶段必须作为保存前置字段补问；已提交且用户不修改时不重复询问。
   - 如果素材保存失败，不要为了调试把推广退回草稿态；草稿态不能保存素材时，应说明当前状态不支持素材保存，并在用户确认后再做必要的状态流转。不要自动切换状态来试接口。

普通创建步骤：

1. 先整理用户已提供字段、可推断字段和缺失字段；如果当前任务环境未确认，把“环境：预发布/线上”列为缺失字段。环境确认后先调用 `mws link pms-login-status --env ${MWS_ENV} --format json` 获取当前用户；当前执行身份不是 `grp.` 时，`projectOwner` 默认用 `data.name`，创建人二级部门默认取 `data.depList[]` 中 `level=2` 的 `name`。如果当前执行身份是 `grp.` 前缀，先判断是否为运营审核机器人/龙虾本部门场景：是则 `projectOwner` 使用当前会话真实发起人邮箱前缀，创建人二级部门默认 `内容运营部`；否则必须让用户填写真实项目负责人邮箱前缀和真实二级部门。机器人/数字员工环境还要在创建前确定管理员补权限名单：真实发起人邮箱前缀必填，群聊中真实被 @ 的协作者一并加入；无法识别真实发起人时，把“真实发起人邮箱前缀”列为缺失字段。如果非 `grp.` 场景下 `pms-login-status` 没有返回二级部门，把创建人二级部门列为缺失字段。字段齐且用户明确要求执行时直接进入下一步，字段不齐时只列一次合并后的轻量缺失项并等待补充。收到补充后先尽量解析同一句里的字段、连续四个业务标签和实际投放资源/投放量，不要先抛出只缺三四项的小补问。
2. 根据用户选择设置 `MWS_ENV`，并在后续该任务所有 MWS 命令中使用 `--env ${MWS_ENV}`。
3. 将用户选择或按实际投放资源类型推断出的投放端转换为内部 `relatedPositionCodes`；用户未指定且无法按资源类型推断时，才使用默认 4 个端：移动端(iPhone&Android)、荣耀白牌、PC、Web。
4. 调 `promotion-tag-config` 和 `promotion-type-list`，把用户中文选择转换为 code。
5. 项目类型需要艺人时，先用 `promotion-artist-list` 校验艺人 ID，填充完整 `promotionArtistList`；修改时若艺人未变，直接沿用 `promotion-detail.promotionArtistList`，不能只传 `artistIds`。
6. 创建阶段如果用户已给投放资源、资源 ID、投放量或人群，就一并转换写入；没给时允许留到第二阶段配物料前补：
   - 标准/歌曲等标准资源：已给资源类型时，`relatedResourceTypes` 传二级资源类型，例如 `song`；如果用户已给资源 ID，则 `relatedResourceIds` 传资源 ID，例如 `108485`；未给时创建阶段可以不传。
   - 非标/活动：已给资源类型时，`relatedResourceTypes` 传 `activity`；通常不传 `relatedResourceIds`。
   - 全量：用户已明确时可传 `fullType:"full"`；未明确时不传，第二阶段保存前补问。
   - 非全量：用户已明确且给出人群时先 `plan-check` 校验，校验通过后可传 `fullType:"nofull"`，并传 `strategyInfo.crowd` 和/或 `crowdList`。注意创建接口两处枚举不同：`strategyInfo.crowd.op` 用 `contain/notcontain`，`crowdList[].type` 用 `include/exclude`。未明确投放量或缺人群时不传，第二阶段保存前补问并校验。
7. 默认在 `promotion-add` 中附带空对象 `autoPreoccupy` 创建后预占；用户明确说不预占时才不带。预占不需要审批，不要为预占补 `businessRemark` / `relateTask` / `forceSave`。
8. 提交 `promotion-add` 前处理推广名称：
   - 标准格式：`【内容大类/版权类型/战略类型/投放资源标签】推广基础名称 –【二级部门】`。
   - 四个业务标签使用用户本轮选择的中文 label，不使用 code；顺序固定为内容大类、版权类型、战略类型、投放资源标签。
   - 用户只给基础名称时，自动补前缀和后缀。例如基础名称 `云打歌企划x限定`、标签 `战略/自制/艺粉/H5`、二级部门 `用户增长部`，最终提交 `【战略/自制/艺粉/H5】云打歌企划x限定 –【用户增长部】`。
   - 如果用户已经给了完整格式，先校验前缀四项和当前选择一致、后缀部门存在；一致则原样提交，不一致则提示差异并让用户确认，不要悄悄覆盖。
   - 如果本次是拆分创建多条推广，在部门后缀前追加日期后缀区分每条，例如 `...线上测试-6.17 –【技术中心】`；不要把多条拆分推广提交成完全相同的名称。
   - 这是为了让服务端 `parseDeptFromName(name)` 写入 `creatorDept`。展示给用户时可同时展示“用户输入推广基础名称”和“最终提交推广名称”。
9. 先 `--dry-run` 校验，再调用 `mws link promotion-add`。
10. `promotion-add` 创建成功拿到推广 ID 后，先执行管理员补权限检查，不能先查详情或回复成功。机器人/数字员工环境必须立即调用 `mws link admin-add`，`userNames` 使用创建前已确认的“真实发起人 + 本轮真实被 @ 协作者”，去重后只传邮箱前缀；没有可追加人员时必须明确记录“非机器人/数字员工环境”或“无真实发起人/协作者可追加”的跳过原因。不要等 `promotion-detail`、素材保存或结果回复阶段再补，也不要用 `admin-update`。硬门槛：没有完成或明确记录管理员补权限结果前，禁止查详情、提取模板、保存素材、回复“创建完成”。
11. 管理员补权限成功、确认无需补或已向用户说明补权限失败后，立即调用 `mws link promotion-detail` 查回状态和详情。最终结果里必须展示管理员补权限状态。
12. 如用户已提供创意/素材，继续执行“创意与素材流程”。如用户未提供创意/素材但明确只预占或素材后补，结果回复到第一阶段完成即可；不要继续追问素材。其它未提供素材的创建场景，按创建时已写入的投放资源和投放端提取模板并输出“素材填写清单”，减少下一轮沟通。

示例：

```bash
mws link promotion-add --env ${MWS_ENV} --reason "创建推广" --json '{
  "name": "【战略/独家/Kpop/MV】对对对-【技术中心】",
  "biz": "banner",
  "projectName": "projectName",
  "projectType": "other",
  "projectLevel": "A",
  "projectOwner": "zhengyouxiang",
  "contentCategory": "strategy",
  "copyrightType": "exclusive",
  "strategyType": "kpop",
  "deliveryResource": "mv",
  "projectBackground": "",
  "relatedPositionCodes": "PAGE_DISCOVERY_BANNER@mobile,PAGE_DISCOVERY_BANNER@magios,BANNER_PC_V2,BANNER_WEB",
  "startTime": "2026-06-11 00:00:00",
  "endTime": "2026-06-12 00:00:00",
  "autoPreoccupy": {}
}'
```

如果未带 `autoPreoccupy`，单独流转：

```bash
mws link promotion-transition --env ${MWS_ENV} --reason "推广预占" --json '{
  "id": 1200000577801,
  "toStatus": "preoccupy"
}'
```

## 查询推广

用户说“查 Banner / 查发现页 Banner / 查推广 / 看下推广 / 查询推广详情”时使用本流程。查询不做 `admin-add`，不修改推广。

1. 环境仍是独立字段。用户明确预发布时用 `pre`；用户明确线上或没说环境时默认 `online`；同一任务已确认环境则沿用。
2. 如果用户给的是推广 ID，优先调用 `promotion-detail`。查询 Banner 推广时必须带 `biz:"banner"`，否则部分环境可能返回空 `400`：

```bash
mws link promotion-detail --env ${MWS_ENV} --reason "查询推广详情" --params '{
  "id": "1200000578809",
  "biz": "banner"
}' --format json
```

3. 如果用户只给推广名称或关键词，不要让用户先补 ID；调用 `promotion-list` 用 `idOrName` 查询，并固定带 `biz:"banner"`、`pageNo:1`、`pageSize:10`、`isSample:true`：

```bash
mws link promotion-list --env ${MWS_ENV} --reason "按名称查询推广" --json '{
  "biz": "banner",
  "idOrName": "zyx_0612_v9",
  "pageNo": 1,
  "pageSize": 10,
  "isSample": true
}' --format json
```

4. 查询结果处理：
   - 0 条：告诉用户没有查到，并让用户确认环境、名称关键词或推广 ID。
   - 1 条：用该条 `id` 再调用 `promotion-detail` 查完整详情。
   - 多条：只展示精简候选，让用户选择 ID；不要猜。候选最多展示 10 条，字段为推广 ID、推广名称、项目名称、起止时间、中文状态、创建人/更新人。
5. 查询回复要面向运营展示中文字段和中文状态，不展示内部 code。建议字段：

```text
查询到推广：
推广 ID：1200000578809
推广名称：xxx
项目名称：xxx
项目负责人：xxx
投放端：移动端、PC、Web
起止时间：2026-06-15 00:00:00 至 2026-06-16 23:59:59
项目等级：A
项目类型：其他类型
投放量：全量 / 非全量
当前状态：已预占
创建人：xxx
更新人：xxx
```

## 复制推广

用户说“复制 Banner / 复制发现页 Banner / 复制推广”时使用本流程。复制是写操作，先 `--dry-run`，再真实调用；复制成功后如果本轮群聊里真实 @ 了协作者，要把这些被 @ 的人追加为新推广普通管理员。没有 @ 人时跳过，不要把发起人、机器人或 `grp.` 账号自动加进去。

1. 如果用户给源推广 ID，先用 `promotion-detail` + `biz:"banner"` 查源推广，确认名称、状态、起止时间和投放端。
2. 如果用户只给源推广名称，先按“查询推广”使用 `promotion-list` 解析源推广；多条候选必须让用户选择 ID。
3. 源推广确认后调用：

```bash
mws link promotion-copy --env ${MWS_ENV} --reason "复制推广" --dry-run --json '{
  "id": 1200000578809
}' --format json
```

```bash
mws link promotion-copy --env ${MWS_ENV} --reason "复制推广" --json '{
  "id": 1200000578809
}' --format json
```

4. `promotion-copy` 返回新推广 ID 后，先处理被 @ 协作者管理员：
   - 本轮没有真实 @ 协作者：记录“无被 @ 协作者，跳过管理员补权限”。
   - 本轮有真实 @ 协作者：用新推广 ID 调 `admin-get` 查已有管理员，只对尚不存在的邮箱前缀调用 `admin-add`；`userNames` 只放被 @ 的协作者邮箱前缀，不放完整邮箱，不放发起人，不放机器人，不放 `grp.`。
   - `admin-add` 失败时，结果里说明“推广已复制，但管理员补权限失败：xxx”，不要回滚复制结果，不要改用 `admin-update`。
5. 管理员补权限完成、确认无需补或失败原因已记录后，调用 `promotion-detail` + `biz:"banner"` 查新推广详情并展示结果。不要在复制后自动改时间、改名称、预占或保存素材，除非用户本轮明确要求这些后续动作；即使用户后续要求修改，也按“修改推广”或“状态修改”流程走。

## 状态修改 / 状态流转

用户说“取消预占”“退回草稿”“预占”“提交上线/待上线”“上线”“下线”“停止投放”“改状态”时使用本流程。状态修改只调用 `mws link promotion-transition`；不要调用 `promotion-update`，也不要调用 `admin-add`。

接口：`promotion-transition`，对应 `POST /api/link/platform/ai/promotion/transition`。入参使用当前 `mws schema link.promotion-transition`，核心字段为 `id`、`toStatus`，可选 `forceSave`、`businessRemark`、`relateTask`。

1. 先解析目标推广。用户给 ID 时调用 `promotion-detail` 查询现状；用户只给名称时，先按“查询推广”用 `promotion-list` 解析 ID。查询 Banner 推广详情必须带 `biz:"banner"`。多条匹配时先让用户选择 ID，不要猜。
2. 把用户语义映射为 `toStatus`：

| 用户说法 | `toStatus` | 展示 |
|---|---|---|
| 预占 / 转预占 | `preoccupy` | 已预占 |
| 取消预占 / 退回草稿 / 改回草稿 | `draft` | 草稿 |
| 提交上线 / 待上线 / 提交待上线 | `stayOnline` | 待上线 |
| 上线 / 立即上线 | `online` | 已上线 |
| 下线 / 停止投放 | `offline` | 已下线 |

3. 如果用户说法对应不到上表，或当前状态和目标状态冲突但用户意图不明确，先让用户确认目标状态；不要猜。
4. 先 `--dry-run`，再真实调用。取消预占示例：

```bash
mws link promotion-transition --env ${MWS_ENV} --reason "推广状态修改" --dry-run --json '{
  "id": 1200000578809,
  "toStatus": "draft"
}' --format json
```

```bash
mws link promotion-transition --env ${MWS_ENV} --reason "推广状态修改" --json '{
  "id": 1200000578809,
  "toStatus": "draft"
}' --format json
```

5. 如果返回 `needApproval=true` 且 `approvalInitiated=false`，说明需要审批说明。向用户补问“这次状态修改的审批说明”，然后用同一份参数补 `businessRemark` 重试；用户本轮明确给了需求单时再传 `relateTask`，不要猜。
6. 如果返回 `requiresForce=true`，把 `warnings/conflicts/message` 用中文展示给用户确认；用户确认强制保存后，用同一份参数补 `forceSave:true` 重试。
7. 成功后必须调用 `promotion-detail` + `biz:"banner"` 查回当前状态，回复中文状态；不要直接展示接口枚举。

## 修改推广

1. 先解析目标推广。用户给 ID 时调用 `promotion-detail` 查询现状；用户只给名称时，先按“查询推广”用 `promotion-list` 解析 ID。查询 Banner 推广详情必须带 `biz:"banner"`。多条匹配时先让用户选择 ID，不要猜。
2. 只传需要修改的字段；未修改字段不要传。`biz` 不可修改；投放端对应的内部 `relatedPositionCodes` 只有 DRAFT 状态可修改。
3. 修改投放端时继续使用“投放端配置”转换，用户不需要感知内部 code。
4. ONLINE/SCHEDULED 且 `fullType=full` 时修改 `startTime/endTime`，如果返回 `requiresForce=true`，必须向用户确认后再带 `forceSave=true` 重试。
5. 修改推广只执行本次字段更新和查回确认，不调用 `admin-add`。管理员补权限只在 `promotion-add` 创建成功后执行。

示例：

```bash
mws link promotion-update --env ${MWS_ENV} --reason "修改推广" --json '{
  "id": 1200000576814,
  "name": "新推广名-【平台业务技术组】",
  "projectBackground": "更新后的背景"
}'
```

## 定向人群

人群逻辑可以在创建推广前处理并随 `promotion-add` 一起提交，也可以在第二阶段配物料/更新物料前补齐。物料保存阶段如果是非全量，必须在 `promotion-update-creative` 的 `strategyInfo` JSON 字符串里携带人群，不要传 `crowdList`、`op`、`crowdIds` 顶层字段，也不要依赖 `promotion-update` 补人群初始化。

用户说“全量”时，`promotion-add` 传 `fullType:"full"`，不传 `strategyInfo/crowdList`。

用户说“非全量/定向人群”时，保存物料前必须收集人群包 ID 和包含/不包含，并先调用 `plan-check` 校验人群有效性。创建阶段如果已经给齐，也可以提前校验并写入 `strategyInfo` 和 `crowdList`；两处枚举不同，不要混用：

| 用户语义 | `strategyInfo.crowd.op` | `crowdList[].type` |
|---|---|---|
| 包含 | `contain` | `include` |
| 不包含 | `notcontain` | `exclude` |

保存物料前，如果是非全量，必须先调用 `plan-check`；创建阶段已给齐非全量人群时也可以提前调用：

```bash
mws link plan-check --env ${MWS_ENV} --reason "校验人群包" --json '{
  "crowdIds": [3691, 84323],
  "positionCode": "PAGE_DISCOVERY_BANNER"
}'
```

`positionCode` 取当前投放端的内部 `positionCode`，如果包含 `@`，只传 `@` 前面的部分。例如 `PAGE_DISCOVERY_BANNER@mobile` 传 `PAGE_DISCOVERY_BANNER`；没有 `@` 时传原值，例如 `BANNER_PC_V2`。多端时任选一个当前投放端即可。返回里任一项 `valid=false` 时停止，不创建推广。

非全量创建字段示例，传给 `promotion-add`：

```json
{
  "fullType": "nofull",
  "strategyInfo": {
    "crowd": {
      "sceneId": 29,
      "crowdIds": [3691, 84323],
      "op": "notcontain"
    }
  },
  "crowdList": [
    {
      "crowdId": 3691,
      "sceneId": 29,
      "type": "exclude"
    }
  ]
}
```

## 创意与素材流程

创意是动态模板驱动，不要写死图片、标题、角标、跳转链接字段。执行前必须读取 [references/creative-dynamic-material.md](references/creative-dynamic-material.md)。

1. 如果推广还没有 ID，先创建推广。
2. 调 `promotion-detail`，读取 `resourceTypes`、`resourceInfo`、`deliveryResourceList`、`promotionAliasTemplateList`、`promotionAliasCreativeList`。
3. 必须先确定“实际投什么资源”和“投放量”。如果用户本轮已明确选择实际投放资源类型，以用户选择为准，并用 `deliveryResourceList` 校验；如果详情 `resourceTypes` / `relatedResourceTypes` 为空且用户也未明确实际投放资源类型，不能用推广基础的 `deliveryResource` 投放资源标签推断。人工创建/历史推广常见缺 `fullType/resourceTypes/resourceInfo`，此时只列一次前置缺失项，让用户补实际投放资源类型、标准资源 ID（标准资源时）、全量/非全量和非全量人群。直接修改、补配或换物料时，标准资源必须先拿到资源 ID，才能继续获取默认值、提取模板和生成素材清单：

```bash
mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000577803"}' --format json \
  | python3 scripts/promotion_resource_wizard.py choices
```

4. 用户选择后，用脚本校验该资源在 `deliveryResourceList` 中存在，并生成每个投放端的模板提取命令。创建后仅展示素材 schema 时，标准资源可以暂时没有资源 ID；直接修改、补配或换物料必须使用 `--require-resource-id`，标准资源缺 ID 时先补问，不进入模板和素材交互。非标资源通常不需要资源 ID：

```bash
mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000577803"}' --format json \
  | python3 scripts/promotion_resource_wizard.py select --first standard --second song --resource-id 111
```

直接修改、补配或换物料使用：

```bash
mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000577803"}' --format json \
  | python3 scripts/promotion_resource_wizard.py select --first standard --second song --resource-id 111 --require-resource-id
```

```bash
mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000577803"}' --format json \
  | python3 scripts/promotion_resource_wizard.py select --first nonstandard --second activity
```

5. 不要替用户默认选择 `nonstandard/activity` 或 `standard/song`；必须以用户选择为准。用户补齐后，使用 `promotion_resource_wizard.py select` 生成标准结构，并把 `fullType/resourceType/resourceInfo/resourceTypes/strategyInfo` 放入后续 `promotion-update-creative` 入参。直接修改/补配/换物料的顺序固定为：先确认资源类型和资源 ID（标准资源时）→ `plan-pack-resource-list` 获取默认值 → `data-template-extract-private` 提取各端模板 → `template_field_summary.py` 生成素材清单并让用户补物料 → 组包预检 → `promotion-update-creative`。不要跳过默认值获取，也不要调用 `promotion-update` 后补这些字段。
6. 标准资源且有资源 ID 时，先调用 `mws link plan-pack-resource-list` 获取资源信息：

```bash
mws link plan-pack-resource-list --env ${MWS_ENV} --params '{
  "resourceType": "song",
  "resourceIds": "111"
}'
```

`plan-pack-resource-list` 的资源 ID 参数必须叫 `resourceIds`（复数，字符串，多个 ID 用英文逗号拼接），禁止写 `resourceId`。如果看到错误 `Required String parameter 'resourceIds' is not present`，不要继续换 HTTP/curl 或猜其它字段，直接把参数从 `resourceId` 改为 `resourceIds` 并通过 `mws link plan-pack-resource-list` 重试：

```bash
mws link plan-pack-resource-list --env ${MWS_ENV} --params '{"resourceType":"album","resourceIds":"382794761"}' --format json
```

随后立即提取默认值：

```bash
mws link plan-pack-resource-list --env ${MWS_ENV} --params '{"resourceType":"song","resourceIds":"111"}' --format json \
  | python3 scripts/resource_defaults.py
```

如果返回 `composedData.commonComposedData.bannerLabel`，用户没给角标时默认使用它。跳转链接不要只取一个全局默认值，必须按投放端选择：

- Web：优先用 `webDefaultUrl`，即顶层 `pcUrl` 或其它 http/https 链接；没有 http/https 时必须让用户手工提供 Web 链接，禁止退化使用 `orpheus`。
- 移动端(iPhone&Android)、荣耀白牌、PC、Mac、iPad(新版)、AndroidPad、iPadHD(旧版)：优先用 `clientDefaultUrl`，即 `composedData.commonComposedData.url` 或顶层 `orpheus`；没有客户端默认值时继续看该端 `data-template-extract-private` 模板 `preData`。仍缺失时让用户提供端维度链接，禁止用 `pcUrl` 或手拼 `https://music.163.com/...` 兜底。
- 特例：如果已经调用 `plan-pack-resource-list` 且返回空，并且当前标准资源是歌曲 `resourceType=song`，可以使用歌曲固定兜底：非 Web 端 `orpheus://song/{歌曲ID}`，Web 端 `https://music.163.com/#/song?id={歌曲ID}`。其它标准类型（专辑/MV/歌单等）先不使用默认兜底，仍按缺失处理，问用户提供端维度链接或停止保存。

例如歌曲资源同时返回 `"pcUrl": "https://music.163.com/#/song?id=108485"` 和 `"orpheus": "orpheus://song/108485"` 时，Web 默认用 `https://music.163.com/#/song?id=108485`，移动端/荣耀白牌/PC/Mac/iPad 等其它端默认用 `orpheus://song/108485`。如果资源只返回 `orpheus`、没有任何 http/https 链接，Web 端链接视为缺失，必须补问用户。回复用户时说明各端将使用的默认角标/跳转链接；用户显式提供的角标、链接、标题、图片始终优先。

如果 `plan-pack-resource-list` 返回空：标准歌曲允许按上面的歌曲固定兜底生成链接，但要说明接口没有查到资源默认角标；其它标准类型不要猜默认链接，提示“资源可能不存在或未上线，无法取资源默认角标/跳转链接”，让用户提供角标和端维度跳转链接后再继续。

保存物料前必须检查推广详情里的资源初始化是否完整。下面是详情里应有的形态；如果详情缺失但本轮用户已经确认，可以在 `promotion-update-creative` 入参中同包补齐。人工创建/历史推广缺失时必须先补问确认，不能直接把空值、推广基础标签或旧创意资源信息当作真实资源初始化：

```json
{
  "resourceType": "song",
  "resourceInfo": "108485",
  "resourceTypes": [["standard", "song"]]
}
```

非标活动示例：

```json
{
  "resourceType": "activity",
  "resourceInfo": "",
  "resourceTypes": [["nonstandard", "activity"]]
}
```

`resourceType` 是二级资源类型字符串，不是二维数组；`resourceInfo` 是标准资源 ID 字符串，非标通常为空。

保存素材时不要省略这些资源信息、`fullType` 或非全量人群信息：优先使用素材阶段用户修改后的值；否则沿用第一阶段已确认值或当前详情值，随 `promotion-update-creative` 一起传。缺失且无法确认时停止并补问。人工创建/历史推广补问确认后，直接在本次 `promotion-update-creative` 同包传入；不要用 `promotion-update` 后补。

保存素材时资源字段固定按下面规则组装，不要省略：

| 实际投放资源 | `resourceType` | `resourceTypes` | `resourceInfo` |
|---|---|---|---|
| 标准/歌曲，资源 ID 为 `108485` | `song` | `[["standard","song"]]` | `108485` |
| 标准/专辑，资源 ID 为 `123` | `album` | `[["standard","album"]]` | `123` |
| 标准/MV，资源 ID 为 `456` | `mv` | `[["standard","mv"]]` | `456` |
| 非标/活动 | `activity` | `[["nonstandard","activity"]]` | 空字符串 |

非全量时，不再传旧接口形态里的顶层 `op` / `crowdIds`；必须把人群写成 `strategyInfo` JSON 字符串，例如：

```json
{
  "fullType": "nofull",
  "resourceType": "song",
  "resourceInfo": "108485",
  "resourceTypes": [["standard", "song"]],
  "strategyInfo": "{\"crowd\":{\"sceneId\":29,\"crowdIds\":[3691],\"op\":\"contain\"}}"
}
```

7. 每个选中端都要单独调用 `data-template-extract-private` 提取模板；不能只用 `position-channel-data-template` 的列表结果替代提交所需的动态模板。
8. 每个端拿到模板后，先用脚本输出需要用户补充的素材字段、图片尺寸和文本长度：

```bash
mws link data-template-extract-private --env ${MWS_ENV} --params '{...}' --format json \
  | python3 scripts/template_field_summary.py
```

脚本输出后，必须整理成面向用户的素材填写清单：

```text
接下来需要你补素材。每个端的模板可能不同，图片尺寸也可能不同；如果你希望多端共用素材，请先确认尺寸和字段完全一致。

通用可填：
- 角标：必填，最多 5 字
- 跳转链接：必填，填 URL；常见合法格式是 orpheus://... 或 https://y.music.163.com/g/yida/...

各端素材：
- 移动端(iPhone&Android)：大卡图片，必填，1080x607，给本地图片路径或图片 URL；普通图片，选填，1080x420；视频/大卡视频，选填
- PC：以模板返回为准列出字段
- Web：以模板返回为准列出字段

投放量和人群：如果当前详情已有 `fullType` 和非全量人群，直接沿用；如果缺失，素材阶段先补问全量/非全量，非全量再补人群包和包含/不包含。

如果各端用同一套素材，请回复“所有端共用”并给对应图片/链接；如果每端单独配置，请按端分别给。
```

不要把脚本原始字段名直接丢给用户；可以在必要时把字段名放到括号里辅助排查。用户需要知道的是“哪个端、什么素材、是否必填、尺寸/字数、怎么给”。模板未要求或未强制的字段写“选填”，不要写“不需要”。

跳转链接校验规则：标准资源不能手拼链接，必须先走资源默认值和模板 `preData`；Web 端必须是 http/https，非 Web 端优先使用客户端默认链接。非标准资源或用户显式覆盖时，如果用户给的链接不是 `orpheus://...`、`https://music.163.com/#/...` 或 `https://y.music.163.com/g/yida/...` 等常见格式，先提示“链接不是常见投放格式，可能无法按预期跳转”，并询问是否仍要保存；用户明确确认后才继续保存。`promotion-update-creative` 当前 schema 没有单独 `forceSave` 字段，不要凭空添加参数；`businessRemark` 只用于物料更新命中 31003 审批时发起审批，不用于跳转链接强制保存。

9. 再收集 `template.schema.children[].resourceTypeCodes[].code`，调用 `component-code` 获取组件字段详情：

```bash
mws link component-code --env ${MWS_ENV} --params '{
  "codes": "[\"bannerImageType4WebAndOther\"]"
}'
```

10. 复制模板 `preData.children[].data` 作为初始创意数据；标准资源的标题、封面、跳转链接可能由模板预填，用户显式提供的字段优先覆盖。但更新/换物料时不能无条件沿用旧创意或上游传入的跳转链接：每次都要先按第 6 步重新获取标准资源默认值并生成本次端维度默认链接，再用用户本轮显式提供的链接覆盖。Web 端如果最终不是 http/https，视为缺失并补问用户，不能继续保存。
11. 从模板 `conditionConfig` 解析字段启用、是否必填、图片宽高、文本长度。用户给本地图片时先校验尺寸；用户给图片 URL 时先下载成本地文件再校验尺寸，不能把原 URL 直接写入 payload。尺寸不符时只能在“原图宽高都大于目标宽高”的情况下征求用户确认，使用 Python 脚本按模板目标宽高中心裁剪/缩放。原图任一边小于目标尺寸时禁止放大裁剪，要求用户补更大原图。裁剪后如果当前客户端可以渲染本地图片，必须用 Markdown 图片语法把每张生成图真实展示出来，图片链接必须是本地绝对路径，不能用 `~`、相对路径或工作区相对路径，并让用户确认后再上传；如果无法渲染图片，只能给本地绝对路径并说明“已生成裁剪文件，请打开路径确认”，不要说“预览已展示”。图片处理和上传依赖见 [references/image-upload-nos.md](references/image-upload-nos.md)。
12. 组装 `promotionAliasCreativeList` 前先处理折叠端。保存素材时不要按用户选择的所有投放端逐个提交，也不要只手写“移动端/荣耀白牌”一个合并特例；必须以当前 `promotion-detail.promotionAliasTemplateList` 返回的折叠后端别名为准组装提交节点。全端常见折叠结果是：移动端(iPhone&Android) 代表移动端/荣耀白牌/iPad(新版)/AndroidPad，另有 PC、Web、Mac、iPadHD(旧版)。如果推广实际有多个折叠后端，`promotionAliasCreativeList` 必须一次性包含所有这些折叠后端，每个端的 `promotionCreativeList` 都非空；不能为了“先验证一个端”只提交移动端或任意单端。只提交部分端会漏掉其它投放端素材，真实保存通常返回“素材不能为空2”。如果用户只给了一端素材，先询问是否所有端共用；不是共用就补齐缺失端素材后再保存。
13. 按动态模板组装完整内嵌创意对象，并通过 `promotion-update-creative` 一次性保存到推广。执行该步骤前必须读取并遵守 [references/creative-dynamic-material.md](references/creative-dynamic-material.md) 中的 `promotion-update-creative 防变形规则`、`内嵌创意对象结构` 和 `保存到推广` 小节；主流程只保留摘要，具体层级、错误对照和 payload 示例都以该引用文档为准。

   摘要规则：真实入参必须来自当前 `mws schema link.promotion-update-creative`、当前推广详情、当前端模板和本轮素材；按 `promotion-detail.promotionAliasTemplateList` 的折叠后端一次性提交全量节点；每个节点必须包含 `positionAlias`、`positionAliasShow`、非空 `promotionCreativeList`，且 `promotionCreativeList[]` 每一项必须是 `{ "creative": { ... } }` 包装结构；每个 `creative` 必须包含 `dataTemplate.id`、完整 `templateSchema` JSON 字符串和 `creativeDetailDataVO`；不能使用 `templateId/resourceTypeCode/data` 简化结构。新增创意名必须按 `creative-dynamic-material.md` 的“创意名称生成”规则生成，不能复用固定前缀或秒级时间戳；同包携带 `fullType/resourceType/resourceInfo/resourceTypes`，非全量再带 `strategyInfo` JSON 字符串。禁止 `creative-add`，禁止只提交一个端验证，禁止 `// ... 其余端`、`NOS_URL` 等省略或占位。真实返回 `素材不能为空2` 时，优先检查是否少传折叠端、是否没有 `creative` 包装、是否缺 `templateSchema/creativeDetailDataVO.children[].data`，不要去改 `fullType` 或重建推广。

   真实调用前必须把当前推广详情和整包 payload 落成 JSON 文件，先跑本 skill 的预检脚本；脚本失败时只修 payload，不调用 MWS，也不换其它接口：

```bash
WORKDIR="/tmp/lingqu-banner-1200000576814-$(date +%Y%m%d%H%M%S)"
mkdir -p "$WORKDIR"
mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000576814"}' --format json > "$WORKDIR/promotion-detail.json"
python3 scripts/validate_update_creative_payload.py \
  "$WORKDIR/promotion-update-creative.json" \
  --detail "$WORKDIR/promotion-detail.json"
```

   只有预检通过后，才允许继续 `mws link promotion-update-creative --dry-run` 和真实保存。`dry-run` 不能替代这一步；如果没有预检脚本输出 `OK promotion-update-creative payload preflight passed`，后续任何 `dry-run` 成功都不能作为继续真实调用的依据。

14. `promotion-update-creative` 已内嵌物料更新校验和 31003 审批处理：
   - 如果返回 `needApproval=true`，不是参数错误。向用户补问“这次物料更新的审批说明”，然后用同一份整包参数补 `businessRemark` 再调用一次。
   - 如果用户本轮已经明确给了审批说明，可以在首次保存物料时直接传 `businessRemark`，接口会自动发起 `updateCreativeApproval`。
   - `relateTask` 是可选字段，只有用户明确给了需求单/任务号时才传。
   - 不要调用额外的 `updateCreativeCheck` / `updateCreativeApproval`，也不要为这个步骤猜 `businessRemark`。
15. `promotion-update-creative` 真实调用失败且不是 `needApproval=true` 时，按 [references/creative-dynamic-material.md](references/creative-dynamic-material.md) 的 `promotion-update-creative 常见错误对照` 排查。若错误是 404、method not found、未注册或环境路由不存在，只确认 `mws schema link.promotion-update-creative`、`--env ${MWS_ENV}` 和方法名；禁止改用 `creative-add`、`promotion-update`、`mws_exec`、`raw_call`、curl/HTTP 直连或其它接口。若错误是当前状态不可保存素材，不要自动退回草稿态或创建新推广验证，停止并提示需要用户确认状态处理。
16. 仍无法定位时，报告 MWS 方法、关键入参摘要和原始错误信息；不要改用代码排查、其它接口、HTTP 直连，或临时补 schema 中不存在的字段。

## 管理员补权限

机器人/数字员工代创建时，管理员补权限是 `promotion-add` 创建成功后的第一个后置动作。复制推广时，只有本轮群聊里真实 @ 了协作者，才在 `promotion-copy` 成功拿到新推广 ID 后追加这些被 @ 的人为新推广普通管理员。修改推广、保存物料、状态流转等其它写操作不调用 `admin-add`。不要等查详情、素材阶段或结果回复时再补。

补权限名单：

- 创建推广：本轮真实发起人邮箱前缀 + 群聊里真实被 @ 的协作者邮箱前缀。
- 复制推广：只包含群聊里本轮真实被 @ 的协作者邮箱前缀；没有 @ 协作者就跳过。
- 去重；不要传完整邮箱；不要传 `grp.` 群组账号；不要传机器人/数字员工账号。
- 创建推广如果无法识别真实发起人，创建前就补问“真实发起人邮箱前缀”，不要写入后跳过。复制推广不因无法识别真实发起人而停止，因为复制只补被 @ 协作者。

`promotion-add` 成功拿到推广 ID 后立刻调用 `mws link admin-add`，先补管理员再查详情、预占后模板、保存素材或回复“创建完成”：

```bash
mws link admin-add --env ${MWS_ENV} --reason "追加推广管理员" --json '{
  "moduleId": 1200000576814,
  "module": "promotion",
  "adminType": "normal",
  "userNames": ["zhengyouxiang", "wb.luohaijin"]
}'
```

`promotion-copy` 成功拿到新推广 ID 后，如果本轮有真实 @ 协作者，先用新推广 ID 查管理员；已存在的人不重复加，缺失的人调用 `admin-add`：

```bash
mws link admin-get --env ${MWS_ENV} --reason "查询推广管理员" --json '{
  "moduleId": 1200000576814,
  "module": "promotion",
  "adminType": "normal"
}'
```

```bash
mws link admin-add --env ${MWS_ENV} --reason "追加被@协作者为推广管理员" --json '{
  "moduleId": 1200000576814,
  "module": "promotion",
  "adminType": "normal",
  "userNames": ["wb.luohaijin"]
}'
```

不要调用 `admin-update` 合并或覆盖已有管理员列表。`admin-add` 失败时要在结果里说明补权限失败原因，但不回滚已创建/复制推广；不要说“下次创建/复制后会补”，本轮能补就本轮补，本轮补不了就明确给出失败原因和需要用户补充的内容。

## 对话输出规则

执行过程中不要把内部流水、参数试错和自我纠错逐条发给用户。尤其禁止这些中间消息：

- “收到。校验配置和资源。”
- “位置校验无关人群，跳过直接创建。”
- “strategyInfo 需为对象非字符串。修正重试。”
- “创建成功，查详情。”
- “接口通了但返回错误，我换个接口试试。”

内部可以做 dry-run、修参数、重试同一 MWS 方法、查详情和预检脚本，但对用户只输出：

- 缺失字段清单。
- 需要用户确认的阻塞点。
- 超过 30 秒时的一句合并进度，且不暴露内部试错细节。
- 最终结果。

“推广创建完成”必须等 `promotion-add`、必要的 `admin-add`、`promotion-detail` 和下一步素材清单处理完后再说；“推广复制完成”必须等 `promotion-copy`、本轮被 @ 协作者的管理员补权限处理和新推广 `promotion-detail` 处理完后再说。若 `promotion-add` 成功但 `admin-add` 失败，结果写“推广已创建，但管理员补权限失败：xxx”；若 `promotion-copy` 成功但被 @ 协作者补权限失败，结果写“推广已复制，但管理员补权限失败：xxx”。不要静默跳过。修改、状态流转、素材保存不展示管理员补权限状态。

## 结果回复

成功后简短回复：

状态必须展示中文，不要直接把接口枚举值裸露给用户。常用映射：

| 接口状态 | 用户展示 |
|---|---|
| `draft` / `DRAFT` | 草稿 |
| `preoccupy` / `PREOCCUPY` | 已预占 |
| `wait_online` / `WAIT_ONLINE` / `stayOnline` / `STAY_ONLINE` | 待上线 |
| `online` / `ONLINE` | 已上线 |
| `scheduled` / `SCHEDULED` | 已排期 |
| `offline` / `OFFLINE` | 已下线 |
| `expired` / `EXPIRED` | 已过期 |

未知状态展示为“未知（原始状态：xxx）”。

```text
推广创建完成
环境：预发布
推广 ID：1200000577801
推广名称：xxx
项目名称：xxx
项目负责人：xxx
投放端：移动端(iPhone&Android)
起止时间：2026-06-12 00:00:00 至 2026-06-13 23:59:59
项目等级：S
项目类型：艺人合作宣发
内容大类：头部
版权类型：独家
战略类型：其他
投放资源：其他
当前状态：已预占
关联艺人 ID：5781
管理员补权限：已处理 / 无需处理（简述跳过原因） / 处理失败（简述原因）
```

如果创建完成但素材还没配置完成，结果后必须追加“下一步素材填写清单”。清单来自当前推广详情、当前投放资源、每个投放端的 `data-template-extract-private` 和 `template_field_summary.py`，不能凭经验写死。仅创建后的素材 schema 展示可以在没有标准资源 ID 时先拉取；直接修改、补配、换物料或最终保存前，标准资源 ID 是硬门槛，因为要先校验资源并重新获取默认角标/跳转链接。

素材清单必须把 schema 里要传的内容说清楚：字段中文名、必填/选填、值怎么给、图片尺寸或文本长度、链接格式提示；必要时附 `fieldName` 方便排查。

```text
下一步需要补素材：

资源与投放量：如果创建阶段已写入则沿用；如果缺资源类型、标准资源 ID、全量/非全量或非全量人群，请先补齐后再配物料。补齐后的值随本次 `promotion-update-creative` 同包提交，不通过 `promotion-update` 后补。

通用字段：
- 角标：通常有默认值；标准资源有资源 ID 时优先用资源返回的默认角标。用户也可以覆盖，最多 5 字
- 跳转链接：通常有默认值；标准资源有资源 ID 时按端使用资源/模板返回的默认跳转，只有 Web 必须使用 `pcUrl` 或其它 http/https 链接，其它端含 PC 优先 `orpheus://...` / `commonComposedData.url` / 模板 `preData`。用户也可以覆盖；Web 覆盖值仍必须是 http/https，非 Web 标准资源不能用手拼的 `music.163.com` Web 链接兜底。

各端素材：
- 移动端(iPhone&Android)
  - 大卡图片（bigPic）：必填，图片，1080x607，给本地图片路径或图片 URL
  - 普通图片（pic）：选填，图片，1080x420，给本地图片路径或图片 URL
  - 角标（typeTitle）：必填/有默认值，文本，最多 5 字
  - 跳转链接（url）：必填/有默认值，URL
- PC：按 PC 当前 schema 输出字段、必填/选填、尺寸和填写方式
- Web：按 Web 当前 schema 输出字段、必填/选填、尺寸和填写方式

说明：每个端的素材可能不一样。若所有端共用，请直接说“所有端共用”并给素材；若特殊配置，请按端分别给。

你可以按下面任一种格式回复：

全部端共用：
投放量：全量
通用角标：新歌首发
通用跳转链接：按端使用资源/模板默认链接；如需覆盖请填写端维度新链接
通用大卡图片：/path/big.png
通用普通图片：/path/pic.png

通用 + 单端覆盖：
投放量：非全量，包含 1691
通用角标：新歌首发
通用跳转链接：按端使用资源/模板默认链接；如需覆盖请填写端维度新链接
通用大卡图片：/path/big.png
PC：普通图片 /path/pc.png，角标 PC 专属
Web：跳转链接 https://y.music.163.com/g/yida/xxx

完全按端配置：
移动端(iPhone&Android)：大卡图片 /path/mobile-big.png，角标 新歌，跳转链接 orpheus://song/108485
荣耀白牌：如果和移动端同时投放，通常由移动端折叠节点覆盖，不单独提交；如果只有荣耀白牌单投，再按荣耀白牌模板给素材
PC：普通图片 /path/pc.png，大卡图片 /path/pc-big.png，角标 PC，跳转链接 orpheus://song/108485
Web：普通图片 /path/web.png，跳转链接 https://music.163.com/#/song?id=108485
```

不要把 `relatedPositionCodes`、`PAGE_DISCOVERY_BANNER@mobile`、`contentCategory=head` 这类内部字段作为给用户看的主结果；需要排查问题时只能放在“技术细节”里。

如果失败，回复必须包含：失败的 MWS 方法、请求目的、错误摘要、可执行的修复方向、下一步需要用户补什么。不要只复述后端原始 message。

`promotion-update-creative` 返回 `素材不能为空2` 时，必须把后端报错翻译成可修复诊断，至少包含：

```text
物料保存失败：后端返回“素材不能为空2”。

这通常不是 fullType/resourceType/resourceInfo 的问题，而是服务端解析到某些投放端没有完整素材。请按下面顺序修：
1. 查当前 promotion-detail.promotionAliasTemplateList，确认需要提交几个折叠端。
2. promotionAliasCreativeList 必须按 promotionAliasTemplateList 的数量、顺序、positionAlias、positionAliasShow 一次性全量提交；少一个折叠端都会被判定为该端素材为空。
3. 每个折叠端的 promotionCreativeList 都必须非空，且每项必须是 {"creative": {...}} 包装。
4. 不能使用 templateId/resourceTypeCode/data 这种简化结构；必须放到 creative.dataTemplate.id、creative.templateSchema、creative.creativeDetailDataVO.children[].data 里。
5. 每个 creative.templateSchema 必须是该端 data-template-extract-private 返回的完整模板 JSON 字符串。

当前需要对照：
- 详情要求的折叠端：{从 promotionAliasTemplateList 列出}
- 当前 payload 已提交的端：{从 payload 列出}
- 缺失端：{列出差集}
- 结构问题：{例如缺 positionAliasShow / 缺 creative 包装 / 缺 templateSchema / data 为空}
```

如果没有当前 `promotion-detail`，不能判断缺哪些端，应先查详情再回复；不要让用户自己猜。若预检脚本已输出错误，优先把脚本错误整理成上面的诊断格式。