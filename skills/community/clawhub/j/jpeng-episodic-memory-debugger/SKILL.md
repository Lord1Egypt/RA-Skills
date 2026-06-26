---
name: episodic-memory-debugger
description: Provides tools for debugging episodic memory systems including recall precision analysis, multi-modal encoding validation, indexing efficiency checks, and irrelevant recall detection for AI agents.
---

# Episodic Memory Debugger

Diagnose and fix episodic memory issues including recall precision, multi-modal encoding, and indexing problems.

## When to Use

- Debugging low recall precision in memory systems
- Validating multi-modal encoding consistency
- Checking indexing efficiency
- Detecting irrelevant recall patterns
- Analyzing memory drift over time
- Optimizing retrieval ranking

## Usage

```javascript
const debugger = require('./skills/episodic-memory-debugger');

// Analyze recall precision
const analysis = debugger.analyzeRecallPrecision(memories, queries, groundTruth);
console.log('Precision:', analysis.overallPrecision);
console.log('Recall:', analysis.overallRecall);

// Detect encoding issues
const issues = debugger.detectEncodingIssues(memories);
console.log('Encoding consistency:', issues.consistency.consistency);

// Check indexing efficiency
const indexing = debugger.checkIndexingEfficiency(memories, indexStats);
console.log('Index coverage:', indexing.efficiency.coverage);

// Generate full diagnostic report
const report = debugger.generateDiagnosticReport(memories, queries, results, groundTruth);
console.log('Health score:', report.summary.healthScore);
```

## API

### `analyzeRecallPrecision(memories, queries, groundTruth)`

Analyze recall precision for a set of queries.

```javascript
const queries = [
  { id: 'q1', text: 'meeting notes', results: [{ id: 'm1' }, { id: 'm2' }] }
];

const groundTruth = {
  'q1': ['m1', 'm3']  // m2 is irrelevant
};

const analysis = analyzeRecallPrecision(memories, queries, groundTruth);
// {
//   overallPrecision: 0.5,
//   overallRecall: 0.5,
//   f1Score: 0.5,
//   perQueryMetrics: [...],
//   issues: [{ type: 'low_precision', queryId: 'q1', ... }]
// }
```

### `detectEncodingIssues(memories)`

Detect multi-modal encoding issues.

```javascript
const issues = detectEncodingIssues(memories);
// {
//   consistency: { modalityStats: {...}, issues: [], consistency: 0.95 },
//   embeddingQuality: { stats: {...}, issues: [] },
//   crossModalAlignment: { alignments: [...], issues: [], avgAlignment: 0.8 }
// }
```

### `checkIndexingEfficiency(memories, indexStats)`

Check indexing efficiency and detect issues.

```javascript
const result = checkIndexingEfficiency(memories, {
  fragmentationRatio: 0.1,
  avgLookupTime: 50
});
// {
//   efficiency: { coverage: 0.98, indexedCount: 980, totalCount: 1000, issues: [] },
//   structure: { depth: 3, branchFactor: 100, utilization: 0.85, issues: [] },
//   duplicates: { duplicateCount: 5, duplicateRate: 0.005, duplicates: [...] }
// }
```

### `detectIrrelevantRecall(queries, groundTruth)`

Detect patterns in irrelevant recalls.

```javascript
const patterns = detectIrrelevantRecall(queries, groundTruth);
// {
//   byModality: { text: 10, image: 5 },
//   byTimeRange: { '<1d': 3, '<1w': 7, '>1m': 5 },
//   bySource: { email: 8, chat: 7 }
// }
```

### `generateDiagnosticReport(memories, queries, results, groundTruth)`

Generate comprehensive diagnostic report.

```javascript
const report = generateDiagnosticReport(memories, queries, results, groundTruth);
// {
//   timestamp: '2026-03-25T08:30:00.000Z',
//   summary: {
//     avgPrecision: 0.85,
//     avgRecall: 0.78,
//     f1Score: 0.81,
//     encodingConsistency: 0.95,
//     indexCoverage: 0.98,
//     healthScore: 0.87
//   },
//   details: { ... },
//   recommendations: [
//     { priority: 'high', area: 'recall_precision', recommendation: '...' }
//   ]
// }
```

## Classes

### RecallPrecisionAnalyzer

Analyze recall precision metrics.

```javascript
const analyzer = new RecallPrecisionAnalyzer();

const analysis = analyzer.analyzeRecallPrecision(memories, queries, groundTruth);
const mrr = analyzer.calculateMRR(queries, groundTruth);
const ndcg = analyzer.calculateNDCG(queries, groundTruth, relevanceScores, 10);
```

### MultiModalEncodingValidator

Validate multi-modal encoding consistency.

```javascript
const validator = new MultiModalEncodingValidator();

const consistency = validator.validateEncodingConsistency(memories);
const quality = validator.checkEmbeddingQuality(memories, 'text');
const alignment = validator.detectCrossModalAlignment(memories);
```

### IndexingEfficiencyChecker

Check indexing efficiency and structure.

```javascript
const checker = new IndexingEfficiencyChecker();

const efficiency = checker.checkIndexingEfficiency(memories, indexStats);
const structure = checker.analyzeIndexStructure(memories, { branchFactor: 100 });
const duplicates = checker.checkDuplicates(memories, 0.99);
```

### IrrelevantRecallDetector

Detect patterns in irrelevant recalls.

```javascript
const detector = new IrrelevantRecallDetector();

const patterns = detector.detectIrrelevantPatterns(queries, groundTruth);
const scores = detector.scoreRelevance(query, memories);
```

### MemoryDriftDetector

Detect memory drift over time.

```javascript
const driftDetector = new MemoryDriftDetector();

// Set baseline
driftDetector.setBaseline(initialMemories);

// Detect drift
const drift = driftDetector.detectDrift(currentMemories);
// {
//   countDrift: 0.1,
//   embeddingDrift: 0.05,
//   modalityDrift: 0.02,
//   timeDrift: 0.15,
//   overallDrift: 0.08,
//   isSignificant: false
// }
```

## Example: Full Memory System Diagnostic

```javascript
const debugger = require('./skills/episodic-memory-debugger');

// Sample memories
const memories = [
  {
    id: 'm1',
    text: 'Meeting with John about project timeline',
    modalities: ['text'],
    embeddings: { text: [0.1, 0.2, 0.3, /* ... */] },
    timestamp: '2026-03-20T10:00:00Z',
    indexed: true
  },
  {
    id: 'm2',
    text: 'Lunch discussion about quarterly goals',
    modalities: ['text'],
    embeddings: { text: [0.4, 0.5, 0.6, /* ... */] },
    timestamp: '2026-03-21T12:00:00Z',
    indexed: true
  }
];

// Sample queries and ground truth
const queries = [
  {
    id: 'q1',
    text: 'project meeting',
    results: [{ id: 'm1' }, { id: 'm2' }]
  }
];

const groundTruth = {
  'q1': ['m1']  // Only m1 is relevant
};

// Generate diagnostic report
const report = debugger.generateDiagnosticReport(memories, queries, null, groundTruth);

console.log('=== Memory System Diagnostic Report ===');
console.log(`Health Score: ${(report.summary.healthScore * 100).toFixed(1)}%`);
console.log(`Precision: ${(report.summary.avgPrecision * 100).toFixed(1)}%`);
console.log(`Recall: ${(report.summary.avgRecall * 100).toFixed(1)}%`);
console.log(`Encoding Consistency: ${(report.summary.encodingConsistency * 100).toFixed(1)}%`);
console.log(`Index Coverage: ${(report.summary.indexCoverage * 100).toFixed(1)}%`);

if (report.recommendations.length > 0) {
  console.log('\nRecommendations:');
  for (const rec of report.recommendations) {
    console.log(`  [${rec.priority}] ${rec.area}: ${rec.recommendation}`);
  }
}
```

## Example: Encoding Validation

```javascript
const debugger = require('./skills/episodic-memory-debugger');

// Multi-modal memories
const memories = [
  {
    id: 'm1',
    text: 'Photo from vacation',
    modalities: ['text', 'image'],
    embeddings: {
      text: [0.1, 0.2, 0.3],
      image: [0.4, 0.5, 0.6]
    }
  },
  {
    id: 'm2',
    text: 'Voice memo',
    modalities: ['text', 'audio'],
    embeddings: {
      text: [0.7, 0.8, 0.9]
      // Missing audio embedding!
    }
  }
];

const issues = debugger.detectEncodingIssues(memories);

console.log('Encoding Consistency:', issues.consistency.consistency);
console.log('Issues found:', issues.consistency.issues.length);

for (const issue of issues.consistency.issues) {
  console.log(`  - ${issue.type}: ${issue.message}`);
}

// Check cross-modal alignment
console.log('\nCross-modal Alignment:', issues.crossModalAlignment.avgAlignment);
```

## Example: Index Optimization

```javascript
const debugger = require('./skills/episodic-memory-debugger');

const memories = [/* ... */];

const result = debugger.checkIndexingEfficiency(memories, {
  fragmentationRatio: 0.15,
  avgLookupTime: 75
});

console.log('Index Coverage:', result.efficiency.coverage);
console.log('Duplicates Found:', result.duplicates.duplicateCount);

if (result.structure.issues.length > 0) {
  console.log('Structure Issues:');
  for (const issue of result.structure.issues) {
    console.log(`  - ${issue.message}`);
  }
}
```

## Notes

- Recall precision analysis requires ground truth labels
- Multi-modal validation checks embedding consistency across modalities
- Indexing efficiency includes duplicate detection
- Memory drift detection helps identify concept drift
- Diagnostic reports include prioritized recommendations
- All metrics are calculated locally without external dependencies
