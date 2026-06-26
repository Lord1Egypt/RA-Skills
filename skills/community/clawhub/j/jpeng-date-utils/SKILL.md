---
name: date-utils
description: Provides date and time manipulation operations for working with dates. Use when you need to format, parse, compare, or manipulate dates and times.
---

# Date Utils

Provides date and time manipulation operations.

## Usage

```javascript
const date = require('./skills/date-utils');

// Formatting
const formatted = date.formatDate(new Date(), 'YYYY-MM-DD HH:mm:ss');

// Parsing
const parsed = date.parseDate('2024-03-15', 'YYYY-MM-DD');

// Differences
const diff = date.diffDays(date1, date2);

// Add/Subtract
const tomorrow = date.addDays(new Date(), 1);
const lastWeek = date.subtractDays(new Date(), 7);
```

## Features

- Date formatting with patterns
- Date parsing from strings
- Date arithmetic (add/subtract)
- Date comparisons
- Timezone handling
- Calendar generation
- Relative time (ago, fromNow)
- Duration calculations
