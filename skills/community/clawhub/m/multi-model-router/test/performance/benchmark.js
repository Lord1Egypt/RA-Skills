// Performance benchmark for MultiModelRouter
const MultiModelRouter = require('../../scripts/router');
const fs = require('fs');
const path = require('path');

class PerformanceBenchmark {
  constructor() {
    const configPath = path.join(__dirname, '../../config/default.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    this.router = new MultiModelRouter(config);
  }

  async benchmarkRoutingDecision(prompt, context = "", iterations = 100) {
    const startTime = process.hrtime.bigint();
    
    for (let i = 0; i < iterations; i++) {
      await this.router.route(prompt, context);
    }
    
    const endTime = process.hrtime.bigint();
    const totalTimeMs = Number(endTime - startTime) / 1000000;
    const avgTimeMs = totalTimeMs / iterations;
    
    return {
      iterations,
      totalTimeMs,
      avgTimeMs,
      promptLength: prompt.length,
      contextLength: context.length
    };
  }

  async runAllBenchmarks() {
    console.log('Running Multi-Model Router Performance Benchmarks...\n');
    
    // Test 1: Simple prompt
    const simpleResult = await this.benchmarkRoutingDecision("Hello, how are you?");
    console.log(`Simple prompt (${simpleResult.promptLength} chars): ${simpleResult.avgTimeMs.toFixed(2)}ms avg`);
    
    // Test 2: Privacy sensitive prompt  
    const privacyResult = await this.benchmarkRoutingDecision("My API key is sk-test123");
    console.log(`Privacy prompt (${privacyResult.promptLength} chars): ${privacyResult.avgTimeMs.toFixed(2)}ms avg`);
    
    // Test 3: Long prompt
    const longPrompt = "This is a long document content ".repeat(1000);
    const longResult = await this.benchmarkRoutingDecision(longPrompt);
    console.log(`Long prompt (${longResult.promptLength} chars): ${longResult.avgTimeMs.toFixed(2)}ms avg`);
    
    // Test 4: With context
    const context = "Previous conversation history ".repeat(500);
    const contextResult = await this.benchmarkRoutingDecision("Follow up question", context);
    console.log(`With context (${contextResult.contextLength} chars): ${contextResult.avgTimeMs.toFixed(2)}ms avg`);
    
    console.log('\nBenchmark completed!');
    return {
      simple: simpleResult,
      privacy: privacyResult, 
      long: longResult,
      withContext: contextResult
    };
  }
}

// Run benchmark if called directly
if (require.main === module) {
  const benchmark = new PerformanceBenchmark();
  benchmark.runAllBenchmarks().catch(console.error);
}

module.exports = PerformanceBenchmark;