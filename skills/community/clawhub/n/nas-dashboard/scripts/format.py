#!/usr/bin/env python3
"""NAS Dashboard V3 — alert-first + assessment + action guide"""
import re, sys
from datetime import datetime

with open(sys.argv[1]) as f:
    lines = [l.strip() for l in f if l.strip()]

data = {}
for line in lines:
    if '=' in line:
        key, val = line.split('=', 1)
        data[key] = val

def g(k, d='?'): return data.get(k, d)
now = datetime.now()
w = ['一','二','三','四','五','六','日'][now.weekday()]

# ── 知识库：每个问题的评估+修复方案 ──
class Alert:
    def __init__(self, severity, icon, title, detail, action, explain):
        self.severity = severity  # 🔴 🟡 🟢
        self.icon = icon          # ❌ ⚠️ ℹ️
        self.title = title
        self.detail = detail
        self.action = action
        self.explain = explain

alerts = []

# ── 环境检测 ──
is_lan = True  # default for home NAS (RFC1918 IP detected)
for l in lines:
    if l.startswith('IFACE=') and 'UP' in l:
        m = re.search(r'\b(\d+\.\d+\.\d+\.\d+)', l)
        if m:
            ip = m.group(1)
            is_lan = ip.startswith('192.168.') or ip.startswith('10.') or bool(re.match(r'172\.(1[6-9]|2\d|3[01])\.', ip))

# ── Security (环境感知) ──
fw_type = g('FW_TYPE', 'none')
if fw_type == 'none':
    if is_lan:
        alerts.append(Alert('🟡','⚠️','防火墙未启用',
            'NAT后内网，外网无法直达',
            'sudo ufw enable && sudo ufw allow 22/tcp',
            '中危：路由器挡了外网，但内网设备可接触所有端口'))
    else:
        alerts.append(Alert('🔴','❌','防火墙未启用',
            '公网直连！全端口暴露',
            'sudo ufw enable && sudo ufw default deny incoming && sudo ufw allow 22/tcp',
            '极高危：公网可扫描所有端口'))

ssh_pass = g('SSH_PASS_AUTH', 'no')
if ssh_pass == 'yes':
    alerts.append(Alert('🟡','⚠️','SSH允许密码登录',
        '内网受影响' if is_lan else '公网可暴力破解',
        'sudo sed -i "s/^PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config && sudo systemctl restart sshd',
        '内网风险可控' if is_lan else '高危：字典攻击可猜解密码'))

try:
    fl = int(g('FAILED_LOGINS', '0'))
    if fl > 50:
        alerts.append(Alert('🔴','❌',f'暴力破解 {fl}次',
            '疑似公网攻击' if not is_lan else '内网异常登录尝试',
            '先禁密码登录: sudo sed -i "s/^PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config && sudo systemctl restart sshd; 查来源: sudo grep Failed /var/log/auth.log | tail -20',
            '高危攻击' if not is_lan else '异常：检查内网设备'))
    elif fl > 10:
        alerts.append(Alert('🟡','⚠️',f'登录失败 {fl}次',
            '','查来源: sudo grep Failed /var/log/auth.log | tail -20',''))
    elif fl > 0:
        alerts.append(Alert('🟢','ℹ️',f'登录失败 {fl}次','','',''))
except: pass

# ── System ──
swap = g('SWAP_USED', '0')
if swap not in ('0', '0B', '0.0B'):
    swv = float(swap.replace('Gi','').replace('Mi','').replace('B','').strip() or 0)
    if 'Gi' in swap and swv > 4:
        alerts.append(Alert('🔴','⚠️','SWAP使用过高',
            f'{swap} — 物理内存不足','考虑加内存或关闭高内存服务；当前可用: free -h 查看',
            '内存不够用了，系统在疯狂写磁盘'))
    elif swv > 0:
        alerts.append(Alert('🟡','⚠️','SWAP使用',
            f'{swap} — 内存有压力','',''))

# ── ZFS ──
pool = g('POOL').split('\t') if g('POOL') != '?' else ['?']*7
pcap = (pool+['?']*5)[4]
try:
    pc = int(pcap.replace('%',''))
    if pc > 90:
        alerts.append(Alert('🔴','❌',f'Pool容量 {pcap}',
            '存储即将耗尽','zfs list -t snapshot | tail -20 清理旧快照；或扩容',
            '高危：ZFS写满会导致pool只读'))
    elif pc > 80:
        alerts.append(Alert('🟡','⚠️',f'Pool容量 {pcap}',
            '存储偏高','检查大文件: du -sh /tank/* | sort -rh | head -10',
            '建议清理旧快照或不需要的大文件'))
except: pass

# L2ARC waste
arc_m = re.match(r'size:([^ ]+) max:([^ ]+) hit:([^ ]+)', g('ARC'))
ah = arc_m.group(3) if arc_m else '?'
l2_m = re.match(r'size:([^ ]+)', g('L2ARC'))
l2s = l2_m.group(1) if l2_m else '0'
try:
    if float(ah.replace('%','')) > 99 and l2s not in ('0','0B','?'):
        alerts.append(Alert('🟡','⚠️','L2ARC浪费SSD寿命',
            f'{l2s} 仅贡献 <1% 读取',
            'sudo zpool remove tank nvme0n1p1 nvme1n1p1  # 移除L2ARC设备',
            'ARC命中率99.9%，L2ARC几乎没用，白白消耗NVMe写入寿命'))
except: pass

# ── Disks ──
for l in lines:
    if l.startswith('DISK_') and 'model:' in l:
        m = re.match(r'DISK_(\w+)=model:(.+?) size:(\S+) .*temp:(\d+)°C hours:(\d+) health:(\w+)', l)
        if not m: continue
        dn,mo,sz,tp,hr,hl = m.groups(); t=int(tp)
        if t>55:
            alerts.append(Alert('🔴','❌',f'{dn} 过热 {t}°C',
                '磁盘温度超标','检查机箱通风、风扇是否正常',
                f'长期高温({t}°C)会大幅缩短磁盘寿命'))
        elif t>45:
            alerts.append(Alert('🟡','⚠️',f'{dn} 温度偏高 {t}°C','','',''))
        if 'udma:' in l:
            u=int(re.search(r'udma:(\d+)',l).group(1))
            if u>100:
                alerts.append(Alert('🔴','❌',f'{dn} CRC错误 {u}次',
                    'SATA链路严重错误','更换SATA数据线，检查接口是否松动',
                    f'{u}次CRC错误说明数据线或接口有问题，继续使用可能导致数据损坏'))
            elif u>0:
                alerts.append(Alert('🟡','⚠️',f'{dn} CRC错误 {u}次',
                    'SATA链路轻微错误','重新插拔SATA数据线，或换一根线',
                    '数据线接触不良，暂时不严重但建议处理'))
        if 'realloc:' in l:
            r=int(re.search(r'realloc:(\d+)',l).group(1))
            if r>0:
                alerts.append(Alert('🔴','❌',f'{dn} 坏道 {r}个',
                    '磁盘物理损坏','立即备份数据，更换硬盘',
                    f'重映射扇区={r}，磁盘正在损坏，随时可能彻底失效'))
        if hl!='PASSED':
            alerts.append(Alert('🔴','❌',f'{dn} SMART {hl}','磁盘健康异常','备份数据并更换',''))

# ── Disk I/O ──
for l in lines:
    if l.startswith('DISKIO_'):
        m = re.match(r'DISKIO_(\w+)=.*r_await:([\d.]+)ms', l)
        if m and float(m.group(2))>20:
            alerts.append(Alert('🟡','⚠️',f'{m.group(1)} 读延迟{m.group(2)}ms',
                '磁盘响应慢','iostat -x 1 观察IO模式；可能是其他进程占用',
                '读等待>20ms，磁盘可能过载或接近故障'))

# ── Services ──
for l in lines:
    if l.startswith('SVC_') and 'inactive' in l:
        svc = l.replace('SVC_','').replace('=inactive','')
        if svc == 'nfs-server':
            alerts.append(Alert('🟢','⚠️',f'{svc} 未运行',
                '','如需NFS: sudo systemctl enable --now nfs-server',''))
        else:
            alerts.append(Alert('🟡','⚠️',f'{svc} 未运行',
                f'{svc}服务停止了','sudo systemctl restart {svc}',''))

# ── Images ──
stale=[]
for l in lines:
    if l.startswith('IMG_AGE='):
        p=l.replace('IMG_AGE=','').split('|')
        if len(p)==2:
            a=re.search(r'(\d+) months',p[1])
            if a and int(a.group(1))>=12:
                stale.append((p[0], int(a.group(1))))
if stale:
    stale.sort(key=lambda x:-x[1])
    worst = stale[0]
    alerts.append(Alert('🟡','⚠️',f'{len(stale)}个镜像>6月未更新',
        f'最旧: {worst[0].split("/")[-1][:20]} ({worst[1]}mo)',
        'docker pull <image> 拉取最新版本；注意先备份配置',
        '旧镜像可能有安全漏洞，建议定期更新'))

# ── APT ──
apt=g('APT_UPDATES','0')
aptn = int(apt) if apt.isdigit() else 0
if aptn > 50:
    alerts.append(Alert('🟡','⚠️',f'{aptn}个APT更新',
        '系统长期未更新','sudo apt update && sudo apt upgrade -y',
        '大量未安装更新包括安全补丁，建议尽快升级'))
elif aptn > 0:
    alerts.append(Alert('🟢','ℹ️',f'{aptn}个APT更新','','',''))

# ── Timeshift ──
try:
    tc=int(g('TIMESHIFT_COUNT','0'))
    if tc>300:
        alerts.append(Alert('🔴','❌',f'Timeshift {tc}个快照',
            '快照数量严重超标','sudo timeshift --delete-all 先清理，再调整策略',
            '大量快照会占满磁盘空间'))
    elif tc>100:
        alerts.append(Alert('🟡','⚠️',f'Timeshift {tc}个快照',
            '快照过多','sudo timeshift --delete 保留最近10个',
            '建议控制100以内'))
except: pass

# ── CPU ──
try:
    ct = re.search(r'\+([\d.]+)', g('CPU_TEMP'))
    ctv = float(ct.group(1)) if ct else 0
    if ctv > 85:
        alerts.append(Alert('🔴','❌',f'CPU过热 {ctv}°C','散热失效','检查风扇和散热器',''))
    elif ctv > 70:
        alerts.append(Alert('🟡','⚠️',f'CPU温度偏高 {ctv}°C','','清灰或改善通风',''))
except: pass

# ══════════════ DASHBOARD OUTPUT ══════════════
host=g('HOSTNAME'); os_s=g('OS').replace(' LTS','')
upt=g('UPTIME').replace(' days, ','d').replace(' hours, ','h').replace(' minutes','m')
l1=g('LOAD').split(',')[0]; cp=g('CPU_USED')
cb='█'*max(1,int(float(cp.replace('%',''))/10))+'░'*max(0,10-int(float(cp.replace('%',''))/10))
mu,mt,mp=g('MEM_USED'),g('MEM_TOTAL'),g('MEM_PCT')
ru=g('DISK_USAGE')
ct2=re.search(r'\+([\d.]+)',g('CPU_TEMP')); ctv2=ct2.group(1) if ct2 else '?'

pool=g('POOL').split('\t') if g('POOL')!='?' else ['?']*7
pn,pt,pu,ph,pf=(pool+['?']*7)[0],(pool+['?']*7)[1],(pool+['?']*7)[2],(pool+['?']*7)[5],(pool+['?']*7)[6]
pb='█'*max(1,int(float(pcap.replace('%',''))/10))+'░'*max(0,10-int(float(pcap.replace('%',''))/10))
scr=g('SCRUB').replace('scrub ','').replace('repaired 0B in ','').replace(' with 0 errors on ',' | ')[:28]
arc_m2=re.match(r'size:([^ ]+) max:([^ ]+) hit:([^ ]+)',g('ARC'))
asz,amx,ah2=(arc_m2.group(i) for i in (1,2,3)) if arc_m2 else ('?','?','?')
l2m2=re.match(r'size:([^ ]+) hit:([^ ]+)',g('L2ARC'))
l2sz=l2m2.group(1) if l2m2 else '0'; l2h=l2m2.group(2) if l2m2 else '?'
sn=g('SNAPSHOT_COUNT')

disks=[]
for l in lines:
    if l.startswith('DISK_') and 'model:' in l:
        m=re.match(r'DISK_(\w+)=model:(.+?) size:(\S+) .*temp:(\d+)°C hours:(\d+) health:(\w+)',l)
        if not m: continue
        dn,mo,sz,tp,hr,hl=m.groups()
        u=int((re.search(r'udma:(\d+)',l) or ['0']).group(1) if 'udma:' in l else '0')
        rl=int((re.search(r'realloc:(\d+)',l) or ['0']).group(1) if 'realloc:' in l else '0')
        aw=''
        for l2 in lines:
            if f'DISKIO_{dn}=' in l2:
                a=re.search(r'r_await:([\d.]+)ms',l2)
                if a and float(a.group(1))>5: aw=f" r:{a.group(1)}ms"
        tags=''
        if rl: tags+=f' realloc:{rl}'
        if u: tags+=f' udma:{u}'
        disks.append((dn,mo[:15],sz,tp,hr,tags+aw,hl))

ctr_t=sum(1 for l in lines if l.startswith('CTR=') and '|' in l)
ctr_h=sum(1 for l in lines if l.startswith('CTR=') and '(healthy)' in l)
ctr_bad=[l.replace('CTR=','').split('|')[0] for l in lines if l.startswith('CTR=') and '|' in l and '(healthy)' not in l]

cam=[]
for l in lines:
    if l.startswith('FRIGATE_CAM='):
        m=re.match(r'FRIGATE_CAM=([^|]+)\|fps:([^|]+)\|.*skip:([^|]+)',l)
        if m: cam.append((m.group(1),m.group(2),m.group(3)))
cmap={'cam_d82e8e00':'车库','cam_ae7e3010':'北门','cam_a24a20c0':'院子'}

gpu=g('GPU','').split(', ')

tm=re.match(r'↓(\d+)MB ↑(\d+)MB',g('TRAFFIC'))
rx=int(tm.group(1))/1024 if tm else 0; tx=int(tm.group(2))/1024 if tm else 0

cpu_p=[]
for l in lines:
    if l.startswith('TOP_CPU=') and '200.0%' not in l:
        m=re.match(r'([\d.]+)% (.+)',l.replace('TOP_CPU=',''))
        if m and len(cpu_p)<3: cpu_p.append((m.group(1),m.group(2).split('/')[-1][:12]))

fs=[l.replace('SVC_','').replace('=inactive','') for l in lines if l.startswith('SVC_') and 'inactive' in l]

op=g('OPEN_PORTS','none')
if op!='none':
    pl=op.split(',')
    imp=[p for p in pl if p in ('22','80','443','8123','8384','8443','8080','8972','8973','9090','9443','51821','3000','3001','8006')]
    ops=','.join(imp[:8]) if imp else pl[0] if pl else '?'
else: ops='?'

ups_s=g('UPS_ups.status','?'); upsi='⚡' if ups_s=='OL' else '🪫'
ups_c=g('UPS_battery.charge','?')
tsc=g('TIMESHIFT_COUNT','0'); tsl=g('TIMESHIFT_LAST','').replace('_',' ')[:16]

# ── BUILD ──
out=[]
out.append(f"╭──────────────────────────────────╮")
out.append(f"│  🏠 {host} · {now.strftime('%m-%d')} 周{w} · {'🏠内网' if is_lan else '⚠️公网'}  │")
out.append(f"╰──────────────────────────────────╯")

# ═══ ALERTS ═══
alerts.sort(key=lambda a: (0 if a.severity=='🔴' else 1 if a.severity=='🟡' else 2))
if alerts:
    crit = [a for a in alerts if a.severity=='🔴']
    warn = [a for a in alerts if a.severity=='🟡']
    info = [a for a in alerts if a.severity=='🟢']
    total = len(alerts)
    
    out.append(f"🚨 预警 · 🔴{len(crit)} 🟡{len(warn)} 🟢{len(info)} · 共{total}项")
    for a in alerts:
        line = f"{a.severity} {a.title}"
        if a.detail: line += f" — {a.detail}"
        out.append(line)

out.append("━"*36)

# ═══ BODY ═══
out.append(f"🖥 {os_s} · up {upt} · load {l1} · {ctv2}°C")
out.append(f"   CPU {cp} {cb} · RAM {mu}/{mt} ({mp}) · / {ru}")
# Find the primary active interface
iface_name = '?'
iface_ip = '?'
for l in lines:
    if l.startswith('IFACE=') and 'UP' in l:
        m = re.match(r'IFACE=(\S+)\s+UP\s+([\d.]+)', l)
        if m:
            iface_name = m.group(1)
            iface_ip = m.group(2)
            break

out.append(f"   🌐 {iface_name}: {iface_ip} · ↓{rx:.0f}G ↑{tx:.0f}G")
out.append(f"")
out.append(f"🗄 tank [{ph}] · {pu}/{pt} ({pcap}) {pb} · frag {pf}")
out.append(f"   ARC {asz}/{amx} hit {ah2}"+(f" · L2 {l2sz} hit {l2h}" if l2sz not in ('0','?') else ""))
out.append(f"   Snap {sn} · Scrub ✓ {scr}")
out.append(f"   DISKS {'─'*20}")
for dn,mo,sz,tp,hr,tags,hl in disks:
    ic='✅' if hl=='PASSED' else '❌'; pf2='⚠️' if (int(tp)>45 or 'realloc' in tags) else '  '
    out.append(f"   {pf2} {dn:<5} {mo:<15} {sz:>6} {tp:>2}°C {hr:>5}h{tags} {ic}")
out.append(f"")
out.append(f"🐳 {ctr_t} ctr ({ctr_h} ok)"+(f" · {len(ctr_bad)} no-hc" if ctr_bad else ""))
if ctr_bad: out.append(f"   ⚠️ {', '.join(ctr_bad[:4])}")
if cam:
    cs=' · '.join(f"{cmap.get(c[0],c[0])}:{c[1]}fps" for c in cam)
    out.append(f"📹 {cs}")
if len(gpu)>=5: out.append(f"\n🎮 {gpu[0]} · {gpu[1]}°C · {gpu[2]} · {gpu[3]}/{gpu[4]}")
out.append(f"\n🔒 Failed login: {g('FAILED_LOGINS','0')}")
ssh=f"port {g('SSH_PORT','?')}"
if g('SSH_PASS_AUTH','?')!='?': ssh+=f" · pass:{g('SSH_PASS_AUTH')}"
if g('SSH_ROOT_LOGIN','?')!='?': ssh+=f" · root:{g('SSH_ROOT_LOGIN')}"
fw_label=fw_type.upper() if fw_type!='none' else '❌ OFF'
out.append(f"   SSH: {ssh} · FW: {fw_label}")
if ops and ops!='?': out.append(f"   Ports: {ops}")
if fs: out.append(f"\n⚙️ ⚠️ {', '.join(fs)} inactive")
if cpu_p: out.append(f"\n📊 {' · '.join(f'{p[0]}% {p[1]}' for p in cpu_p)}")
fp=[]
if ups_s: fp.append(f"🔋 {upsi} {ups_c}%")
if tsc!='0': fp.append(f"💾 TS:{tsc}{' ⚠️' if int(tsc)>100 else ''}")
if apt!='0': fp.append(f"📦 {apt} updates")
if fp: out.append(f"\n{' · '.join(fp)}")

# ═══ ACTION GUIDE ═══
if alerts:
    actionable = [a for a in alerts if a.action]  # only items with concrete fixes
    if actionable:
        out.append(f"\n{'━'*36}")
        out.append(f"📋 行动指南")
        for a in actionable[:5]:  # top 5 most critical
            out.append(f"{a.severity} {a.title}")
            if a.explain: out.append(f"   评估: {a.explain}")
            if a.action: out.append(f"   修复: {a.action}")

print('\n'.join(out))
