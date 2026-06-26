# NWO Robotics OpenClaw Skill

**Homepage:** https://nworobotics.cloud  
**Repository:** https://huggingface.co/spaces/PUBLICAE/nwo-robotics-api-demo  
**Author:** NWO Capital

Control robots and IoT devices through natural language using the NWO Robotics API.

## Description

This skill enables OpenClaw agents to interact with the physical world by controlling robots, querying IoT sensors, and executing vision-language-action tasks through the NWO Robotics API platform.

## Features

- 🤖 **Robot Control** - Send natural language commands to robots
- 📡 **IoT Monitoring** - Query sensor data and device status
- 👁️ **Vision Tasks** - Object detection, segmentation, tracking
- 🗣️ **Voice & Gesture** - Speech and movement control
- 🧠 **Task Planning** - Multi-step robot task orchestration
- 🔒 **Secure** - User-provided API keys, no embedded credentials

## Requirements

### Environment Variables

Users must set these environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `NWO_API_KEY` | Your NWO Robotics API key | Yes |
| `NWO_USER_ID` | Your NWO Robotics user ID | Yes |
| `NWO_API_URL` | API base URL (default: https://nwo.capital/webapp) | No |

### Getting API Credentials

1. Visit https://nwo.capital/webapp/api-key.php
2. Create an account or log in
3. Generate an API key
4. Copy your API key and user ID
5. Set as environment variables in OpenClaw

## Usage

```bash
# Set environment variables
export NWO_API_KEY="your_api_key_here"
export NWO_USER_ID="your_user_id_here"
```

Then in OpenClaw:

```
User: "Check robot status"
→ Queries all connected robots and returns status

User: "Move robot_001 to position x:10, y:20"
→ Sends navigation command to robot_001

User: "What's the temperature in lab 3?"
→ Queries IoT sensors in lab 3

User: "Scan warehouse for boxes"
→ Initiates vision-based object detection
```

## API Reference

### Endpoints Used

- `POST /api-robotics.php` - Core robot control
- `POST /api-iot.php` - IoT sensor data
- `POST /api-perception.php` - Vision tasks
- `POST /api-voice.php` - Speech commands
- `POST /api-tasks.php` - Task planning
- `POST /api-safety.php` - Safety monitoring

### Rate Limits

Default limits apply:
- Free tier: 100,000 calls/month
- Prototype tier: 500,000 calls/month
- Production tier: Unlimited

## Security

- ✅ No embedded API keys
- ✅ Input validation and sanitization
- ✅ Command allowlist
- ✅ Rate limiting enforced server-side
- ✅ No raw API response passthrough

## Example Commands

| Command | Action |
|---------|--------|
| "Robot status" | List all robot states |
| "Stop all robots" | Emergency stop command |
| "Temperature check" | Query temperature sensors |
| "Pick up the red box" | VLA task execution |
| "Patrol mode on" | Activate patrol behavior |

## Support

- Website: https://nwo.capital
- API Docs: https://nwo.capital/webapp/api-key.php
- Issues: Report on GitHub

## License

MIT-0 - Free to use, modify, and redistribute. No attribution required.
