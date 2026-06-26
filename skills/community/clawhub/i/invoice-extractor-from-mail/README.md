<div align="center">

# 📨 Invoice Extractor from Mail

**Intelligent Invoice Extraction Skill for Email**

Built for AP finance teams in overseas procurement and cross-border trade enterprises

`Auto-fetch email attachments` → `ADP intelligent extraction` → `One-click output to Excel / business systems`

</div>

---

## 📖 Product Overview

**Invoice Extractor from Mail** is a dedicated invoice extraction skill officially built by Laiye Technology for finance teams in traditional manufacturing enterprises. Powered by [ADP (Agentic Document Processing)](https://adp-global.laiye.com/?utm_source=github) core capabilities, it establishes an end-to-end automated document processing pipeline from email to business systems, compressing the previously tedious "find attachments → manual data entry" workflow into a single automated execution: auto-fetch attachments → ADP intelligent extraction → one-click output to Excel / business systems, significantly improving cross-border procurement invoice processing efficiency and data accuracy.

It supports integration with mainstream domestic and international email services via IMAP/OAuth secure access, automatically capturing invoice attachments from emails and batch-extracting key information from multilingual invoices worldwide (invoice number, amount, currency, etc.). If invoices are stored locally, they can also be uploaded directly for processing. The entire process requires no manual data entry, significantly improving AP invoice processing efficiency while reducing human error rates and compliance risks.

> 💡 **In one sentence**: Automatically turn supplier invoices scattered across your mailbox into a clean Excel spreadsheet.

### 😩 Before

```
Open mailbox → Search for invoice emails one by one → Download attachments → Open PDF/images
→ Manually identify invoice numbers, amounts, taxes... → Enter into Excel → Double-check repeatedly
→ 30 invoices later, your eyes are exhausted
```

### 🚀 After

```
Connect mailbox → Auto-fetch attachments → AI recognition in seconds → Structured output → Done ✅
```

### ✨ Key Advantages

| Feature | Description |
|---------|-------------|
| **Zero template configuration** | Works out of the box — no need to configure templates for different supplier invoice formats |
| **Global multilingual support** | Recognizes invoices in Chinese, English, Japanese, German, French, and more |
| **High accuracy** | Dual-engine powered by VLM + LLM, key field accuracy > 95% |
| **Batch concurrency** | Supports batch processing, up to 2 concurrent tasks for paid users |
| **Flexible output** | Exports to Excel by default, or integrates with Feishu, DingTalk, OneDrive, and other business systems |

---

## 🎯 Use Cases

| Scenario | Who you are | What you deal with every day | How this skill helps |
|----------|-------------|------------------------------|----------------------|
| **Overseas procurement reconciliation** | AP accountant at a manufacturing enterprise | 200+ overseas supplier emails per month — opening each one, downloading PDFs, manually copying invoice numbers, amounts, and currencies into Excel, frequently making errors that get sent back by management | Automatically connects to your mailbox, batch-downloads all invoice attachments, AI extracts in seconds, one-click reconciliation Excel generation |
| **Multi-currency settlement verification** | Cross-border trade settlement specialist | Suppliers from 5 countries, invoices in English, Japanese, German — all different formats, each requiring field-by-field verification with translation software | Multilingual auto-recognition, unified standardized field output — no more translating invoice by invoice |
| **Quarterly audit preparation** | Internal / external auditors | During audit periods, digging through six months of emails to find all invoices, sorting by date, verifying amounts — just finding the files takes two days | Set a time range for automatic retrieval, batch-extract key information and archive — two days of work becomes 10 minutes |
| **Employee reimbursement processing** | Administrative finance staff | Employee reimbursement invoices come from everywhere — some in emails, some photographed, some as PDFs — scattered sources are hard to manage uniformly | Email attachments + local files processed together, all reimbursement forms handled in one run |
| **ERP system data entry** | Finance IT manager | Invoice information needs to be manually entered into SAP / Kingdee / Yonyou one by one — 3 minutes per invoice, 200 invoices takes a full day | Map fields to business system field names, import directly after extraction — eliminates manual data entry |

---

## 📬 Supported Email Types

This skill uses universal protocol adaptation and is not limited to specific email providers. The following are commonly verified email services:

### IMAP Protocol Access

| Email Type | IMAP Server Address | Port | Encryption | Authentication | Notes |
|------------|---------------------|------|------------|----------------|-------|
| Gmail | `imap.gmail.com` | 993 | SSL/TLS | App Password | Requires 2-step verification and an app-specific password |
| Outlook / Hotmail | `outlook.office365.com` | 993 | SSL/TLS | Password / OAuth | Personal accounts use password; enterprise accounts recommend OAuth |
| Exchange (On-premises) | Depends on enterprise configuration | 993 / 143 | SSL/TLS / STARTTLS | Domain credentials | Requires IT admin to provide server address; some deployments use 143 + STARTTLS |
| Yahoo Mail | `imap.mail.yahoo.com` | 993 | SSL/TLS | App Password | Requires 2-step verification and an app-specific password |
| Zoho Mail | `imap.zoho.com` | 993 | SSL/TLS | App Password | Requires generating an app-specific password in Zoho security settings; custom domain users may use `imappro.zoho.com` |
| iCloud Mail | `imap.mail.me.com` | 993 | SSL/TLS | App Password | Requires two-factor authentication and an app-specific password generated from Apple ID page |
| QQ Mail | `imap.qq.com` | 993 | SSL/TLS | Authorization code | Requires enabling IMAP in settings and generating an authorization code |
| 163 Mail | `imap.163.com` | 993 | SSL/TLS | Authorization code | Requires enabling IMAP in NetEase Mail settings |
| Feishu Mail | `imap.feishu.cn` | 993 | SSL/TLS | Authorization code | Requires enabling IMAP in Feishu admin console |
| DingTalk Mail | `imap.dingtalk.com` | 993 | SSL/TLS | Authorization code | Requires enabling in DingTalk Mail settings |
| WeCom Mail | `imap.exmail.qq.com` | 993 | SSL/TLS | Client-specific password | Admin must enable IMAP functionality |

### API Protocol Access

| Platform Type | Access Method | Required Credentials | Notes |
|---------------|---------------|----------------------|-------|
| Microsoft Graph API | OAuth 2.0 | client_id + client_secret + tenant_id | For Microsoft 365 Enterprise |
| Gmail API | OAuth 2.0 | client_id + client_secret | For Google Workspace |
| Enterprise self-built mail platform | Mail Open API | app_id + app_secret | Requires API documentation from the platform |

> 💡 **Your email not listed?** No problem — just tell the skill your email type, and it will automatically guide you to provide the corresponding connection parameters.

---

## 📎 Supported Attachment Formats

| Format Type | Supported Extensions |
|-------------|----------------------|
| PDF | `.pdf` |
| Images | `.jpeg` `.jpg` `.png` `.bmp` `.tiff` |
| Word | `.doc` `.docx` |
| Excel | `.xls` `.xlsx` |

Maximum file size for all formats is **50 MB**. Files exceeding 20 MB are recommended to be processed using the ADP async interface.

---

## 🔑 Getting Your ADP API Key

ADP provides independent public cloud access URLs for domestic and overseas users. Accessing the nearest endpoint ensures the best network experience:

| Region | Login Address | API Base URL |
|--------|---------------|--------------|
| Chinese Mainland | [adp.laiye.com](https://adp.laiye.com/?utm_source=clawhub) | `https://adp.laiye.com/` |
| Outside Chinese Mainland | [adp-global.laiye.com](https://adp-global.laiye.com/?utm_source=clawhub) | `https://adp-global.laiye.com/` |

**Steps to obtain:**
1. Visit the login address above and register an ADP account (new users receive **100 free credits per month**)
2. After logging in, click on your avatar in the top-right corner to access the API Key management page
3. Copy your API Key

> On first use, the skill will automatically guide you through API Key configuration — no manual setup required.

---

## 💰 Billing

**🎁 New user benefit:** **100 free credits per month**, usable across all applications, reset at the beginning of each month.

| Processing Type | Credits Consumed | Description |
|-----------------|------------------|-------------|
| Document parsing | 0.5 credits/page | Full-text content parsing |
| Invoice/receipt extraction | 1.5 credits/page | Key field structured extraction |
| Purchase order extraction | 1.5 credits/page | Order field structured extraction |
| Custom extraction | 1 credit/page | User-defined field templates |

> When credits are insufficient, you can top up directly by logging into the ADP portal. Run `adp credit` to check your current balance at any time.

---

## 📁 Document Structure

```
invoice-extractor-from-mail/
├── SKILL.md                        # Skill definition (English, primary)
├── README.md                       # Product overview (English)
├── README_CN.md                    # Product overview (Chinese)
├── refers/
│   └── adp-invoice-fields.md      # ADP field schema reference
└── license.md                      # License
```

| File | Purpose |
|------|---------|
| `SKILL.md` | Core skill logic: workflow, configuration, error handling |
| `refers/adp-invoice-fields.md` | ADP output field definitions and mapping rules |
| `README.md` / `README_CN.md` | User-facing product documentation |

---

## 📚 Resources

- **ADP Portal**: [Chinese Mainland](https://adp.laiye.com/?utm_source=github) | [Outside Chinese Mainland](https://adp-global.laiye.com/?utm_source=github)
- **CLI Documentation**: [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation**: [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **User Guide**: [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Feedback**: [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues) | global_product@laiye.com
- **Official Website**: [Laiye Technology](https://laiye.com)

---

<div align="center">

[⬆ Back to top](#-invoice-extractor-from-mail)

**Building the future of agentic AI with ❤️**

Copyright © 2026 [Laiye Technology (Beijing) Co., Ltd.] All rights reserved.

</div>
