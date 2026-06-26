const EMAIL_REGEX = /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi;

function isReasonableEmail(candidate: string): boolean {
  if (candidate.length > 320) {
    return false;
  }
  if (candidate.includes("..")) {
    return false;
  }

  const [localPart, domainPart] = candidate.split("@");
  if (!localPart || !domainPart) {
    return false;
  }
  if (localPart.startsWith(".") || localPart.endsWith(".")) {
    return false;
  }
  if (domainPart.startsWith("-") || domainPart.endsWith("-")) {
    return false;
  }
  if (!domainPart.includes(".")) {
    return false;
  }
  return true;
}

export function extractEmails(text: string): string[] {
  const unique = new Set<string>();
  for (const match of text.matchAll(EMAIL_REGEX)) {
    const email = match[0].trim().toLowerCase();
    if (isReasonableEmail(email)) {
      unique.add(email);
    }
  }
  return [...unique];
}

