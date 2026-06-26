---
name: invoice-gen
description: Generate professional PDF invoices from simple text commands. Supports multiple currencies, tax calculation, CJK text, and customizable templates. No external service needed.
author: zacjiang
version: 1.0.0
tags: invoice, receipt, pdf, billing, business, freelance, accounting, CJK
---

# Invoice Generator

Generate professional PDF invoices from natural language or structured data. Works offline, no external service needed.

## Quick Start

Tell your OpenClaw agent:
```
Generate an invoice for:
- Client: Acme Corp, 123 Main St, New York
- Items: Web Development 40 hours @ $150/hr, Server Setup 1x $500
- Tax: 10%
- Due: Net 30
- My company: Zac Tech LLC
```

The agent will use this skill to generate a professional PDF invoice.

## Script Usage

```bash
python3 {baseDir}/scripts/gen_invoice.py \
  --from "Your Company, 123 Street, City" \
  --to "Client Name, 456 Ave, City" \
  --items "Web Development|40|150" "Server Setup|1|500" \
  --tax 10 \
  --currency USD \
  --due "Net 30" \
  --number "INV-2026-001" \
  --output invoice.pdf
```

## Features

- 📄 Clean, professional PDF layout
- 💰 Multiple currencies (USD, EUR, GBP, CNY, JPY, AUD, etc.)
- 📊 Automatic subtotal, tax, and total calculation
- 🔢 Sequential invoice numbering
- 🇨🇳 CJK text support (Chinese/Japanese/Korean company names and items)
- 📝 Notes and payment terms field
- 🖨️ Print-ready A4 format

## Item Format

Each item is a pipe-separated string: `description|quantity|unit_price`

```
"Website Design|1|2000"
"Hosting (monthly)|12|50"
"Content Writing|20|75"
```

## Dependencies

```bash
pip3 install reportlab
```

For CJK support, install CJK fonts:
```bash
sudo yum install -y google-noto-sans-cjk-ttc-fonts  # RHEL/CentOS
sudo apt install -y fonts-noto-cjk                    # Ubuntu/Debian
```
