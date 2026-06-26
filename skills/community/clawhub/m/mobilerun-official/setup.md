# Mobilerun Setup

This document describes how Mobilerun authentication and device connectivity works,
so you can diagnose issues and guide the user through setup when needed.

---

## Authentication

### How It Works

Mobilerun uses API keys for programmatic access. All API calls go to `https://api.mobilerun.ai/v1`
with the user's key in the Authorization header.

- Keys are prefixed with `dr_sk_` -- if a user provides something without this prefix, it's not a valid Mobilerun key
- Keys are created from the Mobilerun dashboard at cloud.mobilerun.ai and can be revoked or expired
- Each key is tied to a single user account
- The key is stored securely via the `MOBILERUN_API_KEY` environment variable — never hardcode or expose it

### Getting an API Key

The user needs to:

1. Go to **https://cloud.mobilerun.ai/api-keys**
   - If not logged in, the page redirects to login first (Google, GitHub, or Discord -- no email/password option)
   - After login it redirects back to the API keys page
2. Click the **"New Key"** button
3. Give the key a name (anything descriptive is fine)
4. Copy the full key -- it's only shown once at creation time

The key will look like: `dr_sk_a1b2c3d4e5f6...`

### Verifying the API Key

After receiving a key from the user, verify it works by calling `GET /devices` with the key. 

| Response | Meaning |
|----------|---------|
| `200` with JSON body | Key is valid. The response shows the user's devices (may be empty if no devices connected yet) |
| `401 Unauthorized` | Key is invalid, expired, or revoked |

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

## Device Connectivity

### Personal Devices (Portal APK)

A personal device is the user's own Android phone connected to Mobilerun via the Droidrun Portal app.

#### Installing the Portal APK

1. On the Android device, go to **https://droidrun.ai/portal** -- this redirects to the latest GitHub release
2. Download the file named `droidrun-portal-vx.x.x.apk` (the version number varies)
3. Open/install the downloaded APK
   - Android may warn about installing from unknown sources -- the user needs to allow it

#### Connecting to Mobilerun

Once the Portal app is installed and opened:

1. **Grant accessibility permission**: A red banner at the top says "Accessibility Service Not Enabled" -- tap **"Enable Now"** and follow the system prompts to enable it. This Android system permission is required so the agent can read on-screen element names and positions (the UI accessibility tree). The permission is scoped to the Portal app only and does not grant access to other apps' data. The user controls when the connection is active.
2. **Connect to Mobilerun** -- two options:
   - **Tap** "Connect to Mobilerun" -> opens a login page where the user signs in with their account (Google, GitHub, or Discord)
   - **Long-press** "Connect to Mobilerun" -> opens a field labeled "Token" -- despite the label, the user should paste their Mobilerun API key (`dr_sk_...`) here, then tap **Connect**
3. The app connects to Mobilerun and the device should appear in `GET /devices` with `state: "ready"`.

The agent should provide the API key to the user at step 2 -- the same key used for API calls.

#### Checking Device Status

Call `GET /devices` and look for a device with `provider: "personal"`:

| Result | Meaning |
|--------|---------|
| No personal device in list | Portal APK isn't installed, not connected, or accessibility permission not granted |
| Device with `state: "ready"` | Device is connected and ready to use |
| Device with `state: "disconnected"` | Portal app lost connection. User should check that the app is open and phone has internet |

#### Common Issues

- **Device shows `disconnected`**: Portal app was closed, phone went to sleep with aggressive battery optimization, or phone lost internet. Ask user to reopen the Portal app.
- **Device was `ready` but stops responding**: The phone may have locked or the Portal app was killed by the OS. Ask user to check the phone.
- **No device appears at all**: Portal APK isn't installed, accessibility permission wasn't granted, or the user didn't connect with their API key.
- **Connection fails in Portal app**: The API key may be wrong or expired. Ask the user to verify the key.

### Cloud Devices

Cloud devices are virtual/emulated devices hosted by Mobilerun. They require a paid subscription.

If a user tries to provision a cloud device without the right plan, the API will return an error.
In that case, let them know they need to upgrade at https://cloud.mobilerun.ai.

Cloud devices go through these states after provisioning:
`creating` -> `assigned` -> `ready`

Use `GET /devices/{deviceId}/wait` to block until the device is ready (avoids polling).

---

## Accounts & Plans

- **Free accounts** can connect personal devices via Portal APK and use the Tools API to control them
- **Paid plans** add cloud device provisioning, task execution (AI agent credits), and additional features

For full plan details (Hobby, Starter, Pro, Enterprise), see [subscription.md](./subscription.md).

If an API call fails with a billing/plan error, direct the user to https://cloud.mobilerun.ai/billing.

---

## Quick Checklist

When starting a session, verify:

1. **API key works** -- `GET /devices` returns 200
2. **Device is available** -- at least one device with `state: "ready"` in the response
3. **Device is responsive** -- `GET /devices/{id}/screenshot` returns a PNG image

If all three pass, you're ready to control the phone. See [phone-api.md](./phone-api.md) for the full API reference.
