// @ts-nocheck
import { describe, it, assert, beforeEach, afterEach, vi } from 'vitest';


import { compareOpenClawVersions,
    evaluateOpenClawBaseline,
    normalizeGitHubReleaseVersion,
    evaluateOpenClawSourceParity,
 } from '../src/openclaw-upstream';

describe('OpenClaw upstream version comparison', () => {
    it('treats a stable release as newer than an older stable release', () => {
        assert.equal(compareOpenClawVersions('2026.3.12', '2026.3.8'), 1);
    });

    it('treats a stable release as newer than the same prerelease', () => {
        assert.equal(compareOpenClawVersions('2026.3.12', '2026.3.12-beta.1'), 1);
    });

    it('treats an older stable release as behind the latest stable release', () => {
        assert.equal(compareOpenClawVersions('2026.3.8', '2026.3.12'), -1);
    });
});

describe('OpenClaw upstream baseline evaluation', () => {
    it('returns upToDate when the pinned version matches upstream', () => {
        const result = evaluateOpenClawBaseline({
            pinnedVersion: '2026.3.12',
            latestVersion: '2026.3.12',
            latestPublishedAt: '2026-03-13T00:00:00.000Z',
            source: 'npm',
        });

        assert.equal(result.upToDate, true);
        assert.equal(result.behind, false);
    });

    it('returns behind with measured delta when upstream is newer', () => {
        const result = evaluateOpenClawBaseline({
            pinnedVersion: '2026.3.8',
            latestVersion: '2026.3.12',
            latestPublishedAt: '2026-03-13T00:00:00.000Z',
            source: 'npm',
        });

        assert.equal(result.upToDate, false);
        assert.equal(result.behind, true);
        assert.equal(result.pinnedVersion, '2026.3.8');
        assert.equal(result.latestVersion, '2026.3.12');
        assert.equal(result.source, 'npm');
    });
});

describe('OpenClaw source parity evaluation', () => {
    it('normalizes GitHub release tags before comparison', () => {
        assert.equal(normalizeGitHubReleaseVersion('v2026.3.12'), '2026.3.12');
    });

    it('reports parity when npm and GitHub agree on the stable release', () => {
        const result = evaluateOpenClawSourceParity({
            npmLatestVersion: '2026.3.12',
            githubLatestVersion: 'v2026.3.12',
        });

        assert.equal(result.inParity, true);
        assert.equal(result.npmLatestVersion, '2026.3.12');
        assert.equal(result.githubLatestVersion, '2026.3.12');
    });

    it('reports mismatch when npm and GitHub disagree', () => {
        const result = evaluateOpenClawSourceParity({
            npmLatestVersion: '2026.3.12',
            githubLatestVersion: 'v2026.3.8',
        });

        assert.equal(result.inParity, false);
    });
});
