# Troubleshooting Guide

Comprehensive guide for diagnosing and resolving issues with mermaid-cli image export.

## Quick Diagnosis

### First Steps
1. **Check installation**: `python scripts/install_mermaid_cli.py --check`
2. **Test simple export**: `echo 'graph TD; A-->B' > test.mmd && python scripts/export_mermaid_image.py test.mmd -o test.png`
3. **Review error messages**: Copy complete error output

### Common Symptoms
- ❌ "Command not found: mmdc"
- ❌ "Chrome not found"
- ❌ "Timeout error"
- ❌ "Memory allocation failed"
- ❌ "Export failed with code 1"

## Installation Issues

### Node.js Problems

#### "node: command not found"
```bash
# Check if Node.js is installed
which node

# Install Node.js
# Ubuntu/Debian:
sudo apt install nodejs npm

# macOS:
brew install node

# Windows: Download from nodejs.org

# Verify installation
node --version  # Should be v14.x or later
```

#### Node.js Version Too Old
```bash
# Check version
node --version

# Update Node.js
# Using nvm (recommended):
nvm install node
nvm use node

# Using package manager:
# Ubuntu: Use nodesource PPA
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs
```

### npm Problems

#### "npm: command not found"
```bash
# npm should come with Node.js
# If missing, reinstall Node.js

# Or install npm separately
# Ubuntu/Debian:
sudo apt install npm

# Verify
npm --version
```

#### npm Permission Errors
```bash
# Fix permission issues
sudo chown -R $USER:$USER ~/.npm
sudo chown -R $USER:$USER ~/.config

# Or use nvm to avoid permission issues
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
```

### mermaid-cli Installation Issues

#### "mmdc: command not found"
```bash
# Check if installed globally
npm list -g | grep mermaid-cli

# Install globally
npm install -g @mermaid-js/mermaid-cli

# Check PATH includes npm global bin
echo $PATH
# Should include: ~/.npm-global/bin or /usr/local/bin

# Add to PATH if needed
export PATH="$PATH:$HOME/.npm-global/bin"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

#### Installation Fails with Network Errors
```bash
# Try with longer timeout
npm install -g @mermaid-js/mermaid-cli --timeout=600000

# Use taobao mirror (China)
npm config set registry https://registry.npmmirror.com
npm install -g @mermaid-js/mermaid-cli

# Or use yarn
npm install -g yarn
yarn global add @mermaid-js/mermaid-cli
```

#### Local vs Global Conflicts
```bash
# If you have both local and global
# Use npx for local
python scripts/export_mermaid_image.py diagram.mmd --mermaid-cmd "npx mmdc" -o diagram.png

# Or specify global explicitly
python scripts/export_mermaid_image.py diagram.mmd --mermaid-cmd "mmdc" -o diagram.png
```

## Chrome/Puppeteer Issues

### "Chrome not found" or "No usable sandbox"

#### Chrome Not Installed
```bash
# Install Chrome/Chromium
# Ubuntu/Debian:
sudo apt install chromium-browser

# Or install Google Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install google-chrome-stable

# macOS:
brew install --cask google-chrome
```

#### Specify Chrome Path
```bash
# Set environment variable
export PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

# Or in command
python scripts/export_mermaid_image.py diagram.mmd --mermaid-cmd "mmdc --puppeteerConfig '{\"executablePath\":\"/usr/bin/google-chrome\"}'" -o diagram.png
```

#### Sandbox Issues (Docker/CI/CD)
```bash
# Disable sandbox
export PUPPETEER_ARGS="--no-sandbox --disable-setuid-sandbox"

# Or in Puppeteer config
cat > puppeteer-config.json << EOF
{
  "args": ["--no-sandbox", "--disable-setuid-sandbox"],
  "headless": "new"
}
EOF

python scripts/export_mermaid_image.py diagram.mmd -f pdf -C puppeteer-config.json -o diagram.pdf
```

### Chrome Version Issues

#### Chrome Too Old
```bash
# Check Chrome version
google-chrome --version  # or chromium-browser --version

# Update Chrome
# Ubuntu/Debian:
sudo apt update
sudo apt upgrade google-chrome-stable

# macOS:
brew upgrade --cask google-chrome
```

#### Chrome/Chromium Mismatch
```bash
# Puppeteer might expect Chrome but find Chromium
# Specify exact path
export PUPPETEER_EXECUTABLE_PATH=$(which google-chrome || which chromium-browser)

# Or install Chrome specifically
```

## Export Errors

### Timeout Errors

#### "Timeout exporting [filename]"
```bash
# Increase timeout
export MMDC_TIMEOUT=120000  # 120 seconds

# Or in Python script (will be added automatically for complex diagrams)
# The script already handles 60-second timeout

# For very complex diagrams, pre-process
# Simplify the Mermaid diagram
# Reduce number of nodes/edges
# Remove complex styling
```

#### Script Hangs Forever
```bash
# Kill hanging processes
pkill -f mmdc
pkill -f chrome

# Try with simpler diagram first
echo 'graph TD; A-->B' > simple.mmd
python scripts/export_mermaid_image.py simple.mmd -o simple.png

# If simple works, the issue is with your diagram
```

### Memory Errors

#### "JavaScript heap out of memory"
```bash
# Increase Node.js memory limit
export NODE_OPTIONS="--max-old-space-size=4096"  # 4GB

# For very large diagrams
export NODE_OPTIONS="--max-old-space-size=8192"  # 8GB

# Reduce diagram complexity
# Split into multiple diagrams
# Export at lower resolution (-s 1.0 instead of -s 2.0)
```

#### Chrome Crash
```bash
# Reduce Chrome memory usage
export PUPPETEER_ARGS="--disable-gpu --disable-software-rasterizer"

# Run with minimal Chrome
export PUPPETEER_ARGS="--single-process --no-zygote --no-sandbox"

# Check system memory
free -h
# If low, close other applications
```

### Format-Specific Errors

#### PNG Export Issues
```bash
# Corrupted PNG files
# Reinstall mermaid-cli
npm uninstall -g @mermaid-js/mermaid-cli
npm cache clean --force
npm install -g @mermaid-js/mermaid-cli

# Test with basic diagram
echo 'graph TD; A-->B' > test.mmd
mmdc -i test.mmd -o test.png
file test.png  # Should show "PNG image data"
```

#### SVG Export Issues
```bash
# Invalid SVG
# Check SVG syntax
xmllint --noout diagram.svg

# SVG too large
# Simplify diagram
# Remove unnecessary elements
# Use CSS instead of inline styles
```

#### PDF Export Issues
```bash
# PDF generation fails
# Ensure Chrome is installed
# Increase timeout for PDF
export MMDC_TIMEOUT=180000  # 3 minutes for PDF

# Try smaller page size
python scripts/export_mermaid_image.py diagram.mmd -f pdf -w 200 -H 200 -o test.pdf
```

## Performance Issues

### Slow Export

#### General Slowness
```bash
# Check system resources
top  # or htop

# Close other applications
# Increase system memory if possible

# Export in batch but sequentially
for file in *.mmd; do
  python scripts/export_mermaid_image.py "$file" -o "${file%.mmd}.png" -q
done
```

#### Complex Diagrams Very Slow
```bash
# Export at lower quality first
python scripts/export_mermaid_image.py complex.mmd -s 1.0 -o preview.png

# Only export final at high quality
python scripts/export_mermaid_image.py complex.mmd -s 2.0 -o final.png

# Consider splitting diagram
```

### High CPU/Memory Usage

#### During Export
```bash
# Monitor with
htop  # or top

# Limit concurrent exports
# Export one at a time
python scripts/export_mermaid_image.py diagram1.mmd -o diagram1.png
python scripts/export_mermaid_image.py diagram2.mmd -o diagram2.png
# Not in parallel
```

#### Chrome Using Too Much Memory
```bash
# Limit Chrome tabs/processes
export PUPPETEER_ARGS="--single-process"

# Or kill Chrome after each export
pkill -f chrome  # After export completes
```

## Quality Issues

### Blurry or Pixelated Images

#### Low Resolution
```bash
# Increase scale
python scripts/export_mermaid_image.py diagram.mmd -s 2.0 -o highres.png

# Or specify exact dimensions
python scripts/export_mermaid_image.py diagram.mmd -w 1600 -o wide.png
```

#### Anti-aliasing Issues
```bash
# SVG doesn't have this issue
python scripts/export_mermaid_image.py diagram.mmd -f svg -o diagram.svg

# For PNG, ensure Chrome anti-aliasing is on
# Update Chrome to latest version
```

### Color Issues

#### Colors Look Different
```bash
# Check theme
python scripts/export_mermaid_image.py diagram.mmd -t default -o test_default.png
python scripts/export_mermaid_image.py diagram.mmd -t dark -o test_dark.png

# Use custom CSS for exact colors
cat > custom.css << EOF
:root {
  --mermaid-edge-color: #ff0000;
  --mermaid-node-bg: #00ff00;
}
EOF
python scripts/export_mermaid_image.py diagram.mmd -c custom.css -o custom.png
```

#### Transparency Issues
```bash
# Ensure background is transparent
python scripts/export_mermaid_image.py diagram.mmd -b transparent -o transparent.png

# Some formats (PDF) don't support transparency well
# Use PNG with transparency, convert to PDF with white background if needed
```

## Script-Specific Issues

### Python Script Errors

#### Import Errors
```bash
# Ensure Python 3 is installed
python3 --version

# The script has no external dependencies
# Should work with Python 3.6+

# If subprocess fails, check Python installation
python3 -c "import subprocess; print('OK')"
```

#### Permission Errors
```bash
# Make scripts executable
chmod +x scripts/*.py scripts/*.sh

# Run with appropriate permissions
# Not as root unless necessary
```

#### Argument Parsing Errors
```bash
# Check argument syntax
python scripts/export_mermaid_image.py --help

# Common mistake: wrong order
# Correct: python scripts/export_mermaid_image.py input.mmd -o output.png
# Wrong: python scripts/export_mermaid_image.py -o output.png input.mmd
```

### Shell Script Errors

#### "Permission denied"
```bash
chmod +x scripts/batch_export.sh
./scripts/batch_export.sh --help
```

#### "Syntax error"
```bash
# Check shell compatibility
# Script uses bash, not sh
bash scripts/batch_export.sh --help

# Or make executable and run directly
chmod +x scripts/batch_export.sh
./scripts/batch_export.sh *.mmd
```

#### "Unexpected end of file"
```bash
# Check line endings (especially on Windows)
dos2unix scripts/batch_export.sh

# Or convert manually
sed -i 's/\r$//' scripts/batch_export.sh
```

## Network and Proxy Issues

### Behind Corporate Proxy

#### npm Installation Fails
```bash
# Configure npm proxy
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080

# Install with proxy
npm install -g @mermaid-js/mermaid-cli --proxy http://proxy.company.com:8080
```

#### Chrome Blocked by Proxy
```bash
# Configure Chrome proxy via Puppeteer
cat > proxy-config.json << EOF
{
  "args": [
    "--proxy-server=http://proxy.company.com:8080",
    "--no-sandbox"
  ]
}
EOF

python scripts/export_mermaid_image.py diagram.mmd -C proxy-config.json -o diagram.png
```

### Offline Environment

#### Install Without Internet
```bash
# On online machine:
npm pack @mermaid-js/mermaid-cli
# Copy the .tgz file to offline machine

# On offline machine:
npm install -g ./mermaid-js-mermaid-cli-*.tgz

# Install Chrome offline
# Download Chrome .deb/.rpm/.dmg and copy
```

## Platform-Specific Issues

### Linux Issues

#### Missing Libraries
```bash
# Common missing libraries
# Ubuntu/Debian:
sudo apt install libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libgbm1 libasound2

# CentOS/RHEL:
sudo yum install libXScrnSaver GConf2 alsa-lib atk at-spi2-atk

# Check Chrome dependencies
ldd $(which google-chrome) | grep "not found"
```

#### AppArmor/SELinux
```bash
# If blocked by security policies
# Check logs: sudo dmesg | grep -i chrome
# Or: sudo ausearch -m avc | grep chrome

# Temporary disable (not recommended for production)
sudo setenforce 0  # SELinux
# Or adjust AppArmor profile
```

### macOS Issues

#### Gatekeeper Blocking
```bash
# If Chrome is blocked
xattr -d com.apple.quarantine /Applications/Google\ Chrome.app

# Or allow from System Preferences → Security & Privacy
```

#### Homebrew Issues
```bash
# Update Homebrew
brew update
brew upgrade

# Reinstall Chrome
brew reinstall --cask google-chrome

# Check Node.js installation
brew reinstall node
```

### Windows Issues

#### Path Issues
```bash
# Ensure Node.js and Chrome are in PATH
echo %PATH%

# Add to PATH if needed
setx PATH "%PATH%;C:\Program Files\nodejs"
setx PATH "%PATH%;C:\Program Files\Google\Chrome\Application"

# Restart terminal after changing PATH
```

#### File Permission Issues
```bash
# Run as administrator if needed
# But be careful with npm install -g as admin

# Better: Install Node.js for current user only
# Or use nvm-windows
```

#### WSL (Windows Subsystem for Linux)
```bash
# Chrome in WSL needs Windows Chrome
export PUPPETEER_EXECUTABLE_PATH="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

# May need to disable sandbox
export PUPPETEER_ARGS="--no-sandbox"
```

## Debugging Techniques

### Enable Verbose Logging
```bash
# Python script
python scripts/export_mermaid_image.py diagram.mmd -o diagram.png  # Already shows progress

# Shell script
./scripts/batch_export.sh -v *.mmd

# Direct mmdc with debug
mmdc -i diagram.mmd -o diagram.png --verbose
```

### Check Logs
```bash
# System logs
sudo dmesg | tail -20

# Chrome logs (if Chrome crashes)
ls -la ~/.config/google-chrome/Crash\ Reports/

# Node.js/npm logs
npm config get loglevel
npm install -g @mermaid-js/mermaid-cli --loglevel verbose
```

### Test with Minimal Example
```bash
# Create simplest possible diagram
cat > minimal.mmd << 'EOF'
graph TD
    A-->B
EOF

# Test export
python scripts/export_mermaid_image.py minimal.mmd -o minimal.png

# If this works, issue is with your diagram
# If this fails, issue is with installation
```

### Compare Environments
```bash
# Check what's different between working and non-working
node --version
npm --version
mmdc --version
google-chrome --version

# Export same diagram on both
# Compare outputs
```

## Getting Help

### Collect Debug Information
```bash
# Run diagnostics
python scripts/install_mermaid_cli.py --check > debug.txt
echo "=== System ===" >> debug.txt
uname -a >> debug.txt
echo "=== Python ===" >> debug.txt
python3 --version >> debug.txt
echo "=== Test Export ===" >> debug.txt
echo 'graph TD; A-->B' > debug.mmd
python scripts/export_mermaid_image.py debug.mmd -o debug.png 2>&1 >> debug.txt

# Share debug.txt when asking for help
```

### Where to Get Help
1. **This skill's documentation**: Check relevant sections
2. **mermaid-cli GitHub Issues**: https://github.com/mermaid-js/mermaid-cli/issues
3. **Stack Overflow**: Tag with `mermaid` and `mermaid-cli`
4. **Community forums**: Mermaid.js Discord or discussion boards

### What to Include When Asking for Help
- Complete error message
- Debug information (from above)
- Operating system and versions
- Steps to reproduce
- What you've tried already

## Prevention Best Practices

### Regular Maintenance
```bash
# Keep software updated
npm update -g @mermaid-js/mermaid-cli
# Update Chrome regularly
# Update Node.js periodically

# Clean cache
npm cache clean --force
```

### Environment Management
```bash
# Use nvm for Node.js management
nvm install --lts
nvm use --lts

# Use virtual environments for Python
python3 -m venv venv
source venv/bin/activate
```

### Backup Configurations
```bash
# Backup your mermaid-cli config
cp ~/.config/mermaid-cli/config.json ~/backup/

# Version control your diagrams and configs
git add diagrams/ config/
```

### Testing Pipeline
```bash
# Regular test exports
python scripts/export_mermaid_image.py test_diagram.mmd -o test_output.png
# Verify file exists and is valid
file test_output.png
```

---

**Remember**: Most issues can be resolved by:
1. Checking installation with `python scripts/install_mermaid_cli.py --check`
2. Testing with a simple diagram
3. Reviewing error messages carefully
4. Ensuring Chrome is properly installed

If you've tried all troubleshooting steps and still have issues, collect the debug information and seek help from the community.