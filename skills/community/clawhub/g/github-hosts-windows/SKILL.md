---
name: github-hosts-windows
description: Optimize GitHub access speed on Windows by finding the fastest IP addresses and updating the hosts file. Use when the user mentions GitHub is slow, accessing GitHub is sluggish, or wants to update hosts file for GitHub. Triggers on: "GitHub很慢", "github访问慢", "更新github hosts", "优化github速度", "hosts文件".
---

# GitHub Hosts Optimizer

On Windows, directly modify `C:\Windows\System32\drivers\etc\hosts` to map GitHub domains to faster IPs.

## Workflow

1. **Resolve GitHub IPs** using `nslookup`:
   - github.com
   - api.github.com
   - objects.githubusercontent.com

2. **Ping each IP** to measure latency (ping -n 3 <IP>)

3. **Select fastest IP** (lowest average latency)

4. **Update hosts file** with entries:
   ```
   <fastest_ip> github.com
   <fastest_ip> api.github.com
   <fastest_ip> github.com  (duplicate for reliability)
   ```

5. **Flush DNS cache**:
   ```
   ipconfig /flushdns
   ```

## PowerShell Script

```powershell
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$domains = @("github.com", "api.github.com", "objects.githubusercontent.com")

# Resolve IPs
$ips = @{}
foreach ($domain in $domains) {
    $result = nslookup $domain 2>$null
    $ips[$domain] = ($result | Select-String -Pattern "Addresses:" -Context 0,10 | ForEach-Object { $_.Context.PostContext }) -replace '\s+', '' | Where-Object { $_ -match '^\d+\.\d+\.\d+\.\d+$' }
}

# Ping each IP and find fastest
$results = @()
foreach ($ip in ($ips.Values | Select-Object -Unique)) {
    $avg = (ping -n 3 $ip | Select-String -Pattern "平均").ToString() -replace '.*= (\d+)ms.*', '$1'
    if ($avg) { $results += [PSCustomObject]@{ IP = $ip; Avg = [int]$avg } }
}
$fastest = ($results | Sort-Object Avg | Select-Object -First 1).IP

# Update hosts
$entry = "$fastest github.com`n$fastest api.github.com"
$current = Get-Content $hostsPath -Raw -ErrorAction SilentlyContinue
if ($current -notmatch "github\.com") {
    Add-Content -Path $hostsPath -Value $entry
} else {
    $updated = $current -replace "[\d\.]+\s+github\.com`n?[\d\.]+\s+api\.github\.com", $entry
    Set-Content -Path $hostsPath -Value $updated
}

# Flush DNS
ipconfig /flushdns | Out-Null
Write-Host "Done! Fastest IP: $fastest"
```

## Key Notes

- Hosts file requires **Administrator privileges** to modify
- If direct edit fails, output the entry and instruct user to manually add it
- The fastest IP may change over time; re-run when GitHub access slows again
