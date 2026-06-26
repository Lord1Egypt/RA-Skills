# NexLink - Verification Notes

**Last refreshed:** 2026-04-13
**Version:** 0.4.0

---

## Ce este verificat aici

Acest document a fost aliniat la suprafața CLI curentă a repo-ului și la documentația principală.

În mod explicit, această actualizare confirmă:
- comanda principală `nexlink`
- modulele disponibile: `mail`, `cal`, `calendar`, `tasks`, `analytics`, `sync`, `files`
- subcomenzile expuse de help-ul curent
- faptul că task-urile folosesc `trash`, nu `delete`

Pentru verificare funcțională live împotriva Exchange / Nextcloud, rulează checklist-ul de smoke test de mai jos.

---

## ✅ Command Reference (current CLI surface)

### Mail Commands

```bash
nexlink mail connect
nexlink mail read --limit 10
nexlink mail read --unread
nexlink mail get --id ID
nexlink mail send --to EMAIL --subject SUBJECT --body BODY
nexlink mail draft --to EMAIL --subject SUBJECT --body BODY
nexlink mail reply --id ID --body BODY
nexlink mail forward --id ID --to EMAIL
nexlink mail mark --id ID --read
nexlink mail mark --id ID --unread
nexlink mail mark-all-read
nexlink mail list-attachments --id ID
nexlink mail download-attachment --id ID --name FILE --output DIR
```

### Calendar Commands

```bash
nexlink cal connect
nexlink cal list --days 7
nexlink cal today
nexlink cal week
nexlink cal get --id ID
nexlink cal create --subject SUBJECT --start DATETIME [--duration MIN]
nexlink cal update --id ID
nexlink cal delete --id ID
nexlink cal respond --id ID
nexlink cal availability
```

Aliasul `calendar` este de asemenea acceptat de entrypoint-ul unificat.

### Tasks Commands

```bash
nexlink tasks connect
nexlink tasks list
nexlink tasks list --overdue
nexlink tasks list --status STATUS
nexlink tasks get --id ID
nexlink tasks create --subject SUBJECT [--due DATE] [--priority LEVEL]
nexlink tasks assign --to EMAIL --subject SUBJECT [--body BODY] [--due DATE]
nexlink tasks update --id ID
nexlink tasks complete --id ID
nexlink tasks trash --id ID
```

### Analytics Commands

```bash
nexlink analytics stats --days N
nexlink analytics response-time
nexlink analytics top-senders
nexlink analytics heatmap
nexlink analytics folders
nexlink analytics report
```

### Sync Commands

```bash
nexlink sync sync
nexlink sync reminders [--hours N] [--dry-run]
nexlink sync link-calendar --id TASK_ID [--time HH:MM] [--duration MIN]
nexlink sync status
```

### Files Commands (Nextcloud)

```bash
nexlink files list [PATH] [--recursive]
nexlink files search QUERY [PATH]
nexlink files extract-text PATH
nexlink files summarize PATH
nexlink files ask-file PATH QUESTION
nexlink files extract-actions PATH
nexlink files create-tasks-from-file PATH [--mailbox EMAIL] [--priority LEVEL] [--select 1,2] [--execute]
nexlink files upload LOCAL REMOTE
nexlink files download REMOTE LOCAL
nexlink files mkdir PATH
nexlink files delete PATH
nexlink files move OLD NEW
nexlink files copy SRC DEST
nexlink files info PATH
nexlink files shared
nexlink files share-create PATH [--password VALUE] [--expire-date YYYY-MM-DD] [--public-upload]
nexlink files share-list [PATH]
nexlink files share-revoke SHARE_ID
```

---

## 🔎 Accuracy Notes

### Task deletion semantics

Pentru Exchange tasks, comanda documentată corect este:

```bash
nexlink tasks trash --id TASK_ID
```

Asta mută task-ul în **Deleted Items** și este varianta sigură / recuperabilă.

### File-to-task workflow semantics

`create-tasks-from-file` este documentată ca workflow **preview-first**:
- fără `--execute` → vezi propunerile
- cu `--select ... --execute` → creezi efectiv task-urile selectate

### Mail commands

Comanda `draft-reply` **nu** este în suprafața CLI curentă. Documentația trebuie să folosească doar comenzile expuse mai sus.

---

## 🧪 Smoke Test Checklist

Rulează înainte de release sau demo live:

```bash
# Exchange
nexlink mail connect
nexlink mail read --limit 5
nexlink cal today
nexlink tasks list
nexlink analytics stats --days 7
nexlink sync status

# Nextcloud
nexlink files list /
nexlink files search contract /Clients/
nexlink files extract-text /Clients/contract.docx
nexlink files summarize /Clients/contract.docx
nexlink files ask-file /Clients/contract.docx "When is the renewal due?"
nexlink files extract-actions /Clients/contract.txt
nexlink files create-tasks-from-file /Clients/contract.txt
nexlink files share-list
nexlink files shared
```

---

## 📝 Known Documentation Decisions

- top-level docs optimizează pentru CLI-ul unificat `nexlink ...`
- documentația de setup evită exemplele vechi de tip `python3 -m modules.exchange ...`
- pentru task-uri, limbajul preferat este **trash / move to Deleted Items**, nu delete dur

---

## 📚 Related Docs

- `README.md` — overview și quickstart
- `SKILL.md` — descrierea skill-ului pentru OpenClaw
- `references/setup.md` — instalare și configurare
- `CHANGELOG.md` — istoric versiuni
