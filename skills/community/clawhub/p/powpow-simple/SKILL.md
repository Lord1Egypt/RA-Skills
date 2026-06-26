---
name: powpow-simple
slug: powpow-simple
version: 1.0.0
description: POWPOW 简化版 - 在 OpenClaw 中轻松创建和管理 POWPOW 数字人。支持用户注册、数字人创建、位置选择和徽章管理。
author: durenzidu
license: MIT
keywords:
  - openclaw
  - skill
  - powpow
  - digital-human
  - map
  - creation
  - avatar
  - badge
repository:
  type: git
  url: https://github.com/durenzidu/powpow-simple.git
main: dist/index.js
types: dist/index.d.ts
engines:
  node: ">=18.0.0"
config:
  powpowBaseUrl:
    type: string
    required: false
    description: POWPOW API 基础 URL
    default: https://global.powpow.online
  amapKey:
    type: string
    required: false
    description: 高德地图 Web Service Key（用于地理位置查询）
    default: 8477cbc2bfd4288ac09582f583f33cca
  defaultAvatar:
    type: string
    required: false
    description: 默认头像 URL
    default: https://global.powpow.online/logo.png
commands:
  - name: powpow.start
    description: 开始 POWPOW 旅程 - 故事化引导流程
  - name: powpow.register
    description: 注册 POWPOW 账号
    parameters:
      username:
        type: string
        required: true
        description: 用户名（2-50个字符）
      password:
        type: string
        required: true
        description: 密码（至少6位）
  - name: powpow.login
    description: 登录 POWPOW 账号
    parameters:
      username:
        type: string
        required: true
        description: 用户名
      password:
        type: string
        required: true
        description: 密码
  - name: powpow.logout
    description: 退出登录
  - name: powpow.status
    description: 查看当前登录状态
  - name: powpow.create
    description: 创建数字人（交互式流程）
  - name: powpow.create.submit
    description: 提交创建数字人
    parameters:
      name:
        type: string
        required: true
        description: 数字人名称
      description:
        type: string
        required: false
        description: 数字人描述
      avatarUrl:
        type: string
        required: false
        description: 头像URL
      lat:
        type: number
        required: true
        description: 纬度
      lng:
        type: number
        required: true
        description: 经度
      locationName:
        type: string
        required: false
        description: 位置名称
  - name: powpow.list
    description: 查看我的数字人列表
  - name: powpow.renew
    description: 续期数字人
    parameters:
      digitalHumanId:
        type: string
        required: true
        description: 数字人 ID
  - name: powpow.uploadAvatar
    description: 上传头像
    parameters:
      filePath:
        type: string
        required: true
        description: 图片文件路径
  - name: powpow.searchLocation
    description: 搜索地理位置（使用高德地图）
    parameters:
      keyword:
        type: string
        required: true
        description: 地点关键词
  - name: powpow.feedback
    description: 提交反馈或报告问题
    parameters:
      message:
        type: string
        required: true
        description: 反馈内容
      contact:
        type: string
        required: false
        description: 联系方式（可选，用于回复）
---

# POWPOW Simple Skill

在 OpenClaw 中轻松创建和管理 POWPOW 数字人。

## 简介

**POWPOW Simple** 让你可以在 OpenClaw 聊天界面中完成 POWPOW 数字人的完整创建流程。

### 什么是 POWPOW？

POWPOW（泡泡世界）是一个虚实交融的次元空间，在这里你可以：
- 创造数字分身，你就是 Ta 的神
- 让数字人在地图上自由探索
- 与其他数字生命相遇
- 开启一段奇妙的旅程

## 使用方法

### 开始旅程

```
/powpow.start
```

跟随引导完成 POWPOW 之旅。

### 注册账号

```
/powpow.register
用户名: your_username
密码: your_password
```

### 登录账号

```
/powpow.login
用户名: your_username
密码: your_password
```

### 创建数字人

```
/powpow.create
```

按照交互式提示：
1. 输入数字人名称
2. 输入描述（可选）
3. 上传头像（可选）
4. 选择位置

### 查看数字人列表

```
/powpow.list
```

### 续期数字人

```
/powpow.renew
digitalHumanId: 你的数字人ID
```

### 搜索位置

```
/powpow.searchLocation
keyword: 北京故宫
```

### 提交反馈

```
/powpow.feedback
message: 我遇到了一个问题...
contact: 你的联系方式（可选）
```

## 徽章系统

- 🎁 **新用户奖励**：注册即获得 3 枚徽章
- ⭐ **创建数字人**：消耗 2 枚徽章
- 🔄 **续期数字人**：消耗 1 枚徽章（延长 30 天有效期）

## 查看你的数字人

创建成功后，访问以下链接在地图上查看你的数字人：

🗺️ **https://global.powpow.online/map**

## 配置

在初始化 Skill 时可以传入配置：

```typescript
{
  powpowBaseUrl: 'https://global.powpow.online',  // POWPOW API 地址
  amapKey: '你的高德地图Key',                      // 高德地图 Web Service Key
  defaultAvatar: 'https://example.com/default.png', // 默认头像
}
```

## 依赖

- **POWPOW API** - 用户注册、数字人管理
- **高德地图 API** - 地理位置搜索

## 作者

- **durenzidu** - 创建者和维护者

## 链接

- 🌐 POWPOW 官网: https://global.powpow.online
- 🗺️ POWPOW 地图: https://global.powpow.online/map
- 🐛 问题反馈: https://github.com/durenzidu/powpow-simple/issues

---

**创造数字人，你就是 Ta 的神。**
