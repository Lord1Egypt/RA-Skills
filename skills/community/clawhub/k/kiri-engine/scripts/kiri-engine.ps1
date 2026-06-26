<#
.SYNOPSIS
    KIRI Engine API 调用脚本 - 3D 扫描重建 / 高斯泼溅资产生成
    
.DESCRIPTION
    支持 Photo Scan / Featureless Scan / 3DGS Scan 三种算法
    支持视频上传和图片集上传两种输入方式
    
.PARAMETER Action
    balance | photo-video | photo-image | featureless-video | featureless-image | 3dgs-video | 3dgs-image | status | download
    
.PARAMETER Video
    视频文件路径（≤1920x1080, ≤3 分钟）
    
.PARAMETER Images
    图片集路径（文件夹路径 或 通配符如 C:\images\*.jpg），20~300 张
    
.PARAMETER Serialize
    任务序列号（上传后返回的 serialize）
    
.PARAMETER Output
    模型下载保存目录（默认 ~/Downloads/KiriEngine）
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet('balance', 'photo-video', 'photo-image', 
                 'featureless-video', 'featureless-image',
                 '3dgs-video', '3dgs-image', 'status', 'download')]
    [string]$Action,
    
    [string]$Video,
    [string]$Images,
    [string]$Serialize,
    [string]$Output,
    
    # Photo Scan 参数
    [int]$ModelQuality = 1,
    [int]$TextureQuality = 1,
    [string]$FileFormat = 'OBJ',
    [int]$IsMask = 1,
    [int]$TextureSmoothing = 1,
    
    # 3DGS 参数
    [int]$IsMesh = 0
)

$ConfigPath = Join-Path $env:USERPROFILE '.kiri-engine-config.json'
$BaseUrl = 'https://api.kiriengine.app/api/v1/open'

# ── 读取 API Key ──────────────────────────────────────────
function Get-ApiKey {
    if (-not (Test-Path $ConfigPath)) {
        Write-Host "❌ 未找到 API Key 配置" -ForegroundColor Red
        Write-Host "请创建配置文件：$ConfigPath" -ForegroundColor Yellow
        Write-Host "内容格式：{ `"apiKey`": `"kiri-你的密钥`" }" -ForegroundColor Yellow
        exit 1
    }
    $config = Get-Content $ConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $config.apiKey) {
        Write-Host "❌ 配置文件中缺少 apiKey 字段" -ForegroundColor Red
        exit 1
    }
    return $config.apiKey
}

# ── Multipart 上传（.NET 实现，兼容 PS 5.1）──────────────
function Invoke-MultipartUpload {
    param(
        [string]$Url,
        [string]$ApiKey,
        [hashtable]$Fields = @{},
        [string]$FileFieldName = 'videoFile',
        [string[]]$FilePaths = @()
    )
    
    Add-Type -AssemblyName System.Net.Http -ErrorAction SilentlyContinue
    
    $handler = New-Object System.Net.Http.HttpClientHandler
    $client = New-Object System.Net.Http.HttpClient($handler)
    $client.Timeout = [TimeSpan]::FromMinutes(30)
    $client.DefaultRequestHeaders.Add('Authorization', "Bearer $ApiKey")
    
    $content = New-Object System.Net.Http.MultipartFormDataContent
    
    # 添加文本字段
    foreach ($key in $Fields.Keys) {
        $strContent = New-Object System.Net.Http.StringContent("$($Fields[$key])")
        $content.Add($strContent, $key)
    }
    
    # 添加文件
    foreach ($fp in $FilePaths) {
        if (-not (Test-Path $fp)) {
            Write-Host "❌ 文件不存在：$fp" -ForegroundColor Red
            exit 1
        }
        $fs = [System.IO.File]::OpenRead($fp)
        $fileName = [System.IO.Path]::GetFileName($fp)
        $fileContent = New-Object System.Net.Http.StreamContent($fs)
        $fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse('application/octet-stream')
        $content.Add($fileContent, $FileFieldName, $fileName)
    }
    
    try {
        $response = $client.PostAsync($Url, $content).Result
        $body = $response.Content.ReadAsStringAsync().Result
        $result = $body | ConvertFrom-Json
        
        if (-not $result.ok) {
            Write-Host "❌ API 错误：$($result.msg)" -ForegroundColor Red
            Write-Host "HTTP 状态码：$([int]$response.StatusCode)" -ForegroundColor Red
            exit 1
        }
        
        return $result
    }
    catch {
        Write-Host "❌ 请求失败：$_" -ForegroundColor Red
        exit 1
    }
    finally {
        # 清理文件流
        foreach ($item in $content) {
            if ($item -is [System.Net.Http.StreamContent]) {
                $item.Dispose()
            }
        }
        $client.Dispose()
    }
}

# ── GET 请求 ──────────────────────────────────────────────
function Invoke-KiriGet {
    param([string]$Url, [string]$ApiKey)
    
    $headers = @{ 'Authorization' = "Bearer $ApiKey" }
    
    try {
        $response = Invoke-RestMethod -Uri $Url -Method GET -Headers $headers -TimeoutSec 30
        return $response
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "❌ API 请求失败 (HTTP $statusCode)：$($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# ── 检查余额 ──────────────────────────────────────────────
function Get-Balance {
    $apiKey = Get-ApiKey
    $response = Invoke-KiriGet -Url "$BaseUrl/balance" -ApiKey $apiKey
    
    if ($response.ok) {
        Write-Host "✅ 当前余额：$($response.data.balance) 积分" -ForegroundColor Green
    }
    else {
        Write-Host "❌ 查询失败：$($response.msg)" -ForegroundColor Red
    }
}

# ── Photo Scan - 视频 ────────────────────────────────────
function Submit-PhotoVideo {
    if (-not $Video) {
        Write-Host "❌ 必须指定 -video 参数" -ForegroundColor Red
        exit 1
    }
    $apiKey = Get-ApiKey
    $fields = @{
        'modelQuality' = "$ModelQuality"
        'textureQuality' = "$TextureQuality"
        'fileFormat' = $FileFormat
        'isMask' = "$IsMask"
        'textureSmoothing' = "$TextureSmoothing"
    }
    
    $response = Invoke-MultipartUpload -Url "$BaseUrl/photo/video" -ApiKey $apiKey `
        -Fields $fields -FileFieldName 'videoFile' -FilePaths @($Video)
    
    Write-Host "✅ Photo Scan 上传成功！" -ForegroundColor Green
    Write-Host "Serialize: $($response.data.serialize)" -ForegroundColor Cyan
    Write-Host "算法类型：Photo Scan (calculateType=$($response.data.calculateType))" -ForegroundColor Cyan
}

# ── Photo Scan - 图片集 ──────────────────────────────────
function Submit-PhotoImage {
    if (-not $Images) {
        Write-Host "❌ 必须指定 -images 参数" -ForegroundColor Red
        exit 1
    }
    
    $imageFiles = @()
    if (Test-Path $Images -PathType Container) {
        $imageFiles = @(Get-ChildItem $Images -Include *.jpg,*.jpeg,*.png,*.tif,*.tiff -File -Recurse)
    }
    else {
        $imageFiles = @(Get-ChildItem $Images -File)
    }
    
    if ($imageFiles.Count -lt 20) {
        Write-Host "❌ 图片不足：至少 20 张，当前 $($imageFiles.Count) 张" -ForegroundColor Red
        exit 1
    }
    if ($imageFiles.Count -gt 300) {
        Write-Host "❌ 图片超限：最多 300 张，当前 $($imageFiles.Count) 张" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "📸 准备上传 $($imageFiles.Count) 张图片..." -ForegroundColor Yellow
    $apiKey = Get-ApiKey
    $fields = @{
        'modelQuality' = "$ModelQuality"
        'textureQuality' = "$TextureQuality"
        'fileFormat' = $FileFormat
        'isMask' = "$IsMask"
        'textureSmoothing' = "$TextureSmoothing"
    }
    
    $response = Invoke-MultipartUpload -Url "$BaseUrl/photo/image" -ApiKey $apiKey `
        -Fields $fields -FileFieldName 'imagesFiles' -FilePaths ($imageFiles | ForEach-Object { $_.FullName })
    
    Write-Host "✅ Photo Scan 图片集上传成功！" -ForegroundColor Green
    Write-Host "Serialize: $($response.data.serialize)" -ForegroundColor Cyan
}

# ── Featureless Scan - 视频 ──────────────────────────────
function Submit-FeaturelessVideo {
    if (-not $Video) {
        Write-Host "❌ 必须指定 -video 参数" -ForegroundColor Red
        exit 1
    }
    $apiKey = Get-ApiKey
    $fields = @{ 'fileFormat' = $FileFormat }
    
    $response = Invoke-MultipartUpload -Url "$BaseUrl/featureless/video" -ApiKey $apiKey `
        -Fields $fields -FileFieldName 'videoFile' -FilePaths @($Video)
    
    Write-Host "✅ Featureless Scan 上传成功！" -ForegroundColor Green
    Write-Host "Serialize: $($response.data.serialize)" -ForegroundColor Cyan
    Write-Host "算法类型：Featureless (calculateType=$($response.data.calculateType))" -ForegroundColor Cyan
}

# ── Featureless Scan - 图片集 ────────────────────────────
function Submit-FeaturelessImage {
    if (-not $Images) {
        Write-Host "❌ 必须指定 -images 参数" -ForegroundColor Red
        exit 1
    }
    
    $imageFiles = @()
    if (Test-Path $Images -PathType Container) {
        $imageFiles = @(Get-ChildItem $Images -Include *.jpg,*.jpeg,*.png,*.tif,*.tiff -File -Recurse)
    }
    else {
        $imageFiles = @(Get-ChildItem $Images -File)
    }
    
    if ($imageFiles.Count -lt 20 -or $imageFiles.Count -gt 300) {
        Write-Host "❌ 图片数量必须在 20~300 之间，当前 $($imageFiles.Count) 张" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "📸 准备上传 $($imageFiles.Count) 张图片..." -ForegroundColor Yellow
    $apiKey = Get-ApiKey
    $fields = @{ 'fileFormat' = $FileFormat }
    
    $response = Invoke-MultipartUpload -Url "$BaseUrl/featureless/image" -ApiKey $apiKey `
        -Fields $fields -FileFieldName 'imagesFiles' -FilePaths ($imageFiles | ForEach-Object { $_.FullName })
    
    Write-Host "✅ Featureless Scan 图片集上传成功！" -ForegroundColor Green
    Write-Host "Serialize: $($response.data.serialize)" -ForegroundColor Cyan
}

# ── 3DGS Scan - 视频 ─────────────────────────────────────
function Submit-3DGSVideo {
    if (-not $Video) {
        Write-Host "❌ 必须指定 -video 参数" -ForegroundColor Red
        exit 1
    }
    $apiKey = Get-ApiKey
    $fields = @{
        'isMesh' = "$IsMesh"
        'isMask' = "$IsMask"
    }
    
    $response = Invoke-MultipartUpload -Url "$BaseUrl/3dgs/video" -ApiKey $apiKey `
        -Fields $fields -FileFieldName 'videoFile' -FilePaths @($Video)
    
    Write-Host "✅ 3DGS Scan 上传成功！" -ForegroundColor Green
    Write-Host "Serialize: $($response.data.serialize)" -ForegroundColor Cyan
    Write-Host "算法类型：3DGS (calculateType=$($response.data.calculateType))" -ForegroundColor Cyan
}

# ── 3DGS Scan - 图片集 ───────────────────────────────────
function Submit-3DGSImage {
    if (-not $Images) {
        Write-Host "❌ 必须指定 -images 参数" -ForegroundColor Red
        exit 1
    }
    
    $imageFiles = @()
    if (Test-Path $Images -PathType Container) {
        $imageFiles = @(Get-ChildItem $Images -Include *.jpg,*.jpeg,*.png,*.tif,*.tiff -File -Recurse)
    }
    else {
        $imageFiles = @(Get-ChildItem $Images -File)
    }
    
    if ($imageFiles.Count -lt 20 -or $imageFiles.Count -gt 300) {
        Write-Host "❌ 图片数量必须在 20~300 之间，当前 $($imageFiles.Count) 张" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "📸 准备上传 $($imageFiles.Count) 张图片..." -ForegroundColor Yellow
    $apiKey = Get-ApiKey
    $fields = @{
        'isMesh' = "$IsMesh"
        'isMask' = "$IsMask"
    }
    
    $response = Invoke-MultipartUpload -Url "$BaseUrl/3dgs/image" -ApiKey $apiKey `
        -Fields $fields -FileFieldName 'imagesFiles' -FilePaths ($imageFiles | ForEach-Object { $_.FullName })
    
    Write-Host "✅ 3DGS Scan 图片集上传成功！" -ForegroundColor Green
    Write-Host "Serialize: $($response.data.serialize)" -ForegroundColor Cyan
}

# ── 查询任务状态 ──────────────────────────────────────────
function Get-TaskStatus {
    if (-not $Serialize) {
        Write-Host "❌ 必须指定 -serialize 参数" -ForegroundColor Red
        exit 1
    }
    $apiKey = Get-ApiKey
    $response = Invoke-KiriGet -Url "$BaseUrl/model/getStatus?serialize=$Serialize" -ApiKey $apiKey
    
    if ($response.ok) {
        $status = $response.data.status
        $statusMap = @{
            0 = @{ Text = '排队中';  Color = 'Yellow' }
            1 = @{ Text = '处理中';  Color = 'Cyan'   }
            2 = @{ Text = '已完成';  Color = 'Green'  }
            3 = @{ Text = '失败';    Color = 'Red'    }
        }
        $info = if ($statusMap.ContainsKey($status)) { $statusMap[$status] } else { @{ Text = '未知'; Color = 'Gray' } }
        
        Write-Host "任务状态：$($info.Text)" -ForegroundColor $info.Color
        
        if ($status -eq 2) {
            Write-Host "`n✅ 已完成！下载命令：" -ForegroundColor Green
            Write-Host ".\kiri-engine.ps1 download -serialize `"$Serialize`" -output `"C:\output`"" -ForegroundColor White
        }
    }
    else {
        Write-Host "❌ 查询失败：$($response.msg)" -ForegroundColor Red
    }
}

# ── 下载模型 ──────────────────────────────────────────────
function Get-ModelDownload {
    if (-not $Serialize) {
        Write-Host "❌ 必须指定 -serialize 参数" -ForegroundColor Red
        exit 1
    }
    if (-not $Output) {
        $Output = Join-Path $env:USERPROFILE 'Downloads\KiriEngine'
        Write-Host "未指定输出目录，使用默认：$Output" -ForegroundColor Yellow
    }
    if (-not (Test-Path $Output)) {
        New-Item -ItemType Directory -Path $Output -Force | Out-Null
    }
    
    $apiKey = Get-ApiKey
    
    # 获取下载链接
    $response = Invoke-KiriGet -Url "$BaseUrl/model/getModelZip?serialize=$Serialize" -ApiKey $apiKey
    
    if (-not $response.ok -or -not $response.data.modelUrl) {
        Write-Host "❌ 获取下载链接失败：$($response.msg)" -ForegroundColor Red
        exit 1
    }
    
    $downloadUrl = $response.data.modelUrl
    $zipPath = Join-Path $Output "$Serialize.zip"
    
    Write-Host "正在下载..." -ForegroundColor Yellow
    
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath -UseBasicParsing -TimeoutSec 600
        Write-Host "✅ 下载完成" -ForegroundColor Green
        
        # 解压
        $extractPath = Join-Path $Output $Serialize
        Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
        Remove-Item $zipPath -Force
        
        Write-Host "✅ 解压完成！" -ForegroundColor Green
        Write-Host "模型位置：$extractPath" -ForegroundColor Cyan
        Write-Host "`n⚠️  链接 60 分钟失效，服务器保留 3 天后自动删除" -ForegroundColor Yellow
    }
    catch {
        Write-Host "❌ 下载失败：$_" -ForegroundColor Red
    }
}

# ── 主入口 ────────────────────────────────────────────────
switch ($Action) {
    'balance'             { Get-Balance }
    'photo-video'         { Submit-PhotoVideo }
    'photo-image'         { Submit-PhotoImage }
    'featureless-video'   { Submit-FeaturelessVideo }
    'featureless-image'   { Submit-FeaturelessImage }
    '3dgs-video'          { Submit-3DGSVideo }
    '3dgs-image'          { Submit-3DGSImage }
    'status'              { Get-TaskStatus }
    'download'            { Get-ModelDownload }
}
