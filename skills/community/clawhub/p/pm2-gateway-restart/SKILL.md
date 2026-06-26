---
name: pm2-gateway-restart
description: Use PM2 to reliably restart OpenClaw gateway on Windows. Use when the user wants to restart the OpenClaw gateway, fix port conflicts, or recover from a crashed gateway. This skill handles the Windows-specific issues with FIN_WAIT_2 TCP connections and scheduled task failures that plague the standard openclaw gateway start/stop commands.
---

# PM2 Gateway Restart

This skill provides reliable gateway restart using PM2 process manager instead of the built-in openclaw gateway commands.

## Why PM2?

The standard `openclaw gateway start/stop` commands on Windows suffer from:
- FIN_WAIT_2 TCP connection timeouts (~60 seconds)
- Scheduled task race conditions
- Inconsistent startup state reporting

PM2 handles process resurrection and provides reliable restarts.

## Commands

### Quick Restart (Production)
```powershell
pm2 restart openclaw-gateway
```
Wait ~15 seconds for the gateway to fully initialize, then verify with:
```powershell
curl http://127.0.0.1:18789/
```

### Full Cycle Restart (When Issues Persist)
```powershell
pm2 restart openclaw-gateway; sleep 3; pm2 restart openclaw-gateway
```

### Check Status
```powershell
pm2 status
pm2 logs openclaw-gateway --lines 50
```

### Start Gateway (If Not Running)
```powershell
pm2 start "D:/Program Files/nodejs/node.exe" --name "openclaw-gateway" -- "C:/Users/Administrator/AppData/Roaming/npm/node_modules/openclaw/dist/index.js" gateway --port 18789
```

## Troubleshooting

### Port Still in Use After Restart
Wait 65 seconds for Windows TCP timeout to clear FIN_WAIT_2 connections, then:
```powershell
pm2 restart openclaw-gateway
```

### RPC Probe Fails But Gateway Listening
The RPC check may fail briefly during startup. Wait 15 seconds and retry:
```powershell
curl http://127.0.0.1:18789/
```

### PM2 Process Not Found
Reinstall the gateway process:
```powershell
pm2 start "D:/Program Files/nodejs/node.exe" --name "openclaw-gateway" -- "C:/Users/Administrator/AppData/Roaming/npm/node_modules/openclaw/dist/index.js" gateway --port 18789
pm2 save
```

## Setup (One Time)
```powershell
npm install -g pm2
pm2 start "D:/Program Files/nodejs/node.exe" --name "openclaw-gateway" -- "C:/Users/Administrator/AppData/Roaming/npm/node_modules/openclaw/dist/index.js" gateway --port 18789
pm2 save
```
