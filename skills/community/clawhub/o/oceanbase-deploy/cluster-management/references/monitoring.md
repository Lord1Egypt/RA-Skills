# Monitoring Setup (Prometheus & Grafana)

Add GUI-based monitoring to an OceanBase cluster using OBAgent, Prometheus, and Grafana.

## Scenario 1: OBAgent NOT Deployed

Add `obagent`, `prometheus`, and `grafana` to the cluster config file and redeploy/start.

```yaml
obagent:
  servers:
    - <server_ip>
  global:
    home_path: /home/admin/obagent

prometheus:
  servers:
    - <server_ip>
  global:
    home_path: /home/admin/prometheus

grafana:
  servers:
    - <server_ip>
  global:
    home_path: /home/admin/grafana
```

## Scenario 2: OBAgent Already Deployed

Add only `prometheus` and `grafana` to the config. Manually configure Prometheus to scrape OBAgent endpoints.

## Authentication

OBD enables HTTP basic auth for Prometheus. The generated credentials (admin + random password) are displayed in:

```bash
obd cluster display <deploy_name>
```

Use these credentials when accessing:
- Prometheus web UI: `http://<host>:9090`
- API: `curl -u admin:<password> http://<host>:9090/-/ready`

## Component Deletion Order

Components with dependants must be deleted **after** their dependants:

1. Delete `grafana` and `prometheus` first:
   ```bash
   obd cluster component del <name> grafana prometheus
   ```
2. Then delete `obagent`:
   ```bash
   obd cluster component del <name> obagent
   ```

Reversing this order causes a "still depends" error.
