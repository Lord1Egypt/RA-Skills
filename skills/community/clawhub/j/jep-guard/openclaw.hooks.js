/**
 * OpenClaw Integration Hooks v2.0.4 (Security Hardened)
 * 
 * v2.0.4 FIXES:
 * - Removed all child_process shell commands (already clean since v2.0.2)
 * - Added isFullMode() check before any interception
 * - Pure Node.js daemon detection via unix socket
 * - No auto-execution; hooks only contact local IPC socket
 */

const net = require('net');
const path = require('path');
const os = require('os');
const fs = require('fs');

const GUARD_SOCKET = path.join(os.tmpdir(), 'jep-guard.sock');
const CONFIG_DIR = path.join(os.homedir(), '.jep-guard');
const GUARD_TIMEOUT = 5000;

function isFullMode() {
  try {
    const configPath = path.join(CONFIG_DIR, 'config.json');
    if (!fs.existsSync(configPath)) return false;
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    return config.mode !== 'passive' && config.core?.hooks_enabled !== false;
  } catch (e) {
    return false;
  }
}

function guardCall(method, skill, payload, timeout = GUARD_TIMEOUT) {
  return new Promise((resolve, reject) => {
    const client = net.createConnection(GUARD_SOCKET);
    const req = JSON.stringify({ method, skill, payload });

    let data = '';
    let settled = false;

    client.write(req);
    client.on('data', chunk => data += chunk);
    client.on('end', () => {
      if (settled) return;
      settled = true;
      try { resolve(JSON.parse(data)); } catch (e) { reject(new Error(`Invalid response: ${data}`)); }
    });
    client.on('error', (err) => {
      if (settled) return;
      settled = true;
      reject(err);
    });
    setTimeout(() => {
      if (settled) return;
      settled = true;
      client.destroy();
      reject(new Error('Guard timeout'));
    }, timeout);
  });
}

// v2.0.4: Pure Node.js daemon detection, no shell commands, no auto-start
function ensureDaemon() {
  if (!fs.existsSync(GUARD_SOCKET)) {
    // Daemon not running; return false and let caller decide
    console.warn('[JEP Guard] Daemon not running. Start with: claw run jep-guard daemon');
    return false;
  }
  return true;
}

exports.postInstall = async function(skillManifest) {
  console.log(`[JEP Guard] Skill installed: ${skillManifest.name}`);

  if (!isFullMode()) {
    console.log('[JEP Guard] Passive mode: skipping runtime registration');
    return;
  }

  try {
    if (!ensureDaemon()) return;
    await guardCall('REGISTER_SKILL', skillManifest.name, {
      skill_id: skillManifest.name,
      version: skillManifest.version,
      capabilities: skillManifest.capabilities || [],
      risk_level: skillManifest.risk_level || 'low',
      source: skillManifest.source || 'clawhub'
    });
  } catch (err) {
    console.warn(`[JEP Guard] Registration deferred: ${err.message}`);
  }
};

exports.preExec = async function(command, context) {
  if (!isFullMode()) return command;

  if (!fs.existsSync(GUARD_SOCKET)) return command;

  try {
    const result = await guardCall('JUDGE', context.skillId, {
      action: command.action,
      target: command.target,
      context: { args: command.args, cwd: command.cwd }
    });

    if (result.action === 'block') {
      const err = new Error(`JEP Guard blocked: ${result.reason}`);
      err.code = 'JEP_BLOCKED';
      throw err;
    }

    return {
      ...command,
      _jep: { token: result.capabilityToken, eventId: result.event?.nonce, granted: true }
    };
  } catch (err) {
    if (err.code === 'JEP_BLOCKED') throw err;
    return command;
  }
};

exports.postExec = async function(result, context) {
  if (!isFullMode() || !context._jep?.eventId) return;

  try {
    if (result.error || result.exitCode !== 0) {
      await guardCall('TERMINATE', context.skillId, {
        target_event: context._jep.eventId,
        reason: result.error || `exit_code_${result.exitCode}`,
        triggered_by: 'system'
      });
    } else {
      await guardCall('VERIFY', context.skillId, {
        target_event: context._jep.eventId,
        verdict: 'approved',
        evidence: result.output_hash ? [result.output_hash] : []
      });
    }
  } catch (err) {
    console.warn(`[JEP Guard] postExec audit failed: ${err.message}`);
  }
};

exports.preDelegate = async function(fromSkill, toSkill, scope, payload) {
  if (!isFullMode()) {
    return { success: true, note: 'passive_mode' };
  }

  if (!fs.existsSync(GUARD_SOCKET)) {
    return { success: false, error: 'Guard not available' };
  }
  try {
    return await guardCall('DELEGATE', fromSkill, {
      target: toSkill,
      scope: Array.isArray(scope) ? scope : [scope],
      payload
    });
  } catch (err) {
    return { success: false, error: err.message };
  }
};

exports.onError = async function(error, context) {
  if (!isFullMode() || !context._jep?.eventId) return;
  try {
    await guardCall('TERMINATE', context.skillId, {
      target_event: context._jep.eventId,
      reason: error.message,
      triggered_by: 'system'
    });
  } catch (e) {}
};