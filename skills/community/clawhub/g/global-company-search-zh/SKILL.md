---
name: global-company-search-zh
description: 依托全球企业数据库，通过产品品类、所属行业、企业规模筛选目标公司，助力外贸从业者挖掘潜在客户、优质供应商以及长期合作伙伴。
metadata: {"version":"1.0.3","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🏢","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 全球企业库找公司

使用跨境魔方开放平台API从全球企业库数据搜索公司。

## 概述

本技能通过一个列表搜索脚本提供对跨境魔方全球企业库公司数据的访问。通过`auth.py`脚本提供 API密钥生成、充值；

## 脚本运行

### 环境准备

1. **检查 Python**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要**：始终使用直接脚本调用，如 `python scripts/global_company_search.py`。**不要使用** shell 复合命令如 `cd scripts && python global_company_search.py`

### 全球企业库公司列表搜索 (`global_company_search.py`)
- **返回粒度**：每家公司为一行记录
- **适用场景**：关心的是全球企业库数据中"有哪些公司"
- **示例**：
  - "找生产LED灯的厂家"
  - "通过官网链接找公司"
- **参数**：查看参数说明 [全球企业库公司列表](references/global-company-list-api.md)

## API密钥与充值
使用此技能需要API密钥。API密钥保存在 `~/.upkuajing/.env` 文件中：
```bash
cat ~/.upkuajing/.env
```
**文件内容示例**：
```
UPKUAJING_API_KEY=your_api_key_here
```
### **未设置API密钥**
请先检查 `~/.upkuajing/.env` 文件是否有 UPKUAJING_API_KEY;
如果未设置 UPKUAJING_API_KEY API密钥，请提示并让用户选择：
1. 用户有，由用户提供(手动添加到 ~/.upkuajing/.env 文件)
2. 用户没有，你可使用接口进行申请（`auth.py --new_key`），申请到新密钥后，会自动保存到 ~/.upkuajing/.env
等待用户选择；

### **账户充值**
如果调用接口响应账户余额不足时，需说明并引导用户进行账户充值：
1. 创建充值订单（`auth.py --new_rec_order`）
2. 根据订单响应，发送支付页面URL给用户，引导用户打开地址付款，付款成功后告诉你；

### **获取账户信息**
可通过此脚本，获取UPKUAJING_API_KEY对应的账户信息 `auth.py --account_info`

## API密钥与跨境魔方账号
- 新申请的API密钥：在[跨境魔方开放平台](https://developer.upkuajing.com/)注册、登录后进行账号绑定

### **上报Skill调用异常**
当API调用失败或返回异常数据（服务端错误、超时、响应格式错误等）时，先用自然语言向用户解释异常情况，并询问是否需要上报给平台追踪；用户确认后才执行上报：
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/search/depth_company/company/list","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"公司搜索查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**所有API调用都会产生费用**，不同接口计费方式不同。

**最新价格**：用户可访问 [详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或者使用：`python scripts/auth.py --price_info`（返回接口完整定价）

### 列表搜索计费规则

按**调用次数**计费，每次返回最多20条记录：
- 调用次数：`ceil(query_count / 20)` 次
- **只要 query_count > 20，执行前必须：**
  1. 告知用户预计调用次数
  2. 停止，等待用户在独立消息中明确确认后，再执行脚本

### 费用确认原则

**任何会产生费用的操作，都必须先告知、等待用户明确确认，不得在告知的同一条消息中直接执行。**


## 工作流程
根据用户意图选择合适的参数。

### 决策指南

| 用户意图 | 使用API |
|-------------|---------|
| "找生产XXX的公司" | 全球企业库公司列表（products / keywords） |
| "找有邮箱/电话的公司" | 全球企业库公司列表 existEmail=1 / existPhone=1 |
| "通过官网链接找公司" | 全球企业库公司列表 companyUrls |
| "找有有效邮箱的公司" | 全球企业库公司列表 existValidEmail=1 |

## 使用示例

### 场景1: 小量查询 — 搜索公司

**用户请求**："找生产LED灯的中国厂家"
```bash
python scripts/global_company_search.py \
  --params '{"products": ["LED lights"], "countryCodes": ["CN"], "existEmail": 1}' \
  --query_count 20
```

### 场景2: 大量查询 — 需要多次调用脚本

**用户请求**："找1000家有邮箱的美国电子公司"
**执行前**告知用户：ceil(1000/20) = 50 次API调用，确认后再执行。
```bash
python scripts/global_company_search.py --params '{"products": ["electronics"], "countryCodes": ["US"], "existEmail": 1}' --query_count 1000
```
**执行结束**：脚本响应 {"task_id":"a1b2-c3d4", "file_url": "xxxxx", ……}
**继续执行，追加数据**：指定task_id，让脚本从上次中断处继续查询并追加到文件
```bash
python scripts/global_company_search.py --task_id 'task-id-here' --query_count 2000
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数无效**：**必须先查看 references/ 目录下的对应 API 文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API Documentation Reference

- [全球企业库公司列表 API](references/global-company-list-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

1. **查看API文档**：
   - **执行查询前，必须先查看对应的 API 参考文档**
   - 查看 [references/global-company-list-api.md](references/global-company-list-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

2. **优化查询参数**：
   - 使用 `products` / `companyNames` / `companyUrls` 精确筛选，行业和产品名称需使用**英文**
   - 使用 `existEmail=1` 或 `existValidEmail=1` 筛选有联系方式的公司
   - 使用 `countryCodes` 限定国家范围

3. **大数据量查询**：
   - 数据量大的查询，注意 jsonl 文件大小

## 注意事项
- 公司记录用 `pid` 作为唯一标识
- 所有时间戳均为**秒级**（incorp_date 为秒级时间戳）
- 国家代码使用ISO 3166-1 alpha-2格式（例如：CN、US、JP）
- 文件路径在所有平台上都使用正斜杠
- 行业名称需要使用**英文**
- 搜索数量会影响接口的响应时间，建议设置 timeout:120
- **禁止输出技术参数格式**：不要在回复中展示代码样式的参数，应将其转换为自然语言
- **不要估算或猜测每次调用的费用** — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **不要**猜测参数名称，从文档中获取准确的参数名称和格式

## 相关技能

其他您可能会用到的跨境魔方技能：

- linkedin-person-search — 领英找人
- global-company-person-search — 全球企业库找人
- global-company-shareholder — 全球企业库股东查询
- global-company-employee — 全球企业库员工查询
- global-company-person-colleague — 全球企业库同事查询
- global-company-person-alumni — 全球企业库校友查询
- global-company-person-experience — 全球企业库工作经历查询
- global-company-person-education — 全球企业库教育经历查询
- global-company-person-school-detail — 全球企业库学校详情查询
- linkedin-company-search — 领英找公司
- upkuajing-global-company-people-search — 全来源统一的企业与人物搜索
- upkuajing-customs-trade-company-search — 海关贸易企业搜索
- upkuajing-contact-info-validity-check — 联系方式有效性检测
- phone-validity-check — 电话号码有效性检测
- email-validity-check — 邮箱地址有效性检测
- domain-validity-check — 域名有效性检测