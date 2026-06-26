# Morelogin Skill - Full Implementation Based on Official Local API

## ✅ Updated per Official Documentation

**Official API docs**: https://guide.morelogin.com/api-reference/local-api

**API endpoint**: http://127.0.0.1:40000

**Requirements**: MoreLogin desktop app v2.15.0+

---

## 📋 Update Summary

### 1. Use Official Local API

- ✅ API endpoint: `http://127.0.0.1:40000`
- ✅ All requests use POST method
- ✅ Request format: JSON
- ✅ Response format: `{ code: 0, msg: null, data: {...} }`

### 2. Browser Profile Management

| API Endpoint | Function | CLI Command |
|---------|------|---------|
| `POST /api/env/page` | Get profile list | `morelogin browser list` |
| `POST /api/env/start` | Start profile | `morelogin browser start --env-id <ID>` |
| `POST /api/env/close` | Close profile | `morelogin browser close --env-id <ID>` |
| `POST /api/env/status` | Check status | `morelogin browser status --env-id <ID>` |
| `POST /api/env/detail` | Get detail | `morelogin browser detail --env-id <ID>` |
| `POST /api/env/create/quick` | Quick create | `morelogin browser create` |
| `POST /api/env/create/advanced` | Advanced create | `morelogin browser create --advanced` |

### 3. Cloud Phone Management

| API Endpoint | Function | CLI Command |
|---------|------|---------|
| `POST /api/cloudphone/page` | Get cloud phone list | `morelogin cloudphone list` |
| `POST /api/cloudphone/powerOn` | Start cloud phone | `morelogin cloudphone start --id <ID>` |
| `POST /api/cloudphone/powerOff` | Stop cloud phone | `morelogin cloudphone stop --id <ID>` |
| `POST /api/cloudphone/info` | Get detail | `morelogin cloudphone info --id <ID>` |
| `POST /api/cloudphone/updateAdb` | Update ADB status | Auto-handled |

---

## 🚀 Quick Start

### 1. List All Profiles

```bash
cd ~/.openclaw/workspace/skills/morelogin
node bin/morelogin.js browser list
```

**Sample output:**
```
📋 Fetching browser profile list...

Found 11 profiles:

1. P-23 (ID: 2026143235095064576)
   Status: ⚫ Stopped

2. P-22 (ID: 2021192026680651776)
   Status: ⚫ Stopped

3. P-21 (ID: 2018225188292194304)
   Status: ⚫ Stopped

4. P-20 (ID: 2016127261952372736)
   Status: ⚫ Stopped
   Proxy IP: 88.97.244.43 (GB)
```

### 2. Start Profile

```bash
node bin/morelogin.js browser start --env-id 2016127261952372736
```

**Sample output:**
```
🚀 Starting profile: 2016127261952372736

✅ Profile started
🔗 Debug port: 59840
🌐 CDP address: http://localhost:59840
📍 WebSocket: ws://localhost:59840/devtools/browser
```

### 3. Check Profile Status

```bash
node bin/morelogin.js browser status --env-id 2016127261952372736
```

### 4. Close Profile

```bash
node bin/morelogin.js browser close --env-id 2016127261952372736
```

---

## 📱 Cloud Phone Operations

### 1. List Cloud Phones

```bash
node bin/morelogin.js cloudphone list
```

### 2. Start Cloud Phone

```bash
node bin/morelogin.js cloudphone start --id <cloudphone_id>
```

### 3. Get Cloud Phone Detail (Including ADB Info)

```bash
node bin/morelogin.js cloudphone info --id <cloudphone_id>
```

**Sample output:**
```
📄 Fetching cloud phone detail: <ID>

Cloud phone detail:
  Name: CloudPhone-1
  Status: Running
  Android version: 13
  ADB: 127.0.0.1:5555
  ADB password: None
  Group: Default
  Tags: test
  Location: US
```

### 4. Query ADB Metadata

```bash
node bin/morelogin.js cloudphone adb-info --id <cloudphone_id>
```

### 5. Execute ADB Command

This skill no longer exposes a direct `cloudphone exec` command.

---

## 🔧 API Response Format

MoreLogin API unified response format:

```json
{
  "code": 0,          // 0 = success, non-zero = failure
  "msg": null,        // Error message
  "data": { ... },    // Actual data
  "requestId": "..."  // Request ID
}
```

### Success Response Example

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "total": "11",
    "current": "1",
    "pages": "2",
    "dataList": [...]
  },
  "requestId": "..."
}
```

### Start Profile Response

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "debugPort": 59840,
    "webdriverPath": "...",
    "status": "success"
  },
  "requestId": "..."
}
```

---

## 🌐 CDP Connection Examples

### Puppeteer

```javascript
const puppeteer = require('puppeteer-core');

// Get debugPort from API
const debugPort = 59840;

const browser = await puppeteer.connect({
  browserURL: `http://localhost:${debugPort}`,
  defaultViewport: null
});

const page = await browser.newPage();
await page.goto('https://example.com');
```

### Playwright

```javascript
const { chromium } = require('playwright');

const browser = await chromium.connectOverCDP(`http://localhost:${debugPort}`);
const context = browser.contexts()[0];
const page = context.pages()[0];
```

---

## 📱 ADB Connection Example

```bash
# Get ADB address from cloud phone detail
ADB_HOST="127.0.0.1"
ADB_PORT="5555"

# Connect ADB
adb connect ${ADB_HOST}:${ADB_PORT}

# Verify connection
adb devices

# Execute commands
adb -s ${ADB_HOST}:${ADB_PORT} shell
adb -s ${ADB_HOST}:${ADB_PORT} install app.apk
adb -s ${ADB_HOST}:${ADB_PORT} shell input tap 500 1000
adb -s ${ADB_HOST}:${ADB_PORT} shell screencap -p /sdcard/screen.png
adb -s ${ADB_HOST}:${ADB_PORT} pull /sdcard/screen.png
```

---

## 📁 File Structure

```
skills/morelogin/
├── SKILL.md                 # OpenClaw Skill definition (updated)
├── README.md                # This file
├── package.json             # Node.js config
├── bin/
│   ├── morelogin.js        # CLI main program (updated to official API)
│   └── test-api.js         # API test tool
├── examples/
│   ├── puppeteer-example.js
│   └── playwright-example.js
├── query-btc-price.js       # BTC price query example
└── start-and-query.js       # Start and query example
```

---

## ✅ Tested Features

- ✅ List browser profiles
- ✅ Start profile
- ✅ Close profile
- ✅ Check profile status
- ✅ Get profile detail
- ✅ Connect to browser via CDP
- ✅ Automate with Puppeteer
- ✅ Query BTC price

---

## 🐛 Troubleshooting

### 1. API Connection Failed

```bash
# Check if MoreLogin desktop app is running
ps aux | grep -i morelogin

# Check API endpoint
curl http://127.0.0.1:40000
```

### 2. Profile Start Failed

```bash
# Check if profile ID is correct
node bin/morelogin.js browser list

# Check profile status
node bin/morelogin.js browser status --env-id <ID>
```

### 3. CDP Connection Failed

```bash
# Check if profile is running
node bin/morelogin.js browser status --env-id <ID>

# Check if port is accessible
curl http://localhost:<debugPort>/json/version
```

---

## 📚 Reference Documentation

- [MoreLogin Local API Guide](https://guide.morelogin.com/api-reference/local-api)
- [MoreLogin Local API Detailed Docs](https://guide.morelogin.com/api-reference/local-api/local-api)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Puppeteer Docs](https://pptr.dev/)
- [Playwright Docs](https://playwright.dev/)

---

**Last updated**: 2024-02-26
**Version**: v2.0 (based on official Local API)
