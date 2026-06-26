// Operation Quarantine: Skill/Plugin Sanitizer
// Analyzes ClewHub skills and other plugin configs for injection attempts

function parseSkillConfig(rawContent) {
  const parsed = {
    name: null,
    description: null,
    instructions: null,
    tools: [],
    permissions: [],
    urls: [],
    rawText: rawContent,
  };

  try {
    const json = JSON.parse(rawContent);
    parsed.name = json.name || json.skill_name || json.title || null;
    parsed.description = json.description || json.desc || json.about || null;
    parsed.instructions = json.instructions || json.system_prompt || json.prompt || json.system || null;
    parsed.tools = json.tools || json.functions || json.capabilities || [];
    parsed.permissions = json.permissions || json.scopes || json.access || [];
    parsed.rawText = extractAllStrings(json).join("\n");
    return parsed;
  } catch {
    // Not JSON
  }

  const nameMatch = rawContent.match(/(?:^|\n)#?\s*(?:name|title|skill):\s*(.+)/i);
  if (nameMatch) parsed.name = nameMatch[1].trim();

  const descMatch = rawContent.match(/(?:^|\n)#?\s*(?:description|about|desc):\s*([\s\S]+?)(?:\n#|\n---|\n\n\n|$)/i);
  if (descMatch) parsed.description = descMatch[1].trim();

  const instrMatch = rawContent.match(/(?:^|\n)#?\s*(?:instructions?|system[_\s]?prompt|prompt):\s*([\s\S]+?)(?:\n#|\n---|\n\n\n|$)/i);
  if (instrMatch) parsed.instructions = instrMatch[1].trim();

  const urlMatches = rawContent.match(/https?:\/\/[^\s"'<>)}\]]+/gi);
  if (urlMatches) parsed.urls = [...new Set(urlMatches)];

  return parsed;
}

function extractAllStrings(obj, depth = 0) {
  if (depth > 10) return [];
  const strings = [];
  if (typeof obj === "string") {
    strings.push(obj);
  } else if (Array.isArray(obj)) {
    for (const item of obj) {
      strings.push(...extractAllStrings(item, depth + 1));
    }
  } else if (obj && typeof obj === "object") {
    for (const value of Object.values(obj)) {
      strings.push(...extractAllStrings(value, depth + 1));
    }
  }
  return strings;
}

function analyzeUrls(urls) {
  const suspicious = [];
  const knownSafe = [
    "github.com", "clawhub.com", "npmjs.com", "pypi.org",
    "docs.google.com", "stackoverflow.com", "developer.mozilla.org",
  ];
  const knownDangerous = [
    "ngrok.io", "ngrok-free.app", "requestbin.com", "pipedream.net",
    "webhook.site", "burpcollaborator.net", "interact.sh",
    "oastify.com", "canarytokens.com",
  ];

  for (const url of urls) {
    try {
      const hostname = new URL(url).hostname;
      if (knownDangerous.some(d => hostname.includes(d))) {
        suspicious.push({ url, reason: "Known data exfiltration endpoint" });
      } else if (!knownSafe.some(s => hostname.includes(s))) {
        suspicious.push({ url, reason: "Unknown external endpoint" });
      }
    } catch {
      suspicious.push({ url, reason: "Malformed URL" });
    }
  }
  return suspicious;
}

function analyzePermissions(parsed) {
  const concerns = [];
  const dangerousPerms = [
    "email", "gmail", "mail", "contacts", "calendar",
    "financial", "payment", "banking", "debit", "credit",
    "shell", "exec", "sudo", "root", "admin",
    "ssh", "ftp", "database", "db",
  ];

  const allText = parsed.rawText.toLowerCase();
  for (const perm of dangerousPerms) {
    if (allText.includes(perm)) {
      concerns.push(`References "${perm}" - may require elevated access`);
    }
  }
  return concerns;
}

function sanitizeSkill(rawContent) {
  const parsed = parseSkillConfig(rawContent);
  const urlAnalysis = analyzeUrls(parsed.urls);
  const permConcerns = analyzePermissions(parsed);

  return {
    parsed,
    urlAnalysis,
    permissionConcerns: permConcerns,
    hasSuspiciousUrls: urlAnalysis.length > 0,
    hasPermissionConcerns: permConcerns.length > 0,
    textForAnalysis: parsed.rawText,
  };
}

export { sanitizeSkill, parseSkillConfig, analyzeUrls, analyzePermissions };
