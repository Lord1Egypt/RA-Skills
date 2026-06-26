---
name: moark-ocr
description: Perform Optical Character Recognition (OCR) to extract and recognize text from images.
metadata:
  {
    "openclaw":
      {
        "emoji":"📷",
        "requires": { "env": ["GITEEAI_API_KEY"]},
        "primaryEnv": "GITEEAI_API_KEY"
      }
  }
---

# OCR (Optical Character Recognition)
This skill allows users to extract and recognize text from images using an external GITEE AI API. 

## Usage

Ensure you have installed the required dependencies (`pip install openai`). Use the bundled script to perform OCR on an image.

```bash
python {baseDir}/scripts/perform_ocr.py --image /path/to/image.jpg --prompt "Users requirements" --api-key YOUR_API_KEY
```

## Options
No additional parameters are required for this skill.

## Workflow

1. Execute the perform_ocr.py script with the parameters from the user.
2. Parse the script output and find the line starting with `OCR_RESULT:`.
3. Extract the OCR result from that line (format: `OCR_RESULT: ...`).
4. Display the OCR result to the user using markdown syntax: `📷[OCR Result]`.

## Notes
- If GITEEAI_API_KEY is none, you should remind user to provide --api-key argument
- You should not only return the OCR result but also provide a brief summary of the recognized text based on the user's prompt.
- When you add prompt, you should honestly repeat the requirements from user without any additional imaginations.
- The script prints `OCR_RESULT:` in the output - extract this result and display it using markdown image syntax:`📷[OCR Result]`.
- Always look for the line starting with `OCR_RESULT:` in the script output.