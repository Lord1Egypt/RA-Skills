# API Workflow

## Headers

Use this header for JSON API requests:

```text
Content-Type: application/json
```

Optional controlled-access header:

```text
X-Access-Code: $PPTMAGIC_ACCESS_CODE
```

Use `X-Access-Code` only when the deployment operator explicitly provided an access code. For template uploads, use `multipart/form-data`.

## Create project

### Topic -> `idea`

`POST /api/projects`

```json
{
  "creation_type": "idea",
  "idea_prompt": "Make an 8-page Chinese PPT about AI Agent workflows",
  "template_style": "launch-event minimal style",
  "image_aspect_ratio": "16:9"
}
```

### Outline -> `outline`

`POST /api/projects`

```json
{
  "creation_type": "outline",
  "outline_text": "1. Cover\n2. Problem\n3. Demo\n4. Conclusion",
  "template_style": "clean white keynote style",
  "image_aspect_ratio": "16:9"
}
```

### Detailed slide descriptions -> `descriptions`

`POST /api/projects`

```json
{
  "creation_type": "descriptions",
  "description_text": "Slide 1: Cover...",
  "template_style": "high-end consulting style",
  "image_aspect_ratio": "16:9"
}
```

Read `data.project_id` from the response.

## Upload template image

`POST /api/projects/{project_id}/template`

Form field:

- `template_image`

## Generate outline

Use for `idea` and `outline` projects.

`POST /api/projects/{project_id}/generate/outline`

```json
{
  "language": "zh"
}
```

## Generate descriptions

`POST /api/projects/{project_id}/generate/descriptions`

```json
{
  "language": "zh",
  "detail_level": "default"
}
```

This usually returns a `task_id`.

## Generate images

`POST /api/projects/{project_id}/generate/images`

```json
{
  "language": "zh"
}
```

Retry only selected pages when needed:

```json
{
  "language": "zh",
  "page_ids": ["page-id-1", "page-id-2"]
}
```

## Inspect project and tasks

### Project

`GET /api/projects/{project_id}`

Use it to inspect pages, statuses, and generated image URLs.

### Task

`GET /api/projects/{project_id}/tasks/{task_id}`

Watch:

- `data.status`
- `data.progress`
- `data.error`

Recommended poll interval: 2-5 seconds.

## Export

### PPTX

`GET /api/projects/{project_id}/export/pptx`

### PDF

`GET /api/projects/{project_id}/export/pdf`

### Editable PPTX

`POST /api/projects/{project_id}/export/editable-pptx`

```json
{
  "filename": "editable-export",
  "page_ids": null
}
```

## Recommended recovery strategy

1. Keep partially successful projects instead of recreating them immediately.
2. If a task fails, inspect project state before retrying.
3. Retry image generation only for failed pages.
4. Verify project completeness before export.
5. If the gated endpoint returns HTML instead of JSON, switch to a known working deployment or get the correct access flow before continuing.
