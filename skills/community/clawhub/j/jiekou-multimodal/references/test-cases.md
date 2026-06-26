# 测试样例

## API Key 检查测试

### TC-01: 未配置 API Key
```
输入：生成一张猫咪图片
预期：返回配置引导
"您还没有配置接口AI的 API Key。

快速配置（复制运行）：
mkdir -p ~/.jiekou && echo '{"api_key": "你的Key"}' > ~/.jiekou/config.json

获取 Key：https://jiekou.ai/settings/key-management"
```

### TC-02: API Key 无效
```
输入：生成一张猫咪图片（使用无效 Key）
预期：返回 401 错误
"API Key 无效，请检查配置。获取有效 Key：https://jiekou.ai/settings/key-management"
```

### TC-03: API Key 有效
```
输入：生成一张猫咪图片
预期：
1. 显示生成提示
2. 调用 /v3/gemini-3.1-flash-image-text-to-image
3. 返回图片 URL
```

## 文生图测试

### TC-04: 基础文生图
```
输入：生成一张蓝天白云的风景图
预期：
1. 调用 /v3/gemini-3.1-flash-image-text-to-image
2. 请求：{"prompt": "蓝天白云风景", "size": "1K"}
3. 返回图片 URL
```

### TC-05: 快速生成
```
输入：快点生成一张风景图
预期：
1. 调用 /v3/seedream-5.0-lite
2. 提示显示"Seedream 5.0 Lite（快速模式）"
```

### TC-06: 指定尺寸
```
输入：生成一张 16:9 的横版风景图
预期：请求包含 "aspect_ratio": "16:9"
```

## 图片编辑测试

### TC-07: 风格转换
```
输入：把这张照片转成水彩画风格 [附图片]
预期：
1. 调用 /v3/gemini-3.1-flash-image-edit
2. 请求：{"prompt": "watercolor style", "reference_images": ["图片URL"]}
```

### TC-08: 局部修改
```
输入：把图片背景换成海滩 [附图片]
预期：调用 /v3/gemini-3.1-flash-image-edit
```

## 文生视频测试

### TC-09: 基础文生视频
```
输入：生成一段 5 秒的海浪视频
预期：
1. 调用 /v3/async/veo-3.1-generate-text2video
2. 请求：{"prompt": "ocean waves", "duration_seconds": 4}
3. 返回 task_id
4. 轮询 /v3/async/task-result?task_id=xxx
5. 返回视频 URL
```

### TC-10: 快速视频生成
```
输入：快点生成一段日落视频
预期：
1. 调用 /v3/async/minimax-hailuo-2.3-t2v
2. 请求：{"prompt": "sunset", "duration": 6}
```

### TC-11: 指定时长
```
输入：生成 8 秒的延时摄影视频
预期：请求包含 "duration_seconds": 8
```

## 图生视频测试

### TC-12: 图片动画化
```
输入：让这张风景照动起来 [附图片]
预期：
1. 调用 /v3/async/veo-3.1-generate-img2video
2. 请求：{"prompt": "animate", "image": "图片URL"}
```

### TC-13: 快速图生视频
```
输入：快点让这张图动起来 [附图片]
预期：
1. 调用 /v3/async/minimax-hailuo-2.3-i2v
2. 请求：{"prompt": "animate", "first_frame_image": "图片URL"}
```

## TTS 测试

### TC-14: 基础 TTS
```
输入：把"你好世界"转成语音
预期：
1. 调用 /v3/minimax-speech-2.6-turbo
2. 请求：{"text": "你好世界", "voice_setting": {"voice_id": "male-qn-qingse"}}
3. 返回音频 URL
```

### TC-15: 指定女声
```
输入：用女声朗读"欢迎光临"
预期：请求包含 "voice_id": "female-shaonv"
```

### TC-16: 调整语速
```
输入：用 1.5 倍速朗读这段话
预期：请求包含 "speed": 1.5
```

### TC-17: 长文本 TTS
```
输入：朗读一段 500 字的文章
预期：正常执行，返回完整音频
```

## STT 测试

### TC-18: 基础 STT
```
输入：识别这段录音 [附音频]
预期：
1. 调用 /v3/glm-asr
2. 请求：{"audio_url": "音频URL"}
3. 返回识别文字
```

## 图片理解测试

### TC-19: 图片描述
```
输入：描述这张图片 [附图片]
预期：
1. 调用 /openai/v1/chat/completions
2. model="gemini-2.5-flash"
3. 返回详细描述
```

### TC-20: OCR 文字提取
```
输入：识别图片中的文字 [附图片]
预期：返回图片中的所有文字
```

## 错误处理测试

### TC-21: 余额不足
```
输入：生成一张图片（账户余额为 0）
预期：返回 402 错误
"余额不足，请前往 https://jiekou.ai/billing 充值"
```

### TC-22: 请求频率超限
```
输入：短时间内发送大量请求
预期：返回 429 错误，提示稍后重试
```

### TC-23: 无效参数
```
输入：生成一张 99999x99999 的图片
预期：返回 400 错误
```

## 边界测试

### TC-24: 空输入
```
输入：生成一张图片（无具体描述）
预期：提示用户提供描述内容
```

### TC-25: 超长文本 TTS
```
输入：朗读 10000 字的文章
预期：正确处理或提示文本过长（限制 10000 字符）
```

## 异步任务测试

### TC-26: 任务状态轮询
```
输入：生成一段视频
预期：
1. 提交任务返回 task_id
2. 轮询显示状态：TASK_STATUS_QUEUED → TASK_STATUS_PROCESSING → TASK_STATUS_SUCCEED
3. 成功后返回视频 URL
```

### TC-27: 任务失败处理
```
输入：生成违规内容视频
预期：
1. 任务状态变为 TASK_STATUS_FAILED
2. 返回失败原因
```

## 组合任务测试

### TC-28: 图生文再生图
```
输入：分析这张图然后生成类似风格的新图 [附图片]
预期：
1. 调用 /openai/v1/chat/completions 理解图片
2. 调用 /v3/gemini-3.1-flash-image-text-to-image 生成新图
```

### TC-29: 视频转语音摘要
```
输入：把视频内容转成语音 [附视频]
预期：
1. 调用 /openai/v1/chat/completions 理解视频
2. 调用 /v3/minimax-speech-2.6-turbo 生成语音
```

## 并发测试

### TC-30: 同时生成多张图片
```
输入：同时生成 3 张不同主题的图片
预期：3 个请求并行，全部返回结果
```
