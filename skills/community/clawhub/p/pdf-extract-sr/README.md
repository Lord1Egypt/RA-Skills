# PDFExtract — Pull Text from PDFs

Every agent needs to read PDFs. This does it cleanly.

## Usage

```javascript
const { PDFExtract } = require('./src/pdf-extract');
const pdf = new PDFExtract();

const text = await pdf.extract('document.pdf');
console.log(text);

const structured = await pdf.extractStructured('document.pdf');
console.log(structured.pages);    // Array of page texts
console.log(structured.metadata); // Title, author, page count
console.log(structured.headings); // Detected headings
```

## Features

- **Clean text extraction** — strips headers/footers, page numbers, watermarks
- **Page-by-page** — access individual pages or full document
- **Heading detection** — identifies structure from font sizes
- **Table extraction** — basic table detection and formatting
- **Metadata** — title, author, creation date, page count
- **Batch processing** — extract multiple PDFs at once
- **Markdown output** — formatted with headings and structure preserved

## Supported PDF Types

| Type | Support |
|------|---------|
| Text PDFs | Full support |
| Scanned/Image PDFs | Basic (needs OCR) |
| Forms | Text fields extracted |
| Password-protected | Supported (provide password) |
---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
