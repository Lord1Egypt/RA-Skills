# Module 5: VPS Employee — 24/7 Automation and Remote Deployment

## Table of Contents
1. [VPS Provider Comparison](#vps-provider-comparison)
2. [Complete VPS Setup](#complete-vps-setup)
3. [Docker Deployment](#docker-deployment)
4. [Systemd Service Configuration](#systemd-service-configuration)
5. [Cron Jobs and Scheduling](#cron-jobs-and-scheduling)
6. [Web Automation with Playwright](#web-automation-with-playwright)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## VPS Provider Comparison

### Real Pricing Comparison (March 2025)

| Provider | Plan | CPU | RAM | Storage | Transfer | Price/Month | Best For |
|----------|------|-----|-----|---------|----------|-------------|----------|
| **Hetzner** | CX11 | 1 vCPU | 2 GB | 20 GB SSD | 20 TB | **€3.79 (~$4.10)** | Budget, EU users |
| **Hetzner** | CPX11 | 2 vCPU | 2 GB | 40 GB NVMe | 20 TB | **€4.99 (~$5.40)** | Best value |
| **Hetzner** | CPX21 | 2 vCPU | 4 GB | 80 GB NVMe | 20 TB | **€6.49 (~$7.00)** | Recommended |
| **DigitalOcean** | Basic | 1 vCPU | 1 GB | 25 GB SSD | 1 TB | **$6.00** | Beginners |
| **DigitalOcean** | Basic | 2 vCPU | 2 GB | 60 GB SSD | 3 TB | **$18.00** | Standard |
| **DigitalOcean** | Basic | 2 vCPU | 4 GB | 80 GB SSD | 4 TB | **$24.00** | Comfortable |
| **Linode** | Nanode | 1 vCPU | 1 GB | 25 GB SSD | 1 TB | **$5.00** | Light usage |
| **Linode** | Linode 2GB | 1 vCPU | 2 GB | 50 GB SSD | 2 TB | **$12.00** | Entry |
| **Linode** | Linode 4GB | 2 vCPU | 4 GB | 80 GB SSD | 4 TB | **$24.00** | Standard |
| **Vultr** | Cloud Compute | 1 vCPU | 1 GB | 25 GB SSD | 2 TB | **$5.00** | Budget |
| **Vultr** | Cloud Compute | 1 vCPU | 2 GB | 50 GB SSD | 3 TB | **$10.00** | Entry |
| **Vultr** | Cloud Compute | 2 vCPU | 4 GB | 80 GB SSD | 4 TB | **$20.00** | Standard |
| **AWS Lightsail** | 2GB | 1 vCPU | 2 GB | 60 GB SSD | 3 TB | **$10.00** | AWS ecosystem |
| **Oracle Cloud** | Always Free | 1/8 OCPU | 1 GB | 50 GB | 10 TB | **$0** | Free tier |
| **Oracle Cloud** | Always Free | 4 OCPU ARM | 24 GB | 200 GB | 10 TB | **$0** | Free tier (AMPere) |

### Provider Recommendations

| Use Case | Recommended Provider | Plan | Monthly Cost |
|----------|---------------------|------|--------------|
| **Absolute minimum** | Oracle Cloud (Free) | ARM Ampere | $0 |
| **Budget-conscious** | Hetzner | CPX11 | ~$5.40 |
| **Best value** | Hetzner | CPX21 | ~$7.00 |
| **Global presence** | DigitalOcean | 2vCPU/2GB | $18.00 |
| **Enterprise/Compliance** | AWS Lightsail | 2GB | $10.00 |
| **Asian users** | Vultr | Tokyo/Singapore | $5-20 |

---

## Complete VPS Setup

### Step 1: Create Server (Hetzner Example)

```bash
# Using hcloud CLI
hcloud server create --name openclaw-server \
  --type cpx21 \
  --image ubuntu-22.04 \
  --datacenter nbg1-dc3 \
  --ssh-key ~/.ssh/id_ed25519.pub

# Get server IP
hcloud server ip openclaw-server
```

### Step 2: Initial Server Hardening Script

```bash
#!/bin/bash
# save as: setup-vps.sh
# Run on fresh VPS as root

echo "=== OpenClaw VPS Setup ==="

# Update system
apt update && apt upgrade -y

# Create non-root user
adduser --disabled-password --gecos "" openclaw
usermod -aG sudo openclaw

# Setup SSH keys (run from your local machine first!)
# ssh-copy-id -i ~/.ssh/id_ed25519.pub openclaw@SERVER_IP

# Configure SSH hardening
cat >> /etc/ssh/sshd_config << 'EOF'
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
EOF

systemctl restart sshd

# Install essential packages
apt install -y \
  curl \
  git \
  htop \
  fail2ban \
  ufw \
  nginx \
  certbot \
  python3-certbot-nginx \
  jq \
  vim \
  unzip \
  software-properties-common \
  apt-transport-https \
  ca-certificates \
  gnupg \
  lsb-release

# Setup firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 18789/tcp # OpenClaw Gateway (if direct access needed)
ufw --force enable

# Setup fail2ban
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
EOF

systemctl enable fail2ban
systemctl start fail2ban

# Install Node.js 22+
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt-get install -y nodejs

# Verify installations
echo "Node version: $(node --version)"
echo "NPM version: $(npm --version)"

echo "=== Setup Complete ==="
echo "Next steps:"
echo "1. ssh openclaw@SERVER_IP"
echo "2. Run setup-openclaw.sh as openclaw user"
```

### Step 3: OpenClaw Installation Script

```bash
#!/bin/bash
# save as: install-openclaw.sh
# Run as openclaw user

echo "=== Installing OpenClaw ==="

# Install OpenClaw globally
npm install -g openclaw@latest

# Create config directory
mkdir -p ~/.openclaw

# Create environment file
cat > ~/.openclaw/.env << 'EOF'
# API Keys (replace with your actual keys)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxx
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxx

# Gateway security
GATEWAY_PASSWORD=$(openssl rand -base64 32)

# Other configuration
NODE_ENV=production
EOF

chmod 600 ~/.openclaw/.env

# Create OpenClaw configuration
cat > ~/.openclaw/openclaw.json << 'EOF'
{
  "agent": {
    "model": "ollama/glm-5:cloud"
  },
  "gateway": {
    "bind": "0.0.0.0",
    "port": 18789,
    "auth": {
      "mode": "password",
      "password": { "source": "env", "id": "GATEWAY_PASSWORD" }
    }
  },
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://localhost:11434"
      }
    }
  }
}
EOF

# Create workspace
mkdir -p ~/.openclaw/workspace
cd ~/.openclaw/workspace

# Initialize core files
cat > SOUL.md << 'EOF'
# SOUL.md - Agent Identity

You are a helpful AI assistant running on a VPS.
Be concise, professional, and security-conscious.
EOF

cat > AGENTS.md << 'EOF'
# AGENTS.md - Operational Rules

## Security
- Never share API keys or credentials
- Confirm destructive actions before executing
- Respect user privacy

## Automation
- Run scheduled tasks responsibly
- Report failures promptly
- Maintain detailed logs
EOF

echo "=== OpenClaw Installed ==="
echo "Gateway password: $(grep GATEWAY_PASSWORD ~/.openclaw/.env | cut -d= -f2)"
echo "Save this password securely!"
```

---

## Docker Deployment

### Complete docker-compose.yml

```yaml
version: '3.8'

services:
  openclaw:
    image: node:22-alpine
    container_name: openclaw-gateway
    restart: unless-stopped
    ports:
      - "127.0.0.1:18789:18789"  # Local only, use nginx for external
    volumes:
      - openclaw-data:/root/.openclaw
      - openclaw-workspace:/workspace
      - /var/run/docker.sock:/var/run/docker.sock:ro  # For Docker skill
    environment:
      - NODE_ENV=production
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - GATEWAY_PASSWORD=${GATEWAY_PASSWORD}
    working_dir: /workspace
    command: sh -c "npm install -g openclaw@latest && openclaw gateway"
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:18789/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - openclaw-net

  nginx:
    image: nginx:alpine
    container_name: openclaw-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - certbot-data:/etc/letsencrypt
      - certbot-www:/var/www/certbot
    depends_on:
      - openclaw
    networks:
      - openclaw-net

  certbot:
    image: certbot/certbot
    container_name: openclaw-certbot
    volumes:
      - certbot-data:/etc/letsencrypt
      - certbot-www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
    networks:
      - openclaw-net

  # Optional: Ollama for local models
  ollama:
    image: ollama/ollama:latest
    container_name: openclaw-ollama
    restart: unless-stopped
    volumes:
      - ollama-data:/root/.ollama
    # Uncomment for GPU support:
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]
    networks:
      - openclaw-net

  # Optional: Redis for caching
  redis:
    image: redis:7-alpine
    container_name: openclaw-redis
    restart: unless-stopped
    volumes:
      - redis-data:/data
    networks:
      - openclaw-net

volumes:
  openclaw-data:
  openclaw-workspace:
  certbot-data:
  certbot-www:
  ollama-data:
  redis-data:

networks:
  openclaw-net:
    driver: bridge
```

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=general:10m rate=30r/m;

    server {
        listen 80;
        server_name openclaw.yourdomain.com;

        # Certbot challenge
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$server_name$request_uri;
        }
    }

    server {
        listen 443 ssl http2;
        server_name openclaw.yourdomain.com;

        # SSL certificates (managed by certbot)
        ssl_certificate /etc/letsencrypt/live/openclaw.yourdomain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/openclaw.yourdomain.com/privkey.pem;

        # SSL hardening
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;

        # Proxy to OpenClaw
        location / {
            limit_req zone=general burst=20 nodelay;
            
            proxy_pass http://openclaw:18789;
            proxy_http_version 1.1;
            
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
    }
}
```

### .env File

```bash
# Copy to .env and fill in your values
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
GATEWAY_PASSWORD=$(openssl rand -base64 32)
```

### Docker Deployment Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f openclaw

# Update OpenClaw
docker-compose pull
docker-compose up -d

# Backup
docker run --rm -v openclaw_openclaw-data:/data -v $(pwd):/backup alpine tar czf /backup/openclaw-backup-$(date +%Y%m%d).tar.gz -C /data .

# Restore
docker run --rm -v openclaw_openclaw-data:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/openclaw-backup-YYYYMMDD.tar.gz"
```

---

## Systemd Service Configuration

### OpenClaw Service File

```ini
# /etc/systemd/system/openclaw.service
[Unit]
Description=OpenClaw Gateway
Documentation=https://docs.openclaw.ai
After=network.target

[Service]
Type=simple
User=openclaw
Group=openclaw

# Working directory
WorkingDirectory=/home/openclaw

# Environment
Environment="NODE_ENV=production"
Environment="NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache"
Environment="OPENCLAW_NO_RESPAWN=1"
EnvironmentFile=/home/openclaw/.openclaw/.env

# Create compile cache directory
ExecStartPre=/bin/mkdir -p /var/tmp/openclaw-compile-cache
ExecStartPre=/bin/chown openclaw:openclaw /var/tmp/openclaw-compile-cache

# Start command
ExecStart=/usr/bin/openclaw gateway

# Restart configuration
Restart=always
RestartSec=2
TimeoutStartSec=90
TimeoutStopSec=30

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

# Security hardening
NoNewPrivileges=false
ProtectSystem=false
ProtectHome=false
ReadWritePaths=/home/openclaw

[Install]
WantedBy=multi-user.target
```

### Commands to Enable Service

```bash
# Copy service file
sudo cp openclaw.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable openclaw

# Start service
sudo systemctl start openclaw

# Check status
sudo systemctl status openclaw

# View logs
sudo journalctl -u openclaw -f

# Restart
sudo systemctl restart openclaw
```

### Health Check Script

```bash
#!/bin/bash
# /usr/local/bin/openclaw-health-check.sh

ALERT_WEBHOOK="${ALERT_WEBHOOK:-}"
ALERTS=""

# Check OpenClaw Gateway
if ! curl -sf http://localhost:18789/health > /dev/null 2>&1; then
  ALERTS+="⚠️ OpenClaw Gateway not responding\n"
  
  # Try to restart
  systemctl restart openclaw
  sleep 5
  
  if ! curl -sf http://localhost:18789/health > /dev/null 2>&1; then
    ALERTS+="❌ OpenClaw restart failed\n"
  else
    ALERTS+="✅ OpenClaw restarted successfully\n"
  fi
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 85 ]; then
  ALERTS+="⚠️ Disk usage at ${DISK_USAGE}%\n"
fi

# Check memory
MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ "$MEM_USAGE" -gt 90 ]; then
  ALERTS+="⚠️ Memory usage at ${MEM_USAGE}%\n"
fi

# Check load
LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
if (( $(echo "$LOAD > 4.0" | bc -l) )); then
  ALERTS+="⚠️ Load average: $LOAD\n"
fi

# Send alert if needed
if [ -n "$ALERTS" ] && [ -n "$ALERT_WEBHOOK" ]; then
  curl -X POST "$ALERT_WEBHOOK" \
    -H "Content-Type: application/json" \
    -d "{\"text\":\"OpenClaw Health Check Alert:\\n$ALERTS\"}"
fi

if [ -n "$ALERTS" ]; then
  echo -e "$ALERTS"
  exit 1
else
  echo "HEARTBEAT_OK"
  exit 0
fi
```

---

## Cron Jobs and Scheduling

### OpenClaw Cron Configuration

```json5
// ~/.openclaw/openclaw.json
{
  "cron": {
    "enabled": true,
    "maxConcurrentRuns": 3,
    "sessionRetention": "24h",
    "runLog": {
      "maxBytes": "10mb",
      "keepLines": 5000
    }
  }
}
```

### Real Cron Job Templates

```bash
# Add one-shot reminder
openclaw cron add \
  --name "Server maintenance reminder" \
  --at "2026-04-01T02:00:00Z" \
  --session main \
  --message "Perform system updates and restart services" \
  --wake now

# Daily backup check
openclaw cron add \
  --name "daily-backup-check" \
  --cron "0 6 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Check last night's backup completed successfully. Verify file sizes and send summary." \
  --announce \
  --channel telegram

# Weekly report
openclaw cron add \
  --name "weekly-summary" \
  --cron "0 9 * * 1" \
  --tz "UTC" \
  --session isolated \
  --message "Generate weekly summary: system metrics, completed tasks, upcoming items." \
  --announce

# Health check every 30 minutes
openclaw cron add \
  --name "health-check" \
  --cron "*/30 * * * *" \
  --session main \
  --system-event "Run health checks from HEARTBEAT.md" \
  --wake next-heartbeat

# SSL expiry check daily
openclaw cron add \
  --name "ssl-check" \
  --cron "0 0 * * *" \
  --session isolated \
  --message "Check SSL certificate expiry for all domains. Alert if < 7 days." \
  --announce

# Daily research
openclaw cron add \
  --name "daily-research" \
  --cron "0 8 * * *" \
  --session isolated \
  --message "Research latest AI/tech news. Summarize top 5 findings." \
  --announce \
  --channel telegram
```

### System Cron for Maintenance

```bash
# Edit system crontab
sudo crontab -e

# Add these entries:

# Health check every 5 minutes
*/5 * * * * /usr/local/bin/openclaw-health-check.sh >> /var/log/openclaw-health.log 2>&1

# Daily security updates check
0 3 * * * /usr/local/bin/security-update-check.sh

# Weekly backup
0 2 * * 0 /usr/local/bin/backup-openclaw.sh

# Monthly log rotation
0 0 1 * * /usr/local/bin/rotate-openclaw-logs.sh
```

### HEARTBEAT.md Template for VPS

```markdown
# HEARTBEAT.md - VPS Automation Checklist

## System Health Checks

- [ ] **Disk Space** - Alert if < 20% free
- [ ] **Memory Usage** - Alert if > 90%
- [ ] **Load Average** - Alert if > 4.0
- [ ] **Docker Status** - Ensure all containers running

## Service Monitoring

- [ ] **OpenClaw Gateway** - Check /health endpoint
- [ ] **Nginx** - Check web server status
- [ ] **Database** (if running) - Check connectivity

## Security Checks

- [ ] **Failed SSH Attempts** - Report suspicious activity
- [ ] **UFW Status** - Ensure firewall active
- [ ] **Package Updates** - List available updates

## Backup Verification

- [ ] **Config Backup** - ~/.openclaw backed up
- [ ] **Workspace Backup** - Important files synced

## Response Codes

- `HEARTBEAT_OK` - All systems normal
- `⚠️ ALERT: [issue]` - Action needed
```

---

## Web Automation with Playwright

### Installing Playwright on VPS

```bash
# Install Playwright dependencies
sudo apt-get install -y \
  libnss3 \
  libnspr4 \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libcups2 \
  libdrm2 \
  libxkbcommon0 \
  libxcomposite1 \
  libxdamage1 \
  libxfixes3 \
  libxrandr2 \
  libgbm1 \
  libpango-1.0-0 \
  libcairo2 \
  libasound2

# Install Playwright
npm install -g playwright
npx playwright install chromium
```

### Playwright Automation Examples

```javascript
// website-monitor.js - Check if website is up
const { chromium } = require('playwright');

async function monitorWebsite(url) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  try {
    await page.goto(url, { timeout: 30000 });
    const screenshot = await page.screenshot({ fullPage: true });
    
    // Check for error indicators
    const hasError = await page.evaluate(() => {
      const errorTexts = ['error', '404', '500', 'maintenance'];
      const bodyText = document.body.innerText.toLowerCase();
      return errorTexts.some(text => bodyText.includes(text));
    });
    
    if (hasError) {
      console.log(`⚠️  ${url} showing errors`);
      // Send alert via webhook
    } else {
      console.log(`✅ ${url} is healthy`);
    }
  } catch (error) {
    console.log(`❌ ${url} failed: ${error.message}`);
  }
  
  await browser.close();
}

monitorWebsite(process.argv[2] || 'https://example.com');
```

```javascript
// price-monitor.js - Monitor product prices
const { chromium } = require('playwright');

async function checkPrice(url, selector, threshold) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.goto(url);
  const priceText = await page.locator(selector).textContent();
  const price = parseFloat(priceText.replace(/[^0-9.]/g, ''));
  
  if (price < threshold) {
    console.log(`🚨 Price dropped to $${price}! Threshold: $${threshold}`);
    // Send notification
  } else {
    console.log(`Current price: $${price}`);
  }
  
  await browser.close();
}

checkPrice(
  process.argv[2],
  process.argv[3],
  parseFloat(process.argv[4])
);
```

### Cron Job for Web Automation

```bash
# Daily website monitoring
openclaw cron add \
  --name "website-monitoring" \
  --cron "0 */6 * * *" \
  --session isolated \
  --message "Check all monitored websites. Use Playwright to screenshot homepage, verify no errors, report status." \
  --announce

# Price monitoring
openclaw cron add \
  --name "price-monitoring" \
  --cron "0 9 * * *" \
  --session isolated \
  --message "Check product prices on tracked sites. Alert if any dropped below threshold." \
  --announce
```

---

## Monitoring and Maintenance

### Log Management

```bash
# Create log rotation config
sudo tee /etc/logrotate.d/openclaw > /dev/null << 'EOF'
/home/openclaw/.openclaw/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0644 openclaw openclaw
    sharedscripts
    postrotate
        systemctl reload openclaw > /dev/null 2>&1 || true
    endscript
}
EOF

# Manual log cleanup
find /home/openclaw/.openclaw/logs -name "*.log" -mtime +30 -delete
```

### Backup Script

```bash
#!/bin/bash
# /usr/local/bin/backup-openclaw.sh

BACKUP_DIR="/backups/openclaw"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup OpenClaw data
tar czf "$BACKUP_DIR/openclaw-data-$TIMESTAMP.tar.gz" \
  -C /home/openclaw .openclaw

# Backup workspace
tar czf "$BACKUP_DIR/openclaw-workspace-$TIMESTAMP.tar.gz" \
  -C /home/openclaw .openclaw/workspace

# Clean old backups
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

# Optional: Upload to S3
# aws s3 sync "$BACKUP_DIR" s3://your-backup-bucket/openclaw/

echo "Backup completed: $TIMESTAMP"
```

### Troubleshooting

#### High Memory Usage

```bash
# Check memory usage
free -h
ps aux --sort=-%mem | head -20

# Restart OpenClaw if needed
sudo systemctl restart openclaw

# Add swap if needed
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### Gateway Not Responding

```bash
# Check if process is running
sudo systemctl status openclaw

# Check logs
sudo journalctl -u openclaw -n 100

# Check port binding
sudo ss -tlnp | grep 18789

# Restart service
sudo systemctl restart openclaw
```

#### SSL Certificate Issues

```bash
# Renew certificates manually
sudo certbot renew

# Test nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

---

**Estimated Setup Time**: 2-3 hours
**Monthly Cost**: $0-24 (depending on provider)
**Maintenance**: 30 minutes/week
