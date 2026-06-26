# PDF API Hub — Code Examples

All examples use `https://pdfapihub.com/api/v1/` as the base URL.
Replace `your-api-key` with your actual `CLIENT-API-KEY`.

---

## HTML to PDF

### cURL

```bash
curl -X POST https://pdfapihub.com/api/v1/generatePdf \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "html_content": "<h1>Invoice #1234</h1><p>Total: $500</p>",
    "css_content": "h1 { font-size: 28px; color: #333; } p { font-size: 16px; }",
    "paper_size": "A4",
    "margin": "medium",
    "print_background": true,
    "output_format": "url"
  }'
```

### Python (requests)

```python
import requests

API_KEY = "your-api-key"
BASE_URL = "https://pdfapihub.com/api/v1"

response = requests.post(
    f"{BASE_URL}/generatePdf",
    headers={
        "CLIENT-API-KEY": API_KEY,
        "Content-Type": "application/json",
    },
    json={
        "html_content": "<h1>Invoice #1234</h1><p>Total: $500</p>",
        "css_content": "h1 { font-size: 28px; color: #333; }",
        "paper_size": "A4",
        "margin": "medium",
        "print_background": True,
        "output_format": "url",
    },
)

data = response.json()
if data["success"]:
    print(f"PDF URL: {data['pdf_url']}")
```

### Node.js (fetch)

```javascript
const API_KEY = "your-api-key";
const BASE_URL = "https://pdfapihub.com/api/v1";

const response = await fetch(`${BASE_URL}/generatePdf`, {
  method: "POST",
  headers: {
    "CLIENT-API-KEY": API_KEY,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    html_content: "<h1>Invoice #1234</h1><p>Total: $500</p>",
    css_content: "h1 { font-size: 28px; color: #333; }",
    paper_size: "A4",
    margin: "medium",
    print_background: true,
    output_format: "url",
  }),
});

const data = await response.json();
if (data.success) {
  console.log(`PDF URL: ${data.pdf_url}`);
}
```

---

## URL to PDF (Webpage Capture)

### cURL

```bash
curl -X POST https://pdfapihub.com/api/v1/generatePdf \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "paper_size": "A4",
    "wait_until": "networkidle",
    "print_background": true,
    "output_format": "url"
  }'
```

### Python

```python
response = requests.post(
    f"{BASE_URL}/generatePdf",
    headers={"CLIENT-API-KEY": API_KEY, "Content-Type": "application/json"},
    json={
        "url": "https://example.com",
        "paper_size": "A4",
        "wait_until": "networkidle",
        "print_background": True,
        "output_format": "url",
    },
)
```

---

## Dynamic Templates with Placeholders

```bash
curl -X POST https://pdfapihub.com/api/v1/generatePdf \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "html_content": "<h1>Welcome, {{name}}!</h1><p>Your order #{{order_id}} is confirmed.</p>",
    "css_content": "body { font-family: Arial, sans-serif; padding: 40px; }",
    "dynamic_params": {
      "name": "Rishabh",
      "order_id": "ORD-9876"
    },
    "output_format": "url"
  }'
```

---

## Merge PDFs

### cURL

```bash
curl -X POST https://pdfapihub.com/api/v1/pdf/merge \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://example.com/doc1.pdf",
      "https://example.com/doc2.pdf",
      "https://example.com/doc3.pdf"
    ],
    "output_format": "url",
    "output_filename": "combined-report.pdf"
  }'
```

### Python

```python
response = requests.post(
    f"{BASE_URL}/pdf/merge",
    headers={"CLIENT-API-KEY": API_KEY, "Content-Type": "application/json"},
    json={
        "urls": [
            "https://example.com/doc1.pdf",
            "https://example.com/doc2.pdf",
        ],
        "output_format": "url",
    },
)
```

---

## Split PDF

```bash
curl -X POST https://pdfapihub.com/api/v1/pdf/split \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/large-document.pdf",
    "pages": "1-5,10-15",
    "output_format": "url"
  }'
```

---

## Compress PDF

```bash
curl -X POST https://pdfapihub.com/api/v1/compressPdf \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/heavy-file.pdf",
    "compression_level": "high",
    "output_format": "url"
  }'
```

---

## OCR — Extract Text from Scanned PDF

```bash
curl -X POST https://pdfapihub.com/api/v1/pdfOcr \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/scanned-doc.pdf",
    "language": "eng",
    "pages": "1-3",
    "output_format": "url"
  }'
```

---

## OCR — Extract Text from Image

```bash
curl -X POST https://pdfapihub.com/api/v1/imageOcr \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/receipt.jpg",
    "language": "eng",
    "output_format": "url"
  }'
```

---

## Watermark a PDF

```bash
curl -X POST https://pdfapihub.com/api/v1/watermark \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/contract.pdf",
    "text": "DRAFT",
    "opacity": 0.3,
    "position": "center",
    "output_format": "url"
  }'
```

---

## Sign a PDF

```bash
curl -X POST https://pdfapihub.com/api/v1/sign-pdf \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/agreement.pdf",
    "signature_url": "https://example.com/my-signature.png",
    "position": "bottom-right",
    "pages": "last",
    "output_format": "url"
  }'
```

---

## Lock PDF (Encrypt)

```bash
curl -X POST https://pdfapihub.com/api/v1/lockPdf \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/sensitive.pdf",
    "password": "securePass123",
    "permissions": { "print": true, "copy": false, "edit": false },
    "output_format": "url"
  }'
```

---

## Unlock PDF (Decrypt)

```bash
curl -X POST https://pdfapihub.com/api/v1/unlockPdf \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/locked.pdf",
    "password": "securePass123",
    "output_format": "url"
  }'
```

---

## Screenshot — URL to Image

```bash
curl -X POST https://pdfapihub.com/api/v1/generateImage \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "full_page": true,
    "viewPortWidth": 1920,
    "image_format": "png",
    "output_format": "url"
  }'
```

---

## PDF to Image

```bash
curl -X POST https://pdfapihub.com/api/v1/pdfToImage \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/document.pdf",
    "pages": "1-3",
    "image_format": "png",
    "dpi": 300,
    "output_format": "url"
  }'
```

---

## Images to PDF

```bash
curl -X POST https://pdfapihub.com/api/v1/imageToPdf \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://example.com/page1.png",
      "https://example.com/page2.jpg"
    ],
    "paper_size": "A4",
    "fit_mode": "contain",
    "output_format": "url"
  }'
```

---

## Scrape Website — URL to HTML

```bash
curl -X POST https://pdfapihub.com/api/v1/urlToHtml \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/spa-page",
    "wait_until": "networkidle"
  }'
```

---

## Parse / Extract PDF

```bash
curl -X POST https://pdfapihub.com/api/v1/pdf/parse \
  -H "CLIENT-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/report.pdf",
    "extract_type": "tables",
    "pages": "1-5",
    "output_format": "url"
  }'
```

---

## Reusable Helper Pattern (Python)

```python
import os
import requests

class PDFApiHub:
    """Minimal wrapper for PDF API Hub endpoints."""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ["PDFAPIHUB_API_KEY"]
        self.base_url = "https://pdfapihub.com/api/v1"
        self.headers = {
            "CLIENT-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }

    def _post(self, endpoint, payload):
        resp = requests.post(
            f"{self.base_url}/{endpoint}",
            headers=self.headers,
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()

    def generate_pdf(self, **kwargs):
        return self._post("generatePdf", kwargs)

    def merge_pdf(self, urls, **kwargs):
        return self._post("pdf/merge", {"urls": urls, **kwargs})

    def split_pdf(self, url, **kwargs):
        return self._post("pdf/split", {"url": url, **kwargs})

    def compress_pdf(self, url, **kwargs):
        return self._post("compressPdf", {"url": url, **kwargs})

    def pdf_ocr(self, url, **kwargs):
        return self._post("pdfOcr", {"url": url, **kwargs})

    def image_ocr(self, url, **kwargs):
        return self._post("imageOcr", {"url": url, **kwargs})

    def watermark(self, url, **kwargs):
        return self._post("watermark", {"url": url, **kwargs})

    def sign_pdf(self, url, signature_url, **kwargs):
        return self._post("sign-pdf", {"url": url, "signature_url": signature_url, **kwargs})

    def lock_pdf(self, url, password, **kwargs):
        return self._post("lockPdf", {"url": url, "password": password, **kwargs})

    def unlock_pdf(self, url, password, **kwargs):
        return self._post("unlockPdf", {"url": url, "password": password, **kwargs})

    def generate_image(self, **kwargs):
        return self._post("generateImage", kwargs)

    def pdf_to_image(self, url, **kwargs):
        return self._post("pdfToImage", {"url": url, **kwargs})

    def image_to_pdf(self, urls, **kwargs):
        return self._post("imageToPdf", {"urls": urls, **kwargs})

    def parse_pdf(self, url, **kwargs):
        return self._post("pdf/parse", {"url": url, **kwargs})

    def url_to_html(self, url, **kwargs):
        return self._post("urlToHtml", {"url": url, **kwargs})


# Usage
api = PDFApiHub()  # reads PDFAPIHUB_API_KEY from env

result = api.generate_pdf(
    html_content="<h1>Hello World</h1>",
    paper_size="A4",
    output_format="url",
)
print(result["pdf_url"])
```

---

## Reusable Helper Pattern (Node.js)

```javascript
class PDFApiHub {
  constructor(apiKey = process.env.PDFAPIHUB_API_KEY) {
    this.apiKey = apiKey;
    this.baseUrl = "https://pdfapihub.com/api/v1";
  }

  async _post(endpoint, payload) {
    const response = await fetch(`${this.baseUrl}/${endpoint}`, {
      method: "POST",
      headers: {
        "CLIENT-API-KEY": this.apiKey,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return response.json();
  }

  generatePdf(params) { return this._post("generatePdf", params); }
  mergePdf(urls, params = {}) { return this._post("pdf/merge", { urls, ...params }); }
  splitPdf(url, params = {}) { return this._post("pdf/split", { url, ...params }); }
  compressPdf(url, params = {}) { return this._post("compressPdf", { url, ...params }); }
  pdfOcr(url, params = {}) { return this._post("pdfOcr", { url, ...params }); }
  imageOcr(url, params = {}) { return this._post("imageOcr", { url, ...params }); }
  watermark(url, params = {}) { return this._post("watermark", { url, ...params }); }
  signPdf(url, signatureUrl, params = {}) { return this._post("sign-pdf", { url, signature_url: signatureUrl, ...params }); }
  lockPdf(url, password, params = {}) { return this._post("lockPdf", { url, password, ...params }); }
  unlockPdf(url, password, params = {}) { return this._post("unlockPdf", { url, password, ...params }); }
  generateImage(params) { return this._post("generateImage", params); }
  pdfToImage(url, params = {}) { return this._post("pdfToImage", { url, ...params }); }
  imageToPdf(urls, params = {}) { return this._post("imageToPdf", { urls, ...params }); }
  parsePdf(url, params = {}) { return this._post("pdf/parse", { url, ...params }); }
  urlToHtml(url, params = {}) { return this._post("urlToHtml", { url, ...params }); }
}

// Usage
const api = new PDFApiHub();
const result = await api.generatePdf({
  html_content: "<h1>Hello World</h1>",
  paper_size: "A4",
  output_format: "url",
});
console.log(result.pdf_url);
```
