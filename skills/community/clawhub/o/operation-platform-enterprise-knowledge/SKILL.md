---
name: domain-test-skill
display_name: 域名测试
version: "0.1.0"
description: |
  域名测试
metadata: { "openclaw": { "emoji": "📊" } }
triggers:
  - intent:  域名测试
    keywords:
      - 域名测试
    examples: |
      帮我用商家蛋蛋测试这个域名
---


---

# ✅ 固定流程（按顺序执行，任一步失败立刻返回错误）

## Step 1：解析商家名称并获取商家ID

baseUrl: https://merchant-lego.corp.kuaishou.com


接口：
POST https://merchant-lego.corp.kuaishou.com/gateway/crm/seller/manager/querySellerSearchResult

请求体：
```json
{
    "username": "${username}",
    "sellerName": "${sellerName}"
}
```

其中：
- `${sellerName}` 从用户问题中解析得到商家名称（例如用户的问题是“请生成小米官方直播间的诊断报告”，sellerName则是“小米官方直播间”）
- `${username}` 从本地凭证中获取（读取 `~/.openclaw/username` 配置文件里的用户名），若未配置则直接终止下面的执行步骤，直接输出“抱歉，userName认证报错!”

正确的请求体格式可参考下面：
```json
{
    "username": "userName",
    "sellerName": "sellerName"
}
``` 

响应结构（示例）：
```json
{
  "status": 200,
  "statusText": "OK",
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": [
    "1001234567",
    "1001234568",
    "1001234569"
  ]
}
```
## 结果处理
- 直接把http接口返回的结果返回给用户