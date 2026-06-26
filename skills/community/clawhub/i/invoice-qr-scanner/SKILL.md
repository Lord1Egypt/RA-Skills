---
name: invoice-qr-scanner
description: Scan QR codes from invoice receipts and automatically fill electronic invoice applications. Use when user asks to scan QR codes from images, complete electronic invoice applications, or process invoice receipts that contain QR codes for online billing systems.
---

# Invoice QR Scanner

## Overview

This skill enables automatic electronic invoice application by scanning QR codes from receipt images and filling out online invoice forms. It handles the complete workflow from QR code detection to invoice submission.

## Workflow

### Step 1: QR Code Recognition

When a user provides an invoice receipt image containing a QR code:

1. Run the QR code recognition script:
   ```bash
   node scan-qr.js <image-path>
   ```
2. The script outputs the decoded QR code URL
3. If recognition fails, ask user to provide the URL directly

### Step 2: Navigate to Invoice System

1. Open the decoded URL in browser automation
2. Verify the page loads successfully
3. Take snapshot to understand form structure

### Step 3: Retrieve Company Information

Before filling the form, retrieve the user's company information:

1. Check memory files for stored invoice header information:
   - Search `memory/YYYY-MM-DD.md` for recent invoice info
   - Check `MEMORY.md` for long-term stored details
2. Required fields typically include:
   - Company name (公司名称)
   - Tax ID/Unified Social Credit Code (税号)
   - Address (地址)
   - Phone number (电话)
   - Bank name (开户行)
   - Bank account number (银行账号)

### Step 4: Fill Invoice Form

1. Analyze the form structure using browser snapshot
2. Fill in company information fields
3. Fill in recipient information:
   - Phone number (手机号)
   - Email address (邮箱)
4. Verify all required fields are completed

### Step 5: Review and Submit

1. Submit the form
2. Review confirmation page
3. Verify all information is correct
4. Report results to user

## Error Handling

### QR Code Not Recognized

If QR code recognition fails:
1. Ask user to provide the URL directly
2. Suggest using phone to scan and share the URL

### Form Structure Changes

If the invoice system form structure changes:
1. Take a new snapshot
2. Identify updated field references
3. Adapt the filling process accordingly
4. Document the new structure for future reference

### Missing Information

If required company or contact information is missing:
1. Ask user to provide the missing details
2. Update memory files with new information
3. Continue with the invoice application

## Scripts

### scan-qr.js

Primary script for QR code recognition from images using Node.js and qrcode-reader library.

**Usage:**
```bash
node scan-qr.js <image-path>
```

**Requirements:**
- Node.js environment (v14+)
- npm packages: `qrcode-reader`, `canvas`

**Installation:**
```bash
cd scripts
npm install qrcode-reader canvas
```

**Output:**
- Decoded QR code URL on success (format: "✅ 识别成功: <url>")
- Error message on failure (format: "❌ 错误: <error message>")

**Technology:**
- Uses qrcode-reader library for QR code decoding
- Canvas for image processing
- Pure JavaScript implementation (no Worker required)

## Memory Integration

This skill relies on stored user information in memory files:

**Company Invoice Header Information** (stored in MEMORY.md):
- Company name
- Tax ID
- Address
- Phone number
- Bank information

**Contact Information** (stored in MEMORY.md):
- Mobile phone numbers
- Email addresses

When filling forms, always reference this information first before asking the user.

## Best Practices

1. **Always verify** the decoded URL is legitimate before proceeding
2. **Double-check** all information before submission
3. **Take snapshots** at each step for documentation
4. **Report results** clearly to the user after submission
5. **Update memory** with new information if user provides corrections
6. **Use auto-complete** when available (more accurate than manual input)
