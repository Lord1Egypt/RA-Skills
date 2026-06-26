# Miro Web SDK - Error Handling

## Error Types

### Permission Errors

**Code:** `FORBIDDEN`

```typescript
try {
  await miro.board.createShape({...});
} catch (error) {
  if (error.code === 'FORBIDDEN') {
    // User doesn't have required scope
    miro.ui.notify('Missing board:write permission');
  }
}
```

**Solutions:**
- Check scopes in manifest.json
- Reinstall plugin to request permissions
- User needs to accept scope dialog

### Validation Errors

**Code:** `INVALID_ARGUMENT`

```typescript
try {
  await miro.board.createShape({
    x: 'invalid', // Should be number
    y: 0,
    width: 100,
    height: 100
  });
} catch (error) {
  if (error.code === 'INVALID_ARGUMENT') {
    console.error('Invalid shape data:', error.message);
  }
}
```

**Common causes:**
- Wrong data type
- Missing required fields
- Out of range values

### Item Not Found

**Code:** `NOT_FOUND`

```typescript
try {
  await miro.board.getItem('non-existent-id');
} catch (error) {
  if (error.code === 'NOT_FOUND') {
    console.log('Item was deleted or ID is wrong');
  }
}
```

**Solutions:**
- Verify item ID is correct
- Item may have been deleted
- Check board.getAllItems() for valid IDs

### Network Errors

**Code:** `NETWORK_ERROR`

```typescript
try {
  const items = await miro.board.getAllItems();
} catch (error) {
  if (error.code === 'NETWORK_ERROR') {
    miro.ui.notify('Connection lost. Please try again.');
  }
}
```

**Handling:**
- Implement retry logic
- Show offline message
- Queue operations for later

### Rate Limit

**Code:** `RATE_LIMIT`

```typescript
try {
  // Make many API calls
  for (let i = 0; i < 1000; i++) {
    await miro.board.createShape({...});
  }
} catch (error) {
  if (error.code === 'RATE_LIMIT') {
    console.log('Too many requests. Wait before retrying.');
  }
}
```

**Solutions:**
- Implement exponential backoff
- Batch operations
- Use Promise.all() for parallel requests

## Error Handling Patterns

### Basic Try-Catch

```typescript
async function createShape(data) {
  try {
    const shape = await miro.board.createShape(data);
    return shape;
  } catch (error) {
    console.error('Failed to create shape:', error);
    miro.ui.notify('Failed to create shape', 'error');
    throw error;
  }
}
```

### Retry with Backoff

```typescript
async function retryWithBackoff(fn, maxRetries = 3) {
  let lastError;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      // Only retry on network/rate limit errors
      if (error.code !== 'NETWORK_ERROR' && 
          error.code !== 'RATE_LIMIT') {
        throw error;
      }
      
      // Exponential backoff
      const delay = Math.pow(2, attempt) * 1000;
      await new Promise(r => setTimeout(r, delay));
    }
  }
  
  throw lastError;
}

// Usage
const shape = await retryWithBackoff(() => 
  miro.board.createShape({...})
);
```

### Error Recovery

```typescript
async function createShapeWithFallback(data) {
  try {
    // Try with full options
    return await miro.board.createShape({
      ...data,
      style: {
        fillColor: '#FF0000',
        fontSize: 16
      }
    });
  } catch (error) {
    if (error.code === 'INVALID_ARGUMENT') {
      // Fallback: minimal options
      try {
        return await miro.board.createShape({
          x: data.x || 0,
          y: data.y || 0,
          width: data.width || 100,
          height: data.height || 100,
          shape: 'rectangle'
        });
      } catch (fallbackError) {
        miro.ui.notify('Failed to create shape', 'error');
        throw fallbackError;
      }
    }
    throw error;
  }
}
```

### Validation Before API Call

```typescript
interface ShapeData {
  x: number;
  y: number;
  width: number;
  height: number;
  shape: string;
  content?: string;
}

function validateShape(data: any): data is ShapeData {
  if (typeof data.x !== 'number' || data.x < -50000 || data.x > 50000) {
    throw new Error('Invalid x coordinate');
  }
  
  if (typeof data.y !== 'number' || data.y < -50000 || data.y > 50000) {
    throw new Error('Invalid y coordinate');
  }
  
  if (typeof data.width !== 'number' || data.width < 10) {
    throw new Error('Invalid width');
  }
  
  if (typeof data.height !== 'number' || data.height < 10) {
    throw new Error('Invalid height');
  }
  
  const validShapes = ['rectangle', 'circle', 'diamond', 'triangle'];
  if (!validShapes.includes(data.shape)) {
    throw new Error('Invalid shape type');
  }
  
  return true;
}

async function createShape(data: any) {
  try {
    validateShape(data);
    return await miro.board.createShape(data);
  } catch (error) {
    miro.ui.notify('Invalid shape data: ' + error.message, 'error');
    throw error;
  }
}
```

### Error Context Tracking

```typescript
class ErrorContext {
  private context: Record<string, any> = {};
  
  set(key: string, value: any) {
    this.context[key] = value;
  }
  
  get() {
    return { ...this.context };
  }
  
  async run<T>(fn: () => Promise<T>, contextData: Record<string, any>) {
    const previous = this.context;
    this.context = { ...previous, ...contextData };
    
    try {
      return await fn();
    } catch (error) {
      console.error('Error with context:', {
        error: error.message,
        context: this.context
      });
      throw error;
    } finally {
      this.context = previous;
    }
  }
}

const errorContext = new ErrorContext();

// Usage
await errorContext.run(
  () => miro.board.createShape({...}),
  { userId: 'user-123', boardId: 'board-456' }
);
```

## Specific Error Scenarios

### User Offline

```typescript
function setupOfflineHandling() {
  const queue = [];
  
  window.addEventListener('offline', () => {
    miro.ui.notify('You are offline');
  });
  
  window.addEventListener('online', async () => {
    miro.ui.notify('Back online! Syncing...');
    
    while (queue.length > 0) {
      const operation = queue.shift();
      try {
        await operation();
      } catch (error) {
        queue.unshift(operation); // Re-queue
        break;
      }
    }
  });
}
```

### Concurrent Modifications

```typescript
async function handleConcurrentEdit() {
  try {
    await item.update({ content: 'New content' });
  } catch (error) {
    if (error.code === 'CONFLICT') {
      // Item was modified by someone else
      miro.ui.notifyWithButton(
        'Item was modified by another user',
        {
          action: {
            title: 'Reload',
            callback: async () => {
              const updated = await miro.board.getItem(item.id);
              console.log('Reloaded:', updated);
            }
          }
        }
      );
    }
  }
}
```

### Selection Changed

```typescript
async function deleteSelected() {
  const original = await miro.board.getSelection();
  
  if (original.length === 0) {
    miro.ui.notify('Nothing selected');
    return;
  }
  
  for (const item of original) {
    try {
      await item.delete();
    } catch (error) {
      if (error.code === 'NOT_FOUND') {
        // Item already deleted
        console.log('Item already deleted:', item.id);
      } else {
        throw error;
      }
    }
  }
}
```

## Monitoring & Debugging

### Error Logging

```typescript
class ErrorLogger {
  private logs: any[] = [];
  
  log(error: Error, context?: Record<string, any>) {
    this.logs.push({
      message: error.message,
      code: error.code,
      stack: error.stack,
      context,
      timestamp: new Date()
    });
    
    // Send to server
    this.flushIfNeeded();
  }
  
  private async flushIfNeeded() {
    if (this.logs.length > 10) {
      const logs = this.logs.splice(0, 10);
      await fetch('/api/logs', {
        method: 'POST',
        body: JSON.stringify(logs)
      }).catch(console.error);
    }
  }
}

const errorLogger = new ErrorLogger();

// Usage
try {
  // Operation
} catch (error) {
  errorLogger.log(error, { userId: 'user-123' });
}
```

### Error Boundaries

```typescript
// React-like error boundary for Miro SDK
class ErrorBoundary {
  constructor(private onError?: (error: Error) => void) {}
  
  async wrap<T>(fn: () => Promise<T>): Promise<T | null> {
    try {
      return await fn();
    } catch (error) {
      console.error('Error boundary caught:', error);
      
      if (this.onError) {
        this.onError(error as Error);
      }
      
      miro.ui.notify('An error occurred. Please try again.', 'error');
      return null;
    }
  }
}

const boundary = new ErrorBoundary(error => {
  console.error('Global error:', error);
});

// Usage
await boundary.wrap(() => miro.board.createShape({...}));
```

