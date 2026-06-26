/**
 * Comprehensive Test Suite for Smart Memory Curation System
 * 
 * Tests all 6 modules of the Smart Memory Curation System:
 * 1. SmartMemoryCurator - Core orchestrator
 * 2. AutoClassifier - Automatic classification
 * 3. AutoTagger - Multi-dimensional tagging
 * 4. DeduplicationEngine - Intelligent deduplication
 * 5. ImportanceScorer - Importance scoring
 * 6. RelationDiscoverer - Relation discovery
 * 
 * @author Ghost 👻
 * @version 4.3.0
 */

import { SmartMemoryCurator, RawMemory, AnalysisResult } from '../src/smart/SmartMemoryCurator';
import { AutoClassifier } from '../src/smart/AutoClassifier';
import { AutoTagger } from '../src/smart/AutoTagger';
import { DeduplicationEngine } from '../src/smart/DeduplicationEngine';
import { ImportanceScorer } from '../src/smart/ImportanceScorer';
import { RelationDiscoverer } from '../src/smart/RelationDiscoverer';

// ============ Test Data ============

const TEST_MEMORIES: RawMemory[] = [
  {
    id: 'test_tech_001',
    content: 'Successfully implemented TypeScript memory system with 6 modules. The architecture uses GraphRAG and AAAK compression.',
    timestamp: Date.now() - 3600000, // 1 hour ago
    metadata: { source: 'development', project: 'Memory-Master' }
  },
  {
    id: 'test_work_001',
    content: 'Team meeting discussed project milestones and deadlines. Need to complete documentation by Friday.',
    timestamp: Date.now() - 7200000, // 2 hours ago
    metadata: { source: 'work', priority: 'high' }
  },
  {
    id: 'test_personal_001',
    content: 'Feeling happy and accomplished today! Finished a major project and learned new skills.',
    timestamp: Date.now() - 10800000, // 3 hours ago
    metadata: { source: 'personal', mood: 'positive' }
  },
  {
    id: 'test_learning_001',
    content: 'Studied advanced TypeScript patterns and AI memory management techniques. Found several useful resources.',
    timestamp: Date.now() - 14400000, // 4 hours ago
    metadata: { source: 'learning', topic: 'TypeScript' }
  },
  {
    id: 'test_duplicate_001',
    content: 'Successfully implemented TypeScript memory system with 6 modules. The architecture uses GraphRAG and AAAK compression.',
    timestamp: Date.now() - 18000000, // 5 hours ago
    metadata: { source: 'test', isDuplicate: true }
  },
  {
    id: 'test_short_001',
    content: 'Short note.',
    timestamp: Date.now(),
    metadata: { source: 'test' }
  }
];

// ============ Test Runner ============

class TestRunner {
  private tests: Array<{ name: string; fn: () => Promise<void> }> = [];
  private passed = 0;
  private failed = 0;
  private errors: Array<{ test: string; error: any }> = [];

  addTest(name: string, fn: () => Promise<void>) {
    this.tests.push({ name, fn });
  }

  async runAll() {
    console.log('='.repeat(80));
    console.log('🧪 COMPREHENSIVE TEST SUITE - Smart Memory Curation System');
    console.log('='.repeat(80));
    console.log(`Running ${this.tests.length} tests...\n`);

    for (let i = 0; i < this.tests.length; i++) {
      const test = this.tests[i];
      process.stdout.write(`[${i + 1}/${this.tests.length}] ${test.name}... `);
      
      try {
        await test.fn();
        console.log('✅ PASS');
        this.passed++;
      } catch (error) {
        console.log('❌ FAIL');
        console.log(`   Error: ${error}`);
        this.failed++;
        this.errors.push({ test: test.name, error });
      }
    }

    this.report();
  }

  report() {
    console.log('\n' + '='.repeat(80));
    console.log('📊 TEST RESULTS');
    console.log('='.repeat(80));
    console.log(`Total Tests: ${this.tests.length}`);
    console.log(`✅ Passed: ${this.passed}`);
    console.log(`❌ Failed: ${this.failed}`);
    console.log(`📈 Success Rate: ${((this.passed / this.tests.length) * 100).toFixed(1)}%`);

    if (this.errors.length > 0) {
      console.log('\n⚠️ ERRORS:');
      this.errors.forEach((err, i) => {
        console.log(`  ${i + 1}. ${err.test}: ${err.error}`);
      });
    }

    console.log('\n' + '='.repeat(80));
  }

  assert(condition: boolean, message: string) {
    if (!condition) {
      throw new Error(`Assertion failed: ${message}`);
    }
  }

  assertEqual(actual: any, expected: any, message: string) {
    if (actual !== expected) {
      throw new Error(`Assertion failed: ${message} (expected ${expected}, got ${actual})`);
    }
  }

  assertGreater(actual: number, expected: number, message: string) {
    if (actual <= expected) {
      throw new Error(`Assertion failed: ${message} (expected > ${expected}, got ${actual})`);
    }
  }

  assertLess(actual: number, expected: number, message: string) {
    if (actual >= expected) {
      throw new Error(`Assertion failed: ${message} (expected < ${expected}, got ${actual})`);
    }
  }

  assertInRange(actual: number, min: number, max: number, message: string) {
    if (actual < min || actual > max) {
      throw new Error(`Assertion failed: ${message} (expected ${min}-${max}, got ${actual})`);
    }
  }

  assertContains(array: any[], item: any, message: string) {
    if (!array.includes(item)) {
      throw new Error(`Assertion failed: ${message} (array does not contain ${item})`);
    }
  }
}

// ============ Test Suite ============

async function runComprehensiveTests() {
  const runner = new TestRunner();

  // ============ Module 1: SmartMemoryCurator Tests ============
  
  runner.addTest('SmartMemoryCurator - Initialization', async () => {
    const curator = new SmartMemoryCurator();
    runner.assert(!!curator, 'Curator should be created');
    const stats = curator.getStatistics();
    runner.assertEqual(stats.totalProcessed, 0, 'Should start with 0 processed');
  });

  runner.addTest('SmartMemoryCurator - Single Memory Analysis', async () => {
    const curator = new SmartMemoryCurator();
    const memory = TEST_MEMORIES[0];
    const result = await curator.analyze(memory);
    
    runner.assert(!!result, 'Should return analysis result');
    runner.assert(!!result.category, 'Should have category');
    runner.assertInRange(result.categoryConfidence, 0, 1, 'Confidence should be 0-1');
    runner.assert(Array.isArray(result.tags), 'Should have tags array');
    runner.assert(typeof result.importance === 'number', 'Should have importance score');
    runner.assertInRange(result.importance, 0, 100, 'Importance should be 0-100');
  });

  runner.addTest('SmartMemoryCurator - Batch Processing', async () => {
    const curator = new SmartMemoryCurator({ batchSize: 2 });
    const results = await curator.analyzeBatch(TEST_MEMORIES.slice(0, 3));
    
    runner.assertEqual(results.length, 3, 'Should process all memories');
    results.forEach((result, i) => {
      runner.assert(!!result.category, `Memory ${i} should have category`);
      runner.assertGreater(result.tags.length, 0, `Memory ${i} should have tags`);
    });
  });

  runner.addTest('SmartMemoryCurator - Cache Functionality', async () => {
    const curator = new SmartMemoryCurator();
    const memory = TEST_MEMORIES[0];
    
    // First analysis
    const start1 = Date.now();
    const result1 = await curator.analyze(memory);
    const time1 = Date.now() - start1;
    
    // Second analysis (should be cached)
    const start2 = Date.now();
    const result2 = await curator.analyze(memory);
    const time2 = Date.now() - start2;
    
    runner.assertLess(time2, time1 * 2, 'Cached analysis should be faster');
    runner.assertEqual(result1.category, result2.category, 'Cached results should match');
  });

  runner.addTest('SmartMemoryCurator - Statistics Tracking', async () => {
    const curator = new SmartMemoryCurator();
    await curator.analyze(TEST_MEMORIES[0]);
    await curator.analyze(TEST_MEMORIES[1]);
    
    const stats = curator.getStatistics();
    runner.assertEqual(stats.totalProcessed, 2, 'Should track processed count');
    runner.assertGreater(stats.averageProcessingTime, 0, 'Should track processing time');
  });

  // ============ Module 2: AutoClassifier Tests ============

  runner.addTest('AutoClassifier - Technical Content Classification', async () => {
    const classifier = new AutoClassifier();
    const result = await classifier.classify(
      'TypeScript code implementation with AI memory system and GraphRAG architecture'
    );
    
    runner.assert(!!result.category, 'Should return category');
    runner.assertEqual(result.category, 'technical', 'Technical content should classify as technical');
    runner.assertInRange(result.confidence, 0.7, 1.0, 'Should have high confidence');
  });

  runner.addTest('AutoClassifier - Personal Content Classification', async () => {
    const classifier = new AutoClassifier();
    const result = await classifier.classify(
      'Feeling happy about personal achievements and enjoying time with family'
    );
    
    runner.assertContains(['personal', 'social'], result.category, 'Personal content should classify appropriately');
    runner.assertInRange(result.confidence, 0.5, 1.0, 'Should have reasonable confidence');
  });

  runner.addTest('AutoClassifier - Work Content Classification', async () => {
    const classifier = new AutoClassifier();
    const result = await classifier.classify(
      'Project deadline approaching, need to coordinate with team members and update documentation'
    );
    
    runner.assertContains(['work', 'project'], result.category, 'Work content should classify appropriately');
  });

  runner.addTest('AutoClassifier - Short Content Classification', async () => {
    const classifier = new AutoClassifier();
    const result = await classifier.classify('Short note');
    
    runner.assert(!!result.category, 'Should handle short content');
    runner.assertEqual(result.category, 'other', 'Short ambiguous content should be "other"');
  });

  // ============ Module 3: AutoTagger Tests ============

  runner.addTest('AutoTagger - Keyword Extraction', async () => {
    const tagger = new AutoTagger();
    const result = await tagger.tag(
      'Implementing TypeScript memory system with AI capabilities and GraphRAG architecture'
    );
    
    runner.assert(Array.isArray(result.keywordTags), 'Should extract keywords');
    runner.assertGreater(result.keywordTags.length, 0, 'Should extract at least one keyword');
    runner.assertContains(result.keywordTags, 'TypeScript', 'Should contain TypeScript keyword');
    runner.assertContains(result.keywordTags, 'memory', 'Should contain memory keyword');
  });

  runner.addTest('AutoTagger - Emotion Detection', async () => {
    const tagger = new AutoTagger();
    const result = await tagger.tag(
      'Feeling excited and joyful about the successful project completion! This is amazing.'
    );
    
    runner.assert(Array.isArray(result.emotionTags), 'Should detect emotions');
    runner.assertGreater(result.emotionTags.length, 0, 'Should detect at least one emotion');
    runner.assert(!!result.emotionScores, 'Should have emotion scores');
    
    if (result.emotionTags.includes('joy')) {
      const joyScore = result.emotionScores?.joy || 0;
      runner.assertGreater(joyScore, 0.5, 'Joy should have reasonable score');
    }
  });

  runner.addTest('AutoTagger - Entity Recognition', async () => {
    const tagger = new AutoTagger();
    const result = await tagger.tag(
      'Project meeting on 2026-04-20 discussed https://github.com/openclaw/memory implementation'
    );
    
    runner.assert(!!result.extractedEntities, 'Should extract entities');
    runner.assert(Array.isArray(result.extractedEntities?.urls), 'Should extract URLs');
    runner.assert(Array.isArray(result.extractedEntities?.dates), 'Should extract dates');
    
    if (result.extractedEntities?.urls) {
      runner.assertContains(result.extractedEntities.urls, 'https://github.com/openclaw/memory', 'Should contain URL');
    }
    
    if (result.extractedEntities?.dates) {
      runner.assertContains(result.extractedEntities.dates, '2026-04-20', 'Should contain date');
    }
  });

  runner.addTest('AutoTagger - Rule-based Tagging', async () => {
    const tagger = new AutoTagger();
    const result = await tagger.tag(
      'URGENT: Critical bug fix required for production system. High priority task.'
    );
    
    runner.assert(Array.isArray(result.ruleTags), 'Should apply rule tags');
    runner.assertContains(result.ruleTags, 'urgent', 'Should tag as urgent');
    runner.assertContains(result.ruleTags, 'high-priority', 'Should tag as high priority');
  });

  // ============ Module 4: DeduplicationEngine Tests ============

  runner.addTest('DeduplicationEngine - Exact Match Detection', async () => {
    const deduper = new DeduplicationEngine({
      similarityThreshold: 0.8,
      exactMatch: true,
      fuzzyMatch: true,
      semanticCheck: true
    });
    
    const memory1 = TEST_MEMORIES[0];
    const memory2 = TEST_MEMORIES[4]; // Exact duplicate
    
    // First memory
    const result1 = await deduper.checkDuplicate(memory1);
    runner.assertEqual(result1.isDuplicate, false, 'First memory should not be duplicate');
    
    // Duplicate memory
    const result2 = await deduper.checkDuplicate(memory2);
    runner.assertEqual(result2.isDuplicate, true, 'Exact duplicate should be detected');
  });

  runner.addTest('DeduplicationEngine - Similarity Calculation', async () => {
    const deduper = new DeduplicationEngine();
    
    const text1 = 'TypeScript memory system implementation';
    const text2 = 'TypeScript memory system development';
    
    const similarity = await deduper.calculateSimilarity(text1, text2);
    
    runner.assert(!!similarity, 'Should calculate similarity');
    runner.assertInRange(similarity.score, 0, 1, 'Similarity should be 0-1');
    runner.assertGreater(similarity.score, 0.5, 'Similar texts should have high similarity');
  });

  runner.addTest('DeduplicationEngine - Batch Deduplication', async () => {
    const deduper = new DeduplicationEngine({
      similarityThreshold: 0.9,
      exactMatch: true,
      fuzzyMatch: true,
      semanticCheck: false
    });
    
    // Create test data with duplicates
    const memories = [
      { id: '1', content: 'First unique memory', timestamp: Date.now() },
      { id: '2', content: 'Second unique memory', timestamp: Date.now() },
      { id: '3', content: 'First unique memory', timestamp: Date.now() - 1000 }, // Duplicate
      { id: '4', content: 'Third unique memory', timestamp: Date.now() },
    ];
    
    const deduped = await deduper.deduplicateBatch(memories);
    
    runner.assertLess(deduped.length, memories.length, 'Should remove duplicates');
    runner.assertEqual(deduped.length, 3, 'Should keep 3 unique memories');
    
    // Check IDs are preserved
    const ids = deduped.map(m => m.id);
    runner.assertContains(ids, '1', 'Should keep first unique');
    runner.assertContains(ids, '2', 'Should keep second unique');
    runner.assertContains(ids, '4', 'Should keep fourth unique');
  });

  // ============ Module 5: ImportanceScorer Tests ============

  runner.addTest('ImportanceScorer - Technical Content Scoring', async () => {
    const scorer = new ImportanceScorer();
    const classifier = new AutoClassifier();
    const tagger = new AutoTagger();
    
    const content = 'Comprehensive TypeScript implementation of AI memory system with GraphRAG architecture and advanced compression algorithms.';
    const classification = await classifier.classify(content);
    const tagging = await tagger.tag(content);
    
    const importance = scorer.calculate(content, classification, tagging);
    
    runner.assert(!!importance, 'Should calculate importance');
    runner.assertInRange(importance.score, 0, 100, 'Score should be 0-100');
    runner.assertGreater(importance.score, 60, 'Technical content should have medium-high importance');
    runner.assert(!!importance.factors, 'Should include factor breakdown');
    runner.assert(!!importance.interpretation, 'Should include interpretation');
  });

  runner.addTest('ImportanceScorer - Short Content Scoring', async () => {
    const scorer = new ImportanceScorer();
    const classifier = new AutoClassifier();
    const tagger = new AutoTagger();
    
    const content = 'Short note.';
    const classification = await classifier.classify(content);
    const tagging = await tagger.tag(content);
    
    const importance = scorer.calculate(content, classification, tagging);
    
    runner.assertInRange(importance.score, 0, 100, 'Score should be 0-100');
    runner.assertLess(importance.score, 40, 'Short content should have low importance');
  });

  runner.addTest('ImportanceScorer - Emotional Content Scoring', async () => {
    const scorer = new ImportanceScorer();
    const classifier = new AutoClassifier();
    const tagger = new AutoTagger();
    
    const content = 'Extremely important personal achievement! Feeling incredibly proud and joyful about completing major life goal.';
    const classification = await classifier.classify(content);
    const tagging = await tagger.tag(content);
    
    const importance = scorer.calculate(content, classification, tagging);
    
    runner.assertGreater(importance.score, 70, 'Emotional content should have high importance');
    runner.assertGreater(importance.factors.emotionalIntensity, 0.7, 'Should detect high emotional intensity');
  });

  runner.addTest('ImportanceScorer - Batch Scoring', async () => {
    const scorer = new ImportanceScorer();
    const classifier = new AutoClassifier();
    const tagger = new AutoTagger();
    
    const items = [
      {
        content: 'Important technical documentation',
        classification: await classifier.classify('Important technical documentation'),
        tagging: await tagger.tag('Important technical documentation')
      },
      {
        content: 'Short note',
        classification: await classifier.classify('Short note'),
        tagging: await tagger.tag('Short note')
      }
    ];
    
    const scores = scorer.batchCalculate(items);
    
    runner.assertEqual(scores.length, 2, 'Should score all items');
    runner.assertGreater(scores[0].score, scores[1].score, 'Important content should score higher');
  });

  // ============ Module 6: RelationDiscoverer Tests ============

  runner.addTest('RelationDiscoverer - Basic Relation Discovery', async () => {
    const discoverer = new RelationDiscoverer({
      similarityThreshold: 0.5,
      maxRelatedMemories: 3
    });
    
    // Register some memories
    discoverer.registerMemory({
      id: 'mem1',
      content: 'TypeScript memory system development',
      timestamp: Date.now() - 10000
    });
    
    discoverer.registerMemory({
      id: 'mem2', 
      content: 'AI memory management techniques',
      timestamp: Date.now() - 20000
    });
    
    // Discover relations for new memory
    const memory = {
      id: 'mem3',
      content: 'Working on TypeScript implementation of memory system',
      timestamp: Date.now()
    };
    
    const relations = await discoverer.discoverRelations(memory);
    
    runner.assert(Array.isArray(relations.relatedIds), 'Should return related IDs');
    runner.assert(Array.isArray(relations.relationTypes), 'Should return relation types');
    
    // Should find relation with mem1 (similar content)
    runner.assertContains(relations.relatedIds, 'mem1', 'Should relate to similar memory');
  });

  runner.addTest('RelationDiscoverer - Enhanced Relation Discovery', async () => {
    const discoverer = new RelationDiscoverer();
    
    // Register memories with different content
    discoverer.registerMemory({
      id: 'tech1',
      content: 'TypeScript programming and AI systems',
      timestamp: Date.now() - 3600000, // 1 hour ago
      metadata: { category: 'technical' }
    });
    
    discoverer.registerMemory({
      id: 'personal1',
      content: 'Personal feelings and reflections',
      timestamp: Date.now() - 7200000, // 2 hours ago
      metadata: { category: 'personal' }
    });
    
    const memory = {
      id: 'tech2',
      content: 'Developing TypeScript memory system with AI capabilities',
      timestamp: Date.now(),
      metadata: { category: 'technical' }
    };
    
    const enhancedRelations = await discoverer.discoverRelationsEnhanced(memory);
    
    runner.assert(!!enhancedRelations, 'Should return enhanced relations');
    runner.assert(Array.isArray(enhancedRelations.relatedIds), 'Should have related IDs');
    runner.assert(Array.isArray(enhancedRelations.relationStrengths), 'Should have relation strengths');
    runner.assert(!!enhancedRelations.details, 'Should have detailed analysis');
    runner.assert(!!enhancedRelations.explanation, 'Should have explanation');
    
    // Should relate more strongly to tech1 than personal1
    const techIndex = enhancedRelations.relatedIds.indexOf('tech1');
    const personalIndex = enhancedRelations.relatedIds.indexOf('personal1');
    
    if (techIndex >= 0 && personalIndex >= 0) {
      runner.assertGreater(
        enhancedRelations.relationStrengths[techIndex],
        enhancedRelations.relationStrengths[personalIndex],
        'Should have stronger relation to similar content'
      );
    }
  });

  runner.addTest('RelationDiscoverer - Temporal Relations', async () => {
    const discoverer = new RelationDiscoverer({
      temporalWeight: 0.5,
      similarityThreshold: 0.3
    });
    
    const now = Date.now();
    
    // Register memory from 5 minutes ago
    discoverer.registerMemory({
      id: 'recent',
      content: 'Recent memory',
      timestamp: now - 300000 // 5 minutes ago
    });
    
    // Register memory from 5 days ago
    discoverer.registerMemory({
      id: 'old',
      content: 'Old memory',
      timestamp: now - 432000000 // 5 days ago
    });
    
    const memory = {
      id: 'current',
      content: 'Current memory',
      timestamp: now
    };
    
    const relations = await discoverer.discoverRelations(memory);
    
    // Should relate more strongly to recent memory
    if (relations.relatedIds.includes('recent')) {
      // Recent memory should be found
      runner.assertContains(relations.relationTypes, 'temporal_proximity', 'Should detect temporal proximity');
    }
  });

  // ============ Integration Tests ============

  runner.addTest('Full Integration - Complete Pipeline', async () => {
    const curator = new SmartMemoryCurator({
      autoProcess: true,
      batchSize: 5,
      cacheSize: 50
    });
    
    // Test with various memory types
    const memories = [
      {
        content: 'Technical implementation of memory system with TypeScript and AI',
        metadata: { type: 'technical' }
      },
      {
        content: 'Personal reflection on learning journey and achievements',
        metadata: { type: 'personal' }
      },
      {
        content: 'Meeting notes and project planning for upcoming release',
        metadata: { type: 'work' }
      }
    ];
    
    const results = await curator.analyzeBatch(memories);
    
    runner.assertEqual(results.length, 3, 'Should process all memories');
    
    // Verify each result has complete analysis
    results.forEach((result, i) => {
      runner.assert(!!result.category, `Memory ${i} should have category`);
      runner.assertGreater(result.tags.length, 0, `Memory ${i} should have tags`);
      runner.assertInRange(result.importance, 0, 100, `Memory ${i} should have importance score`);
      runner.assert(typeof result.isDuplicate === 'boolean', `Memory ${i} should have duplicate check`);
      runner.assert(Array.isArray(result.relatedMemoryIds), `Memory ${i} should have related IDs`);
    });
    
    // Check system statistics
    const stats = curator.getStatistics();
    runner.assertEqual(stats.totalProcessed, 3, 'Should track all processed memories');
    runner.assertGreater(stats.averageProcessingTime, 0, 'Should measure processing time');
  });

  runner.addTest('Full Integration - Performance Benchmark', async () => {
    const curator = new SmartMemoryCurator({ batchSize: 10 });
    
    // Create test memories
    const testMemories = Array.from({ length: 10 }, (_, i) => ({
      id: `perf_${i}`,
      content: `Test memory ${i} about AI memory systems and TypeScript development`,
      timestamp: Date.now() - (i * 60000) // 1 minute intervals
    }));
    
    const startTime = Date.now();
    const results = await curator.analyzeBatch(testMemories);
    const totalTime = Date.now() - startTime;
    
    runner.assertEqual(results.length, 10, 'Should process all memories');
    runner.assertLess(totalTime, 10000, 'Should process 10 memories in reasonable time');
    
    const avgTimePerMemory = totalTime / 10;
    console.log(`   Average time per memory: ${avgTimePerMemory.toFixed(1)}ms`);
    
    // Performance requirement: < 1000ms per memory
    runner.assertLess(avgTimePerMemory, 1000, 'Should process under 1000ms per memory');
  });

  // ============ Edge Case Tests ============

  runner.addTest('Edge Cases - Empty Content', async () => {
    const curator = new SmartMemoryCurator();
    const memory = { content: '', metadata: { test: true } };
    
    const result = await curator.analyze(memory);
    
    runner.assert(!!result, 'Should handle empty content');
    runner.assertEqual(result.category, 'other', 'Empty content should be "other"');
    runner.assertEqual(result.tags.length, 0, 'Empty content should have no tags');
    runner.assertLess(result.importance, 30, 'Empty content should have low importance');
  });

  runner.addTest('Edge Cases - Very Long Content', async () => {
    const curator = new SmartMemoryCurator();
    
    // Create very long content
    const longContent = 'Very long content. '.repeat(1000);
    const memory = { content: longContent, metadata: { test: 'long' } };
    
    const result = await curator.analyze(memory);
    
    runner.assert(!!result, 'Should handle long content');
    runner.assert(!!result.category, 'Should categorize long content');
    runner.assertGreater(result.tags.length, 0, 'Should extract tags from long content');
    runner.assertGreater(result.importance, 50, 'Long content should have medium importance');
  });

  runner.addTest('Edge Cases - Special Characters', async () => {
    const curator = new SmartMemoryCurator();
    const memory = {
      content: 'Content with special characters: !@#$%^&*()_+{}|:"<>?[]\\;\',./`~ and emoji 😊🎉',
      metadata: { test: 'special' }
    };
    
    const result = await curator.analyze(memory);
    
    runner.assert(!!result, 'Should handle special characters');
    runner.assert(!!result.category, 'Should categorize with special characters');
    runner.assertGreater(result.tags.length, 0, 'Should extract tags despite special chars');
  });

  // ============ Run All Tests ============

  console.log('🚀 Starting comprehensive tests for Smart Memory Curation System...\n');
  await runner.runAll();
  
  return {
    passed: runner['passed'],
    failed: runner['failed'],
    total: runner['tests'].length
  };
}

// ============ Main Execution ============

if (require.main === module) {
  runComprehensiveTests().then(results => {
    console.log('\n🎯 TEST SUMMARY:');
    console.log(`   Total: ${results.total}`);
    console.log(`   Passed: ${results.passed}`);
    console.log(`   Failed: ${results.failed}`);
    console.log(`   Success Rate: ${((results.passed / results.total) * 100).toFixed(1)}%`);
    
    if (results.failed === 0) {
      console.log('\n🎉 ALL TESTS PASSED! Smart Memory Curation System is ready!');
      process.exit(0);
    } else {
      console.log(`\n⚠️ ${results.failed} test(s) failed. Review errors above.`);
      process.exit(1);
    }
  }).catch(error => {
    console.error('❌ Test runner crashed:', error);
    process.exit(1);
  });
}

export { runComprehensiveTests };