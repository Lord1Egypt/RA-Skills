# 场景：invoice-issue-issue（发票开具接口）

## 模板用途

用于描述 POST /invoice-issue/issue 接口的参数校验、字段标准化、请求结构，以及提交后通过 /invoice-issue/issue-status 查询最终结果的处理规则。

## 参数规格

说明：

- 本节“参数规格”用于快速说明接口的必填性、总体结构与关键约束；涉及“用户输入 -> input JSON”的具体字段转换、键名选择、嵌套层级判断时，应以本文件后文“请求参数说明”中的完整字段表为主，若两处信息粒度不同，以“请求参数说明”为准。
- 本接口根参数 `info` 为数组，支持一次提交多张发票；数组内每个元素都必须独立满足相同校验规则。
- 除 `fplsh` 外，接口必填业务字段缺失时必须一次性向用户追问，不得使用示例值替代。
- `fplsh` 虽为接口必填，但属于系统生成字段；若用户未提供，可在执行时自动生成 UUID 作为唯一流水号。
- 接口非必填字段在 input JSON 阶段仅在“用户未提供、且文件/图片中也未无歧义识别出该字段”时允许保持缺失；若用户已明确提供，或文件/图片中已稳定识别出该字段并可无歧义落位，即使该字段为可选，也必须写入 input JSON，避免遗漏。典型示例包括但不限于：`purchaserInfo.uscc`、`purchaserInfo.address`、`purchaserInfo.phone`、`purchaserInfo.bank`、`purchaserInfo.bankAccount`、`noteInfo.note`、明细级 `tax`、`discountInfo.discount`、`discountInfo.discountAmount`。除存在歧义、冲突或特定场景前置约束外，Agent 不需要因可选字段未提供而反复向用户确认，应优先以后续 check 结果为准。
- 对非关键字段，若场景文档没有额外指定特殊原始输入结构，Agent 在“用户输入 -> input JSON”阶段必须严格参照本文件的字段名、嵌套层级与语义做映射；允许缺失，但不得额外生成本接口未定义、脚本未声明支持的 key 或包装层。
- 对原始 input JSON 阶段的明细 `taxRate`，只有在用户明确说明税率语义时才允许写入；若用户没有说明税率，则不得自行识别、推断或补写 `taxRate`，必须保持缺失。检查脚本会在商品编码补全完成后，优先按纳税人类型与商品字典自动匹配参考税率，并取最低税率回填到最终 payload。仅当自动匹配失败时，才要求用户直接提供税率，或补充纳税人类型后重新匹配。
- 当用户未明确指定发票类型时，Agent 不得在 input JSON 阶段仅因票种缺失而中止追问；检查脚本会基于销售方税号查询企业画像，若销方为小规模纳税人，则默认补为“普通发票”。若用户已明确指定“普票/专票”等票种，则必须以用户指定为准，不得被企业画像默认值覆盖。

| 参数名                                  | 类型          | 必填 | 说明                                       | 默认值          | 来源                  |
| --------------------------------------- | ------------- | ---- | ------------------------------------------ | --------------- | --------------------- |
| uscc                                    | string        | Y    | 销售方税号                                 | 无              | 用户输入              |
| areaCode                                | integer       | Y    | 地区编码                                   | 无              | 编码转换              |
| personalAccount                         | string        | Y    | 居民身份证/手机号/用户名                   | 无              | 用户输入              |
| info[]                                  | array<object> | Y    | 发票开具明细数组，至少 1 条                | 无              | 用户输入              |
| info[].basicInfo.invoiceType            | string        | Y    | 发票类型，可选值：普通发票、增值税专用发票 | 小规模销方默认普通发票 | 用户输入/脚本查询默认 |
| info[].sellerInfo.address               | string        | Y    | 销方地址                                   | 无              | 用户输入              |
| info[].sellerInfo.phone                 | string        | Y    | 销方电话                                   | 无              | 用户输入              |
| info[].sellerInfo.bank                  | string        | Y    | 销方开户银行                               | 无              | 用户输入              |
| info[].sellerInfo.bankAccount           | string        | Y    | 销方银行账号                               | 无              | 用户输入              |
| info[].purchaserInfo.name               | string        | Y    | 购方名称                                   | 无              | 用户输入              |
| info[].invoiceDetail.data[]             | array<object> | Y    | 发票项目明细，至少 1 条                    | 无              | 用户输入              |
| info[].invoiceDetail.data[].projectName | string        | Y    | 项目名称                                   | 无              | 用户输入              |
| info[].invoiceDetail.data[].spbm        | string        | Y    | 商品编码                                   | 无              | 用户输入/前置流程     |
| info[].invoiceDetail.data[].amount      | number        | Y    | 项目金额                                   | 无              | 用户输入              |
| info[].invoiceDetail.data[].taxRate     | string        | Y    | 税率/征收率，如 0.13                       | 无              | 用户输入/脚本自动匹配 |
| info[].invoiceDetail.data[].tax         | number        | Y    | 项目税额                                   | 无              | 用户输入              |
| info[].invoiceDetail.amount             | number        | Y    | 合计金额                                   | 无              | 用户输入              |
| info[].invoiceDetail.tax                | number        | Y    | 合计税额                                   | 无              | 用户输入              |
| info[].invoiceDetail.total              | number        | Y    | 合计价税合计                               | 无              | 用户输入              |
| info[].fplsh                            | string        | Y    | 发票流水号，需保证唯一                     | 执行时生成 UUID | 系统生成/用户输入     |
| info[].isIncludeTax                     | boolean       | N    | 金额是否含税，目前固定为 true              | true            | 固定策略              |
| info[].sellerInfo.showBankInfo          | boolean       | N    | 是否展示销方银行信息                       | false           | 默认策略              |
| info[].sellerInfo.showPersonInfo        | boolean       | N    | 是否展示销方地址信息                       | false           | 默认策略              |
| info[].purchaserInfo.isNaturePerson     | boolean       | N    | 是否开票给自然人                           | false           | 默认策略              |
| info[].invoiceDetail.data[].slqdbz      | string        | N    | 数量清单标志                               | Y               | 固定策略              |

## 编码映射

本场景涉及的编码映射规则优先参考 [SKILL.md](../../SKILL.md) 中的参数编码转换步骤；以下为补充规则。

| 参数名                                      | 类型    | 说明               | 映射规则                                                                                                                                                   | 是否需回显确认 |
| ------------------------------------------- | ------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| areaCode                                    | integer | 地区编码           | 自然语言中的省份/城市名称映射为 areaCode                                                                                                                   | 是             |
| info[].basicInfo.invoiceType                | string  | 发票类型           | “普票/普通票”统一转为“普通发票”；“专票/增值税专票”统一转为“增值税专用发票”                                                                                 | 是             |
| info[].basicInfo.giveUpReason               | string  | 放弃减税优惠原因   | 用户提供原因描述时，按场景文案标准化为 `1` 或 `2`；无法明确归类时必须追问                                                                                  | 是             |
| info[].purchaserInfo.identificationTypeCode | string  | 自然人购方证件类型 | 仅接受接口已支持的证件类型编码；若用户只给中文证件名称，需先转换后回显                                                                                     | 是             |
| info[].purchaserInfo.nationCode             | string  | 自然人国籍或地区   | 根据 `common_dict` 的“国籍或地区”分类把名称转换为编码；失败时给出示例                                                                                      | 是             |
| info[].personInfo.certificateType           | string  | 经办人证件类型     | 根据 `common_dict` 的“证件类型”分类把名称转换为编码；失败时给出示例                                                                                        | 是             |
| info[].personInfo.nation                    | string  | 经办人国籍或地区   | 根据 `common_dict` 的“国籍或地区”分类把名称转换为编码；失败时给出示例                                                                                      | 是             |
| info[].paymentInfo[].payChannelCode         | string  | 支付渠道           | 根据 `common_dict` 的“支付渠道”分类把名称转换为编码；失败时给出示例                                                                                        | 是             |
| info[].invoiceDetail.data[].mtzlDm          | string  | 煤炭种类           | 煤炭类商品必填；必须在用户输入转 input JSON 阶段完成识别。可直接接收代码，或按煤炭种类字典把标准名称转换为编码；若描述不清晰，不得自动匹配候选值后通过校验 | 是             |

## 模糊参数处理

| 用户输入                               | 处理逻辑                                                                        | 是否需确认 |
| -------------------------------------- | ------------------------------------------------------------------------------- | ---------- |
| “深圳开票”“广东开票”等地名             | 按 `references/common/code-mappings.md` 转成 `areaCode`，并回显转换结果         | 告知后执行 |
| “普票”“专票”                           | 规范化为接口枚举值“普通发票”或“增值税专用发票”                                  | 告知后执行 |
| “开给个人/自然人”                      | 自动将 `purchaserInfo.isNaturePerson` 置为 `true`，并补充提示自然人相关字段规则 | 告知后执行 |
| 购方是自然人但证件类型或证件号码不完整 | 要求用户补齐 `identificationTypeCode` 或证件信息                                | 必须确认   |
| 明细金额、税额、合计之间不一致         | 停止调用，要求用户确认金额汇总关系后再继续                                      | 必须确认   |
| 煤炭相关明细但煤炭种类描述模糊         | 在生成 input JSON 前中止并追问 `mtzlDm`；不得根据模糊关键词自动选择煤炭种类编码 | 必须确认   |
| 煤炭相关明细缺少单位或单位不合法       | 在生成 input JSON 前中止并追问 `unit`；单位仅支持 `吨`、`千克（公斤）`          | 必须确认   |

## API 请求格式

说明：

- 示例参数已脱敏。
- 本接口仅使用 Body 参数，无 Path、Query 参数。

```http
POST /invoice-issue/issue
Content-Type: application/json

{
    "uscc": "91******************",
    "areaCode": 11,
    "personalAccount": "1**********",
    "info": [
        {
            "basicInfo": {
                "invoiceType": "普通发票",
                "giveUpReason": ""
            },
            "sellerInfo": {
                "address": "**省**市**区**路**号",
                "phone": "1**********",
                "bank": "**银行**支行",
                "bankAccount": "62****************",
                "showBankInfo": false,
                "showPersonInfo": false
            },
            "purchaserInfo": {
                "isNaturePerson": false,
                "name": "**科技有限公司",
                "uscc": "91******************",
                "address": "**省**市**区**路**号",
                "phone": "1**********",
                "showBankInfo": true,
                "bank": "**银行**支行",
                "bankAccount": "62****************",
                "showPersonInfo": true
            },
            "isIncludeTax": true,
            "invoiceDetail": {
                "data": [
                    {
                        "spbm": "101****************",
                        "size": "型号A",
                        "unit": "件",
                        "price": 88.50,
                        "taxInclusivePrice": 100,
                        "quantity": "10",
                        "amount": 885,
                        "taxInclusiveAmount": 1000,
                        "taxRate": "0.13",
                        "tax": 115,
                        "projectName": "**服务费",
                        "xsyhzcbz": "Y",
                        "zzstsgl": "增值税特殊管理说明",
                        "slqdbz": "Y",
                        "sptm": "690**********"
                    }
                ],
                "amount": 1000,
                "tax": 130,
                "total": 1130
            },
            "noteInfo": {
                "note": "测试备注",
                "payee": "张*",
                "reviewer": "李*"
            },
            "paymentInfo": [
                {
                    "payChannelCode": "002",
                    "transactionOrderNo": "TXN********"
                }
            ],
            "fplsh": "0f4d8b70-****-****-****-************"
        }
    ]
}
```

### 请求参数说明

说明：本节是“用户输入 -> input JSON”做字段转换时的主参照表；对非关键字段，若无额外场景规则，应优先按本节字段名、嵌套层级与语义选择对应落位。

| 位置 | 字段                                                    | 类型          | 必填 | 说明                                                                                            |
| ---- | ------------------------------------------------------- | ------------- | ---- | ----------------------------------------------------------------------------------------------- |
| Body | uscc                                                    | string        | Y    | 销售方税号                                                                                      |
| Body | areaCode                                                | integer       | Y    | 地区编码                                                                                        |
| Body | personalAccount                                         | string        | Y    | 居民身份证/手机号/用户名                                                                        |
| Body | info                                                    | array<object> | Y    | 发票开具对象数组，至少 1 条                                                                     |
| Body | info[].basicInfo.invoiceType                            | string        | Y    | 发票类型，仅支持“普通发票”“增值税专用发票”；若用户未指定且销售方为小规模纳税人，检查脚本默认补为“普通发票” |
| Body | info[].basicInfo.giveUpReason                           | string        | N    | 放弃减税优惠原因编码，支持 `1`、`2`                                                             |
| Body | info[].sellerInfo.address                               | string        | Y    | 销方地址                                                                                        |
| Body | info[].sellerInfo.phone                                 | string        | Y    | 销方电话                                                                                        |
| Body | info[].sellerInfo.bank                                  | string        | Y    | 销方开户银行                                                                                    |
| Body | info[].sellerInfo.bankAccount                           | string        | Y    | 销方银行账号                                                                                    |
| Body | info[].sellerInfo.showBankInfo                          | boolean       | N    | 是否展示销方银行信息，默认 `false`                                                              |
| Body | info[].sellerInfo.showPersonInfo                        | boolean       | N    | 是否展示销方地址信息，默认 `false`                                                              |
| Body | info[].purchaserInfo.isNaturePerson                     | boolean       | N    | 是否开票给自然人，默认 `false`                                                                  |
| Body | info[].purchaserInfo.name                               | string        | Y    | 购方名称                                                                                        |
| Body | info[].purchaserInfo.uscc                               | string        | N    | 购方税号；开具增值税专用发票时必填                                                              |
| Body | info[].purchaserInfo.address                            | string        | N    | 购方地址                                                                                        |
| Body | info[].purchaserInfo.phone                              | string        | N    | 购方电话                                                                                        |
| Body | info[].purchaserInfo.showBankInfo                       | boolean       | N    | 是否展示购方银行信息，默认 `false`                                                              |
| Body | info[].purchaserInfo.bank                               | string        | N    | 购方开户银行                                                                                    |
| Body | info[].purchaserInfo.bankAccount                        | string        | N    | 购方银行账号                                                                                    |
| Body | info[].purchaserInfo.showPersonInfo                     | boolean       | N    | 是否展示购方地址信息，默认 `false`                                                              |
| Body | info[].purchaserInfo.identificationTypeCode             | string        | N    | 自然人购方证件类型编码                                                                          |
| Body | info[].purchaserInfo.identificationNumber               | string        | N    | 自然人购方证件号码                                                                              |
| Body | info[].purchaserInfo.nationCode                         | string        | N    | 国籍或地区编码                                                                                  |
| Body | info[].isIncludeTax                                     | boolean       | N    | 是否含税，当前固定为 `true`                                                                     |
| Body | info[].invoiceDetail.data[].spbm                        | string        | Y    | 商品编码                                                                                        |
| Body | info[].invoiceDetail.data[].size                        | string        | N    | 规格型号                                                                                        |
| Body | info[].invoiceDetail.data[].unit                        | string        | N    | 单位；煤炭相关项目时必填，且仅支持 `吨`、`千克（公斤）`                                         |
| Body | info[].invoiceDetail.data[].price                       | number        | N    | 不含税单价                                                                                      |
| Body | info[].invoiceDetail.data[].quantity                    | string        | N    | 数量                                                                                            |
| Body | info[].invoiceDetail.data[].amount                      | number        | Y    | 项目金额                                                                                        |
| Body | info[].invoiceDetail.data[].taxRate                     | string        | Y    | 税率或征收率；最终 payload 必填，但原始 input JSON 阶段允许缺失，由检查脚本自动匹配最低参考税率 |
| Body | info[].invoiceDetail.data[].tax                         | number        | Y    | 税额                                                                                            |
| Body | info[].invoiceDetail.data[].discountInfo                | object        | N    | 折扣信息                                                                                        |
| Body | info[].invoiceDetail.data[].discountInfo.discount       | number        | N    | input JSON 中已归一化的百分比数值；例如 `0.5 -> 50`、`50% -> 50`、`88折 -> 88`、`12.5% -> 12.5` |
| Body | info[].invoiceDetail.data[].discountInfo.discountMode   | integer       | N    | Skill 标准化后固定传 `1`，按金额折扣                                                            |
| Body | info[].invoiceDetail.data[].discountInfo.discountAmount | number        | N    | 标准化后的不含税折扣金额，固定为正数                                                            |
| Body | info[].invoiceDetail.data[].discountInfo.discountTax    | number        | N    | 折扣税额                                                                                        |
| Body | info[].invoiceDetail.data[].projectName                 | string        | Y    | 项目名称                                                                                        |
| Body | info[].invoiceDetail.data[].xsyhzcbz                    | string        | N    | 享受优惠政策标志                                                                                |
| Body | info[].invoiceDetail.data[].zzstsgl                     | string        | N    | 增值税特殊管理说明                                                                              |
| Body | info[].invoiceDetail.data[].slqdbz                      | string        | N    | 默认传 `Y`                                                                                      |
| Body | info[].invoiceDetail.data[].mtzlDm                      | string        | N    | 煤炭种类代码，煤炭相关项目时必填                                                                |
| Body | info[].invoiceDetail.data[].sptm                        | string        | N    | 商品条码，13 位                                                                                 |
| Body | info[].invoiceDetail.amount                             | number        | Y    | 合计金额                                                                                        |
| Body | info[].invoiceDetail.tax                                | number        | Y    | 合计税额                                                                                        |
| Body | info[].invoiceDetail.total                              | number        | Y    | 合计价税合计                                                                                    |
| Body | info[].noteInfo.note                                    | string        | N    | 备注                                                                                            |
| Body | info[].noteInfo.payee                                   | string        | N    | 收款人                                                                                          |
| Body | info[].noteInfo.reviewer                                | string        | N    | 复核人                                                                                          |
| Body | info[].personInfo.name                                  | string        | N    | 经办人姓名                                                                                      |
| Body | info[].personInfo.nation                                | string        | N    | 经办人国籍或地区编码                                                                            |
| Body | info[].personInfo.certificateType                       | string        | N    | 经办人证件类型编码                                                                              |
| Body | info[].personInfo.certificateCode                       | string        | N    | 经办人证件号码                                                                                  |
| Body | info[].personInfo.uscc                                  | string        | N    | 自然人纳税人识别号                                                                              |
| Body | info[].paymentInfo                                      | array<object> | N    | 支付信息数组                                                                                    |
| Body | info[].paymentInfo[].payChannelCode                     | string        | N    | 支付渠道代码                                                                                    |
| Body | info[].paymentInfo[].transactionOrderNo                 | string        | N    | 交易单号                                                                                        |
| Body | info[].fplsh                                            | string        | Y    | 发票流水号，需唯一                                                                              |

补充说明：

1. Skill 侧若识别到用户输入“单价”，默认应视为含税单价。
2. 单票检查脚本会先据此补出 `taxInclusivePrice` 与 `taxInclusiveAmount`，再反算内部 `price`（不含税单价）、`amount`（不含税金额）与 `tax`。
3. 预览阶段展示的“单价（含税）”“金额（含税）”应取含税值，不应直接展示内部 `price` 与 `amount` 的业务语义。
4. 用户输入的“金额”与“单价”在开票语义下默认按含税口径处理；若用户未明确要求按不含税口径，不得自动改判为不含税金额/单价。
5. 对普通零税率，用户输入写成 `0` 或 `0%` 均可，脚本应统一标准化为 `0%`。
6. 涉及煤炭类明细时，`mtzlDm` 必须在用户输入转 input JSON 阶段完成识别并写入；可直接使用用户提供的代码，或依据二进制内置的 `mtzl` 煤炭种类字典执行标准名称到编码的转换。当前允许的标准映射为：`政府保供煤 -> 0100`、`市场煤 -> 0300`、`长协煤-协议期不足半年 -> 0201`、`长协煤-协议期在半年至一年之间 -> 0202`、`长协煤-协议期在一年至两年之间 -> 0203`、`长协煤-协议期在两年以上 -> 0204`。同时，`unit` 必须同步写入，且仅允许 `吨`、`千克（公斤）`。若用户仅给出“长协煤”“普通煤”“常见煤种”等无法唯一映射的描述，或未提供合法单位，必须先追问澄清后再继续，禁止自动选择最相近编码。
7. 对单张与批量开票，除用户输入中可明确识别的字段外，Agent 不得自行推理并补写其他开票字段；所有缺失字段必须通过前置检查脚本自动补全并执行完整性校验。
8. 若用户未提供发票类型，Agent 应保留 `invoiceType` 缺失并进入检查脚本；检查脚本查询销方企业画像后，只有在销方为小规模纳税人时才自动补“普通发票”，其他情况仍按缺失项返回并由 Agent 一次性追问。
9. 若单条明细指定折扣比例或折扣金额，Agent 在 input JSON 阶段必须先把折扣比例归一化为百分比数值，再由检查脚本校验 `discountInfo.discount >= 0 且 < 100` 并换算写回 `discountInfo.discountMode=1`；其中 `discountInfo.discountAmount` 表示不含税折扣金额，`discountInfo.discountTax` 表示折扣税额，二者传给正式开票接口时必须为正数。
10. 预览阶段不得直接把正式开票 payload 中的正数折扣字段当作票面行渲染；必须派生出带“折扣”标识的展示行，其中金额、税额显示为负数。
11. 若某个非关键字段在原始 input JSON 中没有明确的受支持键名或受支持层级，默认不得写入任何替代 key；应保持缺失并交由 check 阶段补全、报错或追问，而不是输出诸如 `buyerName`、`taxAmount`、`invoiceDetails`、`previewData`、`extra`、`metadata` 这类脚本无法识别的字段。

## 响应结果示例

说明：`/invoice-issue/issue` 主要表示“提交是否成功受理”；最终开票结果应以后续 `/invoice-issue/issue-status` 轮询结果为准。

```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "status": 1,
    "msg": "开票成功",
    "fplsh": "0f4d8b70-****-****-****-************",
    "summary": "普通发票开具成功，价税合计 1130 元",
    "pdfUrl": "https://***.***.com/invoice/********.pdf"
  },
  "traceId": "019cfef4-bdfc-77fe-9031-375b22820d79"
}
```

## 响应参数说明

| API 字段     | 展示名称   | 格式处理           | 说明                                    |
| ------------ | ---------- | ------------------ | --------------------------------------- |
| code         | 状态码     | 原样输出           | 0 表示成功，非 0 表示失败               |
| message      | 响应消息   | 原样输出           | 接口返回提示                            |
| data.status  | 开票状态   | 枚举翻译           | `1` 成功，`0/2` 处理中，`-1` 失败       |
| data.msg     | 业务说明   | 原样输出           | 开票结果补充说明                        |
| data.fplsh   | 发票流水号 | 原样输出           | 对应本次开票请求的唯一标识              |
| data.summary | 结果摘要   | 原样输出           | 成功时展示给用户的开票摘要              |
| data.pdfUrl  | PDF附件    | 链接或文件标识展示 | 开票成功后返回的 PDF 附件地址或文件标识 |
| traceId      | 追踪 ID    | 原样输出           | 异常排查使用                            |

## 结果展示规则

### 预览阶段

- 当开票参数校验通过并生成 HTML 票样时，必须同步生成 Markdown 版预览内容。
- Markdown 版预览只由开票信息检查命令在 `validation_passed=true` 时写入任务状态 JSON；`issue-invoice-preview-generator` 仅用于独立生成 HTML 票样，不会生成 Markdown，也不会回写任务状态 JSON。
- 预览 Markdown 必须写入任务状态 JSON 的 `check_result.invoice_preview_markdown`，并由 Skill 在任务执行过程中直接展示给用户。
- 预览 Markdown 顶部必须展示加粗标题“发票预览”以及预览发票票样链接；列表项应使用标准 Markdown 无序列表格式，即 `- ` 后跟文本内容。
- 预览 Markdown 必须按 `fplsh` 依次展示每张发票的“【发票基础信息】”与“【商品明细】”；其中“发票流水号”应优先以加粗形式单独一行展示，下一行单独写“【发票基础信息】”，后续基础信息继续使用无序列表。
- 发票基础信息至少包含：销售方名称、购买方名称、购买方税号、发票种类、价税合计、备注。
- 商品明细至少包含：明细序号、商品简称+项目名称、税收分类编码、规格型号、单位、数量、单价（含税）、税率、税额、金额（含税）。
- 其中税额、金额（含税）以及价税合计必须保留两位小数，并使用千位分隔符；无值字段保留为空字符串，不得填充臆造值。
- 若明细存在折扣信息，Markdown 预览中必须追加折扣展示内容：商品名称前加折扣标识，折扣金额与折扣税额显示为负数。
- 预览阶段税额展示规则：单条“免税”明细税额显示为 `***`；单条“不征税”明细税额显示为空字符串；单条 `0%` 明细税额按普通零税额显示。合计税额遵循以下规则：仅存在同类型特殊明细时，按该类型单条规则展示；若仅存在“免税”与普通有税额明细混合，则合计税额只汇总其它有税额明细；若仅存在“不征税”与普通有税额明细混合，则合计税额只汇总其它有税额明细；若“免税”“不征税”“0税率”中同时出现任意两种及以上不同类型明细，则合计税额显示为空字符串。
- 预览 Markdown 各区块与列表项之间应保留空行，保持与票面预览说明一致的阅读节奏。
- HTML 预览中，若明细存在折扣信息，必须在原明细下方追加一行同项目名折扣行；该行金额、税额显示为负数，仅用于预览展示，不得回写到正式开票 payload 的 `invoiceDetail.data[]`。

1. 调用 `/invoice-issue/issue` 后，必须继续调用 `/invoice-issue/issue-status` 查询最终申报结果；首次查询从开票后 2 秒开始，最多 10 次，后续按指数退避。
   - `/invoice-issue/issue-status` 请求体必须为：`{"taskID": <开票接口返回的 taskID>, "uscc": "销售方税号", "isAuth": true}`。
   - `taskID` 必须来自 `/invoice-issue/issue` 的响应 `data.taskID`；不得再使用 `fplsh` 作为状态查询参数。
2. 只有 `/invoice-issue/issue-status` 返回 `code=0`、`data.status=1` 且 `data.list` 长度为 1 时，才可判定为单张开票成功。
3. 若 `/invoice-issue/issue-status` 返回 `data.status != -1`，即使当前 `data.list[0].result=false` 或存在失败原因文案，也应继续按轮询策略重试，不能立刻判定最终失败。
4. 只有 `/invoice-issue/issue-status` 明确返回 `data.status=-1` 时，才可判定为终态失败；此时必须生成 Markdown，标题使用加粗样式，如 `**开具失败：**`，并以编号项展示失败原因。
5. 单张开票成功时，必须先遍历 `data.list`，读取每个 `item.file` 中的 `pdf/xml/ofd` 链接并下载到本地目录 `根目录/workspace/invoice/issue/{数电票号码}`，再生成 Markdown；Markdown 至少展示以下内容：发票号码、购买方、含税金额、开票时间、发票原件路径、PDF 下载链接；标题使用加粗样式，如 `**开具成功：**`，编号项后保留空格，子项使用缩进无序列表。
6. 当 `data.list` 长度大于 1 时，必须按批量格式生成 Markdown：
   - 标题使用加粗样式“**全部或部分开具成功：**”或“**全部开具失败：**”
   - 关键信息至少包含总数、成功数、失败数、合计开票金额、合计税额
   - 成功项需列出发票原件路径和 PDF 下载链接，子项使用缩进无序列表；“点击查看/点击下载”应优先链接到下载后的本地文件路径，而不是远程 OSS 地址
   - 有失败项时，必须追加“异常说明”并列出任务号及失败原因
7. 若轮询达到最大次数仍未得到明确成功或失败状态，应明确告知“仍在处理中”，不得误报成功。
8. 开票结果 Markdown 必须写入任务状态 JSON 的 `issue_result.issue_result_markdown`，并同步落地到 `issue_result.issue_result_markdown_path` 指向的本地 Markdown 文件；Skill 在任务执行过程中必须优先读取该本地 Markdown 文件并原样展示给用户。
9. 开票结果 Markdown 的展示要求与预览 Markdown 相同：不得摘要、不得改写、不得截断；若展示后发现任一标题、编号项、列表项、链接或段落缺失、截断、漏行，必须重新完整输出。
10. 当前脚本已支持 `list` 长度为 1 的单票 Markdown 和 `list` 长度大于 1 的批量 Markdown。

## 开票结果原件落地规则

- 当 `/invoice-issue/issue-status` 返回 `data.list` 后，执行层必须遍历 `data.list`。
- 每个 `item.file` 视为一个对象，当前至少支持处理 `pdf`、`xml`、`ofd` 三个键。
- 若某个键对应的值为非空 HTTP/HTTPS 链接，则必须下载到本地目录：`根目录/workspace/invoice/issue/{数电票号码}`。
- `{数电票号码}` 优先取 `item.data.sdphm`，其次取 `item.sdphm`；若仍缺失，才可降级使用其他可唯一标识字段。
- 生成开票结果 Markdown 时，“发票原件路径”中的 `点击查看` 链接目标必须替换为下载后的本地文件路径；PDF 下载链接也应优先指向本地 PDF 文件。

## issue-status 请求体约定

```json
{
  "taskID": 341442,
  "uscc": "91440300MAD66AAP45",
  "isAuth": true
}
```

说明：

- `taskID`：取自 `/invoice-issue/issue` 响应中的 `data.taskID`
- `uscc`：取自正式开票请求体顶层 `uscc`
- `isAuth`：固定传 `true`

## 错误码与处理建议（可选）

| 错误码 | 典型含义                   | Skill 侧处理                             |
| ------ | -------------------------- | ---------------------------------------- |
| 400    | 参数缺失或格式错误         | 一次性提示缺失字段或格式问题，并给出示例 |
| 409    | `fplsh` 重复或请求幂等冲突 | 重新生成唯一流水号后再发起请求           |
| 422    | 明细金额、税额、合计不一致 | 要求用户确认金额汇总后重新提交           |
| 500    | 服务端异常                 | 提示稍后重试，并回显 `traceId` 以便排查  |

## 维护检查项

- 场景 ID 已改为小写中划线风格。
- areaCode 与发票类型标准化规则已在文档中说明。
- 示例请求与示例响应均已脱敏。
- 开票结果展示规则已补齐。
