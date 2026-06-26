# Network & Cloud Infrastructure

## Networking Fundamentals

### DNS
- Domain → IP resolution
- Record types: A, AAAA, CNAME, MX, TXT, NS, SOA, PTR
- TTL (Time to Live) caching
- DNS propagation delays
```bash
dig example.com A
dig example.com MX
dig example.com TXT
nslookup example.com
host example.com
```

### SSH
- Key-based auth: `ssh-keygen` → `ssh-copy-id`
- Config: `~/.ssh/config` for aliases
- Tunneling: `ssh -L local:remote user@host`
- Agent forwarding: `ssh-add`, `ssh -A`
- File transfer: `scp`, `rsync`, `sftp`

### Networking Commands
```bash
ip addr / ifconfig        # Interface info
ss -tlnp / netstat -tlnp  # Listening ports
ping host                  # Connectivity
traceroute host            # Route path
mtr host                  # Continuous traceroute
curl -v url               # HTTP debug
wget url                  # Download
nc -zv host port          # Port check
```

### VPN & Tunnels
- WireGuard: modern, fast VPN
- OpenVPN: traditional, widely supported
- SSH tunnels: simple port forwarding
- Tailscale/ZeroTier: mesh VPN

## Cloud Platforms

### AWS Essentials
```bash
aws s3 ls                          # List buckets
aws s3 cp file s3://bucket/        # Upload
aws ec2 describe-instances         # List instances
aws lambda list-functions          # List functions
```

### Azure Essentials
```bash
az login                          # Authenticate
az vm list                        # List VMs
az storage account list           # Storage accounts
az webapp list                    # Web apps
```

### GCP Essentials
```bash
gcloud auth login                 # Authenticate
gcloud compute instances list     # List VMs
gcloud storage ls                 # List storage
gcloud run services list          # Cloud Run
```

### Cloud Cost Optimization
- Right-size instances (monitor utilization)
- Use spot/preemptible for non-critical
- Reserved instances for steady workloads
- Auto-scaling for variable load
- Clean up unused resources regularly

## Monitoring & Observability
- Metrics: CPU, memory, disk, network, latency
- Logs: centralized, structured, searchable
- Alerts: thresholds, anomalies, error rates
- Dashboards: real-time status overview
- Tracing: request flow through services

## Container Orchestration
```bash
# Docker
docker ps / docker images
docker compose up -d / down
docker logs container_name

# Kubernetes
kubectl get pods / services / deployments
kubectl logs pod_name
kubectl exec -it pod_name -- /bin/sh
kubectl apply -f manifest.yaml
```

## Backup & Disaster Recovery
- 3-2-1 rule: 3 copies, 2 media types, 1 offsite
- Automated backups with verification
- RTO (Recovery Time Objective) and RPO (Recovery Point Objective)
- Test restores regularly (not just backups)
- Document recovery procedures
