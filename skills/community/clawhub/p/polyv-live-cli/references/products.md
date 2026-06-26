# 商品管理

管理直播频道商品、频道商品库开关和平台商品库。常用子命令包括 `list`、`add`、`update`、`delete`、`enabled`、`update-enabled`。

## 商品列表

查询频道商品：

```bash
<CLI> product list -c <频道ID>
<CLI> product list -c <频道ID> -P 2 -s 10
<CLI> product list -c <频道ID> -o json
```

查询平台商品库：

```bash
<CLI> product list --platform
<CLI> product list --platform -P 2 -s 10 -o json
```

| 参数 | 说明 |
| --- | --- |
| `-c, --channel-id` | 频道 ID，查询频道商品时使用 |
| `--platform` | 查询账号级平台商品库 |
| `-P, --page` | 页码，默认 `1` |
| `-s, --size` | 每页条数，范围 `1-100`，默认 `20` |
| `-o, --output` | `table` 或 `json` |

## 频道商品库开关

查询频道商品库是否开启：

```bash
<CLI> product enabled -c <频道ID>
<CLI> product enabled -c <频道ID> -o json
```

开启或关闭频道商品库：

```bash
<CLI> product update-enabled -c <频道ID> --enabled Y --force -o json
<CLI> product update-enabled -c <频道ID> --enabled N --force -o json
```

| 参数 | 说明 |
| --- | --- |
| `-c, --channel-id` | 频道 ID |
| `--enabled` | `Y` 开启，`N` 关闭 |
| `-f, --force` | 跳过确认提示 |
| `-o, --output` | `table` 或 `json` |

`product enabled` 只查询状态，不会修改频道商品库；需要让观看页展示商品时，必须使用 `product update-enabled --enabled Y`。

## 添加商品

创建商品只会新增频道商品数据，不会自动打开观看页商品库开关。若用户目标是“观看页展示商品”或“直播间商品可见”，创建/上架商品后还要确认 `product enabled`，必要时执行 `product update-enabled --enabled Y`。

普通商品：

```bash
<CLI> product add \
  -c <频道ID> \
  -n "测试商品" \
  --status 1 \
  --link-type 10 \
  -l "https://example.com/product" \
  --cover "https://example.com/cover.jpg" \
  --real-price 99.9 \
  --price 199.9
```

多端链接商品：

```bash
<CLI> product add \
  -c <频道ID> \
  -n "多端商品" \
  --status 1 \
  --link-type 11 \
  --pc-link "https://example.com/pc" \
  --mobile-link "https://example.com/mobile" \
  --real-price 99.9 \
  --price 199.9
```

## 更新商品

更新商品的上架状态只影响该商品是否可售，不会自动修改频道商品库开关。

```bash
<CLI> product update \
  -c <频道ID> \
  -p 12345 \
  -n "新商品名" \
  --status 1 \
  --link-type 10 \
  -l "https://example.com/product"
```

下架商品：

```bash
<CLI> product update \
  -c <频道ID> \
  -p 12345 \
  -n "商品名" \
  --status 2 \
  --link-type 10
```

## 删除商品

```bash
<CLI> product delete -c <频道ID> -p 12345
<CLI> product delete -c <频道ID> -p 12345 --force
```

## 常用参数

| 参数 | 说明 |
| --- | --- |
| `-c, --channel-id` | 频道 ID |
| `-p, --product-id` | 商品 ID，更新和删除时使用 |
| `-n, --name` | 商品名称 |
| `--status` | `1` 上架，`2` 下架 |
| `--link-type` | `10` 通用链接，`11` 多平台链接 |
| `-t, --product-type` | `normal`、`finance`、`position`，默认 `normal` |
| `--cover` | 商品封面 URL |
| `-l, --link` | 通用链接，`--link-type 10` 时使用 |
| `--pc-link`、`--mobile-link` | 多平台链接 |
| `--wx-miniprogram-link`、`--wx-miniprogram-original-id` | 微信小程序链接信息 |
| `--params`、`--features` | JSON 字符串 |
| `--product-desc` | 商品描述 |
| `--btn-show` | 按钮文案 |
| `--price-type`、`--real-price`、`--custom-price` | 到手价配置 |
| `--original-price-type`、`--price`、`--custom-original-price` | 原价配置 |

## 使用注意

- 当前 npm 版没有商品详情查询子命令，需要通过 `product list -o json` 获取列表数据。
- 频道商品库开关和商品上架状态是两层条件：商品已上架后，还需要频道商品库为 `Y`，观看页才会展示商品。
- 用户说“上架商品”通常对应 `product add` 或 `product update --status 1`；用户说“观看页展示商品”“直播间显示商品列表”还需要 `product update-enabled --enabled Y`。
- `delete` 不可撤销，建议先 `list` 核对商品 ID。
- 价格在输出中按人民币展示，脚本处理时优先使用 JSON。
