<div align="center">
<a id="agentic_doc_parse_and_extract"></a>

# 📄 Laiye Agentic Document Processing CLI (agentic_doc_parse_and_extract)

agentic_doc_parse_and_extract is the official command-line tool released by Laiye Technology's ADP (Agentic Document Processing) product, enabling both humans and AI Agents to invoke ADP capabilities in the terminal for document parsing and extraction.

[English](README.md) | [Simplified Chinese](README-CN.md)

</div>

## 🚀 About Laiye ADP

ADP is Laiye's **intelligent agent document processing product (Agentic Document Processing, referred to as ADP)** , based on the general understanding ability of large models, without relying on rules and annotations, with the general understanding ability of multi-language, MultiModal Machine Learning, and multi-scene; autonomous planning and execution of intelligent agents, able to understand task goals, autonomous planning steps, invoke tools, and complete complex tasks; end-to-end business automation, from document input to business decision-making to human-machine collaboration, forming a complete closed loop.

**agentic-doc-parse-and-extract** is the official open-source CLI tool of ADP, supporting both manual terminal invocation and automatic invocation via AI Skill. With a single command, it can accomplish: structured document parsing + intelligent extraction of key fields, covering all scenarios including invoices, orders, certificates, bills, and general documents, outputting standard JSON, and seamlessly integrating with automation and AI workflows.

---

### 💡 Core Features

agentic-doc-parse-and-extract focuses on intelligent processing of the entire document workflow, taking into account both manual terminal calls and automatic calls by AI Agents. Its core functions cover all scenarios of parsing, extraction, and batch processing, requiring no complex configuration, and operations can be completed with a single command:

| Function Name | Function Description | Optimal Scenario |
|---------|------------------|----------|
| **Document Parsing** | Automatically recognize multi-format documents such as PDFs and images, convert messy unstructured content (e.g., scanned documents, handwritten text, complex layout documents) into standardized Structured Data, while preserving the original document hierarchy and key relationships | Convert unstructured documents into Structured Data for LLM reading and subsequent extraction |
| **Out Of The Box Document Extraction** | Based on the native AI capabilities of the ADP large model, it comes with built-in standardized extraction models for invoices, receipts, orders, commonly used certificates in China, etc. No need to configure rules or manual annotation, one-click extraction of key fields from various types of general documentation, outputting standard JSON | Account Payable automation, expense management, procurement automation, quick entry of card and certificate information into the system |
| **Custom Document Extraction** | Supports independent creation, editing, and management of personalized extraction applications, allowing configuration of exclusive extraction fields and recognition logic for enterprise-specific documentation and industry-customized forms | Private extraction requirements for enterprise-specific documentation, industry-customized forms, and non-standardized documents |
| **Task Query** | Supports asynchronous task submission and status query, enabling quick viewing of task execution progress, success/failure status, and final task processing results | Batch task processing, asynchronous document processing, problem troubleshooting, and processing record tracing |
| **Application Management** | Provides comprehensive application management capabilities, allowing users to view all available extraction applications (system-built + custom), query application details, and manage application tags | Multi-scenario business switching, full lifecycle management of applications, and custom application management |

---

### 🎯 Target Audience

- **AI Agent Developers:** Quickly integrate document parsing and extraction capabilities through standard Skills to empower intelligent agents in automated work processes
- **Enterprise R&D and Architecture Team:** Unified access to CLI tools, enabling low-cost implementation of structured and automated processing for all types of documentation
- **Finance & Administrative Operations Team:** Batch parsing of invoices, receipts, and reimbursement forms, reducing manual entry and verification costs
- **Business System Integrator:** Relying on standardized JSON output, seamlessly connecting with upstream and downstream systems such as ERP, RPA, and Central Product Platform
- **Internal Platform Builder:** Supporting local deployment and environment adaptation to meet the requirements of enterprise intranet security and permission management

## 📁 Project File Structure and File Description

```
agentic-doc-parse-and-extract/
├── skill.md                  # Skill configuration and invocation instructions
├── README.md                 # Introduction to Laiye ADP product and instructions for CLI download and invocation
├── references/               # Parameter enumeration, error codes, and JSON return instructions
    ├── examples.md           # Sample code for invocation and return with parameter explanations
    ├── commands.md           # List of all commands
    ├── response-schema.md    # Return parameter description
    ├── error-handling.md     # Mistakes and what to do about them
├── License                   # License authorization
```

## 📋 API Key
### Get API Key
1. Visit [ADP China Region URL](https://adp.laiye.com/?utm_source=clawhub), [ADP Global Region URL](https://adp-global.laiye.com/?utm_source=clawhub)
2. Register a new account (new users get 100 free credits per month)

## 💻 Environment and Installation
### Supported Platforms and Versions
| Platform | Minimum Requirements |
|---------|------------------|
| **Windows** | Windows 10 or later |
| **Linux** | Ubuntu 18.04+, CentOS 7+, or mainstream Linux distributions |
| **macOS** | macOS 10.14 (Mojave) or later |
---

### Install

 ```bash
  # Method 1: npm (recommended, works on all platforms, China-friendly with npmmirror)
  npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli --registry=https://registry.npmmirror.com/ || npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli
  export PATH="$(npm prefix -g)/bin:$PATH"

  # Method 2: Shell script (Linux / macOS, if npm is not available)
  curl -fsSL https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.sh | bash

  # Method 3: PowerShell script (Windows, if npm is not available)
  Invoke-WebRequest -Uri "https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.ps1" -OutFile "$env:TEMP\adp-init.ps1"; & "$env:TEMP\adp-init.ps1"
  ```

---

## ✨ Product & Technical Highlights

### 📦 Out Of The Box Product

| Product | Extracted Content | Optimal Scenario |
|---------|------------------|----------|
| **Document Parsing** | Extract elements such as text, tables, images, seals, etc. from the document | Convert the document into structured data for LLM to read |
| **Invoice/Receipt Extraction** | Invoice number, date, supplier, item details, total amount, taxes | Accounts payable automation, expense management |
| **Order Extraction** | Purchase Order Number, Commodity, Quantity, Price, Delivery Information | Procurement Automation, E-commerce Integration |
| **Card Extraction** | 11 types of commonly used cards and certificates such as ID card, bank card, driver's license, business license, etc. | Quick entry of card and certificate information into the system |

### 🛠️ Technical Capabilities

- **10+ File Formats**: Covers mainstream image and work document formats (.jpg,.jpeg,.png,.bmp,.tiff,.tif,.pdf,.doc,.docx,.xls,.xlsx)
- **VLM + LLM Dual Engines**: Visual understanding + semantic extraction to achieve maximum accuracy
- **Synchronous and Asynchronous Modes**: All functions are open to external synchronous and asynchronous APIs
- **File Restrictions:** Maximum file size: 50MB
- **Batch Processing:** Supports folder recursion processing
### 🌟 Product Advantages
- Relying on the core capabilities of Laiye Technology's ADP large model and combining the lightweight features of CLI tools, we have created an efficient, flexible, and easily integrated document processing solution with prominent core advantages:
- Zero-threshold entry: No professional technical background is required, no rule configuration or data annotation is needed, with a built-in standardized extraction model that is out of the box, and a single command can complete document parsing and extraction.
- Full-scenario adaptation: Covers common scenarios such as invoices, receipts, orders, certificates, etc., while supporting custom extensions to adapt to enterprise-specific documentation and industry-specific forms, taking into account both general and personalized needs.
- Efficient integration and adaptation: Supports native calls of AI Agent Skill and manual calls from terminals, outputs in standard JSON format, seamlessly connects with upstream and downstream systems such as RPA, ERP, and Central Product Platform, reducing integration costs.
- Multi-terminal compatibility: Supports all platforms including Windows, macOS, and Linux, requires no additional installation of dependencies, can be globally called after configuring environment variables, and adapts to local deployment and multi-scenario work requirements.
- High Precision and Stability: Optimized based on the ADP large model, it has high recognition accuracy for unstructured documents (scanned documents, handwritten text, complex layouts), supports asynchronous task management, and ensures the stable operation of business processes.

<a id="credit"></a>
### 💰 Billing

- **New User Benefits:** Receive 100 free credits per month, with no restrictions on application usage
- **Asset Consumption Rules:**
    | Processing Stage | Cost |
    |-----------------|------|
    | Document Parsing | 0.5 points/page |
    | Purchase Order Extraction | 1.5 points/page |
    | Invoice/Receipt Extraction | 1.5 points/page |
    | Custom Extraction | 1 point/page |

- **Asset Recharge:**  You can directly log in to the ADP Portal to recharge assets. We provide independent Public Cloud access addresses for domestic and international users, which need to be configured separately by region. Accessing from a nearby location can better ensure high-speed and stable invocation across the network.
  - Users in Chinese Mainland [Log in](https://adp.laiye.com/?utm_source=clawhub)
  - Users outside Chinese Mainland [Log in](https://adp-global.laiye.com/?utm_source=clawhub)

 If you encounter any issues with payment, please contact the support email: 📧 global_product@laiye.com

## 📜 License

We adopt a combined model of open-source tools + paid services: the CLI tool is completely free and open-source, making it easy for everyone to quickly integrate; while the core ADP intelligent parsing capability is a Public Cloud commercial service, billed based on actual usage, aiming to provide users with a highly accurate and stable document processing experience.

- **CLI Tool**: Open source under the MIT License, freely available for use, modification, and distribution
- **ADP Service**: AI document processing service based on Public Cloud, billed by usage, [Billing Rules](#credit)

### 💰 Free Quota
New users can receive **100 free credits** per month after registration, allowing them to experience full functionality

## 📞 Support and Contact
- **CLI Documentation**: [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation**: [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd?from=from_copylink)
- **User Guide**: [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Problem Feedback**: [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues) | global_product@laiye.com
- **Official Website**: [Laiye Technology](https://laiye.com/en/)

---

<div align="center">
[⬆ Back to Top](#agentic_doc_parse_and_extract)

**Build the Future of Agentic AI with ❤️**
Copyright © 2026 [Laiye Technology (Beijing) Co., Ltd.] All rights reserved.

</div>