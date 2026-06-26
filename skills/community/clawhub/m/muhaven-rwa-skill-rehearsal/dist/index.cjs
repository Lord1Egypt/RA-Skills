'use strict';

var mcp = require('@muhaven/mcp');

var TOOLSET_SUBSET = [
  "muhaven.read.portfolio",
  "muhaven.read.yields",
  "muhaven.read.distribution",
  "muhaven.read.tokens",
  "muhaven.read.audit",
  // Wave 4 P11 — informational read tools fit the investor surface.
  "muhaven.read.protection_coverage",
  "muhaven.read.kyc_attestation",
  "muhaven.position.buy",
  "muhaven.position.claim",
  "muhaven.policy.pause",
  "muhaven.policy.session_key_status"
];
var TOOLSET_EXCLUDED = [
  "muhaven.position.sell",
  "muhaven.position.rebalance",
  "muhaven.policy.set_tier",
  "muhaven.policy.audit_export",
  // Wave 4 P7 — issuer-side tools are out of scope for the OpenClaw
  // skill (investor-facing surface). Issuer flows live on HavenBot
  // in-dashboard + the standalone `@muhaven/mcp` install. The bundled
  // OpenClaw skill never advertises them.
  "muhaven.issuer.distribute_yield",
  "muhaven.issuer.kyc_add",
  "muhaven.issuer.kyc_remove",
  "muhaven.issuer.unpause_token",
  "muhaven.issuer.audit_query",
  // Wave 4 P11 — governance ceremony requires the dashboard ConfirmModal
  // + cofhe encrypt ceremony, neither of which the OpenClaw skill
  // surface (Telegram bot / inline confirm) can drive. Investors who
  // want to vote follow the dashboard flow.
  "muhaven.governance.propose",
  "muhaven.governance.cast_vote"
];
var SUBSET = new Set(TOOLSET_SUBSET);
function selectOpenClawSubsetRegistry(registry) {
  const upstreamNames = new Set(registry.map((e) => e.descriptor.name));
  const filtered = registry.filter((e) => SUBSET.has(e.descriptor.name));
  const upstreamHasNonRead = registry.some((e) => e.descriptor.group !== "read");
  if (upstreamHasNonRead) {
    const missing = TOOLSET_SUBSET.filter((name) => !upstreamNames.has(name));
    if (missing.length > 0) {
      throw new Error(
        `[openclaw-skill] tool-subset drift: missing ${missing.join(", ")} from upstream @muhaven/mcp registry. The bundled_version triple-match guarantee (manifest.json#mcp.bundled_version === SKILL.md frontmatter bundled_version === packages/mcp/package.json#version) is supposed to catch this at install time \u2014 if you are seeing this at runtime, reinstall the skill at a compatible @muhaven/mcp version rather than patching in place. If reproduces on fresh install: https://github.com/hasToDev/muhaven/issues with the missing list.`
      );
    }
  }
  return filtered;
}
async function runOpenClawSkill() {
  process.env.MUHAVEN_OPENCLAW_SKILL_VERSION = resolveSkillVersion();
  await mcp.runMcpStdioCli({ filterRegistry: selectOpenClawSubsetRegistry });
}
function resolveSkillVersion() {
  {
    return "0.1.0";
  }
}

exports.TOOLSET_EXCLUDED = TOOLSET_EXCLUDED;
exports.TOOLSET_SUBSET = TOOLSET_SUBSET;
exports.runOpenClawSkill = runOpenClawSkill;
exports.selectOpenClawSubsetRegistry = selectOpenClawSubsetRegistry;
