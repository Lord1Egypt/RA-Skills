# HTTP Requests and Binary Data

## Table of Contents
1. [httpRequest — full options reference](#1-httprequest-full-options)
2. [Query params, headers, body patterns](#2-common-patterns)
3. [Getting the full response (status + headers)](#3-full-response)
4. [Binary data — downloading files](#4-binary-data--downloading)
5. [Binary data — uploading files](#5-binary-data--uploading)
6. [Multipart form data](#6-multipart-form-data)
7. [Handling non-JSON responses](#7-non-json-responses)
8. [Streaming / large responses](#8-streaming)

---

## 1. httpRequest Full Options

```typescript
const response = await this.helpers.httpRequest({
  // ── Required ─────────────────────────────────────────────────
  method: 'POST',                        // GET | POST | PUT | PATCH | DELETE | HEAD
  url: 'https://api.example.com/items',  // full URL, OR use baseURL + url separately

  // ── Optional ─────────────────────────────────────────────────
  baseURL: 'https://api.example.com',    // if using relative url below
  // url: '/items',                       // relative path when baseURL is set

  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
    'X-Custom': 'value',
  },

  qs: {                                  // query string parameters
    page: 1,
    limit: 50,
    filter: 'active',
  },

  body: {                                // request body (auto-serialized if json: true)
    name: 'John',
    email: 'john@example.com',
  },

  // Response options
  returnFullResponse: false,             // true = { statusCode, headers, body }
                                         // false (default) = just the body

  // Ignore SSL certificate errors (use carefully)
  skipSslCertificateValidation: false,

  // Timeout in ms
  timeout: 30000,

  // Follow redirects
  followRedirects: true,
  maxRedirects: 10,

  // Proxy
  proxy: {
    host: 'proxy.example.com',
    port: 8080,
  },
});
```

---

## 2. Common Patterns

### GET with query params
```typescript
const response = await this.helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/users',
  headers: { Authorization: `Bearer ${token}` },
  qs: { limit: 50, status: 'active', cursor: 'abc123' },
});
```

### POST JSON body
```typescript
const response = await this.helpers.httpRequest({
  method: 'POST',
  url: 'https://api.example.com/users',
  headers: {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: { name: 'John', email: 'john@example.com' },
});
```

### POST with user-supplied JSON body
```typescript
const rawBody = this.getNodeParameter('body', i, '{}') as string;
let body: IDataObject;
try {
  body = JSON.parse(rawBody);
} catch {
  throw new NodeOperationError(this.getNode(), 'Body is not valid JSON', { itemIndex: i });
}

const response = await this.helpers.httpRequest({
  method: 'POST',
  url: 'https://api.example.com/items',
  headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
  body,
});
```

### PATCH / PUT (partial update)
```typescript
const response = await this.helpers.httpRequest({
  method: 'PATCH',
  url: `https://api.example.com/users/${userId}`,
  headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
  body: { email: 'newemail@example.com' },  // only fields to update
});
```

### DELETE
```typescript
await this.helpers.httpRequest({
  method: 'DELETE',
  url: `https://api.example.com/users/${userId}`,
  headers: { Authorization: `Bearer ${token}` },
});
```

---

## 3. Full Response

Get status code and headers alongside the body:

```typescript
const response = await this.helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/data',
  headers: authHeader,
  returnFullResponse: true,
}) as {
  statusCode: number;
  headers: Record<string, string>;
  body: unknown;
};

console.log(response.statusCode);        // 200
console.log(response.headers['x-rate-limit-remaining']); // rate limit info
const data = response.body;
```

---

## 4. Binary Data — Downloading

Receive a file from an API and pass it to the next node (e.g. for email attachment, Google Drive upload):

```typescript
import { BINARY_ENCODING } from 'n8n-workflow';

// Download file as buffer
const response = await this.helpers.httpRequest({
  method: 'GET',
  url: `https://api.example.com/files/${fileId}/download`,
  headers: { Authorization: `Bearer ${token}` },
  encoding: 'arraybuffer',              // ← get raw bytes
  returnFullResponse: true,
}) as { statusCode: number; headers: Record<string, string>; body: Buffer };

// Detect MIME type from Content-Type header
const contentType = response.headers['content-type'] || 'application/octet-stream';
const fileName    = response.headers['content-disposition']
  ?.match(/filename="?([^"]+)"?/)?.[1] ?? 'download';

// Attach binary to output item
const binaryData = await this.helpers.prepareBinaryData(
  response.body,
  fileName,
  contentType,
);

returnData.push({
  json: { fileName, contentType, size: response.body.length },
  binary: { data: binaryData },           // key 'data' is convention; can be anything
  pairedItem: { item: i },
});
```

Access in next nodes: `{{ $binary.data.fileName }}`, or use "Move Binary Data" node.

---

## 5. Binary Data — Uploading

Send a file that came from a previous node:

```typescript
// Get binary data from input item
const binaryPropertyName = this.getNodeParameter('binaryPropertyName', i, 'data') as string;
const binaryData = this.helpers.assertBinaryData(i, binaryPropertyName);

// Convert to buffer
const buffer = await this.helpers.getBinaryDataBuffer(i, binaryPropertyName);

// Upload as raw binary body
const response = await this.helpers.httpRequest({
  method: 'POST',
  url: 'https://api.example.com/files/upload',
  headers: {
    Authorization: `Bearer ${token}`,
    'Content-Type': binaryData.mimeType,
    'Content-Disposition': `attachment; filename="${binaryData.fileName}"`,
  },
  body: buffer,
});
```

---

## 6. Multipart Form Data

For file uploads where the API expects `multipart/form-data`:

```typescript
import FormData from 'form-data';

const binaryData = this.helpers.assertBinaryData(i, 'data');
const buffer     = await this.helpers.getBinaryDataBuffer(i, 'data');

const formData = new FormData();
formData.append('file', buffer, {
  filename:    binaryData.fileName ?? 'upload',
  contentType: binaryData.mimeType,
});
formData.append('title', this.getNodeParameter('title', i) as string);
formData.append('folder_id', this.getNodeParameter('folderId', i) as string);

const response = await this.helpers.httpRequest({
  method: 'POST',
  url: 'https://api.example.com/files',
  headers: {
    Authorization: `Bearer ${token}`,
    ...formData.getHeaders(),           // ← sets Content-Type: multipart/form-data; boundary=...
  },
  body: formData,
});
```

Add to `package.json` dependencies: `"form-data": "^4.0.0"`

---

## 7. Non-JSON Responses

```typescript
// Plain text response
const response = await this.helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/data.csv',
  headers: authHeader,
  // No Content-Type: application/json → response is returned as string
});
// response is a string

// XML response — parse manually
const xml2js = require('xml2js');
const parsed = await xml2js.parseStringPromise(response as string, { explicitArray: false });

// Return raw text as a field
returnData.push({
  json: { raw: response as string },
  pairedItem: { item: i },
});
```

---

## 8. Streaming / Large Responses

For very large responses, use Node.js streams via `request` helper (lower level):

```typescript
const stream = await this.helpers.httpRequestWithAuthentication.call(
  this,
  'myCredential',
  {
    method: 'GET',
    url: 'https://api.example.com/large-file',
    encoding: null,
    resolveWithFullResponse: true,
  },
);

// Or use prepareBinaryData with a stream
const binaryData = await this.helpers.prepareBinaryData(
  stream.body as Buffer,
  'large-file.bin',
  'application/octet-stream',
);
```

> For most file downloads under ~100MB, `encoding: 'arraybuffer'` (section 4) is simpler and sufficient.
