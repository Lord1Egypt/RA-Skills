#!/bin/bash
# NAS Dashboard - Data Collector
# Generates structured KEY=VALUE data for the agent to format.
#
# === CONFIGURATION ===
# Override any of these before running, or edit defaults below.

# ZFS pool name(s). Auto-detects first pool if empty.
ZPOOL="${ZPOOL:-}"

# Disks to check (sd* only). Auto-detects all /dev/sd? if empty.
DISK_LIST="${DISK_LIST:-}"

# Frigate camera name mapping (optional). Format: "id1:Name1,id2:Name2"
FRIGATE_CAM_MAP="${FRIGATE_CAM_MAP:-}"

# NUT UPS name. Default: ups@localhost
UPS_NAME="${UPS_NAME:-ups@localhost}"

# === SCRIPT ===

# Auto-detect ZFS pool
if [ -z "$ZPOOL" ]; then
    ZPOOL=$(zpool list -H -o name 2>/dev/null | head -1)
fi

# Auto-detect disks
if [ -z "$DISK_LIST" ]; then
    DISK_LIST=$(lsblk -ndo name 2>/dev/null | grep '^sd.$' | tr '\n' ' ')
fi

echo "=== SYSTEM ==="
echo "HOSTNAME=$(hostname)"
echo "OS=$(grep PRETTY_NAME /etc/os-release 2>/dev/null | cut -d'"' -f2 || sw_vers -productName 2>/dev/null || uname -s)"
echo "KERNEL=$(uname -r)"
echo "UPTIME=$(uptime -p 2>/dev/null | sed 's/^up //' || uptime | sed 's/.*up //; s/,.*//')"
echo "LOAD=$(uptime | awk -F'load average:|load averages:' '{print $2}' | xargs)"
echo "CPU_MODEL=$(grep 'model name' /proc/cpuinfo 2>/dev/null | head -1 | cut -d':' -f2 | xargs || sysctl -n machdep.cpu.brand_string 2>/dev/null)"
echo "CPU_CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null)"
# CPU usage (Linux)
if [ -f /proc/stat ]; then
    echo "CPU_USED=$(top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{printf "%.1f", 100 - $1}')%"
else
    echo "CPU_USED=N/A"
fi
# Memory (Linux /proc/meminfo)
if [ -f /proc/meminfo ]; then
    echo "MEM_TOTAL=$(LANG=C free -h 2>/dev/null | awk '/^Mem:/ {print $2}')"
    echo "MEM_USED=$(LANG=C free -h 2>/dev/null | awk '/^Mem:/ {print $3}')"
    echo "MEM_PCT=$(LANG=C free 2>/dev/null | awk '/^Mem:/ {printf "%.1f", $3/$2*100}')%"
    echo "SWAP_TOTAL=$(LANG=C free -h 2>/dev/null | awk '/^Swap:/ {print $2}')"
    echo "SWAP_USED=$(LANG=C free -h 2>/dev/null | awk '/^Swap:/ {print $3}')"
else
    echo "MEM_TOTAL=N/A"
    echo "MEM_USED=N/A"
    echo "MEM_PCT=N/A"
    echo "SWAP_TOTAL=N/A"
    echo "SWAP_USED=N/A"
fi
# CPU temp (Linux sensors, Mac powermetrics)
CPU_TEMP=$(sensors 2>/dev/null | grep -E 'Package|Core 0|Tctl|CPU' | head -3 | awk '{print $1, $2, $3}' | tr '\n' ' / ')
echo "CPU_TEMP=${CPU_TEMP:-N/A}"
echo "DISK_USAGE=$(df -h / 2>/dev/null | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}')"
# Motherboard / chipset temps
MOBO_TEMP=$(sensors 2>/dev/null | grep -E 'SYSTIN|CPUTIN|AUXTIN|PCH|temp1|temp2' | grep -v 'Core\|Package\|CPU' | head -4 | awk '{gsub(/\+/,""); print $1, $2, $3}' | tr '\n' ' / ')
echo "MOBO_TEMP=${MOBO_TEMP:-N/A}"

echo "=== ZFS ==="
if [ -n "$ZPOOL" ]; then
    # Pool basic info
    zpool list -H -o name,size,alloc,free,cap,health,fragmentation "$ZPOOL" 2>/dev/null | while read line; do
        echo "POOL=$line"
    done
    # Pool I/O (1s snap)
    zpool iostat "$ZPOOL" -H 1 1 2>/dev/null | tail -1 | while read pool cap_alloc cap_free rops wops rbytes wbytes; do
        echo "POOL_IO=read:${rbytes:-0} write:${wbytes:-0} ops:${rops:-0}r/${wops:-0}w"
    done
    # Snapshots
    echo "SNAPSHOT_COUNT=$(zfs list -t snapshot -o name "$ZPOOL" 2>/dev/null | tail -n +2 | wc -l)"
    echo "LATEST_SNAPSHOT=$(zfs list -t snapshot -o name,creation -s creation "$ZPOOL" 2>/dev/null | tail -1)"
    echo "SCRUB=$(zpool status "$ZPOOL" 2>/dev/null | grep 'scan:' | sed 's/  scan: //')"
    # Datasets
    zfs list -H -o name,used,avail,refer,mountpoint "$ZPOOL" 2>/dev/null | while read line; do
        echo "DS=$line"
    done
    # Snapshot space top consumers
    zfs list -t snapshot -o name,used -s used -r "$ZPOOL" 2>/dev/null | tail -5 | while read line; do
        echo "SNAPSHOT_TOP=$line"
    done
    # ZFS recent events
    zpool events "$ZPOOL" -H 2>/dev/null | tail -5 | while IFS=$'\t' read -r _ class _ _; do
        [ -n "$class" ] && echo "ZFS_EVENT=$class"
    done
    # VDEV disk mapping: disk→vdev role
    zpool status -P "$ZPOOL" 2>/dev/null | awk '
    /NAME/{in_config=1; next}
    /errors:/||/^$/||/^  (spares|logs|cache|special)/{in_config=0}
    in_config && $1 ~ /^\//{split($1,a,"/"); disk=a[length(a)]; role=$2; gsub(/^mirror-.*|^raidz.*|^draid.*|^spare.*|^special.*|^logs.*/,"",role); print "VDEV_"disk"="$2}
    ' 2>/dev/null
else
    echo "POOL=no-zfs-pool-found"
fi

# ARC stats
if [ -f /proc/spl/kstat/zfs/arcstats ]; then
    arc_size=$(awk '/^size/ {printf "%.0f", $3/1073741824}' /proc/spl/kstat/zfs/arcstats)
    arc_hit=$(awk '/^hits/ {h=$3} /^misses/ {m=$3} END {if(h+m>0) printf "%.1f", h/(h+m)*100; else print "?"}' /proc/spl/kstat/zfs/arcstats)
    arc_max=$(awk '/^c_max/ {printf "%.0f", $3/1073741824}' /proc/spl/kstat/zfs/arcstats)
    echo "ARC=size:${arc_size}GiB max:${arc_max}GiB hit:${arc_hit}%"
else
    echo "ARC=unavailable"
fi
# L2ARC stats
if [ -f /proc/spl/kstat/zfs/arcstats ]; then
    l2_size=$(awk '/^l2_size/ {printf "%.0f", $3/1073741824}' /proc/spl/kstat/zfs/arcstats)
    l2_hit=$(awk '/^l2_hits/ {h=$3} /^l2_misses/ {m=$3} END {if(h+m>0) printf "%.1f", h/(h+m)*100; else print "?"}' /proc/spl/kstat/zfs/arcstats)
    echo "L2ARC=size:${l2_size:-0}GiB hit:${l2_hit:-0}%"
else
    echo "L2ARC=unavailable"
fi

echo "=== DISKS ==="
for disk in $DISK_LIST; do
    model=$(lsblk -ndo model "/dev/$disk" 2>/dev/null | xargs)
    size=$(lsblk -ndo size "/dev/$disk" 2>/dev/null | xargs)
    serial=$(lsblk -ndo serial "/dev/$disk" 2>/dev/null | xargs)
    smartinfo=$(sudo -n smartctl -A "/dev/$disk" 2>/dev/null)
    if [ -n "$smartinfo" ]; then
        temp_raw=$(echo "$smartinfo" | grep -E '^\s*194\s+Temperature_Celsius' | head -1 | awk '{print $10}' | tr -d '()')
        hours=$(echo "$smartinfo" | grep -i 'Power_On_Hours' | head -1 | awk '{print $NF}')
        status=$(sudo -n smartctl -H "/dev/$disk" 2>/dev/null | grep -i 'SMART overall-health\|SMART Health Status' | cut -d':' -f2 | xargs)
        # Critical SMART attributes
        realloc=$(echo "$smartinfo" | grep -E '^\s*5\s+Reallocated_Sector' | awk '{print $NF}')
        pending=$(echo "$smartinfo" | grep -E '^\s*197\s+Current_Pending' | awk '{print $NF}')
        udma=$(echo "$smartinfo" | grep -E '^\s*199\s+UDMA_CRC' | awk '{print $NF}')
        echo "DISK_${disk}=model:${model:-?} size:${size:-?} serial:${serial:-?} temp:${temp_raw:-?}°C hours:${hours:-?} health:${status:-?} realloc:${realloc:-0} pending:${pending:-0} udma:${udma:-0}"
    else
        echo "DISK_${disk}=model:${model:-?} size:${size:-?} serial:${serial:-?} smart:no-access"
    fi
done

# ZFS vdev role lookup (fallback: use zpool status with short names)
if [ -n "$ZPOOL" ]; then
    zpool status "$ZPOOL" 2>/dev/null | awk -v pool="$ZPOOL" '
    /NAME/{in_config=1; next}
    /errors:/||/^$/||/^  (spares|logs|cache|special)/{in_config=0}
    in_config && NF>=2 && $2~/^(mirror|raidz|draid|special|logs|cache|spare)/ && $1!~/^\// {vdev=$2; gsub(/[0-9-].*/,"",vdev)}
    in_config && $1 ~ /^(sd|nvme|vd)/ {disk=$1; if(vdev!="") print "VDEV_DISK="disk"|"pool"-"vdev; else print "VDEV_DISK="disk"|"pool}
    ' 2>/dev/null
fi

# Per-disk I/O latency (via iostat JSON)
if command -v iostat &>/dev/null; then
    iostat -y -x -o JSON 2>/dev/null | python3 -c "
import json,sys
data=json.load(sys.stdin)
for d in data.get('sysstat',{}).get('hosts',[{}])[0].get('statistics',[{}])[0].get('disk',[]):
    name=d.get('disk_device','')
    if name.startswith('sd') and len(name)==3:
        ra=d.get('r_await',0) or 0
        wa=d.get('w_await',0) or 0
        ut=d.get('util',0) or 0
        rkb=float(d.get('rkB/s',0) or 0)
        wkb=float(d.get('wkB/s',0) or 0)
        print(f'DISKIO_{name}=r_await:{ra:.1f}ms w_await:{wa:.1f}ms util:{ut:.1f}% r:{rkb/1024:.1f}M w:{wkb/1024:.1f}M')
" 2>/dev/null
fi

echo "=== DOCKER ==="
docker ps --format '{{.Names}}|{{.Status}}' 2>/dev/null | while read line; do
    echo "CTR=$line"
done
echo "CTR_TOTAL=$(docker ps -q 2>/dev/null | wc -l) running"
docker version --format '{{.Server.Version}}' 2>/dev/null | while read ver; do
    echo "DOCKER_VER=$ver"
done
docker ps --format '{{.Names}}|{{.Image}}' 2>/dev/null | while read line; do
    echo "CTR_IMG=$line"
done
docker system df 2>/dev/null | while read line; do
    echo "DOCKER_DF=$line"
done

echo "=== FRIGATE ==="
frigate_stats=$(curl -s --max-time 5 http://localhost:5000/api/stats 2>/dev/null)
if [ -n "$frigate_stats" ]; then
    echo "$frigate_stats" | python3 -c "
import json,sys,os
try:
    d=json.load(sys.stdin)
    det=d.get('detection_fps',0)
    # Parse camera name mapping from env var or use raw IDs
    cam_map={}
    for pair in os.environ.get('FRIGATE_CAM_MAP','').split(','):
        if ':' in pair:
            k,v=pair.split(':',1)
            cam_map[k.strip()]=v.strip()
    for cam,cinfo in d.get('cameras',{}).items():
        fps=cinfo.get('camera_fps',0)
        pid=cinfo.get('process_fps',0)
        skipped=cinfo.get('skipped_fps',0)
        name=cam_map.get(cam,cam)
        print(f'FRIGATE_CAM={name}|fps:{fps}|proc:{pid}|skip:{skipped}')
    cpu_inf=d.get('detectors',{}).get('cpu1',{}).get('inference_speed',0)
    print(f'FRIGATE_DET=fps:{det}|infer_ms:{cpu_inf:.1f}')
    for disk,info in d.get('service',{}).get('storage',{}).items():
        used=info.get('used',0)/1024
        total=info.get('total',0)/1024
        pct=used/total*100 if total else 0
        print(f'FRIGATE_STORAGE={disk}|{used:.1f}G/{total:.1f}G|{pct:.0f}%')
except:
    print('FRIGATE_ERR=parse_failed')
" FRIGATE_CAM_MAP="$FRIGATE_CAM_MAP" 2>/dev/null
else
    echo "FRIGATE_STATUS=no-response"
fi

echo "=== GPU ==="
nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null | while read line; do
    echo "GPU=$line"
done
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null | while read line; do
    echo "GPU_PROC=$line"
done

echo "=== NETWORK ==="
ip -br addr show 2>/dev/null | grep -v '^lo' | grep -v 'veth' | grep -v 'br-' | grep -v 'docker' | while read line; do
    echo "IFACE=$line"
done
if [ -f /proc/net/dev ]; then
    rx_total=$(awk '/face/{next} /lo/{next} {rx+=$2; tx+=$10} END {printf "↓%.0fMB ↑%.0fMB", rx/1048576, tx/1048576}' /proc/net/dev)
    echo "TRAFFIC=${rx_total}"
else
    echo "TRAFFIC=unavailable"
fi

echo "=== PROCESSES ==="
ps aux --sort=-%cpu 2>/dev/null | head -6 | tail -5 | awk '{printf "%.1f%% %s\n", $3, $11}' | while read line; do
    echo "TOP_CPU=$line"
done
ps aux --sort=-%mem 2>/dev/null | head -6 | tail -5 | awk '{printf "%.1f%% %s\n", $4, $11}' | while read line; do
    echo "TOP_MEM=$line"
done

echo "=== SERVICES ==="
# Failed systemd services (Linux only)
systemctl list-units --state=failed --no-legend 2>/dev/null | head -10 | awk '{print $1}' | while read unit; do
    echo "SVC_FAILED=$unit"
done
# Key services
for svc in ssh smbd nmbd nfs-server; do
    state=$(systemctl is-active "$svc" 2>/dev/null)
    [ -n "$state" ] && echo "SVC_${svc}=${state}"
done
cockpit_state=$(systemctl is-active cockpit.socket 2>/dev/null)
[ -n "$cockpit_state" ] && echo "SVC_cockpit=${cockpit_state} (socket)"

echo "=== LOGS ==="
journalctl -p 3 --since "1 hour ago" --no-pager 2>/dev/null | grep -v 'sudo.*password is required' | tail -5 | sed 's/^/LOG_ERR=/' | while read line; do
    echo "$line"
done
dmesg -T 2>/dev/null | grep -i 'out of memory\|killed process' | tail -3 | while read line; do
    echo "OOM=$line"
done

echo "=== SHARES ==="
smb_status=$(smbstatus -b 2>/dev/null | grep -c '^[0-9]')
echo "SMB_CONNECTIONS=${smb_status}"
nfs_clients=$(ss -tn state established '( sport = 2049 )' 2>/dev/null | tail -n +2 | wc -l)
echo "NFS_CLIENTS=${nfs_clients}"

echo "=== SECURITY ==="
failed_logins=$(sudo -n grep 'Failed password' /var/log/auth.log 2>/dev/null | wc -l || echo "?")
echo "FAILED_LOGINS=${failed_logins}"
last_login=$(last -n 3 2>/dev/null | head -3 | tr '\n' '|')
echo "LAST_LOGINS=${last_login}"

# SSH config audit
sshd_cfg="/etc/ssh/sshd_config"
if [ -f "$sshd_cfg" ]; then
    ssh_port=$(sudo -n grep -E '^Port ' "$sshd_cfg" 2>/dev/null | awk '{print $2}' || echo "22")
    ssh_root=$(sudo -n grep -E '^PermitRootLogin ' "$sshd_cfg" 2>/dev/null | awk '{print $2}' || echo "?")
    ssh_pass=$(sudo -n grep -E '^PasswordAuthentication ' "$sshd_cfg" 2>/dev/null | awk '{print $2}' || echo "?")
    ssh_key=$(sudo -n grep -E '^PubkeyAuthentication ' "$sshd_cfg" 2>/dev/null | awk '{print $2}' || echo "?")
    echo "SSH_PORT=${ssh_port:-22}"
    echo "SSH_ROOT_LOGIN=${ssh_root:-?}"
    echo "SSH_PASS_AUTH=${ssh_pass:-?}"
    echo "SSH_KEY_AUTH=${ssh_key:-?}"
fi

# Firewall status
if command -v ufw &>/dev/null; then
    fw_status=$(sudo -n ufw status 2>/dev/null | head -1 | awk '{print $2}' || echo "inactive")
    fw_rules=$(sudo -n ufw status numbered 2>/dev/null | grep -E '^\[' | wc -l || echo 0)
    echo "FW_UFW=${fw_status}"
    echo "FW_RULES=${fw_rules}"
elif command -v iptables &>/dev/null; then
    fw_rules=$(sudo -n iptables -L INPUT -n 2>/dev/null | grep -cE '^(ACCEPT|DROP|REJECT)' || echo 0)
    echo "FW_TYPE=iptables"
    echo "FW_RULES=${fw_rules}"
else
    echo "FW_TYPE=none"
fi

# Open ports (listening, non-localhost)
listen_ports=$(ss -tlnp 2>/dev/null | grep -v '127.0.0.1\|\[::1\]' | awk 'NR>1 {print $4}' | awk -F: '{print $NF}' | sort -n | uniq | tr '\n' ',' | sed 's/,$//')
echo "OPEN_PORTS=${listen_ports:-none}"

# fail2ban
if command -v fail2ban-client &>/dev/null; then
    f2b_active=$(sudo -n fail2ban-client status 2>/dev/null | grep -c 'Jail list' || echo 0)
    echo "F2B_ACTIVE=${f2b_active}"
fi

echo "=== CONTAINER_AGE ==="
# Image age checks for stale containers
docker images --format '{{.Repository}}:{{.Tag}}|{{.CreatedSince}}' 2>/dev/null | while IFS='|' read img age; do
    echo "IMG_AGE=${img}|${age}"
done

echo "=== UPDATES ==="
apt_updates=$(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)
echo "APT_UPDATES=${apt_updates}"

echo "=== BOOT ==="
echo "BOOT_TIME=$(uptime -s 2>/dev/null || who -b 2>/dev/null | awk '{print $3, $4}')"
echo "BOOT_DAYS=$(( ($(date +%s) - $(date -d "$(uptime -s 2>/dev/null || date -r $(sysctl -n kern.boottime 2>/dev/null | awk '{print $4}' | tr -d ',') '+%Y-%m-%d %H:%M:%S')" +%s 2>/dev/null || echo 0)) / 86400 )) days"

echo "=== UPS ==="
upsc "$UPS_NAME" 2>/dev/null | while IFS=':' read -r key val; do
    key=$(echo "$key" | xargs)
    val=$(echo "$val" | xargs)
    case "$key" in
        battery.charge|ups.status|ups.load|input.voltage|battery.voltage|driver.name|ups.type)
            echo "UPS_${key}=${val}"
            ;;
    esac
done

echo "=== TIMESHIFT ==="
# Try multiple detection paths for timeshift snapshots
TS_COUNT=0
TS_LAST=""
# Method 1: grub-btrfs style (snapshots under /run/timeshift or /timeshift-btrfs)
for ts_path in /run/timeshift /timeshift-btrfs /mnt/timeshift /timeshift; do
    if [ -d "$ts_path" ]; then
        ts_snaps=$(ls -1 "$ts_path"/snapshots* 2>/dev/null | wc -l)
        if [ "$ts_snaps" -gt 0 ] 2>/dev/null; then
            TS_COUNT=$ts_snaps
            TS_LAST=$(ls -1t "$ts_path"/snapshots* 2>/dev/null | head -1 | xargs basename)
            break
        fi
    fi
done
# Method 2: try timeshift --list directly (works if sudo is configured)
if [ "$TS_COUNT" -eq 0 ] 2>/dev/null; then
    ts_list=$(sudo -n timeshift --list 2>/dev/null)
    if [ -n "$ts_list" ]; then
        TS_COUNT=$(echo "$ts_list" | grep -Ec '^[0-9]+[[:space:]]+>' 2>/dev/null || echo 0)
        TS_LAST=$(echo "$ts_list" | grep -E '^[0-9]+[[:space:]]+>' | tail -1 | awk '{print $3}' 2>/dev/null)
    fi
fi
# Method 3: count btrfs subvolumes matching timeshift pattern
if [ "$TS_COUNT" -eq 0 ] 2>/dev/null && command -v btrfs &>/dev/null; then
    TS_COUNT=$(btrfs subvolume list / 2>/dev/null | grep -ci timeshift || echo 0)
fi

if [ -f /etc/cron.d/timeshift-hourly ] || systemctl is-active timeshift.timer &>/dev/null || [ "$TS_COUNT" -gt 0 ] 2>/dev/null; then
    echo "TIMESHIFT_LAST=${TS_LAST:-unknown}"
    echo "TIMESHIFT_COUNT=${TS_COUNT:-0}"
    echo "TIMESHIFT_CRON=active"
else
    echo "TIMESHIFT_CRON=not-found"
fi

echo "=== END ==="
