---
name: jike-zodiac-sign-query
description: 星座查询。输入星座名称，查询星座特征、守护宫、阴阳性、守护星、幸运色、幸运数字、区间和男女特点。 适用场景：用户询问相关传统文化、生活常识或配对资料时使用。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"♓","requires":{"bins":["python3"],"env":["JIKE_ZODIAC_SIGN_QUERY_KEY"]},"primaryEnv":"JIKE_ZODIAC_SIGN_QUERY_KEY"}}
---

# 星座查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

## 前置配置

```bash
export JIKE_ZODIAC_SIGN_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/zodiac_sign_query.py --name 双鱼座
python3 scripts/zodiac_sign_query.py --name 双鱼座 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/zodiac_sign?name=双鱼座&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取查询参数。
2. 执行 `python3 scripts/zodiac_sign_query.py` 并传入对应参数。
3. 默认返回中文文本；需要结构化处理时追加 `--json`。
4. 如果用户没有提供可选参数，可不传该参数，由接口按默认逻辑处理。

## 脚本位置

`scripts/zodiac_sign_query.py`
