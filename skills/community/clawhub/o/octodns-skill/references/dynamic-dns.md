# Dynamic DNS Updates with octoDNS

Automate DNS record updates from scripts, services, or CI/CD pipelines.

## Overview

octoDNS can be used for dynamic DNS updates by:
1. Updating YAML zone files programmatically
2. Running octoDNS sync to apply changes
3. Automating via cron, webhooks, or CI/CD

## Use Cases

- **IP address updates**: Update A/AAAA records when IP changes
- **Service discovery**: Register/deregister service endpoints
- **Infrastructure changes**: Update DNS when servers spin up/down
- **Auto-scaling**: Add/remove records as instances scale

## Basic Pattern

### 1. Update Zone File

```bash
#!/bin/bash
# update-home-ip.sh

ZONE_FILE="config/example.com.yaml"
NEW_IP=$(curl -s https://api.ipify.org)

# Update the home record
yq eval ".home.value = \"$NEW_IP\"" -i "$ZONE_FILE"
```

### 2. Sync Changes

```bash
# Preview
scripts/sync.sh --zone example.com --noop

# Apply
scripts/sync.sh --zone example.com --doit
```

### 3. Automate

```cron
# Update every 15 minutes
*/15 * * * * /path/to/update-home-ip.sh && /path/to/sync.sh --doit
```

## Advanced Patterns

### Python Script for Updates

```python
#!/usr/bin/env python3
# update_dns.py

import yaml
import sys

def update_record(zone_file, name, record_type, value):
    with open(zone_file, 'r') as f:
        zone = yaml.safe_load(f)
    
    # Update or create record
    if name not in zone:
        zone[name] = {}
    
    zone[name]['type'] = record_type
    zone[name]['value'] = value
    zone[name]['ttl'] = 300
    
    with open(zone_file, 'w') as f:
        yaml.dump(zone, f, default_flow_style=False)

if __name__ == '__main__':
    update_record(
        'config/example.com.yaml',
        'dynamic',
        'A',
        '192.0.2.100'
    )
```

Usage:

```bash
python3 update_dns.py
scripts/sync.sh --zone example.com --doit
```

### Service Registration

Register a service when it starts:

```bash
#!/bin/bash
# on-service-start.sh

SERVICE_IP=$(hostname -I | awk '{print $1}')
SERVICE_NAME="api-${HOSTNAME}"

# Add service record
python3 << EOF
import yaml

zone_file = 'config/services.example.com.yaml'

with open(zone_file, 'r') as f:
    zone = yaml.safe_load(f) or {}

zone['$SERVICE_NAME'] = {
    'type': 'A',
    'value': '$SERVICE_IP',
    'ttl': 60
}

with open(zone_file, 'w') as f:
    yaml.dump(zone, f, default_flow_style=False)
EOF

# Sync immediately
scripts/sync.sh --zone services.example.com --doit
```

Deregister on shutdown:

```bash
#!/bin/bash
# on-service-stop.sh

SERVICE_NAME="api-${HOSTNAME}"

python3 << EOF
import yaml

zone_file = 'config/services.example.com.yaml'

with open(zone_file, 'r') as f:
    zone = yaml.safe_load(f)

if '$SERVICE_NAME' in zone:
    del zone['$SERVICE_NAME']

with open(zone_file, 'w') as f:
    yaml.dump(zone, f, default_flow_style=False)
EOF

scripts/sync.sh --zone services.example.com --doit
```

### Webhook-Triggered Updates

```python
#!/usr/bin/env python3
# webhook_server.py

from flask import Flask, request
import subprocess
import yaml

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update_dns():
    data = request.json
    
    # Update zone file
    zone_file = f"config/{data['zone']}.yaml"
    
    with open(zone_file, 'r') as f:
        zone = yaml.safe_load(f)
    
    zone[data['name']] = {
        'type': data['type'],
        'value': data['value'],
        'ttl': data.get('ttl', 300)
    }
    
    with open(zone_file, 'w') as f:
        yaml.dump(zone, f)
    
    # Sync
    result = subprocess.run([
        'scripts/sync.sh',
        '--zone', data['zone'],
        '--doit'
    ], capture_output=True, text=True)
    
    return {
        'success': result.returncode == 0,
        'output': result.stdout
    }

if __name__ == '__main__':
    app.run(port=5000)
```

Trigger updates:

```bash
curl -X POST http://localhost:5000/update \
  -H "Content-Type: application/json" \
  -d '{
    "zone": "example.com",
    "name": "dynamic",
    "type": "A",
    "value": "192.0.2.50",
    "ttl": 60
  }'
```

### CI/CD Integration

GitHub Actions example:

```yaml
# .github/workflows/dns-update.yml
name: Update DNS

on:
  push:
    paths:
      - 'dns/config/**'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install octoDNS
        run: |
          pip install octodns octodns-easydns
      
      - name: Sync DNS
        env:
          EASYDNS_TOKEN: ${{ secrets.EASYDNS_TOKEN }}
          EASYDNS_API_KEY: ${{ secrets.EASYDNS_API_KEY }}
          EASYDNS_PORTFOLIO: ${{ secrets.EASYDNS_PORTFOLIO }}
        run: |
          octodns-sync --config-file=dns/config/production.yaml --doit
```

## Best Practices

### 1. Use Short TTLs for Dynamic Records

```yaml
dynamic-host:
  ttl: 60  # 1 minute for frequently changing records
  type: A
  value: 192.0.2.1
```

### 2. Separate Dynamic Zones

Keep dynamic records in separate zone files:

```
config/
  static.example.com.yaml  # Rarely changes
  dynamic.example.com.yaml # Frequently updated
```

### 3. Lock Files

Prevent concurrent updates:

```bash
#!/bin/bash
LOCKFILE="/tmp/dns-update.lock"

exec 200>$LOCKFILE
flock -n 200 || exit 1

# Update and sync
update_zone_file
scripts/sync.sh --doit

flock -u 200
```

### 4. Error Handling

```bash
#!/bin/bash
if scripts/sync.sh --zone example.com --doit; then
    echo "DNS updated successfully"
else
    echo "DNS update failed!" | mail -s "DNS Alert" admin@example.com
    exit 1
fi
```

### 5. Atomic Updates

```bash
# Update temporary file first
update_zone_file config/example.com.yaml.tmp

# Validate
if scripts/validate.sh config/example.com.yaml.tmp; then
    mv config/example.com.yaml.tmp config/example.com.yaml
    scripts/sync.sh --zone example.com --doit
else
    echo "Validation failed"
    rm config/example.com.yaml.tmp
    exit 1
fi
```

## Monitoring

Track DNS update metrics:

```bash
#!/bin/bash
# monitor-dns-sync.sh

LOG="/var/log/dns-sync.log"

sync_output=$(scripts/sync.sh --zone example.com --doit 2>&1)
exit_code=$?

echo "[$(date)] Exit: $exit_code" >> "$LOG"

if [ $exit_code -ne 0 ]; then
    echo "DNS sync failed:" >> "$LOG"
    echo "$sync_output" >> "$LOG"
    # Alert
    curl -X POST https://monitoring.example.com/alert \
      -d "DNS sync failed for example.com"
fi
```

## Limitations

1. **Sync delay**: octoDNS sync takes a few seconds
2. **Rate limits**: DNS provider API rate limits may apply
3. **Not real-time**: For true dynamic DNS, consider provider-specific APIs
4. **Conflicts**: Concurrent updates may conflict without locking

## When NOT to Use This

- **Real-time requirements**: Use provider API directly
- **Very high frequency**: >1 update/minute
- **Large-scale service discovery**: Use Consul, etcd, or similar
- **DDoS mitigation**: Use CDN dynamic routing

## Alternatives

- **Direct provider API**: Faster but provider-specific
- **dns-update tools**: ddclient, nsupdate for simple DDNS
- **Service discovery**: Consul, CoreDNS with plugins
- **Load balancers**: Cloud provider DNS features
