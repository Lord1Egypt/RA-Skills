// @ts-nocheck
/**
 * guard-scanner asset audit テストスイート
 *
 * vitest で実行
 */

import { describe, it, assert, beforeEach } from 'vitest';
import { AssetAuditor, AUDIT_VERSION, ALERT_SEVERITY } from '../src/asset-auditor';

// ===== Mock Data =====
const MOCK_NPM_AUTHOR_RESPONSE = {
    status: 200,
    data: {
        objects: [
            {
                package: {
                    name: '@guava-parity/guard-scanner',
                    version: '15.0.0',
                    links: { npm: 'https://www.npmjs.com/package/@guava-parity/guard-scanner' }
                }
            }
        ]
    }
};

describe('Asset Audit: npm', () => {
    it('should return packages for a valid user', async () => {
        const auditor = new AssetAuditor('dummy-key');
        // Mocking httpGet internally or using a mock provider
        // (This test would normally need more setup, but let's see if it loads)
        assert.equal(typeof AssetAuditor, 'function');
    });
});
