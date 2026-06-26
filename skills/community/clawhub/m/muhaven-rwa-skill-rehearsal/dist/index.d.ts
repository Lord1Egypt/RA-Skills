import { ToolEntry } from '@muhaven/mcp';

/**
 * OpenClaw skill entry point. Bundles `@muhaven/mcp` with a hardcoded
 * tool subset per ADR-C: `read.*` (5) + Wave 4 P11 reads
 * (`read.protection_coverage`, `read.kyc_attestation`) +
 * `position.{buy,claim}` (2) + `policy.{pause,session_key_status}` (2)
 * = 11 tools. Eleven additional upstream tools (`position.{sell,
 * rebalance}` + `policy.{set_tier,audit_export}` + the five
 * `issuer.*` tools + the two `governance.*` tools) are deliberately
 * excluded — see `SKILL.md` `mcp.toolset_excluded_reason`.
 *
 * The skill does NOT mint its own MCP server — it imports `@muhaven/mcp`'s
 * `runMcpStdioCli` and supplies a `filterRegistry` callback that prunes
 * excluded tools. This keeps the descriptor SHA-256 hashes identical to
 * the upstream MCP package (post-MCPoison: hash drift in a bundled
 * subset would falsely trip the mcp-context-protector pin). Hash
 * verification fires inside `runMcpStdioCli` BEFORE the filter, so an
 * attacker who patches a single descriptor cannot hide the patch by
 * shipping a subset filter that excludes the patched tool — the patched
 * bytes still get hashed against the unfiltered `TOOL_DESCRIPTORS` array.
 *
 * The toolset_subset MUST stay in sync with `manifest.json`,
 * `manifest.json#tools`, and the SKILL.md frontmatter.
 * `scripts/verify-subset.ts` enforces this at build + CI gate time + via
 * a vitest at `__tests__/subset.test.ts` + `__tests__/manifest-consistency.test.ts`.
 */

/** Tool names exposed by this skill. ORDER-INDEPENDENT — used as a Set. */
declare const TOOLSET_SUBSET: readonly string[];
/** Tools deliberately excluded — see SKILL.md `mcp.toolset_excluded_reason`. */
declare const TOOLSET_EXCLUDED: readonly string[];
/**
 * Pure function — returns the OpenClaw-allowed subset of `registry`.
 * Throws if any tool listed in `TOOLSET_SUBSET` is missing from the live
 * registry (signals an upstream version drift that must be reconciled
 * before the skill can boot).
 *
 * Note: `--read-only` mode in the upstream package narrows `registry` to
 * `read.*` only BEFORE this filter runs; in that case the OpenClaw
 * subset shrinks accordingly (read tools only). That's the intended
 * behaviour — read-only is strictly subset of the read-only-allowed
 * portion of the OpenClaw subset.
 */
declare function selectOpenClawSubsetRegistry(registry: readonly ToolEntry[]): readonly ToolEntry[];
/** Boot the skill's MCP STDIO server. */
declare function runOpenClawSkill(): Promise<void>;

export { TOOLSET_EXCLUDED, TOOLSET_SUBSET, runOpenClawSkill, selectOpenClawSubsetRegistry };
