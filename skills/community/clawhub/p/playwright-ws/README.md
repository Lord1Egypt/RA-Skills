# 🎭 Playwright Skill for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)](https://nodejs.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40%2B-blue)](https://playwright.dev/)

> Remote browser automation for OpenClaw agents. No local browser installation required.

## ✨ Features

- 📸 **Screenshots** – Capture full-page or viewport screenshots via remote server
- 📄 **PDF Export** – Generate PDFs from any URL
- 🧪 **Test Runner** – Execute Playwright tests on remote infrastructure
- 🌐 **Multi-browser** – Chromium, Firefox, WebKit support
- 🔧 **Zero Install** – No local browsers needed

## 🚀 Quick Start

### 1. Configure WebSocket URL

```bash
export PLAYWRIGHT_WS=ws://your-playwright-server:3000
```

### 2. Take a Screenshot

```bash
node scripts/screenshot.js https://example.com screenshot.png
node scripts/screenshot.js https://example.com screenshot.png --full-page
node scripts/screenshot.js https://example.com screenshot.png --wait-for=".loaded" --delay=1000
```

### 3. Generate PDF

```bash
node scripts/pdf-export.js https://example.com page.pdf
node scripts/pdf-export.js https://example.com page.pdf --format=A4 --landscape
```

### 4. Run Tests

```bash
node scripts/test-runner.js
node scripts/test-runner.js --headed --project=chromium
```

## 📋 Requirements

- Node.js 18+
- Remote Playwright server running
- Environment variable `PLAYWRIGHT_WS` set

## 🔧 Installation

```bash
# Clone the skill
git clone https://github.com/first-it-consulting/playwright-skill.git
cd playwright-skill

# Install dependencies
npm install
```

## 📚 API Reference

Your Playwright server must expose a WebSocket endpoint for browser connections:

```
WS ws://your-server:3000/
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PLAYWRIGHT_WS` | `ws://localhost:3000` | WebSocket URL of Playwright server |

### Screenshot Options

```javascript
{
  fullPage: false,        // Capture full page or viewport
  viewport: { width: 1280, height: 720 },
  waitForSelector: null,  // Wait for element before screenshot
  delay: 0,               // Delay in ms after load
  type: 'png'             // 'png' or 'jpeg'
}
```

### PDF Options

```javascript
{
  format: 'A4',           // Page format
  landscape: false,       // Landscape orientation
  margin: { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' },
  printBackground: true   // Include background graphics
}
```

## 📖 Documentation

- [Selector Strategies](references/selectors.md) – CSS, text, role, test-id selectors
- [API Reference](references/api-reference.md) – Full Playwright API patterns

## 🧪 Testing

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- tests/screenshot.test.js
```

## 🛠️ Server Setup

Your Playwright server should expose a WebSocket endpoint for browser connections:

```
WS ws://your-server:3000/
```

### Example Server Implementation

```javascript
const { chromium } = require('playwright');

(async () => {
  const browserServer = await chromium.launchServer({
    headless: true,
    port: 3000
  });
  
  console.log(`WebSocket endpoint: ${browserServer.wsEndpoint()}`);
  // ws://localhost:3000/
})();
```

Or using Docker:

```bash
docker run -p 3000:3000 mcr.microsoft.com/playwright:v1.40.0-jammy \
  npx playwright launch-server chromium
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT © [First IT Consulting](https://github.com/first-it-consulting)

---

<p align="center">
  Made with ❤️ for OpenClaw
</p>
