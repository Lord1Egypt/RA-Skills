# Public tool contracts

HTTP base URL: `https://aihub-admin.aimix.pro/api-platform/v1`.

MCP Streamable HTTP endpoint: `POST /mcp`.

Authenticate with `Authorization: Bearer <PIXMIND_API_KEY>`. Keep the key outside model context and chat.

## Pixmind Builder secure transport

Pixmind Builder exposes `pixmind_api_request`. It obtains the credential from **Settings → Providers → Pixmind**, adds the authorization header internally, and accepts only the content-engine MCP Tools listed below plus task-status reads. The Skill must not inspect operating-system environment variables or forward credentials through a shell.

External hosts without this Tool may authenticate directly with `PIXMIND_API_KEY` stored in their process environment.

## MCP content Tools

- `content_create_project`
- `content_get_project`
- `content_generate_outline`
- `content_generate_article`
- `content_review_article`
- `content_generate_images`
- `content_render_wechat`

The normal Skill workflow does not call any `wechat_*` Tool.

## Content endpoints used by this Skill

- `POST /content/projects`: accept `clientRequestId` and `brief`; return a project at revision 1.
- `GET /content/projects/{projectId}`: return the owned project's public artifacts and status.
- `POST /content/projects/{projectId}/outline`: accept `expectedRevision` and `idempotencyKey`.
- `POST /content/projects/{projectId}/article`: require an existing outline.
- `POST /content/projects/{projectId}/review`: require an existing article.
- `POST /content/projects/{projectId}/images`: create paid cover and inline image tasks; poll each through `/tasks/{taskId}`.
- `POST /content/projects/{projectId}/render`: create the versioned article manifest with WeChat-compatible inline styles. Images are optional; pass an empty `coverUrl` and `inlineAssets` when generating a text-only article. Supported themes are `classic`, `graphite`, `maple`, `mint`, `sunrise`, `lake`, `newspaper`, `forest`, `minimal`, `editorial`, `ink`, `warm`, and `techno`. Supported layouts are `balanced`, `compact`, `airy`, and `magazine`.

Every successful mutation increments `revision`. Always query the project after an interrupted or unknown request before deciding whether another paid mutation is necessary.

## Public project fields

`projectId`, `revision`, `status`, `currentStep`, `brief`, `outline`, `article`, `review`, `images`, `manifest`, `error`, `createdAt`, and `updatedAt` are public.

## Optional publisher service

The backend retains account, draft, and publish endpoints for separately approved server integrations. This Skill does not call those endpoints. Its normal completion path is `content_render_wechat` followed by the local `copy.rich-text` action.

The service never returns internal prompts, prompt versions, model routing, scoring weights, provider errors, or chain-of-thought.

## Stable errors

- `CONTENT_AUTH_REQUIRED`
- `CONTENT_PROJECT_NOT_FOUND`
- `CONTENT_BRIEF_INVALID`
- `CONTENT_REVISION_INVALID`
- `CONTENT_REVISION_CONFLICT`
- `CONTENT_IDEMPOTENCY_KEY_INVALID`
- `CONTENT_IDEMPOTENCY_CONFLICT`
- `CONTENT_OPERATION_IN_PROGRESS`
- `CONTENT_OUTLINE_REQUIRED`
- `CONTENT_ARTICLE_REQUIRED`
- `CONTENT_OUTPUT_REJECTED`
- `CONTENT_GENERATION_FAILED`
- `CREDITS_INSUFFICIENT`
