<div align="center">

# 📨 Invoice Extractor from Mail

**邮件发票智能抽取技能**

专为海外采购、跨境贸易企业的 AP 财务团队打造

`自动获取邮件附件` → `ADP 智能抽取` → `一键输出至 Excel / 业务系统`

</div>

---

## 📖 产品介绍

**Invoice Extractor from Mail** 是来也科技官方打造、面向传统制造业财务团队的专属发票抽取技能。依托来也 [ADP（Agentic Document Processing）](https://adp-global.laiye.com/?utm_source=github) 核心能力，打通从邮件到业务系统的端到端自动化文档处理链路，将原本繁琐的 "查找附件 → 手工录入" 压缩为一步自动化执行：自动获取附件 → ADP 智能抽取 → 一键输出至 Excel / 业务系统，大幅提升跨境采购发票处理效率与数据准确性。

支持对接国内外主流邮箱，通过 IMAP/OAuth 安全接入，可自动抓取邮件中的发票附件，批量提取全球多语种发票的关键信息（发票号、金额、币种等）。如果发票存储在本地，也可直接上传处理。全程无需人工手动录入，大幅提升 AP 财务票据处理效率，降低人工出错率与合规风险。

> 💡 **一句话理解**：把你邮箱里散落的供应商发票，自动变成一张干净的 Excel 表。

### 😩 没有它之前

```
打开邮箱 → 逐封查找发票邮件 → 下载附件 → 打开 PDF/图片
→ 肉眼识别发票号、金额、税额… → 手动录入 Excel → 反复核对
→ 一天下来处理了 30 张，眼睛已花
```

### 🚀 有了它之后

```
连接邮箱 → 自动抓取附件 → AI 秒级识别 → 结构化输出 → 完成 ✅
```

### ✨ 核心优势

| 特性 | 说明 |
|------|------|
| **零模板配置** | 开箱即用，无需为不同供应商的发票格式分别配置模板 |
| **全球多语种** | 中、英、日、德、法等多语种发票识别 |
| **高准确率** | VLM + LLM 双引擎驱动，关键字段准确率 > 95% |
| **批量并发** | 支持批量处理，付费用户最高 2 并发 |
| **灵活输出** | 默认导出 Excel，也可对接飞书、钉钉、OneDrive 等业务系统 |

---

## 🎯 适用场景

| 场景 | 你是谁 | 你每天在经历什么 | 这个技能怎么帮你 |
|------|--------|-----------------|-----------------|
| **海外采购对账** | 制造企业 AP 会计 | 每月 200+ 封海外供应商邮件，逐封打开、下载 PDF，手动抄写发票号、金额、币种到 Excel，经常抄错被领导退回 | 自动连接你的邮箱，批量下载所有发票附件，AI 秒级抽取，一键生成对账 Excel |
| **多币种结算核对** | 跨境贸易结算专员 | 供应商来自 5 个国家，发票有英文、日文、德文，格式各不相同，每张都要对着翻译软件逐字段核对 | 多语种自动识别，统一输出标准化字段，不用再逐张翻译 |
| **季度审计备查** | 内审 / 外审人员 | 审计期要从半年的邮件中翻出所有发票，按时间排列、核对金额，光找文件就花了两天 | 设定时间范围自动抓取，批量抽取关键信息并归档，两天的活变成 10 分钟 |
| **员工报销处理** | 行政财务 | 员工的报销发票有的在邮件里、有的拍照发过来、有的是 PDF，来源分散难统一管理 | 邮件附件 + 本地文件统一处理，一次跑完全部报销单 |
| **ERP 系统录入** | 财务信息化负责人 | 发票信息需要手动逐条录入 SAP / 金蝶 / 用友，录一张要 3 分钟，200 张就是一整天 | 字段映射到业务系统字段名，抽取后直接导入，省掉手工录入环节 |

---

## 📬 支持的邮箱类型

本技能采用通用协议适配，不限定具体邮箱品牌。以下为已验证的常见邮箱：

### IMAP 协议接入

| 邮箱类型 | IMAP 服务器地址 | 端口 | 加密 | 认证方式 | 备注 |
|----------|----------------|------|------|---------|------|
| Gmail | `imap.gmail.com` | 993 | SSL/TLS | App Password | 需开启两步验证并生成应用专用密码 |
| Outlook / Hotmail | `outlook.office365.com` | 993 | SSL/TLS | 密码 / OAuth | 个人账户使用密码，企业账户建议 OAuth |
| Exchange (本地部署) | 视企业配置而定 | 993 / 143 | SSL/TLS / STARTTLS | 域账号密码 | 需 IT 管理员提供服务器地址，部分部署使用 143 + STARTTLS |
| Yahoo Mail | `imap.mail.yahoo.com` | 993 | SSL/TLS | App Password | 需开启两步验证并生成应用专用密码 |
| Zoho Mail | `imap.zoho.com` | 993 | SSL/TLS | App Password | 需在 Zoho 安全设置中生成应用专用密码；自定义域名用户服务器可能为 `imappro.zoho.com` |
| iCloud Mail | `imap.mail.me.com` | 993 | SSL/TLS | App Password | 需开启双重认证并在 Apple ID 页面生成应用专用密码 |
| QQ 邮箱 | `imap.qq.com` | 993 | SSL/TLS | 授权码 | 需在设置中开启 IMAP 并生成授权码 |
| 163 邮箱 | `imap.163.com` | 993 | SSL/TLS | 授权码 | 需在网易邮箱设置中开启 IMAP |
| 飞书邮箱 | `imap.feishu.cn` | 993 | SSL/TLS | 授权码 | 需在飞书管理后台开启 IMAP |
| 钉钉邮箱 | `imap.dingtalk.com` | 993 | SSL/TLS | 授权码 | 需在钉钉邮箱设置中开启 |
| 企业微信邮箱 | `imap.exmail.qq.com` | 993 | SSL/TLS | 客户端专用密码 | 管理员需开启 IMAP 功能 |


### API 协议接入

| 平台类型 | 接入方式 | 所需凭证 | 备注 |
|----------|---------|---------|------|
| Microsoft Graph API | OAuth 2.0 | client_id + client_secret + tenant_id | 适用于 Microsoft 365 企业版 |
| Gmail API | OAuth 2.0 | client_id + client_secret | 适用于 Google Workspace |
| 企业自建邮件平台 | Mail Open API | app_id + app_secret | 需平台提供 API 文档 |

> 💡 **你的邮箱不在列表中？** 没关系——只需告诉技能你的邮箱类型，它会自动引导你提供对应的连接参数。

---

## 📎 支持的附件格式

| 格式类型 | 支持的扩展名 |
|---------|-------------|
| PDF | `.pdf` |
| 图片 | `.jpeg` `.jpg` `.png` `.bmp` `.tiff` |
| Word | `.doc` `.docx` |
| Excel | `.xls` `.xlsx` |

所有格式单文件最大支持 **50 MB**。超过 20 MB 的文件建议使用 ADP 异步接口处理。

---

## 🔑 ADP API Key 获取

ADP 为国内外用户提供了独立的公有云接入地址，就近访问可保障最佳网络体验：

| 区域 | 登录地址 | API Base URL |
|------|---------|--------------|
| 中国大陆 | [adp.laiye.com](https://adp.laiye.com/?utm_source=clawhub) | `https://adp.laiye.com/` |
| 非中国大陆 | [adp-global.laiye.com](https://adp-global.laiye.com/?utm_source=clawhub) | `https://adp-global.laiye.com/` |

**获取步骤：**
1. 访问上述登录地址，注册 ADP 账户（新用户每月获得 **100 免费积分**）
2. 登录后，点击右上角个人头像，进入 API Key 管理页面
3. 复制你的 API Key

> 首次使用时，技能会自动引导你完成 API Key 配置，无需手动操作。

---

## 💰 计费规则

**🎁 新用户福利：** 每月获得 **100 免费积分**，不限使用应用，每月初重置。

| 处理类型 | 消耗积分 | 说明 |
|---------|---------|------|
| 文档解析 | 0.5 积分/页 | 全文内容解析 |
| 发票/收据抽取 | 1.5 积分/页 | 关键字段结构化提取 |
| 采购订单抽取 | 1.5 积分/页 | 订单字段结构化提取 |
| 自定义抽取 | 1 积分/页 | 用户自定义字段模板 |

> 积分不足时可直接登录 ADP 门户进行充值。运行 `adp credit` 可随时查看当前余额。

---

## 📁 文档结构

```
invoice-extractor-from-mail/
├── SKILL.md                        # Skill 定义（英文，主文件）
├── README.md                       # 产品说明（英文）
├── README_CN.md                    # 产品说明（中文）
├── refers/
│   └── adp-invoice-fields.md      # ADP 字段 schema 参考
└── license.md                      # 许可证
```

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 核心技能逻辑：工作流、配置、错误处理 |
| `refers/adp-invoice-fields.md` | ADP 输出字段定义与映射规则 |
| `README.md` / `README_CN.md` | 面向用户的产品文档 |

---

## 📚 相关资料

- **ADP 产品入口**：[中国大陆](https://adp.laiye.com/?utm_source=github) | [非中国大陆](https://adp-global.laiye.com/?utm_source=github)
- **CLI 文档**：[ADP CLI 使用指南](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API 文档**：[OpenAPI 使用指南](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **产品手册**：[公有云操作手册](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **问题反馈**：[GitHub Issues](https://github.com/laiye-ai/adp-cli/issues) | global_product@laiye.com
- **官方网站**：[来也科技](https://laiye.com)

---

<div align="center">

[⬆ 返回顶部](#-invoice-extractor-from-mail)

**用 ❤️ 构建智能体 AI 的未来**

版权所有 © 2026 [来也科技（北京）有限公司] 保留所有权利。

</div>
