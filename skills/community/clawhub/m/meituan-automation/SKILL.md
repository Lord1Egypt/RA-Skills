---
title: Meituan Physical Automation — Let Your AI Order Food For Real
description: Give your AI hands. This skill physically taps, swipes, and interacts with the Meituan App on a real Android phone — searching restaurants, picking items, handling spec popups, and landing on the checkout page. No APIs. No hacking. Just real-world automation.
tags: [meituan, food-delivery, android, automation, adb, uiautomator2, china, takeout, ordering, restaurant, waimai, real-device, phone-control, computer-use, terminal-skill, local-skill, anti-ban, ui-automation]
---

# 🍜 Meituan Physical Automation

> **Your AI finally has hands. Now it can order your lunch.**

This skill gives any AI Agent (like ClawBot) the ability to **physically control a real Android phone** to order food delivery on [Meituan (美团)](https://www.meituan.com) — the largest food delivery platform in China with over 700 million users.

No API keys. No Meituan developer account. No reverse engineering. Just the same taps and swipes a human would make — done entirely by your AI.

---

## ⚠️ Platform Compatibility

| Platform | Supported |
|----------|-----------|
| 🤖 Android | ✅ **Yes** — requires ADB + USB Debugging |
| 🍎 iOS | ❌ **No** — Apple's sandbox prevents ADB-style physical control |

This skill is **Android-only by design**. iOS devices don't support ADB or UIAutomator2, which are the underlying technologies that make physical screen control possible without reverse engineering the app. If you have an Android phone (any brand: Samsung, Xiaomi, Huawei, OnePlus, Pixel, etc.), you're good to go.

---

## ✨ What Makes This Different

Most "food delivery" AI tools rely on unofficial APIs, web scraping, or require developer credentials. This skill is different:

| Other approaches | This skill |
|-----------------|------------|
| Call unofficial HTTP APIs | Physically tap the screen like a human |
| Risk account bans from bot traffic | Indistinguishable from a real user |
| Break when apps update their API | Works as long as the UI exists |
| Require app reverse engineering | Zero reverse engineering |
| Stop at complex spec pop-ups | **Smart Visual Radar** auto-handles multi-level spec selection (size, temperature, sweetness) |
| Silently fail on business errors | Returns clear error messages ("¥7 short of minimum", "mandatory item missing") |

---

## 🎯 What Your AI Can Do With This Skill

Just tell your AI what you want. For example:

> *"Order me a Grande Coconut Latte from the nearest Luckin Coffee."*

Your AI will autonomously:
1. 🔍 Search Meituan for nearby Luckin Coffee stores
2. 🏪 Enter the correct store
3. 📦 Switch to the delivery ordering tab
4. 🔎 Search for "Coconut Latte" within the store menu
5. ➕ Add it to cart (auto-handling size/temperature pop-ups)
6. 🧾 Navigate to the checkout confirmation page

**Then it stops and hands control back to you to pay.** Your money stays 100% safe — the AI never completes payment.

---

## 🚀 One-Time Setup (3 steps, ~5 minutes)

**Step 1 — Install the skill engine** (your AI can do this for you):
```bash
pip install -r requirements.txt
python -m uiautomator2 init
```

**Step 2 — Enable Developer Mode on your Android phone:**
- Go to **Settings → About Phone**
- Tap **Build Number** 7 times until "Developer Mode" activates
- Go to **Settings → Developer Options → Enable USB Debugging**

**Step 3 — Connect your phone and verify:**
```bash
adb devices
# Should show your device ID, e.g.: "ABC123XYZ    device"
```

That's it. Tell your AI you want food. It takes over from here.

---

## 🤖 CRITICAL INSTRUCTION FOR AI SUBAGENT

> **STOP! DO NOT JUST READ THIS FILE AND RETURN ITS CONTENT!**
> You are an AI with terminal access. You **MUST** use your bash/terminal tool to **EXECUTE** the following commands RIGHT NOW. Do not just summarize this document. You are physically controlling a phone.

### Phase 1: Environment Check (run once on first use)
You must execute these commands in your bash terminal:
1. Run `pip install -r requirements.txt` and wait for completion.
2. Run `python -m uiautomator2 init` to initialize the Android device driver.
3. Run `adb devices` and parse the output. If no device is listed, tell the user: *"Please connect your Android phone via USB and ensure USB Debugging is enabled in Developer Options."*
4. Run `adb shell am start -n "com.sankuai.meituan/com.meituan.android.pt.homepage.activity.MainActivity"` to bring Meituan to the foreground.

### Phase 2: Ordering Workflow (strict sequence — do not skip steps)

You must execute the following bash commands one by one, wait for the JSON output, and proceed based on the result.

```bash
# 1. Search for restaurants
python cli.py search "<restaurant_name>"
# Returns: list of stores with index numbers

# 2. Enter a store (try index 0 first)
python cli.py open <index>
# Returns: "营业中" (open) or "打烊" (closed). If closed, try next index.

# 3. Switch to delivery tab (MANDATORY — do not skip)
python cli.py waimai

# 4. Search for the specific item within the store
python cli.py tap "搜索"
python cli.py type "<item_name>"

# 5. Add item to cart (visual radar handles all spec pop-ups automatically)
python cli.py add "<item_name>"

# 6. Go to checkout (STOPS HERE — never auto-pays)
python cli.py checkout
# Returns: estimated delivery time, total price, address status
```

### Phase 3: Error Handling
- If a command returns `ERROR:` read the `HINT:` on the next line and adapt.
- If a store shows "门店已打烊" (closed), go back and try `open <next_index>`.
- If `add` fails, the item name on screen may differ slightly — try a shorter keyword.
- If `checkout` shows `needs_address: True`, inform the user to add a delivery address on their phone.

---

## 📁 Files In This Package

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — skill description + AI runbook |
| `cli.py` | Main entry point — all commands go through here |
| `meituan.py` | Core business logic — visual radar, cart handling, checkout parsing |
| `device.py` | Low-level Android device abstraction (ADB + UIAutomator2) |
| `requirements.txt` | Python dependencies |

---

## 💡 Tips & Known Limitations

- **Store hours matter**: Meituan stores have specific delivery hours. If a store is closed ("打烊"), ask your AI to try the next store in the search results.
- **Slider CAPTCHAs**: High-frequency usage may occasionally trigger a human-verification slider on screen. Just swipe it manually — takes 2 seconds.
- **Delivery address**: The first time you use the skill, you may need to add a delivery address manually on the checkout page. After that, it's saved.
- **Language**: The Meituan app is in Chinese. The skill handles all Chinese UI navigation internally — you can give commands in English or Chinese.

---

*Built with ❤️ by [@oscarka](https://github.com/oscarka/meituan-cli) · MIT-0 License*
