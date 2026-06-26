# Payload Contract

The wrapper keeps the legacy ingest fields unchanged:

- `chat_id`
- `reply_to_message_id`
- `request_id`
- `source_kind`
- `source_url`
- `raw_text`
- `image_refs`
- `platform_hint`
- `requested_output_lang`

## Source Kind Rules

- `pasted_text`: plain text only
- `image`: uploaded screenshot or image only
- `video_url`: Bilibili, Xiaohongshu, YouTube, or other video link
- `url`: general webpage or article link
- `mixed`: a combination of text, links, and/or images

## `mixed` Preservation

For `mixed`, never drop fields just because another signal exists:

- main link stays in `source_url`
- pasted long text stays in `raw_text`
- uploaded or local images stay in `image_refs`
- `platform_hint` stays when obvious

The wrapper intentionally preserves the old contract so it can replay existing test cases and route into the untouched `openclaw_capture_workflow` repo.

