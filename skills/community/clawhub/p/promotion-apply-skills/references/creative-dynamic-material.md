# Creative Dynamic Material Reference

## 核心规则

推广创意不是固定表单。图片、角标、标题、跳转链接、视频等字段来自当前数据模板 schema，不能写死为 `imgUrl/title/content/resUrl`。

涉及创意或素材时必须按顺序执行：

1. 调 `mws link promotion-detail` 获取推广详情。
2. 读取 `resourceTypes`、`resourceInfo`、`deliveryResourceList`、`promotionAliasTemplateList`、`promotionAliasCreativeList`。
3. 取 `resourceTypes[0]` 作为当前投放类型。示例：`["standard","song"]` 或 `["nonstandard","activity"]`。人工创建/历史推广可能缺少 `fullType/resourceTypes/resourceInfo`；缺失时先让用户补齐实际投放资源类型、标准资源 ID（标准资源时）、全量/非全量和非全量人群。直接修改、补配或换物料进入素材交互前，必须已经有资源类型和资源 ID（标准资源时），再继续默认值获取和模板提取。
4. 用 `deliveryResourceList` 校验投放类型：一级类型等于 `resourceType[0]`，二级类型等于 `resourceType[1]`。任意一级不存在都停止。
5. 标准资源且有资源 ID 时，必须先用 `mws link plan-pack-resource-list` 获取资源信息并保存返回 JSON；不能用资源 ID 手拼跳转链接。
6. 每个端都按 `positionCode + channelCode + firstResType + resType + resId` 单独调用 `mws link data-template-extract-private` 提取模板，并以该端模板 `preData` 为默认数据基底。
7. 每个端拿到模板后，收集 `schema.children[].resourceTypeCodes[].code`，再调用 `mws link component-code` 获取字段字典。
8. 基于模板 `preData` 填字段。本 skill 不修改已有创意。
9. 组包完成后，先把所有折叠端最终跳转链接发给用户确认；用户确认无误后，调 `mws link promotion-update-creative` 一次性保存推广物料。该方法是 AI 物料更新接口，已内嵌 `updateCreativeCheck`。保存时必须固定携带 `fullType/resourceType/resourceInfo/resourceTypes`，非全量还要携带 `strategyInfo` JSON 字符串。

禁止使用 `creative-add`。创建创意、添加创意、关联素材、验证创意结构、失败重试都不能调用 `creative-add`，也不能为了测试格式创建新推广或独立创意。素材保存只能通过 `promotion-update-creative` 把完整内嵌创意对象保存到推广。

禁止复用上一轮/上次任务的素材。图片、视频、NOS URL、角标、跳转链接、`templateSchema`、`creativeDetailDataVO` 都只能来自本轮用户输入、当前推广详情、当前端模板和本轮上传结果。即使上一轮图片尺寸相同、文件名相同或刚上传成功，也不能自动带到当前推广；只有用户在本轮明确说“所有端共用这张图”或“沿用当前推广已有素材”，才允许在当前推广内复用。

每次开始配物料、补配物料或换物料，都先清空上一轮配置上下文：不要复用浏览器页面残留的表单、旧 `/tmp/promotion-detail.json`、旧模板 JSON、旧默认值 JSON、旧 payload、旧裁剪图或旧 NOS 上传结果。为当前推广新建唯一工作目录，例如 `WORKDIR=/tmp/lingqu-banner-${promotionId}-$(date +%Y%m%d%H%M%S)`，本轮所有中间文件都写到该目录；第一步重新查当前 `promotion-detail`，再提模板和组包。

## 素材收集策略

创意素材可以一次性收齐后批量保存，尤其是用户已经把“投什么端、投什么资源、每端素材”都给到时，不要拆成多轮。

1. 单端投放：
   - 提取该端模板后，列出启用且必填字段。
   - 如果用户已经提供所有必填素材，直接校验、上传并保存。
   - 如果缺字段，只问缺的字段。
2. 多端投放：
   - 每个端都要先提取模板，得到该端自己的必填字段、图片尺寸、文本长度。
   - 默认每个端需要独立素材，不要默认移动端素材可复用到 PC/Web/Mac。
   - 只有用户明确说“所有端共用同一套素材”，且所有端对应字段名、字段含义、图片尺寸都一致时，才复用素材。
   - “共用素材”只对本轮当前推广有效，不表示可以复用上一轮、旧推广或历史测试的图片/NOS URL。
   - 如果模板不同，用矩阵一次性向用户收集：

```text
请一次性补齐各端素材：

移动端(iPhone&Android)
- 大卡图片：1080x607，必填
- 角标：最多 5 字，必填
- 跳转链接：必填，常见合法格式是 orpheus://... 或 https://y.music.163.com/g/yida/...

PC
- 图片：以 PC 模板返回尺寸为准，必填
- 跳转链接：必填，常见合法格式是 orpheus://... 或 https://y.music.163.com/g/yida/...
```

3. 多张图片输入：
   - 先按图片像素和用户描述匹配端/字段。
   - 尺寸唯一匹配时可以自动归位，例如 1080x607 只匹配移动端大卡图。
   - 一张图同时匹配多个端时，必须确认是否复用。
   - 一张图不匹配任何启用字段时，停止并说明期望尺寸。
   - 用户给 http/https 图片 URL 时，不能直接把该 URL 写入创意字段；必须先下载到本地临时文件，按当前模板做像素校验/裁剪确认，再走 [image-upload-nos.md](image-upload-nos.md) 的 token 和 NOS 上传流程，最终只把本轮新上传后的 NOS/CDN URL 写入 payload。即使原 URL 看起来已经是 NOS，也不能跳过重传，因为外部链接可能没有投放所需 CDN 缓存或访问策略。
   - 没有本轮图片输入时，不要从上次对话、旧 `/tmp` 文件、旧 NOS URL 或历史推广里拿图补位。
4. 批量保存：
   - 所有折叠端素材收齐后，构造一个完整 `promotionAliasCreativeList`，每个 `promotion-detail.promotionAliasTemplateList[].positionAlias` 一个节点。
   - 保存节点必须以当前 `promotion-detail.promotionAliasTemplateList` 返回的折叠后位置别名为准，不要按用户选择的所有投放端逐个提交。常见全端折叠结果是：移动端(iPhone&Android) 代表移动端/荣耀白牌/iPad(新版)/AndroidPad，另有 PC、Web、Mac、iPadHD(旧版)。
   - 如果推广实际有多个折叠后端，必须一次性提交所有折叠后端节点；不能只提交移动端或任意单端来“验证格式”。少传任一折叠端时，服务端会把缺失端视为没有素材，常见返回 `素材不能为空2`。用户只给一端素材时，先确认是否所有端共用；不是共用就补齐缺失端素材后再保存。
   - 每个节点下的 `creative` 都要带自己的 `dataTemplate.id`、完整 `templateSchema` 和 `creativeDetailDataVO`。
   - 最后只调用一次 `mws link promotion-update-creative --env ${MWS_ENV}` 保存整包，避免逐端覆盖其他端创意。

## promotion-update-creative 防变形规则

`promotion-update-creative` 的入参不要边试边改形状。保存前必须按下面规则一次组对：

1. `promotionAliasCreativeList.length` 必须等于当前 `promotion-detail.promotionAliasTemplateList.length`。如果详情返回 5 个折叠端，就提交 5 个节点；不是 1 个，也不是用户原始选择的 8 个端。`素材不能为空2` 首先按这一条排查：是否少传了某个折叠端。
2. `promotionAliasCreativeList[].positionAlias` 必须逐项来自 `promotionAliasTemplateList[].positionAlias`，建议保持接口返回顺序，每个 alias 只出现一次。
3. `positionAliasShow` 只是展示文案，必须从同一个 `promotionAliasTemplateList` 节点复制；不要把 `positionAliasShow` 里的“移动端/荣耀白牌/iPad(新版)/AndroidPad”拆成多个提交节点。
4. 移动端折叠节点示例：`positionAlias` 是 `移动端(iPhone&Android)`，`positionAliasShow` 可以是 `移动端(iPhone&Android)/荣耀白牌/iPad(新版)/AndroidPad`。这仍然只算一个节点，除非详情里另有单独的“荣耀白牌”“iPad(新版)”“AndroidPad”节点。
5. 每个节点的 `promotionCreativeList` 必须非空，且每一项必须是 `{ "creative": { ... } }` 包装结构。不要把 `name/tenant/dataTemplate/creativeDetailDataVO` 拍平到 `promotionCreativeList[]`。
6. 每个 `creative` 必须带 `dataTemplate.id`、`templateSchema`、`creativeDetailDataVO`。`templateSchema` 必须是该端 `data-template-extract-private` 返回的完整模板 JSON 字符串，不能省略、不能只传模板 ID、不能用占位符。
7. 图片字段必须是真实 NOS HTTPS URL。不要把 `NOS_URL`、本地文件路径、临时 token 或其它占位值写进最终 payload。模板允许空且字段未启用时才可以传空字符串。
8. JSON 里不能写注释，不能写 `// ... 其余7端` 这类省略。真实调用 payload 必须是完整合法 JSON，所有折叠端节点都明确写出。
9. 标准资源 URL 禁止手拼：只有 Web 默认跳转链接使用资源信息里的 `pcUrl` 或其它 http/https 链接；没有 http/https 时必须补问用户，禁止退化使用 `orpheus`。非 Web 端（移动端、荣耀白牌、PC、Mac、iPad、AndroidPad、iPadHD 等）必须使用 `plan-pack-resource-list` / `data-template-extract-private` 返回的客户端默认链接或模板 `preData`，例如 `composedData.commonComposedData.url`、顶层 `orpheus`；缺失时问用户提供端维度链接，不能用 `https://music.163.com/...` 这类 Web 链接兜底。

不要写以下形态：只提交一个端再写“其余端”；把 `positionAliasShow` 里的多端文案拆成多个节点；缺 `creative.templateSchema`；`creativeDetailDataVO.children[].data` 为空；把 `name/tenant/dataTemplate/creativeDetailDataVO` 拍平到 `promotionCreativeList[]`；图片字段写 `NOS_URL`、本地路径或 token。

正确形态的最小骨架如下。该片段只用于说明一个折叠端节点的内部结构，禁止直接执行；真实调用时，`promotionAliasCreativeList` 必须由当前 `promotionAliasTemplateList` 映射生成完整节点，`templateSchema` 必须替换为当前端完整模板 JSON 字符串：

```json
{
  "positionAlias": "移动端(iPhone&Android)",
  "positionAliasShow": "移动端(iPhone&Android)/荣耀白牌/iPad(新版)/AndroidPad",
  "promotionCreativeList": [
    {
      "creative": {
        "name": "zyx8_mobile_20260612152531",
        "tenant": "music",
        "dataTemplate": {"id": 160002},
        "templateSchema": "{...当前端完整模板 JSON 字符串...}",
        "creativeDetailDataVO": {
          "children": [
            {
              "code": "bannerImageTypeCode",
              "data": {
                "pic": "https://p5.music.126.net/xxx-pic.jpg",
                "typeTitle": "新歌首发",
                "url": "orpheus://song/525253122",
                "bigPic": "https://p5.music.126.net/xxx-big.jpg"
              }
            }
          ]
        }
      }
    }
  ]
}
```

真实调用前必须先把整包 payload 保存为 JSON 文件，并用当前 `promotion-detail` 做预检。`--detail` 是硬要求；没有当前详情就无法确认折叠端是否全部提交，禁止调用 MWS。预检失败时只修 payload，不调用 MWS，也不换成其它接口：

```bash
WORKDIR="/tmp/lingqu-banner-1200000576814-$(date +%Y%m%d%H%M%S)"
mkdir -p "$WORKDIR"
mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000576814"}' --format json > "$WORKDIR/promotion-detail.json"
mws link plan-pack-resource-list --env ${MWS_ENV} --params '{"resourceType":"song","resourceIds":"108485"}' --format json > "$WORKDIR/plan-pack-resource-list.json"
python3 scripts/validate_update_creative_payload.py \
  "$WORKDIR/promotion-update-creative.json" \
  --detail "$WORKDIR/promotion-detail.json" \
  --resource-defaults "$WORKDIR/plan-pack-resource-list.json"
```

脚本会拦截最常见错误：没有传当前详情、标准资源没有传 `--resource-defaults` 证明已调用默认值接口、折叠端数量/顺序不一致、`positionAliasShow` 没按详情复制、`promotionCreativeList` 拍平、只传 `templateId/resourceTypeCode/data` 简化结构、缺 `creative.templateSchema`、模板 JSON 字符串不合法、图片字段仍是本地路径或占位符、资源字段和非全量人群字段缺失、标准资源非 Web 端手拼 `music.163.com` Web 链接。

`promotion-update-creative` 常见错误对照：

| 错误/现象 | 常见原因 | 处理 |
|---|---|---|
| `素材不能为空2` | 1. 只传了部分折叠端，例如全端推广只传移动端；2. `promotionCreativeList[]` 用了 `templateId/resourceTypeCode/data` 简化结构，没有 `{ "creative": {...} }` 包装；3. 某个折叠端的 `creative.templateSchema` / `creativeDetailDataVO.children[].data` 缺失，服务端解析后认为该端素材为空 | 先查当前 `promotion-detail.promotionAliasTemplateList`，按它的数量、顺序、`positionAlias`、`positionAliasShow` 一次性补齐所有折叠端；每端都必须是完整 `creative` 包装，包含 `dataTemplate.id`、完整 `templateSchema`、`creativeDetailDataVO.children[].data`。不要改 `fullType`、不要重建、不要逐端试。 |
| `素材不能为空1` | 有 `creative` 包装但缺 `creative.templateSchema`，或模板字符串不是完整模板 JSON | 每个 `creative.templateSchema` 都填当前端 `data-template-extract-private` 返回的完整 JSON 字符串 |
| `推广关联位置错误` | 给了错误的 `positionAlias` / `positionAliasShow`，或把 `dataTemplate` 放到错误层级 | `positionAlias` 和 `positionAliasShow` 从同一个 `promotionAliasTemplateList` 节点复制；`dataTemplate` 放在 `creative` 内 |
| `Column 'name' cannot be null` / `Music_Link_Creative ... name ... null` | 成品创意 JSON 绕过了本 skill 的创意名称生成，`creative.name` 为空，服务端插入 `Music_Link_Creative.name` 时触发数据库非空约束 | 不要在原 JSON 上只补一个名字后重试。回到本页“创意名称生成”规则，重新查当前推广详情，按每个折叠端生成唯一 `creative.name`，同时补齐 `tenant/dataTemplate/templateSchema/creativeDetailDataVO` 并跑预检。 |
| 500 系统错误 | 结构层级混乱，例如 `dataTemplate` 外层和 `creative` 内层混传 | 回到本节骨架，只保留 `promotionAliasCreativeList[].promotionCreativeList[].creative` 这一种结构 |
| dry-run 通过但真实保存失败 | dry-run 只校验 schema 形状，不校验服务端物料完整性 | 不换接口；按本表检查折叠端、`creative` 包装、`templateSchema`、图片 URL 和资源字段 |
| `creative-add` 成功但推广仍未保存素材 | `creative-add` 是独立创意创建，不等于推广物料保存 | 禁止使用 `creative-add`；所有素材必须通过 `promotion-update-creative` 保存到推广 |

如果上表都确认无误，仍持续返回“素材不能为空1/2”，停止试错，报告 `promotion-update-creative` 的原始错误和关键入参摘要；不要改用 `creative-add`、`promotion-update`、HTTP 直连或创建新推广验证。

## 资源类型判定

推广详情里的资源类型是二维数组，当前投放类型取第一项：

```json
{
  "resourceTypes": [["standard", "song"]],
  "resourceInfo": "111",
  "deliveryResourceList": [
    {
      "code": "standard",
      "subResources": [{ "code": "song" }]
    }
  ]
}
```

判定规则：

1. `resourceTypes` 不是数组、为空、或第一项不是数组时，停止当前保存动作并要求用户选择实际投放资源。使用 `scripts/promotion_resource_wizard.py choices` 根据 `deliveryResourceList` 展示可选项；不要用推广基础的 `deliveryResource` 标签、旧创意或上游 URL 反推。
2. `resourceType = resourceTypes[0]`。
3. `topType = resourceType[0]`，`subType = resourceType[1]`。
4. 在 `deliveryResourceList` 中查找 `code == topType`。
5. 如果存在 `subType`，还要在 `subResources` 中查找 `code == subType`。
6. 校验失败时不要继续生成模板，应提示“当前投放类型不在可投放资源列表中，需要先修改推广投放类型”。
7. 用户选择投放资源后，使用 `scripts/promotion_resource_wizard.py select` 校验并生成标准化结构和每个端的模板提取命令；禁止默认选择任一资源。若详情缺 `fullType`，同时要求用户确认全量/非全量；非全量必须补人群并生成 `strategyInfo` JSON 字符串，随 `promotion-update-creative` 同包提交。

保存物料前需要转换：

```json
{
  "resourceType": "song",
  "resourceTypes": [["standard", "song"]],
  "resourceInfo": "111"
}
```

其中 `resourceType` 是二级资源类型字符串，不能传 `["standard","song"]`；`resourceTypes` 才是二维数组；`resourceInfo` 是标准资源 ID 字符串，非标资源通常为空。

## 标准资源详情

当投放类型是标准资源，例如 `["standard","song"]` 且资源 ID 为 `111`，必须先获取资源信息。

```bash
mws link plan-pack-resource-list --env ${MWS_ENV} --params '{
  "resourceType": "song",
  "resourceIds": "111"
}'
```

参数规则：

- 必须通过 `mws link plan-pack-resource-list` 调用，禁止 curl/HTTP 直连 `/api/link/platform/plan/pack/resource/list`。
- 资源 ID 参数名必须是 `resourceIds`，不能写 `resourceId`。`resourceIds` 是字符串，多个 ID 用英文逗号拼接。
- 如果接口报 `Required String parameter 'resourceIds' is not present`，说明用了 `resourceId` 单数或没传参数；直接改成 `resourceIds` 后重试，不要改用其它接口。

用途：

- 校验资源 ID 是否存在；返回空时，只有标准歌曲可以使用固定兜底链接：非 Web 端 `orpheus://song/{歌曲ID}`，Web 端 `https://music.163.com/#/song?id={歌曲ID}`，但默认角标仍视为缺失。其它标准类型（专辑/MV/歌单等）先不使用默认兜底，提示资源可能不存在或未上线，要求用户手工提供角标、端维度跳转链接和素材后再继续。
- 作为标题、歌手、封面、跳转链接、角标等默认值来源。
- 用户显式提供的素材字段优先覆盖资源默认值。

可直接用脚本提取默认值：

```bash
mws link plan-pack-resource-list --env ${MWS_ENV} --params '{"resourceType":"song","resourceIds":"111"}' --format json \
  | python3 scripts/resource_defaults.py
```

默认值规则：

- `composedData.commonComposedData.bannerLabel`：用户没给角标时作为默认角标。
- 跳转链接默认值必须按端选择：只有 Web 优先用顶层 `pcUrl` 或其它 http/https 链接；如果资源没有任何 http/https 链接，Web 链接视为缺失，必须让用户手工提供，禁止退化使用 `orpheus`。移动端、荣耀白牌、PC、Mac、iPad、AndroidPad、iPadHD 等非 Web 端优先用 `composedData.commonComposedData.url`、顶层 `orpheus` 或该端 `data-template-extract-private` 模板 `preData` 里的默认链接；没有客户端默认值时必须问用户提供端维度链接，禁止用 `pcUrl` 或手拼 `https://music.163.com/...` 兜底。
- 如果 `plan-pack-resource-list` 已调用但返回空，且 `resourceType=song`，允许歌曲固定兜底：非 Web 端 `orpheus://song/{歌曲ID}`，Web 端 `https://music.163.com/#/song?id={歌曲ID}`。除歌曲外的其它标准类型不使用默认兜底。
- 顶层 `name`、`producerName` / `producerNames`：用于向用户确认资源。
- 用户显式提供的角标、链接、标题、图片始终优先于资源默认值。

标准资源的可用信息以 `plan-pack-resource-list` 和 `data-template-extract-private` 返回为准。没有单独资源模板组装方法时，不手写固定字段；只在当前模板 `preData` 的基础上覆盖用户明确提供的字段或资源默认值。最终保存前必须向用户展示端维度链接确认，例如：

```text
请确认最终跳转链接：
- 移动端(iPhone&Android)：orpheus://...
- PC：orpheus://...（来自资源/模板默认值）
- Web：https://music.163.com/...

确认后我再保存物料。
```

## 多端模板

每个端都要单独提取模板，即使多个端最终命中相同 code，也不能省掉端维度。

投放端配置必须从接口获取，不能写死或声明来自配置中心：

```bash
mws link promotion-position-alias --env ${MWS_ENV} --params '{"biz":"banner"}' --format json
```

接口返回是 `code/data/message` 结构，真实端配置在 `data[]` 中；每项包含 `positionAlias`、`positionCode`、`channelCode`。常见返回如下，仅作说明：

| `positionAlias` | `positionCode` | `channelCode` |
|---|---|---|
| 移动端(iPhone&Android) | `PAGE_DISCOVERY_BANNER@mobile` | `page_discovery_banner_channel` |
| 荣耀白牌 | `PAGE_DISCOVERY_BANNER@magios` | `page_discovery_banner_channel_magios` |
| PC | `BANNER_PC_V2` | `pc_banner_op_channel` |
| Web | `BANNER_WEB` | `web_banner_op_channel` |
| Mac | `BANNER_MAC` | `mac_banner_op_channel` |
| iPad(新版) | `PAGE_DISCOVERY_BANNER@newIpad` | `page_discovery_banner_channel_new_ipad` |
| AndroidPad | `PAGE_DISCOVERY_BANNER@androidPad` | `page_discovery_banner_channel_android_pad` |
| iPadHD(旧版) | `BANNER_IPAD_HD` | `ipad_hd_banner_op_channel` |

标准歌曲 `song=111` 的端参数示例：

| 端/别名 | `positionCode` | `channelCode` | `firstResType` | `resType` | `resId` |
|---|---|---|---|---|---|
| 移动端(iPhone&Android) | `PAGE_DISCOVERY_BANNER@mobile` | `page_discovery_banner_channel` | `standard` | `song` | `111` |
| 荣耀白牌 | `PAGE_DISCOVERY_BANNER@magios` | `page_discovery_banner_channel_magios` | `standard` | `song` | `111` |
| PC | `BANNER_PC_V2` | `pc_banner_op_channel` | `standard` | `song` | `111` |
| Web | `BANNER_WEB` | `web_banner_op_channel` | `standard` | `song` | `111` |
| Mac | `BANNER_MAC` | `mac_banner_op_channel` | `standard` | `song` | `111` |
| iPad(新版) | `PAGE_DISCOVERY_BANNER@newIpad` | `page_discovery_banner_channel_new_ipad` | `standard` | `song` | `111` |
| AndroidPad | `PAGE_DISCOVERY_BANNER@androidPad` | `page_discovery_banner_channel_android_pad` | `standard` | `song` | `111` |
| iPadHD(旧版) | `BANNER_IPAD_HD` | `ipad_hd_banner_op_channel` | `standard` | `song` | `111` |

非标资源示例：

```json
{
  "positionCode": "PAGE_DISCOVERY_BANNER@mobile",
  "channelCode": "page_discovery_banner_channel",
  "firstResType": "nonstandard",
  "resType": "activity"
}
```

必须用 `mws link data-template-extract-private` 获取提交创意所需的完整模板。`mws link position-channel-data-template` / `mws link template-detail-get` 只能辅助排查模板配置，不能替代动态模板提取。

保存整包前要处理折叠端：

- 以当前 `promotion-detail.promotionAliasTemplateList` 返回的折叠后位置别名为准组装 `promotionAliasCreativeList`，不要按用户选择端原样全量提交。
- 如果“移动端(iPhone&Android)”同时覆盖荣耀白牌、iPad(新版)、AndroidPad，就只提交“移动端(iPhone&Android)”节点；如果详情里单独返回“荣耀白牌”，才按荣耀白牌节点提交。
- 如果折叠后仍有多个端，例如移动端、PC、Web、Mac、iPadHD(旧版)，必须全部提交；只提交其中一个端不是有效验证，可能导致其它端素材缺失并返回“素材不能为空2”。
- 如果把折叠端和被折叠端都提交，真实保存可能返回“素材不能为空1/2”。

## 组件字段字典

模板提取后必须收集所有资源类型 code：

```text
template.schema.children[].resourceTypeCodes[].code
```

然后查询组件字典：

```bash
mws link component-code --env ${MWS_ENV} --params '{
  "codes": "[\"bannerImageType4WebAndOther\",\"bannerImageType4PcAndMac\"]"
}'
```

`codes` 是 JSON 数组字符串。

用途：

- 获取字段中文名、字段名、输入类型、值类型。
- 识别图片、视频、跳转链接、角标等字段。
- 生成用户需要补充的素材清单。
- 辅助读取图片宽高、文本长度等要求。

如果 `component-code` 缺失目标 code，停止并提示“模板资源类型未注册或 WMS 组件字典缺失”。

## 动态字段填充

不要写死字段名。按模板字段定义填值：

1. 找到模板节点：通常从 `preData.children[]` 与 `schema.children[]` 的 code 对齐。
2. 解析节点 `conditionConfig`。常见结构：

```json
{
  "bannerImageType4WebAndOther": {
    "pic": {
      "select": "true",
      "require": "true",
      "width": 1080,
      "height": 420
    }
  }
}
```

3. 遍历 `resourceTypeFieldList`：
   - `fieldName` 是写入 `creativeDetailDataVO.children[].data` 的 key。
   - `fieldChineseName` 给用户展示。
   - `uiType` / `valueType` 决定值类型。
4. 复制 `preData.children[].data` 作为初始 data。
5. 用户提供图片、角标、标题、链接时，按 `fieldChineseName`、`fieldName` 和业务语义匹配字段，并覆盖默认值。
6. 对未知必填字段，不要猜；列出字段中文名、`fieldName`、尺寸/长度规则让用户补。

## 图片尺寸校验

图片尺寸来自当前模板 `conditionConfig`。解析规则：

- `hidden == true`：字段隐藏，跳过。
- `select == true` 或 `select == "true"`：字段通常启用。
- `require == true` 或 `require == "true"`：只有字段启用时才按必填处理。
- `select == false` 且字段不在 `preData.children[].data` 中时，不要因为 `require == true` 强制填写。
- 字段在最终 data 中有值，或用户为该字段提供了本地文件时，必须按该字段 `width` / `height` 校验像素。
- `maxLength` 存在时必须校验文本长度。

校验命令：

```bash
python3 scripts/validate_image_size.py \
  /tmp/banner_pic.jpg 1080 420
```

如果用户给一张图要同时用于多个字段，必须分别校验每个字段的尺寸。例如一个端可能同时有 `pic=1080x420`、`bigPic=1080x607`，不能直接复用。

尺寸不符时的处理：

- 原图宽高都大于目标宽高时，可以先问用户是否允许中心裁剪/缩放到模板尺寸。
- 原图任一边小于目标宽高时，禁止放大裁剪，要求用户补更大原图。
- 使用 `scripts/resize_cover.py` 裁剪后，必须让用户确认；如果当前客户端能渲染本地图片，用 Markdown 图片语法真实展示生成图，图片链接必须是本地绝对路径，不能用 `~` 或相对路径；如果不能渲染，只给本地绝对路径并说明需要用户打开确认，不要声称已经展示预览。用户确认后才上传 NOS。
- 不要把未经用户确认的裁剪图直接上传或保存到推广。

## 内嵌创意对象结构

推广物料保存时，创意对象必须内嵌在 `promotion-update-creative` 的 `promotionAliasCreativeList[].promotionCreativeList[].creative` 中。关键字段：

| 字段 | 规则 |
|---|---|
| `tenant` | 固定 `music` |
| `name` | 创意名称，1 到 50 字符 |
| `dataTemplate.id` | 对应端当前模板 ID |
| `templateSchema` | 完整模板对象 JSON 字符串 |
| `creativeDetailDataVO` | 动态字段数据对象 |
| `ableToReuse` | 通常传 `true` |
| `needDiffIntervention` | 通常传 `false` |

### 创意名称生成

当前常见重名原因是只使用固定前缀（例如 `banner创意` / 推广名 + `_创意`）或只精确到秒的时间戳；同一批多端保存、同一秒重试、复制旧创意时都可能撞名。保存物料时必须按下面规则生成或保留创意名：

1. 当前详情里已有 `creative.id` 且本次是在更新同一个创意时，只有原 `creative.name` 已符合本节唯一命名规则，或用户明确要求保留原名，才保留原名。
2. 新增创意、复制旧创意到另一个端、用模板新组装出来的创意，或遇到 `wyt_mobile`、`banner创意_20260611144618`、`推广名_创意` 这类不含推广 ID/端别名/模板 ID/唯一后缀的旧名称时，必须生成新名称。不能复用模板名、推广名、`banner创意_YYYYMMDDHHmmss`、上一轮 payload 里的名称，或仅靠端名区分的短名称。
3. 新名称必须包含推广 ID、端别名、排期时间段和模板 ID，并带短唯一后缀。推荐格式：

```text
p{promotionId}_{aliasKey}_{timeKey}_t{templateId}_{unique}
```

示例：

```text
p1056003_mobile_0617_t160002_0930121
p1056003_pc_0617_t1175202_0930122
p1056003_web_0617_t1176202_0930123
```

4. `aliasKey` 使用折叠后的 `positionAlias` 转短码，例如 `移动端(iPhone&Android)=mobile`、`荣耀白牌=magios`、`PC=pc`、`Web=web`、`Mac=mac`、`iPad(新版)=ipad`、`AndroidPad=androidpad`、`iPadHD(旧版)=ipadhd`；未知端用清洗后的英文/拼音短码。
5. `timeKey` 来自本条推广/排期的投放时间：单日用 `MMDD`，跨日用 `MMDD-MMDD`，小时段需要区分时用 `MMDDHHmm-HHmm`。如果推广按时间拆分成多条，必须使用每条自己的时间段；如果同时按端拆分，也必须在每个端的创意名里保留该时间段。
6. `unique` 可用 `HHmmss + seq`、毫秒时间低位或 6 到 8 位短随机串；同一批 payload 内每个端不同即可。
7. 保存前必须收集两类名称做去重：本次 payload 中的所有 `creative.name`，以及当前 `promotion-detail.promotionAliasCreativeList[].promotionCreativeList[].creative.name`。如果新名称已存在，递增 `seq` 或重新生成短随机串，直到不重复。同一个 `creative.id` 的旧名如果被判定为不规范，也要重命名后提交。
8. 多端共用同一套素材时，也要为每个折叠后端生成不同的 `creative.name`；不能因为素材相同就把同一个名字复制到所有端。拆端保存时，每个端名都必须同时包含 `aliasKey` 和 `timeKey`，例如 `p1056003_mobile_0617_...`、`p1056003_pc_0617_...`。
9. 数据库字段 `name` 是 `varchar(128)`；生成后必须校验长度不超过 128。上述推荐格式通常只有 35 到 60 个字符；如果未知端短码过长，优先缩短 `aliasKey`，但不能删除推广 ID、端短码、时间段、模板 ID 和唯一后缀。

示例结构：

```json
{
  "positionAlias": "移动端(iPhone&Android)",
  "positionAliasShow": "移动端(iPhone&Android)",
  "promotionCreativeList": [
    {
      "creative": {
        "tenant": "music",
        "name": "banner创意_20260611144618",
        "dataTemplate": { "id": 160002 },
        "templateSchema": "{\"id\":160002,\"schema\":{},\"preData\":{}}",
        "creativeDetailDataVO": {
          "children": [
            {
              "code": "bannerImageTypeCode",
              "data": {
                "typeTitle": "新歌首发",
                "url": "orpheus://song/111",
                "bigPic": "https://p5.music.126.net/xxx.jpg"
              }
            }
          ]
        }
      }
    }
  ]
}
```

注意：

- `promotionCreativeList[]` 每一项必须是 `{ "creative": { ... } }` 包装结构。不要把 `name`、`tenant`、`dataTemplate`、`creativeDetailDataVO` 直接拍平到 `promotionCreativeList[]` 项上。
- `templateSchema` 必须是完整模板 JSON 字符串，不能只传模板 ID。
- `dataTemplate.id` 必须和模板 ID 一致。
- `creativeDetailDataVO.children[].code` 必须等于模板节点 code。
- `creativeDetailDataVO.children[].data` 的 key 来自模板字段 `fieldName`。
- 投放资源类型、资源 ID、全量/非全量和人群可以在 `promotion-add` 创建阶段写入，也可以第二阶段配物料前补齐。保存物料时必须把已确认值同包携带到 `promotion-update-creative`：`fullType/resourceType/resourceInfo/resourceTypes`，非全量再传 `strategyInfo` JSON 字符串。直接修改、补配或换物料时，必须先补齐资源类型、标准资源 ID（标准资源时）、全量/非全量和非全量人群，再获取默认值、提取模板和收集素材。人工创建/历史推广缺少这些字段时，先补问并标准化，再在本次 `promotion-update-creative` 同包传入；不要用 `promotion-update` 后补。用户素材阶段修改了资源/投放量/人群时使用新值，否则沿用创建阶段或详情值。
- 每个 `creative.name` 必须按“创意名称生成”规则生成或保留：本次请求中唯一，也要避免和当前推广已有创意重名。真实调用返回“存在重名创意”时，只改创意名为每端唯一后用 `promotion-update-creative` 重试，不要改走其它接口。
- 当前详情里已有创意 ID 时，可以保留 `creative.id`；新增物料没有 ID 就不传。禁止为了拿创意 ID 调用 `creative-add`。

多端保存结构示意，禁止直接执行。真实保存必须使用当前推广详情、当前模板和本轮素材生成完整 JSON，再通过预检脚本：

```json
{
  "id": 1200000578804,
  "fullType": "nofull",
  "resourceType": "song",
  "resourceInfo": "525253122",
  "resourceTypes": [["standard", "song"]],
  "strategyInfo": "{\"crowd\":{\"sceneId\":29,\"crowdIds\":[3691],\"op\":\"contain\"}}",
  "promotionAliasCreativeList": [
    {
      "positionAlias": "移动端(iPhone&Android)",
      "positionAliasShow": "移动端(iPhone&Android)",
      "promotionCreativeList": [
        {
          "creative": {
            "tenant": "music",
            "name": "zyx_0612_mobile_20260612143000",
            "dataTemplate": {"id": 160002},
            "templateSchema": "{...移动端完整模板 JSON 字符串...}",
            "creativeDetailDataVO": {
              "children": [
                {
                  "code": "bannerImageTypeCode",
                  "data": {
                    "pic": "",
                    "typeTitle": "新歌首发",
                    "url": "orpheus://song/525253122",
                    "bigPic": "https://p5.music.126.net/xxx-big.jpg"
                  }
                }
              ]
            }
          }
        }
      ]
    },
    {
      "positionAlias": "PC",
      "positionAliasShow": "PC",
      "promotionCreativeList": [
        {
          "creative": {
            "tenant": "music",
            "name": "zyx_0612_pc_20260612143000",
            "dataTemplate": {"id": 1000000017001},
            "templateSchema": "{...PC 完整模板 JSON 字符串...}",
            "creativeDetailDataVO": {
              "children": [
                {
                  "code": "bannerImageType4PcAndMac",
                  "data": {
                    "pic": "https://p5.music.126.net/xxx-pic.jpg",
                    "typeTitle": "新歌首发",
                    "url": "orpheus://song/525253122",
                    "bigPic": "https://p5.music.126.net/xxx-big.jpg"
                  }
                }
              ]
            }
          }
        }
      ]
    },
    {
      "positionAlias": "Web",
      "positionAliasShow": "Web",
      "promotionCreativeList": [
        {
          "creative": {
            "tenant": "music",
            "name": "zyx_0612_web_20260612143000",
            "dataTemplate": {"id": 1000000017005},
            "templateSchema": "{...Web 完整模板 JSON 字符串...}",
            "creativeDetailDataVO": {
              "children": [
                {
                  "code": "bannerImageType4WebAndOther",
                  "data": {
                    "pic": "https://p5.music.126.net/xxx-pic.jpg",
                    "typeTitle": "新歌首发",
                    "url": "https://music.163.com/#/song?id=525253122"
                  }
                }
              ]
            }
          }
        }
      ]
    }
  ]
}
```

上面只展示结构，真实保存必须按当前 `promotionAliasTemplateList` 追加所有折叠后端。`templateSchema` 不能用占位符，必须替换为每个端模板的完整 JSON 字符串；`pic/bigPic/url/typeTitle` 必须来自本轮素材或当前资源默认值。

## 已有创意

本 skill 不修改已有创意。用户提供历史创意 ID 时，不能只把 ID 塞进 `promotionCreativeList`，必须按当前模板组出完整 `creative`、`templateSchema` 和 `creativeDetailDataVO`。如果无法组出完整对象，停止并说明当前 skill 仅支持按当前模板重新保存一份推广物料。真实调用报“素材不能为空”时，按本页保存前检查排查，不要临时翻代码猜字段，不要调用 `creative-add`。

## 保存到推广

保存物料必须使用当前 schema 允许的结构，包含推广 ID、端别名、端展示文案和完整内嵌创意，并固定带上 `fullType/resourceType/resourceInfo/resourceTypes`；非全量固定带 `strategyInfo` JSON 字符串；审批场景再补 `businessRemark/relateTask`。不要添加 schema 不存在的顶层字段，也不要复用文档里的固定 payload。真实入参必须来自当前 `mws schema link.promotion-update-creative`、当前推广详情、当前端模板和本轮素材。

如果用户或上游已经给出完整 `promotion-update-creative` 命令或成品 `promotionAliasCreativeList` JSON，不要直接执行，也不要在原 JSON 上补字段后执行。必须把它拆回业务输入：推广 ID、投放资源、资源 ID、全量/非全量、人群、原始图片素材、角标、跳转链接、审批说明，然后按本页流程重新查详情、获取默认值、提模板、上传图片、生成创意名、补全所有折叠端并预检。

如果一个位置别名已有多个创意，先从 `promotion-detail` 读取原 `promotionAliasCreativeList`，在原列表上增删改对应项，再整体提交，避免覆盖其他端或其他创意。

审批处理：

- `promotion-update-creative` 内嵌物料更新校验。命中审批码 `31003`（`PROMOTION_UPDATE_CREATIVE`）时，未传 `businessRemark` 会返回 `needApproval=true`。
- 收到 `needApproval=true` 时，向用户补问这次物料更新的审批说明，然后使用同一份整包参数补 `businessRemark` 重试；接口会自动发起 `updateCreativeApproval`。
- 如果用户本轮已经明确给了审批说明，可以在首次调用时直接传 `businessRemark`。
- `relateTask` 是可选字段，只有用户明确给了需求单/任务号时才传。
- 不要单独调用 `updateCreativeCheck` / `updateCreativeApproval`，也不要为用户猜审批说明。

保存前检查：

- `promotion-update-creative` 当前 schema 接收 `id`、`promotionAliasCreativeList`、`fullType`、`resourceType`、`resourceInfo`、`resourceTypes`、`strategyInfo`、`businessRemark`、`relateTask`。
- 每次保存物料都必须把 `fullType/resourceType/resourceInfo/resourceTypes` 放进 `promotion-update-creative`；`fullType` 必须是 `full` 或 `nofull`，不能沿用人工历史推广详情里的空串。人工创建/历史推广详情缺字段时，先问用户补齐实际投放资源类型、标准资源 ID（标准资源时）、全量/非全量和非全量人群，再继续保存。直接修改、补配或换物料的标准资源如果还没有资源 ID，必须先补问，不能提模板、不能生成最终素材包。非全量时必须把人群放进 `strategyInfo` JSON 字符串。不要传 `op/crowdIds/forceSave` 这类 schema 不存在的顶层字段。
- `promotionAliasCreativeList[]` 每个节点必须包含 `positionAlias` 和 `positionAliasShow`。`positionAliasShow` 优先从当前详情的 `promotionAliasTemplateList` 或原 `promotionAliasCreativeList` 同 alias 节点复制；没有时用 `positionAlias` 同值。
- `promotionCreativeList[]` 每个元素必须包含 `creative` 包装对象，且 `templateSchema` 位于 `creative.templateSchema`。拍平结构会让服务端无法按推广物料结构解析。
- 标准歌曲在 `promotion-add` 阶段必须写入资源类型，例如 `relatedResourceTypes:"song"`；资源 ID 如果创建阶段已提供则同时写入 `relatedResourceIds:"108485"`，如果创建阶段未提供，则必须在第二阶段配物料/直接修改/换物料前补齐。
- 非标活动通常只需要写入资源类型，例如 `relatedResourceTypes:"activity"`，没有资源 ID 时 `relatedResourceIds` 留空或不传。
- 不要按用户选择端原样提交全部节点；必须按 `promotionAliasTemplateList` 的折叠后节点提交。
- 多端推广不能只提交一个端；每个折叠后端都要有非空 `promotionCreativeList`。如果所有端共用素材，也要复制成每个折叠后端各自的创意节点，而不是只传一个端。
- 不要把本地文件路径、临时占位值或未上传的 token 写入图片字段；图片字段必须是最终可访问 URL。
- 用户提供的 http/https 图片 URL 也视为原始素材，不是最终可写入 URL；必须下载到本地后按当前图片流程重新校验、上传 NOS，并使用本轮上传产物。只有 `promotion-detail` 里已有素材且用户明确说“沿用当前推广已有素材”时，才可以保留已有图片 URL。
- 不要把上一轮/上次任务上传得到的图片 URL 当作当前素材。除非用户本轮明确要求沿用当前推广已有素材，否则每次保存都使用本轮新确认的图片或当前 `promotion-detail` 中明确存在且用户确认保留的素材。
- 调用 `promotion-update-creative` 前必须先运行 `scripts/validate_update_creative_payload.py`；脚本未通过时禁止 `--dry-run` 和真实写入。标准资源必须把本轮 `plan-pack-resource-list` 返回 JSON 通过 `--resource-defaults` 传入脚本，否则预检失败。该脚本会拦截空 `fullType`、缺折叠端、拍平创意结构、图片占位值、Web 端跳转链接不是 http/https，以及标准资源非 Web 端手拼 `music.163.com` 链接的情况。
- 如果真实调用持续返回“素材不能为空2”，且已确认折叠端、`positionAliasShow`、`fullType/resourceType/resourceInfo/resourceTypes`、完整 `creative/templateSchema/creativeDetailDataVO` 和图片 URL 都正确，不要继续换格式试，也不要调用 `creative-add`；停止并报告 `promotion-update-creative` 的原始错误和关键入参摘要。

全量/非全量和人群字段可以创建阶段写入，也可以第二阶段保存物料前补齐：

- 全量：创建阶段已明确时可在 `promotion-add` 传 `fullType:"full"`；未明确时，第二阶段保存前补问并随 `promotion-update-creative` 传 `fullType:"full"`。
- 非全量：保存物料前必须先调用 `mws link plan-check --env ${MWS_ENV}` 校验人群包；创建阶段已给齐时可提前校验并在 `promotion-add` 传 `fullType:"nofull"`、`strategyInfo.crowd` 和/或 `crowdList`。创建阶段未给齐时，第二阶段补问并随 `promotion-update-creative` 传 `fullType:"nofull"` 和 `strategyInfo` JSON 字符串。
- 人群包含/不包含：`strategyInfo.crowd.op` 使用 `contain` / `notcontain`；`crowdList[].type` 使用 `include` / `exclude`，两处枚举不同，不要混用。
- `plan-check.positionCode` 用当前端 `positionCode` 的 `@` 前缀：`PAGE_DISCOVERY_BANNER@mobile` 传 `PAGE_DISCOVERY_BANNER`；没有 `@` 时传原值。

默认两阶段流程里，第一阶段创建推广可以只完成基础字段和预占；投放资源类型、标准资源 ID、全量/非全量和人群都允许在第二阶段配物料前补齐。第二阶段补创意素材、直接修改或换物料时，不论详情是否已有这些信息，都要随 `promotion-update-creative` 同包提交已确认值；标准资源必须先有资源 ID，非全量必须先有人群，才能获取默认值、提取模板和最终保存。若第一阶段是人工创建导致信息缺失，第二阶段必须补问这些初始化字段并同包提交，不能跳过。

跳转链接校验：标准资源优先走资源/模板默认值，禁止用资源 ID 手拼。Web 端必须是 http/https；非 Web 端优先是资源/模板返回的客户端链接，不能用 `music.163.com` Web 链接兜底。如果用户显式提供端维度链接，先把最终端维度链接列表发给用户确认，确认后才继续。不要给 `promotion-update-creative` 添加 schema 中不存在的 `forceSave` 字段；`businessRemark` 只用于物料更新命中 31003 审批时发起审批。

非全量基础信息示例，优先传给 `promotion-add`；物料保存阶段也要把 `strategyInfo` 序列化为 JSON 字符串传给 `promotion-update-creative`：

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
    {"crowdId": 3691, "sceneId": 29, "type": "exclude"}
  ]
}
```

`promotion-update-creative` 保存素材至少要传：

```json
{
  "id": 1200000576814,
  "fullType": "nofull",
  "resourceType": "song",
  "resourceInfo": "108485",
  "resourceTypes": [["standard", "song"]],
  "strategyInfo": "{\"crowd\":{\"sceneId\":29,\"crowdIds\":[3691],\"op\":\"contain\"}}",
  "promotionAliasCreativeList": [],
  "businessRemark": "命中审批时传审批说明",
  "relateTask": "用户明确给需求单时传"
}
```

素材创建流程必须使用 `promotion-update-creative` 保存创意物料；资源、投放量、人群可以来自创建阶段，也可以来自第二阶段前置补问，并且每次保存素材都按当前 schema 随物料保存请求一起提交。禁止使用 `creative-add`、`promotion-update`、`mws_exec`、`raw_call`、curl/HTTP 直连或其它接口替代。
