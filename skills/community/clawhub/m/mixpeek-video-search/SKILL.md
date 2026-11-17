---
name: mixpeek-video-search
description: Find the exact moment in video, images or audio by describing it, using Mixpeek. Use when the user wants to search inside their own video library, find a scene or clip by description, get start and end times for a moment, or index media from a URL or object storage so it becomes searchable.
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - MIXPEEK_API_KEY
    primaryEnv: MIXPEEK_API_KEY
    emoji: "🎞️"
    homepage: https://mixpeek.com
    links:
      homepage: https://mixpeek.com
      documentation: https://mixpeek.com/docs
      signup: https://mixpeek.com/start?utm_source=clawhub
---

# Mixpeek video search

Mixpeek indexes video, images, audio and documents and lets you search them by describing what you want. A video is split into scenes, and each scene becomes a searchable document with a start and end time, so a search lands on the moment, not just the file.

Three objects matter:

- **Bucket**: where the source files go (by URL or from S3, GCS and similar storage).
- **Collection**: processes a bucket into searchable documents (scene splitting, embeddings, transcripts).
- **Retriever**: a saved search over one or more collections. You execute it with inputs such as a text query.

Everything lives in a **namespace**, sent as the `X-Namespace` header.

## Try it first, no API key needed

A public retriever over a small sample of stock footage answers without authentication:

```bash
curl -s -X POST https://api.mixpeek.com/v1/public/retrievers/footage-intelligence-sample/execute \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"query": "waterfall from above"}}'
```

Each item in `results` has `title`, `start_time`, `end_time` (seconds) and `score`. The top result for this query is a drone shot of a forest waterfall, 19.0 to 20.5 seconds in.

## Setup for your own media

1. Create an account and an API key: https://mixpeek.com/start?utm_source=clawhub (Studio, Settings, API Keys).
2. Set the key:
   ```bash
   export MIXPEEK_API_KEY="your-api-key"
   ```

All snippets below use this helper (Python 3.10+, standard library only):

```python
import json, os, time, urllib.request

API = "https://api.mixpeek.com"

def mx(method, path, body=None, ns=None):
    headers = {"Authorization": f"Bearer {os.environ['MIXPEEK_API_KEY']}", "Content-Type": "application/json"}
    if ns:
        headers["X-Namespace"] = ns
    req = urllib.request.Request(API + path, method=method, headers=headers,
                                 data=json.dumps(body).encode() if body is not None else None)
    return json.load(urllib.request.urlopen(req, timeout=300))
```

## Index a video and search it

```python
ns = mx("POST", "/v1/namespaces", {"namespace_name": "my-video-search"})["namespace_id"]

# New namespaces start with a $0.00 daily budget, and processing runs models,
# so set a cap first. Without it the batch fails even though trigger says "Accepted".
mx("PATCH", f"/v1/namespaces/{ns}", {"spend_budget": {"daily_usd": 1, "monthly_usd": 5}})

bucket = mx("POST", "/v1/buckets", {"bucket_name": "videos",
            "bucket_schema": {"properties": {"video": {"type": "video"}}}}, ns)["bucket_id"]
col = mx("POST", "/v1/collections", {"collection_name": "video-scenes",
         "source": {"type": "bucket", "bucket_ids": [bucket]},
         "features": ["video_search"]}, ns)["collection_id"]

mx("POST", f"/v1/buckets/{bucket}/objects", {"blobs": [{"property": "video", "type": "video",
   "data": "https://mixpeek-public-demo.s3.us-east-2.amazonaws.com/gtm/05-s3-files-reel.mp4"}]}, ns)
task = mx("POST", f"/v1/collections/{col}/trigger", {}, ns)["task_id"]

while True:  # wait for a terminal status; COMPLETED_WITH_ERRORS is terminal too
    status = mx("GET", f"/v1/tasks/{task}", ns=ns)["status"]
    if status in ("COMPLETED", "COMPLETED_WITH_ERRORS", "FAILED"):
        break
    time.sleep(15)
print("processing:", status)
```

Then create a retriever and search:

```python
collection = mx("GET", f"/v1/collections/{col}", ns=ns)
feature_uri = collection["vector_indexes"][0]["feature_uri"]   # the embedding the collection produced

ret = mx("POST", "/v1/retrievers", {"retriever_name": "find-moments",
         "collection_identifiers": [col],
         "input_schema": {"query": {"type": "text", "required": True}},
         "stages": [{"stage_name": "search", "stage_type": "filter", "config": {
             "stage_id": "feature_search", "parameters": {
                 "searches": [{"feature_uri": feature_uri,
                               "query": {"input_mode": "text", "value": "{{INPUT.query}}"}, "top_k": 50}],
                 "final_top_k": 10}}}]}, ns)
ret = ret.get("retriever", ret)["retriever_id"]

for d in mx("POST", f"/v1/retrievers/{ret}/execute", {"inputs": {"query": "files uploading to a storage bucket"}}, ns)["documents"]:
    start = d.get("start_time_s", d.get("start_time"))   # seconds; field name depends on the pipeline
    end = d.get("end_time_s", d.get("end_time"))
    print(round(d["score"], 3), start, end, (d.get("description") or "")[:80])
```

## Notes for the agent

- Scene times are seconds, in `start_time_s` and `end_time_s` for collections created with `features`, and `start_time` and `end_time` in some older pipelines such as the public sample. Report each match with its start and end time and score. Say plainly when nothing scored well instead of stretching a weak match.
- Processing a short clip takes a minute or two; long videos take longer. Poll the task; do not re-trigger while it runs.
- Results per call come from the retriever's `final_top_k`; set it there.
- To index files already in S3 or GCS, create a storage connection and a bucket sync instead of uploading by URL: https://mixpeek.com/docs/integrations/object-storage/overview
- Mixpeek also runs an MCP server for agents that speak MCP: https://mixpeek.com/docs/integrations/developer-tools/mcp-server
