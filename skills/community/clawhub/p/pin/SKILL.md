---
name: 查询京东账号（京东pin）的手机号解换绑
description: 查询京东账号（京东pin）绑定手机号及关联员工公司信息流程；入参为：pin（京东账号（京东pin））
---

# 查询京东账号（京东pin）的手机号解换绑

## 适用场景
查询京东账号（京东pin）绑定手机号及关联员工公司信息流程；入参为：pin（京东账号（京东pin））



## 执行流程
> Claude 请严格按以下步骤依次查询数据表并分析，注意每一步的依赖关系、输入与输出字段。

```
step1：【查询账号的手机号解换绑记录】从表：app_lb_acct_bind_mobile_det_t中，根据账号（pin，不区分大小写）查询账号历史绑定手机号的记录
依赖：无
输入：账号（pin，不区分大小写）
输出：
手机号-可逆加密 mobile_phone
手机号-不可逆加密 mobile_phone_sha
操作类型 oper_type
更新时间 oper_time

step2：【查询账号历史绑定手机号的基本信息】从表：app_lb_mob_pool_sum中，根据手机号（mob）查询手机号基础信息
依赖：step1.mobile_phone_sha（将step1中的mobile_phone_sha作为step2中的mob）
输入：手机号（mob，不可逆加密）
输出：按需选取字段

step3-1：【查看账号绑定手机号关联的员工】从表：app_icc_staff_info中，限制DP='mobile'，根据手机号-不可逆加密（MOBILE_SHA）查询对应的员工erp
依赖：step1.mobile_phone_sha（将step1中的mobile_phone_sha作为step3-1中的MOBILE_SHA）
输入：手机号（mobile_sha，不可逆加密）
输出：员工erp（ERP）

step3-2：【查看账号绑定手机号关联员工的基本信息】从表：cdm_m01_org_base_info_da中，限制dt = sysdate(-2) ，根据员工erp（user_name）查询对应的员工基本信息
依赖：step3-2.ERP（将step3-1中的ERP作为step3-2中的user_name）
输入：员工erp（user_name）
输出：按需选择字段

step4-1：【查看账号绑定手机号关联的公司】从表：app_lb_mob_rela_vender_sum中，根据手机号（mobile）查询手机号关联的公司
依赖：step1.mobile_phone_sha（将step1中的mobile_phone_sha作为step4-1中的mobile）
输入：手机号（mobile，不可逆加密）
输出：公司名称（name）

step4-2：【查询账号绑定手机号关联公司的基础信息】从表：app_lb_company_pond_result中，根据公司名称（com_name）查询该账号绑定手机号关联公司的基础信息
依赖：step4-1.src_val（将step4-1中的src_val作为step4-2中的com_name）
输入：公司名称（com_name）
输出：s_type（合作类型）、is_coop（是否合作）、self_supp（供应商简码）

step4-3：【如果关联公司为自营供应商则查询该自营供应商的采销负责人】从表：LB04_0302 中，根据供应商简码（vendor_code）
依赖：step4-2.self_supp（将step4-2中的self_supp作为step4-3中的vendor_code）
供应商简码 vendor_code
采销erp purchaser_code
采销员姓名 purchaser_name
采销类型 purchaser_type
```

---
_来源思维链ID: 2029845474681409667 ｜ owner: 陈思宇（chensiyu106） ｜ 创建时间: 2026-03-16 14:12:06 ｜ 最近更新: yanwenxuan.5 2026-06-09 15:04:35_
