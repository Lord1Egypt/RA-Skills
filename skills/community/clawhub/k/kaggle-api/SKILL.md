---
name: kaggle
description: |
  Kaggle API integration with managed authentication. Access datasets, models, competitions, and kernels.
  Use this skill when users want to search, download, or interact with Kaggle resources.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Kaggle

Access Kaggle datasets, models, competitions, and notebooks via managed API authentication.

## Quick Start

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/kaggle/v1/datasets.DatasetApiService/ListDatasets', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/kaggle/{native-api-path}
```

The gateway proxies requests to `api.kaggle.com` and automatically injects your credentials.

## Authentication

All requests require the Maton API key:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Kaggle connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=kaggle&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'kaggle'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

Open the returned `url` in a browser to complete authentication. Kaggle uses API key authentication - you'll need to provide your Kaggle username and API key from [kaggle.com/settings](https://www.kaggle.com/settings).

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

---

## API Reference

Kaggle uses an RPC-style API. All requests are POST with JSON body.

```
POST /kaggle/v1/{ServiceName}/{MethodName}
Content-Type: application/json
```

---

### Datasets

#### List Datasets

```bash
POST /kaggle/v1/datasets.DatasetApiService/ListDatasets
Content-Type: application/json

{}
```

**Request Body Parameters:**
- `search` - Search term (optional)
- `user` - Filter by username (optional)
- `pageSize` - Results per page (optional)
- `pageToken` - Pagination token (optional)

**Example with search:**
```json
{
  "search": "covid"
}
```

**Response:**
```json
{
  "datasets": [
    {
      "id": 9481458,
      "ref": "amar5693/screen-time-sleep-and-stress-analysis-dataset",
      "title": "Screen Time, Sleep & Stress Analysis Dataset",
      "subtitle": "ML-ready dataset analyzing smartphone usage and productivity.",
      "totalBytes": 787136,
      "downloadCount": 11659,
      "voteCount": 236,
      "usabilityRating": 1,
      "licenseName": "CC0: Public Domain",
      "ownerName": "Amar Tiwari",
      "tags": [...]
    }
  ]
}
```

#### Get Dataset

```bash
POST /kaggle/v1/datasets.DatasetApiService/GetDataset
Content-Type: application/json

{
  "ownerSlug": "amar5693",
  "datasetSlug": "screen-time-sleep-and-stress-analysis-dataset"
}
```

**Response:**
```json
{
  "id": 9481458,
  "title": "Screen Time, Sleep & Stress Analysis Dataset",
  "subtitle": "ML-ready dataset analyzing smartphone usage and productivity.",
  "totalBytes": 787136,
  "downloadCount": 11659,
  "usabilityRating": 1
}
```

#### List Dataset Files

```bash
POST /kaggle/v1/datasets.DatasetApiService/ListDatasetFiles
Content-Type: application/json

{
  "ownerSlug": "amar5693",
  "datasetSlug": "screen-time-sleep-and-stress-analysis-dataset"
}
```

**Response:**
```json
{
  "datasetFiles": [
    {
      "name": "Smartphone_Usage_Productivity_Dataset_50000.csv",
      "creationDate": "2026-02-13T06:56:19.803Z",
      "totalBytes": 2958561
    }
  ]
}
```

#### Get Dataset Metadata

```bash
POST /kaggle/v1/datasets.DatasetApiService/GetDatasetMetadata
Content-Type: application/json

{
  "ownerSlug": "amar5693",
  "datasetSlug": "screen-time-sleep-and-stress-analysis-dataset"
}
```

**Response:**
```json
{
  "info": {
    "datasetId": 9481458,
    "datasetSlug": "screen-time-sleep-and-stress-analysis-dataset",
    "ownerUser": "amar5693",
    "title": "Screen Time, Sleep & Stress Analysis Dataset",
    "description": "...",
    "totalViews": 44291,
    "totalVotes": 236,
    "totalDownloads": 11661
  }
}
```

#### Download Dataset

```bash
POST /kaggle/v1/datasets.DatasetApiService/DownloadDataset
Content-Type: application/json

{
  "ownerSlug": "amar5693",
  "datasetSlug": "screen-time-sleep-and-stress-analysis-dataset"
}
```

Returns binary data (ZIP file). Response headers:
- `Content-Type: application/zip`
- `Content-Length: <size in bytes>`

---

### Models

#### List Models

```bash
POST /kaggle/v1/models.ModelApiService/ListModels
Content-Type: application/json

{}
```

**Request Body Parameters:**
- `owner` - Filter by owner (optional)
- `search` - Search term (optional)
- `pageSize` - Results per page (optional)

**Example:**
```json
{
  "owner": "google"
}
```

**Response:**
```json
{
  "models": [
    {
      "id": 1,
      "owner": "google",
      "slug": "gemma",
      "title": "Gemma",
      "subtitle": "Gemma is a family of lightweight, state-of-the-art models",
      "instanceCount": 16,
      "framework": "transformers"
    }
  ]
}
```

#### Get Model

```bash
POST /kaggle/v1/models.ModelApiService/GetModel
Content-Type: application/json

{
  "ownerSlug": "google",
  "modelSlug": "gemma"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Gemma",
  "slug": "gemma",
  "owner": "google",
  "subtitle": "Gemma is a family of lightweight, state-of-the-art models",
  "publishTime": "2024-02-21T16:00:00Z",
  "instanceCount": 16
}
```

---

### Competitions

#### List Competitions

```bash
POST /kaggle/v1/competitions.CompetitionApiService/ListCompetitions
Content-Type: application/json

{}
```

**Request Body Parameters:**
- `search` - Search term (optional)
- `category` - Filter by category (optional)
- `pageSize` - Results per page (optional)

**Example:**
```json
{
  "search": "nlp"
}
```

**Response:**
```json
{
  "competitions": [
    {
      "id": 118448,
      "ref": "https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3",
      "title": "AI Mathematical Olympiad - Progress Prize 3",
      "url": "https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3",
      "deadline": "2026-06-06T23:59:00Z",
      "category": "Featured",
      "reward": "$1,048,576",
      "teamCount": 1234,
      "userHasEntered": false
    }
  ]
}
```

---

### Kernels (Notebooks)

#### List Kernels

```bash
POST /kaggle/v1/kernels.KernelsApiService/ListKernels
Content-Type: application/json

{}
```

**Request Body Parameters:**
- `search` - Search term (optional)
- `user` - Filter by username (optional)
- `language` - Filter by language: `python`, `r`, etc. (optional)
- `pageSize` - Results per page (optional)

**Example:**
```json
{
  "search": "titanic"
}
```

**Response:**
```json
{
  "kernels": [
    {
      "id": 5660537,
      "ref": "alexisbcook/titanic-tutorial",
      "title": "Titanic Tutorial",
      "author": "alexisbcook",
      "language": "Python",
      "totalVotes": 1234,
      "totalViews": 56789
    }
  ]
}
```

#### Get Kernel

```bash
POST /kaggle/v1/kernels.KernelsApiService/GetKernel
Content-Type: application/json

{
  "userName": "alexisbcook",
  "kernelSlug": "titanic-tutorial"
}
```

**Response:**
```json
{
  "metadata": {
    "id": 5660537,
    "ref": "alexisbcook/titanic-tutorial",
    "title": "Titanic Tutorial",
    "author": "alexisbcook",
    "language": "Python"
  }
}
```

---

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/kaggle/v1/datasets.DatasetApiService/ListDatasets',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ search: 'covid' })
  }
);
const data = await response.json();
console.log(data);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/kaggle/v1/datasets.DatasetApiService/ListDatasets',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'search': 'covid'}
)
print(response.json())
```

---

## Notes

- All API calls use POST method with JSON body
- API follows RPC pattern: `/v1/{ServiceName}/{MethodName}`
- Dataset refs use format: `{owner}/{dataset-slug}`
- Model refs use format: `{owner}/{model-slug}`
- Kernel refs use format: `{user}/{kernel-slug}`
- Download endpoints return binary data (ZIP files)
- Some operations require specific permissions (competition participation, kernel access)

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Invalid request parameters |
| 401 | Invalid or missing authentication |
| 403 | Permission denied |
| 404 | Resource not found |
| 429 | Rate limited |

## Resources

- [Kaggle API Documentation](https://www.kaggle.com/docs/api)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Kaggle Models](https://www.kaggle.com/models)
- [Kaggle Competitions](https://www.kaggle.com/competitions)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
