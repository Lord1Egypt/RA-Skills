# 📓 My Diary

<!--
Mini Diary Template
This template shows the structure of a Mini Diary file.
You can customize it to fit your needs.
-->

## How to Use This Diary

1. **Add Notes**: Use `mini-diary add "Your note here"`
2. **Search**: Use `mini-diary search --tag "📦"` or other options
3. **View Stats**: Use `mini-diary search --stats`

## Diary Structure

Each day has:
- Date header: `## 📅 YYYY-MM-DD Day`
- Notes section: `### 📝 Notes`
- Todo section: `### ✅ Todos`

## Auto-Tagging Reference

| Tag | Meaning | Common Keywords |
|-----|---------|-----------------|
| 🏠 | Family | home, family, household, personal |
| 💰 | Finance | invoice, payment, accounting, money |
| 📦 | Order | order, purchase, buy, stock, inventory |
| 🚚 | Shipping | shipping, delivery, logistics, transport |
| 💻 | Tech | software, system, computer, network, tech |
| 🔧 | Support | repair, fix, issue, problem, maintenance |
| 🎋 | Bambu | bambu, 3d print, printer, filament, pla |
| 📋 | Form | form, report, data, spreadsheet, document |
| 📅 | Daily | meeting, work, routine, task, project |

## Tips for Better Tagging

1. **Be specific**: "Ordered Bambu PLA" → 📦🎋
2. **Multiple aspects**: "Fixed printer and submitted invoice" → 🔧💰
3. **Default tag**: Routine tasks get 📅 automatically
4. **Custom tags**: You can extend the tagging system

## NextCloud Sync Tips

If using NextCloud sync:

1. **Set environment variable**:
   ```bash
   export NEXTCLOUD_SYNC_DIR="/path/to/nextcloud/diary"
   ```

2. **Important**: After file changes, run:
   ```bash
   docker exec nextcloud_app php occ files:scan [username]
   ```

3. **Check permissions**:
   ```bash
   ls -la /path/to/nextcloud/diary/
   # Should be owned by www-data
   ```

## Example Entry

```markdown
## 📅 2024-02-23 Friday

### 📝 Notes

- Team meeting about project timeline 📅
- Ordered office supplies 📦
- Fixed email server issue 💻
- Family weekend plans 🏠

### ✅ Todos

- [ ] Submit weekly report
- [x] Order replacement keyboard
- [ ] Schedule dentist appointment
```

---

*Start your diary journey today!*