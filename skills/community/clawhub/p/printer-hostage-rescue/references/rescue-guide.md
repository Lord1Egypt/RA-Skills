# Printer Rescue — Full Reference

## 1. The business models behind "errors"
- **Ink chips estimate, they don't measure.** "Empty" fires at 5–20% reserve; carts
  often have 20–40% ink left. Override: printer menu (Settings → Ink/Supplies →
  Disable monitoring) or accept-and-warn. Quality fade is the real replacement signal.
- **Cartridge DRM**: chip-ID handshake; vendors push firmware that blocks third-party
  carts. Vendors historically retract blocking firmware after backlash (HP 2016
  "Dynamic Security" class action; Epson/Canon similar). Check the vendor's firmware
  release notes; optional updates can be skipped; downgrade paths sometimes published.
- **Region locks**: carts are regionalized; after relocation the printer rejects local
  carts. All major vendors have a regionalization-reset flow — free with proof
  (serial + local cart purchase); HP/Epson/Canon/Brother support pages document it.
- **Subscription ink (Instant Ink etc.)**: the printer bricks locally if billing
  fails — the cartridges are vendor-leased. Exit: cancel subscription properly; the
  printer switches to your own retail cartridges after a short grace window.

## 2. Legal backdrop (know your lever)
- **EU/UK**: refusing to function with refilled/third-party consumables without
  clear pre-purchase disclosure can breach Unfair Commercial Practices rules; printer
  warranty cannot be voided merely for using third-party ink (must prove the refill
  caused the damage).
- **US**: Magnuson-Moss — warrantors can't require OEM consumables unless provided
  free; "warranty void" stickers are unenforceable (FTC).
- Class actions have repeatedly produced firmware fixes / payouts (HP Dynamic
  Security 2021 settlement).

## 3. Driverless printing (do this first, always)
- **IPP Everywhere / AirPrint / Mopria**: universal standards; Windows 10 1903+,
  macOS 10.something+, iOS, Android 8+, and CUPS 2.x all speak it. No vendor
  software needed. If a printer speaks IPP over the network, it prints.
- Probe order (scripts/print_rescue.py discover):
  - TCP 631 (IPP) → `ipp://IP/ipp/print` — the modern universal queue
  - TCP 9100 (raw JetDirect) — legacy but universal
  - TCP 80/443 — web admin (supplies status, network config, often deeper menus)
  - mDNS `_ipp._tcp` / `_universal._sub._ipp._tcp` → AirPrint capability flag
- Linux add: `lpadmin -p rescue -E -v ipp://IP/ipp/print -m everywhere`
- Windows: Settings → Printers → Add → it appears as IPP if supported.

## 4. Spooler surgery
- Windows: `net stop spooler & del /Q %SYSTEMROOT%\System32\spool\PRINTERS\*.* &
  net start spooler`
- macOS: `cancel -a -` then restart `cupsd` (`sudo launchctl kickstart -k system/org.cups.cupsd`)
- Linux/CUPS: Web UI http://localhost:631 → Jobs → Cancel All; `cancel -a`;
  stuck jobs in /var/spool/cups.

## 5. Mechanical class details
- **Ghost jam**: fragment from an envelope label deep in the duplexer; flashlight +
  rear door + cardstock strip along the whole path; sensors (actuator flags) get
  knocked out of position when pulling paper against the feed direction.
- **Blank pages inkjet**: air in the printhead after cart swap → ONE cleaning,
  print a nozzle check, wait, repeat once; persistent single-color absence = that
  channel's nozzle burned or the cart valve stuck — try another cart before a new head.
- **Laser ghosting every ~7–9 cm**: drum (OPC) wear — replace drum unit, not toner.
  Repeating specks at fixed interval = roller defect; interval length identifies roller.
- **WiFi phantom**: printer re-associated to a mesh extender with client isolation;
  IP-based IPP fixes it; reserve DHCP so it never floats again.

## 6. Service modes (use with care)
- Vendor service menus expose deeper resets (NVRAM, EEPROM, waste-ink counter).
  Model-family key sequences change constantly; look up the exact model + "service
  mode". Resetting waste-ink counters WITHOUT cleaning/absorbing the pad floods the
  printer later — a counter reset is a maintenance-lie unless the pad is serviced.

## 7. Replacement economics
| Scenario | Do |
|---|---|
| <100 text pages/mo | mono laser ($120–180), toner 3k pages, no clogging if used monthly |
| Occasional color photos | inkjet but PRINT WEEKLY or accept cleaning waste; or lab prints |
| Photo volume | dye-sub or lab; inkjet photo page-cost is worst |
| Printhead dead (>~$90 printer value) | replace printer; heads are not economical below mid-range |
| Drum end-of-life on old mono laser | drum $60–90 vs new laser with full toner $130 — usually replace |
Page-cost math: inkjet color ~$0.10–0.25/pg (incl. cleaning waste) vs mono laser
~$0.02–0.04/pg; subscription ink only wins if usage matches the tier closely.

## 8. When it's NOT worth rescuing
- Formatter/WiFi board faults on consumer models (part > printer)
- Waste-ink pad saturated twice (the printer is at end of service life by design)
- Any repair quote > 50% of a new device with warranty
