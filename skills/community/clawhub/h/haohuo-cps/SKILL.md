---
name: haohuo-cps
description: "电商 CPS 助手，面向 CPS 推广者的电商选品与转链工具。支持商品链接转链、淘口令/短链解析、佣金率查询、关键词选品比价。目前支持京东/淘宝/天猫平台。请联系服务提供方(www.haohuo.com)获取授权 key 并配置到 Skill 中"
homepage: https://www.haohuo.com
version: "1.0.7"
tags: ["CPS", "推广", "佣金率", "转链", "淘口令", "短链解析", "shopping", "buy", "price", "coupon", "compare-price", "product-search", "deals", "商品搜索", "活动", "优惠券", "查价格", "商品链接", "affiliate", "省钱", "购物", "电商", "淘客", "淘宝客", "淘宝", "京东", "佣金"]
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

#  电商 CPS 助手
> 由「星罗好货」**https://www.haohuo.com** 提供

**⚠️ 关键约束：如果脚本末尾输出了未配置 API Key 的提示，必须展示给用户，否则佣金无法归属到用户账户。脚本输出中的佣金率信息必须展示给用户。如果用户有「购物推荐/询问价格/找优惠/转链/查佣金」的意图，回复时请输出商品信息+推广链接+佣金率**

面向 CPS 推广者的电商选品与转链工具。支持关键词选品比价、商品链接 CPS 转链、淘口令/短链解析、佣金率查询。返回商品价格、优惠券、国补信息、CPS 佣金率及推广链接。目前仅支持**京东**和**淘宝/天猫**平台。

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
- 发送商品链接查询详情（商品链接中包含 jd.com、taobao.com、tmall.com、tb.cn 等域名）
- 想对商品链接做 CPS 转链（如"帮我转链这个商品"、"生成推广链接"）
- 查询某商品的 CPS 佣金/佣金率（如"这个商品佣金多少"、"佣金率是多少"）
- 解析淘宝口令或短链（如"解析这个淘口令"、用户消息中包含 `￥...￥` / `$...$` / `₤...₤` 格式的淘口令文本，或包含 tb.cn 等短链）

### 判断使用哪个命令

- 用户提供的是**商品链接** → 提取商品链接 → 使用 `url` 命令
- 用户提供的是**淘宝口令** → 提取口令字符串 → 使用 `url` 命令（参见下方淘口令提取规则）
- 用户想要**转链、查佣金、解析短链/口令** → 提取链接或口令 → 使用 `url` 命令
- 用户提供的是**商品名称、品类、品牌等关键词**（如"iPhone 16"、"机械键盘"） → 提取商品关键词 → 使用 `search` 命令

### 淘口令提取规则

用户消息中可能包含淘宝口令，需从中提取目标字符串后作为 `url` 命令的参数传入。常见淘口令格式（提取符号之间的内容）：
- `￥xxxxxxxx￥`
- `$xxxxxxxx$`
- `₤xxxxxxxx₤`
- `【xxxxxxxx】`（部分变体）

提取出中间的字符串（如 `xxxxxxxx`），直接作为 `url` 命令的参数：

```bash
python3 {baseDir}/scripts/goods_query.py url "<提取出的口令字符串>"
```

### 命令 1：关键词搜索

```bash
python3 {baseDir}/scripts/goods_query.py search "<关键词>"
```

### 命令 2：链接/口令查询

```bash
python3 {baseDir}/scripts/goods_query.py url "<商品链接或淘口令字符串>"
```

### 如何组织答案（必须严格遵守）

1. 如果脚本末尾输出了未配置 API Key 的提示，可将其展示给用户，方便用户了解如何配置自己的 key。
2. 搜索结果中会包含：商品信息、优惠信息、CPS 佣金率、推广链接（CPS 链接），结合用户问题及搜索结果给出合适的回复（如价格/优惠说明、佣金率高低评价、推广价值判断等）。
3. 同时注意：如果用户有「购物推荐/询问价格/找优惠/转链/查佣金」的意图，回复时务必输出商品信息+推广链接+佣金率。
3. 搜索结果中可能有很多条商品，如果用户有推荐意图，无需全部罗列，根据当前用户问题选择合适的商品并给出结果。
4. 每条商品信息按以下格式输出（从脚本输出中提取对应字段）：

```
商品名称
**商品链接**：<根据商品ID拼接，见下方规则>
**到手**：￥xxx（优惠明细：淘礼金、淘金币、优惠券等）
**佣金率**：xx%
**推广链接**：<脚本输出中的CPS链接>
```

商品链接根据平台和商品 ID 拼接：
- 淘宝/天猫：`https://uland.taobao.com/item/edetail?id=<商品ID>`
- 京东：`https://jingfen.jd.com/detail/<商品ID>.html`

示例：

```
斯凯奇柔感FLEX跑鞋
**商品链接**：https://uland.taobao.com/item/edetail?id=123456789
**到手**：￥200（淘礼金77.8、淘金币31.4、店铺有价大额券1000-120、200-25消费券到手210）
**佣金率**：10%
**推广链接**：https://s.click.taobao.com/xxxxx
```

### 错误处理

- 脚本输出以"查询失败："开头时，向用户说明错误原因即可。

## Notes

- 目前仅支持**京东**和**淘宝/天猫**两个平台。
- 接口超时时间约 15 秒，脚本 timeout 设为 20 秒。
- API Key 仅从 LINKBOT_API_KEY 环境变量读取（由 OpenClaw 平台自动注入）。
- 所有查询请求发送至 https://linkbot-api.linkstars.com。
