# Internal Data Format Definition

> **Late Brake Project Documentation**
>
> This document defines the unified JSON data structure specification for Late Brake internal usage.
> All data import modules must output JSON conforming to this specification, and downstream analysis modules depend on this unified format for processing.

This document defines the unified JSON data structure specification for Late Brake internal usage.

## 1. Data Point Structure

Each data point contains all information for a specific sampling moment on the track:

```json
{
  "timestamp": float,    // Relative time (seconds), counted from the start of recording
  "latitude": float,     // Latitude (WGS84)
  "longitude": float,    // Longitude (WGS84)
  "altitude": float,     // Altitude (meters), optional field
  "speed": float,        // Instantaneous speed (km/h)
  "distance": float,     // Cumulative distance (meters), counted from the start of recording
  "g_force_x": float,    // Lateral G-force (left-positive, right-negative), optional field
  "g_force_y": float,    // Longitudinal G-force (positive = acceleration, negative = braking), optional field
  "g_force_z": float,    // Vertical G-force, optional field
  "steering_angle": float, // Steering wheel angle (degrees), optional field, negative = left, positive = right
  "throttle_position": float, // Throttle position (0-100%), optional field
  "brake_pressure": float,    // Brake pressure (0-100%), optional field
  "rpm": int,                 // Engine RPM (RPM), optional field
  "gear": int,                // Current gear, 0 = neutral, 1-... = gear number, optional field
}
```

**Notes:**
- Required fields: `timestamp`, `latitude`, `longitude`, `speed`, `distance`
- Optional fields: Depends on what the data source provides. If the data source doesn't have the data, leave it empty or omit the field
- G-force explanation: Following industry standards, lateral G-force reflects centrifugal force, longitudinal G-force reflects acceleration/braking force
- Unit consistency: All units use metric system, speed in km/h, angle in degrees, percentage in 0-100%

## 2. Lap Data Structure

```json
{
  "id": string,              // Lap ID (e.g. "file1.Lap1")
  "source_file": string,     // Source file path
  "lap_number": int,         // Lap number
  "total_time": float,       // Total lap time (seconds)
  "start_time": float,       // Lap start time (seconds, relative to the start of the entire recording)
  "end_time": float,         // Lap end time (seconds, relative to the start of the entire recording)
  "start_distance": float,   // Start cumulative distance (meters, relative to the start of the entire recording)
  "end_distance": float,     // End cumulative distance (meters, relative to the start of the entire recording)
  "is_complete": bool,       // Is this a complete lap. true = completed a full lap crossing start/finish, false = started mid-track / ended mid-track, incomplete
  "lap_distance": float,     // Actual lap driving distance (meters) = end_distance - start_distance
  "points": array,           // Array of data points, contains all sampling points in the lap
}
```

**Field Description:**

- `start_time` / `end_time`: Records the absolute time position of the lap within the entire data recording, facilitates subsequent processing and sector analysis
- `is_complete`: Marks whether the lap is complete. If the recording started when the car was already on track, or ended before the lap was completed, it's considered incomplete
- `start_distance` / `end_distance`: **Keep this field** for the following reasons:
  1. Calculate actual lap distance `lap_distance = end_distance - start_distance`, verify track length
  2. Locate the lap position within the entire data recording, facilitates cutting and extraction
  3. When processing consecutive multi-lap recordings, quickly find lap start/end points by distance
  4. Compare distances between different laps helps discover differences in racing line length
- `lap_distance`: New computed field directly gives lap driving distance for convenience

## 3. Floating Point Precision Convention

In JSON output, floating point numbers retain decimal places according to the following rules to reduce file size and improve readability without affecting analysis accuracy:

| Field Category | Decimal Places | Example |
|----------------|----------------|---------|
| Time related (`timestamp`, `total_time`, `start_time`, `end_time`) | 4 | `68.9500 |
| Distance related (`distance`, `lap_distance`, `start_distance`, `end_distance`) | 2 | `1985.60 |
| Coordinates (`latitude`, `longitude`) | 7 | `31.0794723 |
| Speed (`speed`) | 2 | `68.90` |
| G-forces / Controls (`g_force_x/y/z`, `steering_angle`, `throttle_position`, `brake_pressure`) | 3 | `0.123` |
| Other floating point fields | 3 | — |
