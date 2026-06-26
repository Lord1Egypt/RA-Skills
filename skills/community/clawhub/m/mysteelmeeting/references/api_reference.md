# 我的钢铁网会议查询 API 参考

## API 基础信息

| 项目 | 值 |
|------|-----|
| 基础URL | `https://huizhan.mysteel.com/event/activity` |
| 字符编码 | UTF-8 |
| 内容类型 | `application/json; charset=UTF-8` |

---

## 1. 会议列表查询

### 接口信息
- **URL**: `POST /event/activity/queryActivity`
- **完整地址**: `https://huizhan.mysteel.com/event/activity/queryActivity`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| keyword | string | 否 | 搜索关键词（匹配会议名称等） |
| industryBreedId | string | 否 | 行业ID |
| areaId | string | 否 | 地区ID |
| provinceId | string | 否 | 省份ID |
| activityStatus | string | 否 | 会议状态 |
| chargeType | string | 否 | 收费类型 |
| activityClassify | string | 否 | 活动类型 |
| pageSize | int | 否 | 每页数量，默认10 |
| pageNum | int | 否 | 页码，默认1 |

### 响应示例

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "total": 100,
    "pageNum": 1,
    "pageSize": 10,
    "list": [
      {
        "id": "xxx",
        "name": "2026（第二届）Mysteel镍钴及回收产业链大会",
        "activityStatus": "0",
        "provinceName": "浙江",
        "cityName": "宁波",
        "address": "宁波市",
        "startTime": 1751145600000,
        "endTime": 1751318400000,
        "countdownDay": 62,
        "chargeType": "1",
        "fee": 2000,
        "detailPcPageUrl": "https://huizhan.mysteel.com/activity/xxx",
        "industryBreedId": "10"
      }
    ]
  }
}
```

---

## 2. 行业分类查询

### 接口信息
- **URL**: `GET /event/activity/queryIndustry`
- **完整地址**: `https://huizhan.mysteel.com/event/activity/queryIndustry`

### 响应示例

```json
{
  "code": 0,
  "msg": "success",
  "data": [
    {
      "industryBreedId": "10",
      "industryBreedName": "钢材"
    },
    {
      "industryBreedId": "11",
      "industryBreedName": "铁矿石"
    }
  ]
}
```

---

## 3. 地区分类查询

### 接口信息
- **URL**: `GET /event/activity/queryArea`
- **完整地址**: `https://huizhan.mysteel.com/event/activity/queryArea`
- **可选参数**: `industryBreedId` - 根据行业筛选地区

### 响应示例

```json
{
  "code": 0,
  "msg": "success",
  "data": [
    {
      "areaName": "华北地区",
      "list": [
        {"provinceId": "101", "provinceName": "北京"},
        {"provinceId": "102", "provinceName": "天津"},
        {"provinceId": "103", "provinceName": "河北"}
      ]
    }
  ]
}
```

---

## ID 对照表

### 行业 ID

| ID | 行业名称 | 英文 |
|----|----------|------|
| 10 | 钢材 | Steel |
| 11 | 铁矿石 | Iron Ore |
| 12 | 废钢 | Scrap |
| 13 | 煤焦 | Coal & Coke |
| 14 | 铁合金 | Ferroalloy |
| 15 | 不锈钢 | Stainless Steel |
| 16 | 有色金属 | Non-ferrous Metals |
| 17 | 建筑材料 | Building Materials |
| 18 | 新能源 | New Energy |
| 19 | 农产品 | Agricultural Products |

### 地区 ID

| ID | 地区名称 |
|----|----------|
| 1 | 东北地区 |
| 2 | 港澳台地区 |
| 3 | 华北地区 |
| 4 | 华东地区 |
| 5 | 华南地区 |
| 6 | 华中地区 |
| 7 | 西北地区 |
| 8 | 西南地区 |
| 9 | 全球 |

### 状态 ID

| ID | 状态名称 |
|----|----------|
| 0 | 报名中 |
| 1 | 进行中 |
| 2 | 已结束 |

### 收费类型 ID

| ID | 收费类型 |
|----|----------|
| 0 | 免费 |
| 1 | 收费 |

---

## 常见查询场景

### 查询所有报名中的会议

```python
payload = {
    "activityStatus": "0",
    "pageSize": 10,
    "pageNum": 1
}
```

### 查询免费会议

```python
payload = {
    "chargeType": "0",
    "pageSize": 10,
    "pageNum": 1
}
```

### 查询华东地区钢材会议

```python
payload = {
    "industryBreedId": "10",
    "areaId": "4",
    "pageSize": 10,
    "pageNum": 1
}
```

### 关键词搜索

```python
payload = {
    "keyword": "钢铁",
    "pageSize": 10,
    "pageNum": 1
}
```

---

## 错误码

| code | 说明 |
|------|------|
| 0 | 成功 |
| -1 | 请求失败 |
| 其他 | 接口返回的错误码 |
