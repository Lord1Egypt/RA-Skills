/**
 * OpenClaw Integration Hooks v2.0.4 (Security Hardened)
 * 
 * v2.0.4 FIXES:
 * - Removed all child_process shell commands (already clean since v2.0.2)
 * - Added isFullMode() check before any interception
 * - Pure Node.js daemon detection via unix socket
 * - No auto-execution; hooks only contact local IPC socket
 */

const fs = require('fs');
const path = require('path');
const {guardCall,dir,readPrivate} = require('./transport');
function isFullMode() {
  const file=path.join(dir(),'config.json');
  if(!fs.existsSync(file)) return false;
  const config=JSON.parse(readPrivate(file));
  if(!['passive','full'].includes(config.mode)) throw new Error('Invalid Guard mode');
  return config.mode==='full';
}

exports.postInstall = async function(skillManifest) {
  console.log(`[JEP Guard] Skill installed: ${skillManifest.name}`);

  if (!isFullMode()) {
    console.log('[JEP Guard] Passive mode: skipping runtime registration');
    return;
  }

  try {
    await guardCall('REGISTER_SKILL', skillManifest.name, {
      name: skillManifest.name,
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



  try {
    const result = await guardCall('JUDGE', context.skillId, {
      action: command.action,
      target: command.target || "",
      context: { args: command.args, cwd: command.cwd }
    });

    if (result.action !== 'allow' || !result.capabilityToken || !result.event?.nonce) {
      const err = new Error(`JEP Guard blocked: ${result.reason}`);
      err.code = 'JEP_BLOCKED';
      throw err;
    }

    return {
      ...command,
      _jep: { token: result.capabilityToken, eventId: result.event?.nonce, granted: true }
    };
  } catch (err) {
    err.code = 'JEP_BLOCKED';
    throw err;
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
  } catch (e) { throw new Error("Guard error audit failed: " + e.message); }
};