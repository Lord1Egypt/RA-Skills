# **🎵 MP4 to MP3 Extractor (OpenClaw Skill)**

**高效、智能的本地音频提取工具** 这是一个为 [OpenClaw](https://github.com/openclaw/openclaw) 量身定制的自动化 Skill。它能递归扫描目录，利用 FFmpeg 将 .mp4 视频提取为高质量 .mp3 音频，同时**完美保留原始文件夹层级结构**。

## **✨ 核心特性**

* **📂 完美的结构保持**：自动映射源目录的多级子文件夹到目标目录，确保输出井然有序。  
* **🤖 自动化环境 (Self-bootstrapping)**：  
  * 首次运行自动创建 venv 虚拟环境。  
  * 智能兼容 Windows (Scripts/python.exe) 与 Linux/macOS 环境。  
  * 隔离运行，不污染全局 Python 环境。  
* **⚡ 工业级音频处理**：直接调用系统级 FFmpeg，默认输出 **192kbps** 高质量音频。  
* **📝 智能日志系统**：采用滚动日志技术，**仅保留最近 3 天记录**，平衡审计需求与磁盘空间。  
* **🧠 语义化调用**：深度集成 OpenClaw，Agent 可精准理解意图并自动推断路径。

## **🛠️ 环境依赖 (必读)**

在运行此 Skill 之前，请确保宿主机已安装：

1. **Python 3.8+**（建议安装 python3-venv 支持）。  
2. **FFmpeg**：必须添加到系统环境变量 PATH 中。  
   * *验证：终端输入 ffmpeg \-version 有输出即视为正常。*

**⚠️ 常见排错：若 Skill 状态显示为 blocked**

这通常是因为 OpenClaw 找不到 python 路径。

**修复步骤 (Linux示例)：**

\# 1\. 安装 venv 支持  
sudo apt update && sudo apt install python3-venv  
\# 2\. 建立软链接 (路径请根据实际 Python 安装位置修改)  
sudo ln \-s /usr/bin/python3 /usr/bin/python  
\# 3\. 重启服务  
systemctl \--user restart openclaw-gateway

## **🚀 安装指南**

### **1\. 自动安装 (CLI)**

根据你的环境执行以下命令：

**Linux / macOS:**

\# 视实际安装路径而定  
npx skills add \[https://github.com/wangminrui2022/mp4-to-mp3-extractor\](https://github.com/wangminrui2022/mp4-to-mp3-extractor)

**Windows:**

npx skills add D:\\path\\to\\mp4-to-mp3-extractor

### **2\. 重启生效**

安装完成后，进入 OpenClaw 目录重启 Gateway 即可在技能列表中看到它。

## **💻 使用方法**

### **命令行手动测试**

\# 进入技能目录  
cd \~/.openclaw/skills/mp4-to-mp3-extractor/

\# 运行转换脚本 (Linux)  
python scripts/extract.py "/path/to/videos" "/path/to/audio"

\# 运行转换脚本 (Windows)  
python scripts\\extract.py "F:\\Videos" "F:\\Audio"

### **在 OpenClaw 聊天中**

你可以直接对你的 Agent 说：

“帮我把“F:\命理学”文件夹里的 mp4 都转成 mp3”

“批量把“F:\命理学”这些视频转音频到“F:\命理学-音频”

“把这个视频https://www.douyin.com/jingxuan?modal_id=7611124804929785115下载下来，然后再提取音频”

## **📁 存储说明**

* **代码目录**：\~/.openclaw/skills/mp4-to-mp3-extractor/  
* **日志查看**：执行过程中的详细日志可在技能目录下的 logs/ 文件夹中找到。