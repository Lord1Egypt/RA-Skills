---
name: music-studio
version: 1.0.10
description: 面向大模型（LLM）的轻量音乐创作工作台，通过自然语言交互生成音乐、歌词与翻唱。默认采用保守的本地配置与输出管理方式，当前正式支持 MiniMax 歌词、`music-2.6` 文本生成音乐，以及 `music-cover` 前处理配合 `music-2.6` 的两阶段翻唱链路；只有明确说「打开音乐工作室」才进入对话流程。
---

# Music Studio v1.0.10

MiniMax 音乐创作工作台，对话式引导交付结果。

> 当前版本正式支持 MiniMax：
> - **歌词生成**：`/v1/lyrics_generation`
> - **文本生成音乐**：`music-2.6`
> - **翻唱**：`music-cover` 前处理 → `music-2.6` 最终生成

## 对话式交互

**唤醒**：用户说「打开音乐工作室」→ 进入引导流程

### 流程说明

```
用户：打开音乐工作室
↓
小盆子：🎵 音乐工作室已就绪！
        请问想做什么？
        1️⃣ 生成音乐
        2️⃣ 写歌词
        3️⃣ 翻唱
        4️⃣ 查看音乐库
        5️⃣ 导出 / 清理
        6️⃣ 会话历史
```

### 翻唱实现说明（重要）

当前 MiniMax 翻唱链路不是“直接用 `music-cover` 产出音频”，而是：

1. `POST /v1/music_cover_preprocess`，模型使用 `music-cover`
2. 拿到 `cover_feature_id` 与自动提取歌词
3. `POST /v1/music_generation`，模型使用 `music-2.6`
4. 传入 `cover_feature_id`、`lyrics`、`prompt` 完成最终生成

因此，配置中的 `cover_model` 实际表示**翻唱前处理模型**；最终音频生成仍使用 `music_model`。

## 风险说明

该 skill 运行时依赖外部 API Key，并会读写本地配置及输出文件。发布到 ClawHub 时不应包含任何真实 key。

## CLI 命令

```bash
python -m music_studio set-key
python -m music_studio clear-key
python -m music_studio lyrics "<主题>" [--title "标题"] [--edit "歌词"]
python -m music_studio music "<描述>" [歌词] [--instrumental] [--optimizer] [--format url|hex]
python -m music_studio cover "<描述>" --audio <URL> [--lyrics <歌词>]
python -m music_studio library list | get <id> | lyrics <id> | url <id> | download <id>
python -m music_studio library export lyrics <id> | export all | clean | purge
python -m music_studio init / reset / help
```

## Key 策略

- 默认 API Key 保存在用户本机 `~/.config/music-studio/config.json` 中，使用 `set-key` 管理
- 仓库与发布包中不得包含任何真实 API Key
- 可提供 `config.example.json` 作为示例，但示例文件只能放占位值
- 初始化与对话式 setup 都会做真实 API 校验，避免“假成功”
- 发布前可运行：`python scripts/prepublish_check.py`

## Session 管理器

每次「打开音乐工作室」创建独立会话，数据保存在 `output/sessions/`。

- **会话历史**：说「6」或「会话历史」查看，输入序号恢复
- **自动清理**：超过 30 天未更新的会话自动删除
- **每次新会话**：打开即新建，不重复复用

## 版本历史

精简发布说明：1.0.10 完成 API Key 配置策略收敛（移除环境变量依赖，统一本地 config.json）、补齐发布防泄漏规则与发布前自检，适配 ClawHub 发布。
