# Curl Examples

Assume the public deployment:

```bash
export PPTMAGIC_BASE_URL="https://openclaw-nopass.pptmagic.tech"
```

Optional controlled access when the operator gives you a code:

```bash
export PPTMAGIC_ACCESS_CODE="your-access-code"
```

## Create an outline project

Without access code:

```bash
curl -sS "$PPTMAGIC_BASE_URL/api/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "creation_type": "outline",
    "outline_text": "1. Cover\n2. Demo\n3. Conclusion",
    "template_style": "minimal launch-event style",
    "image_aspect_ratio": "16:9"
  }'
```

With optional access code:

```bash
curl -sS "$PPTMAGIC_BASE_URL/api/projects" \
  -H "Content-Type: application/json" \
  -H "X-Access-Code: $PPTMAGIC_ACCESS_CODE" \
  -d '{
    "creation_type": "outline",
    "outline_text": "1. Cover\n2. Demo\n3. Conclusion",
    "template_style": "minimal launch-event style",
    "image_aspect_ratio": "16:9"
  }'
```

## Generate outline

```bash
curl -sS "$PPTMAGIC_BASE_URL/api/projects/$PROJECT_ID/generate/outline" \
  -H "Content-Type: application/json" \
  -d '{"language":"zh"}'
```

## Generate descriptions

```bash
curl -sS "$PPTMAGIC_BASE_URL/api/projects/$PROJECT_ID/generate/descriptions" \
  -H "Content-Type: application/json" \
  -d '{"language":"zh","detail_level":"default"}'
```

## Generate images

```bash
curl -sS "$PPTMAGIC_BASE_URL/api/projects/$PROJECT_ID/generate/images" \
  -H "Content-Type: application/json" \
  -d '{"language":"zh"}'
```

## Poll task

```bash
curl -sS "$PPTMAGIC_BASE_URL/api/projects/$PROJECT_ID/tasks/$TASK_ID"
```

## Export PPTX

```bash
curl -sS "$PPTMAGIC_BASE_URL/api/projects/$PROJECT_ID/export/pptx"
```

## Export editable PPTX

```bash
curl -sS "$PPTMAGIC_BASE_URL/api/projects/$PROJECT_ID/export/editable-pptx" \
  -H "Content-Type: application/json" \
  -d '{"filename":"editable-export"}'
```
