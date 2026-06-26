#!/usr/bin/env node
var fs = require('fs');
var path = require('path');
var os = require('os');

var TOKEN_ENV_VAR = 'LIEPIN_TOKEN';

function findSkillDir() {
  if (process.env.LIEPIN_SKILL_DIR) return process.env.LIEPIN_SKILL_DIR;
  var scriptDir = path.dirname(__filename);
  var skillRoot = path.dirname(scriptDir);
  var name = path.basename(skillRoot);
  if (name === 'liepin-assistant' || name === 'liepin') return skillRoot;
  var home = os.homedir();
  var defaults = [
    path.join(home, '.openclaw', 'workspace', 'skills', 'liepin-assistant'),
    path.join(home, '.openclaw', 'workspace', 'skills', 'liepin'),
    path.join(home, '.openclaw', 'skills', 'liepin-assistant'),
    path.join(home, '.openclaw', 'skills', 'liepin'),
  ];
  for (var i = 0; i < defaults.length; i++) {
    if (fs.existsSync(path.join(defaults[i], 'SKILL.md'))) return defaults[i];
  }
  return skillRoot;
}

var skillDir = findSkillDir();
var configPath = path.join(skillDir, 'config.json');

function showStatus() {
  // 优先检查环境变量
  if (process.env[TOKEN_ENV_VAR]) {
    var t = process.env[TOKEN_ENV_VAR];
    console.log('Token:', t.slice(0, 4) + '****' + t.slice(-4), '(from env LIEPIN_TOKEN)');
    return;
  }
  if (!fs.existsSync(configPath)) {
    console.log('Token: 未设置 (env LIEPIN_TOKEN 未设置，config.json 也不存在)');
  } else {
    var config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    var t = config.token || '';
    if (!t) console.log('Token: 未设置');
    else console.log('Token:', t.slice(0, 4) + '****' + t.slice(-4), '(from config.json)');
  }
}

var args = process.argv.slice(2);
if (args.length === 0 || args[0] === '--show') {
  showStatus();
} else if (args[0] === '--clear') {
  if (fs.existsSync(configPath)) { fs.unlinkSync(configPath); console.log('已清除 config.json'); }
  else console.log('没有 config.json 可清除');
} else {
  var dir = path.dirname(configPath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(configPath, JSON.stringify({ token: args[0] }, null, 2));
  console.log('已保存到 config.json');
  console.log('Tip: 也可以设置环境变量 LIEPIN_TOKEN 更安全');
}
