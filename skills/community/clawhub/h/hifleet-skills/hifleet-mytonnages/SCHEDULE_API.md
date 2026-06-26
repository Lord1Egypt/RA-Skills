# 船期接口（路由 B）

本文件为 **hifleet-mytonnages** 中 **路由 B** 的约定；**路由 A（邮件船货盘）不适用本文**。

---

## 分发模式

1. 船期数据由 **HiFleet `api.hifleet.com`** 提供；触发路由 B 时由助手在环境中发 **HTTPS** 请求，**不得**用邮件检索、SQLite 或臆造数据代替。  
2. **列表须全量返回**：**`FULL_LIST_POLICY.md`**（分页拉齐 **`total`**，查到多少展示多少，**禁止**只返回前几条）。  
3. 用户在 **HiFleet 网站**申请密钥，与网站账号绑定、**按次计费**；本地存为 `hifleet_api_key` / `HIFLEET_API_KEY`；在请求里以 **`api_key`（query/header）** 或船期列表的 **`sk`（query）** 传递**同一串**，**勿在对话中完整暴露**。

---

## 配置与 API 基址

下文 **`{base}`** 表示**班轮船期 API 根**（无末尾 `/`）。

| 含义 | 默认值 |
|------|--------|
| `{base}`（班轮 OpenClaw 根） | `https://api.hifleet.com/openclaw/vessel/charter/liner`（主机可由 `HIFLEET_API_BASE` 覆盖，见 [../references/api_base.md](../references/api_base.md)） |

**解析顺序**：`hifleet_liner_api_base`（config）→ `HIFLEET_LINER_API_BASE`（环境）→ 上表默认。  
**用户密钥字符串**：`hifleet_api_key`（config）→ `HIFLEET_API_KEY`（环境）。各接口在 HTTP 里以 **`api_key`（query/header）** 或 **`sk`（仅船期列表，见下）** 使用同一串，勿混为两个不同值。

无有效密钥时**不得**调接口，引导用户配置（见 `SKILL.md` Workflow 3）。

---

## 1. 港口联想

**`GET {base}/ports/suggest`**

| 方式 | 名称 | 值 |
|------|------|-----|
| **Header** | `api_key` | 用户 `api_key` 字符串 |
| **Query** | `keyword` | **英文**港口名（如上海 → `Shanghai`；助手需先把中文/口语港名换成英文再请求） |
| **Query** | `from` | `0` |
| **Query** | `size` | `1`（每条港只取一条联想） |
| **Query** | `api_key` | 与用户密钥相同，与 Header 一致 |

**成功响应**（结构示例）中从 **`data[0].portId`** 取装/卸港 ID；`msg` 为 `SUCCESS`、业务成功时 `status` 为 `"1"` 等以线上为准。装港、卸港（若用户有提）**各请求一次**，各取 `size=1` 对应一条。

**与船期查询的衔接（必读）**

- 班轮列表的筛选依据是 **`portId`（及日窗等）** 在 **`POST /schedules` 的 `params` 里**一次提交，**不是**在拿到结果后按**港口名字符串**再挑记录。  
- 用户**同时**说了装货港、卸货港时：须对**装港、卸港各调一次** §1 拿到 **`portid`** 与 **`dischargingPortid`**，并在**同一次** `POST /schedules` 的 **`params` 中同时带上两者**（见 §2 示例）。  
- **禁止**：只传装港的 `portid`、等返回后再在回答里用「卸货港是不是新加坡 / 用港名在文本里筛」**冒充**成「已按两港查过」——**不允许**。缺卸港的 `portId` 时须先走 §1 用卸港**英文** `keyword` 联想不到再提示用户，**不要**用港名在列表里硬筛替代 `dischargingPortid`。

**失败**：如 `code`/`message` 为 token 或鉴权类错误，检查 `api_key` 是否在 Header 与 Query 中均已正确携带。

---

## 2. 船期列表

**`POST {base}/schedules?sk={URL 编码的 api_key 字符串}`**

- **Query**：`sk` = 用户 `api_key`（与上节同一配置值）。若仍报「token 为空」，与后端核对鉴权参数。  
- **Body**：`Content-Type: application/json`。**现网**将装港、卸港、是否公开、**受载日窗** 一并放在 **`params` 中**。筛选与后端数据对齐依赖 **`portid` / `dischargingPortid`**，**不**能靠助手机侧对**港名**的模糊包含来替代。  

| 字段 | 说明 |
|------|------|
| `offset` / `limit` | 分页；**硬性全量**见 **`FULL_LIST_POLICY.md`**：`limit` 取单页上限，循环 `offset` 直至拉齐 **`total`**，**合并全部 `data` 后再向用户输出**；**禁止**只取第一页或只展示前几条 |
| `params.portid` | 装港 `portId`（**仅**能来自 §1 的 `portId`，**禁止**用未解析的港名当查询键） |
| `params.dischargingPortid` | 卸港 `portId`（**同上**）；**用户提了两港时本条必填**；仅单港需求时可省略（以现网为准） |
| `params.isPublic` | 如 `true` |
| `params.openDateStart` | 受载窗**起**，**`yyyy-MM-dd` 裸字符串** |
| `params.openDateEnd` | 受载窗**止**，**`yyyy-MM-dd` 裸字符串** |
| 其它 | 若后端在 `params` 中**增加**解约日窗等字段（如 `openEndDateStart`），**以你方现网/ShowDoc 为准** |

**口语「近期」的组参规则（助手侧）**

- 用户只模糊说「最近」「近期」、未给具体日：仍须通过 §1 取 **portid**；`params.openDateStart` / `openDateEnd` 设为由 **明天** 起算的**较宽**受载窗（**不要**只限 7 天、**不要**强套「解约早于受载」等额外关系）；若用户**未**提卸港，是否传 `dischargingPortid` 以现网为准。  
- 用户给了具体受载窗时，把其起、止**直接**写进 `params.openDateStart`、`params.openDateEnd`（**字符串**）。

**请求示例（`params` 内含受载日）**

```json
{
  "offset": 1,
  "limit": 10,
  "params": {
    "portid": "22214",
    "dischargingPortid": "15843",
    "isPublic": true,
    "openDateStart": "2026-04-23",
    "openDateEnd": "2026-05-07"
  }
}
```

**联调注记**

- 使用**真实** `sk` 时，接口**可用**；成功返回的 **`data` 中每条须有顶层 `id`**, 作 **`dataId` 调解锁。  
- **可**在**仅**关心装港、**未**指定卸港 的场景下，用下面 body **只**带 `portid`+`isPublic` 拉大列表，再在结果上**只**作**受载/解约日**等辅助压缩（**不得**在缺少 `dischargingPortid` 的查询结果上，用「是否含某卸港名字」**冒充**两港全约束查询）。用户**已明确**装港+卸港的，**必须**用 §1 解出**两个** `portId` 并**同次** `POST` 带全（见上节「禁止」）。

```json
{
  "offset": 1,
  "limit": 10,
  "params": {
    "portid": "27800",
    "isPublic": true
  }
}
```

- 历史上曾用 **`filterLabels` + 多段 `openDate*` 数组** 等形态；**当前以本节 `params` 为准**；若你方同时保留**旧式** `openDateDays` 筛桶，**以现网**实际接受为准。  

**联调与鉴权**（在公网用占位/无效 `sk` 试投 **`POST`）：服务**可达**；本环境会返回类似 `{"code":4005,"message":"token is empty.","url":".../schedules"}`，表示**未通过鉴权**、**不会**返回有效业务 `data`。**仅当**在 Query 中带上 HiFleet 下发的**真实** `api_key`（`sk=…`）后，才会按条件返回 `total` / `stat` / `data` 等。

**响应中 `id` 与 `dataId`（必读）**

- 成功时 **`data` 数组的每一条**船期对象，**必须**在**最外层**包含字段 **`id`**（数值或字符串，以线为准）。**解锁联系人**（§3）的 Query 参数 **`dataId`** = 该条记录的 **`id`** 转成字符串后传入。  
- **未解锁**状态下向用户展示时，`id` **须**展示（字段名可用「记录 id」），便于用户指定解锁对象；**不要**用其它嵌套 id 替代（除非线上一致约定）。  
- 若某次响应里 `data` 有元素**缺少**顶层 `id`，即接口不闭环，**无法**正确调用 unlock，应联系后台补全。  

**其它**：`stat` 等统计以线上为准。列表展示规则（Laycan、加密/解密、空字段）见 **§4**。

---

## 3. 解锁联系人

**`POST {base}/unlock`**

仅 **Query 参数**（无特殊说明时 **Body 可为空**）：

| Query | 说明 |
|--------|------|
| `dataId` | 船期列表 `data` 中该条船期对象的**顶层** **`id`**（与 `POST /schedules` 返回的该条 `id` 一致） |
| `typeCode` | 固定为 **`product_vessel_liner_charter`**（默认值） |
| `api_key` | 用户 `api_key` |

**Header**：与 §1 一致，建议同时带 **`api_key`: 与 Query 相同**（若你方网关要求，与 ports 行为对齐）。

成功后解析响应中的明文联系人/公司/电话/邮箱等展示给用户，仍**不**在对话中泄露完整 `api_key`。展示时遵守 **§4**：本条视为**已解锁**——须标注 **`（已解锁）`**，**勿**再提示用户去解锁；**无值的字段不输出**。

---

## 4. 用户可见输出（助手必读）

与 **`WORKFLOW_OUTPUT.md`**「路由 B」一致，摘要如下。

### 4.1 全量（硬性）

- 执行 **`FULL_LIST_POLICY.md`**：`total` 为 N 则须展示 **N 条**；**禁止**前几页摘要、抽样、「共 N 条仅示例 M 条」。  
- 须用 §2 分页拉齐 **`total`** 后**逐条**输出（见 **`WORKFLOW_OUTPUT.md`**）。

### 4.2 Laycan（一行）

- **禁止**分两行分别写「受载日期」「解约日期」等表头。  
- 将响应中的**受载窗**起止、**解约窗**起止（字段名以线上为准；请求里常见 `openDateStart` / `openDateEnd`，响应中若有解约同源字段一并纳入）格式化为 **`yyyy/MM/dd~yyyy/MM/dd`**。  
- **单行示例**：仅一段窗时 `Laycan：2026/05/06~2026/05/20`；两段都有时 `Laycan：受载 2026/05/06~2026/05/10；解约 2026/05/11~2026/05/20`（**仍一行**）。

### 4.3 空字段

- 值为 `null`、空串、仅空白、或本对象**未返回**的键：**不要**向用户展示该字段行。仅展示**有实质内容**的字段（列表查询与 §3 解锁后**均适用**）。

### 4.4 未解锁（加密 / 脱敏）与已解锁（解密）

- **判定已解锁**：优先以接口**显式字段**为准（如 `unlocked`、`decrypted`、`isDecrypt`、`lockStatus` 等，**以现网/ShowDoc 为准**）。若无显式字段，则当**船公司、联系人、电话、邮箱**等敏感项为**正常可读明文**且**不含**脱敏占位（如连续 `*`、`******`、`[已隐藏]`）时，视为**已解锁**。  
- **已解锁**：在本条船期展示**标题或首行**标注 **`（已解锁）`**；除 §4.3 外可输出所有**有值**字段；**禁止**再出现「可以解锁」「请解锁查看联系人」等引导。  
- **未解锁**：**仅允许**输出：**Laycan**（§4.2）、**装货港**、**卸货港**、**记录 id**（顶层 `id`）、**航线**（响应内航线/班次名等字段，以线为准）。**禁止**输出船公司、联系人、电话、邮箱及其它敏感字段（**不要**把 `******` 展开成多行说明）。文末**须**简短提示：用户**确认消耗积分**后可调用 **§3 `/unlock`** 获取完整信息。

---

## 错误

HTTP 4xx/5xx 及 JSON 内 `code`/`message` / `msg` 非成功：用简短中文说明，不贴完整 `api_key`、不贴长堆栈。
