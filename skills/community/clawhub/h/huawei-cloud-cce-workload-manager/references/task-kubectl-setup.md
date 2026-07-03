# Task: kubectl Setup

## Installation

### Linux

#### Option 1: curl (Recommended)

```bash
# Detect latest stable version
curl -L -s https://dl.k8s.io/release/stable.txt

# Detect CPU architecture (amd64 for x86_64, arm64 for aarch64)
ARCH=$(uname -m | sed 's/x86_64/amd64/' | sed 's/aarch64/arm64/')

# Download kubectl binary for detected architecture
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/${ARCH}/kubectl"

# Verify binary matches your architecture
file kubectl

# Install
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify
kubectl version --client
```

#### Option 2: apt (Debian/Ubuntu)

```bash
# Update package index and install dependencies
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

# Add Kubernetes apt repository
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /usr/share/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/usr/share/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Install kubectl
sudo apt-get update
sudo apt-get install -y kubectl
```

#### Option 3: yum (RHEL/CentOS/Fedora)

```bash
# Add Kubernetes yum repository
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/repodata/repomd.xml.key
EOF

# Install kubectl
sudo yum install -y kubectl
```

### macOS

#### Option 1: curl (Recommended)

```bash
# Detect CPU architecture (amd64 for Intel, arm64 for Apple Silicon)
ARCH=$(uname -m | sed 's/x86_64/amd64/' | sed 's/aarch64/arm64/')

# Download kubectl binary for detected architecture
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/${ARCH}/kubectl"

# Install
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
sudo chown root: /usr/local/bin/kubectl

# Verify
kubectl version --client
```

#### Option 2: Homebrew

```bash
# Install via Homebrew
brew install kubectl

# Verify
kubectl version --client
```

### Windows

#### Option 1: curl (Recommended)

```powershell
# Download kubectl binary
curl -LO "https://dl.k8s.io/release/stable.txt"
$version = (Get-Content stable.txt).Trim()

# Detect CPU architecture (amd64 for x86_64, arm64 for ARM64)
$arch = if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { 'arm64' } else { 'amd64' }
curl -LO "https://dl.k8s.io/release/$version/bin/windows/$arch/kubectl.exe"

# Add to PATH (move to a directory in your PATH or add the directory to PATH)
Move-Item kubectl.exe C:\Windows\

# Verify
kubectl version --client
```

#### Option 2: Chocolatey

```powershell
# Install via Chocolatey
choco install kubernetes-cli

# Verify
kubectl version --client
```

## Verification

After installation, verify kubectl is working:

```bash
# Check kubectl version
kubectl version --client

# Expected output format:
# Client Version: v1.XX.Y
# Kustomize Version: vX.Y.Z
```

If the version command succeeds, kubectl is properly installed.

## Kubeconfig Configuration

### Default Kubeconfig Location

kubectl looks for kubeconfig in the following order:
1. `--kubeconfig` flag (explicit path)
2. `KUBECONFIG` environment variable
3. `~/.kube/config` (default location)

### Option 1: --kubeconfig Flag (Recommended for CCE/UCS)

```bash
# Explicit kubeconfig path per command
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get nodes
kubectl --kubeconfig=~/.kube/ucs-kubeconfig.yaml get pods -n production
```

**Advantages**: Most explicit, least risk of operating on wrong cluster.

### Option 2: KUBECONFIG Environment Variable

```bash
# Set environment variable
export KUBECONFIG=~/.kube/cce-kubeconfig.yaml

# All subsequent kubectl commands use this kubeconfig
kubectl get nodes
kubectl get pods -n production

# Switch to another kubeconfig
export KUBECONFIG=~/.kube/ucs-kubeconfig.yaml
kubectl get nodes
```

### Option 3: Default ~/.kube/config

```bash
# Copy kubeconfig to default location
cp cce-kubeconfig.yaml ~/.kube/config

# kubectl uses default config
kubectl get nodes
```

**Caution**: Using `~/.kube/config` as default can lead to accidental operations on the wrong cluster if you switch clusters frequently. Prefer `--kubeconfig` flag or `KUBECONFIG` environment variable.

### Prepare ~/.kube Directory

```bash
# Create ~/.kube directory if it doesn't exist
mkdir -p ~/.kube

# Set appropriate permissions
chmod 700 ~/.kube
```

## Context Operations

When working with a merged or multi-context kubeconfig:

```bash
# List all available contexts
kubectl config get-contexts

# Switch to a specific context
kubectl config use-context <context-name>

# Show current active context
kubectl config current-context

# Delete a context
kubectl config delete-context <context-name>

# Rename a context
kubectl config rename-context <old-name> <new-name>
```

## Shell Completion

### Bash

```bash
# Install bash-completion if not installed
sudo apt-get install bash-completion -y  # Debian/Ubuntu
sudo yum install bash-completion -y       # RHEL/CentOS

# Enable kubectl completion
echo 'source <(kubectl completion bash)' >>~/.bashrc

# Reload shell
source ~/.bashrc
```

### Zsh

```bash
# Enable kubectl completion for zsh
echo 'source <(kubectl completion zsh)' >>~/.zshrc

# If completion doesn't work, add this as well
echo 'autoload -Uz compinit && compinit' >>~/.zshrc

# Reload shell
source ~/.zshrc
```

### PowerShell (Windows)

```powershell
# Generate completion script
kubectl completion powershell | Out-File -Encoding utf8 -FilePath $HOME\kubectl-completion.ps1

# Add to PowerShell profile
Add-Content -Path $PROFILE -Value ". $HOME\kubectl-completion.ps1"
```

## Reference

- Official kubectl installation guide: https://kubernetes.io/docs/tasks/tools/
- Stable version detection URL: `https://dl.k8s.io/release/stable.txt`
- Binary download URL pattern: `https://dl.k8s.io/release/<version>/bin/<os>/<arch>/kubectl`