# 命令与参数

## 命令总览

| 命令 | 说明 | 必填参数 |
|------|------|---------|
| `login` | 检查鉴权状态 | 无 |
| `confirm_auth` | 检查鉴权有效性 | 无 |
| `search_poi` | POI 地址搜索 | `--keyword` |
| `get_address_list` | 获取用户地址簿 | 无 |
| `preview_and_submit` | 配送预览+提交一体化（推荐） | `--sender --recipient --goods` |
| `get_order_status` | 查询订单状态 | `--order-id` |

## 详细参数

### search_poi
```
--keyword <string>     搜索关键词（必填）
--city <string>        城市名（默认"北京"）
--lat <number>         纬度（E6整数或小数）
--lng <number>         经度（E6整数或小数）
```

### get_address_list
```
--address-type <int>   地址类型（默认 1）
--business-type <int>  业务类型（默认 1）
--scene <int>          场景（默认 2）
```

### preview_and_submit
```
--sender <JSON>              发件人地址对象（必填）
--recipient <JSON>           收件人地址对象（必填）
--goods <JSON>               物品信息对象（必填）
--business-type <string>     业务类型: 1=帮取送/帮忙, 2=帮买（默认 1）
--biz-type-scene-tag <string> 场景标签（默认 0，详见 params.md）
--business-type-tag <string>  业务类型标签（默认 0）
--conversation-id <string>   会话ID
--tip-fee <int>              小费（分，默认 0）
--purchase-detail <string>   帮买物品明细（businessType=2 时使用）
--remark <string>            备注
--confirm                    确认提交（不传则只预览）
```

### get_order_status
```
--order-id <string>    订单ID（必填）
```
