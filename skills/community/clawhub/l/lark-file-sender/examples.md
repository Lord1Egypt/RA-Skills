# Feishu File Sender - Usage Examples

## Example 1: Send a PDF Report

**User:** Send this report to me on Feishu
**File:** `/workspace/quarterly_report.pdf`

**Response:**
```python
message action=send filePath="/workspace/quarterly_report.pdf" message="Here's your quarterly report"
```

## Example 2: Send Multiple Generated Files

**User:** Send all the files I just created
**Files:** `/workspace/output/file1.pdf`, `/workspace/output/file2.xlsx`

**Response:**
```python
message action=send filePath="/workspace/output/file1.pdf" message="File 1 of 2"
message action=send filePath="/workspace/output/file2.xlsx" message="File 2 of 2"
```

## Example 3: Send with Custom Message

**User:** Share this document with the team
**File:** `/workspace/project_spec.md`

**Response:**
```python
message action=send filePath="/workspace/project_spec.md" message="Project specification document - please review"
```

## Example 4: Send to Specific User

**User:** Send this to user ou_abc123
**File:** `/workspace/invoice.pdf`

**Response:**
```python
message action=send target="user:ou_abc123" filePath="/workspace/invoice.pdf" message="Invoice for this month"
```

## Example 5: Batch Send After Processing

**User:** Generate and send all CSV files

**Workflow:**
```python
# Generate files
exec command="python generate_csvs.py --output /workspace/csvs/"

# Send each file
files = ["/workspace/csvs/data1.csv", "/workspace/csvs/data2.csv", "/workspace/csvs/data3.csv"]
for file in files:
    message action=send filePath=file
```

## Common File Types

| Extension | Type | Example |
|-----------|------|---------|
| .pdf | Document | Reports, invoices |
| .docx | Word | Contracts, letters |
| .xlsx | Excel | Data, spreadsheets |
| .jpg, .png | Image | Screenshots, photos |
| .zip | Archive | Bundled files |
| .mp4 | Video | Recordings |
