------WebKitFormBoundary1zqzz62iqpu
Content-Disposition: form-data; name="file"; filename="README.md"
Content-Type: text/markdown

# liufeng-greeting-skill

柳峰专属的个性化问候技能，为OpenClaw AI助手定制。

## 🎯 功能概述

当你在任何OpenClaw支持的聊天渠道（WebChat、飞书、企业微信等）中发送问候消息时，这个技能会自动回复个性化的问候语，并显示当前的日期和时间。

## ✨ 特色功能

- **智能识别**：自动识别多种问候语变体（中文、英文、混合）
- **个性化回复**：针对柳峰定制的回复风格
- **时间显示**：自动显示中国标准时间
- **随机回复**：每次回复使用不同的问候语，避免单调
- **简单集成**：无需复杂配置，开箱即用

## 📋 触发关键词

发送以下任意关键词即可触发：

| 关键词 | 说明 |
|--------|------|
| 你好 | 标准中文问候 |
| hello | 英文问候 |
| 嗨 | 轻松问候 |
| 在吗 | 中文常用问候 |
| hi | 简短英文问候 |
| 早上好 | 早晨问候 |
| 下午好 | 下午问候 |
| 晚上好 | 晚上问候 |

**注意**：不区分大小写，可以包含其他文字（如"你好，我想问个问题"也会触发）

## 📝 回复格式

```
[个性化问候语]

当前时间：[YYYY-MM-DD HH:mm:ss]
时区：Asia/Shanghai (中国标准时间)
```

## 🚀 快速开始

### 1. 技能已自动安装
技能已创建在：`C:\Users\liufeng\.openclaw\workspace\skills\liufeng-greeting-skill`

### 2. 立即使用
在任意OpenClaw聊天渠道中发送：
- "你好"
- "Hello"
- "嗨"
- "在吗"

### 3. 示例对话

**你**: 你好  
**大白**: 柳峰，你好！🌄 大白在这里随时为你服务。  
当前时间：2026-03-11 00:10:25  
时区：Asia/Shanghai (中国标准时间)

**你**: Hello, 在吗？  
**大白**: 嗨，柳峰！很高兴见到你。  
当前时间：2026-03-11 00:11:30  
时区：Asia/Shanghai (中国标准时间)

## 🔧 自定义配置

如需修改技能行为，可以编辑以下文件：

### 修改问候语
编辑 `greeting.js` 中的 `GREETING_TEMPLATES` 数组：
```javascript
const GREETING_TEMPLATES = [
  "你的自定义问候语1",
  "你的自定义问候语2",
  // ... 添加更多
];
```

### 添加触发关键词
编辑 `greeting.js` 中的 `GREETING_KEYWORDS` 数组：
```javascript
const GREETING_KEYWORDS = [
  '你好', 'hello', '嗨', '在吗', 'hi',
  // ... 添加更多关键词
];
```

## 🧪 测试技能

运行测试脚本验证功能：
```bash
cd "C:\Users\liufeng\.openclaw\workspace\skills\liufeng-greeting-skill"
node test.js
```

## 📁 文件结构

```
liufeng-greeting-skill/
├── SKILL.md          # 技能元数据
├── greeting.js       # 核心逻辑
├── package.json      # 配置信息
├── test.js          # 测试脚本
└── README.md        # 本文档
```

## 🔄 更新日志

### v1.0.0 (2026-03-11)
- 初始版本发布
- 支持8种问候关键词
- 5种随机问候语模板
- 完整的中国时区时间显示
- 100%测试通过率

## 📞 支持

如有问题或建议，请通过OpenClaw联系大白。

---

**技能作者**: 大白 (柳峰的AI助手)  
**创建时间**: 2026年3月11日  
**最后更新**: 2026年3月11日
------WebKitFormBoundary1zqzz62iqpu--
