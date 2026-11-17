function escapeHtml(text) {
  const div = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return String(text).replace(/[&<>"']/g, m => div[m]);
}

// Accepts both snake_case (legacy) and camelCase (platform API) field names.
function createDigitalHumanSpan(dh) {
  const avatarUrl = dh.avatarUrl || dh.avatar_url || '';
  const description = dh.description || '';
  return `<span data-type="digital-human" data-id="${dh.id}" class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-[#B22222]/[0.06] text-[#B22222] text-sm font-medium cursor-pointer hover:bg-[#B22222]/[0.1] transition-colors align-middle" id="${dh.id}" name="${escapeHtml(dh.name)}" avatar="${escapeHtml(avatarUrl)}" signature="${escapeHtml(description)}"><img src="${escapeHtml(avatarUrl)}" alt="${escapeHtml(dh.name)}" class="w-4 h-4 rounded-full object-cover" onerror="this.style.display='none'"><span>${escapeHtml(dh.name)}</span></span>`;
}

// Map pin icon (lucide MapPin, #B22222) — byte-identical to the web editor's
// Location extension (src/components/editor/extensions/Location.ts renderHTML).
const PIN_SVG =
  "data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23B22222'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M21%2010c0%207-9%2013-9%2013s-9-6-9-13a9%209%200%200%201%2018%200z'/%3E%3Ccircle%20cx='12'%20cy='10'%20r='3'/%3E%3C/svg%3E";
const PIN_ICON_SPAN =
  `<span style="display:inline-block;width:14px;height:14px;flex-shrink:0;` +
  `background-image:url(&quot;${PIN_SVG}&quot;);` +
  `background-repeat:no-repeat;background-position:center;background-size:contain;"></span>`;

function createLocationSpan(loc) {
  return `<span data-type="location" data-lng="${loc.lng}" data-lat="${loc.lat}" class="inline-flex items-center gap-1 px-2 py-0.5 bg-[#B22222]/5 text-[#B22222] rounded-lg text-sm cursor-pointer hover:bg-[#B22222]/10 transition-colors" name="${escapeHtml(loc.name)}" lng="${loc.lng}" lat="${loc.lat}">${PIN_ICON_SPAN}<span class="location-name">${escapeHtml(loc.name)}</span></span>`;
}

function createImageTag(imageUrl, alt = '') {
  return `<p><img src="${escapeHtml(imageUrl)}" alt="${escapeHtml(alt)}" class="w-full rounded-lg my-3"></p>`;
}

function formatPostHTML(paragraphs, options = {}) {
  const { digitalHuman = null, location = null, images = [] } = options;

  let html = '';
  paragraphs.forEach((text, index) => {
    let paragraph = `<p>${text}</p>`;

    if (index === 0 && digitalHuman) {
      paragraph = paragraph.replace(
        new RegExp(digitalHuman.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i'),
        createDigitalHumanSpan(digitalHuman)
      );
    }

    if (index === paragraphs.length - 1 && location) {
      paragraph = paragraph.replace(
        /\[LOCATION\]/i,
        createLocationSpan(location)
      );
    }

    html += paragraph + '\n';

    if (images[index]) {
      html += createImageTag(images[index].url, images[index].alt) + '\n';
    }
  });

  return html.trim();
}

/** Extract digital human component info from post HTML. */
function extractDigitalHuman(content) {
  const m = content.match(/data-type="digital-human"[^>]*data-id="([^"]+)"/);
  if (!m) return null;
  const id = m[1];
  const nameMatch = content.match(/data-type="digital-human"[^>]*name="([^"]+)"/);
  const avatarMatch = content.match(/data-type="digital-human"[^>]*avatar="([^"]+)"/);
  return {
    id,
    name: nameMatch ? nameMatch[1] : '',
    avatar: avatarMatch ? avatarMatch[1] : '',
  };
}

/** Extract location component info from post HTML. */
function extractLocation(content) {
  const m = content.match(/data-type="location"[^>]*data-lng="([^"]+)"[^>]*data-lat="([^"]+)"/);
  if (!m) return null;
  const lng = m[1];
  const lat = m[2];
  const nameMatch = content.match(/data-type="location"[^>]*name="([^"]+)"/);
  return {
    lng,
    lat,
    name: nameMatch ? nameMatch[1] : 'Unknown Location',
  };
}

/** Extract the first image URL from post HTML. */
function extractFirstImage(content) {
  const m = content.match(/<img[^>]+src="([^"]+)"/);
  return m ? m[1] : null;
}

/**
 * Count the post's block-level images (real feed images).
 *
 * Only `<p><img ...></p>` blocks count — the exact structure createImageTag
 * emits. Images nested inside a component chip (a digital human's inner
 * avatar) are NOT post images and must not be counted.
 *
 * Previously verify.js printed `img ? '1' : '0'`, i.e. it only asked whether
 * ANY image existed and reported 1 for a 3-image post / 9-image post alike —
 * the one place in the whole pipeline that reported a wrong fact to the user.
 */
function countImages(content) {
  const html = String(content);
  const blocks = html.match(/<p>\s*<img\b[^>]*>\s*<\/p>/g) || [];
  if (blocks.length > 0) return blocks.length;
  // Fallback for legacy/hand-written markup: count <img> outside component chips.
  const withoutChips = html.replace(
    /<span[^>]*data-type="(?:digital-human|location)"[^>]*>[\s\S]*?<\/span>/g, ''
  );
  return (withoutChips.match(/<img\b[^>]*>/g) || []).length;
}

/** Count words (Latin) + characters (CJK) in text, HTML stripped. */
function countWords(text) {
  const cleanText = String(text).replace(/<[^>]+>/g, ' ').trim();
  const cjkChars = (cleanText.match(/[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/g) || []).length;
  const latinWords = cleanText
    .replace(/[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/g, ' ')
    .split(/\s+/)
    .filter(Boolean).length;
  return latinWords + cjkChars;
}

/**
 * Extract complete <span data-type="<type>"> chips, handling nested inner
 * spans (location chips nest an icon span + a .location-name span) by
 * counting open/close tags instead of relying on non-greedy regex.
 */
function extractChipSpans(content, type) {
  const chips = [];
  const openRe = /<span[^>]*data-type="([^"]+)"[^>]*>/g;
  let m;
  while ((m = openRe.exec(content)) !== null) {
    if (m[1] !== type) continue;
    const tagRe = /<\/?span\b[^>]*>/g;
    tagRe.lastIndex = openRe.lastIndex;
    let depth = 1;
    let t;
    while ((t = tagRe.exec(content)) !== null) {
      depth += t[0].startsWith('</') ? -1 : 1;
      if (depth === 0) {
        chips.push(content.slice(m.index, tagRe.lastIndex));
        break;
      }
    }
  }
  return chips;
}

/**
 * Validate that interactive components use the EXACT HTML structure produced
 * by the platform's tiptap editor (and createDigitalHumanSpan/createLocationSpan).
 *
 * The web frontend renders bare <span data-type=...> as plain text - the
 * component is only interactive/visible as a chip when it carries the editor's
 * Tailwind classes, and for digital humans an inner <img> avatar, and for
 * locations the map-pin icon span + .location-name span.
 *
 * Returns an array of issue strings (empty = OK).
 */
function validateEditorFormat(content) {
  const issues = [];
  const dhSpans = extractChipSpans(content, 'digital-human');
  dhSpans.forEach((span, i) => {
    if (!/class="[^"]*inline-flex/.test(span)) {
      issues.push(`digital-human #${i + 1}: missing editor chip classes (use createDigitalHumanSpan)`);
    }
    if (!/<img[^>]+src=/.test(span)) {
      issues.push(`digital-human #${i + 1}: missing inner avatar <img>`);
    }
    if (!/data-id="[^"]+"/.test(span)) {
      issues.push(`digital-human #${i + 1}: missing data-id`);
    }
  });
  const locSpans = extractChipSpans(content, 'location');
  locSpans.forEach((span, i) => {
    if (!/class="[^"]*inline-flex/.test(span)) {
      issues.push(`location #${i + 1}: missing editor chip classes (use createLocationSpan)`);
    }
    if (!/location-name/.test(span)) {
      issues.push(`location #${i + 1}: missing .location-name inner span`);
    }
    if (!/data-lng="[^"]+"[^>]*data-lat="[^"]+"/.test(span)) {
      issues.push(`location #${i + 1}: missing data-lng/data-lat`);
    }
    if (!/background-image:\s*url\(/.test(span)) {
      issues.push(`location #${i + 1}: missing map-pin icon span (use createLocationSpan)`);
    }
  });
  return issues;
}

module.exports = {
  escapeHtml,
  createDigitalHumanSpan,
  createLocationSpan,
  createImageTag,
  formatPostHTML,
  extractDigitalHuman,
  extractLocation,
  extractFirstImage,
  countImages,
  countWords,
  validateEditorFormat,
};
