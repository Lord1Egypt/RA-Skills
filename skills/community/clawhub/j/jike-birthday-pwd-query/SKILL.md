---
name: jike-birthday-pwd-query
description: 生日密码。输入 MM-DD 生日，查询幸运、健康、建议、名人、塔罗、箴言、优点和缺点。 适用场景：用户询问相关传统文化、生活常识或配对资料时使用。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🎂","requires":{"bins":["python3"],"env":["JIKE_BIRTHDAY_PWD_QUERY_KEY"]},"primaryEnv":"JIKE_BIRTHDAY_PWD_QUERY_KEY"}}
---

# 生日密码 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

## 前置配置

```bash
export JIKE_BIRTHDAY_PWD_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/birthday_pwd_query.py --birthday 01-06
python3 scripts/birthday_pwd_query.py --birthday 01-06 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/birthday/pwd?birthday=01-06&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取查询参数。
2. 执行 `python3 scripts/birthday_pwd_query.py` 并传入对应参数。
3. 默认返回中文文本；需要结构化处理时追加 `--json`。
4. 如果用户没有提供可选参数，可不传该参数，由接口按默认逻辑处理。

## 脚本位置

`scripts/birthday_pwd_query.py`
