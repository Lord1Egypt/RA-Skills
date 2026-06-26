---
name: medgroup-drgdip-skill
description: DRG/DIP 医保分组计算 — ICD 编码搜索、DRG/DIP 分组、医保结算、CC/MCC 查询。需使用个人 MedGroup API Key 并连接 MedGroup MCP SSE。
version: 1.0.11
homepage: https://medgroup.medchat.fun
user-invocable: true
metadata: {"openclaw":{"emoji":"🩺","homepage":"https://medgroup.medchat.fun","skillKey":"medgroup-drgdip-skill","primaryEnv":"MEDGROUP_API_KEY","requires":{"env":["MEDGROUP_API_KEY"],"config":["skills.entries.medgroup-drgdip-skill.config.medgroupMcpSseUrl"]}}}
---

# 🩺 MedGroup DRG/DIP Skill

CHS DRG/DIP 医保分组计算工具。通过 MCP 工具调用，支持多步编排。

## Privacy & Security

This skill relies on an external MedGroup MCP SSE server and a personal MedGroup API key.

**Credential handling**: Before enabling, confirm how your AI client stores the API key, whether it uses secure secret storage, and whether the key is scoped and revocable. When the client supports skill credentials, bind the key to `MEDGROUP_API_KEY`. Otherwise, configure it in the client-side MCP connection.

**Transparency note**: The manifest for this skill declares both a required credential (`MEDGROUP_API_KEY`) and a required MedGroup MCP SSE endpoint setting. If your client cannot surface or securely store those requirements, treat the integration as higher risk.

**Intended inputs**: This skill is intended for structured coding parameters such as ICD codes, gender, age, length of stay, and fee amounts. Do not use real patient identifiers in setup or connectivity tests.

**Vendor review**: Verify the authenticity of `medgroup.medchat.fun` and review its privacy, retention, and logging terms before enabling. If you need assurance that PHI is not logged or retained, request written documentation or an auditable addendum from the vendor.

**Recommended first use**: Test with synthetic data first (for example `J18.900` for pneumonia) to confirm connectivity.

**Regulatory scope**: If you plan to send real patient data, confirm your local legal and regulatory requirements first. Where required, request a Data Processing Agreement or equivalent auditable documentation from the vendor before use.

## 前置条件

使用前需要完成一次 MedGroup MCP 配置：

1. 到 [medgroup.medchat.fun](https://medgroup.medchat.fun) 注册并生成你自己的 API Key（`sk-` 开头）
2. 在支持 skill credential 的客户端中，将该密钥绑定到 `MEDGROUP_API_KEY`
3. 配置 MedGroup MCP SSE 连接地址 `https://medgroup.medchat.fun/mcp/sse`
4. 如需在 OpenClaw / ClawHub 中显式声明依赖，同时填写 `skills.entries.medgroup-drgdip-skill.config.medgroupMcpSseUrl`

配置完成后，以下工具即可使用。

## MCP 配置

### OpenClaw / ClawHub manifest 对应配置

本 skill 的 manifest 声明了以下前置项：

- `MEDGROUP_API_KEY`
- `skills.entries.medgroup-drgdip-skill.config.medgroupMcpSseUrl`

在 `~/.openclaw/openclaw.json` 中可这样填写：

```json
{
  "skills": {
    "entries": {
      "medgroup-drgdip-skill": {
        "apiKey": "sk-your-api-key",
        "config": {
          "medgroupMcpSseUrl": "https://medgroup.medchat.fun/mcp/sse"
        }
      }
    }
  }
}
```

### 通用 MCP 模板

可直接使用本目录下的配置模板文件：

`mcp-server/skills/medgroup-drgdip-skill/mcp.json`

模板内容如下：

```json
{
  "mcpServers": {
    "medgroup": {
      "url": "https://medgroup.medchat.fun/mcp/sse?api_key=sk-your-api-key",
      "transport": "sse"
    }
  }
}
```

使用方式：

1. 下载或复制 `mcp-server/skills/medgroup-drgdip-skill/mcp.json`
2. 将其中的 `sk-your-api-key` 替换为你在 MedGroup 账号中生成的个人 API Key
3. 如果你的客户端支持导入 `mcp.json`，可直接导入
4. 如果你的客户端支持 skill 级 secret storage，优先把 API Key 存在客户端的凭证配置中
5. 如果你的客户端只提供 MCP Server 配置界面，复制其中 `mcpServers.medgroup` 这一段即可

## 典型场景

### 场景 1：完整的 DRG 分组 + 结算

1. 用 `search_icd` 确认主诊断编码（如用户说"肺炎"，搜到 J18.900）
2. 用 `drg_grouping` 做分组，拿到 DRG 编码、分值和 CC 状态
3. 用 `calculate_settlement` 根据分值和总费用计算医保结算金额与盈亏

### 场景 2：DIP 分组查询

1. 用 `search_icd` 查主诊断和手术编码
2. 用 `dip_grouping` 做分组，拿到 DIP 病种编码、名称和分值

### 场景 3：编码与 CC/MCC 分析

1. 用 `find_code_info` 查编码所属的 MDC 和 ADRG 列表
2. 用 `get_cc_status` 查次要诊断的 CC/MCC 等级和排除情况

### 场景 4：盈亏分析

用户给出病种分值、总费用和点值，直接用 `calculate_settlement` 计算，分析高低倍率和医院盈亏。

## 工具详细说明

### search_icd — 搜索 ICD 编码

搜索 ICD-10 诊断编码或 ICD-9 手术操作编码。用户提供疾病/手术名称或编码，返回匹配列表。

| 参数 | 必填 | 说明 |
|---|---|---|
| query | 是 | 搜索关键词，可以是编码或名称 |
| type | 否 | `icd10`（诊断）/ `icd9`（手术）/ `both`（默认） |
| limit | 否 | 返回数量，默认 20，最大 50 |

示例：
```json
{"query": "肺炎", "type": "icd10", "limit": 5}
{"query": "冠脉搭桥", "type": "icd9", "limit": 5}
{"query": "J18.900", "type": "both"}
```

返回：编码列表，每项包含 code（编码）和 name（名称）。

### drg_grouping — DRG 分组计算

根据诊断和手术编码计算 DRG 分组结果，包括 MDC、ADRG、DRG 编码及 CC 状态。

| 参数 | 必填 | 说明 |
|---|---|---|
| pdx_code | 是 | 主诊断 ICD-10 编码，如 `J18.900` |
| gender | 是 | `男` / `女` |
| age | 是 | 患者年龄（岁） |
| adx_codes | 否 | 次要诊断，分号或逗号分隔，如 `I10.x00;E11.900` |
| proc_codes | 否 | 手术编码，分号或逗号分隔，如 `36.1200;39.6101` |
| los | 否 | 住院天数，默认 1 |
| icu | 否 | 是否 ICU：0=否，1=是，默认 0 |
| city_name | 否 | 城市版本，默认 `全国版` |

示例：
```json
{"pdx_code": "J18.900", "adx_codes": "I10.x00;E11.900", "gender": "女", "age": 45, "los": 7, "city_name": "全国版"}
```

返回：mdc_code、adrg_code、drg_code、cc_status（mcc/cc/nocc）、catalogue_info（含分值）。

⚠️ 城市名必须用完整格式：邯郸市、北京市、上海市（不能写：邯郸、北京、上海）。

### dip_grouping — DIP 分组计算

根据诊断和手术编码计算 DIP 分组结果。DIP 主要看主诊断 + 手术操作的组合。参数同 `drg_grouping`。

示例：
```json
{"pdx_code": "J18.900", "proc_codes": "31.0000;93.9600", "gender": "男", "age": 60, "los": 10, "city_name": "全国版"}
```

返回：dip_code、catalogue_info（含 name 名称、score 分值、type 类型）。

### calculate_settlement — 医保结算计算

根据病种分值和总费用计算医保结算金额，分析高低倍率和盈亏。

| 参数 | 必填 | 说明 |
|---|---|---|
| score | 是 | 病种分值（来自分组结果的 catalogue_info.score） |
| total_fee | 是 | 住院总费用（元） |
| fee_per_point | 否 | 分值单价（元），默认 60 |
| rate | 否 | 调整系数，默认 1 |
| high_ratio_limit | 否 | 高倍率阈值，默认 3 |
| low_ratio_limit | 否 | 低倍率阈值，默认 0.5 |

示例：
```json
{"score": 1.5, "total_fee": 15000, "fee_per_point": 60}
```

返回：standard_fee（标准费用）、fee_ratio（费用倍率）、ratio_type（high_ratio/normal_ratio/low_ratio）、payment_fee（结算金额）、balance（盈亏，正数盈利负数亏损）。

计算规则：正常倍率(0.5-3)按标准费用结算；低倍率(<0.5)按实际费用结算；高倍率(>3)按公式调整。

### find_code_info — 编码归属查询

查询诊断编码可能入组的 MDC（主要诊断类别）和 ADRG（相邻疾病诊断相关组）列表。

| 参数 | 必填 | 说明 |
|---|---|---|
| code | 是 | ICD-10 诊断编码，如 `J18.900` |
| city_name | 否 | 城市版本，默认 `全国版` |

示例：
```json
{"code": "J18.900", "city_name": "全国版"}
```

返回：mdc_codes（如 ["MDCE"]）、adrg_codes（如 ["ES1", "ES3"]）。

### get_cc_status — CC/MCC 状态查询

查询次要诊断的合并症/并发症状态。必须同时提供主诊断，因为 CC/MCC 状态取决于主诊断（某些次要诊断会因与主诊断相关而被排除）。

| 参数 | 必填 | 说明 |
|---|---|---|
| pdx_code | 是 | 主诊断编码 |
| adx_codes | 是 | 次要诊断编码数组，如 `["I10.x00", "E11.900"]` |
| city_name | 否 | 城市版本，默认 `全国版` |

示例：
```json
{"pdx_code": "J18.900", "adx_codes": ["I10.x00", "E11.900", "N18.500"], "city_name": "全国版"}
```

返回：每个次要诊断的 code、status（mcc/cc/none）、excluded（是否被排除）。

说明：MCC = 严重合并症/并发症；CC = 一般合并症/并发症；排除 = 与主诊断相关，不计入 CC。
