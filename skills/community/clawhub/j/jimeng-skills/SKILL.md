---
name: jimeng-skills
description: 基于火山引擎即梦 AI 生成图片和视频，并将结果整理为适合 OpenClaw 在飞书、企微、钉钉中发送和查看的纯文本结果、远程直链和可公开分享链接。用于“生成图片”“生成视频”“让飞书/企微/钉钉可查看”“输出适合企业 IM 的分享结果”“调用 jimeng-skills”等场景。
---

# jimeng-skills

使用 `skill.yaml` 里声明的脚本入口，不要直接假设富文本卡片能力可用。

## 工作原则

- 优先返回纯文本摘要，避免依赖平台专有卡片协议。
- 始终返回本地文件路径，便于调试和二次处理。
- 能拿到火山引擎返回的远程 URL 时，一并返回远程直链。
- 如果设置了 `JIMENG_PUBLIC_BASE_URL`，额外返回公开分享 URL。企业 IM 中优先发送这些 `https://...` 链接。

## 输出策略

- 图片任务：返回 `remoteUrls`、`publicUrls`、`localFiles`。
- 视频任务：返回 `remoteUrls`、`publicUrls`、`localFiles`。
- 任务未完成时：返回 `status: pending` 和便于用户重试的说明。
- 文本结果放在 `text` 字段中，内容使用简单换行和编号，不使用 Markdown 表格。

## 推荐调用

图片：

```bash
npx ts-node scripts/openclaw-jimeng.ts image "一只戴墨镜的柴犬，电影海报风格"
```

视频：

```bash
npx ts-node scripts/openclaw-jimeng.ts video "一只戴墨镜的柴犬在沙滩上奔跑" --wait
```

## 公开分享 URL

若需要飞书、企微、钉钉直接打开本地下载文件，先把输出目录映射到你自己的静态文件服务，再设置：

```bash
export JIMENG_PUBLIC_BASE_URL="https://your-domain.example.com/jimeng-output"
```

脚本会把本地 `output/...` 路径转换成对应的公开 URL。

## 注意

- `VOLCENGINE_AK` 必填。
- 永久凭证使用 `VOLCENGINE_SK`；临时凭证使用 `VOLCENGINE_TOKEN`。
- 企业 IM 对本地绝对路径不可见，跨设备查看时必须依赖远程直链或 `JIMENG_PUBLIC_BASE_URL`。
