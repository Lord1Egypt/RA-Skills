# Gotchas: Hyper-V VM Creation

## VHDX Sparse Flag (Showstopper)
- `qemu-img convert` creates VHDX with NTFS sparse attribute
- Hyper-V refuses to start or resize sparse VHDX (error `0xC03A001A`)
- **Fix:** `fsutil sparse setflag "<path>.vhdx" 0` BEFORE Resize-VHD
- **Order matters:** sparse removal -> resize -> permissions -> create VM

## Cloud-Init Network Config (Showstopper)
- Hyper-V NICs use the `hv_netvsc` driver
- Interface names vary between image versions (eth0, ens1, etc.)
- Without a network-config file, VM boots with zero networking
- **Fix:** Match by driver, not interface name:
  ```yaml
  version: 2
  ethernets:
    id0:
      match:
        driver: hv_netvsc
      dhcp4: true
  ```

## File Permissions
- Hyper-V service account needs explicit VHDX access
- **Fix:** `icacls "<path>.vhdx" /grant "NT VIRTUAL MACHINE\Virtual Machines:(F)"`
- Without this, Start-VM fails with "Access denied"

## Secure Boot
- Ubuntu cloud images aren't signed for Hyper-V Secure Boot
- **Fix:** `Set-VMFirmware -VMName <name> -EnableSecureBoot Off`

## Cloud-Init Runs Once
- If cloud-init completes (even with errors), it won't re-run on reboot
- No "retry" mechanism exists
- **Fix:** Delete VM, delete VHDX, reconvert from cloud image, start over

## PowerShell Batching
- Running multiple Hyper-V cmdlets in rapid succession causes intermittent failures
- **Fix:** Execute one command at a time with error checking between each

## Elevated PowerShell Required
- All Hyper-V commands and `fsutil` need admin elevation
- For automation, use: `powershell -ExecutionPolicy Bypass -File script.ps1`

## Docker Compose v2
- Cloud-init must install Compose v2 plugin via curl, NOT via apt
- `apt install docker-compose` installs v1 which is broken with modern images
- **Fix:** curl the compose plugin binary into `/usr/local/lib/docker/cli-plugins/`

## IP Discovery
- `(Get-VMNetworkAdapter -VMName <name>).IPAddresses` returns empty without guest integration services
- Cloud images don't have `linux-tools-virtual` or `hyperv-daemons` installed
- **Fix:** ARP scan: `arp -a | grep "00-15-5d"` and match MAC from PowerShell
- PowerShell MAC format: `00155D38010A`, ARP format: `00-15-5d-38-01-0a`
