# Kie AI Nano Banana Pro 生图

> Google Nano Banana Pro 模型官方生图助手

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.ai/skills/kie-nano-banana-pro)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 Skill 定位

**Kie AI Nano Banana Pro 官方生图助手** —— 通过 Kie AI API 调用 Google Nano Banana Pro 模型，生成高质量、多比例、多分辨率的专业图像

**官方文档：** https://docs.kie.ai/market/google/pro-image-to-image

---

## ⚡ 快速开始

### 安装

```bash
clawhub install kie-nano-banana-pro
```

### 配置 API Key

1. 访问 https://kie.ai/api-key 获取 API Key
2. 在 Skill 配置中添加 API Key
3. 开始生成图像

### 使用示例

**基础生成：**
```
帮我生成一个香蕉英雄的漫画海报，1:1 比例
```

**多图参考：**
```
用这 3 张参考图生成新图像，16:9 宽屏，4K 分辨率
```

**生产环境：**
```
批量生成产品图，回调到 https://api.myshop.com/callback
```

---

## 🏗️ 核心能力

### 1. API 集成
- ✅ Kie AI API 完整集成
- ✅ Bearer Token 认证
- ✅ 自动错误处理
- ✅ 任务状态查询

### 2. 参数支持
- ✅ 10 种画幅比例（1:1 / 9:16 / 16:9 / 21:9 等）
- ✅ 3 种分辨率（1K / 2K / 4K）
- ✅ 2 种输出格式（png / jpg）
- ✅ 最多 8 张参考图

### 3. 回调支持
- ✅ Webhook 回调配置
- ✅ 自动状态通知
- ✅ 签名验证

### 4. 提示词优化
- ✅ 智能提示词生成
- ✅ 模板库支持
- ✅ 参数自动补全

---

## 📊 API 参数

### 请求参数

```json
{
  "model": "nano-banana-pro",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "图像描述（最长 10000 字符）",
    "image_input": [],
    "aspect_ratio": "1:1",
    "resolution": "1K",
    "output_format": "png"
  }
}
```

### 画幅比例

| 比例 | 适用场景 |
|------|----------|
| `1:1` | 头像、产品主图 |
| `9:16` | 抖音、视频号 |
| `16:9` | B 站、YouTube |
| `21:9` | 电影宽屏 |
| `3:4` | 小红书 |

### 分辨率

| 分辨率 | 适用场景 |
|--------|----------|
| `1K` | 快速测试、社交媒体 |
| `2K` | 正式输出、商业使用 |
| `4K` | 高质量印刷、大幅海报 |

---

## 🔧 错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 200 | 成功 | - |
| 401 | 未授权 | 检查 API Key |
| 402 | 余额不足 | 充值账户 |
| 422 | 参数验证失败 | 检查参数格式 |
| 429 | 请求频率超限 | 等待后重试 |
| 500 | 服务器错误 | 联系技术支持 |

---

## 📝 使用场景

### 电商产品图
- 产品主图生成
- 多比例适配（1:1 / 3:4 / 9:16）
- 批量生成

### 社交媒体
- 抖音/快手封面（9:16）
- 小红书笔记（3:4）
- B 站视频封面（16:9）

### 创意设计
- 漫画海报
- 艺术创作
- 概念设计

### 专业摄影
- 风景摄影
- 人像写真
- 商业摄影

---

## 🚀 版本记录

### v1.0.0 (2026-04-03)
- ✅ 初始版本发布
- ✅ Kie AI API 完整集成
- ✅ 10 种画幅比例支持
- ✅ 3 种分辨率支持
- ✅ 回调功能支持

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **ClawHub 页面：** https://clawhub.ai/skills/kie-nano-banana-pro
- **GitHub 仓库：** https://github.com/rfdiosuao/openclaw-skills/tree/main/kie-nano-banana-pro
- **官方文档：** https://docs.kie.ai/market/google/pro-image-to-image
- **API Key 管理：** https://kie.ai/api-key

---

**Kie AI Nano Banana Pro 生图 · 让每一张图都专业**
