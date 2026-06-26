# Installation Guide

Complete installation guide for mermaid-cli and required dependencies.

## Prerequisites

### 1. Operating System Requirements
- **Linux**: Most distributions (Ubuntu, Debian, CentOS, etc.)
- **macOS**: 10.10 or later
- **Windows**: 7 or later (requires additional setup)

### 2. System Requirements
- **CPU**: Modern processor (dual-core minimum)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 1GB free space for Node.js and dependencies
- **Network**: Internet access for package downloads

## Step-by-Step Installation

### Step 1: Install Node.js

#### macOS (Homebrew)
```bash
brew install node
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install nodejs npm
```

#### Windows
1. Download installer from [nodejs.org](https://nodejs.org/)
2. Run the installer (includes npm)
3. Restart terminal/powershell

#### Verify Installation
```bash
node --version  # Should show v14.x or later
npm --version   # Should show 6.x or later
```

### Step 2: Install mermaid-cli

#### Global Installation (Recommended)
```bash
npm install -g @mermaid-js/mermaid-cli
```

#### Local Installation (Project-specific)
```bash
# Navigate to your project directory
cd /path/to/your/project

# Install locally
npm install @mermaid-js/mermaid-cli

# Use with npx
npx mmdc --version
```

#### Verify mermaid-cli
```bash
mmdc --version  # Should show version number
# Or with npx
npx mmdc --version
```

### Step 3: Install Chrome/Chromium

mermaid-cli uses Puppeteer which requires Chrome/Chromium.

#### Linux
```bash
# Ubuntu/Debian
sudo apt install chromium-browser

# Or install Google Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable
```

#### macOS
```bash
# Install via Homebrew
brew install --cask google-chrome

# Or download from google.com/chrome
```

#### Windows
Download from [google.com/chrome](https://www.google.com/chrome/)

#### Verify Chrome Installation
```bash
# Check if Chrome is available
which google-chrome || which chromium-browser
```

## Installation Check Script

Use the provided script to verify everything is installed correctly:

```bash
# Basic check
python scripts/install_mermaid_cli.py --check

# Interactive installation
python scripts/install_mermaid_cli.py --install

# Show installation guide
python scripts/install_mermaid_cli.py --guide
```

### Expected Output
```
Mermaid-CLI Installation Status
==================================================
Node.js              ✅ Node.js v18.12.0
npm                  ✅ npm 8.19.2
mermaid-cli          ✅ mermaid-cli (global)
Chrome/Chromium      ✅ Chrome/Chromium found

✅ All dependencies are installed and ready!
```

## Troubleshooting Installation

### Common Issues

#### 1. "mmdc: command not found"
```bash
# If installed globally but not found
echo $PATH  # Check if npm global bin is in PATH

# Add npm global bin to PATH (Linux/macOS)
export PATH="$PATH:$HOME/.npm-global/bin"

# Or reinstall
npm install -g @mermaid-js/mermaid-cli
```

#### 2. "Error: Cannot find module '@mermaid-js/mermaid-cli'"
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
npm install -g @mermaid-js/mermaid-cli
```

#### 3. Puppeteer Chrome Issues
```bash
# If Chrome not found, install it
# Or set PUPPETEER_EXECUTABLE_PATH
export PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Test with explicit path
mmdc -i test.mmd -o test.png --puppeteerConfig '{"executablePath":"/usr/bin/chromium"}'
```

#### 4. Permission Errors
```bash
# Fix npm permissions (Linux/macOS)
sudo chown -R $USER:$USER ~/.npm
sudo chown -R $USER:$USER ~/.config

# Or use node version manager
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
```

## Alternative Installation Methods

### Docker Installation
```bash
# Run mermaid-cli in Docker
docker run -it --rm -v $(pwd):/data minlag/mermaid-cli -i /data/diagram.mmd -o /data/diagram.png
```

### GitHub Codespaces / Cloud IDEs
Most cloud development environments already include Node.js. Just install mermaid-cli:
```bash
npm install -g @mermaid-js/mermaid-cli
```

### CI/CD Environments

#### GitHub Actions
```yaml
- name: Setup Node.js
  uses: actions/setup-node@v3
  with:
    node-version: '18'
    
- name: Install mermaid-cli
  run: npm install -g @mermaid-js/mermaid-cli
```

#### GitLab CI
```yaml
image: node:18-alpine

before_script:
  - npm install -g @mermaid-js/mermaid-cli
```

## Post-Installation Verification

### Test Export
Create a simple test diagram:
```bash
cat > test.mmd << 'EOF'
graph TD
    A[Start] --> B[Process]
    B --> C[End]
EOF

# Export to PNG
mmdc -i test.mmd -o test.png

# Check the output
file test.png  # Should show: PNG image data
ls -la test.png  # Should have non-zero size
```

### Test with Python Script
```bash
# Use the provided Python script
python scripts/export_mermaid_image.py test.mmd -o test2.png

# Batch test
python scripts/export_mermaid_image.py test.mmd -f svg -o test.svg
python scripts/export_mermaid_image.py test.mmd -f pdf -o test.pdf
```

## Performance Tuning

### Increase Timeout (for complex diagrams)
```bash
# Set environment variable
export MMDC_TIMEOUT=30000  # 30 seconds

# Or use in command
mmdc -i complex.mmd -o complex.png --timeout 30000
```

### Memory Limits
```bash
# Increase Node.js memory
export NODE_OPTIONS="--max-old-space-size=4096"
```

### Disable Sandbox (if running as root)
```bash
# For Docker or CI environments
export PUPPETEER_ARGS="--no-sandbox --disable-setuid-sandbox"
```

## Uninstallation

### Remove mermaid-cli
```bash
npm uninstall -g @mermaid-js/mermaid-cli

# Remove global package
npm list -g --depth=0  # List global packages
```

### Remove Node.js
#### macOS (Homebrew)
```bash
brew uninstall node
```

#### Ubuntu/Debian
```bash
sudo apt remove nodejs npm
sudo apt autoremove
```

#### Windows
Use "Add or Remove Programs" in Control Panel

## Support and Resources

### Official Documentation
- [mermaid-cli GitHub](https://github.com/mermaid-js/mermaid-cli)
- [Mermaid.js Documentation](https://mermaid.js.org/)
- [Puppeteer Documentation](https://pptr.dev/)

### Community Support
- [Stack Overflow](https://stackoverflow.com/questions/tagged/mermaid)
- [GitHub Issues](https://github.com/mermaid-js/mermaid-cli/issues)
- [Discord Community](https://discord.gg/AgrbSrBer3)

### Skill-Specific Help
Use the troubleshooting guide in this skill package for common issues and solutions.

---

**Next Steps**: After successful installation, proceed to the Usage Guide to learn how to export diagrams effectively.