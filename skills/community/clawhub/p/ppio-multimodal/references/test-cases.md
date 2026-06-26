# 测试样例

## API Key 检查测试

### TC-01: 未配置 API Key
```
输入：生成一张猫咪图片
预期：返回配置引导
"您还没有配置 PPIO 的 API Key。

快速配置（复制运行）：
mkdir -p ~/.ppio && echo '{"api_key": "你的Key"}' > ~/.ppio/config.json

获取 Key：https://ppio.com/settings/key-management"
```

### TC-02: API Key 无效
```
输入：生成一张猫咪图片（使用无效 Key）
预期：返回 401 错误
"API Key 无效，请检查配置。获取有效 Key：https://ppio.com/settings/key-management"
```

### TC-03: API Key 有效
```
输入：生成一张猫咪图片
预期：
1. 显示生成提示
2. 调用 https://api.ppio.com/v3/seedream-5.0-lite
3. 返回图片 URL
```

## 文生图测试

### TC-04: 基础文生图
```
输入：生成一张蓝天白云的风景图
预期：
1. 调用 https://api.ppio.com/v3/seedream-5.0-lite
2. 请求：{"prompt": "蓝天白云风景"}
3. 返回图片 URL
```

### TC-05: 详细描述
```
输入：生成一张赛博朋克风格的夜晚城市
预期：
1. 调用 https://api.ppio.com/v3/seedream-5.0-lite
2. 请求包含详细描述
3. 返回图片 URL
```

### TC-06: 多张图片
```
输入：同时生成 3 张不同主题的猫咪图片
预期：发起 3 次 API 调用，返回 3 个 URL
```

## 图片编辑测试

### TC-07: 风格转换
```
输入：把这张照片转成水彩画风格 [附图片]
预期：
1. 调用 https://api.ppio.com/v3/seedream-5.0-lite
2. 请求：{"prompt": "水彩画风格", "reference_images": ["图片URL"]}
```

### TC-08: 背景替换
```
输入：把图片背景换成海滩 [附图片]
预期：调用 https://api.ppio.com/v3/seedream-5.0-lite 并附带编辑指令
```

### TC-09: 对象修改
```
输入：把天空变得更有戏剧性 [附图片]
预期：调用 https://api.ppio.com/v3/seedream-5.0-lite 并附带具体编辑指令
```

## 文生视频测试

### TC-10: 基础文生视频
```
输入：生成一段 4 秒的海浪视频
预期：
1. 调用 https://api.ppio.com/v3/async/vidu-q3-pro-t2v
2. 请求：{"prompt": "海浪", "duration": 4}
3. 返回 task_id
4. 轮询 https://api.ppio.com/v3/async/task-result?task_id=xxx
5. 返回视频 URL
```

### TC-11: 指定时长
```
输入：生成 8 秒的延时摄影视频
预期：请求包含 "duration": 8
```

### TC-12: 复杂场景
```
输入：生成一段雨滴落在城市街道上的视频
预期：
1. 调用 https://api.ppio.com/v3/async/vidu-q3-pro-t2v
2. 请求包含详细描述
```

## 图生视频测试

### TC-13: 图片动画化
```
输入：让这张风景照动起来 [附图片]
预期：
1. 调用 https://api.ppio.com/v3/async/vidu-q3-pro-i2v
2. 请求：{"prompt": "轻柔动画效果", "images": ["图片URL"]}
```

### TC-14: 特定动作
```
输入：给这张图添加风吹效果 [附图片]
预期：
1. 调用 https://api.ppio.com/v3/async/vidu-q3-pro-i2v
2. 请求：{"prompt": "风吹动树叶和草丛", "images": ["图片URL"]}
```

## TTS 测试

### TC-15: 基础 TTS
```
输入：把"你好世界"转成语音
预期：
1. 调用 https://api.ppio.com/v3/async/minimax-speech-2.8-turbo
2. 请求：{"text": "你好世界", "voice_setting": {"voice_id": "male-qn-qingse"}}
3. 返回音频 URL
```

### TC-16: 指定女声
```
输入：用女声朗读"欢迎光临"
预期：请求包含 "voice_id": "female-shaonv"
```

### TC-17: 调整语速
```
输入：用 1.5 倍速朗读这段话
预期：请求包含 "speed": 1.5
```

### TC-18: 长文本 TTS
```
输入：朗读一段 500 字的文章
预期：正常执行，返回完整音频
```

## STT 测试

### TC-19: 基础 STT
```
输入：识别这段录音 [附音频]
预期：
1. 调用 https://api.ppio.com/v3/glm-asr
2. 请求：{"file": "音频URL"}
3. 返回识别文字
```

### TC-20: 不同音频格式
```
输入：识别这段 MP3/WAV/M4A 文件
预期：正确处理各种音频格式
```

## 错误处理测试

### TC-21: 余额不足
```
输入：生成一张图片（账户余额为 0）
预期：返回 402 错误
"余额不足，请前往 https://ppio.com/billing 充值"
```

### TC-22: 请求频率超限
```
输入：短时间内发送大量请求
预期：返回 429 错误，提示稍后重试
```

### TC-23: 无效参数
```
输入：生成一张 99999 秒的视频
预期：返回 400 错误，提示参数无效
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
预期：正确处理或提示文本过长
```

### TC-26: 不支持的文件类型
```
输入：识别这个视频文件
预期：提示仅支持音频文件
```

## 异步任务测试

### TC-27: 任务状态轮询
```
输入：生成一段视频
预期：
1. 提交任务返回 task_id
2. 轮询显示状态：TASK_STATUS_QUEUED → TASK_STATUS_PROCESSING → TASK_STATUS_SUCCEED
3. 成功后返回视频 URL
```

### TC-28: 任务失败处理
```
输入：生成违规内容视频
预期：
1. 任务状态变为 TASK_STATUS_FAILED
2. 返回失败原因
```

## 组合任务测试

### TC-29: 图片分析 + 生成
```
输入：分析这张图然后生成类似风格的新图 [附图片]
预期：
1. 分析图片内容和风格
2. 调用 https://api.ppio.com/v3/seedream-5.0-lite 生成新图
```

### TC-30: 文字摘要 + TTS
```
输入：把这段文字摘要后转成语音 [附文本]
预期：
1. 生成文字摘要
2. 调用 https://api.ppio.com/v3/async/minimax-speech-2.8-turbo 生成语音
```
