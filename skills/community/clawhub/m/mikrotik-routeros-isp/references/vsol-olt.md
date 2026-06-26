# VSOL GPON OLT — SSH Reference

Tested on: VSOL V1600G1-B, V1600D, V1600G4 running VSOL firmware.

---

## Connection

```bash
sshpass -p "$OLT_PASS" ssh \
  -o StrictHostKeyChecking=no \
  -o KexAlgorithms=+diffie-hellman-group14-sha1 \
  -o HostKeyAlgorithms=+ssh-rsa \
  "$OLT_USER@$OLT_HOST"
```

> VSOL OLTs often require legacy SSH algorithms — always include KexAlgorithms and HostKeyAlgorithms flags.

---

## Essential Commands

### System
```
show version
show running-config
show interface gpon-olt_1/1
show interface gpon-onu_1/1:1
show onu state gpon-olt_1/1
show onu optical-info gpon-olt_1/1:1
show onu optical-info all gpon-olt_1/1
```

### ONU Discovery & Authorization
```
# Show unauthorized ONUs
show onu auto-find gpon-olt_1/1

# Authorize ONU by serial
interface gpon-olt_1/1
  onu 1 type RouterHGU sn VSOL12345678

# Bind ONU profile
interface gpon-onu_1/1:1
  service-profile PPPoE-1G
  tcont 1 name tcont1 profile HSI-1G
  gemport 1 name gem1 tcont 1
  vport-mode manual
  vport 1 map-type vlan
  vport-mode manual
```

### VLAN per PON Port (ISP mode)
```
# Upstream VLAN for PON port 1 = VLAN 500, PON port 2 = VLAN 501, etc.
interface vlan 500
  name PON1-PPPoE
interface gpon-olt_1/1
  service-port 1 vport 1 user-vlan untagged vlan 500
```

### ONU Status
```
show onu state gpon-olt_1/1         # all ONUs on port
show onu state gpon-olt_1/1:3       # specific ONU
show onu optical-info gpon-olt_1/1  # Rx/Tx power, laser bias
show mac-addr-table                 # learned MACs
```

### Optical Power Thresholds
| Parameter | Normal Range |
|-----------|-------------|
| ONU Rx Power | -8 to -27 dBm |
| OLT Rx Power | -8 to -27 dBm |
| TX Bias | 10–80 mA |

### Config Backup
```
copy running-config startup-config
copy startup-config tftp://192.168.1.10/olt-backup.cfg
```

---

## Troubleshooting

| Symptom | Command | What to look for |
|---------|---------|-----------------|
| ONU not registering | `show onu auto-find` | SN present? Auth missing? |
| No upstream traffic | `show onu state` | LOS, LOFi errors |
| Weak signal | `show onu optical-info` | Rx < -27 dBm = bad splice/distance |
| VLAN not passing | `show running-config interface gpon-olt` | service-port mapping correct? |
| MikroTik not getting PPPoE | Check upstream VLAN on MikroTik matches OLT VLAN | |
