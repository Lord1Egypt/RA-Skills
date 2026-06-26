import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { buildLaunchdCalendarParts, formatIsoLocal, formatSystemdExactCalendar } from "./calendar.js";

function exists(filePath) {
  try {
    fs.accessSync(filePath, fs.constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

function ensureDirectory(directory) {
  fs.mkdirSync(directory, { recursive: true });
}

function sanitizeId(id) {
  return String(id).replace(/[^A-Za-z0-9_.-]/g, "-");
}

function escapeXml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

function shellEscape(value) {
  if (!/[^\w@%+=:,./-]/.test(value)) return value;
  return `"${String(value).replace(/(["\\$`])/g, "\\$1")}"`;
}

function systemdEscape(value) {
  const string = String(value);
  if (!/[\s"\\]/.test(string)) return string;
  return `"${string.replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"`;
}

function execBestEffort(command, args) {
  try {
    execFileSync(command, args, { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

function detectGuiDomain() {
  return typeof process.getuid === "function" ? `gui/${process.getuid()}` : "gui/501";
}

export function detectSchedulerBackend() {
  const override = process.env.POKE_SCHEDULER_BACKEND?.trim().toLowerCase();
  if (override) return override;
  if (process.platform === "darwin") return "launchd";
  if (process.platform === "win32") return "schtasks";
  return "systemd";
}

function systemdUserDir() {
  const base = process.env.XDG_CONFIG_HOME || path.join(os.homedir(), ".config");
  return path.join(base, "systemd", "user");
}

function schedulerHandle(stateDir, id, backend) {
  const safeId = sanitizeId(id);
  switch (backend) {
    case "mock":
      return {
        backend,
        filePath: path.join(stateDir, ".mock-scheduler", `${safeId}.json`)
      };
    case "launchd":
      return {
        backend,
        label: `ai.openclaw.poke.${safeId}`,
        plistPath: path.join(os.homedir(), "Library", "LaunchAgents", `ai.openclaw.poke.${safeId}.plist`)
      };
    case "schtasks":
      return {
        backend,
        taskName: `OpenClaw Text Reminder ${safeId}`,
        xmlPath: path.join(stateDir, `${safeId}.schtasks.xml`)
      };
    case "systemd":
    default:
      return {
        backend: "systemd",
        unitName: `poke-${safeId}`,
        servicePath: path.join(systemdUserDir(), `poke-${safeId}.service`),
        timerPath: path.join(systemdUserDir(), `poke-${safeId}.timer`)
      };
  }
}

function buildSystemdService(handle, scriptPath, reminderId, envPairs) {
  const environmentLines = Object.entries(envPairs)
    .filter(([, value]) => value)
    .map(([key, value]) => `Environment=${systemdEscape(`${key}=${value}`)}`);
  const unitBase = handle.unitName;
  const deliverCmd = [process.execPath, scriptPath, "--deliver", reminderId].map(systemdEscape).join(" ");
  const cleanupCmd = `systemctl --user disable --now ${shellEscape(`${unitBase}.timer`)} 2>/dev/null; rm -f ${shellEscape(handle.servicePath)} ${shellEscape(handle.timerPath)}; systemctl --user daemon-reload`;
  return [
    "[Unit]",
    `Description=Text reminder: ${reminderId}`,
    "After=network-online.target",
    "",
    "[Service]",
    "Type=oneshot",
    "TimeoutStartSec=555",
    `ExecStart=/bin/sh -c ${systemdEscape(`${deliverCmd}; ${cleanupCmd}`)}`,
    ...environmentLines,
    "",
    "[Install]",
    "WantedBy=default.target",
    ""
  ].join("\n");
}

function buildSystemdTimer(handle, dueAt, catchupMode) {
  const persistent = catchupMode !== "none" ? "Persistent=true" : "";
  return [
    "[Unit]",
    `Description=Text reminder timer: ${handle.unitName}`,
    "",
    "[Timer]",
    `OnCalendar=${formatSystemdExactCalendar(dueAt)}`,
    persistent,
    "AccuracySec=1s",
    "",
    "[Install]",
    "WantedBy=timers.target",
    ""
  ]
    .filter(Boolean)
    .join("\n");
}

function buildLaunchdPlist(handle, dueAt, scriptPath, reminderId, stateDir, envPairs) {
  const interval = buildLaunchdCalendarParts(dueAt);
  const envXml = Object.entries(envPairs)
    .filter(([, value]) => value)
    .map(([key, value]) => `    <key>${escapeXml(key)}</key>\n    <string>${escapeXml(value)}</string>`)
    .join("\n");
  const args = [process.execPath, scriptPath, "--deliver", reminderId]
    .map((arg) => `      <string>${escapeXml(arg)}</string>`)
    .join("\n");
  const logDir = path.join(stateDir, "logs");
  ensureDirectory(logDir);
  return `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>${escapeXml(handle.label)}</string>
    <key>ProgramArguments</key>
    <array>
${args}
    </array>
    <key>StartCalendarInterval</key>
    <dict>
      <key>Month</key>
      <integer>${interval.Month}</integer>
      <key>Day</key>
      <integer>${interval.Day}</integer>
      <key>Hour</key>
      <integer>${interval.Hour}</integer>
      <key>Minute</key>
      <integer>${interval.Minute}</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>${escapeXml(path.join(logDir, `${sanitizeId(reminderId)}.launchd.log`))}</string>
    <key>StandardErrorPath</key>
    <string>${escapeXml(path.join(logDir, `${sanitizeId(reminderId)}.launchd.err.log`))}</string>
    <key>EnvironmentVariables</key>
    <dict>
${envXml}
    </dict>
  </dict>
</plist>
`;
}

function buildWindowsTaskXml(handle, dueAt, scriptPath, reminderId, envPairs) {
  const envCommand = Object.entries(envPairs)
    .filter(([, value]) => value)
    .map(([key, value]) => `set "${key}=${String(value).replace(/"/g, '""')}"`)
    .join(" && ");
  const command = `${envCommand ? `${envCommand} && ` : ""}${shellEscape(process.execPath)} ${shellEscape(
    scriptPath
  )} --deliver ${shellEscape(reminderId)}`;
  const cwd = path.dirname(scriptPath);
  return `<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>${escapeXml(handle.taskName)}</Description>
  </RegistrationInfo>
  <Triggers>
    <TimeTrigger>
      <StartBoundary>${escapeXml(formatIsoLocal(dueAt))}</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT10M</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>cmd.exe</Command>
      <Arguments>/d /s /c "${escapeXml(command)}"</Arguments>
      <WorkingDirectory>${escapeXml(cwd)}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
`;
}

function upsertMock(handle, dueAt, scriptPath, reminderId, envPairs, catchupMode) {
  ensureDirectory(path.dirname(handle.filePath));
  fs.writeFileSync(
    handle.filePath,
    JSON.stringify(
      {
        backend: "mock",
        dueAt: dueAt.toISOString(),
        scriptPath,
        reminderId,
        catchupMode,
        envPairs
      },
      null,
      2
    )
  );
}

function removeMock(handle) {
  if (exists(handle.filePath)) fs.unlinkSync(handle.filePath);
}

function upsertSystemd(handle, dueAt, scriptPath, reminderId, envPairs, catchupMode) {
  ensureDirectory(path.dirname(handle.servicePath));
  fs.writeFileSync(handle.servicePath, buildSystemdService(handle, scriptPath, reminderId, envPairs));
  fs.writeFileSync(handle.timerPath, buildSystemdTimer(handle, dueAt, catchupMode));
  execFileSync("systemctl", ["--user", "daemon-reload"], { stdio: "ignore" });
  execBestEffort("systemctl", ["--user", "disable", `${handle.unitName}.timer`]);
  execFileSync("systemctl", ["--user", "enable", `${handle.unitName}.timer`], { stdio: "ignore" });
  execFileSync("systemctl", ["--user", "restart", `${handle.unitName}.timer`], { stdio: "ignore" });
}

function removeSystemd(handle) {
  execBestEffort("systemctl", ["--user", "stop", `${handle.unitName}.timer`]);
  execBestEffort("systemctl", ["--user", "disable", `${handle.unitName}.timer`]);
  if (exists(handle.servicePath)) fs.unlinkSync(handle.servicePath);
  if (exists(handle.timerPath)) fs.unlinkSync(handle.timerPath);
  execBestEffort("systemctl", ["--user", "daemon-reload"]);
}

function upsertLaunchd(handle, dueAt, scriptPath, reminderId, envPairs, stateDir) {
  ensureDirectory(path.dirname(handle.plistPath));
  fs.writeFileSync(handle.plistPath, buildLaunchdPlist(handle, dueAt, scriptPath, reminderId, stateDir, envPairs));
  const domain = detectGuiDomain();
  execBestEffort("launchctl", ["bootout", `${domain}/${handle.label}`]);
  execBestEffort("launchctl", ["bootout", domain, handle.plistPath]);
  execFileSync("launchctl", ["bootstrap", domain, handle.plistPath], { stdio: "ignore" });
  execBestEffort("launchctl", ["enable", `${domain}/${handle.label}`]);
}

function removeLaunchd(handle) {
  const domain = detectGuiDomain();
  execBestEffort("launchctl", ["bootout", `${domain}/${handle.label}`]);
  execBestEffort("launchctl", ["bootout", domain, handle.plistPath]);
  if (exists(handle.plistPath)) fs.unlinkSync(handle.plistPath);
}

function upsertSchtasks(handle, dueAt, scriptPath, reminderId, envPairs) {
  const xml = buildWindowsTaskXml(handle, dueAt, scriptPath, reminderId, envPairs);
  fs.writeFileSync(handle.xmlPath, `\ufeff${xml}`, "utf16le");
  execFileSync("schtasks", ["/Create", "/TN", handle.taskName, "/XML", handle.xmlPath, "/F"], { stdio: "ignore" });
}

function removeSchtasks(handle) {
  execBestEffort("schtasks", ["/Delete", "/TN", handle.taskName, "/F"]);
  if (exists(handle.xmlPath)) fs.unlinkSync(handle.xmlPath);
}

export function upsertSchedulerWake({ backend, stateDir, reminderId, dueAt, scriptPath, catchupMode = "coalesce" }) {
  const resolvedBackend = backend || detectSchedulerBackend();
  const handle = schedulerHandle(stateDir, reminderId, resolvedBackend);
  const envPairs = {
    POKE_STATE_DIR: stateDir,
    OPENCLAW_STATE_DIR: process.env.OPENCLAW_STATE_DIR || "",
    OPENCLAW_CONFIG_PATH: process.env.OPENCLAW_CONFIG_PATH || ""
  };
  switch (resolvedBackend) {
    case "mock":
      upsertMock(handle, dueAt, scriptPath, reminderId, envPairs, catchupMode);
      break;
    case "launchd":
      upsertLaunchd(handle, dueAt, scriptPath, reminderId, envPairs, stateDir);
      break;
    case "schtasks":
      upsertSchtasks(handle, dueAt, scriptPath, reminderId, envPairs);
      break;
    case "systemd":
    default:
      upsertSystemd(handle, dueAt, scriptPath, reminderId, envPairs, catchupMode);
      break;
  }
  return handle;
}

export function removeSchedulerWake({ backend, stateDir, reminderId, schedulerHandle: existingHandle }) {
  const resolvedBackend = backend || existingHandle?.backend || detectSchedulerBackend();
  const handle = existingHandle || schedulerHandle(stateDir, reminderId, resolvedBackend);
  switch (resolvedBackend) {
    case "mock":
      removeMock(handle);
      break;
    case "launchd":
      removeLaunchd(handle);
      break;
    case "schtasks":
      removeSchtasks(handle);
      break;
    case "systemd":
    default:
      removeSystemd(handle);
      break;
  }
}

export function schedulerIsActive({ backend, stateDir, reminderId, schedulerHandle: existingHandle }) {
  const resolvedBackend = backend || existingHandle?.backend || detectSchedulerBackend();
  const handle = existingHandle || schedulerHandle(stateDir, reminderId, resolvedBackend);
  try {
    switch (resolvedBackend) {
      case "mock":
        return exists(handle.filePath);
      case "launchd":
        execFileSync("launchctl", ["print", `${detectGuiDomain()}/${handle.label}`], { stdio: "ignore" });
        return true;
      case "schtasks":
        execFileSync("schtasks", ["/Query", "/TN", handle.taskName], { stdio: "ignore" });
        return true;
      case "systemd":
      default:
        execFileSync("systemctl", ["--user", "is-active", `${handle.unitName}.timer`], { stdio: "ignore" });
        return true;
    }
  } catch {
    return false;
  }
}

export { buildLaunchdPlist, buildSystemdService, buildSystemdTimer, buildWindowsTaskXml };
