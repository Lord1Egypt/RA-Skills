# Kling AI — API reference


| Subcommand | Endpoints                                                                                                                                                            |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `video`    | `POST/GET /v1/videos/text2video`, `POST/GET /v1/videos/image2video`, `POST/GET /v1/videos/omni-video`                                                                |
| `image`    | `POST/GET /v1/images/generations`, `POST/GET /v1/images/omni-image`                                                                                                  |
| `element`  | `POST/GET /v1/general/advanced-custom-elements`, `GET /v1/general/advanced-presets-elements`, `POST /v1/general/delete-elements`                                     |
| `account`  | `GET /account/costs` (quota/resource packs); bind flow (no Bearer, bind base): `POST /console/api/auth/skill/init-sessions`, `POST /console/api/auth/skill/exchange` |


Auth and polling notes:

- Business APIs (`/v1/...` + `/account/costs`) use Bearer token (JWT from `~/.config/kling/.credentials`, or session `KLING_TOKEN`).
- Bind APIs (`/console/api/auth/skill/...`) are device-bind endpoints and do not use Bearer.
- Submit APIs return `task_id`; polling uses `GET {submit_path}/{task_id}` until `succeed`/`failed`, then read result URLs from `task_result`/`output`.

Account mode mapping:

- `account --costs`: remote call to `GET /account/costs`
- `account --bind` / `account --bind-url`: remote bind calls (`init-sessions` + `exchange`)
- `account --import-env` / `--import-credentials` / `--configure`: local credential operations only (no business API submit)

## Model docs

Official docs (use as primary source; paths may vary by locale):

- [Developer docs home (CN)](https://app.klingai.com/cn/dev/document-api)
- [Developer docs home (Global)](https://kling.ai/document-api/quickStart/productIntroduction/overview)
- Use the navigation from the Global/CN docs home to open model pages for video/image/omni in the current site structure.

