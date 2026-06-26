---
name: mcd-mcp-skills
description: 麦当劳MCP平台集成，提供餐品营养查询、外送点餐、配送地址管理、优惠券管理、积分兑换等20个完整功能；当用户需要查询麦当劳餐品营养、下单外卖、管理地址、查询或领取优惠券、兑换积分商品时使用
metadata: {"openclaw":{"requires":{"env":["MCD_MCP_TOKEN"]},"primaryEnv":"MCD_MCP_TOKEN"}}
---

# 麦当劳MCP平台集成

## 任务目标
- 本Skill用于：集成麦当劳MCP Server，提供完整的麦当劳服务访问能力
- 能力包含：餐品营养信息查询、外送点餐全流程、地址管理、优惠券管理、积分账户管理、积分兑换、营销活动查询等20个功能
- 触发条件：用户询问麦当劳餐品信息、想要点外卖、管理配送地址、查看或使用优惠券、查询或使用积分、了解营销活动等

## 前置准备
- 依赖说明：脚本依赖已在运行环境预装，无需额外安装
- 凭证配置：需要配置麦当劳MCP Token
  - 访问 https://open.mcd.cn 注册并创建应用获取Token
  - 系统已为您创建凭证配置入口，请按提示填写

## 操作步骤

### 一、餐品信息查询

#### 1. 查询餐品营养信息
当用户询问麦当劳餐品的热量、营养成分时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py list-nutrition-foods
```

**功能说明：**
- 获取麦当劳常见餐品的营养成分数据
- 包括能量、蛋白质、脂肪、碳水化合物、钠、钙等信息
- 可用于帮助用户搭配指定热量的套餐

#### 2. 查询门店可售餐品列表
当用户想了解某个门店有哪些餐品时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py query-meals --store-code <门店编码> --be-code <BE编码>
```

**必需参数：**
- `--store-code`: 门店编码（从配送地址查询获取）
- `--be-code`: BE编码（从配送地址查询获取）

**功能说明：**
- 查询指定门店可售卖的餐品菜单
- 返回分类、餐品编码、标签等信息

#### 3. 查询餐品详情
当用户想了解某个餐品的详细组成时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py query-meal-detail --meal-code <餐品编码>
```

**必需参数：**
- `--meal-code`: 餐品编码（从餐品列表查询获取）

**功能说明：**
- 查询餐品的详细信息
- 包括套餐组成、默认选择等

### 二、配送地址管理

#### 4. 查询用户配送地址列表
当用户需要查看或选择配送地址时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py delivery-query-addresses
```

**功能说明：**
- 查询用户已创建的配送地址列表
- 返回地址信息及对应门店信息（storeCode、beCode）
- 用于后续点餐选择配送地址

#### 5. 新增配送地址
当用户需要添加新的配送地址时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py delivery-create-address \
  --address "详细地址" \
  --lat "纬度" \
  --lng "经度" \
  --contact "联系人" \
  --phone "联系电话"
```

**必需参数：**
- `--address`: 详细地址
- `--lat`: 纬度
- `--lng`: 经度
- `--contact`: 联系人姓名
- `--phone`: 联系电话

### 三、外送点餐流程

#### 6. 查询门店可用优惠券
当用户点餐前想查看可用优惠时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py query-store-coupons --store-code <门店编码>
```

**必需参数：**
- `--store-code`: 门店编码

**功能说明：**
- 查询用户在当前门店下可使用的优惠券列表
- 用于点餐时选择可用优惠

#### 7. 商品价格计算
当用户选择商品后需要计算总价时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py calculate-price \
  --store-code <门店编码> \
  --be-code <BE编码> \
  --items '[{"mealCode":"餐品编码","quantity":1}]' \
  --coupons '["优惠券ID"]'
```

**必需参数：**
- `--store-code`: 门店编码
- `--be-code`: BE编码
- `--items`: 商品列表（JSON格式）

**可选参数：**
- `--coupons`: 优惠券ID列表（JSON格式）

**功能说明：**
- 根据选购商品和优惠券计算价格
- 返回商品金额、配送费、优惠金额及应付总价

#### 8. 创建外送订单
当用户确认下单时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py create-order \
  --store-code <门店编码> \
  --be-code <BE编码> \
  --address-id <地址ID> \
  --items '[{"mealCode":"餐品编码","quantity":1}]' \
  --coupons '["优惠券ID"]'
```

**必需参数：**
- `--store-code`: 门店编码
- `--be-code`: BE编码
- `--address-id`: 配送地址ID
- `--items`: 商品列表（JSON格式）

**可选参数：**
- `--coupons`: 优惠券ID列表

**功能说明：**
- 创建外送订单
- 返回订单详情与支付链接

#### 9. 查询订单详情
当用户需要查看订单状态时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py query-order --order-id <订单ID>
```

**必需参数：**
- `--order-id`: 订单ID

**功能说明：**
- 查询订单状态、订单内容、配送信息等
- 用于查看订单进度或确认订单信息

### 四、优惠券管理

#### 10. 麦麦省券列表查询
当用户想查看当前可领取的优惠券时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py available-coupons
```

**功能说明：**
- 查询麦麦省当前可领取的优惠券列表

#### 11. 麦麦省一键领券
当用户想一次性领取所有可用优惠券时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py auto-bind-coupons
```

**功能说明：**
- 自动领取麦麦省所有当前可用的麦当劳优惠券
- 无需指定具体优惠券，系统自动领取所有可领的券

#### 12. 我的优惠券查询
当用户想查看自己已有的优惠券时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py query-my-coupons
```

**功能说明：**
- 查询用户可用的优惠券列表
- 类似打开麦当劳App的"我的优惠券"页面
- 显示所有可以用来点餐的优惠券

### 五、积分账户管理

#### 13. 我的积分查询
当用户想查询积分余额时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py query-my-account
```

**功能说明：**
- 查询用户积分账户信息
- 包括可用积分、累计积分、冻结积分、即将过期积分等

### 六、积分商城兑换

#### 14. 积分兑换商品列表
当用户想用积分兑换商品时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py mall-points-products
```

**功能说明：**
- 查询麦麦商城内可用积分兑换的餐品券
- 不包含积分兑换的实物或第三方码

#### 15. 积分兑换商品详情
当用户想了解某个积分商品的详细信息时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py mall-product-detail --product-id <商品ID>
```

**必需参数：**
- `--product-id`: 商品ID

**功能说明：**
- 查询指定积分兑换商品券的详细信息
- 包括图片、积分、有效期、说明、详情等

#### 16. 积分兑换商品下单
当用户确认用积分兑换商品时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py mall-create-order --product-id <商品ID>
```

**必需参数：**
- `--product-id`: 商品ID

**功能说明：**
- 使用积分兑换指定餐品券
- 完成积分扣减并发放券码
- 返回兑换订单号与券码信息

### 七、营销活动

#### 17. 活动日历查询
当用户想了解麦当劳的营销活动时使用。

**调用方式：**
```python
python scripts/mcd_mcp_client.py campaign-calendar
```

**功能说明：**
- 查询麦当劳中国当月的营销活动日历
- 返回进行中、往期和未来日期的活动

### 八、工具辅助

#### 18. 获取当前时间信息
获取当前时间，用于确定活动有效期、订单时间等。

**调用方式：**
```python
python scripts/mcd_mcp_client.py now-time-info
```

**功能说明：**
- 返回当前的完整时间信息
- 用于了解当前时间和日期

## 资源索引
- MCP客户端脚本：见 [scripts/mcd_mcp_client.py](scripts/mcd_mcp_client.py)
- 工具参数详细说明：见 [references/tools_reference.md](references/tools_reference.md)

## 注意事项
- 所有API调用需要有效的MCP Token，请确保凭证已正确配置
- 门店编码（storeCode）和BE编码（beCode）需要从配送地址查询接口获取
- 餐品编码（mealCode）需要从餐品列表查询接口获取
- 创建订单前需要先查询配送地址、餐品列表、计算价格
- 积分兑换会扣减积分，请提示用户确认后再操作
- 所有JSON参数需使用单引号包裹，如：`--items '[{"mealCode":"XXX","quantity":1}]'`

## 使用示例

### 示例1：查询餐品营养信息
用户："帮我查一下麦当劳有哪些餐品的营养信息"

**执行步骤：**
1. 调用营养信息查询工具
```bash
python scripts/mcd_mcp_client.py list-nutrition-foods
```
2. 向用户展示营养数据，帮助用户了解各餐品的热量和营养成分

### 示例2：完成一次外送点餐
用户："我想在麦当劳点一个巨无霸套餐送到家"

**执行步骤：**
1. 查询配送地址
```bash
python scripts/mcd_mcp_client.py delivery-query-addresses
```
2. 查询门店可售餐品
```bash
python scripts/mcd_mcp_client.py query-meals --store-code XXX --be-code XXX
```
3. 查询餐品详情（获取巨无霸套餐编码）
```bash
python scripts/mcd_mcp_client.py query-meal-detail --meal-code XXX
```
4. 查询可用优惠券
```bash
python scripts/mcd_mcp_client.py query-store-coupons --store-code XXX
```
5. 计算价格
```bash
python scripts/mcd_mcp_client.py calculate-price --store-code XXX --be-code XXX --items '[{"mealCode":"XXX","quantity":1}]'
```
6. 创建订单
```bash
python scripts/mcd_mcp_client.py create-order --store-code XXX --be-code XXX --address-id XXX --items '[{"mealCode":"XXX","quantity":1}]'
```
7. 向用户提供支付链接

### 示例3：领取并使用优惠券
用户："帮我领一下麦当劳的优惠券，然后看看我有哪些券"

**执行步骤：**
1. 一键领取麦麦省优惠券
```bash
python scripts/mcd_mcp_client.py auto-bind-coupons
```
2. 查询我的优惠券
```bash
python scripts/mcd_mcp_client.py query-my-coupons
```
3. 向用户展示已领取的优惠券列表

### 示例4：积分兑换商品
用户："我想用积分兑换一个麦辣鸡腿堡，帮我看看需要多少积分"

**执行步骤：**
1. 查询积分余额
```bash
python scripts/mcd_mcp_client.py query-my-account
```
2. 查询积分兑换商品列表
```bash
python scripts/mcd_mcp_client.py mall-points-products
```
3. 找到麦辣鸡腿堡对应的商品ID，查询详情
```bash
python scripts/mcd_mcp_client.py mall-product-detail --product-id XXX
```
4. 向用户展示所需积分和商品详情
5. 用户确认后，执行兑换
```bash
python scripts/mcd_mcp_client.py mall-create-order --product-id XXX
```
