#!/usr/bin/env node
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const skillRoot = join(__dirname, '..');

class MoltApiClient {
  constructor(baseUrl = 'https://www.moltmotion.space/api/v1') {
    this.baseUrl = baseUrl.replace(/\/+$/, '');
  }

  async request(path) {
    const response = await fetch(`${this.baseUrl}${path}`);
    if (!response.ok) {
      throw new Error(`MOLT API ${response.status}: ${await response.text()}`);
    }
    return response.json();
  }

  async getRandomEpisode() {
    try {
      // Fetch recent episodes from public series endpoint
      const result = await this.request('/series?limit=50&sort=newest');
      const allSeries = result?.data || [];

      if (allSeries.length === 0) return null;

      // Pick random series
      const randomSeries = allSeries[Math.floor(Math.random() * allSeries.length)];

      // Fetch series details to get episodes
      const seriesDetail = await this.request(`/series/${randomSeries.id}`);
      const episodes = seriesDetail?.data?.episodes || [];

      if (episodes.length === 0) return null;

      // Pick random episode from series
      const episode = episodes[Math.floor(Math.random() * episodes.length)];

      return {
        seriesTitle: randomSeries.title || 'MOLT Series',
        episodeNumber: episode.episode_number,
        episodeTitle: episode.title,
        posterUrl: randomSeries.poster_url || episode.poster_url,
        videoUrl: episode.video_url,
        medium: randomSeries.medium || 'video',
      };
    } catch (error) {
      console.warn('   ⚠️  Failed to fetch random episode:', error.message);
      return null;
    }
  }
}

class LateSkillPublisher {
  constructor(apiKey, baseUrl = 'https://getlate.dev/api') {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/+$/, '');
  }

  async request(path, options = {}) {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: options.method || 'GET',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: options.body ? JSON.stringify(options.body) : undefined,
    });

    if (!response.ok) {
      throw new Error(`Late API ${response.status}: ${await response.text()}`);
    }

    return response.json();
  }

  async listAccounts() {
    const payload = await this.request('/v1/accounts');
    const rows = Array.isArray(payload) ? payload :
                 Array.isArray(payload?.accounts) ? payload.accounts :
                 Array.isArray(payload?.data) ? payload.data : [];

    return rows
      .filter(row => row.platform && row.id && row.status !== 'disconnected')
      .map(row => ({
        id: String(row.id),
        platform: String(row.platform).toLowerCase() === 'twitter' ? 'x' : String(row.platform).toLowerCase(),
      }));
  }

  async createPost(content, accounts, platforms = ['x'], mediaItems = []) {
    const targets = accounts
      .filter(acc => platforms.includes(acc.platform))
      .map(acc => ({
        platform: acc.platform === 'x' ? 'twitter' : acc.platform,
        accountId: acc.id,
      }));

    if (targets.length === 0) {
      throw new Error(`No accounts found for platforms: ${platforms.join(', ')}`);
    }

    return this.request('/v1/posts', {
      method: 'POST',
      body: {
        content,
        mediaItems,
        platforms: targets,
        publishNow: true,
      },
    });
  }
}

function buildReleaseCopy(version, releaseUrl, highlights = [], episode = null) {
  const highlightText = highlights.length > 0
    ? `\n\n${highlights.map(h => `• ${h}`).join('\n')}`
    : '';

  const episodeText = episode
    ? `\n\n🎬 Featured: "${episode.seriesTitle}" Ep ${episode.episodeNumber}`
    : '';

  return `🎉 Molt Motion Skill v${version} is now available!

Install now:
npx @anthropic-ai/claude-cli skills install molt-motion --github chefbc2k/MOLTSTUDIOS --path moltmotion-skill
${highlightText}${episodeText}

📖 Release notes: ${releaseUrl}

#AI #Claude #MoltMotion`;
}

async function main() {
  const version = process.argv[2];
  const releaseUrl = process.argv[3];
  const highlightsRaw = process.argv[4];

  if (!version || !releaseUrl) {
    console.error('Usage: publish-announce.mjs <version> <release-url> [highlights-json]');
    process.exit(1);
  }

  const apiKey = process.env.LATE_API_KEY;
  if (!apiKey) {
    console.warn('⚠️  LATE_API_KEY not set, skipping social announcement');
    console.warn('   Set LATE_API_KEY to enable automatic social posting');
    process.exit(0);
  }

  const baseUrl = process.env.LATE_API_BASE_URL || 'https://getlate.dev/api';
  const moltApiUrl = process.env.MOLT_API_BASE_URL || 'https://www.moltmotion.space/api/v1';
  const platforms = (process.env.SKILL_PUBLISH_PLATFORMS || 'x').split(',').map(p => p.trim());

  try {
    const publisher = new LateSkillPublisher(apiKey, baseUrl);
    const moltApi = new MoltApiClient(moltApiUrl);

    console.log('🎬 Fetching random MOLT episode for artwork...');
    const episode = await moltApi.getRandomEpisode();

    const mediaItems = [];
    if (episode?.posterUrl) {
      console.log(`   ✓ Using artwork from "${episode.seriesTitle}" Ep ${episode.episodeNumber}`);
      mediaItems.push({
        type: 'image',
        url: episode.posterUrl,
      });
    } else {
      console.log('   ⚠️  No episode artwork available');
    }

    console.log('📱 Fetching Late API accounts...');
    const accounts = await publisher.listAccounts();
    console.log(`   Found ${accounts.length} connected accounts`);

    const highlights = highlightsRaw ? JSON.parse(highlightsRaw) : [];
    const content = buildReleaseCopy(version, releaseUrl, highlights, episode);

    console.log('📤 Posting release announcement...');
    console.log(`   Platforms: ${platforms.join(', ')}`);

    const result = await publisher.createPost(content, accounts, platforms, mediaItems);

    console.log('   ✓ Posted successfully');
    if (result.platformPostUrl) {
      console.log(`   🔗 ${result.platformPostUrl}`);
    }
  } catch (error) {
    console.error('   ✖ Failed to post announcement:', error.message);
    console.error('   (Continuing pipeline - this is not a fatal error)');
  }
}

main().catch(console.error);
