# Contacts Reference

## List contacts

```
python scripts/contacts_ops.py list --top 20
python scripts/contacts_ops.py list --search "Jane"
```

## Create contact

```
python scripts/contacts_ops.py create \
  --given-name Jane \
  --surname Doe \
  --email jane.doe@example.com \
  --mobile "+1 555 0100" \
  --company "Contoso"
```

## Get contact by ID

```
python scripts/contacts_ops.py get <contactId>
```

## Update contact

```
python scripts/contacts_ops.py update <contactId> \
  --mobile "+1 555 0123" \
  --company "Contoso Ltd"
```

## Delete contact

```
python scripts/contacts_ops.py delete <contactId>
```

### Notes
- This workflow requires `Contacts.ReadWrite`.
- Use `list` first to collect IDs for update/delete operations.
- Contact changes sync with Outlook contacts for the authenticated account.
