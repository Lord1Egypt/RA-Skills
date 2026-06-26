---
name: MoltShell Vision Engine
description: Give your text-based OpenClaw agent the ability to see and describe images
---

# 👁️ MoltShell Vision Engine

Standard OpenClaw agents are **blind**. If your web-scraping bot hits an infographic, or your chatbot receives a user-uploaded image, the agent crashes because it cannot process pixels.

This skill acts as the **visual cortex** for your text-based bots. It securely routes image URLs to a Replicate-powered Vision-Language Model via the [MoltShell M2M Marketplace](https://moltshell.xyz) and returns a structured text description so your agent can continue its reasoning loop.

---

## ⚡ Zero-Config Sandbox (Try it instantly)

We hate API paywalls as much as you do. This skill comes **pre-configured with a Public Sandbox Key**. You do not need to create an account or provide a credit card to test it. Just install the skill, and your bot will instantly receive **$0.25 of free shadow-compute** — enough for roughly **5 vision runs** at $0.05 each.

---

## 🛠️ Usage

Once installed, your OpenClaw agent can call the `moltshell_vision` tool whenever it encounters an image.

### Input Parameters

| Parameter   | Type   | Required | Description                                       |
|-------------|--------|----------|---------------------------------------------------|
| `image_url` | string | ✅       | The public URL of the image to analyze             |
| `prompt`    | string | ✅       | What the agent needs to know about the image       |

### Example

```
Agent receives an image URL → calls moltshell_vision:

  image_url: "https://example.com/dashboard-screenshot.png"
  prompt:    "Describe the layout and key UI elements in this screenshot"

Tool returns:
  "The screenshot shows a modern web dashboard with a dark theme.
   The top navigation bar contains a logo on the left and user
   settings on the right. The main content area displays a grid
   of cards with metrics including revenue, active users, and..."
```

---

## 💳 Going to Production

The built-in sandbox wallet is strictly for **testing** and will throw a `402 Payment Required` error once your free compute runs out.

To use this skill in production:

1. Go to [https://moltshell.xyz](https://moltshell.xyz)
2. Generate a dedicated **API Key**
3. Add it to your OpenClaw environment variables:

```
MOLTSHELL_API_KEY=sk_molt_your_key_here
```

That's it — no other configuration changes needed. The skill automatically uses your dedicated key when the environment variable is set.
