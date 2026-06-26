# HKO Weather Skill for OpenClaw

Get real-time weather information from the Hong Kong Observatory (HKO) directly in your OpenClaw workspace.

## Overview

This skill provides weather data for Hong Kong using the official HKO API. It supports both English and Traditional Chinese, making it ideal for local users and international residents alike.

### Features

- 🌡️ Current weather conditions (temperature, humidity, UV index)
- 🌦️ Weather forecast (up to 7 days)
- ⚠️ Special weather announcements and warnings
- 🇭🇰 Bilingual support (English & Traditional Chinese)
- 💬 Discord integration for channel-based weather updates
- 🔄 Automatic data refresh

## Installation

### Option 1: Manual Copy

```bash
# Copy the skill directory to your OpenClaw skills folder
cp -r /path/to/hko-weather /app/skills/hko-weather

# Verify the skill is recognized
openclaw skills list
```

### Option 2: Using the Installer Script

```bash
# Make the installer executable
chmod +x install.sh

# Run the installer
./install.sh

# Follow the prompts to complete installation
```

### Option 3: Git Clone

```bash
# Clone the skill repository
git clone https://github.com/your-org/hko-weather-skill.git /app/skills/hko-weather

# The skill will be automatically available
```

### Option 4: From Tarball

```bash
# Extract the tarball to the skills directory
tar -xzf hko-weather-skill.tar.gz -C /app/skills/

# Verify installation
openclaw skills list
```

## Usage

### Basic Commands

Once installed, use these keywords to interact with the skill:

```
weather hong kong
HKO weather
Hong Kong forecast
香港天氣
天氣預報
```

### API Calls

The skill exposes the following endpoints via the OpenClaw message tool:

```bash
# Get current weather
openclaw message send --channel discord "weather now"

# Get 7-day forecast
openclaw message send --channel discord "weather forecast"

# Get weather warnings
openclaw message send --channel discord "weather warnings"
```

### Discord Integration

Configure the skill to post weather updates to a specific Discord channel:

```yaml
# In your OpenClaw configuration
skills:
  hko-weather:
    discord_channel: weather-updates
    language: traditional-chinese
    auto_post: true
    post_interval: 3600  # seconds
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HKO_LANGUAGE` | Language preference (`english` or `traditional-chinese`) | `english` |
| `HKO_DISCORD_CHANNEL` | Discord channel ID for weather updates | (none) |
| `HKO_AUTO_REFRESH` | Enable automatic weather refresh | `false` |
| `HKO_REFRESH_INTERVAL` | Refresh interval in seconds | `3600` |

### Configuration File

Create or edit `/app/skills/hko-weather/config.json`:

```json
{
  "language": "traditional-chinese",
  "discord": {
    "enabled": true,
    "channel_id": "1234567890123456789"
  },
  "auto_refresh": {
    "enabled": false,
    "interval_seconds": 3600
  }
}
```

## Troubleshooting

### Skill Not Recognized

**Problem:** OpenClaw doesn't detect the skill after installation.

**Solution:**
```bash
# Restart the OpenClaw gateway
openclaw gateway restart

# Check skill directory permissions
ls -la /app/skills/hko-weather/
```

### API Connection Failed

**Problem:** Weather data fails to load.

**Solution:**
1. Check internet connectivity
2. Verify HKO API status: https://www.hko.gov.hk/en/api/
3. Check firewall rules if behind a proxy

### Discord Integration Not Working

**Problem:** Weather updates don't appear in Discord.

**Solution:**
1. Verify the channel ID is correct
2. Ensure the bot has permission to post in that channel
3. Check Discord channel settings

### Language Not Changing

**Problem:** Skill always responds in English.

**Solution:**
1. Set `HKO_LANGUAGE=traditional-chinese` in your environment
2. Or update `config.json` with `"language": "traditional-chinese"`
3. Restart the skill: `openclaw skills reload hko-weather`

## API Documentation

### HKO Weather API

- **Base URL:** https://www.hko.gov.hk/en/api/
- **Documentation:** https://www.hko.gov.hk/en/api/WeatherInfo.htm
- **Current Weather:** https://www.hko.gov.hk/en/api/current-weather
- **9-Day Forecast:** https://www.hko.gov.hk/en/api/nine-days-weather-forecast

### Rate Limits

The HKO API is free to use but requests should be rate-limited:
- Maximum 100 requests per minute
- Recommended: Cache responses for 10-15 minutes

## Support

For issues, feature requests, or contributions:
- **GitHub Issues:** https://github.com/your-org/hko-weather-skill/issues
- **Documentation:** See CONTRIBUTING.md for contribution guidelines

## License & Attribution

### Skill Code License

The skill code itself is licensed under the MIT License - see the LICENSE file for details.

### HKO Weather Data License

**Weather data is provided by the Hong Kong Observatory (HKO) and is subject to separate terms:**

- **License:** Non-commercial use only (CC BY-NC 4.0 or equivalent)
- **Attribution Required:** Government of the Hong Kong Special Administrative Region
- **Source:** https://www.hko.gov.hk or https://www.weather.gov.hk

#### Required Attribution

When using or displaying HKO weather data, you **must** include the following attribution:

```
資料來源：香港天文台 (https://www.hko.gov.hk)
Data source: Hong Kong Observatory (https://www.hko.gov.hk)
© Government of the Hong Kong Special Administrative Region
```

#### HKO Disclaimer

The following disclaimer must be displayed prominently when using HKO data:

> 香港天文台所提供的天氣預報及氣候預測僅供參考，天文台不就該等天氣預報及氣候預測的準確性或完整性作出任何明示或暗示的保證。在任何情況下，天文台亦不就因使用該等天氣預報及氣候預測而引致或有關的任何損失、損害或費用承擔任何法律責任。
>
> The weather forecasts and climate predictions provided by the Hong Kong Observatory are for reference only. The Observatory does not warrant the accuracy or completeness of such weather forecasts and climate predictions, and does not assume any legal liability or responsibility for any loss, damage or expense resulting from the use of such weather forecasts and climate predictions.

#### Non-Commercial Use

HKO data is provided for **non-commercial use only**. You may not:
- Sell HKO data or exchange it for profit
- Use HKO data for commercial purposes without written permission from the Observatory
- Claim intellectual property rights in HKO data

For commercial use, please contact the Hong Kong Observatory for written permission.

---

*Weather data provided by the Hong Kong Observatory (HKO) - Subject to HKO Terms of Use*
