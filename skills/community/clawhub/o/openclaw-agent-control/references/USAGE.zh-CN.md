# 使用说明（中文）

1. 上传本 skill 到 ClawHub。
2. 安装并执行：
```bash
bash scripts/deploy_project.sh
```
3. 查看日志：
- 后端日志：`/tmp/openclaw-agent-control-backend.log`
- 前端日志：`/root/OpenClaw-Agent-Control/agent-monitor-ui/.run/agent-monitor-ui.log`

## 常见变量
- `PROJECT_DIR`：项目落地目录
- `REPO_URL`：源码仓库地址
- `MONITOR_PORT`：后端端口
- `PORT`：前端端口
