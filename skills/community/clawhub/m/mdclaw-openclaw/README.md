# MDClaw 多模态

通过 MDClaw OpenClaw API 网关访问多模态 AI 能力的 Python 客户端库。

## 支持功能

- 文字转语音 (TTS)
- 文生图 (Text to Image)
- 文生视频 (Text to Video)
- 图生视频 (Image to Video)
- 图片上传
- 全网搜索 / 天气查询 / 网页总结

## 安装

```bash
pip install requests
```

## 快速开始

```python
from mdclaw_client import MDClawClient

# 方式1: 通过环境变量
# export MDCLAW_API_KEY="你的API Key"
client = MDClawClient()

# 方式2: 直接传入
client = MDClawClient(api_key="你的API Key")

# 方式3: 注册获取
client = MDClawClient()
result = client.agent_register("用户名", "密码")
```

## 使用示例

### 文字转语音

```python
result = client.text_to_speech("你好，这是语音测试")
audio_url = result["result"]["audio_url"]
```

### 文生图

```python
result = client.text_to_image("一只可爱的橘猫", aspect_ratio="9:16")
image_url = result["result"]["image_urls"][0]
```

### 文生视频

```python
# 提交任务
result = client.text_to_video("海边日落", duration=6)
task_id = result["result"]["task_id"]

# 等待完成
video_result = client.wait_for_video(task_id)
video_url = video_result["result"]["url"]
```

### 图生视频

```python
# 上传本地图片
upload = client.upload_image("photo.jpg")
image_url = upload["result"]["url"]

# 生成视频
result = client.image_to_video(image_url, "让画面动起来", duration=6)
task_id = result["result"]["task_id"]
video_result = client.wait_for_video(task_id)
```

### 一键生成并下载

```python
# 生成图片并保存
client.generate_image_and_download("美丽的风景", "output.jpg")

# 生成视频并保存
client.generate_video_and_download(
    image_url="https://...",
    prompt="动态效果",
    output_path="output.mp4",
    duration=6
)
```

### 其他功能

```python
# 全网搜索
result = client.ai_search("最新 AI 新闻")

# 天气查询
result = client.weather_query("北京")

# 网页总结
result = client.web_summary("https://example.com")
```

## 注意事项

- 视频/图片生成建议使用英文 prompt，效果更好
- 视频生成通常需要 1-5 分钟
- 不要传递 `resolution` 参数给视频接口，否则不返回 `task_id`
- API Key 请通过环境变量或参数传入，不要硬编码在代码中

## 许可证

MIT License
