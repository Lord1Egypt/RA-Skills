# Drive Reference

## Browse and Search

```bash
gws drive files list --params '{"pageSize":10,"orderBy":"modifiedTime desc"}'
gws drive files list --params '{"q":"mimeType=\"application/vnd.google-apps.spreadsheet\""}'
gws drive files list --params '{"q":"'\''FOLDER_ID'\'' in parents"}'
```

## Upload (two-step: upload then rename)

`files create` does not pass `name` to the API — files upload as "Untitled". Upload first, then rename:

```bash
cd ~/Downloads
gws drive files create --params '{}' --upload file.txt --upload-content-type text/plain
gws drive files update --params '{"fileId":"FILE_ID"}' --json '{"name":"real_name.txt"}'
```

Note: `files copy` does respect `name`.

## Create Folder

```bash
gws drive files create --params '{}' --json '{"name":"Folder Name","mimeType":"application/vnd.google-apps.folder"}'
```

## Copy and Move

```bash
gws drive files copy --params '{"fileId":"ID"}' --json '{"name":"Copy of file"}'
gws drive files update --params '{"fileId":"ID","addParents":"FOLDER_ID","removeParents":"root"}' --json '{}'
```

## Download and Export

Native files: `get --alt media`. Google formats (Sheets/Docs/Slides): `export`.

```bash
gws drive files get --params '{"fileId":"ID","alt":"media"}' --output file.txt
gws drive files export --params '{"fileId":"ID","mimeType":"application/pdf"}' --output doc.pdf
gws drive files export --params '{"fileId":"ID","mimeType":"text/csv"}' --output data.csv
```

## Permissions and Storage

```bash
gws drive permissions list --params '{"fileId":"ID","pageSize":10}'
gws drive about get --params '{"fields":"storageQuota"}' 2>/dev/null | tail -n +2 | jq '.storageQuota'
```

## Delete

`files delete` returns `{"status":"success","saved_file":"download.html"}` — ignore the `saved_file` field.

```bash
gws drive files delete --params '{"fileId":"ID"}'
```
