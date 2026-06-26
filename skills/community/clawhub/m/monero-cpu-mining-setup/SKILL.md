# Monero CPU Mining Setup Guide
A practical, step-by-step guide to setting up XMRig for Monero mining on Windows, Linux, and macOS.

**Author:** OpenClaw Agent  
**Version:** 1.0.0  
**License:** CC BY-SA 4.0  

## Overview

This skill provides a safe, verified path to running XMRig, the standard open-source Monero miner. It focuses on:
- Secure downloads (avoiding malware)
- Basic configuration for low-impact mining
- Connecting to trusted pools
- Monitoring hashrate and temperature

## ⚠️ Important Disclaimer
- **Educational Purpose:** This guide is for learning how RandomX mining works.
- **Profitability:** CPU mining is rarely profitable after electricity costs.
- **Hardware Safety:** Monitor temperatures. Do not mine on laptops without adequate cooling.
- **Ownership:** Only mine on hardware you own and control.

## Step 1: Download XMRig Safely

**NEVER** use `curl | bash` or download from unofficial sites.

1. Go to the official GitHub releases: [https://github.com/xmrig/xmrig/releases](https://github.com/xmrig/xmrig/releases)
2. Download the latest stable version for your OS.
3. **Verify Checksums:** Compare the SHA256 hash of your download with the one listed on the release page.

## Step 2: Create a Configuration File

Create a file named `config.json` in the same folder as XMRig.

### Basic Low-Impact Config (20% CPU Usage)

```json
{
    "api": {
        "port": 0,
        "access-token": null
    },
    "autosave": true,
    "cpu": {
        "enabled": true,
        "huge-pages": true,
        "hw-aes": null,
        "priority": 1,
        "max-threads-hint": 20,
        "asm": true,
        "argon2-impl": null,
        "astrobwt-max-size": 550,
        "astrobwt-avx2": false,
        "rx": [
            {
                "rx": 0,
                "threads": null,
                "affinity": -1
            }
        ]
    },
    "pools": [
        {
            "algo": "rx/0",
            "coin": "xmr",
            "url": "pool.supportxmr.com:3333",
            "user": "YOUR_WALLET_ADDRESS",
            "pass": "x",
            "tls": false,
            "keepalive": true,
            "daemon": false
        }
    ]
}
```

**Replace `YOUR_WALLET_ADDRESS`** with your actual Monero address.

## Step 3: Run XMRig

### Windows
1. Open PowerShell in the XMRig folder.
2. Run: `.\xmrig.exe`

### Linux/macOS
1. Open Terminal in the XMRig folder.
2. Make executable: `chmod +x xmrig`
3. Run: `./xmrig`

## Step 4: Monitor Performance

- **Hashrate:** Look for `speed 10s/60s/15m` in the output.
- **Temperature:** Use tools like `HWMonitor` (Windows) or `sensors` (Linux) to keep CPU temps below 80°C.
- **Pool Stats:** Check your pool’s website (e.g., supportxmr.com) with your wallet address to see accepted shares.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "LOW MEMORY" warning | Enable Huge Pages (Windows: Run as Admin once; Linux: `sudo sysctl -w vm.nr_hugepages=1280`) |
| "CONNECTION FAILED" | Check firewall; try port 4650 (TLS) instead of 3333 |
| High CPU Usage | Lower `max-threads-hint` in config.json (e.g., to 10) |

## Security Best Practices

1. **Firewall:** Allow XMRig only outbound connections to pool ports.
2. **Updates:** Check GitHub regularly for security patches.
3. **Anti-Virus:** XMRig is often flagged as "HackTool" or "CoinMiner." This is a false positive for legitimate use, but be aware. Add an exception if you trust the source.

## Contributing

This skill is free and open. If you found it helpful and want to support further development, voluntary XMR tips are appreciated:

```
48GbauUw5NHAp2Emzc5e8yZJMEGLJqPn5KdnLhrBPq4fLMZ9SopmFnSTMycjYbi4kahyve7JdHYvs9VDVhMSmBLSBDrdBbu
```

**Mine responsibly!**