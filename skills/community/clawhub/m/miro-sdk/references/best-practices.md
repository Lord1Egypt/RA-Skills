# Miro Web SDK - Best Practices

## Performance

### 1. Cache getAllItems()

```typescript
// SLOW - Multiple calls
const items1 = await miro.board.getAllItems();
const items2 = await miro.board.getAllItems();

// FAST - Cache result
let itemsCache = null;

async function getItems() {
  if (!itemsCache) {
    itemsCache = await miro.board.getAllItems();
  }
  return itemsCache;
}
```

### 2. Lazy Load Large Datasets

```typescript
// SLOW - Load everything
const allItems = await miro.board.getAllItems();

// FAST - Load as needed
async function* loadItemsLazy(pageSize = 100) {
  let offset = 0;
  let hasMore = true;
  
  while (hasMore) {
    const items = await miro.board.getAllItems();
    // Process items in batches
    yield items.slice(offset, offset + pageSize);
    
    offset += pageSize;
    hasMore = offset < items.length;
  }
}
```

### 3. Batch Operations

```typescript
// SLOW - Multiple API calls
for (const task of tasks) {
  await miro.board.createShape({...});
}

// FAST - Single batch operation
const shapes = await Promise.all(
  tasks.map(task => 
    miro.board.createShape({...})
  )
);
```

### 4. Event Listener Cleanup

```typescript
// DON'T - Memory leak
miro.board.events.on('item:create', handler);

// DO - Clean up
const handler = (event) => {...};
miro.board.events.on('item:create', handler);

// Later:
miro.board.events.off('item:create', handler);
```

### 5. Minimize Viewport Operations

```typescript
// SLOW - Update viewport frequently
for (let i = 0; i < 100; i++) {
  await miro.board.viewport.zoomIn();
}

// FAST - Single viewport operation
await miro.board.viewport.setViewport({
  zoomLevel: 3
});
```

## Security

### 1. Validate User Input

```typescript
// Validate before creating items
function validateShapeData(data) {
  if (!data.content || typeof data.content !== 'string') {
    throw new Error('Invalid content');
  }
  
  if (data.width < 10 || data.width > 10000) {
    throw new Error('Invalid width');
  }
  
  return true;
}

// Use in creation
const data = getUserInput();
validateShapeData(data);
await miro.board.createShape(data);
```

### 2. Check Permissions

```typescript
async function ensurePermission(scope) {
  try {
    // Attempt operation that requires scope
    await testOperation(scope);
    return true;
  } catch (error) {
    if (error.code === 'FORBIDDEN') {
      miro.ui.notify(`Missing ${scope} permission`);
      return false;
    }
    throw error;
  }
}
```

### 3. Sanitize External Data

```typescript
// Don't trust external APIs
async function importFromApi(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    
    // Validate structure
    if (!Array.isArray(data.items)) {
      throw new Error('Invalid data format');
    }
    
    // Sanitize content
    for (const item of data.items) {
      item.content = sanitizeHtml(item.content);
    }
    
    return data;
  } catch (error) {
    console.error('Import failed:', error);
    miro.ui.notify('Import failed', 'error');
  }
}
```

### 4. Secure Storage

```typescript
// Store sensitive data server-side
async function saveUserData(data) {
  // Don't store in localStorage
  // Send to secure backend
  const response = await fetch('/api/user-data', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  
  return response.json();
}
```

## User Experience

### 1. Provide Feedback

```typescript
// Show progress
miro.ui.notify('Processing...');

try {
  const items = await heavyOperation();
  miro.ui.notify('Done!');
} catch (error) {
  miro.ui.notify('Failed: ' + error.message, 'error');
}
```

### 2. Graceful Degradation

```typescript
async function createShapeWithFallback(data) {
  try {
    // Try with full styling
    return await miro.board.createShape({
      ...data,
      style: {
        fillColor: data.color,
        fontSize: 14,
        fontFamily: 'Arial'
      }
    });
  } catch (error) {
    // Fallback: minimal styling
    console.warn('Detailed styling failed, using defaults');
    return await miro.board.createShape({
      ...data,
      style: { fillColor: '#CCCCCC' }
    });
  }
}
```

### 3. Undo/Redo Support

```typescript
// Track changes for undo
class ChangeHistory {
  constructor() {
    this.history = [];
    this.currentIndex = -1;
  }
  
  push(change) {
    // Remove any redo history
    this.history = this.history.slice(0, this.currentIndex + 1);
    this.history.push(change);
    this.currentIndex++;
  }
  
  undo() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      return this.history[this.currentIndex];
    }
  }
  
  redo() {
    if (this.currentIndex < this.history.length - 1) {
      this.currentIndex++;
      return this.history[this.currentIndex];
    }
  }
}
```

## Code Organization

### 1. Modular Structure

```typescript
// helpers/board.ts
export async function getShapes() {
  return (await miro.board.getAllItems())
    .filter(item => item.type === 'SHAPE');
}

// helpers/ui.ts
export function showSuccess(message) {
  miro.ui.notify(message);
}

// index.ts
import { getShapes } from './helpers/board';
import { showSuccess } from './helpers/ui';

miro.onReady(async () => {
  const shapes = await getShapes();
  showSuccess(`Found ${shapes.length} shapes`);
});
```

### 2. Type Safety

```typescript
// types.ts
interface Shape {
  id: string;
  type: 'SHAPE';
  x: number;
  y: number;
  content: string;
}

// Use in code
async function processShapes(shapes: Shape[]) {
  for (const shape of shapes) {
    console.log(shape.content);
  }
}
```

### 3. Error Handling Hierarchy

```typescript
async function operation() {
  try {
    await miro.board.createShape({...});
  } catch (error) {
    if (error.code === 'FORBIDDEN') {
      handlePermissionError();
    } else if (error.code === 'INVALID_ARGUMENT') {
      handleValidationError(error);
    } else if (error.code === 'NETWORK_ERROR') {
      handleNetworkError();
    } else {
      handleUnknownError(error);
    }
  }
}
```

## Testing

### 1. Test with Developer Team

```typescript
// Use Developer team (sandbox)
// Limited to 3 boards, 5 users
// "Developer team" watermark visible
```

### 2. Mock API for Unit Tests

```typescript
// Mock SDK
const mockMiro = {
  board: {
    getInfo: jest.fn().mockResolvedValue({
      id: 'test-board',
      name: 'Test Board'
    }),
    createShape: jest.fn().mockResolvedValue({
      id: 'shape-1'
    })
  }
};

// Test code
test('creates shape', async () => {
  const shape = await mockMiro.board.createShape({});
  expect(shape.id).toBe('shape-1');
});
```

### 3. Integration Testing

```typescript
// Test with real board
describe('Board Integration', () => {
  it('creates and deletes shape', async () => {
    const shape = await miro.board.createShape({
      x: 0, y: 0, width: 100, height: 100, shape: 'rectangle'
    });
    
    expect(shape.id).toBeDefined();
    
    await shape.delete();
    
    const items = await miro.board.getAllItems();
    expect(items.find(i => i.id === shape.id)).toBeUndefined();
  });
});
```

## Monitoring & Logging

### 1. Error Tracking

```typescript
function setupErrorTracking() {
  window.addEventListener('error', (event) => {
    // Send to monitoring service
    fetch('/api/errors', {
      method: 'POST',
      body: JSON.stringify({
        message: event.message,
        stack: event.error?.stack,
        timestamp: new Date()
      })
    });
  });
}

// Initialize on startup
miro.onReady(() => {
  setupErrorTracking();
});
```

### 2. Performance Monitoring

```typescript
async function measurePerformance(fn) {
  const start = performance.now();
  
  try {
    const result = await fn();
    const duration = performance.now() - start;
    
    console.log(`Operation took ${duration.toFixed(2)}ms`);
    
    if (duration > 1000) {
      console.warn('Slow operation detected');
    }
    
    return result;
  } catch (error) {
    console.error('Operation failed:', error);
    throw error;
  }
}

// Usage
await measurePerformance(() => miro.board.getAllItems());
```

## Deployment

### 1. Environment Configuration

```typescript
const config = {
  development: {
    apiUrl: 'http://localhost:3000'
  },
  production: {
    apiUrl: 'https://api.example.com'
  }
};

const env = process.env.NODE_ENV || 'development';
export const API_URL = config[env].apiUrl;
```

### 2. Feature Flags

```typescript
const features = {
  newUI: process.env.FEATURE_NEW_UI === 'true',
  betaFeatures: process.env.FEATURE_BETA === 'true'
};

if (features.newUI) {
  loadNewUI();
} else {
  loadClassicUI();
}
```

