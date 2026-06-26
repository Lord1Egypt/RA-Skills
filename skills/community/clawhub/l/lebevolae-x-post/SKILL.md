\---

name: Leo X Poster

slug: lebevolae-x-post

version: 0.1.0

description: "Leo 的自定义技能：自动发推文到 X/Twitter，支持文本和图片"

author: "Leo Liu (@LBevolae)"

tags: \[twitter, x, post, social]

requirements:

&#x20; - TWITTER\_API\_KEY

&#x20; - TWITTER\_API\_SECRET

&#x20; - TWITTER\_ACCESS\_TOKEN

&#x20; - TWITTER\_ACCESS\_SECRET

\---



\## 功能

发推文到 X，支持纯文本或带一张本地图片。



\## 使用示例

leo，发推：今天天气不错！ #测试

leo，发带图推文：内容xxx，图片 C:\\Users\\bazin\\Desktop\\photo.jpg



\## 配置

需要 X Developer 账号的 4 个凭证（去 https://developer.twitter.com 申请 App，OAuth 1.0a read+write）。

设置为环境变量或 OpenClaw config。

