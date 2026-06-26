#!/usr/bin/env node
/**
 * bird-tweet-detail.mjs — Fetch a tweet with full article body via TweetResultByRestId GraphQL.
 *
 * Uses the same auth infrastructure as bird-search.mjs (AUTH_TOKEN + CT0).
 * Returns the tweet with article.title, article.body (plain text), and article.summary.
 *
 * Usage:
 *   node bird-tweet-detail.mjs <tweet_id>
 */

import { TwitterClientBase } from './lib/twitter-client-base.js';

const QUERY_ID = 'tmhPpO5sDermwYmq3h034A';  // TweetResultByRestId

const FEATURES = {
  creator_subscriptions_tweet_preview_api_enabled: true,
  premium_content_api_read_enabled: false,
  communities_web_enable_tweet_community_results_fetch: true,
  c9s_tweet_anatomy_moderator_badge_enabled: true,
  responsive_web_grok_analyze_button_fetch_trends_enabled: false,
  responsive_web_grok_analyze_post_followups_enabled: true,
  responsive_web_jetfuel_frame: true,
  responsive_web_grok_share_attachment_enabled: true,
  responsive_web_grok_annotations_enabled: true,
  articles_preview_enabled: true,
  responsive_web_edit_tweet_api_enabled: true,
  graphql_is_translatable_rweb_tweet_is_translatable_enabled: true,
  view_counts_everywhere_api_enabled: true,
  longform_notetweets_consumption_enabled: true,
  responsive_web_twitter_article_tweet_consumption_enabled: true,
  content_disclosure_indicator_enabled: true,
  content_disclosure_ai_generated_indicator_enabled: true,
  responsive_web_grok_show_grok_translated_post: true,
  responsive_web_grok_analysis_button_from_backend: true,
  post_ctas_fetch_enabled: true,
  freedom_of_speech_not_reach_fetch_enabled: true,
  standardized_nudges_misinfo: true,
  tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled: true,
  longform_notetweets_rich_text_read_enabled: true,
  longform_notetweets_inline_media_enabled: false,
  profile_label_improvements_pcf_label_in_post_enabled: true,
  responsive_web_profile_redirect_enabled: false,
  rweb_tipjar_consumption_enabled: false,
  verified_phone_label_enabled: false,
  responsive_web_grok_image_annotation_enabled: true,
  responsive_web_grok_imagine_annotation_enabled: true,
  responsive_web_grok_community_note_auto_translation_is_enabled: true,
  responsive_web_graphql_skip_user_profile_image_extensions_enabled: false,
  responsive_web_graphql_timeline_navigation_enabled: true,
  responsive_web_enhance_cards_enabled: false,
};

const FIELD_TOGGLES = {
  withArticleRichContentState: true,
  withArticlePlainText: false,
  withArticleSummaryText: true,
  withArticleVoiceOver: true,
};

/** Extract plain text from Draft.js content_state blocks */
function blocksToText(contentState) {
  if (!contentState?.blocks) return '';
  return contentState.blocks
    .map(b => b.text || '')
    .filter(Boolean)
    .join('\n\n');
}

class TweetResultClient extends TwitterClientBase {
  async fetchTweetResult(tweetId) {
    const variables = {
      tweetId,
      includePromotedContent: true,
      withBirdwatchNotes: true,
      withVoice: true,
      withCommunity: true,
    };

    const params = new URLSearchParams({
      variables: JSON.stringify(variables),
      features: JSON.stringify(FEATURES),
      fieldToggles: JSON.stringify(FIELD_TOGGLES),
    });

    const url = `https://x.com/i/api/graphql/${QUERY_ID}/TweetResultByRestId?${params}`;
    const resp = await this.fetchWithTimeout(url, {
      method: 'GET',
      headers: this.getHeaders(),
    });

    if (!resp.ok) {
      return { success: false, error: `HTTP ${resp.status}: ${(await resp.text()).slice(0, 200)}` };
    }

    const data = await resp.json();
    if (data.errors?.length) {
      return { success: false, error: data.errors.map(e => e.message).join(', ') };
    }

    const result = data?.data?.tweetResult?.result ?? {};
    const legacy = result.legacy ?? {};
    const author = result.core?.user_results?.result?.legacy ?? {};
    const articleRaw = result.article ?? {};
    const articleResult = articleRaw.article_results?.result ?? {};

    // Extract full body from content_state blocks
    const body = blocksToText(articleResult.content_state);
    const summary = articleResult.summary_text ?? null;
    const title = articleResult.title ?? articleRaw.title ?? null;

    const tweet = {
      id: result.rest_id ?? tweetId,
      text: legacy.full_text ?? '',
      author: `@${author.screen_name ?? ''}`,
      display_name: author.name ?? '',
      followers: author.followers_count ?? null,
      following: author.friends_count ?? null,
      bio: author.description ?? null,
      likes: legacy.favorite_count ?? null,
      retweets: legacy.retweet_count ?? null,
      replies: legacy.reply_count ?? null,
      views: result.views?.count ? parseInt(result.views.count) : null,
      url: `https://x.com/${author.screen_name}/status/${result.rest_id ?? tweetId}`,
      timestamp: legacy.created_at ?? null,
      is_article: !!title,
      article: title ? { title, body, summary } : null,
    };

    return { success: true, tweet };
  }
}

const args = process.argv.slice(2);
const tweetId = args[0];

if (!tweetId || tweetId.startsWith('-')) {
  process.stderr.write('Usage: node bird-tweet-detail.mjs <tweet_id>\n');
  process.exit(1);
}

const cookies = { authToken: process.env.AUTH_TOKEN, ct0: process.env.CT0 };
if (!cookies.authToken || !cookies.ct0) {
  process.stdout.write(JSON.stringify({ error: 'AUTH_TOKEN and CT0 env vars required' }));
  process.exit(1);
}

const client = new TweetResultClient({ cookies, timeoutMs: 30000 });
const result = await client.fetchTweetResult(tweetId);
process.stdout.write(JSON.stringify(result));
process.exit(result.success ? 0 : 1);
