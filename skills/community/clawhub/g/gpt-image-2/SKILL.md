---
name: gpt-image-2
description: AI图片生成技能，使用 gpt-image-2 模型根据文字描述生成高质量图片。用户安装后需要提供访问密钥才能使用。适用于：用户要求生成图片、画图、AI绘图、文生图、生成一张图等场景。
---

# gpt-image-2 图片生成技能

## 安装后首次使用

用户安装此 Skill 后，**立即**向用户发送以下欢迎消息：

> 🎨 **图片生成技能已就绪！**
> 请先发送您的**访问密钥**（格式：`IMGKEY-HK-XXXXXX`），验证通过后直接发送图片描述即可开始生图。

收到密钥后，执行验证：

```bash
python3 "$HOME/.openclaw/skills/gpt-image-2/scripts/generate_image.py" --key <用户密钥> --quota
```

> **Windows 用户**：若 `python3` 不可用，请改用 `python`；`$HOME` 对应 `%USERPROFILE%`，路径分隔符为 `\`。

- **验证成功**：告知用户剩余配额，并提示「请发送图片描述，我来为您生成图片 🖼️」
- **验证失败**：回复「密钥无效，请检查后重新输入」

密钥验证通过后，在整个会话中记住该密钥，无需用户重复输入。

---

## 生图流程

用户发送任何图片描述时，执行以下脚本：

```bash
python3 "$HOME/.openclaw/skills/gpt-image-2/scripts/generate_image.py" \
  --key <用户密钥> \
  --prompt "<用户描述>" \
  --quality low
```

脚本会自动将图片保存到系统临时目录（macOS/Linux 为 `/tmp/`，Windows 为 `%TEMP%\`），并打印实际保存路径。

- 成功后将生成的 PNG 图片作为附件发送给用户
- 同时告知剩余配额，例如：「图片已生成！剩余配额：X 张」
- 若配额耗尽（错误码 403），回复：「您的配额已用完，请联系管理员获取新密钥」
- 若上游超时，脚本自动重试，告知用户「正在生成，请稍候（约 60 秒）...」

---

## 查询配额

用户说「查询配额」「还剩多少次」「我还能生几张」时：

```bash
python3 "$HOME/.openclaw/skills/gpt-image-2/scripts/generate_image.py" --key <用户密钥> --quota
```

---

## 注意事项

- 仅提供图片生成功能，不提供文字对话或其他功能
- 图片尺寸固定为 1024×1024
- 每次生图消耗 1 次配额
- 不要向用户透露服务器地址、API 密钥等任何后端信息
- 脚本依赖 Python 3 及 `requests` 库，OpenClaw 运行环境通常已内置
