# PBS Backup — Setup Guide

Reference for agents guiding PBS setup. Use conversationally — ask one block at a time.

## Install PBS

### As LXC (recommended for homelabs)

On the Proxmox host:
```bash
# Download template if not present
pveam update
# Use `pveam available --section system` to find the latest Debian template
pveam download local <latest-debian-template.tar.zst>

# Create container — replace <VMID>, <SIZE>, <IP> with user's answers
pct create <VMID> local:vztmpl/<latest-debian-template.tar.zst> \
  --hostname pbs \
  --memory 4096 \
  --cores 2 \
  --rootfs local-lvm:<SIZE> \
  --net0 name=eth0,bridge=vmbr0,ip=<IP>/24,gw=<GATEWAY> \
  --start 1

# If DHCP instead of static:
#  --net0 name=eth0,bridge=vmbr0,ip=dhcp
```

Inside the container:
```bash
# Add PBS free repository (no subscription needed)
echo "deb http://download.proxmox.com/debian/pbs bookworm pbs-no-subscription" \
  > /etc/apt/sources.list.d/pbs-no-subscription.list
wget -qO /etc/apt/trusted.gpg.d/proxmox-release-bookworm.gpg \
  https://enterprise.proxmox.com/debian/proxmox-release-bookworm.gpg
apt update && apt install -y proxmox-backup-server
```

Optional SSH:
```bash
apt install -y openssh-server
passwd root  # or create a dedicated user
```

Verify:
```bash
curl -sk https://localhost:8007/api2/json/version
```

PBS Web UI: `https://<pbs-ip>:8007` (login: `root@pam`)

### As VM

Download PBS ISO from https://www.proxmox.com/en/downloads → install via Proxmox "Create VM".

## Storage Setup

### Local datastore

Inside PBS:
```bash
mkdir -p /backup
proxmox-backup-manager datastore create <NAME> /backup
```

### NAS datastore (NFS)

Inside PBS:
```bash
# Mount NFS share
apt install -y nfs-common
mkdir -p /mnt/nas-backup
echo "<NAS_IP>:<EXPORT_PATH> /mnt/nas-backup nfs defaults,_netdev 0 0" >> /etc/fstab
mount -a

# Verify mount
df -h /mnt/nas-backup

# Create datastore on NAS mount
proxmox-backup-manager datastore create <NAME> /mnt/nas-backup
```

For SMB/CIFS:
```bash
apt install -y cifs-utils
mkdir -p /mnt/nas-backup

# Create /root/.smbcreds with:
# username=<smb_user>
# password=<smb_password>
chmod 600 /root/.smbcreds

echo "//<NAS_IP>/<SHARE> /mnt/nas-backup cifs credentials=/root/.smbcreds,_netdev 0 0" >> /etc/fstab
mount -a
```

## Proxmox Host — API Token

1. Proxmox WebUI → **Datacenter → Permissions → API Tokens → Add**
2. User: `root@pam` (recommended: create a dedicated `backup@pve` user first)
3. Token ID: e.g. `backup-token`
4. **Privilege Separation**: Keep this checked for better security.
5. **Permissions**: Assign the `backup` user a role with these privileges:
   - `VM.Backup`
   - `Datastore.AllocateSpace`
   - `Datastore.Audit`
6. Copy the token secret (shown only once)

Test from agent:
```python
from proxmoxer import ProxmoxAPI
prox = ProxmoxAPI("<IP>", user="backup@pve",
    token_name="backup-token", token_value="<SECRET>", verify_ssl=False)
print(prox.nodes.get())
```

If `proxmoxer` is missing: `pip install proxmoxer`

## Add PBS Storage to Proxmox

WebUI: **Datacenter → Storage → Add → Proxmox Backup Server**
- ID: choose a name (e.g. `my-pbs`)
- Server: PBS IP
- Datastore: name from PBS
- Username: `root@pam`
- Password: PBS root password
- Content: "VZDump backup file"

Or CLI on Proxmox host:
```bash
pvesm add pbs <STORAGE_NAME> \
  --server <PBS_IP> \
  --datastore <DATASTORE> \
  --username root@pam \
  --password <PASSWORD> \
  --content backup

pvesm status | grep <STORAGE_NAME>  # verify
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `proxmoxer` missing | `pip install proxmoxer` |
| 401 Unauthorized | Token invalid or privilege separation enabled |
| Storage not found | Add PBS as storage in Proxmox (see above) |
| `pct snapshot` fails | Expected with bind mounts — vzdump snapshot works fine |
| Backup timeout | Check PBS reachability, disk space |
| ENOSPC | PBS datastore full — run garbage collection or expand |
