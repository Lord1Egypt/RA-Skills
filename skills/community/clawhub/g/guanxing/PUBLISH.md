# How to Publish to ClawHub

Run these commands on your Mac Studio (where OpenClaw is installed):

## 1. Install ClawHub CLI (if not already)
```bash
npm install -g clawhub@latest
```

## 2. Login to ClawHub
```bash
clawhub login
```
This opens your browser for GitHub OAuth. Authorize, then come back to terminal.

## 3. Clone and publish
```bash
git clone https://github.com/doggychip/guanxing-skill.git /tmp/guanxing-skill
clawhub publish /tmp/guanxing-skill --slug guanxing --name "GuanXing 观星" --version 1.0.0 --changelog "Initial release: 11 Chinese metaphysics AI actions"
```

## 4. Verify
```bash
clawhub search "guanxing"
```

## After Publishing
Users can install with:
```bash
clawhub install guanxing
```

And immediately use it in any OpenClaw chat:
- "帮我算八字"
- "BTC运势怎么样"
- "帮我求签"
