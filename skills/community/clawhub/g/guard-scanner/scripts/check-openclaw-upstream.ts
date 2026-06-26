import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import fs  from 'node:fs';
import path  from 'node:path';
import {
    evaluateOpenClawBaseline,
    fetchLatestOpenClawRelease,
}  from '../src/openclaw-upstream';

const ROOT = path.join(__dirname, '..');
const PACKAGE_JSON = path.join(ROOT, 'package.json');
const OUTPUT_DIR = path.join(ROOT, 'docs', 'generated');
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'openclaw-upstream-status.json');

async function main() {
    const pkg = JSON.parse(fs.readFileSync(PACKAGE_JSON, 'utf8'));
    const pinnedVersion = pkg.devDependencies?.openclaw;
    if (!pinnedVersion) {
        throw new Error('package.json is missing devDependencies.openclaw');
    }

    const upstream = await fetchLatestOpenClawRelease();
    const result = evaluateOpenClawBaseline({
        pinnedVersion,
        latestVersion: upstream.latestVersion,
        latestPublishedAt: upstream.latestPublishedAt,
        source: upstream.source,
    });

    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    fs.writeFileSync(
        OUTPUT_FILE,
        JSON.stringify(
            {
                checkedAt: new Date().toISOString(),
                pinnedVersion,
                latestVersion: upstream.latestVersion,
                latestPublishedAt: upstream.latestPublishedAt,
                registryModifiedAt: upstream.registryModifiedAt,
                githubLatestVersion: upstream.githubLatestVersion,
                githubPublishedAt: upstream.githubPublishedAt,
                githubUrl: upstream.githubUrl,
                sourceParity: upstream.sourceParity,
                source: upstream.source,
                status: result,
            },
            null,
            2,
        ),
    );

    if (!upstream.sourceParity?.inParity) {
        console.error(
            `❌ upstream source mismatch: npm latest=${upstream.latestVersion}, GitHub latest=${upstream.githubLatestVersion}`,
        );
        process.exit(1);
    }

    if (result.behind) {
        console.error(
            `❌ upstream drift detected: pinned openclaw=${pinnedVersion}, latest=${upstream.latestVersion} (${upstream.latestPublishedAt || 'publish time unavailable'})`,
        );
        process.exit(1);
    }

    if (result.ahead) {
        console.warn(
            `⚠️ pinned openclaw=${pinnedVersion} is newer than npm latest=${upstream.latestVersion}; verify prerelease/internal baseline assumptions`,
        );
        return;
    }

    console.log(
        `✅ upstream check: pinned openclaw=${pinnedVersion} matches npm latest (${upstream.latestPublishedAt || 'publish time unavailable'})`,
    );
}

main().catch((error) => {
    console.error(`❌ upstream check failed: ${error instanceof Error ? error.stack || error.message : String(error)}`);
    process.exit(1);
});
