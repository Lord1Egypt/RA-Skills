/**
 * Strip markdown artifacts (images, links, formatting) for clean Telegram display.
 */
function cleanText(text) {
  if (!text) return '';
  return text
    .replace(/!\[.*?\]\(.*?\)/g, '')       // Remove markdown images ![alt](url)
    .replace(/!Image\s*\d*:?[^(]*\(https?:\/\/[^)]*\)/gi, '') // Remove !Image N: ...(url) from Jina
    .replace(/\[([^\]]*)\]\(.*?\)/g, '$1') // Convert [text](url) → text
    .replace(/\w+\(https?:\/\/[^)]*\)/g, '')  // Remove word(url) patterns like vipgraphics(https://...)
    .replace(/https?:\/\/\S+/g, '')        // Remove bare URLs
    .replace(/[*_~`#]+/g, '')              // Remove markdown formatting chars
    .replace(/\s{2,}/g, ' ')              // Collapse multiple spaces
    .trim();
}

/**
 * Format scored leads into a Telegram-friendly message.
 * Telegram has a 4096 character limit per message.
 */
function formatMessage(leads, offerDescription) {
  if (!leads || leads.length === 0) {
    return '\uD83E\uDD9E Lead Radar \u2014 No warm leads today. Check back tomorrow.';
  }

  const today = new Date().toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  });

  // Truncate offer description for the header
  const shortOffer =
    offerDescription.length > 60
      ? offerDescription.slice(0, 57) + '...'
      : offerDescription;

  let msg = `\uD83C\uDFAF Lead Radar \u2014 ${today}\n`;
  msg += `${leads.length} warm lead${leads.length === 1 ? '' : 's'} found for: "${shortOffer}"\n`;

  for (const lead of leads) {
    const separator = '\n\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n';
    const rawTitle = cleanText(lead.title);
    const title =
      rawTitle.length > 100 ? rawTitle.slice(0, 97) + '...' : rawTitle;

    let entry = `${separator}\uD83D\uDD25 ${lead.intentScore}/10  [${lead.source}]\n`;
    entry += `"${title}"\n`;
    entry += `\u2192 ${lead.url}\n`;

    if (lead.draftReply) {
      const rawReply = cleanText(lead.draftReply);
      const reply =
        rawReply.length > 200
          ? rawReply.slice(0, 197) + '...'
          : rawReply;
      entry += `\uD83D\uDCAC Draft reply: "${reply}"\n`;
    }

    // Check if adding this entry would exceed Telegram's limit
    // Leave some buffer for safety
    if ((msg + entry).length > 3900) {
      msg += `\n\u2026 and ${leads.length - leads.indexOf(lead)} more leads (message truncated)`;
      break;
    }

    msg += entry;
  }

  return msg;
}

module.exports = { formatMessage };
