---
name: privacy-guard
description: Protects sensitive files (contracts, transaction data, personal/customer privacy) by performing deep content inspection for text and binary formats (PDF, DOCX, XLSX) before any read, search, or send operation.
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "always": false,
        "requires": { "bins": ["python3"], "pips": ["pdfplumber", "python-docx", "openpyxl"] }
      }
  }
---

# Privacy Guard (申石隐私卫士)

This skill is designed to protect sensitive files on the user's local system, preventing them from being inadvertently sent to remote servers or external APIs. It performs deep content inspection across various file formats.

该技能用于保护用户本地系统中的敏感文件，避免这些文件被意外发送到远程服务器或外部 API。它支持对多种文件格式进行深度内容检查。

## Core Rules and Mandatory Enforcement

1.  **Mandatory Scan Before Operation**: Before performing *any* action involving file reading, searching, or sending (e.g., `upload`, `send`, `read_file`, `file` tool actions), you **MUST** first scan the target file for sensitive information using the provided `scan_file.py` script. This is a non-negotiable step.
2.  **Strict Blocking on Detection**: If the `scan_file.py` script returns an output starting with `BLOCK:`, you **MUST immediately and unconditionally stop** the current task. You are strictly forbidden from proceeding with the operation or attempting to bypass this restriction. Inform the user clearly about the detected sensitive content and the cessation of the operation.
3.  **No Silent Data Transmission**: Under no circumstances are you permitted to send any local file content to an external API, remote server, or any external destination without prior validation and a `PASS:` result from this skill.

## Supported File Formats

The skill performs deep content scanning for the following formats:
*   **Text-based**: `.txt`, `.csv`, `.md`, `.json`, `.xml`, `.log`, `.py`, `.js`, `.html`
*   **Documents**: `.pdf`, `.docx`
*   **Spreadsheets**: `.xlsx`

## Sensitive Information Categories

The skill monitors for the following four categories of sensitive information:

*   **Contracts/Agreements**: Files containing keywords like “合同”, “协议”, “Contract”, “Agreement”.
*   **Transaction Data**: Files containing keywords like “交易记录”, “支付明细”, “Transaction Data”, “Amount”, “Balance”.
*   **Personal Privacy**: Files containing keywords like “身份证”, “手机号”, “家庭住址”, “Personal Privacy”, “ID Card”, “Phone Number”.
*   **Customer Privacy**: Files containing keywords like “客户信息”, “Client Data”, “Customer Privacy”, “User Profile”.

## Usage Workflow

## Installation

Install required dependencies once before running scans:

```bash
python3 -m pip install -r {baseDir}/requirements.txt
```

Optional helper:

```bash
bash {baseDir}/scripts/install_deps.sh
```

### 1. File Scanning

Before processing any file path, call the built-in scanning script using a relative path from the skill's base directory:

```bash
python3 {baseDir}/scripts/scan_file.py <file_path>
```

### 2. Handling Results

*   **If the output starts with `BLOCK:`**:
    *   Immediately stop all subsequent steps.
    *   Report to the user: "Detected sensitive file [filename], containing [sensitive information type]. Execution has been stopped according to the privacy protection policy."
    *   Do NOT attempt to bypass this restriction.

*   **If the output starts with `PASS:`**:
    *   You may proceed with the intended operation.

## Example Scenario

**Scenario: User requests "Send this contract to my boss"**

1.  Identify the keyword "contract" or "合同".
2.  Invoke the scan: `python3 {baseDir}/scripts/scan_file.py ./contract.pdf`.
3.  If the script returns `BLOCK: Sensitive keyword '合同' found in content (Category: Contract/Agreement).`, stop and inform the user.
4.  Response: "I'm sorry, but I've detected that this file is a protected contract. For your data security, I have stopped the sending operation."
