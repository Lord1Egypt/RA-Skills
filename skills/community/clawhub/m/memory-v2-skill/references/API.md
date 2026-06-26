# Memory V2 API Reference

Complete API documentation for the Memory V2 system.

## Table of Contents

- [Initialization](#initialization)
- [Priority Module](#priority-module)
- [Learning Module](#learning-module)
- [Decision Module](#decision-module)
- [Evolution Module](#evolution-module)
- [Dashboard](#dashboard)
- [Version Management](#version-management)

---

## Initialization

```javascript
const MemoryAPI = require('./api');

// Create instance
const api = new MemoryAPI('./memory-v2.db');

// Initialize database
await api.init();

// Close when done
await api.close();
```

---

## Priority Module

### analyzePriority(message)
Analyze a message and return priority assessment.

**Parameters:**
- `message` (string): The message to analyze

**Returns:**
```javascript
{
  priority_level: 'critical' | 'high' | 'medium' | 'low',
  reasoning: string,
  category: string
}
```

### storePriority(msgId, convId, analysis)
Store priority analysis in database.

**Parameters:**
- `msgId` (string): Message ID
- `convId` (string): Conversation ID
- `analysis` (object): Result from analyzePriority

**Returns:** `Promise<{id: number}>`

### getHighPriority(limit = 10)
Get recent high/critical priority items.

**Parameters:**
- `limit` (number): Maximum results

**Returns:** `Promise<Array>`

### getPriorityStats()
Get priority distribution statistics.

**Returns:**
```javascript
{
  critical: number,
  high: number,
  medium: number,
  low: number,
  total: number
}
```

---

## Learning Module

### startLearning(msgId, convId, message)
Start tracking a new learning topic.

**Parameters:**
- `msgId` (string): Message ID
- `convId` (string): Conversation ID  
- `message` (string): Message describing the learning topic

**Returns:**
```javascript
{
  id: number,
  topic: string,
  status: 'active',
  progress: 0
}
```

### updateLearningProgress(learningId, updates)
Update learning progress.

**Parameters:**
- `learningId` (number): Learning record ID
- `updates` (object):
  - `progress` (number): 0-100
  - `status` (string): 'active' | 'paused' | 'completed' | 'abandoned'

### addMilestone(learningId, milestone)
Add a milestone to a learning record.

**Parameters:**
- `learningId` (number): Learning record ID
- `milestone` (object):
  - `title` (string): Milestone title
  - `description` (string): Optional description

### getActiveLearning(limit = 5)
Get currently active learning topics.

**Parameters:**
- `limit` (number): Maximum results

**Returns:** `Promise<Array>`

### getLearningStats()
Get learning statistics.

**Returns:**
```javascript
{
  active: number,
  completed: number,
  total: number,
  avg_progress: number
}
```

---

## Decision Module

### recordDecision(msgId, convId, decisionData)
Record a new decision.

**Parameters:**
- `msgId` (string): Message ID
- `convId` (string): Conversation ID
- `decisionData` (object):
  - `summary` (string): Decision summary (required)
  - `context` (string): Decision context
  - `expectedOutcome` (string): Expected result
  - `reviewDate` (string): ISO date for review

**Returns:** `Promise<{id: number}>`

### updateDecisionOutcome(decisionId, outcome)
Update the actual outcome of a decision.

**Parameters:**
- `decisionId` (number): Decision ID
- `outcome` (object):
  - `actualOutcome` (string): What actually happened
  - `status` (string): 'implemented' | 'validated' | 'rejected'

### getPendingDecisions()
Get decisions pending review or implementation.

**Returns:** `Promise<Array>`

### scheduleReview(decisionId, reviewDate)
Schedule a review for a decision.

**Parameters:**
- `decisionId` (number): Decision ID
- `reviewDate` (string): ISO date string

---

## Evolution Module

### recordSkillUsage(skillName, category, result)
Record skill usage.

**Parameters:**
- `skillName` (string): Name of the skill
- `category` (string): Skill category
- `result` (string): 'success' | 'failure'

### getTopSkills(limit = 10)
Get most frequently used skills.

**Parameters:**
- `limit` (number): Maximum results

**Returns:** `Promise<Array>`

### getSkillStats(skillName)
Get statistics for a specific skill.

**Parameters:**
- `skillName` (string): Skill name

**Returns:**
```javascript
{
  skill_name: string,
  category: string,
  usage_count: number,
  success_count: number,
  success_rate: number,
  last_used_at: string
}
```

---

## Dashboard

### getDashboard()
Get unified dashboard of all memory data.

**Returns:**
```javascript
{
  summary: {
    total_priorities: number,
    total_learning: number,
    total_decisions: number,
    total_skills: number
  },
  recent: {
    priorities: Array,
    learning: Array,
    decisions: Array
  },
  stats: {
    priorities: Object,
    learning: Object,
    skills: Array
  }
}
```

---

## Version Management

### createBackup(label)
Create a database backup.

**Parameters:**
- `label` (string): Optional label for the backup

**Returns:** `Promise<{backupPath: string}>`

### listBackups()
List all available backups.

**Returns:** `Promise<Array>`

### restoreBackup(backupPath)
Restore from a backup.

**Parameters:**
- `backupPath` (string): Path to backup file

**Returns:** `Promise<boolean>`

### cleanupBackups(keepCount = 10)
Clean up old backups, keeping only the specified number.

**Parameters:**
- `keepCount` (number): Number of backups to keep

---

## Database Views

The following SQL views are available for direct queries:

### v_pending_decisions
Decisions that need attention (pending, overdue, or due soon).

### v_skill_summary
Skill usage statistics with success rates.

### v_weekly_learning_report
Learning activity summary for the past week.

### v_high_priority
Combined view of high priority items and pending decisions.

---

## Error Handling

All API methods return Promises and may throw:

```javascript
try {
  const result = await api.storePriority(msgId, convId, analysis);
} catch (err) {
  console.error('API Error:', err.message);
}
```

Common errors:
- Database not initialized
- Invalid parameters
- Constraint violations
- File system errors (backups)

---

## Examples

### Complete Workflow

```javascript
const MemoryAPI = require('./api');
const api = new MemoryAPI('./memory-v2.db');

async function example() {
  await api.init();
  
  // Record a decision
  const decision = await api.recordDecision('msg-123', 'conv-456', {
    summary: 'Use SQLite for local storage',
    context: 'Need embedded database for skill',
    expectedOutcome: 'Simpler deployment'
  });
  
  // Start learning
  const learning = await api.startLearning('msg-124', 'conv-456', 
    'Learning SQLite advanced features'
  );
  
  // Update progress
  await api.updateLearningProgress(learning.id, { progress: 50 });
  
  // Record skill usage
  await api.recordSkillUsage('memory-v2', 'storage', 'success');
  
  // Get dashboard
  const dashboard = await api.getDashboard();
  console.log(dashboard);
  
  await api.close();
}

example();
```

---

## License

MIT
