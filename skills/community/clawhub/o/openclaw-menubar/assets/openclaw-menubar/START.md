# 🚀 START HERE!

## Your OpenClaw Menu Bar App is Ready!

### ⚡ Quick Start (30 seconds)

```bash
cd /Users/prabhanjansharma/.openclaw/workspace/openclaw-menubar
npm start
```

**That's it!** You should see:
1. ✅ A menu bar icon appear (top right of screen)
2. ✅ Click it to open chat window
3. ✅ **Auto-discovers gateway** - No configuration needed!
4. ✅ Type a message and hit Enter!

---

## 📋 What You Get

✅ **Menu bar access** - Always available  
✅ **Auto-discovery** - Finds OpenClaw Gateway automatically  
✅ **Zero configuration** - Just works!  
✅ **Quick chat** - Instant OpenClaw connection  
✅ **Drag & drop files** - Drop images, docs, code  
✅ **Model switching** - Sonnet (fast) ↔ Opus (powerful)  
✅ **Keyboard shortcut** - `Cmd+Shift+O` to toggle  
✅ **Message history** - Persists across restarts  
✅ **Live status** - Shows connection state  
✅ **Auto-reconnect** - Handles disconnections gracefully  

---

## 🎨 Smart Auto-Discovery

The app automatically:
- ✅ **Reads your OpenClaw config** (`~/.openclaw/openclaw.json`)
- ✅ **Detects gateway URL** (localhost, LAN, custom)
- ✅ **Uses your gateway token** (no manual entry)
- ✅ **Saves connection** for faster startup
- ✅ **Shows setup screen** if gateway offline

**No hardcoded URLs!** Works on any machine with OpenClaw installed.  

---

## 🎯 Try These Commands

Once the app is open:

**Basic chat:**
```
Hey, what's the time?
```

**Trading scan:**
```
Scan BTC for trading setups
```

**Model switch:**
- Click dropdown → Select "Opus"
- Ask a complex question
- Switch back to "Sonnet" to save tokens

**Drag & drop:**
- Drag any file from Finder into chat
- Send with a message: "Analyze this file"

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+Shift+O` | Show/hide app |
| `Enter` | Send message |
| `Shift+Enter` | New line in message |

---

## 🛠️ Optional: Add Custom Icon

Want the 🦞 claw icon in menu bar?

```bash
# Install ImageMagick
brew install imagemagick

# Create icons
./create-icon.sh

# Edit main.js and uncomment icon line
# Then restart app
```

---

## 🔧 Troubleshooting

### "Cannot connect to Gateway"

**Check gateway is running:**
```bash
openclaw status
```

**If offline, start it:**
```bash
openclaw gateway start
```

### "Menu bar icon not appearing"

- Wait 5-10 seconds after `npm start`
- Check Activity Monitor for "Electron" process
- Try quitting and restarting

### "App crashes on start"

```bash
# Clear cache and retry
rm -rf ~/Library/Application\ Support/openclaw-menubar
npm start
```

---

## 📦 Build Standalone App

Want a double-clickable .app file?

```bash
npm run build
```

Creates: `dist/OpenClaw.app`

Drag it to Applications folder!

---

## 🎉 You're All Set!

**Next:** Just run `npm start` and click the menu bar icon!

Questions? Check `README.md` for full documentation.

---

**Built with ❤️ for quick OpenClaw access** 🦞
