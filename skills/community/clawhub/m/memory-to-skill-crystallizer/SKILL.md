---
name: memory-to-skill-crystallizer
description: Convert memory lessons into reusable skills automatically. Extract patterns from memory/YYYY-MM-DD.md and create skills/local/ entries.
---

# Memory to Skill Crystallizer

Convert memory lessons into reusable skills.

## Problem

Lessons learned:
- Stay in memory files only
- Aren't reusable across sessions
- Require manual extraction
- Get lost in daily logs

## Workflow

### 1. Pattern Detection

```powershell
# Scan recent memory for repeated patterns
$memoryFiles = Get-ChildItem "memory/" -Filter "*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 7
$patterns = @{}

foreach ($file in $memoryFiles) {
    $content = Get-Content $file.FullName -Raw
    if ($content -match "Failed|Blocker|Error") {
        # Extract pattern
        $matches = [regex]::Matches($content, "(Failed|Blocker|Error): (.+)")
        foreach ($m in $matches) {
            $key = $m.Groups[2].Value
            $patterns[$key] = $patterns[$key] + 1
        }
    }
}

# Find repeated patterns (2+ occurrences)
$repeated = $patterns.GetEnumerator() | Where-Object { $_.Value -ge 2 }
```

### 2. Skill Generation

```powershell
foreach ($pattern in $repeated) {
    $skillName = $pattern.Key -replace '[^a-z]', '-' -replace '-+', '-'
    $skillPath = "skills/local/$skillName-recovery"
    
    New-Item -ItemType Directory -Path $skillPath -Force | Out-Null
    
    $skillContent = @"
---
name: $skillName-recovery
description: Auto-recovery for: $($pattern.Key)
---

# $($pattern.Key) Recovery

## Trigger
When $($pattern.Key) occurs

## Steps
1. Detect the error pattern
2. Execute recovery steps
3. Verify resolution

## Verification
- [ ] Error resolved
- [ ] Task can continue
"@
    
    $skillContent | Out-File "$skillPath/SKILL.md" -Encoding UTF8
}
```

### 3. Registration

```powershell
# Add to skills index if in bot-output
if (Test-Path "skills/local/") {
    Write-Host "Created skills in skills/local/"
    Get-ChildItem "skills/local/" -Directory | ForEach-Object {
        Write-Host "  - $($_.Name)"
    }
}
```

## Executable Completion Criteria

| Criteria | Verification |
|----------|-------------|
| Pattern detected | 2+ occurrences in memory |
| Skill file created | SKILL.md exists in skills/local/ |
| Trigger defined | ## Trigger section present |
| Steps documented | ## Steps section present |

## Privacy/Safety

- No sensitive data in extracted patterns
- Pattern names only, no specific content
- Local skills only (not published)

## Self-Use Trigger

Use when:
- Same error appears 2+ times
- Weekly review of memory files
- Before creating permanent fix

---

**Crystallize lessons. Reuse forever.**
