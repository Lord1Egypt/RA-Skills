# Reference Documentation for Ocr

## OCR.space API (Demo)

- **Endpoint:** `https://api.ocr.space/parse/image`
- **Method:** `POST`
- **Parameters:**
  - `apikey` (string) – API key. The public demo key is `helloworld` (limited usage, suitable for testing).
  - `url` (string, optional) – Direct URL to the image to process.
  - `language` (string, optional) – Language code (e.g., `eng`, `deu`, `spa`). Default `eng`.
  - `isOverlayRequired` (bool, optional) – Set to `false` for plain text output.
  - `file` (binary, optional) – Upload a local image file when not using a URL.
- **Response (JSON):**
  ```json
  {
    "ParsedResults": [{"ParsedText": "..."}],
    "IsErroredOnProcessing": false,
    "ErrorMessage": []
  }
  ```
- **Rate limits:** The demo key is heavily throttled; for production use obtain a personal API key from https://ocr.space/ocrapi.
- **Supported formats:** JPG, PNG, BMP, GIF, TIFF.
- **Notes:** The demo key may reject large images (>1 MB) and has a daily request cap.

## Usage in the OCR Skill

The `scripts/example.py` script demonstrates how to call this API for both URLs and local files, handling errors and returning the extracted plain text.

