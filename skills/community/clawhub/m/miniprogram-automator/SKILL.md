---
name: miniprogram-automator
description: WeChat Mini Program Automation SDK (miniprogram-automator): Automate UI operations and data validation of mini programs at runtime. Supports page navigation, element selection and interaction, data injection, screenshots, event listening. For E2E testing, UI automation, regression testing.
---

# miniprogram-automator

> WeChat Mini Program Automation SDK · v0.12.1 · Node >= 8.0

Script-driven UI automation and data validation for mini programs running inside WeChat DevTools. Control taps, inputs, screenshots, and more programmatically.

## Installation & Prerequisites

```bash
npm install miniprogram-automator --save-dev
```

**Environment requirements:**
| Condition | Version |
|-----------|---------|
| Node.js | >= 8.0 |
| Base library | >= 2.7.3 |
| DevTools | >= 1.02.1907232 |

**Must enable:** DevTools security settings → CLI/HTTP call functionality

## Quick Start

```js
const automator = require("miniprogram-automator");

automator.launch({
  cliPath: "path/to/cli",          // optional, defaults to standard install path
  projectPath: "path/to/project",  // project absolute path
}).then(async miniProgram => {
  const page = await miniProgram.reLaunch("/page/component/index");
  await page.waitFor(500);

  const element = await page.$(".kind-list-item-hd");
  console.log(await element.attribute("class"));
  await element.tap();

  await miniProgram.close();
});
```

## Automator (Entry Point)

```js
// Method 1: Launch and connect
automator.launch({
  cliPath: "/Applications/.../cli",    // optional, defaults to Mac/Win paths
  projectPath: "/path/to/project",     // required, project absolute path
  timeout: 30000,                       // optional, max wait (ms)
  port: 9420,                           // optional, WebSocket port
  account: "openid_xxx",                // optional, user openid (multi-account)
  projectConfig: {},                    // optional, overrides project.config.json
  ticket: "xxx",                        // optional, login ticket
});

// Method 2: Connect to already open DevTools
automator.connect({
  wsEndpoint: "ws://127.0.0.1:9420",
});
```

**Default cliPath:**
- Mac: `/Applications/wechatwebdevtools.app/Contents/MacOS/cli`
- Win: `C:/Program Files (x86)/Tencent/微信web开发者工具/cli.bat`

## MiniProgram Object

Returned by launch/connect.

### Page Navigation

```js
await miniProgram.navigateTo("/pages/index/index");   // keep current page
await miniProgram.redirectTo("/pages/other");          // close current page
await miniProgram.navigateBack();                       // go back
await miniProgram.reLaunch("/pages/index");            // close all pages
await miniProgram.switchTab("/pages/tab");              // switch to tabBar
await miniProgram.currentPage();                       // get current page
await miniProgram.pageStack();                         // get page stack
```

### Data & Control

```js
const info = await miniProgram.systemInfo();            // wx.getSystemInfo
const res = await miniProgram.callWxMethod("chooseLocation", {});
await miniProgram.pageScrollTo(100);
const base64 = await miniProgram.screenshot();          // returns base64
await miniProgram.screenshot({path: "./shot.png"});    // save to file
```

### Mock & Injection

```js
// Mock wx method return values (essential for UI testing)
await miniProgram.mockWxMethod("chooseLocation", {
  name: "Tiananmen Square", latitude: 39.90, longitude: 116.40,
});
await miniProgram.restoreWxMethod("chooseLocation");   // restore

// Inject code snippet (closures not supported)
const data = await miniProgram.evaluate(appFunction => {
  return getApp().globalData.userInfo;
});

// Expose method globally for mini program to call
await miniProgram.exposeFunction("onTestEvent", (data) => {
  console.log("Event received:", data);
});
```

### Event Listening

```js
miniProgram.on("console", msg => {
  console.log(`[${msg.type}]`, msg.args);
});
miniProgram.on("exception", err => {
  console.error(err.message, err.stack);
});
```

### Connection Management

```js
await miniProgram.disconnect();   // disconnect
await miniProgram.close();        // disconnect and close project window

// Remote debugging (prints QR code)
await miniProgram.remote({auto: true});  // auto launches on device
```

### Login Tickets

```js
const {ticket, expiredTime} = await miniProgram.getTicket();
await miniProgram.setTicket("new_ticket");
await miniProgram.refreshTicket();         // refresh, extend 2 hours
```

### Performance Audit

```js
const report = await miniProgram.stopAudits({path: "./report.json"});
// Requires "auto-run audit" option enabled
```

### Multi-Account Testing

```js
const accounts = await miniProgram.testAccounts();
// [{nickName: "Zhang San", openid: "xxx"}, ...]
```

## Page Object

```js
const page = await miniProgram.currentPage();

page.path                          // page path
page.query                         // page parameters

const el = await page.$(".class");   // single element (CSS selector)
const els = await page.$$("view");   // element array

await page.waitFor(1000);              // wait ms
await page.waitFor(".loaded");         // wait for element
await page.waitFor(() => {             // wait for condition
  return getApp().globalData.ready;
});

const data = await page.data("list");   // get render data
await page.setData({list: []});         // set render data

const {width, height} = await page.size();  // scrollable size
const scrollTop = await page.scrollTop();   // scroll position

await page.callMethod("onCustomEvent", arg1); // call page method
```

## Element Object

```js
el.tagName         // tag name (lowercase)

// Properties & data
el.text()                        // text content
el.attribute("class")            // tag attribute (always string)
el.property("value")             // DOM property (may return non-string)
el.value()                       // element value
el.style("color")                // computed style
el.wxml()                        // WXML (excluding self)
el.outerWxml()                   // WXML (including self)

// Size & position
const {width, height} = await el.size();    // element size
const {left, top} = await el.offset();      // absolute position (px)

// Child element search
const child = await el.$(".inner");         // find within scope
const children = await el.$$("view");

// Interactions
await el.tap();                              // tap
await el.longpress();                        // long press
await el.input("new text");                  // input/textarea only
await el.touchstart({touches, changedTouches});
await el.touchmove({touches, changedTouches});
await el.touchend({touches, changedTouches});
await el.trigger("eventName", {detail});     // trigger event

// Custom components
await el.callMethod("myMethod", arg1);       // call component method
await el.data("path");                       // get component render data
await el.setData({key: val});                // set component render data

// Component-specific
await el.callContextMethod("play");           // video component
await el.scrollTo(100, 200);                  // scroll-view
await el.swipeTo(2);                          // swiper
await el.moveTo(50, 30);                      // movable-view
await el.slideTo(80);                         // slider
el.scrollWidth / el.scrollHeight              // scroll-view dimensions
```

## Reference Files

| File | Content |
|------|---------|
| [references/api.md](references/api.md) | Complete API parameter tables and examples |