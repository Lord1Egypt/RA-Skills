---
name: doubao-media
description: 豆包网页端媒体提取与抓包。用于：通过浏览器 Cookie 调用豆包 chat/completion、抓取 SSE 回复、提取和下载图片/视频资产、监控豆包网页生成流程并保存最终媒体 URL 与文件。适用于“继续研究豆包 skill”“把豆包生成的图片/视频拿到”“抓豆包网页请求/媒体资源”“提取豆包生成结果”等场景。
---

# doubao-media

把这个 skill 当成两条并行路线：

1. **API 路线**：直接调用 `chat/completion`，适合验证 prompt、拿文本、顺便尝试从 SSE 里提取媒体 URL。
2. **浏览器抓包路线**：监听真实网页网络请求，适合最终拿到豆包产出的图片、视频、封面、下载链接。这条路通常更稳。

## 目录重点

### 当前主入口

- `scripts/doubao_api.js`：刷新 Cookie、验证文本聊天链路
- `scripts/doubao_media_api.js`：调用 chat/completion，提取并下载图片/视频资产
- `scripts/capture_doubao_media.js`：监听浏览器网络流量，抓最终媒体 URL，适合视频排查

### 历史脚本

本地工作区保留了 `scripts/legacy/` 作为逆向参考，但公开发布版本不包含这些历史文件。

## 推荐工作流

### A. 先确认会话可用

最省事的一条命令：

```bash
npm run ready
```

或直接：

```bash
node doubao_api.js ready
```

它会自动完成：

1. 检查本地 session
2. 必要时尝试抓当前浏览器登录态
3. 如果还没登录，则自动打开豆包登录页并等待登录
4. 最后输出 `available` / `unavailable`

需要手动拆开排查时，再用：

```bash
npm run check-session
npm run login-if-needed
npm run verify-chat
```

逻辑是：

- `check-session`：检查本地 `~/.doubao_chat_session.json` 是否存在且仍可用
- `login-if-needed`：如果 session 失效，则先尝试直接抓当前浏览器 Cookie；若仍不可用，会自动打开 `https://www.doubao.com/` 并等待你完成登录，然后刷新本地 session
- `verify-chat`：验证 Cookie/API 链路是否正常

默认等待登录约 120 秒。也可用：

```bash
node doubao_api.js login-if-needed --timeout-ms 180000
```

### B. 尝试直接从 API 回复里拿媒体

```bash
node doubao_media_api.js chat "生成一张赛博朋克老虎头像"
node doubao_media_api.js chat "生成一张赛博朋克老虎头像" --download --output ./captures
npm run extract-media
```

输出里重点看：

- `assets[].bestUrl`：当前最推荐直接下载的链接
- `assets[].variants`：同一素材的其他预览/水印/原图变体
- `download.manifestPath`：批量下载后的清单文件

如果返回 JSON 中带 `assets` / `mediaUrls`，优先走这条，最省事。

### C. 真正拿图片/视频时，优先走浏览器抓包

```bash
node capture_doubao_media.js monitor --download --output ./captures
npm run capture-media
```

然后在已登录的浏览器里实际操作豆包：生成图片、生成视频、打开结果页、点击预览/播放/下载。

脚本会：

- 记录请求/响应里的可疑媒体 URL
- 尝试从 JSON/SSE 响应体里递归提取 URL
- 根据父请求与 URL 规则区分“本次生成结果”与页面噪音
- 可选自动下载图片/视频到输出目录
- 生成原始 `.jsonl` 清单、`summary.txt`，以及筛选后的 `*-curated.json`

适合视频链路排查：如果豆包视频不是直接在 API SSE 里给出下载地址，通常也会在网页后续请求里出现 `mp4`、`webm`、`m3u8`、`poster`、`cover`、`play_addr` 等线索。

## 关于稳定性

豆包网页参数、字段名、资源域名都可能变化，所以：

- **不要只押单一 API 字段**
- 优先保存真实网络流量里出现的最终媒体 URL
- 如果 API 提取不到媒体，继续通过浏览器抓包拿资源

## 常见下一步

如果用户要“最终把豆包生成的图片和视频都拿到”，就按这个顺序推进：

1. 修通 `login/chat`
2. 用 `doubao_media_api.js` 看 SSE 里是否已暴露素材 URL
3. 用 `capture_doubao_media.js` 监听真实生成过程
4. 把抓到的 URL 归档/下载
5. 如果确认了稳定接口，再把字段固化回脚本

## 注意

- 依赖浏览器远程调试端口 `18800`
- 需要浏览器里已经登录豆包
- 这是网页自动化/抓包方案，接口可能随网页更新而变化；抓真实媒体请求通常比硬编码接口更耐用
