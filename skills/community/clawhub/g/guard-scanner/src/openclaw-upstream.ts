// @ts-nocheck
import https  from 'node:https';

function parseVersion(version) {
    const [stable, prerelease = ''] = String(version).split('-', 2);
    const parts = stable.split('.').map((value) => Number.parseInt(value, 10));
    while (parts.length < 3) parts.push(0);

    return {
        raw: version,
        parts,
        prerelease,
    };
}

function compareOpenClawVersions(left, right) {
    const a = parseVersion(left);
    const b = parseVersion(right);

    for (let index = 0; index < 3; index += 1) {
        if (a.parts[index] > b.parts[index]) return 1;
        if (a.parts[index] < b.parts[index]) return -1;
    }

    if (!a.prerelease && b.prerelease) return 1;
    if (a.prerelease && !b.prerelease) return -1;
    if (a.prerelease > b.prerelease) return 1;
    if (a.prerelease < b.prerelease) return -1;
    return 0;
}

function evaluateOpenClawBaseline({ pinnedVersion, latestVersion, latestPublishedAt, source }) {
    const comparison = compareOpenClawVersions(pinnedVersion, latestVersion);

    return {
        pinnedVersion,
        latestVersion,
        latestPublishedAt,
        source,
        upToDate: comparison === 0,
        ahead: comparison > 0,
        behind: comparison < 0,
    };
}

function normalizeGitHubReleaseVersion(tagName) {
    return String(tagName).replace(/^v/i, '');
}

function evaluateOpenClawSourceParity({ npmLatestVersion, githubLatestVersion }) {
    const normalizedGitHubVersion = normalizeGitHubReleaseVersion(githubLatestVersion);
    return {
        npmLatestVersion,
        githubLatestVersion: normalizedGitHubVersion,
        inParity: compareOpenClawVersions(npmLatestVersion, normalizedGitHubVersion) === 0,
    };
}

function httpGetJson(url) {
    return new Promise((resolve, reject) => {
        https
            .get(
                url,
                {
                    headers: {
                        'user-agent': 'guard-scanner-openclaw-upstream-check',
                        accept: 'application/json',
                    },
                },
                (response) => {
                    let body = '';
                    response.setEncoding('utf8');
                    response.on('data', (chunk) => {
                        body += chunk;
                    });
                    response.on('end', () => {
                        if (response.statusCode && response.statusCode >= 400) {
                            reject(new Error(`GET ${url} failed with status ${response.statusCode}`));
                            return;
                        }
                        try {
                            resolve(JSON.parse(body));
                        } catch (error) {
                            reject(error);
                        }
                    });
                },
            )
            .on('error', reject);
    });
}

async function fetchLatestOpenClawRelease(fetchJson = httpGetJson) {
    const npmMeta = await fetchJson('https://registry.npmjs.org/openclaw');
    const latestVersion = npmMeta['dist-tags']?.latest;
    if (!latestVersion) {
        throw new Error('npm registry metadata missing dist-tags.latest for openclaw');
    }

    const githubRelease = await fetchJson('https://api.github.com/repos/openclaw/openclaw/releases/latest');
    const githubLatestVersion = normalizeGitHubReleaseVersion(githubRelease.tag_name || '');
    if (!githubLatestVersion) {
        throw new Error('GitHub releases/latest missing tag_name for openclaw/openclaw');
    }

    const parity = evaluateOpenClawSourceParity({
        npmLatestVersion: latestVersion,
        githubLatestVersion,
    });

    return {
        latestVersion,
        latestPublishedAt: npmMeta.time?.[latestVersion] ?? null,
        source: 'npm',
        registryModifiedAt: npmMeta.time?.modified ?? null,
        githubLatestVersion,
        githubPublishedAt: githubRelease.published_at ?? null,
        githubUrl: githubRelease.html_url ?? null,
        sourceParity: parity,
    };
}

export { 
    compareOpenClawVersions,
    evaluateOpenClawBaseline,
    evaluateOpenClawSourceParity,
    fetchLatestOpenClawRelease,
    normalizeGitHubReleaseVersion,
 };
