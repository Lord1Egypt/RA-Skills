# Invoice Compliance Checker
检查发票是否符合监管要求和内部政策，防止合规风险。

## What it does
- 按区域（EU/US/APAC）检查发票模板是否满足电子发票合规要求
- 审计供应商发票是否符合采购订单政策（PO 匹配、审批、定价）
- 搭建发票提交前的自检系统与审批流程
- 提供中国电子发票真伪查验实操指南

## Example scenarios
**1. 欧盟电子发票合规检查**
> 👤 Check if our invoice template meets EU e-invoicing requirements for B2B transactions.
> 🤖 Compliance checklist mapping each field to EU Directive 2014/55/EU requirements — mandatory fields (VAT ID, PO reference, unit price), format (UBL 2.1), digital signature, and archiving rules — with gap identification and remediation steps.

**2. 收到一张发票不知道是真的假的**
> 👤 我在闲鱼上找人代购了一台 iPad，对方给我开了一张电子发票，我怀疑是假的，怎么查验？
> 🤖 发票真伪查验流程：1）登录国家税务总局全国增值税发票查验平台输入发票代码、号码、日期、校验码；2）核对开票方名称和实际销售方是否一致；3）检查电子发票印章（税务机关监制章+开票方电子签章）；4）不合规发票可拨打 12366 举报。

**3. 供应商发票合规审计**
> 👤 Audit these 20 vendor invoices for compliance with our purchase order policy.
> 🤖 Exception report flagging PO mismatches, missing approvals, pricing deviations >5%, duplicate invoice detection, and non-compliant tax treatments — with severity ratings and resolution instructions.
