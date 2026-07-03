# Gmail - All Email Actions Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `gmail-all-email-actions`

x402 availability: not enabled for this product.

## `create_draft`

Action slug: `create-draft`

Price: `5` credits

Create a draft email that can be edited or sent later.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `attachments` | `array` | no | Email attachments. Provide public file URLs that will be fetched and attached. |
| `bcc` | `array` | no | BCC recipients. |
| `body_html` | `string` | no | HTML email body. Can be used instead of or in addition to body_text. |
| `body_text` | `string` | no | Plain text email body. Required unless body_html is provided. |
| `cc` | `array` | no | CC recipients. |
| `from_email` | `string` | no | From address override. Only works if the Gmail account has a configured send-as alias. |
| `subject` | `string` | yes | Email subject line. |
| `thread_id` | `string` | no | Thread ID to associate the draft with an existing conversation. |
| `to` | `array` | yes | Recipient email addresses. |

Sample parameters:

```json
{
  "attachments": [
    {
      "content_type": "application/octet-stream",
      "file_url": "https://example.com",
      "filename": "example filename"
    }
  ],
  "bcc": [
    "example bcc"
  ],
  "body_html": "example body html",
  "body_text": "example body text",
  "cc": [
    "example cc"
  ],
  "from_email": "user@example.com",
  "subject": "example subject",
  "thread_id": "example thread id"
}
```

Generated JSON parameter schema:

```json
{
  "attachments": {
    "description": "Email attachments. Provide public file URLs that will be fetched and attached.",
    "items": {
      "properties": {
        "content_type": {
          "default": "application/octet-stream",
          "description": "MIME type. Auto-detected when omitted.",
          "required": false,
          "type": "string"
        },
        "file_url": {
          "description": "Public URL to fetch the file from.",
          "required": true,
          "type": "string"
        },
        "filename": {
          "description": "Attachment filename.",
          "required": true,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "bcc": {
    "description": "BCC recipients.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "body_html": {
    "description": "HTML email body. Can be used instead of or in addition to body_text.",
    "required": false,
    "type": "string"
  },
  "body_text": {
    "description": "Plain text email body. Required unless body_html is provided.",
    "required": false,
    "type": "string"
  },
  "cc": {
    "description": "CC recipients.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "from_email": {
    "description": "From address override. Only works if the Gmail account has a configured send-as alias.",
    "required": false,
    "type": "string"
  },
  "subject": {
    "description": "Email subject line.",
    "required": true,
    "type": "string"
  },
  "thread_id": {
    "description": "Thread ID to associate the draft with an existing conversation.",
    "required": false,
    "type": "string"
  },
  "to": {
    "description": "Recipient email addresses.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  }
}
```

## `delete_draft`

Action slug: `delete-draft`

Price: `5` credits

Permanently delete a Gmail draft.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `draft_id` | `string` | yes | Gmail draft ID to delete. |

Sample parameters:

```json
{
  "draft_id": "example draft id"
}
```

Generated JSON parameter schema:

```json
{
  "draft_id": {
    "description": "Gmail draft ID to delete.",
    "required": true,
    "type": "string"
  }
}
```

## `forward_message`

Action slug: `forward-message`

Price: `5` credits

Forward an email to new recipients. The source message content is included automatically.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `attachments` | `array` | no | Additional email attachments. Provide public file URLs that will be fetched and attached. |
| `bcc` | `array` | no | BCC recipients. |
| `body_text` | `string` | no | Optional text to add above the forwarded content. |
| `cc` | `array` | no | CC recipients. |
| `message_id` | `string` | yes | Gmail message ID of the email to forward. |
| `to` | `array` | yes | Recipient email addresses to forward to. |

Sample parameters:

```json
{
  "attachments": [
    {
      "content_type": "application/octet-stream",
      "file_url": "https://example.com",
      "filename": "example filename"
    }
  ],
  "bcc": [
    "example bcc"
  ],
  "body_text": "example body text",
  "cc": [
    "example cc"
  ],
  "message_id": "example message id",
  "to": [
    "example to"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "attachments": {
    "description": "Additional email attachments. Provide public file URLs that will be fetched and attached.",
    "items": {
      "properties": {
        "content_type": {
          "default": "application/octet-stream",
          "description": "MIME type. Auto-detected when omitted.",
          "required": false,
          "type": "string"
        },
        "file_url": {
          "description": "Public URL to fetch the file from.",
          "required": true,
          "type": "string"
        },
        "filename": {
          "description": "Attachment filename.",
          "required": true,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "bcc": {
    "description": "BCC recipients.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "body_text": {
    "description": "Optional text to add above the forwarded content.",
    "required": false,
    "type": "string"
  },
  "cc": {
    "description": "CC recipients.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "message_id": {
    "description": "Gmail message ID of the email to forward.",
    "required": true,
    "type": "string"
  },
  "to": {
    "description": "Recipient email addresses to forward to.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  }
}
```

## `get_draft`

Action slug: `get-draft`

Price: `5` credits

Retrieve draft email content with safe body and metadata controls.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `body_format` | `string` | no | Body fields to return when message_format is full. Defaults to text. |
| `draft_id` | `string` | yes | Gmail draft ID. |
| `format` | `string` | no | Deprecated legacy alias for message_format. Use message_format for new calls. |
| `max_body_chars` | `integer` | no | Maximum characters returned per selected body field. Defaults to 8000. |
| `message_format` | `string` | no | Preferred read format: minimal, metadata, text, or full. |
| `metadata_headers` | `array` | no | Headers to request and return in metadata modes. |

Sample parameters:

```json
{
  "body_format": "none",
  "draft_id": "example draft id",
  "format": "full",
  "max_body_chars": 0,
  "message_format": "minimal",
  "metadata_headers": [
    "example metadata header"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "body_format": {
    "description": "Body fields to return when message_format is full. Defaults to text.",
    "enum": [
      "none",
      "text",
      "html",
      "both"
    ],
    "required": false,
    "type": "string"
  },
  "draft_id": {
    "description": "Gmail draft ID.",
    "required": true,
    "type": "string"
  },
  "format": {
    "description": "Deprecated legacy alias for message_format. Use message_format for new calls.",
    "enum": [
      "full",
      "metadata",
      "minimal"
    ],
    "required": false,
    "type": "string"
  },
  "max_body_chars": {
    "description": "Maximum characters returned per selected body field. Defaults to 8000.",
    "maximum": 100000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "message_format": {
    "description": "Preferred read format: minimal, metadata, text, or full.",
    "enum": [
      "minimal",
      "metadata",
      "text",
      "full"
    ],
    "required": false,
    "type": "string"
  },
  "metadata_headers": {
    "description": "Headers to request and return in metadata modes.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```

## `get_instructions`

Action slug: `get-instructions`

Price: `5` credits

Return Gmail tool usage instructions and examples.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `get_message`

Action slug: `get-message`

Price: `5` credits

Read a Gmail message with safe body and metadata controls.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `body_format` | `string` | no | Body fields to return when message_format is full. Defaults to text. Use html or both only when raw HTML is explicitly needed. |
| `format` | `string` | no | Deprecated legacy alias for message_format. Use message_format for new calls. |
| `max_body_chars` | `integer` | no | Maximum characters returned per selected body field. Defaults to 8000. |
| `message_format` | `string` | no | Preferred read format. minimal returns IDs/labels only; metadata returns headers/snippet/signals with no body fields; text returns capped text only; full returns metadata plus selected body fields. |
| `message_id` | `string` | yes | Gmail message ID. |
| `metadata_headers` | `array` | no | Headers to request and return in metadata modes. |

Sample parameters:

```json
{
  "body_format": "none",
  "format": "full",
  "max_body_chars": 0,
  "message_format": "minimal",
  "message_id": "example message id",
  "metadata_headers": [
    "example metadata header"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "body_format": {
    "description": "Body fields to return when message_format is full. Defaults to text. Use html or both only when raw HTML is explicitly needed.",
    "enum": [
      "none",
      "text",
      "html",
      "both"
    ],
    "required": false,
    "type": "string"
  },
  "format": {
    "description": "Deprecated legacy alias for message_format. Use message_format for new calls.",
    "enum": [
      "full",
      "metadata",
      "minimal"
    ],
    "required": false,
    "type": "string"
  },
  "max_body_chars": {
    "description": "Maximum characters returned per selected body field. Defaults to 8000.",
    "maximum": 100000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "message_format": {
    "description": "Preferred read format. minimal returns IDs/labels only; metadata returns headers/snippet/signals with no body fields; text returns capped text only; full returns metadata plus selected body fields.",
    "enum": [
      "minimal",
      "metadata",
      "text",
      "full"
    ],
    "required": false,
    "type": "string"
  },
  "message_id": {
    "description": "Gmail message ID.",
    "required": true,
    "type": "string"
  },
  "metadata_headers": {
    "description": "Headers to request and return in metadata modes.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```

## `get_profile`

Action slug: `get-profile`

Price: `5` credits

Get the authenticated Gmail profile including email address and message/thread counts.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `get_thread`

Action slug: `get-thread`

Price: `5` credits

Read Gmail thread messages with safe body and metadata controls.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `body_format` | `string` | no | Body fields to return when message_format is full. Defaults to text. |
| `format` | `string` | no | Deprecated legacy alias for message_format. Use message_format for new calls. |
| `include_html` | `boolean` | no | Shortcut that includes HTML when body_format is omitted. Defaults to false; body_format is the canonical selector. |
| `max_body_chars` | `integer` | no | Maximum characters returned per selected body field. Defaults to 8000. |
| `max_messages` | `integer` | no | Maximum thread messages to return (1-100). Defaults to 25. |
| `message_format` | `string` | no | Preferred read format for thread messages: minimal, metadata, text, or full. |
| `metadata_headers` | `array` | no | Headers to request and return in metadata modes. |
| `thread_id` | `string` | yes | Gmail thread ID. |

Sample parameters:

```json
{
  "body_format": "none",
  "format": "full",
  "include_html": false,
  "max_body_chars": 0,
  "max_messages": 25,
  "message_format": "minimal",
  "metadata_headers": [
    "example metadata header"
  ],
  "thread_id": "example thread id"
}
```

Generated JSON parameter schema:

```json
{
  "body_format": {
    "description": "Body fields to return when message_format is full. Defaults to text.",
    "enum": [
      "none",
      "text",
      "html",
      "both"
    ],
    "required": false,
    "type": "string"
  },
  "format": {
    "description": "Deprecated legacy alias for message_format. Use message_format for new calls.",
    "enum": [
      "full",
      "metadata",
      "minimal"
    ],
    "required": false,
    "type": "string"
  },
  "include_html": {
    "default": false,
    "description": "Shortcut that includes HTML when body_format is omitted. Defaults to false; body_format is the canonical selector.",
    "required": false,
    "type": "boolean"
  },
  "max_body_chars": {
    "description": "Maximum characters returned per selected body field. Defaults to 8000.",
    "maximum": 100000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "max_messages": {
    "default": 25,
    "description": "Maximum thread messages to return (1-100). Defaults to 25.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "message_format": {
    "description": "Preferred read format for thread messages: minimal, metadata, text, or full.",
    "enum": [
      "minimal",
      "metadata",
      "text",
      "full"
    ],
    "required": false,
    "type": "string"
  },
  "metadata_headers": {
    "description": "Headers to request and return in metadata modes.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "thread_id": {
    "description": "Gmail thread ID.",
    "required": true,
    "type": "string"
  }
}
```

## `list_labels`

Action slug: `list-labels`

Price: `5` credits

List all available Gmail labels, including system and user-created labels.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `list_messages`

Action slug: `list-messages`

Price: `5` credits

Search and list Gmail messages for triage. The tool requests a Gmail message page, fetches compact metadata for each listed message, then applies post-fetch date/category/label filters and optional thread dedupe. Returns messages plus result_size_estimate, next_page_token, fetched_count, and returned_count; returned_count can be lower than fetched_count.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dedupe_by_thread` | `boolean` | no | Return only the first retained message per thread after post-fetch filters. Defaults to true. |
| `exclude_categories` | `array` | no | Post-fetch filter: exclude Gmail categories such as promotions, social, updates, and forums. |
| `exclude_label_ids` | `array` | no | Post-fetch filter: exclude messages containing any of these Gmail label IDs. |
| `include_spam_trash` | `boolean` | no | Include spam and trash in the upstream Gmail list request. Defaults to false. |
| `label_ids` | `array` | no | Include only messages with these Gmail label IDs in the upstream Gmail list request. |
| `max_internal_date_ms` | `integer` | no | Post-fetch filter: exclude messages with internalDate later than this millisecond timestamp. |
| `max_results` | `integer` | no | Maximum Gmail API page size before metadata shaping, post-fetch filters, and thread dedupe (1-500). |
| `min_internal_date_ms` | `integer` | no | Post-fetch filter: exclude messages with internalDate earlier than this millisecond timestamp. |
| `page_token` | `string` | no | Pagination token from a previous list_messages response. |
| `q` | `string` | no | Gmail search query. Examples: is:unread, from:user@example.com, subject:meeting, has:attachment, newer_than:7d. |

Sample parameters:

```json
{
  "dedupe_by_thread": true,
  "exclude_categories": [
    "example exclude categorie"
  ],
  "exclude_label_ids": [
    "example exclude label id"
  ],
  "include_spam_trash": false,
  "label_ids": [
    "example label id"
  ],
  "max_internal_date_ms": 0,
  "max_results": 20,
  "min_internal_date_ms": 0
}
```

Generated JSON parameter schema:

```json
{
  "dedupe_by_thread": {
    "default": true,
    "description": "Return only the first retained message per thread after post-fetch filters. Defaults to true.",
    "required": false,
    "type": "boolean"
  },
  "exclude_categories": {
    "description": "Post-fetch filter: exclude Gmail categories such as promotions, social, updates, and forums.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "exclude_label_ids": {
    "description": "Post-fetch filter: exclude messages containing any of these Gmail label IDs.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "include_spam_trash": {
    "default": false,
    "description": "Include spam and trash in the upstream Gmail list request. Defaults to false.",
    "required": false,
    "type": "boolean"
  },
  "label_ids": {
    "description": "Include only messages with these Gmail label IDs in the upstream Gmail list request.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "max_internal_date_ms": {
    "description": "Post-fetch filter: exclude messages with internalDate later than this millisecond timestamp.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "max_results": {
    "default": 20,
    "description": "Maximum Gmail API page size before metadata shaping, post-fetch filters, and thread dedupe (1-500).",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "min_internal_date_ms": {
    "description": "Post-fetch filter: exclude messages with internalDate earlier than this millisecond timestamp.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "page_token": {
    "description": "Pagination token from a previous list_messages response.",
    "required": false,
    "type": "string"
  },
  "q": {
    "description": "Gmail search query. Examples: is:unread, from:user@example.com, subject:meeting, has:attachment, newer_than:7d.",
    "required": false,
    "type": "string"
  }
}
```

## `modify_labels`

Action slug: `modify-labels`

Price: `5` credits

Add or remove labels from an email. Common uses: mark as read, star, or archive.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `add_label_ids` | `array` | no | Label IDs to add. Common values: STARRED, IMPORTANT, UNREAD. |
| `message_id` | `string` | yes | Gmail message ID. |
| `remove_label_ids` | `array` | no | Label IDs to remove. Common values: UNREAD to mark read, INBOX to archive. |

Sample parameters:

```json
{
  "add_label_ids": [
    "example add label id"
  ],
  "message_id": "example message id",
  "remove_label_ids": [
    "example remove label id"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "add_label_ids": {
    "description": "Label IDs to add. Common values: STARRED, IMPORTANT, UNREAD.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "message_id": {
    "description": "Gmail message ID.",
    "required": true,
    "type": "string"
  },
  "remove_label_ids": {
    "description": "Label IDs to remove. Common values: UNREAD to mark read, INBOX to archive.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```

## `reply_message`

Action slug: `reply-message`

Price: `5` credits

Reply to an existing email. The reply stays in the same thread and automatically uses the original subject and recipient context.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `attachments` | `array` | no | Email attachments. Provide public file URLs that will be fetched and attached. |
| `bcc` | `array` | no | BCC recipients. |
| `body_html` | `string` | no | HTML reply body. Can be used instead of or in addition to body_text. |
| `body_text` | `string` | no | Plain text reply body. Required unless body_html is provided. |
| `cc` | `array` | no | CC recipients. |
| `message_id` | `string` | yes | Gmail message ID of the email to reply to. |

Sample parameters:

```json
{
  "attachments": [
    {
      "content_type": "application/octet-stream",
      "file_url": "https://example.com",
      "filename": "example filename"
    }
  ],
  "bcc": [
    "example bcc"
  ],
  "body_html": "example body html",
  "body_text": "example body text",
  "cc": [
    "example cc"
  ],
  "message_id": "example message id"
}
```

Generated JSON parameter schema:

```json
{
  "attachments": {
    "description": "Email attachments. Provide public file URLs that will be fetched and attached.",
    "items": {
      "properties": {
        "content_type": {
          "default": "application/octet-stream",
          "description": "MIME type. Auto-detected when omitted.",
          "required": false,
          "type": "string"
        },
        "file_url": {
          "description": "Public URL to fetch the file from.",
          "required": true,
          "type": "string"
        },
        "filename": {
          "description": "Attachment filename.",
          "required": true,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "bcc": {
    "description": "BCC recipients.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "body_html": {
    "description": "HTML reply body. Can be used instead of or in addition to body_text.",
    "required": false,
    "type": "string"
  },
  "body_text": {
    "description": "Plain text reply body. Required unless body_html is provided.",
    "required": false,
    "type": "string"
  },
  "cc": {
    "description": "CC recipients.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "message_id": {
    "description": "Gmail message ID of the email to reply to.",
    "required": true,
    "type": "string"
  }
}
```

## `send_draft`

Action slug: `send-draft`

Price: `5` credits

Send a previously created Gmail draft.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `draft_id` | `string` | yes | Gmail draft ID. |

Sample parameters:

```json
{
  "draft_id": "example draft id"
}
```

Generated JSON parameter schema:

```json
{
  "draft_id": {
    "description": "Gmail draft ID.",
    "required": true,
    "type": "string"
  }
}
```

## `send_message`

Action slug: `send-message`

Price: `5` credits

Send a new email. Supports plain text, HTML, attachments, CC/BCC, custom from address, and optional thread continuation.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `attachments` | `array` | no | Email attachments. Provide public file URLs that will be fetched and attached. |
| `bcc` | `array` | no | BCC recipients. |
| `body_html` | `string` | no | HTML email body. Can be used instead of or in addition to body_text. |
| `body_text` | `string` | no | Plain text email body. Required unless body_html is provided. |
| `cc` | `array` | no | CC recipients. |
| `from_email` | `string` | no | From address override. Only works if the Gmail account has a configured send-as alias. |
| `subject` | `string` | yes | Email subject line. |
| `thread_id` | `string` | no | Thread ID to add this message to an existing conversation thread. |
| `to` | `array` | yes | Recipient email addresses. |

Sample parameters:

```json
{
  "attachments": [
    {
      "content_type": "application/octet-stream",
      "file_url": "https://example.com",
      "filename": "example filename"
    }
  ],
  "bcc": [
    "example bcc"
  ],
  "body_html": "example body html",
  "body_text": "example body text",
  "cc": [
    "example cc"
  ],
  "from_email": "user@example.com",
  "subject": "example subject",
  "thread_id": "example thread id"
}
```

Generated JSON parameter schema:

```json
{
  "attachments": {
    "description": "Email attachments. Provide public file URLs that will be fetched and attached.",
    "items": {
      "properties": {
        "content_type": {
          "default": "application/octet-stream",
          "description": "MIME type such as application/pdf. Auto-detected from the URL response when omitted.",
          "required": false,
          "type": "string"
        },
        "file_url": {
          "description": "Public URL to fetch the file from. Must be directly accessible.",
          "required": true,
          "type": "string"
        },
        "filename": {
          "description": "Attachment filename such as report.pdf or image.png.",
          "required": true,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "bcc": {
    "description": "BCC recipients.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "body_html": {
    "description": "HTML email body. Can be used instead of or in addition to body_text.",
    "required": false,
    "type": "string"
  },
  "body_text": {
    "description": "Plain text email body. Required unless body_html is provided.",
    "required": false,
    "type": "string"
  },
  "cc": {
    "description": "CC recipients.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "from_email": {
    "description": "From address override. Only works if the Gmail account has a configured send-as alias.",
    "required": false,
    "type": "string"
  },
  "subject": {
    "description": "Email subject line.",
    "required": true,
    "type": "string"
  },
  "thread_id": {
    "description": "Thread ID to add this message to an existing conversation thread.",
    "required": false,
    "type": "string"
  },
  "to": {
    "description": "Recipient email addresses.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  }
}
```

## `trash_message`

Action slug: `trash-message`

Price: `5` credits

Move an email message to trash.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `message_id` | `string` | yes | Gmail message ID of the email to trash. |

Sample parameters:

```json
{
  "message_id": "example message id"
}
```

Generated JSON parameter schema:

```json
{
  "message_id": {
    "description": "Gmail message ID of the email to trash.",
    "required": true,
    "type": "string"
  }
}
```

## `untrash_message`

Action slug: `untrash-message`

Price: `5` credits

Restore an email message from trash.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `message_id` | `string` | yes | Gmail message ID of the email to restore. |

Sample parameters:

```json
{
  "message_id": "example message id"
}
```

Generated JSON parameter schema:

```json
{
  "message_id": {
    "description": "Gmail message ID of the email to restore.",
    "required": true,
    "type": "string"
  }
}
```
