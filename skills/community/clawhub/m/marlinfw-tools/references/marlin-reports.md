# Marlin inspection reports

| Command | Purpose |
| --- | --- |
| `M115` | Firmware identity and advertised capabilities. |
| `M503` | Current in-memory settings, including values restored from EEPROM. |
| `M105` | Current and target heater temperatures. |
| `M114` | Current logical and machine position. |
| `M119` | Endstop states. |

Availability depends on the firmware build. Marlin documents `M115` capability
reporting and `M503` settings reporting in its G-code reference. A report is a
snapshot, not proof that a hardware sensor or endstop is calibrated.
