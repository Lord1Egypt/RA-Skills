# Mxchip Smart Control

**Control smart home devices configured in Smart Plus APP (智家精灵)**

---

## 📋 Project Information

- **Skill Name:** mxchip-smart-control
- **Version:** 1.0.2
- **Developer:** Shanghai MXCHIP Information Technology Co., Ltd. (上海庆科信息技术有限公司)
- **Official Website:** https://www.mxchip.com/
- **GitHub:** https://github.com/mxchip
- **License:** MIT-0 (Free to use, modify, and redistribute)
- **Protocol:** MCP (Model Context Protocol) + JSON-RPC 2.0
- **Target Application:** Smart Plus APP (智家精灵)

---

## 🏢 About MXCHIP

**Shanghai MXCHIP Information Technology Co., Ltd.** (上海庆科信息技术有限公司) is a leading Chinese IoT solution provider founded in 2005.

### Core Business
- **IoT Hardware**: Wi-Fi modules, Bluetooth modules, IoT development boards
- **Cloud Services**: MXCHIP Cloud platform for device management
- **Smart Home**: Smart Plus APP - Intelligent home automation application
- **AI Integration**: MCP (Model Context Protocol) support for AI assistants

### Smart Plus APP (智家精灵)
**Smart Plus** is MXCHIP's official smart home application that enables users to:
- Configure and manage IoT devices
- Create automation scenes
- Control devices remotely
- Integrate with AI assistants via MCP

---

## 🎯 Features

### MCP Tools (4)
1. **list_home_devices_and_scenes** - Query all devices and scenes
2. **control_device** - Control device power (turn on/off)
3. **control_air_conditioner** - Control AC (temperature, mode)
4. **trigger_scene** - Trigger automation scenes

### MCP Prompts (3)
1. **device_control** - Device control assistant
2. **scene_trigger** - Scene control assistant
3. **smart_home_assistant** - Full-featured smart home assistant

---

## 🚀 Quick Start

### For Users (ClawHub Installation)

**📥 Installation Steps:**

1. **Visit ClawHub**: https://clawhub.ai
2. **Search**: "mxchip-smart-control"
3. **Click**: Install button
4. **Get Token**: https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth
5. **Configure**: Set environment variable
   ```bash
   export MXCHIP_OAUTH_TOKEN="oauth2_YOUR_TOKEN_HERE"
   ```

**📚 Detailed Guides:**
- **Quick Start (3 min)**: [MXCHIP_QUICK_START.md](MXCHIP_QUICK_START.md)
- **Full Installation Guide**: [MXCHIP_USER_INSTALL_GUIDE.md](MXCHIP_USER_INSTALL_GUIDE.md)

### For Developers

```bash
# Install dependencies
pip install requests

# Set OAuth token
export MXCHIP_OAUTH_TOKEN="oauth2_YOUR_TOKEN_HERE"
```

### Get OAuth Token
1. Visit: https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth
2. Login with your Smart Plus APP account
3. Copy the OAuth2 access token

### Usage

```python
from mxchip_mcp_client import MxchipMCPClient

# Initialize client
client = MxchipMCPClient()

# List all devices and scenes
result = client.list_home_devices_and_scenes()
devices = result.get('devices', [])
scenes = result.get('scenes', [])

# Control device
client.control_device("device_id", "TurnOnRequest")

# Control air conditioner
client.control_air_conditioner(
    "ac_device_id",
    "SetTemperatureRequest",
    temperature=26
)

# Trigger scene
client.trigger_scene("sceneid_coming_home")

# Close connection
client.close()
```

---

## 📚 Documentation

- **Skill Documentation:** `SKILL.md`
- **API Reference:** `references/api_reference.md`
- **Python SDK:** `scripts/mxchip_mcp_client.py`

---

## 🔧 Supported Devices

### Device Categories
- **SWITCH**: Smart switches and outlets (12+ supported)
- **LIGHT**: Smart lights and bulbs (20+ supported)
- **AIR_CONDITION**: Air conditioners (16+ supported)

### Device Operations
- **Switches**: Turn on/off
- **Lights**: Turn on/off, brightness control
- **Air Conditioners**: 
  - Set temperature (16-32°C)
  - Set mode (COOL, HEAT, AUTO, FAN, DEHUMIDIFICATION, SLEEP)
  - Increment/decrement temperature

---

## 🌟 Use Cases

### Natural Language Control
```
User: "列出我的智能设备"
User: "打开卢沟桥智能插座"
User: "把财务室空调调到26度"
User: "触发上班场景"
```

### Scene Automation
- **上班场景**: Automatically turn on necessary devices
- **下班场景**: Turn off all devices
- **午休场景**: Adjust lighting for break time
- **区域控制**: Control devices by location

---

## 🔐 Security

- OAuth token required for all operations
- Token should be kept confidential
- Token has expiration time (regenerate as needed)
- Never commit tokens to version control

---

## 📞 Support

- **Official Website:** https://www.mxchip.com/
- **OAuth Token:** https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth
- **Documentation:** See skill package documentation
- **Issues:** Contact MXCHIP support team

---

## 📄 License

**MIT-0 License**
- Free to use, modify, and redistribute
- No attribution required
- Full license: https://spdx.org/licenses/MIT-0.html

---

## 🤝 Credits

**Developed by:** Shanghai MXCHIP Information Technology Co., Ltd.  
**MCP Implementation:** Based on Model Context Protocol specification  
**Protocol:** JSON-RPC 2.0 over HTTP

---

## 📝 Changelog

### v1.0.2 (2026-03-23)
- ✅ Fixed JSON parsing for MCP response structure
- ✅ Updated environment variable from ZHIJIA to MXCHIP
- ✅ Added comprehensive documentation
- ✅ Added Shanghai MXCHIP company information
- ✅ Added Smart Plus APP information

### v1.0.1 (2026-03-23)
- ✅ Initial release
- ✅ Support for 4 MCP tools
- ✅ Support for 3 MCP prompts

---

**© 2026 Shanghai MXCHIP Information Technology Co., Ltd. All rights reserved.**
