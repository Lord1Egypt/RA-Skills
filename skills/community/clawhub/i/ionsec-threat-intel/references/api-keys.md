# API Keys Setup Guide

## Quick Setup

Run setup only when you want to save keys locally:

```bash
python3 scripts/setup.py
```

This writes keys to the skill-local `config.json` file next to the skill resources.
Environment variables override values in `config.json`.

## Free Services (No Key Needed)

| Service | Notes |
|---------|-------|
| MalwareBazaar | Public API |
| URLhaus | Public API |
| DNS0 | Public resolver |
| Google DNS | Public resolver |
| Cloudflare DNS | Public resolver |
| Pulsedive | Free tier available |

## Services Requiring API Keys

| Service | Env Variable | How to Get | Free Tier? |
|---------|-------------|------------|------------|
| VirusTotal v3 | `VT_API_KEY` | https://www.virustotal.com/gui/my-apikey | Yes |
| GreyNoise | `GREYNOISE_API_KEY` | https://viz.greynoise.io/sign-up | Yes |
| Shodan | `SHODAN_API_KEY` | https://account.shodan.io/ | Yes |
| AlienVault OTX | `OTX_API_KEY` | https://otx.alienvault.com/settings | Yes |
| AbuseIPDB | `ABUSEIPDB_API_KEY` | https://www.abuseipdb.com/account/api | Yes |
| URLscan | `URLSCAN_API_KEY` | https://urlscan.io/user/signup | Yes |
| Spur.us | `SPUR_API_KEY` | https://spur.us/ | Paid |
| Validin | `VALIDIN_API_KEY` | https://app.validin.com/ | Yes |

## Local Config Format

```json
{
  "vt_api_key": "...",
  "greynoise_api_key": "...",
  "shodan_api_key": "...",
  "otx_api_key": "...",
  "abuseipdb_api_key": "...",
  "urlscan_api_key": "...",
  "spur_api_key": "...",
  "validin_api_key": "..."
}
```

## Notes

- The skill does not prompt for keys unless you explicitly run `setup`.
- Free services continue to work without configuration.
- Environment variables take precedence over `config.json`.
