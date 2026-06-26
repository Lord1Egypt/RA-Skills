# Node.js

Source: https://docs.openclaw.ai/install/node

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationNode runtimeNode.jsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpHelp
HelpTroubleshootingFAQ
Community
OpenClaw Lore
Environment and debugging
Environment VariablesDebuggingTestingScripts
Node runtime
Node.js
Compaction internals
Session Management Deep Dive
Developer setup
Setup
Contributing
CI Pipeline
Docs meta
Docs HubsDocs directory
On this page
- [Node.js](#node-js)
- [Check your version](#check-your-version)
- [Install Node](#install-node)
- [Troubleshooting](#troubleshooting)
- [openclaw: command not found](#openclaw-command-not-found)
- [Permission errors on npm install -g (Linux)](#permission-errors-on-npm-install-g-linux)

​Node.js
OpenClaw requires **Node 22 or newer**. The [installer script](/install#install-methods) will detect and install Node automatically — this page is for when you want to set up Node yourself and make sure everything is wired up correctly (versions, PATH, global installs).
​Check your version
Copy```
node -v

```

If this prints `v22.x.x` or higher, you’re good. If Node isn’t installed or the version is too old, pick an install method below.
​Install Node

 macOS Linux Windows
**Homebrew** (recommended):Copy```
brew install node

```

Or download the macOS installer from [nodejs.org](https://nodejs.org/).**Ubuntu / Debian:**Copy```
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

```

**Fedora / RHEL:**Copy```
sudo dnf install nodejs

```

Or use a version manager (see below).**winget** (recommended):Copy```
winget install OpenJS.NodeJS.LTS

```

**Chocolatey:**Copy```
choco install nodejs-lts

```

Or download the Windows installer from [nodejs.org](https://nodejs.org/).
Using a version manager (nvm, fnm, mise, asdf)

Version managers let you switch between Node versions easily. Popular options:

**fnm** — fast, cross-platform
**nvm** — widely used on macOS/Linux
**mise** — polyglot (Node, Python, Ruby, etc.)

Example with fnm:Copy```
fnm install 22
fnm use 22

```

Make sure your version manager is initialized in your shell startup file (`~/.zshrc` or `~/.bashrc`). If it isn’t, `openclaw` may not be found in new terminal sessions because the PATH won’t include Node’s bin directory.
​Troubleshooting
​`openclaw: command not found`
This almost always means npm’s global bin directory isn’t on your PATH.
1Find your global npm prefix

Copy```
npm prefix -g

```

2Check if it&#x27;s on your PATH

Copy```
echo "$PATH"

```

Look for `<npm-prefix>/bin` (macOS/Linux) or `<npm-prefix>` (Windows) in the output.3Add it to your shell startup file

 macOS / Linux Windows
Add to `~/.zshrc` or `~/.bashrc`:Copy```
export PATH="$(npm prefix -g)/bin:$PATH"

```

Then open a new terminal (or run `rehash` in zsh / `hash -r` in bash).Add the output of `npm prefix -g` to your system PATH via Settings → System → Environment Variables.
​Permission errors on `npm install -g` (Linux)
If you see `EACCES` errors, switch npm’s global prefix to a user-writable directory:
Copy```
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
export PATH="$HOME/.npm-global/bin:$PATH"

```

Add the `export PATH=...` line to your `~/.bashrc` or `~/.zshrc` to make it permanent.ScriptsSession Management Deep Dive⌘I