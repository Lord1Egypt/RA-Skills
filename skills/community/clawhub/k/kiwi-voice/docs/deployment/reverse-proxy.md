# Reverse Proxy

Expose Kiwi Voice behind a reverse proxy with HTTPS. This is required for the [Web Microphone](../features/web-microphone.md) to work on non-localhost origins (AudioWorklet requires a secure context).

## nginx

```nginx
server {
    listen 443 ssl;
    server_name kiwi.example.com;

    ssl_certificate /etc/letsencrypt/live/kiwi.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kiwi.example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:7789;
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

!!! important "WebSocket support"
    The `Upgrade` and `Connection` headers are required for WebSocket connections (event stream and web audio).

## Caddy

```
kiwi.example.com {
    reverse_proxy localhost:7789
}
```

Caddy handles SSL automatically via Let's Encrypt.

## SSL with Let's Encrypt

```bash
sudo certbot --nginx -d kiwi.example.com
```

Or with Caddy — automatic, no extra steps needed.
