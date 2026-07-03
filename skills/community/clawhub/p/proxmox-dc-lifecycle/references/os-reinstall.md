# OS reinstall (hands-off, autounattend)

Reinstall **onto the existing VM** (same VMID/MAC/disk) — never recreate the VM, or you lose MAC/IP/config. Only enter this phase once the metadata-cleanup gate is green.

## 1. Read the VM's hardware (decides driver + partitioning)
```bash
sudo qm config <vmid> | grep -E '^virtio0|^scsi|^scsihw|^net0|^boot|^bios|^efidisk|^tpmstate'
```
- Boot disk `virtio0` ⇒ **viostor** driver. A `scsiN` disk on `virtio-scsi` ⇒ **vioscsi**. Inject both to be safe.
- `bios: ovmf` ⇒ **UEFI/GPT** partitioning (EFI+MSR+Windows). SeaBIOS ⇒ MBR.
- Note the MAC and `net0` bridge/VLAN — they stay; the unattend just configures the IP on top.

## 2. Confirm the install image index
```bash
sudo apt-get install -y wimtools   # if wiminfo missing
# mount the ISO read-only first, then read the WIM:
sudo mount -o loop,ro <server>.iso /tmp/srviso
wiminfo /tmp/srviso/sources/install.wim
```
For Server 2025 Eval: **1=StandardCore, 2=Standard+Desktop, 3=DatacenterCore, 4=Datacenter+Desktop**. Use the **index** for `/IMAGE/INDEX` in the unattend — selecting by NAME is error-prone (a mismatch silently defaults to Datacenter). NOTE: on some eval media Setup defaults to Datacenter even with a correct INDEX (an `ei.cfg`/`ImageInstall` quirk) — for a DC the edition is functionally irrelevant (Datacenter is a superset), so verify after install with `(Get-WindowsEdition -Online).Edition` + the `InstallationType` reg key (`Server Core` vs `Server`) and accept Datacenter Core if that's what landed. See gotchas.

## 3. Confirm virtio driver paths
Mount `virtio-win-*.iso` and verify `viostor/2k25/amd64`, `vioscsi/2k25/amd64`, `NetKVM/2k25/amd64` exist (use the folder matching your Server version). The unattend template references drive `E:` for these — make sure the virtio ISO ends up as the drive letter the template expects (or edit the paths).

## 4. Build the unattend ISO
Fill `assets/autounattend.xml.template` placeholders (image INDEX, computer name, IP/CIDR, gateway, DNS, domain, timezone, admin password) → `autounattend.xml`, then:
```bash
scripts/build-unattend-iso.sh /path/to/autounattend.xml /tmp/unattend.iso
# copy to a Proxmox ISO storage so qm can attach it
sudo cp /tmp/unattend.iso /mnt/pve/<isoStorage>/template/iso/unattend-<dc>.iso
```
The script puts `autounattend.xml` at the ISO root so Windows Setup auto-detects it. Generate the admin password as a throwaway random; show only its sha256 fingerprint; delete the ISO right after install.

## 5. Attach media, set boot, wipe-and-install  ← DESTRUCTIVE (confirm first)
Confirm the Phase-3 gate is green (no `nTDSDSA` for this DC) and get explicit operator confirmation to wipe this specific `<vmid>` before running:
```bash
sudo qm shutdown <vmid> --timeout 60 || sudo qm stop <vmid>
sudo qm set <vmid> --ide2 <isoStorage>:iso/<server>.iso,media=cdrom
sudo qm set <vmid> --ide0 <isoStorage>:iso/virtio-win-<ver>.iso,media=cdrom
sudo qm set <vmid> --ide1 <isoStorage>:iso/unattend-<dc>.iso,media=cdrom
sudo qm set <vmid> --boot order='ide2;virtio0'
sudo qm start <vmid>
```
Note the drive-letter mapping Windows assigns to the virtio ISO and adjust the unattend `DriverPaths` if needed (it assumes `E:`). For UEFI, Setup honors `autounattend.xml` at the root of any attached removable/CD volume.

## 6. Wait & verify (gate)
- Poll the guest agent until it responds again (install + first boot can be 10–20 min). Note: the agent may answer *during* OOBE — don't treat first response as "done."
- Authoritative "install complete" signal: registry `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Setup\State\ImageState` = `IMAGE_STATE_COMPLETE`. Prefer this over the `oobe_done.txt` marker (FirstLogonCommands redirects can misfire). The template still writes the marker as a secondary hint.
- Confirm hostname, IP, timezone, and that it's a clean member-server-to-be (NTDS NOT present yet — promotion is the next phase).
- After verifying, detach the install media and set boot back to the disk (do this in Finalize, or now if you prefer):
  ```bash
  sudo qm set <vmid> --boot order='virtio0'
  sudo qm set <vmid> --delete ide0,ide1,ide2
  ```

## Notes
- Secure Boot: if the VM has `pre-enrolled-keys=1`, signed Server media boots fine under secure boot.
- If install fails to find the disk → virtio storage driver not injected/wrong path (see gotchas). Grab a console screenshot (`qm terminal`/noVNC) to see where Setup stopped.
