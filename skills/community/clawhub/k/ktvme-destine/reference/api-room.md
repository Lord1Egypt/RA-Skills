# 包厢 API

> ⚠️ **前置依赖**：本接口文档依赖 `km-bot` 工具。详见 [cli-install.md](./cli-install.md)
>
> 📖 **通用约束**：字段映射规则和禁止事项详见 [api-overview.md](./api-overview.md)

---

## queryRoomAvailability - 包厢可预订情况查询

**用途**：一次性返回指定门店在指定到店时间附近，所有可预订的包厢时段列表。每一项可直接用于 `roomHourCreateOrder` 下单。

**调用方式**：

```bash
km-bot call saasktv queryRoomAvailability "{\"company_id\":1265,\"use_date\":\"2026-07-31\",\"begintime\":\"2026-07-31 17:00:00\",\"endtime\":\"2026-07-31 19:00:00\"}"
```

**请求参数**：

| 字段        | 类型   | 必填 | 说明                                                                             |
| ----------- | ------ | ---- | -------------------------------------------------------------------------------- |
| company_id  | Number | 是   | 商家id（来自 searchCompany 返回的 companyid）                                    |
| use_date    | String | 是   | 营业日，格式 YYYY-MM-DD                                                          |
| begintime   | String | **是** | 预计到店时间（YYYY-MM-DD HH:mm:ss）。**⚠️ 实际必填！不传则返回空 hour_packages** |
| endtime     | String | **是** | 查询范围结束时间（YYYY-MM-DD HH:mm:ss）。**⚠️ 实际必填！不传则返回空 hour_packages**。建议取到店时间 +3小时 |

> ⚠️ **【关键提醒】`begintime` 和 `endtime` 实际必填**：不传这两个参数时接口返回 `{"hour_packages": []}` 空数组。必须传入用户预计到店时间范围才能获取到可预订的包厢时段。
>
> `begintime` 取用户预计到店时间，`endtime` 取到店时间 + 合理范围（如 +3 小时）或门店营业结束时间。

**成功返回示例**：

```json
{
  "jsonrpc": "2.0",
  "id": "km_rpc_xxx",
  "result": {
    "ret": 0,
    "msg": "success",
    "data": {
        "use_date": "2026-07-31",
        "hour_packages": [
            {
                "room_id": "62",
                "room_name": "A03",
                "room_type_id": "39",
                "room_type_name": "5D包厢",
                "name": "5D包厢-60分钟",
                "begintime": "2026-07-31 17:00",
                "endtime": "2026-07-31 18:00",
                "charge": 10,
                "protocolcharge": 10,
                "longtime": 60,
                "activity_id": "1001",
                "available_room_count": 2
            },
            {
                "room_id": "947",
                "room_name": "1004",
                "room_type_id": "110",
                "room_type_name": "中包",
                "name": "中包-60分钟",
                "begintime": "2026-07-31 17:00",
                "endtime": "2026-07-31 18:00",
                "charge": 20,
                "protocolcharge": 30,
                "longtime": 60,
                "activity_id": "1002",
                "available_room_count": 1
            }
        ]
    }
  }
}
```

**返回字段说明（顶层）**：

| 字段                       | 类型     | 说明                                                  |
| -------------------------- | -------- | ----------------------------------------------------- |
| data.use_date              | String   | 营业日                                                |
| data.hour_packages         | Array    | **可预订包厢时段列表**（已按 room_type 去重）         |

**hour_packages[] 字段说明**：

| 字段                | 类型   | 说明                                                              |
| ------------------- | ------ | ----------------------------------------------------------------- |
| room_id             | String | 包厢ID（**用于 roomHourCreateOrder 的 roomid**）                  |
| room_name           | String | 包厢名称（展示给用户）                                            |
| room_type_id        | String | 包厢类型ID                                                        |
| room_type_name      | String | 类型名称（**用于展示与分组**）                                    |
| name                | String | 时段展示名称（如"5D包厢-60分钟"）                                 |
| begintime           | String | 时段开始时间（**用于下单，格式 yyyy-MM-dd HH:mm**）               |
| endtime             | String | 时段结束时间（**用于下单，格式 yyyy-MM-dd HH:mm**）               |
| charge              | Number | 售价（**用于下单，直接使用无需校准**）                            |
| protocolcharge      | Number | 原价（**用于下单，直接使用无需校准**）                            |
| longtime            | Number | 时长（分钟）                                                      |
| activity_id         | String | 活动ID（用于 roomHourCreateOrder 的 id 参数，**部分门店不返回此字段，不返回时可省略**） |
| available_room_count | Number | 该时段该类型剩余可订房间数（展示用）                              |

**关键设计说明**：

1. **hour_packages 结构**：每一项是一个可直接下单的包厢时段，含完整下单所需字段
2. **去重**：同一 `room_type` 的多个房间合并展示，仅暴露 `available_room_count`，选项不重复
3. **价格即最终价**：`charge` / `protocolcharge` 可直接用于 `roomHourCreateOrder`，无需再调 `roomHourCheckPrice`
4. **下单衔接**：用户选定某项后，字段直接映射到 `roomHourCreateOrder`：
   - `room_id` → `roomid`
   - `begintime` / `endtime` → `begintime` / `endtime`
   - `charge` / `protocolcharge` → `charge` / `protocolcharge`
   - `activity_id` → `id`
   - `source` 固定传 `7`

**异常返回**：

```json
{
  "jsonrpc": "2.0",
  "id": "km_rpc_xxx",
  "result": {
    "ret": -1,
    "msg": "查询失败"
  }
}
```