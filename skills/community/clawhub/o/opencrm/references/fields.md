# 字段参考

## 客户字段（add）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| customer_name | string | ✅ | 公司全称 |
| short_name | string | | 简称 |
| industry | string | | 行业名称（如：科技型、制造、贸易） |
| industry_id | int | | 行业 ID（与名称二选一） |
| level_name | string | | 客户等级名称（如：A级-战略、B级-重要） |
| level_id | int | | 客户等级 ID |
| source | string | | 来源名称（如：展会、网络搜索、陌拜、客户介绍） |
| source_id | int | | 来源 ID |
| customer_group | string | | 分组名称（如：塑料油墨、UV油墨、金属油墨） |
| group_id | int | | 分组 ID |
| legal_representative | string | | 法定代表人 |
| registered_capital | string | | 注册资本（如：200万元） |
| paid_in_capital | string | | 实缴资本 |
| established_date | string | | 成立日期（格式 YYYY-MM-DD） |
| registration_status | string | | 登记状态（存续/在业/注销/吊销/迁出/停业/清算） |
| tax_number | string | | 统一社会信用代码（18位） |
| business_registration_no | string | | 工商注册号 |
| organization_code | string | | 组织机构代码 |
| business_term | string | | 营业期限 |
| taxpayer_qualification | string | | 纳税人资质（一般纳税人/小规模纳税人） |
| insured_count | string | | 参保人数 |
| approval_date | string | | 核准日期（YYYY-MM-DD） |
| registration_authority | string | | 登记机关 |
| national_industry | string | | 国标行业 |
| registered_address | string | | 注册地址 |
| business_scope | string | | 经营范围 |
| introduction | string | | 公司简介 |
| address | string | | 详细地址 |
| province | string | | 省 |
| city | string | | 市 |
| area | string | | 区 |
| telephone | string | | 公司电话 |
| email | string | | 公司邮箱 |
| website | string | | 网址 |
| credit_limit | string | | 信用额度（元） |
| payment_terms | string | | 结算方式（如：月结30天、款到发货） |
| remark | string | | 备注 |
| extra | string | | 自定义字段（JSON 字符串，如 `{"supervisor":"张三"}`） |

## 客户字段（edit）

PATCH 语义，`id` 必填。用于修改工商信息和联系方式。

| 字段 | 类型 | 说明 |
|------|------|------|
| tax_number | string | 统一社会信用代码（18位） |
| business_registration_no | string | 工商注册号 |
| organization_code | string | 组织机构代码 |
| legal_representative | string | 法定代表人 |
| registered_capital | string | 注册资本 |
| paid_in_capital | string | 实缴资本 |
| established_date | string | 成立日期（YYYY-MM-DD） |
| registration_status | string | 登记状态 |
| taxpayer_qualification | string | 纳税人资质 |
| insured_count | string | 参保人数 |
| business_term | string | 营业期限 |
| approval_date | string | 核准日期（YYYY-MM-DD） |
| registration_authority | string | 登记机关 |
| national_industry | string | 国标行业 |
| registered_address | string | 注册地址 |
| business_scope | string | 经营范围 |
| introduction | string | 公司简介 |
| telephone | string | 公司电话 |
| email | string | 公司邮箱 |
| website | string | 网址 |
| province | string | 省 |
| city | string | 市 |
| area | string | 区 |
| address | string | 详细地址 |
| short_name | string | 简称 |
| remark | string | 备注（覆盖原有内容） |

## 分类标签（独立端点）

分组/等级/行业/来源不放在 edit 中，用专用端点：

| 端点 | 参数 |
|------|------|
| `POST /opencrm.customer/setGroup` | `id`, `customer_group` |
| `POST /opencrm.customer/setLevel` | `id`, `level_name` |
| `POST /opencrm.customer/setIndustry` | `id`, `industry` |
| `POST /opencrm.customer/setSource` | `id`, `source` |

传名称即可，系统自动匹配字典 ID。如名称不在字典中则自动创建。

## 线索字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| lead_name | string | ✅ | 线索名称 |
| company_name | string | | 公司名称 |
| contact_person | string | | 联系人 |
| contact_position | string | | 职位 |
| contact_phone | string | | 手机 |
| source | string | | 来源 |
| remark | string | | 备注 |

## 字典字段说明

`industry`、`level_name`、`source`、`customer_group` 四个字段用于分类标记。传入的名称如果在系统字典中不存在，API 会自动创建新字典项。建议优先传 `_name` 字段，让系统自动匹配 ID。

示例：

```json
{
  "customer_name": "XX科技有限公司",
  "industry": "科技型",
  "level_name": "A级-战略",
  "source": "展会",
  "customer_group": "塑料油墨"
}
```
