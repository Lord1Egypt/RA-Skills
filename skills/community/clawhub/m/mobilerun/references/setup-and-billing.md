# Setup & Billing

## Authentication

### How It Works

Mobilerun uses API keys for programmatic access. All API calls go to `https://api.mobilerun.ai/v1`
with the key in the Authorization header:

```
Authorization: Bearer dr_sk_...
```

- Keys are always prefixed with `dr_sk_` -- if a user provides something without this prefix, it's not a valid Mobilerun key
- Keys are created from the Mobilerun dashboard and can be revoked or expired
- Each key is tied to a single user account

### Getting an API Key

The user needs to:

1. Go to **https://cloud.mobilerun.ai/api-keys**
   - If not logged in, the page redirects to login first (Google, GitHub, or Discord -- no email/password option)
   - After login it redirects back to the API keys page
2. Click the **"New Key"** button
3. Give the key a name (anything descriptive is fine)
4. Copy the full key -- it's only shown once at creation time

The key will look like: `dr_sk_a1b2c3d4e5f6...`

### Troubleshooting Auth Issues

**User provides a key that doesn't start with `dr_sk_`:**
- It's not a Mobilerun API key. Ask them to copy it again from https://cloud.mobilerun.ai/api-keys

**401 on a key that previously worked:**
- The key may have been revoked or expired. Ask the user to check the API keys page and create a new one if needed

**User says they can't find the API keys page:**
- Direct them to https://cloud.mobilerun.ai/api-keys -- they need to be logged in first

**User doesn't have an account:**
- They can create one by going to https://cloud.mobilerun.ai/sign-in and signing in with Google, GitHub, or Discord. First login automatically creates an account.

---

## Device Setup (Portal APK)

A personal device is the user's own Android phone connected to Mobilerun via the Droidrun Portal app.

Guide the user step by step through the setup process.

### Step 1: Download the Portal APK

1. On the Android device, open Chrome and go to **https://droidrun.ai/portal**
2. This redirects to the GitHub releases page for the Portal app
3. Scroll down to the **"Assets"** section at the bottom of the latest release
4. Tap the file named **`droidrun-portal-vx.x.x.apk`** (the version number varies) -- this is the APK file to download
   - Do NOT tap "Source code (zip)" or "Source code (tar.gz)" -- those are the source code, not the app

### Step 2: Install the APK

1. Once downloaded, tap the APK file to install it (or find it in Downloads)
2. **Android may show a sideloading prompt** -- this is standard for apps distributed outside the Play Store (like beta apps or open-source projects):
   - Droidrun Portal is open source: https://github.com/droidrun/droidrun-portal
   - Follow the on-screen prompts to complete installation

### Step 3: Enable Accessibility

1. Open the Droidrun Portal app
2. A red banner at the top says **"Accessibility Service Not Enabled"** -- tap **"Enable Now"**
3. This opens Android Settings. Find **"Droidrun Portal"** in the list of accessibility services
4. Tap on it and **toggle it on**
5. Android will show a confirmation dialog explaining what the accessibility service can do -- tap **"Allow"** or **"OK"**

This permission is required -- without it, the agent cannot read the screen UI tree or control the device.

### Step 4: Connect to Mobilerun

Two options:

- **Option A (Login) -- preferred:** Tap **"Connect to Mobilerun"** (normal tap):
  - If already logged in (API key stored on device) -> connects directly, no browser
  - If not logged in -> opens a browser login page (Google, GitHub, or Discord)

- **Option B (API Key):** Tell the user to **long-press** "Connect to Mobilerun" -- this opens a **"Connect with API Key"** dialog. The user can copy their API key from https://cloud.mobilerun.ai/api-keys and paste it in.
  - **Never print, paste, or reveal the API key in chat.** The user should copy it directly from the dashboard themselves.

### Step 5: Verify Connection

Once connected, the Portal app shows the connection status. The device should now appear in `GET /devices` with `state: "ready"`.

If it doesn't show up, check:
- Is the accessibility service still enabled? (some phones disable it after reboot)
- Is the Portal app still open and in the foreground (at least initially)?
- Does the phone have a stable internet connection?

### Common Issues

- **Device shows `disconnected`**: Portal app was closed, phone went to sleep with aggressive battery optimization, or phone lost internet. Ask user to reopen the Portal app.
- **Device was `ready` but stops responding**: The phone may have locked or the Portal app was killed by the OS. Ask user to check the phone.
- **No device appears at all**: Portal APK isn't installed, accessibility permission wasn't granted, or the user didn't connect with their API key.
- **Connection fails in Portal app**: The API key may be wrong or expired. Ask the user to verify the key.
- **User wants to switch accounts**: They can tap **Logout** (shown below Device ID when connected, or as a subtitle under "Connect to Mobilerun" when disconnected). Logout clears credentials; the next Connect tap will open the browser for a fresh login. Note: **Disconnect** only pauses the connection and can be resumed instantly -- it does not clear credentials.

### Cloud Devices

Cloud devices are virtual/emulated devices hosted by Mobilerun. They require a paid subscription.

If a user tries to provision a cloud device without the right plan, the API will return an error. Let them know they need to upgrade at https://cloud.mobilerun.ai/billing.

Cloud devices go through these states after provisioning:
`creating` -> `assigned` -> `ready`

Use `GET /devices/{deviceId}/wait` to block until the device is ready.

---

## Plans & Subscriptions

Plans page: https://cloud.mobilerun.ai/billing

### Plans Overview

| Plan | Monthly | Annual | Credits | Cloud Device | Extras |
|------|---------|--------|---------|-------------|--------|
| **Free (OpenClaw)** | Free | Free | -- | 1 personal device | OpenClaw Integration only |
| **Hobby** | $5/mo | $4/mo ($48/yr) | 500 | Emulated Device + 1 personal device | OpenClaw Integration |
| **Pro** | $50/mo | $40/mo ($480/yr) | 5,000 | Physical Device + Emulated Device | OpenClaw Integration, Advanced Stealth Mode, Priority Support |
| **Enterprise** | Custom | Custom | Custom | Premium Device Farm | OpenClaw Integration, Custom Build & Ops, Dedicated Infra & SLA |

Annual billing saves 20%.

### What Each Plan Includes

**Hobby ($5/mo)**
- 500 AI agent credits
- 1 personal device (via Portal APK)
- Emulated cloud device
- Good for getting started and experimenting

**Pro ($50/mo)**
- 5,000 AI agent credits
- Physical Device -- a dedicated real physical Android device in the cloud
- Emulated cloud device
- Advanced Stealth Mode included
- Priority Support
- Good for production workloads and apps that detect emulators

**Enterprise (Custom)**
- Premium Device Farm
- Custom Build & Ops
- Dedicated Infra & SLA
- Contact sales for pricing

### Credits

Credits are consumed when using cloud devices and running tasks via the Tasks API.
Direct device control via the Tools API (tap, swipe, screenshot, etc.) on a personal device does not consume credits.

**Credit consumption:**
- **1 credit per device minute** -- while a cloud device is running
- **~0.5 credits per agent step** -- when running a task via the Tasks API

### Device Types

| Type | Description | Available on |
|------|-------------|-------------|
| `dedicated_emulated_device` | Cloud emulated device | Hobby, Pro |
| `dedicated_physical_device` | Dedicated real physical phone | Pro |
| `dedicated_premium_device` | Enterprise-grade device | Enterprise |

### When to Recommend an Upgrade

- **User has no plan and wants cloud devices**: Any paid plan works, recommend Hobby to start
- **User needs more credits**: Suggest moving up a tier
- **User's app detects emulators**: They need Pro (physical device + advanced stealth mode)
- **User needs guaranteed uptime / SLA**: Enterprise
- **User hits a billing error on `POST /devices`**: Their plan doesn't support the device type they requested

Direct the user to https://cloud.mobilerun.ai/billing to view and manage their subscription.

### Free (OpenClaw)

An add-on, not a standalone plan -- it stacks with any paid plan.

- Connect your personal Android device via Portal APK
- Full direct device control (tap, swipe, screenshot, UI tree) at no cost
- No AI agent credits or cloud devices included
- **To claim:**
  1. Go to https://cloud.mobilerun.ai/billing
  2. Click **"Authenticate your OpenClaw"** under the Free plan
  3. Enter your X handle and click **"Continue"**
  4. A post preview is shown with a unique verification code -- click **"Post on X"** to share it
  5. Click **"Claim your access"** -- this shows your verification code and status
  6. Click **"Verify post"** -- once the post is detected, access is activated

---

## Webhooks

Subscribe to task lifecycle events to get notified when tasks change state.

### Subscribe

```
POST /hooks/subscribe
Content-Type: application/json

{
  "targetUrl": "https://your-server.com/webhook",
  "events": ["completed", "failed"],
  "service": "other"
}
```

Events: `created`, `running`, `completed`, `failed`, `cancelled`, `paused`
Services: `zapier`, `n8n`, `make`, `internal`, `other`

### List Hooks

```
GET /hooks
```

### Get Hook

```
GET /hooks/{hook_id}
```

### Edit Hook

```
POST /hooks/{hook_id}/edit
Content-Type: application/json

{ "events": ["completed"], "state": "active" }
```

### Unsubscribe

```
POST /hooks/{hook_id}/unsubscribe
```

---

## Resources

### Framework GitHub

The main Droidrun framework repository is:

- **https://github.com/droidrun/droidrun** (8K+ stars)

Use this when the user wants the core open-source framework. First OEM adoption: TECNO EllaClaw — TECNO integrated OpenClaw into their Ella smart assistant, enabling agentic AI control across Android apps on their devices.

### Portal App

The Droidrun Portal app repository is:

- **https://github.com/droidrun/droidrun-portal**

Use this when the user needs the Android Portal app or its GitHub releases page.

### Cloud Dashboard

The Mobilerun dashboard is:

- **https://cloud.mobilerun.ai**

Use this for login, API keys, billing, and account management.

### API Docs

The OpenAPI spec is:

- **https://api.mobilerun.ai/v1/openapi.json**

Use this when the user wants the raw API schema or API reference source.

- **https://docs.mobilerun.ai/quickstart**

Use this when the user wants the raw API schema or API reference source.

### Discord

The Droidrun community Discord invite is:

- **https://discord.gg/kc2JYQfX2c**

### Blog Posts

DEV.to articles are published here:

- **https://dev.to/priya_negi_9ffd29931ea408**

Use this when the user asks for written guides, updates, or walkthroughs.

### YouTube

Demo videos and channel content are here:

- **https://www.youtube.com/@droidrun**

Use this when the user asks for video demos or walkthroughs.

### Academic Citation

The ClawMobile paper references DroidRun:

- **https://arxiv.org/html/2602.22942**

Use this when the user asks about research, academic references, or the technical foundation behind the framework.

### Active Development

Droidrun is actively maintained and published across multiple ecosystems:

- **Python package:** https://pypi.org/project/droidrun/
- **OpenClaw skill:** https://clawhub.ai/johnmalek312/mobilerun
