---
name: isp-api-tester
description: ISP 开放平台接口测试 Agent。当用户需要对百望开放平台的 ISP 接口进行自动化测试、生成测试报告时使用此 Skill。整合了 isp-login-skill（认证）、queryDB-skill（数据准备）和 api-test-reporter（测试报告）。
---

# ISP API Tester - 开放平台接口测试

## 功能概述

本 Skill 提供完整的百望 ISP 开放平台接口测试能力：
- **认证模块**：自动获取 access_token 并为每条请求动态生成签名
- **数据准备**：从数据库获取真实测试数据（queryDB-skill）
- **接口测试**：批量执行测试用例，支持 v6.0 / v7.0 接口版本
- **报告生成**：生成可视化的 HTML 测试报告（模板与数据分离，极速）

---

## 架构原则（重要）

### 零脚本生成

**Agent 不往项目目录生成、复制或重写任何脚本。** 项目目录只放配置文件。

| 职责 | 脚本位置 | 说明 |
|------|---------|------|
| ISP 专属测试执行器 | `~/.workbuddy/skills/isp-api-tester/scripts/run_isp_test.py` | 内置动态签名 + 云端/本地返参兼容 |
| ISP 认证 | `~/.workbuddy/skills/isp-login-skill/scripts/isp_auth.py` | get_open_token + get_open_sign |
| 数据库查询 | `~/.workbuddy/skills/queryDB-skill/scripts/db_query.py` | DatabaseClient + TestCaseGenerator |
| HTML 报告生成 | `~/.workbuddy/skills/api-test-reporter/scripts/generate_report.py` | 被 isp-api-tester 跨 skill 引用 |

### 配置文件命名规则

- **按接口名分开**：`test_config_{接口方法名}.json`，例如：
  - `test_config_queryinvoicepool.json` → `baiwang.input.invoice.queryinvoicepool`
  - `test_config_invoicepool_query.json` → `baiwang.input.invoicepool.query`
  - `test_config_querymaininfo.json` → `baiwang.input.invoice.querymaininfo`
- 跨会话复用：测试某个接口前，先查项目目录下是否已有对应配置文件，有则直接复用

---

## 执行命令

```bash
# 标准执行（Windows PowerShell）
python $env:USERPROFILE\.workbuddy\skills\isp-api-tester\scripts\run_isp_test.py --config test_config_querymaininfo.json --output ./

# 或使用绝对路径
python "C:\Users\PC\.workbuddy\skills\isp-api-tester\scripts\run_isp_test.py" --config test_config_queryinvoicepool.json --output ./
```

执行完毕自动生成：
- `test_report_<method>_<timestamp>.html`：可视化报告（双击打开）
- `test_results_<method>_<timestamp>.json`：原始结果
- `__REPORT_DATA__.js`：报告数据文件（与 HTML 同目录）

---

## 配置文件格式（test_config_xxx.json）

```json
{
  "meta": {
    "title": "发票主信息查询接口测试",
    "base_url": "http://opapi.test.51baiwang.com/router/rest",
    "method": "baiwang.input.invoice.querymaininfo",
    "version": "6.0",
    "timeout": 30,
    "isp_auth": {
      "appKey": "1000139",
      "appSecret": "1bccbe47-917e-4374-8fe9-85b44fecab84",
      "username": "cpy001",
      "password": "Aa123456.",
      "userSalt": "15258c22aa1349819e8cf20c0da04956"
    }
  },
  "fixed_params": {
    "taxNo": "91440606MA4WHN8C8X"
  },
  "test_cases": [
    {
      "id": "TC_001",
      "group": "票种覆盖-税控票",
      "name": "01-增值税专用发票",
      "desc": "税控票：invoiceCode + invoiceNumber 都必传",
      "body": {
        "invoiceCode": "044031900101",
        "invoiceNumber": "12345678"
      },
      "expect": {
        "success": true,
        "response.invoiceType": "01"
      }
    }
  ]
}
```

### v7.0 接口配置差异

v7.0 接口需要在 `meta` 中指定版本，并在 `body` 中传入额外公共参数：

```json
{
  "meta": {
    "version": "7.0",
    "isp_auth": { ... }
  },
  "fixed_params": {
    "taxNo": "91440606MA4WHN8C8X",
    "encryptType": "AES",
    "encryptScope": "request"
  }
}
```

`encryptType` / `encryptScope` 在 v7.0 中既是 body 字段，也会被自动提取到 URL query 参数并参与签名。

---

## 发票类型入参规则（重要）

### 三类发票的字段差异

| 发票大类 | 票种代码 | invoiceCode | invoiceNumber | 备注 |
|---------|---------|:-----------:|:-------------:|------|
| **数电票** | 31/32/51/59/61/83/84 | ❌ **不传** | ✅ 20位数电号码 | 传空串会触发704 |
| **税控票** | 01/03/04/08/10/11/14/15 | ✅ 必传 | ✅ 必传 | 传统税控票 |
| **数电纸票** | 85/86/87/88 | ✅ 必传 | ✅ 必传 | 同时有数电号码 |

**关键**：数电票（31/32/51/59/61/83/84）查询时，`invoiceCode` 字段**完全不传**（连空字符串都不行，传 `""` 会报704参数为空）。

### DB 字段映射

| 票种 | invoiceNumber 来源 | invoiceCode 来源 |
|------|-----------------|----------------|
| 数电票 | `E_INV_NUM`（20位数电号码） | 无此字段 |
| 税控票 | `INV_NUM` | `INV_KIND`（发票代码） |
| 数电纸票 | `INV_NUM` | `INV_KIND` |

---

## 响应校验规则（不可改动）

1. **`success=true`** → 自动校验 `invoiceList`/`response`/`model` 非空
2. **`success=false`** → 不校验列表
3. **不校验 HTTP 状态码**（用户明确要求）

### `expect` 支持的字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | bool | 校验响应体 success 字段 |
| `response.{field}` | any | 校验 response 节点下的字段值 |
| `model.{field}` | any | 校验 model 节点下的字段值 |
| `has_response` | bool | 期望 response/model 字段存在 |
| `check_page_data` | bool | 期望返回列表/分页数据 |

**不使用 `http_status`、`success_allow_any`、`check_invoice_list_not_empty` 等自定义字段。**

---

## 测试环境信息

| 参数 | 值 |
|------|---|
| 接口地址 | `http://opapi.test.51baiwang.com/router/rest` |
| appKey | `1000139` |
| username | `cpy001` |
| password | `Aa123456.` |
| userSalt | `15258c22aa1349819e8cf20c0da04956` |
| appSecret | `1bccbe47-917e-4374-8fe9-85b44fecab84` |
| 购方税号 | `91440606MA4WHN8C8X` |
| 数据库 | `10.115.96.247:3306/jxindependent0`，user: `jxindependent` |

---

## 用例设计原则

1. **正向用例的入参必须来自数据库真实数据**，确保接口能查到对应记录
2. 数电票用例**不传 invoiceCode 字段**（不是传空串，是完全不传）
3. 正向用例期望 `"success": true`，异常用例期望 `"success": false`
4. 时间范围参数用近期日期（近3个月），避免数据量超500
5. 数据量可能超500的查询必须加 `pageNum`

---

## 依赖

```bash
pip install requests pymysql
```
