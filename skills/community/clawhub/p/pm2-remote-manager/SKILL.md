---
name: pm2-manager
description: SSH-based PM2 service management for remote servers. List processes, restart/stop services, view logs, monitor CPU/memory usage, and perform common PM2 operations on production servers.
---

# PM2 Manager

Manage remote PM2 processes via SSH connection. This skill provides commands for monitoring, controlling, and maintaining Node.js applications deployed with PM2 process manager on remote servers.

## Prerequisites

- SSH access to target server
- PM2 installed on remote server
- SSH key-based authentication (recommended)
- Target server accessible from local machine

## Usage

### Basic Process Management

**List all processes:**
```bash
ssh user@server "pm2 list"
ssh user@server "pm2 status"
```

**Start/Stop/Restart services:**
```bash
# Start specific app
ssh user@server "pm2 start ecosystem.config.js"
ssh user@server "pm2 start app.js --name myapp"

# Restart specific process
ssh user@server "pm2 restart myapp"
ssh user@server "pm2 restart 0"  # by ID

# Stop process
ssh user@server "pm2 stop myapp"
ssh user@server "pm2 delete myapp"  # completely remove

# Restart all processes
ssh user@server "pm2 restart all"
```

### Log Management

**View real-time logs:**
```bash
# All processes
ssh user@server "pm2 logs"

# Specific process
ssh user@server "pm2 logs myapp"
ssh user@server "pm2 logs 0"

# Last N lines
ssh user@server "pm2 logs myapp --lines 100"

# Error logs only
ssh user@server "pm2 logs myapp --err"
```

**Log rotation and cleanup:**
```bash
# Flush all logs
ssh user@server "pm2 flush"

# Install log rotation
ssh user@server "pm2 install pm2-logrotate"
```

### Monitoring and Performance

**Real-time monitoring:**
```bash
# Monitor dashboard
ssh user@server "pm2 monit"

# Show detailed info
ssh user@server "pm2 show myapp"
ssh user@server "pm2 describe 0"
```

**Memory and CPU usage:**
```bash
# List with memory usage
ssh user@server "pm2 list --sort memory"

# JSON output for parsing
ssh user@server "pm2 jlist"
ssh user@server "pm2 prettylist"
```

### Advanced Operations

**Environment management:**
```bash
# Start with different environment
ssh user@server "pm2 start ecosystem.config.js --env production"
ssh user@server "pm2 start app.js --env development"

# Update environment variables
ssh user@server "pm2 restart myapp --update-env"
```

**Process scaling:**
```bash
# Scale to 4 instances
ssh user@server "pm2 scale myapp 4"

# Start in cluster mode
ssh user@server "pm2 start app.js -i max"  # use all CPUs
ssh user@server "pm2 start app.js -i 4"    # 4 instances
```

**Health checks and auto-restart:**
```bash
# Set max memory before restart
ssh user@server "pm2 start app.js --max-memory-restart 100M"

# Set restart delay
ssh user@server "pm2 start app.js --restart-delay 3000"

# Disable auto-restart
ssh user@server "pm2 start app.js --no-autorestart"
```

### Ecosystem Configuration

Create `ecosystem.config.js` for complex deployments:
```javascript
module.exports = {
  apps: [
    {
      name: 'main-app',
      script: './app.js',
      instances: 2,
      env: {
        NODE_ENV: 'development',
        PORT: 3000
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 8080
      }
    },
    {
      name: 'worker',
      script: './worker.js',
      instances: 1,
      cron_restart: '0 0 * * *',  // restart daily
      max_memory_restart: '200M'
    }
  ]
};
```

**Deploy with ecosystem:**
```bash
# Upload and start
scp ecosystem.config.js user@server:/path/to/app/
ssh user@server "cd /path/to/app && pm2 start ecosystem.config.js"

# Production environment
ssh user@server "cd /path/to/app && pm2 start ecosystem.config.js --env production"
```

### Startup and Persistence

**Save current process list:**
```bash
ssh user@server "pm2 save"
```

**Setup startup script:**
```bash
# Generate startup script
ssh user@server "pm2 startup"
# Follow the instructions to run the generated command

# Save and enable startup
ssh user@server "pm2 save && pm2 startup systemd"
```

### Batch Operations Script Example

```bash
#!/bin/bash
# pm2-batch-restart.sh

SERVER="user@10.0.0.213"
APPS=("main-app" "linebot-server" "liff-server")

echo "Restarting PM2 services on $SERVER..."

for app in "${APPS[@]}"; do
    echo "Restarting $app..."
    ssh $SERVER "pm2 restart $app"
    if [ $? -eq 0 ]; then
        echo "✅ $app restarted successfully"
    else
        echo "❌ Failed to restart $app"
    fi
done

echo "Checking status..."
ssh $SERVER "pm2 list"
```

### Troubleshooting

**Common issues and solutions:**

1. **Process not starting:**
```bash
ssh user@server "pm2 logs myapp --err"
ssh user@server "pm2 show myapp"
```

2. **High memory usage:**
```bash
ssh user@server "pm2 restart myapp"  # Quick fix
ssh user@server "pm2 reload myapp"   # Zero-downtime restart
```

3. **Port conflicts:**
```bash
ssh user@server "pm2 show myapp | grep 'port'"
ssh user@server "netstat -tlnp | grep :3000"
```

4. **Clear PM2 cache:**
```bash
ssh user@server "pm2 kill && pm2 start ecosystem.config.js"
```

### Production Example (Pro-Power System)

```bash
# Production server management
SERVER="administrator@10.0.0.213"

# Check all services
ssh $SERVER "pm2 list"

# Restart specific services
ssh $SERVER "pm2 restart main-app"
ssh $SERVER "pm2 restart linebot-server"
ssh $SERVER "pm2 restart ProPower-tunnel"

# View logs
ssh $SERVER "pm2 logs main-app --lines 50"

# Monitor performance
ssh $SERVER "pm2 monit"
```

This skill streamlines remote PM2 management, making it easy to maintain Node.js applications running on production servers.