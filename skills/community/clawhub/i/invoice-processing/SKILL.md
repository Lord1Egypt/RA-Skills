**WORKFLOW SKILL** — Process and organize invoice PDFs using `main.py`. 

USE FOR: Organizing invoices in a directory when the user provides a keyword. Capabilities include:
1. Fixing `.pdf` extensions (files ending in `?` or `？`).
2. Removing duplicate files based on MD5 hash.
3. Removing invalid files (e.g. containing "行程单").
4. Checking PDF contents for a mandatory missing `keyword`.
5. Calculating the grand total amount from all valid invoices.

DO NOT USE FOR: General Python debugging or other non-invoice related tasks.
INVOKES: Terminal tool to run `python main.py process <keyword> -d <dir>`

# Instructions for the Agent

When the user asks you to process or organize invoices (e.g., "整理 ./fapiao 里 的发票，关键字是 银河科技;腾讯"):
1. **Extract Arguments**: 
   - `dir`: The target directory. If the user does not specify a directory, safely default to the current directory (`.`) or ask the user if it is ambiguous.
   - `keyword`: The target keyword to check inside the PDFs (e.g., a company name). Note: Multiple keywords can be provided separated by a semicolon `;` (e.g., `CompanyA;CompanyB`).
2. **Handle Missing Keyword**: 
   - You MUST prompt the user for the `<keyword>` if it is missing from their request. Do not guess it.
3. **Execute Command**:
   - Construct and run the following terminal command (replacing placeholders with extracted values):
     `python main.py process <keyword> -d <dir>`
4. **Report Results**:
   - After the script completes, summarize the printed results for the user (files fixed, dupes removed, files moved to `<dir>/invoices`, and files moved to `<dir>/invoices/unknown`, plus the grand total).
