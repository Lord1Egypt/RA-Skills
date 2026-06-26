#!/usr/bin/env node
/**
 * Node.js Auto Debugger v2
 * 
 * Scans an ENTIRE Node.js project for issues:
 * - Backend: Express/Fastify routes, error handling, secrets, undefined vars
 * - Frontend: Next.js/React hydration, missing 'use client', SSR issues, wagmi/RainbowKit
 * - Config: package.json, tsconfig, next.config, missing deps
 * - Build: Runs next build and captures errors
 * 
 * Usage: node node-auto-debugger.js <project-dir>
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');

class NodeDebugger {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.issues = [];
    this.name = path.basename(projectDir);
  }

  log(msg) { console.log(`[debugger] ${msg}`); }

  // Recursively find all source files
  findFiles(extensions, excludeDirs = ['node_modules', '.next', 'dist', 'build', '.git']) {
    const files = [];
    const scan = (dir) => {
      if (!fs.existsSync(dir)) return;
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && !excludeDirs.includes(entry.name) && !entry.name.startsWith('.')) {
          scan(fullPath);
        } else if (entry.isFile() && extensions.some(ext => entry.name.endsWith(ext))) {
          files.push(fullPath);
        }
      }
    };
    scan(this.projectDir);
    return files;
  }

  // ─── BACKEND CHECKS ─────────────────────────────────────

  checkBackendSecrets(files) {
    const backendFiles = files.filter(f => !f.includes('/app/') && !f.includes('/components/') && !f.includes('/pages/'));
    const secretPatterns = [
      { pattern: /(?:password|secret|api.?key|private.?key|token)\s*[:=]\s*['"][^'"]{10,}/gi, name: 'Potential secret' },
      { pattern: /0x[a-fA-F0-9]{64}/g, name: 'Private key' }
    ];
    
    for (const file of backendFiles) {
      const content = fs.readFileSync(file, 'utf8');
      if (content.includes('process.env') && content.includes('.env')) continue;
      const lines = content.split('\n');
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.trim().startsWith('//') || line.trim().startsWith('*')) continue;
        for (const { pattern, name } of secretPatterns) {
          pattern.lastIndex = 0;
          if (pattern.test(line) && !line.includes('process.env') && !line.includes('pass show')) {
            this.issues.push({ type: 'secret', file: this.rel(file), line: i+1, severity: 'critical', msg: `${name} may be hardcoded` });
          }
        }
      }
    }
  }

  checkAsyncRoutes(files) {
    const routeFiles = files.filter(f => /server|app|route|api/i.test(f) && !f.includes('.test.'));
    for (const file of routeFiles) {
      const content = fs.readFileSync(file, 'utf8');
      const matches = content.matchAll(/(?:app|fastify)\.(get|post|put|delete|patch)\s*\([^)]*async\s*\([^)]*\)\s*=>/g);
      for (const match of matches) {
        const idx = match.index;
        const bodyStart = content.indexOf('{', idx);
        if (bodyStart === -1) continue;
        const snippet = content.substring(bodyStart, bodyStart + 300);
        if (!snippet.includes('try') && !snippet.includes('catch')) {
          const line = content.substring(0, idx).split('\n').length;
          this.issues.push({ type: 'error-handling', file: this.rel(file), line, severity: 'high', msg: `Async ${match[1].toUpperCase()} route missing try/catch` });
        }
      }
    }
  }

  checkUndefinedVars(files) {
    const routeFiles = files.filter(f => /server|app|route|index/i.test(f) && !f.includes('.test.') && !f.includes('.tsx'));
    for (const file of routeFiles) {
      const content = fs.readFileSync(file, 'utf8');
      const lines = content.split('\n');
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const pushMatch = line.match(/^\s*(\w+)\.push\(/);
        if (pushMatch) {
          const v = pushMatch[1];
          if (['req', 'res', 'next', 'console', 'process', 'fs', 'path', 'Math', 'JSON', 'Object', 'Array', 'Promise'].includes(v)) continue;
          if (!content.includes(`const ${v}`) && !content.includes(`let ${v}`) && !content.includes(`var ${v}`) && !content.includes(`${v} =`)) {
            this.issues.push({ type: 'undefined', file: this.rel(file), line: i+1, severity: 'critical', msg: `Variable '${v}' may be undefined` });
          }
        }
      }
    }
  }

  // ─── FRONTEND CHECKS ─────────────────────────────────────

  checkClientDirectives(files) {
    const tsxFiles = files.filter(f => f.endsWith('.tsx'));
    for (const file of tsxFiles) {
      const content = fs.readFileSync(file, 'utf8');
      // Check for hooks without 'use client'
      const usesHooks = /use(State|Effect|Ref|Callback|Memo|Context|Reducer|Layout)/.test(content);
      const usesWindow = /window\./.test(content);
      const usesDocument = /document\./.test(content);
      const hasDirective = content.trimStart().startsWith("'use client'") || content.trimStart().startsWith('"use client"');
      
      if ((usesHooks || usesWindow || usesDocument) && !hasDirective) {
        this.issues.push({ type: 'missing-use-client', file: this.rel(file), line: 1, severity: 'high', msg: 'Uses hooks/browser API but missing "use client" directive' });
      }
    }
  }

  checkHydrationIssues(files) {
    const tsxFiles = files.filter(f => f.endsWith('.tsx') && f.includes('/app/'));
    for (const file of tsxFiles) {
      const content = fs.readFileSync(file, 'utf8');
      // Check for Date.now(), new Date() in render (different on server/client)
      const dateMatches = content.matchAll(/(?:Date\.now|new Date\(\))/g);
      for (const match of dateMatches) {
        const line = content.substring(0, match.index).split('\n').length;
        this.issues.push({ type: 'hydration-risk', file: this.rel(file), line, severity: 'medium', msg: 'Date.now()/new Date() can cause hydration mismatch — use useEffect or suppressHydrationWarning' });
      }
      
      // Check for Math.random() in render
      const randMatches = content.matchAll(/Math\.random\(\)/g);
      for (const match of randMatches) {
        const line = content.substring(0, match.index).split('\n').length;
        this.issues.push({ type: 'hydration-risk', file: this.rel(file), line, severity: 'medium', msg: 'Math.random() can cause hydration mismatch — use useEffect' });
      }

      // Check for direct window/document access (not in useEffect)
      const windowMatches = content.matchAll(/(?:window|document)\.[a-zA-Z]+/g);
      for (const match of windowMatches) {
        const line = content.substring(0, match.index).split('\n').length;
        const lineContent = content.split('\n')[line-1];
        // Skip if inside useEffect or conditional
        const blockBefore = content.substring(Math.max(0, match.index - 500), match.index);
        if (!blockBefore.includes('useEffect') && !blockBefore.includes('typeof window')) {
          this.issues.push({ type: 'ssr-error', file: this.rel(file), line, severity: 'high', msg: `${match[0]} accessed outside useEffect — will crash during SSR` });
        }
      }
    }
  }

  checkWagmiIssues(files) {
    const tsxFiles = files.filter(f => f.endsWith('.tsx') || f.endsWith('.ts'));
    for (const file of tsxFiles) {
      const content = fs.readFileSync(file, 'utf8');
      
      // Check for useAccount/useContractRead without proper loading state
      if (content.includes('useAccount') || content.includes('useContractRead') || content.includes('useBalance')) {
        if (!content.includes('isLoading') && !content.includes('isFetching') && !content.includes('isSuccess')) {
          this.issues.push({ type: 'wagmi-loading', file: this.rel(file), line: 1, severity: 'medium', msg: 'Uses wagmi hooks but may miss loading states — can cause flash of empty content' });
        }
      }

      // Check for chainId hardcoding
      const chainMatch = content.match(/chainId:\s*(\d+)/);
      if (chainMatch) {
        this.issues.push({ type: 'hardcoded-chain', file: this.rel(file), line: 1, severity: 'low', msg: `Chain ID ${chainMatch[1]} is hardcoded — consider using configured chain` });
      }
    }
  }

  checkNextConfig() {
    const nextConfig = path.join(this.projectDir, 'next.config.js');
    const nextConfigTs = path.join(this.projectDir, 'next.config.ts');
    if (!fs.existsSync(nextConfig) && !fs.existsSync(nextConfigTs)) {
      this.issues.push({ type: 'missing-config', file: 'next.config.js', line: 1, severity: 'low', msg: 'No next.config.js found — using defaults' });
    }
  }

  checkPackageJson() {
    const pkgPath = path.join(this.projectDir, 'package.json');
    if (!fs.existsSync(pkgPath)) {
      this.issues.push({ type: 'missing-pkg', file: 'package.json', line: 1, severity: 'critical', msg: 'No package.json found' });
      return;
    }
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
    
    // Check for missing build script
    if (!pkg.scripts?.build) {
      this.issues.push({ type: 'missing-script', file: 'package.json', line: 1, severity: 'medium', msg: 'No "build" script defined' });
    }

    // Check for common missing dependencies
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };
    if (deps.next && !deps.typescript && !fs.existsSync('tsconfig.json')) {
      this.issues.push({ type: 'missing-dep', file: 'package.json', line: 1, severity: 'medium', msg: 'Next.js project without TypeScript' });
    }
  }

  // ─── BUILD CHECK ─────────────────────────────────────────

  checkBuild() {
    const pkgPath = path.join(this.projectDir, 'package.json');
    if (!fs.existsSync(pkgPath)) return;
    
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
    if (!pkg.scripts?.build) return;

    this.log('Running build check...');
    const result = spawnSync('npm', ['run', 'build'], {
      cwd: this.projectDir,
      encoding: 'utf8',
      timeout: 120000,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    const output = (result.stdout || '') + '\n' + (result.stderr || '');
    
    // Parse build errors
    const errorLines = output.split('\n').filter(l => /error|Error|ERROR/.test(l) && !l.includes('node_modules'));
    for (const line of errorLines.slice(0, 10)) {
      // Try to extract file and line from error message
      const fileMatch = line.match(/([\w/.-]+\.(?:tsx?|jsx?)):(\d+)/);
      if (fileMatch) {
        this.issues.push({ type: 'build-error', file: fileMatch[1], line: parseInt(fileMatch[2]), severity: 'critical', msg: line.trim().substring(0, 120) });
      } else if (line.trim().length > 10) {
        this.issues.push({ type: 'build-error', file: 'build', line: 0, severity: 'high', msg: line.trim().substring(0, 120) });
      }
    }

    if (result.status !== 0 && errorLines.length === 0) {
      this.issues.push({ type: 'build-failed', file: 'build', line: 0, severity: 'critical', msg: 'Build failed — check output manually' });
    }
  }

  // ─── HELPERS ─────────────────────────────────────────────

  rel(file) { return path.relative(this.projectDir, file); }

  // ─── MAIN SCAN ───────────────────────────────────────────

  scan(options = {}) {
    this.log(`Scanning ${this.name}...`);
    
    const allFiles = this.findFiles(['.js', '.ts', '.tsx', '.jsx']);
    this.log(`Found ${allFiles.length} source files`);

    // Backend
    this.checkBackendSecrets(allFiles);
    this.checkAsyncRoutes(allFiles);
    this.checkUndefinedVars(allFiles);

    // Frontend
    this.checkClientDirectives(allFiles);
    this.checkHydrationIssues(allFiles);
    this.checkWagmiIssues(allFiles);

    // Config
    this.checkNextConfig();
    this.checkPackageJson();

    // Build (only if requested)
    if (options.runBuild) {
      this.checkBuild();
    }

    // Dedupe
    const seen = new Set();
    this.issues = this.issues.filter(i => {
      const k = `${i.type}:${i.file}:${i.line}`;
      if (seen.has(k)) return false;
      seen.add(k);
      return true;
    });

    // Sort
    const sev = { critical: 0, high: 1, medium: 2, low: 3 };
    this.issues.sort((a, b) => sev[a.severity] - sev[b.severity]);

    return this.issues;
  }

  report() {
    const c = this.issues.filter(i => i.severity === 'critical').length;
    const h = this.issues.filter(i => i.severity === 'high').length;
    const m = this.issues.filter(i => i.severity === 'medium').length;
    const l = this.issues.filter(i => i.severity === 'low').length;

    let out = `# Auto Debugger Report: ${this.name}\n\n`;
    out += `**Scanned:** ${new Date().toISOString()}\n`;
    out += `**Issues:** ${this.issues.length} (🔴 ${c} Critical | 🟠 ${h} High | 🟡 ${m} Medium | 🟢 ${l} Low)\n\n`;

    if (!this.issues.length) {
      out += `✅ No issues found!\n`;
      return out;
    }

    // Group by severity
    for (const sev of ['critical', 'high', 'medium', 'low']) {
      const items = this.issues.filter(i => i.severity === sev);
      if (!items.length) continue;
      const icon = { critical: '🔴', high: '🟠', medium: '🟡', low: '🟢' }[sev];
      out += `## ${icon} ${sev.charAt(0).toUpperCase() + sev.slice(1)} (${items.length})\n\n`;
      for (const i of items) {
        out += `- **\`${i.file}:${i.line}\`** — ${i.msg}\n`;
      }
      out += '\n';
    }

    return out;
  }
}

// CLI
if (require.main === module) {
  const projectDir = process.argv[2] || '.';
  const runBuild = process.argv.includes('--build');
  const nodeDebugger = new NodeDebugger(projectDir);
  const issues = nodeDebugger.scan({ runBuild });
  const report = nodeDebugger.report();
  console.log(report);
  
  fs.writeFileSync(path.join(projectDir, 'AUTO-DEBUG-REPORT.md'), report);
  console.log(`Report: ${path.join(projectDir, 'AUTO-DEBUG-REPORT.md')}`);
  
  process.exit(issues.filter(i => i.severity === 'critical').length > 0 ? 1 : 0);
}

module.exports = NodeDebugger;
