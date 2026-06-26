---
name: memorial
description: 为逝去的亲人建立纪念档案，让记忆得以延续。支持文字追忆、人格重建、声音克隆。
version: 1.1.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: 根据用户第一条消息的语言，全程使用同一语言回复。

# 纪念.skill

## 触发条件

当用户说以下任意内容时启动：

* `/create-memorial`
* "帮我建一份纪念档案"
* "我想纪念 XX"
* "给 XX 建一个档案"

---

## 工具使用规则

| 任务 | 使用工具 |
|------|----------|
| 微信语音提取 | `Bash` → `python tools/wechat_voice_extractor.py` |
| 音频预处理 | `Bash` → `python tools/voice_preprocessor.py` |
| 音频转文字 | `Bash` → `python tools/audio_transcriber.py` |
| 声音模型训练 | `Bash` → `python tools/voice_trainer.py` |
| 语音合成 | `Bash` → `python tools/voice_synthesizer.py` |
| 微信聊天解析 | `Bash` → `python tools/wechat_parser.py` |
| QQ 聊天解析 | `Bash` → `python tools/qq_parser.py` |
| 照片分析 | `Bash` → `python tools/photo_analyzer.py` |
| 访谈问题生成 | `Bash` → `python tools/interview_guide.py` |
| 档案文件管理 | `Bash` → `python tools/skill_writer.py` |
| 读取文件/图片 | `Read` 工具 |
| 写入/更新档案 | `Write` / `Edit` 工具 |

---

## 主流程

### Step 0：建档时机判断

询问用户：

```
这份档案，是为还在的人提前建，还是为已经离开的人建？
```

→ 生前建档模式 或 身后建档模式（参考 `prompts/intake.md`）

---

### Step 1：基础信息采集（3 个问题）

参考 `prompts/intake.md`：
1. **称呼与关系**
2. **基本背景**（生卒年、籍贯、职业）
3. **性格印象**

---

### Step 2：材料导入

#### 2A：微信语音提取（全自动）

如果用户说"微信群里有语音"，执行以下流程：

```bash
# 检测微信并列出群聊
python tools/wechat_voice_extractor.py --list-groups

# 用户告诉群名后，列出语音发送者
python tools/wechat_voice_extractor.py --group "群名关键词"

# 用户指定人名后，提取语音
python tools/wechat_voice_extractor.py --group "群名" --person "人名" --outdir memorials/{slug}/materials/audio/raw
```

#### 2B：音频预处理 + 转文字

```bash
# silk → WAV + 降噪
python tools/voice_preprocessor.py --dir memorials/{slug}/materials/audio/raw --outdir memorials/{slug}/materials/audio/processed

# WAV → 文字转录（用于纪念档案文字部分）
python tools/audio_transcriber.py --dir memorials/{slug}/materials/audio/processed --speaker "{name}" --format chat --output memorials/{slug}/materials/voice_transcripts.md
```

#### 2C：其他材料

- 微信/QQ 文字聊天记录 → `wechat_parser.py` / `qq_parser.py`
- 照片 → `photo_analyzer.py`
- 口述/粘贴 → 直接整理
- 生前访谈 → `interview_guide.py --role self`

---

### Step 3：生成纪念档案

#### 3A：追忆档案（remembrance.md）

参考 `prompts/remembrance_analyzer.md` 分析所有材料，提取 8 个维度。
参考 `prompts/remembrance_builder.md` 生成文件。

#### 3B：人格档案（persona.md）

参考 `prompts/persona_analyzer.md` 分析人格特征（5+1 层）。
参考 `prompts/persona_builder.md` 生成文件。

#### 3C：合并 SKILL.md

```bash
python tools/skill_writer.py --action create --name "{name}" --slug {slug}
# 然后用 Write 工具写入 remembrance.md 和 persona.md
python tools/skill_writer.py --action combine --slug {slug}
```

---

### Step 4：声音模型训练（如有语音数据）

```bash
# 一键训练（prepare + feature extraction + SoVITS fine-tuning）
# 自动检测转录质量，方言数据会跳过 GPT 微调
python tools/voice_trainer.py --action full --slug {slug} --audio-dir memorials/{slug}/materials/audio/processed
```

训练完成后验证：

```bash
python tools/voice_synthesizer.py --slug {slug} --action check
python tools/voice_synthesizer.py --slug {slug} --text "测试一下声音效果"
```

---

### Step 5：交付

完成后向用户展示：

```
纪念档案已建立完成。

📄 文字档案
- 追忆档案：{remembrance.md 摘要}
- 人格档案：{persona.md 摘要}

🔊 声音模型（如有）
- 训练数据：{N} 条语音，{M} 分钟
- 模型状态：已就绪

你可以：
- 对话追忆："给我讲讲他/她的故事"
- 人格模拟："如果告诉他/她这件事，他/她会怎么说？"
- 声音合成："用他/她的声音说'xxx'"
- 继续补充："我又想起了一件事..."
- 纠正："他/她不会这样说"
```

---

## 进化模式

当用户追加材料或纠正时：

- 追加 → 参考 `prompts/merger.md` 增量合并
- 纠正 → 参考 `prompts/correction_handler.md` 写入修正
- 版本管理 → `python tools/version_manager.py`

---

## 伦理边界

1. **追忆声明**：始终提醒这是基于记忆的追忆，不代表本人
2. **不代逝者表态**：不对家庭决策、遗产等给出"逝者的立场"
3. **时态边界**：只能说"以 ta 的性格，ta 可能..."
4. **数据隐私**：所有数据仅本地存储，不上传
5. **声音伦理**：合成语音不可冒充逝者欺骗他人
