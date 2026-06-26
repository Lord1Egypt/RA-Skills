# OpenClaw Common Queries and Solutions

This reference file contains frequently asked questions and their authoritative answers based on official documentation and source code.

## Configuration Questions

### How to configure channels?
- **Documentation**: https://docs.openclaw.ai/guides/channels
- **Key files**: `~/.openclaw/config.json`, channel-specific config sections
- **Common issues**: Missing API tokens, incorrect webhook URLs, permission issues

### How to set up skills?
- **Documentation**: https://docs.openclaw.ai/guides/skills
- **Commands**: `clawhub install <skill>`, `openclaw skills list`
- **Locations**: Global skills in `~/.openclaw/skills/`, workspace skills in `workspace/skills/`

### How to manage agents?
- **Documentation**: https://docs.openclaw.ai/architecture/agents
- **Configuration**: Agent routing, workspace isolation, capability delegation

## Troubleshooting

### Gateway connection issues
- Check if gateway is running: `openclaw gateway status`
- Verify port configuration (default: 18789)
- Check firewall settings and network connectivity

### Skill not appearing in Gateway
- Skills must be in correct directory structure
- SKILL.md must have proper YAML frontmatter
- Gateway may need restart to detect new skills

### Authentication problems
- Verify tokens are correctly configured
- Check token expiration for services like Telegram, Discord
- Ensure proper permissions are granted

## Best Practices

### Security considerations
- Never expose gateway to public internet without authentication
- Use allowlists for group messages
- Regular security audits with healthcheck skill

### Performance optimization  
- Use appropriate model selection for different tasks
- Configure reasonable timeouts and limits
- Monitor resource usage and logs

### Development workflow
- Test skills in isolated environments first
- Use version control for custom skills
- Follow skill creation guidelines for consistency

## Command Reference

### Essential CLI commands
- `openclaw --help` - Main help
- `openclaw gateway [start|stop|status]` - Gateway management
- `openclaw skills [list|info]` - Skill management
- `openclaw channels [login|status]` - Channel management
- `openclaw config [get|set]` - Configuration management

### Debugging commands
- `openclaw logs` - View gateway logs
- `openclaw doctor` - Health checks
- `openclaw status` - System status overview

## File Structure Reference

### Key directories
- `~/.openclaw/` - Main OpenClaw directory
- `~/.openclaw/skills/` - Global skills directory
- `~/.openclaw/agents/` - Agent workspaces
- `~/.openclaw/config.json` - Main configuration file

### Workspace structure
- `workspace/SOUL.md` - Agent personality
- `workspace/USER.md` - User information  
- `workspace/MEMORY.md` - Long-term memory
- `workspace/skills/` - Workspace-specific skills