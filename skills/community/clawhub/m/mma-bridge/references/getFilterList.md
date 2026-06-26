# getFilterList API

## 描述

获取可用的筛选和排序选项列表。

## 命令

```bash
mma post --method getFilterList
```

## 示例

```bash
# 使用默认端口
mma post --method getFilterList

# 指定端口
mma post --method getFilterList --port 9000
```

## 响应格式

```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "isCollect": {
      "value": [0, 1],
      "introduction": "0表示未收藏的，1表示已收藏（已打上星标）的。",
      "description": "可以筛选是否是收藏（星标）的结果。单选。",
      "filterMode": "single",
      "canEmpty": true
    },
    "date": {
      "value": [
        {
          "timeShow": "2025-12-09",
          "time": 1733721600000,
          "targetCount": 42,
          "lastTime": "4小时30分钟"
        }
      ],
      "description": "可以筛选的日期列表。单选。",
      "filterMode": "single",
      "canEmpty": true
    },
    "type": {
      "value": [
        {
          "label": "流星",
          "labelen": "meteor",
          "count": 30,
          "command": 0
        },
        {
          "label": "飞机/卫星/火箭",
          "labelen": "plane/satellite/rocket",
          "count": 8,
          "command": 1
        },
        {
          "label": "精灵/喷流",
          "labelen": "red sprite/jet",
          "count": 2,
          "command": 2
        },
        {
          "label": "闪电",
          "labelen": "lightning",
          "count": 1,
          "command": 3
        },
        {
          "label": "丢弃的结果",
          "labelen": "dropped",
          "count": 5,
          "command": 4
        },
        {
          "label": "虫子",
          "labelen": "bugs",
          "count": 3,
          "command": 5
        },
        {
          "label": "其他",
          "labelen": "others",
          "count": 2,
          "command": 6
        }
      ],
      "description": "可以筛选的结果类型列表。多选。",
      "filterMode": "multiple",
      "canEmpty": true
    },
    "meteorShower": {
      "value": [
        {
          "designation": "Unknown",
          "designationCN": "未知",
          "count": 15,
          "IAUNo": "-1"
        },
        {
          "designationCN": "双子座流星雨",
          "designation": "Geminids",
          "count": 15,
          "IAUNo": "4"
        },
        {
          "designationCN": "英仙座流星雨",
          "designation": "Perseids",
          "count": 10,
          "IAUNo": "7"
        }
      ],
      "description": "结果所归属的流星雨，或者说某颗流星的辐射点来自特定的流星雨。可多选。",
      "filterMode": "multiple",
      "canEmpty": true
    },
    "order": {
      "value": [
        {
          "label": "按所在时间",
          "labelen": "by Time",
          "command": 0,
          "sort": "ASC"
        },
        {
          "command": 1,
          "label": "按置信度",
          "labelen": "by Confidence",
          "title": "",
          "titleen": "",
          "sort": "DESC"
        },
        {
          "command": 2,
          "label": "按流星长度",
          "labelen": "by Screen Length",
          "title": "根据屏幕像素坐标计算",
          "titleen": "Calculated based on screen pixel coordinates",
          "sort": "DESC"
        },
        {
          "command": 3,
          "label": "按流星数量",
          "labelen": "by Meteor Count",
          "title": "",
          "titleen": "",
          "sort": "DESC"
        },
        {
          "command": 4,
          "label": "按持续时间",
          "labelen": "by Duration",
          "title": "",
          "titleen": "",
          "sort": "DESC"
        },
        {
          "command": 5,
          "label": "按亮度",
          "labelen": "by Brightness",
          "title": "目标相对背景的亮度",
          "titleen": "Target brightness relative to background",
          "sort": "DESC"
        },
        {
          "command": 6,
          "label": "按观赏性",
          "labelen": "by Aesthetic",
          "title": "综合亮度和长度的指标",
          "titleen": "Indicators combining brightness and length",
          "sort": "DESC"
        }
      ],
      "description": "结果排序方式。单选。",
      "canEmpty": true
    },
    "summary": "这个接口返回了可用的筛选条件，以及可用的排序条件，具体请查看每个字段的介绍。",
    "msg": "查询成功",
    "suggested_actions": ["getDataList"]
  }
}
```

## 响应字段说明

- `success` (布尔值): 表示请求是否成功
- `message` (字符串): 状态消息
- `data` (对象): 包含实际信息
  - `isCollect` (对象): 收藏筛选选项
    - `value` (数组): 可选值，[0, 1]
    - `introduction` (字符串): 选项说明，"0表示未收藏的，1表示已收藏（已打上星标）的。"
    - `description` (字符串): 筛选描述，"可以筛选是否是收藏（星标）的结果。单选。"
    - `filterMode` (字符串): 筛选模式，"single"表示单选，"multiple"表示多选
    - `canEmpty` (布尔值): 是否允许为空
  - `date` (对象): 日期筛选选项
    - `value` (数组): 可选日期列表
      - 每个元素包含:
        - `timeShow` (字符串): 显示的日期，格式为"yyyy-MM-dd"，这个日期是time去掉时分秒后的字符串
        - `time` (整数): 用于查询的时间戳，这个时间戳并非实际日期00:00:00，而是用于查询的参数
        - `targetCount` (整数): 当天的结果数量
        - `lastTime` (字符串): 当天启动检测的持续时长，如"4小时30分钟"
    - `description` (字符串): 筛选描述，"可以筛选的日期列表。单选。"
    - `filterMode` (字符串): 筛选模式，"single"表示单选，"multiple"表示多选
    - `canEmpty` (布尔值): 是否允许为空
  - `type` (对象): 结果类型筛选选项
    - `value` (数组): 可选类型列表
      - 每个元素包含:
        - `label` (字符串): 类型中文名称
        - `labelen` (字符串): 类型英文名称
        - `count` (整数): 该类型下的结果数量
        - `command` (整数): 用于查询的具体值，0流星 1飞机/卫星/火箭 2红色精灵 3闪电 4丢弃的结果 5虫子 6其他
    - `description` (字符串): 筛选描述，"可以筛选的结果类型列表。多选。"
    - `filterMode` (字符串): 筛选模式，"multiple"表示多选
    - `canEmpty` (布尔值): 是否允许为空
  - `meteorShower` (对象): 流星雨筛选选项
    - `value` (数组): 可选流星雨列表
      - 每个元素包含:
        - `designationCN` (字符串): 流星雨辐射点的中文名称
        - `designation` (字符串): 流星雨辐射点的英文名称
        - `count` (整数): 该流星雨的结果数量
        - `IAUNo` (字符串): 国际流星组织的编号，用于查询
    - `description` (字符串): 筛选描述，"结果所归属的流星雨，或者说某颗流星的辐射点来自特定的流星雨。可多选。"
    - `filterMode` (字符串): 筛选模式，"multiple"表示多选
    - `canEmpty` (布尔值): 是否允许为空
  - `order` (对象): 排序选项
    - `value` (数组): 可选排序方式列表
      - 每个元素包含:
        - `label` (字符串): 排序方式中文名称
        - `labelen` (字符串): 排序方式英文名称
        - `command` (字符串): 用于排序的具体值，即排序字段名
        - `sort` (字符串): 默认排序顺序，"ASC"表示升序，"DESC"表示降序
    - `description` (字符串): 排序描述，"结果排序方式。单选。"
    - `canEmpty` (布尔值): 是否允许为空
  - `summary` (字符串): 接口摘要，"这个接口返回了可用的筛选条件，以及可用的排序条件，具体请查看每个字段的介绍。"
  - `msg` (字符串): 状态消息，"查询成功"
  - `suggested_actions` (数组): 建议的后续操作，["getDataList"]
