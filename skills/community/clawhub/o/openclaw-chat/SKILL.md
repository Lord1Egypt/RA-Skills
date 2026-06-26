# openclaw-chat

> OpenClaw Mobile App - Multi-Agent Chat & Service Management

## Features

1. **OpenClaw Native Chat UI** - Mobile interface designed specifically for OpenClaw
2. **Agent Team Group Discussion** - Create groups for multi-agent collaboration
3. **Remote & Local Memory Sync** - Agent memory syncs automatically
4. **Integrated Remote Management UI** - Manage local services from anywhere
5. **Local Port & App Status Management** - Monitor and control local service status in real-time
6. **Self-Healing Emergency Recovery** - Main Agent auto-repairs system failures
7. **Android APK Available / iOS Pending Review** - Full platform support

## Features

- 💬 **Agent Chat** - Private chat with any Agent
- 🤖 **Agent List** - View all Agents' status and models
- 👥 **Group Management** - Manage Agent groups
- ⚙️ **Service Management** - Add/edit/delete local services, start/stop control
- ⏰ **Cron Jobs** - Manage scheduled tasks
- 📝 **Logs** - Real-time system log viewer
- 🌐 **i18n** - One-click Chinese/English switch
- 📱 **PWA** - Install to home screen

## Installation

### Mobile Browser (PWA - Recommended)
Open http://YOUR_IP:5177, add to home screen

### Android APK
APK location: `android/app/build/outputs/apk/debug/app-debug.apk`

### iOS App
Requires Mac + Xcode for building. See build instructions below.

## Development

```bash
clawhub install openclaw-chat
cd ~/.clawhub/skills/openclaw-chat
npm install
npm run dev
```

## Build Native Apps

### iOS (Requires Mac + Xcode)
```bash
npm run build
npx cap add ios
npx cap open ios
# In Xcode: Product > Archive
```

### Android
```bash
# Requires Java 21
brew install openjdk@21
export JAVA_HOME=$(brew --prefix openjdk@21)

npm run build
npx cap add android
npx cap sync android
cd android && ./gradlew assembleDebug
# APK at: android/app/build/outputs/apk/debug/
```

## Tech Stack

- React 18 + TypeScript
- Vite (PWA)
- TailwindCSS
- Capacitor

## License

MIT
