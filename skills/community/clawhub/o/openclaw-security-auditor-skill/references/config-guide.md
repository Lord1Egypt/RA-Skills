# OpenClaw Security Configuration Guide

## Modern OpenClaw Configuration Structure

### Key Configuration Sections

#### Gateway Configuration
```json
{
  "gateway": {
    "bind": "loopback",           // Binding modes: loopback, lan, custom, tailnet, auto
    "auth": {
      "mode": "token",            // Authentication modes: token, password, none
      "token": "your-64-char-token"
    },
    "tailscale": {
      "mode": "off"               // Tailscale modes: off, auto, manual
    }
  }
}
```

#### Tools Configuration
```json
{
  "tools": {
    "profile": "coding",          // Tool profiles: messaging, coding, full
    "fs": {
      "workspaceOnly": true       // Restrict filesystem access to workspace
    },
    "web": {
      "search": {
        "enabled": true           // Enable web search capabilities
      }
    }
  }
}
```

#### Session Configuration
```json
{
  "session": {
    "dmScope": "per-channel-peer" // Session scopes: paired, per-channel-peer, any
  }
}
```

#### Logging Configuration
```json
{
  "logging": {
    "level": "info"               // Log levels: debug, info, warn, error
  }
}
```

## Security Best Practices

### Gateway Security
1. **Always use `loopback` binding** for production environments
2. **Never use `lan` or `custom` binding** without proper network security
3. **Use strong token authentication** (64+ characters)
4. **Disable Tailscale** in conservative mode
5. **Regularly rotate authentication tokens**

### Tools Security
1. **Use minimal tool profile** required for your use case
   - `messaging`: Basic messaging only
   - `coding`: Development tools enabled  
   - `full`: All tools enabled (high risk)
2. **Always enable `workspaceOnly`** to restrict filesystem access
3. **Disable unnecessary web capabilities** if not needed

### Session Security
1. **Use `paired` scope** for maximum security (conservative mode)
2. **Use `per-channel-peer`** for balanced security (recommended)
3. **Avoid `any` scope** except in isolated test environments
4. **Consider manual pairing strategy** for sensitive deployments

### Network Security
1. **Enable system firewall** (UFW/iptables)
2. **Monitor open ports** regularly
3. **Use Tailscale for remote access** instead of direct internet exposure
4. **Regular security audits** using this tool

## Common Security Issues and Fixes

### Issue: Gateway bound to external interface
- **Risk**: External network exposure
- **Fix**: Set `gateway.bind` to `"loopback"`

### Issue: No authentication enabled  
- **Risk**: Unauthorized access
- **Fix**: Set `gateway.auth.mode` to `"token"` and generate strong token

### Issue: Full tool permissions
- **Risk**: Arbitrary code execution
- **Fix**: Set `tools.profile` to `"coding"` or `"messaging"`

### Issue: Permissive session scope
- **Risk**: Anyone can start sessions
- **Fix**: Set `session.dmScope` to `"per-channel-peer"` or `"paired"`

### Issue: No system firewall
- **Risk**: Network-level attacks
- **Fix**: Enable UFW with `sudo ufw enable`

## Configuration Validation

### Valid Gateway Bind Values
- ✅ `loopback` - Localhost only (recommended)
- ✅ `lan` - Local network only (use with caution)  
- ✅ `tailnet` - Tailscale network only
- ✅ `auto` - Automatic detection
- ❌ IP addresses like `127.0.0.1`, `0.0.0.0` (legacy format)

### Valid Authentication Modes
- ✅ `token` - Token-based authentication (recommended)
- ✅ `password` - Password authentication  
- ✅ `none` - No authentication (high risk, testing only)

### Valid Tool Profiles
- ✅ `messaging` - Minimal permissions
- ✅ `coding` - Development tools enabled
- ✅ `full` - All tools enabled (high risk)

### Valid Session Scopes
- ✅ `paired` - Explicit pairing required (most secure)
- ✅ `per-channel-peer` - Channel-based sessions (recommended)  
- ✅ `any` - Any direct message creates session (least secure)

## Security Audit Checklist

### Before Production Deployment
- [ ] Gateway bound to `loopback`
- [ ] Strong token authentication enabled
- [ ] Tool profile set to minimum required
- [ ] Session scope appropriately restricted
- [ ] System firewall enabled
- [ ] Regular security audit scheduled

### For Development Environments
- [ ] Gateway bound to `loopback` 
- [ ] Token authentication enabled
- [ ] Tool profile set to `coding`
- [ ] Session scope set to `per-channel-peer`
- [ ] Workspace isolation enabled

### For Test Environments
- [ ] Isolated from production networks
- [ ] No sensitive data present
- [ ] Temporary configurations documented
- [ ] Cleanup procedures established

## Troubleshooting Common Errors

### "Config validation failed: gateway.bind host aliases are legacy"
- **Cause**: Using IP addresses instead of bind modes
- **Solution**: Use `loopback`, `lan`, `tailnet`, or `auto` instead of IP addresses

### "Config validation failed: gateway.controlUi: Invalid input: expected object"
- **Cause**: Control UI configuration changed format
- **Solution**: Check current OpenClaw documentation for correct control UI format

### "Unrecognized key: logging.maskSensitive"
- **Cause**: Configuration key removed in newer versions
- **Solution**: Remove this key, use appropriate log level instead

## Version Compatibility Notes

### OpenClaw 2026.3.x+
- Uses `session` (singular) instead of `sessions` (plural)
- Uses bind modes instead of IP addresses
- Tool profiles replace individual tool permissions
- Enhanced security defaults

### Migration from Older Versions
1. Replace IP addresses with bind modes
2. Update `sessions` to `session` 
3. Consolidate tool permissions into profiles
4. Review all security settings against new best practices