---
name: MarketUP管理
description: Marketup CRM - detail/list search, advanced filtering, create, modify, assignment flows, history/behavior lookup, lead-to-account conversion, tags, and pool configuration workflows.
metadata:
  {"openclaw":{"requires":{"bins":["curl","jq"]},"primaryEnv":"MARKETUP_API_KEY"}}
---

## 全局约束（最高优先级）

- 在执行任何 Marketup API 调用前，先检查 `MARKETUP_API_KEY` 是否已存在于当前环境。
- 若未设置 `MARKETUP_API_KEY`，先执行 `references/setup-marketup-api-key.md` 中定义的脚本流程，由脚本提示用户输入并写入全局 `~/.openclaw/.env`。
- `MARKETUP_API_KEY` 缺失时，必须由 agent **直接执行**脚本流程；不要把脚本命令发给用户让用户手动执行。
- 脚本执行后再次检查 `MARKETUP_API_KEY`：存在则继续任务；仍不存在则**停止所有 Marketup API 调用**，仅告知用户需先完成 API Key 配置并提示可重试。
- **严禁**在未实际发起请求、未拿到接口响应前，向用户声称任何写操作已成功。
- 所有写操作（分配、创建、修改、跟进、转客户、领取、退回、打标签等）必须依据接口返回后再总结结果。

## 调用规范

- 主域名：`https://uc.marketup.cn`
- 凡用 `curl` 请求后端接口，必须带请求头：`Authorization: $MARKETUP_API_KEY`、`Referer: MarketUP-Skills`。
- `GET` 的查询参数：使用**扁平**参数名；**不要**在参数名前加 `leadsRPO.`、`companyUserRPO.`、`rpo.` 等前缀（与代码里的包装对象名无关）。
- `POST` 且 body 为 JSON 时：`Content-Type: application/json`，body 用 `-d @file.json` 或 `-d '{...}'`。
- 失败时仅输出 HTTP 状态码或响应 JSON 的 `message`（无 `message` 时用 `code`），不推测原因。

## 表单实体类型（查询字段定义）

`GET /api/uc-open/formField/queryCurrentFields` 使用查询参数 `marketEntityType`（**数字**）：线索 `0`、客户 `2`、联系人 `3`。其它实体类型见 OpenAPI。

---

## 1. 搜索线索

- 从用户话里取手机号或名称关键词；**优先手机号**。
- **线索总数**：用户问「有多少条线索」等时，用列表接口：`page=1`、`size=1`，不传搜索条件（或仅依赖后端默认），从响应中取总条数字段（如 `data.totalElements`）回答。
- **排序**：用户明确要求按某字段排序时，传 `sort`、`sortType`（与后端约定一致）；无需求不传。
- **展示**：线索名称、联系人、手机、负责人、状态、创建时间。

**接口**：`GET https://uc.marketup.cn/api/uc/v1/crm/leads/list`  
常用查询参数示例：`page`、`size`、`type`（`-1` 表示全部线索）、`searchValue`、`cellphone`、`leadsName`、`sort`、`sortType`、`multipleGroupAdvancedQueryFilter`（高级筛选 JSON 字符串）。

**快捷按名单/手机搜**：`GET https://uc.marketup.cn/api/uc/v1/crm/leads/searchLeadsByNameOrCellphone`，查询参数 `searchValue`。

---

## 2. 高级筛选搜索线索

当条件超出手机/名称（时间、来源、标签、行为等）时：

1. 根据用户描述构造**一条**符合后端要求的高级筛选 **JSON 字符串**（可与用户对齐字段含义）；意图类型可覆盖：线索属性、标签、来源、行为记录等。
2. 调用列表接口，将 JSON 字符串放在查询参数 **`multipleGroupAdvancedQueryFilter`**；不要同时用手机/名称参数替代该 JSON（除非用户还要叠加简单条件，按后端能力传）。
3. 需要排序时传 `sort`、`sortType`。
4. 结果展示同普通搜索。

---

## 3. 创建线索

流程：**取字段定义 → 收集并映射为 formFieldId → 调创建接口**。

**第一步** `GET /api/uc-open/formField/queryCurrentFields?marketEntityType=0`  
记录 `formFieldId`、`showName`、`required`、`dataType`、`options`。

**第二步** 构建 `leads`：key 必须是 **数字字符串形式的 formFieldId**（如 `"17263687"`），value 为用户填写值；**禁止**用中文名或 `cellphone` 等逻辑名做 key。  
必填缺失要列出字段名请用户补；枚举类值须在 options 范围内。

**第三步** `POST https://uc.marketup.cn/api/uc/v1/crm/leads/saveLeads`  
JSON body 使用 `LeadsSaveRPO` 形态，与工具一致的核心字段包括：`type`（单条保存为 `1`）、`leads`（对象）、`coverInfo`、`genCompanyAccount`、`assignType`、`autoAssign`、`notAssign`、`ownerCompanyUserId`、`sourceChannelId`、`remark`（可选，结构同跟进里的备注对象）等。  
分配语义（互斥，与工具一致）：

- 不分配：`notAssign: true`
- 按规则自动分配：`assignType: 1` 且 `autoAssign: true`
- 指定成员：`assignType: 2` 且 `ownerCompanyUserId` 为员工的 `companyUserId`（先搜员工或取当前用户）
- 用户未说明分配方式：可不传分配相关字段，由后端默认

创建成功后若有 `leadsId` 一并告知用户。

---

## 4. 修改线索字段

- 解析目标线索（ID；若只有手机/名称则先列表搜索，唯一则取 `leadsId`，多条请用户确认）。
- 再次 `GET .../queryCurrentFields?marketEntityType=0`，用 `showName` 匹配得到 **formFieldId**；禁止用字段名调修改接口。
- **每个字段单独一次请求**：`POST https://uc.marketup.cn/api/uc/v1/crm/leads/modify/profileData?leadsId=<id>`，body JSON：`{ "formFieldId": <number>, "value": "<string>" }`。
- 多字段依次请求，最后汇总成功/失败（失败原因仅来自接口响应，不臆测）。

---

## 5. 添加跟进记录

- 已知 `leadsId`：直接调接口；仅手机/名称则先搜索确认 `leadsId`。
- 无跟进内容请用户补充。

**接口**：`POST https://uc.marketup.cn/api/uc/v1/crm/leads/addOrUpdate/remark`  
Body（与 `LeadsRemarkSaveRPO` 一致）：`leadsId`、`remark`（必填）、`historyId`（可 null）、`attachments`（可 null）、`type_id`（跟进类型，可选）。

---

## 6. 查询线索详情

- 识别正整数 `leadsId`；有歧义时先问清再请求。

**接口**：`GET https://uc.marketup.cn/api/uc/v1/crm/leads/<leadsId>/detail`

成功时建议按下面结构展示（字段为空则省略该行）：

**线索详情 #\<leadsId\>**  
- **线索名称**、**联系人 / 手机 / 邮箱**、**地区**  
- **状态**、**阶段**、**负责人**、**SDR**、**创建人**  
- **来源**、**线索池**、**评分**  
- **创建时间**、**最近跟进**、**跟进记录数**、**未跟进天数**、**分配时间**、**转化时间**  
- **标签**（逗号分隔）、**关联企业**、**待办**（名称、状态、截止日期、负责人）

---

## 7. 分配 / 取消分配线索

- **分配**：用户给姓名/手机号但未给 `companyUserId` 时，先 `GET /api/uc-open/v1/company/user/team/list`（扁平查询：`page`、`size`、`searchValue`、`leadsManageType` 等），结果唯一则取 `companyUserId`，再分配；多条则请用户选择。
- **接口**：`POST https://uc.marketup.cn/api/uc/v1/crm/leads/assign`  
  - URL 查询参数：`leadsId`；若分配则加 `companyUserId`，取消分配则**不传** `companyUserId`。  
  - Body JSON（`LeadsAssignRPO`）：`reason`、`type`（无则 `null`）。

---

## 8. 查询跟进历史

- 需先确定 `leadsId`。

**接口**：`GET https://uc.marketup.cn/api/uc/v1/crm/historyRecord/remarkHistoryList`  
扁平查询参数（与 `HistoryPageRPO` 字段一致，**不要** `rpo.` 前缀）：如 `page`、`size`、`sort`、`sortType`、`startTime`、`endTime`、`historyTypeEnum=LEADS_HISTORY`、`id=<leadsId>` 等。

展示：每条一行 `createTime`、`operatorName`、`remark`（有附件可标「含附件」）；说明总条数，若本页小于总数可提示缩小时间范围或翻页。

---

## 9. 查询修改历史

- 需先确定 `leadsId`。

**接口**：`GET https://uc.marketup.cn/api/uc/v1/crm/historyRecord/entityChangeHistoryList`  
查询参数同上一节扁平形式，`historyTypeEnum=LEADS_HISTORY`，`id=<leadsId>`。

展示：每条一行 `createTime`、`operatorName`（**为 null 时显示「系统」**，禁止编造人名）、`operatorTypeLabel`、`propertyName`、`preValue` → `afterValue`；`preValue` 空显示「（空）」；有 `description` 可优先展示；`reason` 非空追加原因。

---

## 10. 查询行为轨迹

- 需先确定 `leadsId`。

**接口**：`GET https://uc.marketup.cn/api/uc/v1/crm/historyRecord/behaviorRecordList`  
查询参数同上扁平形式，`historyTypeEnum=LEADS_HISTORY`，`id=<leadsId>`。

展示：每条一行 `createTime`、`behaviorName`、`detailMessage` 或 `description`；有 `duration` 可标耗时；有 `visitorNickName` / 关联账户名可追加。

---

## 11. 线索转客户

用户表达「转客户」「转化」等时：

1. **确认 `leadsId`**（必要时先搜索）；`GET .../crm/leads/<id>/detail` 取线索上可映射的字段（名称、手机、邮箱等）。
2. **并行取表单字段**：`GET .../queryCurrentFields?marketEntityType=2`（客户）、`marketEntityType=3`（联系人）。
3. **`accountInfo`**：key 为客户表单的 **formFieldId 数字字符串**；值优先用户输入，否则用线索字段映射（客户名←线索名、联系人←线索联系人名、手机、邮箱等）。
4. **`contacts`**：默认用线索 `name`、`cellphone` 填入联系人表单中「姓名/手机」对应字段（先按 `showName` 匹配 formFieldId）；**仅当**线索姓名与手机均为空时才向用户要联系人；用户明确说没有联系人且线索也无联系人信息时可传空数组 `[]`。
5. **`companyUserId`**：用户未指定负责人则 `GET /api/uc-open/v1/user/currentUser` 取当前用户对应负责人 id；指定了员工则先搜员工列表取 `companyUserId`。
6. **接口**：`POST https://uc.marketup.cn/api/uc/v1/crm/leads/leadsConvertAccount`  
   Body JSON：`{ "leadsId", "accountInfo", "contacts", "companyUserId" }`（与 `LeadsAccountSaveRPO` 一致）。

成功后说明结果，有 `accountId` 则展示。

---

## 12. 给线索打标签 / 移除标签

- 需要 **`leadsId` + `tagId`**。无 `leadsId` 时先搜索确认。
- 若用户只给标签名称，说明需要 **`tagId`**，请用户提供或从标签管理渠道查询。

**添加**：`POST https://uc.marketup.cn/api/uc/v1/crm/leads/addTag`，查询参数 `leadsId`、`tagId`。  
**移除**：`POST https://uc.marketup.cn/api/uc/v1/crm/leads/deleteTag`，查询参数 `leadsId`、`tagId`。

---

## 13. 查询线索公海

用户提到「公海」「未领取」等。

**接口**：`GET https://uc.marketup.cn/api/uc/v1/crm/leads/list`  
查询参数与工具一致的核心组合：`type=5`、`leadPoolId=-1`、`convertedStatus=0`，以及 `page`、`size`、`searchValue`（可选）、`sort`、`sortType`（可选）。  
展示字段同普通搜索。

---

## 14. 领取公海线索

**接口**：`POST https://uc.marketup.cn/api/uc/v1/crm/leads/receive`，查询参数 `leadsId`。  
无 `leadsId` 时可先公海列表搜索，唯一则领取。

---

## 15. 退回线索到公海

**接口**：`POST https://uc.marketup.cn/api/uc/v1/crm/leads/discard`  
Body JSON（`DiscardLeadsRPO`）：`leadsId`、`returnLead: true`、`reason`（可选）、`giveUpReasonId`、`tagId`、`attachments` 等按工具传 null 即可。

---

## 16. 查询线索公海配置

用户问「公海规则」「领取限制」「回收」等。

**接口**：`GET https://uc.marketup.cn/api/uc/v1/leads/leadPool/-1`（默认池 `-1`，与工具一致）

展示建议（与 agent 一致）：

- **领取规则** `visibleRule`：`ALL_LEADS` / `RECYCLED_AND_REJECT_LEADS` / `RECYCLED_LEADS` / `NONE_LEADS` 对应文案：全部无负责人开放；仅收回与拒收；仅收回；均不开放。
- **领取限制** `receiveLimit`：true/false → 已开启/已关闭  
- **自动回收** `autoRecycle`  
- **生效时间**：`executeTime`、`leadMinCreateTime`  
- **回收规则**列表：`name`、天数小时、`state`（`NOT_FLOW_UP` / `NO_BUSINESS_CHANCE` / `NOT_UPDATE_FOLLOW_UP_RECORD` 等对应文案）  
- null 字段省略对应行。

---

## 17. 查询客户详情（crmAccountAgent）

- 从用户输入中识别 `accountId`（正整数），有歧义先确认再请求。

**接口**：`GET https://uc.marketup.cn/api/uc/v1/account/accountDetail/<accountId>`（可带 `abmType`）

展示建议（空值省略）：

- 客户名称、负责人、来源、客户类型
- 创建时间、最近更新时间
- 已收款 / 总金额 / 未开票金额
- 标签（tagName 列表）
- 联系人（name / cellPhone / email / title）
- 商机（chanceName / predictPrice / expireTime）
- 关联线索（leadsName）
- 待办事项（name / status / estimatedCompletionDate）

---

## 18. 查询客户列表（crmAccountAgent）

- 常规筛选：名称关键词、业务阶段、负责人、客户 ID、排序等。
- 若用户说「某人负责的客户」，先查员工列表拿 `companyUserId`，再筛客户。
- 结果建议展示：客户名称、负责人、手机、邮箱、标签、联系人、未跟进天数、创建时间（空值省略）。

**接口**：`GET https://uc.marketup.cn/api/uc-open/v1/account/list`

常用扁平查询参数（不要 `rpo.` 前缀）：

- `page`、`size`
- `searchValue`
- `stageId`
- `accountId`
- `companyUserId`
- `sort`、`sortType`
- `multipleGroupAdvancedQueryFilter`（高级筛选 JSON 字符串）

---

## 19. 高级筛选搜索客户（crmAccountAgent）

当用户条件超出名称范围（时间、标签、来源、动态属性等）时：

1. 根据用户意图构造高级筛选 JSON 字符串（账户场景）。
2. 调客户列表接口，把 JSON 放进 `multipleGroupAdvancedQueryFilter`。
3. 需要排序时再传 `sort` / `sortType`。
4. 结果展示同普通客户列表。

---

## 20. 创建客户（crmAccountAgent）

流程：**取字段定义（并行）→ 构建 accountInfo → 构建 contacts → 创建**。

1. 字段定义：
   - `GET /api/uc-open/formField/queryCurrentFields?marketEntityType=2`（ACCOUNT）
   - `GET /api/uc-open/formField/queryCurrentFields?marketEntityType=3`（CONTACT）
2. `accountInfo`：
   - key 必须是 ACCOUNT 字段的 `formFieldId` 数字字符串，value 为用户值。
   - 必填缺失需先补齐；枚举值需在 options 范围内。
3. `contacts`：
   - 自动从用户输入提取联系人姓名/手机号并映射 CONTACT 的 formFieldId；
   - 支持多联系人；
   - 用户未提供联系人信息时传 `[]`，不强行追问。
4. 创建接口：
   - `POST https://uc.marketup.cn/api/uc/v1/account/saveV2`
   - JSON body 关键字段：`accountInfo`、`contacts`、`accountType`（可选，`DEFAULT_TYPE` / `ABM_TYPE`）。

---

## 21. 修改客户信息（crmAccountAgent）

流程：**取 ACCOUNT 字段定义 → 按字段逐条修改**。

1. 先 `GET .../queryCurrentFields?marketEntityType=2`，匹配目标字段的 `formFieldId`。
2. 每次只改一个字段，多个字段串行调用。
3. 修改接口：
   - `POST https://uc.marketup.cn/api/uc/v1/account/modify/profileData?accountId=<id>`
   - body：`{ "formFieldId": <number>, "value": "<string>" }`
4. 特殊处理：
   - 当目标字段是“客户所有人 / 负责人”（如 `field_name = user_select`），先查员工列表拿 `companyUserId`，再把该 ID 字符串作为 `value` 传入。

---

## 22. 查询客户公海配置（crmAccountAgent）

用户提到客户公海规则/配置/领取限制/回收规则时：

**接口**：`GET https://uc.marketup.cn/api/uc/v1/account/accountPool/-1`

展示建议：

- 领取规则 `visibleRule`：
  - `ALL_ACCOUNT`：对所有成员开放
  - `NONE_ACCOUNT`：不对成员开放
- `receiveLimit`：已开启/已关闭
- `autoRecycle`：已开启/已关闭
- 生效时间：`executeTime`、`accountMinCreateTime`
- 回收规则：逐条展示 `name`、`stage`、`day`、`hour`、`state`
  - `NOT_FLOW_UP`：从未跟进
  - `NO_BUSINESS_CHANCE`：无商机
  - `NOT_UPDATE_FOLLOW_UP_RECORD`：未更新跟进记录

---

## 辅助接口

### 当前用户

`GET https://uc.marketup.cn/api/uc-open/v1/user/currentUser`  
用于「分配给我」、转客户默认负责人等场景；响应里当前员工标识一般为 `data.uid`（与分配接口里的 `companyUserId` / `ownerCompanyUserId` 对应关系以实际 JSON 为准）。

### 搜索公司员工

`GET https://uc.marketup.cn/api/uc-open/v1/company/user/team/list`  
扁平查询：`page`、`size`、`sort`、`sortType`、`searchValue`、`leadsManageType`（`SDR` | `SALE` | `NOT_PARTICIPATE_ASSIGN`）等。

---

## 附：references（详细 curl / jq）
- 索引与说明：[references/README.md](references/README.md)
- API Key 预检与脚本流程：[references/setup-marketup-api-key.md](references/setup-marketup-api-key.md)
- 列表 / 详情 / 快捷搜索 / jq：[references/find-leads.md](references/find-leads.md)
- 创建、改字段、跟进、分配、标签、领取、退回：[references/leads-mutations.md](references/leads-mutations.md)
- 跟进历史、变更历史、行为轨迹：[references/leads-history.md](references/leads-history.md)
- 表单字段、转客户：[references/convert-and-forms.md](references/convert-and-forms.md)
- 公海列表、公海配置、当前用户、搜员工：[references/pool-and-users.md](references/pool-and-users.md)
- 客户查询（详情/列表/高级筛选）：[references/accounts-query.md](references/accounts-query.md)
- 客户创建/修改/公海配置：[references/accounts-mutations-and-pool.md](references/accounts-mutations-and-pool.md)
