# analyzeVideoFile API

## 描述

分析单条视频文件。传入视频文件路径，检查视频信息后自动开始分析。

## 命令

```bash
mma post --method analyzeVideoFile --data-file <filePath>
```

## 请求参数

```json
{
  "filepath": "C:/path/to/video.mp4"
}
```

## 参数说明

- `filepath` (字符串, 必填): 视频文件的完整路径，支持中文路径，无需转义

## 前置条件

- 当前软件必须停留在首页（mode=0）

## 支持的视频格式

- 格式: QuickTime / MOV, Matroska / WebM
- 编码: h264, hevc（非yuv422p10le）

## 响应格式

成功时:
```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "data": "analyzing",
    "msg": "视频分析中",
    "summary": "视频检查通过，已加载完成",
    "suggested_actions": []
  }
}
```

失败时（格式/编码不支持）:
```json
{
  "success": true,
  "message": "视频编码不支持分析，当前视频编码为xxx，请自行将视频转换为h264编码的mp4格式"
}
```

## 注意事项

1. 视频检查通过后，加载完成等待2秒自动开始分析
2. 如果视频格式或编码不支持，返回错误信息，用户需自行转换为h264编码的mp4格式
3. 视频时长无法获取时也会返回错误
