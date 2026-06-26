# openclaw-https-setup

## Description
Setup OpenClaw Gateway with HTTPS access via custom domain on VPS server. This skill automates the process of configuring Nginx reverse proxy with SSL certificates to securely expose OpenClaw Gateway service via HTTPS.

## Prerequisites
- Running OpenClaw Gateway service (typically on port 18789)
- Domain name pointing to the VPS server IP
- Root/administrator privileges on the VPS
- CentOS Stream 10 or similar RedHat-based system (commands may vary for other systems)

## Steps

### 1. Install Nginx
```bash
# For CentOS/RHEL systems
sudo dnf install -y epel-release
sudo dnf install -y nginx

# For Ubuntu/Debian systems
# sudo apt update
# sudo apt install -y nginx
```

### 2. Configure SELinux (for CentOS/RHEL)
```bash
# Check SELinux status
getenforce

# If enforcing, allow Nginx to connect to network services
sudo setsebool -P httpd_can_network_connect 1
```

### 3. Test OpenClaw Gateway locally
```bash
# Ensure OpenClaw Gateway is running and accessible locally
curl -v http://127.0.0.1:18789/
```

### 4. Create Nginx configuration
Create `/etc/nginx/conf.d/openclaw.conf` with the following content:

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN.com;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Replace `YOUR_DOMAIN.com` with your actual domain.

### 5. Test and start Nginx
```bash
sudo nginx -t  # Test configuration
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 6. Install Certbot and get SSL certificate
```bash
# For CentOS/RHEL
sudo dnf install -y certbot python3-certbot-nginx

# For Ubuntu/Debian
# sudo apt install -y certbot python3-certbot-nginx
```

### 7. Obtain SSL certificate
```bash
# Stop Nginx temporarily
sudo systemctl stop nginx

# Get certificate using standalone method
sudo certbot certonly --standalone --non-interactive --agree-tos --email your-email@example.com -d YOUR_DOMAIN.com

# Start Nginx again
sudo systemctl start nginx
```

### 8. Update Nginx configuration for HTTPS
Replace the content of `/etc/nginx/conf.d/openclaw.conf` with:

```nginx
# HTTP server - redirects to HTTPS
server {
    listen 80;
    server_name YOUR_DOMAIN.com;
    
    # Redirect all HTTP requests to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name YOUR_DOMAIN.com;

    ssl_certificate /etc/letsencrypt/live/YOUR_DOMAIN.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/YOUR_DOMAIN.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA256:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Security headers
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy no-referrer always;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host $host;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### 9. Reload Nginx configuration
```bash
sudo nginx -t  # Test configuration
sudo nginx -s reload  # Reload configuration
```

### 10. Set up automatic certificate renewal
```bash
# Add cron job for certificate renewal
sudo crontab -l | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet --nginx"; } | sudo crontab -
```

## Verification
1. Visit `https://YOUR_DOMAIN.com` in a web browser
2. Check that the site loads securely with a valid SSL certificate
3. Verify that all OpenClaw features work properly

## Troubleshooting
- If getting 502 Bad Gateway errors, check that OpenClaw Gateway is running and accessible at 127.0.0.1:18789
- If SSL certificate fails, ensure port 80 is accessible from the internet
- Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`
- Check SELinux: `sudo setsebool -P httpd_can_network_connect 1`

## Security Notes
- The configuration includes proper security headers
- SSL certificate is automatically renewed
- WebSocket connections are properly proxied
- All HTTP requests are redirected to HTTPS