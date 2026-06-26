---
name: novel-workshop
description: |
  多模型命题小说创作工坊。用户给出写作命题，自动完成：AI 写初稿 → 三路并行审阅（逻辑/文学/锐评）→ AI 改稿 → 飞书文档完整存档。
  一键启动，全程自动，零手动干预。支持飞书实时进度推送。
  触发词：命题写作、写一篇小说、命题小说、创作工坊、novel workshop
---

# 🎲 命题小说多模型创作工坊

## 工作流

```
用户命题 → MiMo 写初稿 → Gemini+Claude 三路并行审阅 → Gemini 改稿 → 飞书文档完整存档
```

全流程约 2-5 分钟，飞书群聊实时进度推送。

## 使用方式

用户给出写作命题后，执行脚本：

```bash
python3 skills/novel-workshop/workflow.py "用户的原始命题" "文档标题"
```

**重要**：
- 第一个参数是用户的**原始命题原话**，不要修改、不要补充解释
- 第二个参数是飞书文档标题（简短的标识名）
- 脚本后台运行，自动推送进度到飞书群聊
- 脚本完成后输出 `__SUMMARY__:` JSON，包含文档链接和评分

## 前置要求

1. **OpenRouter API Key**：在 `openclaw.json` 的 `models.providers.openrouter.apiKey` 中配置
2. **飞书应用**：在 `openclaw.json` 的 `channels.feishu` 中配置 `appId` 和 `appSecret`
3. **Python 依赖**：`requests`（通常已预装）
4. **模型注册**（在 `openclaw.json` 的 `models.registered` 中添加）：
   - `xiaomi/mimo-v2-flash`（写初稿）
   - `google/gemini-2.5-pro`（审阅+改稿）
   - `anthropic/claude-opus-4.6`（锐评）

## 环境变量（可选覆盖）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `FEISHU_CHAT_ID` | 飞书群聊 ID（进度推送目标） | 从 openclaw.json 读取 |
| `FEISHU_FOLDER_TOKEN` | 飞书文件夹 token（文档创建位置） | 无（创建到根目录） |
| `FEISHU_OWNER_OPEN_ID` | 文档所有者 open_id（自动授权） | 无 |
| `OPENROUTER_API_KEY` | OpenRouter API Key | 从 openclaw.json 读取 |

## 输出

### 本地文件
`~/.openclaw/workspace/novels/{标题}.md` — 完整 markdown（初稿+审阅+终稿）

### 飞书文档
自动创建到指定文件夹，包含完整内容：
- Part 1：初稿全文
- Part 2：三路审阅全文（逻辑检阅 + 文学性分析 + 锐评）
- Part 3：终稿全文

### 进度消息（飞书群聊）
```
[░░░░░] 0/5 收到命题！工作流启动中 🎲
[█░░░░] 1/5 初稿完成 ✅《标题》(N字) 三路审阅启动中…
[██░░░] 2/5 审阅完成 ✅ 逻辑 X/10 | 文学 X/10 | 改稿启动中…
[███░░] 3/5 改稿完成 ✅ 保存中…
[████░] 4/5 存档完成 ✅ 正在写入飞书文档…
[█████] 5/5 全部完成！🎲 链接 + 评分
```

## 模型角色

| 角色 | 默认模型 | 备选 |
|------|----------|------|
| 初稿写作 | xiaomi/mimo-v2-flash | google/gemini-2.5-pro |
| 逻辑审阅 | google/gemini-2.5-pro | anthropic/claude-opus-4.6 |
| 文学审阅 | google/gemini-2.5-pro | anthropic/claude-opus-4.6 |
| 锐评 | anthropic/claude-opus-4.6 | google/gemini-2.5-pro |
| 改稿 | google/gemini-2.5-pro | anthropic/claude-opus-4.6 |

## ⚠️ 铁律

1. **Prompt 原封不动**：用户怎么说的就怎么传给模型，不要添加解释或修改
2. **飞书文档不省略任何内容**：初稿全文、审阅全文、终稿全文，一个字都不能少
3. **改稿不用写初稿的模型**：避免"自己改自己"导致的保守倾向
4. **全程自动**：用户只需给命题，不需要说"继续"
