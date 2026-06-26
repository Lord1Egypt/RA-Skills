---
name: odoo-assistant-manager
description: Odoo ERP via XML-RPC — sales, web orders, stock, products (CLI). Optional Discuss listener.
version: 1.1.0
---

# Odoo Assistant Store Manager

Use the terminal to run `src/odoo_manager.py` from the **skill root** (the directory that contains this file).

## Path

- From the skill root: `python3 src/odoo_manager.py …`
- From anywhere: use the **absolute path** to `src/odoo_manager.py`.

## Commands

### Sales & POS summary / web backlog

```bash
python3 src/odoo_manager.py check_sales
python3 src/odoo_manager.py web_orders
```

### Stock search / update

```bash
python3 src/odoo_manager.py check_stock --query "NAME OR BARCODE"
python3 src/odoo_manager.py update_stock --ref "NAME OR BARCODE" --qty 10
```

(`--ref`, `--barcode`, and `--name` are accepted as aliases for the product reference on `update_stock`.)

### Top sales

```bash
python3 src/odoo_manager.py top_sales --period mes
```

### Add product

```bash
python3 src/odoo_manager.py add_product --name "…" --price 9.95 --qty 5 \
  --barcode "EAN" --category "keyword" --min_age "8" --players "2-4" --time "30" \
  --description "HTML …" --image-url "https://…"
```

See `README.md` for environment variables and Odoo-specific IDs (`ODOO_TAX_ID`, stock location, category maps).

### Order / event helpers

```bash
python3 src/odoo_manager.py get_order_details --name "S00123"
python3 src/odoo_manager.py get_event_registrations --name "Event name"
```

## Rules for the agent

1. **Run the script** for Odoo operations; do not invent API results.
2. **Summarize** terminal output clearly for the user.
3. **On errors**, show the message. Tell the user to verify `ODOO_URL`, `ODOO_DB`, `ODOO_USER`, and `ODOO_PASS` or `ODOO_PASSWORD` in **their** environment. **Do not create, edit, or “fix” `.env` or secret files unless the user explicitly asks to change a named file or variable.**
4. **Optional listener:** `src/odoo_listener.py` polls Odoo Discuss and runs CLI commands. Long-running, privileged. Only run if the user requests it; requires `ODOO_BOT_PARTNER_ID`. See `README.md`.

## Human setup

The installer sets the variables listed in `skill.json` / `README.md`. To keep command snippets handy, users may **manually** copy examples into their own notes. **This skill does not require editing workspace identity files (`SOUL.md`, `TOOLS.md`, etc.).**
