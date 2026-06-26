# 高级配置

## 手动安装（不用 `install.sh`）

```bash
cd /path/to/openclaw-rpa
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip && pip install -r requirements.txt
python -m playwright install chromium
```

---

## 网关实际调用的 Python

`rpa_manager.py` 使用 `sys.executable`，该解释器必须已装 **Playwright**。若网关用系统 `python3`，请在同一环境装依赖，或把工具指向：

```
~/.openclaw/workspace/skills/openclaw-rpa/.venv/bin/python
```

---

## 语言与 `config.json`

- `SKILL.md` 中 `localeConfig` 指向 `config.json`
- 若无 `config.json`，可按 `SKILL.md` 用 `config.example.json` 读 `locale`
- 详见 `LOCALE.md`

---

## `SKILL.*.md` 里的路径

示例中的 `~/.openclaw/workspace/skills/openclaw-rpa/` 若与你的本机不一致，请改成实际技能目录。

---

## 对外发布技能

**[ClawHub — 发布 skill](https://clawhub.ai/publish-skill)**（绑定本 GitHub 仓库）。

---

## 环境自检

```bash
python3 envcheck.py
# 或
python3 rpa_manager.py env-check
```

`record-start` / `run` 在可能时会自动安装 Chromium。
