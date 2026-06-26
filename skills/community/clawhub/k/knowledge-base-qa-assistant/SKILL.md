---
name: knowledge-base-qa-assistant
version: 1.0.0
description: |
  Build private knowledge bases for AI-powered document Q&A. Supports PDF, Word, TXT, Markdown uploads with smart chunking and vector retrieval. Automatically cites sources in answers. Perfect for enterprise knowledge management and customer service knowledge bases.
tags: ["knowledge-base", "rag", "document-qa", "vector-search", "enterprise", "content-management"]
---

# Knowledge Base QA Assistant

> 📚 Build a private knowledge base for AI-powered document Q&A

## Skill Overview

This skill helps AI Agents build and manage private knowledge bases, supporting document uploads (PDF, Word, TXT, Markdown, etc.), then providing precise Q&A based on the knowledge base content. Ideal for enterprise knowledge management, product documentation Q&A, and customer service knowledge bases.

## Core Capabilities

- **Multi-format Support**: PDF, Word, TXT, Markdown, Excel, PPT, and more
- **Smart Chunking**: Automatically split long documents into semantically complete chunks
- **Vector Retrieval**: Precise matching based on semantic similarity
- **Source Citation**: Automatically cite reference sources in answers
- **Batch Upload**: Support batch upload of multiple documents

## Trigger Keywords

- `/knowledge-qa`
- `/upload-document`
- `/document-qa`
- `/knowledge-base-manage`
- `/doc-question`
- `/rag-qa`

## How to Use

### Step 1: Build Knowledge Base

User uploads documents to build knowledge base:

```
User: Please upload this product document to the knowledge base
Agent: Please provide the document content or upload file

User: [Upload PDF file]
Agent: ✅ Document uploaded to knowledge base successfully!
     
     Document Name: Product Manual.pdf
     File Size: 2.5MB
     Pages: 45
     Status: Indexed, ready for Q&A
     
     Knowledge Points Extracted: 23
     Knowledge Chunks: 12
```

### Step 2: Knowledge Base Q&A

```
User: What payment methods does the product support?
Agent: Searching knowledge base...
     
     ✅ Found relevant information!
     
     Answer: The product supports the following payment methods:
     
     1. **Online Payment**
        - PayPal
        - Stripe
        - Credit Card (Visa, MasterCard supported)
     
     2. **Offline Payment**
        - Bank Transfer
        - Wire Transfer
     
     📎 Reference: Product Manual Section 3.2, Published: 2024-01-15
```

## Knowledge Base Commands

| Command | Function |
|---------|----------|
| `/knowledge-list` | View all documents in knowledge base |
| `/delete-doc [filename]` | Delete specified document |
| `/knowledge-stats` | View knowledge base statistics |
| `/clear-knowledge` | Clear all documents (requires confirmation) |

## Knowledge Base Structure

### Document Storage

```
knowledge_base/
├── documents/
│   ├── doc_001/
│   │   ├── original.pdf          # Original document
│   │   └── metadata.json          # Metadata
│   ├── doc_002/
│   │   ├── content.txt           # Extracted text
│   │   └── metadata.json
│   └── ...
└── index/
    └── vector_index.json          # Vector index
```

### Metadata Format

```json
{
  "doc_id": "doc_001",
  "filename": "Product Manual.pdf",
  "upload_time": "2024-01-20T10:30:00Z",
  "file_size": "2.5MB",
  "page_count": 45,
  "chunk_count": 12,
  "status": "indexed",
  "tags": ["product", "user-guide", "features"]
}
```

## Retrieval Flow

```
User Question
    ↓
Question Embedding
    ↓
Vector Similarity Matching
    ↓
Top-K Relevant Chunks
    ↓
Build Prompt Context
    ↓
LLM Generate Answer
    ↓
Add Citation
    ↓
Return Answer
```

## Usage Examples

### Example 1: Enterprise Knowledge Base Q&A

```
User: What is the company's remote work policy?
Agent: Searching knowledge base...
     
     ✅ Found relevant information!
     
     From Employee Handbook 2024, Chapter 4, Section 2:
     
     **Remote Work Policy:**
     
     | Employee Type | Remote Days | Requirements |
     |---------------|-------------|--------------|
     | Full-time | 3 days/week | Manager approval |
     | Part-time | 2 days/week | Core hours required |
     | Contract | Case-by-case | HR consultation |
     
     📎 Reference: Employee Handbook 2024, Chapter 4, Section 2
```

### Example 2: Technical Documentation Q&A

```
User: How to configure OAuth2.0 login?
Agent: Searching technical docs...
     
     ✅ Found configuration guide!
     
     **OAuth2.0 Configuration Steps:**
     
     1. **Register Application**
        Register app with OAuth provider, get client_id and client_secret
     
     2. **Configure Callback URL**
        Set auth callback URL: https://your-app.com/callback
     
     3. **Implement Auth Flow**
        ```javascript
        const oauth = new OAuth2({
          clientId: 'your_client_id',
          clientSecret: 'your_client_secret',
          redirectUri: 'https://your-app.com/callback'
        });
        ```
     
     📎 Reference: Developer Documentation Section 5.2
```

### Example 3: Batch Document Upload

```
User: I want to upload these 3 documents to the knowledge base:
1. Product Introduction.pdf
2. Technical Whitepaper.docx
3. FAQ.md

Agent: Batch uploading...
     ✅ Upload complete!
     
     | Document | Status | Knowledge Points |
     |----------|--------|-------------------|
     | Product Introduction.pdf | ✅ Success | 15 |
     | Technical Whitepaper.docx | ✅ Success | 28 |
     | FAQ.md | ✅ Success | 42 |
     
     📚 Knowledge Base Stats:
     - Total Documents: 3
     - Total Knowledge Points: 85
     - Knowledge Chunks: 12
```

## Configuration Options

### Retrieval Parameters

| Parameter | Default | Description |
|-----------|--------|-------------|
| top_k | 5 | Number of relevant chunks to return |
| similarity_threshold | 0.7 | Similarity threshold |
| max_tokens | 2000 | Maximum answer tokens |
| include_source | true | Whether to include source citation |

### Chunking Strategies

| Strategy | Use Case |
|----------|----------|
| Fixed Length | General scenarios |
| Semantic Chunking | Maintain semantic integrity |
| Paragraph Chunking | Split by natural paragraphs |

## Notes

1. **Document Quality**: Ensure documents are clear and well-formatted before upload
2. **Privacy Protection**: Be careful when uploading sensitive documents
3. **Knowledge Updates**: Re-upload documents when updated to refresh index
4. **Size Limit**: Single upload recommended not exceeding 50MB
5. **Index Delay**: Indexing takes ~1-5 minutes after upload

## Use Cases

- 🏢 **Enterprise Knowledge Management**: Employee handbooks, product docs, technical docs
- 📖 **Online Education**: Course materials, textbook Q&A
- 🛒 **E-commerce Customer Service**: Product FAQ, shopping guides
- 💼 **Legal Compliance**: Contract terms, regulations interpretation
- 🏥 **Healthcare**: Health guides, medication instructions

## Technical Implementation

### Core Components

```
knowledge_qa/
├── uploader.py          # Document upload module
├── parser.py           # Document parsing module
├── chunker.py          # Text chunking module
├── indexer.py          # Vector indexing module
├── retriever.py        # Retrieval module
└── generator.py        # Answer generation module
```

### API Usage Example

```python
# 1. Upload document
result = upload_document(file_path, knowledge_base_id)

# 2. Retrieve relevant knowledge
chunks = retrieve(query, top_k=5, threshold=0.7)

# 3. Generate answer
answer = generate_answer(question, context_chunks)
```

## Changelog

### v1.0.0 (2024-01-20)
- Initial release
- Support for PDF, Word, TXT, Markdown formats
- Vector retrieval and RAG Q&A implemented
- Source citation support

## Author Info

- Author: AI Agent Helper
- Version: 1.0.0
- Framework: OpenClaw
