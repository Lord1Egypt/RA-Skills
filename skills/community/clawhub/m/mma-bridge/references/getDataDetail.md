# getDataDetail API

## 描述

根据数据ID获取单条流星检测数据的详细信息。

## 命令

```bash
mma post --method getDataDetail --data-file <filePath>
```

## 请求参数

```json
{
  "id": "12345"
}
```

## 参数说明

- `id` (字符串, 必需): 数据的唯一标识符，通过getDataList接口获取

## 示例

```bash
# 将 JSON 数据写入文件
echo '{"id": "12345"}' > data.json

# 查询ID为12345的数据详情
mma post --method getDataDetail --data-file data.json

# 指定端口查询数据详情
mma post --method getDataDetail --port 9000 --data-file data.json
```

## 响应格式

```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "data": {
      "id": "12345",
      "preview": "path/to/preview.jpg",
      "trackImg": "path/to/trackImg.jpg",
      "trackImgStatus": 2,
      "trackImgOutputPath": "/path/to/track.png",
      "trackImgError": "",
      "exif": {
        "camera": {
          "make": "Canon",
          "model": "EOS 6D"
        },
        "exposure": {
          "exposureTime": 30,
          "iso": 3200,
          "aperture": 2.8
        }
      },
      "readExifStatus": 2,
      "recordFilePath": "/path/to/video.mp4",
      "collect": 1,
      "outputStatus": 2,
      "outputFilePath": "/path/to/output.mp4",
      "outputName": "meteor_001.mp4",
      "basetime": 1733721600000,
      "status": 1,
      "actionGroupID": 1733721600000,
      "start_frame": 1000,
      "start_time": "00:06:57.000",
      "end_frame": 1050,
      "end_time": "00:06:59.700",
      "target": [
        {
          "class": 0,
          "pt1_coordinates": [100, 200],
          "pt2_coordinates": [300, 400],
          "meteorShower": [
            {
              "radiant": {
                "IAUNo": "4",
                "name": "Geminids",
                "nameCN": "双子座流星雨"
              }
            }
          ]
        }
      ],
      "video_size": [1920, 1080],
      "source": "/path/to/pic.jpg",
      "sourceFileName": "IMG_0001.jpg",
      "thumb": "/path/to/pic.jpg",
      "largePreview": "/path/to/pic.jpg",
      "width": 1920,
      "height": 1080,
      "originTimeForStarMap": "2025-12-09T20:30:15.000Z",
    },
    "msg": "查询成功",
    "summary": "根据id查询单条数据的详细信息，包括所有字段。"
  }
}
```

## 响应字段说明

- `success` (布尔值): 表示请求是否成功
- `message` (字符串): 状态消息
- `data` (对象): 包含实际信息
  - `data` (对象): 数据详情
    - `id` (字符串): 结果唯一标识符
    - `preview` (字符串): 缩略图，文件路径
    - `trackImg` (字符串): 流星轨迹图，文件路径
    - `trackImgStatus` (整数): 流星轨迹生成状态，0未生成 1生成中 2成功 3失败 4已存储到硬盘
    - `trackImgOutputPath` (字符串): 导出后轨迹图存放位置
    - `trackImgError` (字符串): 流星轨迹生成错误信息
    - `exif` (对象): EXIF信息，包含相机和拍摄参数等元数据
      - `camera` (对象): 相机信息
        - `make` (字符串): 相机制造商
        - `model` (字符串): 相机型号
      - `exposure` (对象): 曝光信息
        - `exposureTime` (浮点数): 曝光时间，单位为秒
        - `iso` (整数): ISO感光度
        - `aperture` (浮点数): 光圈值
    - `readExifStatus` (整数): EXIF读取状态 0未读取 1读取中 2读取完成 3读取失败
    - `recordFilePath` (字符串): 视频文件路径
    - `collect` (整数): 是否收藏，0未收藏，1已收藏
    - `outputStatus` (整数): 视频导出状态，0未导出 1导出中 2已导出
    - `outputFilePath` (字符串): 视频导出后的视频文件地址
    - `outputName` (字符串): 导出的文件名
    - `basetime` (整数): 基准时间戳
    - `status` (整数): 状态标识
    - `actionGroupID` (整数): 操作组ID，用于关联同一时间段内的结果
    - `start_frame` (整数): 开始帧号
    - `start_time` (字符串): 开始时间，ISO 8601格式
    - `end_frame` (整数): 结束帧号
    - `end_time` (字符串): 结束时间，ISO 8601格式
    - `target` (数组): 目标信息数组，包含检测到的流星或其他对象的信息
      - 每个元素包含:
        - `class` (整数): 目标类型，0流星 1飞机/卫星/火箭 2红色精灵 3闪电 4丢弃的结果 5虫子 6其他
        - `pt1_coordinates` (数组): 起点坐标 [x, y]
        - `pt2_coordinates` (数组): 终点坐标 [x, y]
        - `meteorShower` (数组): 流星雨信息（仅当class=0时存在）
          - 每个元素包含:
            - `radiant` (对象): 辐射点信息
              - `IAUNo` (字符串): 国际流星组织编号
              - `name` (字符串): 流星雨英文名称
              - `nameCN` (字符串): 流星雨中文名称
    - `video_size` (数组): 视频尺寸信息，通常包含[width, height]
    - `source` (字符串): 原始图像数据
    - `sourceFileName` (字符串): 源文件名
    - `thumb` (字符串): 缩略图
    - `largePreview` (字符串): 大预览图
    - `width` (整数): 图像宽度（像素）
    - `height` (整数): 图像高度（像素）
    - `originTimeForStarMap` (字符串): 星图原始时间
  - `msg` (字符串): 状态消息，"查询成功"
  - `summary` (字符串): 接口摘要，"根据id查询单条数据的详细信息，包括所有字段。"

## 注意事项

1. `id` 参数必须通过 `getDataList` 接口获取
2. 如果提供的 `id` 不存在，将返回错误信息
3. 返回的数据中，`target`、`exif`、`newTarget`、`video_size` 字段已经过反序列化处理，可以直接使用
4. 如果软件处于首页（mode=0），将返回错误信息"当前软件只停留在首页，没有数据可供查询"
