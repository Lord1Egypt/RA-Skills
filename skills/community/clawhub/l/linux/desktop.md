# Desktop And Laptop — Display, GPU, Suspend, Audio, Wi-Fi, Power

A workstation fails in places a server does not have: a compositor, a GPU driver signed by someone else, a battery, and a session bus. Identify the stack before typing — half of the advice on the internet is for the other one.

```bash
echo "$XDG_SESSION_TYPE"; loginctl show-session "$(loginctl | awk '/tty|seat/{print $1; exit}')" -p Type   # wayland or x11
lspci -k | grep -A3 -iE 'vga|3d'        # GPU and the driver in use ("Kernel driver in use:")
systemd-detect-virt; cat /sys/class/dmi/id/product_name   # VM or a real laptop model
wpctl status 2>/dev/null || pactl info  # PipeWire or PulseAudio
nmcli device status                     # network stack in charge
```

## Wayland Or X11 — What Changes

| Concern | X11 | Wayland |
|---|---|---|
| Screen sharing / recording | Any app can capture the screen | Only through the xdg-desktop-portal; an app without portal support records a black rectangle |
| Global hotkeys, `xdotool`, `wmctrl`, auto-typing | Work | Blocked by design; compositor-specific protocols only |
| `DISPLAY=:0` for a cron job or a remote command | Works with `xhost`/`XAUTHORITY` | Needs `WAYLAND_DISPLAY` and `XDG_RUNTIME_DIR` of the live session |
| NVIDIA proprietary driver | Mature | Workable on recent driver branches; the fallback when something is broken is a single X11 login |
| Per-monitor scaling and mixed DPI | One global scale, blurry on mixed setups | Real per-output scaling, with XWayland apps blurry instead |
| else | `xrandr` for display config | The compositor's own tool (`wlr-randr`, GNOME/KDE settings) |

The diagnostic that saves an hour: log out, pick the other session type at the greeter, and see whether the symptom follows. Most "my app broke after the upgrade" reports on a modern distro are the default flipping to Wayland.

## GPU Drivers

- `lspci -k` "Kernel driver in use" is the ground truth: `nouveau` when you installed the proprietary driver means the install did not take, usually because the module failed to build or load.
- Proprietary NVIDIA modules are built per kernel by DKMS. `dkms status` before rebooting after a kernel upgrade; a kernel that outruns DKMS boots to a black screen or a text console (→ `kernel.md`, `packages.md`).
- **Secure Boot rejects unsigned modules.** The symptom is "Required key not available" in `dmesg` and no GPU. The fix is enrolling a MOK (the installer usually offers it, and the enrolment prompt appears at the NEXT boot, before the OS), not disabling the module.
- Black screen after an install or upgrade: boot with `nomodeset` from the GRUB menu to get a console, then fix the driver from there (→ `boot.md`).
- Hybrid graphics (Intel + NVIDIA/AMD): the discrete card should be idle at the desktop. Check with `nvidia-smi` or `cat /sys/class/drm/card*/device/power_state`; a discrete GPU that never sleeps is most of an unexplained battery drain.
- External monitor dead on a hybrid laptop usually means the port is wired to the discrete GPU, which the current mode does not use.

## Suspend, Hibernate, Resume

- Which sleep the firmware offers: `cat /sys/power/mem_sleep`. `[s2idle]` selected on a machine that supports `deep` gives the "laptop is hot in the bag and the battery is empty" report; select `deep` on the kernel command line (`mem_sleep_default=deep`) where the firmware supports it.
- Wakes up immediately after suspending: something is asserting a wakeup. `cat /proc/acpi/wakeup` lists devices and whether wakeup is enabled; USB devices and the wired NIC are the usual culprits. Test by disabling one at a time.
- Nothing comes back after resume (black screen, no input): read `journalctl -b -1` from the failed attempt — this is the case that needs the journal to be persistent, and the setting has to be there BEFORE the incident (→ `logs.md`).
- Proprietary GPU drivers need their suspend helpers enabled (`nvidia-suspend.service`, `nvidia-hibernate.service`, `nvidia-resume.service`) or the framebuffer comes back corrupted.
- **Hibernation needs swap at least the size of the memory in use** (sizing to full RAM is the safe rule) plus a `resume=UUID=…` kernel parameter pointing at it, plus initramfs support. It is also incompatible with Secure Boot on some distros' lockdown settings.
- `systemctl suspend`, `hibernate`, `hybrid-sleep`, `suspend-then-hibernate` are all systemd targets: `systemctl status systemd-suspend.service` shows what the hooks in `/usr/lib/systemd/system-sleep/` did.

## Audio

- PipeWire has replaced PulseAudio and JACK on current distros, with `pipewire-pulse` as a drop-in replacement. `wpctl status` lists devices and defaults; `wpctl set-default <id>` changes the sink. Running PulseAudio and PipeWire at once produces silence with no error — check that `pulseaudio.service`/`.socket` are masked for the user.
- No sound after switching output: the application picked the old sink and kept it. `wpctl` moves the stream, or restart the app.
- Bluetooth headsets: A2DP is stereo with no microphone; the moment an app opens the mic the device drops to HSP/HFP and the quality collapses. That is the protocol, not a bug — a separate microphone is the only real fix.
- HDMI audio silent while the picture works: the sink exists but is not default, and often needs the correct profile (`wpctl` or the desktop's sound panel).
- Crackling and dropouts under load are usually the quantum/buffer size; raising it trades latency for stability. Do not chase it with a kernel change first.

## Wi-Fi, Bluetooth, Network

- `nmcli device status`, `nmcli connection show`, `nmcli device wifi list` cover most of it; `rfkill list` catches the hardware or software kill switch that makes an adapter simply not exist.
- **Wi-Fi that drops when idle is nearly always power saving.** `iw dev wlan0 get power_save`; disable per-connection with NetworkManager (`wifi.powersave = 2` in a `/etc/NetworkManager/conf.d/` file) rather than a boot script.
- Weak signal on 5 GHz channels can be the regulatory domain: `iw reg get`, set with `iw reg set <CC>` and persist in `/etc/conf.d/wireless-regdom` or the distro's equivalent.
- Missing firmware is the other half of "no Wi-Fi": `dmesg | grep -i firmware` names the file, and the package is usually `linux-firmware` or a vendor one.
- VPN clients rewriting DNS: on systemd-resolved hosts the fix is per-link routing (`resolvectl domain`), not editing `/etc/resolv.conf` (→ `networking.md`).
- Bluetooth pairing that fails after a dual-boot: Windows and Linux each hold a different link key for the same device. Re-pair, or copy the key across.

## Power And Thermals

- Run ONE power manager. `tlp` and `power-profiles-daemon` conflict; distributions ship one or the other, and installing both produces settings that fight. `powerprofilesctl` or `tlp-stat -s` says which is active.
- `powertop --auto-tune` is a diagnostic that also applies aggressive settings — it can disable USB devices mid-session. Read its report, then apply the specific settings you want.
- Unexplained drain checklist: discrete GPU awake, a browser tab pinning a core, `powertop`'s wakeups-per-second list, and a Bluetooth or USB device blocking deeper C-states.
- Thermal throttling on a laptop looks like a slow machine: `watch -n1 "grep MHz /proc/cpuinfo | head"` alongside `sensors`. A machine that runs at half its clock under load is a cooling problem, not a configuration one.
- `cpupower frequency-info` (or the `scaling_governor` files) shows the governor. `powersave` on a plugged-in workstation costs real throughput.

## Session, Portals, And Sandboxed Apps

- User units (`systemctl --user`) run only while the user has a session unless `loginctl enable-linger <user>` is set — this is why a user timer does not fire when nobody is logged in (→ `systemd.md`).
- `xdg-desktop-portal` plus its backend (`-gtk`, `-kde`, `-wlr`) is what gives sandboxed apps file dialogs, screen sharing, and notifications. Screen sharing that lists no windows is nearly always a missing or wrong backend.
- Flatpak and Snap apps run confined: no access to `~/.ssh`, other users' files, or arbitrary paths until granted (`flatpak override --filesystem=…`, `snap connect`). A "permission denied" that no `namei -l` explains is the sandbox, not the filesystem (→ `permissions.md`).
- Themes and fonts not applying to a Flatpak app is the same confinement, solved by installing the theme as a Flatpak runtime extension rather than by chmodding anything.
- The desktop's own keyring (`gnome-keyring`, `kwallet`) holds SSH passphrases and app secrets; a headless or SSH login has no keyring unlocked, which is why an SSH key that works on the desktop prompts over a remote session (→ `ssh.md`).

## Record It

Hardware-specific workarounds are the most re-read thing this file produces and the easiest to lose: the kernel parameter that fixed suspend, the MOK enrolment, the firmware package, the disabled wakeup source. Write them to `artifacts/<machine>-quirks.md` with its `## Boxes` line in `memory.md`, and the change itself with its persistence file and rollback to `changes/<year>.md`. Put the laptop in `## Hosts` too — a workstation is a host, and the next kernel upgrade will ask what its GPU driver was. Formats: `memory-template.md`.

Related: kernel modules, DKMS and parameters → `kernel.md` · boot recovery with `nomodeset` → `boot.md` · user units and lingering → `systemd.md` · network stack details → `networking.md` · distro differences → `distros.md`.
