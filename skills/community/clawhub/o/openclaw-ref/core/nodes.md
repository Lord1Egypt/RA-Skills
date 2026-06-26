# 节点管理参考

## 概述
节点是配套设备(macOS/iOS/Android/无头)，通过WebSocket连接到Gateway，暴露camera/canvas/screen/exec等能力。

## 配对
```bash
openclaw devices list                          # 列出设备
openclaw devices approve <requestId>           # 批准配对
openclaw devices reject <requestId>            # 拒绝配对
openclaw nodes status                          # 节点状态
openclaw nodes list                            # 列出节点
openclaw nodes describe --node <id|name|ip>    # 节点详情
openclaw nodes pending                         # 待批准列表
openclaw nodes approve <requestId>             # 批准节点
openclaw nodes reject <requestId>              # 拒绝节点
openclaw nodes rename --node <id> --name "名称" # 重命名
```

## Canvas (WebView)
```bash
openclaw nodes canvas present --node <id> --target https://example.com  # 显示
openclaw nodes canvas hide --node <id>                                   # 隐藏
openclaw nodes canvas navigate https://example.com --node <id>           # 导航
openclaw nodes canvas eval --node <id> --js "document.title"             # 执行JS
openclaw nodes canvas snapshot --node <id> --format png                  # 截图
openclaw nodes canvas a2ui push --node <id> --text "Hello"               # A2UI推送
openclaw nodes canvas a2ui reset --node <id>                             # A2UI重置
```

## Camera
```bash
openclaw nodes camera list --node <id>                    # 列出摄像头
openclaw nodes camera snap --node <id>                    # 拍照(默认前后)
openclaw nodes camera snap --node <id> --facing front     # 前置
openclaw nodes camera clip --node <id> --duration 10s     # 录制视频
openclaw nodes camera clip --node <id> --duration 3s --no-audio
```
限制: 节点必须前台运行，片段≤60s

## Screen
```bash
openclaw nodes screen record --node <id> --duration 10s --fps 10
openclaw nodes screen record --node <id> --duration 10s --no-audio
openclaw nodes screen record --node <id> --screen 1       # 多显示器
```
限制: ≤60s，需前台

## Location
```bash
openclaw nodes location get --node <id>
openclaw nodes location get --node <id> --accuracy precise --max-age 15000
```
默认关闭，需系统权限。

## 远程执行 (节点主机)
```bash
openclaw nodes run --node <id> -- echo "Hello"
openclaw nodes notify --node <id> --title "Ping" --body "Ready"
openclaw nodes invoke --node <id> --command <cmd> --params '{}'
```

### 启动无头节点主机
```bash
# 前台
openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
# 安装为服务
openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node restart
```

### SSH隧道(loopback绑定)
```bash
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host
OPENCLAW_GATEWAY_TOKEN="<token>" openclaw node run --host 127.0.0.1 --port 18790
```

### Exec节点绑定
```bash
openclaw config set tools.exec.host node
openclaw config set tools.exec.node "<id-or-name>"
openclaw config set tools.exec.security allowlist
# 按智能体
openclaw config set agents.list[0].tools.exec.node "node-id"
# 按会话
/exec host=node security=allowlist node=<id>
```

### 允许列表
```bash
openclaw approvals allowlist add --node <id> "/usr/bin/uname"
```

## 节点类型
| 类型 | 能力 |
|------|------|
| iOS/Android | camera, canvas, screen, location, (sms-Android) |
| macOS应用 | camera, canvas, screen, system.run, system.notify |
| 无头节点主机 | system.run, system.which |
