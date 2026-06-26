# Project File Templates

Copy these into your project root. Replace `YOURSERVICE` / `YourService` / `yourService`.

## Table of Contents
1. [package.json](#1-packagejson)
2. [tsconfig.json](#2-tsconfigjson)
3. [gulpfile.js](#3-gulpfilejs)
4. [.eslintrc.js](#4-eslintrcjs)
5. [index.js (optional)](#5-indexjs)
6. [.prettierrc (optional)](#6-prettierrc)
7. [.gitignore](#7-gitignore)

---

## 1. package.json

> Critical fields explained:
> - `keywords` must include `"n8n-community-node-package"` — n8n won't find it otherwise
> - `n8n.nodes` and `n8n.credentials` must point to compiled `.js` files in `dist/`
> - `files: ["dist"]` means only the compiled output is published to npm (not source)
> - `peerDependencies` ensures the user's n8n provides `n8n-workflow`, not a duplicate

```json
{
  "name": "n8n-nodes-yourservice",
  "version": "0.1.0",
  "description": "n8n community node for YourService API",
  "keywords": [
    "n8n-community-node-package"
  ],
  "license": "MIT",
  "homepage": "https://github.com/YOURGITHUB/n8n-nodes-yourservice",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/YOURGITHUB/n8n-nodes-yourservice.git"
  },
  "main": "index.js",
  "scripts": {
    "build": "tsc && gulp build:icons",
    "dev": "tsc --watch",
    "format": "prettier nodes credentials --write",
    "lint": "eslint nodes credentials --ext .ts",
    "lintfix": "eslint nodes credentials --ext .ts --fix",
    "prepublishOnly": "npm run build && npm run lint"
  },
  "n8n": {
    "n8nNodesApiVersion": 1,
    "credentials": [
      "dist/credentials/YourServiceApi.credentials.js"
    ],
    "nodes": [
      "dist/nodes/YourService/YourService.node.js"
    ]
  },
  "files": [
    "dist"
  ],
  "devDependencies": {
    "@types/node": "^18.16.16",
    "eslint-plugin-n8n-nodes-base": "^1.16.1",
    "gulp": "^4.0.2",
    "n8n-core": "*",
    "n8n-workflow": "*",
    "prettier": "^3.3.2",
    "typescript": "^5.3.3"
  },
  "peerDependencies": {
    "n8n-workflow": "*"
  }
}
```

### Adding more nodes or credentials

```json
"n8n": {
  "n8nNodesApiVersion": 1,
  "credentials": [
    "dist/credentials/YourServiceApi.credentials.js",
    "dist/credentials/YourServiceOAuth2Api.credentials.js"
  ],
  "nodes": [
    "dist/nodes/YourService/YourService.node.js",
    "dist/nodes/YourServiceTrigger/YourServiceTrigger.node.js"
  ]
}
```

### Adding npm dependencies (e.g. form-data, jsonwebtoken)

```json
"dependencies": {
  "form-data": "^4.0.0",
  "jsonwebtoken": "^9.0.2"
}
```

---

## 2. tsconfig.json

```json
{
  "compilerOptions": {
    "strict": true,
    "module": "commonjs",
    "target": "ES2019",
    "lib": ["ES2019"],
    "outDir": "./dist",
    "rootDir": ".",
    "typeRoots": ["./node_modules/@types"],
    "esModuleInterop": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "skipLibCheck": true,
    "resolveJsonModule": true
  },
  "include": ["nodes/**/*.ts", "credentials/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

---

## 3. gulpfile.js

Copies SVG and PNG icons from `nodes/` into `dist/nodes/` after TypeScript compiles. Required because `tsc` only copies `.ts` files.

```javascript
const { src, dest } = require('gulp');

function buildIcons() {
  return src('nodes/**/*.{png,svg}').pipe(dest('dist/nodes'));
}

exports['build:icons'] = buildIcons;
```

---

## 4. .eslintrc.js

Required by n8n community standards. Passes linting is checked before the node can be installed on n8n Cloud.

```javascript
module.exports = {
  root: true,
  env: { node: true },
  parser: '@typescript-eslint/parser',
  parserOptions: {
    project: ['./tsconfig.json'],
    sourceType: 'module',
    extraFileExtensions: ['.json'],
  },
  plugins: ['n8n-nodes-base'],
  extends: ['plugin:n8n-nodes-base/nodes'],
  rules: {
    // Relax specific rules if needed:
    // 'n8n-nodes-base/node-class-description-credentials-name-unsuffixed': 'off',
    // 'n8n-nodes-base/node-dirname-against-convention': 'off',
  },
};
```

Common lint rules you may need to suppress with an inline comment:
```typescript
// eslint-disable-next-line n8n-nodes-base/node-class-description-credentials-name-unsuffixed
name: 'myApiCredential',
```

---

## 5. index.js

Usually not needed — `package.json`'s `n8n` section handles registration. Add this only if n8n complains about a missing entry point:

```javascript
// index.js — explicit entry point (rarely needed)
module.exports = {};
```

---

## 6. .prettierrc

```json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

---

## 7. .gitignore

```
node_modules/
dist/
*.js.map
.env
```

> Note: Some projects commit `dist/` so users can install from GitHub without building. Either approach is fine — just be consistent.
