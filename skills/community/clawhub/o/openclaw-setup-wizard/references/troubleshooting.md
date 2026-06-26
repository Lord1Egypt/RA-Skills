# Troubleshooting Reference

## Gateway Issues

### Gateway won't start
```bash
openclaw gateway status          # Check current state
openclaw gateway restart         # Force restart
lsof -ti:3000 | xargs kill -9   # Kill port conflicts
```

### Gateway crashes repeatedly
- Check logs: `openclaw gateway logs`
- Verify Node.js version: `node --version` (need v20+)
- Check LaunchAgent: `launchctl list | grep openclaw`
- Reinstall: `npm install -g openclaw`

## Provider Issues

### API key errors
- Verify key in `~/.openclaw/agents/main/agent/models.json`
- Test directly: `openclaw models status`
- Check provider dashboard for quota/billing

### Model not responding
- Check fallback: `openclaw models fallbacks list`
- Try different model: `openclaw models set <alternative>`
- Test connectivity: `curl -s https://api.openai.com/v1/models`

### Rate limiting
- Add fallback models to auto-switch
- Use local model (Ollama) as last resort
- Check provider rate limits and upgrade if needed

## Channel Issues

### Telegram bot not responding
- Verify token with @BotFather
- Check allowFrom includes your user ID
- Restart gateway after config changes
- Ensure bot isn't blocked or deleted

### Messages not arriving
- Check `allowFrom` whitelist (empty = allow all)
- Verify channel is enabled in config
- Check firewall/network connectivity
- Review gateway logs for errors

## Skill Issues

### Skill not triggering
- Check skill description matches user intent
- Verify SKILL.md frontmatter is valid YAML
- Check skill is in correct directory
- Restart gateway after adding skills

### Skill script fails
- Check script permissions: `chmod +x script.sh`
- Verify dependencies installed
- Test script manually first
- Check macOS vs Linux compatibility

## Performance Issues

### Slow responses
- Check model latency (try faster model)
- Monitor memory: `vm_stat` (macOS) or `free -h` (Linux)
- Check disk space: `df -h`
- Reduce context window (trim MEMORY.md)

### High memory usage
- Restart gateway periodically
- Limit concurrent sessions
- Use lighter models for simple tasks

## Backup/Recovery

### Restore from backup
```bash
# List backups
ls ~/backups/openclaw/

# Restore (stop gateway first)
openclaw gateway stop
tar xzf ~/backups/openclaw/BACKUP_FILE.tar.gz -C ~/.openclaw/workspace/
openclaw gateway start
```

### Config corrupted
```bash
# Reset to defaults
openclaw configure --reset
# Then reconfigure providers and channels
```
