---
name: miro-sdk
description: Complete Miro Web SDK reference for building web plugins and desktop applications. Covers setup, core APIs (boards, shapes, text, items, selections, events), authentication, real-time collaboration, examples in TypeScript/JavaScript, best practices, and error handling.
---

# Miro Web SDK

The Miro Web SDK enables you to build web plugins that extend Miro's functionality. Create custom tools, automate workflows, and integrate external data directly into Miro boards.

## Quick Start

**Install SDK:**
```bash
npm install @mirohq/websdk-cli @mirohq/miro-webplugin
```

**Create Plugin:**
```bash
npm create @mirohq/websdk-cli my-plugin
cd my-plugin
npm start
```

**Hello World Plugin:**
```typescript
import { Board } from '@mirohq/miro-webplugin';

miro.onReady(async () => {
  console.log('Plugin ready!');
  
  // Get current board
  const board = await miro.board.getInfo();
  console.log('Board name:', board.name);
  
  // Listen for shape creation
  miro.board.events.on('item:create', (event) => {
    console.log('New item:', event.data);
  });
});
```

## Core Capabilities

### 1. Board Interaction
- Get board information (name, owner, size)
- Listen to real-time events (item creation, updates, deletions)
- Manage board selection and viewport
- Access board history and undo/redo

### 2. Create Items
- Shapes (rectangles, circles, diamonds, etc.)
- Text and rich text formatting
- Images and embeds
- Sticky notes and cards
- Frames and groups

### 3. Manipulate Items
- Move, resize, rotate items
- Change styling (colors, opacity, fonts)
- Update content and properties
- Apply connectors between shapes
- Delete items

### 4. Selection & Interaction
- Get selected items
- Listen to selection changes
- Programmatically select items
- Multi-select operations

### 5. User Interaction
- Viewport and zoom control
- Notification system
- Modal dialogs
- Context menus
- Keyboard shortcuts

### 6. Collaboration Features
- Real-time sync with other users
- User presence indicators
- Shared selections
- Live editing

### 7. Data Management
- Metadata and custom properties
- Board-level storage
- Plugin configuration
- Event tracking

### 8. Advanced Features
- Batch operations (bulk create/update)
- Search and filtering
- Viewport navigation
- Animation support
- Performance optimization

## SDK Platforms

### Web Plugin
Browser-based plugin running inside Miro app

**Install:**
```bash
npm install @mirohq/miro-webplugin
```

**Use:**
```typescript
import { Board, Ui } from '@mirohq/miro-webplugin';

// Access board
const board = await miro.board.getInfo();

// Create UI
miro.ui.openPanel({
  url: 'panel.html'
});
```

### Desktop App
Standalone desktop application using Electron

**Install:**
```bash
npm install @mirohq/miro-desktop
```

**Supported Platforms:**
- macOS
- Windows
- Linux

## Architecture

### Plugin Structure
```
my-plugin/
├── src/
│   ├── index.ts          # Main plugin code
│   ├── panel.html        # UI panel
│   ├── panel.ts          # Panel logic
│   └── styles.css        # Styling
├── manifest.json         # Plugin metadata
├── package.json
└── tsconfig.json
```

### Event Flow
```
User Action
  ↓
Browser/Electron
  ↓
Miro SDK
  ↓
Event Handler
  ↓
API Call
  ↓
Board Update
  ↓
Real-time Sync
```

## Authentication

### Web Plugin Auth
Uses implicit flow - user already logged into Miro

```typescript
miro.onReady(async () => {
  // User automatically authenticated
  const user = await miro.currentUser.get();
  console.log('Current user:', user.name);
});
```

### Scopes
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

**Available Scopes:**
- `board:read` - Read board data
- `board:write` - Create/edit items
- `board:history` - Access history
- `identity:read` - Get current user info

## Reference Files

See detailed documentation:
- `references/setup-installation.md` - Project setup and installation
- `references/core-apis.md` - Complete SDK API reference
- `references/authentication.md` - Auth patterns and scopes
- `references/examples.md` - TypeScript/JavaScript code examples
- `references/best-practices.md` - Performance, security, reliability
- `references/error-handling.md` - Error types and handling strategies

## API Overview

### Core Objects

```typescript
// Board
miro.board.getInfo()
miro.board.getAllItems()
miro.board.createShape(shape)
miro.board.getSelection()
miro.board.events

// Items
item.move(deltaX, deltaY)
item.resize(width, height)
item.update(updates)
item.delete()

// User
miro.currentUser.get()

// UI
miro.ui.openPanel()
miro.ui.openModal()
miro.ui.notifyWithButton()

// Viewport
miro.board.viewport.zoomIn()
miro.board.viewport.scrollTo()
```

## Events

```typescript
// Item events
miro.board.events.on('item:create', (event) => {})
miro.board.events.on('item:update', (event) => {})
miro.board.events.on('item:delete', (event) => {})

// Selection events
miro.board.events.on('selection:change', (event) => {})

// User events
miro.board.events.on('user:join', (event) => {})
miro.board.events.on('user:leave', (event) => {})
```

## Version History

**Latest:** 2.0+
**Support:** Web plugins, Desktop apps, Collaborative features

## Getting Help

- **Documentation:** https://developers.miro.com/docs
- **API Reference:** https://developers.miro.com/reference
- **GitHub:** https://github.com/miroapp/api-clients
- **Community:** https://community.miro.com
- **Support:** https://support.miro.com

## Tutorials

- Build your first plugin
- Create interactive shapes
- Real-time collaboration
- Data integration
- Performance optimization
- Testing and debugging

