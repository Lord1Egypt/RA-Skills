# 操作与数据结构

## 导入与预检

`catalog.inspect` 输入 `library_id`、`expected_version`、`data`。首次也可省略库ID创建新库。建议先创建库并上传素材。data示例（替换真实asset_id）：

```json
{"title":"标准配件","template":"cards","show_prices":true,"products":[{"sku":"001","name":"螺栓","category":"五金","description":"标准钢制配件","specifications":[{"label":"直径","value":"10 mm"}],"image_id":"上传返回的asset_id","price":{"amount":"12.30","currency":"USD","unit":"piece","confirmed":true}}]}
```

template为`cards`四卡一页或`details`单品详页，SKU为唯一非空文本，最多200个。名称≤120、分类≤100、说明≤2000字符，规格≤8组。金额用十进制字符串，不换算、不自动舍入；显示价格必须明确确认金额、币种和单位。返回version用于乐观锁，冲突重新读取，不能覆盖别人的修改。

## 可选模型翻译

`catalog.translate` 输入`library_id`、`expected_version`、`language`（en或zh-Hans）。返回候选及真实用量，approved=false。模型只翻译文字字段和规格标签，保留SKU、型号、数值、规格值、币种与原文引用；无效结果不冒充成功翻译。

用户提供译文时，把`translations.en`保存在对应产品，含name/category/description/specifications、`approved:true`及`source_fingerprint`。无术语时指纹绑定规范化源文的name/category/description/specifications，有terms时还绑定术语；JSON序列化及键顺序须与服务端完全一致，优先保留当前服务端候选指纹，工作台勾选人工确认时由服务端处理。源文修改后须重新核对。规范化结果以服务端为准。

## 人工确认并冻结

`catalog.review` 输入`library_id`、`expected_version`、`language`。返回`project_id`、`version:1`、`fingerprint`、SKU数、data_units和expires_at。语言为zh-Hans时使用源文；英文必须有未失效的批准译文。确认冻结独立的素材及内容快照，保留30天，不因生成或下载续期。

## 生成目录

`catalog.generate` 输入确认返回的`project_id`、`version`、`fingerprint`。仅接受原样返回的确认指纹。异步产物包含实际PDF、逐页PNG和manifest，记录SKU/价格/规格/素材checksum/版面区域。检查真实字体、图片、DOM溢出、PDF物理页数及关键文本。超长内容明确失败；请缩短文本或切换详页模板后重新确认。不得把完成排版当作已人工核验。

## 比较改版

`catalog.compare` 输入`before_revision`和`after_revision`，均为确认返回的project_id。只比较同产品库、同语言；输出新增、移除、变更SKU。模板变化或缺少生成产物时不能逐页对应；可比产物列出受影响页码，变长/增删可能使后续页重排。

## 免费交付

`catalog.export` 输入成功生成任务的`source_task_id`，免费生成JSON/CSV及包含PDF、页图、清单的ZIP，CSV字段防公式注入。下载沿用30天期限。请交付SKU—页码定位、检查报告、用户复核提示和明确的未完成事项。

## 不依赖网页模板的最小流程

网页 Excel 模板是手工录入入口，不是 OpenClaw 的前置条件。Agent 可以读取用户原表并整理为 data；不具备读取能力时，走 `/inputs` 上传原 CSV/XLSX，读取返回的 sheets/columns，再明确列映射。PDF/扫描图的产品表没有通用自动导入接口，不能当作 XLSX 上传；先在宿主具备且获授权的读取工具中整理，并让用户核对事实。

### 建库、上传图片并记录对应关系

`POST /libraries`：

```json
{"title":"标准配件目录"}
```

读取 `data.library_id` 和 `data.version`。图片使用 multipart `POST /libraries/{library_id}/assets`，`file` 为单张 JPEG/PNG/WebP。保存每个真实文件名对应的 `data.asset_id`、checksum；图片上传本身不代表用户已确认归属。读取当前库 GET `/libraries/{library_id}`，以 `data.version` 为准。

```sh
: "${PRODUCT_CATALOG_API_KEY:=${AI_SKILLS_API_KEY:?请先配置平台密钥}}"
SITE="${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}"
curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer ${PRODUCT_CATALOG_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: $IMAGE_REQUEST_KEY" \
  -F "file=@$PRODUCT_IMAGE" "$SITE/api/v1/product-catalog/libraries/$LIBRARY_ID/assets"
```

### 整理数据并预检

`REPLACE_*` 是必须替换的真实回执字段，示例 version 也须改为当前整数版本。下面价格确认仅能在用户已核对金额、币种及单位后设置；价格未确认时用 `show_prices:false`、`confirmed:false`。

`POST /catalog.inspect`：

```json
{"library_id":"REPLACE_LIBRARY_ID","expected_version":1,"data":{"title":"标准配件目录","template":"cards","show_prices":true,"products":[{"sku":"001","name":"螺栓","category":"五金","description":"钢制配件","specifications":[{"label":"直径","value":"10 mm"}],"image_id":"REPLACE_ASSET_ID","price":{"amount":"12.30","currency":"USD","unit":"件","confirmed":true}}]}}
```

任务终态读取 `result.library_id`、`result.version`，并 GET 库取得完整 `data.data` 草稿。展示每个产品的主图、SKU、名称、规格、价格/币种/单位让用户核对；编号保留前导零，金额原样保留，不根据名称猜图片或把元转为采购接口的“整数分”。

### 使用原表列映射的替代入口

`POST /inputs` multipart 字段 file 返回 `data.file_id` 与 `data.sheets`。列 ID 是 c1/c2 等，不是 Excel 字母。表内 image_id 列必须放真实的已上传 asset_id；原表只有图片文件名时，应先整理“文件名—asset_id”映射为 data，或在本机生成用户核对过的导入表，不能把文件名冒充素材 ID。

```json
{"library_id":"REPLACE_LIBRARY_ID","expected_version":1,"file_id":"REPLACE_FILE_ID","sheet_index":0,"column_mapping":{"sku":"c1","name":"c2","image_id":"c3","amount":"c4","currency":"c5","unit":"c6"},"data":{"title":"标准配件目录","template":"cards","show_prices":false}}
```

该替代请求同样发到 `/catalog.inspect`。映射导入的价格默认未确认；通过 GET 库拿到完整草稿，在用户核对后对完整 data 执行 PATCH `/libraries/{library_id}` 或再次 inspect，不能遗漏其它产品。输入表、确认和生成分别保存幂等键，不反复上传或新建库来绕过冲突。

### 中文与英文两条路径

中文：用户确认图文事实后直接 `/catalog.review` 冻结中文，不必调用翻译。

英文：用户明确授权模型传输、当前单价及预留上限后提交 `/catalog.translate`：

```json
{"library_id":"REPLACE_LIBRARY_ID","expected_version":2,"language":"en"}
```

翻译成功后 GET 库读取新 `data.version` 与完整候选，逐产品展示英文名称、分类、说明及全部规格标签。只有用户对当前源文/译文明确批准后，才在完整草稿相应 `translations.en.approved` 设 true 并保存新版本。保留服务端返回的当前 `source_fingerprint`，不可用旧源文或不完整字段重算；库含 terms 时指纹还绑定 terms。用户自备译文也必须与当前源文绑定；不能拿宿主自行翻译结果冒充平台模型调用。无法安全计算完整指纹时转工作台批准。

`POST /catalog.review`：

```json
{"library_id":"REPLACE_LIBRARY_ID","expected_version":3,"language":"zh-Hans"}
```

英文改 language 为 en，且版本必须是保存批准译文后的新版本。读取 `result.project_id`、冻结目录 `result.version` 和 `result.fingerprint`；它们与库版本不是同一个概念。

`POST /catalog.generate`：

```json
{"project_id":"REPLACE_CONFIRMED_PROJECT_ID","version":1,"fingerprint":"REPLACE_CONFIRMED_FINGERPRINT"}
```

费用授权应对应本次语言、产品数、每100 SKU向上取整单元和当前单价。完成后 `/catalog.export`：

```json
{"source_task_id":"REPLACE_SUCCESSFUL_GENERATE_TASK_ID"}
```

改价或换图后先保存新库版本、重新确认并生成，不覆盖旧交付。比较改版时 `/catalog.compare` 的 before_revision/after_revision 是两次确认得到的 project_id，不是库version或task_id。

### 不能略过的失败边界

遇到图文归属不明确、产品缺字段、未经批准译文、版本冲突、字体/图片/质量失败，停在该步骤向用户说明。结果包含 `_truncated` 或 `_meta.truncated` 时，不拿摘要代替全部产品；GET 库取完整草稿，或使用工作台核对。不得删SKU、截断文字或降低质量来冒充成功。
