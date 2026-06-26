# L76 Core Architecture - Extension Points Guide

Extend, customize, and build upon the L76 Core Architecture for advanced use cases.

## Extension Architecture

The L76 architecture is designed for extensibility at multiple layers:

```
┌─────────────────────────────────────────┐
│         Skill-Specific Logic            │  ← Extend here for new features
├─────────────────────────────────────────┤
│         SkillExecutor Class             │  ← Override methods for custom workflows
├─────────────────────────────────────────┤
│         StateManager Class              │  ← Extend for custom persistence
├─────────────────────────────────────────┤
│         Tool Integration Layer          │  ← Add custom tool wrappers
├─────────────────────────────────────────┤
│         OpenClaw Runtime                │  ← Base layer (don't modify)
└─────────────────────────────────────────┘
```

---

## Extension Point 1: Custom SkillExecutor

Extend the base `SkillExecutor` to add domain-specific logic.

### Base Class (from index.js)

```javascript
class SkillExecutor {
  async preflight() { /* ... */ }
  async execute(options) { /* ... */ }
  async initialize(options) { /* ... */ }
  async process(options) { /* ... */ }
  async finalize(result) { /* ... */ }
}
```

### Extension Pattern

```javascript
// custom-executor.js
const { SkillExecutor } = require('./index.js');

class CustomSkillExecutor extends SkillExecutor {
  constructor(config) {
    super(config);
    // Add custom properties
    this.customConfig = config.custom || {};
  }

  // Override preflight for custom checks
  async preflight() {
    await super.preflight(); // Run base checks
    
    // Add custom checks
    const customCheck = await this.verifyCustomPrereq();
    if (!customCheck.pass) {
      throw new Error(`Custom prerequisite failed: ${customCheck.reason}`);
    }
    
    return { success: true };
  }

  // Override process for custom logic
  async process(options) {
    // Custom preprocessing
    await this.customSetup();
    
    // Call parent or implement entirely new logic
    const result = await super.process(options);
    
    // Custom postprocessing
    await this.customTeardown(result);
    
    return result;
  }

  // New custom methods
  async verifyCustomPrereq() {
    // Your custom logic
    return { pass: true };
  }

  async customSetup() {
    // Setup before main processing
  }

  async customTeardown(result) {
    // Cleanup after main processing
  }
}

module.exports = { CustomSkillExecutor };
```

### Usage Example: File Processing Skill

```javascript
// file-processor/index.js
const { SkillExecutor, StateManager } = require('../l76-core-arch/index.js');

class FileProcessorExecutor extends SkillExecutor {
  async process(options) {
    const { targetDir, pattern } = options;
    
    // Discover files
    const files = await this.discoverFiles(targetDir, pattern);
    
    // Process with progress tracking
    const results = [];
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const result = await this.processFile(file);
      results.push(result);
      
      // Update progress in state
      this.state.update({
        progress: {
          current: i + 1,
          total: files.length,
          percent: Math.round((i + 1) / files.length * 100)
        }
      });
    }
    
    return { files: results };
  }

  async discoverFiles(dir, pattern) {
    const result = await exec({ 
      command: `find ${dir} -name "${pattern}" -type f`
    });
    return result.stdout.split('\n').filter(Boolean);
  }

  async processFile(filePath) {
    const content = await read({ path: filePath });
    const processed = this.transform(content);
    await write({ path: filePath, content: processed });
    return { file: filePath, status: 'done' };
  }

  transform(content) {
    // Custom transformation logic
    return content.toUpperCase();
  }
}

module.exports = { FileProcessorExecutor };
```

---

## Extension Point 2: Custom StateManager

Extend state management for domain-specific persistence.

### Extension Pattern

```javascript
// custom-state.js
const { StateManager } = require('./index.js');

class AdvancedStateManager extends StateManager {
  constructor(stateFile, options = {}) {
    super(stateFile);
    this.backupEnabled = options.backup !== false;
    this.maxHistory = options.maxHistory || 100;
  }

  // Override save to add backup
  save() {
    if (this.backupEnabled) {
      this.createBackup();
    }
    super.save();
  }

  // Add versioned state
  setVersioned(key, value, version) {
    if (!this.state.versions) {
      this.state.versions = {};
    }
    if (!this.state.versions[key]) {
      this.state.versions[key] = [];
    }
    
    this.state.versions[key].push({ version, value, timestamp: Date.now() });
    
    // Trim old versions
    if (this.state.versions[key].length > this.maxHistory) {
      this.state.versions[key] = this.state.versions[key].slice(-this.maxHistory);
    }
    
    this.save();
  }

  getVersioned(key, version) {
    const versions = this.state.versions?.[key] || [];
    const entry = versions.find(v => v.version === version);
    return entry?.value;
  }

  // Add rollback capability
  rollback(key, steps = 1) {
    const versions = this.state.versions?.[key] || [];
    if (versions.length <= steps) {
      throw new Error('Cannot rollback: not enough history');
    }
    const target = versions[versions.length - steps - 1];
    this.state[key] = target.value;
    this.save();
    return target;
  }

  createBackup() {
    const backupFile = this.stateFile + `.backup.${Date.now()}`;
    try {
      fs.copyFileSync(this.stateFile, backupFile);
      
      // Keep only last 5 backups
      const backups = fs.readdirSync(path.dirname(this.stateFile))
        .filter(f => f.startsWith(path.basename(this.stateFile) + '.backup.'))
        .sort()
        .reverse();
      
      backups.slice(5).forEach(b => {
        fs.unlinkSync(path.join(path.dirname(this.stateFile), b));
      });
    } catch (e) {
      console.warn('Backup failed:', e.message);
    }
  }
}

module.exports = { AdvancedStateManager };
```

---

## Extension Point 3: Custom Tool Wrappers

Create reusable tool wrappers with built-in error handling and logging.

### Pattern

```javascript
// tools/wrapped-tools.js

/**
 * Wrapped read with retry and logging
 */
async function readWithRetry(path, options = {}) {
  const { maxRetries = 3, timeout = 30000 } = options;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      console.log(`📖 Reading: ${path} (attempt ${i + 1}/${maxRetries})`);
      const content = await read({ path, timeout });
      console.log(`✅ Read successful: ${path}`);
      return content;
    } catch (error) {
      console.warn(`⚠️ Read failed: ${path} - ${error.message}`);
      
      if (i === maxRetries - 1) {
        throw error;
      }
      
      // Exponential backoff
      await sleep(1000 * Math.pow(2, i));
    }
  }
}

/**
 * Wrapped exec with timeout and output validation
 */
async function execWithValidation(command, options = {}) {
  const { 
    timeout = 30, 
    expectNonEmpty = true, 
    allowedExitCodes = [0] 
  } = options;
  
  console.log(`⚙️ Executing: ${command}`);
  const start = Date.now();
  
  const result = await exec({ command, timeout });
  const duration = Date.now() - start;
  
  console.log(`✅ Completed in ${duration}ms (exit code: ${result.exitCode})`);
  
  // Validate exit code
  if (!allowedExitCodes.includes(result.exitCode)) {
    throw new Error(`Command failed with exit code ${result.exitCode}: ${result.stderr}`);
  }
  
  // Validate output
  if (expectNonEmpty && !result.stdout?.trim()) {
    throw new Error('Command produced no output');
  }
  
  return result;
}

/**
 * Wrapped write with atomic operation
 */
async function writeAtomic(path, content, options = {}) {
  const { backup = true } = options;
  
  // Backup existing file
  if (backup && fs.existsSync(path)) {
    const backupPath = path + `.backup.${Date.now()}`;
    fs.copyFileSync(path, backupPath);
    console.log(`💾 Backup created: ${backupPath}`);
  }
  
  // Write to temp file first
  const tempPath = path + '.tmp';
  await write({ path: tempPath, content });
  
  // Atomic rename
  fs.renameSync(tempPath, path);
  console.log(`✍️ Written: ${path}`);
}

/**
 * Batch tool call with concurrency limit
 */
async function batchRead(paths, concurrency = 5) {
  const results = [];
  const executing = [];
  
  for (const path of paths) {
    const promise = readWithRetry(path).then(content => {
      results.push({ path, content, status: 'success' });
      executing.splice(executing.indexOf(promise), 1);
      return content;
    }).catch(error => {
      results.push({ path, error: error.message, status: 'failed' });
      executing.splice(executing.indexOf(promise), 1);
    });
    
    executing.push(promise);
    
    if (executing.length >= concurrency) {
      await Promise.race(executing);
    }
  }
  
  await Promise.all(executing);
  return results;
}

module.exports = { 
  readWithRetry, 
  execWithValidation, 
  writeAtomic, 
  batchRead 
};
```

---

## Extension Point 4: Plugin System

Create a plugin architecture for modular skill extensions.

### Plugin Interface

```javascript
// plugins/plugin-interface.js

/**
 * Base plugin class - extend this for custom plugins
 */
class SkillPlugin {
  constructor(skillExecutor) {
    this.executor = skillExecutor;
    this.name = this.constructor.name;
  }

  /**
   * Called during skill initialization
   */
  async onInit(options) {
    // Override in subclass
  }

  /**
   * Called before main processing
   */
  async onBeforeProcess(options) {
    // Override in subclass
  }

  /**
   * Called after main processing
   */
  async onAfterProcess(result) {
    // Override in subclass
  }

  /**
   * Called on error
   */
  async onError(error) {
    // Override in subclass
  }

  /**
   * Called during finalization
   */
  async onFinalize(result) {
    // Override in subclass
  }
}

module.exports = { SkillPlugin };
```

### Plugin Manager

```javascript
// plugins/plugin-manager.js

class PluginManager {
  constructor() {
    this.plugins = [];
  }

  register(plugin) {
    this.plugins.push(plugin);
    console.log(`🔌 Plugin registered: ${plugin.name}`);
  }

  async broadcast(hook, ...args) {
    const results = [];
    for (const plugin of this.plugins) {
      try {
        if (typeof plugin[hook] === 'function') {
          const result = await plugin[hook](...args);
          results.push({ plugin: plugin.name, result });
        }
      } catch (error) {
        console.error(`Plugin ${plugin.name} failed on ${hook}:`, error.message);
        results.push({ plugin: plugin.name, error: error.message });
      }
    }
    return results;
  }
}

module.exports = { PluginManager };
```

### Example Plugin: Logging Plugin

```javascript
// plugins/logging-plugin.js

const { SkillPlugin } = require('./plugin-interface');

class LoggingPlugin extends SkillPlugin {
  constructor(executor, options = {}) {
    super(executor);
    this.logFile = options.logFile || 'skill.log';
    this.verbose = options.verbose || false;
  }

  async onInit(options) {
    await this.log('INIT', 'Skill initialized', options);
  }

  async onBeforeProcess(options) {
    await this.log('BEFORE_PROCESS', 'Starting processing', options);
  }

  async onAfterProcess(result) {
    await this.log('AFTER_PROCESS', 'Processing complete', result);
  }

  async onError(error) {
    await this.log('ERROR', 'Error occurred', { message: error.message, stack: error.stack });
  }

  async onFinalize(result) {
    await this.log('FINALIZE', 'Skill finalized', result);
  }

  async log(level, message, data) {
    const entry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      data,
      plugin: this.name
    };

    if (this.verbose) {
      console.log(`[${level}] ${message}`);
    }

    // Append to log file
    const logEntry = JSON.stringify(entry) + '\n';
    try {
      await exec({ 
        command: `echo ${JSON.stringify(logEntry)} >> ${this.logFile}` 
      });
    } catch (e) {
      console.warn('Failed to write log:', e.message);
    }
  }
}

module.exports = { LoggingPlugin };
```

### Using Plugins

```javascript
// index.js with plugin support

const { SkillExecutor } = require('./index.js');
const { PluginManager } = require('./plugins/plugin-manager');
const { LoggingPlugin } = require('./plugins/logging-plugin');

class PluginEnabledExecutor extends SkillExecutor {
  constructor(config) {
    super(config);
    this.pluginManager = new PluginManager();
    this.registerDefaultPlugins();
  }

  registerDefaultPlugins() {
    this.pluginManager.register(new LoggingPlugin(this, { 
      logFile: 'skill.log',
      verbose: true
    }));
  }

  async initialize(options) {
    await super.initialize(options);
    await this.pluginManager.broadcast('onInit', options);
  }

  async process(options) {
    await this.pluginManager.broadcast('onBeforeProcess', options);
    
    try {
      const result = await super.process(options);
      await this.pluginManager.broadcast('onAfterProcess', result);
      return result;
    } catch (error) {
      await this.pluginManager.broadcast('onError', error);
      throw error;
    }
  }

  async finalize(result) {
    await this.pluginManager.broadcast('onFinalize', result);
    await super.finalize(result);
  }
}

module.exports = { PluginEnabledExecutor };
```

---

## Extension Point 5: Custom Validation Rules

Extend the validation script for skill-specific checks.

### Pattern

```powershell
# scripts/validate-custom.ps1

param(
    [string]$SkillDir = (Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent),
    [string]$CustomRulesDir = (Join-Path $SkillDir "validation-rules")
)

# Load base validation
& (Join-Path $SkillDir "scripts/validate.ps1")

Write-Host ""
Write-Host "🔧 Running custom validation rules..." -ForegroundColor Cyan

# Load and execute custom rules
if (Test-Path $CustomRulesDir) {
    Get-ChildItem $CustomRulesDir -Filter "*.ps1" | ForEach-Object {
        Write-Host "  Loading rule: $($_.Name)" -ForegroundColor Gray
        & $_.FullName -SkillDir $SkillDir
    }
} else {
    Write-Host "⚠️  No custom rules directory found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Custom validation complete!" -ForegroundColor Green
```

### Example Custom Rule

```powershell
# validation-rules/check-license.ps1

param([string]$SkillDir)

$LICENSE_FILE = Join-Path $SkillDir "LICENSE"

if (-not (Test-Path $LICENSE_FILE)) {
    Write-Host "⚠️  Missing LICENSE file" -ForegroundColor Yellow
    Write-Host "  Consider adding a LICENSE file for clarity" -ForegroundColor Gray
} else {
    Write-Host "✅ LICENSE file present" -ForegroundColor Green
}

# Check for common license types
$content = Get-Content $LICENSE_FILE -Raw
if ($content -match "MIT License") {
    Write-Host "  License type: MIT" -ForegroundColor Gray
} elseif ($content -match "Apache License") {
    Write-Host "  License type: Apache 2.0" -ForegroundColor Gray
}
```

---

## Extension Checklist

When extending the L76 architecture:

- [ ] **Preserve base behavior** - Call `super.method()` when overriding
- [ ] **Document extensions** - Add comments explaining custom logic
- [ ] **Test independently** - Verify extensions work in isolation
- [ ] **Handle errors gracefully** - Don't let extensions break core flow
- [ ] **Maintain backwards compatibility** - Don't break existing skills
- [ ] **Update validation** - Add rules for new extension points
- [ ] **Performance test** - Ensure extensions don't degrade performance

---

## Example: Complete Extended Skill

See `references/examples-advanced.md` for a complete example of an extended skill using all extension points.

---

**Last Updated:** 2026-03-22  
**Version:** 1.0.0  
**Maintainer:** openclaw
