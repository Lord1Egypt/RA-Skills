#!/usr/bin/env node
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");

const VERSION = "1.0.0";
const ORDER_URL = "https://www.m78armor.com/order.html";
const DISPLAY_NAME = "m78armor : openclaw security configuration check";

const CHECKS = {
  "CFG-01": {
    name_cn: "网关绑定地址",
    name_en: "Gateway Bind Address",
    path: "gateway.bind",
    expected_cn: "127.0.0.1",
    expected_en: "127.0.0.1",
    action_cn: "将绑定地址收紧到 127.0.0.1 或你已验证的最小监听范围。",
    action_en: "Tighten the bind address to 127.0.0.1 or the smallest verified listening scope.",
    abuse_cn: "如果实例监听范围超出预期，攻击者或同网段的未授权用户可以从你没有预期暴露的网络路径接触到 OpenClaw。",
    abuse_en: "If the instance listens more broadly than intended, an attacker or an unauthorized user on the same network can reach OpenClaw from paths you did not intend to expose.",
    why_cn: "更广的监听范围会扩大暴露面，并让后续配置错误更容易变成实际可达的入口。",
    why_en: "A broader listening scope increases exposure and makes later configuration mistakes more likely to become reachable entry points."
  },
  "CFG-02": {
    name_cn: "网关端口",
    name_en: "Gateway Port",
    path: "gateway.port",
    expected_cn: "避免默认端口",
    expected_en: "avoid default port",
    action_cn: "避免使用默认端口，并结合更严格的监听范围和认证设置。",
    action_en: "Avoid the default port and combine that change with tighter bind scope and authentication.",
    abuse_cn: "默认端口更容易被脚本化探测、指纹识别或运维误暴露场景快速命中。",
    abuse_en: "A default port is easier to probe, fingerprint, or hit during scripted scans and accidental exposure scenarios.",
    why_cn: "默认端口本身不是漏洞，但会降低隐藏成本并放大其他配置失误的影响。",
    why_en: "The default port is not a vulnerability by itself, but it lowers obscurity and magnifies the effect of other mistakes."
  },
  "CFG-03": {
    name_cn: "认证令牌",
    name_en: "Auth Token",
    path: "gateway.auth.token",
    expected_cn: "强随机令牌（至少 32 位）",
    expected_en: "strong random token (32+ chars)",
    action_cn: "替换为高强度随机令牌，并避免弱口令式 token。",
    action_en: "Replace it with a high-entropy random token and avoid weak password-like values.",
    abuse_cn: "一旦实例变得可达，弱令牌会显著降低未授权接管或脚本爆破的门槛。",
    abuse_en: "Once the instance becomes reachable, a weak token significantly reduces the effort required for unauthorized takeover or scripted guessing.",
    why_cn: "认证强度决定了暴露面被命中后，攻击者需要付出的下一步成本。",
    why_en: "Authentication strength determines how much work an attacker needs after the exposure surface is reached."
  },
  "CFG-04": {
    name_cn: "沙箱模式",
    name_en: "Sandbox Mode",
    path: "agents.defaults.sandbox.mode",
    expected_cn: "non-main",
    expected_en: "non-main",
    action_cn: "启用更严格的沙箱模式，避免主进程路径直接承担不必要的执行风险。",
    action_en: "Use a stricter sandbox mode so the main process does not carry unnecessary execution risk.",
    abuse_cn: "缺失或宽松的沙箱会让恶意提示、坏插件或错误操作更容易直接影响主执行面。",
    abuse_en: "A missing or weak sandbox makes it easier for malicious prompts, bad plugins, or operator mistakes to affect the main execution surface directly.",
    why_cn: "沙箱是把错误限制在较小范围内的关键边界。",
    why_en: "The sandbox is a core boundary that keeps mistakes contained to a smaller surface."
  },
  "CFG-05": {
    name_cn: "工作区限制",
    name_en: "Workspace Only",
    path: "tools.fs.workspaceOnly",
    expected_cn: "true",
    expected_en: "true",
    action_cn: "把文件访问收紧到工作区，避免把主机上无关目录暴露给运行时。",
    action_en: "Restrict file access to the workspace so unrelated host directories are not exposed to the runtime.",
    abuse_cn: "如果文件系统范围过宽，被影响的流程可以读取、遍历或修改与你当前任务无关的文件。",
    abuse_en: "If filesystem scope is too broad, an influenced workflow can read, traverse, or modify files unrelated to the current task.",
    why_cn: "文件边界越宽，数据暴露和误改范围越大。",
    why_en: "The broader the file boundary, the larger the data exposure and accidental modification range."
  },
  "CFG-06": {
    name_cn: "提权工具权限",
    name_en: "Elevated Tools",
    path: "tools.elevated.enabled",
    expected_cn: "false",
    expected_en: "false",
    action_cn: "关闭提权工具，只有在书面化、可验证的运维需求下才单独放行。",
    action_en: "Disable elevated tools and only allow them when there is a documented, verified operational need.",
    abuse_cn: "如果攻击者影响了执行链路，提权能力会把普通配置问题升级成主机级风险。",
    abuse_en: "If an attacker influences the execution path, elevated capability can turn an ordinary configuration issue into host-level risk.",
    why_cn: "提权能力会显著扩大单次错误的爆炸半径。",
    why_en: "Elevated capability significantly increases the blast radius of a single mistake."
  },
  "CFG-07": {
    name_cn: "DM 会话隔离",
    name_en: "DM Scope Isolation",
    path: "sessions.dmScope",
    expected_cn: "per-channel-peer",
    expected_en: "per-channel-peer",
    action_cn: "把 DM 隔离收紧到每通道每对象，降低跨会话数据串扰风险。",
    action_en: "Tighten DM isolation to per-channel-peer to reduce cross-session data bleed.",
    abuse_cn: "弱隔离会让本不该共享的会话上下文在邻近对话或对象之间泄漏。",
    abuse_en: "Weak isolation can leak session context across adjacent conversations or peers that should not share it.",
    why_cn: "会话隔离错误通常不会立刻爆炸，但会持续侵蚀数据边界。",
    why_en: "Session isolation issues often do not explode immediately, but they quietly erode data boundaries over time."
  },
  "CFG-08": {
    name_cn: "密钥存储方式",
    name_en: "Secrets Storage",
    path: "config scan",
    expected_cn: "仅环境变量引用",
    expected_en: "env-var references only",
    action_cn: "移除配置中的明文密钥，改用更安全的引用方式。",
    action_en: "Remove plaintext secrets from config and switch to safer reference methods.",
    abuse_cn: "明文密钥可以通过配置复制、日志、备份或更宽的文件访问边界被意外暴露或被人直接拿走。",
    abuse_en: "Plaintext secrets can be exposed through copied configs, logs, backups, or broader file access boundaries and then reused directly.",
    why_cn: "一旦密钥写进配置，很多原本普通的读取行为都会变成凭据泄露问题。",
    why_en: "Once a secret is written into config, many otherwise ordinary read paths become credential-leak paths."
  },
  "CFG-09": {
    name_cn: "TLS/HTTPS 配置",
    name_en: "TLS Configuration",
    path: "gateway.tls",
    expected_cn: "公网暴露时启用",
    expected_en: "enabled when public-facing",
    action_cn: "如果实例不是纯本地使用，启用 TLS 并同步收紧暴露面。",
    action_en: "If the instance is not strictly local, enable TLS and tighten exposure at the same time.",
    abuse_cn: "公网或更广网络暴露但未启用 TLS 时，中间路径上的敏感交互更容易被观察或截获。",
    abuse_en: "If the instance is exposed beyond a local boundary without TLS, sensitive traffic becomes easier to observe or intercept on the path.",
    why_cn: "链路保护不是单独的万能措施，但缺失时会放大暴露风险。",
    why_en: "Transport protection is not a cure-all, but its absence amplifies exposure risk."
  },
  "CFG-10": {
    name_cn: "日志级别",
    name_en: "Log Level",
    path: "logging.level",
    expected_cn: "info 或 warn",
    expected_en: "info or warn",
    action_cn: "生产或长期运行环境避免 debug 级别，减少敏感上下文进入日志。",
    action_en: "Avoid debug level in production or long-running environments so sensitive context does not spill into logs.",
    abuse_cn: "过度详细的日志会让路径、提示、token 片段或行为线索被本地读取者获得。",
    abuse_en: "Overly detailed logs can expose paths, prompts, token fragments, or behavioral clues to anyone who can read them locally.",
    why_cn: "日志常被忽视，但它们会积累可利用的上下文。",
    why_en: "Logs are often ignored, but they accumulate exploitable context."
  },
  "CFG-11": {
    name_cn: "YOLO 执行覆盖",
    name_en: "YOLO Exec Override",
    path: "tools.exec",
    expected_cn: "allowlist + ask=always",
    expected_en: "allowlist + ask=always",
    action_cn: "把执行策略收紧为白名单并始终确认，避免主机命令在弱控制下运行。",
    action_en: "Tighten execution to an allowlist with always-on approval so host commands do not run under weak control.",
    abuse_cn: "如果 host exec 可以在低确认条件下运行，攻击者更容易把提示影响转成真实主机命令。",
    abuse_en: "If host exec can run with weak approval, an attacker has a much easier path from prompt influence to real host commands.",
    why_cn: "这是把“语言影响”变成“主机动作”的关键跳板。",
    why_en: "This is a key bridge that turns language influence into host action."
  },
  "CFG-12": {
    name_cn: "浏览器 SSRF 与 evaluate",
    name_en: "Browser SSRF and Evaluate",
    path: "browser",
    expected_cn: "evaluate=false 且私网访问关闭",
    expected_en: "evaluate=false and private-network access off",
    action_cn: "关闭 evaluate，并默认关闭私网访问，除非有已验证的硬需求。",
    action_en: "Disable evaluate and keep private-network access off unless there is a verified hard requirement.",
    abuse_cn: "浏览器 evaluate 或私网访问开启时，受影响的流程更容易把浏览能力变成内部探测或危险执行跳板。",
    abuse_en: "When browser evaluate or private-network access is enabled, an influenced workflow has an easier path to turn browsing into internal probing or risky execution.",
    why_cn: "浏览器能力一旦越界，风险不再只是页面访问。",
    why_en: "Once browser capability crosses the intended boundary, the risk is no longer just page access."
  },
  "CFG-13": {
    name_cn: "CDP 来源范围",
    name_en: "CDP Source Range",
    path: "agents.defaults.sandbox.browser.cdpSourceRange",
    expected_cn: "仅已验证拓扑的 CIDR",
    expected_en: "verified CIDR only",
    action_cn: "仅在你确认过 Docker 或沙箱网络拓扑后才写入可信来源范围。",
    action_en: "Only write a trusted source range after you have verified the Docker or sandbox network topology.",
    abuse_cn: "来源范围设置错误时，原本不该接入的来源可能接触到浏览器控制面，或正确来源被误阻断。",
    abuse_en: "If source range is set incorrectly, sources that should not have access may reach the browser control plane, or valid sources may be blocked by mistake.",
    why_cn: "这类设置依赖真实拓扑，盲猜往往比不设更危险。",
    why_en: "This setting depends on real topology; guessing is often more dangerous than leaving it unset."
  },
  "CFG-14": {
    name_cn: "mDNS 发现",
    name_en: "mDNS Discovery",
    path: "discovery.mdns.mode",
    expected_cn: "off",
    expected_en: "off",
    action_cn: "关闭 mDNS / Bonjour 发现，避免实例在局域网中被主动广播。",
    action_en: "Disable mDNS / Bonjour discovery so the instance is not actively broadcast on the local network.",
    abuse_cn: "发现功能会让实例更容易被同网段设备识别、枚举或画像。",
    abuse_en: "Discovery makes the instance easier for devices on the same network to identify, enumerate, and profile.",
    why_cn: "低可见性本身就是一种有效的缩面措施。",
    why_en: "Lower visibility is itself a meaningful exposure-reduction measure."
  },
  "CFG-15": {
    name_cn: "真实 IP 回退",
    name_en: "Real-IP Fallback",
    path: "gateway.allowRealIpFallback",
    expected_cn: "false",
    expected_en: "false",
    action_cn: "关闭真实 IP 回退，避免把来源识别建立在宽松信任链上。",
    action_en: "Disable real-IP fallback so source identity is not based on a weak trust chain.",
    abuse_cn: "宽松的来源回退逻辑会让攻击者更容易伪装来源或污染你的访问判断。",
    abuse_en: "Loose fallback logic makes it easier for an attacker to spoof source identity or pollute your access assumptions.",
    why_cn: "来源识别一旦不可信，监控和调查都会变弱。",
    why_en: "Once source identity becomes unreliable, both monitoring and investigation get weaker."
  },
  "CFG-16": {
    name_cn: "Control UI 来源白名单",
    name_en: "Control UI Origin Allowlist",
    path: "gateway.controlUi.allowedOrigins",
    expected_cn: "显式且非通配符白名单",
    expected_en: "explicit non-wildcard allowlist",
    action_cn: "为非 loopback Control UI 明确写入来源白名单，避免使用通配符。",
    action_en: "Set an explicit non-wildcard origin allowlist for non-loopback Control UI access.",
    abuse_cn: "来源控制过宽时，不受信任的浏览器上下文更容易与控制界面建立交互。",
    abuse_en: "If origin control is too broad, untrusted browser contexts have an easier path to interact with the control UI.",
    why_cn: "浏览器侧信任边界过宽，会把原本内部的控制面暴露给不该信任的页面。",
    why_en: "An overly broad browser trust boundary exposes an internal control plane to pages that should not be trusted."
  },
  "PLG-01": {
    name_cn: "插件迁移与白名单",
    name_en: "Plugin Migration and Allowlist",
    path: "plugins",
    expected_cn: "新 schema + 最小 allowlist",
    expected_en: "modern schema + minimum allowlist",
    action_cn: "清理旧插件 schema，并把 plugins.allow 收紧到最小可信集合。",
    action_en: "Clean up legacy plugin schema and tighten plugins.allow to the minimum trusted set.",
    abuse_cn: "弱 allowlist 或迁移漂移会让不必要的插件能力进入运行边界。",
    abuse_en: "A weak allowlist or migration drift can bring unnecessary plugin capability into the runtime boundary.",
    why_cn: "插件边界不清晰时，供应链和执行面会一起变宽。",
    why_en: "When plugin boundaries are unclear, both supply-chain and execution surfaces widen together."
  }
};

function detectLang(argv) {
  const idx = argv.indexOf("--lang");
  if (idx >= 0 && argv[idx + 1]) {
    const value = String(argv[idx + 1]).toLowerCase();
    if (["cn", "zh", "zh-cn", "zh_cn", "zh-hans", "chs"].indexOf(value) >= 0) return "cn";
    if (["en", "en-us", "en_us", "en-gb", "en_gb"].indexOf(value) >= 0) return "en";
  }
  const locale = [process.env.M78ARMOR_LANG, process.env.LC_ALL, process.env.LC_MESSAGES, process.env.LANG, Intl.DateTimeFormat().resolvedOptions().locale].filter(Boolean).join(" ").toLowerCase();
  if (locale.indexOf("zh") >= 0 || locale.indexOf("cn") >= 0) return "cn";
  return "en";
}

function parseArgs(argv) {
  const out = { lang: detectLang(argv), json: false, config: null, help: false, version: false, quiet: false };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--json") {
      out.json = true;
      continue;
    }
    if (token === "--help" || token === "-h") {
      out.help = true;
      continue;
    }
    if (token === "--version" || token === "-V") {
      out.version = true;
      continue;
    }
    if (token === "--quiet" || token === "--silent" || token === "-q") {
      out.quiet = true;
      continue;
    }
    if (token === "--lang") {
      i += 1;
      continue;
    }
    if (token === "--config" && argv[i + 1]) {
      out.config = argv[i + 1];
      i += 1;
    }
  }
  return out;
}

function stripJsonComments(input) {
  let out = "";
  let inString = false;
  let stringChar = "";
  let inLine = false;
  let inBlock = false;
  for (let i = 0; i < input.length; i += 1) {
    const ch = input[i];
    const next = i + 1 < input.length ? input[i + 1] : "";
    if (inLine) {
      if (ch === "\n") {
        inLine = false;
        out += ch;
      }
      continue;
    }
    if (inBlock) {
      if (ch === "*" && next === "/") {
        inBlock = false;
        i += 1;
      }
      continue;
    }
    if (inString) {
      out += ch;
      if (ch === "\\") {
        if (i + 1 < input.length) {
          out += input[i + 1];
          i += 1;
        }
        continue;
      }
      if (ch === stringChar) {
        inString = false;
        stringChar = "";
      }
      continue;
    }
    if (ch === "\"" || ch === "'") {
      inString = true;
      stringChar = ch;
      out += ch;
      continue;
    }
    if (ch === "/" && next === "/") {
      inLine = true;
      i += 1;
      continue;
    }
    if (ch === "/" && next === "*") {
      inBlock = true;
      i += 1;
      continue;
    }
    out += ch;
  }
  return out;
}

function deepGet(obj, dotted) {
  const parts = String(dotted).split(".");
  let current = obj;
  for (let i = 0; i < parts.length; i += 1) {
    if (current === null || current === undefined || !Object.prototype.hasOwnProperty.call(current, parts[i])) {
      return undefined;
    }
    current = current[parts[i]];
  }
  return current;
}

function normalizeLower(value) {
  if (value === null || value === undefined) return "";
  return String(value).trim().toLowerCase();
}

function isTruthy(value) {
  if (value === true) return true;
  const normalized = normalizeLower(value);
  return normalized === "true" || normalized === "1" || normalized === "yes" || normalized === "on" || normalized === "enabled";
}

function isWeakToken(token) {
  const value = String(token || "");
  if (!value) return true;
  if (value.length < 32) return true;
  const low = value.toLowerCase();
  const weak = ["changeme", "default", "openclaw", "password", "token", "admin", "1234", "secret"];
  for (let i = 0; i < weak.length; i += 1) {
    if (low.indexOf(weak[i]) >= 0) return true;
  }
  return false;
}

function maskToken(value) {
  const text = String(value || "");
  if (text.length <= 8) return "***";
  return text.slice(0, 4) + "..." + text.slice(text.length - 4);
}

function isPublicBind(bindValue) {
  const value = normalizeLower(bindValue);
  if (!value) return false;
  if (value === "0.0.0.0" || value === "::" || value === "[::]") return true;
  if (value === "localhost" || value === "127.0.0.1" || value === "::1") return false;
  if (value.indexOf("192.168.") === 0 || value.indexOf("10.") === 0 || value.indexOf("172.") === 0) return true;
  return value !== "127.0.0.1" && value !== "::1";
}

function looksLikeCidr(value) {
  return /^[0-9]{1,3}(\.[0-9]{1,3}){3}\/[0-9]{1,2}$/.test(String(value || ""));
}

function formatValue(value) {
  if (value === undefined) return "UNSET";
  if (value === null) return "null";
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") return String(value);
  try {
    return JSON.stringify(value);
  } catch (_) {
    return String(value);
  }
}

function discoverConfigPath(explicitPath) {
  const candidates = [];
  if (explicitPath) candidates.push(path.resolve(explicitPath));
  const home = os.homedir();
  candidates.push(path.join(home, ".openclaw", "openclaw.json"));
  candidates.push(path.join(home, ".config", "openclaw", "openclaw.json"));
  candidates.push(path.join(home, ".openclaw", "config.json"));
  candidates.push(path.resolve(process.cwd(), "openclaw.json"));
  candidates.push(path.resolve(process.cwd(), ".openclaw", "openclaw.json"));
  for (let i = 0; i < candidates.length; i += 1) {
    if (fs.existsSync(candidates[i]) && fs.statSync(candidates[i]).isFile()) return candidates[i];
  }
  return explicitPath ? path.resolve(explicitPath) : null;
}

function loadConfig(configPath) {
  if (!configPath || !fs.existsSync(configPath)) {
    return { config: {}, error: "config_not_found" };
  }
  try {
    const raw = fs.readFileSync(configPath, "utf8");
    const cleaned = stripJsonComments(raw);
    return { config: JSON.parse(cleaned), error: null };
  } catch (err) {
    return { config: {}, error: err.message || "parse_error" };
  }
}

function hasPlaintextSecrets(obj, prefix, findings) {
  if (!obj || typeof obj !== "object") return;
  if (Array.isArray(obj)) {
    for (let i = 0; i < obj.length; i += 1) {
      hasPlaintextSecrets(obj[i], prefix + "[" + i + "]", findings);
    }
    return;
  }
  const riskyKeys = ["token", "secret", "apikey", "api_key", "password", "passwd", "access_key"];
  const keys = Object.keys(obj);
  for (let i = 0; i < keys.length; i += 1) {
    const key = keys[i];
    const value = obj[key];
    const currentPath = prefix ? prefix + "." + key : key;
    const normalizedKey = key.toLowerCase();
    if (typeof value === "string") {
      let risky = false;
      for (let j = 0; j < riskyKeys.length; j += 1) {
        if (normalizedKey.indexOf(riskyKeys[j]) >= 0) {
          risky = true;
          break;
        }
      }
      if (risky) {
        const lowerValue = value.toLowerCase();
        const looksLikeEnv = lowerValue.indexOf("${") >= 0 || lowerValue.indexOf("env:") === 0 || lowerValue.indexOf("process.env") >= 0;
        if (!looksLikeEnv && value.trim() !== "") {
          findings.push({ path: currentPath, sample: maskToken(value) });
        }
      }
    }
    if (value && typeof value === "object") {
      hasPlaintextSecrets(value, currentPath, findings);
    }
  }
}

function makeFinding(id, severity, currentValue, expectedValue) {
  const meta = CHECKS[id];
  return {
    id: id,
    severity: severity,
    name_cn: meta.name_cn,
    name_en: meta.name_en,
    config_path: meta.path,
    current_value: currentValue,
    expected_value: expectedValue,
    abuse_cn: meta.abuse_cn,
    abuse_en: meta.abuse_en,
    why_cn: meta.why_cn,
    why_en: meta.why_en,
    action_cn: meta.action_cn,
    action_en: meta.action_en
  };
}

function auditConfig(config) {
  const findings = [];
  const bindValue = deepGet(config, "gateway.bind");
  findings.push(makeFinding("CFG-01", bindValue === "127.0.0.1" ? "GREEN" : bindValue === undefined ? "AMBER" : isPublicBind(bindValue) ? "RED" : "AMBER", formatValue(bindValue), CHECKS["CFG-01"].expected_en));

  const portValue = deepGet(config, "gateway.port");
  findings.push(makeFinding("CFG-02", portValue === undefined ? "AMBER" : Number(portValue) === 18789 ? "AMBER" : "GREEN", formatValue(portValue), CHECKS["CFG-02"].expected_en));

  const tokenValue = deepGet(config, "gateway.auth.token");
  findings.push(makeFinding("CFG-03", tokenValue === undefined ? "AMBER" : isWeakToken(tokenValue) ? "RED" : "GREEN", tokenValue === undefined ? "UNSET" : maskToken(tokenValue), CHECKS["CFG-03"].expected_en));

  const sandboxMode = deepGet(config, "agents.defaults.sandbox.mode");
  const sandboxLower = normalizeLower(sandboxMode);
  findings.push(makeFinding("CFG-04", sandboxLower === "non-main" ? "GREEN" : sandboxMode === undefined ? "RED" : "RED", formatValue(sandboxMode), CHECKS["CFG-04"].expected_en));

  const workspaceOnly = deepGet(config, "tools.fs.workspaceOnly");
  findings.push(makeFinding("CFG-05", workspaceOnly === true ? "GREEN" : workspaceOnly === false ? "RED" : "AMBER", formatValue(workspaceOnly), CHECKS["CFG-05"].expected_en));

  const elevatedEnabled = deepGet(config, "tools.elevated.enabled");
  findings.push(makeFinding("CFG-06", elevatedEnabled === false ? "GREEN" : elevatedEnabled === true ? "RED" : "AMBER", formatValue(elevatedEnabled), CHECKS["CFG-06"].expected_en));

  const dmScope = deepGet(config, "sessions.dmScope");
  findings.push(makeFinding("CFG-07", normalizeLower(dmScope) === "per-channel-peer" ? "GREEN" : dmScope === undefined ? "AMBER" : "AMBER", formatValue(dmScope), CHECKS["CFG-07"].expected_en));

  const secretFindings = [];
  hasPlaintextSecrets(config, "", secretFindings);
  findings.push(makeFinding("CFG-08", secretFindings.length > 0 ? "RED" : "GREEN", secretFindings.length > 0 ? JSON.stringify(secretFindings) : "none", CHECKS["CFG-08"].expected_en));

  const tlsValue = deepGet(config, "gateway.tls");
  findings.push(makeFinding("CFG-09", isPublicBind(bindValue) && !isTruthy(tlsValue) ? "AMBER" : "GREEN", formatValue(tlsValue), CHECKS["CFG-09"].expected_en));

  const logLevel = deepGet(config, "logging.level");
  const logLower = normalizeLower(logLevel);
  findings.push(makeFinding("CFG-10", logLower === "info" || logLower === "warn" ? "GREEN" : logLevel === undefined ? "AMBER" : "AMBER", formatValue(logLevel), CHECKS["CFG-10"].expected_en));

  const execSecurity = deepGet(config, "tools.exec.security");
  const execAsk = deepGet(config, "tools.exec.ask");
  const execSeverity = normalizeLower(execSecurity) === "allowlist" && normalizeLower(execAsk) === "always" ? "GREEN" : execSecurity === undefined || execAsk === undefined || normalizeLower(execSecurity) === "full" || normalizeLower(execAsk) === "off" ? "RED" : "AMBER";
  findings.push(makeFinding("CFG-11", execSeverity, JSON.stringify({ security: execSecurity === undefined ? "UNSET" : execSecurity, ask: execAsk === undefined ? "UNSET" : execAsk }), CHECKS["CFG-11"].expected_en));

  const evaluateEnabled = deepGet(config, "browser.evaluateEnabled");
  const privateNetwork = deepGet(config, "browser.ssrfPolicy.dangerouslyAllowPrivateNetwork");
  const browserSeverity = (evaluateEnabled === undefined || isTruthy(evaluateEnabled)) || (privateNetwork === undefined || isTruthy(privateNetwork)) ? "RED" : "GREEN";
  findings.push(makeFinding("CFG-12", browserSeverity, JSON.stringify({ evaluateEnabled: evaluateEnabled === undefined ? "UNSET" : evaluateEnabled, dangerouslyAllowPrivateNetwork: privateNetwork === undefined ? "UNSET" : privateNetwork }), CHECKS["CFG-12"].expected_en));

  const cdpRange = deepGet(config, "agents.defaults.sandbox.browser.cdpSourceRange");
  findings.push(makeFinding("CFG-13", looksLikeCidr(cdpRange) ? "GREEN" : "AMBER", formatValue(cdpRange), CHECKS["CFG-13"].expected_en));

  const mdnsMode = deepGet(config, "discovery.mdns.mode");
  const mdnsLower = normalizeLower(mdnsMode);
  const mdnsSeverity = mdnsLower === "off" ? "GREEN" : mdnsMode === undefined ? "RED" : mdnsLower === "minimal" ? "AMBER" : "RED";
  findings.push(makeFinding("CFG-14", mdnsSeverity, formatValue(mdnsMode), CHECKS["CFG-14"].expected_en));

  const realIpFallback = deepGet(config, "gateway.allowRealIpFallback");
  findings.push(makeFinding("CFG-15", realIpFallback === false ? "GREEN" : realIpFallback === true ? "RED" : "AMBER", formatValue(realIpFallback), CHECKS["CFG-15"].expected_en));

  const allowedOrigins = deepGet(config, "gateway.controlUi.allowedOrigins");
  let cfg16Severity = "GREEN";
  if (Array.isArray(allowedOrigins)) {
    const wildcard = allowedOrigins.some(function(item) { return String(item).indexOf("*") >= 0; });
    cfg16Severity = wildcard ? "RED" : allowedOrigins.length === 0 ? "AMBER" : "GREEN";
  } else if (allowedOrigins === undefined) {
    cfg16Severity = isPublicBind(bindValue) ? "RED" : "AMBER";
  } else if (typeof allowedOrigins === "string") {
    cfg16Severity = allowedOrigins.indexOf("*") >= 0 ? "RED" : "GREEN";
  } else {
    cfg16Severity = "AMBER";
  }
  findings.push(makeFinding("CFG-16", cfg16Severity, formatValue(allowedOrigins), CHECKS["CFG-16"].expected_en));

  const pluginsAllow = deepGet(config, "plugins.allow");
  const legacyPluginSchema = deepGet(config, "plugins.paths") !== undefined || deepGet(config, "plugins.enabled") !== undefined;
  let plgSeverity = "GREEN";
  if (legacyPluginSchema) {
    plgSeverity = "AMBER";
  }
  if (pluginsAllow === undefined) {
    plgSeverity = plgSeverity === "GREEN" ? "AMBER" : plgSeverity;
  }
  if (Array.isArray(pluginsAllow) && pluginsAllow.length === 0) {
    plgSeverity = plgSeverity === "GREEN" ? "AMBER" : plgSeverity;
  }
  findings.push(makeFinding("PLG-01", plgSeverity, JSON.stringify({ legacy_schema_detected: legacyPluginSchema, plugins_allow: pluginsAllow === undefined ? "UNSET" : pluginsAllow }), CHECKS["PLG-01"].expected_en));

  return findings;
}

function summarize(findings) {
  const summary = { total_checks: findings.length, passed: 0, warnings: 0, critical: 0 };
  for (let i = 0; i < findings.length; i += 1) {
    if (findings[i].severity === "GREEN") summary.passed += 1;
    else if (findings[i].severity === "RED") summary.critical += 1;
    else summary.warnings += 1;
  }
  return summary;
}

function rankSeverity(severity) {
  if (severity === "RED") return 0;
  if (severity === "AMBER") return 1;
  return 2;
}

function translate(lang, cn, en) {
  return lang === "cn" ? cn : en;
}

function formatSeverity(lang, severity) {
  if (lang === "cn") {
    if (severity === "RED") return "高风险";
    if (severity === "AMBER") return "待确认";
    return "通过";
  }
  if (severity === "RED") return "high";
  if (severity === "AMBER") return "review";
  return "pass";
}

function useColor() {
  if (process.env.NO_COLOR) return false;
  return Boolean(process.stdout && process.stdout.isTTY);
}

function colorWrap(text, code) {
  if (!useColor()) return String(text);
  return "\u001b[" + code + "m" + String(text) + "\u001b[0m";
}

function colorBySeverity(text, severity) {
  if (severity === "RED") return colorWrap(text, "31");
  if (severity === "AMBER") return colorWrap(text, "33");
  return colorWrap(text, "32");
}

function printHelp() {
  const lines = [
    DISPLAY_NAME + " v" + VERSION,
    "",
    "Usage:",
    "  node ./scripts/m78armor-lite.js --lang en",
    "  node ./scripts/m78armor-lite.js --lang zh",
    "  node ./scripts/m78armor-lite.js --config \"/path/to/openclaw.json\" --lang en",
    "  node ./scripts/m78armor-lite.js --json",
    "  node ./scripts/m78armor-lite.js --quiet",
    "",
    "Flags:",
    "  --lang en|zh   Set output language (default: auto-detect from locale)",
    "  --config PATH  Explicit OpenClaw config file path",
    "  --json         Machine-readable JSON output",
    "  --quiet, -q    Suppress upgrade CTA (for CI/pipeline use)",
    "  --version, -V  Print version and exit",
    "  --help, -h     Print this help and exit",
    "",
    "Environment variables:",
    "  OPENCLAW_CONFIG  Override config file path",
    "  M78ARMOR_LANG    Override language detection",
    "  NO_COLOR         Disable terminal colors",
    "",
    "Environment:",
    "  Valid on WSL2, Ubuntu, macOS, and standard cloud/domestic instances.",
    "  Uses local-first execution. Configuration data is not uploaded.",
    "",
    "Purpose:",
    "  Local read-only security configuration review and hardening check",
    "  (本地只读安全配置检查与加固评估) for the OpenClaw instance itself.",
    "",
    "Common use:",
    "  Run after install or upgrade to review baseline gaps, permission and exposure issues, risky defaults, and drift.",
    "  安装或升级后运行，检查配置基线缺口、权限暴露面、风险默认值与配置漂移。",
    "",
    "Inside OpenClaw, you can also ask:",
    "  run m78armor : openclaw security configuration check",
    "  check this openclaw instance for risky security configuration gaps",
    "  review local openclaw configuration baseline and exposure issues",
    "  检查这个 OpenClaw 实例的安全配置问题",
    "  执行本地 OpenClaw 配置基线与加固评估"
  ];
  process.stdout.write(lines.join("\n") + "\n");
}

function printHuman(result, lang, quiet) {
  const findings = result.findings.slice().sort(function(a, b) { return rankSeverity(a.severity) - rankSeverity(b.severity); });
  const gaps = findings.filter(function(item) { return item.severity !== "GREEN"; });
  console.log(DISPLAY_NAME + " v" + VERSION);
  console.log(translate(lang, "本地只读配置检查与加固评估（免费版）", "Local read-only configuration check and hardening review (free edition)"));
  console.log(translate(lang, "用途：检查 OpenClaw 实例自身的配置基线、暴露面与权限边界。这不是网络扫描器。", "Purpose: review the OpenClaw instance itself for baseline, exposure, and permission-boundary issues. This is not a network scanner."));
  console.log("");
  console.log(translate(lang, "配置文件", "Config file") + ": " + (result.config_path || translate(lang, "未找到", "not found")));
  if (result.config_error) {
    console.log(translate(lang, "状态", "Status") + ": " + translate(lang, "无法完整加载配置", "could not load config completely") + " (" + result.config_error + ")");
  }
  console.log(translate(lang, "检查总数", "Total checks") + ": " + result.summary.total_checks);
  console.log(colorBySeverity(translate(lang, "通过", "Passed"), "GREEN") + ": " + result.summary.passed);
  console.log(colorBySeverity(translate(lang, "待确认", "Review"), "AMBER") + ": " + result.summary.warnings);
  console.log(colorBySeverity(translate(lang, "高风险", "High risk"), "RED") + ": " + result.summary.critical);
  console.log("");
  if (gaps.length === 0) {
    console.log(translate(lang, "未发现明显的配置与安全基线缺口。", "No obvious configuration or secured baseline gaps were found."));
  } else {
    console.log(translate(lang, "发现的配置与安全基线缺口", "Configuration and secured baseline gaps found"));
    console.log("");
    for (let i = 0; i < gaps.length; i += 1) {
      const item = gaps[i];
      console.log("  [" + item.id + "] " + translate(lang, item.name_cn, item.name_en) + "  " + colorBySeverity(formatSeverity(lang, item.severity), item.severity));
      console.log("    " + translate(lang, "当前值", "Current") + ":        " + colorBySeverity(formatValue(item.current_value), item.severity));
      console.log("    " + translate(lang, "安全基线", "Secured baseline") + ":  " + colorWrap(formatValue(item.expected_value), "32"));
      console.log("    " + translate(lang, "风险路径", "Risk") + ":        " + translate(lang, item.abuse_cn, item.abuse_en));
      console.log("    " + translate(lang, "影响", "Impact") + ":      " + translate(lang, item.why_cn, item.why_en));
      console.log("    " + translate(lang, "手动修复", "Manual fix") + ":  " + translate(lang, item.action_cn, item.action_en));
      if (!quiet) {
        console.log("    " + colorWrap(translate(lang, "一键修复", "Auto-fix"), "36") + ":    " + translate(lang, "M78Armor 基础版可一键应用此安全基线，支持备份与回滚。", "M78Armor Starter applies this secured baseline automatically with backup and rollback."));
      }
      console.log("");
    }
  }
  if (!quiet) {
    console.log(translate(lang, "─── 免费版到此为止 ───", "─── Free edition ends here ───"));
    console.log("");
    console.log(translate(lang,
      "本次检查发现 " + result.summary.critical + " 项高风险和 " + result.summary.warnings + " 项待确认配置。手动逐项修复预计需要 1-2 小时，且无回滚保护。",
      "This check found " + result.summary.critical + " high-risk and " + result.summary.warnings + " review items. Manual remediation takes an estimated 1-2 hours with no rollback safety net."));
    console.log("");
    console.log(translate(lang,
      "M78Armor 基础版 (¥88) 一条命令完成全部修复：自动应用安全基线 → 变更前备份 → 回滚保护 → 更深层风险审计 → 可追踪输出。",
      "M78Armor Starter applies all fixes in one command: secured baseline → pre-change backup → rollback protection → deeper risk-aware checks → traceable outputs."));
    console.log("");
    console.log(translate(lang, "请复制以下地址到浏览器升级：", "Copy this URL into your browser to upgrade:"));
    console.log(colorWrap(ORDER_URL, "36"));
  }
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }
  if (options.version) {
    process.stdout.write(DISPLAY_NAME + " v" + VERSION + "\n");
    return;
  }
  const explicitConfig = options.config || process.env.OPENCLAW_CONFIG || null;
  const configPath = discoverConfigPath(explicitConfig);
  const loaded = loadConfig(configPath);
  const findings = auditConfig(loaded.config || {});
  const summary = summarize(findings);
  const result = {
    product: DISPLAY_NAME,
    version: VERSION,
    mode: "lite",
    read_only: true,
    config_path: configPath,
    config_error: loaded.error,
    summary: summary,
    findings: findings,
    upgrade: {
      url: ORDER_URL,
      paid_value_en: "apply secured baseline for OpenClaw, backup and rollback, deeper risk-aware checks, and traceable outputs",
      paid_value_cn: "自动应用安全基线、变更备份与回滚、更深层风险审计、可追踪输出"
    }
  };
  if (options.json) {
    process.stdout.write(JSON.stringify(result, null, 2) + "\n");
    process.exitCode = summary.critical > 0 ? 1 : 0;
    return;
  }
  printHuman(result, options.lang, options.quiet);
  process.exitCode = summary.critical > 0 ? 1 : 0;
}

main();