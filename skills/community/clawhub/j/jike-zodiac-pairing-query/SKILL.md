---
name: jike-zodiac-pairing-query
description: 星座配对。输入男生星座和女生星座，查询配对指数、比例、同情指数、天长地久指数、结果评述和恋爱建议。 适用场景：用户询问相关传统文化、生活常识或配对资料时使用。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"💫","requires":{"bins":["python3"],"env":["JIKE_ZODIAC_PAIRING_QUERY_KEY"]},"primaryEnv":"JIKE_ZODIAC_PAIRING_QUERY_KEY"}}
---

# 星座配对 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

## 前置配置

```bash
export JIKE_ZODIAC_PAIRING_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/zodiac_pairing_query.py --boy-zodiac 双鱼座 --girl-zodiac 天蝎座
python3 scripts/zodiac_pairing_query.py --boy-zodiac 双鱼座 --girl-zodiac 天蝎座 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/zodiac_pairing?boy_zodiac=双鱼座&girl_zodiac=天蝎座&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取查询参数。
2. 执行 `python3 scripts/zodiac_pairing_query.py` 并传入对应参数。
3. 默认返回中文文本；需要结构化处理时追加 `--json`。
4. 如果用户没有提供可选参数，可不传该参数，由接口按默认逻辑处理。

## 脚本位置

`scripts/zodiac_pairing_query.py`
