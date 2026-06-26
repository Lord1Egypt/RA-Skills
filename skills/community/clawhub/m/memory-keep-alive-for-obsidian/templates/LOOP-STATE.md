# Loop State

state: disarmed
last_changed: YYYY-MM-DD
start_trigger: /loop-start
stop_trigger: /loop-stop

Notes:
- When disarmed, the workflow jobs should pause or no-op.
- When armed, the workflow jobs may resume normal monitoring and recovery.
