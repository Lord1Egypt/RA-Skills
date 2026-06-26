# OpenDataLoader PDF — Examples

## 1. RAG Knowledge Base Pipeline

```python
import os
from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def build_rag_pipeline(pdf_folder: str, persist_dir: str = "./chroma_db"):
    """Build RAG pipeline from PDF folder → vector store."""
    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

    # Load all PDFs
    loader = OpenDataLoaderPDFLoader(file_path=pdf_files, format="text")
    documents = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    # Embed and store
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory=persist_dir)
    vectorstore.persist()

    return vectorstore

# Usage
vs = build_rag_pipeline("./fmt_guides/")
retriever = vs.as_retriever()
```

## 2. Extract Tables to CSV

```python
import json
import csv
from opendataloader_pdf import convert

convert(
    input_path=["report.pdf"],
    output_dir="./output/",
    format="json"
)

# Parse JSON and extract table rows
with open("./output/report.json") as f:
    data = json.load(f)

tables = [item for item in data if item["type"] == "table"]
for table in tables:
    rows = table["content"]["rows"]
    headers = rows[0]
    data_rows = rows[1:]
    print(headers)
```

## 3. Batch Process Folder

```python
from opendataloader_pdf import convert
import os

pdf_dir = "./pdfs/"
output_dir = "./parsed/"

pdf_files = [
    os.path.join(pdf_dir, f)
    for f in os.listdir(pdf_dir)
    if f.endswith(".pdf")
]

# Batch: markdown for RAG
convert(
    input_path=pdf_files,
    output_dir=output_dir,
    format="markdown"
)
print(f"Parsed {len(pdf_files)} files → {output_dir}")
```

## 4. Medical Report with Citation Coordinates

```python
from opendataloader_pdf import convert

# Extract with bounding boxes for precise citation
convert(
    input_path=["lab_report.pdf"],
    output_dir="./output/",
    format="json",
    hybrid="docling-fast"  # Better table accuracy
)

# JSON output includes bounding boxes like:
# {
#   "type": "table",
#   "id": 7,
#   "page number": 2,
#   "bounding box": [72.0, 500.0, 540.0, 700.0],
#   "content": { "rows": [["指标", "数值"], ...] }
# }
```

## 5. Scanned Document OCR + RAG

```python
from opendataloader_pdf import convert

# Start hybrid backend first:
# opendataloader-pdf-hybrid --port 5002 --force-ocr

convert(
    input_path=["scanned_document.pdf"],
    output_dir="./output/",
    format="markdown",
    hybrid="docling-fast",
    hybrid_mode="full"
)

# Then feed to RAG pipeline
```
