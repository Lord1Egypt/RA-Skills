#!/bin/bash

# Script to automate OpenClaw Gateway HTTPS setup
# Usage: ./setup_openclaw_https.sh <domain> <email>

DOMAIN=$1
EMAIL=$2

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "Usage: $0 <domain> <email>"
    echo "Example: $0 openclaw.example.com admin@example.com"
    exit 1
fi

echo "Setting up OpenClaw Gateway with HTTPS for domain: $DOMAIN"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root"
   exit 1
fi

# Check if sudo is available
if ! command -v sudo &> /dev/null; then
    echo "sudo is required but not installed"
    exit 1
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo "Cannot detect OS"
    exit 1
fi

echo "Detected OS: $OS"

# Install Nginx
echo "Installing Nginx..."
if [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Rocky"* ]] || [[ "$OS" == *"AlmaLinux"* ]]; then
    sudo dnf install -y epel-release
    sudo dnf install -y nginx certbot python3-certbot-nginx
elif [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
    sudo apt update
    sudo apt install -y nginx certbot python3-certbot-nginx
else
    echo "Unsupported OS: $OS"
    exit 1
fi

# Configure SELinux if present
if command -v getenforce &> /dev/null; then
    if [ "$(getenforce)" = "Enforcing" ]; then
        echo "Configuring SELinux for Nginx network connections..."
        sudo setsebool -P httpd_can_network_connect 1
    fi
fi

# Test OpenClaw Gateway locally
echo "Testing OpenClaw Gateway..."
if ! curl -s http://127.0.0.1:18789/ > /dev/null; then
    echo "Warning: Cannot reach OpenClaw Gateway at http://127.0.0.1:18789"
    echo "Make sure OpenClaw Gateway is running before proceeding."
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create Nginx configuration
CONFIG_FILE="/etc/nginx/conf.d/openclaw-$DOMAIN.conf"

echo "Creating Nginx configuration for $DOMAIN..."
sudo tee $CONFIG_FILE > /dev/null <<EOF
# HTTP server - redirects to HTTPS
server {
    listen 80;
    server_name $DOMAIN;

    # Redirect all HTTP requests to HTTPS
    return 301 https://\$server_name\$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name $DOMAIN;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

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
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host \$host;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

# Test Nginx configuration
echo "Testing Nginx configuration..."
if ! sudo nginx -t; then
    echo "Nginx configuration test failed. Aborting."
    exit 1
fi

# Start Nginx if not running
if ! sudo systemctl is-active --quiet nginx; then
    echo "Starting Nginx..."
    sudo systemctl start nginx
    sudo systemctl enable nginx
fi

# Get SSL certificate
echo "Obtaining SSL certificate for $DOMAIN..."
sudo certbot certonly --nginx --non-interactive --agree-tos --email $EMAIL -d $DOMAIN

if [ $? -ne 0 ]; then
    echo "Failed to obtain SSL certificate. Trying standalone method..."
    sudo systemctl stop nginx
    sleep 3
    sudo certbot certonly --standalone --non-interactive --agree-tos --email $EMAIL -d $DOMAIN
    sudo systemctl start nginx
    
    if [ $? -ne 0 ]; then
        echo "Failed to obtain SSL certificate with both methods."
        exit 1
    fi
fi

# Reload Nginx to apply final configuration
echo "Reloading Nginx..."
sudo nginx -s reload

# Set up automatic renewal
echo "Setting up automatic certificate renewal..."
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet --nginx") | crontab -

echo "Setup complete!"
echo "Your OpenClaw Gateway is now available at: https://$DOMAIN"
echo "SSL certificate will automatically renew."