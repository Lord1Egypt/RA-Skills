# Command Recipes

## Public Page To Markdown File

```powershell
obclip "https://example.com/article" --output "D:\data\Clippings\"
```

## Public Page To stdout

```powershell
obclip "https://example.com/article"
```

## Real Chromium With Dedicated Profile

```powershell
obclip "https://example.com/article" `
  --browser-executable "D:\app\chrome-win\chrome.exe" `
  --browser-profile "D:\obclip-profile" `
  --headful `
  --output "D:\data\Clippings\"
```

## Dynamic SPA With Extra Delay

```powershell
obclip "https://example.com/app" `
  --settle-ms 5000 `
  --output "D:\data\Clippings\"
```

## Dynamic SPA With Explicit Wait Selector

```powershell
obclip "https://example.com/app" `
  --wait-selector "article" `
  --settle-ms 3000 `
  --output "D:\data\Clippings\"
```

## Logged-In X Or Similar Social Page

```powershell
obclip "https://x.com/<user>/status/<id>" `
  --browser-executable "D:\app\chrome-win\chrome.exe" `
  --browser-profile "D:\obclip-x-profile" `
  --headful `
  --wait-selector "article" `
  --settle-ms 5000 `
  --output "D:\data\Clippings\"
```

## Open The Result In Obsidian

```powershell
obclip "https://example.com/article" `
  --output "D:\data\Clippings\" `
  --open `
  --vault "MyVault"
```

## Template Override

```powershell
obclip "https://example.com/article" `
  --template "D:\data\obclip-templates" `
  --output "D:\data\Clippings\"
```

## Notes

- Add `--wait-selector` only when the default waiting rules plus `--settle-ms` are insufficient.
- Use a dedicated browser profile for login-heavy or anti-bot sites.
- Successful saves print the final full path to `stderr`.
