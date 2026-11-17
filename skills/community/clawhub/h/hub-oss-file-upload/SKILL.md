---
name: hub-oss-file-upload
description: "对用户只说简体中文短句。用户要拿到工作区里已有的文件，或要一个能在外面下载、打开、转发给别人的地址时触发。包括：要文件、把文件给我、发我一份、传给我、附件给我、文件地址、文件链接、下载、帮我下载、下载链接、下载地址、给我链接、分享这个文件、发个链接、外链、公网地址、访问地址、打开地址、OSS 链接、传到 OSS、上传一下给我地址。文件刚生成且同时要求给我或给地址时，写完再调 upload-file.sh。把 ossUrl 原文写进回复。禁止手写 curl，禁止 hub-artifact，禁止 send_to_user。不要调用：只生成不给、只问内容、问的是工作区路径、要从网上把文件下进工作区、用户把附件交给 Agent、指定发到飞书/钉钉/企微/Telegram/Slack/WhatsApp/Teams/邮箱。"
---

# Hub OSS 文件上传

**对用户只说简体中文短句。** 不要贴脚本、密钥、curl。

用户要拿到工作区里**已经有的文件**，或要一个能在外面下载、打开、转发给别人的地址时，立刻上传，把 `data.ossUrl` 原文放进回复。不限于某几个固定词，下面都算：

| 用户要的 | 示例 |
|----------|------|
| 文件本身 | 把文件给我、我要这个文件、发我一份、传给我、附件给我 |
| 下载 | 下载、帮我下载、我要下载、下载链接、下载地址、给我链接 |
| 给别人 | 分享这个文件、发个链接给同事、让别人也能下 |
| 能打开的地址 | 文件地址、文件链接、外链、公网地址、访问地址、打开地址 |
| 上传后给地址 | OSS 链接、传到 OSS、上传一下、存上去给我地址 |
| 生成的同时要 | 做一份报表发给我、导出之后把下载地址给我。先写好文件，再上传 |

下面不要调用：

- 只说生成、写、导出，文件留在工作区就行
- 只问文件里写了什么
- 问的是工作区路径（文件在哪、路径发我）。直接回答路径
- 要从网上把文件下进工作区，或用户把附件交给 Agent 保存
- 明确发到飞书、钉钉、企微、Telegram、Slack、WhatsApp、Teams 或邮箱。那是消息渠道，不是这个下载地址

```bash
if [ -n "${HUB_SKILL_ROOT:-}" ]; then
  SKILL_ROOT="$HUB_SKILL_ROOT"
elif [ -n "${HERMES_HOME:-}" ] || [ -f /opt/data/config.yaml ]; then
  SKILL_ROOT="${HERMES_HOME:-/opt/data}/skills"
elif [ -d /home/node/.openclaw/skills ]; then
  SKILL_ROOT=/home/node/.openclaw/skills
else
  SKILL_ROOT=$(ls -d /workspace/.[!.]*/skills 2>/dev/null | head -1)
fi
SKILL_SCRIPT=$(ls "$SKILL_ROOT"/hub-oss-file-upload*/scripts/upload-file.sh 2>/dev/null | head -1)
bash "$SKILL_SCRIPT" "<工作区文件路径>"
```

路径用刚写好的文件，或用户点名的那个文件。一次一个文件，多个文件各执行一次。刚生成的能对上就不要再问。有多份且分不清是哪一份时再问，不要扫整个目录。

成功依据脚本 stdout 的 `data.ossUrl`。失败把 `error` 转告用户，不要改脚本、不要自己 curl、不要重试。

链接默认大约 7 天有效。单文件不超过 20MB。

## 硬禁止

- 禁止手写 curl
- 禁止 `hub-artifact`
- 禁止 `send_to_user`
- 禁止向用户要 token 或密钥
- 禁止在用户没要文件或地址时上传
