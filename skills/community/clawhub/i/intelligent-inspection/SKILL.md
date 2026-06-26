---
name: intelligent-inspection
description: Intelligent workplace inspection system with guided setup, configurable inspection tasks, AI-powered image analysis, and Feishu alerting. Use when you need to monitor employee presence, conduct security patrols, or perform automated visual inspections of workspaces.
---

# Intelligent Inspection - 智能巡检

## Overview

Intelligent Inspection is an intelligent workplace monitoring system that:
- Captures images from surveillance cameras
- Uses AI to analyze images based on user-defined inspection criteria  
- Sends alerts via Feishu (or other configured channels)
- Supports guided configuration and isolated settings

This skill is designed for workplace safety, security monitoring, and employee presence verification.

## Core Features

### 1. Guided Configuration
- First-time setup wizard collects camera parameters
- User-friendly prompts for API endpoints, tokens, and device settings
- Configuration isolation in dedicated config file

### 2. Flexible Inspection Tasks
- Customizable AI prompts for different inspection scenarios
- Support for multiple camera devices and channels
- Configurable patrol schedules and triggers

### 3. AI-Powered Analysis
- Integration with OpenClaw's AI models
- User-defined analysis criteria through custom prompts
- Structured response handling for consistent results

### 4. Multi-Channel Alerting
- Primary integration with Feishu messaging
- Automatic fallback to other configured channels
- Rich message formatting with images and metadata

## Setup Requirements

### Camera System Requirements
- Supported camera APIs:
  - EZVIZ Cloud API (萤石云)
  - Generic RTSP/ONVIF cameras (via camsnap skill)
  - Custom HTTP-based capture endpoints

### Authentication Requirements
- Camera API access tokens or credentials
- Feishu bot permissions (if using Feishu alerts)

### OpenClaw Requirements
- `feishu` channel configured (for Feishu alerts)
- AI model with vision capabilities (e.g., qwen3-max, GPT-4 Vision)

## Usage Scenarios

### Employee Presence Monitoring
- Detect if employees are at their workstations
- Monitor break room usage
- Track attendance during working hours

### Security Patrols  
- Verify door/window status
- Check for unauthorized access
- Monitor restricted areas

### Facility Inspections
- Equipment status verification
- Environmental condition monitoring
- Compliance checks

## Workflow

### 1. Initial Setup (First Run)
When the skill runs for the first time:
1. Prompt user for camera system type
2. Collect API endpoint, access token, device serial, channel number
3. Ask for default inspection prompt template
4. Confirm alert channel preferences
5. Save configuration to `~/.openclaw/workspace/intelligent-inspection-config.json`

### 2. Patrol Execution
For subsequent runs:
1. Load configuration from config file
2. Capture image using configured camera parameters
3. Generate AI analysis prompt based on patrol task
4. Execute AI analysis using OpenClaw's vision model
5. Format and send alert via configured channels

### 3. Configuration Management
- Configuration stored in isolated JSON file
- Users can edit config file directly for advanced settings
- Skill validates configuration on each run
- Option to reset configuration and re-run setup

## Configuration File Structure

The configuration file (`intelligent-inspection-config.json`) contains:

```json
{
  "camera": {
    "type": "ezviz",
    "apiUrl": "https://open.ys7.com/api/open/cloud/v1/capture/save",
    "accessToken": "your-access-token",
    "deviceSerial": "C12345678",
    "channelNo": "1",
    "projectId": "intelligent-inspection-project"
  },
  "inspection": {
    "defaultPrompt": "请分析这张图片中是否有员工在工位上。如果没有人，请回复'离岗'；如果有人，请回复'在岗'。",
    "alertOn": ["离岗"],
    "includeImage": true
  },
  "alerts": {
    "enabled": true,
    "channels": ["feishu"],
    "fallbackToDefault": true
  }
}
```

## Error Handling

- Invalid camera credentials: Clear error messages with setup guidance
- AI analysis failures: Retry logic with fallback prompts
- Alert delivery failures: Log errors and attempt alternative channels
- Missing configuration: Automatically trigger setup wizard

## Privacy and Security

- Camera credentials stored locally only
- Images processed through secure AI endpoints
- No data retention beyond immediate patrol execution
- Compliance with workplace monitoring regulations recommended

## Integration Points

### OpenClaw Tools Used
- `message`: For sending alerts via configured channels
- `web_fetch`/`exec`: For camera image capture
- AI model calls: For image analysis

### External Dependencies
- Camera system APIs (EZVIZ, RTSP, etc.)
- Feishu bot (if configured as alert channel)

## Examples

### Basic Employee Monitoring
```
执行智能巡检任务
```

### Custom Inspection Task
```
执行智能巡检：检查会议室是否有人使用
```

### Reset Configuration
```
重置智能巡检配置
```

## Version History

- v1.0.0: Initial release with EZVIZ support and Feishu alerts