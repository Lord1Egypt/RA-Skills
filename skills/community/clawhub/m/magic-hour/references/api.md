# Magic Hour raw HTTP reference

Base URL: `https://api.magichour.ai/v1`. Auth header: `Authorization: Bearer $MAGIC_HOUR_API_KEY`. All bodies are JSON.

## Create jobs

| Endpoint | Body | Returns |
|---|---|---|
| `POST /v1/text-to-video` | `{name, model, end_seconds, resolution: "480p"\|"720p"\|"1080p", aspect_ratio?: "16:9"\|"9:16"\|"1:1", audio?: bool, style: {prompt}}` | `{id, credits_charged}` |
| `POST /v1/image-to-video` | `{name, model, end_seconds, resolution, style: {prompt}, assets: {image_file_path}}` | `{id}` |
| `POST /v1/ai-image-generator` | `{name, model, image_count, aspect_ratio?, style: {prompt}}` | `{id}` |

`assets.image_file_path` accepts either a public `https://` URL or a `file_path` returned by the upload flow below.

## Poll

`GET /v1/video-projects/{id}` or `GET /v1/image-projects/{id}` ->
`{id, status: "queued"|"rendering"|"complete"|"error"|"canceled", downloads: [{url, expires_at}], credits_charged, width, height, fps, error}`

Poll every ~5 seconds until `status` is `complete` or `error`. Failed jobs auto-refund credits.

## Upload a local image

1. `POST /v1/files/upload-urls` body `{"items":[{"extension":"png","type":"image"}]}` -> `{items:[{upload_url, file_path}]}`
2. `PUT` the raw bytes to `upload_url`.
3. Use `file_path` as `assets.image_file_path`.

## curl example

```bash
ID=$(curl -s https://api.magichour.ai/v1/text-to-video \
  -H "Authorization: Bearer $MAGIC_HOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{"name":"demo","model":"wan-2.2","end_seconds":5,"resolution":"480p","aspect_ratio":"16:9","style":{"prompt":"a corgi surfing at sunset"}}' | jq -r .id)
until curl -s https://api.magichour.ai/v1/video-projects/$ID -H "Authorization: Bearer $MAGIC_HOUR_API_KEY" | jq -e '.status=="complete" or .status=="error"' >/dev/null; do sleep 5; done
curl -s https://api.magichour.ai/v1/video-projects/$ID -H "Authorization: Bearer $MAGIC_HOUR_API_KEY" | jq '{status, url: .downloads[0].url, credits_charged}'
```

## Python SDK equivalents (magic_hour >= 0.75)

```python
from magic_hour import Client
client = Client(token=os.environ["MAGIC_HOUR_API_KEY"])
r = client.v1.text_to_video.generate(end_seconds=5, style={"prompt": "..."}, model="wan-2.2",
        resolution="480p", aspect_ratio="16:9", wait_for_completion=True, download_outputs=False)
r.id, r.status, r.downloads[0].url, r.credits_charged
client.v1.image_to_video.generate(assets={"image_file_path": "photo.png"}, end_seconds=5, style={"prompt": "..."}, model="kling-3.0", resolution="720p")
client.v1.ai_image_generator.generate(image_count=1, style={"prompt": "..."}, model="default", aspect_ratio="1:1")
```
Pass `model` as a plain string; the SDK's Literal types lag the live catalogue.
