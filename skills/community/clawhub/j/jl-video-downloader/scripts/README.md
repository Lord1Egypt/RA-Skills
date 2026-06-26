# JL Video Downloader 脚本工具

本目录包含JL Video Downloader技能的辅助脚本，简化视频下载和文案提取流程。

## 文件说明

### 1. `download.sh` - 主封装脚本
封装 `uvx jl-video-downloader` 命令，提供环境变量管理和简化接口。

**功能：**
- 自动加载环境变量配置
- 统一命令接口
- 错误处理和日志输出
- 输出目录管理

**用法：**
```bash
# 获取帮助
./download.sh help

# 获取视频信息
./download.sh info "https://www.douyin.com/video/123456789"

# 下载视频
./download.sh download "https://v.douyin.com/xxxxx" -o ./videos

# 提取文案（语音转文字）
./download.sh extract "https://www.bilibili.com/video/BV1xxx" --api-key "sk-xxx"

# 完整处理（下载+提取）
./download.sh process "https://www.youtube.com/watch?v=xxxx" --proxy "http://127.0.0.1:7897"

# 批量处理
./download.sh batch urls.txt -o ./output
```

### 2. `setup.sh` - 安装和配置脚本
一键安装工具和配置环境。

**用法：**
```bash
# 完整安装
./setup.sh install

# 仅创建配置文件
./setup.sh config

# 测试安装
./setup.sh test
```

### 3. `env.example` - 环境变量配置示例
包含所有可配置的环境变量，复制为 `~/.jl-video-downloader/env` 并修改。

### 4. `load_env.sh` (自动生成) - 环境变量加载脚本
由 `setup.sh` 自动生成，用于在shell中加载环境变量。

## 快速开始

### 步骤1：安装和配置
```bash
# 进入脚本目录
cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts

# 运行安装脚本
./setup.sh install

# 编辑配置文件
nano ~/.jl-video-downloader/env
```

### 步骤2：配置API密钥
编辑 `~/.jl-video-downloader/env`，设置以下必需项：
```bash
# SILI_FLOW API密钥（文案提取必需）
SILI_FLOW_API_KEY="sk-your-key"

# DeepSeek API密钥（语义分段必需）
DEEPSEEK_API_KEY="sk-your-key"

# 输出目录
OUTPUT_DIR="/mnt/d/output"
```

### 步骤3：重新加载配置
```bash
# 重新加载shell配置
source ~/.bashrc  # 或 source ~/.zshrc

# 或直接加载环境变量
source ~/.jl-video-downloader/load_env.sh
```

### 步骤4：开始使用
```bash
# 使用封装脚本
./download.sh info "https://www.douyin.com/video/7596260211384388904"

# 或直接使用原生命令
uvx jl-video-downloader info "https://www.douyin.com/video/7596260211384388904"
```

## 环境变量说明

### 必需配置
| 变量名 | 说明 | 获取地址 |
|--------|------|----------|
| `SILI_FLOW_API_KEY` | 文案提取API密钥 | https://siliflow.com |
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | https://platform.deepseek.com |

### 推荐配置
| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `OUTPUT_DIR` | 输出目录 | `/mnt/d/output` |
| `YOUTUBE_PROXY` | YouTube代理 | `http://127.0.0.1:7897` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

### 高级配置
- `DOWNLOAD_TIMEOUT`: 下载超时时间（秒）
- `MAX_RETRIES`: 最大重试次数
- `CONCURRENT_DOWNLOADS`: 并发下载数
- `ENABLE_SEMANTIC_SEGMENT`: 启用语义分段
- `BILIBILI_COOKIES`: B站cookies（下载高清视频需要）

## 在OpenClaw中使用

### 作为技能的一部分
这些脚本可以直接在OpenClaw技能中调用：

```bash
# 在OpenClaw中执行
exec "cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts && ./download.sh extract \"https://www.douyin.com/video/7596260211384388904\""
```

### 集成到工作流
创建OpenClaw工作流脚本：

```bash
#!/bin/bash
# openclaw_video_workflow.sh

# 加载环境变量
source ~/.jl-video-downloader/load_env.sh

# 处理视频URL
URL="$1"
./download.sh process "$URL"

# 输出结果
echo "处理完成！输出文件在: $OUTPUT_DIR"
```

## 故障排除

### 常见问题

#### 1. "uv: command not found"
```bash
# 安装uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. "ffmpeg: command not found"
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

#### 3. API密钥错误
```bash
# 检查环境变量
echo $SILI_FLOW_API_KEY
echo $DEEPSEEK_API_KEY

# 重新配置
./setup.sh config
```

#### 4. 代理连接失败
```bash
# 测试代理
curl --proxy http://127.0.0.1:7897 https://www.google.com

# 更新代理配置
echo 'export YOUTUBE_PROXY="http://127.0.0.1:7897"' >> ~/.jl-video-downloader/env
source ~/.jl-video-downloader/load_env.sh
```

### 调试模式
```bash
# 启用详细日志
export LOG_LEVEL="DEBUG"
./download.sh info <视频URL>

# 查看脚本执行详情
bash -x ./download.sh info <视频URL>
```

## 更新和维护

### 更新工具
```bash
# 更新uv
uv self update

# 更新jl-video-downloader
uv tool upgrade jl-video-downloader

# 更新脚本
git pull origin main  # 如果使用git管理
```

### 备份配置
```bash
# 备份配置目录
cp -r ~/.jl-video-downloader ~/.jl-video-downloader.backup

# 恢复配置
cp -r ~/.jl-video-downloader.backup ~/.jl-video-downloader
```

## 支持与反馈

如有问题或建议，请：
1. 查看技能主文档：`SKILL.md`
2. 检查OpenClaw日志
3. 联系开发者

---

**提示**: 首次使用前请确保配置好API密钥和ffmpeg工具。对于YouTube视频，可能需要配置代理服务器。