# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-12

### Added

- Initial release as **ihrflow-hr** (rebranded from hireflow-hr)
- Pure Skill MCP Client mode — no plugins required; the skill acts as an MCP Client via `scripts/mcp-call.sh`
- Per-user credential-based authentication using the `login` MCP tool
- 20 MCP tools covering the full recruitment lifecycle
  - **Auth**: `login`
  - **Candidates**: `search_candidates`, `get_resume_detail`, `add_resume_note`, `recommend_candidate_for_position`
  - **Positions**: `list_positions`, `get_position_detail`, `get_position_candidates`, `update_position_status`, `create_recruitment_need`
  - **Interviews**: `list_interviews`, `get_interview_detail`, `create_interview`, `cancel_interview`, `reschedule_interview`
  - **Pipeline**: `update_screening_status` (HR/dept/final approve/reject)
  - **Evaluations**: `submit_interview_feedback`
  - **Search**: `search_talent` (AI semantic search)
  - **Statistics**: `get_recruitment_statistics`, `get_today_schedule`
- 2 MCP resources: `ihrflow://recruitment/overview`, `ihrflow://positions/active`
- HR domain knowledge (recruitment funnel, position lifecycle, interview states)
- 6 workflow recipes (daily briefing, talent search, interview lifecycle, position creation, pipeline review, interview rescheduling)
- Environment variables: `IHRFLOW_MCP_URL`, `IHRFLOW_USERNAME`, `IHRFLOW_PASSWORD`, `IHRFLOW_TENANT_ID`, `IHRFLOW_API_KEY`
- Chinese language support
