---
name: paid-content-generator
description: AI内容生成器 - 小红书文案、视频脚本、多平台内容一键生成。接入SkillPay收费，每次调用0.001 USDT。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SKILLPAY_API_KEY
---

# Paid Content Generator

付费版AI内容生成器，支持：
- 小红书文案生成
- B站/抖音视频脚本
- 公众号文章
- 多平台内容适配

## 收费模式

每次调用 0.001 USDT（约0.007元人民币）

## 使用方法

```bash
# 小红书文案
node scripts/generate.js xiaohongshu "布偶猫"

# 视频脚本
node scripts/generate.js video "AI工具测评"

# 公众号文章
node scripts/generate.js article "如何选择AI工具"
```

## SkillPay 配置

需要在环境变量中配置：
- `SKILLPAY_API_KEY` - 你的SkillPay API密钥

## API说明

调用前会自动扣费：
- 扣费成功 → 执行生成
- 余额不足 → 返回充值链接
