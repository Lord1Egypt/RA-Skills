---
name: senior-architect
description: Design system architecture, evaluate patterns, and produce architecture artifacts. Use when designing a new system or reviewing an existing one, choosing between monolith and microservices, selecting a database or tech stack, creating architecture diagrams (Mermaid, PlantUML, ASCII), writing ADRs, analyzing dependencies, or planning for scalability.
compatibility: Requires Python 3.8+ for scripts in scripts/.
---

# Senior Architect

Turn architecture questions into structured decisions and validated artifacts.

## Activation

Use this skill when the user asks to:
- design or review a system architecture
- choose between monolith, microservices, or a hybrid approach
- select a database, framework, or cloud service
- generate architecture diagrams from a project
- analyze dependencies for coupling or circular references
- write an Architecture Decision Record (ADR)
- assess scalability, fault tolerance, or domain boundaries

## Workflow

1. **Classify** the request: `design` | `diagram` | `dependency` | `decision` | `review`.
2. **Load the relevant reference**:
   - architecture patterns, monolith vs microservices → `{baseDir}/references/architecture_patterns.md`
   - database / tech stack selection → `{baseDir}/references/tech_decision_guide.md`
   - capacity planning, API design, migration planning → `{baseDir}/references/system_design_workflows.md`
3. **Run the appropriate script** when a project directory is available:
   ```bash
   # Generate architecture diagram (mermaid | plantuml | ascii)
   python {baseDir}/scripts/architecture_diagram_generator.py ./project --format mermaid

   # Analyze dependencies for coupling and circular references
   python {baseDir}/scripts/dependency_analyzer.py ./project --verbose

   # Detect architectural patterns and code organization issues
   python {baseDir}/scripts/project_architect.py ./project --verbose
   ```
4. **Apply the decision framework**: state the options, the trade-offs, and the recommendation with rationale.
5. **Emit the artifact**: diagram, ADR, or assessment report — one primary artifact per response.

## Output Contract

- Open with the dominant architectural tension or decision.
- Emit one primary artifact (diagram, ADR, or assessment).
- For ADRs: include Context, Options, Decision, and Trade-offs sections.
- Annotate non-obvious decisions in diagrams.
- Close with the next recommended step (e.g., "extract service X when team Y reaches N people").

## Key Rules

- Default to **modular monolith** for teams under 10. Document when microservices are justified.
- Every architecture recommendation must state the trade-offs accepted, not just the benefits.
- Use `{baseDir}/references/tech_decision_guide.md` decision matrices before recommending a specific database or framework — do not default to a stack based on recency.
- Flag circular dependencies as blocking issues; flag coupling scores >70 as warnings.

## Guardrails

- Do not generate implementation code (controllers, services, repositories) — stay at architecture level.
- Do not recommend microservices to teams that have not yet identified stable domain boundaries.
- Do not produce diagrams without first identifying the services/components from the project or the user's description.
- Stay within architecture, design, and decision scope; for container/deployment specifics refer to `docker-development` or `senior-devops`.

## Self Check

Before emitting any artifact, verify:
- the chosen pattern matches the team size and operational maturity stated;
- trade-offs are explicitly listed alongside benefits;
- the diagram matches the described system (no invented components);
- dependency issues are graded by severity.
