# Marlin setting writes

`send` accepts only one audited calibration-setting line. It requires
`--apply --confirm-risk` after direct user approval. Its optional `--save`
requires `--confirm-persist` and adds `M500` only after that command receives
Marlin's `ok` response.

Common settings depend on the firmware build:

| Command family | Typical purpose |
| --- | --- |
| `M92` | Axis steps per unit. |
| `M201`, `M203`, `M204`, `M205` | Motion acceleration, feedrate, and advanced motion limits. |
| `M206` | Home offsets. |
| `M301`, `M304` | Hotend or bed PID values. |

Always inspect first, make one change at a time, inspect again, and only then
persist. `M500` stores settings in EEPROM when that firmware feature is
enabled. `M503` reports active RAM settings, not necessarily the bytes stored
in EEPROM. A failed `M503` means persistence must stop until the firmware
capability is understood.

The generic writer blocks raw pin control, emergency and quick stops, EEPROM
load and reset, firmware update, motion, homing, heating, leveling, and every
other non-audited G-code family. Those operations need a separate reviewed tool
and a printer-specific procedure.
