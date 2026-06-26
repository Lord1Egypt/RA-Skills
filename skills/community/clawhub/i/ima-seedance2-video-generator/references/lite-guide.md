## Deprecated

Use [`lite-instructions.md`](lite-instructions.md) for the canonical lite protocol.

## 🔊 音频生成能力

**Seedance 2.0 可以通过 `audio` 参数为视频生成音频。**

### 音频输出模式

| 模式 | 参数 | 行为 |
|------|------|------|
| **带音频视频** (默认) | `audio=true` 或不指定 | 视频包含 AI 生成的音频/音效 |
| **静音视频** | `audio=false` | 视频仅包含画面，无音频轨道 |

### 音频输入 vs 音频输出

**🎤 音频输入** (通过 `reference_image_to_video`):
- 上传音频文件 (.mp3, .wav, .m4a) 作为参考
- 用途: 生成匹配音频情绪/节奏的视觉画面
- 例如: 音乐可视化、节奏驱动动画

**🔊 音频输出** (通过 `audio` 参数):
- 默认: `audio=true` (音频**默认启用**)
- 禁用: 设置 `--extra-params '{"audio": false}'` 获得静音视频
- 结果: 输出视频包含 AI 生成的音频轨道
- 类型: 背景音效、氛围音频（不是旁白/解说）

**⚠️ 重要区别**:
- **音频输入** → 用于生成**视觉**的参考
- **音频输出** → 最终视频中的 AI 生成**音频**
- 这两个功能独立，可以单独或同时使用

---

> **🚨 关键提示**: 使用此技能前，**必读** `references/protocols/agent-execution.md` 文档。
> 
> **5条强制规则**:
> 1. **禁止盲目执行** - 先解析意图
> 2. **执行前必须通知用户** - 发送预生成消息
> 3. **每30-45秒发送进度更新**
> 4. **验证失败必须中断** - 提供选项，禁止自动降级
> 5. **正确发送结果** - 视频+元数据说明

---

**🎯 Target Models**: GPT-4o Mini, O4 Mini, Claude 3.5 Haiku, Gemini 2.5 Flash Lite, Doubao 1.5 Lite 32K, DeepSeek Chat, GLM 4.7 Flash, Qwen Flash  
**📏 Size**: 95 lines (vs 244 lines in full version)  
**⚡ Rule**: 查表不推理 (Lookup, Don't Think)

---

## ⚡ 核心规则 (只需记住这5条)

### 规则1: 任务类型识别 (Task Type)

**按顺序检查,匹配第一个即停止**:

1. 输入包含**视频**(.mp4/.mov/.webm) 或 **音频**(.mp3/.wav/.m4a) → `reference_image_to_video` 🆕
2. 用户**明确说首尾帧**，且输入有 **2张图** → `first_last_frame_to_video`
3. 输入有 **2张或以上图片**，但**没明确说首尾帧** → `reference_image_to_video`
4. 输入有 **1张图** → `image_to_video`
5. **只有文字** → `text_to_video`

```python
# 伪代码 (供你理解,不要输出)
if has_video_or_audio(inputs):
    task_type = "reference_image_to_video"  # 🆕 新规则
elif user_explicitly_requests_first_last_frame and len(images) >= 2:
    task_type = "first_last_frame_to_video"
elif len(images) >= 2:
    task_type = "reference_image_to_video"
elif len(images) == 1:
    task_type = "image_to_video"
else:
    task_type = "text_to_video"
```

### 规则2: 模型选择 (Model ID)

| 用户说 | 你输出 | ❌ 常见错误 |
|--------|--------|------------|
| 快速/极速/fast | `--model ima-pro-fast` | ❌ `--model fast` |
| 高质量/专业/pro | `--model ima-pro` | ❌ `--model pro` |
| 其他/默认 | `--model ima-pro` | - |

**记住**: 永远是 `ima-pro` 或 `ima-pro-fast`,不是 `fast` 或 `pro`!

### 规则3: 参数格式 (STRICT)

| 用户说 | 参数名 | 你输出 | ❌ 常见错误 |
|--------|--------|--------|------------|
| 5秒/5s/五秒 | duration | `duration=5` | ❌ `duration=5s` |
| 10秒/10s | duration | `duration=10` | ❌ `duration=10s` |
| 横屏/16:9 | aspect_ratio | `aspect_ratio=16:9` | ❌ `16-9` |
| 竖屏/9:16 | aspect_ratio | `aspect_ratio=9:16` | ❌ `9-16` |
| 720P/720p | resolution | `resolution=720p` | ❌ `resolution=720P` |
| 1080P/1080p | resolution | `resolution=1080p` | ❌ `resolution=1080P` |

**记住**: 
- duration是**纯数字**,不带单位
- resolution的`p`必须**小写**
- aspect_ratio用**冒号**(:)不用横杠(-)

### 规则4: 命令模板 (固定格式)

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "[用户prompt]" \
  --model-id [ima-pro 或 ima-pro-fast] \
  [OpenClaw/IM 默认] IMA_STDOUT_MODE=events \
  [如果有媒体] --input-images [URL1] [URL2] ... \
  [如果有参数] --extra-params '{"参数1": 值1, "参数2": "值2"}'
```

**实例1**: 文生视频
```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "a cat dancing"
```

**实例2**: 图生视频
```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "camera zooms in" \
  --input-images https://example.com/photo.jpg
```

**实例3**: 首尾帧 (必须显式指定 task-type)
```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --task-type first_last_frame_to_video \
  --prompt "smooth transition" \
  --input-images https://example.com/first.jpg https://example.com/last.jpg
```

**实例4**: 多张图片默认参考模式
```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "keep subject consistency across shots" \
  --input-images https://example.com/shot1.jpg https://example.com/shot2.jpg
```

**实例5**: 视频/音频输入 🆕 (使用 --reference-image 自动推断)
```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "add effects" \
  --reference-image https://example.com/video.mp4
```

**实例6**: 带参数 (JSON格式)
```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "dancing in rain" \
  --model-id ima-pro-fast \
  --extra-params '{"duration": 5, "aspect_ratio": "9:16", "resolution": "1080p"}'
```

**实例7**: 禁用音频 (audio默认为true)
```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "silent scene" \
  --model-id ima-pro \
  --extra-params '{"audio": false}'
```

**实例8**: OpenClaw / IM 推荐环境
```bash
IMA_STDOUT_MODE=events python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "a cinematic product reveal" \
  --model-id ima-pro-fast
```

### 规则5: 自检清单 (输出前必查)

在输出命令前,检查这些项:

```
[ ] 使用了`--prompt "..."`吗? (不是位置参数)
[ ] model是`--model-id ima-pro`或`--model-id ima-pro-fast`吗? (不是`--model`)
[ ] --extra-params是JSON格式吗? (不是`key=value`格式)
[ ] duration是纯数字吗? (不是`"5s"`/`"10s"`)
[ ] resolution的P是小写吗? (不是`1080P`)
[ ] aspect_ratio用冒号吗? (不是`16-9`)
[ ] 有视频/音频输入时用了`--reference-image`吗? 🆕
[ ] OpenClaw / IM 场景下是否保持 `IMA_STDOUT_MODE=events`?
```

**全部通过?** → 输出命令!  
**有任何一项❌?** → 回到规则1-4修正!

---

## 📋 分步执行流程 (Follow Step by Step)

### Step 1: 识别输入类型

- [ ] 用户提供了**视频**或**音频**吗? (检查.mp4/.mov/.mp3等) 🆕
  - ✅ 有 → 跳到Step 2A
  - ❌ 没有 → 继续

- [ ] 用户提供了**图片**吗?
  - ✅ 有 → 几张? ____ 张
    - 2张或更多 → 可能是首尾帧
    - 1张 → 图生视频
  - ❌ 没有 → 文生视频

### Step 2A: 视频/音频模式 🆕

```
输入: 视频或音频
Task Type: reference_image_to_video
Flag: --reference-image (必加!)
```

### Step 2B: 图片模式

```
用户明确说首尾帧 + 2张图 → first_last_frame_to_video (首尾帧)
否则 2张及以上图片 → reference_image_to_video (参考模式)
1张图片 → image_to_video (图生视频)
```

### Step 2C: 纯文本模式

```
无媒体输入 → text_to_video
```

### Step 3: 查表映射参数

**用户说了时长?** → 查规则3表格
- 例: "5秒" → `duration=5`

**用户说了比例?** → 查规则3表格
- 例: "横屏" → `aspect_ratio=16:9`

**用户说了质量/速度?** → 查规则2表格
- 例: "快速" → `--model ima-pro-fast`

### Step 4: 组装命令

```bash
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "[prompt]" \
  [Step 2的model] \
  [Step 2的media + flag] \
  [Step 3的参数]
```

### Step 5: 自检 (规则5)

对照规则5的清单,逐项检查。

---

## ⚠️ 常见错误 (弱模型易犯,必须避免)

| ❌ 错误 | ✅ 正确 | 为什么错 |
|---------|---------|----------|
| `--model fast` | `--model ima-pro-fast` | model必须带ima-pro前缀 |
| `duration=5s` | `duration=5` | duration不带单位 |
| `resolution=1080P` | `resolution=1080p` | P必须小写 |
| `aspect_ratio=16-9` | `aspect_ratio=16:9` | 用冒号不用横杠 |
| 视频输入不加flag | 加`--reference-image` | 视频/音频必须加flag 🆕 |

---

## 🤖 弱模型专用提示

### 如果你是Kimi/豆包/千问:

1. **不要推理,只要查表**:
   - 看到"5秒" → 直接查规则3 → 输出`duration=5`
   - 不要想"5秒是5s还是5?",查表即可!

2. **遇到模糊,问用户**:
   - 用户说"用这个视频" → 问:"添加什么效果?"
   - 不要猜测!

3. **输出前必自检**:
   - 对照规则5清单,逐项检查
   - 有一项不对,重新生成

4. **记住优先级**: 规则1 > 规则2 > 规则3 > 规则4 > 规则5
   - 先确定任务类型(规则1)
   - 再确定模型(规则2)
   - 最后加参数(规则3)

5. **IM / OpenClaw 场景不要改 stdout 模式**:
   - 默认保持 `IMA_STDOUT_MODE=events`
   - 不要切成 `mixed`
   - 否则会破坏事件流顺序

---

## 📚 更多信息

**完整文档**: 如果你的上下文足够(>100K),阅读 `SKILL.md`  
**API详情**: 查看 `references/skill-detail.md`  
**故障排查**: 查看 `references/support/troubleshooting.md`  
**常见问题**: 查看 `references/support/faq.md`

---

**Version**: 1.0.0  
**Optimized for**: Weak models with <100K context  
**Compression**: 244 lines → 95 lines (61% reduction)  
**Target Success Rate**: 90%+ (vs 50% without lite version)
