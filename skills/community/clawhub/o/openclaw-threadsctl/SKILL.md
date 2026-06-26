---
name: openclaw-threadsctl
description: Manage Threads accounts, OAuth connect URLs, drafts, and publishing through the local threadsctl CLI. Use when the user wants to post to Threads, create or publish drafts, connect accounts, inspect stats, or work with image, carousel, or spoiler media posts.
---

# OpenClaw Threads via threadsctl

Use `threadsctl` as the default interface for Threads operations.

This skill is model-agnostic. It can be used with `OpenAI Codex`, `Gemini`, or another OpenClaw text provider. Optional image generation providers are separate from Threads publishing.

Source: https://clawhub.ai/dladislav201/openclaw-threadsctl

## Prerequisites

- `threadsctl` is installed and available in `PATH`.
- `THREADS_SERVICE_URL` and `THREADS_SERVICE_API_KEY` are configured for the CLI.
- At least one working OpenClaw text model is configured.
- Optional: an image generation provider such as `Gemini` if the user wants help creating images before posting.
- Run `threadsctl` from `/opt/threads-service-ts/threads-service` on the server where the service is deployed.

## Use When

- The user wants to publish to Threads.
- The user wants to create, approve, or publish a draft.
- The user wants to connect a Threads account.
- The user wants to inspect accounts, stats, drafts, or published posts.
- The user wants to publish a text, single-image, multi-photo carousel, or spoiler media post.
- The user would otherwise need raw `curl` or direct HTTP requests.

## Rules

1. Prefer `threadsctl` over raw `curl` or manual HTTP requests.
2. Support both workflows: direct publish and draft-first.
3. If the user says "post now", use direct publish.
4. If the user says "draft", "prepare", "queue", or wants review first, use draft flow.
5. If the account is unclear, ask which account label or ID to use.
6. Prefer account labels over raw account IDs when communicating with the user.
7. Use `--confirmed` only when the user clearly intends immediate publishing.
8. Show concise summaries of results and include IDs only when useful.
9. If a command fails, surface the real error and explain the likely next step.
10. If the user wants a new image created, handle image generation separately before publishing.
11. Prefer `--file` for images generated locally by OpenClaw under `/root/.openclaw/media/...`.
12. Use `--media-url` only when the image is already hosted at a reachable public URL.
13. For multiple local images, use `--files <path1,path2>` with `publish carousel`.
14. Use `--spoiler` only when the user wants media blurred as a spoiler. For carousel posts, spoiler applies to all attached media.
15. Run `threadsctl` commands from `/opt/threads-service-ts/threads-service` so the deployed wrapper and Docker setup are used.

## New Media Features

### Multi-photo Posts

The service supports Threads carousel posts for publishing multiple photos in one post.

- Use `threadsctl publish carousel` for immediate publishing.
- Use `threadsctl draft create --type carousel` for draft-first publishing.
- A carousel must contain 2 to 20 image URLs or local image files.
- Use `--media-urls "url1,url2"` when the images are already hosted and reachable by Threads.
- Use `--files "path1,path2"` when the images are local files available inside the deployed service/container.
- Do not publish multiple photos by sending several `publish image` commands unless the user explicitly wants separate posts.

Examples:

```bash
cd /opt/threads-service-ts/threads-service
threadsctl publish carousel --account main-brand --media-urls "https://example.com/1.jpg,https://example.com/2.jpg" --text "Photo dump" --confirmed
threadsctl publish carousel --account main-brand --files "/root/.openclaw/media/one.jpg,/root/.openclaw/media/two.jpg" --text "Photo dump" --confirmed
```

### Photo Spoilers

The service supports Threads media spoilers for image and carousel posts.

- Add `--spoiler` when the user asks for the photo/media to be blurred, hidden, marked as spoiler, or covered until tapped.
- `--spoiler` works with `publish image`, `publish carousel`, and media drafts.
- Do not use `--spoiler` for text-only posts.
- For carousel posts, `--spoiler` applies to every photo in the carousel. Threads API does not let this service mark only one photo in the carousel as spoiler.

Examples:

```bash
cd /opt/threads-service-ts/threads-service
threadsctl publish image --account main-brand --file "/root/.openclaw/media/spoiler.jpg" --text "Spoiler warning" --spoiler --confirmed
threadsctl publish carousel --account main-brand --files "/root/.openclaw/media/one.jpg,/root/.openclaw/media/two.jpg" --text "Spoiler gallery" --spoiler --confirmed
```

## Commands

### Accounts

```bash
threadsctl accounts list
threadsctl accounts stats --account main-brand
```

### OAuth

```bash
threadsctl auth connect-url --label main-brand
```

### Drafts

```bash
threadsctl drafts list --account main-brand
threadsctl draft create --account main-brand --type text --text "Post content" --created-by "OpenClaw"
threadsctl draft create --account main-brand --type image --media-url "https://example.com/image.jpg" --text "Caption" --alt-text "Alt text" --created-by "OpenClaw"
threadsctl draft create --account main-brand --type image --media-url "https://example.com/image.jpg" --text "Caption" --spoiler --created-by "OpenClaw"
threadsctl draft create --account main-brand --type carousel --media-urls "https://example.com/1.jpg,https://example.com/2.jpg" --text "Caption" --spoiler --created-by "OpenClaw"
threadsctl draft approve --id draft_xxx --approved-by "OpenClaw"
threadsctl draft publish --id draft_xxx --actor "OpenClaw"
```

### Direct Publish

```bash
cd /opt/threads-service-ts/threads-service
threadsctl publish text --account main-brand --text "Hello from Threads" --confirmed
threadsctl publish image --account main-brand --file "/root/.openclaw/media/tool-image-generation/image-1---real-file.jpg" --text "Caption" --alt-text "Alt text" --confirmed
threadsctl publish image --account main-brand --media-url "https://example.com/image.jpg" --text "Caption" --alt-text "Alt text" --confirmed
threadsctl publish image --account main-brand --file "/root/.openclaw/media/tool-image-generation/image.jpg" --text "Caption" --spoiler --confirmed
threadsctl publish carousel --account main-brand --media-urls "https://example.com/1.jpg,https://example.com/2.jpg" --text "Photo dump" --confirmed
threadsctl publish carousel --account main-brand --files "/root/.openclaw/media/one.jpg,/root/.openclaw/media/two.jpg" --text "Photo dump" --spoiler --confirmed
```

### Published Posts

```bash
threadsctl published list --account main-brand
```

## Workflow

### Direct Publish

Use when the user clearly wants an immediate post.

```bash
cd /opt/threads-service-ts/threads-service
threadsctl publish text --account main-brand --text "Launching today" --confirmed
```

### Draft First

Use when the user wants review, approval, or preparation before posting.

```bash
threadsctl draft create --account main-brand --type text --text "Launching today" --created-by "OpenClaw"
```

### Image Generation Plus Publish

If the user wants a brand new image, first use the configured image generation provider. If OpenClaw saved the file locally under `/root/.openclaw/media/...`, publish it with `--file`.

```bash
cd /opt/threads-service-ts/threads-service
threadsctl publish image --account main-brand --file "/root/.openclaw/media/tool-image-generation/generated-image.jpg" --text "Launching today" --alt-text "Product launch image" --confirmed
```

Use `--media-url` only when the image is already hosted at a public URL:

```bash
cd /opt/threads-service-ts/threads-service
threadsctl publish image --account main-brand --media-url "https://example.com/generated-image.jpg" --text "Launching today" --alt-text "Product launch image" --confirmed
```

### Carousel Publish

Use carousel for 2 to 20 images in one Threads post.

```bash
cd /opt/threads-service-ts/threads-service
threadsctl publish carousel --account main-brand --files "/root/.openclaw/media/one.jpg,/root/.openclaw/media/two.jpg" --text "Behind the scenes" --confirmed
```

### Spoiler Media

Use `--spoiler` for image or carousel media when the user wants Threads to blur the media as a spoiler.

```bash
cd /opt/threads-service-ts/threads-service
threadsctl publish image --account main-brand --file "/root/.openclaw/media/spoiler.jpg" --text "Spoiler warning" --spoiler --confirmed
```

For carousel posts, `--spoiler` applies to all attached media.

## Account Connection

To connect a new Threads account:

1. Run:

```bash
threadsctl auth connect-url --label client-two
```

2. Return the generated URL to the user.
3. Tell the user to open it in a browser and complete OAuth.

## Do Not

- Do not use raw `curl` when `threadsctl` supports the action.
- Do not invent account IDs.
- Do not silently switch accounts.
- Do not pass `--confirmed` unless immediate publishing is intended.
- Do not hide command errors.
- Do not assume an image generation provider is configured unless the environment actually supports it.
- Do not pass local filesystem paths to `--media-url`.
- Do not use `--spoiler` for text-only posts.

## Output Style

Prefer short result summaries:

- `Published successfully from main-brand.`
- `Draft created for second-brand.`
- `Could not publish because confirmation was not provided.`
