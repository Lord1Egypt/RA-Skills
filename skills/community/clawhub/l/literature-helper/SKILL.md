---
name: literature-helper
description: literature retrieval and single-pdf analysis for academic research. use when the user asks to find papers by topic, author, keyword, or latest papers in the last five years; when the user wants bilingual search terms; when the user uploads a single pdf and asks for keywords, summary, methods, findings, limitations, or question answering grounded in the pdf.
---

# Literature Helper

## Literature retrieval

When the user asks for literature on a topic, author, keyword, research field, or latest papers:

1. Identify:
   - topic
   - optional author
   - optional time range
   - optional language preference

2. If the user asks for "latest literature" but gives no time range, default to the last 5 years.

3. Generate:
   - Chinese keywords
   - English keywords
   - 2 to 4 useful search strings

4. Search for relevant papers and return a structured result list.

5. For each result, include:
   - title
   - authors
   - year
   - source or journal
   - one-sentence summary
   - link
   - availability label:
     - open access
     - repository pdf
     - abstract only
     - availability unconfirmed

6. Never claim full-text availability unless it is actually confirmed.

## Single PDF analysis

When the user uploads one PDF:

1. Extract:
   - title
   - keywords
   - research question
   - methods
   - data or materials
   - main findings
   - conclusion
   - limitations

2. Then give a clear Chinese summary unless the user asks for another language.

3. If the user asks questions about the PDF:
   - answer primarily from the PDF
   - if the answer is not found in the PDF, say clearly that it was not found in the document
   - do not invent details

## Output style

For literature retrieval, use:

### Search terms
- Chinese:
- English:
- Suggested search strings:

### Results
1. Title
   - Authors:
   - Year:
   - Source:
   - Summary:
   - Link:
   - Availability:

For PDF analysis, use:

### Basic information
### Keywords
### Research question
### Methods
### Data or materials
### Main findings
### Conclusion
### Limitations
### Answers to user questions

## Reliability rules

- Be explicit about uncertainty.
- Never fabricate paper links, authors, journals, or availability.
- Distinguish clearly between:
  - open access direct pdf
  - repository version
  - abstract page only
  - unconfirmed access