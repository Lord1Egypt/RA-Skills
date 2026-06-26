# POWPOW Simple Skill

在 OpenClaw 中轻松创建和管理 POWPOW 数字人。

## 简介

**POWPOW Simple** 是一个 OpenClaw Skill，让你可以在 OpenClaw 聊天界面中完成 POWPOW 数字人的完整创建流程。

### 什么是 POWPOW？

POWPOW（泡泡世界）是一个虚实交融的次元空间，在这里你可以：
- 创造数字分身，你就是 Ta 的神
- 让数字人在地图上自由探索
- 与其他数字生命相遇
- 开启一段奇妙的旅程

## 功能特性

- ✅ **用户注册/登录** - 在 OpenClaw 中完成 POWPOW 账号注册
- ✅ **数字人创建** - 交互式流程，引导你创建专属数字人
- ✅ **头像上传** - 支持自定义数字人头像
- ✅ **位置选择** - 使用高德地图 API 搜索和选择位置
- ✅ **数字人管理** - 查看列表、续期管理
- ✅ **徽章系统** - 新用户获得 3 枚徽章，创建数字人消耗 2 枚，续期消耗 1 枚
- ✅ **用户反馈** - 遇到问题可直接提交反馈

## 安装

```bash
npm install powpow-simple
```

## 使用方法

### 1. 开始旅程

```
/powpow.start
```

跟随引导完成 POWPOW 之旅。

### 2. 注册账号

```
/powpow.register
用户名: your_username
密码: your_password
```

### 3. 登录账号

```
/powpow.login
用户名: your_username
密码: your_password
```

### 4. 创建数字人

```
/powpow.create
```

按照交互式提示：
1. 输入数字人名称
2. 输入描述（可选）
3. 上传头像（可选）
4. 选择位置

### 5. 查看数字人列表

```
/powpow.list
```

### 6. 续期数字人

```
/powpow.renew
digitalHumanId: 你的数字人ID
```

### 7. 搜索位置

```
/powpow.searchLocation
keyword: 北京故宫
```

### 8. 提交反馈

```
/powpow.feedback
message: 我遇到了一个问题...
contact: 你的联系方式（可选）
```

## 配置选项

在初始化 Skill 时可以传入配置：

```typescript
import { createSkill } from 'powpow-simple';

const skill = createSkill({
  powpowBaseUrl: 'https://global.powpow.online',  // POWPOW API 地址
  amapKey: '你的高德地图Key',                      // 高德地图 Web Service Key
  defaultAvatar: 'https://example.com/default.png', // 默认头像
  logLevel: 'INFO',                                // 日志级别: DEBUG, INFO, WARN, ERROR
});
```

## 徽章系统

- 🎁 **新用户奖励**：注册即获得 3 枚徽章
- ⭐ **创建数字人**：消耗 2 枚徽章
- 🔄 **续期数字人**：消耗 1 枚徽章（延长 30 天有效期）

## 日志和反馈

### 日志位置

日志文件保存在用户目录：
- Windows: `%USERPROFILE%\.powpow-simple\logs\skill.log`
- macOS/Linux: `~/.powpow-simple/logs/skill.log`

### 提交反馈

如果遇到问题，使用 `/powpow.feedback` 命令提交反馈。反馈信息会保存在：
- Windows: `%USERPROFILE%\.powpow-simple\feedback\`
- macOS/Linux: `~/.powpow-simple/feedback/`

## 查看你的数字人

创建成功后，访问以下链接在地图上查看你的数字人：

🗺️ **https://global.powpow.online/map**

## API 依赖

本 Skill 依赖以下服务：

1. **POWPOW API** - 用户注册、数字人管理
2. **高德地图 API** - 地理位置搜索

## 开发

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建
npm run build

# 运行测试
npm test

# 代码检查
npm run lint
```

## 项目结构

```
powpow-simple/
├── src/
│   └── index.ts          # 主入口文件
├── dist/                 # 编译输出
├── skill.json            # Skill 配置
├── package.json          # 包配置
└── README.md            # 本文档
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 作者

- **durenzidu** - 创建者和维护者

## 链接

- 🌐 POWPOW 官网: https://global.powpow.online
- 🗺️ POWPOW 地图: https://global.powpow.online/map
- 🐛 问题反馈: https://github.com/durenzidu/powpow-simple/issues
- 📦 NPM 包: https://www.npmjs.com/package/powpow-simple

## 更新日志

### v1.0.0 (2026-04-11)

- 🎉 初始版本发布
- ✅ 完整的数字人创建流程
- ✅ 用户注册和登录
- ✅ 头像上传和位置选择
- ✅ 徽章系统
- ✅ 用户反馈功能

---

**创造数字人，你就是 Ta 的神。**
