# Sample macmon JSON fields

Example fields commonly seen from `macmon pipe -s 1`:

- `temp.cpu_temp_avg`
- `temp.gpu_temp_avg`
- `pcpu_usage`: `[mhz, fraction]`
- `ecpu_usage`: `[mhz, fraction]`
- `gpu_usage`: `[mhz, fraction]`
- `memory.ram_total`
- `memory.ram_usage`
- `memory.swap_total`
- `memory.swap_usage`
- `sys_power`
- `cpu_power`
- `gpu_power`
- `timestamp`

Fractions in usage pairs are in the `0..1` range and should usually be shown as percentages.
