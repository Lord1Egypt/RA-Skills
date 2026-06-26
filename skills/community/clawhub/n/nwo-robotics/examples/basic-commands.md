# Basic Commands Examples

## Robot Status

```
Input:  Check robot status
Output: Robot Status:
        • robot_001: online, idle
        • robot_002: online, executing task
        • robot_arm_01: offline
```

## Emergency Stop

```
Input:  Stop all robots
        Emergency halt
        Stop everything now
Output: ⚠️ Emergency stop activated. All robots halted.
```

## Movement Commands

```
Input:  Move robot_001 to position x:10, y:20
        Navigate robot_2 to coordinates 50, 100
        Go to x:0 y:0
Output: Command sent to robot_001. Status: pending
```

## Vision Tasks

```
Input:  Scan for objects
        Find the red box
        Detect all people in the area
Output: Detected 3 objects:
        • box (95% confidence) at [120, 340]
        • person (89% confidence) at [200, 150]
        • chair (76% confidence) at [400, 300]
```

## IoT Sensors

```
Input:  What's the temperature in the lab?
        Check warehouse humidity
        Sensor status
Output: Sensor Readings:
        • Lab 3: 23.5°C
        • Lab 4: 24.1°C
        • Warehouse: 45% humidity
```

## Patrol Mode

```
Input:  Patrol mode on
        Start patrolling
        Stop patrol
Output: Patrol mode activated.
        (or)
        Patrol mode deactivated.
```

## Complex Tasks

```
Input:  Pick up the box and move it to the table
        Follow the path to the exit
        Scan warehouse and report findings
Output: Task submitted. Processing...
```

## Error Handling

```
Input:  Check robot status (when API key is missing)
Output: Error checking robot status: NWO_API_KEY environment variable is required. Get your API key at https://nwo.capital/webapp/api-key.php

Input:  Any command (when rate limited)
Output: API rate limit exceeded. Please upgrade your plan at https://nwo.capital/webapp/api-key.php
```
