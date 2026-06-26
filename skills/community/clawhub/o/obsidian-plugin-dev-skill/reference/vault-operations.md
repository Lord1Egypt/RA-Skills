# Vault & File Operations

## Reading Files

```typescript
// Read file content (cached — preferred for display)
const content = await this.app.vault.cachedRead(file)

// Read file content (uncached — for edit operations)
const content = await this.app.vault.read(file)
```

**Use `cachedRead()` when:**
- Displaying file content in views
- Reading file for non-editing purposes
- Performance matters (avoids disk I/O)

**Use `read()` when:**
- You need the absolute latest content
- You're about to modify the file

## Writing Files

### Background File Edits (Recommended)

```typescript
// Atomic operation — safe with concurrent edits
await this.app.vault.process(file, (data) => {
  return data.replace('old', 'new')
})
```

### Active File Edits (Editor API)

```typescript
// If file is open in editor, use Editor API instead
const view = this.app.workspace.getActiveViewOfType(MarkdownView)
if (view) {
  const editor = view.editor
  editor.replaceSelection('new text')
  // Or:
  editor.replaceRange('text', { line: 0, ch: 0 }, { line: 0, ch: 5 })
}
```

### Direct Modify (Avoid)

```typescript
// Avoid this — use vault.process() instead
await this.app.vault.modify(file, newContent)
// Reason: not atomic; concurrent edits can corrupt data
```

## Creating Files

```typescript
// Create file
const file = await this.app.vault.create('path/to/file.md', '# Hello')

// Create folder (recursive)
await this.app.vault.createFolder('path/to/folder')
```

## Deleting Files

```typescript
// Trash (respects user preference: trash vs permanent delete)
await this.app.fileManager.trashFile(file)

// Permanent delete (use with caution)
await this.app.vault.delete(file)
```

## Renaming Files

```typescript
// Rename/move file — automatically updates all links
await this.app.fileManager.renameFile(file, 'new/path/file.md')
```

## Path Operations

```typescript
import { normalizePath, TFile, TFolder, TAbstractFile } from 'obsidian'

// Normalize user-provided paths
const safePath = normalizePath(userInput)

// Get file/folder by path
const file = this.app.vault.getFileByPath('path/to/file.md')
const folder = this.app.vault.getFolderByPath('path/to/folder')

// Get abstract file (file or folder)
const abstract = this.app.vault.getAbstractFileByPath('path')

// Type checking
if (abstract instanceof TFile) {
  // It's a file
}
if (abstract instanceof TFolder) {
  // It's a folder
}
```

## Listing Files

```typescript
// All markdown files
const files = this.app.vault.getMarkdownFiles()

// All files (including non-markdown)
const allFiles = this.app.vault.getFiles()

// All folders
const folders = this.app.vault.getAllFolders()

// Files in a specific folder
const folder = this.app.vault.getFolderByPath('my-folder')
if (folder) {
  const children = folder.children  // TAbstractFile[]
}
```

## Frontmatter

```typescript
// Read frontmatter
const cache = this.app.metadataCache.getFileCache(file)
const frontmatter = cache?.frontmatter

if (frontmatter) {
  const title = frontmatter.title
  const tags = frontmatter.tags
  const aliases = frontmatter.aliases
}

// Write frontmatter (ALWAYS use this — never parse YAML manually)
await this.app.fileManager.processFrontMatter(file, (fm) => {
  fm.title = 'New Title'
  fm.tags = ['tag1', 'tag2']
  // Delete a property:
  delete fm.oldProperty
})
```

### Resolved Frontmatter

```typescript
// Gets frontmatter with inheritance from parent folders (if using folder notes)
const resolved = this.app.metadataCache.getFileCache(file)?.frontmatter
// Properties from folder notes are merged in
```

## Links & Backlinks

```typescript
// Get resolved links (all outgoing links)
const resolvedLinks = this.app.metadataCache.resolvedLinks
const fileLinks = resolvedLinks[file.path]  // Record<path, count>

// Get backlinks (files that link to this file)
const backlinks = this.app.metadataCache.getBacklinksForFile(file)
for (const [path, links] of backlinks.data) {
  console.log(`${path} links to ${file.path}`)
}
```

## Events with Debouncing

```typescript
import { debounce } from 'obsidian'

// Debounced handler — prevents rapid re-execution
const onModify = debounce(
  (file: TFile) => {
    console.log('File modified:', file.path)
  },
  1000,  // Wait 1 second after last event
  false  // true = leading edge, false = trailing edge
)

this.registerEvent(this.app.vault.on('modify', onModify))

// Don't forget to cancel debounce on unload
this.register(() => onModify.cancel())
```

## File-Level Caching Pattern

```typescript
// Cache parsed data per-file path
const fileCache = new Map<string, ParsedData>()

function getFileData(file: TFile): ParsedData {
  const cached = fileCache.get(file.path)
  if (cached) return cached

  const data = parseFileSync(file)
  fileCache.set(file.path, data)
  return data
}

// Invalidate on modify
this.registerEvent(this.app.vault.on('modify', (file) => {
  if (file instanceof TFile) {
    fileCache.delete(file.path)  // Only invalidate this file
  }
}))

// Invalidate all on rename
this.registerEvent(this.app.vault.on('rename', (file, oldPath) => {
  fileCache.delete(oldPath)
}))
```

## Reading Mode vs Editor

```typescript
// Get content from the editor (active editing session)
const editor = this.app.workspace.activeEditor?.editor
if (editor) {
  const content = editor.getValue()       // Full content
  const selection = editor.getSelection() // Selected text
  const cursor = editor.getCursor()       // Cursor position
}

// Get content from file (disk/cached)
const content = await this.app.vault.cachedRead(file)
```

## Best Practices

1. **`vault.process()` > `vault.modify()`** — atomic, concurrent-safe
2. **`cachedRead()` for display** — avoids disk I/O
3. **`processFrontMatter()` for YAML** — never manual parse
4. **`fileManager.trashFile()` for delete** — respects user preference
5. **`normalizePath()` for user paths** — cross-platform safety
6. **Debounce modify handlers** — files change rapidly
7. **Use `instanceof TFile`** — never cast with `as`
8. **Invalidate caches on events** — modify, delete, rename
