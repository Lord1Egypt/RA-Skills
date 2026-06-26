# Hitem3D API Reference

## Base URL
`https://api.hitem3d.ai`

## Authentication Flow
1. Get token: `POST /open-api/v1/auth/token` with Basic Auth (base64 of `client_id:client_secret`)
2. Use returned `accessToken` as `Bearer` token for all subsequent calls

## Endpoints

### Get Token
- `POST /open-api/v1/auth/token`
- Auth: `Authorization: Basic base64(ak:sk)`
- Response: `{ code: 200, data: { accessToken, tokenType, nonce } }`

### Create Task
- `POST /open-api/v1/submit-task`
- Auth: `Bearer <accessToken>`
- Content-Type: `multipart/form-data`
- Parameters:
  - `request_type` (int, required): 1=mesh only, 2=texture on existing mesh, 3=both (default)
  - `model` (string, required): hitem3dv1.5, hitem3dv2.0, scene-portraitv1.5, scene-portraitv2.0, scene-portraitv2.1
  - `images` (file): Single image (png/jpeg/jpg/webp, max 20MB)
  - `multi_images` (file): Multi-view images (max 4: front/back/left/right)
  - `multi_images_bit` (string): Bitmap for multi-view (e.g. "1010" = front+left)
  - `resolution` (string): 512, 1024, 1536 (default), 1536pro
  - `format` (int): 1=obj, 2=glb, 3=stl, 4=fbx, 5=usdz
  - `face` (int): Face count 100000-2000000
  - `mesh_url` / `mesh` (string/file): For request_type=2 (staged texture)
  - `callback_url` (string): Webhook for status updates
- Note: v2.0 models don't support request_type=2

### Query Task
- `GET /open-api/v1/query-task?task_id=<id>`
- Auth: `Bearer <accessToken>`
- Response states: created, queueing, processing, success, failed
- On success: `data.url` (model download, 1h expiry), `data.cover_url` (preview image)

### Query Balance
- `GET /open-api/v1/balance`
- Auth: `Bearer <accessToken>`
- Response: `{ data: { totalBalance: <decimal> } }`

## Credit Consumption
| Model | Resolution | Textured | Credits | USD |
|-------|-----------|----------|---------|-----|
| v2.0 | 1536³ | No | 40 | $0.80 |
| v2.0 | 1536³ | Yes | 50 | $1.00 |
| v2.0 | 1536Pro³ | No | 60 | $1.20 |
| v2.0 | 1536Pro³ | Yes | 70 | $1.40 |
| v1.5 | 512³ | No | 5 | $0.10 |
| v1.5 | 512³ | Yes | 15 | $0.30 |
| v1.5 | 1024³ | No | 10 | $0.20 |
| v1.5 | 1024³ | Yes | 20 | $0.40 |
| v1.5 | 1536³ | No | 40 | $0.80 |
| v1.5 | 1536³ | Yes | 50 | $1.00 |
| Portrait v2.0/v2.1 | 1536Pro³ | Yes | 70 | $1.40 |

## Error Codes
- 40010000: Invalid client credentials
- 50010001: Generation failed (credits refunded)
- 10000000: Internal server error
