---
name: halo-manager
description: "Manage Halo blogs via API - create/edit/delete posts, manage categories/tags, handle comments, upload media. Use when user asks to manage their Halo blog, post articles, check blog stats, or perform any Halo CMS operations. Triggers on 'halo blog', 'halo cms', 'manage blog', 'post to halo', 'halo api'."
---

# Halo Manager

Manage Halo blogs through the official API.

## First-Time Setup

When this skill is first used, ask the user for:

1. **Blog URL** (e.g., `https://blog.example.com`)
2. **Username**
3. **Password**

Then save credentials to `~/halo-manager/config.json`:

```json
{
  "blog_url": "https://blog.example.com",
  "username": "your-username",
  "password": "your-password"
}
```

**Security Note:** Never expose credentials in logs, responses, or shared channels.

## Authentication

Halo uses RSA-encrypted password + CSRF token + Session cookie.

### Login Flow

1. GET `/login` - Extract CSRF token and RSA public key
2. Encrypt password with RSA public key (JSEncrypt)
3. POST `/login` with form data (username, encrypted password, CSRF token)
4. Receive SESSION cookie for subsequent requests

### Session Management

- Use SESSION cookie for all authenticated requests
- If session expires, re-login automatically
- Store session state in `~/halo-manager/session.json`

## API Endpoints

### Console API Base
```
{blog_url}/apis/api.console.halo.run/v1alpha1/
```

### Posts

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List posts | GET | `/posts` |
| Get post | GET | `/posts/{name}` |
| Create post | POST | `/posts` |
| Update post | PUT | `/posts/{name}` |
| Delete post | DELETE | `/posts/{name}` |

### Categories

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List categories | GET | `/categories` |
| Create category | POST | `/categories` |
| Update category | PUT | `/categories/{name}` |
| Delete category | DELETE | `/categories/{name}` |

### Tags

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List tags | GET | `/tags` |
| Create tag | POST | `/tags` |
| Update tag | PUT | `/tags/{name}` |
| Delete tag | DELETE | `/tags/{name}` |

### Users

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List users | GET | `/users` |
| Get current user | GET | `/users/-` |

### Comments

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List comments | GET | `/comments` |
| Approve comment | PUT | `/comments/{name}/approval` |
| Delete comment | DELETE | `/comments/{name}` |

### Media

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List attachments | GET | `/attachments` |
| Upload attachment | POST | `/attachments` |
| Delete attachment | DELETE | `/attachments/{name}` |

## Common Workflows

### Create a Post

1. Login to get session
2. Prepare post data:

```json
{
  "post": {
    "spec": {
      "title": "Post Title",
      "slug": "post-slug",
      "content": "Post content in Markdown",
      "rawType": "markdown",
      "categories": ["category-name"],
      "tags": ["tag1", "tag2"],
      "publish": true
    }
  }
}
```

3. POST to `/posts`
4. Verify creation

### Upload Media

1. Login to get session
2. Prepare multipart form data
3. POST to `/attachments`
4. Get attachment URL from response

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Unauthorized | Re-login |
| 403 | Forbidden | Check permissions |
| 404 | Not found | Verify resource exists |
| 500 | Server error | Retry or report |

## Output Format

```
【操作名称】

请求：{method} {endpoint}
状态：{status_code}
结果：成功/失败

详情：...
```

## Security Best Practices

1. **Never log credentials** - Mask passwords in all outputs
2. **Use HTTPS** - Always prefer secure connections
3. **Session timeout** - Re-authenticate when session expires
4. **Local storage only** - Credentials stay on user's machine

## References

- [API Reference](references/api-reference.md) - Complete API documentation
- [Examples](references/examples.md) - Common usage examples
