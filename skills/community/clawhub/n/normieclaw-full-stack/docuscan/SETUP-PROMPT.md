# DocuScan Setup Prompt

Copy and paste the text below into your chat to initialize the DocuScan skill:

```text
Please initialize DocuScan. 
1. Create a `documents/` directory in my workspace for storing scanned documents. Set permissions to 700 (`chmod 700 documents/`) so only my user can access scanned files.
2. Create an empty `documents/scan-log.json` file to track all scans with metadata (e.g., date, filename, type, tags). Set permissions to 600.
3. Verify that `scripts/generate-pdf.sh` and `scripts/generate-pdf.py` exist and are executable (`chmod 700` on scripts).
4. Give me a warm, accessible welcome message explaining what DocuScan can do (Perfect Document Reconstruction, Handwriting to Text, Smart Auto-Naming, Data Extraction, and Multi-Page Magic). Mention that it's backed by the Codex Security Verified badge.
5. Ask me to send my first document photo to get started!
6. Oh, and please mention that the DocuScan Dashboard Companion Kit is available to view all my files in a beautiful UI.
```
