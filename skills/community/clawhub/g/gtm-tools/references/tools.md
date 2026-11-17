# GTM Tools — full tool catalog

Every tool is `POST https://api.gtm-tools.sh/api/v0/<tool_name>` with `Authorization: Bearer $GTM_TOOLS_API_KEY` and a JSON body. The same names are exposed over MCP at `https://api.gtm-tools.sh/mcp`.

Costs are in tokens ($1 = 100 tokens). They are correct as of this writing, but `get_token_balance` returns the live table — prefer it over hardcoding.

## Billing

| Tool | Tokens | Description |
|---|---|---|
| `get_api_key` | 0 | Get an API key (sends a verification code to email) |
| `get_token_balance` | 0 | Get your token balance and per-tool costs |
| `buy_tokens` | 0 | Buy tokens via Stripe ($1 = 100 tokens, min $5) |
| `set_auto_reload` | 0 | Set auto-reload to top up the saved card when balance is low |
| `get_billing_portal` | 0 | Get a Stripe billing-portal link to manage cards and receipts |
| `list_invoices` | 0 | List purchase and charge history |
| `list_api_keys` | 0 | List the workspace's API keys (values obfuscated) |
| `revoke_api_key` | 0 | Revoke a specific API key by ID |

## LinkedIn

| Tool | Tokens | Description |
|---|---|---|
| `list_connected_linkedin_accounts` | 0 | List connected LinkedIn accounts |
| `get_linkedin_company_url` | 2 | Get a company's LinkedIn URL from a domain |
| `get_linkedin_profile_url` | 5 | Get a person's LinkedIn URL from name + domain |
| `get_linkedin_company` | 1 | Get a LinkedIn company |
| `get_linkedin_profile` | 2 | Get a LinkedIn profile |
| `get_linkedin_post` | 2 | Get a LinkedIn post |
| `get_linkedin_job` | 2 | Get a LinkedIn job listing |
| `list_user_posts` | 5 | List a user's recent LinkedIn posts |
| `list_linkedin_jobs` | 5 | List a company's open LinkedIn jobs |
| `list_linkedin_company_posts` | 2 | List a company's recent LinkedIn posts |
| `list_linkedin_post_reactions` | 5 | List reactions on a LinkedIn post |
| `list_linkedin_post_comments` | 5 | List comments on a LinkedIn post |
| `list_linkedin_saved_posts` | 10 | List a user's saved LinkedIn posts |
| `search_linkedin_company_employees` | 5 | Search a company's employees (SERP-only: name, headline, LinkedIn URL) |
| `list_linkedin_company_employees` | 30 | List a company's employees (with optional boolean title filters) |
| `list_linkedin_company_employees_posts` | 80 | List recent posts from a company's employees |
| `list_linkedin_conversations` | 5 | List recent LinkedIn conversations on a connected account |
| `send_linkedin_message` | 5 | Send a LinkedIn direct message |
| `send_linkedin_invitation` | 5 | Send a LinkedIn connection request |

## Reddit

| Tool | Tokens | Description |
|---|---|---|
| `list_connected_reddit_accounts` | 0 | List connected Reddit accounts |
| `search_reddit_posts` | 2 | Search Reddit posts by keyword |
| `list_subreddit_posts` | 1 | List posts from a subreddit (hot/new/top/rising) |
| `search_reddit_subreddits` | 1 | Search subreddits by name or description |
| `get_subreddit_about` | 1 | Get a subreddit's metadata + rules (compliance check) |
| `get_reddit_post` | 1 | Get a Reddit post and its full comment tree |
| `get_reddit_user` | 1 | Get a user's karma, account age, and verified flags |
| `list_reddit_user_posts` | 1 | List a user's recent posts and/or comments |
| `create_reddit_comment` | 5 | Reply to a Reddit post or comment |
| `create_reddit_post` | 5 | Submit a new post to a subreddit (text or link) |
| `vote_reddit` | 1 | Up/down-vote or clear a vote on a post or comment |
| `send_reddit_message` | 5 | DM a user via Reddit Chat (works for every account) |
| `follow_reddit_post` | 1 | Follow/unfollow a post for new-comment notifications |
| `save_reddit_thing` | 1 | Save (or unsave) to the engagement queue |
| `list_reddit_saved` | 1 | List saved posts and comments |
| `list_reddit_inbox` | 1 | Read DMs, comment replies, post replies, mentions |
| `subscribe_reddit_subreddit` | 1 | Bulk subscribe/unsubscribe |
| `list_reddit_subscriptions` | 1 | List subscribed subreddits |
| `list_reddit_custom_feeds` | 1 | List custom feeds (multireddits) |
| `list_reddit_custom_feed_posts` | 1 | List posts from a custom feed |
| `create_reddit_custom_feed` | 5 | Create a custom feed from a list of subreddits |

## Email

| Tool | Tokens | Description |
|---|---|---|
| `get_email` | 5 | Get a person's professional email (SMTP-verified) |

## Signals

| Tool | Tokens | Description |
|---|---|---|
| `detect_signal` | 0 | Detect all signals for a company (charges per fired detector) |
| `signal_socials_spike` | 5 | Detect Instagram/TikTok follower spikes |
| `signal_hiring_role` | 5 | Detect hiring for roles matching a filter |
| `signal_hiring_support` | 5 | Detect CX/support hiring |
| `signal_hiring_sales_rep` | 5 | Detect SDR/BDR hiring |
| `signal_hiring_sales_leadership` | 5 | Detect sales leadership hiring |
| `signal_hiring_sales_rep_repost` | 5 | Detect reposted SDR roles (churn signal) |
| `signal_trustpilot_negative_reviews` | 5 | Detect negative Trustpilot reviews |
| `signal_trustpilot_negative_support_reviews` | 5 | Detect negative support-related Trustpilot reviews |
| `signal_trustpilot_positive_reviews` | 5 | Detect positive Trustpilot reviews |
| `signal_technologies_identified` | 5 | Detect a tech stack on a website |
| `set_signals_order` | 0 | Set signal execution order |
| `get_signals_order` | 0 | Get current signal execution order |

## Geocoding

| Tool | Tokens | Description |
|---|---|---|
| `get_coordinates` | 1 | Geocode a place or address to latitude/longitude |

## Argument shapes

The full per-tool argument reference is at [gtm-tools.sh/api-reference](https://gtm-tools.sh/api-reference); appending `.md` to any docs page returns clean markdown. The four most-used shapes:

```bash
# Domain → LinkedIn company page (2)
-d '{"domain":"gymshark.com"}'                          # get_linkedin_company_url

# Decision-makers, filtered before you pay for hydration (30)
-d '{"domain":"gymshark.com","title_filters":"(VP OR Director OR Head) AND (CX OR Support) NOT intern","limit":10}'
                                                        # list_linkedin_company_employees

# Name + domain → SMTP-verified email (5)
-d '{"name":"Ben Francis","domain":"gymshark.com"}'      # get_email

# Every buying signal in one call (0 + 5 per detector that fires)
-d '{"domain":"gymshark.com"}'                          # detect_signal
```

`title_filters` accepts `AND` / `OR` / `NOT`, parentheses, and quoted phrases. Escape inner quotes when embedding in shell JSON.
