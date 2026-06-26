---
name: pms-worklog
description: 自动填写 PingCode/PMS 系统工时记录。支持批量填写多天的工时，自动登录、选择事项类型、填写事项、工时、日期和说明。
read_when:
  - 需要填写 PMS 工时记录
  - 需要批量填写多天的工时
  - 需要在 PingCode 系统中登记工时
metadata:
  clawdbot:
    emoji: ⏱️
    requires:
      bins: [node, npm]
      npm: [playwright]
---

# PMS 工时自动填写技能

## 功能

自动在 PingCode/PMS 系统中填写工时记录，支持：
- 自动登录
- 选择事项类型（工作项）
- 填写事项编号并选择匹配项
- 填写工时、日期、说明
- 批量填写多天的工时

## 前置条件

1. 安装 Playwright：
```bash
npm install -g playwright
playwright install chromium
```

2. 确保系统已安装 Google Chrome

## 使用方法

### 方式 1：直接运行脚本

```bash
NODE_PATH=/Users/aispeech/.npm-global/lib/node_modules node ~/.openclaw/workspace/skills/pms-worklog/scripts/fill_worklog.js
```

### 方式 2：通过 OpenClaw 调用

```
exec: node ~/.openclaw/workspace/skills/pms-worklog/scripts/fill_worklog.js
```

## 配置

编辑脚本中的配置区域：

```javascript
// ===== 配置区域 =====
const username = 'your_username@company.com';  // 你的 PMS 账号
const password = 'your_password';              // 你的 PMS 密码

const dates = ['2026-03-09', '2026-03-10', '2026-03-11'];  // 填写日期

const workItem = 'IOTxxxxxx-xxxx';  // 事项编号
const hours = '8';                       // 每天工时
const description = '工作内容说明';       // 工作说明

const pmsUrl = 'https://pms.aispeech.com.cn/workspace/workload/insight';
const screenshotDir = '/Users/aispeech/.openclaw/workspace';
// ===================
```

### 使用环境变量（推荐）

也可以将敏感信息放在环境变量中：

```bash
export PMS_USERNAME="your_username@company.com"
export PMS_PASSWORD="your_password"
```

然后在脚本中使用：
```javascript
const username = process.env.PMS_USERNAME || 'default_user';
const password = process.env.PMS_PASSWORD || 'default_pass';
```

## 输出

脚本运行后会：
- 在终端显示填写进度
- 保存截图到配置的 `screenshotDir/pms_png` 目录：
  - `day1_filled.png` - 填写完成截图
  - `day1_done.png` - 提交成功截图
  - `day1_error.png` - 提交失败截图（如有）

## 注意事项

1. **事项类型必须先选择**：必须先选择"工作项"类型，再填写事项编号
2. **下拉列表需要等待**：填写事项后需要等待 3 秒让下拉列表刷新
3. **必须点击选项**：不能按回车确认，必须点击下拉列表中的选项
4. **网络要求**：需要能访问 PMS 系统

## 故障排除

### 浏览器启动失败
```bash
# 确保 Chrome 已安装
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# 重新安装 Playwright
npm install -g playwright
playwright install chromium
```

### 事项无法选择
- 检查事项类型是否已选择为"工作项"
- 增加等待时间（将 `waitForTimeout(3000)` 改为更长时间）
- 检查事项编号是否正确

### 表单提交失败
- 检查所有必填字段是否已填写
- 查看 `day*_error.png` 截图确认错误信息

### 登录失败
- 检查账号密码是否正确
- 检查网络连接
- 确认 PMS 系统可访问
