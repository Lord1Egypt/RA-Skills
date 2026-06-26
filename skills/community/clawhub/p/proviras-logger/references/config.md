# Agent Config

agentId: (populated automatically on first heartbeat)

# Notes
- agentId is written here by scripts/register.sh on first run
- Do not edit agentId manually
- skills_used per task are inferred from session logs automatically
- Registration always sends `userId` (PROVIRAS_PARENT_ID — the overarching human user's ID) and `platform` (PROVIRAS_PLATFORM — set by the agent at registration time). When spawned by another agent, `parentAgentId` (PROVIRAS_USER_ID — the owner agent's ID) is also sent
- When spawning a sub-agent, pass the same PROVIRAS_PARENT_ID through unchanged and set PROVIRAS_USER_ID to this agentId