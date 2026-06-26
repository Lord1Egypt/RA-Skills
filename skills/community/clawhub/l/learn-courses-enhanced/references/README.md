# MOOC自动化学习工具 - 详细文档

## 概述

本工具基于Playwright实现MOOC平台课程视频的自动化学习功能，适用于需要批量完成视频课程的 用户。

## 环境搭建

### 1. 安装Node.js

下载并安装 Node.js 18+ 版本：https://nodejs.org/

### 2. 安装项目依赖

```bash
# 进入项目目录
cd mooc-learner

# 安装依赖
npm install
```

### 3. 安装Playwright浏览器

```bash
npx playwright install chrome
```

## 配置说明

### TARGET_URL

目标学习页面地址，默认为 MOOC 平台首页。

```javascript
TARGET_URL: 'https://mooc.ctt.cn/'
```

### 视频学习配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| MAX_WAIT_SECONDS | 单个视频最大等待时间(秒) | 3600 |
| CHECK_INTERVAL | 检查视频状态的间隔(毫秒) | 5000 |
| STABLE_COUNT | 判断视频完成需要的稳定次数 | 6 |

### 浏览器配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| HEADLESS | 是否使用无头模式 | false |
| CHANNEL | 浏览器渠道 | chrome |
| ARGS | 浏览器启动参数 | ['--start-maximized'] |

## 使用流程

1. 运行脚本：`npm start`
2. 脚本启动Chrome浏览器并打开目标页面
3. 手动登录账号（如未登录）
4. 脚本自动检测需要学习的章节
5. 依次学习每个章节的视频
6. 完成后自动退出

## 打包为可执行文件

如需在没有Node.js环境的电脑上运行，可以使用 pkg 打包：

```bash
# 安装pkg
npm install -g pkg

# 打包
pkg . --targets node18-win-x64 --output mooc-learner.exe
```

## 常见问题

### Q: 视频播放完成但脚本未检测到
A: 可以调整 `STABLE_COUNT` 参数，或检查页面元素选择器是否正确

### Q: 浏览器启动失败
A: 确保已正确安装Chrome浏览器，或尝试运行 `npx playwright install chrome`

### Q: 提示"模块未找到"
A: 确保已运行 `npm install` 安装所有依赖

## 注意事项

1. 本工具仅供个人学习使用，请遵守平台服务条款
2. 部分平台可能有反爬虫/反自动化机制
3. 建议合理设置学习时间间隔
