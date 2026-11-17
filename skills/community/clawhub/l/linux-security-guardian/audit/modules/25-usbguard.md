# Module 25 — USBGuard Audit

> **Purpose:** Audit USB device authorization. USBGuard provides a software framework for implementing USB device authorization policies. Without it, any USB device plugged into the server (by data center staff or via IPMI virtual media) is immediately authorized — including malicious USB drives (BadUSB, Rubber Ducky) that can emulate keyboards and inject commands.

## Threat Model
- **Data Center:** Staff with physical access can plug in malicious USB
- **IPMI/iDRAC/iLO:** Virtual media mount appears as USB mass storage
- **Cloud VM:** Less relevant but check if USB controller is exposed to VM
- **Office/On-Prem:** Highest risk — any passerby with physical access

## Commands
```bash
# Check if USBGuard is installed
which usbguard 2>/dev/null || dpkg -l usbguard 2>/dev/null | grep "^ii" || echo "usbguard_not_installed"

# Check USBGuard daemon status
systemctl is-active usbguard 2>/dev/null || echo "usbguard_service_not_active"

# Check USBGuard policy (installed and running)
usbguard list-devices 2>/dev/null | head -30

# Check USBGuard rules
usbguard list-rules 2>/dev/null | head -20

# Check for USB kernel modules loaded
lsmod 2>/dev/null | grep -i usb

# Check USB controllers present
lsusb 2>/dev/null || echo "lsusb_not_available"

# Check if USB storage driver is blacklisted
grep -r "usb-storage\|usb_storage" /etc/modprobe.d/ 2>/dev/null || echo "usb_storage_not_blacklisted"

# Check USB kernel config
cat /sys/module/usb_storage/parameters/delay_use 2>/dev/null && echo "usb_storage_active" || echo "usb_storage_module_not_loaded"

# Check for USBGuard dbus service
busctl list 2>/dev/null | grep usbguard || echo "no_usbguard_dbus"
```

## Checks & Findings

| Condition | Severity | Detail |
|-----------|----------|--------|
| USBGuard not installed | **MEDIUM** | No USB authorization framework |
| USBGuard installed but service stopped | **HIGH** | Installed but not protecting |
| USBGuard active with default policy (block) | **PASS** | All USB devices blocked by default |
| USBGuard active with allow-all policy | **MEDIUM** | Running but not blocking anything |
| usb-storage module loaded on non-cloud server | **MEDIUM** | USB mass storage possible |
| usb-storage not blacklisted | **MEDIUM** | Mass storage driver can be loaded anytime |
| USB controllers present on server | **LOW** | Attack surface exists |
| No USB controllers (pure cloud VM) | **INFO (Skip)** | No USB attack surface |
| IPMI virtual media enabled | **MEDIUM** | Virtual USB via BMC |

## Cloud VM Considerations
- Most cloud VMs (AWS, GCP, Azure) have NO USB controllers → **SKIP** this module
- Contabo VPS may expose USB → **CHECK**
- Bare metal / dedicated servers → **FULL CHECK**

## Auto-Fix Options (Confirm Required)

### Install & Configure USBGuard
```bash
# Install
apt-get install -y usbguard

# Generate initial policy (authorizes currently connected devices)
usbguard generate-policy > /etc/usbguard/rules.conf

# Set default policy to block (most secure)
echo 'allow with-interface equals { 03:01:01 03:01:02 }' >> /etc/usbguard/rules.conf
# (The above allows only HID keyboards/mice)

# Start and enable
systemctl enable --now usbguard
```

### Blacklist USB Storage (Without USBGuard)
```bash
# Prevent USB mass storage driver from loading
echo "blacklist usb-storage" > /etc/modprobe.d/blacklist-usb-storage.conf
echo "install usb-storage /bin/false" >> /etc/modprobe.d/blacklist-usb-storage.conf
update-initramfs -u
```

### Disable USB via Kernel Parameter (Extreme)
```bash
# Add to GRUB_CMDLINE_LINUX in /etc/default/grub:
# usbcore.nousb
# WARNING: This disables ALL USB including keyboards on physical servers
```

## Output Format
```
[HIGH] 25-usbguard: not_running | usbguard installed but service stopped | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 25-usbguard: not_installed | usbguard not installed | usb-storage loaded | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 25-usbguard: usb_storage_not_blacklisted | usb_storage module can be loaded | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 25-usbguard: allow_all_policy | usbguard default policy: allow | all USB devices authorized | action_id: ACT-YYYYMMDD-XXX
[PASS] 25-usbguard: active_block_policy | usbguard active, default: block, 3 rules ✓
[INFO] 25-usbguard: cloud_vm_skip | no USB controllers — cloud VM, module skipped
[INFO] 25-usbguard: summary | usbguard: installed | status: active | policy: block | devices: 0 authorized
```
