# Commands — The Incident Toolkit

Not a tutorial. These are the invocations that answer a question in one line during an incident, grouped by what you are trying to learn. Prefix with sudo according to `privilege_mode`.

## First Sixty Seconds On An Unknown Host

```bash
uptime; nproc                       # load in context of core count
free -h                             # read `available`, not `free`
df -hT | grep -vE 'tmpfs|squashfs'  # which filesystem is full
systemctl --failed                  # what is broken right now
journalctl -b -p err --no-pager | tail -50
ss -tlnp                            # what is listening and who owns it
dmesg -T | tail -30                 # OOM, I/O errors, resets
```

## What Is Consuming The Machine

```bash
ps -eo pid,ppid,user,pcpu,pmem,rss,etime,stat,args --sort=-pcpu | head -15
ps -eo pid,rss,args --sort=-rss | head -15         # top memory by RSS
grep Pss /proc/<pid>/smaps_rollup                  # honest shared-memory accounting
pidstat -u -d 1 3                                  # CPU and disk per process
systemd-cgtop -m                                   # per-service memory and CPU
iostat -xz 1 3                                     # per-device await and queue depth
```

## Disk

```bash
du -xh --max-depth=1 /var 2>/dev/null | sort -h | tail
find / -xdev -type f -size +500M -printf '%s\t%p\n' 2>/dev/null | sort -n | tail
lsof +L1                                   # deleted files still held open
df -i                                       # inode exhaustion
journalctl --disk-usage && journalctl --vacuum-size=500M
lsblk -f                                    # devices, UUIDs, mount points
```

## Processes

```bash
pgrep -af <pattern>                         # ALWAYS before pkill -f
ps -o pid,stat,wchan:20,etime,args -p <pid> # state and what it waits on
ls -l /proc/<pid>/{cwd,exe} ; ls /proc/<pid>/fd | wc -l
tr '\0' '\n' < /proc/<pid>/environ          # its real environment
cat /proc/<pid>/limits                      # the limits it actually got
prlimit --pid <pid> --nofile=65536:65536    # raise them without a restart
kill -TERM <pid>; sleep 10; kill -0 <pid> && kill -KILL <pid>
```

## Network

```bash
ss -tlnp                                    # listeners
ss -tnp state established | head            # who is connected
ip route get 10.0.5.7                       # route AND source address chosen
getent hosts api.internal                   # resolution the way apps do it
nc -zv host 5432                            # is the port actually open
tcpdump -ni any -c 100 'host 10.0.5.7 and port 5432'
nstat -az | grep -iE 'retrans|drop|overflow'
```

## Services And Logs

```bash
systemctl status <unit> -l --no-pager
systemctl cat <unit>                        # vendor file + every drop-in, in order
systemctl show <unit> -p ExecStart -p Environment
journalctl -u <unit> --since "10 min ago" -o short-iso --no-pager
journalctl -b -1 -p err                     # previous boot (needs persistent journal)
systemd-analyze blame | head                # slow boot attribution
```

## Permissions

```bash
namei -l /srv/app/data/file                 # the first failing path component
getfacl /srv/app                            # and read the mask line
ls -Z /srv/app                              # SELinux labels
ausearch -m avc -ts recent                  # actual denials, with contexts
findmnt -T /srv/app                         # noexec/nosuid/ro on this path
getcap -r /usr/bin 2>/dev/null              # binaries with capabilities
```

## Users

```bash
getent passwd alice; id alice; passwd -S alice; chage -l alice
sudo -l -U alice                            # effective sudo rules
loginctl user-status alice                  # live sessions
last -n 20; lastb -n 20                     # recent logins and failures
```

## Change Safety

```bash
sshd -t                                     # validate sshd_config before restarting
visudo -c                                   # validate sudoers
mount -a                                    # validate fstab without rebooting
nft -c -f /etc/nftables.conf                # validate firewall rules
systemd-analyze verify /etc/systemd/system/my.service
systemd-run --on-active=10min --unit=rollback systemctl restart sshd   # scheduled undo
```

## Hardware And Platform

```bash
cat /etc/os-release; hostnamectl            # distro, kernel, virtualization
lscpu; lsmem 2>/dev/null || free -h
smartctl -a /dev/sda | head -40             # disk health
cat /proc/mdstat                            # RAID state
sensors 2>/dev/null                         # thermals on bare metal
```

## Tools Not Installed?

Minimal and container images often lack `lsof`, `ss`, `dig`, `iostat`, `smem`. Fallbacks that need nothing extra: `/proc/<pid>/fd` for open files, `/proc/net/tcp` for sockets, `getent hosts` for resolution, `/proc/diskstats` for I/O counters, `/proc/pressure/*` for saturation. Installing a diagnostic package on a production host during an incident is a change like any other: write it to `~/Clawic/data/linux/changes/<year>.md` with "remove after the incident" as its rollback, and which tools a host is missing to its row in `## Hosts` — arriving at the same box and rediscovering that it has no `lsof` costs minutes you will not have (→ `packages.md`, `memory-template.md`).
