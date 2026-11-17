# AI 音乐创作师 - 快速开始指南

🎵 **AI 驱动的端到端音乐创作技能，将您的声音、歌词和创意转化为专业级音乐作品**

## 📋 前置条件

### 系统要求
- **操作系统**: Linux/macOS/Windows (WSL2)
- **Python**: 3.9-3.11
- **GPU**: NVIDIA GPU ≥ 18GB 显存 (推荐 RTX 4090/A100)
- **内存**: ≥ 32GB RAM
- **存储**: ≥ 500GB SSD (用于缓存和临时文件)
- **网络**: 稳定网络连接 (模型下载需要)

### 软件依赖
```bash
# Linux/Unix 系统
sudo apt update
sudo apt install -y ffmpeg libsndfile1 libgl1-mesa-glx

# macOS
brew install ffmpeg libsndfile

# Windows (WSL2)
# 在 WSL2 中执行 Linux 命令，同时需要在 Windows 安装 NVIDIA 驱动
```

## 🚀 快速安装

### 方法一：直接使用 (推荐)

1. **安装技能**
```bash
# 使用 OpenClaw CLI 安装
openclaw skill install ai-music-composer

# 或手动复制到技能目录
cp -r ai-music-composer ~/.codex/skills/
```

2. **安装 Python 依赖**
```bash
cd ~/.codex/skills/ai-music-composer
python -m pip install -r scripts/requirements.txt
```

3. **运行环境检查**
```bash
python scripts/setup_environment.py --check-only
# 如果有问题，使用 --install 进行修复
python scripts/setup_environment.py --install
```

### 方法二：Docker 部署

1. **启动服务集群**
```bash
docker-compose up -d
```

2. **等待服务就绪**
```bash
# 检查服务状态 (所有服务应为 'healthy')
docker-compose ps
```

## 🎯 快速体验

### 示例 1：使用预设歌词创作

```python
from scripts.generate_music import AIMusicComposer
import asyncio

async def create_song():
    composer = AIMusicComposer()
    
    result = await composer.generate_music(
        voice_sample="path/to/your/voice.wav",
        lyrics="当微风轻抚你发梢 回忆如花瓣飘落
                在这美好的时光里 我轻轻唱着这首歌",
        style="pop",
        theme="浪漫",
        tempo=120,
        emotion="romantic"
    )
    
    if result['success']:
        print(f"✅ 生成成功！")
        audio_path = result['results']['final_audio']['audio_path']
        print(f"🎵 音频文件: {audio_path}")
    else:
        print(f"❌ 生成失败: {result['error']}")

# 运行示例
asyncio.run(create_song())
```

### 示例 2：基于主题自动生成歌词

```bash
python scripts/generate_music.py \
  --voice my_voice.wav \
  --theme "青春回忆" \
  --style folk \
  --emotion peaceful \
  --output ./my_song/
```

### 示例 3：批量生成

创建配置文件 `batch_config.json`:
```json
{
  "jobs": [
    {
      "name": "song1",
      "voice": "voice1.wav",
      "theme": "夏日恋歌",
      "style": "pop"
    },
    {
      "name": "song2", 
      "voice": "voice2.wav",
      "lyrics": "自定义歌词内容...",
      "style": "rock"
    }
  ]
}
```

运行批量生成:
```bash
python scripts/batch_generate.py --config batch_config.json
```

## 🎵 输入素材准备

### 录音样本要求
- **时长**: 15-60 秒 (推荐 30 秒)
- **内容**: 清晰朗读或唱歌，无背景噪音
- **格式**: WAV (48kHz, 16-24bit) 最佳
- **环境**: 安静环境，避免回声

### 歌词输入格式
- **文件编码**: UTF-8
- **中文歌词**: 建议每句 7-15 字
- **英文歌词**: 遵循韵律规则
- **标记支持**: [Verse], [Chorus], [Bridge] 等

### 风格选择指南

| 风格 | 适用场景 | BPM 范围 | 特色 |
|------|----------|----------|------|
| `pop` | 流行歌曲 | 100-140 | 大众化，电子元素 |
| `rock` | 摇滚乐 | 110-160 | 吉他驱动，有力 |
| `folk` | 民谣 | 70-110 | 简单真挚，吉他伴奏 |
| `ballad` | 抒情 | 60-100 | 情感丰富，旋律优美 |
| `electronic` | 电子音乐 | 120-160 | 节奏感强，合成器 |
| `jazz` | 爵士 | 80-120 | 即兴，复杂和声 |
| `rap` | 说唱 | 80-100 | 节拍突出，文字为王 |

## 🔧 配置自定义

### 创建配置文件
复制示例配置并自定义:
```bash
cp config/music_config.json config/my_config.json
```

### 主要配置项
```json
{
  "services": {
    "voice_clone": "http://localhost:8001",  // 语音克隆服务地址
    "music_gen": "http://localhost:8002",     // 音乐生成服务地址
    "lyrics_ai": "http://localhost:8003",     // 歌词服务地址
    "audio_process": "http://localhost:8004"  // 音频处理服务地址
  },
  "max_concurrent_jobs": 4,                    // 最大并发任务数
  "temp_dir": "/tmp/ai_music",                // 临时文件目录
  "output_dir": "/app/data/outputs"            // 输出目录
}
```

## 📖 详细使用教程

### 基础工作流程

1. **准备录音**
   - 录制 30 秒清晣语音
   - 保存为 WAV 格式
   - 确保无背景噪音

2. **选择风格**
   - 根据情绪选择音乐风格
   - 设置合适的 BPM (节拍)
   - 确定调性

3. **输入歌词**
   - 提供完整歌词文本
   - 或只给主题让 AI 创作
   - 检查格式和韵律

4. **启动生成**
   - 提交任务到队列
   - 监控生成进度
   - 等待完成通知

5. **获取结果**
   - 下载生成的音频
   - 查看质量报告
   - 导出多种格式

### 高级技巧

#### 优化音质
- **录音技巧**: 
  - 距离麦克风 15-20cm
  - 使用高质量麦克风
  - 避免爆破音和喷麦

- **参数调整**:
  - 根据人声特点调整音色参数
  - 微调节奏以匹配音色
  - 合理设置情绪和动态

#### 歌词创作建议
- **中文歌词**: 注意押韵和字数一致性
- **意象表达**: 使用具象化的描述
- **情感层次**: 主歌叙事，副歌高潮

## 🚨 常见问题

### 生成速度慢
**问题**: 生成时间超过预期
**解决方案**:
- 检查 GPU 显存使用情况
- 减少并发任务数量
- 升级到更强大的 GPU

### 音色不相似
**问题**: 生成的声音与原录音差异大
**解决方案**:
- 重新录制更清晰的样本
- 增加样本时长到 45-60 秒
- 调整语音克隆参数

### 音频质量不佳
**问题**: 生成的音乐有杂音或失真
**解决方案**:
- 检查输入音频质量
- 降低混音参数
- 重新生成尝试

### 内存不足
**问题**: CUDA out of memory 错误
**解决方案**:
- 重启服务释放内存
- 升级到更大显存的 GPU
- 使用梯度检查点技术

## 📚 资源链接

### 官方文档
- [技术规格详情](docs/technical-spec.md) - 详细的技术架构和模型说明
- [API 接口文档](docs/api-reference.md) - REST API 完整参考
- [扩展开发指南](docs/extension-guide.md) - 自定义开发和插件开发

### 示例和模板
- `examples/` - 完整的使用示例
- `templates/` - 歌词和风格模板
- `assets/samples/` - 示例音频文件

### 社区支持
- GitHub 仓库: https://gitee.com/TinaZen/Juxingyi
- 技术论坛: https://community.huo15.com
- 微信交流群: 添加小助手获取

## 🎯 下一步学习

1. **深入学习**: 阅读 [技术规格详情](docs/technical-spec.md)
2. **API 集成**: 参考 [API 接口文档](docs/api-reference.md) 集成到你的应用
3. **高级定制**: 查看 [扩展开发指南](docs/extension-guide.md) 进行深度定制
4. **社区交流**: 加入开发者社区，分享经验和获取支持

## 🌟 性能优化提示

### GPU 优化
```bash
# 检查 GPU 状态
nvidia-smi

# 设置 GPU 计算模式
nvidia-smi -i 0 -c EXCLUSIVE_PROCESS

# 监控 GPU 使用
nvidia-smi dmon -s u
```

### 内存管理
```python
# 手动清理GPU缓存
torch.cuda.empty_cache()

# 设置内存增长
torch.cuda.set_per_process_memory_fraction(0.8, 0)
```

### 批处理优化
- **小文件合并**: 批量处理小音频文件
- **异步 IO**: 使用异步方式读写文件
- **缓存优化**: 充分利用本地缓存

## 🎵 创作建议

### 音乐风格搭配
- **流行**: 适合爱情、友情、励志主题
- **摇滚**: 适合青春、叛逆、激情主题
- **民谣**: 适合乡愁、叙事、生活主题
- **电子**: 适合科技、未来、派对主题

### 歌词创作要点
1. **主题明确**: 确定核心的情感和故事
2. **形象生动**: 使用具体的视觉、听觉描述
3. **韵律工整**: 注意押韵和节奏感
4. **结构清晰**: 主歌铺垫，副歌渲染，桥段升华

### 演唱表达技巧
- **情感投入**: 让录音带有真实情感
- **节奏稳定**: 保持稳定的语速和节奏
- **音准准确**: 尽量唱准音高
- **发音清晰**: 字正腔圆，便于 AI 学习

---

**🎉 恭喜你！现在你已经掌握了 AI 音乐创作师的基本使用方法。开始使用你的创意创作第一首 AI 音乐吧！**

如有任何问题，随时查阅详细文档或联系技术支持团队。

**快乐创作，让 AI 助力你的音乐梦想！** 🎼✨