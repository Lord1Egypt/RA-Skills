/**
 * Compose a PowPow post HTML file in ONE command.
 *
 * This is the ONLY supported way to build post HTML. It encapsulates the
 * platform editor's exact chip structure (html-formatter.js) so callers
 * never hand-write component spans (which render as plain text).
 *
 * Text file format:
 *   - Paragraphs separated by blank lines
 *   - Optional placeholders inside the text:
 *       {{dh}}   or {{数字人}}   -> digital human chip
 *       {{loc}}  or {{位置}}     -> location chip
 *       {{img}}  or {{图}}       -> image paragraph (consumes --image list in order)
 *
 *   UNKNOWN or MISPLACED placeholders are a HARD ERROR (exit 1), never a
 *   silent deletion. Dropping `{{地点}}` from a sentence would leave broken
 *   text ("我们在坐了一下午") that can reach the live feed unnoticed, because
 *   the skill never relays raw script output to the user. Failing loudly lets
 *   the caller fix the text immediately instead.
 *
 * Usage:
 *   node compose.js --text-file <path> [options]
 *
 * Options:
 *   --dh <id|name:<名称>|auto>   digital human: by ID, by name, or auto-match
 *                                (auto requires --topic)
 *   --topic "<topic>"            topic keywords for --dh auto
 *   --loc <dh>                   use the digital human's own location
 *   --loc <name> --lng <x> --lat <y>   custom location
 *   --image <@local-path|url|search:<keywords>>   repeatable (no fixed limit)
 *                                url also accepts Unsplash photo PAGE links
 *                                (unsplash.com/photos/...) - resolved to a
 *                                direct image URL automatically, key optional
 *   --out <path>                 output HTML (default: post-draft.html)
 *   --no-preview                 skip generating the local preview file
 *   --json                       machine-readable summary
 *
 * Local images (@<path>) are NOT uploaded here. They are recorded in a
 * manifest and referenced as powpow-local://N placeholders; the preview file
 * renders them via file:// URLs. publish.js uploads them at publish time,
 * so revising the draft never touches the server.
 *
 * Outputs:
 *   <out>                    the post HTML (feed this to publish.js)
 *   <out>.preview.html       standalone browser preview approximating chips
 *   <out>.manifest.json      local-image manifest (only when local images exist)
 */
const fs = require('fs');
const path = require('path');
const { api, loadSession, SessionExpiredError } = require('./lib/api-client');
const {
  escapeHtml, createDigitalHumanSpan, createLocationSpan, createImageTag,
  countWords, validateEditorFormat,
} = require('./lib/html-formatter');
const { searchImage, checkImageUrl, isUnsplashPhotoUrl, resolveUnsplashUrl } = require('./search-image');
const { isHealthy, rankByTopic } = require('./lib/dh-match');

const LOCAL_IMG_WARN_COUNT = 200;

function parseArgs(argv) {
  const opts = {
    textFile: null, dh: null, topic: null, loc: null,
    lng: null, lat: null, images: [], out: 'post-draft.html',
    preview: true, json: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    switch (a) {
      case '--text-file': opts.textFile = argv[++i]; break;
      case '--dh': opts.dh = argv[++i]; break;
      case '--topic': opts.topic = argv[++i]; break;
      case '--loc': opts.loc = argv[++i]; break;
      case '--lng': opts.lng = argv[++i]; break;
      case '--lat': opts.lat = argv[++i]; break;
      case '--image': opts.images.push(argv[++i]); break;
      case '--out': opts.out = argv[++i]; break;
      case '--no-preview': opts.preview = false; break;
      case '--json': opts.json = true; break;
      default:
        throw new Error(`Unknown argument: ${a}`);
    }
  }
  return opts;
}

async function resolveDigitalHuman(opts) {
  if (!opts.dh) return null;
  const body = await api('GET', '/api/digital-humans?scope=all');
  const all = body.digitalHumans || [];
  const healthy = all.filter(isHealthy);

  if (opts.dh === 'auto') {
    if (!opts.topic) throw new Error('--dh auto requires --topic "<topic>"');
    const ranked = rankByTopic(all, opts.topic);
    if (ranked.length === 0 || ranked[0].score === 0) {
      throw new Error(
        'No healthy digital human matched the topic. ' +
        'Try: node scripts/list-digital-humans.js "<name>" to search precisely, ' +
        'then pass --dh <id> or --dh name:<名称>.'
      );
    }
    return ranked[0].dh;
  }

  if (opts.dh.startsWith('name:')) {
    const wanted = opts.dh.slice(5).trim();
    const found = healthy.find(dh => dh.name === wanted)
      || healthy.find(dh => dh.name.includes(wanted))
      || healthy.find(dh => wanted.includes(dh.name));
    if (!found) {
      throw new Error(
        `Digital human "${wanted}" not found (or unhealthy). ` +
        'Search precisely with: node scripts/list-digital-humans.js "<name>"'
      );
    }
    return found;
  }

  const byId = all.find(dh => dh.id === opts.dh) || healthy.find(dh => dh.id === opts.dh);
  if (!byId) throw new Error(`Digital human id not found: ${opts.dh}`);
  if (!isHealthy(byId)) console.warn(`  ⚠️ Digital human ${byId.name} looks unhealthy (inactive/test/placeholder avatar).`);
  return byId;
}

function resolveLocation(opts, dh) {
  if (!opts.loc) return null;
  if (opts.loc === 'dh') {
    if (!dh) throw new Error('--loc dh requires --dh to be set');
    if (!dh.locationName || !dh.lng || !dh.lat) {
      throw new Error(`Digital human ${dh.name} has no location. Use --loc <name> --lng <x> --lat <y> instead.`);
    }
    return { name: dh.locationName, lng: dh.lng, lat: dh.lat };
  }
  if (opts.lng === null || opts.lat === null) {
    throw new Error(`Custom location "${opts.loc}" requires --lng and --lat (no geocoding built in).`);
  }
  return { name: opts.loc, lng: opts.lng, lat: opts.lat };
}

async function resolveImages(imageArgs) {
  const resolved = [];
  let localIdx = 0;
  for (const arg of imageArgs) {
    if (arg.startsWith('search:')) {
      const keywords = arg.slice(7).trim();
      const results = await searchImage(keywords, { count: 1 });
      if (results.length === 0) {
        console.warn(`  ⚠️ No image found for "${keywords}" - skipping.`);
      } else {
        resolved.push({ src: results[0].url, alt: results[0].alt, localPath: null });
      }
    } else if (/^https?:\/\//.test(arg)) {
      let src = arg;
      let alt = '';
      // Unsplash photo PAGE links are web pages, not images - resolve them to
      // a direct image URL first (works with or without an API key).
      if (isUnsplashPhotoUrl(arg)) {
        try {
          const resolved = await resolveUnsplashUrl(arg);
          src = resolved.url;
          alt = resolved.alt;
          console.log(`  ✅ Resolved Unsplash photo link -> direct image URL`);
        } catch (err) {
          console.warn(`  ⚠️ ${err.message} - skipping: ${arg}`);
          continue;
        }
      }
      const check = await checkImageUrl(src);
      if (check.ok) {
        resolved.push({ src, alt, localPath: null });
      } else {
        console.warn(`  ⚠️ Image URL rejected (${check.reason}) - skipping: ${src}`);
      }
    } else {
      // Local file: "@<path>" or a bare path that exists on disk.
      // NOT uploaded here - recorded as powpow-local://N; publish.js uploads it.
      const localPath = arg.startsWith('@') ? arg.slice(1) : arg;
      if (fs.existsSync(localPath) && fs.statSync(localPath).isFile()) {
        localIdx++;
        resolved.push({ src: `powpow-local://${localIdx}`, alt: '', localPath: path.resolve(localPath) });
      } else {
        console.warn(`  ⚠️ Unrecognized --image value (expected @<local-path>, URL, or search:<keywords>) - skipping: ${arg}`);
      }
    }
  }
  return resolved;
}

function buildHtml(paragraphs, dh, loc, images) {
  let imageIdx = 0;
  const processed = [];
  const placeholderProblems = [];

  // Pass 1: escape text, split out standalone image paragraphs.
  for (let pi = 0; pi < paragraphs.length; pi++) {
    const html = escapeHtml(paragraphs[pi]);

    // A paragraph that is exactly {{img}} / {{图}} becomes a block image.
    if (/^\s*(\{\{img\}\}|\{\{图\}\})\s*$/.test(html)) {
      if (imageIdx < images.length) {
        processed.push({ type: 'image', html: createImageTag(images[imageIdx].src, images[imageIdx].alt) });
        imageIdx++;
      } else {
        placeholderProblems.push(`第 ${pi + 1} 段：{{img}}/{{图}} 比 --image 条目多（这个位置没有图可用）`);
      }
      continue;
    }
    processed.push({ type: 'text', html });
  }

  // Pass 2: resolve digital human / location placeholders (all occurrences).
  let placedDh = false;
  let placedLoc = false;
  for (const item of processed) {
    if (item.type !== 'text') continue;
    if (/\{\{dh\}\}|\{\{数字人\}\}/.test(item.html)) {
      if (!dh) throw new Error('Text contains {{dh}}/{{数字人}} but no --dh was given.');
      item.html = item.html.replace(/\{\{dh\}\}|\{\{数字人\}\}/g, createDigitalHumanSpan(dh));
      placedDh = true;
    }
    if (/\{\{loc\}\}|\{\{位置\}\}/.test(item.html)) {
      if (!loc) throw new Error('Text contains {{loc}}/{{位置}} but no --loc was given.');
      item.html = item.html.replace(/\{\{loc\}\}|\{\{位置\}\}/g, createLocationSpan(loc));
      placedLoc = true;
    }
  }

  // Pass 3: defaults when a component is configured but was never placed:
  // chip leads the first text paragraph; location trails the last text paragraph.
  const textItems = processed.filter(i => i.type === 'text');
  if (dh && !placedDh) {
    if (textItems.length === 0) throw new Error('Cannot place digital human chip: no text paragraph.');
    textItems[0].html = `${createDigitalHumanSpan(dh)} ${textItems[0].html}`;
  }
  if (loc && !placedLoc) {
    if (textItems.length === 0) throw new Error('Cannot place location chip: no text paragraph.');
    textItems[textItems.length - 1].html = `${textItems[textItems.length - 1].html} ${createLocationSpan(loc)}`;
  }

  // Pass 4: any placeholder still standing is unknown or misplaced (e.g. an
  // inline `{{图}}`, or a typo like `{{地点}}`). This is a HARD ERROR: silently
  // deleting it would leave a broken sentence in the published post that
  // nobody notices, because raw script output is never relayed to the user.
  for (const item of processed) {
    if (item.type !== 'text') continue;
    const leftovers = item.html.match(/\{\{[^}]+\}\}/g) || [];
    for (const l of leftovers) {
      placeholderProblems.push(`无法识别的占位符 ${l}`);
    }
  }
  if (placeholderProblems.length > 0) {
    throw new Error(
      'Placeholder error — refusing to compose (nothing was written):\n' +
      placeholderProblems.map(p => `   - ${p}`).join('\n') + '\n' +
      '   Supported placeholders: {{img}}/{{图}} (must be a standalone paragraph), ' +
      '{{loc}}/{{位置}}, {{dh}}/{{数字人}}.\n' +
      '   Fix the text file and re-run compose.js.'
    );
  }

  // Any unconsumed images are appended at the end.
  while (imageIdx < images.length) {
    processed.push({ type: 'image', html: createImageTag(images[imageIdx].src, images[imageIdx].alt) });
    imageIdx++;
  }

  return processed.map(i => (i.type === 'text' ? `<p>${i.html}</p>` : i.html)).join('\n');
}

const PREVIEW_CSS = `body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:640px;margin:0 auto;padding:20px;background:#f5f5f5}
.post{background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,.1)}
p{line-height:1.6;color:#333;margin:0 0 16px 0}
img{width:100%;border-radius:8px;margin:12px 0}
span[data-type="digital-human"]{display:inline-flex;align-items:center;gap:6px;padding:2px 10px;background:rgba(178,34,34,.06);color:#B22222;border-radius:999px;font-size:14px;font-weight:500;cursor:pointer}
span[data-type="digital-human"] img{width:16px;height:16px;border-radius:50%;margin:0}
span[data-type="location"]{display:inline-flex;align-items:center;gap:4px;padding:2px 10px;background:rgba(178,34,34,.05);color:#B22222;border-radius:8px;font-size:14px;cursor:pointer}
.map-notice{background:#fff8f5;border:1px solid rgba(178,34,34,.25);color:#8a1c1c;border-radius:8px;padding:10px 14px;margin-bottom:12px;font-size:13px;line-height:1.6}
.map-notice b{font-weight:600}
.map-notice .sub{color:#a05a5a;font-size:12px}
.note{font-size:12px;color:#999;margin-top:12px}`;

function buildPreview(contentHtml, loc) {
  const mapNotice = loc
    ? `<div class="map-notice"><b>这条帖子会出现在公开地图上</b><br>`
      + `<span class="sub">地点：${escapeHtml(loc.name)}（${loc.lng}, ${loc.lat}）· 会随时间过气，别人点赞可以把它救活</span></div>`
    : `<div class="map-notice">这条帖子没有带地点，不会出现在公开地图上。</div>`;
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>PowPow 帖子预览 · 本地近似还原</title>
<style>${PREVIEW_CSS}</style>
</head>
<body>
${mapNotice}
<div class="post">
${contentHtml}
</div>
<p class="note">本页是本地近似还原，与平台的实际渲染可能存在差异；最终效果以发布后的帖子页为准。</p>
</body>
</html>
`;
}

/** Replace powpow-local://N placeholders with file:// URLs for the local preview. */
function localizePreview(content, images) {
  let preview = content;
  for (const img of images) {
    if (!img.localPath) continue;
    const fileUrl = encodeURI(`file:///${img.localPath.replace(/\\/g, '/')}`);
    preview = preview.split(img.src).join(fileUrl);
  }
  return preview;
}

async function main() {
  let opts;
  try {
    opts = parseArgs(process.argv.slice(2));
  } catch (err) {
    console.error(`❌ ${err.message}\n\nUsage: node compose.js --text-file <path> [--dh ...] [--loc ...] [--image ...] [--out <path>]`);
    process.exit(1);
  }

  if (!opts.textFile) {
    console.error('Usage: node compose.js --text-file <path> [--dh <id|name:<名称>|auto>] [--topic "<topic>"] [--loc <dh|name> --lng x --lat y] [--image <@local-path|url|search:kw>] [--out <path>]');
    process.exit(1);
  }
  if (!fs.existsSync(opts.textFile)) {
    console.error(`❌ Text file not found: ${opts.textFile}`);
    process.exit(1);
  }
  // Pure argument validation BEFORE the session gate, so bad arguments
  // never surface as misleading "session expired" errors.
  if (opts.dh === 'auto' && !opts.topic) {
    console.error('❌ --dh auto requires --topic "<topic>"');
    process.exit(1);
  }

  const raw = fs.readFileSync(opts.textFile, 'utf-8').replace(/^\uFEFF/, '').replace(/\r\n/g, '\n');
  const paragraphs = raw.split(/\n\s*\n/).map(p => p.trim().split('\n').join(' ')).filter(Boolean);
  if (paragraphs.length === 0) {
    console.error('❌ Text file contains no paragraphs (paragraphs are separated by blank lines).');
    process.exit(1);
  }

  try {
    // Session is only required when a digital human must be resolved via API.
    if (opts.dh && !loadSession()) {
      throw new SessionExpiredError();
    }

    console.log('Composing PowPow post...');
    const dh = await resolveDigitalHuman(opts);
    if (dh) console.log(`  Digital human: ${dh.name} (${dh.id})`);
    const loc = resolveLocation(opts, dh);
    if (loc) console.log(`  Location: ${loc.name} (${loc.lng}, ${loc.lat})`);
    const images = await resolveImages(opts.images);
    images.forEach(img => {
      if (img.localPath) console.log(`  Image (local, uploaded at publish time): ${img.localPath}`);
      else console.log(`  Image: ${img.src}`);
    });
    if (images.length >= LOCAL_IMG_WARN_COUNT) {
      console.warn(`  ⚠️ ${images.length} images: the platform bounds content at 50000 chars (each image tag is ~100 chars). Consider fewer.`);
    }

    const content = buildHtml(paragraphs, dh, loc, images);

    const issues = validateEditorFormat(content);
    if (issues.length > 0) {
      console.error('❌ Generated HTML failed editor-format validation (this is a bug in compose.js):');
      issues.forEach(i => console.error(`   - ${i}`));
      process.exit(1);
    }

    const words = countWords(content);
    if (content.length > 50000) {
      console.error(`❌ Content too long: ${content.length} chars (platform limit 50000).`);
      process.exit(1);
    }

    fs.writeFileSync(opts.out, content, 'utf-8');
    if (opts.preview) {
      fs.writeFileSync(`${opts.out}.preview.html`, buildPreview(localizePreview(content, images), loc), 'utf-8');
    }

    // Manifest of local images for publish.js to upload at publish time.
    const manifestPath = `${opts.out}.manifest.json`;
    const localImages = images
      .filter(img => img.localPath)
      .map(img => ({ key: img.src, path: img.localPath }));
    if (localImages.length > 0) {
      fs.writeFileSync(manifestPath, JSON.stringify({ version: 1, localImages }, null, 2), 'utf-8');
    } else if (fs.existsSync(manifestPath)) {
      fs.unlinkSync(manifestPath); // stale manifest from a previous draft
    }

    const summary = {
      file: path.resolve(opts.out),
      previewFile: opts.preview ? path.resolve(`${opts.out}.preview.html`) : null,
      wordCount: words,
      contentChars: content.length,
      digitalHuman: dh ? { id: dh.id, name: dh.name } : null,
      location: loc ? { name: loc.name, lng: loc.lng, lat: loc.lat } : null,
      imageCount: images.length,
      localImageCount: localImages.length,
      manifestFile: localImages.length > 0 ? path.resolve(manifestPath) : null,
    };

    if (opts.json) {
      console.log(JSON.stringify(summary, null, 2));
    } else {
      console.log('\n✅ Post HTML composed');
      console.log(`   File: ${summary.file}`);
      if (summary.previewFile) console.log(`   Preview (open in browser): ${summary.previewFile}`);
      console.log(`   Words: ${words} | Images: ${images.length} (${localImages.length} local, upload deferred to publish) | Chars: ${content.length}`);
      console.log(`\nNext: node scripts/publish.js ${opts.out}`);
    }
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      console.error(`❌ ${err.message}`);
      process.exitCode = 2;
      return;
    }
    console.error(`❌ Compose failed: ${err.message}`);
    process.exitCode = 1;
  }
}

main();
