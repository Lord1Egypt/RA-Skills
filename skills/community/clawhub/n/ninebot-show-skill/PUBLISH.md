# ClawHub 发布

Skill slug：`ninebot-show-skill`

发布目录必须是本目录（根目录直接包含 `SKILL.md`）。

## 1. 登录与检查

```bash
clawhub login
clawhub whoami
```

## 2. Dry run

```bash
clawhub skill publish ./ninebot-show-skill \
  --slug ninebot-show-skill \
  --name "Ninebot Show Skill" \
  --version 3.2.1 \
  --changelog "Cross-agent Agent Skills package; privacy-safe examples; read-only Ninebot reports and smart-service remaining days." \
  --tags latest,ninebot,ebike \
  --dry-run
```

## 3. 正式发布

确认 dry-run 无误后执行：

```bash
clawhub skill publish ./ninebot-show-skill \
  --slug ninebot-show-skill \
  --name "Ninebot Show Skill" \
  --version 3.2.1 \
  --changelog "Cross-agent Agent Skills package; privacy-safe examples; read-only Ninebot reports and smart-service remaining days." \
  --tags latest,ninebot,ebike
```

发布前再次执行 `PRIVACY.md` 中的检查，尤其不要把 `.env`、真实 `config.json`、HAR、Token/Cookie、真实 SN/VIN/MAC、精确私人位置或真实骑行 ID 加入目录。
