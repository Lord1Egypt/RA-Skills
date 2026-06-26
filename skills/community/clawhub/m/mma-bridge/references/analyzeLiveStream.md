# analyzeLiveStream API

## 描述

分析直播流。从已保存的直播地址列表中选择一个直播流进行连接和分析。

## 命令

```bash
mma post --method analyzeLiveStream --data-file <filePath>
```

## 请求参数

```json
{
  "title": "我的直播"
}
```

## 参数说明

- `title` (字符串, 必填): 直播流的标题，用于从已保存的直播列表中查找

## 前置条件

- 当前软件必须停留在首页（mode=0）
- 必须已在软件中添加过直播地址（livePathList.json存在）

## 响应格式

成功时:
```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "data": "analyzing",
    "msg": "已启动直播流分析",
    "summary": "已选择直播流\"我的直播\"，即将开始分析",
    "suggested_actions": []
  }
}
```

未传入title时:
```json
{
  "success": true,
  "message": "未传入title参数"
}
```

未找到指定直播时:
```json
{
  "success": true,
  "message": "未找到标题为\"xxx\"的直播流，可用标题：直播1, 直播2"
}
```

## 注意事项

1. 连接成功后，等待5秒自动开始分析
2. 如果未传入title或未找到对应title，会返回可用标题列表
3. 直播地址需要事先在软件的"分析直播流"界面中添加
4. 支持rtmp、srt、rtsp、http协议的直播流地址
