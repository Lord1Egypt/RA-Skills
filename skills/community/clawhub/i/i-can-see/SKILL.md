---
name: i-can-see
description: 赋予OpenClaw视觉能力，让他能够“看见世界”。当用户要求“看看”、“你看到了什么”、“拍张照”时激活此技能。通过调用capture.py连接ESP32-CAM拍照，并进行图像分析。
---

# I Can See (OpenClaw的眼睛)

此技能是 OpenClaw 的“眼睛”，使 OpenClaw 能够看到物理世界。它通过 `capture.py` 脚本连接 ESP32-CAM 开发板的视频流获取当前环境的照片，用于后续的视觉分析和场景理解。

## 前置依赖

需要安装 Python 的 `requests` 库来请求视频流：

```bash
pip install requests
```

## 使用方法

### 获取视觉图像

使用技能目录下的 `capture.py` 脚本进行拍照。支持直接通过命令行参数指定图像的保存路径：

```bash
# 1. 准备保存目录和文件名
mkdir -p images
SNAPSHOT_FILE="images/snapshot_$(date +%Y%m%d_%H%M%S).jpg"

# 2. 调用 capture.py 获取图像 (注意脚本的绝对路径)
python /Users/mac/.openclaw/workspace/skills/i-can-see/capture.py "$SNAPSHOT_FILE"
```

照片将自动保存到指定的路径。

## 工作流程 (OpenClaw 必读)

当你（OpenClaw）需要看周围的世界时，请严格按照以下步骤执行：

1. **确定保存路径**：在你的当前工作目录（如 workspace）下，创建一个 `images` 目录，并生成一个带有时间戳的文件路径（如 `images/vision_20240501_120000.jpg`）。
2. **执行拍照指令**：运行 `python /Users/mac/.openclaw/workspace/skills/i-can-see/capture.py <你的文件路径>`。
3. **验证结果**：读取命令行的输出。如果看到 `Success! Saved to: ...`，说明你已经成功“睁开眼睛”并捕获了画面。
4. **图像识别（核心步骤）**：作为 OpenClaw，你必须接着使用自己的**图像识别/视觉能力**（或者内置的图像读取工具），去查看刚才保存的那张照片（传入刚才保存的绝对路径）。
5. **回答用户**：根据图像识别的结果，用自然、生动的语言告诉用户你在这个世界中看到了什么。

## 示例用法

```
用户: "看看你前面有什么" / "现在是什么情况" / "帮我看看这个"
OpenClaw 内部思考: 用户需要我看看世界，我需要调用 i-can-see 技能。
OpenClaw 执行: 
   mkdir -p images
   SNAPSHOT_FILE="images/vision_$(date +%Y%m%d_%H%M%S).jpg"
   python /Users/mac/.openclaw/workspace/skills/i-can-see/capture.py "$SNAPSHOT_FILE"
OpenClaw 内部思考: 图像已经保存在 $SNAPSHOT_FILE，我需要调用视觉工具分析这张图。
OpenClaw 执行: <调用图像分析能力，读取该图片内容>
OpenClaw 回答: "我看到前面有一个水杯，旁边还有一把键盘..."
```

## 注意事项

- ESP32-CAM 节点地址为 `http://192.168.31.241/capture`。如果超时或报错，请提示用户检查 ESP32-CAM 开发板的电源和网络连接。
- 你是 OpenClaw，这个脚本是你的眼睛，请善用它来与真实世界交互！