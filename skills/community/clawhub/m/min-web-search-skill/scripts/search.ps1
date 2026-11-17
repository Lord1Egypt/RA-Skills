#Requires -Version 5.1
<#
.SYNOPSIS
    min-web-search: Bing RSS web search for Windows (no API key).

.DESCRIPTION
    Searches Bing via its public RSS endpoint using native PowerShell.
    No external dependencies, no API key required.

.PARAMETER Query
    The search query string.

.PARAMETER Max
    Maximum number of results (default: 5).

.PARAMETER Json
    Output results as JSON.

.EXAMPLE
    .\search.ps1 "python tutorial"
    .\search.ps1 "python tutorial" -Max 3 -Json
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Query,

    [int]$Max = 5,

    [switch]$Json
)

$ErrorActionPreference = "Stop"
$UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
$encoded = [System.Uri]::EscapeDataString($Query)
$url = "https://www.bing.com/search?q=$encoded&format=rss"

try {
    $resp = Invoke-WebRequest -Uri $url -UserAgent $UA -TimeoutSec 10 -UseBasicParsing
    [xml]$xml = $resp.Content
} catch {
    if ($Json) {
        Write-Output '{"success":false,"error":"' + $_.Exception.Message.Replace('"','\"') + '"}'
    } else {
        Write-Error "Search failed: $($_.Exception.Message)"
    }
    exit 1
}

$items = $xml.rss.channel.item | Select-Object -First $Max
$results = @()

foreach ($item in $items) {
    $title = if ($item.title) { $item.title.Trim() } else { "" }
    $link = if ($item.link) { $item.link.Trim() } else { "" }
    $snippet = ""
    if ($item.description) {
        $snippet = ($item.description -replace '<[^>]+>','').Trim()
    }
    if ($title -and $link) {
        $results += @{ title = $title; url = $link; snippet = $snippet }
    }
}

if ($results.Count -eq 0) {
    if ($Json) {
        Write-Output '{"success":false,"error":"No results returned"}'
    } else {
        Write-Error "No results returned"
    }
    exit 1
}

if ($Json) {
    $output = @{ success = $true; query = $Query; results = $results }
    Write-Output ($output | ConvertTo-Json -Depth 5 -Compress)
} else {
    $i = 1
    foreach ($r in $results) {
        Write-Output "$i. $($r.title)"
        Write-Output "   $($r.url)"
        if ($r.snippet) { Write-Output "   $($r.snippet.Substring(0, [Math]::Min(200, $r.snippet.Length)))" }
        Write-Output ""
        $i++
    }
}
