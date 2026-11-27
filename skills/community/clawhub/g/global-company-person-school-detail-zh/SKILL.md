---
name: global-company-person-school-detail-zh
description: 依托全球企业数据库调取人员对应的院校详细资料，获取完整教育档案，梳理目标人员就读院校及整体教育背景，辅助开展客户尽调与人脉分析。
metadata: {"version":"1.0.4","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🏫","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 全球学校详情查询

使用跨境魔方开放平台API从全球企业库数据查询学校的详细信息。

## 概述

本技能提供对跨境魔方全球企业库学校详情信息的查询。通过学校ID（sid）获取学校的名称、类型、所在地、网址、社交媒体链接等信息。此为单条记录查询，无需翻页。

- `sid`（学校ID）可从 **global-company-person-education**（教育经历查询）结果中获取

## 脚本运行

### 环境准备

1. **检查 Python**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要**：始终使用直接脚本调用，如 `python scripts/school_detail.py`。**不要使用** shell 复合命令如 `cd scripts && python school_detail.py`

### 学校详情查询 (`school_detail.py`)
- **返回粒度**：所有学校详情一次性返回
- **适用场景**：根据学校ID查询学校名称、位置、网址和社交媒体信息
- **示例**：
  - "查询S_001学校的详细信息"
  - "查询学校ID aue1fd986ee5cb5d906f9d36286714ed33的学校信息"
- **参数**：查看参数说明 [学校详情 API](references/school-detail-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/search/depth_company/person/school/detail","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"学校详情查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**所有API调用都会产生费用**，不同接口计费方式不同。

**最新价格**：用户可访问 [详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或者使用：`python scripts/auth.py --price_info`（返回接口完整定价）

### 查询计费规则

按**调用次数**计费，每次查询返回完整的学校详情：
- 每次API调用产生一次费用
- 无需翻页，所有数据一次性返回
- **执行前必须：**
  1. 告知用户本次查询会产生费用
  2. 停止，等待用户在独立消息中明确确认后，再执行脚本

### 费用确认原则

**任何会产生费用的操作，都必须先告知、等待用户明确确认，不得在告知的同一条消息中直接执行。**

### 套餐计费与余额降级

搜索/海关/地图接口**默认走套餐**：脚本会自动携带 `"planMode": 2`。

- **套餐不可用**（无有效套餐或额度已用完）：脚本在业务执行前停止，不会产生扣费；stdout 会输出一行以 `PLAN_UNAVAILABLE ` 开头的 JSON，退出码为 **3**。**禁止自动重试**。
- **先询问用户**：用自然语言说明原因（无套餐 / 额度用完及恢复时间），说明改用余额将按接口定价扣费（单价用 `python scripts/auth.py --price_info` 查询），然后等待用户在独立消息中明确回复。
- **用户同意**：用同一条命令加环境变量 `UPKUAJING_PLAN_MODE=1` 重跑（PowerShell：`$env:UPKUAJING_PLAN_MODE='1'`），成功后向用户展示 `fee` 扣费信息。
- **用户拒绝**：本次不执行、不扣费；给出「稍后重试 / 升级套餐 / 使用余额」三个出口，同一轮不要重复弹窗。
- **改余额后仍余额不足**（95）：提示充值并停止，不再重试。
- **批量调用前**：先用 `python scripts/auth.py --plan_quota` 预检额度（档位上限用 `--plan_config`）；`available=0` 或目标窗口 `remaining=0` 时，直接先问是否用余额，避免必然失败的调用。
- **调用成功**：把 stderr 中 `[套餐]` 开头的用量信息转述给用户。
- **禁止**静默改走余额，**禁止**向用户暴露内部错误码原文。

完整契约见 [references/plan-billing.md](references/plan-billing.md)

## 工作流程

### 决策指南

| 用户意图 | 使用API |
|---------|--------|
| "查询S_001学校的详细信息" | 学校详情查询 |

## 使用示例

### 查询学校详情

**用户请求**："查询S_001学校的详细信息"
```bash
python scripts/school_detail.py --sid S_001
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **套餐不可用（退出码 3 / `PLAN_UNAVAILABLE`）**：说明原因并询问是否改用余额，不要自动重试；参见 [套餐计费与余额降级](references/plan-billing.md)
- **参数无效**：**必须先查看 references/ 目录下的对应 API 文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API Documentation Reference

- 学校详情：查看 [references/school-detail-api.md](references/school-detail-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)
- 套餐计费与余额降级：[references/plan-billing.md](references/plan-billing.md)

## 最佳实践

1. **查看API文档**：
   - **执行查询前，必须先查看对应的 API 参考文档**
   - 查看 [references/school-detail-api.md](references/school-detail-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

2. **跨技能使用**：
   - 学校ID（`sid`）可从 **global-company-person-education** 或 **global-company-person-alumni** 查询结果中获取

## 注意事项
- 学校详情一次性返回完整信息，无需翻页
- 学校ID（`sid`）可从教育经历记录（global-company-person-education）或校友记录（global-company-person-alumni）中获得
- 文件路径在所有平台上都使用正斜杠
- **禁止输出技术参数格式**：不要在回复中展示代码样式的参数，应将其转换为自然语言
- **不要估算或猜测每次调用的费用** — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **不要**猜测参数名称，从文档中获取准确的参数名称和格式

## 相关技能

其他您可能会用到的跨境魔方技能：

- global-company-search — 全球企业库找公司
- global-company-person-search — 全球企业库找人
- global-company-shareholder — 全球企业库股东查询
- global-company-employee — 全球企业库员工查询
- global-company-person-colleague — 全球企业库同事查询
- global-company-person-alumni — 全球企业库校友查询
- global-company-person-experience — 全球企业库工作经历查询
- global-company-person-education — 全球企业库教育经历查询
- linkedin-person-search — 领英找人
- linkedin-company-search — 领英找公司
- upkuajing-global-company-people-search — 全来源统一的企业与人物搜索
- upkuajing-customs-trade-company-search — 海关贸易企业搜索
- upkuajing-contact-info-validity-check — 联系方式有效性检测
- phone-validity-check — 电话号码有效性检测
- email-validity-check — 邮箱地址有效性检测
- domain-validity-check — 域名有效性检测