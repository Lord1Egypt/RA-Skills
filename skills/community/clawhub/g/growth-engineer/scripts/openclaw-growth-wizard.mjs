#!/usr/bin/env node
import { existsSync, promises as fs } from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline/promises';
import { emitKeypressEvents } from 'node:readline';
import { createPrivateKey } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { buildOpenClawCronAddCommand, buildHermesCronCreateCommand, buildGrowthRunnerCommand, deriveSchedulerProofPathFromStatePath, deriveStatePathFromConfigPath, buildExtraSourceConfig, getAutomationConfig, getDefaultSourceCommand, getDefaultSourcePath, inspectHermesCronInstall, inspectOpenClawCronInstall, } from './openclaw-growth-shared.mjs';
import { loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';
const DEFAULT_CONFIG_PATH = 'data/openclaw-growth-engineer/config.json';
const SELF_UPDATE_SKILL_SLUG_CANDIDATES = ['growth-engineer', 'openclaw-growth-engineer'];
const ENABLE_ISOLATED_SECRET_RUNNER_WIZARD = false;
const DEFAULT_GROWTH_INTERVAL_MINUTES = 90;
const DEFAULT_CONNECTOR_HEALTH_INTERVAL_MINUTES = 360;
const DEFAULT_SCHEDULER_PROOF_PATH = 'data/openclaw-growth-engineer/runtime/scheduler-proof.jsonl';
const DELETE_SECRET = '__OPENCLAW_DELETE_SECRET__';
const GROWTH_ENGINEER_PACKAGE_SPEC = process.env.OPENCLAW_GROWTH_ENGINEER_PACKAGE || '@analyticscli/growth-engineer';
const RUNTIME_DIR = path.dirname(fileURLToPath(import.meta.url));
const HEARTBEAT_MARKER_START = '<!-- openclaw-growth-engineer:start -->';
const HEARTBEAT_MARKER_END = '<!-- openclaw-growth-engineer:end -->';
const ACCOUNT_SIGNAL_CONNECTOR_KEYS = [
    'stripe',
    'lemonsqueezy',
    'adapty',
    'superwall',
    'google-play',
    'datadog',
    'bugsnag',
    'intercom',
    'zendesk',
    'apple-search-ads',
    'google-ads',
    'meta-ads',
    'tiktok-ads',
    'vercel',
    'cloudflare',
    'resend',
    'customerio',
    'mailchimp',
    'appfollow',
    'apptweak',
    'linear',
    'postiz',
];
const CONNECTOR_KEYS = [
    'analytics',
    'github',
    'revenuecat',
    'paddle',
    'seo',
    'sentry',
    'coolify',
    'asc',
    ...ACCOUNT_SIGNAL_CONNECTOR_KEYS,
];
class WizardAbortError extends Error {
    exitCode;
    constructor(message, exitCode = 130) {
        super(message);
        this.name = 'WizardAbortError';
        this.exitCode = exitCode;
    }
}
class WizardBackError extends Error {
    constructor(message = 'Go back') {
        super(message);
        this.name = 'WizardBackError';
    }
}
const CONNECTOR_DEFINITIONS = [
    {
        key: 'analytics',
        label: 'AnalyticsCLI product analytics',
        summary: 'Read product events, funnels, retention, users, and feedback.',
        needs: 'An AnalyticsCLI readonly token from dash.analyticscli.com.',
    },
    {
        key: 'github',
        label: 'GitHub code access',
        summary: 'Read repo context and optionally create issues or draft PRs.',
        needs: 'Create a GitHub token with the scopes you want; you can change it later by rerunning the wizard.',
    },
    {
        key: 'revenuecat',
        label: 'RevenueCat monetization data',
        summary: 'Read subscription, product, entitlement, and revenue context.',
        needs: 'A RevenueCat v2 secret API key with read-only project permissions.',
    },
    {
        key: 'paddle',
        label: 'Paddle Billing metrics',
        summary: 'Read web checkout, revenue, MRR, refunds, chargebacks, and active subscriber metrics.',
        needs: 'A scoped Paddle API key for the live account with metrics.read permission.',
    },
    {
        key: 'seo',
        label: 'SEO / GSC / DataForSEO',
        summary: 'Read organic search demand, GSC clicks/impressions/CTR/position, and optional capped DataForSEO keyword ideas.',
        needs: 'A GSC property plus an access token/service-account credential. DataForSEO credentials are optional and paid.',
    },
    {
        key: 'sentry',
        label: 'Sentry-compatible crash monitoring',
        summary: 'Read unresolved crashes, regressions, affected users, releases, and production stability signals.',
        needs: 'A Sentry or GlitchTip-compatible auth token plus the org slug. Project scope is inferred later from app context or config.',
    },
    {
        key: 'coolify',
        label: 'Coolify deployment monitoring',
        summary: 'Read applications, deployments, servers, resources, and production health-check gaps.',
        needs: 'A Coolify API token with read-only permissions from Keys & Tokens / API tokens.',
    },
    {
        key: 'asc',
        label: 'ASC / App Store Connect CLI',
        summary: 'Read App Store analytics, reviews/ratings, builds/TestFlight/release context, subscriptions, purchases, and crash totals.',
        needs: 'Two App Store Connect API keys: a Sales and Reports or Finance key for ongoing use, plus a temporary Admin key for one-time analytics bootstrap.',
    },
    {
        key: 'stripe',
        label: 'Stripe billing and checkout',
        summary: 'Read web payments, subscriptions, trials, invoices, refunds, disputes, coupons, and checkout conversion context.',
        needs: 'An account-level Stripe restricted key or secret key with read access to customers, subscriptions, invoices, balance, charges, disputes, prices, products, coupons, and checkout sessions.',
    },
    {
        key: 'lemonsqueezy',
        label: 'Lemon Squeezy sales and licensing',
        summary: 'Read stores, products, variants, orders, subscriptions, discounts, license keys, and churn/revenue context.',
        needs: 'A live-mode Lemon Squeezy API key from account settings.',
    },
    {
        key: 'adapty',
        label: 'Adapty subscriptions and paywalls',
        summary: 'Read mobile subscription, paywall, product, profile, attribution, and revenue signals across Adapty apps.',
        needs: 'An Adapty server-side API key from dashboard app settings. App/project scope is left unpinned.',
    },
    {
        key: 'superwall',
        label: 'Superwall paywall experiments',
        summary: 'Read paywalls, products, placements/campaigns, experiments, subscription outcomes, and conversion evidence.',
        needs: 'A Superwall organization API key with read scopes.',
    },
    {
        key: 'google-play',
        label: 'Google Play Console',
        summary: 'Read Android store, release, review, subscription, in-app purchase, and order signals across accessible apps.',
        needs: 'A Play Console service account JSON credential with account-level read/reporting access.',
    },
    {
        key: 'datadog',
        label: 'Datadog observability',
        summary: 'Read RUM, logs, errors, APM, monitors, incidents, deployment, and reliability signals.',
        needs: 'Datadog API and application keys plus the Datadog site.',
    },
    {
        key: 'bugsnag',
        label: 'Bugsnag crash monitoring',
        summary: 'Read error, release, session, stability, and affected-user signals across visible projects.',
        needs: 'A Bugsnag data-access auth token with read access.',
    },
    {
        key: 'intercom',
        label: 'Intercom support and feedback',
        summary: 'Read conversations, tickets, contacts, companies, support themes, and onboarding friction signals.',
        needs: 'An Intercom private app access token for the workspace.',
    },
    {
        key: 'zendesk',
        label: 'Zendesk support and feedback',
        summary: 'Read support tickets, tags, CSAT, customer friction, cancellation themes, and help-center signals.',
        needs: 'Zendesk subdomain, agent/admin email, and API token or OAuth token.',
    },
    {
        key: 'apple-search-ads',
        label: 'Apple Search Ads (experimental)',
        summary: 'Read iOS paid search campaigns, spend, installs, taps, CPT/CPA, keywords, and campaign quality signals.',
        needs: 'Apple Ads OAuth client credentials or a current access/refresh token with account-level reporting access.',
        experimental: true,
    },
    {
        key: 'google-ads',
        label: 'Google Ads (experimental)',
        summary: 'Read paid search/app campaign spend, clicks, conversions, CAC, ROAS, and landing-page/ad-group signals.',
        needs: 'Google Ads developer token plus OAuth client/refresh token credentials with account-wide read access.',
        experimental: true,
    },
    {
        key: 'meta-ads',
        label: 'Meta Ads (experimental)',
        summary: 'Read Facebook/Instagram campaign, ad set, creative, spend, conversion, CAC, and ROAS signals.',
        needs: 'A Meta access token with Marketing API read permissions for the ad accounts you want analyzed.',
        experimental: true,
    },
    {
        key: 'tiktok-ads',
        label: 'TikTok Ads (experimental)',
        summary: 'Read TikTok campaign, ad group, creative, spend, conversion, CAC, and ROAS signals.',
        needs: 'TikTok Business API app credentials and access token with advertiser reporting access.',
        experimental: true,
    },
    {
        key: 'vercel',
        label: 'Vercel deployments (experimental)',
        summary: 'Read projects, deployments, build failures, domains, environment health, and frontend reliability signals.',
        needs: 'A Vercel access token with read access across the team/account.',
        experimental: true,
    },
    {
        key: 'cloudflare',
        label: 'Cloudflare traffic and edge (experimental)',
        summary: 'Read zones/accounts, traffic, cache, Workers/Pages, WAF/security, DNS, and edge reliability signals.',
        needs: 'A Cloudflare API token with account/zone read scopes for analytics, Workers/Pages, DNS, and security events as needed.',
        experimental: true,
    },
    {
        key: 'resend',
        label: 'Resend lifecycle email (experimental)',
        summary: 'Read domains, broadcasts, transactional email volume, bounces, complaints, and deliverability signals.',
        needs: 'A Resend API key with account-wide read access where available.',
        experimental: true,
    },
    {
        key: 'customerio',
        label: 'Customer.io lifecycle messaging (experimental)',
        summary: 'Read campaigns, broadcasts, journeys, segments, deliveries, conversions, and lifecycle engagement signals.',
        needs: 'Customer.io App API credentials for the workspace.',
        experimental: true,
    },
    {
        key: 'mailchimp',
        label: 'Mailchimp lifecycle email (experimental)',
        summary: 'Read audiences, campaigns, automations, ecommerce, unsubscribes, bounces, and lifecycle performance signals.',
        needs: 'A Mailchimp Marketing API key for the account.',
        experimental: true,
    },
    {
        key: 'appfollow',
        label: 'AppFollow reviews and ASO (experimental)',
        summary: 'Read app reviews, ratings, semantic review themes, ASO positions, and competitor/app collection signals.',
        needs: 'An AppFollow API token from the API Dashboard with account/app collection read access.',
        experimental: true,
    },
    {
        key: 'apptweak',
        label: 'AppTweak ASO intelligence (experimental)',
        summary: 'Read keyword rankings, ASO metadata, competitor movement, category ranks, and store visibility signals.',
        needs: 'An AppTweak API token from an account with API access.',
        experimental: true,
    },
    {
        key: 'linear',
        label: 'Linear planning context (experimental)',
        summary: 'Read teams, projects, issues, cycles, labels, roadmap context, and delivery bottleneck signals.',
        needs: 'A Linear personal API key or OAuth access token with read access across the workspace.',
        experimental: true,
    },
    {
        key: 'postiz',
        label: 'Postiz social publishing (experimental)',
        summary: 'Read social integrations, scheduled/published posts, platform analytics, posting cadence, and content distribution signals.',
        needs: 'A Postiz Public API key from Settings -> Developers -> Public API. Self-hosted installs can also set a custom API base URL.',
        experimental: true,
    },
];
const ACCOUNT_SIGNAL_CONNECTOR_DEFINITIONS = [
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'stripe'),
        key: 'stripe',
        service: 'stripe',
        docsUrl: 'https://docs.stripe.com/keys',
        sourceKind: 'revenue',
        signalHint: 'Stripe account summary with payments, subscriptions, trials, invoices, refunds, disputes, coupons, checkout sessions, product/price changes, and churn/revenue deltas. Do not pin a single product or price unless the agent explicitly narrows a later run.',
        steps: [
            'Open Stripe Dashboard -> Developers -> API keys.',
            'Create a restricted key for OpenClaw/Growth Engineer, or use a standard secret key only when restricted keys are not practical.',
            'Prefer live-mode read permissions for Customers, Subscriptions, Invoices, Charges, Balance, Disputes, Prices, Products, Coupons, Promotion Codes, and Checkout Sessions.',
            'Do not select a single product, price, or connected account in the wizard. Account-wide access lets the agent discover the relevant products later.',
            'Copy the key once and paste it into this local terminal.',
        ],
        credentials: [{ env: 'STRIPE_API_KEY', prompt: 'Paste STRIPE_API_KEY into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'lemonsqueezy'),
        key: 'lemonsqueezy',
        service: 'lemonsqueezy',
        docsUrl: 'https://docs.lemonsqueezy.com/guides/developer-guide/getting-started',
        sourceKind: 'revenue',
        signalHint: 'Lemon Squeezy account summary with stores, products, variants, orders, subscriptions, discounts, license keys, refunds, and revenue/churn movement. Keep store/product filtering out of setup so the agent can inspect all accessible stores.',
        steps: [
            'Open Lemon Squeezy Dashboard -> Settings -> API.',
            'Create a new API key in live mode for production revenue evidence.',
            'Keep the key private and store it only in this local wizard.',
            'Do not enter a store ID or product ID here; the agent should discover accessible stores from the account.',
            'Copy the key and paste it below.',
        ],
        credentials: [{ env: 'LEMON_SQUEEZY_API_KEY', prompt: 'Paste LEMON_SQUEEZY_API_KEY into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'adapty'),
        key: 'adapty',
        service: 'adapty',
        docsUrl: 'https://adapty.io/docs/api-adapty',
        sourceKind: 'revenue',
        signalHint: 'Adapty summary with apps, paywalls, placements, products, profiles, access levels, subscriptions, attribution, conversion, renewals, cancellations, and revenue signals. Leave app scope unpinned.',
        steps: [
            'Open Adapty Dashboard.',
            'Go to App Settings -> General -> API keys.',
            'Copy the server-side API key for read access.',
            'Do not paste an app ID, product ID, or paywall ID here; the agent can discover visible apps/paywalls later.',
            'Paste the API key into this local terminal.',
        ],
        credentials: [{ env: 'ADAPTY_API_KEY', prompt: 'Paste ADAPTY_API_KEY into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'superwall'),
        key: 'superwall',
        service: 'superwall',
        docsUrl: 'https://api.superwall.com/docs',
        sourceKind: 'revenue',
        signalHint: 'Superwall organization summary with paywalls, placements, campaigns, products, experiments, subscription outcomes, conversion movement, and pricing/package signals. Keep project/paywall scope discoverable.',
        steps: [
            'Open Superwall dashboard.',
            'Create or copy an organization API key with read scopes.',
            'Use organization-wide access so OpenClaw/Hermes can inspect all relevant paywalls and experiments.',
            'Do not enter a paywall, campaign, placement, or product ID in setup.',
            'Paste the organization API key below.',
        ],
        credentials: [{ env: 'SUPERWALL_API_KEY', prompt: 'Paste SUPERWALL_API_KEY into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'google-play'),
        key: 'google-play',
        service: 'google-play',
        docsUrl: 'https://developer.android.com/google/play/developer-api',
        sourceKind: 'store',
        signalHint: 'Google Play account summary with accessible apps, releases, reviews, ratings, Android vitals, subscriptions, in-app products, orders, cancellation reasons, and store/acquisition signals. Do not pin package names during setup.',
        steps: [
            'Open Play Console -> Setup -> API access.',
            'Link or create a Google Cloud project and service account if needed.',
            'Grant read/reporting permissions that cover the apps you want analyzed, including financial/order data only when revenue analysis is desired.',
            'Save the service-account JSON on this host or paste the JSON into a secret env outside chat.',
            'Do not enter a package name in this wizard; accessible apps are discovered from the account.',
        ],
        credentials: [
            {
                env: 'GOOGLE_PLAY_SERVICE_ACCOUNT_JSON',
                prompt: 'Paste GOOGLE_PLAY_SERVICE_ACCOUNT_JSON path or JSON content into this local terminal',
            },
        ],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'datadog'),
        key: 'datadog',
        service: 'datadog',
        docsUrl: 'https://docs.datadoghq.com/account_management/api-app-keys/',
        sourceKind: 'crash',
        signalHint: 'Datadog account summary with RUM, logs, errors, APM, monitors, incidents, deploy markers, performance regressions, and affected-user reliability signals. Do not pin services during setup.',
        steps: [
            'Open Datadog -> Organization Settings -> API Keys and Application Keys.',
            'Create an API key and an application key with read scopes for RUM/logs/APM/monitors/incidents as needed.',
            'Choose the Datadog site for your account, for example datadoghq.com or datadoghq.eu.',
            'Do not enter service names, env names, or monitor IDs here; the agent can discover them later.',
            'Paste the keys below.',
        ],
        credentials: [
            { env: 'DATADOG_API_KEY', prompt: 'Paste DATADOG_API_KEY into this local terminal' },
            { env: 'DATADOG_APP_KEY', prompt: 'Paste DATADOG_APP_KEY into this local terminal' },
            { env: 'DATADOG_SITE', prompt: 'Datadog site', optional: true, defaultValue: process.env.DATADOG_SITE || 'datadoghq.com' },
        ],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'bugsnag'),
        key: 'bugsnag',
        service: 'bugsnag',
        docsUrl: 'https://docs.bugsnag.com/api/',
        sourceKind: 'crash',
        signalHint: 'Bugsnag account summary with organizations, projects, errors, releases, stability score, sessions, affected users, and crash/regression signals. Project scope stays discoverable.',
        steps: [
            'Open Bugsnag settings and create or copy a data-access auth token.',
            'Grant read access for organizations/projects you want analyzed.',
            'Do not enter a project ID in this wizard.',
            'Paste the token below.',
        ],
        credentials: [{ env: 'BUGSNAG_AUTH_TOKEN', prompt: 'Paste BUGSNAG_AUTH_TOKEN into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'intercom'),
        key: 'intercom',
        service: 'intercom',
        docsUrl: 'https://developers.intercom.com/building-apps/docs/authentication',
        sourceKind: 'feedback',
        signalHint: 'Intercom workspace summary with conversations, tickets, contacts, companies, tags, support themes, onboarding friction, cancellation language, and customer feedback loops.',
        steps: [
            'Open Intercom Developer Hub and create or open a private app for your own workspace.',
            'Go to Configure -> Authentication.',
            'Copy the access token for that workspace.',
            'Do not enter workspace-specific filters, tags, or inbox IDs here; the agent can discover relevant support surfaces later.',
            'Paste the token below.',
        ],
        credentials: [{ env: 'INTERCOM_ACCESS_TOKEN', prompt: 'Paste INTERCOM_ACCESS_TOKEN into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'zendesk'),
        key: 'zendesk',
        service: 'zendesk',
        docsUrl: 'https://developer.zendesk.com/api-reference/introduction/security-and-auth/',
        sourceKind: 'feedback',
        signalHint: 'Zendesk account summary with tickets, tags, views, CSAT, help-center signals, support themes, cancellation/friction language, and customer feedback loops.',
        steps: [
            'Open Zendesk Admin Center -> Apps and integrations -> APIs -> Zendesk API.',
            'Create or copy an API token, or use an OAuth token if that is your workspace standard.',
            'Use the account subdomain and an agent/admin email that can read support data.',
            'Do not enter view IDs, brand IDs, product IDs, or ticket tags in setup.',
            'Paste the account credentials below.',
        ],
        credentials: [
            { env: 'ZENDESK_SUBDOMAIN', prompt: 'Zendesk subdomain, for example mycompany', defaultValue: process.env.ZENDESK_SUBDOMAIN || '' },
            { env: 'ZENDESK_EMAIL', prompt: 'Zendesk agent/admin email', defaultValue: process.env.ZENDESK_EMAIL || '' },
            { env: 'ZENDESK_API_TOKEN', prompt: 'Paste ZENDESK_API_TOKEN into this local terminal' },
        ],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'apple-search-ads'),
        key: 'apple-search-ads',
        service: 'apple-search-ads',
        docsUrl: 'https://developer.apple.com/documentation/apple_ads/implementing-oauth-for-the-apple-search-ads-api',
        sourceKind: 'acquisition',
        signalHint: 'Experimental Apple Search Ads account summary with organizations, campaigns, ad groups, keywords, spend, taps, installs, CPT/CPA, ROAS, and iOS paid-search acquisition quality. Keep campaign/app IDs out of setup so the agent can discover accessible accounts later.',
        steps: [
            'Open Apple Search Ads / Apple Ads API access for the account.',
            'Create OAuth credentials or copy an existing refresh/access token from your server-side integration.',
            'Use account-level reporting access for every organization you want analyzed.',
            'Do not enter campaign IDs, ad group IDs, keyword IDs, or app IDs here.',
            'Paste the account credentials below.',
        ],
        credentials: [
            { env: 'APPLE_SEARCH_ADS_CLIENT_ID', prompt: 'Paste APPLE_SEARCH_ADS_CLIENT_ID, or leave empty if using a token only', optional: true },
            { env: 'APPLE_SEARCH_ADS_CLIENT_SECRET', prompt: 'Paste APPLE_SEARCH_ADS_CLIENT_SECRET, or leave empty if using a token only', optional: true },
            { env: 'APPLE_SEARCH_ADS_REFRESH_TOKEN', prompt: 'Paste APPLE_SEARCH_ADS_REFRESH_TOKEN or current access token into this local terminal' },
        ],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'google-ads'),
        key: 'google-ads',
        service: 'google-ads',
        docsUrl: 'https://developers.google.com/google-ads/api/docs/oauth/overview',
        sourceKind: 'acquisition',
        signalHint: 'Experimental Google Ads account summary with accessible customer accounts, campaigns, ad groups, keywords, spend, clicks, conversions, ROAS, CAC, search terms, and app/web acquisition quality. Keep customer IDs and campaign IDs discoverable.',
        steps: [
            'Open Google Ads API Center and Google Cloud OAuth credentials for the account.',
            'Create or copy a developer token plus OAuth client credentials and refresh token.',
            'Use a manager/account credential that can read every customer account you want analyzed.',
            'Do not enter customer IDs, campaign IDs, ad group IDs, or conversion action IDs in setup.',
            'Paste the account-wide credentials below.',
        ],
        credentials: [
            { env: 'GOOGLE_ADS_DEVELOPER_TOKEN', prompt: 'Paste GOOGLE_ADS_DEVELOPER_TOKEN into this local terminal' },
            { env: 'GOOGLE_ADS_CLIENT_ID', prompt: 'Paste GOOGLE_ADS_CLIENT_ID into this local terminal' },
            { env: 'GOOGLE_ADS_CLIENT_SECRET', prompt: 'Paste GOOGLE_ADS_CLIENT_SECRET into this local terminal' },
            { env: 'GOOGLE_ADS_REFRESH_TOKEN', prompt: 'Paste GOOGLE_ADS_REFRESH_TOKEN into this local terminal' },
            { env: 'GOOGLE_ADS_LOGIN_CUSTOMER_ID', prompt: 'Optional manager login customer ID (empty = discover accessible accounts)', optional: true },
        ],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'meta-ads'),
        key: 'meta-ads',
        service: 'meta-ads',
        docsUrl: 'https://developers.facebook.com/docs/marketing-apis/',
        sourceKind: 'acquisition',
        signalHint: 'Experimental Meta Ads account summary with accessible ad accounts, campaigns, ad sets, creatives, spend, impressions, clicks, conversion values, CAC, ROAS, and paid social acquisition quality. Keep ad account IDs and campaign IDs discoverable.',
        steps: [
            'Open Meta for Developers / Business Manager for the app or system user that owns Marketing API access.',
            'Create or copy a long-lived access token with ads_read and related read permissions approved for your business.',
            'Use business/account-level access for all ad accounts you want analyzed.',
            'Do not enter ad account IDs, campaign IDs, pixel IDs, or page IDs here.',
            'Paste the access token below.',
        ],
        credentials: [{ env: 'META_ADS_ACCESS_TOKEN', prompt: 'Paste META_ADS_ACCESS_TOKEN into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'tiktok-ads'),
        key: 'tiktok-ads',
        service: 'tiktok-ads',
        docsUrl: 'https://business-api.tiktok.com/portal/docs',
        sourceKind: 'acquisition',
        signalHint: 'Experimental TikTok Ads account summary with advertisers, campaigns, ad groups, creatives, spend, impressions, clicks, conversions, CAC, ROAS, and paid social acquisition quality. Keep advertiser/campaign IDs out of setup.',
        steps: [
            'Open TikTok Business API / Marketing API portal.',
            'Create or copy app credentials and an access token with advertiser reporting permissions.',
            'Use a credential that can list the advertisers you want analyzed.',
            'Do not enter advertiser IDs, campaign IDs, ad group IDs, or creative IDs in setup.',
            'Paste the credentials below.',
        ],
        credentials: [
            { env: 'TIKTOK_ADS_ACCESS_TOKEN', prompt: 'Paste TIKTOK_ADS_ACCESS_TOKEN into this local terminal' },
            { env: 'TIKTOK_ADS_APP_ID', prompt: 'Paste TIKTOK_ADS_APP_ID, or leave empty if token-only', optional: true },
            { env: 'TIKTOK_ADS_SECRET', prompt: 'Paste TIKTOK_ADS_SECRET, or leave empty if token-only', optional: true },
        ],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'vercel'),
        key: 'vercel',
        service: 'vercel',
        docsUrl: 'https://vercel.com/docs/rest-api/reference/welcome',
        sourceKind: 'infrastructure',
        signalHint: 'Experimental Vercel account summary with projects, deployments, failed builds, domains, edge/runtime errors, environment health, web vitals where available, and release reliability. Keep project IDs/team IDs discoverable.',
        steps: [
            'Open Vercel Account Settings -> Tokens.',
            'Create an access token with read access for the team/account you want analyzed.',
            'Use team/account-level access so the agent can discover projects and deployments.',
            'Do not enter project IDs, deployment IDs, domain names, or team IDs in setup.',
            'Paste the token below.',
        ],
        credentials: [{ env: 'VERCEL_ACCESS_TOKEN', prompt: 'Paste VERCEL_ACCESS_TOKEN into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'cloudflare'),
        key: 'cloudflare',
        service: 'cloudflare',
        docsUrl: 'https://developers.cloudflare.com/fundamentals/api/get-started/create-token/',
        sourceKind: 'infrastructure',
        signalHint: 'Experimental Cloudflare account summary with accounts, zones, Workers, Pages, DNS, traffic, cache, WAF/security events, outages, and edge reliability. Keep account/zone IDs discoverable.',
        steps: [
            'Open Cloudflare dashboard -> My Profile -> API Tokens.',
            'Create a custom token with read scopes for accounts/zones, analytics, Workers/Pages, DNS, and security events as needed.',
            'Prefer account-level read access for every zone/app the agent may analyze.',
            'Do not enter account IDs, zone IDs, Worker names, or domain names here.',
            'Paste the API token below.',
        ],
        credentials: [{ env: 'CLOUDFLARE_API_TOKEN', prompt: 'Paste CLOUDFLARE_API_TOKEN into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'resend'),
        key: 'resend',
        service: 'resend',
        docsUrl: 'https://resend.com/docs/dashboard/api-keys/introduction',
        sourceKind: 'lifecycle',
        signalHint: 'Experimental Resend account summary with domains, broadcasts, transactional volume, bounces, complaints, delivery health, and lifecycle/email deliverability signals. Keep domain filters discoverable.',
        steps: [
            'Open Resend Dashboard -> API Keys.',
            'Create an API key with the narrowest account-wide access available for reporting.',
            'Use account-level access so the agent can inspect all relevant domains and sending streams.',
            'Do not enter domain IDs, broadcast IDs, or audience/list IDs in setup.',
            'Paste the key below.',
        ],
        credentials: [{ env: 'RESEND_API_KEY', prompt: 'Paste RESEND_API_KEY into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'customerio'),
        key: 'customerio',
        service: 'customerio',
        docsUrl: 'https://docs.customer.io/accounts-and-workspaces/managing-credentials/',
        sourceKind: 'lifecycle',
        signalHint: 'Experimental Customer.io account summary with campaigns, broadcasts, journeys, segments, deliveries, conversions, unsubscribes, and lifecycle engagement quality. Keep workspace object IDs discoverable.',
        steps: [
            'Open Customer.io -> Settings -> Workspace Settings -> API and Webhook Credentials.',
            'Create or copy App API credentials for the workspace.',
            'Use workspace-level credentials so the agent can inspect campaigns, broadcasts, journeys, and segments.',
            'Do not enter campaign IDs, segment IDs, newsletter IDs, or workspace-specific filters here.',
            'Paste the credentials below.',
        ],
        credentials: [
            { env: 'CUSTOMERIO_APP_API_KEY', prompt: 'Paste CUSTOMERIO_APP_API_KEY into this local terminal' },
            { env: 'CUSTOMERIO_SITE_ID', prompt: 'Paste CUSTOMERIO_SITE_ID, or leave empty when App API key is enough', optional: true },
        ],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'mailchimp'),
        key: 'mailchimp',
        service: 'mailchimp',
        docsUrl: 'https://mailchimp.com/developer/marketing/guides/quick-start/',
        sourceKind: 'lifecycle',
        signalHint: 'Experimental Mailchimp account summary with audiences, campaigns, automations, ecommerce, unsubscribes, bounces, clicks, opens, and lifecycle/email performance. Keep audience and campaign IDs discoverable.',
        steps: [
            'Open Mailchimp -> Account & billing -> Extras -> API keys.',
            'Create or copy a Marketing API key for the account.',
            'Use account-level access so the agent can inspect all relevant audiences and campaigns.',
            'Do not enter audience IDs, campaign IDs, list IDs, or store IDs in setup.',
            'Paste the API key below.',
        ],
        credentials: [{ env: 'MAILCHIMP_API_KEY', prompt: 'Paste MAILCHIMP_API_KEY into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'appfollow'),
        key: 'appfollow',
        service: 'appfollow',
        docsUrl: 'https://support.appfollow.io/hc/en-us/articles/4403679243409-API-Access-Methods',
        sourceKind: 'aso',
        signalHint: 'Experimental AppFollow account summary with app collections, reviews, ratings, semantic themes, ASO/rank signals, competitor context, and store feedback quality. Keep collection/app IDs discoverable.',
        steps: [
            'Open AppFollow -> Integrations -> API Dashboard.',
            'Create or copy the API token from an Owner/Admin account.',
            'Use account-level access for every app collection you want analyzed.',
            'Do not enter app IDs, collection IDs, country codes, or store IDs in setup.',
            'Paste the API token below.',
        ],
        credentials: [{ env: 'APPFOLLOW_API_TOKEN', prompt: 'Paste APPFOLLOW_API_TOKEN into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'apptweak'),
        key: 'apptweak',
        service: 'apptweak',
        docsUrl: 'https://help.apptweak.com/en/articles/4901806-learn-more-about-apptweak-takeout-api',
        sourceKind: 'aso',
        signalHint: 'Experimental AppTweak account summary with keyword rankings, category ranks, metadata, ASO visibility, competitors, and store-market opportunity signals. Keep app IDs and markets discoverable.',
        steps: [
            'Open AppTweak account/API settings or API documentation area.',
            'Create or copy an API token from an account with API access.',
            'Use account-level API access for every app/market you want analyzed.',
            'Do not enter app IDs, competitor IDs, country codes, keyword IDs, or store IDs here.',
            'Paste the API token below.',
        ],
        credentials: [{ env: 'APPTWEAK_API_TOKEN', prompt: 'Paste APPTWEAK_API_TOKEN into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'linear'),
        key: 'linear',
        service: 'linear',
        docsUrl: 'https://linear.app/developers',
        sourceKind: 'planning',
        signalHint: 'Experimental Linear workspace summary with teams, projects, cycles, issues, labels, stale work, roadmap commitments, delivery bottlenecks, and product execution context. Keep team/project IDs discoverable.',
        steps: [
            'Open Linear -> Settings -> API.',
            'Create a personal API key or use an OAuth token with read access.',
            'Use workspace-level read access so the agent can inspect all relevant teams/projects.',
            'Do not enter team IDs, project IDs, issue IDs, labels, or cycle IDs in setup.',
            'Paste the token below.',
        ],
        credentials: [{ env: 'LINEAR_API_KEY', prompt: 'Paste LINEAR_API_KEY or LINEAR_ACCESS_TOKEN into this local terminal' }],
    },
    {
        ...CONNECTOR_DEFINITIONS.find((connector) => connector.key === 'postiz'),
        key: 'postiz',
        service: 'postiz',
        docsUrl: 'https://docs.postiz.com/public-api',
        sourceKind: 'acquisition',
        signalHint: 'Experimental Postiz account summary with connected social integrations, scheduled/published posts, platform analytics, content cadence, failed/pending posts, and organic distribution signals. Keep integration IDs and channel filters discoverable.',
        steps: [
            'Open Postiz -> Settings -> Developers -> Public API.',
            'Create or copy a Public API key. OAuth2 tokens are also usable for app-user flows.',
            'For Postiz Cloud, keep the default API base URL. For self-hosted Postiz, use your backend public URL ending in /public/v1.',
            'Do not enter integration IDs, channel IDs, platform names, post IDs, or tag filters in setup.',
            'Paste the API credentials below.',
        ],
        credentials: [
            { env: 'POSTIZ_API_KEY', prompt: 'Paste POSTIZ_API_KEY into this local terminal' },
            {
                env: 'POSTIZ_API_BASE_URL',
                prompt: 'Postiz API base URL',
                optional: true,
                defaultValue: process.env.POSTIZ_API_BASE_URL || 'https://api.postiz.com/public/v1',
            },
        ],
    },
];
const ACCOUNT_SIGNAL_CONNECTORS = new Map(ACCOUNT_SIGNAL_CONNECTOR_DEFINITIONS.map((definition) => [definition.key, definition]));
function getAccountSignalConnectorDefinition(key) {
    return ACCOUNT_SIGNAL_CONNECTORS.get(key) || null;
}
function isAccountSignalConnector(key) {
    return ACCOUNT_SIGNAL_CONNECTORS.has(key);
}
const DEFAULT_CADENCE_PLAN = [
    {
        key: 'healthcheck',
        title: '90-minute production error healthcheck',
        intervalMinutes: 90,
        criticalOnly: true,
        focusAreas: ['crash', 'deployment', 'availability'],
        sourcePriorities: ['sentry', 'glitchtip', 'coolify', 'asc_cli'],
        objective: 'Check Sentry/GlitchTip and Coolify for production errors, failed deploys, unhealthy resources, and availability blockers across every configured app.',
        instructions: 'For Sentry/GlitchTip app errors, compare the issue release or app version with ASC production versions first. Ignore errors that only affect TestFlight, debug, staging, unreleased, or non-production app versions. Keep the social output short and action-oriented.',
    },
    {
        key: 'daily',
        title: 'Daily behavioral anomaly guardrail',
        intervalDays: 1,
        criticalOnly: true,
        focusAreas: ['analytics_anomaly', 'onboarding', 'conversion', 'paywall', 'purchase', 'retention', 'revenue'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'asc_cli', 'feedback', 'github', 'sentry', 'glitchtip', 'coolify'],
        objective: 'Detect non-Sentry product and payment anomalies that affect real users: broken login or account flows inferred from behavior, onboarding or purchase drop-offs, zero-conversion days, missing buyers, very low active users, retention cliffs, and revenue anomalies.',
        instructions: 'Compare AnalyticsCLI, RevenueCat, Paddle, ASC, feedback, memory/state, and recent code changes against recent baselines. Use Sentry/GlitchTip/Coolify only as corroborating context; do not repeat pure crash or deployment alerts that belong to the 90-minute healthcheck.',
    },
    {
        key: 'weekly',
        title: 'Weekly executive product and growth summary',
        intervalDays: 7,
        criticalOnly: false,
        focusAreas: ['conversion', 'paywall', 'onboarding', 'marketing', 'retention', 'stability', 'seo'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry', 'coolify', 'github'],
        objective: 'Create a deep app-by-app executive summary across all configured projects, connectors, recent releases, code changes, traffic, SEO/acquisition, revenue, activation, conversion, retention, reviews, and production stability.',
        instructions: 'Be detailed. Group findings per app, explain why each recommendation should improve app usage, revenue, conversion, retention, or traffic, include expected KPI movement, likely code/store surfaces, owner-ready next steps, and verification plans. Generate charts when they clarify the evidence.',
    },
    {
        key: 'monthly',
        title: 'Monthly deep product, business, and code review',
        intervalDays: 30,
        criticalOnly: false,
        focusAreas: ['conversion', 'paywall', 'retention', 'marketing', 'onboarding', 'codebase', 'seo'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry', 'coolify', 'github'],
        objective: 'Compare all configured projects month-over-month: MRR, trial conversion, churn, Paddle revenue/subscriber movement, SEO demand/clicks, acquisition quality, store conversion, retention, review themes, feature usage, crash totals, and codebase changes.',
        instructions: 'Be very detailed and app-grouped. Decide what should be built, changed, deleted, priced differently, marketed differently, or instrumented next. Tie conclusions to connector data plus codebase evidence and explain why each recommendation should move revenue, conversion, retention, traffic, or acquisition quality. Generate charts when useful.',
    },
    {
        key: 'quarterly',
        title: '3-month positioning, pricing, and roadmap review',
        intervalDays: 91,
        criticalOnly: false,
        focusAreas: ['marketing', 'paywall', 'retention', 'conversion', 'onboarding'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'github', 'sentry'],
        objective: 'Revisit positioning, pricing/packaging, onboarding architecture, roadmap assumptions, tracking quality, codebase constraints, and major funnel bets across every configured app.',
        instructions: 'Find structural constraints and durable opportunities, not small UI tweaks. Group the analysis by app and tie recommendations to cohort behavior, monetization, SEO demand, reviews, channel quality, and shipped changes. Include concrete roadmap, pricing, conversion, and traffic recommendations.',
    },
    {
        key: 'six_months',
        title: 'Six-month instrumentation and growth-system audit',
        intervalDays: 182,
        criticalOnly: false,
        focusAreas: ['retention', 'conversion', 'paywall', 'marketing', 'general', 'seo'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry'],
        objective: 'Audit connector coverage, SDK instrumentation, event taxonomy, data reliability, memory, growth loops, and whether product/code strategy still matches the best users across configured apps.',
        instructions: 'Group by app. Prioritize measurement fixes and system changes that make future analysis more trustworthy, then identify the highest-leverage app/revenue/conversion/SEO/traffic improvements. Identify stale events, missing attribution, weak identity, broken feedback loops, and misleading dashboards.',
    },
    {
        key: 'yearly',
        title: 'Yearly evidence reset',
        intervalDays: 365,
        criticalOnly: false,
        focusAreas: ['marketing', 'retention', 'paywall', 'conversion', 'general'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry'],
        objective: 'Reset strategy from evidence across every configured project: market/channel fit, monetization model, retention ceiling, product scope, and whether to double down, reposition, rebuild, or sunset major surfaces/features.',
        instructions: 'Use the full year of memory, releases, revenue, acquisition, reviews, code changes, and cohort behavior. Produce strategic experiments and stop-doing decisions.',
    },
];
const ANSI = {
    bold: '\x1b[1m',
    cyan: '\x1b[36m',
    dim: '\x1b[2m',
    green: '\x1b[32m',
    hideCursor: '\x1b[?25l',
    reset: '\x1b[0m',
    showCursor: '\x1b[?25h',
};
async function ensureDirForFile(filePath) {
    await fs.mkdir(path.dirname(filePath), { recursive: true });
}
async function fileExists(filePath) {
    try {
        await fs.access(filePath);
        return true;
    }
    catch {
        return false;
    }
}
async function readJsonFile(filePath) {
    return JSON.parse(await fs.readFile(filePath, 'utf8'));
}
async function readJsonIfPresent(filePath) {
    if (!(await fileExists(filePath)))
        return null;
    return readJsonFile(filePath);
}
async function writeJsonFile(filePath, value) {
    await ensureDirForFile(filePath);
    await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}
function isTruthyEnv(value) {
    return ['1', 'true', 'yes', 'y', 'on'].includes(String(value || '').trim().toLowerCase());
}
function isFalseyEnv(value) {
    return ['0', 'false', 'no', 'n', 'off'].includes(String(value || '').trim().toLowerCase());
}
function resolveDefaultConfigPath() {
    const explicit = String(process.env.OPENCLAW_GROWTH_CONFIG_PATH || '').trim();
    if (explicit)
        return explicit;
    const homeConfigPath = process.env.HOME ? path.join(process.env.HOME, 'data/openclaw-growth-engineer/config.json') : '';
    const homeStatePath = process.env.HOME ? path.join(process.env.HOME, 'data/openclaw-growth-engineer/state.json') : '';
    if (homeConfigPath && existsSync(homeConfigPath) && existsSync(homeStatePath))
        return homeConfigPath;
    if (!existsSync(DEFAULT_CONFIG_PATH) && homeConfigPath && existsSync(homeConfigPath))
        return homeConfigPath;
    return DEFAULT_CONFIG_PATH;
}
function parseArgs(argv) {
    const defaultConfigPath = resolveDefaultConfigPath();
    const args = {
        config: defaultConfigPath,
        connectorWizard: false,
        connectors: '',
        noSelfUpdate: false,
        out: defaultConfigPath,
        sandboxSmoke: false,
    };
    for (let i = 0; i < argv.length; i += 1) {
        const token = argv[i];
        const next = argv[i + 1];
        if (token === '--') {
            continue;
        }
        else if (token === '--config') {
            args.config = next || args.config;
            args.out = next || args.out;
            i += 1;
        }
        else if (token === '--connectors' || token === '--connector-setup') {
            args.connectorWizard = true;
            if (next && !next.startsWith('-')) {
                args.connectors = next;
                i += 1;
            }
        }
        else if (token === '--out') {
            args.out = next;
            args.config = next;
            i += 1;
        }
        else if (token === '--no-self-update') {
            args.noSelfUpdate = true;
        }
        else if (token === '--sandbox-smoke') {
            args.sandboxSmoke = true;
            args.noSelfUpdate = true;
        }
        else if (token === '--help' || token === '-h') {
            printHelpAndExit(0);
        }
        else {
            printHelpAndExit(1, `Unknown argument: ${token}`);
        }
    }
    return args;
}
function printHelpAndExit(exitCode, reason = null) {
    if (reason) {
        process.stderr.write(`${reason}\n\n`);
    }
    process.stdout.write(`
OpenClaw Growth Setup Wizard

Usage:
  npx -y @analyticscli/growth-engineer wizard [--out <config-path>]
  npx -y @analyticscli/growth-engineer wizard --connectors [${CONNECTOR_KEYS.join(',')}]

Compatibility note:
  Existing cron/heartbeat runners may still execute generated runtime scripts, but user-facing setup and connector repair should use the npx command above.

Options:
  --config <file>    Override auto-discovered config path
  --no-self-update   Skip the ClawHub skill update check for this run
`);
    process.exit(exitCode);
}
function quote(value) {
    if (/^[a-zA-Z0-9_./:-]+$/.test(String(value))) {
        return String(value);
    }
    return `'${String(value).replace(/'/g, `'\\''`)}'`;
}
function escapeRegExp(value) {
    return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
function resolveRuntimeScriptPath(scriptName) {
    const candidates = [
        path.join(RUNTIME_DIR, scriptName),
        path.resolve('scripts', scriptName),
        path.resolve('skills/growth-engineer/scripts', scriptName),
        path.resolve('skills/openclaw-growth-engineer/scripts', scriptName),
    ];
    return candidates.find((candidate) => existsSync(candidate)) || path.join(RUNTIME_DIR, scriptName);
}
function nodeRuntimeScriptCommand(scriptName) {
    return `node ${quote(resolveRuntimeScriptPath(scriptName))}`;
}
function growthEngineerPackageCommand(args) {
    return `npx -y ${quote(GROWTH_ENGINEER_PACKAGE_SPEC)} ${args}`;
}
function getWizardDefaultSourceCommand(sourceName) {
    const normalized = String(sourceName || '').trim().toLowerCase();
    if (normalized === 'analytics' || normalized === 'analyticscli') {
        return nodeRuntimeScriptCommand('export-analytics-summary.mjs');
    }
    if (normalized === 'revenuecat' || normalized === 'revenue-cat') {
        return nodeRuntimeScriptCommand('export-revenuecat-summary.mjs');
    }
    if (normalized === 'paddle') {
        return nodeRuntimeScriptCommand('export-paddle-summary.mjs');
    }
    if (['seo', 'gsc', 'google-search-console', 'search-console', 'dataforseo'].includes(normalized)) {
        return nodeRuntimeScriptCommand('export-seo-summary.mjs');
    }
    if (normalized === 'sentry' || normalized === 'glitchtip') {
        return nodeRuntimeScriptCommand('export-sentry-summary.mjs');
    }
    if (normalized === 'coolify') {
        return growthEngineerPackageCommand('exporters coolify-summary');
    }
    if (normalized === 'feedback') {
        return getDefaultSourceCommand('feedback');
    }
    if (['asc', 'asc-cli', 'app-store-connect', 'app_store_connect'].includes(normalized)) {
        return nodeRuntimeScriptCommand('export-asc-summary.mjs');
    }
    return getDefaultSourceCommand(sourceName);
}
function replaceLegacyRuntimeScriptCommand(command) {
    const trimmed = String(command || '').trim();
    if (!trimmed)
        return trimmed;
    return trimmed
        .replace(/^node\s+scripts\/(export-analytics-summary\.mjs|export-revenuecat-summary\.mjs|export-paddle-summary\.mjs|export-seo-summary\.mjs|export-sentry-summary\.mjs|export-coolify-summary\.mjs|export-asc-summary\.mjs|openclaw-growth-start\.mjs|openclaw-growth-status\.mjs|openclaw-growth-runner\.mjs|openclaw-growth-preflight\.mjs)(?=\s|$)/, (_match, scriptName) => nodeRuntimeScriptCommand(scriptName))
        .replace(/^node\s+(['"]?)(?:\S*\/)?node_modules\/@analyticscli\/growth-engineer\/dist\/runtime\/(export-analytics-summary\.mjs|export-revenuecat-summary\.mjs|export-paddle-summary\.mjs|export-seo-summary\.mjs|export-sentry-summary\.mjs|export-coolify-summary\.mjs|export-asc-summary\.mjs|openclaw-growth-start\.mjs|openclaw-growth-status\.mjs|openclaw-growth-runner\.mjs|openclaw-growth-preflight\.mjs)\1(?=\s|$)/, (_match, _quote, scriptName) => nodeRuntimeScriptCommand(scriptName));
}
function sourceCommandNeedsActiveConfig(sourceName, command) {
    const normalized = String(sourceName || '').trim().toLowerCase();
    const value = String(command || '').toLowerCase();
    return (normalized === 'sentry' ||
        normalized === 'glitchtip' ||
        normalized === 'paddle' ||
        normalized === 'coolify' ||
        value.includes('export-paddle-summary') ||
        value.includes('export-sentry-summary') ||
        value.includes('export-coolify-summary') ||
        value.includes('exporters coolify-summary'));
}
function withWizardConfigArg(sourceName, command, configPath) {
    const trimmed = String(command || '').trim();
    if (!trimmed || !configPath || !sourceCommandNeedsActiveConfig(sourceName, trimmed))
        return trimmed;
    return trimmed
        .replace(/(^|\s)--config=(?:"[^"]*"|'[^']*'|\S+)/, `$1--config ${quote(configPath)}`)
        .replace(/(^|\s)--config\s+(?:"[^"]*"|'[^']*'|\S+)/, `$1--config ${quote(configPath)}`)
        .replace(new RegExp(`^(?!.*(?:^|\\s)--config(?:=|\\s|$))(.+)$`), `$1 --config ${quote(configPath)}`)
        .trim();
}
function normalizeWizardSourceCommand(sourceName, source, configPath = null) {
    const current = replaceLegacyRuntimeScriptCommand(source?.command || '');
    const command = current || getWizardDefaultSourceCommand(sourceName);
    return withWizardConfigArg(sourceName, command, configPath);
}
function migrateRuntimeSourceCommands(config, configPath = null) {
    if (!config || typeof config !== 'object')
        return config;
    const sources = config.sources && typeof config.sources === 'object' ? config.sources : {};
    const nextSources = { ...sources };
    for (const sourceName of ['analytics', 'revenuecat', 'paddle', 'seo', 'sentry', 'coolify']) {
        if (nextSources[sourceName]?.mode === 'command') {
            nextSources[sourceName] = {
                ...nextSources[sourceName],
                command: normalizeWizardSourceCommand(sourceName, nextSources[sourceName], configPath),
            };
        }
    }
    if (Array.isArray(nextSources.extra)) {
        nextSources.extra = nextSources.extra.map((source) => {
            if (!source || source.mode !== 'command')
                return source;
            const service = String(source.service || source.key || '').toLowerCase();
            const sourceName = ['asc', 'asc-cli', 'app-store-connect', 'app_store_connect'].includes(service)
                ? 'asc'
                : service;
            return {
                ...source,
                command: normalizeWizardSourceCommand(sourceName, source, configPath),
            };
        });
    }
    return {
        ...config,
        sources: nextSources,
    };
}
async function migrateRuntimeSourceCommandsFile(configPath) {
    const existing = await readJsonIfPresent(configPath).catch(() => null);
    if (!existing || typeof existing !== 'object')
        return null;
    const migrated = migrateRuntimeSourceCommands(existing, configPath);
    if (JSON.stringify(existing.sources || {}) !== JSON.stringify(migrated.sources || {})) {
        await writeJsonFile(configPath, migrated);
    }
    return migrated;
}
function normalizeConnectorKey(value) {
    const normalized = String(value || '').trim().toLowerCase().replace(/[_\s]+/g, '-');
    if (!normalized)
        return null;
    if (normalized === 'all')
        return 'all';
    if (['analytics', 'analyticscli', 'product-analytics', 'events'].includes(normalized))
        return 'analytics';
    if (['github', 'gh', 'github-code', 'codebase', 'code-access'].includes(normalized))
        return 'github';
    if (['revenuecat', 'revenue-cat', 'rc', 'revenuecat-mcp'].includes(normalized))
        return 'revenuecat';
    if (['paddle', 'paddle-billing', 'billing-metrics', 'web-revenue'].includes(normalized))
        return 'paddle';
    if (['seo', 'gsc', 'google-search-console', 'search-console', 'dataforseo', 'organic-search'].includes(normalized))
        return 'seo';
    if (['sentry', 'sentry-api', 'sentry-mcp', 'crashes', 'errors', 'crash-reporting'].includes(normalized))
        return 'sentry';
    if (['coolify', 'coolify-api', 'deployment', 'deployments', 'hosting', 'infra', 'infrastructure'].includes(normalized))
        return 'coolify';
    if (['asc', 'asc-cli', 'app-store-connect', 'appstoreconnect', 'app-store'].includes(normalized))
        return 'asc';
    if (['stripe', 'stripe-billing', 'stripe-payments'].includes(normalized))
        return 'stripe';
    if (['lemonsqueezy', 'lemon-squeezy', 'lemon', 'ls'].includes(normalized))
        return 'lemonsqueezy';
    if (['adapty', 'adapty-paywalls', 'adapty-subscriptions'].includes(normalized))
        return 'adapty';
    if (['superwall', 'superwall-paywalls'].includes(normalized))
        return 'superwall';
    if (['google-play', 'google-play-console', 'play-console', 'play-store', 'android-store'].includes(normalized))
        return 'google-play';
    if (['datadog', 'datadog-rum', 'datadog-apm', 'datadog-logs'].includes(normalized))
        return 'datadog';
    if (['bugsnag', 'bugsnag-crashes'].includes(normalized))
        return 'bugsnag';
    if (['intercom', 'intercom-support'].includes(normalized))
        return 'intercom';
    if (['zendesk', 'zendesk-support'].includes(normalized))
        return 'zendesk';
    if (['apple-search-ads', 'apple-ads', 'asa', 'search-ads'].includes(normalized))
        return 'apple-search-ads';
    if (['google-ads', 'adwords'].includes(normalized))
        return 'google-ads';
    if (['meta-ads', 'facebook-ads', 'instagram-ads', 'fb-ads'].includes(normalized))
        return 'meta-ads';
    if (['tiktok-ads', 'tiktok-business', 'tiktok-business-api'].includes(normalized))
        return 'tiktok-ads';
    if (['vercel', 'vercel-deployments', 'vercel-hosting'].includes(normalized))
        return 'vercel';
    if (['cloudflare', 'cf', 'cloudflare-workers', 'cloudflare-pages'].includes(normalized))
        return 'cloudflare';
    if (['resend', 'resend-email'].includes(normalized))
        return 'resend';
    if (['customerio', 'customer-io', 'customer.io', 'cio'].includes(normalized))
        return 'customerio';
    if (['mailchimp', 'mailchimp-marketing'].includes(normalized))
        return 'mailchimp';
    if (['appfollow', 'app-follow'].includes(normalized))
        return 'appfollow';
    if (['apptweak', 'app-tweak'].includes(normalized))
        return 'apptweak';
    if (['linear', 'linear-issues', 'linear-planning'].includes(normalized))
        return 'linear';
    if (['postiz', 'postiz-api', 'social-publishing', 'social-scheduler'].includes(normalized))
        return 'postiz';
    return null;
}
function parseConnectorList(value) {
    const selected = new Set();
    for (const entry of String(value || '').split(',')) {
        const connector = normalizeConnectorKey(entry);
        if (!connector)
            continue;
        if (connector === 'all') {
            CONNECTOR_KEYS.forEach((key) => selected.add(key));
        }
        else {
            selected.add(connector);
        }
    }
    return [...selected];
}
function isConnectorLocallyConfigured(key) {
    if (key === 'analytics') {
        return Boolean(process.env.ANALYTICSCLI_ACCESS_TOKEN?.trim() || process.env.ANALYTICSCLI_READONLY_TOKEN?.trim());
    }
    if (key === 'github')
        return Boolean(process.env.GITHUB_TOKEN?.trim());
    if (key === 'revenuecat')
        return Boolean(process.env.REVENUECAT_API_KEY?.trim());
    if (key === 'paddle')
        return Boolean(process.env.PADDLE_API_KEY?.trim());
    if (key === 'seo') {
        return Boolean(process.env.GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN?.trim() ||
            process.env.GSC_ACCESS_TOKEN?.trim() ||
            process.env.GOOGLE_APPLICATION_CREDENTIALS?.trim() ||
            process.env.GSC_SERVICE_ACCOUNT_JSON?.trim());
    }
    if (key === 'sentry')
        return Boolean(process.env.SENTRY_AUTH_TOKEN?.trim());
    if (key === 'coolify')
        return Boolean(process.env.COOLIFY_API_TOKEN?.trim() && process.env.COOLIFY_BASE_URL?.trim());
    if (key === 'asc') {
        return Boolean(process.env.ASC_KEY_ID?.trim() &&
            process.env.ASC_ISSUER_ID?.trim() &&
            (process.env.ASC_PRIVATE_KEY_PATH?.trim() || process.env.ASC_PRIVATE_KEY?.trim()));
    }
    const accountConnector = getAccountSignalConnectorDefinition(key);
    if (accountConnector) {
        return accountConnector.credentials.some((credential) => Boolean(process.env[credential.env]?.trim()));
    }
    return false;
}
function getRequiredConnectorKeys() {
    return new Set(isConnectorLocallyConfigured('analytics') ? [] : ['analytics']);
}
function withMissingRequiredAnalyticsConnector(selected) {
    if (isConnectorLocallyConfigured('analytics') || selected.includes('analytics'))
        return orderConnectors(selected);
    return orderConnectors(['analytics', ...selected]);
}
async function askConnectorSelectionWithHealth(rl, healthByConnector = {}, initialSelected = [], copy = {}) {
    if (!process.stdin.isTTY || !process.stdout.isTTY || !process.stdin.setRawMode) {
        return await askConnectorSelectionByText(rl, healthByConnector, initialSelected, copy);
    }
    rl.pause();
    let completed = false;
    try {
        const selected = await askConnectorSelectionByKeys(healthByConnector, initialSelected, copy);
        completed = true;
        return selected;
    }
    finally {
        if (completed) {
            rl.resume();
        }
        else {
            process.stdin.pause();
        }
    }
}
async function askConnectorSelectionByText(rl, healthByConnector = {}, initialSelected = [], copy = {}) {
    printConnectorIntro(copy);
    for (const group of connectorPickerGroups(healthByConnector)) {
        process.stdout.write(`${ANSI.bold}${group.title}${ANSI.reset}\n`);
        for (const connector of group.connectors) {
            const number = CONNECTOR_DEFINITIONS.findIndex((entry) => entry.key === connector.key) + 1;
            process.stdout.write(`  ${number}) ${connector.label}\n`);
        }
        process.stdout.write('\n');
    }
    const required = copy.mode === 'input' ? new Set() : getRequiredConnectorKeys();
    const defaultSelection = orderConnectors([...new Set([...initialSelected, ...required])]);
    const defaultAnswer = defaultSelection.length > 0
        ? defaultSelection.map((key) => String(CONNECTOR_DEFINITIONS.findIndex((entry) => entry.key === key) + 1)).join(',')
        : '';
    while (true) {
        const answer = await ask(rl, 'Select connectors (comma-separated numbers/names, or all)', defaultAnswer);
        const selected = parseConnectorAnswer(answer);
        if (selected.length > 0)
            return selected;
        process.stdout.write('\nChoose at least one connector.\n\n');
    }
}
function parseConnectorAnswer(answer) {
    const selected = new Set();
    for (const rawEntry of String(answer || '').split(',')) {
        const entry = rawEntry.trim().toLowerCase();
        const numericConnector = CONNECTOR_DEFINITIONS[Number(entry) - 1]?.key;
        if (numericConnector)
            selected.add(numericConnector);
        const key = normalizeConnectorKey(entry);
        if (key === 'all')
            CONNECTOR_KEYS.forEach((connector) => selected.add(connector));
        if (key && key !== 'all')
            selected.add(key);
    }
    return orderConnectors([...selected]);
}
function orderConnectors(keys) {
    const selected = new Set(keys);
    return CONNECTOR_KEYS.filter((key) => selected.has(key));
}
function printConnectorIntro(copy = {}) {
    process.stdout.write(`\n${ANSI.bold}${copy.introTitle || 'OpenClaw connector setup'}${ANSI.reset}\n`);
    const detail = copy.introDetail === undefined
        ? 'You can configure connector secrets here. API keys stay in this host\'s local secrets file, not in chat or config JSON.'
        : copy.introDetail;
    if (detail) {
        process.stdout.write(`${ANSI.dim}${detail}${ANSI.reset}\n`);
    }
    process.stdout.write('\n');
}
async function askMenuChoice(rl, { title, subtitle = 'Use Up/Down to move, Enter to continue.', options, defaultValue, renderHeader, }) {
    if (!process.stdin.isTTY || !process.stdout.isTTY || !process.stdin.setRawMode) {
        process.stdout.write(`\n${title}\n`);
        options.forEach((option, index) => {
            process.stdout.write(`  ${index + 1}) ${option.label}: ${option.detail}\n`);
        });
        const defaultIndex = Math.max(0, options.findIndex((option) => option.value === defaultValue));
        const answer = await ask(rl, `Setup area (1-${options.length})`, String(defaultIndex + 1));
        if (isBackAnswer(answer))
            throw new WizardBackError();
        const selected = options[Number(answer.trim()) - 1] || options[defaultIndex];
        return selected.value;
    }
    rl.pause();
    let completed = false;
    try {
        const selected = await askMenuChoiceByKeys({ title, subtitle, options, defaultValue, renderHeader });
        completed = true;
        return selected;
    }
    finally {
        if (completed) {
            rl.resume();
        }
        else {
            process.stdin.pause();
        }
    }
}
async function askMultiChoice(rl, { title, subtitle = 'Use Up/Down to move, Space to toggle, Enter to continue.', options, defaultValues, requiredValues = [], minSelections = 1, renderHeader, }) {
    const required = new Set(requiredValues);
    const normalizeSelection = (values) => {
        const selected = new Set(values);
        requiredValues.forEach((value) => selected.add(value));
        return options.map((option) => option.value).filter((value) => selected.has(value));
    };
    if (!process.stdin.isTTY || !process.stdout.isTTY || !process.stdin.setRawMode) {
        process.stdout.write(`\n${title}\n`);
        options.forEach((option, index) => {
            const checked = defaultValues.includes(option.value) || required.has(option.value) ? 'x' : ' ';
            const requiredLabel = required.has(option.value) ? ' required' : '';
            process.stdout.write(`  ${index + 1}) [${checked}] ${option.label}${requiredLabel}: ${option.detail}\n`);
        });
        const answer = await ask(rl, `Select one or more (comma-separated 1-${options.length})`, normalizeSelection(defaultValues).map((value) => String(options.findIndex((option) => option.value === value) + 1)).join(','));
        const selected = answer
            .split(',')
            .map((value) => Number.parseInt(value.trim(), 10) - 1)
            .filter((index) => options[index])
            .map((index) => options[index].value);
        const normalized = normalizeSelection(selected);
        return normalized.length >= minSelections ? normalized : normalizeSelection(defaultValues);
    }
    rl.pause();
    let completed = false;
    try {
        const selected = await askMultiChoiceByKeys({
            title,
            subtitle,
            options,
            defaultValues: normalizeSelection(defaultValues),
            requiredValues,
            minSelections,
            renderHeader,
        });
        completed = true;
        return selected;
    }
    finally {
        if (completed) {
            rl.resume();
        }
        else {
            process.stdin.pause();
        }
    }
}
async function askMultiChoiceByKeys({ title, subtitle, options, defaultValues, requiredValues, minSelections, renderHeader, }) {
    emitKeypressEvents(process.stdin);
    const wasRaw = process.stdin.isRaw;
    const wasPaused = process.stdin.isPaused();
    process.stdin.setRawMode(true);
    process.stdin.resume();
    const required = new Set(requiredValues);
    const selected = new Set(defaultValues);
    requiredValues.forEach((value) => selected.add(value));
    let cursorIndex = 0;
    let warning = '';
    return await new Promise((resolve, reject) => {
        const cleanup = () => {
            process.stdin.off('keypress', onKeypress);
            process.stdin.setRawMode(Boolean(wasRaw));
            if (wasPaused) {
                process.stdin.pause();
            }
            process.stdout.write(ANSI.showCursor);
        };
        const selectedValues = () => options.map((option) => option.value).filter((value) => selected.has(value));
        const render = () => {
            process.stdout.write('\x1b[2J\x1b[H');
            renderHeader?.();
            process.stdout.write(`\n${ANSI.bold}${title}${ANSI.reset}\n`);
            process.stdout.write(`${ANSI.dim}${subtitle}${ANSI.reset}\n\n`);
            if (warning) {
                process.stdout.write(`${ANSI.cyan}${warning}${ANSI.reset}\n\n`);
            }
            for (let index = 0; index < options.length; index += 1) {
                const option = options[index];
                const pointer = index === cursorIndex ? `${ANSI.cyan}>${ANSI.reset}` : ' ';
                const checkbox = selected.has(option.value) ? '[x]' : '[ ]';
                const requiredLabel = required.has(option.value) ? ` ${ANSI.dim}(required)${ANSI.reset}` : '';
                process.stdout.write(`${pointer} ${checkbox} ${index + 1}) ${ANSI.bold}${option.label}${ANSI.reset}${requiredLabel}\n`);
                writeWrapped(option.detail, '      ', ANSI.dim);
            }
            process.stdout.write(`\n${ANSI.dim}Esc/← back. Ctrl+C cancels. Space toggles, Enter continues. Number keys 1-${options.length} toggle items.${ANSI.reset}\n`);
        };
        const back = () => {
            cleanup();
            process.stdout.write('\n');
            reject(new WizardBackError());
        };
        const cancel = () => {
            cleanup();
            process.stdout.write('\n');
            reject(new WizardAbortError('Setup cancelled.'));
        };
        const finish = () => {
            const values = selectedValues();
            if (values.length < minSelections) {
                warning = `Select at least ${minSelections} item${minSelections === 1 ? '' : 's'} to continue.`;
                render();
                return;
            }
            cleanup();
            process.stdout.write('\x1b[2J\x1b[H');
            resolve(values);
        };
        const toggleIndex = (index) => {
            const option = options[index];
            if (!option)
                return;
            warning = '';
            if (required.has(option.value)) {
                selected.add(option.value);
                warning = `${option.label} is required.`;
                return;
            }
            if (selected.has(option.value))
                selected.delete(option.value);
            else
                selected.add(option.value);
            requiredValues.forEach((value) => selected.add(value));
        };
        const onKeypress = (_text, key) => {
            if (key?.ctrl && key?.name === 'c') {
                cancel();
                return;
            }
            if (key?.name === 'escape' || key?.name === 'left') {
                back();
                return;
            }
            if (key?.name === 'up') {
                cursorIndex = (cursorIndex - 1 + options.length) % options.length;
                warning = '';
            }
            else if (key?.name === 'down') {
                cursorIndex = (cursorIndex + 1) % options.length;
                warning = '';
            }
            else if (key?.name === 'space') {
                toggleIndex(cursorIndex);
            }
            else if (key?.name === 'return' || key?.name === 'enter') {
                finish();
                return;
            }
            else if (/^[1-9]$/.test(String(_text || ''))) {
                toggleIndex(Number(_text) - 1);
            }
            render();
        };
        process.stdin.on('keypress', onKeypress);
        process.stdout.write(ANSI.hideCursor);
        render();
    });
}
async function askMenuChoiceByKeys({ title, subtitle, options, defaultValue, renderHeader, }) {
    emitKeypressEvents(process.stdin);
    const wasRaw = process.stdin.isRaw;
    const wasPaused = process.stdin.isPaused();
    process.stdin.setRawMode(true);
    process.stdin.resume();
    let cursorIndex = Math.max(0, options.findIndex((option) => option.value === defaultValue));
    return await new Promise((resolve, reject) => {
        const cleanup = () => {
            process.stdin.off('keypress', onKeypress);
            process.stdin.setRawMode(Boolean(wasRaw));
            if (wasPaused) {
                process.stdin.pause();
            }
            process.stdout.write(ANSI.showCursor);
        };
        const render = () => {
            process.stdout.write('\x1b[2J\x1b[H');
            renderHeader?.();
            process.stdout.write(`\n${ANSI.bold}${title}${ANSI.reset}\n`);
            process.stdout.write(`${ANSI.dim}${subtitle}${ANSI.reset}\n\n`);
            for (let index = 0; index < options.length; index += 1) {
                const option = options[index];
                const pointer = index === cursorIndex ? `${ANSI.cyan}>${ANSI.reset}` : ' ';
                const number = `${index + 1})`;
                process.stdout.write(`${pointer} ${number} ${ANSI.bold}${option.label}${ANSI.reset}\n`);
                writeWrapped(option.detail, '     ', ANSI.dim);
            }
            process.stdout.write(`\n${ANSI.dim}Esc/← back. Ctrl+C cancels. Number keys 1-${options.length} select directly.${ANSI.reset}\n`);
        };
        const back = () => {
            cleanup();
            process.stdout.write('\n');
            reject(new WizardBackError());
        };
        const cancel = () => {
            cleanup();
            process.stdout.write('\n');
            reject(new WizardAbortError('Setup cancelled.'));
        };
        const finish = () => {
            cleanup();
            process.stdout.write('\x1b[2J\x1b[H');
            resolve(options[cursorIndex]?.value || defaultValue);
        };
        const onKeypress = (_text, key) => {
            if (key?.ctrl && key?.name === 'c') {
                cancel();
                return;
            }
            if (key?.name === 'escape' || key?.name === 'left') {
                back();
                return;
            }
            if (key?.name === 'up') {
                cursorIndex = (cursorIndex - 1 + options.length) % options.length;
            }
            else if (key?.name === 'down') {
                cursorIndex = (cursorIndex + 1) % options.length;
            }
            else if (key?.name === 'return' || key?.name === 'enter') {
                finish();
                return;
            }
            else if (/^[1-9]$/.test(String(_text || ''))) {
                const selectedIndex = Number(_text) - 1;
                if (options[selectedIndex]) {
                    cursorIndex = selectedIndex;
                    finish();
                    return;
                }
            }
            render();
        };
        process.stdin.on('keypress', onKeypress);
        process.stdout.write(ANSI.hideCursor);
        render();
    });
}
function normalizeConnectorProgressKey(key) {
    const normalized = String(key || '').trim().toLowerCase();
    if (normalized === 'analytics' || normalized === 'analyticscli')
        return 'analytics';
    if (normalized === 'github')
        return 'github';
    if (normalized === 'revenuecat')
        return 'revenuecat';
    if (normalized === 'paddle')
        return 'paddle';
    if (normalized === 'seo' || normalized === 'gsc' || normalized === 'google-search-console')
        return 'seo';
    if (normalized === 'sentry')
        return 'sentry';
    if (normalized === 'coolify')
        return 'coolify';
    if (normalized === 'asc' || normalized === 'appstoreconnect' || normalized === 'app-store-connect')
        return 'asc';
    const accountConnector = normalizeConnectorKey(normalized);
    if (accountConnector && accountConnector !== 'all')
        return accountConnector;
    return null;
}
async function withConnectorHealthLoading(taskFactory, expectedConnectors = [...CONNECTOR_KEYS]) {
    const expected = orderConnectors(expectedConnectors);
    if (expected.length === 0) {
        return await taskFactory(() => { });
    }
    const frames = ['-', '\\', '|', '/'];
    const completed = new Set();
    const expectedSet = new Set(expected);
    let index = 0;
    let current = 'starting';
    const render = () => {
        const count = Math.min(completed.size, expected.length);
        process.stdout.write(`\rChecking connector health ${count}/${expected.length} (${current}) ${frames[index]}`);
    };
    const timer = setInterval(() => {
        index = (index + 1) % frames.length;
        render();
    }, 120);
    render();
    try {
        const result = await taskFactory((event) => {
            const key = normalizeConnectorProgressKey(event?.key);
            if (!key || !expectedSet.has(key))
                return;
            current = connectorLabel(key);
            if (event?.phase === 'finish')
                completed.add(key);
            render();
        });
        expected.forEach((key) => completed.add(key));
        current = 'done';
        render();
        process.stdout.write('\n');
        return result;
    }
    finally {
        clearInterval(timer);
    }
}
function connectorLabel(key) {
    return CONNECTOR_DEFINITIONS.find((connector) => connector.key === key)?.label ?? key;
}
function toConfigId(value, fallback) {
    return String(value || fallback)
        .trim()
        .toLowerCase()
        .replace(/https?:\/\//g, '')
        .replace(/[^a-zA-Z0-9._-]+/g, '_')
        .replace(/^_+|_+$/g, '') || fallback;
}
function toEnvName(value, fallback) {
    return String(value || fallback)
        .trim()
        .toUpperCase()
        .replace(/[^A-Z0-9]+/g, '_')
        .replace(/^_+|_+$/g, '') || fallback;
}
function connectorHealthLabel(status) {
    if (status === 'connected')
        return 'healthy';
    if (status === 'partial')
        return 'partial';
    if (status === 'blocked')
        return 'blocked';
    if (status === 'not_enabled')
        return 'not enabled';
    if (status === 'not_connected')
        return 'not connected';
    if (status === 'unknown')
        return 'unknown';
    return status || 'not checked';
}
function getConnectorHealth(key, healthByConnector = {}) {
    const fallbackStatus = isConnectorLocallyConfigured(key) ? 'unknown' : 'not_connected';
    const fallbackDetail = isConnectorLocallyConfigured(key)
        ? 'credentials exist, but live health was not verified'
        : '';
    return healthByConnector[key] || { status: fallbackStatus, detail: fallbackDetail };
}
function connectorStatusLabel(key, healthByConnector = {}) {
    const health = getConnectorHealth(key, healthByConnector);
    const configured = isConnectorLocallyConfigured(key);
    if (health.status === 'connected')
        return configured ? 'configured, healthy' : 'healthy via local tool auth';
    if (!configured)
        return '';
    return `configured, ${connectorHealthLabel(health.status)}`;
}
function formatConnectorHealthText(key, healthByConnector = {}) {
    const health = getConnectorHealth(key, healthByConnector);
    const label = connectorStatusLabel(key, healthByConnector);
    if (!label)
        return '';
    const detail = health.detail ? ` - ${health.detail}` : '';
    return `Status: ${label}${detail}`;
}
function wrapText(text, indent = '', width = process.stdout.columns || 100) {
    const available = Math.max(32, width - indent.length);
    const words = String(text || '').split(/\s+/).filter(Boolean);
    const lines = [];
    let current = '';
    for (const word of words) {
        if (!current) {
            current = word;
        }
        else if (`${current} ${word}`.length <= available) {
            current = `${current} ${word}`;
        }
        else {
            lines.push(current);
            current = word;
        }
        while (current.length > available) {
            lines.push(current.slice(0, available));
            current = current.slice(available);
        }
    }
    if (current)
        lines.push(current);
    return lines.length > 0 ? lines.map((line) => `${indent}${line}`) : [indent.trimEnd()];
}
function writeWrapped(text, indent = '', style = '') {
    for (const line of wrapText(text, indent)) {
        process.stdout.write(style ? `${style}${line}${ANSI.reset}\n` : `${line}\n`);
    }
}
function connectorPickerGroups(healthByConnector = {}) {
    const groups = [
        { title: 'Configured - needs attention', connectors: [] },
        { title: 'Configured - healthy', connectors: [] },
        { title: 'Not configured', connectors: [] },
    ];
    for (const connector of CONNECTOR_DEFINITIONS) {
        const configured = isConnectorLocallyConfigured(connector.key);
        const health = getConnectorHealth(connector.key, healthByConnector);
        if (!configured && health.status !== 'connected') {
            groups[2].connectors.push(connector);
        }
        else if (health.status === 'connected') {
            groups[1].connectors.push(connector);
        }
        else {
            groups[0].connectors.push(connector);
        }
    }
    return groups.filter((group) => group.connectors.length > 0);
}
function connectorPickerDisplayItems(healthByConnector = {}) {
    return connectorPickerGroups(healthByConnector).flatMap((group) => group.connectors);
}
function connectorKeysNeedingAttention(healthByConnector = {}) {
    return CONNECTOR_KEYS.filter((key) => {
        const health = getConnectorHealth(key, healthByConnector);
        const status = String(health.status || '');
        if (!['blocked', 'partial', 'unknown', 'not_connected'].includes(status))
            return false;
        return isConnectorLocallyConfigured(key) || status !== 'not_connected';
    });
}
function isConfiguredSource(config, sourceName) {
    return Boolean(config?.sources?.[sourceName] && config.sources[sourceName].enabled !== false);
}
function configuredConnectorKeysFromConfig(config) {
    const configured = new Set();
    if (!config || typeof config !== 'object')
        return [];
    for (const key of ['analytics', 'revenuecat', 'paddle', 'seo', 'sentry', 'coolify']) {
        if (isConfiguredSource(config, key))
            configured.add(key);
    }
    if (isConfiguredGitHubRepo(config?.project?.githubRepo))
        configured.add('github');
    for (const source of Array.isArray(config?.sources?.extra) ? config.sources.extra : []) {
        if (!source || source.enabled === false)
            continue;
        if (source.service === 'asc-cli') {
            configured.add('asc');
            continue;
        }
        const connector = normalizeConnectorProgressKey(source.key || source.service || source.type);
        if (connector)
            configured.add(connector);
    }
    return [...configured];
}
async function connectorKeysForHealthCheck(configPath) {
    const configured = new Set();
    CONNECTOR_KEYS.forEach((key) => {
        if (isConnectorLocallyConfigured(key))
            configured.add(key);
    });
    const config = await readJsonIfPresent(configPath).catch(() => null);
    for (const key of configuredConnectorKeysFromConfig(config))
        configured.add(key);
    return orderConnectors([...configured]);
}
function connectorKeyFromRunnerHealthKey(key) {
    const normalized = String(key || '').trim();
    if (normalized === 'analyticscli')
        return 'analytics';
    if (normalized === 'appStoreConnect')
        return 'asc';
    const connector = normalizeConnectorProgressKey(normalized);
    return connector || null;
}
function activeIncidentStatusLabel(status) {
    const normalized = String(status || '').trim();
    return normalized || 'blocked';
}
async function readActiveConnectorIncidents(configPath) {
    const statePath = deriveStatePathFromConfigPath(configPath);
    const state = await readJsonIfPresent(statePath).catch(() => null);
    const healthState = state?.connectorHealth;
    if (!healthState ||
        healthState.lastStatusOk !== false ||
        !healthState.activeIncidentFingerprint) {
        return {};
    }
    const alertJsonPath = healthState.lastAlertJsonPath
        ? path.resolve(String(healthState.lastAlertJsonPath))
        : path.resolve(path.dirname(statePath), 'runtime/connector-health/latest.json');
    const alertJson = await readJsonIfPresent(alertJsonPath).catch(() => null);
    const unhealthyConnectors = Array.isArray(alertJson?.unhealthyConnectors)
        ? alertJson.unhealthyConnectors
        : [];
    const incidents = {};
    for (const entry of unhealthyConnectors) {
        const key = connectorKeyFromRunnerHealthKey(entry?.key);
        if (!key)
            continue;
        incidents[key] = {
            ...entry,
            status: activeIncidentStatusLabel(entry?.status),
            detail: String(entry?.detail || 'Runner still has an active connector-health incident').trim(),
            activeRunnerIncident: true,
            activeIncidentFingerprint: healthState.activeIncidentFingerprint,
            lastCheckedAt: healthState.lastCheckedAt || null,
        };
    }
    return incidents;
}
function mergeActiveConnectorIncidents(healthByConnector, activeIncidents) {
    if (!activeIncidents || Object.keys(activeIncidents).length === 0) {
        return healthByConnector;
    }
    return Object.fromEntries(CONNECTOR_KEYS.map((key) => {
        const liveHealth = getConnectorHealth(key, healthByConnector);
        const incident = activeIncidents[key];
        if (!incident)
            return [key, liveHealth];
        if (liveHealth.status === 'connected') {
            return [key, liveHealth];
        }
        return [
            key,
            {
                ...liveHealth,
                ...incident,
                status: incident.status || liveHealth.status || 'blocked',
                detail: incident.detail || liveHealth.detail,
            },
        ];
    }));
}
async function getConnectorPickerHealth(configPath, onProgress = () => { }, onlyConnectors = []) {
    const activeIncidents = await readActiveConnectorIncidents(configPath);
    if (!(await fileExists(configPath))) {
        const fallbackHealth = Object.fromEntries(CONNECTOR_KEYS.map((key) => [
            key,
            {
                status: isConnectorLocallyConfigured(key) ? 'unknown' : 'not_connected',
                detail: isConnectorLocallyConfigured(key)
                    ? `config file not found at ${configPath}; live check could not run`
                    : '',
            },
        ]));
        return mergeActiveConnectorIncidents(fallbackHealth, activeIncidents);
    }
    if (onlyConnectors.length === 0) {
        const fallbackHealth = Object.fromEntries(CONNECTOR_KEYS.map((key) => [key, getConnectorHealth(key, {})]));
        return mergeActiveConnectorIncidents(fallbackHealth, activeIncidents);
    }
    const onlyArg = ` --only-connectors ${quote(orderConnectors(onlyConnectors).join(','))}`;
    const result = await runCommandCaptureWithProgress(`${nodeRuntimeScriptCommand('openclaw-growth-status.mjs')} --config ${quote(configPath)} --json --progress-json${onlyArg}`, onProgress);
    const payload = parseJsonFromStdout(result.stdout);
    const connectors = payload?.connectors && typeof payload.connectors === 'object' ? payload.connectors : {};
    const healthByConnector = {
        analytics: connectors.analyticscli,
        github: connectors.github,
        revenuecat: connectors.revenuecat,
        paddle: connectors.paddle,
        seo: connectors.seo,
        sentry: connectors.sentry,
        coolify: connectors.coolify,
        asc: connectors.appStoreConnect,
    };
    const liveHealth = Object.fromEntries(CONNECTOR_KEYS.map((key) => [key, getConnectorHealth(key, healthByConnector)]));
    return mergeActiveConnectorIncidents(liveHealth, activeIncidents);
}
function renderConnectorPicker(cursorIndex, selected, required, healthByConnector = {}, warning = '', copy = {}) {
    process.stdout.write('\x1b[2J\x1b[H');
    printConnectorIntro(copy);
    process.stdout.write(`${ANSI.bold}${copy.actionTitle || 'Select connectors to set up or overwrite now'}${ANSI.reset}\n`);
    writeWrapped(copy.helpText || 'Use Up/Down to move, Space to toggle optional connectors, A to toggle all optional connectors, Enter to continue.', '', ANSI.dim);
    process.stdout.write('\n');
    let index = 0;
    for (const group of connectorPickerGroups(healthByConnector)) {
        process.stdout.write(`${ANSI.bold}${group.title}${ANSI.reset}\n`);
        for (const connector of group.connectors) {
            const active = index === cursorIndex;
            const isRequired = required.has(connector.key);
            const checked = isRequired || selected.has(connector.key);
            const pointer = active ? `${ANSI.cyan}>${ANSI.reset}` : ' ';
            const box = checked ? `${ANSI.green}[x]${ANSI.reset}` : '[ ]';
            const suffix = isRequired ? ' (required baseline)' : '';
            const label = `${connector.label}${suffix}`;
            const title = active ? `${ANSI.bold}${label}${ANSI.reset}` : label;
            process.stdout.write(`${pointer} ${box} ${title}\n`);
            index += 1;
        }
        process.stdout.write('\n');
    }
    if (warning) {
        process.stdout.write(`${ANSI.bold}${warning}${ANSI.reset}\n\n`);
    }
    process.stdout.write(`${ANSI.dim}Esc/← back. Ctrl+C cancels. Number keys 1-${CONNECTOR_DEFINITIONS.length} also toggle connectors.${ANSI.reset}\n`);
}
async function askConnectorSelectionByKeys(healthByConnector = {}, initialSelected = [], copy = {}) {
    emitKeypressEvents(process.stdin);
    const wasRaw = process.stdin.isRaw;
    const wasPaused = process.stdin.isPaused();
    process.stdin.setRawMode(true);
    process.stdin.resume();
    let cursorIndex = 0;
    const required = copy.mode === 'input' ? new Set() : getRequiredConnectorKeys();
    const initial = new Set(initialSelected);
    const selected = new Set(CONNECTOR_KEYS.filter((key) => required.has(key) || initial.has(key)));
    let warning = '';
    return await new Promise((resolve, reject) => {
        const displayItems = () => connectorPickerDisplayItems(healthByConnector);
        const selectedDisplayConnector = () => displayItems()[cursorIndex] || displayItems()[0];
        const displayIndexForConnector = (key) => Math.max(0, displayItems().findIndex((connector) => connector.key === key));
        const cleanup = () => {
            process.stdin.off('keypress', onKeypress);
            process.stdin.setRawMode(Boolean(wasRaw));
            if (wasPaused) {
                process.stdin.pause();
            }
            process.stdout.write(ANSI.showCursor);
        };
        const finish = () => {
            required.forEach((key) => selected.add(key));
            if (selected.size === 0) {
                warning = 'No connectors selected. Select a connector to update or press Q to cancel.';
                renderConnectorPicker(cursorIndex, selected, required, healthByConnector, warning, copy);
                return;
            }
            cleanup();
            process.stdout.write('\x1b[2J\x1b[H');
            resolve(orderConnectors([...selected]));
        };
        const cancel = () => {
            cleanup();
            process.stdout.write('\n');
            reject(new WizardAbortError('Connector setup cancelled.'));
        };
        const back = () => {
            cleanup();
            process.stdout.write('\n');
            reject(new WizardBackError());
        };
        const toggleCurrent = () => {
            const connector = selectedDisplayConnector();
            if (!connector)
                return;
            const key = connector.key;
            if (required.has(key)) {
                selected.add(key);
                warning = 'AnalyticsCLI is missing and required for the Growth Engineer baseline.';
                return;
            }
            if (selected.has(key))
                selected.delete(key);
            else
                selected.add(key);
            warning = '';
        };
        const onKeypress = (_text, key) => {
            if (key?.ctrl && key?.name === 'c') {
                cancel();
                return;
            }
            if (key?.name === 'escape' || key?.name === 'left') {
                back();
                return;
            }
            if (key?.name === 'up') {
                const itemCount = displayItems().length || CONNECTOR_DEFINITIONS.length;
                cursorIndex = (cursorIndex - 1 + itemCount) % itemCount;
                warning = '';
            }
            else if (key?.name === 'down') {
                const itemCount = displayItems().length || CONNECTOR_DEFINITIONS.length;
                cursorIndex = (cursorIndex + 1) % itemCount;
                warning = '';
            }
            else if (key?.name === 'space') {
                toggleCurrent();
            }
            else if (key?.name === 'return' || key?.name === 'enter') {
                finish();
                return;
            }
            else if (/^[1-9]$/.test(String(_text || ''))) {
                const index = Number(_text) - 1;
                const connector = CONNECTOR_DEFINITIONS[index];
                if (connector) {
                    cursorIndex = displayIndexForConnector(connector.key);
                    if (required.has(connector.key)) {
                        selected.add(connector.key);
                        warning = 'AnalyticsCLI is missing and required for the Growth Engineer baseline.';
                    }
                    else {
                        if (selected.has(connector.key))
                            selected.delete(connector.key);
                        else
                            selected.add(connector.key);
                        warning = '';
                    }
                }
            }
            renderConnectorPicker(cursorIndex, selected, required, healthByConnector, warning, copy);
        };
        process.stdin.on('keypress', onKeypress);
        process.stdout.write(ANSI.hideCursor);
        renderConnectorPicker(cursorIndex, selected, required, healthByConnector, warning, copy);
    });
}
async function commandExists(commandName) {
    const result = await runInteractiveCommand(`command -v ${quote(commandName)} >/dev/null 2>&1`, {
        silent: true,
    });
    return result === 0;
}
async function runInteractiveCommand(command, options = {}) {
    return await new Promise((resolve) => {
        const child = spawn('/bin/sh', ['-lc', command], {
            env: options.env ?? process.env,
            stdio: options.silent ? 'ignore' : 'inherit',
        });
        child.on('close', (code) => resolve(code));
    });
}
async function runInteractiveProcess(command, args, options = {}) {
    return await new Promise((resolve) => {
        options.rl?.pause?.();
        const child = spawn(command, args, {
            env: options.env ?? process.env,
            stdio: options.silent ? 'ignore' : 'inherit',
        });
        child.on('error', () => {
            options.rl?.resume?.();
            resolve(127);
        });
        child.on('close', (code) => {
            options.rl?.resume?.();
            resolve(code);
        });
    });
}
async function runCommandCapture(command, options = {}) {
    return await new Promise((resolve) => {
        const child = spawn('/bin/sh', ['-lc', command], {
            env: options.env ?? process.env,
            stdio: ['ignore', 'pipe', 'pipe'],
        });
        let stdout = '';
        let stderr = '';
        child.stdout.on('data', (chunk) => {
            stdout += String(chunk);
        });
        child.stderr.on('data', (chunk) => {
            stderr += String(chunk);
        });
        child.on('error', (error) => {
            resolve({ ok: false, stdout, stderr: error.message, code: null });
        });
        child.on('close', (code) => {
            resolve({ ok: code === 0, stdout, stderr, code });
        });
    });
}
async function runCommandCaptureWithTimeout(command, options = {}) {
    return await new Promise((resolve) => {
        const child = spawn('/bin/sh', ['-lc', command], {
            env: options.env ?? process.env,
            stdio: ['ignore', 'pipe', 'pipe'],
        });
        let stdout = '';
        let stderr = '';
        let settled = false;
        const timer = setTimeout(() => {
            if (settled)
                return;
            settled = true;
            child.kill('SIGTERM');
            resolve({ ok: false, stdout, stderr: `${stderr}\nTimed out after ${options.timeoutMs}ms`, code: null });
        }, options.timeoutMs ?? 60_000);
        child.stdout.on('data', (chunk) => {
            stdout += String(chunk);
        });
        child.stderr.on('data', (chunk) => {
            stderr += String(chunk);
        });
        child.on('error', (error) => {
            if (settled)
                return;
            settled = true;
            clearTimeout(timer);
            resolve({ ok: false, stdout, stderr: error.message, code: null });
        });
        child.on('close', (code) => {
            if (settled)
                return;
            settled = true;
            clearTimeout(timer);
            resolve({ ok: code === 0, stdout, stderr, code });
        });
    });
}
async function runCommandCaptureWithProgress(command, onProgress, options = {}) {
    return await new Promise((resolve) => {
        const child = spawn('/bin/sh', ['-lc', command], {
            env: options.env ?? process.env,
            stdio: ['ignore', 'pipe', 'pipe'],
        });
        let stdout = '';
        let stderr = '';
        let stderrBuffer = '';
        let settled = false;
        const timeoutMs = options.timeoutMs ?? 180_000;
        const timer = setTimeout(() => {
            if (settled)
                return;
            settled = true;
            child.kill('SIGTERM');
            resolve({ ok: false, stdout, stderr: `${stderr}\nTimed out after ${timeoutMs}ms`, code: null });
        }, timeoutMs);
        child.stdout.on('data', (chunk) => {
            stdout += String(chunk);
        });
        child.stderr.on('data', (chunk) => {
            const text = String(chunk);
            stderr += text;
            stderrBuffer += text;
            const lines = stderrBuffer.split(/\r?\n/);
            stderrBuffer = lines.pop() || '';
            for (const line of lines) {
                const match = line.match(/^OPENCLAW_PROGRESS\s+(.+)$/);
                if (!match)
                    continue;
                try {
                    onProgress(JSON.parse(match[1]));
                }
                catch {
                    // Ignore malformed progress events; the final JSON result is authoritative.
                }
            }
        });
        child.on('error', (error) => {
            if (settled)
                return;
            settled = true;
            clearTimeout(timer);
            resolve({ ok: false, stdout, stderr: error.message, code: null });
        });
        child.on('close', (code) => {
            if (settled)
                return;
            settled = true;
            clearTimeout(timer);
            const match = stderrBuffer.match(/^OPENCLAW_PROGRESS\s+(.+)$/);
            if (match) {
                try {
                    onProgress(JSON.parse(match[1]));
                }
                catch {
                    // Ignore malformed progress events; the final JSON result is authoritative.
                }
            }
            resolve({ ok: code === 0, stdout, stderr, code });
        });
    });
}
function truncate(value, maxLength = 900) {
    const text = String(value || '').trim();
    if (text.length <= maxLength)
        return text;
    return `${text.slice(0, maxLength - 1)}...`;
}
function parseJsonFromStdout(stdout) {
    const raw = String(stdout || '').trim();
    if (!raw)
        return null;
    const firstBrace = raw.indexOf('{');
    const firstBracket = raw.indexOf('[');
    const starts = [firstBrace, firstBracket].filter((index) => index >= 0);
    if (starts.length === 0)
        return null;
    const start = Math.min(...starts);
    const jsonText = extractFirstJsonValue(raw, start);
    if (!jsonText)
        return null;
    try {
        return JSON.parse(jsonText);
    }
    catch {
        return null;
    }
}
function extractFirstJsonValue(raw, start) {
    const open = raw[start];
    const close = open === '{' ? '}' : open === '[' ? ']' : '';
    if (!close)
        return '';
    let depth = 0;
    let inString = false;
    let escaped = false;
    for (let index = start; index < raw.length; index += 1) {
        const char = raw[index];
        if (inString) {
            if (escaped) {
                escaped = false;
            }
            else if (char === '\\') {
                escaped = true;
            }
            else if (char === '"') {
                inString = false;
            }
            continue;
        }
        if (char === '"') {
            inString = true;
            continue;
        }
        if (char === open)
            depth += 1;
        if (char === close) {
            depth -= 1;
            if (depth === 0)
                return raw.slice(start, index + 1);
        }
    }
    return '';
}
function stripProgressOutput(value) {
    return String(value || '')
        .split(/\r?\n/)
        .filter((line) => !line.startsWith('OPENCLAW_PROGRESS '))
        .join('\n')
        .trim();
}
function clearTerminal() {
    if (process.stdout.isTTY) {
        process.stdout.write('\x1b[2J\x1b[H');
    }
}
function printConnectorSetupProgress(payload) {
    const connectorSetup = Array.isArray(payload?.connectorSetup) ? payload.connectorSetup : [];
    const okConnectors = connectorSetup.filter((entry) => entry?.ok).map((entry) => entry.connector).filter(Boolean);
    if (okConnectors.length > 0) {
        process.stdout.write(`Configured locally: ${okConnectors.map(connectorTitle).join(', ')}.\n`);
    }
}
function checkConnectorKey(check) {
    return connectorFromCheckName(`${check?.name || ''} ${check?.detail || ''}`);
}
function getConfiguredConnectorKeys(payload) {
    const connectorSetup = Array.isArray(payload?.connectorSetup) ? payload.connectorSetup : [];
    return new Set(connectorSetup
        .filter((entry) => entry?.ok)
        .map((entry) => entry.connector)
        .filter(Boolean));
}
function getPassingConnectorKeys(payload, failedConnectors = new Set()) {
    const checks = Array.isArray(payload?.checks) ? payload.checks : [];
    const configuredConnectors = getConfiguredConnectorKeys(payload);
    const passing = new Set();
    for (const check of checks) {
        if (check?.status !== 'pass')
            continue;
        const connector = checkConnectorKey(check);
        if (!connector || failedConnectors.has(connector))
            continue;
        if (configuredConnectors.size > 0 && !configuredConnectors.has(connector))
            continue;
        passing.add(connector);
    }
    return orderConnectors([...passing]);
}
function summarizeFailureReason(detail) {
    const text = String(detail || '').replace(/\s+/g, ' ').trim();
    if (/ASC Reports key auth failed: .*\.p8 key could not be parsed/i.test(text)) {
        return 'ASC Reports key auth failed: the .p8 key could not be parsed';
    }
    if (/ASC Setup Admin key auth failed: .*\.p8 key could not be parsed/i.test(text)) {
        return 'ASC Setup Admin key auth failed: the .p8 key could not be parsed';
    }
    if (/ASC Reports key auth failed: .*\.p8 file permissions are too open/i.test(text)) {
        return 'ASC Reports key auth failed: .p8 file permissions are too open';
    }
    if (/ASC Setup Admin key auth failed: .*\.p8 file permissions are too open/i.test(text)) {
        return 'ASC Setup Admin key auth failed: .p8 file permissions are too open';
    }
    if (/ASC .*\.p8 private key is invalid|invalid private key|failed to parse|sequence truncated|malformed|asn1/i.test(text)) {
        return 'ASC auth failed: the .p8 key could not be parsed';
    }
    if (/token has been revoked/i.test(text))
        return 'token has been revoked';
    if (/unauthorized|UNAUTHORIZED/i.test(text))
        return 'token is unauthorized';
    if (/Sentry API 404|Not Found/i.test(text))
        return 'API returned 404 Not Found';
    if (/project\.githubRepo is missing/i.test(text))
        return 'GitHub repo is not configured';
    if (/missing/i.test(text))
        return text;
    return cleanHealthDetail(text);
}
function summarizeFailureFix(connector, blockers) {
    const combined = blockers.map((blocker) => `${blocker.check || ''} ${blocker.detail || ''}`).join('\n');
    if (connector === 'analytics') {
        if (/revoked|unauthorized|UNAUTHORIZED/i.test(combined)) {
            return 'Paste a fresh AnalyticsCLI readonly CLI token in the wizard, then let setup retest.';
        }
        return 'Verify the AnalyticsCLI token can list accessible projects. Per-project query failures are reported as warnings and should not block connector setup.';
    }
    if (connector === 'sentry') {
        if (/404|Not Found/i.test(combined)) {
            return 'Rerun Sentry/GlitchTip setup and use the correct base URL + visible org. Project scope stays unpinned and is resolved from app context later.';
        }
        return 'Verify the Sentry/GlitchTip token, base URL, and org, then rerun setup.';
    }
    if (connector === 'github') {
        return 'Verify the GitHub token. Repo scope is inferred from OPENCLAW_GITHUB_REPO, the local git remote, or runtime context.';
    }
    if (connector === 'revenuecat') {
        return 'Paste a RevenueCat v2 secret API key with read-only project permissions, then rerun setup.';
    }
    if (connector === 'paddle') {
        return 'Paste a live Paddle API key from Developer Tools > Authentication v2 with metrics.read permission, then rerun setup.';
    }
    if (connector === 'seo') {
        return 'Configure Search Console read access. Leave GSC_SITE_URL empty to scan all verified properties in the account, or set it only when you intentionally want one property.';
    }
    if (connector === 'coolify') {
        return 'Paste a Coolify base URL and read-only API token from Keys & Tokens / API tokens, then rerun setup.';
    }
    if (connector === 'asc') {
        if (/invalid value: ['"]?state|parameter has an invalid value: ['"]?state|--state/i.test(combined)) {
            return 'Update Growth Engineer and rerun ASC setup. Setup no longer uses the flaky ASC analytics request state filter.';
        }
        if (/file permissions are too open|too permissive|chmod 600/i.test(combined)) {
            return 'Rerun ASC setup. The wizard saves a secure local copy of AuthKey_<KEY_ID>.p8 with chmod 600 before testing.';
        }
        if (/Reports key auth failed|Reports key/i.test(combined) && /private key|could not be parsed|failed to parse|asn1/i.test(combined)) {
            return 'Use the original downloaded AuthKey_<KEY_ID>.p8 file for the Reports key. The wizard bypasses old asc keychain/config credentials during setup.';
        }
        if (/Setup Admin key auth failed|Admin key/i.test(combined) && /private key|could not be parsed|failed to parse|asn1/i.test(combined)) {
            return 'Use the original downloaded AuthKey_<KEY_ID>.p8 file for the Setup Admin key. This key is temporary and should have the Admin role.';
        }
        if (/invalid|truncated|malformed|private key|could not be parsed|failed to parse|asn1/i.test(combined)) {
            return 'Use the original downloaded AuthKey_<KEY_ID>.p8 for the Reports key. Old pasted ASC_PRIVATE_KEY values are removed when you choose a file path.';
        }
        return 'Rerun ASC setup and verify ASC credentials, key role access, and `asc apps list --output json`.';
    }
    if (isAccountSignalConnector(connector)) {
        const definition = getAccountSignalConnectorDefinition(connector);
        return `Paste ${definition?.credentials.map((credential) => credential.env).join(' / ') || connector} in the connector wizard. Keep setup account-wide; do not add project, app, product, paywall, or service IDs unless a later run explicitly narrows scope.`;
    }
    return blockers.find((blocker) => blocker.remediation)?.remediation || 'Fix the failing configuration and rerun setup.';
}
function connectorForBlocker(blocker) {
    return connectorFromCheckName(`${blocker?.check || ''} ${blocker?.detail || ''}`) || 'setup';
}
function groupBlockersByConnector(blockers, focusConnectors = null) {
    const groups = new Map();
    const focus = focusConnectors ? new Set(focusConnectors) : null;
    for (const blocker of blockers) {
        if (isDeferredGitHubFailure(blocker))
            continue;
        const connector = connectorForBlocker(blocker);
        if (focus && !focus.has(connector))
            continue;
        const entries = groups.get(connector) || [];
        entries.push(blocker);
        groups.set(connector, entries);
    }
    return groups;
}
function printDeferredSetupNotes(blockers, focusConnectors = null) {
    const focus = focusConnectors ? new Set(focusConnectors) : null;
    const deferredGitHub = blockers.some((blocker) => isDeferredGitHubFailure(blocker));
    if (!deferredGitHub || (focus && !focus.has('github')))
        return;
    process.stdout.write('\nDeferred / optional:\n');
    process.stdout.write('- GitHub: repo is not configured. This is only needed for GitHub issue/PR delivery.\n');
}
function printConciseSetupBlockers(payload, command, options = {}) {
    const blockers = Array.isArray(payload?.blockers) ? payload.blockers : [];
    const focusConnectors = Array.isArray(options.focusConnectors) ? options.focusConnectors : null;
    const groups = groupBlockersByConnector(blockers, focusConnectors);
    const failedConnectors = new Set([...groups.keys()].filter((key) => key !== 'setup'));
    let passingConnectors = getPassingConnectorKeys(payload, failedConnectors);
    if (focusConnectors) {
        const focus = new Set(focusConnectors);
        passingConnectors = passingConnectors.filter((connector) => focus.has(connector));
    }
    if (passingConnectors.length > 0) {
        process.stdout.write(`Live checks passed: ${passingConnectors.map(connectorTitle).join(', ')}.\n`);
    }
    if (groups.size > 0) {
        process.stdout.write('\nNeeds attention:\n');
        for (const [connector, connectorBlockers] of groups.entries()) {
            const primary = connectorBlockers[0] || {};
            process.stdout.write(`- ${connectorTitle(connector)}: ${summarizeFailureReason(primary.detail || primary.check)}\n`);
            process.stdout.write(`  Fix: ${summarizeFailureFix(connector, connectorBlockers)}\n`);
        }
    }
    printDeferredSetupNotes(blockers, focusConnectors);
    if (!options.hideRerun && (groups.size > 0 || !options.hideRerunWhenClean)) {
        process.stdout.write(`\nRerun: ${command}\n`);
    }
}
function payloadHasConnectorFailures(payload, connector) {
    const blockers = Array.isArray(payload?.blockers) ? payload.blockers : [];
    return blockers.some((blocker) => !isDeferredGitHubFailure(blocker) && connectorForBlocker(blocker) === connector);
}
function payloadOtherConnectorFailures(payload, connector) {
    const blockers = Array.isArray(payload?.blockers) ? payload.blockers : [];
    return blockers.filter((blocker) => {
        if (isDeferredGitHubFailure(blocker))
            return false;
        const blockerConnector = connectorForBlocker(blocker);
        return blockerConnector !== connector && blockerConnector !== 'setup';
    });
}
async function askListSelection(rl, label, entries, options = {}) {
    const includeManual = Boolean(options.includeManual);
    const includeDefer = Boolean(options.includeDefer);
    entries.forEach((entry, index) => {
        process.stdout.write(`  ${index + 1}) ${entry.label}\n`);
    });
    const manualIndex = includeManual ? entries.length + 1 : null;
    const deferIndex = includeDefer ? entries.length + (includeManual ? 2 : 1) : null;
    if (manualIndex)
        process.stdout.write(`  ${manualIndex}) Enter manually\n`);
    if (deferIndex)
        process.stdout.write(`  ${deferIndex}) Defer\n`);
    while (true) {
        const answer = (await ask(rl, label, entries.length === 1 ? '1' : '')).trim();
        const numericIndex = Number.parseInt(answer, 10);
        if (Number.isInteger(numericIndex)) {
            if (numericIndex >= 1 && numericIndex <= entries.length)
                return entries[numericIndex - 1].value;
            if (manualIndex && numericIndex === manualIndex)
                return '__manual__';
            if (deferIndex && numericIndex === deferIndex)
                return '';
        }
        const matchingEntry = entries.find((entry) => [entry.value, entry.label].some((value) => String(value || '').toLowerCase() === answer.toLowerCase()));
        if (matchingEntry)
            return matchingEntry.value;
        process.stdout.write('Choose one of the listed numbers.\n');
    }
}
function printSetupFailure({ result, payload, command }) {
    process.stdout.write('\nFAILED: Connector setup needs attention.\n');
    printConnectorSetupProgress(payload);
    const blockers = Array.isArray(payload?.blockers) ? payload.blockers : [];
    if (blockers.length > 0) {
        printConciseSetupBlockers(payload, command);
        return;
    }
    const reason = result.code === null ? 'setup command did not report an exit code' : `setup command exited with code ${result.code}`;
    process.stdout.write(`Reason: ${reason}.\n`);
    const output = truncate(stripProgressOutput(result.stderr) || stripProgressOutput(result.stdout));
    if (output) {
        process.stdout.write(`Details: ${output}\n`);
    }
}
function printSetupSuccess(payload) {
    process.stdout.write('\nSUCCESS: Connector setup finished.\n');
    printConnectorSetupProgress(payload);
    if (payload?.message) {
        process.stdout.write(`${payload.message}\n`);
    }
}
function connectorFromCheckName(name) {
    const value = String(name || '');
    if (value.includes('asc') || value.includes('ASC_') || /App Store Connect|app-store-connect|app_store_connect|Analytics Report Request/i.test(value))
        return 'asc';
    if (value.includes('analytics') || value.includes('ANALYTICSCLI'))
        return 'analytics';
    if (value.includes('github') || value.includes('GITHUB'))
        return 'github';
    if (value.includes('revenuecat') || value.includes('REVENUECAT'))
        return 'revenuecat';
    if (value.includes('paddle') || value.includes('PADDLE'))
        return 'paddle';
    if (value.includes('seo') || value.includes('GSC') || value.includes('GOOGLE_SEARCH_CONSOLE'))
        return 'seo';
    if (value.includes('sentry') || value.includes('SENTRY') || value.includes('GLITCHTIP'))
        return 'sentry';
    if (value.includes('coolify') || value.includes('COOLIFY'))
        return 'coolify';
    for (const key of ACCOUNT_SIGNAL_CONNECTOR_KEYS) {
        const definition = getAccountSignalConnectorDefinition(key);
        const envMatch = definition?.credentials.some((credential) => value.includes(credential.env));
        if (value.includes(key) || value.includes(key.toUpperCase()) || envMatch)
            return key;
    }
    return null;
}
function connectorTitle(key) {
    return CONNECTOR_DEFINITIONS.find((connector) => connector.key === key)?.label || key || 'General setup';
}
function compactJsonError(value) {
    const text = String(value || '');
    const jsonStart = text.indexOf('{"error"');
    if (jsonStart < 0)
        return '';
    try {
        const payload = JSON.parse(text.slice(jsonStart).replace(/\)+\s*$/g, '').trim());
        const error = payload?.error || payload;
        const parts = [
            error.code ? `code=${error.code}` : '',
            error.message ? `message=${error.message}` : '',
            error.details?.reason ? `reason=${error.details.reason}` : '',
            error.details?.upgradeUrl ? `upgradeUrl=${error.details.upgradeUrl}` : '',
        ].filter(Boolean);
        return parts.join(', ');
    }
    catch {
        return '';
    }
}
function cleanHealthDetail(detail) {
    const raw = String(detail || '').replace(/\s+/g, ' ').trim();
    const compactError = compactJsonError(raw);
    if (/project\.githubRepo is required/i.test(raw)) {
        return 'No GitHub repo is configured yet. This is optional unless you want GitHub issue/PR delivery now.';
    }
    if (/project\.githubRepo is missing/i.test(raw)) {
        return 'GitHub repo access test is deferred until a repo is known.';
    }
    if (/invalid token|unauthorized|token has been revoked/i.test(raw)) {
        return `AnalyticsCLI token is invalid${compactError ? ` (${compactError})` : ''}.`;
    }
    if (/No Sentry projects configured/i.test(raw)) {
        return 'Sentry project scope is deferred; the AI can discover visible projects from org + token.';
    }
    if (/smoke test failed/i.test(raw)) {
        const withoutWrappedJson = raw.replace(/\{"error".*$/, '').replace(/\s*\(+\s*$/, '').trim();
        return withoutWrappedJson || raw;
    }
    return truncate(raw, 180);
}
function isDeferredGitHubFailure(failure) {
    const name = String(failure?.name || '');
    const detail = String(failure?.detail || '');
    return (name === 'project:github-repo' ||
        (name === 'connection:github' && /project\.githubRepo|repo is missing|repo is not configured/i.test(detail)));
}
function healthStatusLabel(status, spinner = '') {
    if (status === 'running')
        return spinner ? `running ${spinner}` : 'running';
    if (status === 'pass')
        return 'done';
    if (status === 'warn')
        return 'needs attention';
    if (status === 'fail')
        return 'needs attention';
    if (status === 'deferred')
        return 'deferred';
    return spinner ? `pending ${spinner}` : 'pending';
}
function renderHealthProgress(items, message = 'Live checks running...', title = 'Health check', options = {}) {
    if (process.stdout.isTTY)
        clearTerminal();
    const final = Boolean(options.final);
    const visibleItems = final
        ? items.filter((item) => !['pending', 'running'].includes(String(item.status || '')) && item.key !== 'finalize')
        : items;
    const finished = visibleItems.filter((item) => !['pending', 'running'].includes(String(item.status || ''))).length;
    process.stdout.write(`${title}\n`);
    process.stdout.write('------------\n');
    process.stdout.write(`${message}\n\n`);
    if (final) {
        process.stdout.write('');
    }
    else {
        process.stdout.write(`${finished}/${visibleItems.length} checks finished.\n\n`);
    }
    for (const item of visibleItems) {
        process.stdout.write(`[${healthStatusLabel(item.status, options.spinner || '')}] ${item.label}: ${item.detail}\n`);
    }
}
function updateHealthProgress(items, event) {
    const key = String(event?.key || '');
    const item = items.find((entry) => entry.key === key);
    if (!item)
        return false;
    if (event.phase === 'start') {
        item.status = 'running';
        if (event.detail)
            item.detail = String(event.detail);
        if (event.label)
            item.label = String(event.label);
        return true;
    }
    if (event.phase === 'finish') {
        item.status = event.status || 'pass';
        if (event.detail)
            item.detail = String(event.detail);
        if (event.label)
            item.label = String(event.label);
        return true;
    }
    return false;
}
function buildSetupTestProgressPlan(selected) {
    const selectedSet = new Set(selected);
    const items = [
        {
            key: 'connectorSetup',
            label: 'Connector helpers',
            detail: 'waiting to install and enable selected helpers',
            status: 'pending',
        },
        {
            key: 'analyticsProject',
            label: 'AnalyticsCLI scope',
            detail: 'waiting to check accessible analytics projects',
            status: 'pending',
        },
    ];
    if (selectedSet.has('asc')) {
        items.push({
            key: 'ascApp',
            label: 'ASC app scope',
            detail: 'waiting to resolve App Store Connect app scope',
            status: 'pending',
        });
    }
    items.push({
        key: 'preflight',
        label: 'Local preflight',
        detail: 'waiting to validate config, dependencies, and source wiring',
        status: 'pending',
    });
    if (selectedSet.has('analytics')) {
        items.push({ key: 'analytics', label: 'AnalyticsCLI', detail: 'waiting for token auth + readonly query', status: 'pending' });
    }
    if (selectedSet.has('sentry')) {
        items.push({ key: 'sentry', label: 'Sentry / GlitchTip', detail: 'waiting for token/org API + project discovery', status: 'pending' });
    }
    if (selectedSet.has('revenuecat')) {
        items.push({ key: 'revenuecat', label: 'RevenueCat', detail: 'waiting for API key auth + project read', status: 'pending' });
    }
    if (selectedSet.has('paddle')) {
        items.push({ key: 'paddle', label: 'Paddle', detail: 'waiting for metrics API auth + revenue read', status: 'pending' });
    }
    if (selectedSet.has('seo')) {
        items.push({ key: 'seo', label: 'SEO / GSC', detail: 'waiting for Search Console auth or CSV/DataForSEO config', status: 'pending' });
    }
    if (selectedSet.has('coolify')) {
        items.push({ key: 'coolify', label: 'Coolify', detail: 'waiting for API key auth + deployment/resource read', status: 'pending' });
    }
    if (selectedSet.has('github')) {
        items.push({ key: 'github', label: 'GitHub', detail: 'waiting for repo/token access check', status: 'pending' });
    }
    for (const key of ACCOUNT_SIGNAL_CONNECTOR_KEYS) {
        if (!selectedSet.has(key))
            continue;
        const definition = getAccountSignalConnectorDefinition(key);
        items.push({
            key,
            label: definition?.label || key,
            detail: 'waiting for account-wide credential presence and source wiring',
            status: 'pending',
        });
    }
    items.push({
        key: 'finalize',
        label: 'Finalizing result',
        detail: 'waiting for command output, parsing, and follow-up checks',
        status: 'pending',
    });
    return items;
}
function primaryProgressItemsFinished(items) {
    return items
        .filter((item) => item.key !== 'finalize')
        .every((item) => !['pending', 'running'].includes(String(item.status || '')));
}
function updateProgressItem(items, key, status, detail) {
    const item = items.find((entry) => entry.key === key);
    if (!item)
        return;
    item.status = status;
    if (detail)
        item.detail = detail;
}
function reconcileSuccessfulSetupProgress(items) {
    for (const item of items) {
        if (item.key === 'finalize')
            continue;
        if (['fail', 'warn'].includes(String(item.status || ''))) {
            item.status = 'pass';
            if (item.key === 'preflight') {
                item.detail = 'passed with non-blocking checks';
            }
        }
    }
}
async function runSetupCommandWithProgress(command, env, selected, message) {
    const plan = buildSetupTestProgressPlan(selected);
    const spinnerFrames = ['-', '\\', '|', '/'];
    let spinnerIndex = 0;
    let currentMessage = message;
    const render = (nextMessage = currentMessage, options = {}) => {
        currentMessage = nextMessage;
        renderHealthProgress(plan, currentMessage, 'Connector setup test', {
            ...options,
            spinner: spinnerFrames[spinnerIndex++ % spinnerFrames.length],
        });
    };
    render(message);
    const spinnerInterval = process.stdout.isTTY
        ? setInterval(() => render(currentMessage), 800)
        : null;
    const progressCommand = command.includes('--progress-json') ? command : `${command} --progress-json`;
    const result = await runCommandCaptureWithProgress(progressCommand, (event) => {
        if (!updateHealthProgress(plan, event))
            return;
        const primaryFinished = primaryProgressItemsFinished(plan);
        if (primaryFinished) {
            updateProgressItem(plan, 'finalize', 'running', 'finishing');
        }
        render(primaryFinished ? 'Finishing setup test...' : 'Testing connector setup...');
    }, { env, timeoutMs: 180_000 }).finally(() => {
        if (spinnerInterval)
            clearInterval(spinnerInterval);
    });
    const payload = parseJsonFromStdout(result.stdout);
    if (Array.isArray(payload?.blockers) && payload.blockers.length > 0) {
        if (process.stdout.isTTY)
            clearTerminal();
        return result;
    }
    if (result.ok) {
        reconcileSuccessfulSetupProgress(plan);
    }
    updateProgressItem(plan, 'finalize', 'pass', 'result received');
    renderHealthProgress(plan, 'Connector setup test finished.', 'Connector setup test', { final: true });
    return result;
}
async function saveSecretsImmediately(secrets) {
    if (Object.keys(secrets).length === 0)
        return false;
    const secretsFile = resolveSecretsFile();
    await writeSecretsFile(secretsFile, secrets);
    applySecretsToProcessEnv(secrets);
    process.stdout.write(`Saved local secrets to ${secretsFile} with chmod 600.\n`);
    return true;
}
async function runImmediateConnectorHealthCheck({ rl, configPath, connector, secrets, runtimeEnv = {}, sentryAccounts = [], paddleAccounts = [], }) {
    if (connector === 'sentry' && sentryAccounts.length > 0) {
        await upsertSentryAccountsConfig(configPath, sentryAccounts);
    }
    if (connector === 'paddle' && paddleAccounts.length > 0) {
        await upsertPaddleAccountsConfig(configPath, paddleAccounts);
    }
    await saveSecretsImmediately(secrets);
    const env = mergeRuntimeEnv(secrets, connector === 'asc' ? { ASC_BYPASS_KEYCHAIN: '1' } : {}, runtimeEnv);
    const command = `${nodeRuntimeScriptCommand('openclaw-growth-start.mjs')} --config ${quote(configPath)} --setup-only --connectors ${quote(connector)} --only-connectors ${quote(connector)}`;
    let result = await runSetupCommandWithProgress(command, env, [connector], `Checking ${connectorLabel(connector)} immediately after setup...`);
    let payload = parseJsonFromStdout(result.stdout);
    if (payloadHasConnectorFailures(payload, connector)) {
        process.stdout.write(`\n${connectorLabel(connector)} needs attention before continuing.\n`);
        printConciseSetupBlockers(payload, command, {
            focusConnectors: [connector],
            hideRerunWhenClean: true,
            hideRerun: true,
        });
        const retry = await askYesNo(rl, `Re-enter ${connectorLabel(connector)} configuration now?`, true);
        return { ok: false, retry, result, payload };
    }
    const otherConnectorBlockers = payloadOtherConnectorFailures(payload, connector);
    if (otherConnectorBlockers.length > 0) {
        process.stdout.write(`\n${connectorLabel(connector)} immediate health check passed, but another configured connector needs attention.\n`);
        printConciseSetupBlockers({
            ...payload,
            blockers: otherConnectorBlockers,
        }, command, {
            hideRerunWhenClean: true,
        });
        return { ok: false, retry: false, result, payload };
    }
    process.stdout.write(`\n${connectorLabel(connector)} immediate health check passed or is only waiting on optional/deferred context.\n`);
    return { ok: true, retry: false, result, payload };
}
function getUserLocalBinDir() {
    return process.env.HOME ? path.join(process.env.HOME, '.local', 'bin') : null;
}
function prependPath(dir) {
    const current = process.env.PATH || '';
    if (!current.split(':').includes(dir)) {
        process.env.PATH = `${dir}:${current}`;
    }
}
function getGitHubCliReleaseAssetName(version) {
    const arch = process.arch === 'x64' ? 'amd64' : process.arch === 'arm64' ? 'arm64' : '';
    if (process.platform === 'linux' && arch) {
        return `gh_${version}_linux_${arch}.tar.gz`;
    }
    return null;
}
async function resolveGitHubCliReleaseAssetUrl() {
    const response = await fetch('https://api.github.com/repos/cli/cli/releases/latest', {
        headers: {
            Accept: 'application/vnd.github+json',
            'User-Agent': 'openclaw-growth-wizard',
        },
    });
    if (!response.ok) {
        throw new Error(`GitHub CLI release lookup failed (${response.status})`);
    }
    const release = await response.json();
    const version = String(release.tag_name || '').replace(/^v/, '');
    const assetName = getGitHubCliReleaseAssetName(version);
    if (!assetName) {
        throw new Error(`No user-local gh installer is defined for ${process.platform}/${process.arch}`);
    }
    const asset = release.assets?.find((entry) => entry.name === assetName);
    if (!asset?.browser_download_url) {
        throw new Error(`GitHub CLI release asset not found: ${assetName}`);
    }
    return asset.browser_download_url;
}
async function installGitHubCliUserLocal() {
    const binDir = getUserLocalBinDir();
    if (!binDir) {
        process.stdout.write('Cannot install gh automatically because HOME is not set.\n');
        return false;
    }
    if (!(await commandExists('curl'))) {
        process.stdout.write('Cannot install gh automatically because curl is not available.\n');
        return false;
    }
    if (!(await commandExists('tar'))) {
        process.stdout.write('Cannot install gh automatically because tar is not available.\n');
        return false;
    }
    try {
        const url = await resolveGitHubCliReleaseAssetUrl();
        const cacheDir = process.env.HOME
            ? path.join(process.env.HOME, '.cache', 'openclaw-gh')
            : path.join(process.cwd(), '.openclaw-gh-cache');
        const command = [
            'set -eu',
            `mkdir -p ${quote(binDir)} ${quote(cacheDir)}`,
            `tmp="$(mktemp -d ${quote(path.join(cacheDir, 'gh.XXXXXX'))})"`,
            'trap \'rm -rf "$tmp"\' EXIT',
            `curl -fsSL ${quote(url)} -o "$tmp/gh.tar.gz"`,
            'tar -xzf "$tmp/gh.tar.gz" -C "$tmp"',
            'gh_bin="$(find "$tmp" -path "*/bin/gh" -type f | head -n 1)"',
            'test -n "$gh_bin"',
            `cp "$gh_bin" ${quote(path.join(binDir, 'gh'))}`,
            `chmod 755 ${quote(path.join(binDir, 'gh'))}`,
            'for profile in "$HOME/.profile" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc" "$HOME/.zprofile"; do touch "$profile"; grep -Fq \'export PATH="$HOME/.local/bin:$PATH"\' "$profile" || printf \'\\n# OpenClaw user-local bin\\nexport PATH="$HOME/.local/bin:$PATH"\\n\' >> "$profile"; done',
        ].join(' && ');
        process.stdout.write(`Installing GitHub CLI locally into ${binDir}/gh...\n`);
        const code = await runInteractiveCommand(command);
        prependPath(binDir);
        return code === 0 && await commandExists('gh');
    }
    catch (error) {
        process.stdout.write(`Automatic gh install failed: ${error instanceof Error ? error.message : String(error)}\n`);
        return false;
    }
}
function parseGitHubRepoFromRemote(remoteUrl) {
    const value = String(remoteUrl || '').trim();
    if (!value)
        return null;
    const sshMatch = value.match(/^git@github\.com:([^/]+\/[^/]+?)(?:\.git)?$/i);
    if (sshMatch)
        return sshMatch[1];
    const httpsMatch = value.match(/^https?:\/\/github\.com\/([^/]+\/[^/]+?)(?:\.git)?$/i);
    if (httpsMatch)
        return httpsMatch[1];
    return null;
}
function isConfiguredGitHubRepo(value) {
    const repo = String(value || '').trim();
    return Boolean(repo && repo !== 'owner/repo' && /^[^/\s]+\/[^/\s]+$/.test(repo));
}
async function detectGitHubRepo() {
    const explicit = String(process.env.OPENCLAW_GITHUB_REPO || '').trim();
    if (isConfiguredGitHubRepo(explicit))
        return explicit;
    const remoteResult = await runCommandCapture('git config --get remote.origin.url');
    if (!remoteResult.ok)
        return null;
    return parseGitHubRepoFromRemote(remoteResult.stdout);
}
function resolveSecretsFile() {
    const explicit = process.env.OPENCLAW_GROWTH_SECRETS_FILE?.trim();
    if (explicit)
        return path.resolve(explicit);
    if (process.env.HOME)
        return path.join(process.env.HOME, '.config', 'openclaw-growth', 'secrets.env');
    return path.resolve('.openclaw-growth-secrets.env');
}
function resolveAscPrivateKeyPath(keyId, suffix = '') {
    const safeKeyId = (keyId || 'OPENCLAW').trim().replace(/[^a-zA-Z0-9_-]/g, '_') || 'OPENCLAW';
    const baseDir = process.env.HOME
        ? path.join(process.env.HOME, '.config', 'openclaw-growth')
        : path.resolve('.openclaw-growth');
    return path.join(baseDir, `AuthKey_${safeKeyId}${suffix}.p8`);
}
function inferAscKeyIdFromPrivateKeyPath(filePath) {
    const fileName = path.basename(String(filePath || '').trim());
    const match = fileName.match(/^AuthKey_([A-Za-z0-9]+)\.p8$/);
    return match?.[1] || '';
}
async function copyAscPrivateKeyToSecurePath(sourcePath, keyId, suffix = '') {
    const destinationPath = resolveAscPrivateKeyPath(keyId, suffix);
    await fs.mkdir(path.dirname(destinationPath), { recursive: true, mode: 0o700 });
    if (path.resolve(sourcePath) !== path.resolve(destinationPath)) {
        await fs.copyFile(sourcePath, destinationPath);
    }
    await fs.chmod(destinationPath, 0o600);
    return destinationPath;
}
function renderEnvValue(value) {
    return `"${String(value).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\$/g, '\\$')}"`;
}
async function readSecretsFile(filePath) {
    const values = new Map();
    let raw = '';
    try {
        raw = await fs.readFile(filePath, 'utf8');
    }
    catch {
        return values;
    }
    for (const line of raw.split(/\r?\n/)) {
        const match = line.match(/^\s*(?:export\s+)?([A-Z0-9_]+)=(.*)\s*$/);
        if (!match)
            continue;
        values.set(match[1], match[2].replace(/^"|"$/g, ''));
    }
    return values;
}
async function writeSecretsFile(filePath, nextValues) {
    const current = await readSecretsFile(filePath);
    for (const [key, value] of Object.entries(nextValues)) {
        if (value === DELETE_SECRET) {
            current.delete(key);
            continue;
        }
        if (value.trim())
            current.set(key, value.trim());
    }
    await fs.mkdir(path.dirname(filePath), { recursive: true, mode: 0o700 });
    const lines = [
        '# OpenClaw Growth local secrets.',
        '# This file is generated by openclaw-growth-wizard.mjs and should not be committed.',
        ...[...current.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([key, value]) => `export ${key}=${renderEnvValue(value)}`),
        '',
    ];
    await fs.writeFile(filePath, lines.join('\n'), { encoding: 'utf8', mode: 0o600 });
    await fs.chmod(filePath, 0o600);
}
function applySecretsToProcessEnv(nextValues) {
    for (const [key, value] of Object.entries(nextValues)) {
        if (value === DELETE_SECRET) {
            delete process.env[key];
            continue;
        }
        if (value.trim())
            process.env[key] = value.trim();
    }
}
function mergeRuntimeEnv(...sources) {
    const env = { ...process.env };
    for (const source of sources) {
        for (const [key, value] of Object.entries(source || {})) {
            if (value === DELETE_SECRET) {
                delete env[key];
                continue;
            }
            if (String(value || '').trim())
                env[key] = String(value).trim();
        }
    }
    return env;
}
function renderBashSingleQuoted(value) {
    return `'${String(value).replace(/'/g, `'\\''`)}'`;
}
function renderIsolatedSecretRunnerInstallScript({ workspaceRoot, configPath, serviceUser, agentUser, }) {
    const workspaceLiteral = renderBashSingleQuoted(workspaceRoot);
    const configLiteral = renderBashSingleQuoted(path.relative(workspaceRoot, configPath) || configPath);
    const serviceUserLiteral = renderBashSingleQuoted(serviceUser);
    const agentUserLiteral = renderBashSingleQuoted(agentUser);
    return `#!/usr/bin/env bash
set -euo pipefail

SERVICE_USER=\${OPENCLAW_GROWTH_SERVICE_USER:-${serviceUserLiteral}}
AGENT_USER=\${OPENCLAW_GROWTH_AGENT_USER:-${agentUserLiteral}}
WORKSPACE=${workspaceLiteral}
CONFIG_PATH=\${OPENCLAW_GROWTH_CONFIG_PATH:-${configLiteral}}
STATE_PATH=\${OPENCLAW_GROWTH_STATE_PATH:-data/openclaw-growth-engineer/state.json}
RUNTIME_DIR=/var/lib/openclaw-growth
SECRETS_FILE="\${RUNTIME_DIR}/secrets.env"
LOCAL_SECRETS_FILE="\${OPENCLAW_GROWTH_LOCAL_SECRETS_FILE:-\${HOME}/.config/openclaw-growth/secrets.env}"
SUDOERS_FILE=/etc/sudoers.d/openclaw-growth

if [ "$(id -u)" -ne 0 ]; then
  echo "Run with sudo: sudo bash .openclaw/secret-runner/install.sh" >&2
  exit 1
fi

if ! id "$SERVICE_USER" >/dev/null 2>&1; then
  if command -v useradd >/dev/null 2>&1; then
    useradd --system --create-home --home-dir "$RUNTIME_DIR" --shell /usr/sbin/nologin "$SERVICE_USER"
  elif command -v dscl >/dev/null 2>&1; then
    echo "macOS service-user creation is not automated by this script. Create $SERVICE_USER manually or use launchd/keychain." >&2
    exit 1
  else
    echo "No supported user creation tool found." >&2
    exit 1
  fi
fi

install -d -m 0750 -o "$SERVICE_USER" -g "$SERVICE_USER" "$RUNTIME_DIR"
install -d -m 0750 -o "$SERVICE_USER" -g "$SERVICE_USER" "$RUNTIME_DIR/keys"
install -d -m 0775 -o "$AGENT_USER" -g "$SERVICE_USER" "$WORKSPACE/data/openclaw-growth-engineer" "$WORKSPACE/.openclaw"
chmod g+rwX "$WORKSPACE/data/openclaw-growth-engineer" "$WORKSPACE/.openclaw"

if [ ! -f "$SECRETS_FILE" ]; then
  install -m 0600 -o "$SERVICE_USER" -g "$SERVICE_USER" /dev/null "$SECRETS_FILE"
fi

if [ -s "$LOCAL_SECRETS_FILE" ] && [ ! -s "$SECRETS_FILE" ]; then
  cp "$LOCAL_SECRETS_FILE" "$SECRETS_FILE"
  chown "$SERVICE_USER:$SERVICE_USER" "$SECRETS_FILE"
  chmod 0600 "$SECRETS_FILE"
  echo "Migrated existing local secrets into $SECRETS_FILE."
  echo "After verifying the isolated runner, delete the old local file if OpenClaw runs as that same user:"
  echo "  rm -f $LOCAL_SECRETS_FILE"
fi

cat >/usr/local/bin/openclaw-growth-health <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="\${OPENCLAW_GROWTH_WORKSPACE:-__WORKSPACE__}"
CONFIG_PATH="\${OPENCLAW_GROWTH_CONFIG_PATH:-__CONFIG_PATH__}"
cd "$WORKSPACE"
export OPENCLAW_GROWTH_SECRETS_FILE="\${OPENCLAW_GROWTH_SECRETS_FILE:-/var/lib/openclaw-growth/secrets.env}"
exec node scripts/openclaw-growth-status.mjs --config "$CONFIG_PATH" --timeout-ms "\${OPENCLAW_GROWTH_STATUS_TIMEOUT_MS:-15000}" --json "$@"
EOF
sed -i.bak "s#__WORKSPACE__#$WORKSPACE#g; s#__CONFIG_PATH__#$CONFIG_PATH#g" /usr/local/bin/openclaw-growth-health
rm -f /usr/local/bin/openclaw-growth-health.bak

cat >/usr/local/bin/openclaw-growth-run <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="\${OPENCLAW_GROWTH_WORKSPACE:-__WORKSPACE__}"
CONFIG_PATH="\${OPENCLAW_GROWTH_CONFIG_PATH:-__CONFIG_PATH__}"
STATE_PATH="\${OPENCLAW_GROWTH_STATE_PATH:-data/openclaw-growth-engineer/state.json}"
cd "$WORKSPACE"
export OPENCLAW_GROWTH_SECRETS_FILE="\${OPENCLAW_GROWTH_SECRETS_FILE:-/var/lib/openclaw-growth/secrets.env}"
exec node scripts/openclaw-growth-runner.mjs --config "$CONFIG_PATH" --state "$STATE_PATH" "$@"
EOF
sed -i.bak "s#__WORKSPACE__#$WORKSPACE#g; s#__CONFIG_PATH__#$CONFIG_PATH#g" /usr/local/bin/openclaw-growth-run
rm -f /usr/local/bin/openclaw-growth-run.bak

chown root:root /usr/local/bin/openclaw-growth-health /usr/local/bin/openclaw-growth-run
chmod 0755 /usr/local/bin/openclaw-growth-health /usr/local/bin/openclaw-growth-run

cat >"$SUDOERS_FILE" <<EOF
# OpenClaw Growth isolated secret runner.
# Allows the agent user to run only the sanitized Growth Engineer wrappers as the secret-owning service user.
$AGENT_USER ALL=($SERVICE_USER) NOPASSWD: /usr/local/bin/openclaw-growth-health
$AGENT_USER ALL=($SERVICE_USER) NOPASSWD: /usr/local/bin/openclaw-growth-run
EOF
chmod 0440 "$SUDOERS_FILE"
if command -v visudo >/dev/null 2>&1; then
  visudo -cf "$SUDOERS_FILE"
fi

echo "Installed isolated OpenClaw Growth secret runner."
echo "Persisted secret file: $SECRETS_FILE"
echo "Edit secrets as root/service operator only:"
echo "  sudoedit $SECRETS_FILE"
echo "OpenClaw may run:"
echo "  sudo -n -u $SERVICE_USER /usr/local/bin/openclaw-growth-health"
echo "  sudo -n -u $SERVICE_USER /usr/local/bin/openclaw-growth-run"
`;
}
async function writeIsolatedSecretRunnerKit(configPath, config, options = {}) {
    const serviceUser = String(options.serviceUser || config?.security?.connectorSecrets?.serviceUser || 'openclaw-growth');
    const agentUser = String(options.agentUser ||
        config?.security?.connectorSecrets?.agentUser ||
        process.env.SUDO_USER ||
        process.env.USER ||
        'openclaw');
    const kitDir = path.resolve('.openclaw/secret-runner');
    const installScriptPath = path.join(kitDir, 'install.sh');
    const readmePath = path.join(kitDir, 'README.md');
    await fs.mkdir(kitDir, { recursive: true });
    await fs.writeFile(installScriptPath, renderIsolatedSecretRunnerInstallScript({
        workspaceRoot: process.cwd(),
        configPath,
        serviceUser,
        agentUser,
    }), { encoding: 'utf8', mode: 0o700 });
    await fs.chmod(installScriptPath, 0o700);
    await fs.writeFile(readmePath, [
        '# OpenClaw Growth Isolated Secret Runner',
        '',
        'This kit keeps connector API keys out of the OpenClaw-readable workspace.',
        '',
        '1. Run `sudo bash .openclaw/secret-runner/install.sh` from this workspace.',
        '2. Put connector secrets in `/var/lib/openclaw-growth/secrets.env` with `sudoedit`.',
        '3. Configure OpenClaw/heartbeat jobs to use the generated sudo commands.',
        '',
        'OpenClaw can read and modify non-secret connector config, but must not read or write API keys.',
        '',
    ].join('\n'), 'utf8');
    config.security = {
        ...(config.security || {}),
        connectorSecrets: {
            mode: 'isolated-runner',
            persisted: true,
            agentReadable: false,
            serviceUser,
            agentUser,
            secretsFile: '/var/lib/openclaw-growth/secrets.env',
            installScript: path.relative(process.cwd(), installScriptPath),
            healthCommand: `sudo -n -u ${serviceUser} /usr/local/bin/openclaw-growth-health`,
            runCommand: `sudo -n -u ${serviceUser} /usr/local/bin/openclaw-growth-run`,
        },
    };
    return { installScriptPath, readmePath, serviceUser };
}
async function askSecretAccessModel(rl, configPath, config) {
    if (!ENABLE_ISOLATED_SECRET_RUNNER_WIZARD) {
        config.security = {
            ...(config.security || {}),
            connectorSecrets: {
                ...(config.security?.connectorSecrets || {}),
                mode: 'openclaw-secret-refs',
                persisted: true,
                agentReadable: 'runtime_resolves_secret_refs',
                secretsFile: resolveSecretsFile(),
            },
        };
        return { config, kit: null };
    }
    process.stdout.write('\nSecret access model\n');
    process.stdout.write('  1) Local user secrets file: simplest, same OS user can read it\n');
    process.stdout.write('  2) Isolated secret runner: separate service user owns persisted secrets; OpenClaw only gets allowlisted run/health commands\n');
    const currentMode = config?.security?.connectorSecrets?.mode === 'isolated-runner' ? '2' : '1';
    const answer = await ask(rl, 'Secret access model (1/2)', currentMode);
    if (answer.trim() !== '2') {
        config.security = {
            ...(config.security || {}),
            connectorSecrets: {
                ...(config.security?.connectorSecrets || {}),
                mode: 'local-user-file',
                persisted: true,
                agentReadable: 'same-os-user-can-read',
                secretsFile: resolveSecretsFile(),
            },
        };
        return { config, kit: null };
    }
    const serviceUser = await ask(rl, 'Service user that owns connector secrets', config?.security?.connectorSecrets?.serviceUser || 'openclaw-growth');
    const agentUser = await ask(rl, 'Agent OS user allowed to run health/growth commands', config?.security?.connectorSecrets?.agentUser || process.env.SUDO_USER || process.env.USER || 'openclaw');
    const kit = await writeIsolatedSecretRunnerKit(configPath, config, { serviceUser, agentUser });
    return { config, kit };
}
function printSecretRunnerKitInstructions(kit) {
    if (!kit)
        return;
    process.stdout.write(`Saved isolated secret runner setup: ${kit.installScriptPath}\n`);
    process.stdout.write('Run once from this workspace after the wizard finishes:\n');
    process.stdout.write(`  sudo bash ${path.relative(process.cwd(), kit.installScriptPath)}\n`);
    process.stdout.write('Then move/persist connector secrets under /var/lib/openclaw-growth/secrets.env with sudoedit.\n');
}
function getGrowthRunCommand(config, displayConfigPath) {
    if (config?.security?.connectorSecrets?.mode === 'isolated-runner' && config.security.connectorSecrets.runCommand) {
        return config.security.connectorSecrets.runCommand;
    }
    return buildGrowthRunnerCommand(displayConfigPath, deriveStatePathFromConfigPath(displayConfigPath));
}
function getConnectorHealthCommand(config, displayConfigPath) {
    if (config?.security?.connectorSecrets?.mode === 'isolated-runner' && config.security.connectorSecrets.healthCommand) {
        return config.security.connectorSecrets.healthCommand;
    }
    return buildGrowthRunnerCommand(displayConfigPath, deriveStatePathFromConfigPath(displayConfigPath));
}
async function maybePromptSecret(rl, label, envName) {
    const existing = process.env[envName]?.trim();
    const suffix = existing ? 'already set in current environment; press Enter to keep' : 'leave empty to skip';
    const value = await ask(rl, `${label} (${suffix})`, '');
    const trimmed = value.trim();
    if (trimmed)
        return trimmed;
    if (existing) {
        process.stdout.write(`Keeping existing ${envName} from the local environment.\n`);
        return existing;
    }
    return '';
}
function defaultSentryTokenEnv({ index, label, baseUrl }) {
    const value = `${label || ''} ${baseUrl || ''}`.toLowerCase();
    if (index === 0 && !value.includes('glitchtip'))
        return 'SENTRY_AUTH_TOKEN';
    if (value.includes('glitchtip'))
        return 'GLITCHTIP_AUTH_TOKEN';
    return `${toEnvName(label || `SENTRY_${index + 1}`, `SENTRY_${index + 1}`)}_AUTH_TOKEN`;
}
function defaultSentryAccountLabel({ index, baseUrl }) {
    const value = String(baseUrl || '').toLowerCase();
    if (value.includes('glitchtip'))
        return 'GlitchTip';
    if (index === 0)
        return 'Sentry Cloud';
    return `Sentry Account ${index + 1}`;
}
function isSentryCloudBaseUrl(baseUrl) {
    const normalized = String(baseUrl || '').trim().replace(/\/$/, '').toLowerCase();
    return normalized === 'https://sentry.io' || normalized === 'https://www.sentry.io';
}
function printSentryTokenGuidance({ baseUrl, tokenEnv }) {
    if (isSentryCloudBaseUrl(baseUrl)) {
        process.stdout.write('\nToken type: use a Sentry personal user/auth token, not an organization integration token.\n');
        process.stdout.write('Sentry token page: https://sentry.io/settings/account/api/auth-tokens/\n');
    }
    else {
        process.stdout.write('\nToken type: use a GlitchTip/Sentry-compatible user auth token for this host.\n');
        process.stdout.write('GlitchTip token page: Profile -> Auth Tokens on your GlitchTip instance.\n');
    }
    printBullets([
        `Paste it as ${tokenEnv}.`,
        'Required scopes: `org:read`, `team:read`, `project:read`, and `event:read`.',
        'Optional for richer release context: `project:releases`.',
    ]);
}
function buildUrl(baseUrl, pathname, params = {}) {
    const url = new URL(pathname, `${String(baseUrl || 'https://sentry.io').replace(/\/$/, '')}/`);
    for (const [key, value] of Object.entries(params)) {
        if (value === undefined || value === null || value === '')
            continue;
        url.searchParams.set(key, String(value));
    }
    return url;
}
function apiListItems(payload) {
    if (Array.isArray(payload))
        return payload;
    if (!payload || typeof payload !== 'object')
        return [];
    if (Array.isArray(payload.results))
        return payload.results;
    if (Array.isArray(payload.data))
        return payload.data;
    if (Array.isArray(payload.projects))
        return payload.projects;
    if (Array.isArray(payload.teams))
        return payload.teams;
    return [];
}
async function fetchSentryJsonPage({ token, url }) {
    const normalizedToken = String(token || '').trim();
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            Authorization: `Bearer ${normalizedToken}`,
            'User-Agent': 'openclaw-growth-wizard',
        },
    });
    const body = await response.text();
    if (!response.ok) {
        return {
            ok: false,
            payload: null,
            detail: `${url.pathname}: HTTP ${response.status}: ${truncate(body, 220)}`,
        };
    }
    try {
        return { ok: true, payload: body ? JSON.parse(body) : null, detail: url.pathname };
    }
    catch (error) {
        return {
            ok: false,
            payload: null,
            detail: `${url.pathname}: invalid JSON (${error instanceof Error ? error.message : String(error)})`,
        };
    }
}
async function fetchSentryJsonList({ baseUrl, token, url }) {
    const items = [];
    const pages = [];
    let nextUrl = url;
    for (let page = 0; nextUrl && page < 10; page += 1) {
        const result = await fetchSentryJsonPage({ token, url: nextUrl });
        pages.push(result.detail);
        if (!result.ok)
            return { ...result, payload: items, detail: pages.join('; ') };
        items.push(...apiListItems(result.payload));
        const next = result.payload && typeof result.payload === 'object' ? result.payload.next : null;
        nextUrl = typeof next === 'string' && next.trim() ? new URL(next, `${String(baseUrl || 'https://sentry.io').replace(/\/$/, '')}/`) : null;
    }
    return { ok: true, payload: items, detail: pages.join('; ') };
}
async function discoverSentryOrganizations({ baseUrl, token }) {
    const normalizedToken = String(token || '').trim();
    if (!normalizedToken)
        return { ok: false, organizations: [], detail: 'missing token' };
    const url = buildUrl(baseUrl, '/api/0/organizations/', { per_page: 100 });
    const result = await fetchSentryJsonList({ baseUrl, token: normalizedToken, url });
    if (!result.ok)
        return { ok: false, organizations: [], detail: result.detail };
    const organizations = apiListItems(result.payload)
        .map((organization) => ({
        slug: String(organization?.slug || organization?.name || '').trim(),
        name: String(organization?.name || organization?.slug || '').trim(),
    }))
        .filter((organization) => organization.slug);
    return {
        ok: true,
        organizations: Array.from(new Map(organizations.map((organization) => [organization.slug, organization])).values()),
        detail: `found ${organizations.length} org(s)`,
    };
}
async function discoverSentryProjects({ baseUrl, token, org }) {
    const normalizedOrg = String(org || '').trim();
    const normalizedToken = String(token || '').trim();
    if (!normalizedOrg || !normalizedToken) {
        return { ok: false, projects: [], detail: 'missing org or token' };
    }
    const projectSlugs = (payload) => apiListItems(payload)
        .map((project) => String(project?.slug || project?.name || '').trim())
        .filter(Boolean);
    const attempted = [];
    try {
        const orgProjectsUrl = buildUrl(baseUrl, `/api/0/organizations/${encodeURIComponent(normalizedOrg)}/projects/`, {
            per_page: 100,
        });
        const orgProjects = await fetchSentryJsonList({ baseUrl, token: normalizedToken, url: orgProjectsUrl });
        attempted.push(orgProjects.detail);
        if (orgProjects.ok) {
            const projects = projectSlugs(orgProjects.payload);
            if (projects.length > 0) {
                return { ok: true, projects: [...new Set(projects)], detail: `found ${projects.length} project(s)` };
            }
        }
        const teamsUrl = buildUrl(baseUrl, `/api/0/organizations/${encodeURIComponent(normalizedOrg)}/teams/`, {
            per_page: 100,
        });
        const teams = await fetchSentryJsonList({ baseUrl, token: normalizedToken, url: teamsUrl });
        attempted.push(teams.detail);
        if (teams.ok) {
            const teamSlugs = apiListItems(teams.payload)
                .map((team) => String(team?.slug || team?.name || '').trim())
                .filter(Boolean);
            const allTeamProjects = [];
            for (const teamSlug of teamSlugs) {
                const teamProjectsUrl = buildUrl(baseUrl, `/api/0/teams/${encodeURIComponent(normalizedOrg)}/${encodeURIComponent(teamSlug)}/projects/`, { per_page: 100 });
                const teamProjects = await fetchSentryJsonList({ baseUrl, token: normalizedToken, url: teamProjectsUrl });
                attempted.push(teamProjects.detail);
                if (teamProjects.ok)
                    allTeamProjects.push(...projectSlugs(teamProjects.payload));
            }
            if (allTeamProjects.length > 0) {
                return {
                    ok: true,
                    projects: [...new Set(allTeamProjects)],
                    detail: `found ${allTeamProjects.length} project(s) via teams`,
                };
            }
        }
        const allProjectsUrl = buildUrl(baseUrl, '/api/0/projects/', { per_page: 100 });
        const allProjects = await fetchSentryJsonList({ baseUrl, token: normalizedToken, url: allProjectsUrl });
        attempted.push(allProjects.detail);
        if (allProjects.ok) {
            const projects = apiListItems(allProjects.payload)
                .filter((project) => {
                const projectOrg = String(project?.organization?.slug || project?.organization?.name || '').trim();
                return !projectOrg || projectOrg === normalizedOrg;
            })
                .map((project) => String(project?.slug || project?.name || '').trim())
                .filter(Boolean);
            if (projects.length > 0) {
                return { ok: true, projects: [...new Set(projects)], detail: `found ${projects.length} project(s)` };
            }
        }
        return {
            ok: false,
            projects: [],
            detail: `found 0 project(s); tried ${attempted.filter(Boolean).join('; ')}`,
        };
    }
    catch (error) {
        return {
            ok: false,
            projects: [],
            detail: `${error instanceof Error ? error.message : String(error)}; tried ${attempted.filter(Boolean).join('; ')}`,
        };
    }
}
async function upsertSentryAccountsConfig(configPath, accounts) {
    if (!accounts.length || !(await fileExists(configPath)))
        return false;
    const config = await readJsonFile(configPath);
    const existingAccounts = Array.isArray(config?.sources?.sentry?.accounts)
        ? config.sources.sentry.accounts
        : [];
    const merged = new Map();
    for (const account of existingAccounts) {
        if (isPlaceholderSentryAccount(account))
            continue;
        const id = String(account?.id || account?.key || account?.label || '').trim();
        if (id)
            merged.set(id, account);
    }
    for (const account of accounts) {
        merged.set(account.id, {
            ...(merged.get(account.id) || {}),
            ...account,
        });
    }
    config.sources = {
        ...(config.sources || {}),
        sentry: {
            ...(config.sources?.sentry || {}),
            enabled: true,
            mode: 'command',
            command: normalizeWizardSourceCommand('sentry', config.sources?.sentry || {}, configPath),
            accounts: [...merged.values()],
        },
    };
    await writeJsonFile(configPath, config);
    return true;
}
function isPlaceholderSentryAccount(account) {
    const baseUrl = String(account?.baseUrl || account?.base_url || account?.url || '').trim().toLowerCase();
    const org = String(account?.org || account?.organization || '').trim().toLowerCase();
    const projects = Array.isArray(account?.projects)
        ? account.projects.map((project) => String(project || '').trim().toLowerCase())
        : [];
    return (org === 'owner-org' ||
        baseUrl.includes('example.com') ||
        projects.includes('ios-app') ||
        projects.includes('backend-api') ||
        projects.includes('web-app'));
}
async function verifySentryAccountsConfig(configPath, expectedAccounts) {
    if (!(await fileExists(configPath))) {
        return { ok: false, detail: `${configPath} does not exist` };
    }
    const config = await readJsonFile(configPath);
    const source = config?.sources?.sentry;
    if (!source || source.enabled !== true) {
        return { ok: false, detail: 'sources.sentry.enabled is not true' };
    }
    if (source.mode !== 'command') {
        return { ok: false, detail: 'sources.sentry.mode is not command' };
    }
    const configuredAccounts = Array.isArray(source.accounts) ? source.accounts : [];
    const realAccounts = configuredAccounts.filter((account) => !isPlaceholderSentryAccount(account));
    if (realAccounts.length === 0) {
        return { ok: false, detail: 'sources.sentry.accounts contains no non-placeholder account' };
    }
    const configuredIds = new Set(realAccounts.map((account) => String(account?.id || account?.key || '').trim()).filter(Boolean));
    const missingIds = expectedAccounts
        .map((account) => String(account?.id || '').trim())
        .filter((id) => id && !configuredIds.has(id));
    if (missingIds.length > 0) {
        return { ok: false, detail: `sources.sentry.accounts is missing configured account id(s): ${missingIds.join(', ')}` };
    }
    return { ok: true, detail: `${realAccounts.length} active Sentry-compatible account(s) configured` };
}
async function upsertPaddleAccountsConfig(configPath, accounts) {
    if (!accounts.length || !(await fileExists(configPath)))
        return false;
    const config = await readJsonFile(configPath);
    const existingAccounts = Array.isArray(config?.sources?.paddle?.accounts)
        ? config.sources.paddle.accounts
        : [];
    const merged = new Map();
    for (const account of existingAccounts) {
        const id = String(account?.id || account?.key || account?.label || '').trim();
        if (id)
            merged.set(id, account);
    }
    for (const account of accounts) {
        merged.set(account.id, {
            ...(merged.get(account.id) || {}),
            ...account,
        });
    }
    const tokenEnv = accounts[0]?.tokenEnv || config?.sources?.paddle?.tokenEnv || config?.secrets?.paddleTokenEnv || 'PADDLE_API_KEY';
    config.sources = {
        ...(config.sources || {}),
        paddle: {
            ...(config.sources?.paddle || {}),
            enabled: true,
            mode: 'command',
            command: normalizeWizardSourceCommand('paddle', config.sources?.paddle || {}, configPath),
            environment: config.sources?.paddle?.environment || 'live',
            tokenEnv,
            accounts: [...merged.values()],
        },
    };
    config.secrets = {
        ...(config.secrets || {}),
        paddleTokenEnv: tokenEnv,
        paddleTokenRef: { source: 'env', provider: 'default', id: tokenEnv },
    };
    await writeJsonFile(configPath, config);
    return true;
}
async function verifyPaddleAccountsConfig(configPath, expectedAccounts) {
    if (!(await fileExists(configPath))) {
        return { ok: false, detail: `${configPath} does not exist` };
    }
    const config = await readJsonFile(configPath);
    const source = config?.sources?.paddle;
    if (!source || source.enabled !== true) {
        return { ok: false, detail: 'sources.paddle.enabled is not true' };
    }
    if (source.mode !== 'command') {
        return { ok: false, detail: 'sources.paddle.mode is not command' };
    }
    const configuredAccounts = Array.isArray(source.accounts) ? source.accounts : [];
    if (configuredAccounts.length === 0) {
        return { ok: false, detail: 'sources.paddle.accounts contains no account' };
    }
    const configuredIds = new Set(configuredAccounts.map((account) => String(account?.id || account?.key || '').trim()).filter(Boolean));
    const missingIds = expectedAccounts
        .map((account) => String(account?.id || '').trim())
        .filter((id) => id && !configuredIds.has(id));
    if (missingIds.length > 0) {
        return { ok: false, detail: `sources.paddle.accounts is missing configured account id(s): ${missingIds.join(', ')}` };
    }
    return { ok: true, detail: `${configuredAccounts.length} Paddle account(s) configured` };
}
async function upsertCoolifyConfig(configPath, { baseUrl, tokenEnv = 'COOLIFY_API_TOKEN' }) {
    if (!(await fileExists(configPath)))
        return false;
    const coolifyCommand = `${getWizardDefaultSourceCommand('coolify')} --config ${quote(configPath)}`;
    const config = await readJsonFile(configPath);
    config.sources = {
        ...(config.sources || {}),
        coolify: {
            ...(config.sources?.coolify || {}),
            enabled: true,
            mode: 'command',
            command: coolifyCommand,
            baseUrl,
            tokenEnv,
        },
    };
    config.secrets = {
        ...(config.secrets || {}),
        coolifyTokenEnv: tokenEnv,
        coolifyTokenRef: { source: 'env', provider: 'default', id: tokenEnv },
    };
    await writeJsonFile(configPath, config);
    return true;
}
const ASC_PRIVATE_KEY_BEGIN = '-----BEGIN PRIVATE KEY-----';
const ASC_PRIVATE_KEY_END = '-----END PRIVATE KEY-----';
const BRACKETED_PASTE_START = new RegExp(`${String.fromCharCode(27)}\\[200~`, 'g');
const BRACKETED_PASTE_END = new RegExp(`${String.fromCharCode(27)}\\[201~`, 'g');
function formatPemBase64(value) {
    return String(value || '').match(/.{1,64}/g)?.join('\n') || '';
}
function normalizeAscPrivateKeyContent(value) {
    const raw = String(value || '')
        .replace(BRACKETED_PASTE_START, '')
        .replace(BRACKETED_PASTE_END, '')
        .replace(/\r\n/g, '\n')
        .trim();
    if (!raw) {
        return { ok: false, value: '', error: 'No private key content pasted.' };
    }
    const beginIndex = raw.indexOf(ASC_PRIVATE_KEY_BEGIN);
    const endIndex = raw.indexOf(ASC_PRIVATE_KEY_END);
    if (beginIndex < 0 || endIndex < 0 || endIndex <= beginIndex) {
        if (raw.includes('-----BEGIN PRIVATE KEY') && beginIndex < 0) {
            return {
                ok: false,
                value: '',
                error: `Malformed .p8 header. The first line must be exactly ${ASC_PRIVATE_KEY_BEGIN}`,
            };
        }
        if (raw.includes('-----END PRIVATE KEY') && endIndex < 0) {
            return {
                ok: false,
                value: '',
                error: `Malformed .p8 footer. The last line must be exactly ${ASC_PRIVATE_KEY_END}`,
            };
        }
        return {
            ok: false,
            value: '',
            error: `Missing exact .p8 markers. Paste from ${ASC_PRIVATE_KEY_BEGIN} through ${ASC_PRIVATE_KEY_END}.`,
        };
    }
    const body = raw
        .slice(beginIndex + ASC_PRIVATE_KEY_BEGIN.length, endIndex)
        .replace(/\s+/g, '');
    if (!body) {
        return { ok: false, value: '', error: 'The .p8 key body is empty.' };
    }
    if (!/^[A-Za-z0-9+/=]+$/.test(body)) {
        return {
            ok: false,
            value: '',
            error: 'The .p8 key body contains non-base64 characters. Copy the downloaded AuthKey file content without redactions or extra text.',
        };
    }
    return {
        ok: true,
        value: `${ASC_PRIVATE_KEY_BEGIN}\n${formatPemBase64(body)}\n${ASC_PRIVATE_KEY_END}\n`,
        error: null,
    };
}
function validateAscPrivateKeyContent(value) {
    const normalized = normalizeAscPrivateKeyContent(value);
    if (!normalized.ok)
        return normalized;
    try {
        createPrivateKey(normalized.value);
        return normalized;
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            ok: false,
            value: '',
            error: `Invalid .p8 private key content: ${message}. Make sure you copied the downloaded AuthKey_<KEY_ID>.p8 file, including both marker lines, with no truncation.`,
        };
    }
}
async function askAscPrivateKeyContent(rl, options = {}) {
    const envName = options.envName || 'ASC_PRIVATE_KEY';
    const persistLabel = options.persistLabel || 'ASC_PRIVATE_KEY_PATH';
    const keyLabel = options.keyLabel || 'this App Store Connect key';
    process.stdout.write(`\nPaste the full .p8 file content for ${keyLabel}.\nLeave the first line empty if the .p8 file is already saved on this host.\n`);
    process.stdout.write(`The wizard validates the pasted key, stores it locally with chmod 600, and only saves ${persistLabel}.\n`);
    while (true) {
        const value = await readAscPrivateKeyPaste(rl, envName);
        if (!value.trim())
            return '';
        const validation = validateAscPrivateKeyContent(value);
        if (validation.ok)
            return validation.value;
        process.stdout.write(`${validation.error}\n`);
        process.stdout.write('The .p8 was not saved. Paste the full file again from BEGIN to END, or leave empty to use a path.\n');
    }
}
async function readAscPrivateKeyPaste(rl, envName = 'ASC_PRIVATE_KEY') {
    return await new Promise((resolve, reject) => {
        let buffer = '';
        let settled = false;
        let finishing = false;
        let lineCount = 0;
        const previousEncoding = process.stdin.readableEncoding;
        const cleanup = () => {
            process.stdin.off('data', onData);
            process.stdin.off('error', onError);
            if (previousEncoding)
                process.stdin.setEncoding(previousEncoding);
            rl.resume();
        };
        const complete = (value) => {
            settled = true;
            cleanup();
            resolve(value ? `${String(value).trim()}\n` : '');
        };
        const finish = (value, options = {}) => {
            if (settled || finishing)
                return;
            finishing = true;
            const drainMs = options.drainMs ?? 0;
            if (drainMs > 0) {
                setTimeout(() => complete(value), drainMs);
            }
            else {
                complete(value);
            }
        };
        const onError = (error) => {
            if (settled || finishing)
                return;
            settled = true;
            cleanup();
            reject(error);
        };
        const onData = (chunk) => {
            if (finishing)
                return;
            buffer += String(chunk);
            lineCount = buffer.split(/\r?\n/).length;
            if (/^\s*(?:\r?\n)/.test(buffer)) {
                finish('');
                return;
            }
            const endMatch = buffer.match(/-----END PRIVATE KEY-+[^\r\n]*(?:\r?\n|$)/);
            if (endMatch?.index !== undefined) {
                finish(buffer.slice(0, endMatch.index + endMatch[0].length), { drainMs: 750 });
                return;
            }
            if (lineCount > 80) {
                process.stdout.write('Paste looks incomplete: no -----END PRIVATE KEY----- line found within 80 lines.\n');
                finish('');
            }
        };
        rl.pause();
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', onData);
        process.stdin.on('error', onError);
        process.stdout.write(`${envName} content: `);
        process.stdin.resume();
    });
}
async function validateAscPrivateKeyPath(filePath) {
    const raw = await fs.readFile(filePath, 'utf8');
    return validateAscPrivateKeyContent(raw);
}
async function askAscPrivateKeyPath(rl, options = {}) {
    const label = options.label || 'ASC_PRIVATE_KEY_PATH (path to AuthKey_XXXX.p8, leave empty to skip)';
    const defaultValue = options.defaultValue ?? process.env.ASC_PRIVATE_KEY_PATH ?? '';
    while (true) {
        const privateKeyPath = await ask(rl, label, defaultValue);
        const trimmedPath = privateKeyPath.trim();
        if (!trimmedPath)
            return '';
        try {
            const validation = await validateAscPrivateKeyPath(trimmedPath);
            if (validation.ok)
                return trimmedPath;
            process.stdout.write(`${validation.error}\n`);
        }
        catch (error) {
            process.stdout.write(`Could not read .p8 file: ${error instanceof Error ? error.message : String(error)}\n`);
        }
        process.stdout.write('The ASC private key path was not saved. Paste a valid path, or leave empty to skip.\n');
    }
}
async function askAscPrivateKeyPathWithKeyId(rl, options = {}) {
    const keyLabel = options.keyLabel || 'App Store Connect key';
    while (true) {
        const privateKeyPath = await askAscPrivateKeyPath(rl, options);
        if (!privateKeyPath)
            return { privateKeyPath: '', keyId: '' };
        const keyId = inferAscKeyIdFromPrivateKeyPath(privateKeyPath);
        if (keyId)
            return { privateKeyPath, keyId };
        process.stdout.write(`Could not infer Key ID for ${keyLabel} from the .p8 file name.\n`);
        process.stdout.write('Use Apple\'s original downloaded file name: AuthKey_<KEY_ID>.p8. Do not rename the .p8 file.\n');
    }
}
function printSection(title, lines = []) {
    process.stdout.write(`\n${ANSI.bold}${title}${ANSI.reset}\n`);
    process.stdout.write(`${'-'.repeat(title.length)}\n`);
    for (const line of lines) {
        process.stdout.write(`${line}\n`);
    }
    if (lines.length > 0)
        process.stdout.write('\n');
}
function printBullets(lines) {
    for (const line of lines) {
        process.stdout.write(`  - ${line}\n`);
    }
    process.stdout.write('\n');
}
function bold(text) {
    return `${ANSI.bold}${text}${ANSI.reset}`;
}
async function guideGitHubConnector(rl, secrets) {
    printSection('GitHub code access', [
        `${bold('Create token')} here: https://github.com/settings/tokens/new`,
        `${bold('Scopes')}: public repos = public_repo, private repos/issues/PRs = repo.`,
        `${bold('Only add workflow')} if OpenClaw should edit GitHub Actions files.`,
    ]);
    let hasGh = await commandExists('gh');
    if (!hasGh) {
        hasGh = await installGitHubCliUserLocal();
    }
    if (hasGh) {
        process.stdout.write('GitHub CLI is available for helper commands.\n\n');
    }
    const token = await maybePromptSecret(rl, 'Paste GITHUB_TOKEN into this local terminal', 'GITHUB_TOKEN');
    if (token)
        secrets.GITHUB_TOKEN = token;
    else
        process.stdout.write('No GitHub token saved. GitHub setup remains pending; rerun this wizard when ready.\n\n');
    const detectedRepo = await detectGitHubRepo();
    if (detectedRepo) {
        secrets.OPENCLAW_GITHUB_REPO = detectedRepo;
        process.stdout.write(`Detected GitHub repo for this workspace: ${detectedRepo}\n\n`);
    }
    else if (token || process.env.GITHUB_TOKEN) {
        process.stdout.write('GitHub auth is saved. Repo selection is deferred per app/task; no global repo is required.\n\n');
    }
}
function shouldForceFreshAnalyticsToken(healthByConnector = {}) {
    const health = getConnectorHealth('analytics', healthByConnector);
    const detail = String(health?.detail || '');
    return ['blocked', 'partial'].includes(String(health?.status || '')) || /revoked|unauthorized|invalid token/i.test(detail);
}
async function guideAnalyticsConnector(rl, secrets, options = {}) {
    printSection('AnalyticsCLI', [
        `${bold('Create readonly CLI token')}: https://dash.analyticscli.com/`,
        `${bold('Path')}: Account -> API Keys -> Create Access Token.`,
    ]);
    const forceFresh = Boolean(options.forceFresh);
    if (forceFresh && process.env.ANALYTICSCLI_ACCESS_TOKEN) {
        process.stdout.write('Stored token failed. Paste a new token.\n\n');
    }
    const token = forceFresh
        ? await ask(rl, 'Paste the new AnalyticsCLI readonly CLI token into this local terminal', '')
        : await maybePromptSecret(rl, 'Paste AnalyticsCLI readonly CLI token into this local terminal', 'ANALYTICSCLI_ACCESS_TOKEN');
    if (token) {
        secrets.ANALYTICSCLI_ACCESS_TOKEN = token;
        secrets.ANALYTICSCLI_READONLY_TOKEN = token;
    }
    else
        process.stdout.write('No AnalyticsCLI token saved. Product analytics setup remains pending; rerun this wizard when ready.\n\n');
}
async function guideRevenueCatConnector(rl, secrets) {
    printSection('RevenueCat monetization data', [
        `${bold('Create secret API key')}: https://app.revenuecat.com/`,
        `${bold('Path')}: Apps & providers -> API keys -> New secret key.`,
        `${bold('Permissions')}: API v2, read for Charts metrics, Customer information, Project configuration.`,
    ]);
    const apiKey = await maybePromptSecret(rl, 'Paste REVENUECAT_API_KEY into this local terminal', 'REVENUECAT_API_KEY');
    if (apiKey)
        secrets.REVENUECAT_API_KEY = apiKey;
}
function paddleAccountIdFromLabel(label, index) {
    const normalized = String(label || '')
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '_')
        .replace(/^_+|_+$/g, '');
    return normalized || `paddle_${index + 1}`;
}
function paddleTokenEnvForAccount(index, label) {
    if (index === 0)
        return 'PADDLE_API_KEY';
    const suffix = paddleAccountIdFromLabel(label, index).toUpperCase().replace(/[^A-Z0-9]+/g, '_');
    const base = suffix && suffix !== `PADDLE_${index + 1}` ? `PADDLE_API_KEY_${suffix}` : `PADDLE_API_KEY_${index + 1}`;
    return base.replace(/_+/g, '_');
}
async function guidePaddleConnector(rl, secrets) {
    printSection('Paddle Billing metrics', [
        `${bold('Create live API key')}: https://vendors.paddle.com/authentication-v2`,
        `${bold('Minimum')}: metrics.read. Better: all read-only *.read scopes.`,
        `${bold('Do not grant write scopes')} unless you explicitly need them elsewhere.`,
    ]);
    const accounts = [];
    let index = 0;
    while (true) {
        const label = await ask(rl, index === 0 ? 'Paddle account label' : 'Next Paddle account label (empty = done)', index === 0 ? 'Paddle' : '');
        if (!label.trim())
            break;
        const tokenEnv = paddleTokenEnvForAccount(index, label);
        const apiKey = await maybePromptSecret(rl, `Paste ${tokenEnv} into this local terminal`, tokenEnv);
        if (apiKey)
            secrets[tokenEnv] = apiKey;
        accounts.push({
            id: paddleAccountIdFromLabel(label, index),
            label: label.trim(),
            tokenEnv,
            environment: 'live',
        });
        index += 1;
        const addAnother = await askYesNo(rl, 'Add another Paddle account?', false);
        if (!addAnother)
            break;
    }
    return accounts;
}
async function guideSeoConnector(rl, secrets) {
    printSection('SEO / Google Search Console / DataForSEO', [
        `${bold('GSC')}: https://search.google.com/search-console`,
        `${bold('Service account')}: https://console.cloud.google.com/iam-admin/serviceaccounts`,
        `${bold('Optional paid keyword data')}: https://app.dataforseo.com/api-dashboard`,
        `${bold('Default')}: leave property URL empty to use all verified GSC properties.`,
    ]);
    const siteUrl = await ask(rl, 'Optional GSC property URL (empty = all verified properties)', process.env.GSC_SITE_URL || '');
    if (siteUrl.trim())
        secrets.GSC_SITE_URL = siteUrl.trim();
    const gscToken = await maybePromptSecret(rl, 'Paste GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN, or leave empty for service-account/all-sites/CSV mode', 'GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN');
    if (gscToken)
        secrets.GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN = gscToken;
    const useDataForSeo = await askYesNo(rl, 'Also store DataForSEO credentials for optional paid keyword research?', false);
    if (useDataForSeo) {
        const login = await maybePromptSecret(rl, 'Paste DATAFORSEO_LOGIN into this local terminal', 'DATAFORSEO_LOGIN');
        const password = await maybePromptSecret(rl, 'Paste DATAFORSEO_PASSWORD into this local terminal', 'DATAFORSEO_PASSWORD');
        if (login)
            secrets.DATAFORSEO_LOGIN = login;
        if (password)
            secrets.DATAFORSEO_PASSWORD = password;
    }
}
function buildAccountSignalExtraSourceConfig(key, existing = {}, accounts = []) {
    const definition = getAccountSignalConnectorDefinition(key);
    if (!definition)
        return existing;
    const accountConfig = accounts.length > 0
        ? {
            accounts: mergeConnectorAccounts(existing.accounts, accounts),
        }
        : {};
    return {
        ...buildExtraSourceConfig(definition.service, {
            key: definition.key,
            label: definition.label,
            enabled: true,
            mode: 'file',
            secretEnv: definition.credentials[0]?.env || null,
            hint: definition.signalHint,
        }),
        ...existing,
        key: definition.key,
        label: definition.label,
        service: definition.service,
        enabled: true,
        mode: existing.mode || 'file',
        path: existing.path || getDefaultSourcePath(definition.key),
        secretEnv: existing.secretEnv || definition.credentials[0]?.env || null,
        accountWide: true,
        projectScope: 'discover_from_account',
        docsUrl: definition.docsUrl,
        signalKind: definition.sourceKind,
        experimental: Boolean(definition.experimental),
        hint: existing.hint || definition.signalHint,
        ...accountConfig,
    };
}
function mergeConnectorAccounts(existingAccounts, nextAccounts) {
    const merged = new Map();
    for (const account of Array.isArray(existingAccounts) ? existingAccounts : []) {
        const id = String(account?.id || account?.key || account?.label || '').trim();
        if (id)
            merged.set(id, account);
    }
    for (const account of nextAccounts) {
        const id = String(account?.id || account?.key || account?.label || '').trim();
        if (!id)
            continue;
        merged.set(id, {
            ...(merged.get(id) || {}),
            ...account,
        });
    }
    return [...merged.values()];
}
async function upsertAccountSignalConnectorConfig(configPath, key, accounts = []) {
    const definition = getAccountSignalConnectorDefinition(key);
    if (!definition)
        return false;
    const config = await loadEditableConfig(configPath);
    const sources = config.sources && typeof config.sources === 'object' ? config.sources : {};
    const extra = Array.isArray(sources.extra) ? sources.extra : [];
    const nextExtra = extra.filter((source) => String(source?.key || source?.service || '') !== definition.key);
    const existing = extra.find((source) => String(source?.key || source?.service || '') === definition.key) || {};
    nextExtra.push(buildAccountSignalExtraSourceConfig(key, existing, accounts));
    config.sources = {
        ...sources,
        extra: nextExtra,
    };
    await writeJsonFile(configPath, config);
    return true;
}
function accountSignalTokenEnvForAccount(baseEnv, key, index, label) {
    if (index === 0)
        return baseEnv;
    const suffix = toConfigId(label || key, `${key}_${index + 1}`).toUpperCase().replace(/[^A-Z0-9]+/g, '_');
    return `${baseEnv}_${suffix}`.replace(/_+/g, '_');
}
async function guideAccountSignalConnector(rl, secrets, key) {
    const definition = getAccountSignalConnectorDefinition(key);
    if (!definition)
        return [];
    printSection(definition.label, [
        `${bold('Docs')}: ${definition.docsUrl}`,
        `${bold('Setup is account-wide')}. Do not paste project IDs, app IDs, product IDs, package names, paywall IDs, service names, or tags here.`,
        `${bold('Paste only credentials')} below. The agent discovers accounts/apps/projects later.`,
    ]);
    const accounts = [];
    let index = 0;
    while (true) {
        const label = await ask(rl, index === 0 ? `${definition.label} account label` : `Next ${definition.label} account label (empty = done)`, index === 0 ? definition.label.replace(/\s+\(experimental\)$/i, '') : '');
        if (!label.trim())
            break;
        const credentialEnvs = {};
        for (const credential of definition.credentials) {
            const envName = accountSignalTokenEnvForAccount(credential.env, key, index, label);
            const defaultValue = index === 0 ? credential.defaultValue ?? process.env[credential.env] ?? '' : '';
            const prompt = envName === credential.env ? credential.prompt : `${credential.prompt.replace(credential.env, envName)}`;
            const value = credential.optional
                ? await maybePromptSecret(rl, prompt, envName)
                : await maybePromptSecret(rl, prompt, envName);
            const finalValue = value || defaultValue;
            credentialEnvs[credential.env] = envName;
            if (finalValue)
                secrets[envName] = finalValue;
            else if (!credential.optional) {
                process.stdout.write(`${envName} was not saved. ${definition.label} setup remains pending for ${label}; rerun this wizard when ready.\n`);
            }
        }
        accounts.push({
            id: toConfigId(label, `${key}_${index + 1}`),
            label: label.trim(),
            credentialEnvs,
            tokenEnv: credentialEnvs[definition.credentials[0]?.env] || definition.credentials[0]?.env || null,
            accountWide: true,
            projectScope: 'discover_from_account',
        });
        index += 1;
        const addAnother = await askYesNo(rl, `Add another ${definition.label} account?`, false);
        if (!addAnother)
            break;
    }
    return accounts;
}
async function guideSentryConnector(rl, secrets) {
    printSection('Sentry / GlitchTip', [
        `${bold('Base URL')}: https://sentry.io for Sentry Cloud, otherwise your GlitchTip/self-hosted URL.`,
        `${bold('Token + org')} are needed. Project scope remains unpinned.`,
    ]);
    const accounts = [];
    let index = 0;
    while (true) {
        const baseUrl = await ask(rl, `Sentry account ${index + 1} base URL`, index === 0 ? process.env.SENTRY_BASE_URL || 'https://sentry.io' : 'https://sentry.io');
        const defaultLabel = defaultSentryAccountLabel({ index, baseUrl });
        const label = await ask(rl, `Sentry account ${index + 1} label`, defaultLabel);
        const id = toConfigId(label || baseUrl, `sentry_${index + 1}`);
        const tokenEnv = defaultSentryTokenEnv({ index, label, baseUrl });
        printSentryTokenGuidance({ baseUrl, tokenEnv });
        const token = await maybePromptSecret(rl, `Paste ${tokenEnv} into this local terminal`, tokenEnv);
        if (token)
            secrets[tokenEnv] = token;
        let discoveredOrganizations = [];
        if (token) {
            process.stdout.write(`Discovering Sentry / GlitchTip organizations for ${label}...\n`);
            const organizationDiscovery = await discoverSentryOrganizations({ baseUrl, token });
            if (organizationDiscovery.ok && organizationDiscovery.organizations.length > 0) {
                discoveredOrganizations = organizationDiscovery.organizations;
                process.stdout.write(`Found org(s): ${discoveredOrganizations.map((organization) => organization.slug).join(', ')}\n`);
            }
            else if (!organizationDiscovery.ok) {
                process.stdout.write(`${ANSI.dim}Could not list organizations automatically (${organizationDiscovery.detail}).${ANSI.reset}\n`);
            }
        }
        let org = '';
        if (discoveredOrganizations.length === 1) {
            org = discoveredOrganizations[0].slug;
            process.stdout.write(`Using organization: ${org}\n`);
        }
        else if (discoveredOrganizations.length > 1) {
            process.stdout.write('Select organization:\n');
            const orgChoice = await askListSelection(rl, `Organization for ${label}`, discoveredOrganizations.map((organization) => ({
                value: organization.slug,
                label: organization.slug,
                description: organization.name && organization.name !== organization.slug ? organization.name : '',
            })), { includeManual: true, includeDefer: true });
            org = orgChoice === '__manual__'
                ? await ask(rl, `Sentry org slug for ${label}`, index === 0 ? process.env.SENTRY_ORG || '' : '')
                : orgChoice;
        }
        else {
            org = await ask(rl, `Sentry org slug for ${label} (leave empty to defer)`, index === 0 ? process.env.SENTRY_ORG || '' : '');
        }
        const environment = await ask(rl, `Sentry environment for ${label}`, index === 0 ? process.env.SENTRY_ENVIRONMENT || 'production' : 'production');
        if (org.trim() && token) {
            process.stdout.write(`Checking visible Sentry projects for ${label} without pinning project scope...\n`);
            const discovery = await discoverSentryProjects({ baseUrl, token, org });
            let verifiedVisibleProjects = false;
            if (discovery.ok && discovery.projects.length > 0) {
                verifiedVisibleProjects = true;
                process.stdout.write(`Found ${discovery.projects.length} visible project(s). Project scope remains unpinned.\n`);
            }
            else {
                const fallbackOrgs = discoveredOrganizations
                    .map((organization) => organization.slug)
                    .filter((slug) => slug && slug !== org.trim());
                for (const fallbackOrg of fallbackOrgs) {
                    process.stdout.write(`Trying visible org ${fallbackOrg}...\n`);
                    const fallbackDiscovery = await discoverSentryProjects({ baseUrl, token, org: fallbackOrg });
                    if (fallbackDiscovery.ok && fallbackDiscovery.projects.length > 0) {
                        org = fallbackOrg;
                        verifiedVisibleProjects = true;
                        process.stdout.write(`Using org ${fallbackOrg}; found ${fallbackDiscovery.projects.length} visible project(s). Project scope remains unpinned.\n`);
                        break;
                    }
                }
                if (!verifiedVisibleProjects && !discovery.ok) {
                    process.stdout.write(`Could not verify visible projects automatically (${discovery.detail}). Project scope will be resolved from app context later.\n`);
                }
            }
        }
        else {
            process.stdout.write('Project discovery needs both a token and org slug. Project scope will be resolved from app context later.\n');
        }
        accounts.push({
            id,
            label,
            baseUrl,
            tokenEnv,
            ...(org.trim() ? { org: org.trim() } : {}),
            ...(environment.trim() ? { environment: environment.trim() } : {}),
        });
        if (index === 0) {
            if (tokenEnv === 'SENTRY_AUTH_TOKEN' && token)
                secrets.SENTRY_AUTH_TOKEN = token;
            if (org.trim())
                secrets.SENTRY_ORG = org.trim();
            if (environment.trim())
                secrets.SENTRY_ENVIRONMENT = environment.trim();
            if (baseUrl.trim() && baseUrl.trim() !== 'https://sentry.io')
                secrets.SENTRY_BASE_URL = baseUrl.trim();
        }
        const addAnother = await askYesNo(rl, 'Configure another Sentry / GlitchTip account now, for example on another base URL?', false);
        if (!addAnother)
            break;
        index += 1;
    }
    return accounts;
}
function normalizeCoolifyBaseUrl(value) {
    const raw = String(value || '').trim().replace(/\/+$/, '');
    if (!raw)
        return '';
    return /^https?:\/\//i.test(raw) ? raw : `https://${raw}`;
}
async function guideCoolifyConnector(rl, secrets) {
    printSection('Coolify deployment monitoring', [
        `${bold('Create read-only API token')} in Coolify.`,
        `${bold('Do not use * or sensitive-token permissions')} for normal monitoring.`,
    ]);
    const baseUrl = normalizeCoolifyBaseUrl(await ask(rl, 'Coolify base URL', process.env.COOLIFY_BASE_URL || 'https://coolify.wotaso.com'));
    const tokenUrl = baseUrl ? `${baseUrl}/security/api-tokens` : 'https://<your-coolify-host>/security/api-tokens';
    process.stdout.write(`${bold('Token page')}: ${tokenUrl}\n\n`);
    const token = await maybePromptSecret(rl, 'Paste COOLIFY_API_TOKEN into this local terminal', 'COOLIFY_API_TOKEN');
    if (baseUrl)
        secrets.COOLIFY_BASE_URL = baseUrl;
    if (token)
        secrets.COOLIFY_API_TOKEN = token;
    return { baseUrl, tokenEnv: 'COOLIFY_API_TOKEN' };
}
async function guideAscConnector(rl, secrets) {
    printSection('App Store Connect CLI', [
        `${bold('Create 2 API keys')} here: https://appstoreconnect.apple.com/access/integrations/api`,
        `1. ${bold('Reports key')} - role ${bold('Sales and Reports')} - saved for Growth Engineer.`,
        `2. ${bold('Setup key')} - role ${bold('Admin')} - used once, then revoke.`,
    ]);
    process.stdout.write(`${bold('Enter the Reports key now:')}\n`);
    printBullets([
        `${bold('.p8 path')} to Apple\'s original ${bold('AuthKey_<KEY_ID>.p8')} file. ${bold('Do not rename it')}; KEY_ID is read from the filename.`,
        `The wizard saves a secure local copy with ${bold('chmod 600')}.`,
        `${bold('Issuer ID')} from the API keys page. Same value for both keys.`,
        `${bold('Vendor Number')} from Sales and Trends > Reports.`,
    ]);
    const normalKeyPath = await askAscPrivateKeyPathWithKeyId(rl, {
        label: 'Reports .p8 path (AuthKey_<KEY_ID>.p8, empty = paste)',
        defaultValue: process.env.ASC_PRIVATE_KEY_PATH || '',
        keyLabel: 'the normal reporting key',
    });
    let keyId = normalKeyPath.keyId;
    if (normalKeyPath.privateKeyPath) {
        const securePrivateKeyPath = await copyAscPrivateKeyToSecurePath(normalKeyPath.privateKeyPath, keyId);
        secrets.ASC_PRIVATE_KEY_PATH = securePrivateKeyPath;
        secrets.ASC_PRIVATE_KEY = DELETE_SECRET;
        secrets.ASC_PRIVATE_KEY_B64 = DELETE_SECRET;
        secrets.ASC_KEY_ID = keyId;
        process.stdout.write(`Inferred ASC_KEY_ID=${keyId} from ${path.basename(normalKeyPath.privateKeyPath)}.\n`);
        process.stdout.write(`Saved secure Reports key copy to ${securePrivateKeyPath} with chmod 600.\n`);
    }
    const issuerId = await ask(rl, 'ASC_ISSUER_ID (same for both keys, empty = skip)', process.env.ASC_ISSUER_ID || '');
    if (issuerId.trim())
        secrets.ASC_ISSUER_ID = issuerId.trim();
    if (!normalKeyPath.privateKeyPath) {
        keyId = await ask(rl, 'ASC_KEY_ID (from AuthKey_<KEY_ID>.p8, empty = skip)', process.env.ASC_KEY_ID || '');
        if (keyId.trim())
            secrets.ASC_KEY_ID = keyId.trim();
        const privateKeyContent = await askAscPrivateKeyContent(rl, {
            keyLabel: 'the normal reporting key',
        });
        if (!privateKeyContent)
            return await guideAscBootstrapAdminKey(rl, issuerId.trim());
        const privateKeyPath = resolveAscPrivateKeyPath(keyId);
        await fs.mkdir(path.dirname(privateKeyPath), { recursive: true, mode: 0o700 });
        await fs.writeFile(privateKeyPath, privateKeyContent, { encoding: 'utf8', mode: 0o600 });
        await fs.chmod(privateKeyPath, 0o600);
        secrets.ASC_PRIVATE_KEY_PATH = privateKeyPath;
        secrets.ASC_PRIVATE_KEY = DELETE_SECRET;
        secrets.ASC_PRIVATE_KEY_B64 = DELETE_SECRET;
        process.stdout.write(`Saved ASC private key to ${privateKeyPath} with chmod 600.\n`);
    }
    const vendorNumber = await ask(rl, 'ASC_VENDOR_NUMBER (Sales and Trends > Reports)', process.env.ASC_VENDOR_NUMBER || '');
    if (vendorNumber.trim())
        secrets.ASC_VENDOR_NUMBER = vendorNumber.trim();
    return await guideAscBootstrapAdminKey(rl, issuerId.trim());
}
async function guideAscBootstrapAdminKey(rl, issuerIdDefault = '') {
    const bootstrapEnv = {};
    process.stdout.write(`\n${bold('Enter the Setup Admin key:')}\n`);
    printBullets([
        `${bold('Role must be Admin')} so Apple can create the first App Analytics report request.`,
        `${bold('Use original AuthKey_<KEY_ID>.p8 filename')} so KEY_ID is read automatically.`,
        `${bold('Not saved')} to secrets.env. The temporary secure copy stays on this host; revoke the Admin key after setup.`,
    ]);
    const bootstrapKeyPath = await askAscPrivateKeyPathWithKeyId(rl, {
        label: 'Setup Admin .p8 path (AuthKey_<KEY_ID>.p8, empty = paste)',
        defaultValue: '',
        keyLabel: 'the temporary Admin key',
    });
    let bootstrapKeyId = bootstrapKeyPath.keyId;
    let bootstrapIssuerId = String(issuerIdDefault || '').trim();
    if (!bootstrapIssuerId) {
        bootstrapIssuerId = await ask(rl, 'ASC_ISSUER_ID (same API keys page)', process.env.ASC_ISSUER_ID || '');
    }
    if (bootstrapKeyPath.privateKeyPath) {
        const secureBootstrapPath = await copyAscPrivateKeyToSecurePath(bootstrapKeyPath.privateKeyPath, bootstrapKeyId, '_bootstrap_admin');
        bootstrapEnv.ASC_BOOTSTRAP_PRIVATE_KEY_PATH = secureBootstrapPath;
        process.stdout.write(`Inferred ASC_BOOTSTRAP_KEY_ID=${bootstrapKeyId} from ${path.basename(bootstrapKeyPath.privateKeyPath)}.\n`);
        process.stdout.write(`Saved secure temporary Admin key copy to ${secureBootstrapPath} with chmod 600.\n`);
    }
    else {
        bootstrapKeyId = await ask(rl, 'ASC_BOOTSTRAP_KEY_ID (from AuthKey_<KEY_ID>.p8)', '');
    }
    if (!bootstrapKeyId.trim() || !bootstrapIssuerId.trim())
        return { bootstrapEnv };
    bootstrapEnv.ASC_BOOTSTRAP_KEY_ID = bootstrapKeyId.trim();
    bootstrapEnv.ASC_BOOTSTRAP_ISSUER_ID = bootstrapIssuerId.trim();
    if (!bootstrapKeyPath.privateKeyPath) {
        const bootstrapPrivateKeyContent = await askAscPrivateKeyContent(rl, {
            envName: 'ASC_BOOTSTRAP_PRIVATE_KEY',
            persistLabel: 'ASC_BOOTSTRAP_PRIVATE_KEY_PATH temporarily',
            keyLabel: 'the temporary Admin key',
        });
        if (!bootstrapPrivateKeyContent)
            return { bootstrapEnv };
        const bootstrapPrivateKeyPath = resolveAscPrivateKeyPath(bootstrapKeyId, '_bootstrap_admin');
        await fs.mkdir(path.dirname(bootstrapPrivateKeyPath), { recursive: true, mode: 0o700 });
        await fs.writeFile(bootstrapPrivateKeyPath, bootstrapPrivateKeyContent, { encoding: 'utf8', mode: 0o600 });
        await fs.chmod(bootstrapPrivateKeyPath, 0o600);
        bootstrapEnv.ASC_BOOTSTRAP_PRIVATE_KEY_PATH = bootstrapPrivateKeyPath;
        process.stdout.write(`Saved temporary Admin ASC private key to ${bootstrapPrivateKeyPath} with chmod 600. Revoke the Admin key after setup.\n`);
    }
    return { bootstrapEnv };
}
async function cleanupTemporaryAscBootstrapPrivateKey(bootstrapEnv = {}) {
    const privateKeyPath = String(bootstrapEnv.ASC_BOOTSTRAP_PRIVATE_KEY_PATH || '').trim();
    if (!privateKeyPath)
        return;
    if (privateKeyPath === String(bootstrapEnv.ASC_PRIVATE_KEY_PATH || process.env.ASC_PRIVATE_KEY_PATH || '').trim()) {
        process.stdout.write('Temporary Admin .p8 path matches the steady-state ASC_PRIVATE_KEY_PATH; kept it in place.\n');
        return;
    }
    process.stdout.write(`Kept temporary Admin .p8 copy at ${privateKeyPath}.\n`);
}
function printAscBootstrapAdminRevokeNotice(bootstrapEnv = {}) {
    const keyId = String(bootstrapEnv.ASC_BOOTSTRAP_KEY_ID || '').trim();
    const keyLabel = keyId ? `Admin key ${keyId}` : 'temporary Admin key';
    process.stdout.write(`\n${bold(`IMPORTANT: Revoke the ASC ${keyLabel} now.`)}\n`);
    process.stdout.write('Growth Engineer only needed this Admin key once for setup. The Reports key is used from now on.\n');
    process.stdout.write('App Store Connect API keys: https://appstoreconnect.apple.com/access/integrations/api\n');
}
async function writeSelfUpdateState(workspaceRoot, value) {
    const statePath = path.join(workspaceRoot, 'data/openclaw-growth-engineer/self-update.json');
    await writeJsonFile(statePath, {
        version: 1,
        checkedAt: new Date().toISOString(),
        ...value,
    });
}
async function rerunCurrentWizardWithoutSelfUpdate() {
    return await new Promise((resolve) => {
        const child = spawn(process.execPath, process.argv.slice(1), {
            env: {
                ...process.env,
                OPENCLAW_GROWTH_SKIP_SELF_UPDATE: '1',
            },
            stdio: 'inherit',
        });
        child.on('error', () => resolve(1));
        child.on('close', (code) => resolve(code));
    });
}
async function filesHaveSameContent(leftPath, rightPath) {
    try {
        const [left, right] = await Promise.all([fs.readFile(leftPath), fs.readFile(rightPath)]);
        return left.equals(right);
    }
    catch {
        return false;
    }
}
function getSelfUpdateSkillCandidates(workspaceRoot) {
    const explicit = String(process.env.OPENCLAW_GROWTH_SKILL_SLUG || '').trim();
    const uniqueSlugs = [...new Set([explicit, ...SELF_UPDATE_SKILL_SLUG_CANDIDATES].filter(Boolean))];
    return uniqueSlugs.map((slug) => {
        const skillRoot = path.join(workspaceRoot, 'skills', slug);
        return {
            slug,
            skillRoot,
            originPath: path.join(skillRoot, '.clawhub/origin.json'),
            wizardPath: path.join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'),
            bootstrapPath: path.join(skillRoot, 'scripts/bootstrap-openclaw-workspace.sh'),
        };
    });
}
function resolveInstalledSelfUpdateSkill(workspaceRoot) {
    return getSelfUpdateSkillCandidates(workspaceRoot).find((candidate) => existsSync(candidate.originPath)) || null;
}
async function maybeSelfUpdateFromClawHub(args) {
    if (args.noSelfUpdate)
        return false;
    if (isTruthyEnv(process.env.OPENCLAW_GROWTH_SKIP_SELF_UPDATE))
        return false;
    if (isTruthyEnv(process.env.OPENCLAW_GROWTH_DISABLE_SELF_UPDATE))
        return false;
    if (isFalseyEnv(process.env.OPENCLAW_GROWTH_SELF_UPDATE))
        return false;
    const workspaceRoot = process.cwd();
    const installedSkill = resolveInstalledSelfUpdateSkill(workspaceRoot);
    if (!installedSkill)
        return false;
    if (!(await commandExists('npx')))
        return false;
    const beforeOrigin = await readJsonIfPresent(installedSkill.originPath).catch(() => null);
    const beforeVersion = String(beforeOrigin?.installedVersion || '');
    process.stdout.write(`Checking for Growth Engineer skill updates (${installedSkill.slug})...\n`);
    const updateResult = await runCommandCaptureWithTimeout(`npx -y clawhub --no-input --dir skills update ${quote(installedSkill.slug)} --force`, { timeoutMs: 120_000 });
    const afterOrigin = await readJsonIfPresent(installedSkill.originPath).catch(() => null);
    const afterVersion = String(afterOrigin?.installedVersion || beforeVersion || '');
    const workspaceWizardPath = path.resolve(process.argv[1] || 'scripts/openclaw-growth-wizard.mjs');
    const runtimeOutdated = !(await filesHaveSameContent(workspaceWizardPath, installedSkill.wizardPath));
    await writeSelfUpdateState(workspaceRoot, {
        lastCheckedAt: new Date().toISOString(),
        ok: updateResult.ok,
        skillSlug: installedSkill.slug,
        skillRoot: installedSkill.skillRoot,
        previousVersion: beforeVersion || null,
        installedVersion: afterVersion || null,
    }).catch(() => { });
    if (!updateResult.ok) {
        const detail = String(updateResult.stderr || updateResult.stdout || 'update failed').trim().split(/\r?\n/).pop();
        process.stdout.write(`${ANSI.dim}Skill update check skipped: ${detail}${ANSI.reset}\n`);
        return false;
    }
    if ((!afterVersion || afterVersion === beforeVersion) && !runtimeOutdated) {
        return false;
    }
    if (afterVersion && afterVersion !== beforeVersion) {
        process.stdout.write(`Updated OpenClaw Growth Engineer skill ${beforeVersion || 'unknown'} -> ${afterVersion}. Refreshing workspace runtime...\n`);
    }
    else {
        process.stdout.write('Refreshing workspace runtime from the installed OpenClaw Growth Engineer skill...\n');
    }
    const bootstrapResult = await runCommandCaptureWithTimeout(`bash ${quote(installedSkill.bootstrapPath)}`, { timeoutMs: 60_000 });
    if (!bootstrapResult.ok) {
        process.stdout.write(`${ANSI.dim}Workspace runtime refresh failed; continuing with current process.${ANSI.reset}\n`);
        return false;
    }
    process.stdout.write('Restarting wizard with refreshed runtime...\n');
    const code = await rerunCurrentWizardWithoutSelfUpdate();
    process.exit(code ?? 0);
}
async function runConnectorSetupSteps({ rl, args, selected, healthByConnector, allowIsolationPrompt = true, }) {
    clearTerminal();
    printConnectorIntro();
    process.stdout.write(`${ANSI.bold}Selected connectors${ANSI.reset}\n`);
    for (const key of selected) {
        process.stdout.write(`  - ${connectorLabel(key)}\n`);
    }
    process.stdout.write('\n');
    const secrets = {};
    let sentryAccounts = [];
    let paddleAccounts = [];
    let coolifyConfig = null;
    let ascBootstrapRevokeEnv = null;
    if (selected.includes('analytics')) {
        let forceFreshAnalyticsToken = shouldForceFreshAnalyticsToken(healthByConnector);
        while (true) {
            clearTerminal();
            await guideAnalyticsConnector(rl, secrets, { forceFresh: forceFreshAnalyticsToken });
            const check = await runImmediateConnectorHealthCheck({
                rl,
                configPath: args.config,
                connector: 'analytics',
                secrets,
            });
            if (!check.retry)
                break;
            forceFreshAnalyticsToken = true;
        }
    }
    if (selected.includes('github')) {
        while (true) {
            clearTerminal();
            await guideGitHubConnector(rl, secrets);
            const check = await runImmediateConnectorHealthCheck({
                rl,
                configPath: args.config,
                connector: 'github',
                secrets,
            });
            if (!check.retry)
                break;
        }
    }
    if (selected.includes('revenuecat')) {
        while (true) {
            clearTerminal();
            await guideRevenueCatConnector(rl, secrets);
            const check = await runImmediateConnectorHealthCheck({
                rl,
                configPath: args.config,
                connector: 'revenuecat',
                secrets,
            });
            if (!check.retry)
                break;
        }
    }
    if (selected.includes('paddle')) {
        while (true) {
            clearTerminal();
            paddleAccounts = await guidePaddleConnector(rl, secrets);
            const check = await runImmediateConnectorHealthCheck({
                rl,
                configPath: args.config,
                connector: 'paddle',
                secrets,
                paddleAccounts,
            });
            if (!check.retry)
                break;
        }
    }
    if (selected.includes('seo')) {
        while (true) {
            clearTerminal();
            await guideSeoConnector(rl, secrets);
            const check = await runImmediateConnectorHealthCheck({
                rl,
                configPath: args.config,
                connector: 'seo',
                secrets,
            });
            if (!check.retry)
                break;
        }
    }
    if (selected.includes('sentry')) {
        while (true) {
            clearTerminal();
            sentryAccounts = await guideSentryConnector(rl, secrets);
            const check = await runImmediateConnectorHealthCheck({
                rl,
                configPath: args.config,
                connector: 'sentry',
                secrets,
                sentryAccounts,
            });
            if (!check.retry)
                break;
        }
    }
    if (selected.includes('coolify')) {
        while (true) {
            clearTerminal();
            coolifyConfig = await guideCoolifyConnector(rl, secrets);
            if (coolifyConfig?.baseUrl) {
                await upsertCoolifyConfig(args.config, coolifyConfig);
            }
            const check = await runImmediateConnectorHealthCheck({
                rl,
                configPath: args.config,
                connector: 'coolify',
                secrets,
            });
            if (!check.retry)
                break;
        }
    }
    if (selected.includes('asc')) {
        while (true) {
            clearTerminal();
            const ascSetup = await guideAscConnector(rl, secrets);
            let bootstrapEnv = ascSetup?.bootstrapEnv || {};
            let check = await runImmediateConnectorHealthCheck({
                rl,
                configPath: args.config,
                connector: 'asc',
                secrets,
                runtimeEnv: bootstrapEnv,
            });
            await cleanupTemporaryAscBootstrapPrivateKey(bootstrapEnv);
            if (check.ok) {
                ascBootstrapRevokeEnv = bootstrapEnv;
            }
            if (!check.retry)
                break;
        }
    }
    for (const connector of selected.filter(isAccountSignalConnector)) {
        while (true) {
            clearTerminal();
            const accountSignalAccounts = await guideAccountSignalConnector(rl, secrets, connector);
            await upsertAccountSignalConnectorConfig(args.config, connector, accountSignalAccounts);
            const check = await runImmediateConnectorHealthCheck({
                rl,
                configPath: args.config,
                connector,
                secrets,
            });
            if (!check.retry)
                break;
        }
    }
    const secretsFile = resolveSecretsFile();
    const wroteSecrets = Object.keys(secrets).length > 0;
    clearTerminal();
    if (wroteSecrets) {
        await writeSecretsFile(secretsFile, secrets);
        process.stdout.write(`\nSaved local secrets to ${secretsFile} with chmod 600.\n`);
    }
    else {
        process.stdout.write('\nNo new secrets were written.\n');
    }
    if (sentryAccounts.length > 0 && await upsertSentryAccountsConfig(args.config, sentryAccounts)) {
        const readiness = await verifySentryAccountsConfig(args.config, sentryAccounts);
        if (readiness.ok) {
            process.stdout.write(`Configured ${sentryAccounts.length} Sentry-compatible account(s) in ${args.config}.\n`);
        }
    }
    if (paddleAccounts.length > 0 && await upsertPaddleAccountsConfig(args.config, paddleAccounts)) {
        const readiness = await verifyPaddleAccountsConfig(args.config, paddleAccounts);
        if (readiness.ok) {
            process.stdout.write(`Configured ${paddleAccounts.length} Paddle account(s) in ${args.config}.\n`);
        }
    }
    if (coolifyConfig?.baseUrl && await upsertCoolifyConfig(args.config, coolifyConfig)) {
        process.stdout.write(`Configured Coolify monitoring for ${coolifyConfig.baseUrl} in ${args.config}.\n`);
    }
    const env = mergeRuntimeEnv(secrets, selected.includes('asc') ? { ASC_BYPASS_KEYCHAIN: '1' } : {});
    const command = `${nodeRuntimeScriptCommand('openclaw-growth-start.mjs')} --config ${quote(args.config)} --setup-only --connectors ${quote(selected.join(','))} --only-connectors ${quote(selected.join(','))}`;
    let setupResult = await runSetupCommandWithProgress(command, env, selected, 'Testing connector setup...');
    let setupPayload = parseJsonFromStdout(setupResult.stdout);
    const postSetupBlockers = [];
    if (sentryAccounts.length > 0 && await upsertSentryAccountsConfig(args.config, sentryAccounts)) {
        const readiness = await verifySentryAccountsConfig(args.config, sentryAccounts);
        if (readiness.ok) {
            process.stdout.write(`Sentry-compatible account config is up to date in ${args.config}.\n`);
        }
        else {
            postSetupBlockers.push({
                check: 'connection:sentry',
                detail: readiness.detail,
                remediation: 'Rerun Sentry/GlitchTip setup so the active config persists sources.sentry.enabled=true and sources.sentry.accounts[].',
            });
        }
    }
    if (paddleAccounts.length > 0 && await upsertPaddleAccountsConfig(args.config, paddleAccounts)) {
        const readiness = await verifyPaddleAccountsConfig(args.config, paddleAccounts);
        if (readiness.ok) {
            process.stdout.write(`Paddle account config is up to date in ${args.config}.\n`);
        }
        else {
            postSetupBlockers.push({
                check: 'connection:paddle',
                detail: readiness.detail,
                remediation: 'Rerun Paddle setup so the active config persists sources.paddle.enabled=true and sources.paddle.accounts[].',
            });
        }
    }
    if (coolifyConfig?.baseUrl && await upsertCoolifyConfig(args.config, coolifyConfig)) {
        process.stdout.write(`Coolify config is up to date in ${args.config}.\n`);
    }
    if (postSetupBlockers.length > 0) {
        setupPayload = {
            ...(setupPayload || {}),
            ok: false,
            blockers: [...(Array.isArray(setupPayload?.blockers) ? setupPayload.blockers : []), ...postSetupBlockers],
        };
        printSetupFailure({ result: { ...setupResult, ok: false, code: setupResult.code ?? 1 }, payload: setupPayload, command });
        process.exitCode = 1;
        return false;
    }
    if (setupResult.ok && setupPayload?.ok !== false) {
        printSetupSuccess(setupPayload);
        if (wroteSecrets) {
            process.stdout.write('Future OpenClaw Growth commands load this secrets file automatically.\n');
        }
        if (ascBootstrapRevokeEnv) {
            printAscBootstrapAdminRevokeNotice(ascBootstrapRevokeEnv);
        }
        await maybeRefreshOpenClawSessionInstructions(rl, args.config);
        const configureIsolation = allowIsolationPrompt && ENABLE_ISOLATED_SECRET_RUNNER_WIZARD && await askYesNo(rl, 'Generate an isolated secret runner so OpenClaw can run health checks without reading API keys?', true);
        if (configureIsolation) {
            const config = await loadEditableConfig(args.config);
            const secretAccess = await askSecretAccessModel(rl, path.resolve(args.config), config);
            await writeJsonFile(path.resolve(args.config), config);
            const manifestPath = await writeOpenClawJobManifest(path.resolve(args.config), config);
            process.stdout.write(`Saved OpenClaw job manifest: ${manifestPath}\n`);
            printSecretRunnerKitInstructions(secretAccess.kit);
        }
        return true;
    }
    printSetupFailure({ result: setupResult, payload: setupPayload, command });
    process.exitCode = 1;
    return false;
}
async function runConnectorSetupWizard(args) {
    if (!process.stdin.isTTY || !process.stdout.isTTY) {
        throw new Error('Connector wizard requires an interactive terminal.');
    }
    const rl = createInterface({ input: process.stdin, output: process.stdout });
    try {
        while (true) {
            clearTerminal();
            printConnectorIntro({
                introDetail: 'API keys stay in this host\'s local secrets file. Use Esc/← in menus or type :back in text prompts to return.',
            });
            await migrateRuntimeSourceCommandsFile(args.config);
            const requestedConnectors = args.connectors ? parseConnectorList(args.connectors) : [];
            const healthCheckConnectors = requestedConnectors.length > 0
                ? orderConnectors(requestedConnectors)
                : await connectorKeysForHealthCheck(args.config);
            const healthByConnector = await withConnectorHealthLoading((onProgress) => getConnectorPickerHealth(args.config, onProgress, healthCheckConnectors), healthCheckConnectors);
            const existingFixes = connectorKeysNeedingAttention(healthByConnector);
            let chosenConnectors;
            try {
                chosenConnectors =
                    requestedConnectors.length > 0
                        ? orderConnectors(requestedConnectors)
                        : await askConnectorSelectionWithHealth(rl, healthByConnector, existingFixes);
            }
            catch (error) {
                if (error instanceof WizardBackError)
                    return 'back';
                throw error;
            }
            const selected = requestedConnectors.length > 0
                ? orderConnectors(chosenConnectors)
                : withMissingRequiredAnalyticsConnector(chosenConnectors);
            if (selected.length === 0) {
                throw new Error(`No supported connectors selected. Use ${CONNECTOR_KEYS.join(', ')}, or all.`);
            }
            try {
                const setupOk = await runConnectorSetupSteps({ rl, args, selected, healthByConnector });
                if (!setupOk)
                    return 'done';
            }
            catch (error) {
                if (error instanceof WizardBackError)
                    continue;
                throw error;
            }
            return 'done';
        }
    }
    finally {
        rl.close();
    }
}
function clearPromptInput(rl) {
    try {
        rl.write?.(null, { ctrl: true, name: 'u' });
    }
    catch {
        // Best-effort cleanup for stale pasted terminal input before showing a prompt.
    }
}
function isBackAnswer(value) {
    const normalized = String(value || '').trim().toLowerCase();
    return [':back', '\x1b'].includes(normalized);
}
async function askQuestionWithEscBack(rl, query) {
    if (!process.stdin.isTTY || !process.stdin.setRawMode) {
        return await rl.question(query);
    }
    emitKeypressEvents(process.stdin);
    const wasRaw = process.stdin.isRaw;
    const controller = new AbortController();
    let backRequested = false;
    const onKeypress = (_text, key) => {
        if (key?.name !== 'escape')
            return;
        backRequested = true;
        clearPromptInput(rl);
        controller.abort();
    };
    process.stdin.on('keypress', onKeypress);
    process.stdin.setRawMode(true);
    try {
        return await rl.question(query, { signal: controller.signal });
    }
    catch (error) {
        if (backRequested || error?.name === 'AbortError') {
            process.stdout.write('\n');
            throw new WizardBackError();
        }
        throw error;
    }
    finally {
        process.stdin.off('keypress', onKeypress);
        process.stdin.setRawMode(Boolean(wasRaw));
    }
}
async function ask(rl, label, defaultValue = '') {
    const suffix = defaultValue ? ` (${defaultValue})` : '';
    clearPromptInput(rl);
    const answer = (await askQuestionWithEscBack(rl, `${label}${suffix}: `)).trim();
    if (isBackAnswer(answer))
        throw new WizardBackError();
    return answer || defaultValue;
}
async function askYesNo(rl, label, defaultYes = true) {
    const suffix = defaultYes ? '[Y/n]' : '[y/N]';
    while (true) {
        clearPromptInput(rl);
        const answer = (await askQuestionWithEscBack(rl, `${label} ${suffix} `)).trim().toLowerCase();
        if (isBackAnswer(answer))
            throw new WizardBackError();
        if (!answer)
            return defaultYes;
        if (answer === 'y' || answer === 'yes')
            return true;
        if (answer === 'n' || answer === 'no')
            return false;
        if (answer.includes('private key')) {
            process.stdout.write('That looks like leftover .p8 key text, not a yes/no answer. Ignoring it.\n');
        }
        else {
            process.stdout.write('Please answer y or n.\n');
        }
    }
}
function truncateTableCell(value, width) {
    const text = String(value || '').replace(/\s+/g, ' ').trim();
    if (text.length <= width)
        return text.padEnd(width, ' ');
    return `${text.slice(0, Math.max(0, width - 3))}...`.padEnd(width, ' ');
}
function printAsciiTable(headers, rows, widths) {
    const border = `+${widths.map((width) => '-'.repeat(width + 2)).join('+')}+`;
    const renderRow = (cells) => `| ${cells.map((cell, index) => truncateTableCell(cell, widths[index])).join(' | ')} |`;
    process.stdout.write(`${border}\n`);
    process.stdout.write(`${renderRow(headers)}\n`);
    process.stdout.write(`${border}\n`);
    for (const row of rows) {
        process.stdout.write(`${renderRow(row)}\n`);
    }
    process.stdout.write(`${border}\n`);
}
function printCadencePlan(cadences) {
    process.stdout.write('\nDefault growth cadence:\n');
    printAsciiTable(['Cadence', 'Every', 'Mode', 'Primary focus', 'What it decides'], cadences.map((cadence) => [
        cadence.key,
        cadence.intervalMinutes ? `${cadence.intervalMinutes}m` : `${cadence.intervalDays}d`,
        cadence.criticalOnly ? 'critical only' : 'full review',
        Array.isArray(cadence.focusAreas) ? cadence.focusAreas.slice(0, 4).join(', ') : '',
        cadence.objective,
    ]), [12, 7, 13, 30, 42]);
    process.stdout.write('\n');
}
async function askToolUsage(rl) {
    return await askMenuChoice(rl, {
        title: 'How should OpenClaw Growth Engineer run?',
        subtitle: 'Use Up/Down to move, Enter to continue, or press 1-3.',
        defaultValue: 'production_autopilot',
        options: [
            {
                value: 'production_autopilot',
                label: 'Production autopilot',
                detail: 'Notify, draft issues/PR handoffs, and analyze on schedule.',
            },
            {
                value: 'advisory',
                label: 'Advisory only',
                detail: 'Analyze and write OpenClaw chat summaries; no GitHub artifacts by default.',
            },
            {
                value: 'manual_reports',
                label: 'Manual reports',
                detail: 'Mostly one-off runs with conservative scheduling.',
            },
        ],
    });
}
async function askSchedulePreset(rl) {
    return await askMenuChoice(rl, {
        title: 'Schedule preset',
        subtitle: 'Use Up/Down to move, Enter to continue, or press 1-3.',
        defaultValue: 'recommended',
        options: [
            {
                value: 'recommended',
                label: 'Recommended',
                detail: 'OpenClaw/Hermes wake every 30m; Sentry/GlitchTip/Coolify healthcheck runs every 90m; daily and larger reviews stay on cadence.',
            },
            {
                value: 'quiet',
                label: 'Quiet',
                detail: 'OpenClaw/Hermes wake hourly; healthcheck runs every 6h; deep reviews unchanged.',
            },
            {
                value: 'manual',
                label: 'Manual',
                detail: 'Enter runner, connector-health, cron, and cadence intervals yourself.',
            },
        ],
    });
}
async function askCadencePlan(rl, existingCadences = []) {
    const existingByKey = new Map((Array.isArray(existingCadences) ? existingCadences : [])
        .filter((cadence) => cadence?.key)
        .map((cadence) => [String(cadence.key), cadence]));
    const cadences = DEFAULT_CADENCE_PLAN.map((cadence) => ({
        ...cadence,
        ...(existingByKey.get(cadence.key) || {}),
    }));
    printCadencePlan(cadences);
    const selectedCadences = await askMultiChoice(rl, {
        title: 'Scheduled review cadences',
        subtitle: 'Use Up/Down to move, Space to toggle cadences, A to toggle all, Enter to continue.',
        defaultValues: cadences.filter((cadence) => cadence.enabled !== false).map((cadence) => cadence.key),
        minSelections: 1,
        options: cadences.map((cadence) => ({
            value: cadence.key,
            label: cadence.title,
            detail: `${cadence.intervalMinutes ? `${cadence.intervalMinutes}m` : `${cadence.intervalDays}d`}, ${cadence.criticalOnly ? 'critical only' : 'full review'} - ${cadence.objective}`,
        })),
    });
    const selected = new Set(selectedCadences);
    cadences.forEach((cadence) => {
        cadence.enabled = selected.has(cadence.key);
    });
    const customize = await askYesNo(rl, 'Customize objectives, instructions, focus areas, or source priorities for enabled cadences?', false);
    if (!customize)
        return cadences;
    for (const cadence of cadences) {
        if (cadence.enabled === false)
            continue;
        process.stdout.write(`\n${cadence.title}\n`);
        const intervalDefault = cadence.intervalMinutes ? `${cadence.intervalMinutes}m` : `${cadence.intervalDays || 1}d`;
        const intervalRaw = await ask(rl, `${cadence.key} interval (for example 90m, 1d, 7d)`, intervalDefault);
        const intervalMatch = String(intervalRaw || intervalDefault).trim().match(/^(\d+)\s*([md])$/i);
        if (intervalMatch?.[2]?.toLowerCase() === 'm') {
            cadence.intervalMinutes = Number.parseInt(intervalMatch[1], 10) || cadence.intervalMinutes || 90;
            delete cadence.intervalDays;
        }
        else if (intervalMatch?.[2]?.toLowerCase() === 'd') {
            cadence.intervalDays = Number.parseInt(intervalMatch[1], 10) || cadence.intervalDays || 1;
            delete cadence.intervalMinutes;
        }
        cadence.objective = await ask(rl, `${cadence.key} objective`, cadence.objective);
        cadence.instructions = await ask(rl, `${cadence.key} instructions`, cadence.instructions);
        const focusAreas = await ask(rl, `${cadence.key} focus areas (comma-separated)`, cadence.focusAreas.join(','));
        cadence.focusAreas = focusAreas.split(',').map((value) => value.trim()).filter(Boolean);
        const sourcePriorities = await ask(rl, `${cadence.key} source priorities (comma-separated)`, cadence.sourcePriorities.join(','));
        cadence.sourcePriorities = sourcePriorities.split(',').map((value) => value.trim()).filter(Boolean);
        cadence.criticalOnly = await askYesNo(rl, `${cadence.key} should only alert on critical findings?`, cadence.criticalOnly);
    }
    return cadences;
}
async function askWizardGoal(rl) {
    return await askMenuChoice(rl, {
        title: 'What do you want to configure?',
        subtitle: 'Use Up/Down to move, Enter to continue, or press 1-4.',
        defaultValue: 'full',
        renderHeader: printWizardHeader,
        options: [
            {
                value: 'connectors',
                label: 'Connectors',
                detail: 'Credentials, provider setup, and health checks.',
            },
            {
                value: 'outputs_intervals',
                label: 'Outputs and intervals',
                detail: 'Daily/weekly/monthly jobs, GitHub issue/PR delivery, and OpenClaw chat notifications.',
            },
            {
                value: 'full',
                label: 'Full setup',
                detail: 'Project, connectors, outputs, intervals, and sources.',
            },
            {
                value: 'intervals',
                label: 'Advanced intervals only',
                detail: 'Runner wake-up interval and connector health check cadence.',
            },
        ],
    });
}
function printWizardHeader() {
    process.stdout.write('OpenClaw Growth Engineer - Setup Wizard\n');
    process.stdout.write('This wizard can configure connector secrets. Normal config is written to config JSON; API keys stay in the local chmod 600 secrets file.\n');
    process.stdout.write(`${ANSI.dim}Use Esc/← in menus or type :back in text prompts to return.${ANSI.reset}\n\n`);
}
async function buildDefaultWizardConfig(configPath = null) {
    return {
        version: 7,
        generatedAt: new Date().toISOString(),
        project: {
            githubRepo: '',
            repoRoot: '.',
            outFile: 'data/openclaw-growth-engineer/issues.generated.json',
            maxIssues: 4,
            titlePrefix: '[Growth]',
            labels: ['ai-growth', 'autogenerated', 'product'],
        },
        sources: {
            analytics: {
                enabled: true,
                mode: 'command',
                command: getWizardDefaultSourceCommand('analytics'),
            },
            revenuecat: {
                enabled: true,
                mode: 'command',
                command: getWizardDefaultSourceCommand('revenuecat'),
            },
            paddle: {
                enabled: true,
                mode: 'command',
                command: getWizardDefaultSourceCommand('paddle'),
                environment: 'live',
            },
            seo: {
                enabled: true,
                mode: 'command',
                command: getWizardDefaultSourceCommand('seo'),
                siteUrl: process.env.GSC_SITE_URL || '',
                paidProvider: {
                    dataforseo: {
                        enabled: false,
                        confirmPaid: false,
                        maxPaidRequests: 1,
                    },
                },
            },
            sentry: {
                enabled: true,
                mode: 'command',
                command: normalizeWizardSourceCommand('sentry', {}, configPath),
            },
            coolify: {
                enabled: true,
                mode: 'command',
                command: normalizeWizardSourceCommand('coolify', {}, configPath),
                baseUrl: process.env.COOLIFY_BASE_URL || 'https://coolify.wotaso.com',
                tokenEnv: 'COOLIFY_API_TOKEN',
            },
            feedback: {
                enabled: true,
                mode: 'command',
                command: getDefaultSourceCommand('feedback'),
                cursorMode: 'auto_since_last_fetch',
                initialLookback: '30d',
            },
            extra: [
                buildExtraSourceConfig('asc-cli', { enabled: true, mode: 'command', command: getWizardDefaultSourceCommand('asc') }),
            ],
        },
        schedule: {
            intervalMinutes: DEFAULT_GROWTH_INTERVAL_MINUTES,
            connectorHealthCheckIntervalMinutes: DEFAULT_CONNECTOR_HEALTH_INTERVAL_MINUTES,
            skipIfNoDataChange: true,
            skipIfIssueSetUnchanged: true,
            cadences: DEFAULT_CADENCE_PLAN.map((cadence) => ({ ...cadence })),
        },
        actions: {
            autoCreateIssues: true,
            autoCreatePullRequests: false,
            autoCreateWhenGitHubWriteAccess: true,
            disableAutoCreateGitHubArtifacts: false,
            mode: 'issue',
            outputDestinations: ['openclaw_chat', 'github_issue'],
            productionErrorMode: 'issue',
            usageMode: 'production_autopilot',
            draftPullRequests: true,
            proposalBranchPrefix: 'openclaw/proposals',
        },
        deliveries: {
            openclawChat: {
                enabled: true,
                markdownPath: '.openclaw/chat/latest.md',
                jsonPath: '.openclaw/chat/latest.json',
            },
            github: {
                enabled: true,
                mode: 'issue',
                autoCreate: true,
                draftPullRequests: true,
                proposalBranchPrefix: 'openclaw/proposals',
            },
            slack: {
                enabled: false,
                webhookEnv: 'SLACK_WEBHOOK_URL',
            },
            webhook: {
                enabled: false,
                urlEnv: 'OPENCLAW_WEBHOOK_URL',
                method: 'POST',
                headers: {},
            },
            command: {
                enabled: false,
                label: 'command',
                command: '',
            },
            discord: {
                enabled: false,
                label: 'discord',
                command: '',
            },
        },
        charting: {
            enabled: true,
            command: null,
        },
        notifications: {
            connectorHealth: {
                enabled: true,
                channels: [
                    {
                        type: 'openclaw-chat',
                        enabled: true,
                        markdownPath: '.openclaw/chat/connector-health.md',
                        jsonPath: '.openclaw/chat/connector-health.json',
                    },
                ],
            },
            growthRun: {
                enabled: true,
                channels: [
                    {
                        type: 'openclaw-chat',
                        enabled: true,
                        markdownPath: '.openclaw/chat/growth-summary.md',
                        jsonPath: '.openclaw/chat/growth-summary.json',
                    },
                ],
            },
        },
        automation: {
            openclawCron: {
                enabled: true,
                mode: 'main',
                schedule: '*/30 * * * *',
                timezone: process.env.TZ || 'UTC',
                name: 'OpenClaw Growth Engineer scheduler',
                delivery: {
                    enabled: true,
                    mode: 'announce',
                    channel: 'last',
                    to: '',
                },
            },
        },
        secrets: {
            githubTokenEnv: 'GITHUB_TOKEN',
            githubTokenRef: { source: 'env', provider: 'default', id: 'GITHUB_TOKEN' },
            analyticsTokenEnv: 'ANALYTICSCLI_ACCESS_TOKEN',
            analyticsTokenRef: { source: 'env', provider: 'default', id: 'ANALYTICSCLI_ACCESS_TOKEN' },
            revenuecatTokenEnv: 'REVENUECAT_API_KEY',
            revenuecatTokenRef: { source: 'env', provider: 'default', id: 'REVENUECAT_API_KEY' },
            paddleTokenEnv: 'PADDLE_API_KEY',
            paddleTokenRef: { source: 'env', provider: 'default', id: 'PADDLE_API_KEY' },
            gscTokenEnv: 'GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN',
            gscTokenRef: { source: 'env', provider: 'default', id: 'GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN' },
            dataforseoLoginEnv: 'DATAFORSEO_LOGIN',
            dataforseoLoginRef: { source: 'env', provider: 'default', id: 'DATAFORSEO_LOGIN' },
            dataforseoPasswordEnv: 'DATAFORSEO_PASSWORD',
            dataforseoPasswordRef: { source: 'env', provider: 'default', id: 'DATAFORSEO_PASSWORD' },
            sentryTokenEnv: 'SENTRY_AUTH_TOKEN',
            sentryTokenRef: { source: 'env', provider: 'default', id: 'SENTRY_AUTH_TOKEN' },
            coolifyTokenEnv: 'COOLIFY_API_TOKEN',
            coolifyTokenRef: { source: 'env', provider: 'default', id: 'COOLIFY_API_TOKEN' },
        },
    };
}
function buildRecommendedSourceConfig(configPath = null) {
    return {
        analytics: {
            enabled: true,
            mode: 'command',
            command: getWizardDefaultSourceCommand('analytics'),
        },
        revenuecat: {
            enabled: true,
            mode: 'command',
            command: getWizardDefaultSourceCommand('revenuecat'),
        },
        paddle: {
            enabled: true,
            mode: 'command',
            command: getWizardDefaultSourceCommand('paddle'),
            environment: 'live',
        },
        seo: {
            enabled: true,
            mode: 'command',
            command: getWizardDefaultSourceCommand('seo'),
            siteUrl: process.env.GSC_SITE_URL || '',
            paidProvider: {
                dataforseo: {
                    enabled: false,
                    confirmPaid: false,
                    maxPaidRequests: 1,
                },
            },
        },
        sentry: {
            enabled: true,
            mode: 'command',
            command: normalizeWizardSourceCommand('sentry', {}, configPath),
        },
        coolify: {
            enabled: true,
            mode: 'command',
            command: normalizeWizardSourceCommand('coolify', {}, configPath),
            baseUrl: process.env.COOLIFY_BASE_URL || 'https://coolify.wotaso.com',
            tokenEnv: 'COOLIFY_API_TOKEN',
        },
        feedback: {
            enabled: true,
            mode: 'command',
            command: getDefaultSourceCommand('feedback'),
            cursorMode: 'auto_since_last_fetch',
            initialLookback: '30d',
        },
        extra: [
            buildExtraSourceConfig('asc-cli', { enabled: true, mode: 'command', command: getWizardDefaultSourceCommand('asc') }),
        ],
    };
}
function getInputChannelInitialSelection(config) {
    const sources = config?.sources || {};
    const extraSources = Array.isArray(sources.extra) ? sources.extra : [];
    const selected = new Set();
    const hasExplicitSources = Boolean(config?.sources);
    if (!hasExplicitSources)
        return orderConnectors([...CONNECTOR_KEYS]);
    if (!hasExplicitSources || sources.analytics?.enabled !== false)
        selected.add('analytics');
    if (sources.revenuecat?.enabled === true || isConnectorLocallyConfigured('revenuecat'))
        selected.add('revenuecat');
    if (sources.paddle?.enabled === true || isConnectorLocallyConfigured('paddle'))
        selected.add('paddle');
    if (sources.seo?.enabled === true || isConnectorLocallyConfigured('seo'))
        selected.add('seo');
    if (!hasExplicitSources || sources.sentry?.enabled !== false)
        selected.add('sentry');
    if (sources.coolify?.enabled === true || isConnectorLocallyConfigured('coolify'))
        selected.add('coolify');
    if (extraSources.some((source) => ['asc', 'asc-cli', 'app-store-connect', 'app_store_connect'].includes(String(source?.service || source?.key || '').toLowerCase()) &&
        source?.enabled !== false) ||
        isConnectorLocallyConfigured('asc')) {
        selected.add('asc');
    }
    for (const key of ACCOUNT_SIGNAL_CONNECTOR_KEYS) {
        if (extraSources.some((source) => String(source?.key || source?.service || '').toLowerCase() === key && source?.enabled !== false) ||
            isConnectorLocallyConfigured(key)) {
            selected.add(key);
        }
    }
    selected.add('github');
    if (selected.size === 0)
        return orderConnectors([...CONNECTOR_KEYS]);
    return orderConnectors([...selected]);
}
function buildSourceConfigFromInputChannels(selectedConnectors, existingSources = {}, configPath = null) {
    const selected = new Set(selectedConnectors);
    const recommended = buildRecommendedSourceConfig(configPath);
    const migratedSources = migrateRuntimeSourceCommands({ sources: existingSources }, configPath).sources || {};
    const existingExtra = Array.isArray(migratedSources.extra) ? migratedSources.extra : [];
    const ascSource = existingExtra.find((source) => ['asc', 'asc-cli', 'app-store-connect', 'app_store_connect'].includes(String(source?.service || source?.key || '').toLowerCase()));
    const managedAccountKeys = new Set(ACCOUNT_SIGNAL_CONNECTOR_KEYS);
    const accountSourceByKey = new Map(existingExtra
        .filter((source) => managedAccountKeys.has(String(source?.key || source?.service || '').toLowerCase()))
        .map((source) => [String(source?.key || source?.service || '').toLowerCase(), source]));
    const nonAscExtra = existingExtra.filter((source) => {
        if (source === ascSource)
            return false;
        return !managedAccountKeys.has(String(source?.key || source?.service || '').toLowerCase());
    });
    const accountExtra = ACCOUNT_SIGNAL_CONNECTOR_KEYS.map((key) => buildAccountSignalExtraSourceConfig(key, accountSourceByKey.get(key) || { enabled: selected.has(key) })).map((source) => ({ ...source, enabled: selected.has(source.key) }));
    return {
        ...recommended,
        ...migratedSources,
        analytics: {
            ...recommended.analytics,
            ...(migratedSources.analytics || {}),
            command: normalizeWizardSourceCommand('analytics', {
                ...recommended.analytics,
                ...(migratedSources.analytics || {}),
            }, configPath),
            enabled: selected.has('analytics'),
        },
        revenuecat: {
            ...recommended.revenuecat,
            ...(migratedSources.revenuecat || {}),
            command: normalizeWizardSourceCommand('revenuecat', {
                ...recommended.revenuecat,
                ...(migratedSources.revenuecat || {}),
            }, configPath),
            enabled: selected.has('revenuecat'),
        },
        paddle: {
            ...recommended.paddle,
            ...(migratedSources.paddle || {}),
            command: normalizeWizardSourceCommand('paddle', {
                ...recommended.paddle,
                ...(migratedSources.paddle || {}),
            }, configPath),
            enabled: selected.has('paddle'),
        },
        seo: {
            ...recommended.seo,
            ...(migratedSources.seo || {}),
            command: normalizeWizardSourceCommand('seo', {
                ...recommended.seo,
                ...(migratedSources.seo || {}),
            }, configPath),
            enabled: selected.has('seo'),
        },
        sentry: {
            ...recommended.sentry,
            ...(migratedSources.sentry || {}),
            command: normalizeWizardSourceCommand('sentry', {
                ...recommended.sentry,
                ...(migratedSources.sentry || {}),
            }, configPath),
            enabled: selected.has('sentry'),
        },
        coolify: {
            ...recommended.coolify,
            ...(migratedSources.coolify || {}),
            command: normalizeWizardSourceCommand('coolify', {
                ...recommended.coolify,
                ...(migratedSources.coolify || {}),
            }, configPath),
            enabled: selected.has('coolify'),
        },
        feedback: {
            ...recommended.feedback,
            ...(migratedSources.feedback || {}),
            enabled: selected.has('analytics'),
        },
        extra: [
            ...nonAscExtra,
            ...accountExtra,
            {
                ...buildExtraSourceConfig('asc-cli', {
                    enabled: selected.has('asc'),
                    mode: 'command',
                    command: getWizardDefaultSourceCommand('asc'),
                }),
                ...(ascSource || {}),
                command: normalizeWizardSourceCommand('asc', {
                    ...buildExtraSourceConfig('asc-cli', {
                        enabled: selected.has('asc'),
                        mode: 'command',
                        command: getWizardDefaultSourceCommand('asc'),
                    }),
                    ...(ascSource || {}),
                }, configPath),
                enabled: selected.has('asc'),
            },
        ],
    };
}
async function loadEditableConfig(configPath) {
    const existing = await readJsonIfPresent(configPath).catch(() => null);
    if (existing && typeof existing === 'object')
        return migrateRuntimeSourceCommands(existing, configPath);
    return await buildDefaultWizardConfig(configPath);
}
function mergeNotificationChannels(baseChannels, extraChannels) {
    const channels = [];
    const seen = new Set();
    for (const channel of [...baseChannels, ...extraChannels]) {
        if (!channel || channel.enabled === false)
            continue;
        const key = `${channel.type}:${channel.markdownPath || channel.jsonPath || channel.webhookEnv || channel.urlEnv || channel.command || channel.label || ''}`;
        if (seen.has(key))
            continue;
        seen.add(key);
        channels.push(channel);
    }
    return channels;
}
async function askNotificationChannels(rl, config) {
    const channels = [
        {
            type: 'openclaw-chat',
            enabled: true,
            markdownPath: '.openclaw/chat/growth-summary.md',
            jsonPath: '.openclaw/chat/growth-summary.json',
        },
    ];
    const slackDefault = Boolean(config?.deliveries?.slack?.enabled);
    if (await askYesNo(rl, 'Send summaries and connector-health alerts to Slack?', slackDefault)) {
        const webhookEnv = await ask(rl, 'Slack webhook env var', config?.deliveries?.slack?.webhookEnv || 'SLACK_WEBHOOK_URL');
        channels.push({ type: 'slack', enabled: true, webhookEnv });
    }
    const webhookDefault = Boolean(config?.deliveries?.webhook?.enabled);
    if (await askYesNo(rl, 'Send summaries and connector-health alerts to a generic webhook/social bridge?', webhookDefault)) {
        const urlEnv = await ask(rl, 'Webhook URL env var', config?.deliveries?.webhook?.urlEnv || 'OPENCLAW_WEBHOOK_URL');
        channels.push({ type: 'webhook', enabled: true, urlEnv, method: 'POST', headers: {} });
    }
    const commandDefault = Boolean(config?.deliveries?.command?.enabled || config?.deliveries?.discord?.enabled);
    if (await askYesNo(rl, 'Send summaries and connector-health alerts through a local command channel?', commandDefault)) {
        const command = await ask(rl, 'Command that receives the message on stdin', config?.deliveries?.command?.command || config?.deliveries?.discord?.command || '');
        channels.push({ type: 'command', enabled: true, label: 'command', command });
    }
    return channels;
}
async function askOutputConfig(rl, config) {
    printSection('Outputs and notifications', [
        'OpenClaw chat is always enabled so the agent has a readable handoff.',
        'GitHub issues or draft PRs are optional and only run when a token plus an inferred repo are available.',
    ]);
    const currentMode = config?.actions?.mode || config?.deliveries?.github?.mode || 'issue';
    const configuredDestinations = Array.isArray(config?.actions?.outputDestinations)
        ? config.actions.outputDestinations
        : [];
    const currentAutoCreateIssue = Boolean(config?.actions?.autoCreateIssues ||
        configuredDestinations.includes('github_issue') ||
        (config?.deliveries?.github?.autoCreate && currentMode !== 'pull_request'));
    const currentAutoCreatePullRequest = Boolean(config?.actions?.autoCreatePullRequests ||
        configuredDestinations.includes('github_pull_request') ||
        (config?.deliveries?.github?.autoCreate && currentMode === 'pull_request'));
    const outputChoices = await askMultiChoice(rl, {
        title: 'Output destinations',
        subtitle: 'Use Up/Down to move, Space to toggle outputs, A to toggle all optional outputs, Enter to continue.',
        defaultValues: [
            'chat',
            ...(currentAutoCreateIssue ? ['issue'] : []),
            ...(currentAutoCreatePullRequest ? ['pull_request'] : []),
        ],
        requiredValues: ['chat'],
        minSelections: 1,
        options: [
            {
                value: 'chat',
                label: 'OpenClaw chat',
                detail: 'Write readable summaries and leave GitHub as runtime fallback.',
            },
            {
                value: 'issue',
                label: 'GitHub issues',
                detail: 'Auto-create issues for concrete findings when GitHub access allows it.',
            },
            {
                value: 'pull_request',
                label: 'Draft PR proposals',
                detail: 'Auto-create draft PR-oriented proposal branches for implementation-ready fixes.',
            },
        ],
    });
    const wantsIssue = outputChoices.includes('issue');
    const wantsPullRequest = outputChoices.includes('pull_request');
    const productionErrorMode = await askMenuChoice(rl, {
        title: 'Production error handling',
        subtitle: 'What should happen when the 90-minute healthcheck confirms a production Sentry/GlitchTip/Coolify issue?',
        defaultValue: config?.actions?.productionErrorMode || (wantsPullRequest ? 'pull_request' : wantsIssue ? 'issue' : 'alert'),
        options: [
            {
                value: 'alert',
                label: 'Alert only',
                detail: 'Send the short alert/handoff; do not auto-create GitHub artifacts for production errors.',
            },
            {
                value: 'issue',
                label: 'GitHub issue',
                detail: 'Create a GitHub issue with the production evidence and suggested investigation when access allows it.',
            },
            {
                value: 'pull_request',
                label: 'Draft PR',
                detail: 'Create a draft PR proposal for implementation-ready production fixes when access allows it.',
            },
        ],
    });
    const effectiveWantsIssue = wantsIssue || productionErrorMode === 'issue';
    const effectiveWantsPullRequest = wantsPullRequest || productionErrorMode === 'pull_request';
    const summaryOnly = !effectiveWantsIssue && !effectiveWantsPullRequest;
    const mode = effectiveWantsPullRequest ? 'pull_request' : 'issue';
    const autoCreate = effectiveWantsIssue || effectiveWantsPullRequest;
    if (!summaryOnly) {
        process.stdout.write('GitHub repo scope is not pinned by the wizard; OpenClaw/Hermes will infer it from OPENCLAW_GITHUB_REPO, the local git remote, or runtime context when creating issues/PRs.\n');
    }
    const channels = await askNotificationChannels(rl, config);
    const connectorHealthChannels = channels.map((channel) => {
        if (channel.type !== 'openclaw-chat')
            return channel;
        return {
            ...channel,
            markdownPath: '.openclaw/chat/connector-health.md',
            jsonPath: '.openclaw/chat/connector-health.json',
        };
    });
    config.actions = {
        ...(config.actions || {}),
        mode,
        outputDestinations: [
            'openclaw_chat',
            ...(effectiveWantsIssue ? ['github_issue'] : []),
            ...(effectiveWantsPullRequest ? ['github_pull_request'] : []),
        ],
        productionErrorMode,
        autoCreateIssues: effectiveWantsIssue,
        autoCreatePullRequests: effectiveWantsPullRequest,
        autoCreateWhenGitHubWriteAccess: config.actions?.autoCreateWhenGitHubWriteAccess !== false,
        disableAutoCreateGitHubArtifacts: config.actions?.disableAutoCreateGitHubArtifacts === true,
        draftPullRequests: true,
        proposalBranchPrefix: config?.actions?.proposalBranchPrefix || 'openclaw/proposals',
    };
    config.deliveries = {
        ...(config.deliveries || {}),
        openclawChat: {
            ...(config.deliveries?.openclawChat || {}),
            enabled: true,
            markdownPath: config.deliveries?.openclawChat?.markdownPath || '.openclaw/chat/latest.md',
            jsonPath: config.deliveries?.openclawChat?.jsonPath || '.openclaw/chat/latest.json',
        },
        github: {
            ...(config.deliveries?.github || {}),
            enabled: !summaryOnly,
            mode,
            modes: [
                ...(effectiveWantsIssue ? ['issue'] : []),
                ...(effectiveWantsPullRequest ? ['pull_request'] : []),
            ],
            autoCreate,
            draftPullRequests: true,
            proposalBranchPrefix: config?.actions?.proposalBranchPrefix || 'openclaw/proposals',
        },
        slack: {
            ...(config.deliveries?.slack || {}),
            enabled: channels.some((channel) => channel.type === 'slack'),
            webhookEnv: channels.find((channel) => channel.type === 'slack')?.webhookEnv || config.deliveries?.slack?.webhookEnv || 'SLACK_WEBHOOK_URL',
        },
        webhook: {
            ...(config.deliveries?.webhook || {}),
            enabled: channels.some((channel) => channel.type === 'webhook'),
            urlEnv: channels.find((channel) => channel.type === 'webhook')?.urlEnv || config.deliveries?.webhook?.urlEnv || 'OPENCLAW_WEBHOOK_URL',
            method: 'POST',
            headers: config.deliveries?.webhook?.headers || {},
        },
        command: {
            ...(config.deliveries?.command || {}),
            enabled: channels.some((channel) => channel.type === 'command'),
            label: channels.find((channel) => channel.type === 'command')?.label || config.deliveries?.command?.label || 'command',
            command: channels.find((channel) => channel.type === 'command')?.command || config.deliveries?.command?.command || '',
        },
        discord: {
            ...(config.deliveries?.discord || {}),
            enabled: Boolean(config.deliveries?.discord?.enabled),
            label: config.deliveries?.discord?.label || 'discord',
            command: config.deliveries?.discord?.command || '',
        },
    };
    config.notifications = {
        ...(config.notifications || {}),
        connectorHealth: {
            ...(config.notifications?.connectorHealth || {}),
            enabled: true,
            channels: mergeNotificationChannels([], connectorHealthChannels),
        },
        growthRun: {
            ...(config.notifications?.growthRun || {}),
            enabled: true,
            channels: mergeNotificationChannels([], channels),
        },
    };
    return config;
}
async function askGitHubArtifactDetails(rl, config) {
    const githubEnabled = Boolean(config?.actions?.autoCreateIssues ||
        config?.actions?.autoCreatePullRequests ||
        config?.deliveries?.github?.enabled ||
        config?.deliveries?.github?.autoCreate);
    config.project = {
        ...(config.project || {}),
        githubRepo: '',
        repoRoot: config.project?.repoRoot || '.',
        outFile: config.project?.outFile || 'data/openclaw-growth-engineer/issues.generated.json',
        maxIssues: Number(config.project?.maxIssues || 4),
        titlePrefix: config.project?.titlePrefix || '[Growth]',
        labels: Array.isArray(config.project?.labels) && config.project.labels.length > 0
            ? config.project.labels
            : ['ai-growth', 'autogenerated', 'product'],
    };
    if (!githubEnabled) {
        return config;
    }
    process.stdout.write('\nGitHub repo scope is not pinned by the wizard. OpenClaw/Hermes infers it from OPENCLAW_GITHUB_REPO, the local git remote, or runtime context.\n');
    const customize = await askYesNo(rl, 'Customize GitHub issue/PR limits, labels, or chart attachment settings?', false);
    if (!customize) {
        config.charting = {
            ...(config.charting || {}),
            enabled: config.charting?.enabled !== false,
            command: config.charting?.command || null,
        };
        return config;
    }
    const labelsRaw = await ask(rl, 'GitHub labels for created issues/PRs', config.project.labels.join(','));
    config.project.labels = labelsRaw
        .split(',')
        .map((value) => value.trim())
        .filter(Boolean);
    config.project.maxIssues = Number.parseInt(await ask(rl, 'Maximum GitHub artifacts per run', String(config.project.maxIssues || 4)), 10) || 4;
    config.project.titlePrefix = await ask(rl, 'GitHub artifact title prefix', config.project.titlePrefix || '[Growth]');
    const enableCharting = await askYesNo(rl, 'Attach generated charts to GitHub artifacts when useful?', config.charting?.enabled === true);
    config.charting = {
        ...(config.charting || {}),
        enabled: enableCharting,
        command: enableCharting
            ? await ask(rl, 'Optional chart command override', config.charting?.command || '')
            : null,
    };
    return config;
}
async function askIntervalConfig(rl, config) {
    printSection('Schedule and analysis depth', [
        'The runner wakes up often, but larger reviews only run on their daily/weekly/monthly cadence.',
        'Connector health checks are separate and default to every 6 hours.',
        'On OpenClaw or Hermes VPS installs, the agent scheduler should wake Growth Engineer; heartbeat stays as a fallback checklist.',
    ]);
    const currentSchedule = config?.schedule || {};
    const currentAutomation = getAutomationConfig(config);
    const usageMode = await askToolUsage(rl);
    const schedulePreset = await askSchedulePreset(rl);
    const recommendedRunnerInterval = schedulePreset === 'quiet' ? 360 : 90;
    const recommendedConnectorHealthInterval = schedulePreset === 'quiet' ? 360 : DEFAULT_CONNECTOR_HEALTH_INTERVAL_MINUTES;
    const recommendedOpenClawCronSchedule = schedulePreset === 'quiet' ? '0 * * * *' : '*/30 * * * *';
    const intervalMinutes = schedulePreset === 'manual'
        ? Number.parseInt(await ask(rl, 'Growth runner fallback loop interval in minutes', String(currentSchedule.intervalMinutes || recommendedRunnerInterval)), 10) || recommendedRunnerInterval
        : recommendedRunnerInterval;
    const connectorHealthCheckIntervalMinutes = schedulePreset === 'manual'
        ? Number.parseInt(await ask(rl, 'Connector credentials health check interval in minutes', String(currentSchedule.connectorHealthCheckIntervalMinutes || recommendedConnectorHealthInterval)), 10) || recommendedConnectorHealthInterval
        : recommendedConnectorHealthInterval;
    const cadences = await askCadencePlan(rl, currentSchedule.cadences);
    const enableOpenClawCron = await askYesNo(rl, 'Install an OpenClaw Gateway cron job to wake Growth Engineer on this VPS?', currentAutomation.openclawCron.enabled !== false);
    const openclawCronSchedule = enableOpenClawCron
        ? schedulePreset === 'manual'
            ? await ask(rl, 'OpenClaw cron expression for scheduler wakeups', currentAutomation.openclawCron.schedule || recommendedOpenClawCronSchedule)
            : recommendedOpenClawCronSchedule
        : currentAutomation.openclawCron.schedule;
    const openclawCronTimezone = enableOpenClawCron
        ? await ask(rl, 'OpenClaw cron timezone', currentAutomation.openclawCron.timezone || process.env.TZ || 'UTC')
        : currentAutomation.openclawCron.timezone;
    const enableHermesCron = await askYesNo(rl, 'Install a Hermes cron job when Hermes is available on this host?', currentAutomation.hermesCron.enabled !== false);
    const hermesCronSchedule = enableHermesCron
        ? schedulePreset === 'manual'
            ? await ask(rl, 'Hermes cron expression for scheduler wakeups', currentAutomation.hermesCron.schedule || openclawCronSchedule || recommendedOpenClawCronSchedule)
            : openclawCronSchedule || recommendedOpenClawCronSchedule
        : currentAutomation.hermesCron.schedule;
    config.schedule = {
        ...currentSchedule,
        intervalMinutes,
        connectorHealthCheckIntervalMinutes,
        skipIfNoDataChange: currentSchedule.skipIfNoDataChange !== false,
        skipIfIssueSetUnchanged: currentSchedule.skipIfIssueSetUnchanged !== false,
        cadences,
    };
    config.actions = {
        ...(config.actions || {}),
        usageMode,
    };
    config.automation = {
        ...(config.automation || {}),
        openclawCron: {
            ...(currentAutomation.openclawCron || {}),
            enabled: enableOpenClawCron,
            mode: 'main',
            schedule: openclawCronSchedule || '*/30 * * * *',
            timezone: openclawCronTimezone || 'UTC',
            name: currentAutomation.openclawCron.name || 'OpenClaw Growth Engineer scheduler',
            delivery: {
                ...(currentAutomation.openclawCron.delivery || {}),
                enabled: currentAutomation.openclawCron.delivery?.enabled !== false,
                mode: currentAutomation.openclawCron.delivery?.mode || 'announce',
                channel: currentAutomation.openclawCron.delivery?.channel || 'last',
                to: currentAutomation.openclawCron.delivery?.to || '',
            },
        },
        hermesCron: {
            ...(currentAutomation.hermesCron || {}),
            enabled: enableHermesCron,
            schedule: hermesCronSchedule || '*/30 * * * *',
            name: currentAutomation.hermesCron.name || 'Hermes Growth Engineer scheduler',
            skill: currentAutomation.hermesCron.skill || 'growth-engineer',
            deliver: currentAutomation.hermesCron.deliver || 'local',
        },
    };
    return config;
}
async function askOutputsAndIntervalsConfig(rl, config) {
    const withIntervals = await askIntervalConfig(rl, config);
    const withOutput = await askOutputConfig(rl, withIntervals);
    return await askGitHubArtifactDetails(rl, withOutput);
}
async function askInputSourceConfig(rl, config, configPath) {
    config = migrateRuntimeSourceCommands(config, configPath);
    await ensureDirForFile(configPath);
    await writeJsonFile(configPath, config);
    const healthCheckConnectors = await connectorKeysForHealthCheck(configPath);
    const healthByConnector = await withConnectorHealthLoading((onProgress) => getConnectorPickerHealth(configPath, onProgress, healthCheckConnectors), healthCheckConnectors);
    const selected = await askConnectorSelectionWithHealth(rl, healthByConnector, getInputChannelInitialSelection(config), {
        introTitle: 'Input channels',
        introDetail: null,
        actionTitle: 'Select input channels',
        helpText: 'Use Up/Down to move, Space to toggle channels, A to toggle all channels, Enter to continue.',
        mode: 'input',
    });
    config.sources = buildSourceConfigFromInputChannels(selected, config.sources || {}, configPath);
    return { config, selected, healthByConnector };
}
async function writeOpenClawJobManifest(configPath, config) {
    const manifestPath = path.resolve('.openclaw/jobs/openclaw-growth-engineer.json');
    const displayConfigPath = path.relative(process.cwd(), configPath) || configPath;
    const statePath = deriveStatePathFromConfigPath(displayConfigPath);
    const proofPath = deriveSchedulerProofPathFromStatePath(statePath);
    const intervalMinutes = Math.max(1, Number(config?.schedule?.intervalMinutes || DEFAULT_GROWTH_INTERVAL_MINUTES));
    const connectorHealthCheckIntervalMinutes = Math.max(1, Number(config?.schedule?.connectorHealthCheckIntervalMinutes || DEFAULT_CONNECTOR_HEALTH_INTERVAL_MINUTES));
    const actionMode = config?.actions?.mode || config?.deliveries?.github?.mode || 'issue';
    const growthRunCommand = getGrowthRunCommand(config, displayConfigPath);
    const connectorHealthCommand = getConnectorHealthCommand(config, displayConfigPath);
    const ascStatusCommand = `node scripts/openclaw-growth-status.mjs --config ${quote(displayConfigPath)} --json --only-connectors asc`;
    const automation = getAutomationConfig(config);
    const manifest = {
        version: 1,
        generatedAt: new Date().toISOString(),
        managedBy: 'openclaw-growth-wizard',
        agentPolicy: {
            openClawCanRunGrowthJobs: true,
            openClawCanEditGrowthCadences: true,
            openClawCanEditOutputDelivery: true,
            openClawCanEditConnectors: true,
            openClawCanEditConnectorSecrets: false,
            connectorChanges: 'OpenClaw may read and modify non-secret connector config such as enabled flags, source commands, project/app mappings, and source priorities. Use `npx -y @analyticscli/growth-engineer wizard --connectors` for API keys or other connector secrets; never write secret values into config files, manifests, issues, PRs, or chat output.',
            secretAccessMode: config?.security?.connectorSecrets?.mode || 'local-user-file',
            secretPolicy: config?.security?.connectorSecrets?.mode === 'isolated-runner'
                ? 'OpenClaw must use the allowlisted sudo wrapper commands and must not read the persisted secret file.'
                : 'Secrets are persisted in a local chmod 600 file. This protects against other OS users, not against the same OS user.',
            ascAnswerPolicy: {
                sourceOfTruth: 'Growth Engineer local status, not loaded chat/MCP tools',
                statusCommand: ascStatusCommand,
                positiveWhen: 'ASC setup/status reports pass, connected, healthy, or the wizard just finished ASC connector setup successfully.',
                answer: 'Yes. ASC analytics is connected through Growth Engineer local asc CLI/API-key setup.',
                forbiddenAnswer: 'Do not answer no only because no App Store Connect chat tool is callable.',
            },
        },
        scheduler: {
            recommended: 'openclaw-cron',
            openclawCron: automation.openclawCron,
            hermesCron: automation.hermesCron,
            statePath,
            proofPath,
            verifyCommands: [
                'openclaw cron list',
                'openclaw tasks list',
                'openclaw tasks audit',
                'hermes cron list',
                `tail -n 20 ${proofPath}`,
                `jq '.connectorHealth, .cadences, .lastRunAt, .skippedReason' ${statePath}`,
            ],
        },
        jobs: [
            {
                key: 'connector-health',
                kind: 'health-check',
                intervalMinutes: connectorHealthCheckIntervalMinutes,
                command: connectorHealthCommand,
                notificationPolicy: 'once_per_unhealthy_incident_until_recovery_or_changed_fingerprint',
            },
            {
                key: 'growth-runner',
                kind: 'growth-analysis',
                intervalMinutes,
                command: growthRunCommand,
                outputMode: actionMode,
                cadences: Array.isArray(config?.schedule?.cadences) ? config.schedule.cadences : [],
            },
        ],
    };
    await writeJsonFile(manifestPath, manifest);
    return manifestPath;
}
function formatHeartbeatInterval(minutes) {
    const value = Math.max(1, Number(minutes || DEFAULT_CONNECTOR_HEALTH_INTERVAL_MINUTES));
    if (value % 1440 === 0)
        return `${value / 1440}d`;
    if (value % 60 === 0)
        return `${value / 60}h`;
    return `${value}m`;
}
async function refreshWorkspaceRuntimeFromCurrentWizard() {
    const scriptsDir = path.resolve('scripts');
    await fs.mkdir(scriptsDir, { recursive: true });
    let copied = 0;
    for (const entry of await fs.readdir(RUNTIME_DIR, { withFileTypes: true })) {
        if (!entry.isFile())
            continue;
        if (!/\.(mjs|py)$/.test(entry.name))
            continue;
        await fs.copyFile(path.join(RUNTIME_DIR, entry.name), path.join(scriptsDir, entry.name));
        copied += 1;
    }
    return copied;
}
async function writeOpenClawHeartbeat(configPath, config) {
    const heartbeatPath = path.resolve('HEARTBEAT.md');
    const displayConfigPath = path.relative(process.cwd(), path.resolve(configPath)) || configPath;
    const statePath = deriveStatePathFromConfigPath(displayConfigPath);
    const interval = formatHeartbeatInterval(config?.schedule?.connectorHealthCheckIntervalMinutes);
    const runnerCommand = buildGrowthRunnerCommand(displayConfigPath, statePath);
    const statusCommand = `node scripts/openclaw-growth-status.mjs --config ${quote(displayConfigPath)} --json --only-connectors asc`;
    const wizardCommand = `npx -y ${GROWTH_ENGINEER_PACKAGE_SPEC} wizard --connectors --config ${displayConfigPath}`;
    const block = `${HEARTBEAT_MARKER_START}
tasks:

- name: openclaw-growth-engineer-run
  interval: ${interval}
  prompt: "Run \`${runnerCommand}\` from the workspace if the config and runtime files exist. The runner owns schedule.cadences, connectorHealthCheckIntervalMinutes, skipIfNoDataChange, and skipIfIssueSetUnchanged. ASC/App Store Connect is a Growth Engineer local CLI connector, not a chat tool. If asked whether ASC analytics access is available, never inspect loaded chat/MCP tools and never answer no because no Apple tool is callable. Answer from \`${statusCommand}\` or the latest connector setup result. If ASC reports connected/pass/healthy, or setup just finished successfully, answer exactly: Yes. ASC analytics is connected through Growth Engineer local asc CLI/API-key setup. If it reports connector-health alerts, production crashes, generated issues, or actionable growth findings, summarize only the action and evidence. If setup files are missing, tell the user to run \`${wizardCommand}\`. If there is no actionable output, reply HEARTBEAT_OK."

# Keep this section small. Do not put secrets in HEARTBEAT.md.
${HEARTBEAT_MARKER_END}`;
    let existing = '';
    try {
        existing = await fs.readFile(heartbeatPath, 'utf8');
    }
    catch {
        existing = '';
    }
    const markerPattern = new RegExp(`${escapeRegExp(HEARTBEAT_MARKER_START)}[\\s\\S]*?${escapeRegExp(HEARTBEAT_MARKER_END)}`);
    const hasWork = existing
        .split(/\r?\n/)
        .map((line) => line.trim())
        .some((line) => line && !line.startsWith('#') && !line.startsWith('<!--') && !line.startsWith('-->'));
    const next = markerPattern.test(existing)
        ? existing.replace(markerPattern, block)
        : hasWork
            ? `${existing.trimEnd()}\n\n${block}\n`
            : `# OpenClaw heartbeat checklist\n\n${block}\n`;
    if (next !== existing)
        await fs.writeFile(heartbeatPath, next, 'utf8');
    return heartbeatPath;
}
async function writeOpenClawSessionNote(configPath, config) {
    const notePath = path.resolve('.openclaw/growth-engineer-session.md');
    const displayConfigPath = path.relative(process.cwd(), path.resolve(configPath)) || configPath;
    const statePath = deriveStatePathFromConfigPath(displayConfigPath);
    const runnerCommand = buildGrowthRunnerCommand(displayConfigPath, statePath);
    const statusCommand = `node scripts/openclaw-growth-status.mjs --config ${quote(displayConfigPath)} --json --only-connectors asc`;
    const enabledConnectors = configuredConnectorKeysFromConfig(config).map((key) => connectorLabel(key));
    const lines = [
        '# Growth Engineer Session Context',
        '',
        'Use this file as local OpenClaw context after connector setup changes.',
        '',
        '## ASC Answer Rule',
        '',
        '- ASC/App Store Connect is a Growth Engineer local CLI/API-key connector, not a chat/MCP tool.',
        '- Do not inspect loaded tools to answer ASC availability.',
        '- Do not answer "no" because no App Store Connect tool is callable.',
        '- If ASC setup just finished with SUCCESS, answer: Yes. ASC analytics is connected through Growth Engineer local asc CLI/API-key setup.',
        '- If unsure, run the status command below and answer yes when ASC reports pass, connected, or healthy.',
        `- Check ASC status with: \`${statusCommand}\``,
        '',
        '## Growth Engineer',
        '',
        `- Run Growth Engineer with: \`${runnerCommand}\``,
        enabledConnectors.length > 0
            ? `- Configured connector groups: ${enabledConnectors.join(', ')}`
            : '- Configured connector groups: none yet',
        '',
    ];
    await ensureDirForFile(notePath);
    await fs.writeFile(notePath, `${lines.join('\n')}\n`, 'utf8');
    return notePath;
}
async function maybeRefreshOpenClawSessionInstructions(rl, configPath) {
    if (isFalseyEnv(process.env.OPENCLAW_GROWTH_REFRESH_OPENCLAW_SESSION))
        return false;
    const refresh = isTruthyEnv(process.env.OPENCLAW_GROWTH_REFRESH_OPENCLAW_SESSION)
        || await askYesNo(rl, 'Update OpenClaw runtime and heartbeat files now?', true);
    if (!refresh)
        return false;
    const config = await loadEditableConfig(configPath);
    const copied = await refreshWorkspaceRuntimeFromCurrentWizard();
    const heartbeatPath = await writeOpenClawHeartbeat(configPath, config);
    const manifestPath = await writeOpenClawJobManifest(path.resolve(configPath), config);
    const sessionNotePath = await writeOpenClawSessionNote(configPath, config);
    process.stdout.write(`${ANSI.bold}OpenClaw files updated.${ANSI.reset}\n`);
    process.stdout.write(`Runtime files: scripts/ (${copied} files)\n`);
    process.stdout.write(`Heartbeat: ${path.relative(process.cwd(), heartbeatPath) || heartbeatPath}\n`);
    process.stdout.write(`Job manifest: ${path.relative(process.cwd(), manifestPath) || manifestPath}\n`);
    process.stdout.write(`Session note: ${path.relative(process.cwd(), sessionNotePath) || sessionNotePath}\n`);
    process.stdout.write('ASC will not appear as a chat tool; OpenClaw should answer ASC access from Growth Engineer status.\n');
    process.stdout.write('If an existing OpenClaw chat still checks loaded tools, start a new chat or tell it to read .openclaw/growth-engineer-session.md.\n');
    return true;
}
async function ensureOpenClawCronFromWizard(configPath, config) {
    const automation = getAutomationConfig(config).openclawCron;
    const displayConfigPath = path.relative(process.cwd(), configPath) || configPath;
    const statePath = deriveStatePathFromConfigPath(displayConfigPath);
    const proofPath = path.resolve(deriveSchedulerProofPathFromStatePath(statePath));
    if (automation.enabled === false) {
        return {
            ok: true,
            installed: false,
            status: 'disabled',
            detail: 'OpenClaw Gateway cron disabled by user choice.',
            statePath,
            proofPath,
        };
    }
    const addCommand = buildOpenClawCronAddCommand(displayConfigPath, config);
    if (!(await commandExists('openclaw'))) {
        return {
            ok: true,
            installed: false,
            status: 'openclaw_cli_missing',
            detail: 'openclaw CLI was not found on PATH. Run the shown command on the VPS shell where OpenClaw Gateway is installed.',
            command: addCommand,
            statePath,
            proofPath,
        };
    }
    const inspection = await inspectOpenClawCronInstall({
        configPath: displayConfigPath,
        config,
        runCommand: runCommandCapture,
        readFile: fs.readFile,
    });
    if (inspection.exists && inspection.verified) {
        return {
            ok: true,
            installed: true,
            status: 'already_configured_verified',
            detail: `OpenClaw cron job already exists and matches the Growth Engineer runner contract: ${automation.name}`,
            source: inspection.source,
            statePath,
            proofPath,
        };
    }
    const add = await runCommandCapture(addCommand);
    const existingDetail = inspection.exists
        ? `Existing OpenClaw cron job "${automation.name}" was not verifiably wired to the current runner contract (${inspection.reason} via ${inspection.source}). `
        : '';
    return {
        ok: add.ok,
        installed: add.ok,
        status: add.ok ? (inspection.exists ? 'reconfigured' : 'configured') : inspection.exists ? 'needs_repair' : 'failed',
        detail: add.ok
            ? `${existingDetail}Configured OpenClaw cron job: ${automation.name}`
            : `${existingDetail}${add.stderr || add.stdout || `exit ${add.code}`}`,
        command: addCommand,
        remediation: inspection.exists && !add.ok
            ? `Remove the stale OpenClaw cron job named "${automation.name}" with your installed OpenClaw CLI, then rerun: ${addCommand}`
            : undefined,
        statePath,
        proofPath,
    };
}
async function ensureHermesCronFromWizard(configPath, config) {
    const automation = getAutomationConfig(config).hermesCron;
    const displayConfigPath = path.relative(process.cwd(), configPath) || configPath;
    const statePath = deriveStatePathFromConfigPath(displayConfigPath);
    const proofPath = path.resolve(deriveSchedulerProofPathFromStatePath(statePath));
    const workdir = path.resolve(automation.workdir || process.cwd());
    if (automation.enabled === false) {
        return {
            ok: true,
            installed: false,
            status: 'disabled',
            detail: 'Hermes cron disabled by user choice.',
            statePath,
            proofPath,
        };
    }
    const createCommand = buildHermesCronCreateCommand(displayConfigPath, config, { workdir });
    if (!(await commandExists('hermes'))) {
        return {
            ok: true,
            installed: false,
            status: 'hermes_cli_missing',
            detail: 'hermes CLI was not found on PATH. Run the shown command on the host where Hermes Gateway is installed.',
            command: createCommand,
            statePath,
            proofPath,
            workdir,
        };
    }
    const inspection = await inspectHermesCronInstall({
        configPath: displayConfigPath,
        config,
        runCommand: runCommandCapture,
        readFile: fs.readFile,
        workdir,
    });
    if (inspection.exists && inspection.verified) {
        return {
            ok: true,
            installed: true,
            status: 'already_configured_verified',
            detail: `Hermes cron job already exists and matches the Growth Engineer runner contract: ${automation.name}`,
            source: inspection.source,
            statePath,
            proofPath,
            workdir,
        };
    }
    const create = await runCommandCapture(createCommand);
    const existingDetail = inspection.exists
        ? `Existing Hermes cron job "${automation.name}" was not verifiably wired to the current runner contract (${inspection.reason} via ${inspection.source}). `
        : '';
    return {
        ok: create.ok,
        installed: create.ok,
        status: create.ok ? (inspection.exists ? 'reconfigured' : 'configured') : inspection.exists ? 'needs_repair' : 'failed',
        detail: create.ok
            ? `${existingDetail}Configured Hermes cron job: ${automation.name}`
            : `${existingDetail}${create.stderr || create.stdout || `exit ${create.code}`}`,
        command: createCommand,
        remediation: inspection.exists && !create.ok
            ? `Remove the stale Hermes cron job named "${automation.name}" with your installed Hermes CLI, then rerun: ${createCommand}`
            : undefined,
        statePath,
        proofPath,
        workdir,
    };
}
function printOpenClawCronResult(result) {
    process.stdout.write(`OpenClaw cron: ${result.status} - ${result.detail}\n`);
    if (result.command && result.status === 'openclaw_cli_missing') {
        process.stdout.write('\nRun this on the VPS where OpenClaw Gateway is installed:\n');
        process.stdout.write(`${result.command}\n`);
    }
    if (result.remediation) {
        process.stdout.write('\nOpenClaw cron repair:\n');
        process.stdout.write(`${result.remediation}\n`);
    }
    process.stdout.write('\nVPS verification commands:\n');
    process.stdout.write('  openclaw cron list\n');
    process.stdout.write('  openclaw tasks list\n');
    process.stdout.write('  openclaw tasks audit\n');
    process.stdout.write(`  tail -n 20 ${result.proofPath || path.resolve(DEFAULT_SCHEDULER_PROOF_PATH)}\n`);
    process.stdout.write(`  jq '.connectorHealth, .cadences, .lastRunAt, .skippedReason' ${result.statePath || 'data/openclaw-growth-engineer/state.json'}\n`);
}
function printHermesCronResult(result) {
    process.stdout.write(`Hermes cron: ${result.status} - ${result.detail}\n`);
    if (result.command && result.status === 'hermes_cli_missing') {
        process.stdout.write('\nRun this on the host where Hermes Gateway is installed:\n');
        process.stdout.write(`${result.command}\n`);
    }
    if (result.remediation) {
        process.stdout.write('\nHermes cron repair:\n');
        process.stdout.write(`${result.remediation}\n`);
    }
    process.stdout.write('\nHermes verification commands:\n');
    process.stdout.write('  hermes cron list\n');
    process.stdout.write('  hermes gateway status\n');
    process.stdout.write(`  tail -n 20 ${result.proofPath || path.resolve(DEFAULT_SCHEDULER_PROOF_PATH)}\n`);
    process.stdout.write(`  jq '.connectorHealth, .cadences, .lastRunAt, .skippedReason' ${result.statePath || 'data/openclaw-growth-engineer/state.json'}\n`);
}
async function main() {
    await loadOpenClawGrowthSecrets();
    const args = parseArgs(process.argv.slice(2));
    await maybeSelfUpdateFromClawHub(args);
    if (args.sandboxSmoke) {
        const configPath = path.resolve(args.out);
        const config = await loadEditableConfig(configPath);
        await writeJsonFile(configPath, config);
        process.stdout.write(`${JSON.stringify({ ok: true, configPath, sources: config.sources || {} })}\n`);
        return;
    }
    if (args.connectorWizard) {
        await runConnectorSetupWizard(args);
        return;
    }
    const configPath = path.resolve(args.out);
    if (!process.stdin.isTTY || !process.stdout.isTTY) {
        throw new Error('Wizard requires an interactive terminal.');
    }
    while (true) {
        const rl = createInterface({ input: process.stdin, output: process.stdout });
        try {
            printWizardHeader();
            const goal = await askWizardGoal(rl);
            if (goal === 'connectors') {
                rl.close();
                const result = await runConnectorSetupWizard({ ...args, connectorWizard: true });
                if (result === 'back')
                    continue;
                return;
            }
            if (goal === 'intervals') {
                const config = await askIntervalConfig(rl, await loadEditableConfig(configPath));
                const secretAccess = await askSecretAccessModel(rl, configPath, config);
                await writeJsonFile(configPath, config);
                const manifestPath = await writeOpenClawJobManifest(configPath, config);
                const cronResult = await ensureOpenClawCronFromWizard(configPath, config);
                const hermesCronResult = await ensureHermesCronFromWizard(configPath, config);
                process.stdout.write(`\nSaved schedule config: ${configPath}\n`);
                process.stdout.write(`Saved OpenClaw job manifest: ${manifestPath}\n`);
                printOpenClawCronResult(cronResult);
                printHermesCronResult(hermesCronResult);
                printSecretRunnerKitInstructions(secretAccess.kit);
                process.stdout.write('OpenClaw can run and update growth jobs plus non-secret connector config from the manifest; connector API keys stay behind the connector wizard.\n');
                return;
            }
            if (goal === 'outputs_intervals') {
                const config = await askOutputsAndIntervalsConfig(rl, await loadEditableConfig(configPath));
                const secretAccess = await askSecretAccessModel(rl, configPath, config);
                await writeJsonFile(configPath, config);
                const manifestPath = await writeOpenClawJobManifest(configPath, config);
                const cronResult = await ensureOpenClawCronFromWizard(configPath, config);
                const hermesCronResult = await ensureHermesCronFromWizard(configPath, config);
                process.stdout.write(`\nSaved output and interval config: ${configPath}\n`);
                process.stdout.write(`Saved OpenClaw job manifest: ${manifestPath}\n`);
                printOpenClawCronResult(cronResult);
                printHermesCronResult(hermesCronResult);
                printSecretRunnerKitInstructions(secretAccess.kit);
                process.stdout.write('Daily checks prioritize Sentry and production anomalies; larger cadences analyze all configured projects and connectors.\n');
                return;
            }
            let config = await loadEditableConfig(configPath);
            config.version = Number(config.version || 7);
            config.generatedAt = new Date().toISOString();
            const inputSetup = await askInputSourceConfig(rl, config, configPath);
            config = inputSetup.config;
            await ensureDirForFile(configPath);
            await writeJsonFile(configPath, config);
            const connectorsOk = await runConnectorSetupSteps({
                rl,
                args: { ...args, config: configPath },
                selected: inputSetup.selected,
                healthByConnector: inputSetup.healthByConnector,
                allowIsolationPrompt: false,
            });
            if (!connectorsOk) {
                return;
            }
            config = await loadEditableConfig(configPath);
            config.version = Number(config.version || 7);
            config.generatedAt = new Date().toISOString();
            config = await askIntervalConfig(rl, config);
            config = await askOutputConfig(rl, config);
            config = await askGitHubArtifactDetails(rl, config);
            const secretAccess = await askSecretAccessModel(rl, configPath, config);
            await ensureDirForFile(configPath);
            await fs.writeFile(configPath, JSON.stringify(config, null, 2), 'utf8');
            const manifestPath = await writeOpenClawJobManifest(configPath, config);
            const cronResult = await ensureOpenClawCronFromWizard(configPath, config);
            const hermesCronResult = await ensureHermesCronFromWizard(configPath, config);
            process.stdout.write(`\nSaved config: ${configPath}\n`);
            process.stdout.write(`Saved OpenClaw job manifest: ${manifestPath}\n`);
            printOpenClawCronResult(cronResult);
            printHermesCronResult(hermesCronResult);
            printSecretRunnerKitInstructions(secretAccess.kit);
            process.stdout.write('\nNext steps:\n');
            process.stdout.write(`1) Set secrets in OpenClaw secret store (env var names in config.secrets)\n`);
            process.stdout.write(`2) Run once: ${growthEngineerPackageCommand(`run --config ${quote(configPath)}`)}\n`);
            process.stdout.write('3) Prefer OpenClaw Gateway cron for recurring VPS runs; use the interval loop only as a manual fallback.\n');
            return;
        }
        catch (error) {
            if (error instanceof WizardBackError) {
                clearTerminal();
                continue;
            }
            throw error;
        }
        finally {
            rl.close();
        }
    }
}
main().catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = error instanceof WizardAbortError ? error.exitCode : 1;
});
