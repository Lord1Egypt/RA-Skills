# OneDrive Reference

## List items

```
python scripts/drive_ops.py list --path / --top 20
python scripts/drive_ops.py list --path /Documentos --top 20
python scripts/drive_ops.py list --path /Documents --top 20
```

## Upload

```
python scripts/drive_ops.py upload --local files/briefing.docx --remote /Clients/briefing.docx
```

## Download

```
python scripts/drive_ops.py download --remote /Clients/briefing.docx --local /tmp/briefing.docx
```

## Move

```
python scripts/drive_ops.py move <itemId> --dest /Archive/Processed
```

## Share link

```
python scripts/drive_ops.py share <itemId> --scope organization --type view
```

### Notes
- Remote paths should always start with `/`.
- The script resolves localized special-folder names and global aliases (for example `Documents` or `Documentos`).
- For root-level listing, `--path /` uses the dedicated root endpoint.
- To get an `item_id`, run `list` and copy the `id` field.
- Chunked upload is not implemented yet; large files require upload session support.
