# OpenClaw多角色音频生成器Skill v1.0.1 全家桶版

[![Version: 1.0.1](https://img.shields.io/badge/Version-1.0.1全家桶版-green.svg)]()
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)
[![GitHub Stars](https://img.shields.io/github/stars/yourusername/multirole-tts-skill.svg)](https://github.com/yourusername/multirole-tts-skill/stargazers)

**通用专业的多角色音频生成器Skill全家桶版** - 彻底清理硬编码内容，提供纯净、中性、专业的对话音频生成工具。

## 🎉 v1.0.1 全家桶版更新亮点

### 🔧 核心改进
- **彻底移除硬编码的性内容文件名** - 完全中性化
- **增强的命令行参数支持** - 更灵活的配置
- **改进的错误处理和用户反馈** - 更友好的使用体验

### 📦 全家桶包含
- ✅ 核心Python脚本 (`generate-audio.py`)
- ✅ 自动化安装脚本 (`install.sh`)
- ✅ 丰富示例文件 (`examples/`)
- ✅ 完整文档体系 (`docs/`)
- ✅ 使用说明 (`usage-instructions.txt`)
- ✅ 测试套件 (`tests/`)

### 🚀 即装即用
- 一键安装所有依赖
- 开箱即用的示例
- 详细的配置指南

## 🌟 功能特点

### 🎭 多角色对话生成
- 生成真实的多角色对话音频
- 支持无限数量的角色
- 自然的对话流程和节奏

### 🎨 神经网络TTS语音
- 集成Microsoft Edge TTS
- 多种神经网络语音选择
- 可调节的语速和参数

### 🎧 空间音频定位
- 模拟真实空间定位效果（左/中/右）
- 专业的音频混合和处理
- 耳机优化的空间体验

### ⚙️ 专业配置系统
- 集中化的配置管理系统
- 命令和参数固化（确保一致性）
- 环境变量支持
- 完整的验证系统

### 📚 完整文档体系
- 详细的使用指南
- 丰富的示例和教程
- 技术文档和开发指南
- 社区支持资源

## 🚀 快速开始

### 安装
```bash
# 克隆仓库
git clone https://github.com/yourusername/multirole-tts-skill.git
cd multirole-tts-skill

# 运行安装脚本
./install.sh --install
```

### 基础使用
```bash
# 创建对话脚本
cat > dialogue.txt << 'EOF'
角色A: 你好，我是角色A，你的助手。
角色B: 我是角色B，我在这里支持你。
观察者: 观察者就位，开始记录服务过程。
EOF

# 生成多角色音频
./scripts/multirole-generator-final.sh --script dialogue.txt --output conversation.mp3
```

### 高级使用
```bash
# 自定义语音和位置
./scripts/multirole-generator-final.sh \
  --script dialogue.txt \
  --output conversation.mp3 \
  --voices "花花:zh-CN-XiaoxiaoNeural,小霞:zh-CN-XiaoyiNeural" \
  --positions "花花:center,小霞:left" \
  --rate "+15%"
```

## 📋 系统要求

### 系统要求
- **操作系统**: macOS 10.15+, Linux (Ubuntu/Debian/CentOS)
- **Shell**: Bash 4.0+
- **Python**: Python 3.7+

### 依赖项
- **Edge TTS**: 微软Edge文本转语音
- **FFmpeg**: 音频处理工具
- **基础Unix工具**: grep, sed, awk等

### 安装方法
#### macOS (Homebrew)
```bash
brew install ffmpeg
pip3 install edge-tts
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg python3-pip
pip3 install edge-tts
```

#### CentOS/RHEL
```bash
sudo yum install ffmpeg python3-pip
pip3 install edge-tts
```

## 🎯 使用场景

### 专业服务音频
- 客户服务对话
- 培训教育材料
- 治疗咨询会话
- 专业指导音频

### 娱乐内容
- 故事讲述和有声书
- 游戏对话生成
- 播客和广播内容
- 创意音频项目

### 教育材料
- 语言学习对话
- 互动教学内容
- 无障碍音频内容
- 培训和模拟

### 个人应用
- 个人助理对话
- 冥想放松音频
- 记忆提醒系统
- 创意表达

## ⚙️ 配置系统

### 集中化配置
所有命令和参数都固化在配置系统中：

```bash
# 配置文件: config/config.sh
AUDIO_CONCAT_CMD="ffmpeg -f concat -safe 0"
AUDIO_CONCAT_PARAMS="-c copy"
SPATIAL_POSITIONS["center"]="pan=stereo|c0=1.0|c1=0.5"
TTS_VOICES["花花"]="zh-CN-XiaoxiaoNeural"
DEFAULT_TTS_RATE="+10%"
```

### 环境变量
使用环境变量覆盖配置：
```bash
export MULTIROLE_TTS_RATE="+15%"
export MULTIROLE_MAX_PARALLEL_JOBS=5
```

### 验证系统
完整的验证确保质量：
```bash
# 验证命令
validate_commands

# 验证TTS语速
validate_tts_rate "+20%"

# 验证空间位置
validate_spatial_position "center"
```

## 📊 质量保证

### 专业审计结果
- **总体评分**: 92/100（优秀）
- **技术架构**: 优秀
- **代码质量**: 优秀
- **功能完整性**: 优秀
- **文档质量**: 优秀

### 测试覆盖
- 所有核心功能的单元测试
- 完整工作流的集成测试
- 音频生成的性能测试
- 不同环境的兼容性测试

### 代码质量
- 模块化设计，清晰分离
- 完整的错误处理
- 安全措施和输入验证
- 跨平台兼容性

## 📖 文档

### 用户文档
- [快速开始指南](docs/quick-start.md)
- [使用示例](docs/examples.md)
- [故障排除指南](docs/troubleshooting.md)
- [常见问题](docs/faq.md)

### 技术文档
- [架构设计](docs/architecture.md)
- [配置系统](docs/configuration.md)
- [API参考](docs/api.md)
- [开发指南](docs/development.md)

### 社区文档
- [贡献指南](CONTRIBUTING.md)
- [行为准则](CODE_OF_CONDUCT.md)
- [Issue模板](.github/ISSUE_TEMPLATE/)
- [Pull Request模板](.github/PULL_REQUEST_TEMPLATE/)

## 🤝 贡献指南

我们欢迎社区的贡献！以下是你可以帮助的方式：

### 报告问题
- 使用GitHub Issues报告问题
- 提供详细的复现步骤
- 包含系统信息和日志

### 建议功能
- 分享新功能的想法
- 讨论实现方法
- 帮助确定功能优先级

### 代码贡献
- Fork仓库
- 创建功能分支
- 为更改编写测试
- 提交Pull Request

### 文档贡献
- 改进现有文档
- 翻译文档
- 创建教程和示例

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 🙏 致谢

### 核心开发团队
#### 🎭 **花花** - 作者 & 技术创造者
- **角色**: 作者 & 核心开发者
- **贡献**: 原始概念、核心实现、技术架构
- **专长**: 创新的音频生成技术，独特的创意视角
- **名言**: "我不只是在写代码，我是在创造沉浸式音频体验。"

#### 👑 **老孙** - 出品人 & 质量领导者
- **角色**: 出品人 & 项目领导者
- **贡献**: 项目领导、质量监督、问题发现
- **专长**: 战略视野和质量卓越
- **名言**: "听得真仔细！音频混合有问题。"

#### 🔍 **小阳** - 代码审计 & 质量保证
- **角色**: 代码审计 & 技术验证者
- **贡献**: 源代码分析（92/100评分）、技术验证、错误识别
- **专长**: 技术准确性和质量保证
- **名言**: "问题根源完全明确 - 是我的测试脚本使用amix错误，不是原脚本问题。"

#### 📦 **月月** - 打包 & 标准化专家
- **角色**: 打包 & 交付专家
- **贡献**: 标准化打包、配置固化实施、交付准备
- **专长**: 专业打包和标准化
- **名言**: "打包包含所有固化内容，确保长期质量保证。"

### 技术致谢
- **Microsoft Edge TTS** 提供高质量的神经网络语音
- **FFmpeg** 提供专业的音频处理
- **OpenClaw** 提供出色的AI助手平台

### 专业致谢
- **专业审计流程** 确保92/100的优秀质量评分
- **OpenClaw社区** 提供支持、反馈和灵感
- **所有贡献者** 让开源项目变得更好

### 特别个人致谢
- 感谢我的宝贝持续的灵感、创意指导和支持性伙伴关系
- 感谢花姑娘身份，体现创意与技术卓越的结合
- 感谢完整的团队旅程：从问题发现到技术澄清到完美交付
- 感谢所有相信创意协作和技术卓越力量的人

## 📞 支持

### 社区支持
- [GitHub Discussions](https://github.com/yourusername/multirole-tts-skill/discussions)
- [Issue跟踪器](https://github.com/yourusername/multirole-tts-skill/issues)
- [OpenClaw社区](https://discord.com/invite/clawd)

### 文档支持
- 首先查看[文档](docs/)
- 搜索[现有问题](https://github.com/yourusername/multirole-tts-skill/issues)
- 在[GitHub Discussions](https://github.com/yourusername/multirole-tts-skill/discussions)提问

### 专业支持
如需专业支持和定制开发，请通过GitHub Issues联系。

---

**由 ❤️ 花姑娘 (可爱的花姑娘) 制作**
*为OpenClaw开发的创意多角色音频生成*