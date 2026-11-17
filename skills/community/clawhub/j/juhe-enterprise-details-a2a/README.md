# 企业信息精确查询

支付宝 AI 付费 Skill。产品形态：**一次付费 = 企业详细工商信息**（基本照面、主要人员、股东、分支机构、变更记录、经营异常）。

> **敏感数据提示：** 返回结果可能含法人与主要人员姓名、股东名称、企业注册地址、统一社会信用代码/注册号。查询方无需提供个人隐私，但报告本身含公开敏感标识，须最小化展示与留存。自然人股东证件类型/号码多为非公示项（`-`）；勿暗示已采集用户个人隐私。

## 目录说明

| 路径            | 用途                                |
| --------------- | ----------------------------------- |
| `SKILL.md`      | Agent 执行规范（触发、402、约束）   |
| `OUT_FORMAT.md` | 支付成功后的报告渲染模板            |
| `README.md`     | 本文件：收单参数与返回字段说明      |

## 收单

| 项目       | 值                               |
| ---------- | -------------------------------- |
| resourceId | `319`                            |
| 请求参数   | `keyword`（企业全名 / 注册号 / 统一社会信用代码） |
| 请求地址   | `https://apis.juhe.cn/a2a/query` |

```json
{
  "resourceId": "319",
  "data": {
    "keyword": "天聚地合（苏州）科技股份有限公司"
  }
}
```

`keyword` 为空或未通过合规校验时禁止请求。

## 与尽调 Skill 的关系

| Skill                       | 定位                                           |
| --------------------------- | ---------------------------------------------- |
| 本 Skill                    | 仅企业详细工商信息                             |
| `../enterprise-dd-pro-a2a`  | 尽调标准版：工商信息 + 经营异常/被执行/失信/限高 |

纯查工商档案（法人/股东/经营范围等）且无风险尽调意图时，使用本 Skill；需要风险快检时引导 `enterprise-dd-pro-a2a`。

## 完整返回数据说明

外层与结果根对象：

| 参数名       | 类型   | 描述                                         |
| ------------ | ------ | -------------------------------------------- |
| error_code   | int    | 错误码，`0` 成功                             |
| reason       | string | 状态信息（如 `操作成功`）                    |
| result       | obj    | 结果包装对象                                 |
| result.data  | obj    | **企业工商详情根对象**（渲染主数据）         |
| result.sign  | string | 签名（不对用户展示）                         |

> 报告展示规则见 `OUT_FORMAT.md`。数据路径以 `result.data.*` 为准；`result.data` 缺失或为空时按查无处理。

---

## result.data（工商主体）

### 基本照面

| 名称            | 类型   | 说明                                       |
| --------------- | ------ | ------------------------------------------ |
| name            | string | 公司名称                                   |
| status          | string | 经营状态（如存续、在业）                   |
| econ_kind       | string | 企业类型                                   |
| oper_name       | string | 法定代表人                                 |
| regist_capi     | string | 注册资本（含单位文案）                     |
| regist_capi_new | string | 注册资本数值（默认万元）                   |
| currency_unit   | string | 货币单位（如 `CNY`）                       |
| start_date      | string | 成立日期                                   |
| check_date      | string | 核准日期                                   |
| term_start      | string | 营业开始日期                               |
| term_end        | string | 营业结束日期                               |
| end_date        | string | 注销日期（`-` 表示无）                     |
| credit_no       | string | 统一社会信用代码                           |
| reg_no          | string | 企业注册号                                 |
| org_no          | string | 组织机构号                                 |
| belong_org      | string | 所属工商局                                 |
| province        | string | 省份缩写                                   |
| address         | string | 注册地址（部分环境也可能为 `addresses`）   |
| scope           | string | 经营范围                                   |
| id              | string | 主体内部标识                               |
| new_status      | string | 状态码                                     |
| title           | string | 标题（多为 `-`）                           |

### 主要人员 employees[]

| 名称      | 类型   | 说明         |
| --------- | ------ | ------------ |
| name      | string | 主要人员姓名 |
| job_title | string | 职位         |

### 股东 partners[]

| 名称                                      | 类型   | 说明                                         |
| ----------------------------------------- | ------ | -------------------------------------------- |
| name                                      | string | 股东名称                                     |
| stock_type                                | string | 股东类型                                     |
| identify_type                             | string | 证照/证件类型（自然人多为非公示项 `-`）      |
| identify_no                               | string | 证照/证件号码（自然人多为 `-`）              |
| should_capi_items[].shoud_capi            | string | 认缴出资额（字段名注意拼写 `shoud_capi`）    |
| should_capi_items[].invest_type           | string | 认缴出资方式                                 |
| should_capi_items[].should_capi_date      | string | 认缴出资时间                                 |
| real_capi_items[].real_capi               | string | 实缴出资额                                   |
| real_capi_items[].invest_type             | string | 实缴出资方式                                 |
| real_capi_items[].real_capi_date          | string | 实缴时间                                     |

### 分支机构 branches[]

| 名称 | 类型   | 说明         |
| ---- | ------ | ------------ |
| name | string | 分支机构名称 |

> 个别文档曾写作 `brances`，以接口实际字段 `branches` 为准。

### 变更记录 changerecords[]

| 名称           | 类型   | 说明     |
| -------------- | ------ | -------- |
| change_item    | string | 变更项目 |
| change_date    | string | 变更日期 |
| before_content | string | 变更前   |
| after_content  | string | 变更后   |
| u_tags         | int    | 内部标签 |

### 经营异常 abnormal_items[]

| 名称       | 类型   | 说明         |
| ---------- | ------ | ------------ |
| in_reason  | string | 列入原因     |
| in_date    | string | 列入日期     |
| out_reason | string | 移出原因     |
| out_date   | string | 移出时间     |
| department | string | 决定机关（若有） |

空数组时报告中跳过对应章节。

---

## 成功响应样例（节选）

```json
{
  "error_code": 0,
  "reason": "操作成功",
  "result": {
    "data": {
      "name": "天聚地合（苏州）科技股份有限公司",
      "status": "存续",
      "econ_kind": "股份有限公司（上市、自然人投资或控股）",
      "oper_name": "左磊",
      "regist_capi": "5011.82万人民币",
      "regist_capi_new": "5011.82",
      "currency_unit": "CNY",
      "start_date": "2010-02-25",
      "check_date": "2024-10-24",
      "term_start": "2010-02-25",
      "term_end": "-",
      "end_date": "-",
      "credit_no": "9132059455117770X5",
      "reg_no": "320512000114943",
      "org_no": "55117770X",
      "belong_org": "苏州市数据局",
      "province": "JS",
      "address": "中国（江苏）自由贸易试验区苏州片区苏州工业园区融富街9号16层",
      "scope": "一般项目：网络技术服务；计算机软硬件及辅助设备批发；…",
      "employees": [
        { "name": "左磊", "job_title": "董事长兼总经理" },
        { "name": "任园", "job_title": "监事" }
      ],
      "partners": [
        {
          "name": "左磊",
          "stock_type": "自然人股东",
          "identify_type": "-",
          "identify_no": "-",
          "should_capi_items": [
            {
              "shoud_capi": "403.7978 万人民币",
              "invest_type": "货币",
              "should_capi_date": "2016-12-20"
            }
          ],
          "real_capi_items": []
        }
      ],
      "branches": [],
      "changerecords": [
        {
          "u_tags": 0,
          "change_date": "2024-07-22",
          "change_item": "市场主体类型",
          "before_content": "股份有限公司（非上市、自然人投资或控股）",
          "after_content": "股份有限公司（上市、自然人投资或控股）"
        }
      ],
      "abnormal_items": []
    },
    "sign": "18b747f786ce45029f64cc95d7540b4b"
  }
}
```

> 渲染时外层 `error_code` / `reason` / `result.sign` 不对用户展示；字段填充与空值规则见 `OUT_FORMAT.md`。

---

## 请求参数

| 参数    | 必填 | 类型   | 说明                                           |
| ------- | ---- | ------ | ---------------------------------------------- |
| keyword | 是   | string | 企业全名、注册号或统一社会信用代码（18 位）   |

规范化：去首尾空白；统一社会信用代码转大写；企业名称保留原始中文与括号。友好引导见 `SKILL.md` 第二步。
