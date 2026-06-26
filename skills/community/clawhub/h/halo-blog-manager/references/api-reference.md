# Halo API Reference

Complete API documentation for Halo CMS v2.x.

## Authentication

### Login Endpoint

```
POST /login
Content-Type: application/x-www-form-urlencoded
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| username | string | Yes | Username |
| password | string | Yes | RSA-encrypted password |
| _csrf | string | Yes | CSRF token from login page |

**Response:**
- 302 redirect to `/uc` on success
- SESSION cookie set

### RSA Encryption

1. GET `/login` to retrieve public key
2. Find `window.publicKey` in response
3. Encrypt password using JSEncrypt (RSA)
4. Use encrypted password in login request

---

## Posts API

### List Posts

```
GET /apis/api.console.halo.run/v1alpha1/posts
```

**Query Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| page | int | 1 | Page number |
| size | int | 10 | Items per page |
| keyword | string | - | Search keyword |
| publishStatus | string | - | ALL/PUBLISHED/DRAFT |
| sort | string | - | Sort field |

**Response:**
```json
{
  "items": [
    {
      "metadata": {
        "name": "post-name",
        "creationTimestamp": "2024-01-01T00:00:00Z"
      },
      "spec": {
        "title": "Post Title",
        "slug": "post-slug",
        "content": "Post content",
        "rawType": "markdown",
        "publish": true,
        "categories": ["category-name"],
        "tags": ["tag1"]
      },
      "status": {
        "phase": "PUBLISHED",
        "lastReleasedSnapshot": "snapshot-name"
      }
    }
  ],
  "total": 100,
  "page": 1,
  "size": 10
}
```

### Get Post

```
GET /apis/api.console.halo.run/v1alpha1/posts/{name}
```

### Create Post

```
POST /apis/api.console.halo.run/v1alpha1/posts
Content-Type: application/json
```

**Request Body:**
```json
{
  "post": {
    "spec": {
      "title": "Post Title",
      "slug": "post-slug",
      "content": "Post content in Markdown",
      "rawType": "markdown",
      "categories": [],
      "tags": [],
      "publish": false,
      "pinned": false,
      "allowComment": true
    },
    "metadata": {
      "name": "",
      "annotations": {}
    }
  }
}
```

### Update Post

```
PUT /apis/api.console.halo.run/v1alpha1/posts/{name}
Content-Type: application/json
```

### Delete Post

```
DELETE /apis/api.console.halo.run/v1alpha1/posts/{name}
```

---

## Categories API

### List Categories

```
GET /apis/api.console.halo.run/v1alpha1/categories
```

**Response:**
```json
{
  "items": [
    {
      "metadata": {
        "name": "category-name"
      },
      "spec": {
        "displayName": "Category Name",
        "slug": "category-slug",
        "description": "Category description",
        "cover": "",
        "template": "",
        "priority": 0
      }
    }
  ]
}
```

### Create Category

```
POST /apis/api.console.halo.run/v1alpha1/categories
Content-Type: application/json
```

**Request Body:**
```json
{
  "category": {
    "spec": {
      "displayName": "Category Name",
      "slug": "category-slug",
      "description": "",
      "cover": "",
      "template": "",
      "priority": 0
    },
    "metadata": {
      "name": ""
    }
  }
}
```

---

## Tags API

### List Tags

```
GET /apis/api.console.halo.run/v1alpha1/tags
```

**Response:**
```json
{
  "items": [
    {
      "metadata": {
        "name": "tag-name"
      },
      "spec": {
        "displayName": "Tag Name",
        "slug": "tag-slug",
        "color": "#ffffff"
      }
    }
  ]
}
```

### Create Tag

```
POST /apis/api.console.halo.run/v1alpha1/tags
Content-Type: application/json
```

**Request Body:**
```json
{
  "tag": {
    "spec": {
      "displayName": "Tag Name",
      "slug": "tag-slug",
      "color": "#ffffff"
    },
    "metadata": {
      "name": ""
    }
  }
}
```

---

## Users API

### List Users

```
GET /apis/api.console.halo.run/v1alpha1/users
```

### Get Current User

```
GET /apis/api.console.halo.run/v1alpha1/users/-
```

---

## Comments API

### List Comments

```
GET /apis/api.console.halo.run/v1alpha1/comments
```

**Query Parameters:**
| Name | Type | Description |
|------|------|-------------|
| postName | string | Filter by post |
| approved | boolean | Filter by approval status |

### Approve Comment

```
PUT /apis/api.console.halo.run/v1alpha1/comments/{name}/approval
```

### Delete Comment

```
DELETE /apis/api.console.halo.run/v1alpha1/comments/{name}
```

---

## Attachments API

### List Attachments

```
GET /apis/api.console.halo.run/v1alpha1/attachments
```

### Upload Attachment

```
POST /apis/api.console.halo.run/v1alpha1/attachments
Content-Type: multipart/form-data
```

**Form Fields:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | file | Yes | The file to upload |
| groupName | string | No | Attachment group |

**Response:**
```json
{
  "metadata": {
    "name": "attachment-name"
  },
  "spec": {
    "displayName": "filename.jpg",
    "url": "/upload/filename.jpg"
  }
}
```

### Delete Attachment

```
DELETE /apis/api.console.halo.run/v1alpha1/attachments/{name}
```

---

## Public API

For public (unauthenticated) access:

```
GET /apis/api.halo.run/v1alpha1/posts
GET /apis/api.halo.run/v1alpha1/posts/{name}
GET /apis/api.halo.run/v1alpha1/categories
GET /apis/api.halo.run/v1alpha1/tags
```

---

## Error Responses

### Common Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Login required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 500 | Internal Server Error |

### Error Response Format

```json
{
  "type": "about:blank",
  "title": "Error Title",
  "status": 400,
  "detail": "Error details",
  "instance": "/api/endpoint"
}
```
