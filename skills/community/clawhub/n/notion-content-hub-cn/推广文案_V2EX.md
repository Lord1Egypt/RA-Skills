# V2EX 推广文案 — 飞书内容管理中枢
# 发布节点：分享创造

---

**做了个接实时热榜 + 飞书多维表格的内容管理 OpenClaw Skill**

背景：运营自媒体账号时，选题、发布记录、数据复盘散落在各处，管理混乱。

实现：OpenClaw Skill 接入 5 个免费无鉴权热榜 API（知乎/微博/百度/头条/抖音），结合用户飞书多维表格里的历史内容数据，生成有流量基础的选题并直接写入飞书。

热榜 API 来源（全部国内直连，无需 key）：
```
知乎热榜：GET https://tenapi.cn/v2/zhihuhot
微博热搜：GET https://v2.xxapi.cn/api/weibohot
百度热搜：GET https://tenapi.cn/v2/baiduhot
头条热榜：GET https://tenapi.cn/v2/toutiaohotnew
抖音热点：GET https://tenapi.cn/v2/douyinhot
```

飞书 Bitable API 做 CRUD，支持：选题生成写入、发布数据更新、月度数据汇总分析、超期草稿提醒。

```
openclaw skills install notion-content-hub-cn
```
clawhub.ai/skills/notion-content-hub-cn

飞书 Bitable 多条件 filter 写法有点绕，有踩过这个坑的吗？另外这几个热榜第三方 API 稳定性一般，有没有更好的数据源？
