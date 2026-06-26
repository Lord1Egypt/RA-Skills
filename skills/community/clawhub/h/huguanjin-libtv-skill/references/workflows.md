# 典型工作流

理解这些工作流，才能正确组合脚本完成用户需求。

## 场景 1：用户要求生成图片/视频（最常见）

```
1. create_session.py "用户的描述"  →  拿到 sessionId + projectUuid
2. 每隔 8 秒调用 query_session.py SESSION_ID --after-seq 0 轮询
3. 检查 messages：当出现 assistant 角色的消息且包含图片/视频 URL → 任务完成
4. 自动下载：download_results.py SESSION_ID --output-dir ~/Downloads/项目名 --prefix 有意义的前缀
5. 向用户展示：本地文件列表 + projectUrl（画布链接）
```

生成完成后**自动执行下载**，不需要用户额外请求。下载目录和前缀根据任务语义自动命名（如分镜用 `storyboard`，角色设定用 `character` 等）。

## 场景 2：用户提供图片/视频要求编辑修改（如"把纸船换成爱心"）

```
1. upload_file.py /path/to/video.mp4  →  拿到 OSS URL
2. create_session.py "把四周的纸船都换成白色的纸爱心 参考视频：{oss_url}"
3. 后续同场景 1 的步骤 2-5
```

用户给了文件路径 + 编辑指令 = 先上传文件，再把编辑指令和 OSS URL 一起发送。

## 场景 3：用户提供参考图/视频要求生成新内容

```
1. upload_file.py /path/to/ref.png  →  拿到 OSS URL
2. create_session.py "根据参考图生成xxx，参考图：{oss_url}"
3. 后续同场景 1 的步骤 2-5
```

## 场景 4：在已有会话中追加新需求

```
1. create_session.py "新的描述" --session-id SESSION_ID
2. 后续同场景 1 的步骤 2-5
```

## 场景 5：用户明确要求 Gemini 文生图（如"用 gemini-3-pro-image-preview 生成海报"）

```
1. gemini_generate_image.py "用户的描述" --aspect-ratio 16:9 --image-size 2K
2. 从脚本返回中读取 saved（本地图片路径）
3. 向用户展示图片结果（Gemini 路径无 projectUrl）
```

## 场景 6：用户明确要求 Sora/Veo 文生视频或图生视频

```
1. 如有参考图：直接使用本地路径调用 sora_generate_video.py（或 veo_generate_video.py） --input-reference ...
2. 执行 sora_generate_video.py（或 veo_generate_video.py） "用户原始描述" ...  →  拿到 task_id
3. 每隔 5 秒调用 sora_query_video.py（或 veo_query_video.py） TASK_ID --wait --interval 5
4. 当 status=completed 且返回 videoUrl/url/output 时，向用户展示视频地址
```

## 轮询策略

以下策略仅适用于 LibTV 会话模式。

- **间隔**：每 8 秒查询一次
- **增量拉取**：首次用 `--after-seq 0`，后续用上次拿到的最大 seq 值
- **完成判断**：messages 中出现 assistant 消息且 content 包含结果 URL（图片/视频地址）
- **超时**：连续轮询 3 分钟仍无结果，告知用户"生成时间较长，可稍后通过项目画布链接查看"，不再继续轮询
- **错误重试**：单次查询失败可重试 1 次，连续 3 次失败则停止并告知用户
