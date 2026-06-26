# 使用指南

## 🎯 快速开始

### 1. 安装Skill
```bash
# 进入Skill目录
cd multirole-tts-skill-standard

# 运行安装脚本
./install.sh --install
```

### 2. 测试安装
```bash
# 测试Skill是否正常工作
./install.sh --test
```

### 3. 生成第一个音频
```bash
# 使用示例脚本生成音频
./scripts/multirole-generator-final.sh --script examples/basic-dialogue.txt --output my-first-dialogue.mp3
```

## 📝 脚本格式

### 基本格式
```
角色名: 对话内容
角色名: 对话内容
```

### 示例
```
角色A: 你好，我是角色A。
角色B: 我是角色B，很高兴见到你。
旁白: 对话开始记录。
```

### 规则说明
1. **角色标记**：角色名后跟冒号（如`角色A:`）
2. **对话内容**：冒号后的所有内容为对话
3. **空行**：空行会被忽略
4. **注释**：以`#`开头的行是注释
5. **多行对话**：不支持多行对话，每行必须是完整对话

## ⚙️ 配置选项

### 命令选项
```bash
./scripts/multirole-generator-final.sh [选项]
```

### 选项说明
| 选项 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `--script` | `-s` | 输入脚本文件（必需） | 无 |
| `--output` | `-o` | 输出音频文件 | `output.mp3` |
| `--voices` | `-v` | 角色声音配置 | `角色A:xiaoxiao,角色B:xiaoyi,旁白:yunxi` |
| `--positions` | `-p` | 空间位置配置 | `角色A:center,角色B:left,旁白:right` |
| `--rate` | `-r` | TTS语速调整 | `+10%` |
| `--help` | `-h` | 显示帮助信息 | 无 |

### 配置示例
```bash
# 基本使用
./scripts/multirole-generator-final.sh --script dialogue.txt --output audio.mp3

# 自定义声音
./scripts/multirole-generator-final.sh --script script.txt --voices "角色A:xiaoxiao,助手:xiaoyi"

# 自定义位置
./scripts/multirole-generator-final.sh --script script.txt --positions "主讲人:center,助手:left"

# 调整语速
./scripts/multirole-generator-final.sh --script script.txt --rate "+5%"
```

## 🎨 角色配置

### 预设角色
Skill预设了三个角色，可以直接使用：

| 角色 | 默认声音 | 默认位置 | 描述 |
|------|----------|----------|------|
| 角色A | zh-CN-XiaoxiaoNeural | center | 温柔专业女声 |
| 角色B | zh-CN-XiaoyiNeural | left | 温暖支持女声 |
| 观察者 | zh-CN-YunxiNeural | right | 中性分析声音 |

### 声音列表
Edge TTS支持的声音（部分）：
- `zh-CN-XiaoxiaoNeural` - 温柔女声（默认角色A）
- `zh-CN-XiaoyiNeural` - 温暖女声（默认角色B）
- `zh-CN-YunxiNeural` - 中性声音（默认观察者）
- `zh-CN-YunyangNeural` - 专业男声
- `zh-CN-XiaochenNeural` - 活泼女声

### 位置选项
- `center` - 中央位置
- `left` - 左侧位置
- `right` - 右侧位置
- `leftfront` - 左前方
- `rightfront` - 右前方

## 🔧 高级使用

### 自定义角色配置
创建配置文件`config.json`：
```json
{
  "roles": {
    "主讲人": {
      "voice": "zh-CN-XiaoxiaoNeural",
      "position": "center"
    },
    "助手": {
      "voice": "zh-CN-XiaoyiNeural", 
      "position": "left"
    }
  }
}
```

### 批量处理
创建批量处理脚本`batch-process.sh`：
```bash
#!/bin/bash
for script in scripts/*.txt; do
  output="${script%.txt}.mp3"
  ./scripts/multirole-generator-final.sh --script "$script" --output "$output"
done
```

### 集成到工作流
```bash
#!/bin/bash
# 完整工作流示例

# 1. 生成脚本
echo "角色A: 开始服务。" > service.txt
echo "角色B: 准备就绪。" >> service.txt

# 2. 生成音频
./scripts/multirole-generator-final.sh --script service.txt --output service.mp3

# 3. 播放音频
afplay service.mp3  # macOS
# 或 mpg123 service.mp3  # Linux
```

## 🐛 故障排除

### 常见问题

#### 1. Edge TTS未安装
```bash
# 安装Edge TTS
pip install edge-tts

# 或使用pip3
pip3 install edge-tts
```

#### 2. FFmpeg未安装
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

#### 3. 权限问题
```bash
# 设置脚本可执行权限
chmod +x scripts/*.sh
chmod +x install.sh
```

#### 4. 脚本解析失败
- 检查脚本格式是否正确
- 确保角色标记后是冒号（`:`）
- 检查文件编码（应为UTF-8）

#### 5. 音频生成失败
- 检查网络连接（Edge TTS需要网络）
- 检查磁盘空间
- 查看错误日志

### 错误信息
运行脚本时添加`--verbose`选项查看详细日志：
```bash
./scripts/multirole-generator-final.sh --script test.txt --output test.mp3 --verbose
```

## 📊 性能优化

### 生成速度优化
1. **使用SSD存储**：加快文件读写速度
2. **良好网络连接**：Edge TTS需要网络访问
3. **减少对话长度**：较短的对话生成更快
4. **并行处理**：可以修改脚本支持并行生成

### 音频质量优化
1. **调整语速**：使用`--rate`选项调整语速
2. **选择合适声音**：不同声音适合不同场景
3. **优化脚本**：自然的对话节奏
4. **后期处理**：可以使用Audacity等工具进一步优化

### 文件大小优化
1. **调整比特率**：修改FFmpeg参数调整比特率
2. **压缩音频**：生成后使用音频压缩工具
3. **删除中间文件**：脚本会自动清理中间文件

## 🔄 更新和维护

### 更新Skill
```bash
# 进入Skill目录
cd multirole-tts-skill

# 拉取最新代码
git pull origin main

# 重新安装
./install.sh --install
```

### 更新依赖
```bash
# 更新Edge TTS
pip install edge-tts --upgrade

# 更新FFmpeg
brew upgrade ffmpeg  # macOS
sudo apt upgrade ffmpeg  # Ubuntu/Debian
```

### 备份配置
建议备份自定义配置：
```bash
# 备份配置文件
cp config.json config.json.backup

# 备份示例脚本
cp -r examples/ examples-backup/
```

## 🤝 获取帮助

### 查看帮助
```bash
# 查看脚本帮助
./scripts/multirole-generator-final.sh --help

# 查看安装帮助
./install.sh --help
```

### 查看日志
```bash
# 查看生成日志
cat multirole-generator.log

# 查看安装日志
cat install.log
```

### 报告问题
1. 记录错误信息
2. 提供复现步骤
3. 包括系统信息
4. 在GitHub Issues中报告

---

**开始使用**：从`examples/`目录中的示例开始
**深入学习**：阅读技术文档了解实现细节
**贡献改进**：欢迎提交改进建议和代码