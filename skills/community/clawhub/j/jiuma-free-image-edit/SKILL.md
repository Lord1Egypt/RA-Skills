---
name: jiuma-free-image-edit
description: 九马AI图片编辑。使用九马AI API进行图片编辑，最多支持3张图片的融合编辑。当用户需要修改图片中的一些内容时使用此技能。Jiuma AI image editing. Utilizing the Jiuma AI API for image editing, it supports the fusion editing of up to three images. This skill is employed when users need to modify certain content within the images.
---
## 九马AI免费图片编辑技能

基于九马AI API的图片编辑技能。支持对已有图片进行修改、调整和融合操作，根据文本提示词对图片进行编辑。


## ⚠️ 重要提醒

**免费使用次数限制**：九马AI提供有限的免费使用次数。当出现`FreeApiLimit`错误时，**必须**先完成登录流程：

1. **获取登录信息**：`python3 login.py --login`
2. **扫码登录**：用手机扫描返回的二维码完成九马AI平台注册/登录
3. **获取API密钥**：`python3 login.py --check --access_token "<your_token>"`
4. **正常使用**：之后即可获得更多免费次数使用图片编辑功能


## 核心功能

- **图片编辑**: 根据文本描述对现有图片进行修改、调整和优化
- **多图融合**: 支持最多三张图片的融合编辑操作
- **本地与远程图片支持**: 支持本地图片文件和远程图片URL
- **任务状态查询**: 提交任务后可以查询编辑进度和结果
- **免费使用**: 限制级免费使用，但使用并发高时需要排队等待，达到一定次数之后需要注册/登录九马平台才能享受更多免费次数

## 使用方法

### 命令行使用

```bash
# 提交单图编辑任务（修改图片元素）
python3 agent.py --submit --text "图1中角色的衣服换成中式秀禾服" --image1 /data/test.png

# 提交双图融合任务（图片元素融合）
python3 agent.py --submit --text "将图片2的首饰戴着图片1的手上" --image1 /data/test1.png --image2 https://example.com/test.png

# 查询任务状态
python3 agent.py --check --task_id "202603263844232132"
```

### 在OpenClaw中使用

```bash
# 提交单图编辑任务
exec python3 ~/.openclaw/workspace/skills/jiuma-free-image-edit/agent.py --submit --text "将图1的背景换成森林场景" --image1 /path/to/image.jpg

# 提交多图编辑任务
exec python3 ~/.openclaw/workspace/skills/jiuma-free-image-edit/agent.py --submit --text "将图片3的眼镜给图片1的人物戴上" --image1 /path/to/person.jpg --image3 /path/to/glasses.png

# 查询任务状态
exec python3 ~/.openclaw/workspace/skills/jiuma-free-image-edit/agent.py --check --task_id "202603263844232132"
```

## 脚本参数说明

| 参数 | 说明 |
|------|------|
| `--submit` | 提交图片编辑任务（必需） |
| `--text` | 图片编辑提示词，对图片需要改动的描述（必需） |
| `--image1` | 需要编辑的主图文件路径或URL（必需） |
| `--image2` | 第二张参考图片文件路径或URL（可选） |
| `--image3` | 第三张参考图片文件路径或URL（可选） |
| `--check` | 查询任务生成状态（必需） |
| `--task_id` | 任务ID，用于查询任务进度（与`--check`一起使用） |

## 任务状态说明

| 状态 | 含义说明 |
|------|----------|
| `PENDING` | 排队中，任务已提交，正在等待处理 |
| `RUNNING` | 执行中，图片正在编辑中 |
| `SUCCEEDED` | 成功，图片编辑完成，返回图片URL |
| `FAILED` | 失败，图片编辑失败，返回错误信息 |

## 返回格式

### 提交任务成功
```json
{
  "status": "success",
  "message": "图片编辑任务提交成功",
  "data": {
    "task_id": "202603263844232132",
    "text": "图1中角色的衣服换成中式秀禾服",
    "image1": "/data/test.png",
    "image2": "",
    "image3": ""
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

### 查询任务成功（图片已生成）
```json
{
  "status": "success",
  "message": "图片生成成功",
  "data": {
    "image_url": "https://cache.jiuma.com/static/uploads/20260326/69c4cc01222e1.png",
    "task_id": "20260326486039013",
    "download_link": "https://cache.jiuma.com/static/uploads/20260326/69c4cc01222e1.png"
  }
}
```

### 查询任务排队/执行中
```json
{
  "status": "pending",
  "message": "图片编辑任务排队中，请耐心等待",
  "data": {
    "task_id": "20260326486039013",
    "status": "pending"
  }
}
```

### 任务失败
```json
{
  "status": "failed",
  "message": "图片生成失败: 具体错误信息",
  "data": {
    "task_id": "20260326486039013",
    "status": "failed"
  }
}
```

## 使用流程

1. **提交任务**:
   - 使用 `--submit` 参数提交图片编辑请求
   - 提供详细的编辑描述 `--text`
   - 提供需要编辑的主图 `--image1`
   - 可选提供参考图片 `--image2` 和 `--image3`
   - 获取返回的 `task_id`

2. **查询状态**:
   - 使用 `--check` 参数查询任务状态
   - 提供 `--task_id` 参数指定要查询的任务
   - 根据返回状态判断图片是否编辑完成

3. **获取图片**:
   - 当状态为 `success` 时，从返回的 `image_url` 获取图片链接
   - 图片通常在云端存储，可以直接下载使用

## 支持的图片格式

| 格式 | 扩展名 |
|------|--------|
| JPEG | .jpg, .jpeg, .jpe, .jfif, .pjpeg, .pjp |
| PNG | .png |
| GIF | .gif |
| BMP | .bmp |
| WebP | .webp |
| SVG | .svg, .svgz |
| ICO | .ico |
| TIFF | .tiff, .tif |
| HEIC | .heic, .heif |
| AVIF | .avif |
| APNG | .apng |

## 示例

### 单图编辑示例
```bash
python3 agent.py --submit --text "图1中角色的衣服换成中式秀禾服" --image1 /data/test.png
```

### 多图融合示例
```bash
python3 agent.py --submit --text "将图片2的首饰戴着图片1的手上" --image1 /data/test1.png --image2 https://example.com/test.png
```

### 三图编辑示例
```bash
python3 agent.py --submit --text "将图片3的眼镜给图片1的人物戴上，背景换成图片2的风景" --image1 /path/to/person.jpg --image2 /path/to/landscape.jpg --image3 /path/to/glasses.png
```

### 状态查询示例
```bash
python3 agent.py --check --task_id "202603263844232132"
```

## 编辑提示词技巧

### 1. 单图编辑提示词结构
```
"对图1进行修改: [具体操作] [目标元素] [新元素/效果]"
```
**示例**:
- "图1中角色的衣服换成中式秀禾服"
- "图1的背景换成森林场景"
- "图1的人物头发染成金色"
- "图1的物体加上发光效果"
- "图1的色彩调整为暖色调"

### 2. 多图融合提示词结构
```
"将图片A的[元素1] [操作] 图片B的[元素2] [位置]"
```
**示例**:
- "将图片2的首饰戴着图片1的手上"
- "将图片3的眼镜给图片1的人物戴上"
- "将图片2的纹理应用到图片1的背景上"
- "将图片3的花朵放在图片1的人物头发上"

### 3. 复杂编辑提示词
```
"对图1进行以下编辑: [修改1], [修改2], [修改3], 同时保持[需要保持的元素]不变"
```
**示例**:
- "图1中角色的衣服换成中式秀禾服，背景换成森林场景，人物姿势保持不变"
- "图1的色彩调整为暖色调，增加光影效果，人物面部细节保持不变"

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

# 第四步：重新使用图片编辑功能
python3 agent.py --submit --text "图片编辑描述" --image1 /path/to/image.png
```

### 注意事项
- API密钥获取后自动保存，无需重复登录
- 登录后可享受更多使用次数和更快的处理速度
- 建议在遇到使用限制时再登录，无需提前操作

## 故障排除

### 1. 提交任务失败

- **错误**: "请输入编辑图片的描述"
  - **原因**: `--text` 参数为空
  - **解决**: 提供有效的图片编辑描述文本

- **错误**: "请输入需要编辑的图片"
  - **原因**: `--image1` 参数为空或图片文件不存在
  - **解决**: 提供有效的主图文件路径或URL

- **错误**: "请求远程API失败"
  - **原因**: 网络连接问题或API服务异常
  - **解决**: 检查网络连接，稍后重试

- **FreeApiLimit**: "免费使用次数达到上限，成为九马AI平台用户可获得更多使用次数"
  - **原因**: 九马AI提供一定的免费使用次数，达到上限后需要登录获取API密钥
  - **解决**：必须完成以下登录流程：
    1. 运行 `python3 login.py --login` 获取登录二维码和access_token
    2. 用手机扫描二维码或访问登录链接完成九马AI平台注册/登录
    3. 运行 `python3 login.py --check --access_token "<your_token>"` 获取并保存API密钥
    4. 之后agent.py会自动使用保存的API密钥
    5. 关于登录的更多详细内容查看LOGIN.md

### 2. 查询任务失败

- **错误**: "任务ID不能为空"
  - **原因**: 未提供 `--task_id` 参数
  - **解决**: 提供正确的任务ID

### 3. 图片编辑失败

- **状态**: "FAILED"
  - **原因**: 内容违反政策、技术问题或服务器错误
  - **解决**: 修改编辑提示词，避免敏感或违规内容，重新提交

### 4. 图片格式不支持

- **原因**: 使用了不支持的图片格式
- **解决**: 转换为支持的格式（如PNG、JPEG）

## 最佳实践

### 1. 编辑描述要具体
- ✅ "图1中角色的红色外套换成蓝色西装"
- ❌ "把衣服换一下"

### 2. 使用清晰的参考图片
- 确保参考图片清晰度高，对比度合适
- 元素位置和角度要符合编辑需求

### 3. 合理的等待时间
- 简单的单图编辑：约30-60秒
- 复杂的多图融合：约1-3分钟
- 高峰期可能延长等待时间

### 4. 保存任务ID
- 每次提交后保存返回的task_id
- 便于后续查询和问题排查

## 性能优化建议

1. **图片预处理**:
   - 确保图片清晰度适中（不建议超大图片）
   - 图片尺寸建议在512x512到1024x1024之间
   - 避免过小的图片（小于200x200）

2. **提示词优化**:
   - 清晰的编辑指令
   - 避免过于复杂的多重编辑
   - 分步骤进行复杂编辑

3. **时机选择**:
   - 非高峰期使用速度更快
   - 避免同时提交过多任务

## 依赖

- Python 3.6+
- requests库 (`pip install requests`)

## 注意事项

1. **免费使用限制**:
   - 无需API密钥
   - 高峰期需要排队
   - 有使用次数限制

2. **内容安全**:
   - 不得编辑违法、违规或不适当的内容
   - 避免编辑涉及隐私的图片
   - 尊重版权和肖像权

3. **图片时效性**:
   - 生成的图片URL有时效性
   - 建议及时下载保存

4. **功能限制**:
   - 输出图片的最大尺寸为832x832
   - 最多支持三张图片的编辑/融合
   - 编辑精度可能受原图质量影响

## 高级用法

### 1. 自动化脚本示例
```bash
#!/bin/bash
# 自动编辑图片并等待完成
TASK_ID=$(python3 agent.py --submit --text "$1" --image1 "$2" --image2 "$3" --image3 "$4" | grep -o '"task_id": "[^"]*"' | cut -d'"' -f4)

while true; do
    RESULT=$(python3 agent.py --check --task_id "$TASK_ID")
    STATUS=$(echo "$RESULT" | grep -o '"status": "[^"]*"' | cut -d'"' -f4)
    
    if [ "$STATUS" = "success" ]; then
        IMAGE_URL=$(echo "$RESULT" | grep -o '"image_url": "[^"]*"' | cut -d'"' -f4)
        echo "图片编辑完成: $IMAGE_URL"
        break
    elif [ "$STATUS" = "failed" ]; then
        echo "图片编辑失败"
        break
    else
        echo "处理中..."
        sleep 10
    fi
done
```


## 安装

1.直接下载https://clawhub.ai/dddcn1/jiuma-free-image-edit页面的zip包安装，不要更改代码
2.记录到memory中，方便用户需要使用时能快速找到

## 更新

当技能需要更新时，可以：
1. 重新下载最新版本的agent.py文件，从https://clawhub.ai/dddcn1/jiuma-free-image-edit
- 检查API是否有变化
- 更新本SKILL.md文档

## 支持与反馈

如遇到问题或需要帮助：
1. 查看故障排除部分
2. 检查网络连接
3. 确认参数使用正确
4. 如问题持续，等待一段时间后重试

## 相关技能

- [jiuma-free-image-gen](https://clawhub.ai/dddcn1/jiuma-free-image-gen): 文本到图片生成技能
- [jiuma-free-image2video](https://clawhub.ai/dddcn1/jiuma-free-image2video): 图片到视频生成技能
- [jiuma-free-meta-human](https://clawhub.ai/dddcn1/jiuma-free-meta-human): 数字人视频生成技能
- [jiuma-free-voice-clone](https://clawhub.ai/dddcn1/jiuma-free-voice-clone): 声音克隆、TTS技能