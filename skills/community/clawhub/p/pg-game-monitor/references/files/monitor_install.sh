#!/bin/bash
# Prometheus + Grafana Monitoring Stack Installer
# Supports: Prometheus 3.x, Alertmanager, Pushgateway, Grafana 10.x
# Required: CentOS 7+, root, internet access
# Usage: bash monitor_install.sh
set -e

# ================= Env Config (modify before running) =================
# FEISHU_WEBHOOK_URL  Feishu bot webhook URL (required)
# GRAFANA_PORT        Grafana listen port (default: 3000)
# PUSH_INTERVAL       Agent push interval in seconds (default: 60)
# DATA_RETENTION      Prometheus retention days (default: 60d)
# ADMIN_PASSWORD      Grafana admin password (change after install)

FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-}"
GRAFANA_PORT="${GRAFANA_PORT:-3000}"
PUSH_INTERVAL="${PUSH_INTERVAL:-60}"
DATA_RETENTION="${DATA_RETENTION:-60d}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}"

# ================= Paths =================
BASE_DIR="${BASE_DIR:-/opt/monitor}"
DATA_DIR="${DATA_DIR:-/data/monitor}"
mkdir -p $BASE_DIR/{prometheus,alertmanager,pushgateway,feishu}
mkdir -p $DATA_DIR/{prometheus,alertmanager}

# ================= Versions =================
PROMETHEUS_VER="3.5.1"
ALERTMANAGER_VER="0.29.0"
PUSHGATEWAY_VER="1.5.1"
GRAFANA_RPM_URL="https://dl.grafana.com/enterprise/release/grafana-enterprise-10.4.19-1.x86_64.rpm"

echo "== Downloading components =="
cd /tmp

wget -c "https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VER}/prometheus-${PROMETHEUS_VER}.linux-amd64.tar.gz"
wget -c "https://github.com/prometheus/alertmanager/releases/download/v${ALERTMANAGER_VER}/alertmanager-${ALERTMANAGER_VER}.linux-amd64.tar.gz"
wget -c "https://github.com/prometheus/pushgateway/releases/download/v${PUSHGATEWAY_VER}/pushgateway-${PUSHGATEWAY_VER}.linux-amd64.tar.gz"
wget -c "$GRAFANA_RPM_URL"

echo "== Extracting =="
tar -xf prometheus-*.tar.gz
mv prometheus-${PROMETHEUS_VER}.linux-amd64/* $BASE_DIR/prometheus/

tar -xf alertmanager-*.tar.gz
mv alertmanager-${ALERTMANAGER_VER}.linux-amd64/* $BASE_DIR/alertmanager/

tar -xf pushgateway-*.tar.gz
mv pushgateway-${PUSHGATEWAY_VER}.linux-amd64/* $BASE_DIR/pushgateway/

echo "== Installing Grafana =="
yum install -y grafana-enterprise-*.rpm
pip install -q flask requests==2.27.1

# ================= Prometheus Rules =================
cat > $BASE_DIR/prometheus/rules.yml <<'EOF'
groups:

- name: jvm_alerts
  rules:

  - alert: JVMHeapUsageHigh
    expr: (heap_used_bytes / clamp_min(heap_committed_bytes, 1)) > 0.85
      and (time() - jvm_start_time_seconds > 3600)
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "JVM heap usage high"
      description: "{{ $labels.hostname }} {{ $labels.game_dir }} heap usage is {{ $value | humanizePercentage }}"
      value: "{{ $value }}"

  - alert: JVMGcPressureWarning
    expr: gc_time_seconds / 60 > 0.3
    for: 3m
    labels:
      severity: warning
    annotations:
      summary: "JVM GC pressure high"
      description: "{{ $labels.hostname }} {{ $labels.game_dir }} GC is consuming {{ $value | humanizePercentage }} of CPU time"
      value: "{{ $value }}"

  - alert: JVMGcPressureCritical
    expr: gc_time_seconds / 60 > 0.6
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "JVM GC critical"
      description: "{{ $labels.hostname }} {{ $labels.game_dir }} GC is consuming {{ $value | humanizePercentage }} of CPU time"
      value: "{{ $value }}"

- name: mysql_alerts
  rules:

  - alert: MySQLDown
    expr: mysql_up == 0
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "MySQL down"
      description: "{{ $labels.hostname }} MySQL is not reachable"
      value: "{{ $value }}"

  - alert: MySQLBufferPoolHigh
    expr: (innodb_buffer_pool_bytes_data / clamp_min(innodb_buffer_pool_bytes_total, 1)) > 0.85
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "MySQL buffer pool high"
      description: "{{ $labels.hostname }} InnoDB buffer pool usage is {{ $value | humanizePercentage }}"
      value: "{{ $value }}"

  - alert: MySQLMemoryHigh
    expr: mysql_process_resident_memory_bytes > 8589934592
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "MySQL memory high"
      description: "{{ $labels.hostname }} MySQL RSS is above 8GB"
      value: "{{ $value | humanize1024 }}B"
EOF

# ================= Prometheus Config =================
cat > $BASE_DIR/prometheus/prometheus.yml <<EOF
global:
  scrape_interval: ${PUSH_INTERVAL}s

rule_files:
  - "rules.yml"

scrape_configs:
  - job_name: 'pushgateway'
    honor_labels: true
    static_configs:
      - targets: ['127.0.0.1:9091']

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['127.0.0.1:9093']
EOF

# ================= Alertmanager Config =================
cat > $BASE_DIR/alertmanager/alertmanager.yml <<'EOF'
route:
  group_by: ['alertname']
  group_wait: 30s
  group_interval: 30m
  repeat_interval: 120m
  receiver: 'feishu_default'

  routes:
    - match:
        severity: critical
      receiver: feishu_critical
    - match:
        severity: warning
      receiver: feishu_warning

receivers:
- name: feishu_critical
  webhook_configs:
  - url: 'http://127.0.0.1:5000/webhook?level=critical'

- name: feishu_warning
  webhook_configs:
  - url: 'http://127.0.0.1:5000/webhook?level=warning'

- name: feishu_default
  webhook_configs:
  - url: 'http://127.0.0.1:5000/webhook'
EOF

# ================= Feishu Webhook Service =================
cat > $BASE_DIR/feishu/webhook.env <<EOF
FEISHU_WEBHOOK_URL=${FEISHU_WEBHOOK_URL}
WEBHOOK_PORT=5000
PUSH_INTERVAL=${PUSH_INTERVAL}
EOF

cat > $BASE_DIR/feishu/webhook.py <<'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alert webhook receiver.
Receives from Alertmanager, forwards to Feishu/Lark.
Configure via /opt/monitor/feishu/webhook.env
"""

import os
import re
import sys
from flask import Flask, request
import requests

app = Flask(__name__)

FEISHU_WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK_URL", "")
WEBHOOK_PORT = int(os.environ.get("WEBHOOK_PORT", "5000"))
PUSH_INTERVAL = int(os.environ.get("PUSH_INTERVAL", "60"))


def extract_ip(hostname):
    try:
        m = re.search(r'(\d+\.\d+\.\d+\.\d+)', hostname)
        return m.group(1) if m else "unknown"
    except Exception:
        return "unknown"


def format_value(alertname, value):
    try:
        if alertname in ["JVMProcessDown", "MySQLDown"]:
            return str(value)
        v = float(value)
        if alertname in ["JVMHeapUsageHigh", "JVMOldGenHigh",
                          "JVMHeapUsageHighWarmup", "MySQLBufferPoolHigh"]:
            return f"{v * 100:.2f}%"
        if "Gc" in alertname:
            return f"{v:.2f}s ({v / PUSH_INTERVAL * 100:.1f}% of cycle)"
        if alertname == "MySQLMemoryHigh":
            return f"{v / 1024**3:.2f} GB"
        return str(v)
    except Exception:
        return str(value)


@app.route('/webhook', methods=['POST'])
def webhook():
    if not FEISHU_WEBHOOK_URL:
        return "FEISHU_WEBHOOK_URL not configured", 500

    data = request.json or {}
    level = request.args.get("level", "info")

    title = "告警通知"
    if level == "critical":
        title = "严重告警"
    elif level == "warning":
        title = "警告告警"

    text = ""
    for a in data.get("alerts", []):
        labels = a.get("labels", {})
        annotations = a.get("annotations", {})
        alertname = labels.get("alertname", "unknown")
        hostname = labels.get("hostname", "unknown")
        game_dir = labels.get("game_dir", "")
        value = annotations.get("value", "0")
        summary = annotations.get("summary", "")
        desc = annotations.get("description", "")
        ip = extract_ip(hostname)

        text += f"""### {summary}
- 主机: {hostname}
- IP: {ip}
{"- 服务: " + game_dir if game_dir else ""}
- 当前值: {format_value(alertname, value)}
- 描述: {desc}

"""

    msg = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": title}},
            "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": text}}]
        }
    }

    requests.post(FEISHU_WEBHOOK_URL, json=msg)
    return "ok"


if __name__ == "__main__":
    if not FEISHU_WEBHOOK_URL:
        print("ERROR: FEISHU_WEBHOOK_URL environment variable is not set", file=sys.stderr)
        sys.exit(1)
    # Bind to 127.0.0.1 — Alertmanager calls via localhost only
    app.run(host="127.0.0.1", port=WEBHOOK_PORT)
EOF

# ================= Systemd Units =================
cat > /etc/systemd/system/feishu.service <<'EOF'
[Unit]
Description=Feishu Alert Webhook
After=network.target

[Service]
EnvironmentFile=/opt/monitor/feishu/webhook.env
ExecStart=/usr/bin/python3 /opt/monitor/feishu/webhook.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/systemd/system/prometheus.service <<EOF
[Service]
ExecStart=$BASE_DIR/prometheus/prometheus \
  --config.file=$BASE_DIR/prometheus/prometheus.yml \
  --storage.tsdb.path=$DATA_DIR/prometheus \
  --storage.tsdb.retention.time=${DATA_RETENTION}
Restart=always
EOF

cat > /etc/systemd/system/alertmanager.service <<'EOF'
[Service]
ExecStart=/opt/monitor/alertmanager/alertmanager \
  --config.file=/opt/monitor/alertmanager/alertmanager.yml
Restart=always
EOF

cat > /etc/systemd/system/pushgateway.service <<'EOF'
[Service]
ExecStart=/opt/monitor/pushgateway/pushgateway
Restart=always
EOF

# ================= Start Services =================
systemctl daemon-reload
systemctl enable prometheus alertmanager pushgateway grafana-server feishu
systemctl start prometheus alertmanager pushgateway grafana-server feishu

echo ""
echo "=== Installation complete ==="
echo ""
if [ -z "$FEISHU_WEBHOOK_URL" ]; then
    echo "WARNING: FEISHU_WEBHOOK_URL not set. Edit /opt/monitor/feishu/webhook.env and run:"
    echo "  systemctl restart feishu"
else
    echo "Feishu webhook configured."
fi
echo ""
echo "Services:"
systemctl status prometheus alertmanager pushgateway grafana-server feishu --no-pager
echo ""
echo "Default ports: Prometheus=9090 Pushgateway=9091 Alertmanager=9093 Grafana=${GRAFANA_PORT}"
echo "Grafana default credentials: admin / ${ADMIN_PASSWORD}"
echo "Change admin password after first login!"
