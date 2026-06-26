#!/usr/bin/env node
/**
 * Tool: install_skill
 * Skill: install-shared-skill
 *
 * Installs a skill using clawhub CLI.
 * Usage: install_skill <skill_name>
 */

const { exec } = require('child_process');

async function run() {
  // Get skill_name from arguments (passed by OpenClaw)
  const skillName = process.argv[2];

  if (!skillName) {
    console.error('ERROR: skill_name parameter is required');
    process.exit(1);
  }

  // Execute exactly: clawhub install <skill_name> --workdir ./
  const command = `clawhub install ${skillName} --workdir ./`;

  // Run in current workspace
  exec(command, { cwd: process.env.OPENCLAW_WORKSPACE || process.cwd() }, (error, stdout, stderr) => {
    // Output everything exactly as produced
    if (stdout) process.stdout.write(stdout);
    if (stderr) process.stderr.write(stderr);

    // Exit with the command's exit code
    process.exit(error ? 1 : 0);
  });
}

run();