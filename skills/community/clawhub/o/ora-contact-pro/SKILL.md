---
name: Ora决策人开发专家
description: Ora外贸获客矩阵精准触达引擎。通过企业名称、企业网址域名或企业领英号，查询企业基本信息及决策人列表，精准获取老板、采购等关键决策人的邮箱与电话联系方式。作为一款AI外贸客户开发软件，支持海外决策人查询、领英客户开发与精准联系人开发，内置邮箱搜索工具与域名搜索能力，可挖掘已有联系人信息。适用于邮箱挖掘、邮箱搜索神器等外贸获客场景。当用户需要查找企业决策人联系方式、使用邮箱搜索工具获取老板/采购信息或使用AI外贸客户开发软件进行精准开发时使用此技能。
argument-hint: <name|domain|linkedin> <企业名称/域名/LinkedIn号>
---

# Topeasy 企业详情搜索技能

## 使用方式

用户输入：

- `/ora-contact-pro name <企业名称>`
- `/ora-contact-pro domain <企业域名>`
- `/ora-contact-pro linkedin <LinkedIn企业号>`

示例：

- `/ora-contact-pro name Microsoft`
- `/ora-contact-pro domain microsoft.com`
- `/ora-contact-pro linkedin microsoft`

如果用户给出完整 LinkedIn 公司链接，例如 `https://www.linkedin.com/company/microsoft/`，按 `linkedin` 类型处理。

## 规则

- 每次只搜索一个企业。
- 必须调用下面对应的脚本查询，不要自己拼接接口请求。
- 不要修改或重写脚本。
- 如果用户没有明确搜索类型，根据输入判断：
  - 像 `example.com` 或完整官网链接的内容，调用域名脚本。
  - 包含 `linkedin.com/company/` 的内容，调用 LinkedIn 脚本。
  - 其他内容，调用企业名称脚本。

## 脚本选择

| 用户要查什么 | 调用脚本 |
| --- | --- |
| 企业名称 | `node ./scripts/search_by_company_name.js "<企业名称>"` |
| 企业域名 | `node ./scripts/search_by_domain.js "<企业域名>"` |
| LinkedIn 企业号 | `node ./scripts/search_by_linkedin.js "<LinkedIn企业号或公司链接>"` |

## 执行步骤（严格按顺序）

### 步骤 1：判断搜索类型

从用户输入中判断要按企业名称、企业域名还是 LinkedIn 企业号查询。

### 步骤 2：执行对应脚本

Bash 工具参数：

- `command`: 使用“脚本选择”表中的对应命令
- `timeout`: `600000`
- `run_in_background`: `false`

脚本会自动读取 `OraAgent.key`，请求对应接口，并输出原始数据文件路径和文件名标识。

### 步骤 3：读取原始数据

读取脚本输出的 JSON 文件，按企业详情、联系方式、社媒、职员信息几个部分自然整理给用户。

### 步骤 4：中文企业名无结果时重查

如果按企业名称搜索时，用户输入的是中文企业名，且脚本返回 `data` 为空或没有有效企业详情，由 AI 自行将企业名称翻译成英文，再调用一次企业名称脚本重新搜索。

示例：

```bash
node ./scripts/search_by_company_name.js "<翻译后的英文企业名称>"
```

只允许在“中文企业名称搜索无结果”时进行这一次英文重查；域名搜索和 LinkedIn 企业号搜索不要翻译。

## 展示要求

- 优先展示企业名称、官网/域名、行业、国家/城市、员工数量、成立时间、简介。
- 企业名称搜索返回的是聚合数据，其中 `LinkedinCompanyDetail` 是主要企业详情，其他字段是补充信息；补充信息不能直接过滤掉。
- 域名和 LinkedIn 企业号搜索也可能返回聚合数据，不能只看公司详情字段，要检查完整 `data` 对象。
- 如果返回结果中有邮箱、电话、传真、地址、社媒链接，必须单独展示。
- 邮箱很多时，展示前 5 个，并说明还有多少个未展开；如果只有 1-5 个则全部展示。
- 社媒字段有值时必须展示对应平台和值，包括 `Linkedin`、`Facebook`、`Twitter`、`Youtube`、`Instagram`、`Pinterest`、`TikTok` 等。
- 电话、传真、地址字段有值时也要展示；多个值用简洁列表或逗号分隔。
- 如果返回结果中有 `ContactInfo`、`Contacts`、`ConnectionInfo`、`LinkedinConnections` 或类似职员/联系人数组，必须单独展示“职员信息”部分。
- 职员信息要优先展示姓名、职位/岗位、公司、邮箱、手机、电话、地区、国家、LinkedIn 标识或个人主页、照片链接、个人社媒。
- 职员很多时，展示前 10 个较完整的职员，并说明总数或剩余数量；如果只有 1-10 个则全部展示。
- 对职员数据做简短分析，例如岗位分布、是否包含决策层/销售/采购/技术等关键角色、可用邮箱数量、可用电话数量、地区集中情况。
- 如果只有邮箱但没有姓名，也要作为“未匹配姓名的联系人邮箱”展示，不要丢弃。
- 如果 `data` 为空，明确说明通过该方式没有查询到企业详情，不要编造信息。

## 错误处理

- 如果脚本输出 `STATUS:401`，说明 Skill Key 缺失、无效或未授权。
- 如果脚本输出 `STATUS:402`，说明免费额度已用尽。必须提示用户前往 `https://www.oraskl.com/platform` 充值或使用有效 Key。
- 如果脚本提示接口错误，向用户说明接口状态码和错误信息。
- 如果读取不到结果文件，检查脚本输出的原始数据文件路径是否正确。
