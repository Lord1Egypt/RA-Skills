# 发布指南

## 发布前检查

- [ ] 更新 `clawhub.json` 中的 `homepage` 和 `support_url` 为你的 GitHub 仓库地址
- [ ] 在 `screenshots/` 目录添加 3–5 张截图（1920x1080 或 1280x720 PNG），可截取 Cursor 中 skill 评估输出界面
- [ ] 可选：录制 30–90 秒演示视频，上传到 YouTube/Vimeo，将 URL 加入 clawhub.json
- [ ] 确认 `.clawhubignore` 已排除 `backend/`、`frontend/` 等非 skill 代码

## 步骤 1：发布到 GitHub

```bash
cd /Users/kevin/SpeakingCoachV1/ielts-speaking-coach-skill
git add -A && git commit -m "v1.1.1: safety fix - exclude backend from ClawHub package"
git push origin main
```

## 步骤 2：发布到 ClawHub

`.clawhubignore` 文件会自动排除 `backend/`、`frontend/` 等目录。如果 ClawHub CLI 不支持 ignore 文件，使用临时目录方式发布：

```bash
# 方式 A：直接发布（依赖 .clawhubignore）
clawhub publish /Users/kevin/SpeakingCoachV1/ielts-speaking-coach-skill \
  --slug ielts-speaking-coach \
  --name "IELTS Speaking Coach" \
  --version 1.1.1 \
  --changelog "Safety fix: exclude backend code from ClawHub package, clarify shell permission is for ffmpeg only."

# 方式 B：如果 .clawhubignore 不生效，用临时目录
./publish-clean.sh
```

## 权限说明（供 ClawHub 审核）

| 权限 | 用途 |
|------|------|
| network | 调用内置 LLM 能力进行评分、反馈生成、模型答案 |
| shell | 仅用于 ffmpeg 音频格式转换（将用户语音消息转为 WAV 以便发音评分） |

## 安全说明

- 本 skill 不包含任何 Python 后端代码、深度学习模型加载、或运行时下载
- `shell` 权限仅用于调用 ffmpeg 进行音频格式转换
- 不使用 `trust_remote_code`、`eval()`、`exec()` 或任何动态代码执行
- 不依赖未文档化的环境变量
- 可选的后端服务代码仅在 GitHub 仓库中提供，不包含在 ClawHub 发布包中
