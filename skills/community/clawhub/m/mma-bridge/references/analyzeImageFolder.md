# analyzeImageFolder API

## 描述

分析图片文件夹中的jpg/jpeg图片。传入文件夹路径，读取所有jpg/jpeg文件后自动开始分析。

## 命令

```bash
mma post --method analyzeImageFolder --data-file <filePath>
```

## 请求参数

```json
{
  "folderpath": "C:/path/to/images"
}
```

## 参数说明

- `folderpath` (字符串, 必填): 图片文件夹的完整路径，支持中文路径，无需转义

## 前置条件

- 当前软件必须停留在首页（mode=0）

## 支持的图片格式

- jpg
- jpeg

## 响应格式

成功时:
```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "data": "analyzing",
    "msg": "图片分析中",
    "summary": "已加载10张图片，开始分析",
    "suggested_actions": []
  }
}
```

失败时:
```json
{
  "success": true,
  "message": "文件夹中没有找到jpg或jpeg格式的图片文件"
}
```

## 注意事项

1. 图片加载完成后，等待2秒自动开始分析
2. 只支持jpg和jpeg格式，不支持png或其他格式
3. 文件夹中未找到支持的图片文件时返回错误
4. 不支持raw格式图片
