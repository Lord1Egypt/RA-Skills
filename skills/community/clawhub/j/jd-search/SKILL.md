# JD Search Skill - 工采云垂搜接口封装

## 概述

封装京东工采云垂搜搜索接口，支持关键词搜索、类目筛选、价格过滤等功能。

## 接口信息

- **接口地址**: `http://vproxy-search.jd.local/`
- **后台域名**: `http://gcy.p-search.jd.local/`
- **调用方式**: HTTP GET

## 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `client` | 调用方标识（13 位数字） | `1614133550001` |
| `key` | 搜索关键词 | `手机` |
| `charset` | 编码 | `utf8` |
| `urlencode` | 返回编码 | `yes` |
| `client_type` | 客户端类型 | `pc` 或 `app` |

## 可选参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `expression_key` | 组 id | `groupids,,131241`（可选，不传返回全部） |
| `page` | 页码 | `1` |
| `pagesize` | 每页数量 | `20` |
| `filt_type` | 过滤条件 | `redisstore,1`（有货） |
| `scene` | 场景 id | `0`（主搜） |

## 场景 ID 对照

- `0` - 主搜关键词
- `1` - 优惠券搜索默认跳转
- `5` - 类目列表页
- `9` - 店铺内全部商品
- `10` - 店铺内关键词

## 编码注意事项

- 中文参数需要用 UTF-8 编码后再 URL encode
- 空格必须 encode 为 `%20`，不能用 `+` 号
- 逗号 `,` 需要 encode 为 `%2C`

## 使用方法

### 基本搜索

```bash
jd-search "断路器"
```

### 指定页码和数量

```bash
jd-search "断路器" --page 2 --pagesize 50
```

### 按类目搜索

```bash
jd-search --catid 14081
```

### 带价格过滤

```bash
jd-search "断路器" --price 100-500
```

### 输出格式

```bash
jd-search "断路器" --format table    # 表格格式（默认）
jd-search "断路器" --format json     # JSON 格式
jd-search "断路器" --format csv      # CSV 格式
```

### 显示类目信息

```bash
jd-search "断路器" --with-category
```

## 返回字段

| 字段 | 说明 |
|------|------|
| `wareid` | 商品 ID |
| `item_sku_id` | SKU ID |
| `warename` | 商品名称 |
| `brand` | 品牌 |
| `dredisprice` | 价格 |
| `totalsales` | 销量 |
| `cid1/cid2/catid` | 类目 ID |
| `cid1name/cid2name/catname` | 类目名称 |

## 类目层级

商品可能分布在多个类目下，常见类目路径：

```
家装建材 / 电工电料 / 断路器
工业品 / 中低压配电 / 断路器
```

## 示例输出

```
SKUID           商品名称                                               品牌                           价格      类目路径                                    
100005261983    正泰 (CHNT) 空气开关 家用小型断路器 空开 NBE7 2P 32A               正泰                   ¥   39.84  家装建材 / 电工电料 / 断路器                       
100005259429    正泰 (CHNT) 空气开关 家用小型断路器 空开 NBE7 2P 63A               正泰                   ¥   42.47  家装建材 / 电工电料 / 断路器                       
```

## 注意事项

1. 接口为内网服务，需在京东内网环境调用
2. 默认 `expression_key` 不传，返回全部商品
3. 中文关键词自动进行 UTF-8 URL 编码
4. 响应时间约 15-20ms
