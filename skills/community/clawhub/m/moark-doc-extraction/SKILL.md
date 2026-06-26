---
name: moark-doc-extraction
description: Extract and recognize text from documents, including PDF and DOCX files.
metadata:
  {
    "openclaw":
      {
        "emoji":"📖",
        "requires": { "env": ["GITEEAI_API_KEY"]},
        "primaryEnv": "GITEEAI_API_KEY"
      }
  }
---

# Document Extraction
This skill allows users to extract and recognize text from documents, including PDF and DOCX files, using an external GITEE AI API.

## Usage

Ensure you have installed the required dependencies (`pip install requests requests-toolbelt`). Use the bundled script to perform document extraction.

```bash
python {baseDir}/scripts/perform_doc_extraction.py --file /path/to/document.pdf --api-key YOUR_API
```

## Options
No additional parameters are required for this skill.

## Workflow

1. Execute the perform_doc_extraction.py script with the parameters from the user.
2. Parse the script output and find the line starting with `EXTRACTION_RESULT:`.
3. Extract the OCR result from that line (format: `EXTRACTION_RESULT: ...`).
4. Display the OCR result to the user using markdown syntax: `📖[EXTRACTION_RESULT Result]`.

## Notes
- If GITEEAI_API_KEY is none, you should remind user to provide --api-key argument
- Please handle the output of the script carefully, ensuring that you only extract and display the relevant information without adding any extra commentary or interpretation.
- You should optimize the output format to make it more concise and user-friendly, but do not change or ignore the content of the result.
- The script prints `EXTRACTION_RESULT:` in the output - extract this result and display it using markdown image syntax:`📖[EXTRACTION_RESULT Result]`.
- Always look for the line starting with `EXTRACTION_RESULT:` in the script output.