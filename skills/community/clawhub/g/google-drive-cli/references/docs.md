# Google Docs Operations

Use `drivectl` to create, read, and manage Google Docs.

## Exporting Google Docs to Markdown

To extract the content of a Google Doc as Markdown (which accurately parses the document AST):
```bash
drivectl get <google-doc-id> --format md
```

To save the exported Markdown directly to a file:
```bash
drivectl get <google-doc-id> --format md -o output.md
```

## Creating Google Docs from Markdown

To convert a local Markdown file into a richly formatted Google Doc:
```bash
drivectl docs create "Document Title" path/to/document.md -O json
```
This will output JSON containing the new Document ID and a link to the created document.

## Exploring Document Structure

To view the structural hierarchy of tabs within a Google Doc:
```bash
drivectl docs tabs <document-id> -O json
```
