// @ts-nocheck
/**
 * Threat Model Layer
 * Generates a threat model by identifying capabilities (network, exec, fs, etc.)
 * within a given context/codebase to contextualize heuristic pattern findings.
 */

const CAPABILITY_PATTERNS = {
  network: /(?:fetch|axios|http\.get|https\.request|XMLHttpRequest|WebSocket)/i,
  exec: /(?:exec|spawn|child_process|eval|Function|system)/i,
  fs_read: /(?:readFileSync|readFile|createReadStream)/i,
  fs_write: /(?:writeFileSync|writeFile|createWriteStream|appendFile)/i,
  env_access: /(?:process\.env)/i,
  untrusted_input: /(?:req\.(?:body|query|params)|user(?:Input|_input)?|prompt|upload|multipart|tool[s]?\/call|resources\/(?:read|list)|prompts\/(?:get|list)|stdin)/i,
  external_communication: /(?:https?:\/\/|fetch|axios|WebSocket|EventSource|postMessage|send\s*\()/i,
};

function generateModel(codeContent) {
  const capabilities = {
    network: false,
    exec: false,
    fs_read: false,
    fs_write: false,
    env_access: false,
    private_data_access: false,
    untrusted_input: false,
    external_communication: false,
  };

  let riskScore = 0;

  for (const [cap, regex] of Object.entries(CAPABILITY_PATTERNS)) {
    if (regex.test(codeContent)) {
      capabilities[cap] = true;
      riskScore += 10; // Base score for having a risky capability
    }
  }

  capabilities.private_data_access = capabilities.fs_read || capabilities.env_access;
  capabilities.external_communication = capabilities.network || capabilities.external_communication;

  // Capability compounding (e.g. read + network = exfil risk)
  const compoundedRisks = [];
  if (capabilities.fs_read && capabilities.network) {
    riskScore += 20;
    compoundedRisks.push({
      id: 'compound.fs_read_network',
      severity: 'HIGH',
      description: 'File-system reads combined with outbound communication create exfiltration risk.',
      triggered: true,
      contributing_capabilities: ['fs_read', 'network'],
    });
  }
  if (capabilities.env_access && capabilities.network) {
    riskScore += 30; // High risk of credential exfiltration
    compoundedRisks.push({
      id: 'compound.env_access_network',
      severity: 'CRITICAL',
      description: 'Environment access combined with outbound communication suggests credential exfiltration risk.',
      triggered: true,
      contributing_capabilities: ['env_access', 'network'],
    });
  }
  if (capabilities.untrusted_input && capabilities.exec) {
    riskScore += 20;
    compoundedRisks.push({
      id: 'compound.untrusted_input_exec',
      severity: 'CRITICAL',
      description: 'Untrusted input combined with execution primitives suggests prompt-to-code injection risk.',
      triggered: true,
      contributing_capabilities: ['untrusted_input', 'exec'],
    });
  }

  const lethalTrifectaTriggered = capabilities.private_data_access && capabilities.untrusted_input && capabilities.external_communication;
  if (lethalTrifectaTriggered) {
    riskScore += 40;
  }

  return {
    capabilities,
    compounded_risks: compoundedRisks,
    lethal_trifecta: {
      triggered: lethalTrifectaTriggered,
      severity: lethalTrifectaTriggered ? 'CRITICAL' : 'LOW',
      contributing_capabilities: ['private_data_access', 'untrusted_input', 'external_communication'].filter((key) => capabilities[key]),
      rationale: lethalTrifectaTriggered
        ? 'Private data access, untrusted input handling, and external communication are simultaneously present.'
        : 'All three lethal-trifecta conditions are not simultaneously present.',
    },
    riskScore,
    summary: `Capabilities detected: ${Object.keys(capabilities).filter(k => capabilities[k]).join(', ')}`
  };
}

export { 
  generateModel
 };
