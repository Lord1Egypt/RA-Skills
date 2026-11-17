<#
    Companion-Starter — Vorlage.

    Anpassen: $AppName, $Script, $DefaultPort. Alles andere kann so bleiben.

    Der Aufwand steckt nicht im Starten, sondern in den vier Faellen, in denen
    es schiefgeht: Laufzeit fehlt, laeuft schon, Port antwortet nicht,
    Programm bricht sofort ab. Jeder davon braucht eine Antwort, die dem
    Nutzer sagt, was er tun soll.

    Aufruf:
      .\start.ps1                 starten und oeffnen
      .\start.ps1 -Stop           beenden
      .\start.ps1 -Status         nachsehen, ob es laeuft
      .\start.ps1 -Port 9000      anderer Port
      .\start.ps1 -Console        sichtbares Fenster (Fehlersuche)
      .\start.ps1 -NoBrowser      nur starten, kein Fenster
#>
[CmdletBinding()]
param(
  [int]    $Port     = 0,
  [int]    $Interval = 120,
  [switch] $Stop,
  [switch] $Status,
  [switch] $Console,
  [switch] $NoBrowser
)

# ------------------------------------------------------------ anpassen ---
$AppName     = 'Companion'
$Script      = 'server.py'
$DefaultPort = 8765
$HealthPath  = '/api/status'          # muss HTTP 200 liefern, wenn bereit
# -------------------------------------------------------------------------

$ErrorActionPreference = 'Stop'
if ($Port -eq 0) { $Port = $DefaultPort }

$Root    = Split-Path -Parent $MyInvocation.MyCommand.Path
$DataDir = Join-Path $Root 'data'
$PidFile = Join-Path $DataDir 'companion.pid'
$LogFile = Join-Path $DataDir 'companion.log'
$Url     = "http://127.0.0.1:$Port"

function Say($m) { Write-Host "  $m" }

function Test-Alive {
  try { (Invoke-WebRequest -Uri "$Url$HealthPath" -TimeoutSec 2 -UseBasicParsing).StatusCode -eq 200 }
  catch { $false }
}

function Get-Running {
  if (-not (Test-Path $PidFile)) { return $null }
  $id = Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
  if (-not $id) { return $null }
  Get-Process -Id ([int]$id) -ErrorAction SilentlyContinue
}

if ($Stop) {
  $p = Get-Running
  if ($p) { Stop-Process -Id $p.Id -Force; Say "$AppName beendet (PID $($p.Id))." }
  else    { Say 'Es lief nichts aus diesem Starter.' }
  Remove-Item $PidFile -ErrorAction SilentlyContinue
  return
}

if ($Status) {
  if (Test-Alive) { $p = Get-Running; Say "Laeuft auf $Url$(if ($p) { " (PID $($p.Id))" })." }
  else            { Say "Auf $Url antwortet nichts." }
  return
}

Write-Host ''
Write-Host "  $AppName"
Write-Host ('  ' + '-' * $AppName.Length)

# 1. Laufzeit suchen — und beim Fehlen konkret helfen.
$exe = $null; $pre = @()
foreach ($c in @(@{e='py';a=@('-3')}, @{e='python';a=@()}, @{e='python3';a=@()})) {
  if (Get-Command $c.e -ErrorAction SilentlyContinue) { $exe = $c.e; $pre = $c.a; break }
}
if (-not $exe) {
  Write-Host ''
  Write-Host '  Python wurde nicht gefunden.' -ForegroundColor Yellow
  Write-Host '  Herunterladen: https://www.python.org/downloads/'
  Write-Host '  Beim Installieren "Add python.exe to PATH" ankreuzen — ohne'
  Write-Host '  diesen Haken findet der Starter Python spaeter nicht.'
  Write-Host ''
  Read-Host '  Eingabetaste zum Schliessen'
  exit 1
}
Say "Python: $exe $($pre -join ' ')"

# 2. Nicht doppelt starten.
if (Test-Alive) {
  Say "Laeuft bereits auf $Url — wird nicht erneut gestartet."
} else {
  New-Item -ItemType Directory -Force -Path $DataDir | Out-Null
  $a = $pre + @($Script, '--port', "$Port", '--poll-interval', "$Interval", '--no-browser')

  if ($Console) {
    $proc = Start-Process -FilePath $exe -ArgumentList $a -WorkingDirectory $Root -PassThru
  } else {
    $proc = Start-Process -FilePath $exe -ArgumentList $a -WorkingDirectory $Root `
              -WindowStyle Hidden -PassThru `
              -RedirectStandardOutput $LogFile -RedirectStandardError "$LogFile.err"
  }
  Set-Content -Path $PidFile -Value $proc.Id
  Say "Gestartet (PID $($proc.Id)), warte auf Antwort ..."

  # 3. Auf den Port warten, nicht auf die Uhr.
  $ok = $false
  foreach ($i in 1..40) {                       # bis zu 20 Sekunden
    Start-Sleep -Milliseconds 500
    if (Test-Alive)      { $ok = $true; break }
    if ($proc.HasExited) { break }
  }

  # 4. Beim Scheitern zeigen, woran es lag.
  if (-not $ok) {
    Write-Host ''
    Write-Host '  Keine Antwort.' -ForegroundColor Yellow
    if (Test-Path "$LogFile.err") {
      Write-Host '  Letzte Zeilen der Fehlerausgabe:'
      Get-Content "$LogFile.err" -Tail 15 | ForEach-Object { Write-Host "    $_" }
    }
    Write-Host ''
    Write-Host '  Nochmal mit sichtbarem Fenster:  .\start.ps1 -Console'
    Read-Host '  Eingabetaste zum Schliessen'
    exit 1
  }
  Say 'Antwortet.'
}

if ($NoBrowser) { Say "Bereit: $Url"; return }

# Als eigenes Fenster oeffnen — ohne Adressleiste wirkt es wie ein Programm.
$edge   = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
$chrome = "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe"
if     (Test-Path $edge)   { Start-Process $edge   "--app=$Url"; Say 'Eigenes Fenster (Edge).' }
elseif (Test-Path $chrome) { Start-Process $chrome "--app=$Url"; Say 'Eigenes Fenster (Chrome).' }
else                       { Start-Process $Url;                 Say 'Im Standardbrowser.' }

Write-Host ''
Write-Host "  Laeuft im Hintergrund auf $Url"
Write-Host '  Beenden:  .\start.ps1 -Stop'
Write-Host ''
