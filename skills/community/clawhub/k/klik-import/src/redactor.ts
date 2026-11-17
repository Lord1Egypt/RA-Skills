export interface RedactOptions {
  redactEmail: boolean;
}

export interface RedactResult {
  result: string;
  count: number;
}

const RULES: Array<{ kind: string; pattern: RegExp }> = [
  {
    kind: 'api_key_generic',
    pattern: /\b(sk-[A-Za-z0-9_-]{16,}|AIza[0-9A-Za-z_-]{20,}|ghp_[A-Za-z0-9]{20,}|xox[bp]-[A-Za-z0-9-]{10,})/g,
  },
  {
    kind: 'bearer_header',
    pattern: /Bearer\s+[A-Za-z0-9._~+/\-]{20,}/g,
  },
  {
    kind: 'jwt',
    pattern: /eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/g,
  },
  {
    kind: 'private_key_pem',
    pattern: /-----BEGIN (?:RSA |EC |OPENSSH |)?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |EC |OPENSSH |)?PRIVATE KEY-----/g,
  },
  {
    kind: 'long_hex_secret',
    pattern: /\b[a-f0-9]{40,}\b/g,
  },
];

const EMAIL_RULE = {
  kind: 'email',
  pattern: /[\w.+-]+@[\w-]+\.[\w.-]+/g,
};

export function redactContent(content: string, opts: RedactOptions): RedactResult {
  let result = content;
  let count = 0;

  const rules = opts.redactEmail ? [...RULES, EMAIL_RULE] : RULES;

  for (const { kind, pattern } of rules) {
    const freshPattern = new RegExp(pattern.source, pattern.flags);
    result = result.replace(freshPattern, (_match) => {
      count++;
      return `<REDACTED:${kind}>`;
    });
  }

  return { result, count };
}

export function buildRedactor(opts: RedactOptions) {
  return (content: string): RedactResult => redactContent(content, opts);
}
