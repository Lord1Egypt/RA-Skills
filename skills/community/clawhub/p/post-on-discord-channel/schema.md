# Post On Discord Channel Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `post-on-discord-channel`

x402 availability: not enabled for this product.

## `send`

Action slug: `send`

Price: `3` credits

Send a message to a Discord channel via webhook. Supports text content with Discord markdown, rich embeds, file attachments, custom bot identity, text-to-speech, and mention controls. At least one of content, embeds, or files must be provided.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `allowed_mentions` | `object` | no | Controls which mentions are allowed to ping users/roles in the message. |
| `avatar_url` | `string` | no | Override the default webhook avatar with a custom image URL. |
| `content` | `string` | no | Message content text (max 2000 characters). Supports Discord markdown formatting. At least one of content, embeds, or files must be provided. |
| `embeds` | `array` | no | Array of rich embed objects (maximum 10 embeds per message). At least one of content, embeds, or files must be provided. |
| `files` | `array` | no | Array of file attachments (maximum 10 files per message). Files must be base64-encoded. At least one of content, embeds, or files must be provided. |
| `tts` | `boolean` | no | Enable text-to-speech for the message. Default: false. |
| `username` | `string` | no | Override the default webhook username (displayed as the message author name). Max 80 characters. |
| `webhook_url` | `string` | yes | Discord webhook URL. Must match the pattern: https://discord.com/api/webhooks/{webhook_id}/{webhook_token} or https://discordapp.com/api/webhooks/{webhook_id}/{webhook_token}. |

Sample parameters:

```json
{
  "allowed_mentions": {
    "parse": [
      "roles"
    ],
    "roles": [
      "example role"
    ],
    "users": [
      "example user"
    ]
  },
  "avatar_url": "https://example.com",
  "content": "Draft marketing copy to check for banned phrases.",
  "embeds": [
    {
      "author": {
        "icon_url": "https://example.com",
        "name": "example name",
        "url": "https://example.com"
      },
      "color": 1,
      "description": "example description",
      "fields": [
        {
          "inline": false,
          "name": "example name",
          "value": "example value"
        }
      ],
      "footer": {
        "icon_url": "https://example.com",
        "text": "example text"
      },
      "image": {
        "url": "https://example.com"
      },
      "thumbnail": {
        "url": "https://example.com"
      },
      "timestamp": "example timestamp"
    }
  ],
  "files": [
    {
      "content": "Draft marketing copy to check for banned phrases.",
      "description": "example description",
      "filename": "example filename"
    }
  ],
  "tts": false,
  "username": "example username",
  "webhook_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "allowed_mentions": {
    "description": "Controls which mentions are allowed to ping users/roles in the message.",
    "properties": {
      "parse": {
        "description": "Array of allowed mention types: 'roles', 'users', 'everyone'.",
        "items": {
          "enum": [
            "roles",
            "users",
            "everyone"
          ],
          "type": "string"
        },
        "required": false,
        "type": "array"
      },
      "roles": {
        "description": "Array of specific role IDs that are allowed to be mentioned.",
        "items": {
          "type": "string"
        },
        "required": false,
        "type": "array"
      },
      "users": {
        "description": "Array of specific user IDs that are allowed to be mentioned.",
        "items": {
          "type": "string"
        },
        "required": false,
        "type": "array"
      }
    },
    "required": false,
    "type": "object"
  },
  "avatar_url": {
    "description": "Override the default webhook avatar with a custom image URL.",
    "required": false,
    "type": "string"
  },
  "content": {
    "description": "Message content text (max 2000 characters). Supports Discord markdown formatting. At least one of content, embeds, or files must be provided.",
    "maxLength": 2000,
    "required": false,
    "type": "string"
  },
  "embeds": {
    "description": "Array of rich embed objects (maximum 10 embeds per message). At least one of content, embeds, or files must be provided.",
    "items": {
      "properties": {
        "author": {
          "description": "Embed author information.",
          "properties": {
            "icon_url": {
              "description": "URL of author icon (only supports http(s)).",
              "required": false,
              "type": "string"
            },
            "name": {
              "description": "Author name.",
              "required": true,
              "type": "string"
            },
            "url": {
              "description": "URL that the author name will link to.",
              "required": false,
              "type": "string"
            }
          },
          "required": false,
          "type": "object"
        },
        "color": {
          "description": "Color code in decimal format (not hex). Example: Blue (0x0099FF) = 39423, Red (0xFF0000) = 16711680, Green (0x00FF00) = 65280.",
          "required": false,
          "type": "integer"
        },
        "description": {
          "description": "Embed description text. Supports Discord markdown. Max 4096 characters.",
          "maxLength": 4096,
          "required": false,
          "type": "string"
        },
        "fields": {
          "description": "Array of embed field objects (maximum 25 fields per embed).",
          "items": {
            "properties": {
              "inline": {
                "default": false,
                "description": "Whether the field should display inline (side-by-side with other inline fields). Default: false.",
                "required": false,
                "type": "boolean"
              },
              "name": {
                "description": "Field name/title (max 256 characters).",
                "maxLength": 256,
                "required": true,
                "type": "string"
              },
              "value": {
                "description": "Field value/content (max 1024 characters).",
                "maxLength": 1024,
                "required": true,
                "type": "string"
              }
            },
            "type": "object"
          },
          "maxItems": 25,
          "required": false,
          "type": "array"
        },
        "footer": {
          "description": "Embed footer text and icon.",
          "properties": {
            "icon_url": {
              "description": "URL of footer icon (only supports http(s)).",
              "required": false,
              "type": "string"
            },
            "text": {
              "description": "Footer text (does not support markdown). Max 2048 characters.",
              "maxLength": 2048,
              "required": true,
              "type": "string"
            }
          },
          "required": false,
          "type": "object"
        },
        "image": {
          "description": "Embed image (displayed as large image below embed content).",
          "properties": {
            "url": {
              "description": "URL of image (supports http(s) and attachment://).",
              "required": true,
              "type": "string"
            }
          },
          "required": false,
          "type": "object"
        },
        "thumbnail": {
          "description": "Embed thumbnail image (displayed in top-right corner).",
          "properties": {
            "url": {
              "description": "URL of thumbnail image (supports http(s) and attachment://).",
              "required": true,
              "type": "string"
            }
          },
          "required": false,
          "type": "object"
        },
        "timestamp": {
          "description": "ISO8601 timestamp string (e.g., 2026-03-09T12:00:00Z). Displayed in footer.",
          "required": false,
          "type": "string"
        },
        "title": {
          "description": "Embed title (max 256 characters).",
          "maxLength": 256,
          "required": false,
          "type": "string"
        },
        "url": {
          "description": "URL that the title will link to.",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "maxItems": 10,
    "required": false,
    "type": "array"
  },
  "files": {
    "description": "Array of file attachments (maximum 10 files per message). Files must be base64-encoded. At least one of content, embeds, or files must be provided.",
    "items": {
      "properties": {
        "content": {
          "description": "Base64-encoded file content.",
          "required": true,
          "type": "string"
        },
        "description": {
          "description": "Description of the file attachment.",
          "required": false,
          "type": "string"
        },
        "filename": {
          "description": "Name of the file including extension (e.g., 'report.csv', 'image.png').",
          "required": true,
          "type": "string"
        }
      },
      "type": "object"
    },
    "maxItems": 10,
    "required": false,
    "type": "array"
  },
  "tts": {
    "default": false,
    "description": "Enable text-to-speech for the message. Default: false.",
    "required": false,
    "type": "boolean"
  },
  "username": {
    "description": "Override the default webhook username (displayed as the message author name). Max 80 characters.",
    "maxLength": 80,
    "required": false,
    "type": "string"
  },
  "webhook_url": {
    "description": "Discord webhook URL. Must match the pattern: https://discord.com/api/webhooks/{webhook_id}/{webhook_token} or https://discordapp.com/api/webhooks/{webhook_id}/{webhook_token}.",
    "required": true,
    "type": "string"
  }
}
```
