param(
    [Parameter(Mandatory = $true)]
    [string]$InputDocx,
    [string]$OutputDocx,
    [string]$PdfPath
)

# Keep Chinese paths and diagnostics readable even when Windows starts
# PowerShell with the legacy GBK console code page.
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[Console]::InputEncoding = $utf8NoBom
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

$source = (Resolve-Path -LiteralPath $InputDocx).Path
if ([string]::IsNullOrWhiteSpace($OutputDocx)) {
    $target = $source
} else {
    $target = [System.IO.Path]::GetFullPath($OutputDocx)
    if ($target -ne $source) {
        Copy-Item -LiteralPath $source -Destination $target -Force
    }
}

$app = $null
$doc = $null
$provider = $null
foreach ($candidate in @('Word.Application', 'kwps.Application')) {
    try {
        $app = New-Object -ComObject $candidate
        $provider = $candidate
        break
    } catch {
        $app = $null
    }
}
if ($null -eq $app) {
    throw '未找到可自动化的 Microsoft Word 或 WPS。不能可靠刷新 TOC/PAGE 字段。'
}

try {
    $app.Visible = $false
    $doc = $app.Documents.Open($target)
    $doc.Fields.Update() | Out-Null
    for ($i = 1; $i -le $doc.TablesOfContents.Count; $i++) {
        $doc.TablesOfContents.Item($i).Update()
    }
    foreach ($section in $doc.Sections) {
        foreach ($header in $section.Headers) {
            if ($header.Exists) { $header.Range.Fields.Update() | Out-Null }
        }
        foreach ($footer in $section.Footers) {
            if ($footer.Exists) { $footer.Range.Fields.Update() | Out-Null }
        }
    }
    $doc.Save()
    if (-not [string]::IsNullOrWhiteSpace($PdfPath)) {
        $pdf = [System.IO.Path]::GetFullPath($PdfPath)
        $doc.ExportAsFixedFormat($pdf, 17)
    }
    [pscustomobject]@{
        Provider = $provider
        Document = $target
        Sections = $doc.Sections.Count
        TablesOfContents = $doc.TablesOfContents.Count
        Pages = $doc.ComputeStatistics(2)
        Pdf = if ($PdfPath) { [System.IO.Path]::GetFullPath($PdfPath) } else { $null }
    }
} finally {
    if ($null -ne $doc) { $doc.Close($false) }
    if ($null -ne $app) { $app.Quit() }
}
