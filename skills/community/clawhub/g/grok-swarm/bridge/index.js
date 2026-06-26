#!/usr/bin/env node
/**
 * index.js — Node.js wrapper for grok_bridge.py
 *
 * Enforces timeout at the process level to prevent 502 Bad Gateway errors.
 * Supports multiple task modes, custom system prompts, file context, and tool use.
 *
 * Usage:
 *   node index.js --prompt "Analyze security" --mode analyze --files src/*.js
 *   node index.js --prompt "Build feature" --mode orchestrate --system "You are a Go expert" --files main.go
 */

const { spawn } = require('child_process');
const path = require('path');

const BRIDGE_SCRIPT = path.join(__dirname, 'grok_bridge.py');
const PYTHON = path.join(__dirname, '.venv', 'bin', 'python3');

const VALID_MODES = ['refactor', 'analyze', 'code', 'reason', 'orchestrate'];

function parseArgs() {
  const args = process.argv.slice(2);
  const parsed = {
    prompt: null,
    mode: 'reason',
    files: [],
    system: null,
    tools: null,
    timeout: 120,
    output: null,
    writeFiles: false,
    outputDir: './grok-output/',
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--prompt':
        parsed.prompt = args[++i];
        break;
      case '--mode':
        parsed.mode = args[++i];
        break;
      case '--files':
        while (i + 1 < args.length && !args[i + 1].startsWith('--')) {
          parsed.files.push(args[++i]);
        }
        break;
      case '--system':
        parsed.system = args[++i];
        break;
      case '--tools':
        parsed.tools = args[++i];
        break;
      case '--timeout':
        parsed.timeout = parseInt(args[++i], 10) || 120;
        break;
      case '--output':
        parsed.output = args[++i];
        break;
      case '--write-files':
        parsed.writeFiles = true;
        break;
      case '--output-dir':
        parsed.outputDir = args[++i];
        break;
      case '--help':
        console.log(`
grok_swarm — Bridge to xAI Grok 4.20 Multi-Agent Beta (4-agent swarm)

Usage:
  node index.js --prompt "instruction" [options]

Options:
  --prompt <text>     Task instruction (required)
  --mode <mode>       Task mode: refactor|analyze|code|reason|orchestrate (default: reason)
  --files <path...>   Files to include as context
  --system <text>     Override system prompt (required for orchestrate mode)
  --tools <path>      JSON file with OpenAI-format tool definitions
  --timeout <secs>    Timeout in seconds (default: 120)
  --output <path>     Output file (default: stdout)
  --write-files       Parse response for annotated code blocks and write files
  --output-dir <path> Directory for file writes (default: ./grok-output/)
  --help              Show this help

Modes:
  refactor   Large-scale code refactoring, modernization, migration
  analyze    Code review, security audit, architecture assessment
  code       Generate new code, implement features, write tests
  reason     Complex reasoning, research synthesis, multi-perspective analysis
  orchestrate  Full prompt control — requires --system flag
`);
        process.exit(0);
    }
  }

  if (!parsed.prompt) {
    console.error('ERROR: --prompt is required');
    process.exit(1);
  }

  if (!VALID_MODES.includes(parsed.mode)) {
    console.error(`ERROR: Invalid mode '${parsed.mode}'. Valid: ${VALID_MODES.join(', ')}`);
    process.exit(1);
  }

  if (parsed.mode === 'orchestrate' && !parsed.system) {
    console.error('ERROR: --mode orchestrate requires --system flag');
    process.exit(1);
  }

  return parsed;
}

function run() {
  const opts = parseArgs();

  // Build Python args
  const pyArgs = [
    BRIDGE_SCRIPT,
    '--prompt', opts.prompt,
    '--mode', opts.mode,
    '--timeout', String(opts.timeout),
  ];

  if (opts.files.length > 0) {
    pyArgs.push('--files', ...opts.files);
  }

  if (opts.system) {
    pyArgs.push('--system', opts.system);
  }

  if (opts.tools) {
    pyArgs.push('--tools', opts.tools);
  }

  if (opts.output) {
    pyArgs.push('--output', opts.output);
  }

  if (opts.writeFiles) {
    pyArgs.push('--write-files');
  }

  // Skip --output-dir if it matches the Python bridge default.
  // This optimization reduces CLI noise; CLI invocations bypass this wrapper
  // via src/plugin/index.ts, which sets defaults at the plugin layer.
  if (opts.outputDir && opts.outputDir !== './grok-output/') {
    pyArgs.push('--output-dir', opts.outputDir);
  }

  // Spawn Python process
  const child = spawn(PYTHON, pyArgs, {
    stdio: ['inherit', 'pipe', 'pipe'],
    env: { ...process.env },
  });

  let stdout = '';
  let stderr = '';
  let timedOut = false;

  // Enforce timeout at process level
  const timer = setTimeout(() => {
    timedOut = true;
    child.kill('SIGTERM');
    setTimeout(() => child.kill('SIGKILL'), 5000);
  }, opts.timeout * 1000);

  child.stdout.on('data', (data) => {
    stdout += data.toString();
  });

  child.stderr.on('data', (data) => {
    stderr += data.toString();
    process.stderr.write(data);
  });

  child.on('close', (code) => {
    clearTimeout(timer);

    if (timedOut) {
      console.error(`\nTIMEOUT: Grok call exceeded ${opts.timeout}s limit`);
      process.exit(124);
    }

    if (code !== 0) {
      console.error(`\nBridge exited with code ${code}`);
      process.exit(code);
    }

    if (opts.output) {
      console.error(`Output written to: ${opts.output}`);
    } else {
      process.stdout.write(stdout);
    }
  });

  child.on('error', (err) => {
    clearTimeout(timer);
    console.error(`Failed to spawn bridge: ${err.message}`);
    process.exit(1);
  });
}

run();