---
name: "opensprinkler"
description: "Monitor and control an OpenSprinkler irrigation controller. Allows checking status, running manual stations/programs, toggling rain delays, viewing logs, pausing the queue, and managing overall system operation."
env:
  OPENSPRINKLER_IP_ADDRESS:
  OPENSPRINKLER_PASSWORD:
---
# OpenSprinkler Local Controller

This skill grants access to an OpenSprinkler irrigation controller via its local HTTP API. 

### Guidelines for the AI
* **Station IDs & Program IDs:** You will exclusively use 1-based Station IDs (1-72) and Program IDs when interacting with the user and the tools. 
* **Special Program IDs in Logs:** When reading logs, note that Program ID 255 indicates a manual station run, and Program ID 254 indicates a manual run-once sequence.
* **Naming:** Try to respond using human-readable Station Names and Program Names when they are available or provided by the user. Fall back to numerical IDs if names are missing or if it makes the response clearer.
* **Duration:** When turning on a station manually, always ask the user for a duration if they do not provide one. Do not guess water times.
* **System Diagnostics & Weather:** * If the user asks about the physical "Rain Sensor" or other hardware sensors, use `get_status` to check `rain_sensor_active`.
  * If the user asks about the "Watering Level" (weather adjustment percentage), whether weather adjustments are currently active, firmware versions, or sunrise/sunset times, you must use the `get_options` tool.
