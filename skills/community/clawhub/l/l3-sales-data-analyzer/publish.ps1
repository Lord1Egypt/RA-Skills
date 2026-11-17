# Publish data_analyzer skill to OpenClaw ClawHub
# Prerequisites: npm install -g clawhub && clawhub login

$ErrorActionPreference = "Stop"
$SkillDir = $PSScriptRoot

Write-Host "Checking ClawHub login..."
clawhub whoami

Write-Host "`nDry-run..."
clawhub skill publish $SkillDir `
    --slug l3-sales-data-analyzer `
    --name "L3 Sales Data Analyzer" `
    --version 1.0.0 `
    --changelog "Initial release: sales query, chart generation and trend analysis" `
    --dry-run

Write-Host "`nPublishing..."
clawhub skill publish $SkillDir `
    --slug l3-sales-data-analyzer `
    --name "L3 Sales Data Analyzer" `
    --version 1.0.0 `
    --changelog "Initial release: sales query, chart generation and trend analysis"

Write-Host "`nDone. Inspect:"
Write-Host "  clawhub inspect l3-sales-data-analyzer"
