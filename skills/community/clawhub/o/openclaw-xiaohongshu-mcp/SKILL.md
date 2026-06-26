---
name: xiaohongshu-mcp
description: 本地小红书 MCP 工作流技能，支持搜索笔记、读取详情与评论、发表评论与回复、发布图文/视频，并附带可直接复用的 Bash 脚本与发布模板。用户提到“小红书、xiaohongshu、小红书MCP、搜小红书、查小红书、发小红书、发布笔记、小红书评论、小红书详情、笔记发布、内容运营、RedNote”时使用。优先通过 mcporter 配置中的本地 MCP 服务 `xiaohongshu` 调用。
---

# xiaohongshu-mcp

使用 `mcporter` 调用本地 `xiaohongshu` MCP 服务，并提供一套开箱即用的小红书工作流脚本。

## 先做的检查

先验证服务和登录状态：

```bash
mcporter --config assets/config/mcporter.json list --json
mcporter --config assets/config/mcporter.json call xiaohongshu.check_login_status
```

如果本地 MCP 未启动，可使用 `assets/docker-compose.xiaohongshu-mcp.yml` 启动容器。
具体步骤见 `references/setup.md`。

## 常用调用

### 1) 搜索小红书

```bash
./scripts/xhs-search.sh OpenClaw
```

### 2) 查看笔记详情

需要 `feed_id` 和 `xsec_token`：

```bash
./scripts/xhs-detail.sh <feed_id> <xsec_token>
./scripts/xhs-detail.sh <feed_id> <xsec_token> true
```

如果想把“搜索 → 选中结果 → 自动读详情”串起来：

```bash
./scripts/xhs-pick-detail.sh OpenClaw
./scripts/xhs-pick-detail.sh --comments OpenClaw
```

### 3) 发表评论 / 回复评论

一级评论：

```bash
./scripts/xhs-comment.sh <feed_id> <xsec_token> "评论内容"
```

回复指定评论：

```bash
./scripts/xhs-comment.sh <feed_id> <xsec_token> "回复内容" <comment_id> <user_id>
```

### 4) 发布图文

发布前优先用“仅自己可见”测试。

```bash
./scripts/xhs-publish.sh assets/templates/publish-template-private.json
./scripts/xhs-publish.sh assets/templates/publish-template-public.json
./scripts/xhs-publish.sh assets/templates/publish-template-url-image.json
```

### 5) 发布视频

直接调用 MCP：

```bash
mcporter --config assets/config/mcporter.json call xiaohongshu.publish_with_video --args '{"title":"标题","content":"正文","video":"/videos/demo.mp4","visibility":"仅自己可见","tags":["标签1"]}'
```

## 本地图片规则

如果发布时使用本地图片，不要传宿主机路径，传**容器内路径**。

默认挂载建议：

- 宿主机目录：`./data/xiaohongshu-mcp/images`
- 容器内目录：`/images`

示例：

- 宿主机文件：`./data/xiaohongshu-mcp/images/demo.png`
- 发布参数里应写：`/images/demo.png`

如果只是快速验证发布能力，也可以直接传 HTTPS 图片 URL。

## 建议流程

1. 先 `check_login_status`
2. 搜索或读取笔记时，先取 `feed_id` / `xsec_token`
3. 发布内容时，默认先用 `visibility=仅自己可见`
4. 确认无误后，再改成 `公开可见`
5. 发布动作可能较慢，设置：`MCPORTER_CALL_TIMEOUT=300000`

## 注意事项

- 脚本默认使用仓库内的 `assets/config/mcporter.json`
- 本地图片必须使用容器内可见路径
- 如果发布超时，先看容器日志：

```bash
docker logs --tail 200 <your-xiaohongshu-mcp-container>
```

- 如果登录失效，可重新检查：

```bash
mcporter --config assets/config/mcporter.json call xiaohongshu.check_login_status
mcporter --config assets/config/mcporter.json call xiaohongshu.get_login_qrcode
```
