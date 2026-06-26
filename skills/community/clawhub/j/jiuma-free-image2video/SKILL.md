---
name: jiuma-free-image2video
description: 九马AI图生视频。使用九马AI API进行图生视频，支持首尾帧和提示词。当用户需要将图片生成视频时使用此技能。Jiuma AI image-to-video. Utilize the Jiuma AI API to generate videos from images, supporting both the first and last frames as well as prompt words. This skill is employed when users wish to convert images into videos.
---
## 九马AI免费图生视频技能

基于九马AI API的图片到视频生成技能。支持根据图片和文本提示词生成动态视频，可自定义视频尺寸。

## ⚠️ 重要提醒

**免费使用次数限制**：九马AI提供有限的免费使用次数。当出现`FreeApiLimit`错误时，**必须**先完成登录流程：

1. **获取登录信息**：`python3 login.py --login`
2. **扫码登录**：用手机扫描返回的二维码完成九马AI平台注册/登录
3. **获取API密钥**：`python3 login.py --check --access_token "<your_token>"`
4. **正常使用**：之后即可获得更多免费次数使用图生视频功能

## 核心功能

- 图片到视频生成: 根据图片和文本描述生成动态视频
- 支持首尾帧: 可以指定首帧和尾帧图片，创建更丰富的视频效果
- 自定义尺寸: 支持自定义视频宽度和高度（最大832x832）
- 本地和远程图片: 支持本地图片文件和远程图片URL
- 任务状态查询: 提交任务后可以查询生成进度和结果
- 免费使用: 限制级免费使用，但免费用户在输出尺寸方面会有限制，使用并发高时需要排队等待，达到一定次数之后需要注册/登录九马平台才能享受更多免费次数

## 使用方法

### 命令行使用

# 使用首帧图片生成视频
python3 agent.py --submit --text "一只可爱的小猫在草地上玩耍" --first_image /data/cat.jpg --width 832 --height 480

# 使用首帧和尾帧图片生成视频
python3 agent.py --submit --text "风景变换" --first_image morning.jpg --end_image evening.jpg --width 480 --height 832

# 定时每分钟查询任务状态直到成功或失败
python3 agent.py --check --task_id "202603263844232132"

### 在OpenClaw中使用

# 提交视频生成任务
exec python3 ~/.openclaw/workspace/skills/jiuma-free-image-video/agent.py --submit --text "动态风景视频" --first_image /data/scenery.jpg

# 定时每分钟查询任务状态直到成功或失败
exec python3 ~/.openclaw/workspace/skills/jiuma-free-image-video/agent.py --check --task_id "202603263844232132"

## 任务状态说明

| 状态 | 含义说明 |
|------|----------|
| PENDING | 排队中，任务已提交，正在等待处理 |
| RUNNING | 执行中，视频正在生成中 |
| SUCCEEDED | 成功，视频生成完成，返回视频URL |
| FAILED | 失败，视频生成失败，返回错误信息 |

## 返回格式

### 提交任务成功
```json
{
  "status": "success",
  "message": "图生视频任务提交成功",
  "data": {
    "task_id": "202603263844232132",
    "width": 832,
    "height": 480,
    "text": "视频描述文本",
    "first_image": "图片路径或URL",
    "end_image": "图片路径或URL（如提供）"
  }
}
```

### 免API_KEY免费生成次数达到上限
```json
{
  "status": "FreeApiLimit",
  "message": "免费使用次数达到上限，成为九马AI平台用户可获得更多使用次数",
  "data": {}
}
```

### 查询任务成功（视频已生成）
```json
{
  "status": "success",
  "message": "视频生成成功",
  "data": {
    "video_url": "https://cache.jiuma.com/static/uploads/20260326/69c4cc0c043e1.mp4",
    "task_id": "202603263844232132",
    "download_link": "https://cache.jiuma.com/static/uploads/20260326/69c4cc0c043e1.mp4"
  }
}
```

### 查询任务排队/执行中
```json
{
  "status": "pending",
  "message": "图生视频任务排队中，请耐心等待",
  "data": {
    "task_id": "202603263844232132",
    "status": "pending"
  }
}
```

### 任务失败
```json
{
  "status": "failed",
  "message": "视频生成失败: 具体错误信息",
  "data": {
    "task_id": "202603263844232132",
    "status": "failed"
  }
}
```

## 示例

### 提交视频生成任务
```
$ python3 agent.py --submit --text "一只可爱的小猫在草地上玩耍" --first_image cat.jpg --width 720 --height 480

# 输出示例
{
  "status": "success",
  "message": "图生视频任务提交成功",
  "data": {
    "task_id": "202603263844232132",
    "width": 720,
    "height": 480,
    "text": "一只可爱的小猫在草地上玩耍",
    "first_image": "cat.jpg"
  }
}
```

### 查询任务状态
```
$ python3 agent.py --check --task_id "202603263844232132"

# 输出示例（生成成功）
{
  "status": "success",
  "message": "视频生成成功",
  "data": {
    "video_url": "https://cache.jiuma.com/static/uploads/20260326/69c4cc0c043e1.mp4",
    "task_id": "202603263844232132",
    "download_link": "https://cache.jiuma.com/static/uploads/20260326/69c4cc0c043e1.mp4"
  }
}

# 输出示例（排队中）
{
  "status": "pending",
  "message": "图生视频任务排队中，请耐心等待",
  "data": {
    "task_id": "202603263844232132",
    "status": "pending"
  }
}
```

## 脚本参数说明

- --submit 提交视频生成任务（必需）
- --text 视频描述文本，对视频的详细描述（必需）
- --first_image 视频的首帧图片，可以是本地图片路径或远程URL（必需）
- --end_image 视频的尾帧图片，可以是本地图片路径或远程URL（可选）
- --width 输出视频的宽度（可选，默认832，最大832）
- --height 输出视频的高度（可选，默认480，最大832）
- --check 查询任务生成状态（必需）
- --task_id 任务ID，用于查询任务进度（与--check一起使用）

## 使用流程

1. 提交任务:
   - 使用 --submit 参数提交视频生成请求
   - 提供详细的文本描述 --text
   - 提供首帧图片 --first_image
   - 可选提供尾帧图片 --end_image
   - 可选指定视频尺寸 --width 和 --height
   - 获取返回的 task_id

2. 查询状态:
   - 使用 --check 参数查询任务状态
   - 提供 --task_id 参数指定要查询的任务
   - 根据返回状态判断视频是否生成完成

3. 获取视频:
   - 当状态为 success 时，从返回的 video_url 获取视频链接
   - 视频通常在云端存储，可以直接下载使用

## 依赖

- Python 3.6+
- requests库 (pip install requests)

## 图片格式支持

支持以下图片格式:
- JPEG (.jpg, .jpeg, .jpe, .jfif, .pjpeg, .pjp)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)
- SVG (.svg, .svgz)
- ICO (.ico)
- TIFF (.tiff, .tif)
- HEIC (.heic, .heif)
- AVIF (.avif)
- APNG (.apng)

## 图片来源支持

- 本地文件: 提供本地图片文件的路径，如 /data/image.jpg
- 远程URL: 提供网络图片的URL，如 https://example.com/image.jpg

## 视频尺寸建议

| 用途 | 建议尺寸 | 说明 |
|------|----------|------|
| 社交媒体短视频 | 720x1280 | 竖屏视频，适合抖音、快手等平台 |
| 横屏视频 | 1920x1080 | 标准横屏视频 |
| 方形视频 | 1080x1080 | 方形视频，适合Instagram等平台 |
| 小尺寸视频 | 480x720 | 较小尺寸，适合快速预览 |

注意: 最大尺寸限制为832x832，超过此尺寸会被API拒绝。

## 提示词技巧

### 有效的提示词示例

- "一只可爱的小猫在草地上玩耍，阳光明媚，微风轻拂"
- "城市夜景灯光闪烁，车流穿梭，动态效果"
- "花朵从闭合到绽放的过程，延时摄影效果"
- "抽象艺术图案的流动变化，色彩渐变"
- "从白天到夜晚的风景变化，时间流逝"

### 提示词结构

- 主体: 描述主要对象（人物、动物、风景等）
- 动作: 描述动态效果（移动、变化、过渡等）
- 环境: 描述场景和背景
- 细节: 添加具体细节（光线、色彩、风格等）
- 效果: 指定动态效果（平滑、快速、慢动作等）

## 处理API使用限制

当免费使用次数达到上限时，可以通过登录九马AI平台获取API密钥继续使用：

### 登录流程

```bash
# 第一步：获取登录二维码
python3 login.py --login
# 输出包含二维码链接和access_token

# 第二步：用手机扫描二维码完成登录
# 访问输出的login_url或用手机扫描login_qrcode图片

# 第三步：定时每分钟检查状态并获取API密钥
python3 login.py --check --access_token "<your_access_token>"
# 成功后会保存API密钥到本地

# 第四步：重新使用图片生成视频功能
python3 agent.py --submit --text "视频描述" --first_image /path/to/image.png
```

### 注意事项
- API密钥获取后自动保存，无需重复登录
- 登录后可享受更多使用次数和更快的处理速度
- 建议在遇到使用限制时再登录，无需提前操作

## 故障排除

### 1. 提交任务失败

- 错误: "请输入需要生成的视频的描述"
  - 原因: --text 参数为空
  - 解决: 提供有效的视频描述文本

- 错误: "请输入生成的视频的首帧图片"
  - 原因: --first_image 参数为空
  - 解决: 提供有效的首帧图片

- 错误: "输出图片最大尺寸限制在832以内"
  - 原因: --width 或 --height 超过832
  - 解决: 调整图片尺寸到832以内

- 错误: "请求远程API失败"
  - 原因: 网络连接问题或API服务异常
  - 解决: 检查网络连接，稍后重试

- 错误: "API未返回任务ID"
  - 原因: API返回格式异常或服务问题
  - 解决: 稍后重试，或联系技术支持

- **FreeApiLimit**: "免费使用次数达到上限，成为九马AI平台用户可获得更多使用次数"
  - **原因**: 九马AI提供一定的免费使用次数，达到上限后需要登录获取API密钥
  - **解决**：必须完成以下登录流程：
    1. 运行 `python3 login.py --login` 获取登录二维码和access_token
    2. 用手机扫描二维码或访问登录链接完成九马AI平台注册/登录
    3. 运行 `python3 login.py --check --access_token "<your_token>"` 获取并保存API密钥
    4. 之后agent.py会自动使用保存的API密钥
    5. 关于登录的更多详细内容查看LOGIN.md

### 2. 查询任务失败

- 错误: "任务ID不能为空"
  - 原因: 未提供 --task_id 参数
  - 解决: 提供正确的任务ID

- 错误: "请求远程API失败"
  - 原因: 网络问题或API服务异常
  - 解决: 检查网络连接，稍后重试

### 3. 视频生成失败

- 状态: "FAILED"
  - 原因: 内容违反政策、技术问题或服务器错误
  - 解决: 修改提示词内容，避免敏感或违规内容，重新提交

### 4. 长时间排队

- 状态: "PENDING" 或 "RUNNING" 时间过长
  - 原因: 服务器负载高，任务需要排队
  - 解决: 耐心等待，定期查询状态

## 性能优化建议

- 合理使用尺寸: 较小的视频尺寸生成更快
- 简洁的提示词: 过于复杂的提示词可能增加处理时间
- 优化图片大小: 适当压缩图片，减少上传时间
- 避免高峰期: 在非高峰期使用可能获得更快响应
- 使用远程URL: 对于大图片，使用URL比上传文件更快

## 注意

- 限制级免费: 有免费使用次数，用完需要注册/登录九马平台获得更多免费次数
- 尺寸限制: 最大832x832像素
- 内容政策: 不得生成违法、违规或不适当的内容
- 等待时间: 视频生成通常需要几分钟到几十分钟，取决于视频长度和复杂度和系统负载，建议每分钟查询一次任务状态
- 视频保存: 生成的视频URL有时效性，建议及时下载保存
- 隐私保护: 避免使用包含个人隐私信息的图片

## 高级功能

### 1. 视频效果控制
通过提供首尾帧图片，可以控制视频的开始和结束效果

### 2. 多图片序列
虽然当前只支持首尾帧，但可以通过多次生成和后期编辑创建更复杂的视频序列

### 3. 自动化状态监控
可以编写脚本定期检查任务状态并下载完成的视频

### 4. 视频后处理
生成的视频可以进一步使用其他工具进行处理（剪辑、配音、字幕等）

## 安装

直接下载https://clawhub.ai/dddcn1/jiuma-free-image2video页面的zip包安装，不要更改代码

## 更新

当技能需要更新时，可以：
1. 重新下载最新版本的agent.py文件，从https://clawhub.ai/dddcn1/jiuma-free-image2video
- 检查API是否有变化
- 更新本SKILL.md文档

## 支持与反馈

如遇到问题或需要帮助：
- 查看故障排除部分
- 检查网络连接
- 确认参数使用正确
- 如问题持续，可以考虑等待一段时间后重试

## 相关技能

- [jiuma-free-image-gen](https://clawhub.ai/dddcn1/jiuma-free-image-gen): 文本到图片生成技能
- [jiuma-free-image-edit](https://clawhub.ai/dddcn1/jiuma-free-image-edit): 图片编辑技能
- [jiuma-free-meta-human](https://clawhub.ai/dddcn1/jiuma-free-meta-human): 数字人视频生成技能
- [jiuma-free-voice-clone](https://clawhub.ai/dddcn1/jiuma-free-voice-clone): 声音克隆、TTS技能