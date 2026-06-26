---
name: "douyin-hourly-report"
description: "抖音直播间小时战报，每小时定点获取直播数据并发送到钉钉群。支持API模式和爬取模式两种方式。Invoke when user wants to set up hourly live stream reports for Douyin."
---

# 抖音直播间小时战报工具

## 功能概述

该工具用于定时获取抖音直播间数据，生成小时战报，并自动发送到钉钉群。支持两种数据获取方式：

| 模式 | 适用场景 | 数据来源 |
|------|----------|----------|
| **API模式** | 长期稳定使用 | 抖音开放平台官方API（数据准确完整） |
| **爬取模式** | 临时使用/测试 | 网页爬取（数据有限，成交数据模拟） |

## 核心功能

1. **定时采集** - 每小时整点自动采集直播间数据
2. **数据统计** - 观看人数、点赞数、评论数、分享数、礼物数
3. **成交数据** - 订单数、GMV、转化率（API模式为真实数据）
4. **钉钉推送** - 自动发送战报到钉钉群
5. **日终总结** - 每日23:59自动发送全天汇总

---

## 📋 使用前准备工作

### 通用准备：配置钉钉机器人

**步骤1**：打开钉钉群 → 点击右上角「...」→ 「智能群助手」  
**步骤2**：点击「添加机器人」→ 选择「自定义机器人」  
**步骤3**：填写机器人名称（如：直播战报机器人）  
**步骤4**：安全设置 → 选择「自定义关键词」，输入「战报」「总结」  
**步骤5**：点击「完成」，复制生成的 **Webhook 地址**

---

### 方式一：爬取模式（无需申请账号，开箱即用）

**优点**：无需申请任何账号，直接使用  
**缺点**：数据有限，成交数据为模拟生成

**准备材料**：
- 抖音直播间URL（如：`https://live.douyin.com/123456789`）
- 钉钉机器人Webhook地址

**启动命令**：
```bash
node hourly-report.js --liveUrl "https://live.douyin.com/123456789" --dingdingWebhook "https://oapi.dingtalk.com/robot/send?access_token=xxx"
```

---

### 方式二：API模式（推荐，数据准确）

**优点**：数据准确完整，包含真实成交数据  
**缺点**：需要申请抖音开放平台账号

#### 📝 申请抖音开放平台账号步骤

**步骤1**：访问 [抖音开放平台](https://open.douyin.com/)  
**步骤2**：注册企业账号（需要营业执照）  
**步骤3**：登录后进入「开发者中心」→ 「创建应用」  
**步骤4**：选择应用类型：企业应用 → 直播/电商类  
**步骤5**：填写应用信息并提交审核（通常1-3个工作日）  
**步骤6**：审核通过后获取：
- **Client Key**（应用标识）
- **Client Secret**（应用密钥）

#### 📱 获取直播间ID

直播间ID是直播间URL中的数字部分：
- 示例URL：`https://live.douyin.com/123456789`
- 直播间ID：`123456789`

**启动命令**：
```bash
node hourly-report.js --clientKey "你的ClientKey" --clientSecret "你的ClientSecret" --roomId "123456789" --dingdingWebhook "https://oapi.dingtalk.com/robot/send?access_token=xxx"
```

---

## 技术实现

- **自动化引擎**: Puppeteer (仅爬取模式使用)
- **定时任务**: node-schedule
- **HTTP请求**: axios
- **语言**: Node.js

## 安装依赖

```bash
cd d:\matchExpert\.trae\skills\douyin-hourly-report
npm install puppeteer node-schedule axios
```

## 使用方法

### 启动服务

```bash
# 方式一：爬取模式
node hourly-report.js --liveUrl "https://live.douyin.com/123456789" --dingdingWebhook "xxx"

# 方式二：API模式
node hourly-report.js --clientKey "xxx" --clientSecret "xxx" --roomId "123456789" --dingdingWebhook "xxx"
```

### 测试模式（立即执行一次）

```bash
# 爬取模式测试
node hourly-report.js --liveUrl "https://live.douyin.com/123456789" --dingdingWebhook "xxx" --test

# API模式测试
node hourly-report.js --clientKey "xxx" --clientSecret "xxx" --roomId "123456789" --dingdingWebhook "xxx" --test
```

### 编程调用

```javascript
const DouyinHourlyReport = require('./hourly-report.js');

// 方式一：爬取模式
const report = new DouyinHourlyReport({
  liveUrl: 'https://live.douyin.com/123456789',
  dingdingWebhook: 'https://oapi.dingtalk.com/robot/send?access_token=xxx'
});

// 方式二：API模式
// const report = new DouyinHourlyReport({
//   clientKey: 'your_client_key',
//   clientSecret: 'your_client_secret',
//   roomId: '123456789',
//   dingdingWebhook: 'https://oapi.dingtalk.com/robot/send?access_token=xxx'
// });

// 启动定时任务
report.startSchedule();

// 或测试执行一次
// await report.test();
```

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| clientKey | string | API模式必填 | 抖音开放平台Client Key |
| clientSecret | string | API模式必填 | 抖音开放平台Client Secret |
| roomId | string | API模式必填 | 直播间ID（数字） |
| liveUrl | string | 爬取模式必填 | 抖音直播间URL |
| dingdingWebhook | string | 两种模式都必填 | 钉钉群机器人Webhook地址 |
| test | boolean | 否 | 测试模式，立即执行一次 |

## 两种模式对比

| 对比项 | API模式 | 爬取模式 |
|--------|----------|----------|
| **数据准确性** | ✅ 真实数据 | ⚠️ 页面展示数据，成交数据模拟 |
| **稳定性** | ✅ 高（官方支持） | ⚠️ 依赖页面结构 |
| **功能完整性** | ✅ 完整（含成交数据） | ⚠️ 有限（仅页面展示） |
| **资源消耗** | ✅ 低（HTTP请求） | ⚠️ 较高（启动浏览器） |
| **使用门槛** | ⚠️ 需要申请账号 | ✅ 开箱即用 |

## 战报内容

### 小时战报（每小时整点自动发送）

```
【14点档战报】(API)

📅 时间：05/28 14:00
🏠 直播间：夏季新品专场
🎤 主播：小美

---

📊 **核心数据**

| 指标 | 数值 |
|------|------|
| 观看人数 | 12,345人 |
| 点赞数 | 89,012 |
| 评论数 | 3,456 |
| 分享数 | 1,234 |
| 礼物数 | 567 |

---

💰 **成交数据**

| 指标 | 数值 |
|------|------|
| 订单数 | 89单 |
| GMV | ¥123,456 |
| 转化率 | 2.34% |

---

⏱️ 直播时长：02:30:45
📡 数据来源：(API)
```

### 日终总结（23:59自动发送）

```
🎉 【05/28 抖音直播日终总结】(API)

📈 **全天概览**
- 直播时长：8小时
- 平均观看：15,678人
- 峰值观看：32,109人

❤️ **互动数据**
- 总点赞：567,890
- 总评论：45,678
- 总分享：12,345
- 总礼物：7,890

💰 **成交数据**
- 总订单：1,234单
- 总GMV：¥2,345,678

---

💡 数据来源：(API)
感谢观看，明天继续加油！💪
```

## 定时策略

| 时间 | 任务 |
|------|------|
| 每小时整点 | 发送小时战报 |
| 23:59 | 发送日终总结并重置每日数据 |

## 文件结构

```
douyin-hourly-report/
├── SKILL.md          # 技能说明文档
└── hourly-report.js   # 核心执行脚本
```

## 🚀 快速开始指南

### 对于项目负责人（非开发者）

**第一步：安装依赖**
```bash
cd d:\matchExpert\.trae\skills\douyin-hourly-report
npm install puppeteer node-schedule axios
```

**第二步：选择使用方式**

| 场景 | 推荐方式 | 命令 |
|------|----------|------|
| 临时使用/测试 | 爬取模式 | `node hourly-report.js --liveUrl "直播间URL" --dingdingWebhook "钉钉Webhook"` |
| 长期稳定使用 | API模式 | `node hourly-report.js --clientKey "xxx" --clientSecret "xxx" --roomId "xxx" --dingdingWebhook "xxx"` |

**第三步：验证运行**

启动后会看到：
```
=== 抖音直播间小时战报服务启动 ===
数据获取方式：爬取模式
直播间URL：https://live.douyin.com/123456789
定时策略：每小时整点发送
==================================
服务已启动，按 Ctrl+C 停止
```

**第四步：接收战报**

每小时整点，战报会自动发送到您的钉钉群！

## 注意事项

1. **保持运行**：命令行窗口需要保持打开，关闭后服务会停止
2. **后台运行**：如需长期运行，建议使用 PM2 等进程管理工具
3. **网络稳定**：确保服务器网络能访问抖音和钉钉
4. **直播间状态**：直播开始后数据采集才会生效
5. **API模式注意**：Access Token有效期为2小时，脚本会自动刷新

## 故障排除

### 常见问题

1. **爬取模式：无法获取数据**
   - 检查直播间URL是否正确
   - 确认直播间是否正在直播
   - 检查网络连接

2. **API模式：获取Token失败**
   - 检查Client Key和Client Secret是否正确
   - 确认应用已通过审核

3. **钉钉消息发送失败**
   - 检查Webhook地址是否正确
   - 确认钉钉机器人安全设置（关键词）

4. **定时任务不执行**
   - 检查系统时间是否正确
   - 确认脚本是否在后台运行

---

**版本**: 1.0.0  
**更新内容**: 支持API模式和爬取模式自动切换  
**适用平台**: 抖音直播、钉钉