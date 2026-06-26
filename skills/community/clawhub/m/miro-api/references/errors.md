# Miro REST API - Error Handling

## HTTP Status Codes

| Code | Name | Meaning | Action |
|------|------|---------|--------|
| 200 | OK | Request succeeded | None, operation complete |
| 201 | Created | Resource created | Check Location header for new resource URL |
| 204 | No Content | Success, no response body | Operation complete, nothing to parse |
| 400 | Bad Request | Invalid parameters | Check error details, fix request |
| 401 | Unauthorized | Missing/invalid token | Verify token, refresh if needed |
| 403 | Forbidden | Insufficient permissions | Check user permissions on board/item |
| 404 | Not Found | Resource doesn't exist | Verify board_id/item_id is correct |
| 409 | Conflict | Resource conflict (e.g., duplicate) | Check if resource already exists |
| 429 | Too Many Requests | Rate limited | Wait and retry with exponential backoff |
| 500 | Server Error | Miro API error | Retry later, contact support if persistent |
| 503 | Service Unavailable | Service maintenance | Retry later |

## Error Response Format

All error responses include:
```json
{
  "code": 400,
  "message": "Invalid request",
  "details": {
    "param": "board_id",
    "reason": "Expected UUID format, got 'invalid'"
  }
}
```

## Common Errors

### 400 Bad Request - Invalid Parameter Format

**Problem:**
```json
{
  "code": 400,
  "message": "Invalid board_id format",
  "details": {"param": "board_id", "reason": "Expected UUID"}
}
```

**Solution:**
- Ensure board_id is valid UUID format
- Don't include special characters
- Example valid: `uXjVGAeRkgI=`

### 401 Unauthorized - Invalid Token

**Problem:**
```json
{
  "code": 401,
  "message": "Unauthorized"
}
```

**Solutions:**
- Token may be expired (OAuth tokens expire after 1 hour)
- Token may be revoked
- Token format incorrect (should be `Bearer <token>`)
- Check Authorization header: `Authorization: Bearer YOUR_TOKEN`

**For OAuth:**
```javascript
// Check if token expired
if (response.status === 401) {
  // Refresh token
  const newToken = await refreshOAuthToken(refreshToken);
  // Retry request with new token
}
```

### 403 Forbidden - Insufficient Permissions

**Problem:**
```json
{
  "code": 403,
  "message": "You do not have permission to access this board"
}
```

**Solutions:**
- User doesn't have access to the board
- Verify user is invited to board
- Check OAuth scopes include required permissions
- Board may be private/restricted

### 404 Not Found - Resource Doesn't Exist

**Problem:**
```json
{
  "code": 404,
  "message": "Board not found"
}
```

**Solutions:**
- Verify board_id is correct and still exists
- Board may have been deleted
- User may not have access to board
- Try listing boards to find correct ID

### 429 Too Many Requests - Rate Limited

**Problem:**
```json
{
  "code": 429,
  "message": "Rate limit exceeded"
}
```

**Solutions:**
- Check X-RateLimit-Remaining header
- Implement exponential backoff
- Batch operations to use fewer requests
- Cache responses locally
- Use webhooks instead of polling

**Exponential Backoff Example (JavaScript):**
```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429 && attempt < maxRetries) {
        const delay = Math.pow(2, attempt) * 1000; // 2s, 4s, 8s
        console.log(`Rate limited. Waiting ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
}

// Usage
const boards = await retryWithBackoff(() => miro.get('/boards'));
```

### 500 Internal Server Error

**Problem:**
```json
{
  "code": 500,
  "message": "Internal server error"
}
```

**Solutions:**
- Retry request (may be temporary)
- Check https://status.miro.com for incidents
- Contact Miro support if persistent
- Implement exponential backoff
- Log error for debugging

## Handling Errors in Code

### JavaScript/Node.js

```javascript
const miro = axios.create({
  baseURL: 'https://api.miro.com/v2',
  headers: {'Authorization': `Bearer ${TOKEN}`}
});

miro.interceptors.response.use(
  response => response,
  error => {
    const status = error.response?.status;
    const data = error.response?.data;
    
    switch (status) {
      case 400:
        console.error('Bad request:', data.details);
        break;
      case 401:
        console.error('Unauthorized - token may be expired');
        // Refresh token here
        break;
      case 403:
        console.error('Forbidden - no permission');
        break;
      case 404:
        console.error('Not found - check ID');
        break;
      case 429:
        console.error('Rate limited - wait before retrying');
        break;
      case 500:
        console.error('Server error - try again later');
        break;
      default:
        console.error(`Error ${status}:`, data.message);
    }
    
    throw error;
  }
);
```

### Python

```python
import requests
import time

def api_call_with_error_handling(method, endpoint, **kwargs):
    max_retries = 3
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.request(
                method,
                f'https://api.miro.com/v2{endpoint}',
                headers={'Authorization': f'Bearer {TOKEN}'},
                **kwargs
            )
            
            if response.status_code == 401:
                print("Token expired - need refresh")
                raise AuthError("Token expired")
            elif response.status_code == 403:
                print("No permission for this resource")
                raise PermissionError("Insufficient permissions")
            elif response.status_code == 404:
                print("Resource not found")
                raise ValueError("Resource not found")
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = base_delay ** (attempt + 1)
                    print(f"Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
            elif response.status_code >= 500:
                if attempt < max_retries - 1:
                    wait_time = base_delay ** (attempt + 1)
                    print(f"Server error. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise

# Usage
boards = api_call_with_error_handling('GET', '/boards')
```

## Debugging Tips

1. **Check Headers in Response**
   ```bash
   curl -i https://api.miro.com/v2/boards \
     -H "Authorization: Bearer TOKEN"
   ```
   Look for X-RateLimit-* headers

2. **Log Full Response**
   ```javascript
   console.log('Status:', response.status);
   console.log('Headers:', response.headers);
   console.log('Body:', response.data);
   ```

3. **Test in API Playground**
   - https://developers.miro.com/playground
   - Try requests before implementing

4. **Check Status Page**
   - https://status.miro.com
   - See if API is experiencing issues

5. **Verify Permissions**
   - User must be invited to board
   - Check OAuth scopes
   - Verify token hasn't been revoked

