# Publish command example

## Suggested first public release

- slug: `openai-auth-switcher-public`
- name: `OpenAI Auth Switcher Public`
- version: `0.1.0`
- before running the command, set `OPENCLAW_WORKSPACE` to your local OpenClaw workspace path if it is not already set

## Suggested changelog text

```text
首个公开版本：提供环境检测、运行时检查、账号槽位管理、受控切换实验、回滚、本地 token 账本与小时日统计，并补齐公开发布所需兼容性与安全文档。
```

## Example command

```bash
cd "$OPENCLAW_WORKSPACE"
clawhub login
clawhub whoami
clawhub publish ./skills/openai-auth-switcher-public \
  --slug openai-auth-switcher-public \
  --name "OpenAI Auth Switcher Public" \
  --version 0.1.0 \
  --changelog "首个公开版本：提供环境检测、运行时检查、账号槽位管理、受控切换实验、回滚、本地 token 账本与小时日统计，并补齐公开发布所需兼容性与安全文档。"
```

## Conservative alternative

If you prefer to publish the packaged artifact workflow internally first, keep using:

```bash
python3 skills/openai-auth-switcher-public/scripts/package_public_skill.py
```

and inspect the generated `.skill` package before running the final `clawhub publish` command.
