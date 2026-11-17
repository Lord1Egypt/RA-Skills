# 带货口播常见失败与排查

前 6 行是参数契约问题，本 Skill 直接拒绝，不会调用底层能力；后 3 行是底层任务失败，说明已经调到底层。排查时先分清在哪一侧。

| 现象 | 原因 | 处理 |
|------|------|------|
| `Missing required structured parameter: ...` | `customer_keywords` / `targetAudience` / `videoDuration` 只写进了 `prompt`，没有作为顶层字段传 | 补齐顶层结构化字段后重试 |
| 提示需要结构化方案 | `selectedScheme` 传了 `"方案一"` 这类静态文本 | 改传完整方案对象，或传 `schemes` + `selectedSchemeNumber` |
| 未选择方案即被拒绝 | 只传了 `prompt`，没有传 `skipSchemeSelection: true` | 走正常两阶段流程，或确认 `prompt` 已是成片提示词后显式跳过 |
| 参数错误，未调用底层 skill | `videoType` 无法归一到 4 个枚举 | 使用 `SEED` / `SEED_FAST` / `WAN` / `HAPPY_HORSE` 或其别名 |
| 图片数量错误 | `videoType=WAN` 却传了多张图 | 让用户保留 1 张主商品图，改传 `imageUrl` |
| 参数错误，未调用底层 skill | `imageList` 为空，或图片不是 http(s) 可访问 URL | 上游先把本地图片转成可访问 URL，本 Skill 不负责上传 |
| `status=FAILED`，`errorMsg` 为图片审核不通过 | 素材涉及审核、侵权、人脸或明星/名人肖像 | 终态。提示用户更换合规图片，不重试、不换模型、不改 prompt 绕过 |
| `status=FAILED`，其它原因（如服务器繁忙） | 底层任务失败 | 终态。按 `errmsg` 做用户可读说明，不自动重试、不重建任务 |
| stdout 只有 `Saved full response: xxx.json` | 底层未返回视频，落盘的是错误响应 | 读该 JSON 的 `errcode` / `errmsg` / `error` 做用户可读说明，不展示 Python traceback |
