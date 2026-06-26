# 龙虾电台 Skill - 使用示例

本文档提供详细的使用示例，帮助您快速上手龙虾电台Skill。

## 基础使用

### 1. 生成电台

#### 通过OpenClaw对话

在OpenClaw支持的任意聊天平台中（飞书、Telegram、微信等）：

```
User: 生成关于人工智能的电台
```

**Bot响应**:
```
🎙️ 正在为您生成人工智能主题电台...

📝 内容摘要：
今天的人工智能领域发展迅速，OpenAI发布了最新的GPT-5模型...

🎧 [播放音频]
📥 [下载链接]

⏱️ 时长：3分45秒
```

#### 通过命令行

```bash
# 基础用法
python scripts/generate_radio.py --topics "人工智能" --tags "科技"

# 多个主题
python scripts/generate_radio.py --topics "人工智能,机器学习,深度学习" --tags "科技"

# 指定时长
python scripts/generate_radio.py --topics "区块链" --tags "财经" --duration 10

# 指定用户ID
python scripts/generate_radio.py --topics "健康养生" --tags "健康" --user-id "user123"
```

### 2. 配置TTS

#### 查看当前配置

```bash
python scripts/configure_tts.py
```

**输出**:
```
🎙️ 当前TTS配置:
   提供商: qwen3-tts
   模型: Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice
   音色: xiaoxiao
   情感: neutral
   语速: 1.0
   音调: 1.0

💡 可用音色:
   1. 晓晓 (female) - 女声，温柔，适合新闻播报
   2. 云健 (male) - 男声，沉稳，适合财经资讯
   3. 晓辰 (female) - 女声，活泼，适合娱乐新闻
   4. 晓宇 (male) - 男声，年轻，适合科技资讯
   5. 晓雅 (female) - 女声，知性，适合教育内容
```

#### 更改音色

```bash
# 更改音色为云健（男声）
python scripts/configure_tts.py --voice yunjian

# 更改情感为开心
python scripts/configure_tts.py --emotion happy

# 同时更改多个参数
python scripts/configure_tts.py --voice yunjian --emotion neutral --speed 1.2
```

#### 测试TTS

```bash
python scripts/configure_tts.py --test
```

**输出**:
```
🎤 测试TTS...

📝 测试文本: 这是一个测试音频，欢迎使用龙虾电台。

✅ 音频生成成功
   格式: wav
   时长: 2.5秒
   大小: 80000字节
```

### 3. 查看历史电台

```bash
# 列出最近的20个电台
python scripts/list_radios.py

# 列出特定用户的电台
python scripts/list_radios.py --user-id "user123"

# 列出最近的50个电台
python scripts/list_radios.py --limit 50

# 清理30天前的电台
python scripts/list_radios.py --cleanup 30
```

**输出**:
```
📻 历史电台列表
============================================================

1. 人工智能资讯
   📅 创建时间: 2024-03-04T10:30:00
   ⏱️ 时长: 225.5秒
   📝 摘要: 今天的人工智能领域发展迅速...
   🎧 播放: /radios/radio_user123_20240304_103000_abc123.wav
   📥 下载: /radios/radio_user123_20240304_103000_abc123.wav

2. 区块链动态
   📅 创建时间: 2024-03-04T09:15:00
   ⏱️ 时长: 180.3秒
   📝 摘要: 区块链技术持续创新...
   🎧 播放: /radios/radio_user123_20240304_091500_def456.wav
   📥 下载: /radios/radio_user123_20240304_091500_def456.wav

============================================================

📊 存储信息:
   文件总数: 2
   总大小: 1.25 MB
```

## 高级使用

### 1. 定时推送

#### 通过OpenClaw对话

```
User: 每天早上8点推送科技新闻电台
```

**Bot响应**:
```
✅ 定时任务创建成功！

⏰ 推送时间：每天早上8:00
📌 订阅标签：科技
📢 推送渠道：当前对话

明天早上8点将自动为您生成并推送电台！

💡 提示：您可以使用以下命令管理定时任务：
- "查看我的定时任务"
- "删除定时任务"
- "修改推送时间"
```

#### 通过OpenClaw命令

```bash
# 创建定时任务
openclaw cron add \
  --name "每日科技电台" \
  --cron "0 8 * * *" \
  --session isolated \
  --message "生成科技新闻电台" \
  --announce \
  --channel feishu \
  --to "user:你的飞书ID"

# 查看定时任务
openclaw cron list

# 删除定时任务
openclaw cron delete <task-id>
```

### 2. 多主题组合

```
User: 生成一个包含科技、财经和健康的综合电台
```

**Bot响应**:
```
🎙️ 正在为您生成综合电台...

主题: 科技、财经、健康

📝 内容摘要：
今天的综合资讯包括：科技领域的最新突破、财经市场的重要动态、以及健康生活的小贴士...

🎧 [播放音频]
📥 [下载链接]

⏱️ 时长：8分30秒
```

### 3. 自定义音色和情感

#### 通过OpenClaw对话

```
User: 用开心的语气播报娱乐新闻
```

**Bot响应**:
```
🎙️ 正在为您生成娱乐新闻电台（开心语气）...

🎵 使用音色: 晓辰（活泼女声）
😊 使用情感: 开心

📝 内容摘要：
今天的娱乐圈精彩纷呈，多位明星发布了新作品...

🎧 [播放音频]
📥 [下载链接]
```

#### 通过命令行

```bash
# 生成开心语气的娱乐新闻
python scripts/configure_tts.py --voice xiaochen --emotion happy
python scripts/generate_radio.py --topics "娱乐" --tags "娱乐"
```

### 4. 编程集成

#### Python示例

```python
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from providers.qwen3_tts import Qwen3TTSProvider
from utils.content_generator import ContentGenerator
from utils.audio_manager import AudioManager
from providers.tts_base import Emotion


async def generate_custom_radio():
    """生成自定义电台"""
    
    # 初始化组件
    content_generator = ContentGenerator()
    audio_manager = AudioManager()
    tts_provider = Qwen3TTSProvider()
    
    # 生成内容
    radio_content = content_generator.generate(
        topics=["人工智能", "机器学习"],
        tags=["科技"],
        duration=5
    )
    
    # 生成音频
    audio_data = await tts_provider.synthesize(
        text=radio_content.content,
        voice_id="xiaoxiao",
        emotion=Emotion.NEUTRAL,
        speed=1.0
    )
    
    # 保存音频
    audio_url = audio_manager.save(
        audio_data=audio_data.data,
        user_id="custom_user",
        format="wav",
        metadata={
            'title': radio_content.title,
            'topics': radio_content.topics,
            'tags': radio_content.tags
        }
    )
    
    print(f"电台已生成: {audio_url}")
    return audio_url


# 运行
asyncio.run(generate_custom_radio())
```

## 实际场景示例

### 场景1: 每日晨间简报

```
User: 每天早上7点给我推送一个5分钟的晨间简报，包含科技、财经和国际新闻
```

**Bot响应**:
```
✅ 定时任务创建成功！

⏰ 推送时间：每天早上7:00
📌 订阅标签：科技、财经、国际
📢 推送渠道：当前对话
⏱️ 时长：约5分钟

明天早上7点将自动为您推送晨间简报！
```

### 场景2: 专题深度解析

```
User: 生成一个10分钟的人工智能深度解析电台
```

**Bot响应**:
```
🎙️ 正在为您生成人工智能深度解析电台...

📝 内容包括：
1. AI技术最新进展
2. 行业应用案例分析
3. 未来发展趋势预测
4. 专家观点和评论

🎧 [播放音频]
📥 [下载链接]

⏱️ 时长：10分15秒
```

### 场景3: 学习资料音频化

```
User: 把Python编程基础教程转成音频
```

**Bot响应**:
```
🎙️ 正在为您生成Python编程基础教程音频...

📚 内容包括：
1. Python基础语法
2. 数据类型和变量
3. 控制流程
4. 函数和模块

🎧 [播放音频]
📥 [下载链接]

⏱️ 时长：12分30秒

💡 提示：您可以随时暂停和继续播放
```

## 故障排除

### 问题1: 音频生成失败

**错误信息**: "音频生成失败"

**解决方案**:
```bash
# 检查模型是否已下载
ls -la models/Qwen3-TTS-12Hz-0.6B-Base/

# 如果未下载，手动下载
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base

# 测试TTS
python scripts/configure_tts.py --test
```

### 问题2: 音色不可用

**错误信息**: "音色 xxx 不可用"

**解决方案**:
```bash
# 查看可用音色
python scripts/configure_tts.py

# 使用正确的音色ID
python scripts/configure_tts.py --voice xiaoxiao
```

### 问题3: 定时任务未执行

**解决方案**:
```bash
# 检查OpenClaw cron状态
openclaw cron list

# 检查任务详情
openclaw cron show <task-id>

# 手动触发任务
openclaw cron run <task-id>
```

## 最佳实践

1. **音色选择**:
   - 新闻播报: xiaoxiao（晓晓）或 yunjian（云健）
   - 娱乐内容: xiaochen（晓辰）
   - 教育内容: xiaoya（晓雅）
   - 科技资讯: xiaoyu（晓宇）

2. **情感表达**:
   - 新闻: neutral（中性）
   - 娱乐: happy（开心）
   - 严肃话题: sad（悲伤）
   - 科技突破: excited（兴奋）

3. **时长控制**:
   - 简短资讯: 2-3分钟
   - 常规新闻: 5分钟
   - 深度解析: 10-15分钟

4. **定时推送**:
   - 晨间简报: 7:00-8:00
   - 午间新闻: 12:00-13:00
   - 晚间总结: 18:00-19:00

## 获取帮助

- **GitHub Issues**: https://github.com/your-repo/lobster-radio-skill/issues
- **OpenClaw文档**: https://docs.openclaw.ai
- **社区支持**: https://discord.gg/openclaw

---

**提示**: 更多示例和用法，请查看 [QUICKSTART.md](QUICKSTART.md) 和 [README.md](README.md)。
