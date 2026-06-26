---
name: mac-battery
version: 1.0.0
description: Check Mac laptop battery status including percentage, charging state, and time remaining. Use when user asks about battery level, power status, or how much time left until fully charged/discharged on a Mac laptop.
---

# Mac Battery Status

Query Mac laptop battery information using the `pmset` command.

## Command

```bash
pmset -g batt | grep -E "([0-9]+%)"
```

## Output Format

Returns battery percentage, charging state, and time remaining:
- **Percentage**: e.g., "79%"
- **Charging state**: "charging", "discharging", or "charged"
- **Time remaining**: e.g., "0:47 remaining" (for charging) or "2:30 remaining" (for discharging)

## Example Response

```
🔋 79%; charging; 0:47 remaining
```

Respond to user with the battery info in a friendly format with emoji.
