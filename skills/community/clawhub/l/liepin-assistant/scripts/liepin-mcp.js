#!/usr/bin/env node
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const MCP_ENDPOINT = 'https://open-agent.liepin.com/mcp/user';
const TOKEN_ENV_VAR = 'LIEPIN_TOKEN';

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

function loadConfig() {
  // 1. 优先从环境变量读取
  if (process.env[TOKEN_ENV_VAR]) {
    return { token: process.env[TOKEN_ENV_VAR] };
  }

  // 2. 降级到 config.json
  var skillDir = findSkillDir();
  var configPath = path.join(skillDir, 'config.json');
  if (!fs.existsSync(configPath)) {
    console.error('Error: token not configured. Set LIEPIN_TOKEN env var, or run "set-liepin-token <your-token>" first.');
    process.exit(1);
  }
  var config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  if (!config.token) {
    console.error('Error: token is empty. Please configure again.');
    process.exit(1);
  }
  return config;
}

function mcpRequest(toolName, arguments_) {
  return new Promise(function(resolve, reject) {
    var config = loadConfig();
    var id = Date.now();

    var bodyObj = {
      jsonrpc: '2.0',
      id: id,
      method: 'tools/call',
      params: {
        name: toolName,
        arguments: arguments_ || {}
      }
    };
    var body = JSON.stringify(bodyObj);

    var url = new URL(MCP_ENDPOINT);
    var options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
        'x-user-token': config.token,
        'Accept': 'application/json, text/event-stream'
      },
      timeout: 30000
    };

    var protocol = url.protocol === 'https:' ? https : http;
    var req = protocol.request(options, function(res) {
      var chunks = [];
      res.on('data', function(chunk) { chunks.push(chunk); });
      res.on('end', function() {
        var raw = chunks.join('').trim();
        if (!raw) { resolve({ result: null }); return; }

        var lines = raw.split('\n');
        for (var i = 0; i < lines.length; i++) {
          var trimmed = lines[i].trim();
          if (trimmed.startsWith('data:')) {
            var jsonStr = trimmed.slice(5).trim();
            try {
              var obj = JSON.parse(jsonStr);
              if (obj.result !== undefined) { resolve(obj); return; }
              if (obj.error) { resolve(obj); return; }
            } catch (e) {}
          }
        }

        if (raw.slice(0, 5).toLowerCase() === '<html' || raw.includes('<!DOCTYPE') || raw.includes('<!doctype')) {
          reject(new Error('Server returned HTML (possibly login page or 404). Check: (1) Token is valid; (2) API endpoint is correct.'));
          return;
        }

        try { resolve(JSON.parse(raw)); return; } catch (e) {}

        for (var j = 0; j < lines.length; j++) {
          var line = lines[j].trim();
          if (line && !line.startsWith('data:')) {
            try { resolve(JSON.parse(line)); return; } catch (e) {}
          }
        }
        reject(new Error('Failed to parse response: ' + raw.slice(0, 200)));
      });
    });

    req.on('error', function(e) { reject(e); });
    req.on('timeout', function() { req.destroy(); reject(new Error('Request timeout')); });
    req.write(body);
    req.end();
  });
}

var args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: node liepin-mcp.js <toolName> [paramsJson]');
  console.error('Example: node liepin-mcp.js user-search-job \'{"jobName":"AI","address":"北京"}\'');
  console.error('         node liepin-mcp.js user-apply-job \'{"jobId":81543059,"jobKind":"2"}\'');
  process.exit(1);
}

var toolName = args[0];
var toolArgs = {};
if (args.length > 1) {
  try { toolArgs = JSON.parse(args[1]); }
  catch (e) {
    console.error('Invalid params JSON: ' + args[1]);
    process.exit(1);
  }
}

mcpRequest(toolName, toolArgs)
  .then(function(result) {
    if (result.error) {
      console.error('MCP Error: ' + result.error.message + ' (code: ' + result.error.code + ')');
      process.exit(1);
    }
    if (result.result && result.result.content) {
      var text = result.result.content[0].text;
      try {
        var parsed = JSON.parse(text);
        console.log(JSON.stringify(parsed, null, 2));
      } catch (e) {
        console.log(text);
      }
    } else {
      console.log(JSON.stringify(result, null, 2));
    }
  })
  .catch(function(err) {
    console.error('Request failed: ' + err.message);
    process.exit(1);
  });
