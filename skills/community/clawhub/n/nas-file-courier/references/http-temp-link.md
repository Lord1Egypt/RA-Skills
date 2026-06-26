# HTTP 临时下载链接方案

> 当消息渠道无原生文件发送能力，或文件超出平台大小限制时使用。

---

## 前置条件

- 双方均在 Tailscale 网络中
- rclone 可用

## 完整脚本

```bash
# 1. 启动临时 HTTP 服务（后台运行，仅监听 Tailscale IP）
TAILSCALE_IP=$(tailscale ip -4)
PORT=18080

rclone serve http /tmp/openclaw/nas-courier/ \
  --addr "${TAILSCALE_IP}:${PORT}" \
  --read-only &
SERVE_PID=$!

# 2. 生成下载链接（URL-encode 文件名中的特殊字符）
FILENAME="file.pdf"  # 替换为实际文件名
ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${FILENAME}'))")
DOWNLOAD_URL="http://${TAILSCALE_IP}:${PORT}/${ENCODED}"

# 3. 将下载链接发送给用户
echo "📥 文件已就绪，请点击下载："
echo "${DOWNLOAD_URL}"
echo "⏰ 链接有效期：10 分钟"

# 4. 等待用户下载完成后关闭服务
sleep 600  # 10 分钟超时
kill $SERVE_PID 2>/dev/null
```

## 发送消息格式

```
📥 文件已就绪，请在 Tailscale 网络下点击下载：
🔗 http://<TAILSCALE_IP>:18080/<文件名>
⏰ 链接有效期 10 分钟，下载完成后请告诉我。
```

## 故障排查

| 问题 | 排查 |
|------|------|
| rclone serve 启动失败 | 检查端口占用: `ss -tlnp \| grep 18080` |
| 用户无法访问链接 | 检查 Tailscale 连通性: `tailscale ping <对方IP>` |
| 链接过期 | 重新启动 rclone serve，生成新链接 |
