# Installation Guide - Human-Rent v0.2.0

Complete step-by-step installation and setup guide for the Human-Rent skill.

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL
- **Node.js**: Version 18.0.0 or higher
- **ClawHub CLI**: Latest version
- **Internet Connection**: Required for API access

### Check Prerequisites

```bash
# Check Node.js version
node --version
# Should output: v18.0.0 or higher

# Check npm is available
npm --version

# Check ClawHub is installed
clawhub --version
```

If Node.js is not installed, visit https://nodejs.org/

## Step 1: Install the Skill

Install the Human-Rent skill from ClawHub:

```bash
clawhub install human-rent
```

Expected output:
```
✓ Installing human-rent v0.2.0...
✓ Verifying package integrity...
✓ Setting up CLI...
✓ Installation complete!

Next steps:
1. Set up credentials: https://www.zhenrent.com/api/keys
2. Export environment variables
3. Test connection: human-rent test
```

### Verify Installation

Check that the CLI is available:

```bash
human-rent --version
# Output: human-rent v0.2.0

human-rent help
# Should display help documentation
```

## Step 2: Get API Credentials

### Create ZhenRent Account

1. Visit https://www.zhenrent.com
2. Click "Sign Up" or "Get Started"
3. Complete registration
4. Verify email address

### Generate API Keys

1. Log in to https://www.zhenrent.com
2. Navigate to https://www.zhenrent.com/api/keys
3. Click "Create New API Key"
4. Name your key (e.g., "OpenClaw Agent")
5. Copy the API Key and API Secret immediately
   - API Key: Starts with `zr_key_`
   - API Secret: Starts with `zr_secret_`
   - **Important**: API Secret is only shown once. Save it securely!

### Secure Credential Storage

**DO NOT** commit credentials to version control!

Create a secure credential file:

```bash
# Option 1: Add to shell profile (recommended)
echo 'export ZHENRENT_API_KEY="zr_key_your_key_here"' >> ~/.bashrc
echo 'export ZHENRENT_API_SECRET="zr_secret_your_secret_here"' >> ~/.bashrc
source ~/.bashrc

# Option 2: Add to shell profile (macOS)
echo 'export ZHENRENT_API_KEY="zr_key_your_key_here"' >> ~/.zshrc
echo 'export ZHENRENT_API_SECRET="zr_secret_your_secret_here"' >> ~/.zshrc
source ~/.zshrc

# Option 3: Create .env file (for project-specific use)
cat > ~/.human-rent.env <<EOF
export ZHENRENT_API_KEY="zr_key_your_key_here"
export ZHENRENT_API_SECRET="zr_secret_your_secret_here"
EOF

# Then source before use:
source ~/.human-rent.env
```

## Step 3: Configure Environment

### Required Environment Variables

Set up your credentials:

```bash
export ZHENRENT_API_KEY="zr_key_your_key_here"
export ZHENRENT_API_SECRET="zr_secret_your_secret_here"
```

### Optional Environment Variables

```bash
# Custom API endpoint (default: https://www.zhenrent.com/api/v1)
export ZHENRENT_BASE_URL="https://www.zhenrent.com/api/v1"

# Auto-confirm dispatches (USE WITH CAUTION)
# Only for non-interactive/automated environments
export HUMAN_RENT_AUTO_CONFIRM="false"
```

### Verify Environment

Check that credentials are set:

```bash
echo $ZHENRENT_API_KEY
# Should output: zr_key_your_key_here (not empty)

echo $ZHENRENT_API_SECRET
# Should output: zr_secret_your_secret_here (not empty)
```

## Step 4: Test Connection

Test that everything is working:

```bash
human-rent test
```

Expected output:
```
========================================
HUMAN-RENT TEST MODE
========================================

Testing API connection...

1. Testing worker list endpoint...
   ✓ Success: Found 42 workers

2. Testing credentials...
   ✓ API Key: zr_key_abc...
   ✓ API Secret: [REDACTED]

All tests passed! ✅

You can now dispatch tasks with:
  human-rent dispatch "Your task instruction here"
```

### Troubleshooting Test Failures

#### Error: "Missing credentials"

**Problem**: Environment variables not set

**Solution**:
```bash
export ZHENRENT_API_KEY="your-key"
export ZHENRENT_API_SECRET="your-secret"
```

#### Error: "Authentication failed"

**Problem**: Invalid credentials

**Solutions**:
1. Verify credentials are correct (check for typos)
2. Regenerate API keys at https://www.zhenrent.com/api/keys
3. Ensure API key is not expired or revoked

#### Error: "Network error"

**Problem**: Cannot reach API

**Solutions**:
1. Check internet connection
2. Verify API endpoint: `echo $ZHENRENT_BASE_URL`
3. Check firewall settings
4. Try different network (not behind corporate proxy)

#### Error: "Node.js version"

**Problem**: Node.js version too old

**Solution**:
```bash
# Update Node.js to v18+
# Visit https://nodejs.org/ for installation instructions
```

## Step 5: Dispatch Your First Task

### Basic Task

```bash
human-rent dispatch "Take a photo of the Golden Gate Bridge"
```

You'll be prompted:
```
========================================
DISPATCH CONFIRMATION REQUIRED
========================================

Task Details:
  Description: Take a photo of the Golden Gate Bridge
  Location: (not specified)
  Estimated Cost: $15-20
  Estimated Time: 15 minutes

This will dispatch a real human worker to perform a physical task.
You will be charged for this service.

Dispatch human worker? [y/N]:
```

Type `y` and press Enter to confirm.

### Task with Location

```bash
human-rent dispatch "Verify address 123 Main St exists" \
  --location="37.7749,-122.4194"
```

### Task with Budget

```bash
human-rent dispatch "Inspect warehouse condition" \
  --location="37.7749,-122.4194" \
  --budget="$50"
```

## Step 6: Check Task Status

After dispatching a task, you'll receive a task ID:

```
✓ Task dispatched successfully!

Task Details:
  Task ID: task_abc123def456
  Status: assigned
  Estimated completion: 2026-03-31 14:30:00

Check status with: human-rent status task_abc123def456
```

Check the status:

```bash
human-rent status task_abc123def456
```

Or wait for completion:

```bash
human-rent status task_abc123def456 --wait
```

## Step 7: List Available Workers

See available human workers:

```bash
human-rent humans
```

Filter by location:

```bash
human-rent humans --location="37.7749,-122.4194" --radius=10000
```

Search by skills:

```bash
human-rent humans --skills="photography,legal_reading"
```

## Advanced Configuration

### Multiple Environments

Manage different environments (dev, staging, prod):

```bash
# Development
cat > ~/.human-rent-dev.env <<EOF
export ZHENRENT_API_KEY="zr_key_dev_key"
export ZHENRENT_API_SECRET="zr_secret_dev_secret"
export ZHENRENT_BASE_URL="https://dev.zhenrent.com/api/v1"
EOF

# Production
cat > ~/.human-rent-prod.env <<EOF
export ZHENRENT_API_KEY="zr_key_prod_key"
export ZHENRENT_API_SECRET="zr_secret_prod_secret"
export ZHENRENT_BASE_URL="https://www.zhenrent.com/api/v1"
EOF

# Switch environments
source ~/.human-rent-dev.env    # Development
source ~/.human-rent-prod.env   # Production
```

### Automation Setup

For non-interactive/automated environments:

```bash
# Enable auto-confirm (skips confirmation prompts)
export HUMAN_RENT_AUTO_CONFIRM=true

# Now dispatches won't prompt for confirmation
human-rent dispatch "Automated task"
```

**WARNING**: Only use auto-confirm in trusted, controlled environments. You will be charged for all dispatched tasks.

### Logging

Enable detailed logging:

```bash
# Set Node.js logging level
export NODE_DEBUG=http,https

# Run command
human-rent dispatch "Task with logging"
```

### Custom API Endpoint

Use a custom or self-hosted API endpoint:

```bash
export ZHENRENT_BASE_URL="https://custom.api.endpoint.com/v1"
human-rent test
```

## Integration with OpenClaw

### Add to OpenClaw Agent

```javascript
// In your OpenClaw agent
const { exec } = require('child_process');

async function dispatchHuman(instruction, options = {}) {
  const cmd = `human-rent dispatch "${instruction}" ${options.location ? `--location="${options.location}"` : ''}`;
  
  return new Promise((resolve, reject) => {
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        reject(error);
        return;
      }
      
      // Parse task ID from output
      const taskIdMatch = stdout.match(/Task ID: (\S+)/);
      if (taskIdMatch) {
        resolve(taskIdMatch[1]);
      } else {
        reject(new Error('Could not parse task ID'));
      }
    });
  });
}

// Usage
const taskId = await dispatchHuman(
  "Take a photo of 123 Main St",
  { location: "37.7749,-122.4194" }
);

console.log(`Task dispatched: ${taskId}`);
```

### Environment Variables in Docker

If running OpenClaw in Docker:

```dockerfile
# Dockerfile
FROM node:18
ENV ZHENRENT_API_KEY=""
ENV ZHENRENT_API_SECRET=""
```

```bash
# Run container with credentials
docker run -e ZHENRENT_API_KEY="your-key" \
           -e ZHENRENT_API_SECRET="your-secret" \
           your-openclaw-image
```

## Security Best Practices

### Credential Security

1. **Never commit credentials** to version control
   ```bash
   # Add to .gitignore
   echo ".human-rent.env" >> .gitignore
   echo "*.env" >> .gitignore
   ```

2. **Rotate credentials regularly**
   - Generate new API keys every 90 days
   - Revoke old keys after migration

3. **Use separate keys per environment**
   - Development keys
   - Staging keys
   - Production keys

4. **Limit key permissions**
   - Only grant necessary permissions
   - Use read-only keys where possible

### Network Security

1. **Use HTTPS only** (default)
2. **Verify TLS certificates** (automatic)
3. **Use VPN** for sensitive operations
4. **Whitelist IP addresses** (configure in ZhenRent dashboard)

### Audit Logging

Enable audit logging:

```bash
# Log all dispatches
human-rent dispatch "Task" 2>&1 | tee -a ~/human-rent-audit.log
```

## Uninstallation

To remove the skill:

```bash
# Uninstall from ClawHub
clawhub uninstall human-rent

# Remove credentials from shell profile
# Edit ~/.bashrc or ~/.zshrc and remove:
# export ZHENRENT_API_KEY="..."
# export ZHENRENT_API_SECRET="..."

# Remove credential files
rm -f ~/.human-rent.env
rm -f ~/.human-rent-*.env

# Remove audit logs (optional)
rm -f ~/human-rent-audit.log
```

## Getting Help

### Documentation

- README: `/path/to/human-rent/README.md`
- SKILL.md: `/path/to/human-rent/SKILL.md`
- CHANGELOG: `/path/to/human-rent/CHANGELOG.md`

### Command Help

```bash
human-rent help
human-rent dispatch --help
human-rent status --help
human-rent humans --help
```

### Online Resources

- GitHub: https://github.com/ZhenRobotics/openclaw-human-rent
- ClawHub: https://clawhub.ai/zhenstaff/human-rent
- ZhenRent Docs: https://www.zhenrent.com/docs
- API Reference: https://www.zhenrent.com/api/docs

### Support

- GitHub Issues: https://github.com/ZhenRobotics/openclaw-human-rent/issues
- Email: support@zhenrent.com
- Discord: https://discord.gg/zhenrent

## Appendix: Complete Example

Full end-to-end example:

```bash
# 1. Install
clawhub install human-rent

# 2. Configure
export ZHENRENT_API_KEY="zr_key_abc123"
export ZHENRENT_API_SECRET="zr_secret_xyz789"

# 3. Test
human-rent test

# 4. List workers
human-rent humans --location="37.7749,-122.4194"

# 5. Dispatch task
human-rent dispatch "Verify 123 Main St San Francisco exists and take photo" \
  --location="37.7749,-122.4194" \
  --budget="$20"

# Output: Task ID: task_abc123

# 6. Check status
human-rent status task_abc123

# 7. Wait for completion
human-rent status task_abc123 --wait

# 8. View results
# Results displayed in status output
```

Congratulations! You're now ready to use Human-Rent. 🎉
