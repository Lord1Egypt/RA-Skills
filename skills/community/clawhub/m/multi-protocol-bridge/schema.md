# Multi-Protocol Bridge Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `multi-protocol-bridge`

x402 availability: not enabled for this product.

## `ftp_delete`

Action slug: `ftp-delete`

Price: `5` credits

Delete a file on an FTP or FTPS server. Requires explicit confirmation via options.confirm_delete.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | yes | Delete options |
| `url` | `string` | yes | FTP/FTPS URL with path to the file to delete (e.g., ftp://user:pass@ftp.example.com:21/old-files/archive.zip) |

Sample parameters:

```json
{
  "options": {
    "confirm_delete": "example confirm delete"
  },
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Delete options",
    "properties": {
      "confirm_delete": {
        "description": "Must be set to the string 'DELETE' to confirm file deletion",
        "required": true,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  },
  "url": {
    "description": "FTP/FTPS URL with path to the file to delete (e.g., ftp://user:pass@ftp.example.com:21/old-files/archive.zip)",
    "required": true,
    "type": "string"
  }
}
```

## `ftp_download`

Action slug: `ftp-download`

Price: `5` credits

Download a file from an FTP or FTPS server. Returns file content as text or base64.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Download options |
| `url` | `string` | yes | FTP/FTPS URL with path to the file to download (e.g., ftp://user:pass@ftp.example.com:21/reports/q1.csv) |

Sample parameters:

```json
{
  "options": {
    "return_base64": false
  },
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Download options",
    "properties": {
      "return_base64": {
        "default": false,
        "description": "Return file content as base64 instead of text. Use for binary files.",
        "required": false,
        "type": "boolean"
      }
    },
    "required": false,
    "type": "object"
  },
  "url": {
    "description": "FTP/FTPS URL with path to the file to download (e.g., ftp://user:pass@ftp.example.com:21/reports/q1.csv)",
    "required": true,
    "type": "string"
  }
}
```

## `ftp_list`

Action slug: `ftp-list`

Price: `5` credits

List the contents of a directory on an FTP or FTPS server.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Listing options |
| `url` | `string` | yes | FTP/FTPS URL with path to the directory (e.g., ftp://user:pass@ftp.example.com:21/documents/) |

Sample parameters:

```json
{
  "options": {
    "recursive": false
  },
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Listing options",
    "properties": {
      "recursive": {
        "default": false,
        "description": "List subdirectories recursively",
        "required": false,
        "type": "boolean"
      }
    },
    "required": false,
    "type": "object"
  },
  "url": {
    "description": "FTP/FTPS URL with path to the directory (e.g., ftp://user:pass@ftp.example.com:21/documents/)",
    "required": true,
    "type": "string"
  }
}
```

## `ftp_upload`

Action slug: `ftp-upload`

Price: `5` credits

Upload a file to an FTP or FTPS server. Supports text and base64-encoded binary content.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | `string` | yes | File content to upload. For binary files, provide base64-encoded content and set content_encoding to 'base64'. |
| `content_encoding` | `string` | no | How content is encoded: 'text' for plain text, 'base64' for binary files |
| `url` | `string` | yes | FTP/FTPS URL with path to the destination file (e.g., ftp://user:pass@ftp.example.com:21/path/to/file.txt). Use ftps:// for encrypted connections. |

Sample parameters:

```json
{
  "content": "Draft marketing copy to check for banned phrases.",
  "content_encoding": "text",
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "content": {
    "description": "File content to upload. For binary files, provide base64-encoded content and set content_encoding to 'base64'.",
    "required": true,
    "type": "string"
  },
  "content_encoding": {
    "default": "text",
    "description": "How content is encoded: 'text' for plain text, 'base64' for binary files",
    "enum": [
      "text",
      "base64"
    ],
    "required": false,
    "type": "string"
  },
  "url": {
    "description": "FTP/FTPS URL with path to the destination file (e.g., ftp://user:pass@ftp.example.com:21/path/to/file.txt). Use ftps:// for encrypted connections.",
    "required": true,
    "type": "string"
  }
}
```

## `mqtt_publish`

Action slug: `mqtt-publish`

Price: `5` credits

Publish a message to an MQTT or MQTTS broker. The topic is specified as the URL path.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | `string` | yes | Message payload to publish (plain text or JSON string) |
| `options` | `object` | no | MQTT publish options |
| `url` | `string` | yes | MQTT URL with the topic as the path (e.g., mqtt://user:pass@broker.example.com:1883/sensors/temperature). Use mqtts:// for TLS. |

Sample parameters:

```json
{
  "content": "Draft marketing copy to check for banned phrases.",
  "options": {
    "client_id": "example client id",
    "qos": 0,
    "retain": false
  },
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "content": {
    "description": "Message payload to publish (plain text or JSON string)",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "MQTT publish options",
    "properties": {
      "client_id": {
        "description": "MQTT client identifier. Auto-generated if not provided.",
        "required": false,
        "type": "string"
      },
      "qos": {
        "default": 0,
        "description": "Quality of Service level: 0=at most once, 1=at least once, 2=exactly once",
        "required": false,
        "type": "integer"
      },
      "retain": {
        "default": false,
        "description": "Broker retains the message for future subscribers",
        "required": false,
        "type": "boolean"
      }
    },
    "required": false,
    "type": "object"
  },
  "url": {
    "description": "MQTT URL with the topic as the path (e.g., mqtt://user:pass@broker.example.com:1883/sensors/temperature). Use mqtts:// for TLS.",
    "required": true,
    "type": "string"
  }
}
```

## `ssh_execute`

Action slug: `ssh-execute`

Price: `5` credits

Execute a shell command on a remote server via SSH. Supports password and key-based authentication.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | `string` | yes | Shell command to execute on the remote server (e.g., 'ls -la /home/user') |
| `options` | `object` | no | SSH connection options |
| `url` | `string` | yes | SSH URL (e.g., ssh://user:pass@server.example.com:22). For key auth, omit password and provide private_key in options. |

Sample parameters:

```json
{
  "content": "Draft marketing copy to check for banned phrases.",
  "options": {
    "known_hosts": "example known hosts",
    "private_key": "example private key",
    "timeout": 30
  },
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "content": {
    "description": "Shell command to execute on the remote server (e.g., 'ls -la /home/user')",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "SSH connection options",
    "properties": {
      "known_hosts": {
        "description": "SSH known hosts string for host verification",
        "required": false,
        "type": "string"
      },
      "private_key": {
        "description": "SSH private key in PEM format for key-based authentication",
        "required": false,
        "type": "string"
      },
      "timeout": {
        "default": 30,
        "description": "Command timeout in seconds",
        "required": false,
        "type": "integer"
      }
    },
    "required": false,
    "type": "object"
  },
  "url": {
    "description": "SSH URL (e.g., ssh://user:pass@server.example.com:22). For key auth, omit password and provide private_key in options.",
    "required": true,
    "type": "string"
  }
}
```
