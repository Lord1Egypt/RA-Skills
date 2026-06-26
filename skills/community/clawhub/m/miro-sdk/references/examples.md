# Miro Web SDK - Code Examples

## TypeScript/JavaScript Setup

### Basic Plugin

```typescript
import { Board } from '@mirohq/miro-webplugin';

miro.onReady(async () => {
  console.log('Plugin is ready');
  
  // Get current board info
  const board = await miro.board.getInfo();
  console.log('Current board:', board.name);
});
```

### Create Shape

```typescript
const shape = await miro.board.createShape({
  x: 0,
  y: 0,
  width: 300,
  height: 200,
  shape: 'rectangle',
  style: {
    fillColor: '#FF6B6B',
    fillOpacity: 0.8,
    strokeColor: '#000000',
    strokeWidth: 2,
    fontSize: 16
  },
  content: 'Hello Miro!'
});

console.log('Created shape:', shape.id);
```

### Create Multiple Shapes

```typescript
async function createTaskBoard() {
  const tasks = [
    'Design',
    'Development', 
    'Testing',
    'Deployment'
  ];
  
  let x = 0;
  const shapes = [];
  
  for (const task of tasks) {
    const shape = await miro.board.createShape({
      x: x,
      y: 0,
      width: 200,
      height: 150,
      shape: 'rectangle',
      style: { fillColor: '#4A90E2' },
      content: task
    });
    
    shapes.push(shape);
    x += 250; // Space them out
  }
  
  return shapes;
}

await createTaskBoard();
```

### Listen to Events

```typescript
miro.board.events.on('item:create', (event) => {
  console.log('New item created:', event.data);
});

miro.board.events.on('item:update', (event) => {
  console.log('Item updated:', event.data);
});

miro.board.events.on('selection:change', (event) => {
  console.log('Selection changed:', event.data);
});
```

### Process Selected Items

```typescript
async function processSelection() {
  const selected = await miro.board.getSelection();
  
  for (const item of selected) {
    if (item.type === 'SHAPE') {
      // Change color
      await item.update({
        style: {
          fillColor: '#00FF00'
        }
      });
      
      // Move down
      await item.move(0, 100);
    }
  }
}
```

### Create Side Panel

**main.ts:**
```typescript
async function openPanel() {
  miro.ui.openPanel({
    url: 'panel.html',
    width: 300
  });
}

// Button listener
document.getElementById('open-panel').addEventListener('click', openPanel);
```

**panel.html:**
```html
<div id="panel">
  <h2>Task Creator</h2>
  <input id="task-input" type="text" placeholder="Task name">
  <button id="create-btn">Create Task</button>
</div>

<script>
  document.getElementById('create-btn').addEventListener('click', async () => {
    const input = document.getElementById('task-input');
    const taskName = input.value;
    
    // Create shape in main board
    await miro.board.createShape({
      x: 0,
      y: 0,
      width: 200,
      height: 100,
      shape: 'sticky',
      content: taskName
    });
    
    input.value = '';
  });
</script>
```

### Real-time Collaboration

```typescript
miro.board.events.on('user:join', (event) => {
  console.log(`${event.data.name} joined the board`);
  
  // Show notification
  miro.ui.notify(`Welcome ${event.data.name}!`);
});

miro.board.events.on('item:create', (event) => {
  // Show who created what
  const creator = event.data.createdBy?.name || 'Unknown';
  console.log(`${creator} created ${event.data.type}`);
});
```

### Search and Filter

```typescript
async function findAllTasks() {
  const items = await miro.board.getAllItems();
  
  const tasks = items.filter(item => 
    item.type === 'SHAPE' && 
    item.content?.includes('TODO')
  );
  
  console.log('Found tasks:', tasks.length);
  return tasks;
}

const tasks = await findAllTasks();
await miro.board.select(tasks.map(t => t.id));
```

### Export Board Data

```typescript
async function exportBoardData() {
  const items = await miro.board.getAllItems();
  
  const data = items.map(item => ({
    id: item.id,
    type: item.type,
    content: item.content,
    position: { x: item.x, y: item.y },
    size: { width: item.width, height: item.height }
  }));
  
  // Download as JSON
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = 'board-export.json';
  a.click();
}
```

### Custom Menu

```typescript
document.addEventListener('contextmenu', (event) => {
  event.preventDefault();
  
  // Show custom context menu
  const menu = document.createElement('div');
  menu.className = 'custom-menu';
  menu.style.position = 'absolute';
  menu.style.left = event.clientX + 'px';
  menu.style.top = event.clientY + 'px';
  
  menu.innerHTML = `
    <div class="menu-item" data-action="copy">Copy</div>
    <div class="menu-item" data-action="paste">Paste</div>
    <div class="menu-item" data-action="delete">Delete</div>
  `;
  
  document.body.appendChild(menu);
  
  menu.addEventListener('click', (e) => {
    const action = e.target.dataset.action;
    handleMenuAction(action);
  });
});
```

### Data Persistence

```typescript
async function savePluginData() {
  const board = await miro.board.getInfo();
  
  const data = {
    timestamp: new Date(),
    boardId: board.id,
    settings: {
      theme: 'dark',
      autoSave: true
    }
  };
  
  // Store in board metadata
  await miro.board.info.setMeta('plugin-settings', data);
}

async function loadPluginData() {
  const data = await miro.board.info.getMeta('plugin-settings');
  console.log('Loaded settings:', data);
  return data;
}
```

### Error Handling

```typescript
async function safeCreateShape(shapeData) {
  try {
    const shape = await miro.board.createShape(shapeData);
    miro.ui.notify('Shape created successfully!');
    return shape;
  } catch (error) {
    if (error.code === 'INVALID_ARGUMENT') {
      miro.ui.notify('Invalid shape data', 'error');
    } else if (error.code === 'FORBIDDEN') {
      miro.ui.notify('You don\'t have permission', 'error');
    } else {
      miro.ui.notify('Failed to create shape', 'error');
      console.error(error);
    }
  }
}
```

### Keyboard Shortcuts

```typescript
document.addEventListener('keydown', (event) => {
  // Ctrl+S or Cmd+S
  if ((event.ctrlKey || event.metaKey) && event.key === 's') {
    event.preventDefault();
    saveBoard();
  }
  
  // Delete key
  if (event.key === 'Delete') {
    deleteSelected();
  }
});

async function deleteSelected() {
  const selected = await miro.board.getSelection();
  await Promise.all(selected.map(item => item.delete()));
}
```

### Batch Operations

```typescript
async function createWorkflow() {
  // Create multiple connected shapes
  const shapes = [];
  const positions = [
    { x: 0, y: 0, label: 'Start' },
    { x: 300, y: 0, label: 'Process' },
    { x: 600, y: 0, label: 'End' }
  ];
  
  for (const pos of positions) {
    const shape = await miro.board.createShape({
      x: pos.x,
      y: pos.y,
      width: 150,
      height: 100,
      shape: 'rectangle',
      content: pos.label
    });
    shapes.push(shape);
  }
  
  // Connect shapes
  for (let i = 0; i < shapes.length - 1; i++) {
    await miro.board.createConnector({
      startItem: shapes[i],
      endItem: shapes[i + 1]
    });
  }
}
```

### Performance Optimization

```typescript
// Cache board data
let cachedItems = null;

async function getItemsCached() {
  if (!cachedItems) {
    cachedItems = await miro.board.getAllItems();
  }
  return cachedItems;
}

// Invalidate cache on changes
miro.board.events.on('item:create', () => {
  cachedItems = null;
});

miro.board.events.on('item:update', () => {
  cachedItems = null;
});

miro.board.events.on('item:delete', () => {
  cachedItems = null;
});
```

