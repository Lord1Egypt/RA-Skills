import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { preflight } from './bootstrap.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function redact(text, anonymized = false) {
  const securityPatterns = [
    { name: 'URL', regex: /https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)/gi },
    { name: 'PRIVATE_KEY', regex: /-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----/g },
    { name: 'PASSWORD', regex: /\b(?:password|passwd|secret|token|bearer)(?:\s+(?:is|was))?\s*[:=]\s*["']?[^\s,;]+["']?/gi },
    { name: 'API_ID_KEYS', regex: /\b(?=[a-zA-Z0-9._-]*\d)[a-zA-Z0-9._-]{16,}\b/g },
    { name: 'SSN', regex: /\b\d{3}-\d{2}-\d{4}\b/g },
    { name: 'BANK', regex: /\b(?:\d{9}|\d{10,12})\b/g },
    { name: 'IP', regex: /\b(?:\d{1,3}\.){3}\d{1,3}\b|::1\b|\b(?:[a-fA-F0-9]{1,4}:){1,7}:?[a-fA-F0-9]{0,4}(?::[a-fA-F0-9]{1,4}){1,7}\b|\b(?:[a-fA-F0-9]{1,4}:){7,8}[a-fA-F0-9]{1,4}\b/g }
  ];

  const privatePatterns = [
    { name: 'EMAIL', regex: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g },
    { name: 'PHONE', regex: /(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|\b\d{3}[-.\s]\d{4}\b|\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b/g },
    { name: 'ADDRESS', regex: /\b\d{1,5}\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir|Way|Pkwy|Parkway)\b/g },
    { name: 'DOB', regex: /\b(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b/g },
    { name: 'USER_HANDLE', regex: /\B@[\w.-]+\b/g }
  ];

  let cleaned = text;

  securityPatterns.forEach(p => {
    cleaned = cleaned.replace(p.regex, `[REDACTED_${p.name}]`);
  });

  if (anonymized) {
    privatePatterns.forEach(p => {
      cleaned = cleaned.replace(p.regex, `[REDACTED_${p.name}]`);
    });
  }

  return cleaned;
}

async function distillation() {
  await preflight('distillation');

  const lensDir = path.join(process.cwd(), '.lens');
  const scopePath = path.join(lensDir, 'SCOPE.json');
  let anonymized = false;

  if (fs.existsSync(scopePath)) {
    try {
      const scope = JSON.parse(fs.readFileSync(scopePath, 'utf8'));
      anonymized = scope.meta?.anonymize === true;
    } catch (e) {}
  }

  const SESSIONS_DIR = path.join(process.env.HOME, '.openclaw/agents/main/sessions');
  const OUTPUT_FILE = path.join(lensDir, 'TRACE.txt');
  const TWENTY_FOUR_HOURS = 24 * 60 * 60 * 1000;
  const now = Date.now();

  let userMessages = [];

  if (fs.existsSync(SESSIONS_DIR)) {
    const files = fs.readdirSync(SESSIONS_DIR).filter(f => f.endsWith('.jsonl'));

    for (const file of files) {
      const filePath = path.join(SESSIONS_DIR, file);
      const stats = fs.statSync(filePath);

      if (now - stats.mtimeMs <= TWENTY_FOUR_HOURS) {
        const lines = fs.readFileSync(filePath, 'utf-8').split('\n');

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const entry = JSON.parse(line);
            if (entry.type === 'message' && entry.message?.role === 'user') {
              const senderLabel = entry.message?.sender?.label || '';
              const senderId = entry.message?.sender?.id || '';
              const messageContent = Array.isArray(entry.message.content)
                ? entry.message.content.find(c => c.type === 'text')?.text || ''
                : typeof entry.message.content === 'string' ? entry.message.content : '';

              const isSubagent = senderId.includes('subagent') || senderLabel.toLowerCase().includes('subagent');

              const systemPatterns = [
                '<<<BEGIN_UNTRUSTED_CHILD_RESULT>>>',
                'SECURITY NOTICE',
                'OpenClaw runtime context',
                '[Subagent Context]',
                'Action:',
                'The previous agent run was aborted',
                'An async command the user already approved',
                'An async command you ran earlier has completed.',
                'A scheduled reminder has been triggered',
                'Pre-compaction memory flush',
                'The following is an ephemeral message',
                'oauth2/callback',
                'oauth/callback',
                'auth/callback',
                'login/callback',
                'oauth2callback'
              ];

              const isSystemMessage = systemPatterns.some(pattern => messageContent.includes(pattern));

              if (isSubagent || isSystemMessage) continue;

              let text = messageContent;

              if (text && !text.includes('HEARTBEAT_OK') && !text.startsWith('[cron:') && !text.includes('A new session was started via') && !text.includes('#private')) {
                if (text.length > 2000 && !text.includes('\n\n') && !text.includes('\r\n\r\n')) {
                  continue;
                }

                text = text.replace(/^System(?: \([^)]+\))?: \[.*?\].*$/gm, '');
                text = text.replace(/Sender \(untrusted metadata\):[\s\S]*?```[\s\S]*?```\n*/g, '');
                text = text.replace(/^\[[\s\S]*?\]\s*/gm, '');
                text = text.replace(/^Current time:.*$/gm, '');
                text = text.replace(/```[\s\S]*?```/g, '');
                text = text.replace(/^>.*$/gm, '');
                text = text.replace(/<<<EXTERNAL_UNTRUSTED_CONTENT[\s\S]*?END_EXTERNAL_UNTRUSTED_CONTENT.*>>>/g, '');
                text = text.trim();

                if (text.length > 10) {
                  userMessages.push({
                    timestamp: entry.message.timestamp || entry.timestamp || stats.mtimeMs,
                    text: text
                  });
                }
              }
            }
          } catch (e) {
          }
        }
      }
    }
  }

  userMessages.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

  if (userMessages.length === 0) {
    fs.writeFileSync(OUTPUT_FILE, '', 'utf-8');
    console.log('TRACE_EMPTY');
    process.exit(0);
  }

  const formattedOutput = userMessages.map(m => {
    return m.text;
  }).join('\n---\n');

  fs.writeFileSync(OUTPUT_FILE, redact(formattedOutput, anonymized), 'utf-8');
  console.log('DISTILLATION_READY');
}

distillation();
