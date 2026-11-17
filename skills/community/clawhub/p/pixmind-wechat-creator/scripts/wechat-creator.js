#!/usr/bin/env node

import { randomUUID } from 'crypto';
import { readFile } from 'fs/promises';

const API_BASE = (process.env.PIXMIND_API_BASE_URL || 'https://aihub-admin.aimix.pro')
  .replace(/\/$/, '');

function parseArgs(argv) {
  const options = { sourceUrls: [], inlineImages: [] };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    if (key === 'sourceUrl') {
      options.sourceUrls.push(argv[index + 1]);
      index += 1;
      continue;
    }
    if (key === 'inlineImage') {
      options.inlineImages.push(argv[index + 1]);
      index += 1;
      continue;
    }
    if (index + 1 < argv.length && !argv[index + 1].startsWith('--')) {
      options[key] = argv[index + 1];
      index += 1;
      continue;
    }
    options[key] = true;
  }
  return options;
}

function usage() {
  return `Pixmind WeChat Creator

Usage:
  node wechat-creator.js --topic <topic> --yes [options]
  node wechat-creator.js --project-id <projectId> --yes [--outline-only]

Options:
  --topic <text>             Article topic
  --audience <text>          Target readers
  --goal <text>              Article objective
  --tone <text>              Writing tone
  --language <locale>        zh-CN, zh-TW, or en
  --target-words <number>    300-10000
  --material-file <path>     UTF-8 text or Markdown material
  --source-url <url>         Repeatable public source URL
  --project-id <id>          Resume an existing project
  --request-id <id>          Stable idempotency namespace
  --outline-only             Stop after generating the outline
  --with-images              Generate Pixmind cover and inline image tasks
  --image-model <model>      Optional Pixmind image model override
  --cover-url <url>          Use an existing public HTTPS cover image
  --inline-image <url>       Repeatable existing public HTTPS inline image
  --theme <theme>            classic, graphite, maple, mint, sunrise, lake, newspaper, forest, minimal, editorial, ink, warm, or techno
  --layout <layout>          balanced, compact, airy, or magazine
  --yes                      Confirm paid content generation
`;
}

function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function pollImages(project, apiKey) {
  const tasks = project.images?.tasks || [];
  if (!tasks.length) throw Object.assign(new Error('No image tasks were created'), { code: 'CONTENT_IMAGE_TASKS_MISSING' });
  const deadline = Date.now() + 10 * 60 * 1000;
  while (Date.now() < deadline) {
    const results = await Promise.all(tasks.map(task => request(`/api-platform/v1/tasks/${task.taskId}`, apiKey)));
    const failed = results.find(result => result.status === 'failed');
    if (failed) throw Object.assign(new Error('A Pixmind image task failed. It was not retried.'), { code: 'CONTENT_IMAGE_GENERATION_FAILED' });
    if (results.every(result => result.status === 'ready')) {
      return tasks.map((task, index) => ({ ...task, url: results[index].images?.[0] })).filter(item => item.url);
    }
    progress(`Waiting for ${results.filter(result => result.status !== 'ready').length} image task(s)`);
    await wait(3000);
  }
  throw Object.assign(new Error('Timed out while waiting for image tasks. Query the project before retrying.'), { code: 'CONTENT_IMAGE_TIMEOUT' });
}

async function request(path, apiKey, init = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      ...(init.headers || {}),
    },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok || body.code !== 1000) {
    const error = new Error(body.message || `Pixmind API request failed (${response.status})`);
    error.code = body.code || `HTTP_${response.status}`;
    error.status = response.status;
    throw error;
  }
  return body.data;
}

function progress(message) {
  process.stderr.write(`[pixmind-wechat-creator] ${message}\n`);
}

function idempotencyKey(requestId, operation) {
  return `${requestId}:${operation}`.slice(0, 128);
}

async function mutate(project, operation, requestId, apiKey) {
  progress(`Generating ${operation} for ${project.projectId} at revision ${project.revision}`);
  return request(`/api-platform/v1/content/projects/${encodeURIComponent(project.projectId)}/${operation}`, apiKey, {
    method: 'POST',
    body: JSON.stringify({
      expectedRevision: project.revision,
      idempotencyKey: idempotencyKey(requestId, operation),
    }),
  });
}

function presentation(project) {
  const article = project.article || {};
  const review = project.review || (project.manifest?.contentHtml ? {
    status: 'not_available',
    summary: '审核报告未生成，请在发布前人工核验文章内容。',
  } : null);
  return {
    type: 'document.article',
    version: 1,
    data: {
      platform: 'wechat',
      projectId: project.projectId,
      revision: project.revision,
      status: project.status,
      title: article.title || project.outline?.recommendedTitle || '',
      author: article.author || '',
      digest: article.digest || project.outline?.digest || '',
      contentMarkdown: article.contentMarkdown || '',
      contentHtml: project.manifest?.contentHtml || '',
      coverUrl: project.manifest?.coverUrl || '',
      theme: project.manifest?.theme || '',
      layout: project.manifest?.layout || '',
      imageCount: project.manifest?.inlineAssets?.length || article.imageBriefs?.length || 0,
      sources: article.sources || project.outline?.sources || [],
      outline: project.outline || null,
      review,
    },
    actions: project.manifest?.contentHtml ? [{
      type: 'command',
      action: 'copy.rich-text',
      label: '复制到公众号编辑器',
    }] : [],
  };
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    process.stdout.write(usage());
    return;
  }
  const apiKey = process.env.PIXMIND_API_KEY;
  if (!apiKey) throw Object.assign(new Error('This external-host CLI requires PIXMIND_API_KEY in its process environment. In Pixmind Builder, use pixmind_api_request with the key saved under Settings → Providers → Pixmind instead of running this script.'), { code: 'MISSING_API_KEY' });
  if (!options.projectId && !options.topic) throw new Error('--topic or --project-id is required');

  const requestId = String(options.requestId || `wechat-${randomUUID()}`);
  const materials = options.materialFile
    ? [await readFile(options.materialFile, 'utf8')]
    : [];
  let project = options.projectId
    ? await request(`/api-platform/v1/content/projects/${encodeURIComponent(options.projectId)}`, apiKey)
    : await request('/api-platform/v1/content/projects', apiKey, {
        method: 'POST',
        body: JSON.stringify({
          clientRequestId: requestId,
          brief: {
            topic: options.topic,
            audience: options.audience || '微信公众号读者',
            goal: options.goal || '提供有价值且可发布的内容',
            tone: options.tone || '专业、自然、清晰',
            language: options.language || 'zh-CN',
            targetWords: Number(options.targetWords || 1800),
            materials,
            sourceUrls: options.sourceUrls.filter(Boolean),
          },
        }),
      });

  if (!options.yes) {
    process.stdout.write(`${JSON.stringify({
      type: 'pixmind-wechat-creator-confirmation',
      projectId: project.projectId,
      revision: project.revision,
      requestId,
      requiresConfirmation: true,
      message: 'Outline, article, and review generation use Pixmind API credits. Re-run with --project-id and --yes after approval.',
    }, null, 2)}\n`);
    return;
  }

  if (!project.outline) project = await mutate(project, 'outline', requestId, apiKey);
  if (options.outlineOnly) {
    process.stdout.write(`${JSON.stringify({
      type: 'pixmind-wechat-outline',
      projectId: project.projectId,
      revision: project.revision,
      requestId,
      outline: project.outline,
      presentation: {
        type: 'document.outline',
        version: 1,
        data: { projectId: project.projectId, revision: project.revision, ...project.outline },
      },
    }, null, 2)}\n`);
    return;
  }
  if (!project.article) project = await mutate(project, 'article', requestId, apiKey);
  if (!project.review && !project.manifest && !(project.currentStep === 'review' && project.error)) {
    try {
      project = await mutate(project, 'review', requestId, apiKey);
    } catch (error) {
      project = await request(`/api-platform/v1/content/projects/${encodeURIComponent(project.projectId)}`, apiKey);
      if (!project.article) throw error;
      progress(`Review failed with ${error.code || 'CONTENT_REVIEW_FAILED'}; preserving the article and continuing to unpaid rendering`);
    }
  }

  const wantsImages = options.withImages === true;
  let generatedImages = [];
  if (wantsImages && !options.coverUrl) {
    if (!project.images) {
      project = await request(`/api-platform/v1/content/projects/${encodeURIComponent(project.projectId)}/images`, apiKey, {
        method: 'POST',
        body: JSON.stringify({
          expectedRevision: project.revision,
          idempotencyKey: idempotencyKey(requestId, 'images'),
          ...(options.imageModel ? { model: options.imageModel } : {}),
        }),
      });
    }
    generatedImages = await pollImages(project, apiKey);
  }

  if (!project.manifest) {
    const coverUrl = options.coverUrl || generatedImages.find(image => image.role === 'cover')?.url || '';
    const generatedInline = generatedImages.filter(image => image.role === 'inline').map(image => ({
      url: image.url,
      alt: image.alt || '',
      placement: image.placement || 'end',
    }));
    const suppliedInline = options.inlineImages.filter(Boolean).map((url, index) => ({
      url,
      alt: project.article?.imageBriefs?.[index]?.alt || '',
      placement: project.article?.imageBriefs?.[index]?.placement || 'end',
    }));
    project = await request(`/api-platform/v1/content/projects/${encodeURIComponent(project.projectId)}/render`, apiKey, {
      method: 'POST',
      body: JSON.stringify({
        expectedRevision: project.revision,
        idempotencyKey: idempotencyKey(requestId, 'render'),
        render: {
          coverUrl,
          inlineAssets: suppliedInline.length ? suppliedInline : generatedInline,
          theme: options.theme || 'classic',
          layout: options.layout || 'balanced',
          ...(options.sourceUrls[0] ? { sourceUrl: options.sourceUrls[0] } : {}),
          commentEnabled: options.comments !== 'false',
          onlyFansCanComment: options.onlyFansCanComment === 'true',
        },
      }),
    });
  }

  process.stdout.write(`${JSON.stringify({
    type: 'pixmind-wechat-article',
    projectId: project.projectId,
    revision: project.revision,
    requestId,
    status: project.status,
    outline: project.outline,
    article: project.article,
    review: project.review,
    images: project.images,
    manifest: project.manifest,
    presentation: presentation(project),
  }, null, 2)}\n`);
}

main().catch((error) => {
  process.stdout.write(`${JSON.stringify({
    type: 'pixmind-wechat-creator-error',
    code: error.code || 'CONTENT_CLIENT_ERROR',
    message: error.message || String(error),
    retryable: false,
  }, null, 2)}\n`);
  process.exitCode = 1;
});
