# PowerShell HTTP Static Server

## Pode Module (recommended)

Install:

```powershell
Install-Module -Name Pode
```

One-liner:

```powershell
Start-PodeStaticServer -Port 8000 -FileBrowser -Address 0.0.0.0
```

Features:
- Directory listing: Yes (`-FileBrowser`)
- HTTPS support
- Authentication middleware
- Cross-platform (PowerShell Core)

## .NET HttpListener (no modules needed)

```powershell
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("http://localhost:8000/")
$listener.Start()
Write-Host "Serving on http://localhost:8000/"
while ($listener.IsListening) {
    $context = $listener.GetContext()
    $path = Join-Path $PWD $context.Request.Url.LocalPath
    if (Test-Path $path -PathType Leaf) {
        $bytes = [System.IO.File]::ReadAllBytes($path)
        $context.Response.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
        $context.Response.StatusCode = 404
    }
    $context.Response.Close()
}
```

Features:
- No module install needed
- Works on Windows PowerShell and PowerShell Core

## IIS Express (Windows only)

```cmd
"C:\Program Files (x86)\IIS Express\iisexpress.exe" /path:C:\MyWeb /port:8000
```

Features:
- Directory listing: No
- `/path` must be an absolute path
- Full IIS feature set
- Windows only
