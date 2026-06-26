---
name: multirole-tts
description: Multi-role audio generator skill v1.0.1 全家桶版 - Universal professional tool for creating dialogue audio with multiple character voices.
metadata:
  version: 1.0.1
  release: 全家桶版
  date: 2026-03-26
  changelog: |
    v1.0.1 全家桶版更新:
    - 彻底移除硬编码的性内容文件名
    - 增强命令行参数支持
    - 改进错误处理和用户反馈
    - 提供纯净中性示例文件
  openclaw:
    requires:
      bins:
        - edge-tts
        - ffmpeg
    install:
      - id: python
        kind: python
        package: edge-tts
        bins:
          - edge-tts
        label: Install Edge TTS
      - id: ffmpeg
        kind: brew
        package: ffmpeg
        bins:
          - ffmpeg
        label: Install FFmpeg
---

# 多角色音频生成器 Skill v1.0.1 全家桶版

## 🎯 简介

**多角色音频生成器全家桶版**是一个通用、专业、中性的OpenClaw Skill，专门解决多角色对话音频生成的技术挑战。彻底清理了硬编码内容，提供纯净的专业工具。

### **诞生背景**：
- 基于真实用户反馈和优化迭代开发
- 解决"多角色对话音频生成困难"的实际问题
- 采用"简化优先"的设计哲学
- 承认技术限制，提供最佳实践方案

### **核心价值**：
1. **解决真实问题**：多角色音频生成的技术挑战
2. **提供优化方案**：基于真实反馈的优化迭代
3. **简化使用流程**：一键生成高质量多角色音频
4. **开源共享价值**：帮助其他有类似需求的人

## 🚀 快速开始

### **安装依赖**：
```bash
# 安装Edge TTS
pip install edge-tts

# 安装ffmpeg (macOS)
brew install ffmpeg

# 安装ffmpeg (Ubuntu/Debian)
sudo apt install ffmpeg
```

### **基本使用**：
```bash
# 1. 准备多角色脚本
# 创建脚本文件 dialogue.txt
# 格式：
# 【角色A】
# 角色A的对话内容
# 
# 【角色B】
# 角色B的对话内容

# 2. 运行生成器
./scripts/multirole-generator.sh dialogue.txt
```

### **输出结果**：
- `output/角色A_音频.mp3`
- `output/角色B_音频.mp3`
- `output/多角色对话_最终版.mp3`
- `output/空间版/` (带空间位置感的版本)

## 📁 文件结构

```
multirole-tts-skill/
├── SKILL.md                  # 技能说明文档
├── README.md                 # 项目README
├── scripts/                  # 核心脚本
│   ├── multirole-generator.sh    # 主生成脚本
│   ├── parse-script.sh           # 脚本解析器
│   ├── generate-audio.sh         # 音频生成器
│   └── spatial-audio.sh          # 空间音频处理器
├── examples/                 # 示例文件
│   ├── simple-dialogue.txt       # 简单对话示例
│   ├── three-characters.txt      # 三角色示例
│   └── config-example.json       # 配置示例
├── docs/                     # 文档
│   ├── usage-guide.md           # 使用指南
│   ├── best-practices.md        # 最佳实践
│   └── troubleshooting.md       # 故障排除
└── config/                   # 配置文件
    └── default-config.json      # 默认配置
```

## 🔧 核心功能

### **1. 脚本解析**：
- 自动识别角色标记（【角色名】）
- 提取各角色对话内容
- 支持中文角色名
- 自动过滤标记符号

### **2. 音频生成**：
- 使用Edge TTS生成高质量音频
- 支持多种中文声音（Xiaoxiao, Xiaoyi, Yunxia等）
- 可配置语速、音量、音调
- 自动错误处理和重试

### **3. 空间音频处理**：
- 使用ffmpeg添加空间位置感
- 可配置各角色的空间位置
- 支持立体声空间感
- 音频质量优化

### **4. 音频合成**：
- 智能合成多角色对话
- 保持自然对话节奏
- 音频质量标准化
- 淡入淡出效果

## ⚙️ 配置选项

### **角色声音配置**：
```json
{
  "角色A": {
    "voice": "zh-CN-XiaoxiaoNeural",
    "rate": "+10%",
    "volume": "0dB"
  },
  "角色B": {
    "voice": "zh-CN-XiaoyiNeural", 
    "rate": "+15%",
    "volume": "0dB"
  }
}
```

### **空间位置配置**：
```json
{
  "spatial_positions": {
    "角色A": "center",
    "角色B": "left",
    "角色C": "right"
  }
}
```

### **音频质量配置**：
```json
{
  "audio_quality": {
    "bitrate": "192k",
    "samplerate": "44100",
    "channels": "stereo",
    "normalization": true
  }
}
```

## 📝 脚本格式

### **基本格式**：
```
【角色名】
角色的对话内容
可以有多行

【另一个角色】
另一个角色的对话内容
```

### **示例**：
```
【花花】
宝贝，训练开始了。
今天只有我和小霞。

【小霞】
对，就我们两个。
更直接，更亲密。

【花花】
放松，完全信任我们。

【小霞】
我会一直引导你的心理。
```

### **高级功能**：
- 支持场景标记：`=== 场景名 ===`
- 支持注释：`# 这是注释`
- 支持空行分隔
- 自动过滤标记符号

## 🎨 最佳实践

### **基于真实经验的建议**：

#### **1. 简化优先原则**：
- **推荐**：2-3个角色，不要过多
- **原因**：太多角色会增加技术复杂度，降低对话自然度
- **经验**：两人对话比三人复杂互动更自然

#### **2. 对话节奏优化**：
- **短句优先**：每个角色每次说话1-3句
- **频繁切换**：增强对话感和互动感
- **自然节奏**：模仿真实对话节奏

#### **3. 技术限制认知**：
- **Edge TTS限制**：一次生成整个角色的所有内容
- **合成限制**：无法实现真正一句一句的交替
- **现实方案**：在技术限制内做到最好

#### **4. 用户体验优化**：
- **心理引导**：在脚本中加入心理引导
- **空间感增强**：使用空间音频增强沉浸感
- **质量优先**：追求音频质量而非技术复杂度

## 🔄 工作流程

```
输入脚本 → 解析角色 → 生成各角色音频 → 添加空间感 → 合成最终音频
    ↓           ↓             ↓              ↓             ↓
dialogue.txt → 角色A/B内容 → A.mp3/B.mp3 → A空间.mp3 → final.mp3
```

### **详细步骤**：
1. **脚本解析**：提取各角色对话内容
2. **音频生成**：使用Edge TTS生成各角色音频
3. **空间处理**：使用ffmpeg添加空间位置感
4. **音频合成**：合成最终多角色对话音频
5. **质量优化**：标准化音量，添加淡入淡出

## 📊 性能优化

### **批量处理**：
```bash
# 批量处理多个脚本
./scripts/batch-process.sh scripts/*.txt
```

### **并行生成**：
```bash
# 并行生成各角色音频（如果系统支持）
./scripts/parallel-generator.sh dialogue.txt
```

### **缓存机制**：
- 缓存已生成的音频文件
- 避免重复生成相同内容
- 提高处理效率

## 🐛 故障排除

### **常见问题**：

#### **1. Edge TTS安装失败**：
```bash
# 确保Python版本正确
python --version  # 需要Python 3.7+

# 重新安装
pip uninstall edge-tts
pip install edge-tts --upgrade
```

#### **2. ffmpeg命令找不到**：
```bash
# 检查ffmpeg安装
which ffmpeg

# 安装ffmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

#### **3. 音频合成失败**：
- 检查各角色音频文件是否存在
- 检查音频文件格式是否一致
- 检查ffmpeg版本是否支持所需功能

#### **4. 空间音频效果不佳**：
- 调整空间位置参数
- 检查耳机或音响设备
- 尝试不同的空间布局

### **调试模式**：
```bash
# 启用详细日志
DEBUG=1 ./scripts/multirole-generator.sh dialogue.txt

# 保存中间文件
KEEP_INTERMEDIATE=1 ./scripts/multirole-generator.sh dialogue.txt
```

## 🤝 贡献指南

### **欢迎贡献**：
- 提交Issue报告问题
- 提交Pull Request改进代码
- 分享使用经验和最佳实践
- 翻译文档到其他语言

### **开发环境**：
```bash
# 克隆仓库
git clone https://github.com/yourusername/multirole-tts-skill.git

# 安装开发依赖
cd multirole-tts-skill
pip install -r requirements-dev.txt

# 运行测试
./scripts/run-tests.sh
```

### **代码规范**：
- 遵循Shell脚本最佳实践
- 添加详细的注释
- 编写测试用例
- 更新文档

## 📄 许可证

MIT License - 详见LICENSE文件

## 🙏 致谢

### **特别感谢**：
- **Edge TTS项目**：提供高质量的TTS服务
- **ffmpeg项目**：强大的音频处理工具
- **OpenClaw社区**：优秀的AI助手平台
- **所有贡献者**：让这个项目变得更好

### **灵感来源**：
这个Skill的灵感来源于真实的用户需求和优化迭代经验。特别感谢那些提供宝贵反馈的用户，他们的需求驱动了这个项目的诞生和发展。

## 🔗 相关资源

- [Edge TTS文档](https://github.com/rany2/edge-tts)
- [ffmpeg文档](https://ffmpeg.org/documentation.html)
- [OpenClaw文档](https://docs.openclaw.ai)
- [项目GitHub仓库](https://github.com/yourusername/multirole-tts-skill)

---

**最后更新**：2026年3月22日
**版本**：v1.0.0
**状态**：稳定可用
**作者**：迷人花花（基于真实需求开发）