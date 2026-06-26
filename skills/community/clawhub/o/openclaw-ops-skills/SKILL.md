# OpenClaw Ops Skills Pack

> **Production-ready skills for autonomous agent operations**

## Metadata

**Name**: Ops Skills Pack
**Version**: 1.0.0
**Category**: Operations
**Author**: Eric Jie <jxmerich@mail.com>
**License**: MIT
**Compatibility**: OpenClaw >= 2.0.0
**Repository**: https://github.com/Erich1566/openclaw-ops-skills

## Description

Transform your OpenClaw agent from a chatbot into production-ready autonomous infrastructure. Based on 1.4+ billion tokens of real-world testing, this skill pack provides the guardrails, workflows, and best practices needed for autonomous operations that work while you sleep.

## Skills Included (14)

### Core Infrastructure
1. **model-routing** - Optimize model selection for 80% cost reduction
2. **execution-discipline** - Enforce Build→Test→Document→Decide cycle
3. **docs-first** - Mandatory reconnaissance before code changes
4. **scope-control** - Define and enforce operational boundaries
5. **task-autonomy** - Self-expanding task management
6. **progress-logging** - Comprehensive execution logs

### Operations
7. **memory-persistence** - File-based memory system
8. **cron-orchestration** - Scheduled autonomous operations
9. **error-recovery** - Graceful failure handling
10. **security-hardening** - Security best practices

### Advanced
11. **cost-optimization** - Token waste prevention
12. **testing-protocol** - Quality assurance standards
13. **communication** - Structured update templates
14. **integration-guide** - Safe third-party connections

## Key Benefits

- **80% Cost Reduction** - Intelligent model routing (Sonnet 4.6 for daily work)
- **True Autonomy** - Self-expanding task lists continue work overnight
- **Persistent Memory** - Survives session compression
- **Complete Visibility** - Morning briefings replace chat history scrolling
- **Security Hardened** - Built-in security practices

## Quick Start

```bash
# Install skills
cp skills/*.md ~/.openclaw/workspace/skills/

# Set up workspace templates
cp templates/*.md ~/.openclaw/workspace/

# Configure model routing (see README.md)

# Set up cron jobs
openclaw cron add --name "overnight-2am" --cron "0 2 * * *" \
  --message "Check Todo.md. Continue work. Log progress."

# Restart
openclaw restart
```

## Requirements

- OpenClaw 2.0+
- 15 minutes for initial setup
- Willingness to treat configuration as work

## Documentation

- **README.md** - Full documentation
- **QUICKSTART.md** - 15-minute setup guide
- **FEATURES.md** - Bilingual feature guide
- **DESCRIPTION.md** - Project overview

## Installation Order

**Week 1**: Core skills (model-routing, execution-discipline, scope-control)
**Week 2**: Operational skills (docs-first, task-autonomy, progress-logging)
**Week 3**: Advanced skills (memory-persistence, cron-orchestration, error-recovery)

## Support

- GitHub: https://github.com/yourusername/openclaw-ops-skills
- Issues: Report bugs and request features
- Discussions: Ask questions and share experiences
