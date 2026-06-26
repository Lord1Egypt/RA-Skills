import assert from 'node:assert/strict';
import test from 'node:test';
import {
  buildAnalyticsSummary,
  buildAscSummary,
  buildCoolifySummary,
  buildRevenueCatSummary,
  buildSeoSummary,
  buildSentrySummary,
} from '../scripts/openclaw-exporters-lib.mjs';

test('buildAnalyticsSummary emits onboarding, paywall, and retention signals from weak funnel data', () => {
  const summary = buildAnalyticsSummary({
    projectId: 'project-123',
    last: '30d',
    onboardingJourney: {
      starters: 200,
      completedUsers: 72,
      completionRate: 36,
      paywallReachedUsers: 120,
      paywallSkippedUsers: 84,
      paywallSkipRateFromPaywall: 70,
      purchasedUsers: 8,
      purchaseRateFromPaywall: 6.67,
      paywallAnchorEvent: 'paywall:shown',
      paywallSkipEvent: 'paywall:skip',
      purchaseEvent: 'purchase:success',
      trends: {
        completionRate: {
          direction: 'down',
          percentChange: -18.5,
          startValue: 44,
          currentValue: 36,
        },
      },
    },
    retention: {
      cohortSize: 180,
      avgActiveDays: 2.7,
      days: [
        { day: 1, retainedUsers: 70, retentionRate: 0.39 },
        { day: 3, retainedUsers: 24, retentionRate: 0.13 },
        { day: 7, retainedUsers: 12, retentionRate: 0.067 },
      ],
    },
    maxSignals: 4,
  });

  assert.equal(summary.project, 'project-123');
  assert.equal(summary.window, 'last_30d');
  assert.equal(summary.signals.length, 4);
  assert.deepEqual(
    summary.signals.map((signal) => signal.id),
    [
      'paywall_skip_rate_above_target',
      'onboarding_completion_below_target',
      'retention_d7_below_target',
      'paywall_purchase_rate_below_target',
    ],
  );
});

test('buildAscSummary emits release blocker, rating, and review-theme signals', () => {
  const summary = buildAscSummary({
    appId: '123456789',
    statusPayload: {
      submission: {
        latest: {
          status: 'REJECTED',
        },
      },
      builds: {
        latest: {
          processingState: 'PROCESSING',
        },
      },
    },
    ratingsPayload: {
      averageRating: 3.7,
      ratingCount: 142,
    },
    reviewSummariesPayload: {
      data: [
        { attributes: { text: 'Users mention crashes and subscription pricing confusion.' } },
        { attributes: { text: 'Crashing after purchase and unclear paywall copy.' } },
      ],
    },
    feedbackPayload: {
      data: [
        { attributes: { feedback: 'Login feels broken and the app freezes.' } },
      ],
    },
    maxSignals: 4,
  });

  assert.equal(summary.project, 'app-store-connect:123456789');
  assert.equal(summary.window, 'latest');
  assert.equal(summary.signals.length, 4);
  assert.equal(summary.signals[0].id, 'asc_release_blockers_detected');
  assert(summary.signals.some((signal) => signal.id === 'asc_rating_below_target'));
  assert(summary.signals.some((signal) => signal.id === 'asc_review_theme_stability'));
  assert(summary.signals.some((signal) => signal.id === 'asc_review_theme_pricing'));
});

test('buildAscSummary emits ASC analytics crashes, units, conversion, and source signals', () => {
  const summary = buildAscSummary({
    appId: '123456789',
    analyticsMetricsPayload: {
      result: {
        results: [
          {
            measure: 'units',
            total: 100,
            previousTotal: 160,
            percentChange: -0.375,
            data: [{ date: '2026-05-03T00:00:00Z', value: 4 }],
          },
          {
            measure: 'redownloads',
            total: 12,
            previousTotal: 10,
            percentChange: 0.2,
            data: [{ date: '2026-05-03T00:00:00Z', value: 1 }],
          },
          {
            measure: 'conversionRate',
            total: 4.5,
            previousTotal: 6.2,
            percentChange: -0.274,
            data: [{ date: '2026-05-03T00:00:00Z', value: 3.9 }],
          },
          {
            measure: 'crashRate',
            total: 1.1,
            previousTotal: 0,
            percentChange: 1,
            data: [{ date: '2026-05-03T00:00:00Z', value: 1.1 }],
          },
        ],
      },
    },
    analyticsSourcesPayload: {
      result: {
        results: [
          {
            group: { key: 'Search', title: 'App Store Search' },
            data: [{ date: '2026-05-03T00:00:00Z', pageViewUnique: 90 }],
          },
          {
            group: { key: 'WebRef', title: 'Web Referrer' },
            data: [{ date: '2026-05-03T00:00:00Z', pageViewUnique: 10 }],
          },
        ],
      },
    },
    analyticsOverviewPayload: {
      acquisition: [
        {
          measure: 'pageViewCount',
          total: 80,
          previousTotal: 120,
          percentChange: -0.333,
          type: 'COUNT',
        },
      ],
      appUsageBreakdowns: [
        {
          measure: 'crashes',
          total: 3,
          items: [{ key: '1.0.0 (1)', label: '1.0.0 (iOS)', value: 3 }],
        },
      ],
    },
    analyticsWindow: { start: '2026-04-04', end: '2026-05-03' },
    maxSignals: 5,
  });

  assert.equal(summary.meta.analytics.totalCrashes, 3);
  assert.equal(summary.meta.analyticsAvailability, 'available');
  assert.equal(summary.meta.analytics.units.total, 100);
  assert.equal(summary.meta.analytics.sourceBreakdown[0].title, 'App Store Search');
  assert(summary.meta.analytics.overviewMetricCatalog.some((metric) => metric.measure === 'pageViewCount'));
  assert(summary.signals.some((signal) => signal.id === 'asc_production_crashes_detected'));
  assert(summary.signals.some((signal) => signal.id === 'asc_units_declining'));
  assert(summary.signals.some((signal) => signal.id === 'asc_conversion_rate_declining'));
  assert(summary.signals.some((signal) => signal.id === 'asc_source_mix_available'));
  assert(summary.signals.some((signal) => signal.id === 'asc_overview_metric_movements_detected'));
});

test('buildAscSummary normalizes API-key ASC batch report usage and commerce metrics', () => {
  const summary = buildAscSummary({
    appId: '123456789',
    batchAnalyticsPayload: {
      results: [
        { measure: 'impressions', total: 1200, data: [{ date: '2026-06-09', value: 1200 }] },
        { measure: 'pageViewUnique', total: 240, data: [{ date: '2026-06-09', value: 240 }] },
        { measure: 'units', total: 48, data: [{ date: '2026-06-09', value: 48 }] },
        { measure: 'sessions', total: 310, data: [{ date: '2026-06-09', value: 310 }] },
        { measure: 'activeDevices', total: 92, data: [{ date: '2026-06-09', value: 92 }] },
        { measure: 'purchases', total: 7, data: [{ date: '2026-06-09', value: 7 }] },
        { measure: 'proceeds', total: 42.5, data: [{ date: '2026-06-09', value: 42.5 }] },
        { measure: 'crashes', total: 2, data: [{ date: '2026-06-09', value: 2 }] },
      ],
      sourceBreakdown: [
        { key: 'APP_STORE_SEARCH', title: 'App Store Search', impressions: 900, pageViewUnique: 180, units: 36, purchases: 5 },
        { key: 'WEB_REFERRER', title: 'Web Referrer', impressions: 300, pageViewUnique: 60, units: 12, purchases: 2 },
      ],
      crashBreakdown: [{ label: '2.0.0 (iPhone)', value: 2 }],
      overviewMetricCatalog: [
        { section: 'batchReports', measure: 'sessions', total: 310, previousTotal: null, percentChange: null, type: 'COUNT' },
      ],
    },
    batchReports: [
      { label: 'ASC App Analytics batch report abc', outputPath: 'asc-cache/123456789/2026-06-09/analytics-abc.txt', rowCount: 4, cacheStatus: 'downloaded' },
    ],
    analyticsWindow: { start: '2026-05-11', end: '2026-06-09' },
    maxSignals: 8,
  });

  assert.equal(summary.meta.analyticsAvailability, 'available');
  assert.equal(summary.meta.analytics.impressions.total, 1200);
  assert.equal(summary.meta.analytics.sessions.total, 310);
  assert.equal(summary.meta.analytics.purchases.total, 7);
  assert.equal(summary.meta.analytics.proceeds.total, 42.5);
  assert.equal(summary.meta.analytics.totalCrashes, 2);
  assert.equal(summary.meta.analytics.sourceBreakdown[0].title, 'App Store Search');
  assert.equal(summary.meta.batchReports[0].cacheStatus, 'downloaded');
  assert(summary.signals.some((signal) => signal.id === 'asc_source_mix_available'));
  assert(summary.signals.some((signal) => signal.id === 'asc_commerce_metrics_available'));
  assert(summary.signals.some((signal) => signal.id === 'asc_usage_metrics_available'));
  assert(summary.signals.some((signal) => signal.id === 'asc_production_crashes_detected'));
});

test('buildRevenueCatSummary emits live metrics and catalog signals', () => {
  const summary = buildRevenueCatSummary({
    project: { id: 'proj_123', name: 'Flashes' },
    window: '2026-05-01_2026-05-30',
    revenuePayload: { value: 1240 },
    previousRevenuePayload: { value: 900 },
    overviewPayload: {
      metrics: [
        { id: 'revenue', name: 'Revenue', value: 1240 },
        { id: 'active_trials', name: 'Active Trials', value: 34 },
      ],
    },
    appsPayload: { items: [{ id: 'app_1', name: 'Flashes iOS' }] },
    productsPayload: { items: [{ id: 'prod_1', store_identifier: 'premium_monthly' }] },
    offeringsPayload: { items: [{ id: 'offering_1', display_name: 'Default' }] },
    entitlementsPayload: { items: [{ id: 'entitlement_1', display_name: 'Premium' }] },
    paywallsPayload: { items: [{ id: 'paywall_1', display_name: 'Main paywall' }] },
    webhooksPayload: { items: [{ id: 'webhook_1', display_name: 'Analytics webhook' }] },
    customersPayload: {
      items: [
        {
          id: 'redacted-in-real-output',
          last_seen_platform: 'ios',
          last_seen_country: 'US',
          active_entitlements: { items: [{ entitlement_id: 'entitlement_1' }] },
        },
      ],
    },
    chartsPayload: {
      mrr: { display_name: 'MRR', summary: { total: 500 } },
      trials_new: { display_name: 'New Trials', summary: { total: 12 } },
    },
    maxSignals: 8,
  });

  assert.equal(summary.project, 'revenuecat:proj_123');
  assert.equal(summary.meta.source, 'revenuecat');
  assert.equal(summary.meta.productsCount, 1);
  assert.equal(summary.meta.paywallsCount, 1);
  assert.equal(summary.meta.webhookIntegrationsCount, 1);
  assert.equal(summary.meta.customerSample.sampledCustomers, 1);
  assert.equal(summary.meta.chartsCount, 2);
  assert.equal(summary.meta.revenue, 1240);
  assert(summary.signals.some((signal) => signal.id === 'revenuecat_revenue_window'));
  assert(summary.signals.some((signal) => signal.id === 'revenuecat_growth_charts_available'));
  assert(summary.signals.some((signal) => signal.id === 'revenuecat_customer_sample_available'));
  assert(summary.signals.some((signal) => signal.id === 'revenuecat_overview_metrics_available'));
  assert(summary.signals.some((signal) => signal.id === 'revenuecat_catalog_summary'));
});

test('buildRevenueCatSummary combines multiple projects', () => {
  const first = buildRevenueCatSummary({
    project: { id: 'proj_ios', name: 'iOS' },
    revenuePayload: { value: 100 },
    appsPayload: { items: [{ id: 'app_ios' }] },
    productsPayload: { items: [{ id: 'prod_ios' }] },
    offeringsPayload: { items: [{ id: 'off_ios' }] },
    entitlementsPayload: { items: [{ id: 'ent_ios' }] },
    paywallsPayload: { items: [{ id: 'pw_ios' }] },
    webhooksPayload: { items: [{ id: 'wh_ios' }] },
  });
  const second = buildRevenueCatSummary({
    project: { id: 'proj_android', name: 'Android' },
    revenuePayload: { value: 50 },
    appsPayload: { items: [{ id: 'app_android' }] },
    productsPayload: { items: [{ id: 'prod_android' }] },
    offeringsPayload: { items: [{ id: 'off_android' }] },
    entitlementsPayload: { items: [{ id: 'ent_android' }] },
    paywallsPayload: { items: [] },
    webhooksPayload: { items: [] },
  });
  const summary = buildRevenueCatSummary({
    projects: [first, second],
    availableProjectCount: 2,
    availableProjectIds: ['proj_ios', 'proj_android'],
    maxSignals: 8,
  });

  assert.equal(summary.project, 'revenuecat:multiple');
  assert.equal(summary.meta.multiProject, true);
  assert.equal(summary.meta.projectCount, 2);
  assert(summary.signals.some((signal) => signal.id.startsWith('proj_ios:')));
  assert(summary.signals.some((signal) => signal.id.startsWith('proj_android:')));
});

test('buildCoolifySummary emits deployment and health-check signals', () => {
  const summary = buildCoolifySummary({
    baseUrl: 'https://coolify.wotaso.com',
    last: '24h',
    applications: [
      {
        uuid: 'app-1',
        name: 'Landing',
        domains: 'https://analyticscli.com',
        status: 'running',
        health_check_enabled: false,
      },
      {
        uuid: 'app-2',
        name: 'API',
        domains: 'https://api.analyticscli.com',
        status: 'unhealthy',
        health_check_enabled: true,
      },
    ],
    deployments: [
      {
        deployment_uuid: 'dep-1',
        application_name: 'API',
        status: 'failed',
        created_at: new Date().toISOString(),
      },
    ],
    maxSignals: 5,
  });

  assert.equal(summary.project, 'coolify:https://coolify.wotaso.com');
  assert.equal(summary.meta.source, 'coolify');
  assert(summary.signals.some((signal) => signal.id === 'coolify_failed_deployments'));
  assert(summary.signals.some((signal) => signal.id === 'coolify_unhealthy_resources'));
  assert(summary.signals.some((signal) => signal.id === 'coolify_public_apps_without_health_checks'));
});

test('buildSeoSummary emits GSC sitemap and URL inspection signals', () => {
  const summary = buildSeoSummary({
    siteUrl: 'https://example.com/',
    window: '2026-04-01_2026-06-30',
    rows: [
      { keys: ['analytics cli', 'https://example.com/'], impressions: 1000, clicks: 10, ctr: 0.01, position: 7 },
    ],
    gscContext: {
      sites: ['https://example.com/'],
      sitemaps: [
        {
          siteUrl: 'https://example.com/',
          sitemaps: [
            { path: 'https://example.com/sitemap.xml', errors: 2, warnings: 1, isPending: false },
          ],
        },
      ],
      inspections: [
        {
          siteUrl: 'https://example.com/',
          inspectionUrl: 'https://example.com/pricing',
          result: {
            indexStatusResult: {
              verdict: 'FAIL',
              coverageState: 'Crawled - currently not indexed',
              robotsTxtState: 'ALLOWED',
            },
          },
        },
      ],
    },
    maxSignals: 8,
  });

  assert.equal(summary.project, 'seo:https://example.com/');
  assert.equal(summary.meta.gscSites.length, 1);
  assert.equal(summary.meta.gscSitemaps.length, 1);
  assert.equal(summary.meta.gscInspections.length, 1);
  assert(summary.signals.some((signal) => signal.id === 'seo_gsc_high_impression_low_ctr'));
  assert(summary.signals.some((signal) => signal.id === 'seo_gsc_sitemap_issues'));
  assert(summary.signals.some((signal) => signal.id === 'seo_gsc_url_inspection_issues'));
});

test('buildSentrySummary emits crash issues and signals from unresolved issues', () => {
  const summary = buildSentrySummary({
    org: 'wotaso',
    project: 'flashes',
    environment: 'production',
    last: '7d',
    issuesPayload: [
      {
        id: '123',
        shortId: 'FLASHES-1',
        title: 'TypeError: cannot read property paywallPackage',
        level: 'error',
        count: 42,
        userCount: 11,
        firstSeen: '2026-05-01T00:00:00Z',
        lastSeen: '2026-05-03T00:00:00Z',
        culprit: 'PaywallScreen',
        permalink: 'https://sentry.io/issues/123',
        eventsPayload: [
          {
            id: 'event-1',
            timestamp: '2026-05-03T01:00:00Z',
            release: '1.2.3',
            webUrl: 'https://sentry.io/events/event-1',
          },
        ],
      },
    ],
    maxSignals: 3,
  });

  assert.equal(summary.project, 'sentry:wotaso/flashes');
  assert.equal(summary.meta.source, 'sentry');
  assert.equal(summary.issues.length, 1);
  assert.equal(summary.issues[0].id, '123');
  assert.equal(summary.issues[0].priority, 'medium');
  assert.equal(summary.issues[0].sourceUrl, 'https://sentry.io/issues/123');
  assert.equal(summary.issues[0].app, 'sentry:wotaso/flashes');
  assert.equal(summary.issues[0].sampleEvents, 1);
  assert.equal(summary.meta.sampledIssueEvents, 1);
  assert.equal(summary.signals[0].area, 'crash');
  assert.equal(summary.signals[0].sampleEvents, 1);
  assert.equal(summary.signals[0].sourceUrl, 'https://sentry.io/issues/123');
  assert.equal(summary.signals[0].app, 'sentry:wotaso/flashes');
  assert(summary.signals[0].evidence.some((entry) => entry.includes('FLASHES-1')));
  assert(summary.signals[0].evidence.some((entry) => entry.includes('https://sentry.io/issues/123')));
  assert(summary.signals[0].evidence.some((entry) => entry.includes('Sampled issue events: 1')));
});

test('buildSentrySummary combines multiple Sentry-compatible accounts', () => {
  const summary = buildSentrySummary({
    accounts: [
      {
        id: 'sentry_cloud_ios',
        label: 'Sentry Cloud iOS',
        org: 'wotaso',
        project: 'flashes-ios',
        environment: 'production',
        issuesPayload: [{ id: 'ios-1', title: 'Fatal iOS crash', level: 'fatal', count: 3, userCount: 2, permalink: 'https://sentry.io/issues/ios-1' }],
      },
      {
        id: 'glitchtip_api',
        label: 'GlitchTip API',
        org: 'wotaso',
        project: 'flashes-api',
        environment: 'production',
        issuesPayload: [{ id: 'api-1', title: 'Webhook error', level: 'error', count: 30, userCount: 9, permalink: 'https://glitchtip.wotaso.com/issues/api-1' }],
      },
    ],
    last: '7d',
    maxSignals: 5,
  });

  assert.equal(summary.project, 'sentry:multiple');
  assert.equal(summary.meta.multiAccount, true);
  assert.equal(summary.meta.accountCount, 2);
  assert.equal(summary.issues.length, 2);
  assert(summary.issues.some((issue) => issue.app === 'sentry:wotaso/flashes-ios'));
  assert(summary.issues.some((issue) => issue.sourceUrl === 'https://glitchtip.wotaso.com/issues/api-1'));
  assert(summary.signals.some((signal) => signal.id.startsWith('sentry_cloud_ios:')));
  assert(summary.signals.some((signal) => signal.id.startsWith('glitchtip_api:')));
  assert(summary.signals.some((signal) => signal.app === 'sentry:wotaso/flashes-api'));
  assert(summary.signals.some((signal) => signal.sourceUrl === 'https://sentry.io/issues/ios-1'));
  assert(summary.signals.every((signal) => signal.evidence.some((entry) => entry.startsWith('Sentry account:'))));
});
