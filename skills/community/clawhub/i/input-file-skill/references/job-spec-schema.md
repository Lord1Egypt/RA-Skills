# Job Spec Schema

The skill should normalize user requests into the following JSON structure:

```json
{
  "task_type": "geometry_optimization",
  "system_type": "molecule",
  "structure_file": "uploaded.xyz",
  "periodicity": "NONE",
  "charge": 0,
  "multiplicity": 1,
  "priority": "balanced",
  "hardware": {
    "type": "cpu",
    "cores": null,
    "memory_gb": null
  },
  "notes": [],
  "defaults_applied": []
}