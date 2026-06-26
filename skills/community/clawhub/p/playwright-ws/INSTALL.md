# Installation

## Prerequisites

- Node.js 18+
- Playwright WebSocket server

## Install

```bash
cd playwright-skill
npm install
```

## Configure

Set your Playwright server URL:

```bash
export PLAYWRIGHT_WS=ws://your-server:3000
```

## Verify

```bash
bash test.sh
```