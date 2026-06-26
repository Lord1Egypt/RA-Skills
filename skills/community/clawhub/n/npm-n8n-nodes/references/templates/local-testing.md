# Local Testing

## Table of Contents
1. [npm link workflow](#1-npm-link-workflow)
2. [n8n custom folder locations](#2-n8n-custom-folder-locations)
3. [Using the official starter with hot reload](#3-hot-reload-dev-mode)
4. [Testing in Docker](#4-testing-in-docker)
5. [Debugging tips](#5-debugging-tips)

---

## 1. npm link Workflow

The standard way to test locally without publishing:

```bash
# 1. Build the node
npm run build

# 2. Register it globally on your machine
npm link

# 3. Navigate to n8n's custom node folder
#    (create the folder if it doesn't exist)
cd ~/.n8n/custom

# 4. Link your package into n8n's custom folder
npm link n8n-nodes-yourservice

# 5. Start n8n
n8n start
# → Open http://localhost:5678
# → Your node should appear in the node picker
```

After making changes:
```bash
# In your package directory:
npm run build   # recompile
# n8n should pick up changes after restart (or save + refresh in the editor)
```

To unlink:
```bash
cd ~/.n8n/custom
npm unlink n8n-nodes-yourservice
```

---

## 2. n8n Custom Folder Locations

| OS | Path |
|---|---|
| macOS / Linux | `~/.n8n/custom/` |
| Windows | `C:\Users\<YourUser>\.n8n\custom\` |
| Docker | Mount a volume — see section 4 |
| n8n Cloud | Install via Settings → Community Nodes (npm only) |

Create the folder if it doesn't exist:
```bash
mkdir -p ~/.n8n/custom
```

---

## 3. Hot-Reload Dev Mode

The official n8n starter template includes n8n as a dev dependency with hot reload:

```bash
# Clone the starter
git clone https://github.com/n8n-io/n8n-nodes-starter.git n8n-nodes-yourservice
cd n8n-nodes-yourservice
npm install

# Develop with hot reload (recompiles and reloads on file save)
npm run dev
# → Starts n8n at http://localhost:5678 with your node already loaded
```

This is the fastest development loop for new nodes.

---

## 4. Testing in Docker

Mount your built node directory as a volume:

```bash
# Build first
npm run build

# Run n8n with the node mounted
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -v $(pwd)/dist:/home/node/.n8n/custom/node_modules/n8n-nodes-yourservice/dist \
  n8nio/n8n
```

Or use docker-compose:
```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - '5678:5678'
    volumes:
      - ~/.n8n:/home/node/.n8n
      - ./:/home/node/.n8n/custom/node_modules/n8n-nodes-yourservice
    environment:
      - N8N_CUSTOM_EXTENSIONS=/home/node/.n8n/custom
```

---

## 5. Debugging Tips

### Node doesn't appear in picker
- Check `npm run build` completed without TypeScript errors
- Verify `n8n.nodes` in `package.json` points to the correct `dist/` path
- Confirm the `dist/` folder exists and has your compiled files
- Restart n8n completely (hot reload doesn't always catch structural changes)
- Check n8n logs for "Error loading node" messages

### Credentials don't load
- Check `n8n.credentials` path in `package.json`
- Ensure credential `name` property exactly matches `getCredentials('...')` string (case-sensitive)
- The credential class name in `package.json` path must match the actual file path

### "Cannot find module" error
- Run `npm install` to install dependencies
- For `npm link` setups, check the symlink is intact: `ls ~/.n8n/custom/node_modules/`

### Changes not reflected after build
- Hard-refresh n8n in browser (Ctrl+Shift+R)
- Restart the n8n process completely
- Check you saved and the TypeScript compiled (watch for tsc errors)

### Console logging for debugging
```typescript
// Temporary — remove before publishing
console.log('DEBUG credentials:', JSON.stringify(credentials, null, 2));
console.log('DEBUG response:', JSON.stringify(response, null, 2));
console.log('DEBUG item:', JSON.stringify(items[i], null, 2));
```

### Test a specific credential test
In n8n UI → Credentials → open your credential → click "Test" button.  
The result shows any error from your `test` block or credential test method.
