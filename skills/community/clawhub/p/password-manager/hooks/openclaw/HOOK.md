# password-manager Hook

OpenClaw integration hook providing password management functionality.

## Tool List

| Tool Name | Description |
|-----------|-------------|
| `password_manager_add` | Add entry to password manager |
| `password_manager_get` | Get entry content |
| `password_manager_update` | Update entry |
| `password_manager_delete` | Delete entry (sensitive operation) |
| `password_manager_search` | Search entries |
| `password_manager_list` | List all entries |
| `password_manager_generate` | Generate random password |
| `password_manager_check_strength` | Check password strength |
| `password_manager_status` | View status |
| `password_manager_detect` | Detect sensitive information |

## Usage Examples

### Add Entry

```javascript
{
  name: "password_manager_add",
  arguments: {
    name: "github-token",
    type: "token",
    username: "user@example.com",
    password: "ghp_xxx",
    tags: ["work", "git"]
  }
}
```

### Get Entry

```javascript
{
  name: "password_manager_get",
  arguments: {
    name: "github-token",
    showPassword: true
  }
}
```

### Generate Password

```javascript
{
  name: "password_manager_generate",
  arguments: {
    length: 32,
    includeSymbols: true
  }
}
```

## Authentication Flow

1. **First Use**: Returns `requiresAuth: true, action: 'init'`
2. **Locked**: Returns `requiresAuth: true, action: 'unlock'`
3. **Sensitive Operation**: Returns `requiresAuth: true, action: 'confirm_delete'`

## Sensitive Information Detection

When user message contains sensitive information, the `onUserMessage` hook returns:

```javascript
{
  hasSensitiveInfo: true,
  detections: [
    {
      type: "github_token",
      name: "GitHub Token",
      sensitivity: "high",
      suggestedEntryName: "github-token"
    }
  ],
  prompt: "🔍 Sensitive information detected..."
}
```
