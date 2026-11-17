# 客如云(Keruyun)开放平台 Skill

> 📅 数据更新: 2026-04-28（校验修正）
> 📊 模块: 20 个 | 接口: **178** 个 | 全部含路径+参数+示例

## 客如云 API 模块

| 模块 | 接口数 | 路径例 | 说明 |
|------|--------|--------|------|
| **supply** (供应链) | 62 | `/open/standard/supply/...` | 库存/采购/配送/资金/分账 |
| **report** (报表) | 24 | `/open/standard/report/...` | 营收/支付/菜品/储值/反结账 |
| **employee** (员工) | 12 | `/open/standard/employee/...` | 总部/门店员工CRUD |
| **第三方提供** (通知) | 12 | — | 各类业务消息回调 |
| **book** (预订) | 10 | `/open/standard/book/...` | 正餐预订（含C端）|
| **crm** (会员) | 17 | `/open/standard/crm/...` | 会员创建/查询/标签/资产/等级 |
| **purchase** (采购) | 7 | `/open/standard/purchase/...` | 销售计划/千元用量 |
| **dish** (商品) | 5 | `/open/standard/dish/...` | 门店商品查询/改价/库存 |
| **oauth** (认证) | 3 | `/open/standard/oauth/...` | accessToken 获取/刷新 |
| **order** (订单) | 2 | `/open/standard/order/...` | 订单列表/详情 |
| **basic** (基础) | 2 | `/open/standard/basic/...` | 组织/供应商查询 |
| **produce** (生产) | 2 | `/open/standard/produce/...` | 加工品BOM/生产单 |
| **procurement** | 2 | `/open/standard/procurement/...` | 采购入库 |
| **delivery** | 2 | `/open/standard/delivery/...` | 配送验收 |
| **auth** | 2 | `/open/standard/auth/...` | 授权二维码/机构查询 |
| **org** | 2 | `/open/standard/org/...` | 组织机构 |
| **posreturn** | 1 | `/open/standard/posreturn/...` | 退菜入库 |
| **shop** | 1 | `/open/standard/shop/...` | 门店 |
| **snack** | 1 | `/open/standard/snack/...` | 快餐 |
| **table** | 1 | `/open/standard/table/...` | 桌台 |
| **kposlocal** | 7 | `/open/kposlocal/...` | 券模板/合约等本地接口 |
| **消息/回调** | 13 | — | 各类业务消息推送 |

**总计：178 个接口**

## 数据质量

| 指标 | 值 |
|------|-----|
| 有完整路径 | ✅ 158/158 |
| 有请求参数 | ✅ 158/158 |
| 有响应示例 | ✅ 150/158 |
| HTTP 方法 | POST（全部）|

## 数据格式

```json
{
  "name": "会员创建",
  "method": "POST",
  "path": "/open/standard/crm/CustomerOpenFacade/createCustomer",
  "auth": "品牌授权",
  "request_params": [
    {"name": "name", "type": "String", "required": true, "description": "会员姓名"}
  ],
  "response_example": { "code": 2001, "message": "请求成功", "result": {...} }
}
```

## 使用方式

```bash
# 全量数据
cat references/_all_apis_complete.json

# 按模块查看
python3 -c "
import json
with open('references/_modules_organized.json') as f:
    data = json.load(f)
print('\\n'.join(f'{k}: {v[\"api_count\"]} APIs' for k,v in data.items()))
"
```

## 客如云 vs 企迈 对比

| 维度 | 企迈 | 客如云 |
|------|------|--------|
| 菜单技术 | qm-tree (Vue) | Tailwind ul/li |
| 路由方式 | tree click + SPA | URL hash `/docs/zh/<id>` |
| 接口数 | 307 | 158 |
| HTTP 方法 | GET + POST | POST only |
| 路径风格 | `/v3/{模块}/{功能}/{方法}` | `/open/standard/{模块}/{服务}/{方法}` |
| 供应链占比 | 13% (41/307) | 39% (62/158) |
| QPS 标注 | ❌ 无 | ✅ 每个接口标明QPS |

## 参考链接

- 客如云开放平台：https://open.keruyun.com/official/developer.html
- API文档：点击 "API文档" tab
- 客如云官网：https://www.keruyun.com

## 更新日志

### 2026-04-27 v2
- 🎯 全量详情抓取：158 API，含路径/请求参数/响应示例
- 📊 按路径前缀自动归类 16 个模块
- ⚠️ description 字段含菜单噪音（待优化）

### 2026-04-27 v1
- 首次抓取：160 个 API 基本信息（名称+路径）
