# Capability Matrix (Role -> Tools/Skills/Permissions)

Use this matrix to derive per-agent provisioning plans.

## Global mandatory role

### team-leader
- required_tools: read, write
- optional_tools: sessions_send
- required_skills: none
- permission_profile: team-leader-standard

## Product + Engineering baseline

### product-manager
- required_tools: read, write
- optional_tools: web_search, web_fetch
- required_skills: none (domain-specific optional)
- permission_profile: planner-low-risk

### tech-architect
- required_tools: read, write, edit
- optional_tools: exec
- required_skills: none
- permission_profile: architect-standard

### backend-engineer
- required_tools: read, write, edit, exec
- optional_tools: process
- required_skills: github (optional by repo workflow)
- permission_profile: builder-standard

### frontend-engineer
- required_tools: read, write, edit, exec
- optional_tools: browser
- required_skills: agent-browser (optional)
- permission_profile: builder-standard

### qa-engineer
- required_tools: read, write, exec
- optional_tools: browser, process
- required_skills: none
- permission_profile: tester-standard

## Growth + Marketing baseline

### growth-lead
- required_tools: read, write, web_search, web_fetch
- optional_tools: browser
- required_skills: none
- permission_profile: planner-low-risk

### campaign-operator
- required_tools: read, write, web_search, web_fetch
- optional_tools: browser
- required_skills: none
- permission_profile: operator-standard

### performance-analyst
- required_tools: read, write
- optional_tools: web_search, web_fetch
- required_skills: none
- permission_profile: analyst-low-risk

## Notes
- Keep minimum viable tools by default.
- Add tools only when a role has explicit deliverables requiring them.
- Mark uncertain skills as optional and ask for confirmation before install.
