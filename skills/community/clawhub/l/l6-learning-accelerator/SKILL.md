# l6-learning-accelerator - Learning Accelerator Skill

## Description
A learning acceleration skill that implements 2-signal fusion retrieval (Vector + Time) with temporal routing for intelligent memory access. Provides progress tracking and time-aware context retrieval for enhanced learning workflows.

## Triggers
- `learning accelerator`
- `accelerated learning`
- `time-aware retrieval`
- `memory fusion`
- `l6`
- `study accelerator`
- `learning boost`

## Capabilities

### 2-Signal Fusion Retrieval
Combines vector similarity search with temporal relevance scoring to retrieve the most contextually appropriate memories and notes.

### Temporal Routing
- `detect_temporal()` - Identifies temporal intent in queries
- `get_date_range()` - Extracts date ranges from natural language

### Progress Tracking
- Track learning sessions
- Monitor progress over time
- Generate progress reports

## Files

- `SKILL.md` - This metadata file
- `src/retrieval.js` - 2-signal fusion retrieval implementation
- `src/temporal.js` - Time routing functions
- `src/progress.js` - Progress tracking module
- `test/basic.test.js` - Basic test suite

## Usage

```javascript
// Import the skill modules
const { retrieve } = require('./src/retrieval');
const { detect_temporal, get_date_range } = require('./src/temporal');
const { track_progress, get_report } = require('./src/progress');

// Example: Time-aware retrieval
const results = await retrieve(query, {
  vector_weight: 0.6,
  time_weight: 0.4,
  date_range: get_date_range('last week')
});

// Example: Progress tracking
track_progress('session', { topic: 'JavaScript', duration: 45 });
const report = get_report('weekly');
```

## Configuration

Add to your workspace config:

```json
{
  "l6": {
    "vector_weight": 0.6,
    "time_weight": 0.4,
    "decay_factor": 0.95,
    "memory_path": "./memory"
  }
}
```

## Dependencies

- None (pure JavaScript implementation)

## Version
1.0.0

## Author
OpenClaw Skills
