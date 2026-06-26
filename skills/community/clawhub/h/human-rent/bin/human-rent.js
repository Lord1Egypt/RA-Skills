#!/usr/bin/env node
/**
 * Human-Rent CLI
 * Command-line interface for human-as-a-service
 */

const path = require('path');
const fs = require('fs');
const crypto = require('crypto');

// Verify integrity on startup
const verifyIntegrity = () => {
  const checksumsPath = path.join(__dirname, 'checksums.txt');

  if (!fs.existsSync(checksumsPath)) {
    console.error('❌ Security Error: Integrity verification failed (checksums.txt missing)');
    console.error('This package may have been tampered with. Do not proceed.');
    process.exit(1);
  }

  // Read and parse checksums
  let checksumData;
  try {
    checksumData = fs.readFileSync(checksumsPath, 'utf8');
  } catch (error) {
    console.error('❌ Security Error: Cannot read checksums.txt');
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }

  const expectedChecksums = {};
  checksumData.trim().split('\n').forEach(line => {
    const parts = line.trim().split(/\s+/);
    if (parts.length >= 2) {
      const hash = parts[0];
      const file = parts.slice(1).join(' '); // Handle filenames with spaces
      expectedChecksums[file] = hash;
    }
  });

  // Verify each critical file
  const criticalFiles = [
    'lib/api-client.js',
    'lib/dispatch.js',
    'lib/status.js',
    'lib/humans.js',
    'lib/confirmation.js',
    'bin/human-rent.js'
  ];

  for (const file of criticalFiles) {
    const filePath = path.join(__dirname, '..', file);

    // Check file exists
    if (!fs.existsSync(filePath)) {
      console.error(`❌ Integrity check failed: Missing file ${file}`);
      process.exit(1);
    }

    // Calculate SHA256 hash
    let fileData;
    try {
      fileData = fs.readFileSync(filePath);
    } catch (error) {
      console.error(`❌ Integrity check failed: Cannot read ${file}`);
      console.error(`Error: ${error.message}`);
      process.exit(1);
    }

    const actualHash = crypto.createHash('sha256').update(fileData).digest('hex');
    const expectedHash = expectedChecksums[file];

    if (!expectedHash) {
      console.error(`❌ Integrity check failed: No checksum for ${file}`);
      console.error('This package may have been tampered with. Do not proceed.');
      process.exit(1);
    }

    if (actualHash !== expectedHash) {
      console.error(`❌ Integrity check failed: ${file}`);
      console.error(`   Expected: ${expectedHash}`);
      console.error(`   Got:      ${actualHash}`);
      console.error('This package may have been tampered with. Do not proceed.');
      process.exit(1);
    }
  }

  return true;
};

// Check Node.js version
const checkNodeVersion = () => {
  const version = process.version;
  const major = parseInt(version.split('.')[0].substring(1));

  if (major < 18) {
    console.error('❌ Error: Node.js 18.0.0 or higher is required');
    console.error(`   Current version: ${version}`);
    process.exit(1);
  }
};

// Check credentials
const checkCredentials = () => {
  const apiKey = process.env.ZHENRENT_API_KEY;
  const apiSecret = process.env.ZHENRENT_API_SECRET;

  if (!apiKey || !apiSecret) {
    console.error('❌ Error: Missing credentials\n');
    console.error('Please set the following environment variables:');
    console.error('  ZHENRENT_API_KEY     - Your API key');
    console.error('  ZHENRENT_API_SECRET  - Your API secret\n');
    console.error('Get your credentials at: https://www.zhenrent.com/api/keys\n');
    console.error('Example:');
    console.error('  export ZHENRENT_API_KEY="your-key-here"');
    console.error('  export ZHENRENT_API_SECRET="your-secret-here"\n');
    process.exit(1);
  }
};

// Main CLI logic
const main = async () => {
  // Run checks
  checkNodeVersion();
  verifyIntegrity();

  const args = process.argv.slice(2);
  const command = args[0] || 'help';

  // Help command doesn't need credentials
  if (command === 'help' || command === '--help' || command === '-h') {
    showHelp();
    return;
  }

  // Version command doesn't need credentials
  if (command === 'version' || command === '--version' || command === '-v') {
    showVersion();
    return;
  }

  // All other commands require credentials
  checkCredentials();

  // Load modules
  const TaskDispatcher = require('../lib/dispatch');
  const StatusChecker = require('../lib/status');
  const HumanManager = require('../lib/humans');

  try {
    switch (command) {
      case 'dispatch':
        await handleDispatch(args.slice(1));
        break;

      case 'status':
        await handleStatus(args.slice(1));
        break;

      case 'humans':
        await handleHumans(args.slice(1));
        break;

      case 'test':
        await handleTest();
        break;

      default:
        console.error(`❌ Unknown command: ${command}\n`);
        showHelp();
        process.exit(1);
    }
  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
};

// Command handlers

async function handleDispatch(args) {
  const TaskDispatcher = require('../lib/dispatch');
  const dispatcher = new TaskDispatcher();

  // Parse instruction
  let instruction = '';
  const options = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg.startsWith('--location=')) {
      options.location = arg.substring('--location='.length);
    } else if (arg.startsWith('--budget=')) {
      options.budget = arg.substring('--budget='.length);
    } else if (arg.startsWith('--priority=')) {
      options.priority = arg.substring('--priority='.length);
    } else if (arg.startsWith('--timeout=')) {
      options.timeout = parseInt(arg.substring('--timeout='.length));
    } else if (arg.startsWith('--type=')) {
      options.taskType = arg.substring('--type='.length);
    } else {
      instruction += (instruction ? ' ' : '') + arg;
    }
  }

  if (!instruction) {
    console.error('❌ Error: Instruction required\n');
    console.error('Usage: human-rent dispatch <instruction> [options]\n');
    console.error('Example:');
    console.error('  human-rent dispatch "Take a photo of 123 Main St" --location="37.7749,-122.4194"');
    process.exit(1);
  }

  await dispatcher.dispatch(instruction, options);
}

async function handleStatus(args) {
  const StatusChecker = require('../lib/status');
  const checker = new StatusChecker();

  const taskId = args[0];
  const shouldWait = args.includes('--wait');

  if (!taskId) {
    console.error('❌ Error: Task ID required\n');
    console.error('Usage: human-rent status <task_id> [--wait]\n');
    console.error('Example:');
    console.error('  human-rent status abc-123-def');
    process.exit(1);
  }

  if (shouldWait) {
    await checker.waitForCompletion(taskId);
  } else {
    await checker.checkStatus(taskId);
  }
}

async function handleHumans(args) {
  const HumanManager = require('../lib/humans');
  const manager = new HumanManager();

  const options = {};

  for (const arg of args) {
    if (arg.startsWith('--location=')) {
      options.location = arg.substring('--location='.length);
    } else if (arg.startsWith('--radius=')) {
      options.radius = parseInt(arg.substring('--radius='.length));
    } else if (arg.startsWith('--skills=')) {
      const skills = arg.substring('--skills='.length).split(',');
      await manager.searchBySkills(skills, options);
      return;
    }
  }

  await manager.listHumans(options);
}

async function handleTest() {
  console.log('========================================');
  console.log('HUMAN-RENT TEST MODE');
  console.log('========================================\n');

  console.log('Testing API connection...\n');

  const ZhenRentAPIClient = require('../lib/api-client');
  const client = new ZhenRentAPIClient();

  try {
    // Test listing workers
    console.log('1. Testing worker list endpoint...');
    const workers = await client.listWorkers();
    console.log(`   ✓ Success: Found ${workers.workers?.length || 0} workers\n`);

    console.log('2. Testing credentials...');
    console.log(`   ✓ API Key: ${process.env.ZHENRENT_API_KEY?.substring(0, 10)}...`);
    console.log(`   ✓ API Secret: [REDACTED]\n`);

    console.log('All tests passed! ✅\n');
    console.log('You can now dispatch tasks with:');
    console.log('  human-rent dispatch "Your task instruction here"\n');

  } catch (error) {
    console.error(`   ✗ Test failed: ${error.message}\n`);
    console.error('Please check your credentials and network connection.\n');
    process.exit(1);
  }
}

function showHelp() {
  console.log(`
Human-Rent CLI v0.2.1
Human-as-a-Service for AI Agents

USAGE:
  human-rent <command> [options]

COMMANDS:
  dispatch <instruction>     Dispatch a human task (requires confirmation)
  status <task_id>          Check task status
  humans                    List available human workers
  test                      Test API connection
  help                      Show this help message
  version                   Show version information

DISPATCH OPTIONS:
  --location=<lat,lng>      Location for the task (e.g., "37.7749,-122.4194")
  --budget=<amount>         Budget in dollars (e.g., "$20" or "$15-25")
  --priority=<level>        Priority: low, normal, high, urgent
  --timeout=<minutes>       Task timeout in minutes (default: 30)
  --type=<task_type>        Task type (auto-detected if not specified)

TASK TYPES:
  photo_verification        Take photos for verification
  address_verification      Verify physical address exists
  document_scan            Scan physical documents
  visual_inspection        Detailed visual inspection
  voice_verification       Make phone calls and verify
  purchase_verification    Check product availability

EXAMPLES:
  # Dispatch a photo verification task
  human-rent dispatch "Take a photo of 123 Main St and verify the door number" \\
    --location="37.7749,-122.4194"

  # Check task status
  human-rent status abc-123-def

  # List available humans in San Francisco
  human-rent humans --location="37.7749,-122.4194" --radius=10000

  # Search for workers with specific skills
  human-rent humans --skills="photography,legal_reading"

  # Test API connection
  human-rent test

CONFIGURATION:
  Required environment variables:
    ZHENRENT_API_KEY         API key from https://www.zhenrent.com/api/keys
    ZHENRENT_API_SECRET      API secret for authentication

  Optional environment variables:
    ZHENRENT_BASE_URL        API base URL (default: https://www.zhenrent.com/api/v1)
    HUMAN_RENT_AUTO_CONFIRM  Set to 'true' to skip confirmation prompts (not recommended)

DOCUMENTATION:
  https://github.com/ZhenRobotics/openclaw-human-rent
  https://www.zhenrent.com/docs

SUPPORT:
  https://github.com/ZhenRobotics/openclaw-human-rent/issues
`);
}

function showVersion() {
  const packageJson = require('../package.json');
  console.log(`human-rent v${packageJson.version}`);
}

// Run
main().catch(error => {
  console.error(`Fatal error: ${error.message}`);
  process.exit(1);
});
