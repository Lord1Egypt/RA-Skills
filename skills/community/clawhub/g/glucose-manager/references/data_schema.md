# Data Schema

## Glucose Readings Data Structure

### Main Data File Location
```
~/.workbuddy/data/glucose_readings.json
```

### JSON Structure

```json
{
  "readings": [
    {
      "id": "20260324080000001",
      "timestamp": "2026-03-24T08:00:00",
      "value": 7.2,
      "unit": "mmol/L",
      "meal_context": "fasting",
      "notes": "Before breakfast",
      "tags": ["morning", "routine"]
    }
  ],
  "metadata": {
    "created": "2026-01-01T00:00:00",
    "last_updated": "2026-03-24T08:00:00",
    "version": "1.0"
  }
}
```

### Field Specifications

#### Reading Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Auto | Unique identifier (timestamp-based) |
| `timestamp` | string | Yes | ISO 8601 format datetime |
| `value` | number | Yes | Glucose value |
| `unit` | string | Yes | "mmol/L" or "mg/dL" |
| `meal_context` | string | No | Meal context (see below) |
| `notes` | string | No | User notes |
| `tags` | array | No | Array of tag strings |

#### Meal Context Values
- `fasting`: No food for 8+ hours
- `pre-meal`: Before a meal
- `post-meal`: After a meal (typically 1-2 hours)
- `bedtime`: Before sleep
- `random`: No specific context

#### Metadata Object

| Field | Type | Description |
|-------|------|-------------|
| `created` | string | Creation timestamp (ISO 8601) |
| `last_updated` | string | Last update timestamp (ISO 8601) |
| `version` | string | Schema version |

## Import File Formats

### CSV Format

```csv
date,time,value,unit,meal_context,notes
2026-03-24,08:00,7.2,mmol/L,fasting,Before breakfast
2026-03-24,10:30,8.5,mmol/L,post-meal,After breakfast
```

**Supported columns**:
- `date` (required): Date in YYYY-MM-DD format
- `time` (optional): Time in HH:MM or HH:MM:SS format
- `value` (required): Glucose value as number
- `unit` (optional): "mmol/L" or "mg/dL"
- `meal_context` (optional): Meal context
- `notes` (optional): Notes text

**Alternative column names**:
- Date: `date`, `Date`, `datetime`, `timestamp`
- Time: `time`, `Time`
- Value: `value`, `Value`, `glucose`, `reading`
- Unit: `unit`, `Unit`, `units`
- Meal Context: `meal_context`, `context`, `meal`
- Notes: `notes`, `Notes`, `comment`, `remarks`

### Excel Format

Same columns as CSV, in Excel format (.xlsx or .xls).

**Sheet handling**:
- If no sheet specified, reads first sheet
- Specify sheet name with `--sheet` parameter

## Backup Structure

### Backup Location
```
~/.workbuddy/data/backups/
```

### Backup File Naming
```
glucose_readings_YYYYMMDD_HHMMSS.json
```

### Backup Policy
- Automatic backup before each modification
- Keep last 10 backups
- Manual backup possible via data manager

## Data Validation Rules

### Required Fields
- `value`: Must be a positive number
- `unit`: Must be "mmol/L" or "mg/dL"

### Value Ranges
- **mmol/L**: 1.0 - 50.0 (reasonable physiological range)
- **mg/dL**: 18 - 900 (converted range)

**Warning thresholds**:
- **Hypoglycemia**: < 4.0 mmol/L (< 72 mg/dL)
- **Hyperglycemia**: > 13.9 mmol/L (> 250 mg/dL)

### Timestamp Validation
- Must be valid ISO 8601 format
- Cannot be in the future
- Cannot be before year 2000

### Unit Handling
- Values are stored in original unit
- Conversions done on-the-fly when needed
- Conversion factor: 1 mmol/L = 18.018 mg/dL

## Data Export Formats

### JSON Export
Full data structure with all fields.

### CSV Export
Flattened structure for spreadsheet compatibility.

### HTML Report
Styled report with charts and statistics.

## Security and Privacy

### Data Storage
- All data stored locally on user's device
- No cloud storage or transmission
- User maintains full control

### File Permissions
- User-only read/write access
- Protected by operating system permissions

### Sensitive Information
- User notes may contain personal information
- Data is not encrypted (future enhancement)
- Recommend secure device practices

## Performance Considerations

### File Size
- Typical reading size: ~150 bytes
- 1000 readings ≈ 150 KB
- 10000 readings ≈ 1.5 MB

### Optimization
- Data sorted by timestamp on save
- Efficient querying with date filters
- Statistics cached where possible

## Future Enhancements

Potential future schema additions:

1. **Medication tracking**
   ```json
   "medications": [
     {
       "name": "Metformin",
       "dose": "500mg",
       "time": "2026-03-24T08:00:00"
     }
   ]
   ```

2. **Activity tracking**
   ```json
   "activities": [
     {
       "type": "walking",
       "duration_minutes": 30,
       "time": "2026-03-24T10:00:00"
     }
   ]
   ```

3. **Food logging**
   ```json
   "meals": [
     {
       "time": "2026-03-24T07:30:00",
       "carbs_grams": 45,
       "description": "Breakfast"
     }
   ]
   ```

4. **Health indicators**
   ```json
   "health_metrics": [
     {
       "type": "weight",
       "value": 70,
       "unit": "kg",
       "time": "2026-03-24T07:00:00"
     }
   ]
   ```

## Version History

### Version 1.0 (Current)
- Initial schema
- Basic glucose readings
- Manual and file import
- Statistics and analysis
