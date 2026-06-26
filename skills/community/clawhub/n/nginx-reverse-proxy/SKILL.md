---
name: nginx-reverse-proxy
description: Configure nginx reverse proxy for domain binding. Trigger when user says "绑定域名" or "配置nginx" or "反向代理" to bind a domain to a specific IP:port.
---

# Nginx 反向代理配置

When user requests to bind a domain to IP:port (e.g., "绑定域名 claw.nul.qzz.io 到 127.0.0.1:18789"), create nginx config:

1. Extract domain (e.g., `claw.nul.qzz.io`) and target (e.g., `127.0.0.1:18789`)
2. Generate nginx config file at `/etc/nginx/conf.d/{domain}.conf`:

```nginx
server {
    listen 443 ssl;
    server_name {domain};

    ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://{target};
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. If HTTP (not HTTPS) needed:
```nginx
server {{
    listen 80;
    server_name {domain};
    location / {{
        proxy_pass http://{target};
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
}}
```

4. Execute:
```bash
sudo tee /etc/nginx/conf.d/{domain}.conf > /dev/null <<'EOF'
<config>
EOF
sudo nginx -t && sudo systemctl reload nginx
```

5. If SSL needed, also run:
```bash
sudo certbot --nginx -d {domain}
```

6. Report success with domain and target info.