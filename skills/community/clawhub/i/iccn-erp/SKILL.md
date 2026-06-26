---
name: iccn-erp
description: 【零壹问界IC ERP外贸管理系统】，提供查询数据的技能。当用户提到查询订单、采购单、需求单、入库单、出库单、客户、供应商、库存、现货等任何ERP业务数据时，必须使用此技能。触发词包括但不限于："查订单"、"采购单详情"、"需求单"、"入库记录"、"出库情况"、"客户信息"、"供应商"、"现货库存"、"有没有货"、"库存多少"等，应立即触发此技能。
metadata: {"openclaw":{"primaryEnv":"ERP_API_TOKEN","requires":{"env":["ERP_API_TOKEN","ERP_API_BASE_URL"]}}}
---

# ERP 系统查询技能

## 统一调用规范

所有查询统一使用以下方式：

- **方法**：POST
- **Content-Type**：application/json
- **URL 格式**：`{ERP_API_BASE_URL}/v1/{table}/lists`
- **Token**：从环境变量 `ERP_API_TOKEN` 读取
```javascript
const ERP_TOKEN = process.env.ERP_API_TOKEN;
const ERP_BASE_URL = process.env.ERP_API_BASE_URL;

const erpQuery = async (table, params = {}) => {
  const url = `${ERP_BASE_URL}/v1/${table}/lists`;
  const body = {
    page: 1,
    pagenum: 50,
    like: {},
    where: {},
    order: {},
    ...params
  };
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'authorization': `Bearer ${ERP_TOKEN}`
    },
    body: JSON.stringify(body)
  });
  return await response.json();
};
```

---

## 表格映射

| 用户说的             | table 名称           | 说明       |
|----------------------|----------------------|------------|
| 订单、销售单         | `order`              | 销售订单   |
| 采购单、采购订单     | `purchase`           | 采购单     |
| 需求单、需求         | `demand`             | 需求单     |
| 入库单、入库记录     | `purchase_in`        | 采购入库单 |
| 出库单、出库记录     | `order_out`          | 销售出库单 |
| 客户、客户信息       | `customer`           | 客户档案   |
| 供应商、供应商信息   | `supplier`           | 供应商档案 |
| 现货、库存、有没有货 | `products_inventory` | 现货库存   |

---

## 查询参数说明

| 参数    | 类型   | 说明                             |
|---------|--------|----------------------------------|
| page    | number | 页码，默认 1                     |
| pagenum | number | 每页条数，默认 50                |
| like    | object | 模糊搜索，如 `{"model":"ABC"}`   |
| where   | object | 精确过滤，如 `{"status":"1"}`    |
| order   | object | 排序，如 `{"created_at":"desc"}` |

---

## 调用示例
```javascript
const data = await erpQuery('order', { where: { order_no: 'SO20240001' } });
const data = await erpQuery('products_inventory', { like: { model: 'ABS10' } });
const data = await erpQuery('customer', { like: { name: 'ABC公司' } });
const data = await erpQuery('supplier', { like: { name: '某供应商' } });
const data = await erpQuery('purchase', { where: { purchase_no: 'PO20240001' } });
const data = await erpQuery('purchase_in', { where: { purchase_no: 'PO20240001' } });
const data = await erpQuery('order_out', { where: { order_no: 'SO20240001' } });
const data = await erpQuery('demand', { like: { model: 'ABC123' } });
```

---

## 调用流程

1. **识别意图**：对照"表格映射"确定 `table`
2. **提取参数**：有单号用 `where` 精确匹配，有关键词用 `like` 模糊搜索，不足则主动询问
3. **调用接口**：使用 `erpQuery(table, params)` 发起请求
4. **展示结果**：以表格形式展示，标注总条数
5. **报错处理**：401 提示 Token 过期；空结果提示检查参数

## 注意事项

- Token 和 API 地址通过环境变量注入，在 `openclaw.json` 的 `skills.entries.iccn-erp.env` 中配置
- 更换 Token 只需修改 `openclaw.json`，无需改动此文件
- 模糊搜索用 `like`，精确匹配用 `where`，可同时使用
