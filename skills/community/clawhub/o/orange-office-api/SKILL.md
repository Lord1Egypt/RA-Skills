---
name: orange-office-api
description: 橙子通（orange-office.cn）库存管理系统 API 自动化。用于通过 API 创建出库单、查询库存、管理主播仓库等，无需浏览器。
---

# 橙子通 API 自动化技能

通过 API 操作橙子通库存管理系统，包括创建出库单、查询库存、管理主播仓库等。

## 基础信息

- **API 站点**：https://orange-office.cn
- **签名 Salt**：`68756c61`
- **Cookie**：`ASP.NET_SessionId=<当前有效会话>`

## 双系统识别

| 系统名 | teamId | 用途 |
|---|---|---|
| 库存通-库存通 | 952393 | 固定仓库出入库 |
| 库存通-幼稚鬼潮玩 | 724308 | **主播出库用这个** |

## API 调用

### 签名算法

```python
import hashlib

SALT = '68756c61'

def md5(data: str) -> str:
    return hashlib.md5((SALT + data).encode()).digest().hex()
```

所有 API 请求 body 经过签名，`sign = md5(json.dumps(body, separators=(',',':')))`

### 请求头

```python
headers = {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'sign': md5(json.dumps(body, separators=(',',':'))),
    'client': 'pcWeb',
    'Cookie': f'ASP.NET_SessionId={SESSION}'
}
```

### 常用 API

| 功能 | 路径 | 说明 |
|---|---|---|
| 创建出库单 | POST /stock/stockout/create | |
| 修改出库单 | POST /stock/stockout/update | |
| 删除出库单 | POST /stock/stockout/delete | |
| 获取出库单列表 | POST /stock/stockout/getList | |
| 获取出库单详情 | POST /stock/stockout/getInfo | |
| 查询库存 | POST /stock/prod/getStockList | 必须带 locId |

## 查询库存

```python
POST /stock/prod/getStockList
{
    "keyword": "", "catId": "", "page": 1, "rows": 500,
    "sort": "barcode", "order": "descending",
    "teamId": 724308,        # 场景B用724308，场景A用952393
    "ifValue": "Y",
    "ifShowSku": "Y",
    "ifShowZero": "N",
    "locId": 63              # 仓库ID，必须填写
}
```

返回：`response.obj.list[]` — 每项含 `prodId`、`prodName`、`stockQty`、`outPrice`

## 创建出库单

```python
POST /stock/stockout/create
{
    "teamId": 724308,
    "outNo": "",             # 空字符串自动生成
    "outDate": "2026-03-26",
    "refId": 695620,         # 抖店售卖
    "refName": "抖店售卖",
    "locId": 63,             # 仓库ID
    "locName": "梅天娇",
    "amount": 1234.56,       # 总金额 = 各行 amount 之和
    "remark": "机器人操作",
    "itemList": [
        {
            "prodId": 9973574,
            "qty": 24,
            "price": 15,      # 单价从 getStockList 的 outPrice 字段获取
            "amount": 360,    # qty × price，保留2位小数
            "outQty": 24,
            "stockQty": 36
        }
    ]
}
```

**注意**：
- 单价用 `outPrice`（不是 price）
- 金额：`amount = qty × outPrice`，保留2位小数
- 总金额 `amount` = 各行 amount 之和

## 出库操作三原则

1. **只认"销售数量"字段** — 其他字段（库存、今日转仓、销售金额等）一律不看
2. **每个主播只建一张出库单** — 出错时在原单上修改，不删除重建
3. **先查库存再创建** — 必须先调 API 查询实际库存，确认足够后再创建

## 主播仓库 locId 对应表

**系统：库存通-幼稚鬼潮玩（teamId=724308）**

| 主播 | locId |
|---|---|
| 邓晓美 | 15 |
| 梅天娇 | 63 |
| 罗文婧 | 57 |
| 苟林分 | 71 |
| 张儒尊 | 16 |
| 廖紫帆 | 68 |
| 冉红霞 | 9 |
| 周语妍 | 7 |
| 杜瑶 | 79 |
| 倪玉婷 | 44 |
| 曹洢珂晗 | 80 |
| 谷乐欣 | 49 |
| 高李伟 | 69 |
| 王馨宇 | 30 |
| 李妍茜 | 29 |
| 钟雨欣 | 8 |
| 黄敏慧 | 50 |
| 廖文琪 | 3 |
| 杨名 | 10 |
| 刘明月 | 4 |

## 钉钉主播库存表

- **baseId**：`dxXB52LJqnrEb4pjcQQQjq598qjMp697`
- **每个主播有独立的 tableId**

| 主播 | tableId | 销售数量字段 |
|---|---|---|
| 邓晓美 | yj6ZAgX | Ccg9VfH |
| 梅天娇 | exNEdWq | lFRkHI3 |
| 罗文婧 | TZvYd1V | ACXQniC |
| 苟林分 | kIcLRmk | YdlC9og |
| 张儒尊 | yy2mQJS | 6WcPYAw |
| 廖紫帆 | ER5lrFr | LMixcf1 |
| 冉红霞 | YMnnPwV | tzjnNNK |
| 周语妍 | JR04qLu | qKu49Ok |
| 杜瑶 | 143LNaM | Y3XobF0 |
| 倪玉婷 | HTfR4Pu | BKCiXNl |
| 曹洢珂晗 | xyAVrjr | KilxGYr |
| 谷乐欣 | MwtqlRv | 05RaEdP |
| 高李伟 | ETlz1vw | Y3FmkMG |
| 王馨宇 | 6xK7UjK | So8eWZ5 |
| 李妍茜 | wUBEIED | dtZXTtB |
| 钟雨欣 | 3P6EtSy | o9BFZd2 |
| 黄敏慧 | sXo9484 | vCBtAiB |
| 廖文琪 | vFkcdBh | BleldKK |
| 杨名 | 11ESFXj | OXj619G |
| 刘明月 | RFkRdbH | eKjh1jK |

**注意**：每个主播的"销售数量"字段ID可能不同，操作前必须先调用 `get_fields` 读取表头确认。

## 商品名称注意

- kpl**竟**燃礼盒（是"竟"不是"竞"）
- pel物竞天择风云变系列**盲抽镭射票** 和 **盲抽亚克力挂件** 是两个不同商品
- 卡夹类（130pt卡夹、75pt卡夹等）忽略，无需出库

## 钉钉主播库存表写入规范（重要！）

录入主播库存快照时，**必须包含以下全部字段**：

| 字段 | 说明 | 来源 |
|---|---|---|
| 日期 | 库存账面日期 | 手动指定，如 `2026-03-27T00:00:00+08:00` |
| 商品编号 | 商品编码 | API `getStockList` 返回的 `prodNo` |
| 商品名称 | 商品全名 | API `getStockList` 返回的 `prodName` |
| 规格型号 | 包装规格 | API `getStockList` 返回的 `prodSpec` |
| 单位 | 计量单位 | API `getStockList` 返回的 `unit` |
| 库存数量 | 账面库存 | 计算得出（当前库存 + 当日出库回补） |

**写入格式**：使用 `cells` 而非 `fields`，每个字段对应其 `fieldId`：
```javascript
const records = snapshot.map(item => ({
  cells: {
    [fieldId_日期]: '2026-03-27T00:00:00+08:00',
    [fieldId_商品编号]: item.prodNo || '',
    [fieldId_商品名称]: item.prodName,
    [fieldId_规格型号]: item.prodSpec || '',
    [fieldId_单位]: item.unit || '包',
    [fieldId_库存数量]: item.qty,
    // 以下字段填0或空
    [fieldId_今日入库]: 0,
    [fieldId_今日剩余]: 0,
    [fieldId_销售金额]: '',
    [fieldId_送出]: 0,
    [fieldId_销售数量]: 0,
    [fieldId_今日转仓]: 0
  }
}));
```

**日期格式**：必须是 ISO 格式（如 `2026-03-27T00:00:00+08:00`），不能只写 `2026-03-27`。

**计算3月27日库存快照**：
1. 调用 `getStockList` 获取当前库存
2. 调用 `getList` 查询日期=3月27日的出库单
3. 对每张出库单调用 `getInfo` 获取明细
4. 将出库数量加回到当前库存，得到3月27日账面库存

**3月28日之后做快照**：由于3月27日之后可能还有出库，必须先查3月28日之后有无新的出库单，如有则同样回补。如果3月28日至今无出库单，直接用当前库存即为3月27日快照。

## 常见问题

**Q：保存时报"总金额错误"**
A：确保每个商品的 `amount = qty × outPrice`，且总金额 `obj.amount` 等于各行 `amount` 之和

**Q：商品找不到**
A：用更短的关键词搜索相近商品名称

**Q：Session 过期**
A：重新登录并获取新的 Cookie
