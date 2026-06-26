# Agency Division — 55+ Specialist Agents

All agent definitions live in `reference/agency-agents-main/`. Each file contains the agent's identity, personality, core mission, critical rules, workflow, and success metrics.

To activate any specialist, read their definition file and adopt their role.

## Engineering Division

Building and deploying technical systems.

| Agent | File | When to Activate |
|-------|------|-----------------|
| Frontend Developer | `reference/agency-agents-main/engineering/engineering-frontend-developer.md` | React/Vue/Angular, UI implementation, Core Web Vitals |
| Backend Architect | `reference/agency-agents-main/engineering/engineering-backend-architect.md` | API design, database architecture, microservices |
| Mobile App Builder | `reference/agency-agents-main/engineering/engineering-mobile-app-builder.md` | iOS/Android, React Native, Flutter |
| AI Engineer | `reference/agency-agents-main/engineering/engineering-ai-engineer.md` | ML models, AI integration, data pipelines |
| DevOps Automator | `reference/agency-agents-main/engineering/engineering-devops-automator.md` | CI/CD, infrastructure automation, monitoring |
| Rapid Prototyper | `reference/agency-agents-main/engineering/engineering-rapid-prototyper.md` | Fast POC/MVP, hackathon projects |
| Senior Developer | `reference/agency-agents-main/engineering/engineering-senior-developer.md` | Complex implementations, architecture decisions |

## Design Division

Visual design, user experience, and brand consistency.

| Agent | File | When to Activate |
|-------|------|-----------------|
| UI Designer | `reference/agency-agents-main/design/design-ui-designer.md` | Interface creation, component design, design systems |
| UX Researcher | `reference/agency-agents-main/design/design-ux-researcher.md` | User testing, behavior analysis, usability |
| UX Architect | `reference/agency-agents-main/design/design-ux-architect.md` | Technical architecture, CSS systems, developer-friendly foundations |
| Brand Guardian | `reference/agency-agents-main/design/design-brand-guardian.md` | Brand identity, consistency, positioning |
| Visual Storyteller | `reference/agency-agents-main/design/design-visual-storyteller.md` | Visual narratives, multimedia content, brand storytelling |
| Whimsy Injector | `reference/agency-agents-main/design/design-whimsy-injector.md` | Personality, micro-interactions, delight |
| Image Prompt Engineer | `reference/agency-agents-main/design/design-image-prompt-engineer.md` | AI image generation prompts, photography terminology, structured prompt crafting |

### Key Pairing: Image Prompt Engineer + Artist
The Image Prompt Engineer crafts detailed, structured prompts using photography terminology (aperture, focal length, lighting setups). Feed these prompts to the Artist agent for generation via xAI. This pairing produces significantly better results than raw text prompts.

## Marketing Division

Growth, content, and audience engagement.

| Agent | File | When to Activate |
|-------|------|-----------------|
| Growth Hacker | `reference/agency-agents-main/marketing/marketing-growth-hacker.md` | User acquisition, viral loops, conversion optimization |
| Content Creator | `reference/agency-agents-main/marketing/marketing-content-creator.md` | Multi-platform content, editorial calendars, copywriting |
| Twitter Engager | `reference/agency-agents-main/marketing/marketing-twitter-engager.md` | Twitter/X strategy, thought leadership |
| TikTok Strategist | `reference/agency-agents-main/marketing/marketing-tiktok-strategist.md` | Viral content, algorithm optimization, Gen Z audience |
| Instagram Curator | `reference/agency-agents-main/marketing/marketing-instagram-curator.md` | Visual storytelling, community building |
| Reddit Community Builder | `reference/agency-agents-main/marketing/marketing-reddit-community-builder.md` | Authentic engagement, value-driven content |
| App Store Optimizer | `reference/agency-agents-main/marketing/marketing-app-store-optimizer.md` | ASO, discoverability, app growth |
| Social Media Strategist | `reference/agency-agents-main/marketing/marketing-social-media-strategist.md` | Cross-platform strategy, campaigns |

## Product Division

Strategy, research, and prioritization.

| Agent | File | When to Activate |
|-------|------|-----------------|
| Sprint Prioritizer | `reference/agency-agents-main/product/product-sprint-prioritizer.md` | Agile planning, feature prioritization, backlog management |
| Trend Researcher | `reference/agency-agents-main/product/product-trend-researcher.md` | Market intelligence, competitive analysis |
| Feedback Synthesizer | `reference/agency-agents-main/product/product-feedback-synthesizer.md` | User feedback analysis, insights extraction |

## Project Management Division

Orchestration, timelines, and execution.

| Agent | File | When to Activate |
|-------|------|-----------------|
| Studio Producer | `reference/agency-agents-main/project-management/project-management-studio-producer.md` | Multi-project oversight, portfolio management |
| Project Shepherd | `reference/agency-agents-main/project-management/project-management-project-shepherd.md` | Cross-functional coordination, timeline management |
| Studio Operations | `reference/agency-agents-main/project-management/project-management-studio-operations.md` | Day-to-day efficiency, process optimization |
| Experiment Tracker | `reference/agency-agents-main/project-management/project-management-experiment-tracker.md` | A/B tests, hypothesis validation |
| Senior Project Manager | `reference/agency-agents-main/project-management/project-manager-senior.md` | Converting specs to tasks, realistic scoping |

### Key Role: Senior PM as Planner
The Senior PM is the primary Planner agent. When the team-builder PLANNER.md workflow runs, it draws from this agent's spec-to-task methodology: quote exact requirements, break into 30-60 min tasks, include acceptance criteria, no scope creep.

## Testing Division

Quality assurance and validation.

| Agent | File | When to Activate |
|-------|------|-----------------|
| Evidence Collector | `reference/agency-agents-main/testing/testing-evidence-collector.md` | Screenshot-based QA, visual proof, bug documentation |
| Reality Checker | `reference/agency-agents-main/testing/testing-reality-checker.md` | Production readiness, quality gates, evidence-based certification |
| Test Results Analyzer | `reference/agency-agents-main/testing/testing-test-results-analyzer.md` | Test evaluation, metrics analysis, coverage reporting |
| Performance Benchmarker | `reference/agency-agents-main/testing/testing-performance-benchmarker.md` | Speed testing, load testing, performance tuning |
| API Tester | `reference/agency-agents-main/testing/testing-api-tester.md` | API validation, endpoint verification, integration QA |
| Tool Evaluator | `reference/agency-agents-main/testing/testing-tool-evaluator.md` | Technology assessment, tool selection |
| Workflow Optimizer | `reference/agency-agents-main/testing/testing-workflow-optimizer.md` | Process analysis, efficiency gains, automation |

### Key Roles: Evidence Collector + Reality Checker as Reviewer
These two agents form the Reviewer pair in the REVIEWER.md workflow:
- **Evidence Collector**: First pass — screenshots, functional verification, issue finding (defaults to finding 3-5 issues)
- **Reality Checker**: Final gate — stops fantasy approvals, requires overwhelming evidence for production certification

## Support Division

Operations, finance, and compliance.

| Agent | File | When to Activate |
|-------|------|-----------------|
| Support Responder | `reference/agency-agents-main/support/support-support-responder.md` | Customer service, issue resolution |
| Analytics Reporter | `reference/agency-agents-main/support/support-analytics-reporter.md` | Business intelligence, KPI tracking, dashboards |
| Finance Tracker | `reference/agency-agents-main/support/support-finance-tracker.md` | Financial planning, budget management |
| Infrastructure Maintainer | `reference/agency-agents-main/support/support-infrastructure-maintainer.md` | System reliability, monitoring |
| Legal Compliance Checker | `reference/agency-agents-main/support/support-legal-compliance-checker.md` | Compliance, regulations, risk management |
| Executive Summary Generator | `reference/agency-agents-main/support/support-executive-summary-generator.md` | C-suite communication, strategic summaries |

## Spatial Computing Division

Immersive technologies (AR/VR/XR).

| Agent | File | When to Activate |
|-------|------|-----------------|
| XR Interface Architect | `reference/agency-agents-main/spatial-computing/xr-interface-architect.md` | Spatial interaction design, immersive UX |
| macOS Spatial/Metal Engineer | `reference/agency-agents-main/spatial-computing/macos-spatial-metal-engineer.md` | Swift, Metal, high-performance 3D, Vision Pro native |
| XR Immersive Developer | `reference/agency-agents-main/spatial-computing/xr-immersive-developer.md` | WebXR, browser-based AR/VR |
| XR Cockpit Interaction Specialist | `reference/agency-agents-main/spatial-computing/xr-cockpit-interaction-specialist.md` | Cockpit controls, immersive control systems |
| visionOS Spatial Engineer | `reference/agency-agents-main/spatial-computing/visionos-spatial-engineer.md` | Apple Vision Pro development |
| Terminal Integration Specialist | `reference/agency-agents-main/spatial-computing/terminal-integration-specialist.md` | CLI tools, terminal workflows |

## Specialized Division

Cross-functional coordination and deep analytics.

| Agent | File | When to Activate |
|-------|------|-----------------|
| Agents Orchestrator | `reference/agency-agents-main/specialized/agents-orchestrator.md` | Multi-agent pipeline management, NEXUS controller |
| Agentic Identity & Trust Architect | `reference/agency-agents-main/specialized/agentic-identity-trust.md` | Agent identity, trust frameworks |
| Data Analytics Reporter | `reference/agency-agents-main/specialized/data-analytics-reporter.md` | Deep data analysis, business metrics |
| LSP/Index Engineer | `reference/agency-agents-main/specialized/lsp-index-engineer.md` | Code intelligence, semantic indexing |
| Sales Data Extraction Agent | `reference/agency-agents-main/specialized/sales-data-extraction-agent.md` | Sales metric extraction, Excel monitoring |
| Data Consolidation Agent | `reference/agency-agents-main/specialized/data-consolidation-agent.md` | Data aggregation, dashboard reports |
| Report Distribution Agent | `reference/agency-agents-main/specialized/report-distribution-agent.md` | Automated report delivery |

## Quick Activation Template

To activate any specialist, use this prompt pattern:

```
Activate [Agent Name] from the Agency [Division] division.

Read the full agent definition at:
reference/agency-agents-main/[division]/[filename].md

Task: [TASK DESCRIPTION]
Acceptance criteria: [WHAT DONE LOOKS LIKE]
Context: [RELEVANT FILES AND STATE]
Reviewer: [WHO VALIDATES — Evidence Collector or Reality Checker]
```

For ready-to-use activation prompts for every agent, see:
`reference/agency-agents-main/strategy/coordination/agent-activation-prompts.md`
