# MCP TOOL PROTOCOL AND PER-AGENT SUBSETS

All tools in this harness are accessed via MCP (Model Context Protocol), the standardized
unified interface for agent-to-tool communication. No agent calls tools directly.

---

## WHY MCP

MCP provides:
  - Standardized request/response format across all tool types
  - Centralized routing through the tool-router (tools/tool-router.md)
  - Consistent logging, redaction, and safety enforcement
  - Tool isolation: the tool implementation runs outside the agent's context
  - Audit trail: all MCP calls are logged (metadata only)

---

## TOOL SUBSET RULE

Every agent is provisioned with only the tools its role requires.
Excess tools increase context token usage, increase hallucination risk,
produce worse results, and violate the principle of least privilege.

The dispatcher is responsible for assigning tool subsets at dispatch time.
See agents/dispatcher.md DISPATCH FORMAT -> TOOLS ALLOWED field.

---

## PER-AGENT TOOL SUBSETS

SENSITIVE PATH POLICY applies to ALL agents that use read_file or list_dir.
See references/sensitive-paths.md. The tool router blocks forbidden paths.
Agents must also apply the policy before making any read call.

researcher_agent:
  read_file, list_dir, search_code, collect_logs, git_status, git_diff
  -- read-only, no writes
  -- must filter file lists against references/sensitive-paths.md before dispatching
     sub-researchers; sub-researchers receive pre-filtered lists

planner_agent:
  read_file, write_file(docs/ only), search_code
  -- write limited to plan output only

implementer_agent:
  read_file, write_file(src/ and tests/ only), search_code,
  run_unit_tests, git_status, git_commit
  -- no PR creation, no broad directory scanning

reviewer_agent:
  read_file, search_code, run_unit_tests, run_integration_tests,
  scan_vulnerabilities, git_diff
  -- no write tools (except review markdown output)

tester_agent:
  run_unit_tests, run_integration_tests, run_e2e_tests, run_fuzz_tests, collect_logs,
  write_file(tests/ only)

debugger_agent:
  read_file, search_code, collect_logs, git_diff, run_unit_tests, code_search,
  dependency_lookup
  -- web_search with staging gate (output to docs/generated/search-staging/ only)

optimizer_agent:
  read_file, search_code, performance_profile, collect_logs, dependency_audit

doc_writer_agent:
  read_file, list_dir, write_file(docs/ only), search_code

garbage_collector_agent:
  read_file, list_dir, search_code, git_diff, performance_profile

dispatcher (orchestrator only):
  All tools needed to spawn sub-agents and read their outputs.
  Does not call implementation tools directly.

---

## SANDBOX ISOLATION

Generated code execution (tests, linters, scripts) runs in an isolated sandbox:
  - The sandbox has NO access to the harness security context
  - The sandbox has NO access to environment variables or credentials
  - Each execution gets a fresh, ephemeral environment
  - The sandbox can communicate results back only through structured output files

The harness agent and the sandbox are separate security contexts.
This ensures that unintended directives in test output cannot reach the harness.
(Rationale: Vercel security boundary model -- harness compute separate from
 generated code compute.)

---

## MCP CALL FORMAT

All agents use this structure when requesting a tool call:

TOOL:     <tool name from TOOL_REGISTRY.md>
INPUT:    <parameters -- no authentication material or credentials>
EXPECT:   <what a successful result looks like>
VALIDATE: <how the agent will verify correctness>
PLAN REF: <PLAN-NNN.md that authorized this action>

The tool-router validates all fields before execution.
See tools/execution-protocol.md for the full lifecycle.
