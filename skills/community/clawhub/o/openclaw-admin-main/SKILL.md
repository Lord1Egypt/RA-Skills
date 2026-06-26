# SKILL.md

This skill provides a comprehensive administrative web interface for managing your OpenClaw deployment. It allows you to monitor nodes, manage agent configurations, and oversee the entire ecosystem through a centralized dashboard.

## Key Features

### Node Management
- Monitor the health and connectivity status of all registered OpenClaw nodes (Android, iOS, macOS, and Linux).
- Check real-time logs and performance metrics for your Gateway and companion apps.
- Manage pairing tokens and troubleshoot connection issues.

### Agent Configuration
- Dynamically adjust agent settings and permissions without restarting services.
- View active automation tasks and scheduled cron jobs.
- Audit agent actions and system-wide changes.

### System Oversight
- Visualize system-wide resource usage.
- Manage security policies and access control lists (ACLs).
- Review historical activity and event logs.

## Installation and Setup

### Prerequisites
- A running OpenClaw Gateway.
- Node.js environment (for backend components).

### Deployment
You can deploy this admin interface using the `clawhub` CLI:

```bash
clawhub publish D:\skill\OpenClaw-Admin-main\OpenClaw-Admin-main
```

After publishing, ensure your gateway is configured to allow traffic from the admin dashboard's network location.

## Troubleshooting
If you encounter connection issues between the dashboard and the gateway, check your `gateway.remote.url` configuration and ensure all necessary ports are open in your firewall.
