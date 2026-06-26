/**
 * RulesEngine — Static phishing detection rules.
 * Port of the Python rules_engine.py adapted for the OpenClaw skill.
 */

const SUSPICIOUS_TLD = [".xyz", ".tk", ".ml", ".ga", ".cf", ".gq", ".top",
  ".click", ".loan", ".win", ".download", ".stream", ".gdn"];

const KNOWN_LEGITIMATE_DOMAINS = [
  "gmail.com", "outlook.com", "hotmail.com", "yahoo.com",
  "microsoft.com", "apple.com", "amazon.com", "paypal.com",
  "google.com", "facebook.com", "linkedin.com", "twitter.com",
];

const URGENCY_PATTERNS = [
  /\burgent\b/i, /\bimmediate(ly)?\b/i, /\bverif(y|ication)\b/i,
  /\bsuspicious activity\b/i, /\baccount (suspended|blocked|limited)\b/i,
  /\bclick here\b/i, /\bconfirm your\b/i,
  /\bupdate your (account|password|info)\b/i,
  /\byou (have )?won\b/i, /\bclaim (your )?(prize|reward)\b/i,
  /\bact now\b/i, /\bexpires? (today|in \d+ hours?)\b/i,
  /\bverifica tu cuenta\b/i, /\bcuenta suspendida\b/i,
  /\bconfirma tus datos\b/i, /\bacceso no autorizado\b/i,
];

const SUSPICIOUS_URL_PATTERNS = [
  /https?:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/,
  /https?:\/\/[^/]*@/,
  /bit\.ly|tinyurl|goo\.gl|t\.co|ow\.ly|is\.gd/,
  /[a-z0-9-]*paypal[a-z0-9-]*\.(com|net|org)?[^.]*\./i,
  /[a-z0-9-]*google[a-z0-9-]*\.(com|net|org)?[^.]*\./i,
  /[a-z0-9-]*amazon[a-z0-9-]*\.(com|net|org)?[^.]*\./i,
  /[a-z0-9-]*microsoft[a-z0-9-]*\.(com|net|org)?[^.]*\./i,
  /[a-z0-9-]*apple[a-z0-9-]*\.(com|net|org)?[^.]*\./i,
];

const SENSITIVE_INFO_PATTERNS = [
  /\b(credit|debit) card\b/i, /\bcvv\b/i, /\bssn\b/i,
  /\bsocial security\b/i, /\bpassword\b/i, /\bpin\b/i,
  /\bbank account\b/i, /\brouting number\b/i,
  /\bnumero de tarjeta\b/i, /\bcontrasena\b/i,
  /\bdatos bancarios\b/i, /\bclave\b/i,
];

const DANGEROUS_EXTENSIONS = [
  ".exe", ".vbs", ".bat", ".cmd", ".ps1",
  ".js", ".jar", ".scr", ".pif", ".hta", ".wsf",
];

export class RulesEngine {
  analyze(email) {
    const matches = [
      ...this.checkAuthentication(email),
      ...this.checkSender(email),
      ...this.checkSubject(email),
      ...this.checkBody(email),
      ...this.checkUrls(email),
      ...this.checkAttachments(email),
      ...this.checkReplyToMismatch(email),
    ];
    const score = Math.min(matches.reduce((sum, m) => sum + m.scoreImpact, 0), 100);
    return { matches, score };
  }

  checkAuthentication({ spfResult, dkimResult }) {
    const matches = [];
    if (spfResult && ["fail", "softfail"].includes(spfResult.toLowerCase())) {
      matches.push({ ruleId: "AUTH_SPF_FAIL", description: "SPF validation failed (" + spfResult + ")", severity: "high", scoreImpact: 25 });
    }
    if (dkimResult && dkimResult.toLowerCase() === "fail") {
      matches.push({ ruleId: "AUTH_DKIM_FAIL", description: "DKIM signature invalid or missing", severity: "high", scoreImpact: 20 });
    }
    return matches;
  }

  checkSender({ sender }) {
    const matches = [];
    const domain = extractDomain(sender);
    if (!domain) return matches;

    for (const tld of SUSPICIOUS_TLD) {
      if (domain.endsWith(tld)) {
        matches.push({ ruleId: "SENDER_SUSPICIOUS_TLD", description: "Sender uses suspicious TLD: " + tld, severity: "medium", scoreImpact: 15 });
        break;
      }
    }

    for (const legit of KNOWN_LEGITIMATE_DOMAINS) {
      const legitName = legit.split(".")[0];
      if (domain.includes(legitName) && domain !== legit) {
        matches.push({ ruleId: "SENDER_TYPOSQUATTING", description: "Sender domain may be impersonating " + legit + " (got: " + domain + ")", severity: "critical", scoreImpact: 35 });
        break;
      }
    }

    // Display name mismatch
    if (sender.includes("<") && sender.includes(">")) {
      const displayName = sender.split("<")[0].trim().toLowerCase();
      for (const legit of KNOWN_LEGITIMATE_DOMAINS) {
        const legitName = legit.split(".")[0];
        if (displayName.includes(legitName) && !domain.includes(legitName)) {
          matches.push({ ruleId: "SENDER_DISPLAY_MISMATCH", description: "Display name mentions '" + legitName + "' but domain is '" + domain + "'", severity: "critical", scoreImpact: 35 });
          break;
        }
      }
    }

    return matches;
  }

  checkSubject({ subject }) {
    const matches = [];
    const lower = subject.toLowerCase();
    const urgencyCount = URGENCY_PATTERNS.filter(p => p.test(lower)).length;

    if (urgencyCount >= 2) {
      matches.push({ ruleId: "SUBJECT_HIGH_URGENCY", description: "Subject contains " + urgencyCount + " urgency/phishing keywords", severity: "high", scoreImpact: 20 });
    } else if (urgencyCount === 1) {
      matches.push({ ruleId: "SUBJECT_LOW_URGENCY", description: "Subject contains urgency keyword", severity: "medium", scoreImpact: 8 });
    }

    const upperRatio = [...subject].filter(c => c === c.toUpperCase() && c !== c.toLowerCase()).length / Math.max(subject.length, 1);
    if (upperRatio > 0.6 && subject.length > 5) {
      matches.push({ ruleId: "SUBJECT_EXCESSIVE_CAPS", description: "Subject has excessive uppercase letters", severity: "low", scoreImpact: 5 });
    }

    return matches;
  }

  checkBody({ bodyText, urls }) {
    const matches = [];
    const lower = (bodyText ?? "").toLowerCase();

    const sensitiveHits = SENSITIVE_INFO_PATTERNS.filter(p => p.test(lower));
    if (sensitiveHits.length > 0) {
      matches.push({ ruleId: "BODY_SENSITIVE_REQUEST", description: "Body requests sensitive information (" + sensitiveHits.length + " indicators)", severity: "critical", scoreImpact: 30 });
    }

    const urgencyCount = URGENCY_PATTERNS.filter(p => p.test(lower)).length;
    if (urgencyCount >= 3) {
      matches.push({ ruleId: "BODY_HIGH_URGENCY", description: "Body contains " + urgencyCount + " urgency phrases", severity: "high", scoreImpact: 18 });
    }

    const wordCount = lower.split(/\s+/).length;
    if (wordCount < 20 && urls && urls.length > 0) {
      matches.push({ ruleId: "BODY_SHORT_WITH_URL", description: "Very short body with URLs — typical phishing pattern", severity: "medium", scoreImpact: 12 });
    }

    return matches;
  }

  checkUrls({ urls }) {
    const matches = [];
    if (!urls || urls.length === 0) return matches;

    for (const url of urls) {
      for (const pattern of SUSPICIOUS_URL_PATTERNS) {
        if (pattern.test(url)) {
          matches.push({ ruleId: "URL_SUSPICIOUS", description: "Suspicious URL pattern: " + url.slice(0, 60), severity: "high", scoreImpact: 25 });
          break;
        }
      }
      for (const tld of SUSPICIOUS_TLD) {
        if (url.toLowerCase().includes(tld)) {
          matches.push({ ruleId: "URL_SUSPICIOUS_TLD", description: "URL uses suspicious TLD " + tld, severity: "medium", scoreImpact: 12 });
          break;
        }
      }
    }

    return matches;
  }

  checkAttachments({ attachments }) {
    const matches = [];
    if (!attachments || attachments.length === 0) return matches;

    for (const name of attachments) {
      for (const ext of DANGEROUS_EXTENSIONS) {
        if (name.toLowerCase().endsWith(ext)) {
          matches.push({ ruleId: "ATTACHMENT_DANGEROUS", description: "Potentially dangerous attachment: " + name, severity: "critical", scoreImpact: 40 });
          break;
        }
      }
    }

    return matches;
  }

  checkReplyToMismatch({ sender, replyTo }) {
    if (!replyTo) return [];
    const senderDomain = extractDomain(sender);
    const replyDomain = extractDomain(replyTo);
    if (senderDomain && replyDomain && senderDomain !== replyDomain) {
      return [{ ruleId: "REPLY_TO_MISMATCH", description: "Reply-To domain (" + replyDomain + ") differs from sender (" + senderDomain + ")", severity: "high", scoreImpact: 22 }];
    }
    return [];
  }
}

function extractDomain(emailAddress) {
  const match = emailAddress?.match(/@([\w.-]+)/);
  return match ? match[1].toLowerCase() : null;
}
