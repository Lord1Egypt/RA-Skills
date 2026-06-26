# getDataList API

## 描述

根据筛选和排序条件获取流星检测数据列表。

## 命令

```bash
mma post --method getDataList --data-file <filePath>
```

## 请求参数

```json
{
  "isCollect": 0,
  "date": "2025-12-09",
  "type": [0],
  "meteorShower": ["4"],
  "orderBy": "start_time",
  "sort": "DESC",
  "pageSize": 10,
  "pageIndex": 1
}
```

## 参数说明

- `isCollect` (整数, 可选): 筛选收藏的结果，0表示未收藏，1表示已收藏
- `date` (字符串, 可选): 筛选日期，格式为"yyyy-MM-dd"，是从getFilterList接口里面拿到的timeShow。只有当系统信息中的mode为2、3、5时，这个参数才有效
- `type` (数组, 可选): 筛选结果类型，数组元素为数字，可选值：
  - 0: 流星
  - 1: 飞机/卫星/火箭
  - 2: 红色精灵
  - 3: 闪电
  - 4: 丢弃的结果
  - 5: 虫子
  - 6: 其他
- `meteorShower` (数组, 可选): 筛选流星雨归属（流星雨辐射点），传入的是IAUNo，多选
- `orderBy` (字符串, 可选): 排序方式，传入的是可用排序方式的command，也就是具体排序排哪个字段，单选
- `sort` (字符串, 可选): 排序的顺序，"ASC"表示升序，"DESC"表示降序
- `pageSize` (整数, 可选): 每页显示数量，默认为10，最大不得超过500
- `pageIndex` (整数, 可选): 页码，从1开始，默认为1

## 示例

```bash
# 将 JSON 数据写入文件
echo '{"type": [0], "orderBy": "start_time", "sort": "DESC", "pageSize": 10, "pageIndex": 1}' > data.json

# 使用默认端口查询流星数据
mma post --method getDataList --data-file data.json

# 指定端口查询双子座流星雨的数据
mma post --method getDataList --port 9000 --data-file data.json

# 查询收藏的流星数据
echo '{"isCollect": 1, "type": [0], "orderBy": "start_time", "sort": "DESC", "pageSize": 10, "pageIndex": 1}' > data.json
mma post --method getDataList --data-file data.json
```

## 响应格式

```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "total_count": 42,
    "datalist": [
      {
        "id": "12345",
        "start_time": "2025-12-09T20:30:15.000Z",
        "end_time": "2025-12-09T20:30:18.500Z",
        "duration": 3.5,
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
        "newTarget": [],
        "video_size": {
          "width": 1920,
          "height": 1080
        },
        "collect": 1,
        "actionGroupID": 1733721600000
      }
    ],
    "pageIndex": 1,
    "pageSize": 10,
    "filters_applied": ["结果类型", "归属流星雨"],
    "cost": "178ms",
    "summary": "这个接口根据请求的筛选和排序条件返回了具体的数据列表。",
    "msg": "查询成功"
  }
}
```

## 响应字段说明

- `success` (布尔值): 表示请求是否成功
- `message` (字符串): 状态消息
- `data` (对象): 包含实际信息
  - `total_count` (整数): 无视分页条件的数据总量
  - `datalist` (数组): 查询出来的数据列表
    - 每个元素包含以下字段:
      - `id` (字符串): 结果唯一标识符
      - `start_time` (字符串): 开始时间，ISO 8601格式
      - `end_time` (字符串): 结束时间，ISO 8601格式
      - `duration` (浮点数): 持续时间，单位为秒
      - `target` (数组): 目标信息数组
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
      - `exif` (对象): EXIF信息
        - `camera` (对象): 相机信息
          - `make` (字符串): 相机制造商
          - `model` (字符串): 相机型号
        - `exposure` (对象): 曝光信息
          - `exposureTime` (浮点数): 曝光时间，单位为秒
          - `iso` (整数): ISO感光度
          - `aperture` (浮点数): 光圈值
      - `newTarget` (数组): 新目标信息数组（结构与target相同）
      - `video_size` (对象): 视频尺寸信息
        - `width` (整数): 视频宽度（像素）
        - `height` (整数): 视频高度（像素）
      - `collect` (整数): 是否收藏，0未收藏，1已收藏
      - `actionGroupID` (整数): 操作组ID，用于关联同一时间段内的结果
  - `pageIndex` (整数): 当前页码，从1开始
  - `pageSize` (整数): 当前每页显示数量
  - `filters_applied` (数组): 应用了哪些筛选条件，如["结果类型", "归属流星雨"]
  - `cost` (字符串): 查询耗时，单位为毫秒
  - `summary` (字符串): 接口摘要，"这个接口根据请求的筛选和排序条件返回了具体的数据列表。"
  - `msg` (字符串): 状态消息，"查询成功"

## 注意事项

1. `pageIndex` 从 1 开始，表示第一页
2. `pageSize` 最大值为 500，超过此值将返回错误
3. `orderBy` 和 `sort` 默认是按所在时间，由新到旧排序
4. 可以通过调用 `getFilterList` 接口获取可用的筛选和排序选项
5. `type` 参数中的数字必须在 1-6 之间，否则将被忽略
6. `date` 参数必须是有效的日期，且存在于 `getFilterList` 返回的日期列表中，否则将被忽略
7. 当筛选条件为空时，将返回所有数据
