# Google Drive (Maton Gateway) – cURL Guide

Access the Google Drive API with managed OAuth authentication using cURL.

---

## 🔹 Base URL

https://gateway.maton.ai/google-drive/{native-api-path}


---

## 🔹 Authentication

All requests require your API key:

```bash
export MATON_API_KEY="YOUR_API_KEY"
Header:

Authorization: Bearer $MATON_API_KEY
🚀 Quick Start
List Files
curl -X GET "https://gateway.maton.ai/google-drive/drive/v3/files?pageSize=10" \
  -H "Authorization: Bearer $MATON_API_KEY"
🔗 Connection Management
List Connections
curl -X GET "https://ctrl.maton.ai/connections?app=google-drive&status=ACTIVE" \
  -H "Authorization: Bearer $MATON_API_KEY"
Create Connection
curl -X POST "https://ctrl.maton.ai/connections" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"app": "google-drive"}'
Get Connection
curl -X GET "https://ctrl.maton.ai/connections/{connection_id}" \
  -H "Authorization: Bearer $MATON_API_KEY"
Delete Connection
curl -X DELETE "https://ctrl.maton.ai/connections/{connection_id}" \
  -H "Authorization: Bearer $MATON_API_KEY"
Specify Connection
curl -X GET "https://gateway.maton.ai/google-drive/drive/v3/files?pageSize=10" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Maton-Connection: CONNECTION_ID"
📁 File Operations
List Files
curl -X GET "https://gateway.maton.ai/google-drive/drive/v3/files?pageSize=10" \
  -H "Authorization: Bearer $MATON_API_KEY"
Search Files
curl -G "https://gateway.maton.ai/google-drive/drive/v3/files" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  --data-urlencode "q=name contains 'report'" \
  --data-urlencode "pageSize=10"
Only Folders
curl -G "https://gateway.maton.ai/google-drive/drive/v3/files" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  --data-urlencode "q=mimeType='application/vnd.google-apps.folder'"
Files in Folder
curl -G "https://gateway.maton.ai/google-drive/drive/v3/files" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  --data-urlencode "q='FOLDER_ID' in parents"
Select Fields
curl -g "https://gateway.maton.ai/google-drive/drive/v3/files?fields=files(id,name,mimeType,createdTime,modifiedTime,size)" \
  -H "Authorization: Bearer $MATON_API_KEY"
Get File Metadata
curl -X GET "https://gateway.maton.ai/google-drive/drive/v3/files/{fileId}?fields=id,name,mimeType,size,createdTime" \
  -H "Authorization: Bearer $MATON_API_KEY"
Download File
curl -X GET "https://gateway.maton.ai/google-drive/drive/v3/files/{fileId}?alt=media" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -o file.bin
Export Google Docs (PDF)
curl -X GET "https://gateway.maton.ai/google-drive/drive/v3/files/{fileId}/export?mimeType=application/pdf" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -o file.pdf
✏️ Create & Update
Create File
curl -X POST "https://gateway.maton.ai/google-drive/drive/v3/files" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Document",
    "mimeType": "application/vnd.google-apps.document"
  }'
Create Folder
curl -X POST "https://gateway.maton.ai/google-drive/drive/v3/files" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Folder",
    "mimeType": "application/vnd.google-apps.folder"
  }'
Update Metadata
curl -X PATCH "https://gateway.maton.ai/google-drive/drive/v3/files/{fileId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Renamed File"}'
Move File
curl -X PATCH "https://gateway.maton.ai/google-drive/drive/v3/files/{fileId}?addParents=NEW_FOLDER_ID&removeParents=OLD_FOLDER_ID" \
  -H "Authorization: Bearer $MATON_API_KEY"
Delete File
curl -X DELETE "https://gateway.maton.ai/google-drive/drive/v3/files/{fileId}" \
  -H "Authorization: Bearer $MATON_API_KEY"
Copy File
curl -X POST "https://gateway.maton.ai/google-drive/drive/v3/files/{fileId}/copy" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Copy of File"}'
⬆️ Uploads
Simple Upload (≤5MB)
curl -X POST "https://gateway.maton.ai/google-drive/upload/drive/v3/files?uploadType=media" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: text/plain" \
  --data-binary @file.txt
Multipart Upload
curl -X POST "https://gateway.maton.ai/google-drive/upload/drive/v3/files?uploadType=multipart" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: multipart/related; boundary=boundary" \
  --data-binary $'--boundary\r
Content-Type: application/json; charset=UTF-8\r
\r
{"name": "myfile.txt", "description": "My file"}\r
--boundary\r
Content-Type: text/plain\r
\r
Hello file content\r
--boundary--'
Resumable Upload
Step 1: Start Session
curl -i -X POST "https://gateway.maton.ai/google-drive/upload/drive/v3/files?uploadType=resumable" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json; charset=UTF-8" \
  -H "X-Upload-Content-Type: application/octet-stream" \
  -H "X-Upload-Content-Length: <FILE_SIZE>" \
  -d '{"name": "large_file.bin"}'
Step 2: Upload File
curl -X PUT "<UPLOAD_URL>" \
  -H "Content-Length: <FILE_SIZE>" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @large_file.bin
Update File Content
curl -X PATCH "https://gateway.maton.ai/google-drive/upload/drive/v3/files/{fileId}?uploadType=media" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: text/plain" \
  --data-binary @file.txt
🔐 Sharing
curl -X POST "https://gateway.maton.ai/google-drive/drive/v3/files/{fileId}/permissions" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "reader",
    "type": "user",
    "emailAddress": "user@example.com"
  }'
🧠 Query Examples
name contains 'report'
mimeType = 'application/pdf'
'folderId' in parents
trashed = false
modifiedTime > '2024-01-01T00:00:00'
⚠️ Notes
Use -G for query parameters

Use --data-binary for file uploads

Use -o to save files

Use curl -g when URL contains brackets

Pagination uses nextPageToken

❗ Error Codes
Status	Meaning
400	Missing Google Drive connection
401	Invalid API key
429	Rate limited
4xx/5xx	Google API error
🔧 Troubleshooting
Check API Key
echo $MATON_API_KEY
Test Connection
curl -X GET "https://ctrl.maton.ai/connections" \
  -H "Authorization: Bearer $MATON_API_KEY"
📌 Important
✔ Correct:

https://gateway.maton.ai/google-drive/drive/v3/files
❌ Incorrect:

https://gateway.maton.ai/drive/v3/files