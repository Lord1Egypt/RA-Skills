const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const VERSION = '1.0.0';


// Parse CLI args
const args = process.argv.slice(2);
const isQuick = args.includes('--quick');
const isSilent = args.includes('--silent');
const isVersion = args.includes('--version') || args.includes('-v');
const saveIndex = args.indexOf('--save');
const savePath = saveIndex >= 0 ? args[saveIndex + 1] : null;
const outputMode = args.includes('--report') ? 'report' : args.includes('--json') ? 'json' : 'json';


if (isVersion) { console.log(`pc-health-check ${VERSION}`); process.exit(0); }

// Run a PowerShell command and return trimmed output (UTF-8 encoded)
function ps(cmd) {
  try {
    const result = execSync(`powershell -NoProfile -Command "[Console]::OutputEncoding = [Text.Encoding]::UTF8; ${cmd.replace(/"/g, '\\"')}"`, {
      encoding: 'utf8',
      timeout: 30000,
      windowsHide: true
    });
    return result.trim();
  } catch (e) {
    return null;
  }
}

// Run PowerShell and return parsed JSON
function psJson(cmd) {
  const raw = ps(cmd + ' | ConvertTo-Json -Compress');
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

// Parse PowerShell /Date(...)/ format to ISO string
function parsePsDate(psDate) {
  if (!psDate) return null;
  if (typeof psDate === 'string' && psDate.startsWith('/Date(')) {
    const match = psDate.match(/\/Date\((\d+)\)/);
    if (match) {
      return new Date(parseInt(match[1])).toISOString();
    }
  }
  if (psDate.DateTime) return parsePsDate(psDate.DateTime);
  if (psDate.value) return parsePsDate(psDate.value);
  return psDate;
}

function formatBytes(bytes) {
  if (!bytes || bytes <= 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + units[i];
}

function formatBits(bits) {
  if (bits >= 1e9) return (bits / 1e9).toFixed(1) + ' Gbps';
  if (bits >= 1e6) return (bits / 1e6).toFixed(1) + ' Mbps';
  return bits + ' bps';
}

function formatDuration(ms) {
  const days = Math.floor(ms / 86400000);
  const hours = Math.floor((ms % 86400000) / 3600000);
  const mins = Math.floor((ms % 3600000) / 60000);
  return `${days}d ${hours}h ${mins}m`;
}

// === CHECK FUNCTIONS ===

function checkOS() {
  const data = psJson(`Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture, LastBootUpTime`);
  if (!data) return { status: 'error', message: 'Cannot retrieve OS info' };
  let uptimeStr = 'unknown';
  try {
    const bootTick = ps(`(Get-CimInstance Win32_OperatingSystem).LastBootUpTime | Get-Date -Format o`);
    if (bootTick) {
      const bootTime = new Date(bootTick);
      const diff = Date.now() - bootTime.getTime();
      if (diff > 0) uptimeStr = formatDuration(diff);
    }
  } catch {}
  return {
    status: 'ok',
    data: {
      name: data.Caption,
      arch: data.OSArchitecture,
      version: `${data.Version} (Build ${data.BuildNumber})`,
      uptime: uptimeStr
    }
  };
}

function checkCPU() {
  const data = psJson(`Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, LoadPercentage, MaxClockSpeed`);
  if (!data) return { status: 'error', message: 'Cannot retrieve CPU info' };
  const load = data.LoadPercentage || 0;
  return {
    status: load > 90 ? 'error' : load > 70 ? 'warn' : 'ok',
    data: {
      name: data.Name,
      cores: data.NumberOfCores,
      threads: data.NumberOfLogicalProcessors,
      load: load,
      maxSpeed: data.MaxClockSpeed
    }
  };
}

function checkMemory() {
  const data = psJson(`Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory`);
  if (!data) return { status: 'error', message: 'Cannot retrieve memory info' };
  const total = data.TotalVisibleMemorySize * 1024;
  const free = data.FreePhysicalMemory * 1024;
  const used = total - free;
  const usagePercent = Math.round(used / total * 100);
  return {
    status: usagePercent > 90 ? 'error' : usagePercent > 80 ? 'warn' : 'ok',
    data: {
      totalGB: Math.round(total / 1e9 * 10) / 10,
      usedGB: Math.round(used / 1e9 * 10) / 10,
      freeGB: Math.round(free / 1e9 * 10) / 10,
      usagePercent: usagePercent
    }
  };
}

function checkDisk() {
  const data = psJson(`Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Select-Object DeviceID, VolumeName, Size, FreeSpace, FileSystem`);
  if (!data) return { status: 'error', message: 'Cannot retrieve disk info' };
  const disks = Array.isArray(data) ? data : [data];
  const results = disks.map(d => {
    const total = d.Size || 0;
    const free = d.FreeSpace || 0;
    const used = total - free;
    const usagePercent = total > 0 ? Math.round(used / total * 100) : 0;
    return {
      drive: d.DeviceID,
      label: d.VolumeName || '',
      totalGB: Math.round(total / 1e9 * 10) / 10,
      freeGB: Math.round(free / 1e9 * 10) / 10,
      usagePercent: usagePercent,
      fs: d.FileSystem || ''
    };
  });
  const hasCritical = results.some(d => d.usagePercent > 90);
  const hasWarning = results.some(d => d.usagePercent > 80);
  return {
    status: hasCritical ? 'error' : hasWarning ? 'warn' : 'ok',
    data: results
  };
}

function checkNetwork() {
  const adapters = psJson(`Get-CimInstance Win32_NetworkAdapter -Filter "NetConnectionStatus=2" | Select-Object Name, Speed, MACAddress`);
  const dns = ps(`Get-DnsClientServerAddress -AddressFamily IPv4 | Select-Object -First 5 | Format-Table -HideTableHeaders`);
  const ping = ps(`Test-Connection -ComputerName 8.8.8.8 -Count 1 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty ResponseTime`);
  return {
    status: 'ok',
    data: {
      adapters: Array.isArray(adapters) ? adapters.map(a => ({ name: a.Name, speed: a.Speed ? formatBits(a.Speed) : 'unknown' })) : adapters ? [{ name: adapters.Name, speed: adapters.Speed ? formatBits(adapters.Speed) : 'unknown' }] : [],
      internetPing: ping ? parseInt(ping) : null,
      dnsConfigured: !!dns
    }
  };
}

function checkTopProcesses() {
  const cpuProcs = psJson(`Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, Id, CPU, @{N='MemMB';E={[math]::Round($_.WorkingSet64/1MB,1)}}`);
  const memProcs = psJson(`Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name, Id, @{N='MemMB';E={[math]::Round($_.WorkingSet64/1MB,1)}}, CPU`);
  return {
    status: 'ok',
    data: {
      topCPU: Array.isArray(cpuProcs) ? cpuProcs : cpuProcs ? [cpuProcs] : [],
      topMem: Array.isArray(memProcs) ? memProcs : memProcs ? [memProcs] : []
    }
  };
}

function checkDevices() {
  const data = psJson(`Get-CimInstance Win32_PnPEntity | Where-Object { $_.Status -ne 'OK' } | Select-Object Name, Status, ConfigManagerErrorCode | Sort-Object Status`);
  if (!data) return { status: 'ok', data: { errorDevices: [] } };
  const devices = Array.isArray(data) ? data : [data];
  const errorDevices = devices.filter(d => d.Status === 'Error');
  return {
    status: errorDevices.length > 0 ? 'error' : devices.length > 0 ? 'warn' : 'ok',
    data: {
      errorDevices: errorDevices.map(d => ({ name: d.Name, status: d.Status, errorCode: d.ConfigManagerErrorCode })),
      warningDevices: devices.filter(d => d.Status !== 'Error').map(d => ({ name: d.Name, status: d.Status }))
    }
  };
}

function checkSystemEvents() {
  const data = psJson(`Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddHours(-24)} -MaxEvents 20 -ErrorAction SilentlyContinue | Select-Object TimeCreated, Id, LevelDisplayName, Message`);
  if (!data) return { status: 'ok', data: { events: [] } };
  const events = Array.isArray(data) ? data : [data];
  return {
    status: events.length > 5 ? 'error' : events.length > 0 ? 'warn' : 'ok',
    data: {
      count: events.length,
      events: events.map(e => ({
        time: parsePsDate(e.TimeCreated),
        id: e.Id,
        level: e.LevelDisplayName,
        message: (e.Message || '').substring(0, 150).replace(/\r\n/g, ' ')
      }))
    }
  };
}

function checkStartup() {
  const data = psJson(`Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location`);
  if (!data) return { status: 'ok', data: { items: [] } };
  const items = Array.isArray(data) ? data : [data];
  return {
    status: 'ok',
    data: {
      count: items.length,
      items: items.map(i => ({ name: i.Name, command: (i.Command || '').substring(0, 100), location: i.Location }))
    }
  };
}

function checkListeningPorts() {
  const data = psJson(`Get-NetTCPConnection -State Listen | Select-Object LocalAddress, LocalPort, OwningProcess | Sort-Object LocalPort`);
  if (!data) return { status: 'ok', data: { ports: [] } };
  const conns = Array.isArray(data) ? data : [data];
  
  // Get process names for PIDs
  const pidMap = {};
  try {
    const procs = psJson(`Get-Process | Select-Object Id, ProcessName`);
    if (procs) {
      (Array.isArray(procs) ? procs : [procs]).forEach(p => { pidMap[p.Id] = p.ProcessName; });
    }
  } catch {}
  
  const highRisk = [23, 445, 3389, 5800, 5900];
  const ports = conns.map(c => ({
    address: c.LocalAddress,
    port: c.LocalPort,
    pid: c.OwningProcess,
    process: pidMap[c.OwningProcess] || 'unknown',
    risk: highRisk.includes(c.LocalPort) ? 'high' : c.LocalPort < 1024 ? 'medium' : 'low'
  }));
  const hasHighRisk = ports.some(p => p.risk === 'high');
  return {
    status: hasHighRisk ? 'warn' : 'ok',
    data: { count: ports.length, ports: ports.slice(0, 30) }
  };
}

function checkSecurityUpdates() {
  const data = psJson(`Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10 HotFixID, Description, InstalledOn`);
  if (!data) return { status: 'ok', data: { recentUpdates: [] } };
  const updates = Array.isArray(data) ? data : [data];
  return {
    status: 'ok',
    data: {
      recentUpdates: updates.map(u => ({
        id: u.HotFixID,
        description: (u.Description || '').substring(0, 60),
        installed: parsePsDate(u.InstalledOn)
      }))
    }
  };
}

// === REPORT GENERATOR ===

function generateMarkdownReport(report) {
  const r = report.results;
  const now = new Date(report.timestamp).toLocaleString('zh-CN');
  
  const icon = report.overall === 'good' ? '✅' : report.overall === 'attention' ? '⚠️' : '🔴';
  const statusText = report.overall === 'good' ? '良好' : report.overall === 'attention' ? '注意' : '警告';
  
  let md = `# PC健康体检报告\n\n**检查时间**：${now}\n\n## ${icon} 总评：${statusText}\n\n| 检查项 | 正常 | 警告 | 错误 |\n|--------|------|------|------|\n| 总计 | ${report.summary.ok} | ${report.summary.warnings} | ${report.summary.errors} |\n\n`;
  
  // System Overview
  md += `## 系统概况\n\n`;
  if (r.OS?.status === 'ok') {
    md += `- **操作系统**：${r.OS.data.name} ${r.OS.data.arch}\n`;
    md += `- **版本**：${r.OS.data.version}\n`;
    md += `- **运行时间**：${r.OS.data.uptime}\n\n`;
  }
  
  if (r.CPU?.status === 'ok') {
    const cpuIcon = r.CPU.status === 'error' ? '🔴' : r.CPU.status === 'warn' ? '⚠️' : '✅';
    md += `### ${cpuIcon} CPU\n- ${r.CPU.data.name}\n- ${r.CPU.data.cores}核/${r.CPU.data.threads}线程 | 负载 ${r.CPU.data.load}%\n\n`;
  }
  
  if (r.Memory?.status === 'ok') {
    const memIcon = r.Memory.status === 'error' ? '🔴' : r.Memory.status === 'warn' ? '⚠️' : '✅';
    md += `### ${memIcon} 内存\n- 总计：${r.Memory.data.totalGB} GB\n- 已用：${r.Memory.data.usedGB} GB (${r.Memory.data.usagePercent}%)\n- 可用：${r.Memory.data.freeGB} GB\n\n`;
  }
  
  if (r.Disk?.status === 'ok') {
    const diskIcon = r.Disk.status === 'error' ? '🔴' : r.Disk.status === 'warn' ? '⚠️' : '✅';
    md += `### ${diskIcon} 磁盘\n| 分区 | 总容量 | 已用 | 剩余 | 使用率 |\n|------|--------|------|------|--------|\n`;
    r.Disk.data.forEach(d => {
      const icon = d.usagePercent > 90 ? '🔴' : d.usagePercent > 80 ? '⚠️' : '✅';
      md += `| ${icon} ${d.drive} | ${d.totalGB}GB | ${(d.totalGB - d.freeGB).toFixed(1)}GB | ${d.freeGB}GB | ${d.usagePercent}% |\n`;
    });
    md += '\n';
  }
  
  // Issues Section
  const issues = [];
  if (r.Devices?.status === 'error' && r.Devices.data.errorDevices.length > 0) {
    issues.push({ title: '设备异常', icon: '🔴', items: r.Devices.data.errorDevices.map(d => `${d.name} (错误码: ${d.errorCode})`) });
  }
  if (r.Devices?.status !== 'error' && r.Devices?.data?.warningDevices?.length > 0) {
    issues.push({ title: '设备警告', icon: '⚠️', items: r.Devices.data.warningDevices.map(d => `${d.name} (${d.status})`) });
  }
  if (r.SystemEvents?.status !== 'ok' && r.SystemEvents?.data?.count > 0) {
    const evIcon = r.SystemEvents.status === 'error' ? '🔴' : '⚠️';
    issues.push({ title: '系统事件', icon: evIcon, items: r.SystemEvents.data.events.slice(0, 5).map(e => `[${e.level}] ${e.message.substring(0, 80)}${e.message.length > 80 ? '...' : ''}`) });
  }
  if (r.ListeningPorts?.status === 'warn') {
    const highRiskPorts = r.ListeningPorts.data.ports.filter(p => p.risk === 'high');
    if (highRiskPorts.length > 0) {
      issues.push({ title: '高危端口', icon: '⚠️', items: highRiskPorts.map(p => `端口 ${p.port} (${p.process})`) });
    }
  }
  
  if (issues.length > 0) {
    md += `## 需要关注的问题\n\n`;
    issues.forEach(issue => {
      md += `### ${issue.icon} ${issue.title}\n`;
      issue.items.forEach(item => md += `- ${item}\n`);
      md += '\n';
    });
  }
  
  md += `---\n*由 PC Health Check Skill 生成*`;
  return md;
}

// === MAIN ===

function runHealthCheck() {
  const quickChecks = [
    { name: 'OS', fn: checkOS },
    { name: 'CPU', fn: checkCPU },
    { name: 'Memory', fn: checkMemory },
    { name: 'Disk', fn: checkDisk },
    { name: 'Network', fn: checkNetwork }
  ];
  
  const fullChecks = [
    ...quickChecks,
    { name: 'TopProcesses', fn: checkTopProcesses },
    { name: 'Devices', fn: checkDevices },
    { name: 'SystemEvents', fn: checkSystemEvents },
    { name: 'Startup', fn: checkStartup },
    { name: 'ListeningPorts', fn: checkListeningPorts },
    { name: 'SecurityUpdates', fn: checkSecurityUpdates }
  ];
  
  const checks = isQuick ? quickChecks : fullChecks;
  const results = {};
  let errorCount = 0;
  let warnCount = 0;

  for (const check of checks) {
    try {
      const result = check.fn();
      results[check.name] = result;
      if (result.status === 'error') errorCount++;
      if (result.status === 'warn') warnCount++;
    } catch (e) {
      results[check.name] = { status: 'error', message: e.message };
      errorCount++;
    }
  }

  const overall = errorCount > 0 ? 'warning' : warnCount > 0 ? 'attention' : 'good';

  return {
    timestamp: new Date().toISOString(),
    overall,
    mode: isQuick ? 'quick' : 'full',
    summary: {
      totalChecks: checks.length,
      ok: checks.length - errorCount - warnCount,
      warnings: warnCount,
      errors: errorCount
    },
    results
  };
}

// Run and output
const report = runHealthCheck();

let outputText;
if (outputMode === 'report') {
  outputText = generateMarkdownReport(report);
} else {
  outputText = JSON.stringify(report, null, 2);
}

if (!isSilent) {
  console.log(outputText);
}

if (savePath) {
  try {
    const absPath = path.resolve(savePath);
    fs.writeFileSync(absPath, outputText, 'utf8');
    if (!isSilent) console.log(`\n[已保存: ${absPath}]`);
  } catch (e) {
    if (!isSilent) console.error(`[保存失败: ${e.message}]`);
  }
}
