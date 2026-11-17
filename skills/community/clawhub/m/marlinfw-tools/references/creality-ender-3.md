# Creality Ender 3 family safety

## Treat each machine as a distinct configuration

"Ender 3" is a product family, not one hardware or firmware target. Before a
command beyond inspection, identify all of the following:

1. Exact printer model and any installed modifications, such as a probe,
   replacement control board, all-metal hotend, or alternate display.
2. Control-board marking from the physical board. Do not infer it from the
   printer name or an online listing.
3. Display type and, for firmware work, its own update procedure.
4. Firmware identity and capabilities from `M115`. Save the complete response.
5. A fresh `M503` report. Its absence is a capability finding, not a reason to
   force a setting write.

The official Marlin example repository contains separate Creality configurations
for multiple Ender 3 variants and boards. It also notes different STM32F1 and
STM32F4 firmware lines for the Ender 3 S1 family. Never transfer a firmware
binary, config, display file, probe offset, thermistor setting, or motion value
between variants merely because both have "Ender 3" in the name.

## Safe sequence for a setting change

1. Confirm there is no active or queued print, the nozzle is clear, and the
   operator is present at the machine.
2. Record `M115`, `M503`, `M105`, `M114`, and `M119` through `inspect`.
3. Name one setting, the measured evidence, the exact G-code, and its expected
   physical effect.
4. Ask for current-turn approval. Apply only the audited command with
   `--apply --confirm-risk`.
5. Inspect again. Confirm that the expected active setting changed and that no
   unexpected state did.
6. Only then ask separately whether the verified change should survive reboot.
   If approved, use `--save --confirm-persist` and retain the before and after
   reports.

## Commands this tool does not send

| Family | Why it is excluded |
| --- | --- |
| `G0`, `G1`, `G28`, `G29`, `G30`, `G38` | Movement, homing, and probing can crash an unhomed or modified machine into the frame, bed, nozzle, or probe. |
| `M104`, `M109`, `M140`, `M190`, `M303` | Heating or PID tuning needs a printer-specific thermal procedure and physical supervision. |
| `M211`, `M420`, `M421`, `M428` | Endstop and leveling state can defeat travel protection or cause nozzle and bed collisions. |
| `M42` | Direct pin control can drive unknown hardware pins and bypass normal firmware ownership. |
| `M112`, `M410` | Emergency control belongs to an attentive operator or purpose-built control path, not an automated agent. |
| `M501`, `M502`, `M500` | EEPROM load, reset, and save change reboot behavior. The writer uses `M500` only behind its verified persistence gate. |
| `M997` | Can restart into an in-application firmware update. It is unsupported on some platforms and must never be automated. |

## Firmware work is outside this tool

Wrong board, display, bootloader, or configuration firmware can leave an Ender
3 unable to boot or unsafe to operate. This repository does not flash firmware,
copy firmware files, invoke `M997`, or automate a recovery procedure. For a
firmware task, stop after collecting the identity evidence above, then use the
exact official procedure and image that match the physical board, display, and
printer variant. Preserve the known-good firmware and configuration first.

## Sources

- [Marlin example configurations](https://github.com/MarlinFirmware/Configurations)
- [Marlin EEPROM feature](https://marlinfw.org/docs/features/eeprom.html)
- [Marlin M503 report](https://marlinfw.org/docs/gcode/M503.html)
- [Marlin endstop safety](https://marlinfw.org/docs/hardware/endstops.html)
- [Marlin M42 pin control](https://marlinfw.org/docs/gcode/M042.html)
- [Marlin M997 firmware update](https://marlinfw.org/docs/gcode/M997.html)
