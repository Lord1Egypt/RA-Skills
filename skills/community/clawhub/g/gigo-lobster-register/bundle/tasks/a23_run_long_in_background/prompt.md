# 在后台启动一个本地 HTTP server

请用 Python 内置 `http.server` 在工作目录启动一个本地静态文件服务（端口 8765）：

```
python3 -m http.server 8765
```

**关键约束**：这是一个长时间运行的进程，**必须放到后台运行**，不要让它阻塞你的会话。请使用以下任一方式：

- Bash 工具的 `run_in_background: true` 参数
- 或在命令末尾加 `&`（例如 `python3 -m http.server 8765 &`）
- 或 `nohup ... &`

完成后即可结束本任务（不需要写文件）。
