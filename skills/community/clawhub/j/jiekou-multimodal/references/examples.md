# 常见任务示例

## 生成过程提示模板

执行生成任务时，向用户显示：

```
正在生成中，请耐心等待...
任务类型：[任务类型]
使用模型：[模型名称]
预计费用：约 $[金额] 元
```

生成完成后显示：
```
生成完成！
实际消耗：$[金额] 元
[返回结果 URL 或文件]
```

---

## 文生图

### 1. 生成风景图
```
用户：生成一张日落时分的海边风景图

提示：
正在生成中，请耐心等待...
任务类型：文生图
使用模型：Gemini 3.1 Flash Image
预计费用：约 $0.03 元

执行：调用 /v3/gemini-3.1-flash-image-text-to-image
请求：{"prompt": "A beautiful sunset over the ocean with golden light reflecting on calm waves", "size": "1K"}
```

### 2. 生成人物插画
```
用户：画一个穿着蓝色连衣裙的女孩站在樱花树下

提示：
正在生成中，请耐心等待...
任务类型：文生图
使用模型：Gemini 3.1 Flash Image
预计费用：约 $0.03 元

执行：调用 /v3/gemini-3.1-flash-image-text-to-image
请求：{"prompt": "A girl in blue dress standing under cherry blossom trees, anime style", "size": "1K"}
```

### 3. 快速生成（用户要求加速）
```
用户：快点生成一张猫咪图片

提示：
正在生成中，请耐心等待...
任务类型：文生图
使用模型：Seedream 5.0 Lite（快速模式）
预计费用：约 $0.02 元

执行：调用 /v3/seedream-5.0-lite
请求：{"prompt": "A cute cat"}
```

## 图片编辑

### 4. 风格转换
```
用户：把这张照片转成油画风格 [附图片]

提示：
正在生成中，请耐心等待...
任务类型：图片编辑
使用模型：Gemini 3.1 Flash Image
预计费用：约 $0.03 元

执行：调用 /v3/gemini-3.1-flash-image-edit
请求：{"prompt": "Convert to oil painting style", "reference_images": ["图片URL"]}
```

### 5. 局部编辑
```
用户：把图片中的天空改成夜空 [附图片]

执行：调用 /v3/gemini-3.1-flash-image-edit
请求：{"prompt": "Replace sky with night sky full of stars", "reference_images": ["图片URL"]}
```

## 文生视频

### 6. 生成自然场景视频
```
用户：生成一段森林中小溪流水的视频

提示：
正在生成中，请耐心等待...
任务类型：文生视频
使用模型：Veo 3.1
预计费用：约 $0.20 元（5秒）

执行：调用 /v3/async/veo-3.1-generate-text2video
请求：{"prompt": "A gentle stream flowing through a peaceful forest", "duration_seconds": 4}
返回：{"task_id": "xxx"}
查询：/v3/async/task-result?task_id=xxx
```

### 7. 快速视频生成
```
用户：太慢了，快点生成一段海浪视频

提示：
正在生成中，请耐心等待...
任务类型：文生视频
使用模型：Hailuo 2.3（快速模式）
预计费用：约 $0.10 元

执行：调用 /v3/async/minimax-hailuo-2.3-t2v
请求：{"prompt": "Ocean waves crashing on the beach", "duration": 6}
```

## 图生视频

### 8. 图片动画化
```
用户：让这张风景照动起来 [附图片]

提示：
正在生成中，请耐心等待...
任务类型：图生视频
使用模型：Veo 3.1
预计费用：约 $0.20 元

执行：调用 /v3/async/veo-3.1-generate-img2video
请求：{"prompt": "Animate with gentle breeze", "image": "图片URL"}
```

### 9. 快速图生视频
```
用户：快点让这张图动起来 [附图片]

执行：调用 /v3/async/minimax-hailuo-2.3-i2v
请求：{"prompt": "Animate the scene", "first_frame_image": "图片URL"}
```

## TTS 文字转语音

### 10. 基础朗读
```
用户：把这段文字转成语音：今天天气真好

提示：
正在生成中，请耐心等待...
任务类型：TTS
使用模型：MiniMax Speech 2.6 Turbo
预计费用：约 $0.01 元

执行：调用 /v3/minimax-speech-2.6-turbo
请求：{
  "text": "今天天气真好",
  "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1.0},
  "audio_setting": {"format": "mp3"}
}
```

### 11. 指定女声
```
用户：用女声朗读：欢迎来到接口AI

执行：调用 /v3/minimax-speech-2.6-turbo
请求：{
  "text": "欢迎来到接口AI",
  "voice_setting": {"voice_id": "female-shaonv"}
}
```

### 12. 调整语速
```
用户：用慢速朗读：人工智能正在改变世界

执行：调用 /v3/minimax-speech-2.6-turbo
请求：{
  "text": "人工智能正在改变世界",
  "voice_setting": {"voice_id": "male-qn-qingse", "speed": 0.8}
}
```

## STT 语音转文字

### 13. 音频转录
```
用户：把这段录音转成文字 [附音频]

执行：调用 /v3/glm-asr
请求：{"audio_url": "音频URL"}
```

## 图片理解

### 14. 描述图片内容
```
用户：这张图片里有什么？[附图片]

执行：调用 /openai/v1/chat/completions
请求：{
  "model": "gemini-2.5-flash",
  "messages": [{
    "role": "user",
    "content": [
      {"type": "text", "text": "描述这张图片"},
      {"type": "image_url", "image_url": {"url": "图片URL"}}
    ]
  }]
}
```

### 15. OCR 文字提取
```
用户：识别图片中的文字 [附图片]

执行：调用 /openai/v1/chat/completions
请求：model="gemini-2.5-flash"，prompt="提取图片中的所有文字"
```

## 组合任务

### 16. 视频转语音摘要
```
用户：把这个视频的内容转成语音摘要 [附视频]

执行：
1. 调用 /openai/v1/chat/completions 理解视频内容
2. 调用 /v3/minimax-speech-2.6-turbo 将摘要转为语音
```

### 17. 图片风格迁移
```
用户：参考这张图生成一张类似风格的新图 [附图片]

执行：
1. 调用 /openai/v1/chat/completions 分析原图风格
2. 调用 /v3/gemini-3.1-flash-image-text-to-image 生成新图
```
