---
name: parcel-station-chat
description: "Build a courier station AI chat system with Express, GPT-5.5, local JSON DB, OCR, and WeChat-style frontend."
---

# 快递驿站智能客服系统

快速搭建快递驿站 AI 客服系统。Express 后端 + GPT-5.5 对话 + JSON 本地数据库 + 面单 OCR + 微信风格聊天前端。

## 系统架构

```
用户 (微信小程序/浏览器)
        │
   POST /api/chat
   POST /api/ocr
   GET  /api/packages/:code
        │
┌───────▼──────────────────────┐
│  Express server.js (v3.1)    │
│  ├ loadApiConfig() → SU2     │
│  ├ buildLookupBlock()        │
│  │  ├ extractPickupCode()    │
│  │  └ extractTrackingTail()  │
│  ├ callAI() → GPT-5.5       │
│  └ handleFallback()          │
├──────────────────────────────┤
│  db.js (JSON 文件存储)        │
│  ├ findByPickupCode()        │
│  ├ findByTrackingTail()      │
│  ├ findByPhoneTail()         │
│  ├ listPackages() (分页)     │
│  └ insertPackage()           │
├──────────────────────────────┤
│  ocr.js (GPT-5.5 Vision)    │
│  └ recognizeWaybill()        │
└──────────────────────────────┘
```

## 取件码格式

```
1-2-25001
│ │ ││││
│ │ │││└── 001 = 当天第1个包裹
│ │ ││└─── 25 = 日期(当月第几天)
│ │ └┴──── 5位日期序号(DDNNN)
│ └────── 排号
└──────── 货架号
```

正则：`/(\d{1,2})\s*[-－—–]\s*(\d{1,2})\s*[-－—–]\s*(\d{5})/`

## 搭建步骤

### 1. 初始化项目

```powershell
mkdir parcel-help && cd parcel-help
npm init -y
npm install express
```

### 2. 创建 db.js

JSON 文件存储，零原生依赖。关键函数：
- `findByPickupCode(code)` — 取件码查询
- `findByTrackingTail(tail)` — 运单号后5位查询
- `findByPhoneTail(tail)` — 手机尾号4位查询
- `listPackages({page, pageSize, q})` — 分页+搜索
- `insertPackage(p)` — 新增包裹（含冲突检测）

种子数据：12条包裹覆盖全部货架，当天日期自动计算。

### 3. 创建 ocr.js

调用 GPT-5.5 Vision 识别面单，返回 JSON：
```json
{"pickup_code":"","tracking_no":"","recipient_name":"","recipient_phone_tail":"","carrier":"","confidence":"low|medium|high"}
```

注意：AI 可能返回 markdown 包裹的 JSON，parseOcrJson 需处理 ` ```json ``` `。

### 4. 创建 server.js

核心逻辑流程：
1. `loadApiConfig()` → 读 SU2_API_KEY + baseUrl
2. `buildLookupBlock(message)` → 自动识别取件码/运单号尾号
3. 有 AI → `callAI()` → 带会话历史 + 查库结果
4. 无 AI → `handleFallback()` → 本地关键词+查库

会话管理：30分钟 TTL，保留最近5轮对话。

### 5. 创建前端 (public/index.html)

微信风格聊天界面，注意：
- ❌ 不加入"管理"入口（客户端）
- ✅ 底部快捷按钮：找不到包裹 / 取件码说明 / 运单号查询
- ✅ 支持图片上传拍照
- ✅ 移动端优化

### 6. 启动测试

```powershell
node server.js
# 聊天界面: http://localhost:3000
# 管理后台: http://localhost:3000/admin.html
# 健康检查: http://localhost:3000/api/health
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查（版本、AI状态、数据库总量） |
| POST | `/api/chat` | 聊天（message + image + sessionId） |
| POST | `/api/ocr` | 面单识别（image） |
| GET | `/api/packages` | 包裹列表（page, pageSize, q） |
| POST | `/api/packages` | 录入包裹 |
| GET | `/api/packages/:code` | 按取件码查询 |

## 核心设计决策

1. **不用 better-sqlite3** — Windows 需要 VC++ 编译工具，改用纯 JS JSON 文件存储
2. **不用 shelf_color/shelf_area** — 真实驿站用"第X号货架 第Y排"，不设颜色/区号
3. **取件码正则匹配 5 位日期序号** — 区别于其他数字输入
4. **运单号查询** — 匹配 5 位及以上连续数字，支持部分单号
5. **管理后台单独存在** — 不和客户端 UI 混在一起

## 坑与注意事项

- `better-sqlite3` 在 Windows 编译失败 → 换 JSON
- Unicode 中文在 `taskkill /F /IM node.exe` 后可能输出乱码，但服务正常
- API 调用超时默认 30s，中转站偶尔延迟需重试
- `curl.exe` 在 PowerShell 中 JSON 引号会转义出错 → 用 `Invoke-RestMethod`
