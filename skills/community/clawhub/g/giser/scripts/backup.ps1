# @author 坤图_GIS | @fingerprint d24782d2025a
# GIS 知识库备份脚本
# 用法: .\backup.ps1 [备份目标目录]
# 默认备份到: $env:USERPROFILE\Documents\GIS_Backup\

param(
    [string]$BackupDir = "$env:USERPROFILE\Documents\GIS_Backup"
)

$SkillPath = "$env:USERPROFILE\.workbuddy\skills\GIS"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupName = "GIS_Skill_Backup_$Timestamp.zip"
$BackupFullPath = Join-Path $BackupDir $BackupName

Write-Host "==============================" -ForegroundColor Cyan
Write-Host "  GIS 知识库备份工具" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# 检查源目录
if (-not (Test-Path "$SkillPath\SKILL.md")) {
    Write-Host "❌ 错误：找不到 GIS 技能目录 ($SkillPath)" -ForegroundColor Red
    Write-Host "   请确认 .workbuddy\skills\GIS 目录存在"
    exit 1
}

# 创建备份目标目录
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null

# 获取知识库大小
$skillSize = (Get-ChildItem -Path $SkillPath -Recurse -File | Measure-Object -Property Length -Sum).Sum
$skillSizeMB = [math]::Round($skillSize / 1MB, 2)

Write-Host "知识库位置: $SkillPath" -ForegroundColor Yellow
Write-Host "知识库大小: $skillSizeMB MB" -ForegroundColor Yellow
Write-Host "备份目标:   $BackupFullPath" -ForegroundColor Yellow
Write-Host ""

# 执行压缩备份
try {
    Compress-Archive -Path "$SkillPath\*" -DestinationPath $BackupFullPath -Force
    $backupSize = (Get-Item $BackupFullPath).Length
    $backupSizeMB = [math]::Round($backupSize / 1MB, 2)
    
    Write-Host "✅ 备份成功！" -ForegroundColor Green
    Write-Host "   文件: $BackupName"
    Write-Host "   大小: $backupSizeMB MB"
    Write-Host "   路径: $BackupFullPath"
    Write-Host ""
    Write-Host "📋 备份内容包括：" -ForegroundColor Yellow
    Get-ChildItem -Path $SkillPath -Recurse -File | ForEach-Object {
        $relative = $_.FullName.Replace($SkillPath, "").TrimStart("\")
        Write-Host "   - $relative ($([math]::Round($_.Length/1KB, 1)) KB)"
    }
    Write-Host ""
    Write-Host "💾 建议将此备份文件复制到:" -ForegroundColor Cyan
    Write-Host "   - U盘或移动硬盘"
    Write-Host "   - 腾讯微云 / 百度网盘"
    Write-Host "   - 其他电脑的 $env:USERPROFILE\.workbuddy\skills\GIS\ 目录"
    Write-Host ""

    # 清理旧备份（保留最近5个）
    $oldBackups = Get-ChildItem -Path $BackupDir -Filter "GIS_Skill_Backup_*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -Skip 5
    if ($oldBackups.Count -gt 0) {
        Write-Host "🧹 清理旧备份（保留最近5个）:" -ForegroundColor DarkYellow
        $oldBackups | ForEach-Object {
            Remove-Item $_.FullName
            Write-Host "   已删除: $($_.Name)"
        }
    }
    
} catch {
    Write-Host "❌ 备份失败: $_" -ForegroundColor Red
    exit 1
}

Write-Host "==============================" -ForegroundColor Cyan
