param(
  [Parameter(Mandatory = $true)][string]$InputJson,
  [Parameter(Mandatory = $true)][string]$OutputHtml
)

$ErrorActionPreference = "Stop"

function Esc([object]$x) {
  return [System.Net.WebUtility]::HtmlEncode([string]$x)
}

function MdInline([string]$text) {
  if ($null -eq $text) { return "" }
  $s = Esc $text
  $s = [Regex]::Replace($s, '`([^`]+)`', '<code>$1</code>')
  $s = [Regex]::Replace($s, '\*\*([^*]+)\*\*', '<strong>$1</strong>')
  $paras = @()
  foreach ($p in ($s -split '(\r?\n){2,}')) {
    if (-not [string]::IsNullOrWhiteSpace($p)) {
      $paras += "<p>$($p -replace '\r?\n','<br/>')</p>"
    }
  }
  return ($paras -join "")
}

$raw = Get-Content -Raw -Encoding UTF8 $InputJson
$data = $raw | ConvertFrom-Json

foreach ($c in ($data.commits | ForEach-Object { $_ })) {
  foreach ($f in ($c.findings | ForEach-Object { $_ })) {
    if ([string]::IsNullOrWhiteSpace([string]$f.code)) {
      throw "[render_report] finding '$($f.title)' missing code"
    }
    if ([string]::IsNullOrWhiteSpace([string]$f.fix_code)) {
      throw "[render_report] finding '$($f.title)' missing fix_code"
    }
  }
}

$severityMeta = @{
  "P0"      = @{ label = "P0 - Blocker"; color = "#ef4444"; bg = "#fef2f2"; border = "#fecaca" }
  "blocker" = @{ label = "Blocker"; color = "#ef4444"; bg = "#fef2f2"; border = "#fecaca" }
  "P1"      = @{ label = "P1 - Major"; color = "#f59e0b"; bg = "#fffbeb"; border = "#fde68a" }
  "major"   = @{ label = "Major"; color = "#f59e0b"; bg = "#fffbeb"; border = "#fde68a" }
  "P2"      = @{ label = "P2 - Minor"; color = "#3b82f6"; bg = "#eff6ff"; border = "#bfdbfe" }
  "minor"   = @{ label = "Minor"; color = "#3b82f6"; bg = "#eff6ff"; border = "#bfdbfe" }
  "nit"     = @{ label = "Nit"; color = "#64748b"; bg = "#f8fafc"; border = "#e2e8f0" }
}

$severityOrder = @("P0", "blocker", "P1", "major", "P2", "minor", "nit")

function SeverityIndex([string]$sev) {
  $i = [Array]::IndexOf($severityOrder, $sev)
  if ($i -lt 0) { return 99 }
  return $i
}

function RenderFinding([int]$idx, $f) {
  $sev = [string]($f.severity)
  if ([string]::IsNullOrWhiteSpace($sev)) { $sev = "P2" }
  $meta = $severityMeta[$sev]
  if ($null -eq $meta) { $meta = $severityMeta["P2"] }

  $title = Esc $f.title
  $file = Esc $f.file
  $line = Esc $f.line
  $dim = Esc $f.dimension
  $rule = Esc $f.rule_source
  $problemHtml = MdInline ([string]$f.problem)
  $fixHtml = MdInline ([string]$f.fix_suggestion)

  $codeLang = Esc $f.code_lang
  if ([string]::IsNullOrWhiteSpace($codeLang)) { $codeLang = "text" }
  $fixLang = Esc $f.fix_lang
  if ([string]::IsNullOrWhiteSpace($fixLang)) { $fixLang = $codeLang }

  $code = Esc $f.code
  $fixCode = Esc $f.fix_code

  return @"
<article class="finding" data-sev="$(Esc $sev)" style="--sev-color:$($meta.color); --sev-bg:$($meta.bg); --sev-border:$($meta.border);">
  <header class="f-head">
    <span class="badge">$(Esc $meta.label)</span>
    <span class="dim">$dim</span>
    <span class="rule-src">rule: $rule</span>
  </header>
  <h4 class="f-title">#$idx $title</h4>
  <div class="f-loc"><span class="file">$file</span><span class="line">:$line</span></div>
  <div class="f-section"><div class="f-label">Problem</div><div class="f-body">$problemHtml</div></div>
  <div class="f-section"><div class="f-label">Original Snippet</div><pre class="code"><code class="lang-$codeLang">$code</code></pre></div>
  <div class="f-section"><div class="f-label">Fix</div><div class="f-body">$fixHtml</div><pre class="code fix"><code class="lang-$fixLang">$fixCode</code></pre></div>
</article>
"@
}

function RenderCommit([int]$i, [int]$total, $c) {
  $findings = @()
  if ($null -ne $c.findings) { $findings = @($c.findings) }
  $sorted = $findings | Sort-Object { SeverityIndex ([string]$_.severity) }

  $findingsHtml = ""
  if ($sorted.Count -eq 0) {
    $findingsHtml = '<p class="empty">No issues</p>'
  } else {
    $chunks = @()
    $j = 1
    foreach ($f in $sorted) {
      $chunks += (RenderFinding $j $f)
      $j++
    }
    $findingsHtml = ($chunks -join "`n")
  }

  $p0 = ($findings | Where-Object { $_.severity -in @("P0", "blocker") }).Count
  $p1 = ($findings | Where-Object { $_.severity -in @("P1", "major") }).Count
  $p2 = ($findings | Where-Object { $_.severity -in @("P2", "minor", "nit") }).Count

  $shaShort = ""
  if ($c.sha) { $shaShort = ([string]$c.sha).Substring(0, [Math]::Min(10, ([string]$c.sha).Length)) }

  return @"
<section class="commit-card" id="commit-$shaShort">
  <header class="c-head">
    <div class="c-idx">Commit $i/$total</div>
    <code class="c-sha">$shaShort</code>
    <h3 class="c-subject">$(Esc $c.subject)</h3>
  </header>
  <div class="c-meta">
    <span>Author: $(Esc $c.author)</span>
    <span>Date: $(Esc $c.date)</span>
    <span>Files: $(Esc $c.files_changed)</span>
    <span class="pill p0">P0: $p0</span>
    <span class="pill p1">P1: $p1</span>
    <span class="pill p2">P2: $p2</span>
  </div>
  <div class="findings">$findingsHtml</div>
</section>
"@
}

$repo = Esc $data.repo
$platform = Esc $data.platform
$rng = Esc $data.range
$generatedAt = Esc $data.generated_at
$stats = $data.stats
$summaryHtml = MdInline ([string]$data.summary)
$commits = @()
if ($null -ne $data.commits) { $commits = @($data.commits) }

$tocItems = @()
foreach ($c in $commits) {
  $shaShort = ""
  if ($c.sha) { $shaShort = ([string]$c.sha).Substring(0, [Math]::Min(10, ([string]$c.sha).Length)) }
  $tocItems += "<li><a href=""#commit-$shaShort"">$shaShort - $(Esc $c.subject)</a></li>"
}
$toc = ($tocItems -join "")

$commitCards = @()
$idx = 1
foreach ($c in $commits) {
  $commitCards += (RenderCommit $idx $commits.Count $c)
  $idx++
}
$commitsHtml = ($commitCards -join "`n")

$css = @"
:root {
  --panel: #ffffff;
  --text: #1e293b;
  --muted: #64748b;
  --border: #e2e8f0;
  --accent: #6366f1;
  --accent-2: #8b5cf6;
  --code-bg: #0b1020;
  --code-fg: #e2e8f0;
  --p0: #ef4444;
  --p1: #f59e0b;
  --p2: #3b82f6;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif; color: var(--text); background: linear-gradient(135deg, #f5f7fb 0%, #eef2ff 100%); line-height: 1.6; }
.hero { background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%); color: white; padding: 48px 32px 36px; }
.hero h1 { margin: 0 0 8px; font-size: 28px; }
.hero .meta { display: flex; flex-wrap: wrap; gap: 16px; opacity: .92; font-size: 14px; }
.hero .stats { display: flex; gap: 12px; margin-top: 18px; flex-wrap: wrap; }
.hero .stat { background: rgba(255,255,255,.18); border: 1px solid rgba(255,255,255,.25); border-radius: 10px; padding: 10px 14px; font-size: 13px; }
.hero .stat b { font-size: 18px; display: block; margin-bottom: 2px; }
.container { max-width: 1100px; margin: -24px auto 60px; padding: 0 24px; }
.summary-card, .toc, .commit-card { background: var(--panel); border-radius: 14px; box-shadow: 0 4px 16px rgba(15,23,42,.06); padding: 22px 24px; margin-bottom: 20px; border: 1px solid var(--border); }
.toc h2 { margin: 0 0 12px; font-size: 16px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
.toc ol { margin: 0; padding-left: 20px; }
.toc li { margin: 6px 0; }
.toc a { color: var(--accent); text-decoration: none; }
.toc a:hover { text-decoration: underline; }
.commit-card .c-head { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 8px; }
.c-idx { font-size: 12px; color: var(--muted); background:#f1f5f9; padding: 2px 8px; border-radius: 6px; }
.c-sha { font-family: ui-monospace, Menlo, Consolas, monospace; background:#eef2ff; color:#4338ca; padding:2px 8px; border-radius:6px; font-size:13px; }
.c-subject { margin: 0; font-size: 18px; }
.c-meta { display: flex; gap: 12px; flex-wrap: wrap; color: var(--muted); font-size: 13px; margin-bottom: 18px; padding-bottom: 14px; border-bottom: 1px dashed var(--border); }
.pill { padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; color: white; }
.pill.p0 { background: var(--p0); }
.pill.p1 { background: var(--p1); }
.pill.p2 { background: var(--p2); }
.finding { border-left: 4px solid var(--sev-color); background: var(--sev-bg); border: 1px solid var(--sev-border); border-left-width: 4px; border-radius: 10px; padding: 16px 18px; margin: 14px 0; }
.finding .f-head { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 6px; }
.finding .badge { background: var(--sev-color); color: white; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; }
.finding .dim { color: var(--muted); font-size: 12px; }
.finding .rule-src { color: var(--muted); font-size: 12px; font-family: ui-monospace, monospace; }
.f-title { margin: 4px 0 6px; font-size: 16px; }
.f-loc { font-size: 13px; color: var(--muted); margin-bottom: 12px; font-family: ui-monospace, monospace; }
.f-section { margin-top: 10px; }
.f-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px; color: var(--muted); font-weight: 700; margin-bottom: 6px; }
.f-body p { margin: 4px 0; }
.f-body code { background: rgba(15,23,42,.08); padding: 1px 5px; border-radius: 4px; font-size: 90%; }
pre.code { background: var(--code-bg); color: var(--code-fg); padding: 14px 16px; border-radius: 8px; overflow-x: auto; font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 13px; line-height: 1.55; margin: 6px 0 0; }
pre.code.fix { background: #052e1a; border-left: 3px solid #10b981; }
.filter-bar { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.filter-bar button { border: 1px solid var(--border); background: white; padding: 6px 14px; border-radius: 999px; cursor: pointer; font-size: 13px; color: var(--text); transition: all .15s; }
.filter-bar button.active { background: var(--accent); color: white; border-color: var(--accent); }
.filter-bar button:hover:not(.active) { background: #f1f5f9; }
footer { text-align: center; color: var(--muted); font-size: 12px; padding: 30px 0; }
.empty { color: var(--muted); font-style: italic; }
"@

$js = @"
document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.filter-bar button');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const sev = btn.dataset.sev;
      document.querySelectorAll('.finding').forEach(f => {
        if (sev === 'all') {
          f.style.display = '';
        } else {
          const fsev = f.dataset.sev;
          const matches = (sev === 'P0' && (fsev === 'P0' || fsev === 'blocker')) ||
                          (sev === 'P1' && (fsev === 'P1' || fsev === 'major')) ||
                          (sev === 'P2' && (fsev === 'P2' || fsev === 'minor' || fsev === 'nit'));
          f.style.display = matches ? '' : 'none';
        }
      });
    });
  });
});
"@

$title = "Code Review - $rng"
$filesChanged = Esc $stats.files_changed
$added = Esc $stats.added
$removed = Esc $stats.removed
$commitCount = $commits.Count

$html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>$title</title>
<style>$css</style>
</head>
<body>
<div class="hero">
  <h1>Code Review Report</h1>
  <div class="meta">
    <span>Repo: $repo</span>
    <span>Platform: $platform</span>
    <span>Range: $rng</span>
    <span>Generated: $generatedAt</span>
  </div>
  <div class="stats">
    <div class="stat"><b>$filesChanged</b>files changed</div>
    <div class="stat"><b style="color:#bbf7d0">+$added</b>insertions</div>
    <div class="stat"><b style="color:#fecaca">-$removed</b>deletions</div>
    <div class="stat"><b>$commitCount</b>commits reviewed</div>
  </div>
</div>

<div class="container">
  <section class="summary-card">
    <h2>Summary</h2>
    $summaryHtml
  </section>

  <section class="toc">
    <h2>Commits</h2>
    <ol>$toc</ol>
  </section>

  <div class="filter-bar">
    <button class="active" data-sev="all">All</button>
    <button data-sev="P0">P0</button>
    <button data-sev="P1">P1</button>
    <button data-sev="P2">P2</button>
  </div>

  $commitsHtml

  <footer>Generated by code-reviewer skill - $generatedAt</footer>
</div>
<script>$js</script>
</body>
</html>
"@

$outPath = [System.IO.Path]::GetFullPath($OutputHtml)
[System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($outPath)) | Out-Null
$html | Out-File -FilePath $outPath -Encoding UTF8
Write-Output $outPath
