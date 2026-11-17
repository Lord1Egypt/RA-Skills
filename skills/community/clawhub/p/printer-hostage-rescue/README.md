# printer-hostage-rescue

Printers refuse to print for reasons that are mostly business models, not faults:
"empty" cartridges with ink in them, region locks after a move, "non-genuine"
refusals on legally refilled carts, wedged spoolers masquerading as dead hardware,
and 2009 driver CDs. This skill classifies the failure and walks the actual fix —
including driverless IPP setup that skips vendor software entirely.

## The real-world problem
- Ink chips estimate, not measure — "empty" fires at 5–20% reserve
- Firmware updates re-enable cartridge blocking after class actions forced retreats
- Half of "dead printers" are a wedged print queue on one machine
- Every new device triggers the vendor "full feature" driver stack when IPP
  Everywhere / AirPrint has been built into every OS for years
- Subscription ink bricks the printer when billing fails

## What it does
`scripts/print_rescue.py` (stdlib only) — four working subcommands:

- **diagnose** — keyword classifier over 11 failure classes with the real cause +
  fix path for each
- **spooler** — lists/clears CUPS queues (`cancel -a`), prints exact Windows/macOS
  spooler-surgery commands otherwise
- **discover** — subnet scan for ports 631/9100/80/443, tags each hit
  (IPP/driverless, raw JetDirect, web admin), sends a real **IPP
  Get-Printer-Attributes request** to prove the printer speaks driverless, prints
  the `lpadmin -m everywhere` one-liner to add it with zero vendor drivers
- **economics** — inkjet vs mono-laser page-cost comparison with crossover math

```
$ python3 scripts/print_rescue.py diagnose --symptom "non-genuine cartridge detected"
[non-genuine] (match 1)
  Cartridge DRM. Check firmware version against blocking updates; …

$ python3 scripts/print_rescue.py discover --subnet 192.168.3.0/24
  192.168.3.30     [631, 80]  IPP/driverless-likely + web-admin
  192.168.3.30: IPP alive (version 2.0, 89B resp)
  Add driverless queue: lpadmin -p rescue -E -v ipp://192.168.3.30/ipp/print -m everywhere
```

## Files
- `SKILL.md` — 12-class failure→fix table, workflow, pitfalls, replacement economics
- `references/rescue-guide.md` — DRM/legal backdrop, driverless protocols, spooler
  surgery, service-mode warnings, page-cost tables
- `scripts/print_rescue.py` — diagnose / spooler / discover / economics

For home/SOHO printers. No affiliation with any vendor.
