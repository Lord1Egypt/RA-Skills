# 编译脚本（使用相对路径）
# 需要：JAVA_HOME 环境变量指向 JDK 25+，Maven 在 PATH 中
Set-Location $PSScriptRoot
mvn compile -q
Write-Host "COMPILE=$LASTEXITCODE"
