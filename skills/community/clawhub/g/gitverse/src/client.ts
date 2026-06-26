import { GitVerse } from '@onreza/gitverse-sdk';

let gitverse: GitVerse | null = null;

export function getClient(): GitVerse {
  if (!gitverse) {
    const token = process.env.GITVERSE_TOKEN;
    if (!token) {
      throw new Error('GITVERSE_TOKEN environment variable is required');
    }

    gitverse = new GitVerse({
      token,
      baseUrl: process.env.GITVERSE_BASE_URL || 'https://gitverse.ru/api/v1',
    });
  }

  return gitverse;
}
