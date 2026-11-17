# Handheld Product Video — Response Schema

## GET /aigc/ec_product_video/image/create/avatar_options

`data.items[]`: `{ id, imageThumb, ... }`; pagination: `count`, `more`, `start`.

## POST /aigc/ec_product_video/image/create

Required: `avatarId`, `model`, `ratio`, `size`. Optional: `prompt`, `images`.

WebSocket: `product_video_image_result_refresh` → `data.images[]` candidate URLs.

## POST /aigc/ec_product_video/text_create

Returns script string in `data`.

## POST /aigc/ec_product_video/video/create

`create_mode` always `1`; `attaches[0]` = first frame URL (required).

## GET /aigc/ec_product_video/video/create/logs

`items[].url` = output video.

## WebSocket

- `product_video_image_result_refresh` — first-frame candidates
- `video_result_refresh` — refresh video logs
