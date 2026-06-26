import { promises as fs } from 'node:fs';
import path from 'node:path';
function coerceNumber(value) {
    if (typeof value === 'number' && Number.isFinite(value)) {
        return value;
    }
    if (typeof value === 'string' && value.trim()) {
        const parsed = Number(value);
        if (Number.isFinite(parsed)) {
            return parsed;
        }
    }
    return null;
}
function coerceRatioFromPercent(value) {
    const numeric = coerceNumber(value);
    if (numeric === null)
        return null;
    return numeric / 100;
}
function round(value, digits = 4) {
    if (!Number.isFinite(value))
        return 0;
    return Number(value.toFixed(digits));
}
function computeDeltaPercent(currentValue, baselineValue) {
    if (!Number.isFinite(currentValue) || !Number.isFinite(baselineValue)) {
        return null;
    }
    if (Math.abs(baselineValue) < 1e-9) {
        if (Math.abs(currentValue) < 1e-9)
            return 0;
        return currentValue > 0 ? 100 : -100;
    }
    return round(((currentValue - baselineValue) / Math.abs(baselineValue)) * 100, 2);
}
function normalizeWindow(last) {
    const normalized = String(last || '30d')
        .trim()
        .toLowerCase();
    if (!normalized)
        return 'last_30d';
    if (normalized.startsWith('last_'))
        return normalized;
    return `last_${normalized}`;
}
function priorityRank(priority) {
    if (priority === 'high')
        return 3;
    if (priority === 'medium')
        return 2;
    return 1;
}
function sortSignals(signals) {
    return [...signals].sort((a, b) => {
        const priorityDelta = priorityRank(String(b.priority || 'low')) - priorityRank(String(a.priority || 'low'));
        if (priorityDelta !== 0)
            return priorityDelta;
        const deltaA = Math.abs(coerceNumber(a.delta_percent ?? a.deltaPercent) || 0);
        const deltaB = Math.abs(coerceNumber(b.delta_percent ?? b.deltaPercent) || 0);
        return deltaB - deltaA;
    });
}
function hasMinimumSample(value, minimum = 20) {
    const numeric = coerceNumber(value);
    return numeric !== null && numeric >= minimum;
}
function normalizeRetentionReliability(retention) {
    if (!retention?.quality || typeof retention.quality !== 'object') {
        return null;
    }
    const value = String(retention?.quality?.reliability || '')
        .trim()
        .toLowerCase();
    if (value === 'high' || value === 'medium' || value === 'low' || value === 'unknown') {
        return value;
    }
    return 'unknown';
}
function buildRetentionQualityEvidence(retention) {
    const quality = retention?.quality;
    if (!quality || typeof quality !== 'object') {
        return [];
    }
    const evidence = [`Retention reliability: ${normalizeRetentionReliability(retention)}`];
    const stableShare = coerceNumber(quality.stableIdentityShare);
    const multiSessionShare = coerceNumber(quality.multiSessionShare);
    if (stableShare !== null) {
        evidence.push(`Stable identity share: ${(stableShare * 100).toFixed(1)}%`);
    }
    if (multiSessionShare !== null) {
        evidence.push(`Multi-session identity share: ${(multiSessionShare * 100).toFixed(1)}%`);
    }
    if (Array.isArray(quality.warnings)) {
        for (const warning of quality.warnings.slice(0, 2)) {
            if (typeof warning === 'string' && warning.trim()) {
                evidence.push(`Retention caveat: ${warning.trim()}`);
            }
        }
    }
    return evidence;
}
function hasRetentionIdentityPersistenceGap(retention) {
    const reliability = normalizeRetentionReliability(retention);
    if (reliability !== 'low' && reliability !== 'unknown') {
        return false;
    }
    const stableShare = coerceNumber(retention?.quality?.stableIdentityShare);
    const multiSessionShare = coerceNumber(retention?.quality?.multiSessionShare);
    if (stableShare !== null && stableShare >= 0.5) {
        return false;
    }
    if (multiSessionShare !== null && multiSessionShare >= 0.2) {
        return false;
    }
    return true;
}
function maybePushSignal(signals, signal) {
    if (!signal)
        return;
    signals.push(signal);
}
function buildAnalyticsTrendEvidence(label, trend) {
    if (!trend || typeof trend !== 'object')
        return null;
    const direction = String(trend.direction || '').trim();
    const percentChange = coerceNumber(trend.percentChange);
    const startValue = coerceNumber(trend.startValue);
    const currentValue = coerceNumber(trend.currentValue);
    if (!direction || percentChange === null || startValue === null || currentValue === null) {
        return null;
    }
    const signed = percentChange > 0 ? `+${percentChange}%` : `${percentChange}%`;
    return `${label} trend: ${direction} ${signed} (start=${startValue}, current=${currentValue})`;
}
export function buildAnalyticsSummary(input) {
    const last = String(input?.last || '30d');
    const onboardingJourney = input?.onboardingJourney || null;
    const retention = input?.retention || null;
    const project = String(onboardingJourney?.projectId || input?.projectId || input?.project || 'analyticscli-project').trim() || 'analyticscli-project';
    const signals = [];
    const starters = coerceNumber(onboardingJourney?.starters) || 0;
    const paywallReachedUsers = coerceNumber(onboardingJourney?.paywallReachedUsers) || 0;
    const completionRate = coerceRatioFromPercent(onboardingJourney?.completionRate);
    const paywallSkipRate = coerceRatioFromPercent(onboardingJourney?.paywallSkipRateFromPaywall);
    const purchaseRateFromPaywall = coerceRatioFromPercent(onboardingJourney?.purchaseRateFromPaywall);
    if (hasMinimumSample(starters)) {
        const completionBaseline = 0.6;
        if (completionRate !== null && completionRate < completionBaseline) {
            maybePushSignal(signals, {
                id: 'onboarding_completion_below_target',
                title: 'Onboarding completion rate is below target',
                area: 'onboarding',
                priority: completionRate < 0.45 ? 'high' : 'medium',
                metric: 'onboarding_completion_rate',
                current_value: round(completionRate),
                baseline_value: completionBaseline,
                delta_percent: computeDeltaPercent(completionRate, completionBaseline),
                evidence: [
                    `${onboardingJourney?.completedUsers || 0} of ${starters} onboarding starters completed successfully`,
                    onboardingJourney?.paywallAnchorEvent
                        ? `Paywall anchor event in the flow: ${onboardingJourney.paywallAnchorEvent}`
                        : 'No stable paywall anchor event detected in the onboarding journey payload',
                    buildAnalyticsTrendEvidence('Completion rate', onboardingJourney?.trends?.completionRate),
                ].filter(Boolean),
                suggested_actions: [
                    'Shorten the onboarding path before the first value moment',
                    'Delay monetization or permission friction until after the first core success event',
                    'Inspect the heaviest drop-off steps in the onboarding journey and simplify one of them',
                ],
                keywords: ['onboarding', 'completion', 'dropoff', 'first_value'],
            });
        }
    }
    if (hasMinimumSample(paywallReachedUsers)) {
        const paywallSkipBaseline = 0.45;
        if (paywallSkipRate !== null && paywallSkipRate > paywallSkipBaseline) {
            maybePushSignal(signals, {
                id: 'paywall_skip_rate_above_target',
                title: 'Paywall skip rate is above target',
                area: 'paywall',
                priority: paywallSkipRate > 0.6 ? 'high' : 'medium',
                metric: 'paywall_skip_rate',
                current_value: round(paywallSkipRate),
                baseline_value: paywallSkipBaseline,
                delta_percent: computeDeltaPercent(paywallSkipRate, paywallSkipBaseline),
                evidence: [
                    `${onboardingJourney?.paywallSkippedUsers || 0} users skipped after ${paywallReachedUsers} reached the paywall`,
                    onboardingJourney?.paywallSkipEvent
                        ? `Most visible skip event: ${onboardingJourney.paywallSkipEvent}`
                        : 'No stable skip event detected in the onboarding journey payload',
                    buildAnalyticsTrendEvidence('Paywall reached rate', onboardingJourney?.trends?.paywallReachedRate),
                ].filter(Boolean),
                suggested_actions: [
                    'Clarify the premium value proposition and annual-vs-monthly trade-off',
                    'Reduce cognitive load on the first paywall view and tighten the CTA hierarchy',
                    'Test a later paywall placement after a stronger proof-of-value moment',
                ],
                keywords: ['paywall', 'skip', 'pricing', 'conversion'],
            });
        }
        const purchaseBaseline = 0.12;
        if (purchaseRateFromPaywall !== null && purchaseRateFromPaywall < purchaseBaseline) {
            maybePushSignal(signals, {
                id: 'paywall_purchase_rate_below_target',
                title: 'Paywall-to-purchase conversion is below target',
                area: 'conversion',
                priority: purchaseRateFromPaywall < 0.06 ? 'high' : 'medium',
                metric: 'purchase_rate_from_paywall',
                current_value: round(purchaseRateFromPaywall),
                baseline_value: purchaseBaseline,
                delta_percent: computeDeltaPercent(purchaseRateFromPaywall, purchaseBaseline),
                evidence: [
                    `${onboardingJourney?.purchasedUsers || 0} purchases from ${paywallReachedUsers} paywall exposures`,
                    onboardingJourney?.purchaseEvent
                        ? `Purchase success event observed: ${onboardingJourney.purchaseEvent}`
                        : 'No stable purchase success event detected in the onboarding journey payload',
                    buildAnalyticsTrendEvidence('Purchase rate', onboardingJourney?.trends?.purchaseRate),
                ].filter(Boolean),
                suggested_actions: [
                    'Simplify the paywall package comparison and highlight the default recommended offer',
                    'Reduce ambiguity around trial terms, pricing cadence, and restore flow',
                    'Test a stronger trust/benefit section near the purchase CTA',
                ],
                keywords: ['purchase', 'paywall', 'subscription', 'conversion'],
            });
        }
    }
    const retentionByDay = new Map(Array.isArray(retention?.days)
        ? retention.days
            .map((entry) => {
            const day = coerceNumber(entry?.day);
            const rate = coerceNumber(entry?.retentionRate);
            if (day === null || rate === null)
                return null;
            return [day, rate];
        })
            .filter((entry) => entry !== null)
        : []);
    const retentionTargets = [
        { day: 7, baseline: 0.1 },
        { day: 3, baseline: 0.2 },
        { day: 1, baseline: 0.35 },
    ];
    const retentionReliability = normalizeRetentionReliability(retention);
    const retentionHasLowConfidence = retentionReliability === 'low' || retentionReliability === 'unknown';
    const retentionQualityEvidence = buildRetentionQualityEvidence(retention);
    const retentionIdentityPersistenceGap = hasRetentionIdentityPersistenceGap(retention);
    if (hasMinimumSample(retention?.cohortSize)) {
        if (retentionIdentityPersistenceGap) {
            maybePushSignal(signals, {
                id: 'analytics_identity_persistence_missing',
                title: 'Analytics identity persistence is missing; D7 retention is not reliable',
                area: 'analytics_anomaly',
                priority: 'high',
                metric: 'retention_identity_quality',
                current_value: coerceNumber(retention?.quality?.stableIdentityShare) || 0,
                baseline_value: 0.5,
                delta_percent: computeDeltaPercent(coerceNumber(retention?.quality?.stableIdentityShare) || 0, 0.5),
                evidence: [
                    `Retention cohort size: ${retention.cohortSize}`,
                    ...retentionQualityEvidence,
                    'D1/D7 retention is suppressed from product findings until the host app persists a stable SDK identity.',
                ].filter(Boolean),
                suggested_actions: [
                    'Enable persistent AnalyticsCLI SDK identity in the host app before evaluating D1/D7 retention',
                    'Verify new release events carry identityQuality=persistent or identified instead of ephemeral or unknown',
                    'Rerun retention after at least one cohort has stable identity coverage',
                ],
                keywords: ['analyticscli', 'identity', 'persistence', 'retention', 'd7'],
            });
        }
        else {
            for (const target of retentionTargets) {
                const actual = retentionByDay.get(target.day);
                if (actual === undefined || actual >= target.baseline) {
                    continue;
                }
                maybePushSignal(signals, {
                    id: `retention_d${target.day}_below_target`,
                    title: retentionHasLowConfidence
                        ? `Day-${target.day} retention appears below target, but identity quality is low`
                        : `Day-${target.day} retention is below target`,
                    area: 'retention',
                    priority: retentionHasLowConfidence ? 'medium' : target.day >= 3 ? 'high' : 'medium',
                    metric: `d${target.day}_retention`,
                    current_value: round(actual),
                    baseline_value: target.baseline,
                    delta_percent: computeDeltaPercent(actual, target.baseline),
                    evidence: [
                        `Retention cohort size: ${retention.cohortSize}`,
                        `Observed D${target.day} retention: ${(actual * 100).toFixed(2)}%`,
                        ...retentionQualityEvidence,
                        retention?.avgActiveDays !== undefined
                            ? `Average active days in the cohort: ${retention.avgActiveDays}`
                            : null,
                    ].filter(Boolean),
                    suggested_actions: [
                        retentionHasLowConfidence
                            ? 'Verify SDK identity persistence and rerun retention with stable identity filtering before treating D1/D7 as a product fact'
                            : null,
                        'Revisit the first-session value loop and ensure the core action completes quickly',
                        'Add targeted re-entry prompts or reminders after the first session',
                        'Instrument the major early-session drop-off points to isolate which step drives the retention loss',
                    ].filter(Boolean),
                    keywords: ['retention', 'engagement', 'activation', `d${target.day}`],
                });
                break;
            }
        }
    }
    return {
        project,
        window: normalizeWindow(last),
        signals: sortSignals(signals).slice(0, Math.max(1, Number(input?.maxSignals) || 4)),
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'analyticscli',
            starters,
            paywallReachedUsers,
            retentionCohortSize: coerceNumber(retention?.cohortSize) || 0,
            retentionReliability: retentionReliability || 'unreported',
            retentionStableIdentityShare: coerceNumber(retention?.quality?.stableIdentityShare) || 0,
        },
    };
}
function isObject(value) {
    return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}
function walk(value, visitor, pathParts = []) {
    if (Array.isArray(value)) {
        value.forEach((entry, index) => {
            walk(entry, visitor, [...pathParts, String(index)]);
        });
        return;
    }
    if (!isObject(value)) {
        visitor(value, pathParts);
        return;
    }
    for (const [key, entry] of Object.entries(value)) {
        const nextPath = [...pathParts, key];
        visitor(entry, nextPath, key);
        walk(entry, visitor, nextPath);
    }
}
function collectStatusEntries(payload) {
    const entries = [];
    walk(payload, (value, pathParts, key) => {
        if (typeof value !== 'string')
            return;
        const normalizedKey = String(key || '').toLowerCase();
        if (!['state', 'status', 'processingstate', 'reviewstate'].includes(normalizedKey)) {
            return;
        }
        entries.push({
            path: pathParts.join('.'),
            value: value.trim(),
        });
    });
    return entries;
}
function normalizeVersionToken(value) {
    const normalized = String(value || '').trim();
    if (!normalized)
        return '';
    const match = normalized.match(/\b\d+(?:\.\d+){1,3}(?:\+\d+)?\b/);
    return match ? match[0] : '';
}
function collectAscProductionVersions(payload) {
    const candidates = [];
    walk(payload, (value, pathParts, key) => {
        if (typeof value !== 'string' && typeof value !== 'number')
            return;
        const normalizedKey = String(key || '').toLowerCase();
        if (!/(version|string|build|release)/.test(normalizedKey))
            return;
        const version = normalizeVersionToken(value);
        if (!version)
            return;
        const pathText = pathParts.join('.').toLowerCase();
        const parentPath = pathParts.slice(0, -1).join('.').toLowerCase();
        const context = String(JSON.stringify(resolvePathPayload(payload, pathParts.slice(0, -1))) || '').toLowerCase();
        if (/(ready_for_sale|readyforsale|approved|active|available|current|live|production)/.test(`${pathText} ${parentPath} ${context}`)) {
            candidates.push(version);
        }
    });
    return [...new Set(candidates)].sort();
}
function resolvePathPayload(payload, pathParts) {
    let current = payload;
    for (const part of pathParts) {
        if (!current || typeof current !== 'object')
            return null;
        current = current[part];
    }
    return current;
}
function classifyAscStatus(value) {
    const normalized = String(value || '')
        .trim()
        .toLowerCase();
    if (!normalized)
        return null;
    if (/(reject|rejected|fail|failed|error|invalid|missing|remove|blocked|denied|cancel)/.test(normalized)) {
        return 'blocking';
    }
    if (/(processing|pending|waiting|prepare_for_submission|ready_for_review|in_review)/.test(normalized)) {
        return 'watch';
    }
    if (/(ready_for_sale|approved|active|available|complete|passed|ok)/.test(normalized)) {
        return 'healthy';
    }
    return null;
}
function findNumbersByCandidateKeys(payload, candidateKeys) {
    const matches = [];
    walk(payload, (value, pathParts, key) => {
        if (!key)
            return;
        const normalizedKey = String(key).toLowerCase();
        if (!candidateKeys.includes(normalizedKey))
            return;
        const numeric = coerceNumber(value);
        if (numeric === null)
            return;
        matches.push({ path: pathParts.join('.'), value: numeric });
    });
    return matches;
}
function extractReviewTexts(payload) {
    const texts = [];
    walk(payload, (value, pathParts, key) => {
        if (typeof value !== 'string')
            return;
        const normalizedKey = String(key || '').toLowerCase();
        if (!['text', 'comment', 'summary', 'body', 'title', 'feedback'].includes(normalizedKey)) {
            return;
        }
        const trimmed = value.trim();
        if (!trimmed)
            return;
        texts.push({
            path: pathParts.join('.'),
            text: trimmed,
        });
    });
    return texts;
}
function rankKeywordThemes(texts) {
    const themeDefinitions = [
        {
            id: 'stability',
            area: 'stability',
            keywords: ['crash', 'crashes', 'crashing', 'freeze', 'frozen', 'bug', 'broken'],
            suggestedActions: [
                'Review recent crash and review signals together to isolate the highest-impact regression',
                'Prioritize the failing flow in the next patch release and add deterministic regression coverage',
            ],
        },
        {
            id: 'pricing',
            area: 'paywall',
            keywords: [
                'subscription',
                'subscribe',
                'paywall',
                'price',
                'pricing',
                'trial',
                'premium',
                'restore',
            ],
            suggestedActions: [
                'Clarify package differences and restore messaging in the paywall flow',
                'Use review phrasing directly to rewrite confusing pricing copy',
            ],
        },
        {
            id: 'auth',
            area: 'authentication',
            keywords: ['login', 'log in', 'sign in', 'account', 'password'],
            suggestedActions: [
                'Audit authentication entry points and reduce avoidable sign-in friction',
                'Surface clearer account state and recovery messaging in the first-session path',
            ],
        },
        {
            id: 'onboarding',
            area: 'onboarding',
            keywords: ['onboarding', 'tutorial', 'signup', 'sign up', 'permission', 'too long'],
            suggestedActions: [
                'Trim the onboarding path and move optional steps later',
                'Match onboarding copy more closely to the first-value promise from the store listing',
            ],
        },
        {
            id: 'performance',
            area: 'performance',
            keywords: ['slow', 'lag', 'loading', 'stuck', 'wait'],
            suggestedActions: [
                'Measure the slowest startup and primary interaction paths that users mention',
                'Ship a focused performance pass on the worst-loading user journeys',
            ],
        },
    ];
    return themeDefinitions
        .map((theme) => {
        let hits = 0;
        for (const entry of texts) {
            const normalized = entry.text.toLowerCase();
            for (const keyword of theme.keywords) {
                if (normalized.includes(keyword)) {
                    hits += 1;
                }
            }
        }
        return { ...theme, hits };
    })
        .filter((theme) => theme.hits > 0)
        .sort((a, b) => b.hits - a.hits);
}
function collectAscMetricEntries(payload) {
    if (Array.isArray(payload?.result?.results))
        return payload.result.results;
    if (Array.isArray(payload?.results))
        return payload.results;
    if (Array.isArray(payload?.acquisition))
        return payload.acquisition;
    if (Array.isArray(payload))
        return payload;
    return [];
}
function findAscMetric(payload, measure) {
    const normalized = String(measure || '').toLowerCase();
    return collectAscMetricEntries(payload).find((entry) => String(entry?.measure || '').toLowerCase() === normalized) || null;
}
function normalizeMetricData(entry) {
    return Array.isArray(entry?.data)
        ? entry.data
            .map((point) => ({
            date: String(point?.date || '').slice(0, 10),
            value: coerceNumber(point?.value),
        }))
            .filter((point) => point.date && point.value !== null)
        : [];
}
function summarizeSourceBreakdown(payload) {
    const entries = Array.isArray(payload?.result?.results)
        ? payload.result.results
        : Array.isArray(payload?.results)
            ? payload.results
            : [];
    return entries
        .map((entry) => {
        const data = Array.isArray(entry?.data) ? entry.data : [];
        const total = data.reduce((sum, point) => sum + (coerceNumber(point?.pageViewUnique ?? point?.value) || 0), 0);
        return {
            key: String(entry?.group?.key || entry?.key || entry?.source || 'unknown'),
            title: String(entry?.group?.title || entry?.title || entry?.label || entry?.group?.key || 'Unknown'),
            pageViewUnique: total,
        };
    })
        .filter((entry) => entry.pageViewUnique > 0)
        .sort((a, b) => b.pageViewUnique - a.pageViewUnique);
}
function normalizeBatchSourceBreakdown(entries) {
    return (Array.isArray(entries) ? entries : [])
        .map((entry) => ({
        key: String(entry?.key || entry?.title || 'unknown'),
        title: String(entry?.title || entry?.key || 'Unknown'),
        impressions: coerceNumber(entry?.impressions) || 0,
        pageViewUnique: coerceNumber(entry?.pageViewUnique) || 0,
        units: coerceNumber(entry?.units) || 0,
        redownloads: coerceNumber(entry?.redownloads) || 0,
        purchases: coerceNumber(entry?.purchases) || 0,
        proceeds: coerceNumber(entry?.proceeds) || 0,
    }))
        .filter((entry) => entry.impressions > 0 ||
        entry.pageViewUnique > 0 ||
        entry.units > 0 ||
        entry.redownloads > 0 ||
        entry.purchases > 0 ||
        entry.proceeds > 0)
        .sort((a, b) => {
        const aValue = a.pageViewUnique || a.impressions || a.units || a.purchases || a.proceeds || 0;
        const bValue = b.pageViewUnique || b.impressions || b.units || b.purchases || b.proceeds || 0;
        return bValue - aValue;
    });
}
function extractAscCrashBreakdowns(payload) {
    const breakdowns = Array.isArray(payload?.appUsageBreakdowns) ? payload.appUsageBreakdowns : [];
    return breakdowns
        .filter((breakdown) => String(breakdown?.measure || '').toLowerCase() === 'crashes')
        .flatMap((breakdown) => Array.isArray(breakdown?.items)
        ? breakdown.items.map((item) => ({
            label: String(item?.label || item?.key || 'Unknown app version'),
            value: coerceNumber(item?.value) || 0,
        }))
        : [])
        .filter((entry) => entry.value > 0)
        .sort((a, b) => b.value - a.value);
}
function totalAscCrashes(payload) {
    const breakdowns = Array.isArray(payload?.appUsageBreakdowns) ? payload.appUsageBreakdowns : [];
    const directTotal = breakdowns
        .filter((breakdown) => String(breakdown?.measure || '').toLowerCase() === 'crashes')
        .reduce((sum, breakdown) => sum + (coerceNumber(breakdown?.total) || 0), 0);
    if (directTotal > 0)
        return directTotal;
    return extractAscCrashBreakdowns(payload).reduce((sum, entry) => sum + entry.value, 0);
}
function collectAscOverviewMetricCatalog(payload) {
    const sections = ['acquisition', 'sales', 'subscriptions'];
    const metrics = [];
    for (const section of sections) {
        const entries = Array.isArray(payload?.[section]) ? payload[section] : [];
        for (const entry of entries) {
            const measure = String(entry?.measure || '').trim();
            if (!measure)
                continue;
            metrics.push({
                section,
                measure,
                total: coerceNumber(entry?.total),
                previousTotal: coerceNumber(entry?.previousTotal),
                percentChange: coerceNumber(entry?.percentChange),
                type: String(entry?.type || '').trim() || null,
            });
        }
    }
    const breakdownSections = ['featureBreakdowns', 'appUsageBreakdowns'];
    for (const section of breakdownSections) {
        const entries = Array.isArray(payload?.[section]) ? payload[section] : [];
        for (const entry of entries) {
            const measure = String(entry?.measure || entry?.name || '').trim();
            if (!measure)
                continue;
            metrics.push({
                section,
                measure,
                total: coerceNumber(entry?.total),
                previousTotal: coerceNumber(entry?.previousTotal),
                percentChange: coerceNumber(entry?.percentChange),
                type: 'BREAKDOWN',
            });
        }
    }
    const planTimeline = Array.isArray(payload?.planTimeline) ? payload.planTimeline : [];
    for (const entry of planTimeline) {
        const totals = entry?.totals && typeof entry.totals === 'object' ? entry.totals : null;
        const measure = String(totals?.key || '').trim();
        if (!measure)
            continue;
        metrics.push({
            section: 'planTimeline',
            measure,
            total: coerceNumber(totals?.value),
            previousTotal: null,
            percentChange: null,
            type: String(totals?.type || 'COUNT'),
        });
    }
    const byKey = new Map();
    for (const metric of metrics) {
        const key = `${metric.section}:${metric.measure}`;
        if (!byKey.has(key))
            byKey.set(key, metric);
    }
    return [...byKey.values()];
}
function mergeMetricCatalogs(...catalogs) {
    const byKey = new Map();
    for (const catalog of catalogs) {
        for (const metric of Array.isArray(catalog) ? catalog : []) {
            const section = String(metric?.section || 'unknown');
            const measure = String(metric?.measure || '').trim();
            if (!measure)
                continue;
            const key = `${section}:${measure}`;
            if (!byKey.has(key)) {
                byKey.set(key, {
                    section,
                    measure,
                    total: coerceNumber(metric?.total),
                    previousTotal: coerceNumber(metric?.previousTotal),
                    percentChange: coerceNumber(metric?.percentChange),
                    type: String(metric?.type || 'COUNT'),
                });
            }
        }
    }
    return [...byKey.values()];
}
function metricSnapshot(metric) {
    return metric
        ? {
            total: coerceNumber(metric.total) ?? 0,
            previousTotal: coerceNumber(metric.previousTotal),
            percentChange: coerceNumber(metric.percentChange),
        }
        : null;
}
function formatMetricMovement(metric) {
    const total = metric.total === null ? 'unknown' : round(metric.total);
    const previous = metric.previousTotal === null ? null : ` previous ${round(metric.previousTotal)}`;
    const change = metric.percentChange === null ? null : ` change ${formatPercent(metric.percentChange)}`;
    return `${metric.section}.${metric.measure}: ${total}${previous || ''}${change || ''}`;
}
function formatPercent(value) {
    if (value === null || value === undefined || !Number.isFinite(Number(value)))
        return 'unknown';
    return `${round(Number(value) * 100)}%`;
}
export function buildAscSummary(input) {
    const appId = String(input?.appId || 'ASC_APP_ID').trim() || 'ASC_APP_ID';
    const statusEntries = collectStatusEntries(input?.statusPayload);
    const productionVersions = collectAscProductionVersions(input?.statusPayload);
    const blockingStatuses = statusEntries.filter((entry) => classifyAscStatus(entry.value) === 'blocking');
    const watchStatuses = statusEntries.filter((entry) => classifyAscStatus(entry.value) === 'watch');
    const averageRatingCandidates = findNumbersByCandidateKeys(input?.ratingsPayload, [
        'averagerating',
        'averageuserrating',
        'ratingaverage',
        'avgrating',
    ]).filter((entry) => entry.value >= 0 && entry.value <= 5);
    const ratingCountCandidates = findNumbersByCandidateKeys(input?.ratingsPayload, [
        'ratingcount',
        'userratingcount',
        'ratingscount',
        'count',
    ]).filter((entry) => entry.value >= 0);
    const averageRating = averageRatingCandidates[0]?.value ?? null;
    const ratingCount = ratingCountCandidates[0]?.value ?? null;
    const reviewTexts = [
        ...extractReviewTexts(input?.reviewSummariesPayload),
        ...extractReviewTexts(input?.feedbackPayload),
    ];
    const topThemes = rankKeywordThemes(reviewTexts).slice(0, 2);
    const analyticsMetricsPayload = input?.batchAnalyticsPayload || input?.analyticsMetricsPayload || input?.analyticsOverviewPayload;
    const impressionsMetric = findAscMetric(analyticsMetricsPayload, 'impressions');
    const pageViewsMetric = findAscMetric(analyticsMetricsPayload, 'pageViewUnique');
    const unitsMetric = findAscMetric(analyticsMetricsPayload, 'units');
    const redownloadsMetric = findAscMetric(analyticsMetricsPayload, 'redownloads');
    const conversionRateMetric = findAscMetric(analyticsMetricsPayload || input?.analyticsOverviewPayload, 'conversionRate');
    const crashRateMetric = findAscMetric(analyticsMetricsPayload, 'crashRate');
    const crashesMetric = findAscMetric(analyticsMetricsPayload, 'crashes');
    const sessionsMetric = findAscMetric(analyticsMetricsPayload, 'sessions');
    const activeDevicesMetric = findAscMetric(analyticsMetricsPayload, 'activeDevices');
    const installationsMetric = findAscMetric(analyticsMetricsPayload, 'installations');
    const deletionsMetric = findAscMetric(analyticsMetricsPayload, 'deletions');
    const purchasesMetric = findAscMetric(analyticsMetricsPayload, 'purchases');
    const proceedsMetric = findAscMetric(analyticsMetricsPayload, 'proceeds');
    const payingUsersMetric = findAscMetric(analyticsMetricsPayload, 'payingUsers');
    const subscriptionsMetric = findAscMetric(analyticsMetricsPayload, 'subscriptions');
    const trialStartsMetric = findAscMetric(analyticsMetricsPayload, 'trialStarts');
    const sourceBreakdown = [
        ...normalizeBatchSourceBreakdown(input?.batchAnalyticsPayload?.sourceBreakdown),
        ...summarizeSourceBreakdown(input?.analyticsSourcesPayload),
    ];
    const totalSourcePageViews = sourceBreakdown.reduce((sum, source) => sum + (source.pageViewUnique || source.impressions || source.units || 0), 0);
    const topSource = sourceBreakdown[0] || null;
    const crashBreakdown = [
        ...(Array.isArray(input?.batchAnalyticsPayload?.crashBreakdown)
            ? input.batchAnalyticsPayload.crashBreakdown
            : []),
        ...extractAscCrashBreakdowns(input?.analyticsOverviewPayload),
    ]
        .filter((entry) => coerceNumber(entry?.value) > 0)
        .sort((a, b) => (coerceNumber(b?.value) || 0) - (coerceNumber(a?.value) || 0));
    const totalCrashes = coerceNumber(crashesMetric?.total) ||
        totalAscCrashes(input?.analyticsOverviewPayload) ||
        crashBreakdown.reduce((sum, entry) => sum + (coerceNumber(entry?.value) || 0), 0);
    const analyticsWarnings = Array.isArray(input?.analyticsWarnings) ? input.analyticsWarnings : [];
    const batchReports = Array.isArray(input?.batchReports) ? input.batchReports : [];
    const analyticsWarningText = analyticsWarnings
        .map((warning) => String(warning))
        .filter((warning) => /analytics|batch report|sales report|sales batch|direct api|request listing|report segment/i.test(warning))
        .join('\n')
        .toLowerCase();
    const analyticsAuthBlocked = analyticsWarningText.includes('forbidden for security') ||
        analyticsWarningText.includes('api key in use does not allow this request') ||
        analyticsWarningText.includes('does not allow this request') ||
        analyticsWarningText.includes('403') ||
        analyticsWarningText.includes('forbidden');
    const analyticsTemporarilyUnavailable = analyticsWarningText.includes('timed out after') ||
        analyticsWarningText.includes('temporarily unavailable') ||
        analyticsWarningText.includes('unexpected error occurred') ||
        analyticsWarningText.includes('fetch failed') ||
        analyticsWarningText.includes('network timeout');
    const hasAnalyticsData = Boolean(analyticsMetricsPayload ||
        unitsMetric ||
        conversionRateMetric ||
        sourceBreakdown.length > 0 ||
        totalCrashes > 0 ||
        batchReports.length > 0);
    const analyticsAvailability = analyticsAuthBlocked
        ? hasAnalyticsData
            ? 'partial_auth_blocked'
            : 'auth_blocked'
        : analyticsTemporarilyUnavailable
            ? hasAnalyticsData
                ? 'partial_temporarily_unavailable'
                : 'temporarily_unavailable'
            : hasAnalyticsData
                ? 'available'
                : 'unknown';
    const overviewMetricCatalog = mergeMetricCatalogs(collectAscOverviewMetricCatalog(input?.analyticsOverviewPayload), input?.batchAnalyticsPayload?.overviewMetricCatalog);
    const notableOverviewMetrics = overviewMetricCatalog
        .filter((metric) => {
        const measure = metric.measure.toLowerCase();
        if (['units', 'redownloads', 'conversionrate'].includes(measure))
            return false;
        if (measure === 'crashrate' || measure === 'crashes')
            return false;
        const percentChange = Math.abs(coerceNumber(metric.percentChange) || 0);
        const total = Math.abs(coerceNumber(metric.total) || 0);
        return percentChange >= 0.1 || total > 0;
    })
        .sort((a, b) => {
        const aChange = Math.abs(coerceNumber(a.percentChange) || 0);
        const bChange = Math.abs(coerceNumber(b.percentChange) || 0);
        if (aChange !== bChange)
            return bChange - aChange;
        return Math.abs(coerceNumber(b.total) || 0) - Math.abs(coerceNumber(a.total) || 0);
    })
        .slice(0, 6);
    const nonZeroCrashRateDays = normalizeMetricData(crashRateMetric)
        .filter((point) => Number(point.value) > 0)
        .slice(-5);
    const signals = [];
    if (blockingStatuses.length > 0) {
        maybePushSignal(signals, {
            id: 'asc_release_blockers_detected',
            title: 'App Store Connect reports blocking release states',
            area: 'release',
            priority: 'high',
            metric: 'asc_release_blockers',
            current_value: blockingStatuses.length,
            baseline_value: 0,
            delta_percent: blockingStatuses.length > 0 ? 100 : 0,
            evidence: blockingStatuses.slice(0, 5).map((entry) => `${entry.path}: ${entry.value}`),
            suggested_actions: [
                'Open the failing ASC section and resolve the blocking review, submission, or build issue',
                'Link the blocking ASC state to the corresponding release checklist item before the next submission',
            ],
            keywords: ['asc', 'review', 'submission', 'release', 'blocker'],
        });
    }
    else if (watchStatuses.length > 0) {
        maybePushSignal(signals, {
            id: 'asc_release_in_progress',
            title: 'App Store Connect still shows in-progress release states',
            area: 'release',
            priority: 'medium',
            metric: 'asc_release_watch_states',
            current_value: watchStatuses.length,
            baseline_value: 0,
            delta_percent: watchStatuses.length > 0 ? 100 : 0,
            evidence: watchStatuses.slice(0, 5).map((entry) => `${entry.path}: ${entry.value}`),
            suggested_actions: [
                'Monitor build processing and review transitions until they reach a terminal healthy state',
                'Avoid scheduling a coordinated release action until ASC processing has finished',
            ],
            keywords: ['asc', 'processing', 'review', 'submission'],
        });
    }
    if (averageRating !== null && ratingCount !== null && ratingCount >= 20 && averageRating < 4.2) {
        const ratingBaseline = 4.2;
        maybePushSignal(signals, {
            id: 'asc_rating_below_target',
            title: 'App Store rating is below target',
            area: 'store',
            priority: averageRating < 3.8 ? 'high' : 'medium',
            metric: 'app_store_average_rating',
            current_value: round(averageRating),
            baseline_value: ratingBaseline,
            delta_percent: computeDeltaPercent(averageRating, ratingBaseline),
            evidence: [
                `Average rating: ${averageRating.toFixed(2)} from ${Math.round(ratingCount)} ratings`,
                'Ratings came from the ASC review ratings command output',
            ],
            suggested_actions: [
                'Read recent review summaries to identify the dominant complaint before changing store copy',
                'Tie the next release notes and onboarding/paywall adjustments to the main rating complaint themes',
            ],
            keywords: ['app_store', 'rating', 'reviews', 'aso'],
        });
    }
    for (const theme of topThemes) {
        maybePushSignal(signals, {
            id: `asc_review_theme_${theme.id}`,
            title: `Store and beta feedback repeatedly mention ${theme.area} issues`,
            area: theme.area,
            priority: theme.hits >= 4 ? 'high' : 'medium',
            metric: `feedback_theme_${theme.id}`,
            current_value: theme.hits,
            baseline_value: 0,
            delta_percent: theme.hits > 0 ? 100 : 0,
            evidence: reviewTexts
                .slice(0, 3)
                .map((entry) => entry.text)
                .filter(Boolean),
            suggested_actions: theme.suggestedActions,
            keywords: ['reviews', 'feedback', theme.area, ...theme.keywords.slice(0, 3)],
        });
    }
    if (totalCrashes > 0 || nonZeroCrashRateDays.length > 0) {
        maybePushSignal(signals, {
            id: 'asc_production_crashes_detected',
            title: 'ASC reports production crashes',
            area: 'crash',
            priority: totalCrashes >= 10 || nonZeroCrashRateDays.length >= 3 ? 'high' : 'medium',
            metric: 'asc_total_crashes',
            current_value: totalCrashes,
            baseline_value: 0,
            delta_percent: totalCrashes > 0 ? 100 : null,
            evidence: [
                totalCrashes > 0 ? `ASC total crashes: ${totalCrashes}` : null,
                ...crashBreakdown
                    .slice(0, 3)
                    .map((entry) => `Crashes by app version: ${entry.label} = ${entry.value}`),
                ...nonZeroCrashRateDays.map((point) => `Crash rate ${point.date}: ${point.value}`),
            ].filter(Boolean),
            suggested_actions: [
                'Notify the OpenClaw user through the connected chat or social delivery channel before growth traffic is scaled',
                'Compare ASC total crashes with Sentry production issues for the same app version and date range',
                'If GitHub issue/PR write access is configured in OpenClaw, create the tracking issue or implementation PR automatically',
            ],
            keywords: ['asc', 'crash', 'production', 'sentry', 'release'],
        });
    }
    if (notableOverviewMetrics.length > 0) {
        maybePushSignal(signals, {
            id: 'asc_overview_metric_movements_detected',
            title: 'ASC overview metrics have movement worth comparing',
            area: 'analytics',
            priority: notableOverviewMetrics.some((metric) => Math.abs(coerceNumber(metric.percentChange) || 0) >= 0.5)
                ? 'medium'
                : 'low',
            metric: 'asc_overview_metrics',
            current_value: notableOverviewMetrics.length,
            baseline_value: overviewMetricCatalog.length,
            delta_percent: null,
            evidence: notableOverviewMetrics.map(formatMetricMovement),
            suggested_actions: [
                'Analyze every available ASC batch-report metric together with units, conversion, sources, AnalyticsCLI funnels, Sentry stability, and reviews before choosing a recommendation',
                'Keep financial metrics secondary unless the user asks, but still use them as validation for acquisition and conversion quality',
            ],
            keywords: ['asc', 'analytics', 'overview_metrics', 'conversion', 'handlungsempfehlung'],
        });
    }
    if (purchasesMetric || proceedsMetric || payingUsersMetric || subscriptionsMetric || trialStartsMetric) {
        const purchases = coerceNumber(purchasesMetric?.total) || 0;
        const proceeds = coerceNumber(proceedsMetric?.total) || 0;
        const payingUsers = coerceNumber(payingUsersMetric?.total) || 0;
        maybePushSignal(signals, {
            id: 'asc_commerce_metrics_available',
            title: 'ASC commerce metrics are available for store-to-revenue analysis',
            area: 'revenue',
            priority: 'low',
            metric: purchasesMetric ? 'asc_purchases' : proceedsMetric ? 'asc_proceeds' : 'asc_commerce_metrics',
            current_value: purchases || proceeds || payingUsers || coerceNumber(subscriptionsMetric?.total) || coerceNumber(trialStartsMetric?.total) || 0,
            baseline_value: null,
            delta_percent: null,
            evidence: [
                purchasesMetric ? `Purchases: ${purchases}` : null,
                proceedsMetric ? `Developer proceeds: ${round(proceeds)}` : null,
                payingUsersMetric ? `Paying users: ${payingUsers}` : null,
                subscriptionsMetric ? `Subscriptions: ${coerceNumber(subscriptionsMetric.total) || 0}` : null,
                trialStartsMetric ? `Trial starts: ${coerceNumber(trialStartsMetric.total) || 0}` : null,
            ].filter(Boolean),
            suggested_actions: [
                'Compare ASC commerce movement with RevenueCat/Paddle entitlement and subscription signals before changing pricing',
                'Use download source and purchase source dimensions to separate acquisition quality from paywall or product issues',
            ],
            keywords: ['asc', 'commerce', 'revenue', 'purchase', 'subscription'],
        });
    }
    if (sessionsMetric || activeDevicesMetric || installationsMetric || deletionsMetric) {
        maybePushSignal(signals, {
            id: 'asc_usage_metrics_available',
            title: 'ASC app usage metrics are available for retention checks',
            area: 'retention',
            priority: 'low',
            metric: sessionsMetric ? 'asc_sessions' : activeDevicesMetric ? 'asc_active_devices' : 'asc_usage_metrics',
            current_value: coerceNumber(sessionsMetric?.total) ||
                coerceNumber(activeDevicesMetric?.total) ||
                coerceNumber(installationsMetric?.total) ||
                coerceNumber(deletionsMetric?.total) ||
                0,
            baseline_value: null,
            delta_percent: null,
            evidence: [
                sessionsMetric ? `Sessions: ${coerceNumber(sessionsMetric.total) || 0}` : null,
                activeDevicesMetric ? `Active devices: ${coerceNumber(activeDevicesMetric.total) || 0}` : null,
                installationsMetric ? `Installations: ${coerceNumber(installationsMetric.total) || 0}` : null,
                deletionsMetric ? `Deletions: ${coerceNumber(deletionsMetric.total) || 0}` : null,
            ].filter(Boolean),
            suggested_actions: [
                'Compare ASC usage and deletion movement with AnalyticsCLI retention cohorts and first-session funnels',
                'Treat low-volume usage reports as directional because Apple applies privacy thresholds and opt-in limits',
            ],
            keywords: ['asc', 'usage', 'sessions', 'retention', 'deletions'],
        });
    }
    if (unitsMetric && coerceNumber(unitsMetric.total) !== null) {
        const units = coerceNumber(unitsMetric.total) || 0;
        const percentChange = coerceNumber(unitsMetric.percentChange);
        if (units >= 10 && percentChange !== null && percentChange <= -0.2) {
            maybePushSignal(signals, {
                id: 'asc_units_declining',
                title: 'App Store downloads are down versus the previous comparable period',
                area: 'acquisition',
                priority: percentChange <= -0.4 ? 'high' : 'medium',
                metric: 'asc_units',
                current_value: units,
                baseline_value: coerceNumber(unitsMetric.previousTotal),
                delta_percent: round(percentChange * 100),
                evidence: [
                    `Units: ${units}`,
                    `Previous units: ${coerceNumber(unitsMetric.previousTotal) ?? 'unknown'}`,
                    `Change: ${formatPercent(percentChange)}`,
                    redownloadsMetric ? `Redownloads: ${coerceNumber(redownloadsMetric.total) ?? 0}` : null,
                ].filter(Boolean),
                suggested_actions: [
                    'Compare the download drop with source traffic, store impressions, page views, ranking/search changes, and recent releases',
                    'Segment the recommendation into ASO, web/referrer, browse, or app-referrer work based on the source mix',
                ],
                keywords: ['asc', 'units', 'downloads', 'acquisition', 'sources'],
            });
        }
    }
    if (conversionRateMetric && coerceNumber(conversionRateMetric.total) !== null) {
        const conversionRate = coerceNumber(conversionRateMetric.total) || 0;
        const percentChange = coerceNumber(conversionRateMetric.percentChange);
        if (percentChange !== null && percentChange <= -0.1) {
            maybePushSignal(signals, {
                id: 'asc_conversion_rate_declining',
                title: 'App Store conversion rate is declining',
                area: 'conversion',
                priority: percentChange <= -0.25 ? 'high' : 'medium',
                metric: 'asc_conversion_rate',
                current_value: round(conversionRate),
                baseline_value: coerceNumber(conversionRateMetric.previousTotal),
                delta_percent: round(percentChange * 100),
                evidence: [
                    `Conversion rate: ${round(conversionRate)}`,
                    `Previous conversion rate: ${coerceNumber(conversionRateMetric.previousTotal) ?? 'unknown'}`,
                    `Change: ${formatPercent(percentChange)}`,
                    topSource ? `Top source by unique product page views: ${topSource.title} (${topSource.pageViewUnique})` : null,
                ].filter(Boolean),
                suggested_actions: [
                    'Review store listing screenshots, subtitle, keywords, and price/paywall promise for the source that changed most',
                    'Compare ASC conversion movement with AnalyticsCLI onboarding and paywall conversion before changing app code',
                ],
                keywords: ['asc', 'conversion', 'store_listing', 'sources', 'aso'],
            });
        }
    }
    if (topSource && totalSourcePageViews > 0) {
        const topSourceValue = topSource.pageViewUnique || topSource.impressions || topSource.units || topSource.purchases || topSource.proceeds || 0;
        const share = topSourceValue / totalSourcePageViews;
        if (share >= 0.5 || sourceBreakdown.length >= 2) {
            maybePushSignal(signals, {
                id: 'asc_source_mix_available',
                title: 'ASC source traffic is available for acquisition recommendations',
                area: 'acquisition',
                priority: share >= 0.7 ? 'medium' : 'low',
                metric: topSource.pageViewUnique ? 'asc_source_page_view_unique' : topSource.impressions ? 'asc_source_impressions' : 'asc_source_units',
                current_value: topSourceValue,
                baseline_value: totalSourcePageViews,
                delta_percent: round(share * 100),
                evidence: [
                    `Top source: ${topSource.title} (${topSourceValue} source-attributed events)`,
                    `Source mix: ${sourceBreakdown
                        .slice(0, 5)
                        .map((source) => `${source.title} ${source.pageViewUnique || source.impressions || source.units || source.purchases || source.proceeds || 0}`)
                        .join(', ')}`,
                    'ASC source dimensions may represent impressions, product page views, downloads, purchases, or proceeds depending on the downloaded report instance',
                ],
                suggested_actions: [
                    'Turn the dominant source into a specific Handlungsempfehlung: Search -> ASO/keywords, Web Referrer -> landing pages/UTMs, Browse -> creative/category positioning, App Referrer -> cross-promo/deep links',
                    'Compare source movement with units, redownloads, conversion rate, AnalyticsCLI activation, and Sentry crashes before recommending more spend or traffic',
                ],
                keywords: ['asc', 'sources', 'traffic', 'page_views', 'handlungsempfehlung'],
            });
        }
    }
    return {
        project: `app-store-connect:${appId}`,
        window: 'latest',
        signals: sortSignals(signals).slice(0, Math.max(1, Number(input?.maxSignals) || 4)),
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'asc',
            appId,
            ratingCount: ratingCount ?? 0,
            feedbackTextCount: reviewTexts.length,
            analyticsWindow: input?.analyticsWindow || null,
            analyticsAvailability,
            analyticsWarnings,
            batchReports,
            productionVersions,
            analytics: {
                impressions: metricSnapshot(impressionsMetric),
                pageViewUnique: metricSnapshot(pageViewsMetric),
                units: metricSnapshot(unitsMetric),
                redownloads: metricSnapshot(redownloadsMetric),
                conversionRate: metricSnapshot(conversionRateMetric),
                crashRate: crashRateMetric
                    ? {
                        total: coerceNumber(crashRateMetric.total) ?? 0,
                        previousTotal: coerceNumber(crashRateMetric.previousTotal),
                        percentChange: coerceNumber(crashRateMetric.percentChange),
                        nonZeroDays: nonZeroCrashRateDays,
                    }
                    : null,
                crashes: metricSnapshot(crashesMetric),
                sessions: metricSnapshot(sessionsMetric),
                activeDevices: metricSnapshot(activeDevicesMetric),
                installations: metricSnapshot(installationsMetric),
                deletions: metricSnapshot(deletionsMetric),
                purchases: metricSnapshot(purchasesMetric),
                proceeds: metricSnapshot(proceedsMetric),
                payingUsers: metricSnapshot(payingUsersMetric),
                subscriptions: metricSnapshot(subscriptionsMetric),
                trialStarts: metricSnapshot(trialStartsMetric),
                totalCrashes,
                crashBreakdown,
                sourceBreakdown,
                overviewMetricCatalog,
            },
        },
    };
}
function extractListItems(payload) {
    if (Array.isArray(payload))
        return payload;
    if (Array.isArray(payload?.items))
        return payload.items;
    if (Array.isArray(payload?.data))
        return payload.data;
    return [];
}
function displayName(value) {
    return String(value?.display_name ||
        value?.displayName ||
        value?.name ||
        value?.store_identifier ||
        value?.lookup_key ||
        value?.id ||
        '').trim();
}
function metricValueById(metrics, candidateIds) {
    const candidates = new Set(candidateIds.map((id) => String(id).toLowerCase()));
    for (const metric of metrics) {
        const id = String(metric?.id || metric?.name || '').toLowerCase();
        if (!candidates.has(id))
            continue;
        const value = coerceNumber(metric?.value);
        if (value !== null)
            return { id, value, metric };
    }
    return null;
}
function numericFromObject(value, candidateKeys = []) {
    if (!value || typeof value !== 'object')
        return null;
    for (const key of candidateKeys) {
        const direct = coerceNumber(value[key]);
        if (direct !== null)
            return direct;
    }
    return null;
}
function chartSummaryValue(payload) {
    if (!payload || typeof payload !== 'object')
        return null;
    const summary = payload.summary && typeof payload.summary === 'object' ? payload.summary : null;
    const summaryValue = numericFromObject(summary, ['total', 'average', 'value', 'count', 'rate']);
    if (summaryValue !== null)
        return summaryValue;
    const values = Array.isArray(payload.values) ? payload.values : [];
    const numericValues = [];
    walk(values, (value) => {
        const numeric = coerceNumber(value);
        if (numeric !== null)
            numericValues.push(numeric);
    });
    if (numericValues.length === 0)
        return null;
    return numericValues.reduce((total, value) => total + value, 0);
}
function revenueMetricValue(payload) {
    return numericFromObject(payload, ['value', 'revenue', 'amount', 'total']);
}
function chartDisplayName(payload, fallback) {
    return String(payload?.display_name || payload?.name || fallback || 'chart').trim();
}
function listCount(payload) {
    return extractListItems(payload).length;
}
function summarizeRevenueCatCustomers(payload) {
    const customers = extractListItems(payload);
    const byPlatform = new Map();
    const byCountry = new Map();
    let activeEntitlementCustomers = 0;
    for (const customer of customers) {
        const platform = String(customer?.last_seen_platform || customer?.platform || '').trim();
        const country = String(customer?.last_seen_country || customer?.country || '').trim();
        if (platform)
            byPlatform.set(platform, (byPlatform.get(platform) || 0) + 1);
        if (country)
            byCountry.set(country, (byCountry.get(country) || 0) + 1);
        if (extractListItems(customer?.active_entitlements || customer?.activeEntitlements).length > 0) {
            activeEntitlementCustomers += 1;
        }
    }
    const topEntries = (map) => [...map.entries()]
        .map(([key, count]) => ({ key, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 5);
    return {
        sampledCustomers: customers.length,
        activeEntitlementCustomers,
        topPlatforms: topEntries(byPlatform),
        topCountries: topEntries(byCountry),
    };
}
function buildCombinedRevenueCatSummary(input) {
    const projects = Array.isArray(input?.projects) ? input.projects : [];
    const maxSignals = Math.max(1, Number(input?.maxSignals) || 8);
    const signals = projects
        .flatMap((summary) => (Array.isArray(summary?.signals) ? summary.signals : []).map((signal) => ({
        ...signal,
        id: `${summary?.meta?.projectId || summary?.project || 'revenuecat'}:${signal.id}`,
        sourceProject: summary?.project || null,
        evidence: [`RevenueCat project: ${summary?.meta?.projectName || summary?.project || 'unknown'}`, ...(signal.evidence || [])],
        keywords: [summary?.meta?.projectId, ...(signal.keywords || [])].filter(Boolean),
    })))
        .sort((a, b) => {
        const priorityDelta = priorityRank(b.priority) - priorityRank(a.priority);
        if (priorityDelta !== 0)
            return priorityDelta;
        return Math.abs(Number(b.delta_percent) || 0) - Math.abs(Number(a.delta_percent) || 0);
    })
        .slice(0, maxSignals);
    const warnings = projects.flatMap((summary) => (Array.isArray(summary?.meta?.warnings) ? summary.meta.warnings : []).map((warning) => `${summary?.meta?.projectName || summary?.project}: ${warning}`));
    return {
        project: 'revenuecat:multiple',
        window: String(input?.window || projects[0]?.window || 'latest'),
        signals,
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'revenuecat',
            multiProject: true,
            projectCount: projects.length,
            availableProjectCount: input?.availableProjectCount || projects.length,
            availableProjectIds: Array.isArray(input?.availableProjectIds) ? input.availableProjectIds : [],
            projects: projects.map((summary) => ({
                project: summary?.project || null,
                projectId: summary?.meta?.projectId || null,
                projectName: summary?.meta?.projectName || null,
                appsCount: summary?.meta?.appsCount || 0,
                productsCount: summary?.meta?.productsCount || 0,
                offeringsCount: summary?.meta?.offeringsCount || 0,
                entitlementsCount: summary?.meta?.entitlementsCount || 0,
                paywallsCount: summary?.meta?.paywallsCount || 0,
                webhookIntegrationsCount: summary?.meta?.webhookIntegrationsCount || 0,
                sampledCustomers: summary?.meta?.customerSample?.sampledCustomers || 0,
                chartsCount: summary?.meta?.chartsCount || 0,
            })),
            warnings,
        },
    };
}
export function buildRevenueCatSummary(input) {
    if (Array.isArray(input?.projects)) {
        return buildCombinedRevenueCatSummary(input);
    }
    const projectId = String(input?.projectId || input?.project?.id || 'revenuecat-project').trim() ||
        'revenuecat-project';
    const projectName = displayName(input?.project) || projectId;
    const apps = extractListItems(input?.appsPayload);
    const products = extractListItems(input?.productsPayload);
    const offerings = extractListItems(input?.offeringsPayload);
    const entitlements = extractListItems(input?.entitlementsPayload);
    const paywalls = extractListItems(input?.paywallsPayload);
    const webhookIntegrations = extractListItems(input?.webhooksPayload);
    const customerSample = summarizeRevenueCatCustomers(input?.customersPayload);
    const metrics = Array.isArray(input?.overviewPayload?.metrics)
        ? input.overviewPayload.metrics
        : [];
    const chartsPayload = input?.chartsPayload && typeof input.chartsPayload === 'object' ? input.chartsPayload : {};
    const chartEntries = Object.entries(chartsPayload)
        .map(([name, payload]) => {
        const chartPayload = payload && typeof payload === 'object' ? payload : {};
        return {
            name,
            displayName: chartDisplayName(chartPayload, name),
            value: chartSummaryValue(chartPayload),
            category: String(chartPayload.category || '').trim() || null,
        };
    })
        .filter((entry) => entry.value !== null);
    const warnings = Array.isArray(input?.warnings) ? input.warnings.filter(Boolean) : [];
    const signals = [];
    const revenueValue = revenueMetricValue(input?.revenuePayload);
    const previousRevenueValue = revenueMetricValue(input?.previousRevenuePayload);
    if (revenueValue !== null) {
        const delta = previousRevenueValue !== null ? computeDeltaPercent(revenueValue, previousRevenueValue) : null;
        maybePushSignal(signals, {
            id: 'revenuecat_revenue_window',
            title: delta !== null && delta < -15 ? 'RevenueCat revenue dropped versus the previous period' : 'RevenueCat revenue is available for monetization analysis',
            area: delta !== null && delta < -15 ? 'retention' : 'revenue',
            priority: delta !== null && delta < -25 ? 'high' : 'medium',
            metric: 'revenuecat_revenue',
            current_value: round(revenueValue),
            baseline_value: previousRevenueValue,
            delta_percent: delta,
            evidence: [
                `Revenue ${input?.window || 'current window'}: ${round(revenueValue)}`,
                previousRevenueValue !== null ? `Previous comparable revenue: ${round(previousRevenueValue)}` : null,
                delta !== null ? `Revenue delta: ${delta}%` : null,
            ].filter(Boolean),
            suggested_actions: [
                'Compare RevenueCat revenue movement with AnalyticsCLI paywall exposure, purchase success, and activation cohorts',
                'Check whether the revenue movement started after a release, paywall, pricing, or acquisition-source change',
            ],
            keywords: ['revenuecat', 'revenue', 'mrr', 'subscription', 'paywall'],
            confidence: 'high',
        });
    }
    const revenueMetric = metricValueById(metrics, [
        'revenue',
        'mrr',
        'arr',
        'new_revenue',
        'monthly_recurring_revenue',
    ]);
    const activeTrialsMetric = metricValueById(metrics, ['active_trials']);
    const activeSubscriptionsMetric = metricValueById(metrics, ['active_subscriptions', 'actives']);
    const churnMetric = metricValueById(metrics, ['churn', 'churn_rate']);
    const refundMetric = metricValueById(metrics, ['refund_rate', 'refunds']);
    if (revenueMetric || activeSubscriptionsMetric || activeTrialsMetric) {
        maybePushSignal(signals, {
            id: 'revenuecat_overview_metrics_available',
            title: 'RevenueCat overview metrics are connected',
            area: 'revenue',
            priority: 'medium',
            metric: revenueMetric?.id ||
                activeSubscriptionsMetric?.id ||
                activeTrialsMetric?.id ||
                'revenuecat_metrics',
            current_value: revenueMetric?.value ?? activeSubscriptionsMetric?.value ?? activeTrialsMetric?.value ?? 0,
            baseline_value: null,
            delta_percent: null,
            evidence: [
                revenueMetric
                    ? `${revenueMetric.metric?.name || revenueMetric.id}: ${revenueMetric.value}`
                    : null,
                activeSubscriptionsMetric
                    ? `${activeSubscriptionsMetric.metric?.name || activeSubscriptionsMetric.id}: ${activeSubscriptionsMetric.value}`
                    : null,
                activeTrialsMetric
                    ? `${activeTrialsMetric.metric?.name || activeTrialsMetric.id}: ${activeTrialsMetric.value}`
                    : null,
            ].filter(Boolean),
            suggested_actions: [
                'Compare RevenueCat movement with AnalyticsCLI paywall and purchase funnel signals',
                'Use product and entitlement metadata to verify the paid path users see in the app',
            ],
            keywords: ['revenuecat', 'revenue', 'subscription', 'metrics'],
        });
    }
    if (churnMetric && churnMetric.value > 0) {
        maybePushSignal(signals, {
            id: 'revenuecat_churn_visible',
            title: 'RevenueCat reports churn movement',
            area: 'retention',
            priority: churnMetric.value >= 10 ? 'high' : 'medium',
            metric: churnMetric.id,
            current_value: churnMetric.value,
            baseline_value: 0,
            delta_percent: 100,
            evidence: [`${churnMetric.metric?.name || churnMetric.id}: ${churnMetric.value}`],
            suggested_actions: [
                'Inspect cancellation timing against onboarding and first-week retention signals',
                'Prioritize paywall promise and subscription value alignment if churn clusters after trial or first renewal',
            ],
            keywords: ['revenuecat', 'churn', 'subscription', 'retention'],
        });
    }
    const growthCharts = chartEntries
        .filter((entry) => ['mrr', 'actives', 'trials', 'trials_new', 'trial_conversion_rate', 'conversion_to_paying'].includes(entry.name))
        .slice(0, 6);
    if (growthCharts.length > 0) {
        maybePushSignal(signals, {
            id: 'revenuecat_growth_charts_available',
            title: 'RevenueCat subscription and trial charts are available',
            area: 'revenue',
            priority: 'medium',
            metric: 'revenuecat_chart_metrics',
            current_value: growthCharts.length,
            baseline_value: null,
            delta_percent: null,
            evidence: growthCharts.map((entry) => `${entry.displayName}: ${round(entry.value)}`),
            suggested_actions: [
                'Use trials, trial conversion, MRR, and active subscription movement to distinguish paywall conversion problems from retention/churn problems',
                'Segment the strongest movement by release, product, country, and source where RevenueCat chart options allow it',
            ],
            keywords: ['revenuecat', 'charts', 'trials', 'mrr', 'actives', 'conversion'],
            confidence: 'high',
        });
    }
    const riskCharts = chartEntries
        .filter((entry) => ['churn', 'refund_rate'].includes(entry.name) || entry.value > 0 && ['retention'].includes(entry.category || ''))
        .slice(0, 4);
    if ((refundMetric && refundMetric.value > 0) || riskCharts.length > 0) {
        maybePushSignal(signals, {
            id: 'revenuecat_churn_refund_charts_available',
            title: 'RevenueCat churn/refund context is available',
            area: 'retention',
            priority: riskCharts.some((entry) => entry.value >= 10) || (refundMetric?.value || 0) >= 10 ? 'high' : 'medium',
            metric: refundMetric?.id || riskCharts[0]?.name || 'revenuecat_retention_risk',
            current_value: refundMetric?.value ?? riskCharts[0]?.value ?? 0,
            baseline_value: 0,
            delta_percent: null,
            evidence: [
                refundMetric ? `${refundMetric.metric?.name || refundMetric.id}: ${refundMetric.value}` : null,
                ...riskCharts.map((entry) => `${entry.displayName}: ${round(entry.value)}`),
            ].filter(Boolean),
            suggested_actions: [
                'Compare churn/refund timing with first-week retention, paywall promise, onboarding completion, and support feedback',
                'Do not scale acquisition until refund/churn movement is explained for the affected cohort or product',
            ],
            keywords: ['revenuecat', 'churn', 'refund', 'retention', 'subscription'],
            confidence: 'medium',
        });
    }
    if (products.length === 0 || offerings.length === 0 || entitlements.length === 0) {
        maybePushSignal(signals, {
            id: 'revenuecat_catalog_incomplete',
            title: 'RevenueCat product catalog looks incomplete',
            area: 'paywall',
            priority: products.length === 0 || offerings.length === 0 ? 'high' : 'medium',
            metric: 'revenuecat_catalog_entities',
            current_value: products.length + offerings.length + entitlements.length,
            baseline_value: 3,
            delta_percent: computeDeltaPercent(products.length + offerings.length + entitlements.length, 3),
            evidence: [
                `Products: ${products.length}`,
                `Offerings: ${offerings.length}`,
                `Entitlements: ${entitlements.length}`,
            ],
            suggested_actions: [
                'Verify the app has at least one active product, entitlement, and offering in RevenueCat',
                'Check that App Store Connect product identifiers match the RevenueCat products used by the app',
            ],
            keywords: ['revenuecat', 'products', 'offerings', 'entitlements', 'paywall'],
        });
    }
    else {
        maybePushSignal(signals, {
            id: 'revenuecat_catalog_summary',
            title: 'RevenueCat catalog is available for monetization analysis',
            area: 'paywall',
            priority: 'low',
            metric: 'revenuecat_products',
            current_value: products.length,
            baseline_value: 1,
            delta_percent: computeDeltaPercent(products.length, 1),
            evidence: [
                `Apps: ${apps.length}`,
                `Products: ${products.slice(0, 5).map(displayName).filter(Boolean).join(', ') || products.length}`,
                `Offerings: ${offerings.slice(0, 5).map(displayName).filter(Boolean).join(', ') || offerings.length}`,
                `Entitlements: ${entitlements.slice(0, 5).map(displayName).filter(Boolean).join(', ') || entitlements.length}`,
            ],
            suggested_actions: [
                'Use this catalog context when evaluating paywall copy, package order, and entitlement naming',
                'Cross-check product availability with ASC if users report unavailable purchases',
            ],
            keywords: ['revenuecat', 'catalog', 'products', 'offerings', 'entitlements'],
        });
    }
    if (paywalls.length > 0) {
        maybePushSignal(signals, {
            id: 'revenuecat_paywalls_available',
            title: 'RevenueCat paywall configuration is available',
            area: 'paywall',
            priority: 'low',
            metric: 'revenuecat_paywalls',
            current_value: paywalls.length,
            baseline_value: 1,
            delta_percent: computeDeltaPercent(paywalls.length, 1),
            evidence: [
                `Paywalls: ${paywalls.slice(0, 5).map(displayName).filter(Boolean).join(', ') || paywalls.length}`,
                `Offerings: ${offerings.length}`,
                `Products: ${products.length}`,
            ],
            suggested_actions: [
                'Map configured paywalls to AnalyticsCLI paywall screen events before changing copy or package order',
                'Use RevenueCat paywall names as hypotheses when investigating purchase conversion and trial starts',
            ],
            keywords: ['revenuecat', 'paywall', 'offerings', 'conversion'],
            confidence: 'medium',
        });
    }
    if (webhookIntegrations.length === 0) {
        maybePushSignal(signals, {
            id: 'revenuecat_webhooks_missing',
            title: 'RevenueCat webhook integrations were not visible',
            area: 'analytics_anomaly',
            priority: 'medium',
            metric: 'revenuecat_webhook_integrations',
            current_value: 0,
            baseline_value: 1,
            delta_percent: -100,
            evidence: [
                'No RevenueCat webhook integration was returned by the API for this project.',
                'Without webhooks, local product analytics may miss renewal, cancellation, refund, and billing-state changes.',
            ],
            suggested_actions: [
                'Connect RevenueCat webhooks to the analytics backend if subscription lifecycle events are needed for churn and LTV analysis',
                'Verify renewal/cancellation/refund events appear in AnalyticsCLI before using monetization cohorts for decisions',
            ],
            keywords: ['revenuecat', 'webhooks', 'subscription_lifecycle', 'churn'],
            confidence: 'medium',
        });
    }
    if (customerSample.sampledCustomers > 0) {
        maybePushSignal(signals, {
            id: 'revenuecat_customer_sample_available',
            title: 'RevenueCat customer sample is available for monetization segmentation',
            area: 'revenue',
            priority: 'low',
            metric: 'revenuecat_sampled_customers',
            current_value: customerSample.sampledCustomers,
            baseline_value: null,
            delta_percent: null,
            evidence: [
                `Sampled customers: ${customerSample.sampledCustomers}`,
                `Customers with active entitlements in sample: ${customerSample.activeEntitlementCustomers}`,
                customerSample.topPlatforms.length > 0 ? `Top platforms: ${customerSample.topPlatforms.map((entry) => `${entry.key} ${entry.count}`).join(', ')}` : null,
                customerSample.topCountries.length > 0 ? `Top countries: ${customerSample.topCountries.map((entry) => `${entry.key} ${entry.count}`).join(', ')}` : null,
            ].filter(Boolean),
            suggested_actions: [
                'Use the customer sample only as segmentation context; rely on RevenueCat charts and AnalyticsCLI cohorts for aggregate decisions',
                'Compare platform/country monetization patterns with ASC source mix and AnalyticsCLI activation quality before changing pricing',
            ],
            keywords: ['revenuecat', 'customers', 'segmentation', 'platform', 'country'],
            confidence: 'medium',
        });
    }
    return {
        project: `revenuecat:${projectId}`,
        window: input?.window || 'latest',
        signals: sortSignals(signals).slice(0, Math.max(1, Number(input?.maxSignals) || 8)),
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'revenuecat',
            projectId,
            projectName,
            appsCount: apps.length,
            productsCount: products.length,
            offeringsCount: offerings.length,
            entitlementsCount: entitlements.length,
            paywallsCount: paywalls.length,
            webhookIntegrationsCount: webhookIntegrations.length,
            customerSample,
            metricsCount: metrics.length,
            chartsCount: Object.keys(chartsPayload).length,
            chartMetrics: chartEntries.map((entry) => ({
                name: entry.name,
                displayName: entry.displayName,
                value: entry.value,
                category: entry.category,
            })),
            revenue: revenueValue,
            previousRevenue: previousRevenueValue,
            listCounts: {
                apps: listCount(input?.appsPayload),
                products: listCount(input?.productsPayload),
                offerings: listCount(input?.offeringsPayload),
                entitlements: listCount(input?.entitlementsPayload),
                paywalls: listCount(input?.paywallsPayload),
                webhookIntegrations: listCount(input?.webhooksPayload),
                customers: listCount(input?.customersPayload),
            },
            warnings,
        },
    };
}
function metricSeries(payload) {
    if (Array.isArray(payload?.data?.timeseries))
        return payload.data.timeseries;
    if (Array.isArray(payload?.timeseries))
        return payload.timeseries;
    return [];
}
function metricCurrency(payload) {
    return String(payload?.data?.currency_code || payload?.currency_code || '').trim();
}
function metricUpdatedAt(payload) {
    return String(payload?.data?.updated_at || payload?.updated_at || '').trim();
}
function amountValue(value) {
    const numeric = coerceNumber(value);
    return numeric === null ? 0 : numeric;
}
function sumAmounts(series) {
    return series.reduce((total, point) => total + amountValue(point?.amount), 0);
}
function sumCounts(series, key = 'count') {
    return series.reduce((total, point) => total + (coerceNumber(point?.[key]) || 0), 0);
}
function firstLastNumeric(series, key) {
    const values = series
        .map((point) => coerceNumber(point?.[key]))
        .filter((value) => value !== null);
    if (values.length === 0)
        return { first: null, last: null, deltaPercent: null };
    const first = values[0];
    const last = values[values.length - 1];
    return {
        first,
        last,
        deltaPercent: computeDeltaPercent(last, first),
    };
}
function formatMinorCurrency(amount, currencyCode) {
    const currency = String(currencyCode || '').trim().toUpperCase();
    const value = amountValue(amount) / 100;
    if (!currency)
        return String(value);
    try {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(value);
    }
    catch {
        return `${value.toFixed(2)} ${currency}`;
    }
}
export function buildPaddleSummary(input) {
    if (Array.isArray(input?.accounts)) {
        return buildCombinedPaddleSummary(input);
    }
    const revenue = input?.metrics?.revenue || null;
    const mrr = input?.metrics?.monthlyRecurringRevenue || null;
    const activeSubscribers = input?.metrics?.activeSubscribers || null;
    const refunds = input?.metrics?.refunds || null;
    const chargebacks = input?.metrics?.chargebacks || null;
    const checkoutConversion = input?.metrics?.checkoutConversion || null;
    const warnings = Array.isArray(input?.warnings) ? input.warnings.filter(Boolean).map(String) : [];
    const window = String(input?.window || 'last_30d');
    const currency = metricCurrency(revenue) || metricCurrency(mrr) || metricCurrency(refunds) || '';
    const revenueSeries = metricSeries(revenue);
    const mrrSeries = metricSeries(mrr);
    const subscriberSeries = metricSeries(activeSubscribers);
    const refundSeries = metricSeries(refunds);
    const chargebackSeries = metricSeries(chargebacks);
    const checkoutSeries = metricSeries(checkoutConversion);
    const signals = [];
    const totalRevenue = sumAmounts(revenueSeries);
    const transactionCount = sumCounts(revenueSeries);
    if (revenueSeries.length > 0) {
        const midpoint = Math.floor(revenueSeries.length / 2);
        const firstHalf = sumAmounts(revenueSeries.slice(0, midpoint || revenueSeries.length));
        const secondHalf = midpoint > 0 ? sumAmounts(revenueSeries.slice(midpoint)) : totalRevenue;
        const delta = midpoint > 0 ? computeDeltaPercent(secondHalf, firstHalf) : null;
        maybePushSignal(signals, {
            id: 'paddle_revenue_trend',
            title: delta !== null && delta < -20 ? 'Paddle revenue dropped versus the prior part of the window' : 'Paddle revenue metrics are connected',
            area: 'revenue',
            priority: delta !== null && delta < -20 ? 'high' : totalRevenue > 0 ? 'medium' : 'low',
            metric: 'paddle_revenue',
            current_value: totalRevenue,
            baseline_value: firstHalf || null,
            delta_percent: delta,
            evidence: [
                `Revenue in window: ${formatMinorCurrency(totalRevenue, currency)}`,
                `Completed payment count: ${transactionCount}`,
                delta !== null ? `Recent-half revenue delta: ${delta}%` : null,
            ].filter(Boolean),
            suggested_actions: [
                'Compare Paddle revenue movement with AnalyticsCLI checkout and activation funnels',
                'Segment revenue movement by recent releases, traffic sources, and pricing page changes before changing pricing',
            ],
            keywords: ['paddle', 'revenue', 'checkout', 'billing'],
            confidence: transactionCount > 0 ? 'high' : 'medium',
        });
    }
    const mrrTrend = firstLastNumeric(mrrSeries, 'amount');
    if (mrrTrend.last !== null) {
        maybePushSignal(signals, {
            id: 'paddle_mrr_trend',
            title: mrrTrend.deltaPercent !== null && mrrTrend.deltaPercent < -10 ? 'Paddle MRR is contracting' : 'Paddle MRR is available for subscription analysis',
            area: mrrTrend.deltaPercent !== null && mrrTrend.deltaPercent < -10 ? 'retention' : 'revenue',
            priority: mrrTrend.deltaPercent !== null && mrrTrend.deltaPercent < -10 ? 'high' : 'medium',
            metric: 'paddle_mrr',
            current_value: mrrTrend.last,
            baseline_value: mrrTrend.first,
            delta_percent: mrrTrend.deltaPercent,
            evidence: [
                `MRR start: ${formatMinorCurrency(mrrTrend.first, currency)}`,
                `MRR end: ${formatMinorCurrency(mrrTrend.last, currency)}`,
                mrrTrend.deltaPercent !== null ? `MRR delta: ${mrrTrend.deltaPercent}%` : null,
            ].filter(Boolean),
            suggested_actions: [
                'Investigate churn, failed renewals, and downgrade timing before adding acquisition spend',
                'Pair MRR changes with product usage cohorts to find whether contraction follows activation or value-delivery gaps',
            ],
            keywords: ['paddle', 'mrr', 'subscription', 'retention'],
            confidence: 'high',
        });
    }
    const subscriberTrend = firstLastNumeric(subscriberSeries, 'count');
    if (subscriberTrend.last !== null) {
        maybePushSignal(signals, {
            id: 'paddle_active_subscribers_trend',
            title: subscriberTrend.deltaPercent !== null && subscriberTrend.deltaPercent < -10 ? 'Paddle active subscribers declined' : 'Paddle active subscriber count is connected',
            area: subscriberTrend.deltaPercent !== null && subscriberTrend.deltaPercent < -10 ? 'retention' : 'revenue',
            priority: subscriberTrend.deltaPercent !== null && subscriberTrend.deltaPercent < -10 ? 'high' : 'medium',
            metric: 'paddle_active_subscribers',
            current_value: subscriberTrend.last,
            baseline_value: subscriberTrend.first,
            delta_percent: subscriberTrend.deltaPercent,
            evidence: [
                `Active subscribers start: ${subscriberTrend.first}`,
                `Active subscribers end: ${subscriberTrend.last}`,
                subscriberTrend.deltaPercent !== null ? `Subscriber delta: ${subscriberTrend.deltaPercent}%` : null,
            ].filter(Boolean),
            suggested_actions: [
                'Compare subscriber movement with onboarding completion, activation, and cancellation feedback',
                'Check whether acquisition quality or pricing page changes shifted subscriber mix',
            ],
            keywords: ['paddle', 'subscribers', 'subscription', 'retention'],
            confidence: 'high',
        });
    }
    const totalRefunds = sumAmounts(refundSeries);
    const totalChargebacks = sumCounts(chargebackSeries) || sumAmounts(chargebackSeries);
    if (totalRefunds > 0 || totalChargebacks > 0) {
        maybePushSignal(signals, {
            id: 'paddle_refunds_or_chargebacks_visible',
            title: 'Paddle reports refunds or chargebacks',
            area: 'revenue',
            priority: totalChargebacks > 0 || totalRefunds >= totalRevenue * 0.1 ? 'high' : 'medium',
            metric: 'paddle_refunds_chargebacks',
            current_value: totalRefunds + totalChargebacks,
            baseline_value: 0,
            delta_percent: 100,
            evidence: [
                `Refund amount: ${formatMinorCurrency(totalRefunds, currency)}`,
                `Chargebacks/count signal: ${totalChargebacks}`,
            ],
            suggested_actions: [
                'Review refund reasons and payment disputes before scaling acquisition',
                'Compare refund timing with product promise, onboarding quality, and checkout copy',
            ],
            keywords: ['paddle', 'refunds', 'chargebacks', 'revenue'],
            confidence: 'medium',
        });
    }
    if (checkoutSeries.length > 0) {
        const latest = checkoutSeries[checkoutSeries.length - 1] || {};
        const rate = coerceNumber(latest.rate);
        const started = coerceNumber(latest.count);
        const completed = coerceNumber(latest.completed_count ?? latest.completedCount);
        if (rate !== null || started !== null || completed !== null) {
            maybePushSignal(signals, {
                id: 'paddle_checkout_conversion',
                title: rate !== null && rate < 0.05 ? 'Paddle checkout conversion is low' : 'Paddle checkout conversion is measurable',
                area: 'conversion',
                priority: rate !== null && rate < 0.05 ? 'high' : 'medium',
                metric: 'paddle_checkout_conversion',
                current_value: rate,
                baseline_value: null,
                delta_percent: null,
                evidence: [
                    rate !== null ? `Latest checkout conversion rate: ${(rate * 100).toFixed(2)}%` : null,
                    started !== null ? `Latest checkout sessions: ${started}` : null,
                    completed !== null ? `Latest completed checkouts: ${completed}` : null,
                ].filter(Boolean),
                suggested_actions: [
                    'Inspect checkout abandonment by plan, geography, and device before changing the paywall',
                    'Cross-check pricing page CTA clicks against Paddle checkout starts and completions',
                ],
                keywords: ['paddle', 'checkout', 'conversion', 'pricing'],
                confidence: 'medium',
            });
        }
    }
    if (warnings.length > 0) {
        maybePushSignal(signals, {
            id: 'paddle_api_partial_read',
            title: 'Paddle metrics summary is partial',
            area: 'general',
            priority: 'low',
            metric: 'paddle_api_warnings',
            current_value: warnings.length,
            evidence: warnings.slice(0, 8),
            suggested_actions: [
                'Verify the Paddle API key is valid for the live account metrics endpoints',
                'Keep sandbox and live keys separate; Paddle metrics endpoints are intended for live account reporting',
            ],
            keywords: ['paddle', 'api', 'metrics', 'permissions'],
            confidence: 'medium',
        });
    }
    return {
        project: 'paddle',
        window,
        metrics: input?.metrics || {},
        signals: sortSignals(signals).slice(0, Math.max(1, Number(input?.maxSignals) || 6)),
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'paddle',
            environment: input?.environment || 'live',
            accountId: input?.id || input?.accountId || null,
            accountLabel: input?.label || null,
            currencyCode: currency || null,
            updatedAt: [
                metricUpdatedAt(revenue),
                metricUpdatedAt(mrr),
                metricUpdatedAt(activeSubscribers),
                metricUpdatedAt(refunds),
                metricUpdatedAt(chargebacks),
                metricUpdatedAt(checkoutConversion),
            ].filter(Boolean)[0] || null,
            warnings,
        },
    };
}
function buildCombinedPaddleSummary(input) {
    const accounts = Array.isArray(input?.accounts) ? input.accounts : [];
    const maxSignals = Math.max(1, Number(input?.maxSignals) || 6);
    const summaries = accounts
        .filter((account) => account && typeof account === 'object')
        .map((account, index) => {
        const accountId = String(account.id || account.key || account.label || `paddle_${index + 1}`).trim();
        const label = String(account.label || accountId).trim();
        const summary = buildPaddleSummary({
            ...account,
            accounts: undefined,
            maxSignals: account.maxSignals || maxSignals,
        });
        return { accountId, label, summary };
    });
    const signals = summaries
        .flatMap(({ accountId, label, summary }) => (Array.isArray(summary.signals) ? summary.signals : []).map((signal) => ({
        ...signal,
        id: `${accountId}:${signal.id}`,
        sourceProject: summary.project,
        evidence: [`Paddle account: ${label}`, ...(signal.evidence || [])],
        keywords: [accountId, ...(signal.keywords || [])],
    })))
        .sort((a, b) => {
        const priorityDelta = priorityRank(b.priority) - priorityRank(a.priority);
        if (priorityDelta !== 0)
            return priorityDelta;
        return (Number(b.current_value) || 0) - (Number(a.current_value) || 0);
    })
        .slice(0, maxSignals);
    const warnings = summaries.flatMap(({ label, summary }) => (Array.isArray(summary.meta?.warnings) ? summary.meta.warnings : []).map((warning) => `${label}: ${warning}`));
    return {
        project: 'paddle:multiple',
        window: String(input?.window || summaries[0]?.summary?.window || 'last_30d'),
        metrics: {
            accounts: summaries.map(({ accountId, label, summary }) => ({
                id: accountId,
                label,
                environment: summary.meta?.environment || null,
                metrics: summary.metrics || {},
            })),
        },
        signals,
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'paddle',
            multiAccount: true,
            accountCount: summaries.length,
            accounts: summaries.map(({ accountId, label, summary }) => ({
                id: accountId,
                label,
                environment: summary.meta?.environment || null,
                currencyCode: summary.meta?.currencyCode || null,
                updatedAt: summary.meta?.updatedAt || null,
            })),
            warnings,
        },
    };
}
function seoNumber(value) {
    const numeric = coerceNumber(value);
    return numeric === null ? 0 : numeric;
}
function normalizeSeoRow(row) {
    const keys = Array.isArray(row?.keys) ? row.keys.map((value) => String(value || '').trim()) : [];
    const query = String(row?.query || row?.keyword || keys[0] || '').trim();
    const page = String(row?.page || row?.url || keys[1] || '').trim();
    return {
        query,
        page,
        clicks: seoNumber(row?.clicks),
        impressions: seoNumber(row?.impressions),
        ctr: coerceNumber(row?.ctr) ?? null,
        position: coerceNumber(row?.position) ?? null,
        volume: coerceNumber(row?.volume ?? row?.search_volume) ?? null,
        difficulty: coerceNumber(row?.difficulty ?? row?.keyword_difficulty ?? row?.competition_index) ?? null,
        cpc: coerceNumber(row?.cpc) ?? null,
        source: String(row?.source || 'seo').trim(),
    };
}
function seoCtr(row) {
    if (row.ctr !== null)
        return row.ctr;
    return row.impressions > 0 ? row.clicks / row.impressions : 0;
}
function seoLabel(row) {
    return [row.query, row.page].filter(Boolean).join(' -> ') || row.query || row.page || 'unknown';
}
function normalizeGscSitemapEntries(gscContext) {
    const groups = Array.isArray(gscContext?.sitemaps) ? gscContext.sitemaps : [];
    return groups.flatMap((group) => (Array.isArray(group?.sitemaps) ? group.sitemaps : []).map((sitemap) => ({
        siteUrl: String(group?.siteUrl || '').trim(),
        path: String(sitemap?.path || sitemap?.url || '').trim(),
        type: String(sitemap?.type || '').trim() || null,
        isPending: Boolean(sitemap?.isPending),
        isSitemapsIndex: Boolean(sitemap?.isSitemapsIndex),
        lastSubmitted: String(sitemap?.lastSubmitted || '').trim() || null,
        lastDownloaded: String(sitemap?.lastDownloaded || '').trim() || null,
        warnings: coerceNumber(sitemap?.warnings) || 0,
        errors: coerceNumber(sitemap?.errors) || 0,
        contents: Array.isArray(sitemap?.contents) ? sitemap.contents : [],
    })));
}
function normalizeGscInspections(gscContext) {
    const inspections = Array.isArray(gscContext?.inspections) ? gscContext.inspections : [];
    return inspections.map((entry) => {
        const indexStatus = entry?.result?.indexStatusResult || {};
        return {
            siteUrl: String(entry?.siteUrl || '').trim(),
            inspectionUrl: String(entry?.inspectionUrl || '').trim(),
            verdict: String(indexStatus?.verdict || '').trim() || null,
            coverageState: String(indexStatus?.coverageState || '').trim() || null,
            indexingState: String(indexStatus?.indexingState || '').trim() || null,
            robotsTxtState: String(indexStatus?.robotsTxtState || '').trim() || null,
            lastCrawlTime: String(indexStatus?.lastCrawlTime || '').trim() || null,
            pageFetchState: String(indexStatus?.pageFetchState || '').trim() || null,
            googleCanonical: String(indexStatus?.googleCanonical || '').trim() || null,
            userCanonical: String(indexStatus?.userCanonical || '').trim() || null,
        };
    });
}
export function buildSeoSummary(input) {
    const rows = Array.isArray(input?.rows) ? input.rows.map(normalizeSeoRow) : [];
    const keywordRows = Array.isArray(input?.keywordRows) ? input.keywordRows.map(normalizeSeoRow) : [];
    const warnings = Array.isArray(input?.warnings) ? input.warnings.filter(Boolean).map(String) : [];
    const gscSites = Array.isArray(input?.gscContext?.sites) ? input.gscContext.sites.map((site) => String(site).trim()).filter(Boolean) : [];
    const gscSitemaps = normalizeGscSitemapEntries(input?.gscContext);
    const gscInspections = normalizeGscInspections(input?.gscContext);
    const maxSignals = Math.max(1, Number(input?.maxSignals) || 8);
    const signals = [];
    const gscRows = rows.filter((row) => row.impressions > 0);
    const lowCtr = [...gscRows]
        .filter((row) => row.impressions >= 100 && seoCtr(row) < 0.02)
        .sort((a, b) => b.impressions - a.impressions)
        .slice(0, 5);
    if (lowCtr.length > 0) {
        maybePushSignal(signals, {
            id: 'seo_gsc_high_impression_low_ctr',
            title: 'Google Search Console shows high-impression queries with low CTR',
            area: 'marketing',
            priority: lowCtr.some((row) => row.impressions >= 1000) ? 'high' : 'medium',
            metric: 'gsc_low_ctr_impressions',
            current_value: lowCtr.reduce((total, row) => total + row.impressions, 0),
            baseline_value: null,
            delta_percent: null,
            evidence: lowCtr.map((row) => `${seoLabel(row)}: ${row.impressions} impressions, ${row.clicks} clicks, ${(seoCtr(row) * 100).toFixed(2)}% CTR, avg position ${row.position ?? 'n/a'}`),
            suggested_actions: [
                'Refresh title, meta description, and above-the-fold promise for the affected page/query pair',
                'Check SERP intent and make the page answer the query more directly before creating new pages',
            ],
            keywords: ['seo', 'gsc', 'ctr', 'search-console'],
            confidence: 'high',
        });
    }
    const strikingDistance = [...gscRows]
        .filter((row) => row.impressions >= 50 && row.position !== null && row.position >= 4 && row.position <= 20)
        .sort((a, b) => b.impressions - a.impressions)
        .slice(0, 5);
    if (strikingDistance.length > 0) {
        maybePushSignal(signals, {
            id: 'seo_gsc_striking_distance_queries',
            title: 'Google Search Console has striking-distance SEO opportunities',
            area: 'marketing',
            priority: strikingDistance.some((row) => row.position <= 10 && row.impressions >= 500) ? 'high' : 'medium',
            metric: 'gsc_striking_distance_impressions',
            current_value: strikingDistance.reduce((total, row) => total + row.impressions, 0),
            baseline_value: null,
            delta_percent: null,
            evidence: strikingDistance.map((row) => `${seoLabel(row)}: avg position ${row.position}, ${row.impressions} impressions, ${row.clicks} clicks`),
            suggested_actions: [
                'Improve the existing ranking URL first: intent match, internal links, comparison proof, and product-specific examples',
                'Only create a new page if the current URL cannot satisfy the query intent without cannibalization',
            ],
            keywords: ['seo', 'gsc', 'ranking', 'content-refresh'],
            confidence: 'high',
        });
    }
    const keywordOpportunities = [...keywordRows]
        .filter((row) => (row.volume || 0) >= 20)
        .sort((a, b) => (b.volume || 0) - (a.volume || 0) || (a.difficulty || 100) - (b.difficulty || 100))
        .slice(0, 5);
    if (keywordOpportunities.length > 0) {
        maybePushSignal(signals, {
            id: 'seo_keyword_research_opportunities',
            title: 'Keyword research found acquisition opportunities',
            area: 'marketing',
            priority: keywordOpportunities.some((row) => (row.volume || 0) >= 500) ? 'high' : 'medium',
            metric: 'seo_keyword_volume',
            current_value: keywordOpportunities.reduce((total, row) => total + (row.volume || 0), 0),
            baseline_value: null,
            delta_percent: null,
            evidence: keywordOpportunities.map((row) => `${row.query}: volume ${row.volume ?? 'n/a'}, difficulty ${row.difficulty ?? 'n/a'}, CPC ${row.cpc ?? 'n/a'}, source ${row.source}`),
            suggested_actions: [
                'Map each keyword to an existing URL before creating new content',
                'Prioritize BOF, comparison, integration, and template pages where the product can add unique evidence',
            ],
            keywords: ['seo', 'keyword-research', 'dataforseo', 'content'],
            confidence: keywordOpportunities.some((row) => row.source.includes('dataforseo')) ? 'high' : 'medium',
        });
    }
    const sitemapErrors = gscSitemaps.filter((sitemap) => sitemap.errors > 0 || sitemap.warnings > 0 || sitemap.isPending);
    if (gscSitemaps.length === 0 && gscSites.length > 0) {
        maybePushSignal(signals, {
            id: 'seo_gsc_no_sitemaps_visible',
            title: 'Search Console has verified properties but no visible sitemaps',
            area: 'marketing',
            priority: 'medium',
            metric: 'gsc_sitemaps',
            current_value: 0,
            baseline_value: 1,
            delta_percent: -100,
            evidence: gscSites.slice(0, 5).map((site) => `${site}: no sitemap entries returned`),
            suggested_actions: [
                'Submit the canonical sitemap or sitemap index for each public property in Search Console',
                'Verify sitemap URLs match the public canonical URLs used by the app and landing pages',
            ],
            keywords: ['seo', 'gsc', 'sitemap', 'indexing'],
            confidence: 'medium',
        });
    }
    else if (sitemapErrors.length > 0) {
        maybePushSignal(signals, {
            id: 'seo_gsc_sitemap_issues',
            title: 'Search Console sitemap status needs attention',
            area: 'marketing',
            priority: sitemapErrors.some((sitemap) => sitemap.errors > 0) ? 'high' : 'medium',
            metric: 'gsc_sitemap_errors',
            current_value: sitemapErrors.reduce((total, sitemap) => total + sitemap.errors + sitemap.warnings + (sitemap.isPending ? 1 : 0), 0),
            baseline_value: 0,
            delta_percent: 100,
            evidence: sitemapErrors.slice(0, 6).map((sitemap) => `${sitemap.siteUrl} ${sitemap.path || 'sitemap'}: errors=${sitemap.errors}, warnings=${sitemap.warnings}, pending=${sitemap.isPending}`),
            suggested_actions: [
                'Fix sitemap errors before treating low indexed-page coverage as a content or keyword problem',
                'Compare sitemap lastDownloaded/lastSubmitted dates with recent deploys and generated page changes',
            ],
            keywords: ['seo', 'gsc', 'sitemap', 'indexing', 'technical-seo'],
            confidence: 'high',
        });
    }
    const failingInspections = gscInspections.filter((inspection) => {
        const verdict = String(inspection.verdict || '').toUpperCase();
        const coverage = String(inspection.coverageState || '').toLowerCase();
        return verdict && verdict !== 'PASS' || /(not indexed|excluded|blocked|error|duplicate|alternate)/.test(coverage);
    });
    if (failingInspections.length > 0) {
        maybePushSignal(signals, {
            id: 'seo_gsc_url_inspection_issues',
            title: 'Search Console URL Inspection found indexability problems',
            area: 'marketing',
            priority: 'high',
            metric: 'gsc_url_inspection_failures',
            current_value: failingInspections.length,
            baseline_value: 0,
            delta_percent: 100,
            evidence: failingInspections.slice(0, 6).map((inspection) => `${inspection.inspectionUrl}: verdict=${inspection.verdict || 'unknown'}, coverage=${inspection.coverageState || 'unknown'}, robots=${inspection.robotsTxtState || 'unknown'}`),
            suggested_actions: [
                'Fix canonical, robots, noindex, redirect, or crawlability issues before creating more SEO pages',
                'Re-inspect only the corrected priority URLs after deploy; URL Inspection is a diagnostic sample, not a bulk indexing lever',
            ],
            keywords: ['seo', 'gsc', 'url-inspection', 'indexing', 'canonical'],
            confidence: 'high',
        });
    }
    if (gscRows.length === 0 && keywordRows.length === 0) {
        maybePushSignal(signals, {
            id: 'seo_no_search_data',
            title: 'SEO connector has no search data yet',
            area: 'marketing',
            priority: 'low',
            metric: 'seo_rows',
            current_value: 0,
            baseline_value: 1,
            delta_percent: -100,
            evidence: warnings.length > 0 ? warnings.slice(0, 5) : ['No GSC rows, keyword CSV rows, or DataForSEO rows were available.'],
            suggested_actions: [
                'Connect Google Search Console or provide a recent GSC/keyword CSV export',
                'Use DataForSEO only after narrowing seed topics and setting a paid request cap',
            ],
            keywords: ['seo', 'gsc', 'dataforseo', 'setup'],
            confidence: 'medium',
        });
    }
    if (warnings.length > 0) {
        maybePushSignal(signals, {
            id: 'seo_partial_read',
            title: 'SEO summary is partial',
            area: 'marketing',
            priority: 'low',
            metric: 'seo_warnings',
            current_value: warnings.length,
            evidence: warnings.slice(0, 8),
            suggested_actions: [
                'Fix the missing SEO credential/export only if SEO is part of the active growth cadence',
                'Prefer cached exports for repeatable analysis and bounded paid API usage',
            ],
            keywords: ['seo', 'gsc', 'dataforseo', 'credentials'],
            confidence: 'medium',
        });
    }
    return {
        project: input?.siteUrl ? `seo:${input.siteUrl}` : 'seo',
        window: input?.window || 'latest',
        rows: gscRows.slice(0, 100),
        keywordRows: keywordRows.slice(0, 100),
        signals: sortSignals(signals).slice(0, maxSignals),
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'seo',
            siteUrl: input?.siteUrl || null,
            gscRows: gscRows.length,
            gscSites,
            gscSitemaps,
            gscInspections,
            keywordRows: keywordRows.length,
            paidProvider: input?.paidProvider || null,
            warnings,
        },
    };
}
function normalizeSentryIssueCount(issue) {
    return coerceNumber(issue?.count ?? issue?.events ?? issue?.eventCount ?? issue?.stats?.sum) || 0;
}
function normalizeSentryUserCount(issue) {
    return coerceNumber(issue?.userCount ?? issue?.users ?? issue?.affectedUsers) || 0;
}
function normalizeSentryIssueTitle(issue) {
    return String(issue?.title || issue?.metadata?.title || issue?.culprit || 'Untitled Sentry issue').trim();
}
function normalizeSentryIssueUrl(issue) {
    return String(issue?.permalink ||
        issue?.issueUrl ||
        issue?.issue_url ||
        issue?.webUrl ||
        issue?.web_url ||
        issue?.links?.permalink ||
        issue?.links?.html ||
        '').trim();
}
function normalizeSentryPriority(issue) {
    const level = String(issue?.level || issue?.priority || '').toLowerCase();
    const events = normalizeSentryIssueCount(issue);
    const users = normalizeSentryUserCount(issue);
    if (level === 'fatal' || events >= 100 || users >= 25)
        return 'high';
    if (level === 'error' || events >= 20 || users >= 5)
        return 'medium';
    return 'low';
}
function normalizeSentryEvidence(issue, environment) {
    const releaseVersions = extractSentryReleaseVersions(issue);
    const issueUrl = normalizeSentryIssueUrl(issue);
    return [
        issue?.shortId ? `Sentry issue: ${issue.shortId}` : issue?.id ? `Sentry issue id: ${issue.id}` : null,
        issueUrl ? `Issue link: ${issueUrl}` : null,
        issue?.level ? `Level: ${issue.level}` : null,
        issue?.status ? `Status: ${issue.status}` : null,
        issue?.firstSeen ? `First seen: ${issue.firstSeen}` : null,
        issue?.lastSeen ? `Last seen: ${issue.lastSeen}` : null,
        environment ? `Environment: ${environment}` : null,
        releaseVersions.length > 0 ? `Release/app version: ${releaseVersions.join(', ')}` : null,
        normalizeSentryIssueCount(issue) ? `Events: ${normalizeSentryIssueCount(issue)}` : null,
        normalizeSentryUserCount(issue) ? `Affected users: ${normalizeSentryUserCount(issue)}` : null,
        issue?.culprit ? `Culprit: ${issue.culprit}` : null,
    ].filter(Boolean);
}
function extractSentryReleaseVersions(issue) {
    const values = [
        issue?.release,
        issue?.firstRelease?.version,
        issue?.firstRelease?.shortVersion,
        issue?.lastRelease?.version,
        issue?.lastRelease?.shortVersion,
        issue?.metadata?.release,
        issue?.metadata?.version,
        issue?.metadata?.appVersion,
        issue?.metadata?.['app.version'],
    ];
    if (Array.isArray(issue?.tags)) {
        for (const tag of issue.tags) {
            const key = String(tag?.key || tag?.name || '').toLowerCase();
            if (/(release|version|app\.version|dist|build)/.test(key)) {
                values.push(tag?.value);
            }
        }
    }
    if (Array.isArray(issue?.eventsPayload)) {
        for (const event of issue.eventsPayload) {
            values.push(event?.release, event?.metadata?.release, event?.metadata?.version, event?.metadata?.appVersion);
            if (Array.isArray(event?.tags)) {
                for (const tag of event.tags) {
                    const key = String(tag?.key || tag?.name || '').toLowerCase();
                    if (/(release|version|app\.version|dist|build)/.test(key)) {
                        values.push(tag?.value);
                    }
                }
            }
        }
    }
    return [...new Set(values.map(normalizeVersionToken).filter(Boolean))].sort();
}
function summarizeSentryEvents(issue) {
    const events = Array.isArray(issue?.eventsPayload) ? issue.eventsPayload : [];
    return {
        count: events.length,
        latestTimestamp: events
            .map((event) => String(event?.dateCreated || event?.timestamp || '').trim())
            .filter(Boolean)
            .sort()
            .pop() || null,
        releases: [...new Set(events.flatMap((event) => [
                event?.release,
                event?.metadata?.release,
                event?.metadata?.version,
                event?.metadata?.appVersion,
                ...(Array.isArray(event?.tags)
                    ? event.tags
                        .filter((tag) => /(release|version|app\.version|dist|build)/.test(String(tag?.key || tag?.name || '').toLowerCase()))
                        .map((tag) => tag?.value)
                    : []),
            ]).map(normalizeVersionToken).filter(Boolean))].sort(),
        urls: [...new Set(events.map((event) => String(event?.webUrl || event?.web_url || event?.url || '').trim()).filter(Boolean))].slice(0, 3),
    };
}
function buildCombinedSentrySummary(input) {
    const accounts = Array.isArray(input?.accounts) ? input.accounts : [];
    const maxSignals = Math.max(1, Number(input?.maxSignals) || 5);
    const summaries = accounts
        .filter((account) => account && typeof account === 'object')
        .map((account, index) => {
        const accountId = String(account.id || account.key || account.label || `sentry_${index + 1}`).trim();
        const label = String(account.label || accountId).trim();
        const summary = buildSentrySummary({
            ...account,
            accounts: undefined,
            maxSignals: account.maxSignals || maxSignals,
        });
        return { accountId, label, summary };
    });
    const issues = summaries.flatMap(({ accountId, label, summary }) => (Array.isArray(summary.issues) ? summary.issues : []).map((issue) => ({
        ...issue,
        id: `${accountId}:${issue.id}`,
        accountId,
        accountLabel: label,
        sourceProject: summary.project,
        app: issue.app || summary.project,
    })));
    const signals = summaries
        .flatMap(({ accountId, label, summary }) => (Array.isArray(summary.signals) ? summary.signals : []).map((signal) => ({
        ...signal,
        id: `${accountId}:${signal.id}`,
        app: signal.app || summary.project,
        sourceProject: summary.project,
        evidence: [`Sentry account: ${label}`, `Sentry project: ${summary.project}`, ...(signal.evidence || [])],
        keywords: [accountId, ...(signal.keywords || [])],
    })))
        .sort((a, b) => {
        const priorityDelta = priorityRank(b.priority) - priorityRank(a.priority);
        if (priorityDelta !== 0)
            return priorityDelta;
        return (Number(b.current_value) || 0) - (Number(a.current_value) || 0);
    })
        .slice(0, maxSignals);
    return {
        project: 'sentry:multiple',
        window: normalizeWindow(input?.last || input?.window || '24h'),
        issues,
        signals,
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'sentry',
            multiAccount: true,
            accountCount: summaries.length,
            accounts: summaries.map(({ accountId, label, summary }) => ({
                id: accountId,
                label,
                project: summary.project,
                issuesReturned: summary.meta?.issuesReturned ?? 0,
                environment: summary.meta?.environment ?? null,
            })),
            issuesReturned: issues.length,
        },
    };
}
export function buildSentrySummary(input) {
    if (Array.isArray(input?.accounts)) {
        return buildCombinedSentrySummary(input);
    }
    const issues = Array.isArray(input?.issuesPayload)
        ? input.issuesPayload
        : Array.isArray(input?.issues)
            ? input.issues
            : [];
    const org = String(input?.org || input?.organization || process.env.SENTRY_ORG || '').trim();
    const project = String(input?.project || process.env.SENTRY_PROJECT || 'sentry-project').trim();
    const environment = String(input?.environment || process.env.SENTRY_ENVIRONMENT || '').trim();
    const last = String(input?.last || input?.window || '24h');
    const maxSignals = Math.max(1, Number(input?.maxSignals) || 5);
    const normalizedIssues = issues
        .filter((issue) => issue && typeof issue === 'object')
        .map((issue, index) => {
        const releaseVersions = extractSentryReleaseVersions(issue);
        const issueUrl = normalizeSentryIssueUrl(issue);
        const eventSummary = summarizeSentryEvents(issue);
        return {
            id: String(issue.id || issue.shortId || `sentry_${index + 1}`),
            shortId: issue.shortId ? String(issue.shortId) : null,
            title: normalizeSentryIssueTitle(issue),
            priority: normalizeSentryPriority(issue),
            impact: normalizeSentryUserCount(issue) > 0
                ? `${normalizeSentryUserCount(issue)} affected users in ${last}`
                : `Production stability issue observed in ${last}`,
            events: normalizeSentryIssueCount(issue),
            users: normalizeSentryUserCount(issue),
            releaseVersions,
            sampleEvents: eventSummary.count,
            latestEventAt: eventSummary.latestTimestamp,
            area: 'crash',
            metric: 'sentry_unresolved_issues',
            sourceUrl: issueUrl || null,
            issueUrl: issueUrl || null,
            app: org ? `sentry:${org}/${project}` : `sentry:${project}`,
            stack_keywords: [
                issue.level,
                issue.type,
                issue.platform,
                issue.metadata?.type,
                issue.culprit,
                ...releaseVersions,
            ]
                .filter(Boolean)
                .map((value) => String(value).slice(0, 80)),
            evidence: [
                ...normalizeSentryEvidence(issue, environment),
                eventSummary.count > 0 ? `Sampled issue events: ${eventSummary.count}` : null,
                eventSummary.latestTimestamp ? `Latest sampled event: ${eventSummary.latestTimestamp}` : null,
                eventSummary.urls.length > 0 ? `Sample event links: ${eventSummary.urls.join(', ')}` : null,
            ].filter(Boolean),
            suggested_actions: [
                'Map this Sentry issue to the current production release and affected user journey',
                'Check whether the crash intersects onboarding, paywall, purchase, or first value events',
                'Fix or mitigate the highest-user-impact issue before running new growth experiments that send more traffic into the broken path',
            ],
            confidence: 'high',
        };
    })
        .sort((a, b) => {
        const priorityDelta = priorityRank(b.priority) - priorityRank(a.priority);
        if (priorityDelta !== 0)
            return priorityDelta;
        const usersDelta = (b.users || 0) - (a.users || 0);
        if (usersDelta !== 0)
            return usersDelta;
        return (b.events || 0) - (a.events || 0);
    })
        .slice(0, maxSignals);
    return {
        project: org ? `sentry:${org}/${project}` : `sentry:${project}`,
        window: normalizeWindow(last),
        issues: normalizedIssues,
        signals: normalizedIssues.map((issue) => ({
            id: issue.id,
            title: issue.title,
            area: issue.area,
            priority: issue.priority,
            metric: issue.metric,
            current_value: issue.events,
            releaseVersions: issue.releaseVersions,
            sampleEvents: issue.sampleEvents,
            latestEventAt: issue.latestEventAt,
            evidence: issue.evidence,
            suggested_actions: issue.suggested_actions,
            keywords: issue.stack_keywords,
            confidence: issue.confidence,
            app: issue.app,
            sourceUrl: issue.sourceUrl,
            issueUrl: issue.issueUrl,
        })),
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'sentry',
            org,
            project,
            environment: environment || null,
            issuesReturned: normalizedIssues.length,
            sampledIssueEvents: normalizedIssues.reduce((total, issue) => total + (Number(issue.sampleEvents) || 0), 0),
        },
    };
}
function normalizeCoolifyName(value, fallback) {
    const text = String(value || '').trim();
    return text || fallback;
}
function normalizeCoolifyDomains(resource) {
    const raw = resource?.domains ?? resource?.fqdn ?? resource?.domain ?? resource?.url ?? '';
    if (Array.isArray(raw))
        return raw.map((entry) => String(entry).trim()).filter(Boolean);
    return String(raw || '')
        .split(',')
        .map((entry) => entry.trim())
        .filter(Boolean);
}
function normalizeCoolifyStatus(value) {
    return String(value || '')
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9._-]+/g, '_');
}
function isCoolifyDeploymentFailed(deployment) {
    const status = normalizeCoolifyStatus(deployment?.status || deployment?.state);
    return Boolean(status && /(failed|error|cancelled|canceled|exited|unhealthy)/i.test(status));
}
function isCoolifyDeploymentRecent(deployment, sinceMs) {
    const candidates = [
        deployment?.created_at,
        deployment?.createdAt,
        deployment?.updated_at,
        deployment?.updatedAt,
        deployment?.finished_at,
        deployment?.finishedAt,
    ];
    const timestamps = candidates
        .map((value) => Date.parse(String(value || '')))
        .filter((value) => Number.isFinite(value));
    if (timestamps.length === 0)
        return true;
    return Math.max(...timestamps) >= sinceMs;
}
function isCoolifyResourceUnhealthy(resource) {
    const status = normalizeCoolifyStatus(resource?.status || resource?.state || resource?.health);
    if (!status)
        return false;
    return /(unhealthy|failed|error|exited|stopped|dead|degraded|missing)/i.test(status);
}
function coolifyResourceLabel(resource, fallback) {
    return normalizeCoolifyName(resource?.name || resource?.application_name || resource?.service_name || resource?.uuid || resource?.id, fallback);
}
export function buildCoolifySummary(input) {
    const applications = Array.isArray(input?.applications) ? input.applications : [];
    const deployments = Array.isArray(input?.deployments) ? input.deployments : [];
    const resources = Array.isArray(input?.resources) ? input.resources : [];
    const servers = Array.isArray(input?.servers) ? input.servers : [];
    const warnings = Array.isArray(input?.warnings) ? input.warnings.map((entry) => String(entry)).filter(Boolean) : [];
    const baseUrl = String(input?.baseUrl || process.env.COOLIFY_BASE_URL || '').replace(/\/$/, '');
    const last = String(input?.last || input?.window || '24h');
    const maxSignals = Math.max(1, Number(input?.maxSignals) || 8);
    const durationValue = Number(last.slice(0, -1));
    const durationMs = Number.isFinite(durationValue) && last.endsWith('d')
        ? durationValue * 24 * 60 * 60 * 1000
        : Number.isFinite(durationValue) && last.endsWith('h')
            ? durationValue * 60 * 60 * 1000
            : Number.isFinite(durationValue) && last.endsWith('m')
                ? durationValue * 60 * 1000
                : 24 * 60 * 60 * 1000;
    const sinceMs = Date.now() - durationMs;
    const signals = [];
    const failedDeployments = deployments
        .filter((deployment) => isCoolifyDeploymentFailed(deployment) && isCoolifyDeploymentRecent(deployment, sinceMs))
        .slice(0, maxSignals);
    if (failedDeployments.length > 0) {
        signals.push({
            id: 'coolify_failed_deployments',
            title: 'Coolify has recent failed deployments',
            area: 'crash',
            priority: failedDeployments.length >= 3 ? 'high' : 'medium',
            metric: 'coolify_failed_deployments',
            current_value: failedDeployments.length,
            evidence: failedDeployments.slice(0, 5).map((deployment) => {
                const app = coolifyResourceLabel(deployment, 'unknown resource');
                const status = deployment?.status || deployment?.state || 'unknown status';
                const when = deployment?.created_at || deployment?.createdAt || deployment?.finished_at || deployment?.finishedAt || '';
                return `${app}: ${status}${when ? ` at ${when}` : ''}`;
            }),
            suggested_actions: [
                'Open the failed Coolify deployment and inspect build/runtime logs before pushing more traffic to the app',
                'Correlate the failed deploy with Sentry issues, release changes, and AnalyticsCLI conversion or activation drops',
                'Fix the deployment blocker or roll back the affected service before running growth experiments',
            ],
            keywords: ['coolify', 'deployment', 'hosting', 'production'],
            confidence: 'high',
        });
    }
    const unhealthyResources = [...applications, ...resources]
        .filter((resource) => isCoolifyResourceUnhealthy(resource))
        .slice(0, maxSignals);
    if (unhealthyResources.length > 0) {
        signals.push({
            id: 'coolify_unhealthy_resources',
            title: 'Coolify reports unhealthy or stopped resources',
            area: 'crash',
            priority: 'high',
            metric: 'coolify_unhealthy_resources',
            current_value: unhealthyResources.length,
            evidence: unhealthyResources.slice(0, 8).map((resource) => {
                const name = coolifyResourceLabel(resource, 'unknown resource');
                const status = resource?.status || resource?.state || resource?.health || 'unknown status';
                const domains = normalizeCoolifyDomains(resource);
                return `${name}: ${status}${domains.length ? ` (${domains.join(', ')})` : ''}`;
            }),
            suggested_actions: [
                'Restore or restart the unhealthy Coolify resource and verify its public domain before prioritizing product-growth work',
                'Check whether Sentry error volume and AnalyticsCLI active users changed after the resource became unhealthy',
                'Add or tighten health checks for the affected service so future incidents are caught earlier',
            ],
            keywords: ['coolify', 'health', 'availability', 'hosting'],
            confidence: 'high',
        });
    }
    const publicAppsWithoutHealthChecks = applications
        .filter((app) => normalizeCoolifyDomains(app).length > 0 && app?.health_check_enabled === false)
        .slice(0, maxSignals);
    if (publicAppsWithoutHealthChecks.length > 0) {
        signals.push({
            id: 'coolify_public_apps_without_health_checks',
            title: 'Public Coolify applications are missing health checks',
            area: 'crash',
            priority: 'medium',
            metric: 'coolify_missing_health_checks',
            current_value: publicAppsWithoutHealthChecks.length,
            evidence: publicAppsWithoutHealthChecks.slice(0, 8).map((app) => {
                const name = coolifyResourceLabel(app, 'unknown application');
                return `${name}: ${normalizeCoolifyDomains(app).join(', ')}`;
            }),
            suggested_actions: [
                'Enable Coolify health checks for public production applications',
                'Use the health endpoint that best reflects the real app dependency path, not only process liveness',
                'Pair Coolify health-check alerts with Sentry and AnalyticsCLI anomaly checks in the daily guardrail',
            ],
            keywords: ['coolify', 'health_check', 'production', 'monitoring'],
            confidence: 'medium',
        });
    }
    if (warnings.length > 0) {
        signals.push({
            id: 'coolify_api_partial_read',
            title: 'Coolify API summary is partial',
            area: 'general',
            priority: 'low',
            metric: 'coolify_api_warnings',
            current_value: warnings.length,
            evidence: warnings.slice(0, 8),
            suggested_actions: [
                'Verify the Coolify API token has read-only access to the team that owns the production resources',
                'Keep the token read-only; only expand permissions if a specific API endpoint requires it',
            ],
            keywords: ['coolify', 'api', 'token', 'permissions'],
            confidence: 'medium',
        });
    }
    return {
        project: baseUrl ? `coolify:${baseUrl}` : 'coolify',
        window: normalizeWindow(last),
        applications,
        deployments,
        resources,
        servers,
        signals: signals.slice(0, maxSignals),
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'coolify',
            baseUrl: baseUrl || null,
            applicationsReturned: applications.length,
            deploymentsReturned: deployments.length,
            resourcesReturned: resources.length,
            serversReturned: servers.length,
            warnings,
        },
    };
}
export async function writeJsonOutput(outPath, payload) {
    const serialized = `${JSON.stringify(payload, null, 2)}\n`;
    if (outPath) {
        const resolved = path.resolve(String(outPath));
        await fs.mkdir(path.dirname(resolved), { recursive: true });
        await fs.writeFile(resolved, serialized, 'utf8');
        return resolved;
    }
    process.stdout.write(serialized);
    return null;
}
