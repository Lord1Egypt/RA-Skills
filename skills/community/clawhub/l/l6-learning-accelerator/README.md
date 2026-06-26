# l6-learning-accelerator

A learning acceleration skill that implements **2-signal fusion retrieval** (Vector + Time) with temporal routing for intelligent memory access.

## Features

- 🔍 **2-Signal Fusion Retrieval**: Combines vector similarity with temporal relevance
- ⏰ **Temporal Routing**: Natural language date parsing and range extraction
- 📊 **Progress Tracking**: Session tracking, milestones, and reports
- 🧪 **Tested**: 29 comprehensive tests covering all modules

## Installation

This skill is located at:
```
D:\OpenClaw\workspace\skills\l6-learning-accelerator\
```

## Usage

### Basic Import

```javascript
const l6 = require('./index.js');

// Or import specific modules
const { retrieve } = require('./src/retrieval');
const { detect_temporal, get_date_range } = require('./src/temporal');
const { track_progress, get_report } = require('./src/progress');
```

### 2-Signal Fusion Retrieval

```javascript
const items = [
  { 
    id: 1, 
    vector: [0.8, 0.2, 0.1], 
    date: new Date().toISOString(),
    content: 'Recent note'
  },
  { 
    id: 2, 
    vector: [0.7, 0.3, 0.2], 
    date: new Date(Date.now() - 86400000).toISOString(),
    content: 'Yesterday note'
  }
];

const results = l6.retrieve('query', {
  queryVector: [0.8, 0.2, 0.1],
  items,
  weights: { vector: 0.6, time: 0.4 },
  topK: 5
});

console.log(results);
// Returns items ranked by fused score
```

### Temporal Routing

```javascript
// Detect temporal intent
const detection = l6.detect_temporal('What did I learn last week?');
console.log(detection);
// { hasTemporal: true, intent: 'relative', expressions: [...] }

// Get date range from natural language
const range = l6.get_date_range('last week');
console.log(range);
// { start: Date, end: Date }

// Supported expressions:
// - 'today', 'yesterday', 'tomorrow'
// - 'last week', 'this week', 'next week'
// - 'last month', 'this month', 'next month'
// - 'past 7 days', 'last 30 days'
// - '2024-03-15' (ISO date)
```

### Progress Tracking

```javascript
// Track a learning session
l6.track_progress('study', {
  topic: 'JavaScript',
  duration: 45,  // minutes
  notes: 'Learned about closures'
});

// Get progress report
const report = l6.get_report('weekly');
console.log(report.summary);
// { totalSessions: 5, totalTimeMinutes: 180, avgSessionTime: 36 }

// Set milestones
l6.set_milestone('Week Warrior', { totalSessions: 7 });

// Check streak
const streak = l6.calculateStreak();
console.log(`${streak} day streak!`);
```

## API Reference

### Retrieval Module

| Function | Description |
|----------|-------------|
| `retrieve(query, options)` | Search items with 2-signal fusion |
| `batchRetrieve(queries, options)` | Batch search multiple queries |
| `cosineSimilarity(vec1, vec2)` | Calculate vector similarity |
| `calculateTemporalScore(date, refDate, decay)` | Calculate temporal relevance |
| `fuseScores(vector, temporal, weights)` | Combine scores with weights |
| `getRetrievalStats(results)` | Get retrieval statistics |

### Temporal Module

| Function | Description |
|----------|-------------|
| `detect_temporal(query)` | Detect temporal intent in query |
| `get_date_range(expression, refDate)` | Parse date range from text |
| `getRelativeTime(date, refDate)` | Get human-readable time description |

### Progress Module

| Function | Description |
|----------|-------------|
| `track_progress(type, data)` | Record a learning session |
| `get_report(period)` | Generate progress report |
| `set_milestone(name, criteria)` | Create achievement milestone |
| `calculateStreak()` | Get current day streak |
| `export_to_file(path)` | Export data to JSON |
| `import_from_file(path)` | Import data from JSON |

## Configuration

```javascript
const options = {
  weights: { vector: 0.6, time: 0.4 },  // Score weights
  decayFactor: 0.95,                     // Temporal decay
  topK: 10                               // Max results
};
```

## Running Tests

```bash
cd D:\OpenClaw\workspace\skills\l6-learning-accelerator
node test/basic.test.js
```

## File Structure

```
l6-learning-accelerator/
├── SKILL.md              # Skill metadata
├── index.js              # Main entry point
├── src/
│   ├── retrieval.js      # 2-signal fusion retrieval
│   ├── temporal.js       # Time routing functions
│   └── progress.js       # Progress tracking
├── test/
│   └── basic.test.js     # Test suite
└── README.md             # This file
```

## License

MIT - OpenClaw Skills
