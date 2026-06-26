# PDF API Hub — Advanced Workflows

## Batch Invoice Generation

Generate multiple PDFs from a data source using templates and `dynamic_params`.

```python
import requests

API_KEY = "your-api-key"
BASE_URL = "https://pdfapihub.com/api/v1"
HEADERS = {"CLIENT-API-KEY": API_KEY, "Content-Type": "application/json"}

invoice_template = """
<html>
<head><style>
  body { font-family: Arial, sans-serif; margin: 40px; }
  .header { display: flex; justify-content: space-between; }
  table { width: 100%; border-collapse: collapse; margin: 20px 0; }
  th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
  th { background: #f5f5f5; }
  .total { font-size: 18px; font-weight: bold; text-align: right; }
</style></head>
<body>
  <div class="header">
    <h1>{{company_name}}</h1>
    <h2>INVOICE #{{invoice_number}}</h2>
  </div>
  <p><strong>Date:</strong> {{date}}</p>
  <p><strong>Bill To:</strong> {{client_name}}</p>
  <p>{{client_address}}</p>
  {{items_table}}
  <p class="total">Total: ${{total}}</p>
</body>
</html>
"""

invoices = [
    {
        "invoice_number": "INV-001",
        "company_name": "Acme Inc",
        "date": "2026-04-17",
        "client_name": "Client Corp",
        "client_address": "123 Main St, NY",
        "items_table": "<table><tr><th>Item</th><th>Qty</th><th>Rate</th></tr><tr><td>Consulting</td><td>10</td><td>$150</td></tr></table>",
        "total": "1500",
    },
    {
        "invoice_number": "INV-002",
        "company_name": "Acme Inc",
        "date": "2026-04-17",
        "client_name": "Beta LLC",
        "client_address": "456 Oak Ave, CA",
        "items_table": "<table><tr><th>Item</th><th>Qty</th><th>Rate</th></tr><tr><td>Development</td><td>20</td><td>$200</td></tr></table>",
        "total": "4000",
    },
]

results = []
for inv in invoices:
    resp = requests.post(
        f"{BASE_URL}/generatePdf",
        headers=HEADERS,
        json={
            "html_content": invoice_template,
            "dynamic_params": inv,
            "paper_size": "A4",
            "margin": "medium",
            "output_format": "url",
            "output_filename": f"invoice-{inv['invoice_number']}.pdf",
        },
    )
    data = resp.json()
    if data["success"]:
        results.append(data["pdf_url"])
        print(f"{inv['invoice_number']}: {data['pdf_url']}")

# Optionally merge all invoices into one
if len(results) > 1:
    merge_resp = requests.post(
        f"{BASE_URL}/pdf/merge",
        headers=HEADERS,
        json={"urls": results, "output_format": "url", "output_filename": "all-invoices.pdf"},
    )
    print(f"Merged: {merge_resp.json()['pdf_url']}")
```

---

## Generate → Watermark → Lock Pipeline

Chain multiple endpoints to create, watermark, and encrypt a document.

```python
# Step 1: Generate PDF
gen = requests.post(
    f"{BASE_URL}/generatePdf",
    headers=HEADERS,
    json={
        "html_content": "<h1>Confidential Report</h1><p>Q1 2026 Financials...</p>",
        "paper_size": "A4",
        "output_format": "url",
    },
).json()

pdf_url = gen["pdf_url"]

# Step 2: Add watermark
wm = requests.post(
    f"{BASE_URL}/watermark",
    headers=HEADERS,
    json={
        "url": pdf_url,
        "text": "CONFIDENTIAL",
        "opacity": 0.2,
        "position": "center",
        "output_format": "url",
    },
).json()

watermarked_url = wm["pdf_url"]

# Step 3: Lock with password
locked = requests.post(
    f"{BASE_URL}/lockPdf",
    headers=HEADERS,
    json={
        "url": watermarked_url,
        "password": "securePass2026",
        "permissions": {"print": True, "copy": False, "edit": False},
        "output_format": "url",
    },
).json()

print(f"Final secured PDF: {locked['pdf_url']}")
```

---

## OCR → Parse → Export Pipeline

Extract text from scanned documents and convert to structured data.

```python
# Step 1: OCR the scanned PDF
ocr_result = requests.post(
    f"{BASE_URL}/pdfOcr",
    headers=HEADERS,
    json={
        "url": "https://example.com/scanned-bank-statement.pdf",
        "language": "eng",
        "output_format": "url",
    },
).json()

# Step 2: Parse the OCR'd PDF for tables
parsed = requests.post(
    f"{BASE_URL}/pdf/parse",
    headers=HEADERS,
    json={
        "url": ocr_result["pdf_url"],
        "extract_type": "tables",
        "output_format": "url",
    },
).json()

print(f"Extracted data: {parsed}")
```

---

## Webpage Screenshot + PDF Dual Output

Capture a webpage as both an image and a PDF simultaneously.

```python
import concurrent.futures

def capture_image():
    return requests.post(
        f"{BASE_URL}/generateImage",
        headers=HEADERS,
        json={
            "url": "https://example.com/dashboard",
            "full_page": True,
            "viewPortWidth": 1920,
            "image_format": "png",
            "output_format": "url",
        },
    ).json()

def capture_pdf():
    return requests.post(
        f"{BASE_URL}/generatePdf",
        headers=HEADERS,
        json={
            "url": "https://example.com/dashboard",
            "paper_size": "A4",
            "landscape": True,
            "wait_until": "networkidle",
            "output_format": "url",
        },
    ).json()

with concurrent.futures.ThreadPoolExecutor() as executor:
    img_future = executor.submit(capture_image)
    pdf_future = executor.submit(capture_pdf)
    
    img_result = img_future.result()
    pdf_result = pdf_future.result()

print(f"Screenshot: {img_result}")
print(f"PDF: {pdf_result['pdf_url']}")
```

---

## Compress + Split for Email Attachments

Split a large PDF and compress each chunk to stay under email size limits.

```python
# Step 1: Split into smaller parts
split_result = requests.post(
    f"{BASE_URL}/pdf/split",
    headers=HEADERS,
    json={
        "url": "https://example.com/large-report.pdf",
        "split_every": 5,  # 5 pages per chunk
        "output_format": "url",
    },
).json()

# Step 2: Compress each part
compressed_parts = []
for part_url in split_result.get("urls", []):
    comp = requests.post(
        f"{BASE_URL}/compressPdf",
        headers=HEADERS,
        json={
            "url": part_url,
            "compression_level": "high",
            "output_format": "url",
        },
    ).json()
    compressed_parts.append(comp["pdf_url"])

print(f"Ready to email: {compressed_parts}")
```

---

## Image Collection to PDF Booklet

Convert a folder of images into a single PDF document.

```python
image_urls = [
    "https://example.com/photos/img001.jpg",
    "https://example.com/photos/img002.jpg",
    "https://example.com/photos/img003.jpg",
    "https://example.com/photos/img004.jpg",
]

result = requests.post(
    f"{BASE_URL}/imageToPdf",
    headers=HEADERS,
    json={
        "urls": image_urls,
        "paper_size": "A4",
        "landscape": False,
        "fit_mode": "contain",
        "output_format": "url",
        "output_filename": "photo-booklet.pdf",
    },
).json()

print(f"Booklet PDF: {result['pdf_url']}")
```

---

## Retry with Exponential Backoff

Handle rate limits (429) gracefully.

```python
import time

def call_api(endpoint, payload, max_retries=3):
    for attempt in range(max_retries):
        resp = requests.post(
            f"{BASE_URL}/{endpoint}",
            headers=HEADERS,
            json=payload,
        )
        if resp.status_code == 429:
            wait = 2 ** attempt
            print(f"Rate limited. Retrying in {wait}s...")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise Exception(f"Failed after {max_retries} retries")
```

---

## Download PDF to Local File

Save the hosted URL result to a local file.

```python
def download_pdf(pdf_url, output_path):
    resp = requests.get(pdf_url)
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(resp.content)
    print(f"Saved to {output_path} ({len(resp.content)} bytes)")

# After any API call that returns a pdf_url:
result = requests.post(
    f"{BASE_URL}/generatePdf",
    headers=HEADERS,
    json={"html_content": "<h1>Test</h1>", "output_format": "url"},
).json()

download_pdf(result["pdf_url"], "output.pdf")
```

---

## Using Templates for Consistent Branding

Save a template once, reuse with different data each time.

```python
# Step 1: Create a template (one-time)
requests.post(
    f"{BASE_URL}/createTemplate",
    headers=HEADERS,
    json={
        "name": "company-invoice-v1",
        "html_content": """
            <div style="font-family: Arial; padding: 40px;">
                <img src="{{logo_url}}" height="40">
                <h1>Invoice #{{number}}</h1>
                <p>Date: {{date}}</p>
                <p>Client: {{client}}</p>
                {{line_items}}
                <h2>Total: ${{total}}</h2>
            </div>
        """,
        "css_content": "h1 { color: #2c3e50; } h2 { text-align: right; }",
    },
).json()

# Step 2: Generate PDFs using the template + dynamic_params
result = requests.post(
    f"{BASE_URL}/generatePdf",
    headers=HEADERS,
    json={
        "html_content": "{{template:company-invoice-v1}}",
        "dynamic_params": {
            "logo_url": "https://example.com/logo.png",
            "number": "INV-100",
            "date": "2026-04-17",
            "client": "Acme Corp",
            "line_items": "<table><tr><td>Service</td><td>$5000</td></tr></table>",
            "total": "5000",
        },
        "output_format": "url",
    },
).json()

print(result["pdf_url"])
```
