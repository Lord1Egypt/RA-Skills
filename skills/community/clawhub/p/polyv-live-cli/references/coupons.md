# 优惠券管理

管理账号级优惠券，以及频道观看页领券入口。常用子命令包括 `add`、`list`、`delete`、`channel add`、`channel list`、`channel enabled`、`channel update-enabled`。

## 创建优惠券

创建优惠券只会新增账号级优惠券，不会自动在某个频道观看页展示。若用户目标是“观看页展示优惠券”或“直播间可领券”，创建优惠券后还要把优惠券绑定到频道，并打开频道领券开关。

满减券：

```bash
<CLI> coupon add \
  --name "满100减20" \
  --type MAX_OUT \
  --availableAmount 100 \
  --receiveStart 1704067200000 \
  --receiveEnd 1704153600000 \
  --useTimeType RANGE \
  --useStart 1704067200000 \
  --useEnd 1704758400000 \
  --condition FULL_REDUCE \
  --full 100 \
  --reduce 20 \
  --limitPerPerson 1
```

折扣券：

```bash
<CLI> coupon add \
  --name "8折优惠券" \
  --type DISCOUNT \
  --availableAmount 200 \
  --receiveStart 1704067200000 \
  --receiveEnd 1704153600000 \
  --useTimeType DAY \
  --dayOfUse 7 \
  --condition UNCONDITIONAL \
  --discount 80 \
  --limitPerPerson 1
```

## 查询优惠券

```bash
<CLI> coupon list
<CLI> coupon list -p 2 -s 20
<CLI> coupon list --status GOING -o json
```

| 参数 | 说明 |
| --- | --- |
| `-p, --page` | 页码 |
| `-s, --size` | 每页条数 |
| `--status` | `NOT_START`、`GOING`、`FINISHED`、`INVALID` |
| `-o, --output` | `table` 或 `json` |

## 频道优惠券展示

把账号级优惠券绑定到频道：

```bash
<CLI> coupon channel add -c <频道ID> --coupon-ids <优惠券ID> --force -o json
<CLI> coupon channel add -c <频道ID> --coupon-ids <优惠券ID1>,<优惠券ID2> --force -o json
```

查询频道已绑定优惠券：

```bash
<CLI> coupon channel list -c <频道ID>
<CLI> coupon channel list -c <频道ID> -o json
```

查询频道领券开关：

```bash
<CLI> coupon channel enabled -c <频道ID>
<CLI> coupon channel enabled -c <频道ID> -o json
```

开启或关闭频道领券入口：

```bash
<CLI> coupon channel update-enabled -c <频道ID> --enabled Y --force -o json
<CLI> coupon channel update-enabled -c <频道ID> --enabled N --force -o json
```

解绑频道优惠券：

```bash
<CLI> coupon channel delete -c <频道ID> --coupon-ids <优惠券ID> --force -o json
```

| 参数 | 说明 |
| --- | --- |
| `-c, --channel-id` | 频道 ID |
| `--coupon-ids` | 优惠券 ID，多个 ID 用英文逗号分隔，单次最多 30 个 |
| `--enabled` | `Y` 开启领券入口，`N` 关闭领券入口 |
| `-f, --force` | 跳过确认提示 |
| `-o, --output` | `table` 或 `json` |

`coupon channel enabled` 只查询状态，不会修改频道领券入口；需要让观看页展示领券入口时，必须使用 `coupon channel update-enabled --enabled Y`。

## 删除优惠券

```bash
<CLI> coupon delete --couponIds coupon001
<CLI> coupon delete --couponIds coupon001 coupon002 coupon003
```

单次最多删除 200 个优惠券 ID。

## 参数说明

| 参数 | 说明 |
| --- | --- |
| `--name` | 优惠券名称，最多 50 个字符 |
| `--type` | `MAX_OUT` 满减券，`DISCOUNT` 折扣券 |
| `--availableAmount` | 发放数量，`0` 表示按接口规则处理 |
| `--receiveStart`、`--receiveEnd` | 领取开始和结束时间，13 位毫秒时间戳 |
| `--useTimeType` | `RANGE` 指定可用时间范围，`DAY` 领取后若干天有效 |
| `--useStart`、`--useEnd` | `RANGE` 模式下的使用时间范围 |
| `--dayOfUse` | `DAY` 模式下领取后有效天数 |
| `--condition` | `UNCONDITIONAL` 无门槛，`FULL_REDUCE` 满减门槛 |
| `--discount` | 无门槛折扣值 |
| `--full`、`--reduce` | 满减门槛和减免金额 |
| `--limitPerPerson` | 每人限领数量，`-1` 表示不限 |

## 使用注意

- 优惠券命令不接收频道 ID。
- `coupon add` 创建的是账号级优惠券；观看页展示还需要 `coupon channel add` 绑定频道，并确认 `coupon channel update-enabled --enabled Y`。
- 当前 npm 版没有单张优惠券详情查询子命令，详情类需求先使用 `coupon list -o json`。
- 删除优惠券不可撤销，执行前核对 `--couponIds`。
