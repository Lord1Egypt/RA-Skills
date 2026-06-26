# L76 Core Architecture - Advanced Examples

Complete, production-ready examples demonstrating advanced patterns and extensions.

---

## Example 1: Multi-Stage Pipeline Skill

A skill that processes data through multiple stages with validation between each stage.

```javascript
// pipeline-skill/index.js

const { SkillExecutor, StateManager } = require('../l76-core-arch/index.js');

class PipelineExecutor extends SkillExecutor {
  constructor(config) {
    super(config);
    this.stages = [
      { name: 'extract', fn: this.extract.bind(this) },
      { name: 'transform', fn: this.transform.bind(this) },
      { name: 'validate', fn: this.validate.bind(this) },
      { name: 'load', fn: this.load.bind(this) }
    ];
  }

  async process(options) {
    const { input, outputDir } = options;
    let data = null;
    const stageResults = [];

    for (const stage of this.stages) {
      console.log(`🔄 Starting stage: ${stage.name}`);
      
      const stageStart = Date.now();
      
      try {
        data = await stage.fn(data, options);
        const duration = Date.now() - stageStart;
        
        stageResults.push({
          stage: stage.name,
          status: 'success',
          duration,
          timestamp: new Date().toISOString()
        });

        console.log(`✅ Stage complete: ${stage.name} (${duration}ms)`);
        
        // Update state after each stage
        this.state.update({
          lastStage: stage.name,
          stageResults,
          progress: {
            current: stageResults.length,
            total: this.stages.length,
            percent: Math.round(stageResults.length / this.stages.length * 100)
          }
        });

      } catch (error) {
        stageResults.push({
          stage: stage.name,
          status: 'failed',
          error: error.message,
          duration: Date.now() - stageStart
        });

        console.error(`❌ Stage failed: ${stage.name} - ${error.message}`);
        
        // Attempt stage-specific recovery
        const recovered = await this.recoverStage(stage, data, options);
        if (!recovered) {
          throw error; // Re-throw if recovery failed
        }
      }
    }

    return {
      status: 'complete',
      stages: stageResults,
      totalDuration: stageResults.reduce((sum, s) => sum + s.duration, 0)
    };
  }

  async extract(data, options) {
    // Extract data from source
    const result = await exec({ 
      command: `cat ${options.input}` 
    });
    return result.stdout;
  }

  async transform(data, options) {
    // Transform data (example: JSON parsing and enrichment)
    const parsed = JSON.parse(data);
    parsed.processedAt = new Date().toISOString();
    parsed.enriched = true;
    return JSON.stringify(parsed, null, 2);
  }

  async validate(data, options) {
    // Validate transformed data
    const parsed = JSON.parse(data);
    
    if (!parsed.id) {
      throw new Error('Validation failed: missing required field "id"');
    }
    
    return data; // Return unchanged if valid
  }

  async load(data, options) {
    // Load to destination
    const outputPath = `${options.outputDir}/output.json`;
    await write({ path: outputPath, content: data });
    return outputPath;
  }

  async recoverStage(stage, data, options) {
    console.log(`🔧 Attempting recovery for stage: ${stage.name}`);
    
    // Stage-specific recovery strategies
    switch (stage.name) {
      case 'extract':
        // Retry with different encoding
        try {
          const result = await exec({ 
            command: `iconv -f UTF-8 -t ASCII//TRANSLIT ${options.input}` 
          });
          return result.stdout;
        } catch (e) {
          return false;
        }
      
      case 'validate':
        // Log validation errors and continue
        console.warn('⚠️ Validation failed, continuing anyway');
        return data;
      
      default:
        return false; // No recovery available
    }
  }
}

module.exports = { PipelineExecutor };
```

**Usage:**

```bash
node index.js --input ./data.json --output-dir ./output
```

---

## Example 2: Watcher Skill (File System Monitoring)

A skill that watches for file changes and processes them automatically.

```javascript
// watcher-skill/index.js

const { SkillExecutor } = require('../l76-core-arch/index.js');
const fs = require('fs');
const path = require('path');

class WatcherExecutor extends SkillExecutor {
  constructor(config) {
    super(config);
    this.watchers = new Map();
    this.debounceTimers = new Map();
  }

  async process(options) {
    const { watchDir, pattern, handler } = options;
    
    console.log(`👁️ Starting watcher on: ${watchDir}`);
    console.log(`   Pattern: ${pattern}`);
    console.log(`   Handler: ${handler}`);

    // Start watching
    this.startWatcher(watchDir, pattern, handler);

    // Keep process alive
    return new Promise((resolve) => {
      process.on('SIGINT', () => {
        console.log('\n🛑 Stopping watcher...');
        this.stopAllWatchers();
        resolve({ status: 'stopped' });
      });
    });
  }

  startWatcher(dir, pattern, handler) {
    const watcher = fs.watch(dir, { recursive: true }, (eventType, filename) => {
      if (!filename || !filename.match(new RegExp(pattern))) {
        return;
      }

      console.log(`📝 Change detected: ${eventType} - ${filename}`);

      // Debounce rapid changes
      const key = `${dir}/${filename}`;
      if (this.debounceTimers.has(key)) {
        clearTimeout(this.debounceTimers.get(key));
      }

      const timer = setTimeout(async () => {
        try {
          await this.handleFileChange(dir, filename, handler);
        } catch (error) {
          console.error(`Handler failed for ${filename}:`, error.message);
        }
      }, 500); // 500ms debounce

      this.debounceTimers.set(key, timer);
    });

    this.watchers.set(dir, watcher);
    console.log(`✅ Watching: ${dir}`);
  }

  async handleFileChange(dir, filename, handler) {
    const filePath = path.join(dir, filename);
    
    // Get file info
    const stat = await fs.promises.stat(filePath);
    
    console.log(`   Size: ${stat.size} bytes`);
    console.log(`   Modified: ${stat.mtime}`);

    // Execute handler
    switch (handler) {
      case 'log':
        console.log(`   Content preview: ${filePath}`);
        break;
      
      case 'process':
        await this.processFile(filePath);
        break;
      
      case 'backup':
        await this.backupFile(filePath);
        break;
      
      default:
        console.warn(`Unknown handler: ${handler}`);
    }

    // Update state
    this.state.update({
      lastChange: {
        file: filename,
        time: new Date().toISOString(),
        size: stat.size
      },
      totalChanges: (this.state.state.totalChanges || 0) + 1
    });
  }

  async processFile(filePath) {
    console.log(`⚙️ Processing: ${filePath}`);
    const content = await read({ path: filePath });
    // Add processing logic here
    console.log(`✅ Processed: ${filePath}`);
  }

  async backupFile(filePath) {
    const backupPath = filePath + `.backup.${Date.now()}`;
    console.log(`💾 Backing up: ${filePath} → ${backupPath}`);
    await exec({ command: `copy "${filePath}" "${backupPath}"` });
  }

  stopAllWatchers() {
    for (const [dir, watcher] of this.watchers) {
      watcher.close();
      console.log(`🛑 Stopped watching: ${dir}`);
    }
    this.watchers.clear();

    for (const timer of this.debounceTimers.values()) {
      clearTimeout(timer);
    }
    this.debounceTimers.clear();
  }
}

module.exports = { WatcherExecutor };
```

**Usage:**

```bash
# Watch for markdown changes and log them
node index.js --watch-dir ./docs --pattern ".*\.md$" --handler log

# Watch for JSON changes and process them
node index.js --watch-dir ./data --pattern ".*\.json$" --handler process
```

---

## Example 3: API Integration Skill

A skill that integrates with external APIs with rate limiting and retry logic.

```javascript
// api-skill/index.js

const { SkillExecutor } = require('../l76-core-arch/index.js');

class APIExecutor extends SkillExecutor {
  constructor(config) {
    super(config);
    this.rateLimiter = new RateLimiter(100, 1000); // 100 requests per second
    this.retryConfig = {
      maxRetries: 3,
      baseDelay: 1000,
      maxDelay: 30000
    };
  }

  async process(options) {
    const { endpoint, method = 'GET', data, headers = {} } = options;
    
    const result = await this.request(endpoint, method, data, headers);
    
    return {
      status: 'success',
      data: result,
      cached: false
    };
  }

  async request(endpoint, method, data, headers) {
    // Check cache first
    const cacheKey = `${method}:${endpoint}:${JSON.stringify(data)}`;
    const cached = await this.getCached(cacheKey);
    if (cached) {
      console.log(`💾 Cache hit: ${cacheKey}`);
      return cached;
    }

    // Rate limiting
    await this.rateLimiter.wait();

    // Execute with retry
    return this.withRetry(async () => {
      console.log(`🌐 ${method} ${endpoint}`);
      
      const result = await exec({
        command: `curl -s -X ${method} ${endpoint} ${this.formatHeaders(headers)} ${this.formatData(data)}`
      });

      if (result.exitCode !== 0) {
        throw new Error(`API request failed: ${result.stderr}`);
      }

      const parsed = JSON.parse(result.stdout);
      
      // Cache successful response
      await this.cache(cacheKey, parsed);
      
      return parsed;
    });
  }

  async withRetry(fn) {
    let lastError;
    
    for (let i = 0; i < this.retryConfig.maxRetries; i++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error;
        
        if (this.isRetryable(error)) {
          const delay = this.calculateDelay(i);
          console.log(`⚠️ Retryable error, waiting ${delay}ms...`);
          await sleep(delay);
        } else {
          throw error; // Non-retryable error
        }
      }
    }
    
    throw lastError;
  }

  isRetryable(error) {
    const message = error.message.toLowerCase();
    return message.includes('timeout') || 
           message.includes('econnreset') || 
           message.includes('503') ||
           message.includes('429');
  }

  calculateDelay(attempt) {
    const delay = this.retryConfig.baseDelay * Math.pow(2, attempt);
    return Math.min(delay, this.retryConfig.maxDelay);
  }

  formatHeaders(headers) {
    return Object.entries(headers)
      .map(([key, value]) => `-H "${key}: ${value}"`)
      .join(' ');
  }

  formatData(data) {
    if (!data) return '';
    return `-d '${JSON.stringify(data)}'`;
  }

  async cache(key, value) {
    // Simple file-based cache
    const cacheDir = './.cache';
    await exec({ command: `mkdir -p ${cacheDir}` });
    
    const cacheFile = `${cacheDir}/${this.hash(key)}.json`;
    const cacheEntry = {
      value,
      timestamp: Date.now(),
      ttl: 3600000 // 1 hour
    };
    
    await write({ path: cacheFile, content: JSON.stringify(cacheEntry) });
  }

  async getCached(key) {
    const cacheDir = './.cache';
    const cacheFile = `${cacheDir}/${this.hash(key)}.json`;
    
    try {
      const content = await read({ path: cacheFile });
      const entry = JSON.parse(content);
      
      if (Date.now() - entry.timestamp > entry.ttl) {
        // Expired
        await exec({ command: `rm -f ${cacheFile}` });
        return null;
      }
      
      return entry.value;
    } catch (e) {
      return null;
    }
  }

  hash(str) {
    // Simple hash for cache key
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(36);
  }
}

class RateLimiter {
  constructor(limit, windowMs) {
    this.limit = limit;
    this.windowMs = windowMs;
    this.tokens = [];
  }

  async wait() {
    const now = Date.now();
    
    // Remove old tokens
    this.tokens = this.tokens.filter(t => now - t < this.windowMs);
    
    if (this.tokens.length >= this.limit) {
      const oldestToken = this.tokens[0];
      const waitTime = this.windowMs - (now - oldestToken);
      console.log(`⏳ Rate limit reached, waiting ${waitTime}ms`);
      await sleep(waitTime);
      return this.wait(); // Recursively check again
    }
    
    this.tokens.push(now);
  }
}

module.exports = { APIExecutor };
```

**Usage:**

```bash
# Fetch from API with automatic retry and rate limiting
node index.js --endpoint "https://api.github.com/repos/openclaw/openclaw" --method GET
```

---

## Example 4: Report Generator Skill

A skill that generates comprehensive reports from multiple data sources.

```javascript
// report-skill/index.js

const { SkillExecutor } = require('../l76-core-arch/index.js');

class ReportExecutor extends SkillExecutor {
  async process(options) {
    const { title, sections, outputPath } = options;
    
    console.log(`📊 Generating report: ${title}`);
    
    // Collect data for all sections
    const sectionData = await this.collectSectionData(sections);
    
    // Generate report
    const report = this.generateReport(title, sectionData);
    
    // Write output
    await write({ path: outputPath, content: report });
    
    console.log(`✅ Report generated: ${outputPath}`);
    
    return {
      status: 'complete',
      outputPath,
      sections: sectionData.map(s => s.name),
      size: report.length
    };
  }

  async collectSectionData(sections) {
    const results = [];
    
    for (const section of sections) {
      console.log(`📋 Collecting: ${section.name}`);
      
      try {
        const data = await this.fetchSectionData(section);
        results.push({
          name: section.name,
          type: section.type,
          data,
          status: 'success'
        });
      } catch (error) {
        results.push({
          name: section.name,
          type: section.type,
          error: error.message,
          status: 'failed'
        });
      }
    }
    
    return results;
  }

  async fetchSectionData(section) {
    switch (section.type) {
      case 'file':
        return await read({ path: section.source });
      
      case 'exec':
        const result = await exec({ command: section.command });
        return result.stdout;
      
      case 'git':
        return await this.fetchGitData(section.command);
      
      case 'system':
        return await this.fetchSystemMetrics();
      
      default:
        throw new Error(`Unknown section type: ${section.type}`);
    }
  }

  async fetchGitData(command) {
    const result = await exec({ command: `git ${command}` });
    return result.stdout;
  }

  async fetchSystemMetrics() {
    const metrics = {};
    
    // Disk usage
    const disk = await exec({ command: 'df -h /' });
    metrics.disk = disk.stdout;
    
    // Memory
    const memory = await exec({ command: 'free -m' });
    metrics.memory = memory.stdout;
    
    // Uptime
    const uptime = await exec({ command: 'uptime' });
    metrics.uptime = uptime.stdout;
    
    return metrics;
  }

  generateReport(title, sections) {
    let report = `# ${title}\n\n`;
    report += `Generated: ${new Date().toISOString()}\n\n`;
    report += `---\n\n`;

    for (const section of sections) {
      report += `## ${section.name}\n\n`;
      
      if (section.status === 'failed') {
        report += `⚠️ **Failed to collect data:** ${section.error}\n\n`;
      } else {
        report += this.formatSectionData(section.type, section.data);
      }
      
      report += `\n---\n\n`;
    }

    report += `## Summary\n\n`;
    report += `- Total sections: ${sections.length}\n`;
    report += `- Successful: ${sections.filter(s => s.status === 'success').length}\n`;
    report += `- Failed: ${sections.filter(s => s.status === 'failed').length}\n`;

    return report;
  }

  formatSectionData(type, data) {
    switch (type) {
      case 'file':
      case 'exec':
      case 'git':
        return `\`\`\`\n${data}\n\`\`\``;
      
      case 'system':
        return Object.entries(data)
          .map(([key, value]) => `### ${key}\n\`\`\`\n${value}\n\`\`\``)
          .join('\n');
      
      default:
        return data;
    }
  }
}

module.exports = { ReportExecutor };
```

**Usage:**

```javascript
// config.json
{
  "title": "Weekly Project Report",
  "sections": [
    { "name": "Git Log", "type": "git", "command": "log --oneline -20" },
    { "name": "Open Issues", "type": "file", "source": "./issues.md" },
    { "name": "System Status", "type": "system" }
  ],
  "outputPath": "./reports/weekly-report.md"
}

// Run
node index.js --config config.json
```

---

## Example 5: Batch Processor with Progress Tracking

```javascript
// batch-skill/index.js

const { SkillExecutor } = require('../l76-core-arch/index.js');

class BatchExecutor extends SkillExecutor {
  async process(options) {
    const { items, batchSize = 10, processor } = options;
    
    console.log(`📦 Processing ${items.length} items (batch size: ${batchSize})`);
    
    const results = [];
    const errors = [];
    let processed = 0;

    for (let i = 0; i < items.length; i += batchSize) {
      const batch = items.slice(i, i + batchSize);
      const batchNum = Math.floor(i / batchSize) + 1;
      const totalBatches = Math.ceil(items.length / batchSize);
      
      console.log(`🔄 Batch ${batchNum}/${totalBatches}`);
      
      const batchResults = await Promise.allSettled(
        batch.map((item, idx) => this.processItem(item, processor, i + idx))
      );
      
      for (let j = 0; j < batchResults.length; j++) {
        const result = batchResults[j];
        const globalIdx = i + j;
        
        if (result.status === 'fulfilled') {
          results.push({ index: globalIdx, ...result.value });
        } else {
          errors.push({ index: globalIdx, error: result.reason.message });
        }
      }
      
      processed += batch.length;
      
      // Update progress
      this.state.update({
        progress: {
          processed,
          total: items.length,
          percent: Math.round(processed / items.length * 100),
          batch: batchNum,
          totalBatches,
          errors: errors.length
        },
        lastUpdate: new Date().toISOString()
      });
    }

    return {
      status: 'complete',
      total: items.length,
      successful: results.length,
      failed: errors.length,
      results,
      errors
    };
  }

  async processItem(item, processor, index) {
    console.log(`  Processing item ${index + 1}`);
    
    switch (processor) {
      case 'read':
        return { content: await read({ path: item }) };
      
      case 'exec':
        const result = await exec({ command: item.command });
        return { output: result.stdout, exitCode: result.exitCode };
      
      case 'transform':
        const content = await read({ path: item.source });
        const transformed = this.transform(content, item.options);
        await write({ path: item.target, content: transformed });
        return { source: item.source, target: item.target };
      
      default:
        throw new Error(`Unknown processor: ${processor}`);
    }
  }

  transform(content, options = {}) {
    // Example transformations
    if (options.uppercase) {
      content = content.toUpperCase();
    }
    if (options.lowercase) {
      content = content.toLowerCase();
    }
    if (options.trim) {
      content = content.trim();
    }
    return content;
  }
}

module.exports = { BatchExecutor };
```

**Usage:**

```javascript
// Process multiple files
const files = ['file1.txt', 'file2.txt', 'file3.txt'];
await executor.execute({
  items: files,
  batchSize: 2,
  processor: 'read'
});

// Transform files
const transforms = [
  { source: 'input1.md', target: 'output1.md', options: { uppercase: true } },
  { source: 'input2.md', target: 'output2.md', options: { lowercase: true } }
];
await executor.execute({
  items: transforms,
  batchSize: 5,
  processor: 'transform'
});
```

---

## Integration Examples

### Combining Multiple Examples

```javascript
// advanced-skill/index.js

const { PipelineExecutor } = require('../pipeline-skill');
const { APIExecutor } = require('../api-skill');
const { ReportExecutor } = require('../report-skill');
const { BatchExecutor } = require('../batch-skill');

class AdvancedSkillExecutor extends PipelineExecutor {
  constructor(config) {
    super(config);
    
    // Override stages with advanced implementations
    this.stages = [
      { name: 'fetch', fn: this.fetchData.bind(this) },
      { name: 'process', fn: this.processData.bind(this) },
      { name: 'analyze', fn: this.analyzeData.bind(this) },
      { name: 'report', fn: this.generateReport.bind(this) }
    ];
    
    this.api = new APIExecutor(config);
    this.batch = new BatchExecutor(config);
    this.report = new ReportExecutor(config);
  }

  async fetchData(data, options) {
    // Fetch from multiple APIs
    const endpoints = [
      'https://api.example.com/data1',
      'https://api.example.com/data2'
    ];
    
    const results = await this.batch.execute({
      items: endpoints.map(url => ({ endpoint: url })),
      processor: 'api'
    });
    
    return results;
  }

  async processData(data, options) {
    // Process fetched data
    return data;
  }

  async analyzeData(data, options) {
    // Analyze processed data
    return { insights: 'Analysis results' };
  }

  async generateReport(analysis, options) {
    // Generate final report
    return this.report.execute({
      title: 'Analysis Report',
      sections: [{ name: 'Insights', type: 'file', source: analysis }],
      outputPath: './report.md'
    });
  }
}

module.exports = { AdvancedSkillExecutor };
```

---

**Last Updated:** 2026-03-22  
**Version:** 1.0.0  
**Maintainer:** openclaw
