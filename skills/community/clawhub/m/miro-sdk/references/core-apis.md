# Miro Web SDK - Core APIs Reference

## Board API

### Get Board Info

```typescript
const board = await miro.board.getInfo();
// Returns:
// {
//   id: "board-id",
//   name: "Board Name",
//   owner: { id: "user-id", email: "user@example.com" },
//   createdAt: "2024-01-15T10:30:00Z",
//   updatedAt: "2024-01-20T14:45:00Z",
//   isPublic: false
// }
```

### Get All Items

```typescript
const items = await miro.board.getAllItems();
// Returns array of all board items

// With filter
const shapes = await miro.board.getAllItems({
  type: ['SHAPE']
});
```

### Get Items by ID

```typescript
const item = await miro.board.getItem('item-id');
```

### Get Selection

```typescript
const selected = await miro.board.getSelection();
// Returns array of selected items
```

### Set Selection

```typescript
await miro.board.select(['item-id-1', 'item-id-2']);
```

### Clear Selection

```typescript
await miro.board.deselect();
```

## Item Creation

### Create Shape

```typescript
const shape = await miro.board.createShape({
  x: 0,
  y: 0,
  width: 300,
  height: 200,
  shape: 'rectangle',
  style: {
    fillColor: '#FF0000',
    fillOpacity: 0.8,
    strokeColor: '#000000',
    strokeWidth: 2,
    fontSize: 14
  },
  content: 'My Shape'
});
```

**Shape Types:**
- `rectangle`, `circle`, `diamond`
- `triangle`, `pentagon`, `hexagon`
- `line`, `arrow`, `flowchart_*`

### Create Text

```typescript
const text = await miro.board.createText({
  x: 100,
  y: 100,
  content: 'Hello World',
  style: {
    color: '#000000',
    fontSize: 24,
    fontFamily: 'Arial',
    textAlign: 'center'
  }
});
```

### Create Sticky Note

```typescript
const sticky = await miro.board.createShape({
  x: 200,
  y: 200,
  shape: 'sticky',
  style: {
    fillColor: '#FFFF00'
  },
  content: 'To do: Review design'
});
```

### Create Image

```typescript
const image = await miro.board.createImage({
  x: 0,
  y: 0,
  width: 400,
  height: 300,
  url: 'https://example.com/image.jpg'
});
```

### Create Connector

```typescript
const connector = await miro.board.createConnector({
  startItem: sourceShape,
  endItem: targetShape,
  captions: ['label'],
  style: {
    strokeColor: '#0000FF',
    strokeWidth: 2
  }
});
```

## Item Manipulation

### Update Item

```typescript
await item.update({
  x: 100,
  y: 100,
  width: 400,
  height: 300,
  content: 'Updated content',
  style: {
    fillColor: '#00FF00'
  }
});
```

### Move Item

```typescript
await item.move(100, 50); // deltaX, deltaY
```

### Resize Item

```typescript
await item.resize(500, 400); // width, height
```

### Rotate Item

```typescript
await item.rotate(45); // degrees
```

### Delete Item

```typescript
await item.delete();
```

### Batch Delete

```typescript
const items = await miro.board.getAllItems();
await Promise.all(items.map(item => item.delete()));
```

## Item Properties

```typescript
// Read properties
console.log(item.id);
console.log(item.type); // 'SHAPE', 'TEXT', 'IMAGE', etc.
console.log(item.x, item.y); // Position
console.log(item.width, item.height); // Dimensions
console.log(item.rotation); // Rotation angle
console.log(item.content); // Text content
console.log(item.style); // Style properties
console.log(item.metadata); // Custom data

// Custom metadata
item.metadata.customField = 'value';
await item.update({ metadata: item.metadata });
```

## Events

### Listen to Item Events

```typescript
// Item created
miro.board.events.on('item:create', (event) => {
  console.log('New item:', event.data);
});

// Item updated
miro.board.events.on('item:update', (event) => {
  console.log('Updated:', event.data);
});

// Item deleted
miro.board.events.on('item:delete', (event) => {
  console.log('Deleted:', event.data.id);
});
```

### Selection Events

```typescript
miro.board.events.on('selection:change', (event) => {
  console.log('Selected:', event.data);
});
```

### User Presence

```typescript
miro.board.events.on('user:join', (event) => {
  console.log('User joined:', event.data.name);
});

miro.board.events.on('user:leave', (event) => {
  console.log('User left:', event.data.name);
});
```

### Remove Listeners

```typescript
const handler = (event) => console.log(event);
miro.board.events.on('item:create', handler);

// Later:
miro.board.events.off('item:create', handler);
```

## Viewport API

### Get Viewport

```typescript
const viewport = await miro.board.viewport.get();
// {
//   x, y: Position
//   width, height: Size
//   zoomLevel: number (0.1 - 5.0)
// }
```

### Set Viewport

```typescript
await miro.board.viewport.setViewport({
  x: 0,
  y: 0,
  zoomLevel: 1
});
```

### Zoom

```typescript
await miro.board.viewport.zoomIn(); // 1.5x
await miro.board.viewport.zoomOut(); // 0.7x
await miro.board.viewport.zoomToFit(items); // Fit items
```

### Scroll

```typescript
await miro.board.viewport.scrollTo({ x: 100, y: 100 });
```

## User API

### Get Current User

```typescript
const user = await miro.currentUser.get();
// {
//   id: "user-id",
//   name: "John Doe",
//   email: "john@example.com",
//   picture: "https://..."
// }
```

## UI API

### Open Side Panel

```typescript
miro.ui.openPanel({
  url: 'panel.html',
  width: 300
});
```

### Open Modal

```typescript
const result = await miro.ui.openModal({
  url: 'modal.html',
  width: 400,
  height: 300
});
```

### Notifications

```typescript
// Simple notification
miro.ui.notify('Task completed!');

// With button
miro.ui.notifyWithButton('Undo?', {
  action: {
    title: 'Undo',
    callback: () => {
      // Handle undo
    }
  }
});

// Error notification
miro.ui.notify('Something went wrong', 'error');
```

### Context Menu

```typescript
miro.board.ui.on('contextmenu', (event) => {
  event.preventDefault();
  // Show custom menu
});
```

## Storage API

### Get/Set Data

```typescript
// Board-level storage
const data = await miro.board.info.getAllMeta();
await miro.board.info.setMeta('key', { value: 'data' });

// User-level storage
const userMeta = await miro.currentUser.getMeta('key');
await miro.currentUser.setMeta('key', { value: 'data' });
```

## Keyboard Shortcuts

```typescript
miro.board.ui.on('keydown', (event) => {
  if (event.key === 'Enter' && event.ctrlKey) {
    // Ctrl+Enter pressed
    handleSubmit();
  }
});
```

## Search & Filter

```typescript
const items = await miro.board.getAllItems({
  type: ['SHAPE', 'TEXT'],
  query: 'Task' // Search content
});
```

## Batch Operations

```typescript
// Create multiple items efficiently
const newItems = await miro.board.batch(async () => {
  const shape1 = await miro.board.createShape({...});
  const shape2 = await miro.board.createShape({...});
  return [shape1, shape2];
});
```

## Performance Tips

- Cache getAllItems() results
- Use event listeners instead of polling
- Batch item creation
- Limit event listener scope
- Clean up listeners when done

