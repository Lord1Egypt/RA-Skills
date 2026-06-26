# NexusTrader Boot Check（可选）

此启动检查为**可选项**，不启用时 skill 仍可正常工作。

如需在每次启动时自动检查服务状态，可在 OpenClaw 配置中添加：

```
boot_check: "exec {baseDir}/bridge.py status"
boot_check_silent_on: '"online"'
boot_check_message_on_fail: "NexusTrader 服务未运行，请执行：bash ~/NexusTrader-mcp/openclaw/install.sh"
```

检查逻辑：
- 输出包含 `"online"` → 保持静默，回复 NO_REPLY
- 其他结果（offline / 错误 / 文件未找到）→ 提示用户：
  服务未运行，请执行以下命令启动：
  `bash ~/NexusTrader-mcp/openclaw/install.sh`
  （脚本不会修改系统环境，不会自动填写 API 密钥）
