---
name: feedback-loop-fine-tuner
description: Provides tools for implementing feedback loops to fine-tune LLM agents using user feedback for continuous personalization and improvement, including training dataset generation, prompt optimization, and A/B testing.
---

# Feedback Loop Fine-Tuner

Implement feedback loops to fine-tune LLM agents using user feedback for continuous personalization and improvement.

## When to Use

- Collecting user feedback from agent interactions
- Generating training datasets for fine-tuning
- Optimizing prompts based on feedback
- Tracking improvement metrics over time
- Running A/B tests for prompt variants
- Implementing RLHF preference learning

## Usage

```javascript
const fineTuner = require('./skills/feedback-loop-fine-tuner');

// Collect feedback
const feedback = fineTuner.collectFeedback({
  conversationId: 'conv_123',
  messageId: 'msg_456',
  query: 'What is machine learning?',
  response: 'Machine learning is...',
  rating: 'positive',
  model: 'llama-3',
  temperature: 0.7
});

// Generate training data
const dataset = fineTuner.generateTrainingData(feedbackHistory, {
  format: 'openai',
  includeCorrections: true
});

// Optimize prompts
const optimization = fineTuner.optimizePrompts(feedbackHistory, {
  'default': 'You are a helpful assistant.',
  'detailed': 'You are a detailed, thorough assistant.'
});

// Track improvement
const improvement = fineTuner.trackImprovement(beforeMetrics, afterMetrics);

// Create A/B test
const experiment = fineTuner.createABTest('prompt_test', [
  { name: 'control', template: 'You are helpful.' },
  { name: 'variant', template: 'You are a detailed, helpful assistant.' }
]);
```

## API

### `collectFeedback(interaction)`

Collect feedback from a user interaction.

```javascript
const feedback = collectFeedback({
  conversationId: 'conv_123',
  messageId: 'msg_456',
  query: 'Explain quantum computing',
  response: 'Quantum computing uses...',
  rating: 'positive', // 'positive', 'negative', 'neutral', 'correction'
  userCorrection: null, // Optional corrected response
  model: 'llama-3-70b',
  temperature: 0.7,
  promptTemplate: 'default',
  responseTime: 1500,
  tokensUsed: 256
});
```

### `generateTrainingData(feedbackHistory, options)`

Generate fine-tuning dataset from feedback history.

```javascript
const dataset = generateTrainingData(feedbackHistory, {
  includeNegative: false,
  includeCorrections: true,
  minRating: 'neutral',
  format: 'jsonl' // 'jsonl', 'openai', 'llama', 'alpaca'
});
```

Supported formats:
- **jsonl**: `{ "prompt": "...", "completion": "..." }`
- **openai**: `{ "messages": [{ "role": "user", "content": "..." }, ...] }`
- **llama**: Llama 3 chat format with special tokens
- **alpaca**: `{ "instruction": "...", "input": "", "output": "..." }`

### `optimizePrompts(feedbackHistory, templates)`

Optimize prompts based on feedback analysis.

```javascript
const result = optimizePrompts(feedbackHistory, {
  'concise': 'Answer briefly.',
  'detailed': 'Answer with full details.',
  'friendly': 'Answer in a friendly tone.'
});

console.log(result.bestTemplate); // 'detailed'
console.log(result.suggestions); // [{ type: 'length', suggestion: '...' }]
console.log(result.optimizedVariant); // Optimized prompt template
```

### `trackImprovement(before, after)`

Track improvement metrics between two snapshots.

```javascript
const improvement = trackImprovement(
  { qualityScore: 0.65, positiveRate: 0.70 },
  { qualityScore: 0.82, positiveRate: 0.85 }
);

console.log(improvement.qualityScore);
// { baseline: 0.65, current: 0.82, change: 0.17, percentChange: 26.15, improved: true }
```

### `generateImprovementReport(metricsHistory)`

Generate comprehensive improvement report.

```javascript
const report = generateImprovementReport([
  { qualityScore: 0.65, positiveRate: 0.70 },
  { qualityScore: 0.72, positiveRate: 0.75 },
  { qualityScore: 0.82, positiveRate: 0.85 }
]);

console.log(report.trends.qualityScore.direction); // 'improving'
console.log(report.summary.latestQualityScore); // 0.82
```

### `createABTest(name, variants, config)`

Create an A/B test experiment for prompt variants.

```javascript
const experiment = createABTest('tone_test', [
  { name: 'formal', template: 'You are a formal assistant.' },
  { name: 'casual', template: 'You are a friendly, casual assistant.' }
], {
  trafficSplit: [0.5, 0.5],
  minSamples: 100,
  confidenceLevel: 0.95
});
```

## Classes

### FeedbackCollector

Collect and aggregate user feedback.

```javascript
const collector = new FeedbackCollector();

// Collect individual feedback
const fb = collector.collectFeedback(interaction);

// Batch collect
collector.batchCollect(interactions);

// Aggregate by category
const aggregation = collector.aggregateByCategory({
  start: Date.now() - 7 * 24 * 60 * 60 * 1000, // Last 7 days
  end: Date.now()
});

// Export for analysis
const csv = collector.exportFeedback('csv');
```

### TrainingDatasetGenerator

Generate fine-tuning datasets from feedback.

```javascript
const generator = new TrainingDatasetGenerator();

// Generate training data
const dataset = generator.generateTrainingData(feedbackHistory, { format: 'openai' });

// Generate preference pairs for RLHF
const pairs = generator.generatePreferencePairs(feedbackHistory);

// Split into train/validation
const { train, validation } = generator.splitDataset(examples, 0.8);
```

### PromptOptimizer

Optimize prompts based on feedback.

```javascript
const optimizer = new PromptOptimizer();

// Register templates
optimizer.registerTemplate('default', 'You are helpful.');
optimizer.registerTemplate('detailed', 'You are detailed and thorough.');

// Update performance
optimizer.updatePerformance('default', feedback);

// Get best template
const best = optimizer.getBestTemplate();

// Get improvement suggestions
const suggestions = optimizer.suggestImprovements(feedbackHistory, 'default');

// Generate optimized variant
const variant = optimizer.generateVariant('default', suggestions);
```

### ImprovementTracker

Track improvement metrics over time.

```javascript
const tracker = new ImprovementTracker();

// Set baseline
tracker.setBaseline('initial', { qualityScore: 0.5 });

// Record snapshots
tracker.recordSnapshot({ qualityScore: 0.6 });
tracker.recordSnapshot({ qualityScore: 0.7 });

// Calculate improvement
const improvement = tracker.calculateImprovement({ qualityScore: 0.8 }, 'initial');

// Get trend
const trend = tracker.getTrend('qualityScore', 10);

// Generate report
const report = tracker.generateReport();
```

### ABTester

Run A/B tests for prompt variants.

```javascript
const tester = new ABTester();

// Create experiment
tester.createExperiment('tone_test', [
  { name: 'formal', template: 'Be formal.' },
  { name: 'casual', template: 'Be casual.' }
]);

// Assign variant
const variant = tester.assignVariant('tone_test');

// Record result
tester.recordResult('tone_test', variant.variantIndex, {
  rating: 'positive',
  responseTime: 1200
});

// Analyze results
const analysis = tester.analyzeResults('tone_test');

// Stop experiment
tester.stopExperiment('tone_test');
```

## Example: Complete Feedback Loop

```javascript
const fineTuner = require('./skills/feedback-loop-fine-tuner');

// 1. Initialize components
const collector = new fineTuner.FeedbackCollector();
const generator = new fineTuner.TrainingDatasetGenerator();
const optimizer = new fineTuner.PromptOptimizer();
const tracker = new fineTuner.ImprovementTracker();

// 2. Register prompt templates
optimizer.registerTemplate('v1', 'You are a helpful assistant.');
optimizer.registerTemplate('v2', 'You are a detailed, helpful assistant.');

// 3. Set baseline
tracker.setBaseline('initial', {
  qualityScore: 0.5,
  positiveRate: 0.5,
  avgResponseTime: 2000
});

// 4. Collect feedback (simulated)
const interactions = [
  { conversationId: 'c1', query: 'What is AI?', response: 'AI is...', rating: 'positive' },
  { conversationId: 'c2', query: 'Explain ML', response: 'ML is...', rating: 'negative' },
  { conversationId: 'c3', query: 'What is DL?', response: 'DL is...', rating: 'positive', userCorrection: 'Deep learning is a subset of ML that uses neural networks...' }
];

for (const interaction of interactions) {
  const feedback = collector.collectFeedback(interaction);
  optimizer.updatePerformance(interaction.promptTemplate || 'v1', feedback);
}

// 5. Generate training data
const feedbackHistory = collector.feedbackStore;
const trainingData = generator.generateTrainingData(feedbackHistory, {
  format: 'openai',
  includeCorrections: true
});

console.log('Training examples:', trainingData.split('\n').length);

// 6. Optimize prompts
const optimization = fineTuner.optimizePrompts(feedbackHistory, {
  'v1': 'You are a helpful assistant.',
  'v2': 'You are a detailed, helpful assistant.'
});

console.log('Best template:', optimization.bestTemplate);
console.log('Suggestions:', optimization.suggestions);

// 7. Track improvement
const aggregation = collector.aggregateByCategory();
tracker.recordSnapshot({
  qualityScore: aggregation.qualityScore,
  positiveRate: aggregation.byRating.positive?.length / aggregation.total || 0,
  avgResponseTime: aggregation.avgResponseTime,
  totalFeedback: aggregation.total
});

const report = tracker.generateReport();
console.log('Improvement trend:', report.trends.qualityScore?.direction);
```

## Example: RLHF Preference Learning

```javascript
const fineTuner = require('./skills/feedback-loop-fine-tuner');
const generator = new fineTuner.TrainingDatasetGenerator();

// Collect feedback with comparisons
const feedbackHistory = [
  { query: 'Explain AI', rating: 'positive', response: 'AI is artificial intelligence...' },
  { query: 'Explain AI', rating: 'negative', response: 'AI means artificial intelligence.' }
];

// Generate preference pairs
const pairs = generator.generatePreferencePairs(feedbackHistory);

console.log('Preference pairs:');
for (const pair of pairs) {
  console.log(`Prompt: ${pair.prompt}`);
  console.log(`Chosen: ${pair.chosen.substring(0, 50)}...`);
  console.log(`Rejected: ${pair.rejected.substring(0, 50)}...`);
}
```

## Notes

- Feedback ratings: 'positive', 'negative', 'neutral', 'correction'
- User corrections are treated as high-quality training examples
- Preference pairs are generated from positive/negative feedback on similar queries
- A/B testing uses simplified statistical significance (use proper libraries for production)
- Training data formats support OpenAI, Llama 3, and Alpaca fine-tuning
- All metrics are calculated locally without external dependencies
