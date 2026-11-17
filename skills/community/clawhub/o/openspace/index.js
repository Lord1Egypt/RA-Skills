'use strict';

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function checkEnv() {
  const required = [
    'OPENSPACE_WORKSPACE',
    'OPENSPACE_HOST_SKILL_DIRS',
  ];
  const missing = required.filter(key => !process.env[key]);
  return missing;
}

function ensureEnv() {
  const missing = checkEnv();
  if (missing.length > 0) {
    throw new Error('Missing OpenSpace env vars: ' + missing.join(', '));
  }
}

function workspaceExists() {
  const ws = process.env.OPENSPACE_WORKSPACE;
  return ws && fs.existsSync(ws);
}

function listRegisteredSkills() {
  const dirs = (process.env.OPENSPACE_HOST_SKILL_DIRS || '')
    .split(',')
    .map(s => s.trim())
    .filter(Boolean);

  const skills = [];
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) continue;
    for (const entry of fs.readdirSync(dir)) {
      const skillDir = path.join(dir, entry);
      const skillMd = path.join(skillDir, 'SKILL.md');
      if (fs.existsSync(skillMd)) {
        skills.push(entry);
      }
    }
  }
  return skills;
}

function status() {
  return {
    envMissing: checkEnv(),
    workspaceExists: workspaceExists(),
    registeredSkills: listRegisteredSkills(),
  };
}

module.exports = {
  checkEnv,
  ensureEnv,
  workspaceExists,
  listRegisteredSkills,
  status,
};
