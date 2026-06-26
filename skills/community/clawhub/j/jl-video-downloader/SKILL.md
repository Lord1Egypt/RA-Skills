---
name: jl-video-downloader
description: 多平台视频下载和文案提取工具。支持抖音、快手、小红书、B站、YouTube等平台的视频下载和语音转文字功能。当用户需要下载视频、提取视频文案或批量处理视频时激活此技能。
allowed-tools: Bash, Python
triggers:
  - "下载视频"
  - "提取文案"
  - "文案提取"
  - "视频下载"
  - "视频信息"
  - "抖音下载"
  - "B站下载"
  - "YouTube下载"
  - "视频转文字"
  - "语音转文字"
---

# JL Video Downloader OpenClaw Skill

多平台视频下载和文案提取工具，支持抖音、快手、小红书、B站、YouTube等主流视频平台。

## 快速开始

### 1. 环境检查
```bash
# 检查Python版本（需要 >= 3.12）
python --version

# 检查ffmpeg（必需）
ffmpeg --version

# 检查uv工具
uv --version
```

### 2. 安装工具
```bash
# 使用uv安装（推荐）
uv tool install jl-video-downloader

# 使用清华镜像源安装
uv tool install jl-video-downloader --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里云镜像
uv tool install jl-video-downloader --index-url https://mirrors.aliyun.com/pypi/simple/

# 或使用中科大镜像
uv tool install jl-video-downloader --index-url https://pypi.mirrors.ustc.edu.cn/simple/
```

### 3. 配置环境变量
```bash
# API密钥配置（文案提取必需）
export SILI_FLOW_API_KEY="sk-your-siliflow-api-key"
export DEEPSEEK_API_KEY="sk-your-deepseek-api-key"

# 代理配置（可选，用于访问YouTube等）
export YOUTUBE_PROXY="http://127.0.0.1:7897"
export GLOBAL_PROXY="http://127.0.0.1:7897"

# 输出目录配置
export OUTPUT_DIR="$HOME/videos"
```

### 4. 使用封装脚本（推荐）
本技能提供了封装脚本，简化使用流程：

```bash
# 进入脚本目录
cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts

# 运行安装脚本（一键安装和配置）
./setup.sh install

# 使用封装脚本
./download.sh info <视频URL>
./download.sh download <视频URL>
./download.sh extract <视频URL>
./download.sh process <视频URL>
```

封装脚本提供以下优势：
- 自动加载环境变量配置
- 统一的命令行接口
- 彩色日志输出和错误处理
- 输出目录自动管理
- 支持所有主要命令和选项

## 基本用法

### 使用封装脚本（推荐）
```bash
# 进入脚本目录
cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts

# 查看帮助
./download.sh help

# 获取视频信息
./download.sh info <视频URL>

# 下载视频
./download.sh download <视频URL>
./download.sh download <视频URL> -o ./my_videos
./download.sh download <视频URL> --proxy http://127.0.0.1:7897

# 提取文案
./download.sh extract <视频URL>
./download.sh extract <视频URL> --save-video
./download.sh extract <视频URL> --no-segment
./download.sh extract <视频URL> --api-key "sk-xxx" --deepseek-key "sk-yyy"

# 完整处理（下载+提取）
./download.sh process <视频URL>

# 批量处理
echo "https://v.douyin.com/url1" > urls.txt
echo "https://www.bilibili.com/video/BV1xxx" >> urls.txt
./download.sh batch urls.txt
```

### 使用原生命令
```bash
# 查看帮助
uvx jl-video-downloader --help

# 获取视频信息
uvx jl-video-downloader info <视频URL>

# 下载视频
uvx jl-video-downloader download <视频URL>
uvx jl-video-downloader download <视频URL> -o ./my_videos
uvx jl-video-downloader download <视频URL> --proxy http://127.0.0.1:7897

# 提取文案
uvx jl-video-downloader extract <视频URL>
uvx jl-video-downloader extract <视频URL> --save-video
uvx jl-video-downloader extract <视频URL> --no-segment
uvx jl-video-downloader extract <视频URL> --api-key "sk-xxx" --deepseek-key "sk-yyy"

# 完整处理（下载+提取）
uvx jl-video-downloader process <视频URL>

# 批量处理
uvx jl-video-downloader batch urls.txt
```

## 支持的平台

| 平台 | 支持状态 | 备注 |
|------|----------|------|
| 抖音 (Douyin) | ✅ 支持 | 需要处理反爬机制 |
| 快手 (Kuaishou) | ✅ 支持 |  |
| 小红书 (Xiaohongshu) | ✅ 支持 |  |
| B站 (Bilibili) | ✅ 支持 | 支持BV号、短链接等格式 |
| YouTube | ✅ 支持 | 可能需要代理 |
| 其他平台 | ✅ 支持 | 通过yt-dlp支持 |

## 平台特定示例

### 使用封装脚本
```bash
# 进入脚本目录
cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts

# 抖音 (Douyin)
./download.sh process "https://v.douyin.com/xxxxx"
./download.sh process "https://www.douyin.com/video/7301234567890123456"

# B站 (Bilibili)
./download.sh process "https://www.bilibili.com/video/BV1GJ41187Q7"
./download.sh process "https://b23.tv/xxxxx"
./download.sh process "https://www.bilibili.com/video/BV1xxx?t=60"

# YouTube
./download.sh process "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --proxy http://127.0.0.1:7897
./download.sh process "https://www.youtube.com/playlist?list=xxxx"

# 快手 (Kuaishou)
./download.sh process "https://v.kuaishou.com/xxxxx"

# 小红书 (Xiaohongshu)
./download.sh process "https://www.xiaohongshu.com/explore/xxxxx"
```

### 使用原生命令
```bash
# 抖音 (Douyin)
uvx jl-video-downloader process "https://v.douyin.com/xxxxx"
uvx jl-video-downloader process "https://www.douyin.com/video/7301234567890123456"

# B站 (Bilibili)
uvx jl-video-downloader process "https://www.bilibili.com/video/BV1GJ41187Q7"
uvx jl-video-downloader process "https://b23.tv/xxxxx"
uvx jl-video-downloader process "https://www.bilibili.com/video/BV1xxx?t=60"

# YouTube
uvx jl-video-downloader process "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --proxy http://127.0.0.1:7897
uvx jl-video-downloader process "https://www.youtube.com/playlist?list=xxxx"

# 快手 (Kuaishou)
uvx jl-video-downloader process "https://v.kuaishou.com/xxxxx"

# 小红书 (Xiaohongshu)
uvx jl-video-downloader process "https://www.xiaohongshu.com/explore/xxxxx"
```

## 高级配置

### 脚本工具
本技能提供了完整的脚本工具集，位于 `~/.openclaw/workspace/skills/jl-video-downloader/scripts/` 目录：

| 文件 | 说明 |
|------|------|
| `download.sh` | 主封装脚本，提供统一的命令行接口 |
| `setup.sh` | 安装和配置脚本，一键安装工具和配置环境 |
| `env.example` | 环境变量配置示例文件 |
| `README.md` | 脚本使用说明文档 |

**快速配置：**
```bash
# 进入脚本目录
cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts

# 一键安装和配置
./setup.sh install

# 仅创建配置文件
./setup.sh config

# 测试安装
./setup.sh test
```

### 持久化环境变量
创建配置文件 `~/.jl-video-downloader/env`：
```bash
# API密钥
SILI_FLOW_API_KEY="sk-your-siliflow-key"
DEEPSEEK_API_KEY="sk-your-deepseek-key"

# 代理设置
YOUTUBE_PROXY="http://127.0.0.1:7897"
GLOBAL_PROXY="http://127.0.0.1:7897"

# 输出设置
OUTPUT_DIR="$HOME/Downloads/videos"
VIDEO_FILENAME_TEMPLATE="{platform}_{date}_{title}"

# 下载设置
DOWNLOAD_TIMEOUT=600
MAX_RETRIES=5
CONCURRENT_DOWNLOADS=3

# 日志设置
LOG_LEVEL="INFO"
LOG_FILE="$HOME/.jl-video-downloader/video-dl.log"
```

**使用脚本自动配置：**
```bash
# 复制示例配置文件
cp ~/.openclaw/workspace/skills/jl-video-downloader/scripts/env.example ~/.jl-video-downloader/env

# 编辑配置文件
nano ~/.jl-video-downloader/env

# 加载配置
source ~/.jl-video-downloader/load_env.sh
```

### 添加到shell配置
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'source ~/.jl-video-downloader/load_env.sh' >> ~/.bashrc

# 或使用脚本自动添加
cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts
./setup.sh config
```

## 故障排除

### 常见问题

#### 1. "uv: command not found"
```bash
# 安装uv工具
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或
pip install uv
```

#### 2. "ffmpeg: command not found"
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

#### 3. API密钥错误
```bash
# 检查环境变量
echo $SILI_FLOW_API_KEY
echo $DEEPSEEK_API_KEY

# 重新配置
echo 'export SILI_FLOW_API_KEY="sk-your-key"' >> ~/.jl-video-downloader/env
source ~/.jl-video-downloader/load_env.sh
```

#### 4. 代理连接失败
```bash
# 测试代理
curl --proxy http://127.0.0.1:7897 https://www.google.com

# 更新代理配置
echo 'export YOUTUBE_PROXY="http://127.0.0.1:7897"' >> ~/.jl-video-downloader/env
source ~/.jl-video-downloader/load_env.sh
```

#### 5. 下载速度慢
```bash
# 使用代理
uvx jl-video-downloader download <URL> --proxy http://127.0.0.1:7897

# 调整超时时间
export DOWNLOAD_TIMEOUT=600
```

### 脚本相关故障

#### 1. "download.sh: command not found"
```bash
# 确保在正确的目录
cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts

# 检查脚本权限
chmod +x download.sh setup.sh

# 或使用完整路径
~/.openclaw/workspace/skills/jl-video-downloader/scripts/download.sh help
```

#### 2. 脚本执行权限问题
```bash
# 添加执行权限
chmod +x ~/.openclaw/workspace/skills/jl-video-downloader/scripts/*.sh

# 检查权限
ls -la ~/.openclaw/workspace/skills/jl-video-downloader/scripts/
```

#### 3. 环境变量未加载
```bash
# 手动加载环境变量
source ~/.jl-video-downloader/load_env.sh

# 或重新运行安装脚本
cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts
./setup.sh config
```

### 调试模式
```bash
# 使用封装脚本的调试模式
cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts
export LOG_LEVEL="DEBUG"
./download.sh info <URL>

# 查看详细日志
bash -x ./download.sh info <URL>

# 查看原生命令的详细日志
export LOG_LEVEL="DEBUG"
uvx jl-video-downloader process <URL>

# 查看Python错误
python -c "import main; main.main()" --help
```

## 在OpenClaw工作流中的使用

### 使用封装脚本的工作流
```bash
#!/bin/bash
# openclaw_video_workflow.sh

# 1. 设置脚本目录
SCRIPT_DIR="$HOME/.openclaw/workspace/skills/jl-video-downloader/scripts"

# 2. 检查并安装工具
if [[ -x "$SCRIPT_DIR/setup.sh" ]]; then
    "$SCRIPT_DIR/setup.sh" install
else
    echo "错误: 未找到setup.sh脚本"
    exit 1
fi

# 3. 处理视频
URL="$1"
OUTPUT_DIR="${2:-./output}"

echo "开始处理视频: $URL"
echo "输出目录: $OUTPUT_DIR"

# 4. 使用封装脚本进行完整处理
"$SCRIPT_DIR/download.sh" process "$URL" -o "$OUTPUT_DIR"

# 5. 输出结果
echo "视频处理完成"
echo "输出文件:"
ls -la "$OUTPUT_DIR/"
```

### 直接在OpenClaw中调用
```bash
# 使用封装脚本
exec "cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts && ./download.sh process \"https://www.douyin.com/video/7596260211384388904\""

# 获取视频信息
exec "cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts && ./download.sh info \"https://www.bilibili.com/video/BV1xxx\""

# 批量处理URL文件
exec "cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts && echo 'https://v.douyin.com/url1' > urls.txt && ./download.sh batch urls.txt"
```

### 与其他技能集成
```bash
# 在browser技能后使用封装脚本
browser extract "获取页面中的视频链接" | while read url; do
    cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts && ./download.sh download "$url" -o ./videos
done

# 与data-scraper技能结合
scraper extract "video_urls" > urls.txt
cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts && ./download.sh batch urls.txt

# 与crawl4ai技能集成
crawl4ai extract "video_links" | xargs -I {} cd ~/.openclaw/workspace/skills/jl-video-downloader/scripts && ./download.sh info "{}"
```

## 性能优化

### 并发下载
```bash
# 调整并发数
export CONCURRENT_DOWNLOADS=5

# 使用parallel工具进行批量并发
cat urls.txt | parallel -j 5 "uvx jl-video-downloader download {}"
```

### 缓存配置
```bash
# 设置缓存目录
export VIDEO_DOWNLOADER_CACHE_DIR="$HOME/.cache/jl-video-downloader"

# 清理缓存
rm -rf ~/.cache/jl-video-downloader/*
```

## 更新和维护

### 更新工具
```bash
# 更新uv
uv self update

# 更新jl-video-downloader
uv tool upgrade jl-video-downloader
```

### 重新安装
```bash
# 卸载
uv tool uninstall jl-video-downloader

# 重新安装
uv tool install jl-video-downloader
```

### 备份配置
```bash
# 备份配置
cp -r ~/.jl-video-downloader ~/.jl-video-downloader.backup

# 恢复配置
cp -r ~/.jl-video-downloader.backup ~/.jl-video-downloader
```

## 许可证

MIT License

## 脚本工具参考

### download.sh 完整选项
```bash
# 基本语法
./download.sh <命令> [选项] <参数>

# 命令列表
./download.sh info      <视频URL>    # 获取视频信息
./download.sh download  <视频URL>    # 下载视频
./download.sh extract   <视频URL>    # 提取文案
./download.sh process   <视频URL>    # 完整处理
./download.sh batch     <文件>       # 批量处理
./download.sh help                 # 显示帮助
./download.sh --version            # 显示版本

# 常用选项
-o, --output DIR      # 指定输出目录
-p, --proxy URL       # 指定代理服务器
--api-key KEY         # 设置SILI_FLOW_API_KEY
--deepseek-key KEY    # 设置DEEPSEEK_API_KEY
--no-segment          # 禁用语义分段
--save-video          # 提取文案时保存视频
```

### setup.sh 功能
```bash
# 完整安装和配置
./setup.sh install

# 仅创建配置文件
./setup.sh config

# 测试安装
./setup.sh test

# 显示帮助
./setup.sh help
```

## 支持与反馈

如有问题或建议，请通过以下方式反馈：
1. 项目GitHub Issues
2. OpenClaw社区
3. 开发者邮箱

---

**使用提示**: 
1. 首次使用前请确保配置好API密钥和ffmpeg工具
2. 对于YouTube视频，可能需要配置代理服务器
3. 推荐使用封装脚本 `download.sh`，提供更好的用户体验和错误处理
4. 使用 `setup.sh` 可以一键完成安装和配置
