# 卡片推送

管理直播间的卡片配置，并在直播中推送或取消推送卡片。

## 当前 npm 命令面

```bash
<CLI> card-push list --channelId <频道ID>
<CLI> card-push create --channelId <频道ID> ...
<CLI> card-push update --channelId <频道ID> --cardPushId <卡片ID> ...
<CLI> card-push push --channelId <频道ID> --cardPushId <卡片ID>
<CLI> card-push cancel --channelId <频道ID> --cardPushId <卡片ID>
<CLI> card-push delete --channelId <频道ID> --cardPushId <卡片ID>
```

`card-push` 使用 camelCase 参数，例如 `--channelId`、`--cardPushId`、`--imageType`、`--showCondition`。

## 列出卡片

```bash
<CLI> card-push list --channelId <频道ID>
<CLI> card-push list --channelId <频道ID> -o json
```

## 创建卡片

手动推送卡片：

```bash
<CLI> card-push create \
  --channelId <频道ID> \
  --cardType common \
  --imageType giftbox \
  --title "限时优惠" \
  --link "https://shop.example.com/promo" \
  --duration 10 \
  --showCondition PUSH
```

观看时长触发卡片：

```bash
<CLI> card-push create \
  --channelId <频道ID> \
  --cardType common \
  --imageType redpack \
  --title "新手红包" \
  --link "https://shop.example.com/redpack" \
  --duration 15 \
  --showCondition WATCH \
  --conditionValue 30 \
  --conditionUnit SECONDS
```

## 更新卡片

```bash
<CLI> card-push update \
  --channelId <频道ID> \
  --cardPushId 123 \
  --title "更新后的标题" \
  --duration 20
```

## 推送、取消、删除

```bash
<CLI> card-push push --channelId <频道ID> --cardPushId 123
<CLI> card-push cancel --channelId <频道ID> --cardPushId 123
<CLI> card-push delete --channelId <频道ID> --cardPushId 123
```

## 常用参数

| 参数 | 说明 |
| --- | --- |
| `--channelId` | 频道 ID |
| `--cardPushId` | 卡片推送 ID，更新、推送、取消、删除时使用 |
| `--cardType` | `common` 或 `qrCode` |
| `--imageType` | `giftbox`、`redpack`、`custom`、`weixinWork` |
| `--title` | 卡片标题，最多 16 个字符 |
| `--link` | 点击跳转链接 |
| `--duration` | 倒计时秒数，支持 `0`、`5`、`10`、`20`、`30` |
| `--durationPosition` | `bottom` 或 `top` |
| `--showCondition` | `PUSH` 手动推送，`WATCH` 观看时长触发 |
| `--conditionValue` | 观看时长触发值 |
| `--conditionUnit` | `SECONDS` 或 `MINUTES` |
| `--countdownMsg` | 倒计时文案，最多 8 个字符 |
| `--enterEnabled` | `Y` 或 `N` |
| `--linkEnabled` | `Y` 或 `N` |
| `--redirectType` | `iframe` 或 `tab` |

## 使用注意

- `push` 会影响观众端展示，执行前确认频道 ID 和卡片 ID。
- `delete` 为删除配置操作，执行前建议先 `list` 核对。
- 写脚本时使用 `-o json`，避免依赖表格列宽。
