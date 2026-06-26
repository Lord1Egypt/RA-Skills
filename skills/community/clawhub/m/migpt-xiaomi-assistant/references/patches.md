# Required Code Patches

## Patch 1: mi-service-lite — Skip login with cached credentials

**File**: `node_modules/mi-service-lite/dist/index.js`
**Function**: `getMiService()`

Add after `account` object construction, before the `getAccount()` call:

```js
if (account.serviceToken && account.pass && account.pass.ssecurity) {
  console.log("🔑 Using cached " + service + " credentials");
  if (service === "miiot") {
    account = await MiIOT.getDevice(account);
  } else {
    account = await MiNA.getDevice(account);
  }
  return service === "miiot" ? new MiIOT(account) : new MiNA(account);
}
```

## Patch 2: mi-gpt — Allow keepAlive without streamResponse

**File**: `node_modules/mi-gpt/dist/index.js`
**Function**: `enterKeepAlive()` in the Speaker subclass

Remove the `streamResponse` guard:

```js
// REMOVE these lines:
if (!this.streamResponse) {
  await this.response({ text: "您已关闭流式响应..." });
  return;
}
```

This allows continuous conversation mode even with `streamResponse: false` (required for X08E and similar models).

## Patch 3 (Optional): MIoT-optional fallback mode

If MIoT login is unreliable, patch mi-gpt to work with MiNA only. Modify these locations in `node_modules/mi-gpt/dist/index.js`:

1. **`initMiServices()`**: Assert only MiNA, log warning if MIoT fails
2. **`wakeUp()`**: Fallback to `MiNA.play({ tts: " " })`
3. **`response()` TTS section**: Fallback to `MiNA.play({ tts: text })`
4. **`playingCommand` check**: Guard with `if (this.MiIOT)` before `getProperty()`
5. **`activeKeepAliveMode()`**: Fallback to `MiNA.play()`
6. **Debug device info**: Use `(this.MiIOT || this.MiNA).account`

Note: MiNA TTS fallback does NOT work on X08E (returns success but no audio). This patch is only useful for models where MiNA TTS actually works.

## Applying Patches

Patches modify files inside `node_modules/`. They will be overwritten by `npm install` or `npm update`. To persist:

1. Keep a `patches/` directory with patch files
2. Use `patch-package` npm module
3. Or re-apply patches via a `postinstall` script in `package.json`
