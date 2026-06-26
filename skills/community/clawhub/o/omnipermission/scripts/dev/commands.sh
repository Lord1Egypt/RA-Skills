pnpm dev --dev onboard

# Stops running gateways. 
pnpm dev --profile dev gateway stop

# Run the gateway. Exit it by Control + C
pnpm dev --dev gateway --verbose 

# Hatch the bot
pnpm dev --dev tui

# Print logs
pnpm dev --dev logs

# List all the installed plugins
pnpm dev --dev plugins list

# Install the plugin
pnpm dev --dev plugins install --link ./extensions/omnipermission

# Run the web dashboard
pnpm dev --dev dashboard

# Add Slack
pnpm dev --dev channels add 

# Enable a plugin
pnpm dev --dev plugins enable slack

# Necessary for enabling hooks
pnpm dev --dev config set plugins.allow "[\"omnipermission\"]"


pnpm dev --dev config set agents.defaults.model "ollama/qwen2.5:1.5b"

pnpm dev --dev models

pnpm dev --dev configure

pnpm dev --dev doctor

pnpm dev --dev omnipermission set-key
pnpm dev --dev omnipermission blacklist-tools
pnpm dev --dev omnipermission clear-blacklist

pnpm dev --dev omnipermission status

pnpm dev --dev omnipermission enable-dev-mode

pnpm dev --dev skills list

pnpm dev --dev status --claws

code /Users/mohammadkarbalee/.openclaw-dev/openclaw.json
