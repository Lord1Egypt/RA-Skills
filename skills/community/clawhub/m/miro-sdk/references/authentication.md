# Miro Web SDK - Authentication

## Web Plugin Authentication

Web plugins use implicit authentication - no login flow needed. User already logged into Miro.

### Check if Ready

```typescript
miro.onReady(() => {
  // Plugin is ready
  // User is authenticated
});
```

### Get Current User

```typescript
const user = await miro.currentUser.get();
console.log(user.name, user.email);
```

## Scopes

Define what your plugin can do:

```json
{
  "requiredScopes": [
    "board:read",
    "board:write",
    "identity:read"
  ]
}
```

### Available Scopes

| Scope | Permission |
|-------|-----------|
| `board:read` | Read board data and items |
| `board:write` | Create, edit, delete items |
| `board:history` | Access undo/redo history |
| `identity:read` | Get current user info |
| `identity:write` | Update user profile |

### Scope Dialog

When plugin installs, user sees scope permissions:

```
"My Plugin" is requesting access to:
✓ Read your boards
✓ Create and edit items
✓ Your profile information
```

User must accept to continue.

## Authorization Flow

```
1. User opens plugin
    ↓
2. Browser checks Miro auth
    ↓
3. If not logged in → Miro login
    ↓
4. Check plugin scopes
    ↓
5. If first time → Show permissions dialog
    ↓
6. User accepts
    ↓
7. Plugin loads with access
```

## Handling Unauthorized

```typescript
miro.onReady(async () => {
  try {
    const board = await miro.board.getInfo();
  } catch (error) {
    if (error.code === 'FORBIDDEN') {
      // Insufficient permissions
      console.log('Need board:read scope');
    }
  }
});
```

## Token Management

**SDK handles tokens automatically** - no manual management needed.

### Behind the Scenes

```
miro.board.getInfo()
  ↓
SDK gets access token
  ↓
API request with token
  ↓
Response
```

## Offline Support

Plugin still works when user goes offline:

```typescript
miro.onReady(() => {
  // Can read local cache
  const items = miro.board.getAllItems(); // From cache
  
  // Write operations queue for sync
  miro.board.createShape({...}); // Queued
  
  // When back online, syncs automatically
});
```

## Multi-User Auth

Each user has own context:

```typescript
const user = await miro.currentUser.get();
// Returns logged-in user only
// No access to other users' credentials
```

## Security Practices

### DO

- ✅ Request minimal required scopes
- ✅ Handle auth errors gracefully
- ✅ Validate user permissions
- ✅ Use HTTPS for plugin URL
- ✅ Store secure data server-side

### DON'T

- ❌ Don't store tokens in localStorage
- ❌ Don't request unnecessary scopes
- ❌ Don't expose user data publicly
- ❌ Don't use HTTP (use HTTPS only)
- ❌ Don't hardcode credentials

## Testing Auth

### Test with Developer Team

1. Create Developer team (sandbox)
2. Install plugin in Developer team
3. Test with multiple users if needed
4. 5 collaborator limit for testing

### Permissions Testing

```typescript
async function testScopes() {
  try {
    // Will fail if scope not granted
    await miro.board.createShape({
      x: 0,
      y: 0,
      width: 100,
      height: 100,
      shape: 'rectangle'
    });
  } catch (error) {
    if (error.code === 'FORBIDDEN') {
      console.log('Need board:write scope');
    }
  }
}
```

## Marketplace Auth

For published apps on Miro Marketplace:

1. OAuth consent screen required
2. User reviews scopes
3. Token flow same as development
4. No additional setup needed

## Troubleshooting

### Plugin says "Not Authorized"
- Check scopes in manifest.json
- Try reinstalling plugin
- Check user has board access

### Can't read board data
- Verify `board:read` scope
- Check if board exists
- User might not have access

### Scope not appearing
- Update manifest.json
- Reinstall plugin
- Clear browser cache

### User profile access denied
- Check `identity:read` scope
- May be privacy setting issue

