---
name: 查询公司|供应商|POP商家|对接商毛利及经营排名
description: 查询公司、供应商、POP商家及对接商的基础信息、董监高，及订单量级、收入、成本、毛利、利润、毛保、返利、净毛利、损益及排名等经营财务数据；注意：该SOP侧重查询毛利/利润情况，非销售数据。
---

# 查询公司|供应商|POP商家|对接商毛利及经营排名

## 适用场景
查询公司、供应商、POP商家及对接商的基础信息、董监高，及订单量级、收入、成本、毛利、利润、毛保、返利、净毛利、损益及排名等经营财务数据；注意：该SOP侧重查询毛利/利润情况，非销售数据。

## 输入参数
- com_name（公司名称）

## 执行流程
> Claude 请严格按以下步骤依次查询数据表并分析，注意每一步的依赖关系、输入与输出字段。

```
step1: 
从表 app_lb_company_bus_pond_base_view 中根据com_name（公司名称）查询该公司的工商注
step2:
从表 tmp_paxy_company_p_key_rel_s_det 中根据company_name（公司名称）查询该公司的董监
step3:
从表 app_lb_company_jd_pop_shop 中根据vender_name（POP企业名称）字段查询POP商家信息
step4:
从表 app_lb_company_jd_self_supp 中根据vendor_name（供应商名称）字段查询供应商信息
step5:
从表 app_logicbatch_order_adv_rebate_result_da 中根据supp_corp_name（供应商名称）查询供应商的订单量级、收入总金额、成本总金额、毛利总金额、返利总金额、净毛利、净毛利率等信息
step6:
从表 cdm_pop_m12_order_sku_profit_loss_det 中根据pop_vender_name（POP商家名称）查询POP商家的优惠后金额、订单量级、损益金额等信息
```

---
_来源思维链ID: 2029845474681409723 ｜ owner: 张兴世（zhangxingshi.2） ｜ 创建时间: 2026-03-30 10:39:21 ｜ 最近更新: lijianliang.21 2026-07-08 22:45:46_
