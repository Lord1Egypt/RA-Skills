---
name: miniprogram-ci
description: WeChat Mini Program CI (miniprogram-ci): A compilation module extracted from WeChat DevTools for uploading/previewing mini program/mini game code, building npm, deploying cloud functions, and managing cloud containers. Enables CI/CD without opening DevTools. For automated publishing, CI/CD pipelines, pre-release preview.
---

# miniprogram-ci

> WeChat Mini Program CI tool · v2.1.31 · Node >= 16.1.0

A compilation module extracted from the WeChat Developer Tools for mini program/mini game projects. Supports both Node.js script calls and CLI commands.

## Installation

```bash
npm install miniprogram-ci
# Global install (for CLI usage)
npm install -g miniprogram-ci
```

## Prerequisites

1. **Get AppID** — appid of your mini program/mini game
2. **Generate private key** — WeChat Official Platform → Management → Development → Development Settings → Mini Program Code Upload → Generate "Upload Private Key" (`.key` file)
3. **Configure IP whitelist** (recommended) — Only whitelisted IPs can call upload/preview APIs
4. **Key security** — Private keys are not stored in plaintext on the platform. Must reset if lost.

## Quick Start

```js
const ci = require("miniprogram-ci");

(async () => {
  const project = new ci.Project({
    appid: "wx0000000000000000",
    type: "miniProgram",            // miniProgram | miniProgramPlugin | miniGame | miniGamePlugin
    projectPath: "./dist/build/mp-weixin",
    privateKeyPath: "./key/private.wx.xxxxx.key",
    ignores: ["node_modules/**/*"],
  });

  // Upload code
  const uploadResult = await ci.upload({
    project,
    version: "1.0.0",
    desc: "Fixed several issues",
    setting: { es6: true, minify: true },
    onProgressUpdate: console.log,
    robot: 1,
  });
  console.log("subPackageInfo:", uploadResult.subPackageInfo);

  // Preview (generate QR code)
  await ci.preview({
    project,
    desc: "Preview version",
    setting: { es6: true },
    qrcodeFormat: "image",          // image | base64 | terminal
    qrcodeOutputDest: "./preview.jpg",
    pagePath: "pages/index/index",
    searchQuery: "id=123",
    onProgressUpdate: console.log,
    robot: 1,
  });
})();
```

## Main API

| Method | Purpose | Key Parameters |
|--------|---------|---------------|
| `ci.upload()` | Upload code | project, version(required), desc, setting, robot |
| `ci.preview()` | Preview (QR code) | project, qrcodeOutputDest(required), desc, setting, robot |
| `ci.buildNpm()` | Build npm | project, options.ignores |
| `ci.getDevSourceMap()` | Get latest sourceMap | project, robot(required), sourceMapSavePath(required) |
| `ci.cloudFunctionDeploy()` | Upload cloud function | project, env(required), name(required), path(required) |
| `ci.cloudFileUpload()` | Upload cloud storage/static hosting | project, env(required), path(required) [alpha] |
| `ci.cloudContainerDeploy()` | Deploy cloud container version | project, env(required), containerRoot + version [alpha] |
| `ci.proxy()` | Set proxy | proxyUrl(optional) |

## Compile Settings

```js
{
  es6: true,           // ES6 → ES5
  es7: true,           // Enhanced compilation
  minifyJS: true,      // Minify JS
  minifyWXML: true,    // Minify WXML
  minifyWXSS: true,    // Minify WXSS
  minify: true,        // Minify all
  codeProtect: true,   // Code protection
  autoPrefixWXSS: true, // Auto prefix CSS
}
```

## Project Object

```js
new ci.Project({
  appid: "wx...",           // required
  projectPath: "./dist",    // required (directory containing project.config.json)
  privateKeyPath: "./key",  // required
  type: "miniProgram",      // optional, defaults to miniProgram
  ignores: ["node_modules"],// optional
})
```

## CLI Commands

```bash
# Upload
miniprogram-ci upload \
  --pp ./dist \
  --pkp ./key/private.key \
  --appid wx0000000000000000 \
  --uv 1.0.0 \
  --ud "Version description" \
  --r 1

# Preview
miniprogram-ci preview \
  --pp ./dist \
  --pkp ./key/private.key \
  --appid wx0000000000000000 \
  --uv 1.0.0 \
  --ud "Preview description" \
  --qrcode-format image \
  --qrcode-output-dest ./preview.jpg
```

## Proxy Configuration

Auto-detection order: `HTTPS_PROXY` → `https_proxy` → `HTTP_PROXY` → `http_proxy` → npm config → manual

```js
ci.proxy("http://127.0.0.1:8888");   // manual
ci.proxy();                           // clear, restore auto
```

`servicewechat.com` is automatically added to `no_proxy`.

## Return Values (upload/preview)

```js
{
  subPackageInfo: [
    { name: "__FULL__", size: 123456 },    // entire package
    { name: "__APP__", size: 100000 },     // main package
    { name: "subPack1", size: 23456 },     // sub package
  ],
  pluginInfo: [
    { pluginProviderAppid: "wx...", version: "1.0.0", size: 12345 },
  ],
  devPluginId: "wx...",
}
```

## Third-Party Platform

Supported since 1.0.28. Note:
- Project must have a valid `ext.json`
- Use the private key of the **development mini program bound to the third-party platform**
- IP whitelist also belongs to that development mini program
- The appid passed in must be the bound development mini program's appid

## Robot Parameter

Specify which CI robot to use (1~30), enabling concurrent operations without conflicts.

## Reference Files

| File | Content |
|------|---------|
| [references/cloud.md](references/cloud.md) | Cloud development (cloud functions/cloud containers/cloud storage) |
| [references/cli.md](references/cli.md) | CLI command detailed options |