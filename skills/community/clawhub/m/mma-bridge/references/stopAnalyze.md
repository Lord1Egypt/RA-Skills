# stopAnalyze API

## 描述

停止当前正在进行的直播/摄像头/推流分析。

## 命令

```bash
mma post --method stopAnalyze
```

## 请求参数

无请求参数。

## 前置条件

- 当前软件必须在直播分析模式（mode=2）、摄像头分析模式（mode=3）或推流模式（mode=5）

## 响应格式

成功时:
```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "data": "stopped",
    "msg": "已停止分析",
    "summary": "已停止直播/摄像头/推流分析",
    "suggested_actions": []
  }
}
```

失败时:
```json
{
  "success": true,
  "message": "当前状态不允许停止分析，必须在直播分析模式（mode=2）、摄像头分析模式（mode=3）或推流模式（mode=5）下才能停止分析"
}
```

## 注意事项

1. 此接口只适用于直播/摄像头/推流分析模式的停止
2. 视频分析模式（mode=1）和图片序列分析模式（mode=4）不支持此接口
3. 停止操作会同时停止录像和分析
