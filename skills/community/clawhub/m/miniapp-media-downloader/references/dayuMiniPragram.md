# 多平台解析服务说明

这是面向使用者的解析服务说明。不要在公开文档里展示服务器地址、本机路径、仓库地址、环境变量、Cookie、管理员账号密码或历史接口。

## 能解析什么

- 视频号
- 抖音
- 小红书

远程解析服务主要覆盖前三个平台。B站下载由新版 skill 在用户本机通过 `yt-dlp` 处理，不需要走远程解析服务，也不消耗分发 Key。

兼容说明：如果旧版 skill 仍然把 B站链接提交到 `/api/resolve`，后端会保留兼容处理；新流程优先本地下载。

## 如何使用

联系 `helloaigc2023` 获取这两个变量：

- `MINIAPP_RESOLVER_BASE_URL`
- `MINIAPP_DISTRIBUTION_KEY`

拿到后，在客户端或脚本里配置：

```bash
MINIAPP_RESOLVER_BASE_URL=大瑜提供的解析服务地址
MINIAPP_DISTRIBUTION_KEY=大瑜提供的分发key
```

然后请求解析接口：

```bash
curl -X POST "${MINIAPP_RESOLVER_BASE_URL}/api/resolve" \
  -H 'Content-Type: application/json' \
  -H "X-Distribution-Key: ${MINIAPP_DISTRIBUTION_KEY}" \
  -d '{"url":"复制来的分享链接或完整分享文案"}'
```

也可以批量提交：

```bash
curl -X POST "${MINIAPP_RESOLVER_BASE_URL}/api/resolve" \
  -H 'Content-Type: application/json' \
  -H "X-Distribution-Key: ${MINIAPP_DISTRIBUTION_KEY}" \
  -d '{"urls":["https://weixin.qq.com/sph/...","https://v.douyin.com/...","https://xhslink.com/..."]}'
```

## 返回内容

成功时会返回平台、标题、作者、媒体类型和下载/播放地址：

```json
{
  "ok": true,
  "resolved": [
    {
      "platformName": "视频号",
      "mediaType": "video",
      "title": "标题",
      "author": "作者",
      "downloadUrls": ["https://..."],
      "videoUrl": "https://..."
    }
  ],
  "failed": []
}
```

失败时会返回 `failed`，里面包含失败链接和原因。

## 权限规则

- 视频号、抖音、小红书远程解析需要分发 Key。
- B站新版 skill 本地下载，不需要远程分发 Key；旧版 B站请求走后端时仍按接口权限校验。
- 一个 Key 可以绑定到一个唯一用户。
- Key 可以设置有效期、解析次数和可用平台。
- 服务只记录解析行为，不代理真实视频或图片流量。

## 常见错误

- 没有 Key 或 Key 不正确：请联系 `helloaigc2023` 开通。
- B站本地下载遇到登录限制或风控：`B站需要登录态或被风控，当前视频无法解析`。

## 维护原则

- 公开文档只写使用方式和能力边界。
- 内部部署路径、服务器地址、数据库路径、Cookie、管理员密码、历史接口不要写进公开文档。
- 如果需要维护服务端配置，请在私有运维记录中处理，不放进使用者说明。
