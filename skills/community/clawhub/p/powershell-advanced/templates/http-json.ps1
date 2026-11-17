# HTTP JSON with a bounded timeout.
# Keep tokens out of logs; read from the process environment.

param(
    [Parameter(Mandatory)][string]$Uri,
    [string]$Method = 'GET',
    [string]$TokenEnv = 'LYGO_API_TOKEN',
    [string]$BodyPath = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$headers = @{ Accept = 'application/json' }
$token = [Environment]::GetEnvironmentVariable($TokenEnv)
if ($token) { $headers.Authorization = "Bearer $token" }

$params = @{
    Uri         = $Uri
    Method      = $Method
    Headers     = $headers
    TimeoutSec  = 30
    ErrorAction = 'Stop'
}
if ($BodyPath) { $params.Body = Get-Content -LiteralPath $BodyPath -Raw }
if ($BodyPath) { $params.ContentType = 'application/json' }

try {
    $r = Invoke-RestMethod @params
    $r | ConvertTo-Json -Depth 20
}
catch {
    Write-Error ("HTTP_FAILED {0}`n{1}" -f $_.Exception.Message, $_.ScriptStackTrace)
    exit 1
}
