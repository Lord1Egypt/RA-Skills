
# Map Query Skill - Installation Guide

## Prerequisites

- Node.js &gt;= 18
- At least one map provider API Key

---

## Step 1: Get Map API Key

### AMap (Recommended)
1. Visit https://lbs.amap.com/
2. Register/Login account
3. Go to Console → App Management → Create New App
4. Add Key, select "Web Service" type
5. Copy your API Key

### Baidu Maps
1. Visit https://lbsyun.baidu.com/
2. Register/Login account
3. Go to Console → Create App
4. Select "Server" type
5. Copy your AK

### Tencent Maps
1. Visit https://lbs.qq.com/
2. Register/Login account
3. Go to Console → App Management → Create App
4. Select "WebService API"
5. Copy your Key

---

## Step 2: Configure Environment Variables

### Windows (PowerShell)
```powershell
# Temporary setting (current terminal only)
$env:AMAP_KEY = "your_amap_api_key"
$env:BAIDU_MAP_KEY = "your_baidu_map_key"
$env:TENCENT_MAP_KEY = "your_tencent_map_key"

# Permanent setting (requires terminal restart)
[Environment]::SetEnvironmentVariable("AMAP_KEY", "your_amap_api_key", "User")
```

### Linux/Mac (Bash/Zsh)
```bash
# Temporary setting (current terminal only)
export AMAP_KEY="your_amap_api_key"
export BAIDU_MAP_KEY="your_baidu_map_key"
export TENCENT_MAP_KEY="your_tencent_map_key"

# Permanent setting (add to ~/.bashrc or ~/.zshrc)
echo 'export AMAP_KEY="your_amap_api_key"' &gt;&gt; ~/.bashrc
source ~/.bashrc
```

---

## Step 3: Install the Skill

### Manual Installation

```powershell
# Copy to OpenClaw skills directory
xcopy /E /I map-query %USERPROFILE%\.openclaw\skills\map-query
```

```bash
# Linux/Mac
cp -r map-query ~/.openclaw/skills/map-query
```

### Restart OpenClaw Gateway

```bash
openclaw restart
```

---

## Step 4: Verify Installation

### Test Address Geocoding
```bash
node scripts/geocode.mjs "Sanlitun, Chaoyang District, Beijing"
```

### Test Nearby Search
```bash
node scripts/search.mjs "Teemall, Guangzhou" --type food --radius 1000
```

### Test via AI Conversation
Open OpenClaw, try asking:
- "Help me find what's good to eat near Nanjing East Road, Shanghai"
- "Are there any promotions near Sanlitun, Beijing recently?"

---

## FAQ

### Q: What if API calls fail?
A: Check the following:
1. Is API Key configured correctly?
2. Does API Key have sufficient quota?
3. Is network connection normal?

### Q: Address geocoding not accurate?
A: Try to provide more detailed address, including province, city, district, street, and house number.

### Q: Can I use multiple map providers at the same time?
A: Yes! The skill will automatically select available providers, or you can specify which one to use.

---

## Uninstall

```powershell
# Windows
rmdir /S /Q %USERPROFILE%\.openclaw\skills\map-query

# Linux/Mac
rm -rf ~/.openclaw/skills/map-query
```
