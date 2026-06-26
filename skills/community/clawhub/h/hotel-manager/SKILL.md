---
name: hotel-manager
description: 酒店管家 Skill - 管理酒店 OTA 基础信息、房价库存及订单同步。
env_vars:
  - OTA_CTRIP_API_KEY
  - OTA_CTRIP_SECRET
  - OTA_MEITUAN_API_KEY
  - OTA_MEITUAN_SECRET
  - INTERNAL_PMS_URL
  - INTERNAL_PMS_TOKEN
---

# Hotel Manager Skill

本 Skill 为酒店管理人员提供多平台（OTA）统一管理方案，支持 **API 自动化** 与 **浏览器自动化** 双模式。

> **[!IMPORTANT]**
> 本仓库目前提供的是 **集成架构模板**。在使用前，您需要根据特定平台的 API 文档完善 `scripts/ota_client.js` 中的协议细节。

## 安全与隐私 (Security)

为了保护您的 API 密钥，本 Skill 采用以下安全策略：
1. **环境变量优先**：强烈建议通过环境变量配置凭证。
2. **浏览器沙箱**：UI 自动化模式利用 Agent 已有的浏览器会话，不需本地存储明文密码。
3. **安全传输**：脚本强制使用 HTTPS 请求。

## 配置指南

### 方法 A: 环境变量 (推荐 API 模式)
设置 `OTA_CTRIP_API_KEY` 等变量。详细列表见上方元数据。

### 方法 B: UI 自动化模式 (无 API 时)
无需特殊 API 配置，Agent 将直接操作浏览器。参考 `scripts/browser_controller.js` 了解 SOP。

## 核心功能

1. **OTA 基础信息管理**：同步酒店描述、设施等。
2. **日常价库调整**：支持批量 API 更新及智能体 **直接改价（浏览器模拟）**。
3. **房态控制**：快速开关特定房型，支持跨平台同步。
4. **自动接单同步**：一键开启订单抓取并推送到内部系统。

## 操作模式

### 1. API 模式
高速执行，适用于大型酒店连锁。逻辑位于 `scripts/ota_client.js`。

### 2. 浏览器直接改价 (Visual Mode)
适用于无法获取 API 权限的小型客栈或特殊 OTA 平台。
- **Agent 执行逻辑**：打开对应的 OTA 后台网页 -> 自动定位改价区 -> 执行修改并截图存证。
- **详见**：`scripts/browser_controller.js`。

## 权限说明
- **网络访问**：访问 OTA 后台及内部 API。
- **浏览器权限**：需要读写及点击操作权限。

## 最佳实践
- **操作留痕**：UI 模式下建议 Agent 在每次改价后提供页面截图。
- **速率限制**：避免过快操作导致封禁，脚本预留了休眠策略。
