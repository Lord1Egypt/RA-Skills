# Product Image Design — Response Schema

## Common envelope

`status` `1` = success; `code` `2001` = invalid Token, `2002` = insufficient credits; `data` = payload.

## GET /aigc/ec_product_media/platform_options

Array of `{ code, name, regions: [{ code, name }] }`.

## POST /aigc/ec_media/image/create

Extra fields vs general image create: `target_platform` (required), `image_scene`, `region`.

## GET /aigc/ec_media/image/create/logs/product

Same pagination as `/logs`; `items[].param` includes `image_scene`, `target_platform`, `region`.
