---
name: pinkr-crm
version: 1.0.0 
description: 品氪后台 API 调用工具，用于 AI 模型自动调用品氪 CRM 系统。所有接口均为 POST，参数通过 JSON 请求体传递，包含会员查询等常用接口。
required_env_vars:
  - PINKR_ADMIN_NAME
  - PINKR_PASSWORD
primary_credential:
  - PINKR_ADMIN_NAME
  - PINKR_PASSWORD
allowed-tools: Bash(python pinkr_crm.py:*), Read(config.json), Read(.env)
---

# 品氪 CRM API Skill

## 触发场景
- AI 模型需要调取品氪后台接口（包括会员相关功能等），通过 Python CLI 完成。
- 需要统一的登录、Token 管理、接口调用和错误处理能力。

## 功能说明

根据**用户问句**自动识别意图并调用对应接口，支持以下功能模块：

1. **会员管理**：查询会员列表、查询会员详情。


## 核心能力
- 登录认证：POST https://crm.pinkr.com/Crm/Business/getToken
- Token 管理：内存级缓存，单次运行期间有效
- API 调用：POST+JSON 请求体，Bearer Token 认证
- 错误处理：Token 失效自动重新登录，网络错误自动重试
- 输出：美化 JSON，便于 AI 模型解析

## 登录认证
- 地址：`https://crm.pinkr.com/Crm/Business/getToken`
- 方法：POST
- 参数：`admin_name`，`password`
- 返回：包含 `token` 的 JSON（如：`{"code": 200, "data": {"token": "xxx"}, "message": "success"}`）
- Token 有效期：1 天（内存缓存，单次运行有效）

## 数据请求格式

所有接口使用统一的 POST 表单方式提交：

- 路径：`Crm/Customer/GetCustomers`
- 完整 URL：`https://crm.pinkr.com/Crm/Customer/GetCustomers`
- 方法：POST
- 请求体：`{"phone": "13800138000"}`
- 响应示例：

## 公共响应参数

| 参数名 | 类型 | 说明 |
| :--- | :--- | :--- |
| code | string | 状态码 |
| message | string | 信息 |
| data | string | 数据 |

## 功能概览

| 接口名称 | 接口地址 | 说明 |
| --- | --- | --- | --- |
| 会员列表 | `Crm/Customer/GetCustomers` | 会员列表 |
| 会员详情 | `Crm/Customer/GetCustomer` | 会员详情，通过会员列表返回的 customer_id 访问 | 

## 接口说明

### 1. 会员列表

- **功能**：会员列表
- **接口名称**：`Crm/Customer/GetCustomers`
- **请求参数**：无
- **返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| phone | string | 手机号 |

### 1. 会员详情

- **功能**：会员详情
- **接口名称**：`Crm/Customer/GetCustomer`
- **请求参数**：无
- **返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| id | string | 会员 id |



## 使用方法
- 环境变量（推荐）
- PINKR_BASE_URL、PINKR_ADMIN_NAME、PINKR_PASSWORD

## 命令行接口概览
- login: 登录并缓存 Token 在内存
- api: 调用 API，需提供 --endpoint 与 --data
- clear-cache: 清除内存中的 Token
- test-connection: 测试登录与连接
- show-config: 显示当前配置
