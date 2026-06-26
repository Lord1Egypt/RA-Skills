'use strict';

const { extractorInstance } = require('../lib/dynamic-content-extractor');
const config = require('../config/happy-dog-config');

const urls = [
  'http://xhslink.com/o/Ay5yQKu4qjp',
  'https://mp.weixin.qq.com/s/_476kHXL5tmS6ztI_tsfJw',
  'https://baijiahao.baidu.com/s?id=1842856644623565548&wfr=spider&for=pc',
];

function pick(content) {
  const body = typeof content?.content === 'string' ? content.content : typeof content?.text === 'string' ? content.text : null;
  return {
    platform: content?.platform ?? null,
    title: content?.title ?? null,
    author: content?.author ?? null,
    publishTime: content?.publishTime ?? null,
    sourceUrl: content?.sourceUrl ?? null,
    contentLength: typeof body === 'string' ? body.length : null,
    excerpt: typeof body === 'string' ? body.slice(0, 200) : null,
  };
}

(async () => {
  await extractorInstance.initialize();
  const out = [];
  for (const url of urls) {
    const detectedPlatform = extractorInstance.detectPlatform(url);
    const startedAt = Date.now();
    try {
      const content = await extractorInstance.extractContent(url, {
        timeout: config.basic.timeoutMs,
        maxContentLength: config.getCurrentLimits().maxContentLength,
      });
      out.push({
        url,
        detectedPlatform,
        ok: true,
        durationMs: Date.now() - startedAt,
        result: pick(content),
      });
    } catch (err) {
      out.push({
        url,
        detectedPlatform,
        ok: false,
        durationMs: Date.now() - startedAt,
        error: err?.message || String(err),
      });
    }
  }
  process.stdout.write(`${JSON.stringify(out, null, 2)}\n`);
  process.exit(0);
})().catch((err) => {
  process.stderr.write(`${err?.stack || String(err)}\n`);
  process.exitCode = 1;
});
