# 🚀 Deployment Guide: Polymarket Sniper Bot

Follow these steps to deploy your autonomous sniper bot on a Linux server (EC2, VPS, or local).

## 1. Prerequisites
- **Python 3.12+** installed.
- **Git** installed.
- A **Polygon RPC URL** (from Alchemy, QuickNode, etc.).
- A **Polymarket Wallet** with some MATIC (for gas) and USDC.e (for trading).
- **Polymarket API Keys** (from Settings -> API on Polymarket.com).

## 2. Installation
Clone the repository and run the bootstrap script:
```bash
git clone https://github.com/wjs829/polymarket-sniper-skill.git
cd polymarket-sniper-skill/scripts
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

## 3. Configuration
Edit the `config.yaml` file created by the bootstrap script:
```yaml
polygon_rpc_url: "https://your-rpc-url"
wallet_address: "0x..."
wallet_private_key: "your-private-key"
clob_api_key: "..."
clob_api_secret: "..."
clob_api_passphrase: "..."
```

## 4. Trading Mode

The bot runs in **Simulation Mode** by default (no real trades). To enable live trading:

1. Ensure your wallet is funded with MATIC (gas) and USDC.e (trading).
2. Configure all required Polymarket CLOB API credentials in `config.yaml`.
3. Set `live_trading: true` in your configuration (or simply ensure simulation mode is disabled).

The bot will validate wallet balance and API connectivity on startup. Logs will indicate the active mode.

**Note:** Live trading involves real funds. thoroughly test in simulation first.

## 5. Run the Dashboard
Start the real-time monitoring UI:
```bash
python3 dashboard.py
```
View the dashboard at `http://your-server-ip:5000`.

## 6. Enable Automation (OpenClaw)
If you are using OpenClaw, register the agent and add the cron jobs:
```bash
openclaw agents add sniper --workspace . --model google/gemini-3-flash-preview
openclaw cron add --name "Sniper: Scan" --cron "*/5 * * * *" --agent sniper --message "scan"
```

## 🛡️ Security Best Practices
- **Use a Burner Wallet:** Never use your main storage wallet.
- **Restrict Ports:** In AWS/Your Firewall, only allow your own IP to access Port 5000.
- **Key Scoping:** Ensure your API keys have "Trade" permissions enabled but keep your private key secure.

---
*Support: [Your Email/Discord]*
