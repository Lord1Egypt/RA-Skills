# Meeting Efficiency Pro - API Documentation

## Overview

Meeting Efficiency Pro provides programmatic access to its meeting analysis capabilities through a JavaScript API. This document describes the available classes, methods, and usage patterns.

## Installation

```javascript
// Import the skill modules
const Calendar = require('meeting-efficiency-pro/lib/calendar');
const Analyzer = require('meeting-efficiency-pro/lib/analyzer');
const Reporter = require('meeting-efficiency-pro/lib/reporter');
```

## Configuration

### Basic Configuration
```javascript
const config = {
  ai_provider: 'openai',           // 'openai', 'grok', or 'none'
  ai_api_key: 'your-api-key',      // Optional, for AI features
  calendar_type: 'google',         // 'google', 'outlook', 'ical', or 'none'
  efficiency_threshold: 70,        // 0-100
  auto_briefing: true,
  briefing_time: '08:00'
};
```

## Calendar Class

### Constructor
```javascript
const calendar = new Calendar(config);
```

### Methods

#### `initialize()`
Initializes the calendar connection based on configuration.

```javascript
await calendar.initialize();
// Returns: Promise<boolean>
```

#### `getTodaysMeetings()`
Retrieves meetings scheduled for today.

```javascript
const meetings = await calendar.getTodaysMeetings();
// Returns: Promise<Array<Meeting>>
```

#### `getWeeklyMeetings()`
Retrieves meetings from the past week.

```javascript
const meetings = await calendar.getWeeklyMeetings();
// Returns: Promise<Array<Meeting>>
```

#### `getMeetingStats(timeframe)`
Gets statistics about meetings.

```javascript
const stats = await calendar.getMeetingStats('week');
// Returns: Promise<MeetingStats>
```

#### `testConnection()`
Tests the calendar connection.

```javascript
const result = await calendar.testConnection();
// Returns: Promise<ConnectionTestResult>
```

### Data Types

#### Meeting Object
```typescript
interface Meeting {
  id: string;
  title: string;
  description: string;
  startTime: string;    // Format: 'HH:MM'
  endTime: string;      // Format: 'HH:MM'
  duration: number;     // Minutes
  attendees: number;
  location: string;
  recurring: boolean;
  type?: string;        // 'standup', 'review', 'planning', etc.
}
```

#### MeetingStats
```typescript
interface MeetingStats {
  totalMeetings: number;
  totalDuration: number;    // Minutes
  averageDuration: number;
  averageAttendees: number;
  estimatedCost: number;    // USD
  byType: Record<string, TypeStats>;
  byDay: Record<string, DayStats>;
}

interface TypeStats {
  count: number;
  totalDuration: number;
  averageEfficiency?: number;
}

interface DayStats {
  count: number;
  totalDuration: number;
}
```

## Analyzer Class

### Constructor
```javascript
const analyzer = new Analyzer(config);
```

### Methods

#### `analyzeMeeting(meeting)`
Analyzes a meeting and provides efficiency score and suggestions.

```javascript
const analysis = await analyzer.analyzeMeeting(meeting);
// Returns: Promise<MeetingAnalysis>
```

#### `processMeetingNotes(notes)`
Processes meeting notes to extract key information.

```javascript
const result = await analyzer.processMeetingNotes(notesText);
// Returns: Promise<NotesAnalysis>
```

#### `generateDailySummary(meetings)`
Generates a summary of daily meetings.

```javascript
const summary = await analyzer.generateDailySummary(meetings);
// Returns: Promise<DailySummary>
```

### Data Types

#### MeetingAnalysis
```typescript
interface MeetingAnalysis {
  meetingId: string;
  title: string;
  efficiencyScore: number;      // 0-100
  meetingType: string;
  optimalDuration: number;      // Minutes
  suggestions: string[];
  recommendations: string[];
  riskFactors: string[];
  aiEnhanced?: boolean;
  sentiment?: 'positive' | 'negative' | 'neutral';
  complexity?: 'low' | 'medium' | 'high';
  preparationScore?: number;    // 0-100
}
```

#### NotesAnalysis
```typescript
interface NotesAnalysis {
  summary: string[];
  actionItems: ActionItem[];
  decisions: string[];
  questions: string[];
  efficiencyScore: number;      // 0-100
  participants: string[];
}

interface ActionItem {
  text: string;
  owner: string;
  dueDate: string;
  priority: 'High' | 'Medium' | 'Low';
}
```

#### DailySummary
```typescript
interface DailySummary {
  totalMeetings: number;
  totalMinutes: number;
  averageEfficiency: number;    // 0-100
  potentialSavings: number;     // Minutes
  recommendations: string[];
}
```

## Reporter Class

### Constructor
```javascript
const reporter = new Reporter(config);
```

### Initialization
```javascript
reporter.setAnalyzer(analyzer);  // Required before use
```

### Methods

#### `generateWeeklyReport(meetings)`
Generates a comprehensive weekly report.

```javascript
const report = await reporter.generateWeeklyReport(meetings);
// Returns: Promise<WeeklyReport>
```

#### `generateMeetingSummary(meeting, analysis)`
Generates a formatted summary for a single meeting.

```javascript
const summary = reporter.generateMeetingSummary(meeting, analysis);
// Returns: MeetingSummary
```

#### `formatReport(report, format)`
Formats a report in different output formats.

```javascript
const textReport = reporter.formatReport(report, 'text');
const jsonReport = reporter.formatReport(report, 'json');
// Returns: string
```

#### `generateComparativeReport(week1Data, week2Data)`
Generates a comparison between two weeks.

```javascript
const comparison = await reporter.generateComparativeReport(week1, week2);
// Returns: Promise<ComparativeReport>
```

#### `exportData(data, format)`
Exports data in various formats.

```javascript
const csv = await reporter.exportData(meetings, 'csv');
const json = await reporter.exportData(report, 'json');
const md = await reporter.exportData(summary, 'markdown');
// Returns: Promise<string>
```

### Data Types

#### WeeklyReport
```typescript
interface WeeklyReport {
  period: string;
  totalMeetings: number;
  totalMinutes: number;
  averageEfficiency: number;
  estimatedCost: number;
  potentialSavings: number;
  trends: Trend[];
  topMeetings: RankedMeeting[];
  bottomMeetings: RankedMeeting[];
  recommendations: string[];
  byType: Record<string, TypeStats>;
  byDay: Record<string, DayStats>;
}

interface Trend {
  category: string;
  value: string | number;
  change: number;      // Percentage
  direction: 'improving' | 'declining' | 'stable';
}

interface RankedMeeting {
  id: string;
  title: string;
  efficiency: number;
  duration: number;
  attendees: number;
}
```

#### MeetingSummary
```typescript
interface MeetingSummary {
  title: string;
  date: string;
  duration: string;
  attendees: string | number;
  efficiencyScore: number;
  efficiencyLevel: string;      // 'Excellent', 'Good', 'Fair', etc.
  keySuggestions: string[];
  riskFactors: string[];
  actionItems: ActionItem[];
  decisions: string[];
}
```

#### ComparativeReport
```typescript
interface ComparativeReport {
  week1: WeeklyReport;
  week2: WeeklyReport;
  changes: Record<string, MetricChange>;
  insights: string[];
}

interface MetricChange {
  absolute: number;
  percent: number;
  direction: 'increase' | 'decrease' | 'no change';
}
```

## Usage Examples

### Basic Analysis
```javascript
const config = { /* your config */ };
const calendar = new Calendar(config);
const analyzer = new Analyzer(config);
const reporter = new Reporter(config);
reporter.setAnalyzer(analyzer);

// Get and analyze today's meetings
const meetings = await calendar.getTodaysMeetings();
const analyses = await Promise.all(
  meetings.map(meeting => analyzer.analyzeMeeting(meeting))
);

// Generate daily summary
const dailySummary = await analyzer.generateDailySummary(meetings);

// Generate weekly report
const weeklyMeetings = await calendar.getWeeklyMeetings();
const weeklyReport = await reporter.generateWeeklyReport(weeklyMeetings);

// Export as CSV
const csvData = await reporter.exportData(weeklyMeetings, 'csv');
```

### Custom Integration
```javascript
// Integrate with your own meeting data
const customMeeting = {
  id: 'custom-1',
  title: 'Team Retrospective',
  description: 'Monthly team retrospective and improvement planning',
  duration: 90,
  attendees: 10,
  // ... other fields
};

const analysis = await analyzer.analyzeMeeting(customMeeting);
console.log(`Efficiency: ${analysis.efficiencyScore}/100`);
console.log('Suggestions:', analysis.suggestions);

// Process meeting notes from your app
const notes = `Meeting notes from our retrospective...`;
const notesAnalysis = await analyzer.processMeetingNotes(notes);
console.log('Action items:', notesAnalysis.actionItems);
```

### Advanced Reporting
```javascript
// Generate comparative report
const week1Report = await reporter.generateWeeklyReport(week1Meetings);
const week2Report = await reporter.generateWeeklyReport(week2Meetings);
const comparison = await reporter.generateComparativeReport(week1Report, week2Report);

console.log('Efficiency change:', comparison.changes.averageEfficiency.percent + '%');
console.log('Insights:', comparison.insights);

// Format for different outputs
const textOutput = reporter.formatReport(week2Report, 'text');
const jsonOutput = reporter.formatReport(week2Report, 'json');

// Save to file
fs.writeFileSync('weekly-report.txt', textOutput);
fs.writeFileSync('weekly-report.json', jsonOutput);
```

## Error Handling

```javascript
try {
  const meetings = await calendar.getTodaysMeetings();
  const analysis = await analyzer.analyzeMeeting(meetings[0]);
} catch (error) {
  if (error.message.includes('calendar not configured')) {
    console.error('Calendar integration not configured. Run setup first.');
  } else if (error.message.includes('API key')) {
    console.error('AI API key missing. Some features will be limited.');
  } else {
    console.error('Analysis failed:', error.message);
  }
}
```

## Environment Variables

The skill can also be configured via environment variables:

```bash
export MEP_AI_PROVIDER=openai
export MEP_AI_API_KEY=sk-...
export MEP_CALENDAR_TYPE=google
export MEP_EFFICIENCY_THRESHOLD=70
```

Environment variables take precedence over configuration file values.

## Performance Tips

1. **Batch Processing**: Use `Promise.all()` for analyzing multiple meetings
2. **Caching**: Cache calendar data to reduce API calls
3. **Lazy Loading**: Initialize components only when needed
4. **Error Recovery**: Implement retry logic for external API calls

## Extension Points

The API is designed to be extensible. You can:

1. **Create custom analyzers** by extending the `Analyzer` class
2. **Add new calendar providers** by implementing the calendar interface
3. **Create custom reporters** for specific output formats
4. **Integrate with other systems** using the provided data structures

## Support

For API-related questions or issues:
- Check the troubleshooting guide
- Review the example implementations
- Contact support@clawhub.com