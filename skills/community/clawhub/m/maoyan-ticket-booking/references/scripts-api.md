# 脚本 API 参考文档

> 当需要脚本的详细入参/出参格式时读此文件。

---

## 调用格式

```bash
echo '<JSON>' | node "{baseDir}/scripts/<script>.mjs"
```

---

## 查询类脚本

### get-cities.mjs

**用途**：获取猫眼城市列表，用于获取 cityId

**入参**：无（传 `{}` 即可）

**出参**：
```json
{
  "cities": [
    { "id": 1, "name": "北京" },
    { "id": 2, "name": "上海" }
  ]
}
```

---

### get-hot-movies.mjs

**用途**：获取当前热映影片列表

**入参**：
```json
{
  "cityId": 1
}
```
| 参数 | 必填 | 说明 |
|------|------|------|
| cityId | 否 | 城市ID，默认1（北京）。兼容 `ci`，统一推荐使用 `cityId` |

**出参**：
```json
{
  "movies": [
    {
      "id": 123456,
      "nm": "影片名称",
      "sc": 9.2,
      "dir": "导演名",
      "star": "主演1,主演2",
      "dur": 120,
      "cat": "剧情,动作",
      "desc": "简介"
    }
  ]
}
```

---

### search-movies.mjs

**用途**：按关键词搜索影片

**入参**：
```json
{
  "keyword": "飞驰人生"
}
```
| 参数 | 必填 | 说明 |
|------|------|------|
| keyword | 是 | 搜索关键词 |

**出参**：同 `get-hot-movies.mjs`

---

### get-nearby-cinemas.mjs

**用途**：获取用户附近的影院

**入参**：
```json
{
  "lat": 39.9042,
  "lng": 116.4074,
  "cityId": 1
}
```
| 参数 | 必填 | 说明 |
|------|------|------|
| lat | 是 | 纬度 |
| lng | 是 | 经度 |
| cityId | 是 | 城市ID（从 get-cities.mjs 获取） |

**出参**：
```json
{
  "cinemas": [
    {
      "id": 11111,
      "nm": "万达影城（某某店）",
      "addr": "某某路123号",
      "dist": 0.5,
      "eTicketFlag": 1,
      "lowestPrice": 35
    }
  ]
}
```

---

### search-cinemas.mjs

**用途**：按关键词搜索影院

**入参**：
```json
{
  "keyword": "万达",
  "cityId": 1
}
```
| 参数 | 必填 | 说明 |
|------|------|------|
| keyword | 是 | 搜索关键词（自动提取核心词） |
| cityId | 是 | 城市ID |

**出参**：同 `get-nearby-cinemas.mjs`

---

### get-cinemas-by-movie.mjs

**用途**：查询放映某部影片的影院

**入参**：
```json
{
  "movieId": 123456,
  "cityId": 1
}
```
| 参数 | 必填 | 说明 |
|------|------|------|
| movieId | 是 | 影片ID（从搜索结果获取） |
| cityId | 是 | 城市ID |

**出参**：同 `get-nearby-cinemas.mjs`

---

### get-showtimes.mjs

**用途**：获取某影院的排片场次，返回该影院所有在映影片及场次

**入参**：
```json
{
  "cinemaId": 11111,
  "cityId": 1
}
```
| 参数 | 必填 | 说明 |
|------|------|------|
| cinemaId | 是 | 影院ID |
| cityId | 否 | 城市ID，默认1（北京）。兼容 `ci`，统一推荐使用 `cityId` |

> ⚠️ 不需要传 movieId，接口返回该影院所有在映影片的全部场次

**出参**：
```json
{
  "cinemaName": "青春光线国际影城",
  "movies": [
    {
      "movieId": 123456,
      "name": "影片名称",
      "score": 9.2,
      "dur": 120,
      "shows": [
        {
          "showDate": "2026-04-03",
          "dateShow": "今天 4月3日",
          "plist": [
            {
              "seqNo": "202604030409791",
              "tm": "10:30",
              "dt": "2026-04-03",
              "lang": "国语",
              "hallType": "2D",
              "price": 45
            }
          ]
        }
      ]
    }
  ]
}
```

> ⚠️ 已知影片名时用 `movies.find(m => m.name.includes("影片名"))` 筛选；未指定影片时直接展示所有在映影片供用户选择

---

## AuthKey 管理脚本

### load-authkey.mjs

**用途**：读取本地保存的 AuthKey

**入参**：`{}`

**出参（有效）**：
```json
{
  "token": "xxxxx",
  "nickname": "用户昵称",
  "userId": "12345"
}
```

**出参（无/过期）**：
```json
{
  "token": null
}
```

---

### validate-maoyan-authkey.mjs

**用途**：验证 AuthKey 是否有效

**入参**：
```json
{
  "token": "xxxxx"
}
```

**出参（有效）**：
```json
{
  "valid": true,
  "nickname": "用户昵称",
  "userId": "12345"
}
```

**出参（无效/过期）**：
```json
{
  "valid": false,
  "error": "token invalid"
}
```

---

### save-authkey.mjs

**用途**：保存 AuthKey 到本地

**入参**：
```json
{
  "token": "xxxxx"
}
```

**出参**：
```json
{ "success": true }
```

---

### clear-authkey.mjs

**用途**：清除本地 AuthKey（切换账号时调用）

**入参**：`{}`

**出参**：
```json
{ "success": true }
```

---

## 座位/订单类脚本

### get-seat-map.mjs

**用途**：获取座位图及推荐座位

**入参**：
```json
{
  "seqNo": "202604030409791",
  "ticketCount": 2
}
```
| 参数 | 必填 | 说明 |
|------|------|------|
| seqNo | 是 | 场次号（从 get-showtimes 获取） |
| ticketCount | 否 | 购票张数，默认1，最多4 |

**出参**：
```json
{
  "cinema": { "cinemaId": 11111, "cinemaName": "万达影城" },
  "show": { "showDate": "2026-04-03", "showTime": "10:30", "movieName": "飞驰人生3" },
  "buyNumLimit": 4,
  "regions": [{ "rows": [...] }],
  "seatMapText": "（座位图文本，直接展示给用户）",
  "recommendedSeats": [
    {
      "rowNum": "6",
      "rowId": "6",
      "columnId": "07",
      "seatNo": "0000000000000001-6-07",
      "price": 45,
      "sectionName": "默认分区"
    }
  ],
  "priceInfo": "¥45/张，2张共¥90"
}
```

---

### create-order.mjs

**用途**：创建订单（锁定座位）

**入参**：
```json
{
  "seqNo": "202604030409791",
  "seats": {
    "count": 2,
    "list": [
      {
        "rowId": "6",
        "columnId": "07",
        "seatNo": "0000000000000001-6-07",
        "seatStatus": 1,
        "seatType": "N",
        "sectionId": "0",
        "type": "N",
        "sectionName": "默认分区"
      }
    ]
  }
}
```

> ⚠️ seats.list 的每个座位对象必须从 **seatMapRows**（`get-seat-map` 返回的 `regions[0].rows`）中按 rowId + columnId 查找完整数据，**不可使用 `recommendedSeats` 直接作为参数**（字段不完整）：
> ```
> row  = seatMapRows.find(r => r.rowId === 目标rowId)
> seat = row.seats.find(s => s.columnId === 目标columnId)
> ```
> 必填字段（缺一不可）：
> - `rowId`       ← `seat.rowId`
> - `columnId`    ← `seat.columnId`
> - `seatNo`      ← `seat.seatNo`（不同影院格式不同，如 `"1101084102#05#09"` 或 `"0000000000000001-6-07"`，**不可自行构造**）
> - `seatStatus`  ← `seat.seatStatus`
> - `seatType`    ← `seat.seatType`
> - `type`        ← `seat.seatType`（与 seatType 相同，**不可省略**）
> - `sectionId`   ← `seat.sectionId`
> - `sectionName` ← `seat.sectionName`

**出参（成功）**：
```json
{
  "orderId": "ORDER_xxx",
  "lockExpireTime": 900
}
```

**出参（失败）**：
```json
{
  "code": 1004,
  "message": "座位已被占用"
}
```

---

### query-ticket-status.mjs

**用途**：查询出票状态

**入参**：
```json
{
  "orderId": "ORDER_xxx"
}
```

**出参**：
```json
{
  "payStatus": 1,
  "uniqueStatus": 9,
  "ticketCode": "取票码",
  "qrUrl": "取票二维码URL"
}
```

| payStatus | uniqueStatus | 含义 |
|-----------|-------------|------|
| 0 | - | 未支付 |
| 1 | 0-8 | 已支付，出票中 |
| 1 | 9 | 出票成功 |
| 1 | 10 | 出票失败 |

---

### render-seat-map.mjs

**用途**：以用户选中座位为中心渲染座位图，用于换座位时展示确认图

**入参**：
```json
{
  "rows": "<来自 get-seat-map.mjs 返回的 regions[0].rows，调用后缓存在 seatMapRows>",
  "centerSeats": [
    { "rowId": "5", "columnId": "08", "mark": "★" }
  ],
  "rowRange": 3,
  "colRange": 5
}
```

| 参数 | 必填 | 说明 |
|------|------|------|
| rows | 是 | 完整座位行数据，取自 get-seat-map 返回的 regions[0].rows |
| centerSeats | 是 | 中心座位列表，rowId/columnId 从 seatMapRows 中查找用户指定的排列号 |
| rowRange | 否 | 上下显示行数，默认 3 |
| colRange | 否 | 左右显示列数，默认 5 |

**出参**：
```json
{
  "seatMapText": "渲染后的座位图文本（直接展示给用户）",
  "centerSeats": [
    { "rowId": "5", "rowNum": "5", "columnId": "08", "seatNo": "xxx", "seatStatus": 1, "price": 45, "mark": "★" }
  ],
  "displayRange": {
    "rows": { "start": 2, "end": 8 },
    "cols": { "start": 3, "end": 13 },
    "primaryCenter": { "rowIndex": 4, "colIndex": 7 }
  }
}
```

> centerSeats 返回值包含完整座位信息，用于更新 selectedSeats

---

## 发送类脚本

### send-qr.mjs

**用途**：发送二维码图片或降级返回链接

**入参**：
```json
["auth", { "context": { "channel": "feishu_xxx", "targetId": "user_xxx" } }]
```

第一个参数为 `"auth"`（登录）或 `"pay"`（支付）。

**出参（成功发送）**：
```json
{ "success": true, "qrType": "auth" }
```

**出参（降级，无渠道信息）**：
```json
{
  "success": false,
  "fallback": true,
  "fallbackLink": "https://m.maoyan.com/mtrade/openclaw/token",
  "message": "无渠道信息，请在文案末尾附加以下链接发送给用户"
}
```
