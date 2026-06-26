# 龙虾电台 Skill 更新日志

## 版本 1.0.0 (2026-03-04)

### 🎉 初始发布

#### 核心功能
- ✅ 个性化电台生成
- ✅ 多主题/标签支持
- ✅ 定时推送（使用OpenClaw Cron）
- ✅ 多音色选择（5种中文音色）
- ✅ 情感表达（5种情感类型）
- ✅ 音频文件管理
- ✅ 配置管理（MEMORY.md集成）

#### TTS集成
- ✅ Qwen3-TTS Provider（主要）
  - 支持0.6B和1.7B模型
  - 支持声音克隆（3秒样本）
  - 支持语音设计（文字描述）
  - 支持多语言和多方言
  - 实时流式输出（97ms延迟）
  
- ✅ Ollama TTS Provider（备用）
  - 支持Ollama托管的TTS模型

#### 文档
- ✅ README.md - 项目说明和快速开始
- ✅ INSTALL.md - 详细安装指南
- ✅ QUICKSTART.md - 快速开始指南
- ✅ QWEN3TTS_GUIDE.md - Qwen3-TTS详细使用说明
- ✅ EXAMPLES.md - 使用示例
- ✅ LICENSE - MIT许可证

#### 脚本工具
- ✅ generate_radio.py - 生成电台
- ✅ configure_tts.py - 配置TTS
- ✅ list_radios.py - 列出历史电台
- ✅ install.sh - 一键安装脚本
- ✅ package_skill.py - 打包工具
- ✅ verify_all.py - 完整验证脚本

#### 测试
- ✅ test_skill.py - 基础功能测试
- ✅ verify_all.py - 完整验证测试

---

## 重要更新说明

### Qwen3-TTS模型集成

**问题**: Qwen3-TTS模型不在Ollama公共仓库中

**解决方案**: 
1. 创建了Qwen3TTSProvider，支持从HuggingFace和ModelScope下载模型
2. 提供了三种模型下载方法
3. 支持自动下载（首次使用时）
4. 创建了详细的Qwen3-TTS使用指南

**模型下载方法**:

```bash
# 方法1：HuggingFace
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base

# 方法2：ModelScope（国内推荐）
python -c "from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-Base', cache_dir='./models')"

# 方法3：自动下载（首次使用时）
python scripts/generate_radio.py --topics "测试" --tags "测试"
```

---

## 系统要求

### 最低配置（Qwen3-TTS-12Hz-0.6B-Base）
- CPU: 任意现代CPU
- 内存: 8GB RAM
- 存储: 5GB可用空间
- GPU: 可选（推荐）

### 推荐配置（Qwen3-TTS-12Hz-0.6B-Base）
- GPU: NVIDIA显卡（支持CUDA）
- 显存: 4GB以上
- 内存: 16GB RAM
- 存储: 10GB可用空间

### 推荐配置（Qwen3-TTS-1.7B）
- GPU: NVIDIA显卡（RTX 3080及以上）
- 显存: 8GB以上（推荐16GB）
- 内存: 32GB RAM
- 存储: 20GB可用空间

---

## 安装验证

运行完整验证脚本：

```bash
cd lobster-radio-skill
python tests/verify_all.py
```

验证内容：
- ✅ 依赖包检查
- ✅ 模型文件检查
- ✅ TTS Provider检查
- ✅ 内容生成器检查
- ✅ 音频管理器检查
- ✅ 配置管理器检查
- ✅ 语音合成测试

---

## 使用示例

### 基础使用

```bash
# 生成电台
python scripts/generate_radio.py --topics "人工智能" --tags "科技"

# 配置音色
python scripts/configure_tts.py --voice xiaoxiao --emotion neutral

# 查看历史电台
python scripts/list_radios.py
```

### OpenClaw集成

```
User: 生成关于人工智能的电台
Bot: 🎙️ 正在为您生成人工智能主题电台...
     [生成中...]
     
     ✅ 您的电台已生成！
     📝 标题: 人工智能资讯
     🎧 [播放音频]
     📥 [下载链接]
```

---

## 文件结构

```
lobster-radio-skill/
├── SKILL.md                 # OpenClaw Skill定义
├── README.md               # 项目说明
├── INSTALL.md              # 安装指南
├── QUICKSTART.md           # 快速开始
├── QWEN3TTS_GUIDE.md       # Qwen3-TTS指南
├── EXAMPLES.md             # 使用示例
├── CHANGELOG.md            # 更新日志
├── LICENSE                 # MIT许可证
├── requirements.txt        # Python依赖
├── providers/              # TTS提供商
│   ├── tts_base.py        # TTS基类
│   ├── tts_factory.py     # 工厂模式
│   ├── qwen3_tts.py       # Qwen3-TTS实现
│   └── ollama_tts.py      # Ollama实现
├── scripts/                # 主脚本
│   ├── generate_radio.py  # 生成电台
│   ├── configure_tts.py   # 配置TTS
│   ├── list_radios.py     # 历史电台
│   ├── install.sh         # 安装脚本
│   └── package_skill.py   # 打包工具
├── utils/                  # 工具模块
│   ├── content_generator.py
│   ├── audio_manager.py
│   └── config_manager.py
├── tests/                  # 测试文件
│   ├── test_skill.py
│   └── verify_all.py
└── templates/              # 模板文件
    └── prompts/
        └── radio_content.txt
```

---

## 已知问题

### 1. 模型下载速度慢
**解决方案**: 使用ModelScope镜像（国内用户）

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

### 2. 显存不足
**解决方案**: 
- 使用0.6B模型而非1.7B
- 使用量化（8-bit或4-bit）
- 使用CPU模式

### 3. 生成速度慢
**解决方案**:
- 使用GPU加速
- 使用FP16精度
- 启用CUDA优化

---

## 下一步计划

- [ ] 添加更多音色
- [ ] 支持更多语言
- [ ] 优化生成速度
- [ ] 添加Web界面
- [ ] 支持音频效果处理
- [ ] 添加背景音乐
- [ ] 支持多播客格式

---

## 贡献

欢迎贡献！请查看 GitHub Issues 提交问题或建议。

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

- GitHub: https://github.com/your-repo/lobster-radio-skill
- OpenClaw: https://openclaw.ai
- Qwen3-TTS: https://github.com/QwenLM/Qwen3-TTS
