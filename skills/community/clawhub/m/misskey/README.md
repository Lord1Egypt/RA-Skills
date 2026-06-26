# Misskey Skill

A skill for posting notes and uploading media to Misskey/Fediverse instances via API.

## Features

- 📝 Post text notes
- 🖼️ Upload and attach images
- 🗑️ Delete notes
- 👤 Get user information

## Setup

### 1. Get API Token

1. Login to your Misskey instance
2. Go to **Settings > API > Access Tokens**
3. Create a new token with required permissions

### 2. Configure Environment

```bash
export MISSKEY_HOST="https://your-instance.misskey.io"
export MISSKEY_TOKEN="your-api-token"
```

## Popular Misskey Instances

| Instance | URL | Description |
|----------|-----|-------------|
| maid.lat | https://maid.lat | メイド情報局 - A Misskey instance for maid lovers |
| misskey.io | https://misskey.io | Official Misskey instance |
| misskey.design | https://misskey.design | For designers |

## Usage

### Post a Text Note

```bash
# Example: Post to maid.lat
export MISSKEY_HOST="https://maid.lat"
export MISSKEY_TOKEN="your-api-token"
bash scripts/post.sh "Hello, Fediverse!"
```

### Post with Images

```bash
bash scripts/post.sh "Check out this image!" "/path/to/image.png"
```

### Post with Multiple Images

```bash
bash scripts/post.sh "Multiple images" "/path/to/img1.png" "/path/to/img2.png"
```

### Delete a Note

```bash
bash scripts/delete.sh "note-id-here"
```

### Upload File to Drive

```bash
bash scripts/upload.sh "/path/to/file.png"
```

### Get Current User Info

```bash
bash scripts/whoami.sh
```

## Options

### Visibility

```bash
# Public (default)
bash scripts/post.sh "Content" --visibility public

# Home timeline only
bash scripts/post.sh "Content" --visibility home

# Followers only
bash scripts/post.sh "Content" --visibility followers
```

### Content Warning (CW)

```bash
bash scripts/post.sh "Hidden content" --cw "Content warning"
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/notes/create` | POST | Create a note |
| `/api/notes/delete` | POST | Delete a note |
| `/api/drive/files/create` | POST | Upload file to drive |
| `/api/i` | POST | Get current user info |

## Files

```
misskey/
├── SKILL.md          # Skill documentation
├── README.md         # This file
├── _meta.json        # Metadata
└── scripts/
    ├── post.sh       # Post notes with optional images
    ├── delete.sh     # Delete notes
    ├── upload.sh     # Upload files to drive
    └── whoami.sh     # Display user info
```

## Error Handling

| Status | Meaning |
|--------|---------|
| 401 | Invalid or expired token |
| 400 | Invalid parameters |
| 429 | Rate limited |

## Security Notes

- Never commit your API token to version control
- Use environment variables for sensitive data
- Consider using tokens with minimal required permissions

## License

MIT
