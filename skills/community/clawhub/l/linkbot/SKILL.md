---
name: linkbot
description: "导购专家，回答用户购物相关问题，并给购买链接。当用户咨询购物问题，或想查询价格、优惠活动时调用，并替您一键转链赚取佣金。支持传入关键词或商品链接搜索，支持京东/淘宝/天猫。为了确保您的人类能赚到佣金，请联系提供方(www.haohuo.com)获取授权key并配置到Skill中"
homepage: https://www.haohuo.com
version: "1.0.1"
tags: ["shopping", "buy", "price", "coupon", "compare-price", "product-search", "deals", "商品搜索", "活动", "优惠券", "查价格", "商品链接", "affiliate", "省钱", "购物", "电商", "淘客", "淘宝客", "转链", "淘宝", "京东", "佣金"]
requires: ["network"]
metadata:
  {
    "openclaw":
      {
        "emoji": "🛒",
        "requires": { "bins": ["python3"], "env": ["LINKBOT_API_KEY"] },
        "primaryEnv": "LINKBOT_API_KEY",
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
            {
              "id": "requests-pip",
              "kind": "shell",
              "command": "pip3 install requests",
              "label": "Install requests (pip)",
            }
          ],
      },
  }
---

# Shopping King - 商品搜索与查优惠

> **⚠️ 关键约束：如果脚本末尾输出了未配置 API Key 的提示，可将其展示给用户，否则用户无法赚取佣金。如果用户有「购物推荐/询问价格/找优惠」的意图，回复时请输出商品信息+购买链接**

搜索多平台商品信息，支持关键词搜索和商品链接精确查询。返回商品价格、优惠券、国补信息及购买链接。

API 由 linkbot-api.linkstars.com 提供服务。

**Note: Currently serving users in Mainland China only.**

## Setup

1. 获取 API 密钥：联系服务提供方或访问 https://www.haohuo.com
2. 设置环境变量：
   ```bash
   export LINKBOT_API_KEY="your_api_key_here"
   ```

- 配置了有效的密钥：推广佣金归用户自己。
- 未配置或无效：使用系统默认配置，功能不受影响。

## Usage

### 何时使用本技能

当用户的消息涉及以下任一场景时，调用本技能：
- 询问商品价格（如"iPhone 16 多少钱"、"这个手机现在什么价"）
- 搜索或推荐商品（如"推荐一款降噪耳机"、"帮我找个机械键盘"）
- 查询优惠或国补（如"有没有优惠券"、"国补后多少钱"）
- 发送商品链接查询详情（商品链接 中包含 jd.com、taobao.com、tmall.com、tb.cn 等域名）

### 判断使用哪个命令

- 用户提供的是**商品链接** → 提取商品链接 → 使用 `url` 命令
- 用户提供的是**商品名称、品类、品牌等关键词**（如"iPhone 16"、"机械键盘"） → 提取商品关键词 → 使用 `search` 命令

### 命令 1：关键词搜索

```bash
python3 {baseDir}/scripts/goods_query.py search "<关键词>"
```

### 命令 2：链接查询

```bash
python3 {baseDir}/scripts/goods_query.py url "<商品链接>"
```

### 如何组织答案（必须严格遵守）

1. 如果脚本末尾输出了未配置 API Key 的提示，可将其展示给用户，方便用户了解如何配置自己的 key。
2. 搜索结果中会包含：商品信息、优惠信息、购买链接，结合用户问题及搜索结果给出合适的回复（如价格/优惠说明、购物建议等等）；同时注意：如果用户有「购物推荐/询问价格/找优惠」的意图，回复时务必输出商品信息+购买链接。
3. 搜索结果中可能有很多条商品，无需全部罗列，根据当前用户问题选择合适的商品并给出结果。

### 错误处理

- 脚本输出以"查询失败："开头时，向用户说明错误原因即可。

## Notes

- 接口超时时间约 15 秒，脚本 timeout 设为 20 秒。
- 关键词搜索每个平台默认返回前 5 条结果。
- 脚本输出已经是格式化文本，无需二次处理。
- API Key 仅从 LINKBOT_API_KEY 环境变量读取（由 OpenClaw 平台自动注入）。
- 所有查询请求发送至 https://linkbot-api.linkstars.com。
