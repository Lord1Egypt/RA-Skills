# MIoT Authentication Bypass via Browser Cookies

## Problem

`mi-service-lite` generates a random `deviceId` each startup:
```js
const randomDeviceId = "android_" + uuid();  // New UUID every time
```
Xiaomi treats each login as a new device → triggers SMS security verification (`securityStatus: 16`) → MIoT login fails.

## Solution

Use browser cookies from an already-authenticated Xiaomi session to call `serviceLoginAuth2`, bypassing security verification.

### Prerequisites

A browser logged into `account.xiaomi.com` with valid session cookies. The key cookies needed:
- `passport_slh` — Session login hash
- `passport_ph` — Passport hash
- `deviceId` — Browser's device ID (e.g., `wb_xxx`)
- `userId` — Xiaomi user ID

### Step-by-step

#### 1. Get ssecurity and passToken via serviceLoginAuth2

```js
const crypto = require('crypto');
const axios = require('axios');

const userId = 'YOUR_XIAOMI_USER_ID';
const password = 'YOUR_PASSWORD';
const hash = crypto.createHash('md5').update(password).digest('hex').toUpperCase();

// Browser cookies from account.xiaomi.com
const browserCookies = [
  'deviceId=YOUR_BROWSER_DEVICE_ID',
  'userId=' + userId,
  'passInfo=login-end',
  'passport_slh=YOUR_PASSPORT_SLH',
  'passport_ph=YOUR_PASSPORT_PH',
  'sdkVersion=3.4.1',
  'PassportDeviceId=YOUR_BROWSER_DEVICE_ID'
].join('; ');

const qs = new URLSearchParams({
  _json: 'true',
  sid: 'xiaomiio',
  qs: '%3Fsid%3Dxiaomiio',
  user: userId,
  hash: hash
});

const { data } = await axios.post(
  'https://account.xiaomi.com/pass/serviceLoginAuth2',
  qs.toString(),
  {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': browserCookies
    },
    maxRedirects: 0,
    validateStatus: () => true
  }
);

const pass = JSON.parse(data.replace('&&&START&&&', ''));
// pass.securityStatus === 0  ← No verification!
// pass.ssecurity ← RC4 signing key for MIoT API
// pass.passToken ← Needed for service token exchange
```

#### 2. Exchange passToken for serviceToken

```js
const tokenResponse = await axios.get(pass.location, {
  maxRedirects: 0,
  validateStatus: () => true,
  headers: {
    'Cookie': `deviceId=YOUR_BROWSER_DEVICE_ID; userId=${userId}; passToken=${pass.passToken}`
  }
});

let serviceToken = '';
for (const cookie of (tokenResponse.headers['set-cookie'] || [])) {
  const match = cookie.match(/serviceToken=([^;]+)/);
  if (match) serviceToken = match[1];
}
```

#### 3. Inject into .mi.json

```js
const fs = require('fs');
const store = JSON.parse(fs.readFileSync('.mi.json', 'utf8'));
store.miiot = {
  deviceId: 'YOUR_BROWSER_DEVICE_ID',
  userId, password,
  did: 'YOUR_DEVICE_NAME',
  sid: 'xiaomiio',
  pass: {
    ssecurity: pass.ssecurity,
    nonce: String(pass.nonce),
    passToken: pass.passToken,
    cUserId: pass.cUserId,
    userId: String(pass.userId)
  },
  serviceToken
};
fs.writeFileSync('.mi.json', JSON.stringify(store, null, 2));
```

#### 4. Patch mi-service-lite to skip login

In `node_modules/mi-service-lite/dist/index.js`, find `getMiService()` and add before the password login:

```js
// Skip login if cached credentials exist
if (account.serviceToken && account.pass && account.pass.ssecurity) {
  console.log("🔑 Using cached " + service + " credentials, skipping login");
  if (service === "miiot") {
    account = await MiIOT.getDevice(account);
  } else {
    account = await MiNA.getDevice(account);
  }
  return service === "miiot" ? new MiIOT(account) : new MiNA(account);
}
```

## Critical Warning: psecurity ≠ ssecurity

| API Endpoint | Returns | Used For |
|-------------|---------|----------|
| `serviceLogin` (browser redirect) | `psecurity` | Cookie-based web auth |
| `serviceLoginAuth2` (password login) | `ssecurity` | MIoT RC4 request signing |

These are **different values**. MIoT's `encodeMiIOT()` requires `ssecurity`. Using `psecurity` causes signature verification failure — the API call will return non-decodable responses.

## Token Expiry

The injected `serviceToken` has an expiry (typically days to weeks). When it expires, MIoT API calls will fail. Re-run the browser cookie injection process to refresh.
