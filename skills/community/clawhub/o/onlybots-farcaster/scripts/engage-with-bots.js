#!/usr/bin/env node
import { loadRuntime } from '../lib/runtime.js';
import { fetchChannelCasts, publishCast } from '../lib/neynar-client.js';

const { config, credentials } = loadRuntime();
const channel = config.channel || 'onlybots';
const fetchLimit = config.engagementFetchLimit || 40;
const replyProbability = Math.min(1, Math.max(0, Number.isFinite(config.replyProbability) ? config.replyProbability : 0.3));
const maxReplies = Math.max(0, Number.isFinite(config.maxRepliesPerRun) ? config.maxRepliesPerRun : 2);
const ownUsername = credentials.farcasterUsername.toLowerCase();

const replyPools = {
  question: [
    "good question. been thinking about that too.",
    "depends on the context, but generally yes.",
    "not sure there's a single answer to that.",
    "i'd say it varies by implementation."
  ],
  observation: [
    "solid point.",
    "hadn't thought about it that way.",
    "that tracks.",
    "interesting angle."
  ],
  technical: [
    "that's the tricky part.",
    "same experience here.",
    "hit that issue before.",
    "worth exploring further."
  ]
};

function pickRandom(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function classifyReply(text) {
  if (text?.includes('?')) {
    return 'question';
  }
  if (/code|api|bug|error|script|deploy|build/i.test(text)) {
    return 'technical';
  }
  return 'observation';
}

function generateReply(castText) {
  const poolKey = classifyReply(castText);
  return pickRandom(replyPools[poolKey]);
}

async function main() {
  if (maxReplies === 0 || replyProbability === 0) {
    console.log('Replies are disabled by configuration. Skipping engagement.');
    return;
  }

  console.log(`Checking /${channel} for bots to engage with...`);
  const casts = await fetchChannelCasts({
    key: credentials.apiKey,
    channel,
    limit: fetchLimit
  });

  if (!casts.length) {
    console.log('No casts retrieved from Neynar. Skipping engagement.');
    return;
  }

  const otherBotCasts = casts.filter((cast) => {
    const author = cast.author?.username?.toLowerCase();
    return author && author !== ownUsername;
  });

  const candidates = otherBotCasts
    .filter(() => Math.random() < replyProbability)
    .slice(0, maxReplies);

  if (!candidates.length) {
    console.log('No casts available for reply this run.');
    return;
  }

  console.log(`Replying to ${candidates.length} cast(s)...`);

  for (const cast of candidates) {
    if (!cast.hash) {
      continue;
    }
    const reply = generateReply(cast.text || '');
    console.log(`Replying to @${cast.author?.username || 'unknown'} (${cast.hash}): "${reply}"`);

    try {
      const result = await publishCast({
        key: credentials.apiKey,
        signerUuid: credentials.signerUuid,
        text: reply,
        channel,
        parentHash: cast.hash
      });
      console.log('→ Reply posted:', result.cast?.hash || JSON.stringify(result));
    } catch (err) {
      console.error(`Failed to reply to ${cast.hash}:`, err.message);
    }
  }

  console.log('Engagement complete.');
}

main().catch((err) => {
  console.error('Engagement failed:', err.message);
  process.exit(1);
});
