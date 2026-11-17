# 用户接口（套餐信息 / 积分）

用于查询当前 Token 绑定用户的套餐列表、积分额度、已消耗、有效期和状态。

## 对应脚本

- 套餐 / 积分查询：`scripts/utils.py` 通用请求调 `/user/package/usage`（本接口 0 积分）

## 接口选择规则

`GET /user/package/usage`（**0 积分**）：
- 何时调：用户问「我还剩多少积分」「我的套餐」「额度够不够」、准备连续大量调用前确认、收到「积分不足」错误时
- 何时不调：纯业务分析、不需要每次 API 前都查（按需）

---

## GET /user/package/usage 我的套餐信息

> ⚡ **0 积分** ｜ 无请求参数（通过 Authorization 头识别用户）｜ 方法：GET

### 返回字段

**外层公共**：`code / msg / data / timestamp`

**`data` 顶层字段（必须优先展示）**：
- `nickName`：用户名/昵称
- `phoneNo`：电话号码
- `packageList[]`：套餐数组（每条见下）

**`data.packageList[*]` 单套餐字段**：
- `settingId`：内部主键（一般不展示）
- `tcId`：套餐编码 → 查下方「tcId 映射表」得套餐中文名
- `tcCount`：**总积分**（无论 tcId=99 无限制套餐，均按数据库原值返回，不会 null）
- `useCount`：**已消耗积分**（不会 null）
- `buyDate`：购买时间 ISO
- `deadLine`：过期时间 ISO

### 衍生字段（本地计算，不要问后端）

| 衍生字段 | 公式/规则 |
|---|---|
| remainingPoints（剩余积分） | `tcCount - useCount` |
| tcName（套餐中文名） | 查 tcId 映射表 |
| packageTypeDesc（套餐类型描述） | 查 tcId 映射表 |
| status（状态） | **有效**：在有效期内 且（无限制 或 剩余>0）｜ **已过期**：超 deadLine ｜ **已用完**：有效期内但剩余≤0 |
| validPeriod（有效期描述） | 正常：`yyyy-MM-dd ~ yyyy-MM-dd`｜ tcId=99：`长期有效`｜ 缺失：`""` |

### tcId 映射表

| tcId | 套餐中文名称 tcName | 套餐类型描述 packageTypeDesc |
|---:|---|---|
| 1 | 一个月 | 月度套餐（30天） |
| 2 | 一季度 | 季度套餐（90天） |
| 3 | 半年 | 半年套餐（180天） |
| 4 | 一年 | 年度套餐（365天） |
| 11 | 一次性加餐包 | 加餐包（可叠加，不独立有效期） |
| 99 | 无限制 | 不限量套餐（tcCount 仍按数据库超大数字显示，前端可展示为「∞」） |
| 其他 | 未知套餐 | 未知类型 |

---

## 套餐查询输出规范（AI 回答套餐/积分问题，必须严格此顺序格式）

> **核心原则**：先展示用户信息 → 再逐套餐展示 → 再汇总积分。**禁止把 `tcCount`/`useCount` 说成「次数」，必须读作「积分」**。

### phoneNo 隐私展示规则（Finding 5 强制合规）
> ⚠️ 手机号属于 PII。默认情况下任何回复里的 `phoneNo` 必须**脱敏**，格式 `前3位****后4位`（如 `138****8888`）。
>
> **只有一个例外**：用户在同一条消息里**明确写了「请完整显示我的手机号」/「显示明文手机号」**等明示请求，才可以在回复里输出 phoneNo 全文。任何其他情况（包括"给我看套餐"「查询积分」）都按脱敏处理。

### 展示顺序（严格执行）

1. **用户身份信息**（必须最先展示）：`查询用户：{nickName}（手机号：{phoneNo 脱敏格式}）`
   - 脱敏算法：长度 ≥ 7 位时 `phoneNo.slice(0,3) + '****' + phoneNo.slice(-4)`；<7 位时 `phoneNo.slice(0,1) + '****'`（确保不泄露）
   - 如果用户要求全文：写 `查询用户：{nickName}（手机号：{phoneNo 全文}，已按您的请求明文展示）`
2. **套餐列表表格**（遍历 packageList），列：
   - 套餐名（用 tcId 查映射表，**不要直接显示 tcId 数字**）
   - 类型（packageTypeDesc）
   - 总积分（tcCount）
   - 已用积分（useCount）
   - 剩余积分（tcCount − useCount）
   - 有效期（validPeriod）
   - 状态（✅有效 / ❌已过期 / ❌已用完）
3. **汇总**：所有「有效」套餐的剩余积分之和 = `当前可用总积分：X（N 份有效套餐）`
4. **紧接着附上下面的「各接口积分定价全表」**（不要等用户问）
5. 接 SKILL.md 的「积分消耗统计」（本接口 0 积分）
6. 接 SKILL.md 的「后续分析引导」话术

---

## 各接口积分定价全表（回答套餐后建议一并展示）

> 单次消耗；同一接口多次需累计；`GET /category/tree` 有缓存（默认 7 天）命中免费，首次/`--refresh` 扣 10 积分。

| 接口路径 | 功能描述 | 单次积分 |
|---|---|---:|
| `GET /category/tree` | 站点类目树（首次 10 / 命中缓存免费；默认缓存 7 天） | 10 |
| `GET /cost/weight/list/cbt` | 自发货运费重量列表 | 8 |
| `POST /items/search` | 商品查询（分页列表） | 5 |
| `POST /catalogs/search` | 目录链接查询（分页列表） | 4 |
| `POST /keywords/search` | 热搜词查询（日度 / 月度） | 3 |
| `GET /item/daily` | 商品每日历史数据 | 2 |
| `GET /item/monthly` | 商品每月历史数据 | 2 |
| `GET /item/keyword/reverse` | 商品流量词反查 | 2 |
| `GET /catalog/daily` | 目录链接每日历史数据 | 2 |
| `POST /seller/search` | 店铺查询（分页列表） | 2 |
| `GET /trends/price/list` | 行业价格分布 | 2 |
| `GET /trends/new/items` | 新品机会指数 | 2 |
| `GET /trends/brand/top/brands` | 竞争品牌（Top Brands） | 2 |
| `GET /trends/brand/top/sellers` | 竞争店铺（Top Sellers） | 2 |
| `GET /trends/sale/list` | 行业销量分布 | 2 |
| `GET /trends/sold/his` | 行业销量历史 | 2 |
| `GET /trends/statistical` | 行业趋势统计概览 | 2 |
| `GET /trends/store/inventoryType` | 仓储类型分布（FBA/FBM） | 2 |
| `GET /trends/brand/top/items` | 竞争商品（Top Items） | 2 |
| `GET /cost/weight/filter` | 运费查询 | 1 |
| `GET /rate/{siteId}` | 站点汇率查询 | 1 |
| `GET /item/info` | 商品详情概要 | 1 |
| `GET /item/review` | 商品评价信息 | 1 |
| `GET /catalog/info` | 目录链接详情 | 1 |
| `GET /user/package/usage` | 我的套餐信息 | 0 |

---

## 本模块积分明细表

| 接口 | 功能 | 积分 |
|---|---|---:|
| `GET /user/package/usage` | 我的套餐信息 | 0 |
