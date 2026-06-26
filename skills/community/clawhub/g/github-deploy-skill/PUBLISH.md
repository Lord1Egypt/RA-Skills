# Manual publish steps (ClawHub)

Run in PowerShell:

```powershell
clawhub whoami
clawhub publish E:\repository\skills\github-deploy-skill --slug github-deploy-skill --name "GitHub Deploy Skill" --version 1.0.0 --tags latest --changelog "Initial release"
```

If not logged in:

```powershell
clawhub login
```

If browser login fails, use token login:

```powershell
clawhub login --token <YOUR_TOKEN> --no-browser
```

Validate after publish:

```powershell
clawhub inspect github-deploy-skill
```
