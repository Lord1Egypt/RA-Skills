param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [string]$OutputFile,

    [int]$Width = 480,

    [int]$Fps = 15
)

if (-not (Test-Path $InputFile)) {
    Write-Error "File not found: $InputFile"
    exit 1
}

if (-not $OutputFile) {
    $OutputFile = [System.IO.Path]::ChangeExtension($InputFile, ".gif")
}

$palette = [System.IO.Path]::GetTempFileName() + ".png"

Write-Host "Generating palette..."
ffmpeg -y -i $InputFile -vf "fps=$Fps,scale=${Width}:-1:flags=lanczos,palettegen=stats_mode=diff" $palette 2>$null

Write-Host "Converting to GIF..."
ffmpeg -y -i $InputFile -i $palette -lavfi "fps=$Fps,scale=${Width}:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" $OutputFile 2>$null

Remove-Item $palette -ErrorAction SilentlyContinue

if (Test-Path $OutputFile) {
    $size = [math]::Round((Get-Item $OutputFile).Length / 1MB, 2)
    Write-Host "Done: $OutputFile ($size MB)"
} else {
    Write-Error "Conversion failed."
    exit 1
}
