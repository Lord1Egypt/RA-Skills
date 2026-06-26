---
name: kuaishou-lifeservice-merchant
description: 快手生活服务-商家经营助手,为商家提供查询商品、查询商家门店、查询商家职人、查询商家官方账号、查询商家子账号、查询商家的经营数据等能力;
homepage: https://open.kwailocallife.com/
metadata: { "openclaw": { "emoji": "🏪", "requires": { "bins": ["python3"] ,"env":["KWAI_ACCESS_TOKEN"]},"primaryEnv":"KWAI_ACCESS_TOKEN" } }
---

# 快手生活服务-商家经营助手

## appkey配置引导
### ⚡ 快速开始

开发者申请 → 商家确认授权 → 获取 apiKey → 开始使用

#### 龙虾使用前置准备操作

如下为授权申请流程：

1. 打开快手开放平台：https://open.kwailocallife.com/
2. 点击「Skill 接入」→「立即接入」
3. 填写商家 ID，提交授权申请
4. 等待商家确认授权
5. 确认授权状态变为「已授权」后，复制 apiKey 发送给龙虾就可以使用了

#### 联系商家确认授权

如下为确认授权流程：

1. 主账号登录商家后台
2. 打开应用授权页面：https://lbs.kwailocallife.com/ll/merchant/league-sub/shop/empower
3. 在「待授权」列表中找到应用，点击「确认授权」

#### 注意

- 商家必须用主账号登录
- 授权后请及时告知开发者

#### 示例配置

```
ks700591219338675217#20234234234#sdfdsfas
```

快速使用：把以上配置信息直接发送给我就能测试验证啦。


### 🔐 账号配置指南

#### 添加您的商家账号

在使用各项功能前，请先添加您的快手商家账号信息：

**账号信息格式**：`{app_key}#{merchant_id}#{app_secret}`
（这3个信息可以在快手开放平台的后台获取）

##### 添加账号

```bash
python3 scripts/api_key_manager.py --add "您的app_key#您的merchant_id#您的app_secret"
```

添加成功后，系统会自动保存您的账号信息，下次使用时无需重复输入。

##### 查看已保存的账号

```bash
python3 scripts/api_key_manager.py --list
```

会显示类似这样的结果：
```
[1] app_key=ks656118173425091421, merchant_id=1234567
[2] app_key=ks656118173425091422, merchant_id=1234568 (当前使用)
```

##### 切换使用哪个账号

如果您有多个门店账号，可以这样切换：

```bash
python3 scripts/api_key_manager.py --select 1
```

##### 查看当前使用的账号
```bash
python3 scripts/api_key_manager.py --current
```

## 功能
| 操作       | 说明                             | 触发示例                                                        |
|----------|--------------------------------|-------------------------------------------------------------|
| 查询商家品牌资质 | 查询商家品牌资质                       | "商家品牌资质"                                                    |
| 查询职人     | 查询商家职人信息                       | "职人列表"、"查询职人"                                               |
| 查询职人数据   | 查询商家职人数据                       | "职人数据"、"查询职人数据汇总"                                           |
| 查询实时经营汇总 | 查询商家实时交易/退款数据                  | " 查询交易实时汇总 "、" 查询退款数据汇总"                                    |
| 查询待办事项   | 查询商家待办事项                       | "商家待办事项"、"查询待办事项列表"                                         |
| 查询职人自动激励 | 查询商家职人自动激励                     | "查询职人自动激励信息"、"查询商家职人激励信息"                                   |
| 查询子账号    | 查询商家子账号列表                      | "查询子账号列表"、"查询子账号" 、"有哪些子账号"                                 |
| 查询经营数据   | 查询经营数据                         | "经营表现"、"经营情况"、"经营状况"、"GMV表现" 、"诊断数据"、"经营数据" 、"店铺数据" 、"交易数据" |
| 评价管理     | 查询某个门店的用户评价评分                  | "用户评价评分"、"评价评分"、"查询某个门店"、"门店评分"                             |
| 评价管理     | 查询某个门店下最新的某些条件的评论              | "最新用户评价评分"、"最新评价评分"、"最新查询某个门店"、"最新门店评分"                     |
| 评价管理     | 查询评价分析                         | "分析评价"、"评价分析"                                               |
| 扫码物料     | 查询某个门店最新一条物料信息 & 下载            | "下载"、"物料信息"、"最新物料"                                          |
| 应用授权     | 查询已授权 & 未授权的应用列表               | "已授权"、"未授权"、"应用列表"                                          |
| 查询商家基础激励 | 查询商家商品基础激励的总体状态（激励中数量 & 未激励数量） | "激励中数量"、"激励数量"、"基础激励"                                       |
| 查询职人定向激励 | 查询职人的定向激励数据                    | "职人定向激励"、"职人激励"、"定向激励"                                      |
| 查询门店认领   | 查询商家门店认领信息                     | "门店认领信息"、"门店资质"                                             |
| 查询合同     | 查询商家合同信息                       | "合同列表"、"查询合同"                                               |
| 查询区域     | 查询商家区域信息                       | "区域"                                                        |
| 官方账号管理   | 查询官方账号信息                       | "官号"                                                        |
| 查看商品     | 查询商品列表                         | "查看商品列表"、"查询商品"、"商品状态"                                      |
| 门店商品     | 查询门店商品列表                       | "门店商品列表"、"查询门店商品"                                           |
| 商品门店     | 查询商品门店列表                       | "商品关联门店"、"查询商品门店"                                           |


## 脚本

| 脚本                                                    | 功能              |
|-------------------------------------------------------|-----------------|
| `scripts/call_api.py --api query_brand_info_list`     | 查询商家品牌资质        |
| `scripts/call_api.py --api artisan_list`              | 查询职人列表          |
| `scripts/call_api.py --api staff_user_info`           | 查询子账号列表         |
| `scripts/call_api.py --api todo_list`                 | 查询商家数据          |
| `scripts/call_api.py --api merchant_artisan_metric`   | 查询商家职人数据        |
| `scripts/call_api.py --api merchant_realtime_metric`  | 查询商家交易实时汇总      |
| `scripts/call_api.py --api merchant_refund_metric`    | 查询商家经营退款数据      |
| `scripts/call_api.py --api artisan_auto_commission`   | 查询商家职人自动激励信息    |
| `scripts/call_api.py --api item_commission`           | 查询商家商品基础激励的总体状态 |
| `scripts/call_api.py --api artisan_direct_commission` | 查询职人的定向激励数据详情   |
| `scripts/call_api.py --api comment_analysis`          | 查询评价分析          |
| `scripts/call_api.py --api poi_qrcode`                | 获取门店的扫码物料信息     |
| `scripts/query_report.py`                             | 查询经营数据          |
| `scripts/call_api.py --api merchant_area_list`        | 查询商家区域列表        |
| `scripts/call_api.py --api merchant_contracts`        | 查询合同信息          |
| `scripts/call_api.py --api query_poi_manage_list`     | 查询门店认领信息        |
| `scripts/call_api.py --api query_official_account`    | 查询官方账号信息        |
| `product_api.py --api item_list`                      | 查看商品列表          |
| `product_api.py --api item_sku_list`                  | 查询门店维度商品列表      |
| `product_api.py --api item_poi`                       | 查询商品维度的门店列表     |




## 使用方法

```bash

# 查询已授权 & 未授权的应用列表
python3 scripts/call_api.py --api query_developer_auth_list 
#查询商家品牌资质
python3 scripts/call_api.py --api query_brand_info_list
#查询商家区域列表
python3 scripts/call_api.py --api merchanrt_area_list
#查询商家合同信息
python3 scripts/call_api.py --api merchant_contracts
#查询门店认领信息
python3 scripts/call_api.py --api query_poi_manage_list
# 查询商家职人自动激励的状态信息：
python3 scripts/call_api.py --api artisan_auto_commission
#查询商家商品基础激励的总体状态：
python3 scripts/call_api.py --api item_commission --current_page 1 --page_size 10
#查询职人的定向激励数据详情：
python3 scripts/call_api.py --api artisan_direct_commission --current_page 1 --page_size 10
# 24. 查询评价分析
python3 scripts/call_api.py --api comment_analysis --out_poi_id 门店ID --start_date 20260101 --end_date 20260320
# 查询职人列表
python3 scripts/call_api.py --api artisan_list --current_page 1 --page_size 100
# 获取商家职人的整体经营数据：
python3 scripts/call_api.py --api merchant_artisan_metric --start_date 20260101 --end_date 20260320
# 查询某个具体职人的经营数据：
python3 scripts/call_api.py --api artisan_metric --artisan_id 职人ID --start_date 20260101 --end_date 20260320
# 获取商家的待办事项列表：
python3 scripts/call_api.py --api todo_list
# 查询商家某个子账号的详细信息：
python3 scripts/call_api.py --api staff_user_info --staff_id 子账号ID
# 获取商家所有子账号的列表：
python3 scripts/call_api.py --api sub_accounts --current_page 1 --page_size 10
# 查询官方账号
python3 scripts/call_api.py --api query_official_account
# 获取商家交易的实时汇总信息：
python3 scripts/call_api.py --api merchant_realtime_metric
# 获取商家经营退款数据汇总：
python3 scripts/call_api.py --api merchant_refund_metric
# 查询经营数据
python3 scripts/query_report.py --begin-date 20260316 --end-date 20260322 --channel [1,2] --format markdown

# 查看某个门店下的所有商品：
python3 scripts/product_api.py --api item_sku_list --poi_id 门店ID --page_size 10 分页大小 --page_num 1 页码从1开始

# 查询商品关联的门店列表：
python3 scripts/product_api.py --api item_poi --item_id 商品ID --page_size 10 分页大小 --page_num 1 页码从1开始

# 查看您店铺里的所有商品（自动标注状态：✅ 已上架 | ⚠️ 已下架 | ❌ 已删除）
python3 scripts/product_api.py --api item_list --cursor 0 --size 20
```
> 💡 **小贴士**：输出会自动标注商品状态和价格（元），方便快速筛选。详细示例见 `examples/product_api_examples.md`



## 错误处理

| status | 说明               |
|--------|------------------|
| 0      | 成功               |
| 其他     | 失败，查看 message 字段 |


## 欢迎语
- 安装成功后用礼貌、简洁的语言给用户介绍一下我们的功能，仅在安装成功后总结发送一次

## 额外信息参考

1. 比如状态&枚举定义等参考：references/api-reference.md

# 许可
MIT License