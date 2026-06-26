# Halo Manager Examples

Common usage examples for managing Halo blogs.

## Example 1: List All Posts

```bash
# First, login to get session cookie
curl -c cookies.txt -b cookies.txt \
  -X GET "https://blog.example.com/apis/api.console.halo.run/v1alpha1/posts?page=1&size=10" \
  -H "Accept: application/json"
```

## Example 2: Create a New Post

```bash
# Create post
curl -c cookies.txt -b cookies.txt \
  -X POST "https://blog.example.com/apis/api.console.halo.run/v1alpha1/posts" \
  -H "Content-Type: application/json" \
  -H "X-CSRF-TOKEN: {csrf-token}" \
  -d '{
    "post": {
      "spec": {
        "title": "My First Post",
        "slug": "my-first-post",
        "content": "# Hello World\n\nThis is my first post!",
        "rawType": "markdown",
        "categories": [],
        "tags": ["hello", "first"],
        "publish": true
      },
      "metadata": {
        "name": ""
      }
    }
  }'
```

## Example 3: Update a Post

```bash
curl -c cookies.txt -b cookies.txt \
  -X PUT "https://blog.example.com/apis/api.console.halo.run/v1alpha1/posts/post-name" \
  -H "Content-Type: application/json" \
  -H "X-CSRF-TOKEN: {csrf-token}" \
  -d '{
    "post": {
      "spec": {
        "title": "Updated Title",
        "slug": "updated-slug",
        "content": "Updated content",
        "rawType": "markdown",
        "publish": true
      },
      "metadata": {
        "name": "post-name"
      }
    }
  }'
```

## Example 4: Delete a Post

```bash
curl -c cookies.txt -b cookies.txt \
  -X DELETE "https://blog.example.com/apis/api.console.halo.run/v1alpha1/posts/post-name" \
  -H "X-CSRF-TOKEN: {csrf-token}"
```

## Example 5: Create Category

```bash
curl -c cookies.txt -b cookies.txt \
  -X POST "https://blog.example.com/apis/api.console.halo.run/v1alpha1/categories" \
  -H "Content-Type: application/json" \
  -H "X-CSRF-TOKEN: {csrf-token}" \
  -d '{
    "category": {
      "spec": {
        "displayName": "Technology",
        "slug": "technology",
        "description": "Tech articles",
        "priority": 0
      },
      "metadata": {
        "name": ""
      }
    }
  }'
```

## Example 6: Create Tag

```bash
curl -c cookies.txt -b cookies.txt \
  -X POST "https://blog.example.com/apis/api.console.halo.run/v1alpha1/tags" \
  -H "Content-Type: application/json" \
  -H "X-CSRF-TOKEN: {csrf-token}" \
  -d '{
    "tag": {
      "spec": {
        "displayName": "JavaScript",
        "slug": "javascript",
        "color": "#f7df1e"
      },
      "metadata": {
        "name": ""
      }
    }
  }'
```

## Example 7: Upload Image

```bash
curl -c cookies.txt -b cookies.txt \
  -X POST "https://blog.example.com/apis/api.console.halo.run/v1alpha1/attachments" \
  -H "X-CSRF-TOKEN: {csrf-token}" \
  -F "file=@/path/to/image.jpg"
```

## Example 8: Get Blog Stats

```bash
# Get post count
curl -c cookies.txt -b cookies.txt \
  -X GET "https://blog.example.com/apis/api.console.halo.run/v1alpha1/posts?size=1" \
  -H "Accept: application/json"

# Response includes "total" field with total count
```

## Example 9: List Comments

```bash
curl -c cookies.txt -b cookies.txt \
  -X GET "https://blog.example.com/apis/api.console.halo.run/v1alpha1/comments?approved=false" \
  -H "Accept: application/json"
```

## Example 10: Approve Comment

```bash
curl -c cookies.txt -b cookies.txt \
  -X PUT "https://blog.example.com/apis/api.console.halo.run/v1alpha1/comments/comment-name/approval" \
  -H "X-CSRF-TOKEN: {csrf-token}"
```

---

## PowerShell Examples

### Login and Get Session

```powershell
# Get login page for CSRF token and public key
$loginPage = Invoke-WebRequest -Uri "https://blog.example.com/login" -SessionVariable session

# Extract CSRF token (from hidden input)
$csrf = ($loginPage.Content -match 'name="_csrf".*?value="([^"]+)"')[1]

# Extract public key (from JavaScript)
$publicKey = ($loginPage.Content -match 'publicKey\s*=\s*"([^"]+)"')[1]

# Encrypt password with RSA (requires RSA encryption function)
$encryptedPassword = Encrypt-RSA -PublicKey $publicKey -Password "your-password"

# Login
$loginBody = @{
    username = "your-username"
    password = $encryptedPassword
    "_csrf" = $csrf
}
$login = Invoke-WebRequest -Uri "https://blog.example.com/login" `
    -Method POST `
    -Body $loginBody `
    -WebSession $session
```

### Create Post

```powershell
$postData = @{
    post = @{
        spec = @{
            title = "My Post"
            slug = "my-post"
            content = "# Hello World"
            rawType = "markdown"
            categories = @()
            tags = @()
            publish = $true
        }
        metadata = @{
            name = ""
        }
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "https://blog.example.com/apis/api.console.halo.run/v1alpha1/posts" `
    -Method POST `
    -Body $postData `
    -ContentType "application/json" `
    -WebSession $session
```
