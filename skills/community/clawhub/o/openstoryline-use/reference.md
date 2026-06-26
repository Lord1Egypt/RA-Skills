## Troubleshooting

### 1. `bridge_openstoryline.py` 报连接失败 / connection refused
- 检查 `uvicorn` 是否仍在 `127.0.0.1:8005` 运行。
- 如果没有运行，重新启动 MCP 和 Web 服务。
- 等两个服务都输出成功日志后，再重新发起请求。

### 2. MCP / Web 服务命令执行后没有看到成功日志
- 很可能是启动命令被错误包装了。
- 必须回到原始裸命令重新启动：
  - `PYTHONPATH=src python -m open_storyline.mcp.server`
  - `uvicorn agent_fastapi:app --host 127.0.0.1 --port 8005`
- 不要再加 `head` / `tail` / `timeout` / `grep` 等探测包装。

### 3. 服务能启动，但回复说配置缺失
- `config.toml` 的 LLM / VLM 三元组不完整。
- 回到第 1 步补齐以下 6 个字段：
  - `llm.model`
  - `llm.base_url`
  - `llm.api_key`
  - `vlm.model`
  - `vlm.base_url`
  - `vlm.api_key`

### 4. 看起来流程卡住了
- 先看 Web 服务日志，不要只看 bridge 脚本有没有输出。
- 如果节点还在推进，例如：
  - `filter_clips`
  - `group_clips`
  - `generate_script`
  - `generate_voiceover`
  - `render_video`
  说明服务端仍在正常处理。
- 只有在日志长时间不再推进，或出现明确报错时，才进行人工干预。

### 5. 提示“上一条消息尚未完成，请稍后再发送”
- 不要新建 session。
- 先等待。
- 如果确认只是本地请求卡住，杀掉 bridge/client 进程后，稍等几秒，继续用原 `session_id` 重发。

### 6. `outputs/` 下没找到最终视频
- 优先检查：
  ```bash
  .storyline/.server_cache/<session_id>/render_video_*/output_*.mp4
  ```

### 7. 需要验证二次编辑是否真的生成了新视频
使用：

```bash
cd <repo-root> && find .storyline/.server_cache -name "output_*.mp4" -newer "<previous_output_mp4>" 2>/dev/null
```

如果找到更新的 `output_*.mp4`，就说明二次编辑成功。

### 8. 端口冲突
- 修改 `config.toml` 中的 MCP 端口：
  ```bash
  cd <repo-root> && source .venv/bin/activate && python scripts/update_config.py --config ./config.toml --set local_mcp_server.port=8002
  ```
- 然后重启 MCP 服务。
- Web 服务默认保持 8005，除非用户明确要求修改。