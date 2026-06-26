# Pi GPIO Control Skill
This skill allows OpenClaw agents to control GPIO pins on a Raspberry Pi via RPC.
## Purpose
Expose Raspberry Pi GPIO actions as local-like functions to the agent, while execution happens remotely
on the Pi.
## Actions
- gpio_on(pin): Set GPIO pin HIGH
- gpio_off(pin): Set GPIO pin LOW
## Requirements
- Raspberry Pi running pi-agent RPC server
- HTTP endpoint available at http://pi.local:9000/run
## Security
Only predefined GPIO actions are allowed on the Pi side.