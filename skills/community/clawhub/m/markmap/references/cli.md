# CLI

```bash
npm install -g markmap-cli
markmap README.md              → markmap.html
markmap README.md -o out.html  → Specify output
markmap README.md --open       → Generate and open
markmap README.md --offline    → Offline standalone HTML
markmap README.md --toolbar    → Add toolbar
cat README.md | markmap        → Pipe mode
markmap README.md --dev        → Dev server
markmap README.md --dev --port 8080
```

## Programmatic API

```ts
import { createMarkmap } from 'markmap-cli';
await createMarkmap({
  content, output: 'out.html', open: true,
  offline: false, toolbar: true, dev: false, port: 8080,
});
```

## Dev Server Architecture

```
Hono HTTP + chokidar file watcher
├─ GET /?key=<hash>          → HTML mindmap
├─ GET /~data?key=<hash>     → Long polling (10s timeout)
├─ GET /~client.*            → Client JS/CSS
└─ POST /~api                → setContent/setCursor
```

Content change → Transformer.transform() → push new root+frontmatter. FileSystemProvider watches files automatically.

```ts
import { develop } from 'markmap-cli';
const dev = await develop({ port: 8080, toolbar: true });
dev.addProvider({ filePath: 'README.md' });     // File watch
dev.addProvider({ key: 'doc1' });               // Manual control
dev.addProvider({ key: 'doc1' }).setContent('# New');
```

## Toolbar

`--toolbar` adds markmap-toolbar (zoom/fit buttons):

```ts
const toolbar = new markmap.Toolbar();
toolbar.attach(mm);
toolbar.render(); // Insert in bottom-right corner
```

## Environment Variables

`ZERO_NATIVE_FRONTEND_URL` `ZERO_NATIVE_LOG_DIR` `ZERO_NATIVE_LOG_FORMAT`