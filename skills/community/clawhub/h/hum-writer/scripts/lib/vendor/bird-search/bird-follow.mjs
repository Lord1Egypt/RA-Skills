#!/usr/bin/env node
/**
 * bird-follow.mjs — Follow X accounts via CreateFriendship GraphQL.
 *
 * Uses the same auth infrastructure as bird-search.mjs (AUTH_TOKEN + CT0).
 * Resolves handles to user IDs via UserByScreenName, then calls CreateFriendship.
 *
 * Usage:
 *   node bird-follow.mjs <handle> [handle2] [handle3] ...
 *
 * Outputs JSON: { results: [ { handle, success, userId, error? }, ... ] }
 */

import { TwitterClientBase } from './lib/twitter-client-base.js';

// UserByScreenName query ID (standard Twitter GraphQL)
const USER_BY_SCREEN_NAME_QUERY_ID = 'sLVLhk0bGj3MVFEKTdax1w';

const USER_FEATURES = {
  hidden_profile_likes_enabled: true,
  hidden_profile_subscriptions_enabled: true,
  rweb_tipjar_consumption_enabled: true,
  responsive_web_graphql_exclude_directive_enabled: true,
  verified_phone_label_enabled: false,
  subscriptions_verification_info_is_identity_verified_enabled: true,
  subscriptions_verification_info_verified_since_enabled: true,
  highlights_tweets_tab_ui_enabled: true,
  responsive_web_twitter_article_notes_tab_enabled: true,
  subscriptions_feature_can_gift_premium: false,
  creator_subscriptions_tweet_preview_api_enabled: true,
  responsive_web_graphql_skip_user_profile_image_extensions_enabled: false,
  responsive_web_graphql_timeline_navigation_enabled: true,
};

class FollowClient extends TwitterClientBase {
  async resolveUserId(screenName) {
    const variables = {
      screen_name: screenName,
      withSafetyModeUserFields: true,
    };
    const params = new URLSearchParams({
      variables: JSON.stringify(variables),
      features: JSON.stringify(USER_FEATURES),
    });

    const url = `https://x.com/i/api/graphql/${USER_BY_SCREEN_NAME_QUERY_ID}/UserByScreenName?${params}`;
    try {
      const resp = await this.fetchWithTimeout(url, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      if (!resp.ok) {
        return { success: false, error: `HTTP ${resp.status}` };
      }

      const data = await resp.json();
      const userId = data?.data?.user?.result?.rest_id;
      if (!userId) {
        return { success: false, error: 'User not found' };
      }
      return { success: true, userId };
    } catch (e) {
      return { success: false, error: String(e) };
    }
  }

  async follow(userId) {
    // Use v1.1 REST API — works with session cookies and same Bearer token
    const body = new URLSearchParams({ user_id: userId, skip_status: 'true' });
    try {
      const resp = await this.fetchWithTimeout(
        'https://x.com/i/api/1.1/friendships/create.json',
        {
          method: 'POST',
          headers: {
            ...this.getBaseHeaders(),
            'content-type': 'application/x-www-form-urlencoded',
          },
          body: body.toString(),
        }
      );

      if (!resp.ok) {
        const text = await resp.text();
        return { success: false, error: `HTTP ${resp.status}: ${text.slice(0, 200)}` };
      }
      const data = await resp.json();
      // v1.1 returns the user object on success, or errors array
      if (data.errors?.length) {
        return { success: false, error: data.errors.map(e => e.message).join(', ') };
      }
      return { success: true };
    } catch (e) {
      return { success: false, error: String(e) };
    }
  }

  async followHandle(handle) {
    const screenName = handle.replace(/^@/, '');
    const resolved = await this.resolveUserId(screenName);
    if (!resolved.success) {
      return { handle, success: false, error: resolved.error };
    }

    const followed = await this.follow(resolved.userId);
    if (!followed.success) {
      return { handle, success: false, userId: resolved.userId, error: followed.error };
    }

    return { handle, success: true, userId: resolved.userId };
  }
}

const args = process.argv.slice(2);
if (!args.length || args[0].startsWith('-')) {
  process.stderr.write('Usage: node bird-follow.mjs <handle> [handle2] ...\n');
  process.exit(1);
}

const cookies = { authToken: process.env.AUTH_TOKEN, ct0: process.env.CT0 };
if (!cookies.authToken || !cookies.ct0) {
  process.stdout.write(JSON.stringify({ error: 'AUTH_TOKEN and CT0 env vars required' }));
  process.exit(1);
}

const client = new FollowClient({ cookies, timeoutMs: 30000 });
const results = [];

for (const handle of args) {
  const result = await client.followHandle(handle);
  results.push(result);
  const status = result.success ? 'OK' : `FAIL: ${result.error}`;
  process.stderr.write(`  @${handle.replace(/^@/, '')}: ${status}\n`);
}

process.stdout.write(JSON.stringify({ results }));
process.exit(results.every(r => r.success) ? 0 : 1);
