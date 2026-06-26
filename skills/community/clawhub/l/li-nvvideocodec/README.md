# li_nvvideocodec - NVIDIA AV1 视频压缩工具

**作者**: 北京老李 (beijingLL)  
**版本**: 1.0.0  
**兼容Agent**: hermes, openclaw, qwen-code

## 📋 简介

这是一个使用NVIDIA GPU硬件加速的AV1视频批量压缩工具。通过FFmpeg调用NVIDIA NVENC编码器，可以高效压缩视频文件，节省硬盘空间。

### 核心特性

- ✅ **智能验证** - 自动测试压缩效果，避免无效压缩
- ✅ **三种方案** - 保守/平衡/激进，满足不同需求
- ✅ **双平台** - 支持Windows和Ubuntu Linux
- ✅ **多Agent兼容** - hermes, openclaw, qwen-code
- ✅ **安全保护** - 原文件不删除，输出到独立目录

## 📁 目录结构

```
li_nvvideocodec/
├── SKILL.md              # Skill描述文件（通用）
├── skill.json            # 结构化配置（hermes/openclaw）
├── agent_interface.py    # Agent统一API接口
├── AGENT_USAGE.md        # Agent集成指南
├── README.md             # 本文件
└── scripts/
    └── compress_videos.py  # 主压缩脚本
```

## 🚀 快速开始

### 方式1：直接运行脚本

```bash
# 交互式模式
python scripts/compress_videos.py

# 命令行模式
python scripts/compress_videos.py -i "输入目录" -p B --no-confirm

# 测试模式
python scripts/compress_videos.py -i "输入目录" -p B --test --test-count 1
```

### 方式2：使用Agent统一接口

```bash
# 检查环境
python agent_interface.py --action check

# 分析视频
python agent_interface.py --action analyze -i "输入目录"

# 压缩视频
python agent_interface.py --action compress -i "输入目录" -p B --test
```

## 📊 压缩方案对比

| 方案 | 分辨率 | CRF | 帧率 | 音频 | 预估节省 | 适用场景 |
|------|--------|-----|------|------|----------|----------|
| **A** | 保持原样 | 23 | 保持 | 128k | 40-60% | 追求质量 |
| **B** ⭐ | 1280x720 | 24 | 24fps | 96k | 65-75% | **平衡推荐** |
| **C** | 1280x720 | 28 | 15fps | 64k | 78-85% | 最大节省 |

## 🤖 Agent集成

### hermes

在hermes配置中添加：

```json
{
  "skills": [
    {
      "name": "li_nvvideocodec",
      "type": "video_compression",
      "path": "/path/to/li_nvvideocodec",
      "entry": "agent_interface.py",
      "actions": ["check", "analyze", "compress"]
    }
  ]
}
```

### openclaw

在openclaw配置中添加：

```yaml
skills:
  - name: li_nvvideocodec
    description: "NVIDIA AV1视频压缩"
    script: agent_interface.py
    interpreter: python
    capabilities:
      - check_environment
      - analyze_videos
      - compress_videos
```

### qwen-code

Qwen Code可以直接使用，当用户提到"压缩视频"时自动推荐。

## ⚙️ 系统要求

### 必需

- **FFmpeg** - 需要支持av1_nvenc编码器
- **NVIDIA GPU** - GTX 1650及以上
- **NVIDIA驱动** - 已安装并正常
- **Python 3.7+** - 运行脚本

### 检查环境

```bash
# 检查FFmpeg
ffmpeg -version
ffmpeg -encoders | grep av1_nvenc

# 检查GPU
nvidia-smi

# 检查Python依赖
pip install tqdm
```

## 📝 使用示例

### 示例1：首次使用（测试模式）

```bash
python agent_interface.py --action compress \
  -i "E:\视频输出\docker-2021" \
  -p B \
  --test \
  --test-count 1
```

### 示例2：完整压缩

```bash
python agent_interface.py --action compress \
  -i "E:\视频输出\docker-2021" \
  -p B \
  --no-confirm
```

### 示例3：先分析再压缩

```bash
# 分析
python agent_interface.py --action analyze \
  -i "E:\视频输出\docker-2021"

# 根据分析结果压缩
python agent_interface.py --action compress \
  -i "E:\视频输出\docker-2021" \
  -p B
```

## ⚠️ 重要提示

### B站视频

如果视频来自B站等平台，可能已经被高度压缩：
- 再次压缩可能不会节省空间
- 脚本会自动检测并提示

### 原文件保护

- ✅ 原文件**不会删除**
- ✅ 输出到独立目录
- ✅ 可以安全对比测试

## 🔧 故障排除

### FFmpeg未找到

```bash
# Windows: 下载 https://ffmpeg.org/download.html
# Ubuntu:
sudo apt install ffmpeg
```

### 不支持av1_nvenc

- 更新FFmpeg到最新版本
- 确保NVIDIA驱动已安装

### GPU检测失败

- 检查NVIDIA驱动
- 运行 `nvidia-smi` 测试

## 📄 许可证

作者: 北京老李 (beijingLL)

本工具供个人学习和使用。

## 📞 联系

如有问题或建议，请联系作者。
