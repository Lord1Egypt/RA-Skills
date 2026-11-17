# 船舶制裁风险评估 API / Vessel Sanction Risk Assessment API

按 **IMO** 评估船舶制裁风险（依次检索 US SDN → EU → UK → Canada SEMA → UN → CN），返回风险等级、制裁信息来源、制裁对象、明细列表等。**需配置 `api_key`**。

**API 基址**：默认 `https://api.hifleet.com`（`{base}`）；其它部署可设 **`HIFLEET_API_BASE`**（无末尾 `/`）。见 [api_base.md](api_base.md)。

> **Agent 必读（易错点）**  
> 1. 只调 data.api：`{base}/sanction/assess/shiprisk/token`。  
> 2. 参数名是 **`imonumber`**，不是常见的 `imo`。传 `imo=` 会参数校验失败或拿不到结果。  
> 3. 不要用网站路径 `www.hifleet.com/shipdetail/sanction/assess/shiprisk`（那是浏览器页，不是 OpenClaw 接口）。  
> 4. 不要与海事处罚 `/maritime/penalty/list/token`、制裁区港口 `/sanctions/port/token` 混淆。

---

## 请求

| 项目 | 值 |
|------|-----|
| 请求 URL | `{base}/sanction/assess/shiprisk/token` |
| 请求方式 | `GET` 或 `POST` |

### Query 参数

| 参数名 | 示例值 | 必选 | 类型 | 说明 |
|--------|--------|------|------|------|
| api_key | (从配置读取) | 是 | string | 接口授权 `api_key`（也可放请求头 `x-api-key`） |
| imonumber | 9123456 | 是 | int | **参数名固定为 imonumber**（IMO，通常 7 位） |

兼容旧路径（需 `usertoken`，非 OpenClaw）：`{base}/sanction/assess/shiprisk`。技能请只用 **`/token`**。

网站档案页同源能力对应 shipdetail 的 `/shipdetail/sanction/assess/shiprisk`，**仅作业务对齐说明，Agent 禁止直调该网站路径**。

---

## 成功响应

- `status`: `"1"`
- `msg`: `"SUCCESS"`
- `data`: 评估结果对象

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| shipImo | int | 查询 IMO |
| riskLevel | string | **字符串**：`HIGH_RISK` / `MEDIUM_RISK` / `LOW_RISK` / `STANDARD`（不是数字 0/1/2） |
| reason | string | 风险原因说明（英文） |
| source | string | 制裁信息来源（如 US SDN list、EU sanctions list） |
| checkTime | string | 检查/数据更新日期 |
| target | string | 制裁对象角色（如本船、UBO、TEC、OPT、OTH 等） |
| data | array | 高风险时的制裁明细（已归一化） |
| otherships | array | 中风险时：关联公司下其他高风险船舶 |

#### data[] 明细（高风险）

| 字段 | 说明 |
|------|------|
| imo | IMO |
| date_designated | 制裁时间 |
| data_source | 来源 |
| check_date | 检查时间 |
| sanction_reason | 制裁原因 |
| legal_basis | 法律依据 |

#### otherships[]（中风险）

| 字段 | 说明 |
|------|------|
| shipName | 关联船名 |
| shipImo | 关联船 IMO |
| parentCompanyRole | 关联公司角色 |
| sanctionDate | 制裁日期 |
| legalBasis | 法律依据 |

### 风险等级含义（展示话术）

| riskLevel | 含义 |
|-----------|------|
| HIGH_RISK | 本船或 UBO/TEC/OPT 公司已在官方制裁名单 |
| MEDIUM_RISK | 本船未直接上榜，但同关联公司下其他船舶有制裁记录（潜在风险） |
| LOW_RISK | 当前未发现制裁风险 |
| STANDARD | 未知/未评估 |

---

## 调用流程（Agent）

1. 检查 `api_key`（`HIFLEET_API_KEY`）。
2. 仅有船名时先 `position/shipSearch` 取 IMO（结果字段可能叫 `imonumber` / `imo`，填入本接口时统一用参数名 **`imonumber=`**）。
3. **正确示例**：`GET {base}/sanction/assess/shiprisk/token?imonumber={imo}&api_key=...`
4. 按 `riskLevel` 展示：高风险列出来源/对象/`data`；中风险展示 `otherships`；低风险如实说明无制裁风险。
5. 勿伪造名单内容；勿与 PSC、事故事件、海事处罚混答。

---

## 错误与权限

- 参数错误：`imonumber` 为空或 ≤0。
- `api_key` 无效或未授权能力 `vessel.sanction.shiprisk`：提示开通制裁数据接口。
- 若请求打到 `/shipdetail/...` 或返回 404：说明用了网站路径，应改回 `{base}/sanction/assess/shiprisk/token`。