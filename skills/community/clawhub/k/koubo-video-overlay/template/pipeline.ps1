# Run in the project folder. Render evidence-image transparent sequences, overlay onto original at narration times, keep original audio.
# Adjust $T1/$T2/$T3 (seconds) to sync images to narration. Add/remove EvN blocks to match the number of images.
# NOTE: save this file as UTF-8 WITH BOM if any path contains Chinese, else PowerShell parses it as GBK and fails.
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Source = Join-Path $Root '本次素材\原片.mp4'
$Work = Join-Path $Root 'work'
$OutDir = Join-Path $Root '成片'
$Out = Join-Path $OutDir 'final.mp4'
$Chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'

$T1 = 4
$T2 = 30
$T3 = 60

foreach ($cmd in @('node', 'npm', 'ffmpeg', 'ffprobe')) {
  if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { throw "missing $cmd" }
}
if (-not (Test-Path -LiteralPath $Source)) { throw "missing source video" }
if (-not (Test-Path -LiteralPath $Chrome)) { throw "missing Chrome" }
foreach ($img in @('img1.png','img2.png','img3.png')) {
  if (-not (Test-Path -LiteralPath (Join-Path $Root "public\$img"))) { throw "missing public\$img" }
}

Set-Location $Root
New-Item -ItemType Directory -Force -Path $OutDir, (Join-Path $Work 'frames1'), (Join-Path $Work 'frames2'), (Join-Path $Work 'frames3') | Out-Null
if (-not (Test-Path -LiteralPath (Join-Path $Root 'node_modules\remotion'))) { throw 'node_modules\remotion missing (junction broken? run npm ci)' }

foreach ($pair in @(@('Ev1','frames1'), @('Ev2','frames2'), @('Ev3','frames3'))) {
  $comp = $pair[0]; $dir = $pair[1]
  Get-ChildItem (Join-Path $Work $dir) -Filter *.png -ErrorAction SilentlyContinue | Remove-Item -Force
  npx remotion render src/index.ts $comp "work/$dir" `
    --sequence --image-format=png `
    --image-sequence-pattern='frame-[frame].png' `
    --concurrency=2 `
    --browser-executable="$Chrome"
  if ($LASTEXITCODE -ne 0) { throw "Remotion render $comp failed" }
}

Push-Location $Work
try {
  ffmpeg -y `
    -i $Source `
    -itsoffset $T1 -framerate 30 -start_number 0 -i (Join-Path $Work 'frames1\frame-%03d.png') `
    -itsoffset $T2 -framerate 30 -start_number 0 -i (Join-Path $Work 'frames2\frame-%03d.png') `
    -itsoffset $T3 -framerate 30 -start_number 0 -i (Join-Path $Work 'frames3\frame-%03d.png') `
    -filter_complex_script (Join-Path $Work 'composite.txt') `
    -map '[v]' -map '[a]' `
    -c:v libx264 -pix_fmt yuv420p -crf 18 `
    -c:a aac -ar 32000 -ac 2 -b:a 128k `
    $Out
  if ($LASTEXITCODE -ne 0) { throw 'ffmpeg composite failed' }
}
finally { Pop-Location }

ffprobe -hide_banner -show_entries stream=codec_type,duration -of default $Out
Write-Output "DONE: $Out"