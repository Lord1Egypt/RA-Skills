# Council of Wisdom - Skill Package

A sophisticated multi-agent AI debate framework with structured voting, automatic cleanup, multi-LLM provider support, and enterprise-grade monitoring.

## Quick Start

```bash
# Initialize a new council workspace
council-of-wisdom init strategic-decisions

# Run a debate
council-of-wisdom debate \
  "Should we use microservices or monolithic architecture?" \
  --domain software-architecture \
  --perspective-a "Microservices offer scalability" \
  --perspective-b "Monolith offers simplicity"

# View the outcome report
council-of-wisdom report latest
```

## Features

- **Structured Debate:** Two expert agents debate opposing viewpoints
- **Council of 9 Experts:** Specialized analytical frameworks evaluate arguments
- **Automatic Cleanup:** Agents terminated and context cleared after voting
- **Multi-LLM Support:** Different providers for diverse reasoning
- **Enterprise Monitoring:** 5-cadence operating rhythm
- **Testing Framework:** Unit, integration, quality, and performance tests
- **Feedback Loops:** Continuous optimization and improvement
- **GitHub Integration:** Private repos with issue tracking and releases

## Architecture

```
Query → Referee → 2 Debaters → Council of 9 → Vote → Outcome Report → Cleanup
```

## Workspace Structure

```
council-of-wisdom/<project>/
├── workspace/
│   ├── strategy.md              # Council purpose and decision criteria
│   ├── monitoring/              # Metrics and dashboards
│   ├── testing/                 # Test cases and quality checks
│   ├── feedback/                # User feedback and improvements
│   ├── prompts/                 # Agent prompts (referee, debaters, council)
│   ├── agents/                  # Agent configurations
│   ├── logs/                    # Debate transcripts and votes
│   └── reports/                 # Outcome reports
├── .github/                     # GitHub Actions and issues
└── README.md                    # Project documentation
```

## Installation

This skill is installed in OpenClaw. The CLI is available at:

```bash
~/.openclaw/workspace/skills/council-of-wisdom/scripts/council-of-wisdom.sh
```

Add to PATH for convenience:

```bash
export PATH="$PATH:~/.openclaw/workspace/skills/council-of-wisdom/scripts"
```

Or create a symlink:

```bash
sudo ln -s ~/.openclaw/workspace/skills/council-of-wisdom/scripts/council-of-wisdom.sh /usr/local/bin/council-of-wisdom
```

## Documentation

Full documentation in **SKILL.md**:

- Complete architecture overview
- Council of 9 expert specializations
- Monitoring and metrics framework
- Testing and optimization procedures
- Troubleshooting guide

## Requirements

- OpenClaw with ACP (Agent Control Panel) for agent spawning
- GitHub CLI (`gh`) for repo integration (optional but recommended)
- Bash shell for CLI

## License

MIT License - See LICENSE file for details

## Contributing

This is part of Fayez's OpenClaw workspace. Contributions and improvements welcome.

---

**Council of Wisdom: Structured debate, collective intelligence, actionable decisions.**
