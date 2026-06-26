\# 鉴权说明



本文档说明“跨境卫士客户端 OpenAPI”的鉴权方式与调用约定。



\## 1. 鉴权方式



本 API 使用自定义 Header 鉴权，请在每个请求中传入以下请求头：



\- `x-app-id`:   TinqIbRCZdwzpkaD

\- `x-app-secret`:  BcTmTA6gN8phMvSI2wZj5YO7



二者均为必填。



\## 2. 请求头要求



推荐至少携带以下 Header：



```http

x-app-id: your\_app\_id

x-app-secret: your\_app\_secret

Accept: application/json

Content-Type: application/json

