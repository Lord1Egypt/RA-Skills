#!/usr/bin/env node
/**
 * portable-deployment-audit
 * Read-only, target-driven security audit with pure JSON output.
 * This version does not execute external binaries; it inspects files only.
 */

const fs = require('fs');
const os = require('os');
const path = require('path');

const DEFAULT_EXTENSIONS = [
  '.js', '.cjs', '.mjs', '.ts', '.tsx', '.jsx', '.java', '.kt', '.groovy',
  '.json', '.env', '.yml', '.yaml', '.properties', '.conf', '.ini', '.xml'
];

const DEFAULT_IGNORED_DIRS = new Set([
  '.git', 'node_modules', 'dist', 'build', '.next', '.idea', '.vscode', 'coverage', 'target', 'out'
]);

const DEFAULT_CHECKS = ['credentials', 'ports', 'configs', 'permissions', 'docker', 'git'];
const UNIX_LIKE = new Set(['linux', 'darwin', 'freebsd', 'openbsd', 'sunos', 'aix']);
const COMMON_EXPOSED_PORTS = new Set([
  21, 22, 23, 25, 53, 80, 110, 123, 143, 389, 443, 445, 465, 587, 636,
  1433, 1521, 2049, 2375, 2376, 3000, 3306, 3389, 4000, 5000, 5432, 5601,
  5672, 5900, 6379, 6443, 8000, 8008, 8080, 8081, 8443, 9000, 9200, 9300,
  10000, 11211, 15672, 27017
]);

function parseArgs(argv) {
  const options = {
    target: process.cwd(),
    format: 'text',
    envFile: null,
    dockerfile: null,
    checks: [],
    excludeDirs: [],
    allowPorts: [],
    strict: false,
    fixRequested: false,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];

    switch (arg) {
      case '--help':
      case '-h':
        options.help = true;
        break;
      case '--target':
        options.target = argv[++i];
        break;
      case '--env-file':
        options.envFile = argv[++i];
        break;
      case '--dockerfile':
        options.dockerfile = argv[++i];
        break;
      case '--format':
        options.format = (argv[++i] || '').toLowerCase();
        break;
      case '--json':
        options.format = 'json';
        break;
      case '--check': {
        const raw = argv[++i] || '';
        options.checks.push(...raw.split(',').map(s => s.trim().toLowerCase()).filter(Boolean));
        break;
      }
      case '--exclude-dir': {
        const raw = argv[++i] || '';
        options.excludeDirs.push(...raw.split(',').map(s => s.trim()).filter(Boolean));
        break;
      }
      case '--allow-port': {
        const raw = argv[++i] || '';
        options.allowPorts.push(...raw.split(',').map(s => Number.parseInt(s.trim(), 10)).filter(Number.isInteger));
        break;
      }
      case '--full':
        break;
      case '--strict':
        options.strict = true;
        break;
      case '--credentials':
      case '--ports':
      case '--configs':
      case '--permissions':
      case '--docker':
      case '--git':
        options.checks.push(arg.slice(2));
        break;
      case '--fix':
        options.fixRequested = true;
        break;
      default:
        if (!arg.startsWith('--') && !options.targetExplicitConsumed) {
          options.target = arg;
          options.targetExplicitConsumed = true;
        } else {
          throw new Error(`Unknown argument: ${arg}`);
        }
        break;
    }
  }

  options.target = path.resolve(options.target || process.cwd());
  if (options.envFile) options.envFile = path.resolve(options.envFile);
  if (options.dockerfile) options.dockerfile = path.resolve(options.dockerfile);

  if (!['text', 'json'].includes(options.format)) {
    throw new Error(`Unsupported format: ${options.format}`);
  }

  const requestedChecks = options.checks.length > 0 ? Array.from(new Set(options.checks)) : DEFAULT_CHECKS;
  const invalidChecks = requestedChecks.filter(check => !DEFAULT_CHECKS.includes(check));
  if (invalidChecks.length > 0) {
    throw new Error(`Unsupported check(s): ${invalidChecks.join(', ')}`);
  }

  options.checks = requestedChecks;
  options.excludeDirs = Array.from(new Set(options.excludeDirs));
  options.allowPorts = Array.from(new Set(options.allowPorts)).sort((a, b) => a - b);

  return options;
}

function printHelp() {
  console.log(`portable-deployment-audit

Usage:
  node skills/portable-deployment-audit/scripts/audit.cjs [options]

Options:
  --target <dir>         Target directory to audit (default: current directory)
  --env-file <path>      Explicit env file to inspect
  --dockerfile <path>    Explicit Dockerfile path to inspect
  --check <list>         Comma-separated checks: credentials,ports,configs,permissions,docker,git
  --exclude-dir <list>   Comma-separated directory names to skip during file scans
  --allow-port <list>    Comma-separated TCP ports to suppress in port warnings
  --credentials          Run credentials check only (can combine with other single flags)
  --ports                Run network exposure hint checks from config/compose files
  --configs              Run config check
  --permissions          Run permissions check
  --docker               Run Docker and compose checks
  --git                  Run Git filesystem checks
  --format text|json     Output format (default: text)
  --json                 Alias for --format json
  --strict               Exit non-zero on any HIGH finding
  --fix                  Disabled in this read-only rewrite
  --help, -h             Show help
`);
}

function buildRuntime(options) {
  if (!fs.existsSync(options.target) || !fs.statSync(options.target).isDirectory()) {
    throw new Error(`Target directory not found or not a directory: ${options.target}`);
  }

  const runtime = {
    options,
    targetDir: options.target,
    platform: process.platform,
    hostname: os.hostname(),
    startedAt: new Date().toISOString(),
    findings: [],
    ignoredDirs: new Set([...DEFAULT_IGNORED_DIRS, ...options.excludeDirs]),
    allowedPorts: new Set(options.allowPorts),
  };

  runtime.envFiles = discoverEnvFiles(runtime.targetDir, options.envFile);
  runtime.dockerfiles = discoverDockerfiles(runtime.targetDir, options.dockerfile);
  runtime.composeFiles = discoverComposeFiles(runtime.targetDir);
  runtime.configFiles = discoverConfigFiles(runtime.targetDir, runtime.envFiles, runtime.dockerfiles, runtime.composeFiles);
  runtime.sourceFiles = getFilesRecursively(runtime.targetDir, DEFAULT_EXTENSIONS, runtime.ignoredDirs);
  return runtime;
}

function addFinding(runtime, level, category, message, details = null) {
  runtime.findings.push({
    level,
    category,
    message,
    details,
    timestamp: new Date().toISOString(),
  });
}

function discoverEnvFiles(targetDir, explicitPath) {
  const candidates = new Set();
  if (explicitPath) candidates.add(explicitPath);
  ['.env', '.env.local', '.env.production', '.env.development', path.join('skills', '.env')].forEach(rel => {
    candidates.add(path.join(targetDir, rel));
  });
  return Array.from(candidates).filter(fileExists);
}

function discoverDockerfiles(targetDir, explicitPath) {
  const candidates = new Set();
  if (explicitPath) candidates.add(explicitPath);
  ['Dockerfile', path.join('docker', 'Dockerfile')].forEach(rel => candidates.add(path.join(targetDir, rel)));
  return Array.from(candidates).filter(fileExists);
}

function discoverComposeFiles(targetDir) {
  const candidates = new Set();
  ['docker-compose.yml', 'docker-compose.yaml', 'compose.yml', 'compose.yaml'].forEach(rel => {
    candidates.add(path.join(targetDir, rel));
  });
  return Array.from(candidates).filter(fileExists);
}

function discoverConfigFiles(targetDir, envFiles, dockerfiles, composeFiles = []) {
  const candidates = new Set([...envFiles, ...dockerfiles, ...composeFiles]);
  ['config.json', 'application.yml', 'application.yaml', 'application.properties'].forEach(rel => {
    candidates.add(path.join(targetDir, rel));
  });
  return Array.from(candidates).filter(fileExists);
}

function fileExists(filePath) {
  try {
    return fs.existsSync(filePath);
  } catch {
    return false;
  }
}

function readUtf8(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch {
    return null;
  }
}

function getFilesRecursively(dir, extensions = DEFAULT_EXTENSIONS, ignoredDirs = DEFAULT_IGNORED_DIRS) {
  const files = [];

  function walk(currentDir) {
    let entries = [];
    try {
      entries = fs.readdirSync(currentDir, { withFileTypes: true });
    } catch {
      return;
    }

    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        if (!ignoredDirs.has(entry.name)) {
          walk(fullPath);
        }
        continue;
      }

      if (extensions.some(ext => entry.name.endsWith(ext))) {
        files.push(fullPath);
      }
    }
  }

  walk(dir);
  return files;
}

function relativeToTarget(runtime, filePath) {
  return path.relative(runtime.targetDir, filePath) || '.';
}

function scanFileForPatterns(runtime, filePath, patterns, category) {
  const content = readUtf8(filePath);
  if (content == null) return;

  for (const pattern of patterns) {
    pattern.regex.lastIndex = 0;
    if (pattern.regex.test(content)) {
      addFinding(runtime, pattern.level, category, pattern.message, {
        file: relativeToTarget(runtime, filePath),
        match: pattern.match,
      });
    }
  }
}

function countByLevel(findings) {
  return findings.reduce((acc, finding) => {
    acc[finding.level] = (acc[finding.level] || 0) + 1;
    return acc;
  }, { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0, INFO: 0 });
}

function uniqueFiles(files) {
  return Array.from(new Set(files));
}

function checkCredentials(runtime) {
  addFinding(runtime, 'INFO', 'CREDENTIALS', 'Starting credential scan', {
    filesPlanned: runtime.sourceFiles.length,
  });

  const highConfidencePatterns = [
    {
      level: 'CRITICAL',
      message: 'Potential private key material found',
      regex: /-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----/g,
      match: 'private-key',
    },
    {
      level: 'CRITICAL',
      message: 'Potential hardcoded API key found',
      regex: /api[_-]?key\s*[:=]\s*['"][A-Za-z0-9_\-]{20,}['"]/gi,
      match: 'api-key',
    },
    {
      level: 'HIGH',
      message: 'Potential hardcoded secret or token found',
      regex: /(secret|token|auth)[_-]?(key|token|secret)?\s*[:=]\s*['"][A-Za-z0-9_\-]{16,}['"]/gi,
      match: 'secret-token',
    },
    {
      level: 'HIGH',
      message: 'Potential hardcoded password found',
      regex: /password\s*[:=]\s*['"][^'"\n]{8,}['"]/gi,
      match: 'password',
    },
    {
      level: 'MEDIUM',
      message: 'URL with embedded credentials found',
      regex: /https?:\/\/[^:\s]+:[^@\s]+@/g,
      match: 'credential-url',
    },
  ];

  const candidateFiles = uniqueFiles([...runtime.envFiles, ...runtime.configFiles, ...runtime.sourceFiles]);
  for (const file of candidateFiles) {
    scanFileForPatterns(runtime, file, highConfidencePatterns, 'CREDENTIALS');
  }

  addFinding(runtime, 'INFO', 'CREDENTIALS', 'Credential scan completed', {
    scannedFiles: candidateFiles.length,
  });
}

function extractPortSignals(content) {
  const ports = [];
  const patterns = [
    /(?:^|\b)(?:PORT|SERVER_PORT|HTTP_PORT|HTTPS_PORT|MANAGEMENT_PORT)\s*[:=]\s*['"]?(\d{2,5})/gim,
    /server\.port\s*[:=]\s*(\d{2,5})/gim,
    /listen\s+(\d{2,5})\b/gim,
    /0\.0\.0\.0:(\d{2,5})/g,
    /["'](\d{2,5}):(\d{2,5})(?:\/(?:tcp|udp))?["']/g,
    /-\s*(\d{2,5}):(\d{2,5})(?:\/(?:tcp|udp))?\b/g,
  ];

  for (const regex of patterns) {
    regex.lastIndex = 0;
    let match;
    while ((match = regex.exec(content)) !== null) {
      const portText = match[2] ? match[1] : match[1];
      const port = Number.parseInt(portText, 10);
      if (Number.isInteger(port) && port >= 1 && port <= 65535) {
        ports.push(port);
      }
    }
  }

  return Array.from(new Set(ports)).sort((a, b) => a - b);
}

function hasWildcardExposureHint(content) {
  return /0\.0\.0\.0|\bnetwork_mode\s*:\s*["']?host["']?|\bhostNetwork\s*:\s*true\b/i.test(content);
}

function checkPorts(runtime) {
  const reviewFiles = uniqueFiles([...runtime.composeFiles, ...runtime.configFiles]);
  addFinding(runtime, 'INFO', 'PORTS', 'Reviewing explicit network exposure hints from configuration files', {
    files: reviewFiles.map(file => relativeToTarget(runtime, file)),
    allowedPorts: Array.from(runtime.allowedPorts).sort((a, b) => a - b),
  });

  if (reviewFiles.length === 0) {
    addFinding(runtime, 'INFO', 'PORTS', 'No config or compose files found; skipped explicit port exposure checks');
    return;
  }

  const exposed = [];
  for (const file of reviewFiles) {
    const content = readUtf8(file);
    if (content == null) continue;

    const rel = relativeToTarget(runtime, file);
    const ports = extractPortSignals(content);
    const wildcard = hasWildcardExposureHint(content);

    for (const port of ports) {
      if (runtime.allowedPorts.has(port)) continue;
      exposed.push({ file: rel, port, wildcard });
    }
  }

  if (exposed.length === 0) {
    addFinding(runtime, 'INFO', 'PORTS', 'No explicit port exposure hints detected after applying allow-port filters');
    return;
  }

  addFinding(runtime, 'INFO', 'PORTS', 'Explicit port exposure hints detected', {
    entries: exposed,
  });

  const commonExposed = exposed.filter(item => COMMON_EXPOSED_PORTS.has(item.port));
  const wildcardExposed = exposed.filter(item => item.wildcard && !COMMON_EXPOSED_PORTS.has(item.port));

  if (commonExposed.length > 0) {
    addFinding(runtime, 'MEDIUM', 'PORTS', 'Commonly exposed service ports are configured or published', {
      entries: commonExposed,
    });
  }

  if (wildcardExposed.length > 0) {
    addFinding(runtime, 'LOW', 'PORTS', 'Wildcard or host-network exposure hints detected on configured ports', {
      entries: wildcardExposed,
    });
  }
}

function checkConfigs(runtime) {
  addFinding(runtime, 'INFO', 'CONFIGS', 'Reviewing configuration files', {
    files: runtime.configFiles.map(file => relativeToTarget(runtime, file)),
  });

  if (runtime.configFiles.length === 0) {
    addFinding(runtime, 'INFO', 'CONFIGS', 'No known configuration files found; skipped config-specific checks');
    return;
  }

  const placeholderSecretRegex = /(API_KEY|TOKEN|SECRET|PASSWORD)\s*[:=]\s*(changeme|change-me|example|sample|default|password|secret|todo)?\s*$/gim;
  const blankSecretRegex = /(API_KEY|TOKEN|SECRET|PASSWORD)\s*[:=]\s*$/gim;

  for (const file of runtime.configFiles) {
    const content = readUtf8(file);
    if (content == null) continue;

    const rel = relativeToTarget(runtime, file);
    if (/LOG_LEVEL\s*[:=]\s*(debug|trace)/i.test(content)) {
      addFinding(runtime, 'MEDIUM', 'CONFIGS', 'Verbose debug logging enabled', { file: rel });
    }
    if (/CORS(_ORIGIN|_ALLOW_ALL)?\s*[:=]\s*\*/i.test(content) || /CORS_ALLOW_ALL\s*[:=]\s*true/i.test(content)) {
      addFinding(runtime, 'HIGH', 'CONFIGS', 'Wildcard CORS configuration found', { file: rel });
    }
    if (blankSecretRegex.test(content)) {
      addFinding(runtime, 'HIGH', 'CONFIGS', 'Blank secret-like configuration found', { file: rel });
    }
    blankSecretRegex.lastIndex = 0;
    if (placeholderSecretRegex.test(content)) {
      addFinding(runtime, 'MEDIUM', 'CONFIGS', 'Placeholder/default secret-like configuration found', { file: rel });
    }
    placeholderSecretRegex.lastIndex = 0;
  }
}

function checkPermissions(runtime) {
  addFinding(runtime, 'INFO', 'PERMISSIONS', 'Checking file permissions', { platform: runtime.platform });

  if (!UNIX_LIKE.has(runtime.platform)) {
    addFinding(runtime, 'INFO', 'PERMISSIONS', 'Detailed permission-bit checks skipped on this platform', {
      reason: 'unix-mode-bits-not-portable',
    });
    return;
  }

  const sensitivePatterns = [
    { pattern: /(^|\/)\.env(\.|$)?/, level: 'CRITICAL', message: 'Sensitive env file is world-readable' },
    { pattern: /\.(key|pem)$/i, level: 'CRITICAL', message: 'Key material is world-readable' },
    { pattern: /\.(json|ya?ml|properties)$/i, level: 'HIGH', message: 'Configuration file is world-readable' },
  ];

  for (const file of runtime.sourceFiles) {
    let stats;
    try {
      stats = fs.statSync(file);
    } catch {
      continue;
    }

    const mode = stats.mode & 0o777;
    if ((mode & 0o004) !== 0) {
      for (const rule of sensitivePatterns) {
        if (rule.pattern.test(file)) {
          addFinding(runtime, rule.level, 'PERMISSIONS', rule.message, {
            file: relativeToTarget(runtime, file),
            mode: mode.toString(8),
          });
        }
      }
    }

    if ((mode & 0o001) !== 0 && /\.(js|cjs|mjs|sh)$/i.test(file)) {
      addFinding(runtime, 'LOW', 'PERMISSIONS', 'Executable script is world-executable', {
        file: relativeToTarget(runtime, file),
        mode: mode.toString(8),
      });
    }
  }
}

function checkDocker(runtime) {
  addFinding(runtime, 'INFO', 'DOCKER', 'Inspecting Docker configuration', {
    files: runtime.dockerfiles.map(file => relativeToTarget(runtime, file)),
    composeFiles: runtime.composeFiles.map(file => relativeToTarget(runtime, file)),
  });

  if (runtime.dockerfiles.length === 0 && runtime.composeFiles.length === 0) {
    addFinding(runtime, 'INFO', 'DOCKER', 'No Dockerfile or compose file found; skipped Docker checks');
    return;
  }

  for (const dockerFile of runtime.dockerfiles) {
    const content = readUtf8(dockerFile);
    if (content == null) continue;
    const rel = relativeToTarget(runtime, dockerFile);

    if (/^\s*USER\s+root\b/im.test(content)) {
      addFinding(runtime, 'HIGH', 'DOCKER', 'Dockerfile runs as root user', { file: rel });
    }
    if (!/^\s*USER\s+/im.test(content)) {
      addFinding(runtime, 'MEDIUM', 'DOCKER', 'Dockerfile does not declare an explicit USER', { file: rel });
    }
    if (!/^\s*HEALTHCHECK\b/im.test(content)) {
      addFinding(runtime, 'LOW', 'DOCKER', 'Dockerfile does not declare HEALTHCHECK', { file: rel });
    }
    if (/:latest\b/i.test(content)) {
      addFinding(runtime, 'MEDIUM', 'DOCKER', 'Dockerfile uses floating :latest tag', { file: rel });
    }
    if (/--privileged/i.test(content)) {
      addFinding(runtime, 'CRITICAL', 'DOCKER', 'Privileged container flag detected', { file: rel });
    }
  }

  for (const composeFile of runtime.composeFiles) {
    const content = readUtf8(composeFile);
    if (content == null) continue;
    const rel = relativeToTarget(runtime, composeFile);

    if (/^\s*privileged\s*:\s*true\b/im.test(content)) {
      addFinding(runtime, 'CRITICAL', 'DOCKER', 'Compose file enables privileged mode', { file: rel });
    }
    if (/^\s*network_mode\s*:\s*["']?host["']?\b/im.test(content)) {
      addFinding(runtime, 'HIGH', 'DOCKER', 'Compose file uses host network mode', { file: rel });
    }
    if (/^\s*ports\s*:\s*\n([\s\S]*?)^\S/m.test(content) || /^\s*ports\s*:/im.test(content)) {
      if (/0\.0\.0\.0:|"\d+:\d+"|'\d+:\d+'/m.test(content)) {
        addFinding(runtime, 'LOW', 'DOCKER', 'Compose file publishes container ports; verify exposure is intentional', { file: rel });
      }
    }
    if (/:latest\b/i.test(content)) {
      addFinding(runtime, 'MEDIUM', 'DOCKER', 'Compose file uses floating :latest tag', { file: rel });
    }
  }
}

function checkGit(runtime) {
  addFinding(runtime, 'INFO', 'GIT', 'Inspecting repository exposure indicators');

  const gitDir = path.join(runtime.targetDir, '.git');
  const gitIgnore = path.join(runtime.targetDir, '.gitignore');

  if (fileExists(gitDir)) {
    addFinding(runtime, 'LOW', 'GIT', 'Target contains a .git directory; this is normal for local repositories, but do not expose it from web-served directories', {
      file: '.git',
    });
  } else {
    addFinding(runtime, 'INFO', 'GIT', 'Target is not a Git working tree');
    return;
  }

  if (!fileExists(gitIgnore)) {
    addFinding(runtime, 'LOW', 'GIT', 'Repository has no .gitignore file', {
      file: '.gitignore',
    });
  }
}

function runSelectedChecks(runtime) {
  for (const check of runtime.options.checks) {
    switch (check) {
      case 'credentials':
        checkCredentials(runtime);
        break;
      case 'ports':
        checkPorts(runtime);
        break;
      case 'configs':
        checkConfigs(runtime);
        break;
      case 'permissions':
        checkPermissions(runtime);
        break;
      case 'docker':
        checkDocker(runtime);
        break;
      case 'git':
        checkGit(runtime);
        break;
      default:
        throw new Error(`Unsupported check: ${check}`);
    }
  }
}

function createRecommendations(result) {
  const recommendations = [];
  const findings = result.findings;

  if (findings.some(item => item.category === 'CREDENTIALS' && ['CRITICAL', 'HIGH'].includes(item.level))) {
    recommendations.push('Review all flagged secrets immediately and move hardcoded credentials into environment-managed secrets.');
  }
  if (findings.some(item => item.category === 'CONFIGS' && item.message.includes('Wildcard CORS'))) {
    recommendations.push('Restrict CORS to trusted origins instead of wildcard access.');
  }
  if (findings.some(item => item.category === 'DOCKER' && item.message.includes('root user'))) {
    recommendations.push('Run containers as a non-root user wherever possible.');
  }
  if (findings.some(item => item.category === 'DOCKER' && item.message.includes('privileged'))) {
    recommendations.push('Remove privileged container mode unless it is strictly required and documented.');
  }
  if (findings.some(item => item.category === 'PORTS' && item.level !== 'INFO')) {
    recommendations.push('Review configured or published ports and add expected ones to --allow-port when the exposure is intentional.');
  }
  if (findings.some(item => item.category === 'GIT' && item.message.includes('.gitignore'))) {
    recommendations.push('Add a .gitignore that excludes secrets, logs, and local build artifacts.');
  }

  if (recommendations.length === 0) {
    recommendations.push('No immediate remediation guidance generated; review findings and environment-specific expectations manually.');
  }

  return recommendations;
}

function buildResult(runtime) {
  const counts = countByLevel(runtime.findings);
  const summary = {
    targetDir: runtime.targetDir,
    platform: runtime.platform,
    hostname: runtime.hostname,
    startedAt: runtime.startedAt,
    finishedAt: new Date().toISOString(),
    readonly: true,
    checksRequested: runtime.options.checks,
    excludeDirs: runtime.options.excludeDirs,
    allowPorts: runtime.options.allowPorts,
    findingsTotal: runtime.findings.length,
    counts,
  };

  const result = {
    tool: 'portable-deployment-audit',
    version: '1.3.0',
    summary,
    findings: runtime.findings,
  };

  result.recommendations = createRecommendations(result);
  return result;
}

function renderText(result) {
  const lines = [];
  lines.push('Portable Deployment Audit');
  lines.push(`Target: ${result.summary.targetDir}`);
  lines.push(`Platform: ${result.summary.platform}`);
  lines.push('Mode: read-only');
  lines.push(`Checks: ${result.summary.checksRequested.join(', ')}`);
  if (result.summary.excludeDirs.length > 0) {
    lines.push(`Excluded dirs: ${result.summary.excludeDirs.join(', ')}`);
  }
  if (result.summary.allowPorts.length > 0) {
    lines.push(`Allowed ports: ${result.summary.allowPorts.join(', ')}`);
  }
  lines.push('');
  lines.push(`Findings: ${result.summary.findingsTotal}`);
  lines.push(`Critical: ${result.summary.counts.CRITICAL}`);
  lines.push(`High: ${result.summary.counts.HIGH}`);
  lines.push(`Medium: ${result.summary.counts.MEDIUM}`);
  lines.push(`Low: ${result.summary.counts.LOW}`);
  lines.push(`Info: ${result.summary.counts.INFO}`);
  lines.push('');

  const groupedLevels = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'];
  for (const level of groupedLevels) {
    const items = result.findings.filter(finding => finding.level === level);
    if (items.length === 0) continue;
    lines.push(`${level}:`);
    for (const item of items) {
      let line = `- [${item.category}] ${item.message}`;
      if (item.details?.file) line += ` (${item.details.file})`;
      lines.push(line);
    }
    lines.push('');
  }

  lines.push('Recommendations:');
  for (const item of result.recommendations) {
    lines.push(`- ${item}`);
  }
  lines.push('');

  lines.push('Info:');
  for (const item of result.findings.filter(finding => finding.level === 'INFO')) {
    lines.push(`- [${item.category}] ${item.message}`);
  }

  return lines.join('\n');
}

function determineExitCode(result, strict) {
  if (result.summary.counts.CRITICAL > 0) return 1;
  if (strict && result.summary.counts.HIGH > 0) return 1;
  return 0;
}

function outputResult(result, format) {
  if (format === 'json') {
    process.stdout.write(JSON.stringify(result, null, 2));
    process.stdout.write('\n');
    return;
  }
  process.stdout.write(renderText(result));
  process.stdout.write('\n');
}

function outputError(error, format) {
  if (format === 'json') {
    process.stdout.write(JSON.stringify({
      tool: 'portable-deployment-audit',
      error: true,
      message: error.message,
    }, null, 2));
    process.stdout.write('\n');
    return;
  }
  process.stderr.write(`Error: ${error.message}\n`);
}

function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    outputError(error, 'text');
    process.exit(1);
  }

  if (options.help) {
    printHelp();
    return;
  }

  if (options.fixRequested) {
    const error = new Error('Auto-fix is disabled in this version. This skill is read-only.');
    outputError(error, options.format);
    process.exit(2);
  }

  try {
    const runtime = buildRuntime(options);
    runSelectedChecks(runtime);
    const result = buildResult(runtime);
    outputResult(result, options.format);
    process.exitCode = determineExitCode(result, options.strict);
  } catch (error) {
    outputError(error, options.format);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  parseArgs,
  buildRuntime,
  runSelectedChecks,
  buildResult,
  checkCredentials,
  checkPorts,
  checkConfigs,
  checkPermissions,
  checkDocker,
  checkGit,
};
