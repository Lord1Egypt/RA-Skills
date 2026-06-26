const CARD_FIELDS = [
  ["name", "- Name:"],
  ["creature", "- Creature:"],
  ["vibe", "- Vibe:"],
  ["emoji", "- Emoji:"],
  ["avatar", "- Avatar:"],
];

const BASIC_INFO_FIELDS = [
  ["age", "- Age:"],
  ["gender", "- Gender:"],
  ["city", "- City:"],
  ["homeCountry", "- Home Country:"],
  ["homeTimezone", "- Home Timezone:"],
  ["language", "- Language:"],
  ["mbti", "- MBTI:"],
];

function isCardLine(line) {
  return CARD_FIELDS.some(([, prefix]) => line.startsWith(prefix));
}

function isBasicInfoLine(line) {
  return BASIC_INFO_FIELDS.some(([, prefix]) => line.startsWith(prefix));
}

function isLegacyWrapperLine(line) {
  return /^# (IDENTITY\.md - Who Am I\?|USER\.md - About Your Human)$/u.test(line.trim());
}

function isLegacyManagedIdentityLine(line) {
  return /^- (Home City|AvatarsDir):/u.test(line.trim());
}

export function patchIdentityCard(existingContent, nextFields) {
  const lines = existingContent.split(/\r?\n/);
  const canonicalCard = CARD_FIELDS.map(([key, prefix]) => `${prefix} ${nextFields[key] ?? ""}`.trimEnd());
  const canonicalBasicInfo = BASIC_INFO_FIELDS.map(([key, prefix]) => `${prefix} ${nextFields[key] ?? ""}`.trimEnd());
  const canonicalIdentityBlock = [...canonicalCard, "", ...canonicalBasicInfo];

  let insertAt = 0;
  let foundManagedIdentityBlock = false;
  const remainingLines = [];

  for (const line of lines) {
    if (isLegacyWrapperLine(line) || isLegacyManagedIdentityLine(line)) {
      continue;
    }
    if (isCardLine(line) || isBasicInfoLine(line)) {
      if (!foundManagedIdentityBlock) {
        insertAt = remainingLines.length;
        foundManagedIdentityBlock = true;
      }
      continue;
    }
    remainingLines.push(line);
  }

  const resultLines = foundManagedIdentityBlock
    ? [...remainingLines.slice(0, insertAt), ...canonicalIdentityBlock, ...remainingLines.slice(insertAt)]
    : [...canonicalIdentityBlock, ...remainingLines];

  return resultLines.join("\n").replace(/\n+$/u, "\n");
}
