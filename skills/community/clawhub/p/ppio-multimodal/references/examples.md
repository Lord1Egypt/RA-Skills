# 常见任务示例

## 生成过程提示模板

执行生成任务时，向用户显示：

```
正在生成中，请耐心等待...
任务类型：[任务类型]
使用模型：[模型名称]
预计费用：约 ￥[金额]
```

生成完成后显示：
```
生成完成！
实际消耗：￥[金额]
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
使用模型：Seedream 5.0 Lite
预计费用：约 ￥0.245

执行：POST https://api.ppio.com/v3/seedream-5.0-lite
请求：{"prompt": "日落时分的海边风景，金色阳光洒在平静的海面上"}
```

### 2. 生成人物插画
```
用户：画一个穿着蓝色连衣裙的女孩站在樱花树下

提示：
正在生成中，请耐心等待...
任务类型：文生图
使用模型：Seedream 5.0 Lite
预计费用：约 ￥0.245

执行：POST https://api.ppio.com/v3/seedream-5.0-lite
请求：{"prompt": "穿着蓝色连衣裙的女孩站在樱花树下，动漫风格"}
```

### 3. 生成产品图
```
用户：生成一张大理石桌面上的手机产品图

执行：POST https://api.ppio.com/v3/seedream-5.0-lite
请求：{"prompt": "白色大理石表面上的现代智能手机，专业产品摄影，柔和灯光"}
```

## 图片编辑

### 4. 风格转换
```
用户：把这张照片转成油画风格 [附图片]

提示：
正在生成中，请耐心等待...
任务类型：图片编辑
使用模型：Seedream 5.0 Lite
预计费用：约 ￥0.245

执行：POST https://api.ppio.com/v3/seedream-5.0-lite
请求：{"prompt": "转换为油画风格", "reference_images": ["图片URL"]}
```

### 5. 背景替换
```
用户：把图片背景换成海滩 [附图片]

执行：POST https://api.ppio.com/v3/seedream-5.0-lite
请求：{"prompt": "替换背景为热带海滩", "reference_images": ["图片URL"]}
```

## 文生视频

### 6. 生成自然场景视频
```
用户：生成一段森林中小溪流水的视频

提示：
正在生成中，请耐心等待...
任务类型：文生视频
使用模型：Vidu Q3 Pro
预计费用：约 ￥1.9-4（4秒）

执行：POST https://api.ppio.com/v3/async/vidu-q3-pro-t2v
请求：{"prompt": "宁静的森林中，小溪潺潺流过", "duration": 4}
返回：{"task_id": "xxx"}
查询：https://api.ppio.com/v3/async/task-result?task_id=xxx
```

### 7. 生成城市场景视频
```
用户：生成一段夜晚城市车流的延时摄影视频

执行：POST https://api.ppio.com/v3/async/vidu-q3-pro-t2v
请求：{"prompt": "夜晚城市车流延时摄影，车灯形成光轨，城市天际线", "duration": 4}
```

## 图生视频

### 8. 图片动画化
```
用户：让这张风景照动起来 [附图片]

提示：
正在生成中，请耐心等待...
任务类型：图生视频
使用模型：Vidu Q3 Pro
预计费用：约 ￥1.9-4

执行：POST https://api.ppio.com/v3/async/vidu-q3-pro-i2v
请求：{"prompt": "微风轻拂，云朵飘动，草丛摇曳", "images": ["图片URL"]}
```

### 9. 人像动画化
```
用户：给这张人像照片添加微动效果 [附图片]

执行：POST https://api.ppio.com/v3/async/vidu-q3-pro-i2v
请求：{"prompt": "轻微的头部转动，眨眼，自然呼吸", "images": ["图片URL"]}
```

## TTS 文字转语音

### 10. 基础朗读
```
用户：把这段文字转成语音：今天天气真好

提示：
正在生成中，请耐心等待...
任务类型：TTS
使用模型：MiniMax Speech 2.8 Turbo
预计费用：约 ￥0.02

执行：POST https://api.ppio.com/v3/async/minimax-speech-2.8-turbo
请求：{
  "text": "今天天气真好",
  "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1.0},
  "audio_setting": {"format": "mp3"}
}
```

### 11. 指定女声
```
用户：用女声朗读：欢迎来到 PPIO

执行：POST https://api.ppio.com/v3/async/minimax-speech-2.8-turbo
请求：{
  "text": "欢迎来到 PPIO",
  "voice_setting": {"voice_id": "female-shaonv"}
}
```

### 12. 调整语速
```
用户：用慢速朗读：人工智能正在改变世界

执行：POST https://api.ppio.com/v3/async/minimax-speech-2.8-turbo
请求：{
  "text": "人工智能正在改变世界",
  "voice_setting": {"voice_id": "male-qn-qingse", "speed": 0.8}
}
```

## STT 语音转文字

### 13. 音频转录
```
用户：把这段录音转成文字 [附音频]

执行：POST https://api.ppio.com/v3/glm-asr
请求：{"file": "音频URL"}
```

### 14. 会议记录
```
用户：把这段会议录音转成文字 [附音频]

执行：POST https://api.ppio.com/v3/glm-asr
请求：{"file": "音频URL"}
```

## 组合任务

### 15. 图片分析 + 生成新图
```
用户：分析这张图然后生成类似风格的新图 [附图片]

执行：
1. 分析图片内容和风格
2. POST https://api.ppio.com/v3/seedream-5.0-lite 生成新图
```

### 16. 文字摘要 + 转语音
```
用户：把这段文字摘要后转成语音 [附文本]

执行：
1. 生成文字摘要
2. POST https://api.ppio.com/v3/async/minimax-speech-2.8-turbo 转为语音
```
