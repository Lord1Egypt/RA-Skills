"use strict";
/**
 * Earned Value Management (EVM) Calculations
 * PMBOK 7th Edition — Cost Management
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_THRESHOLDS = void 0;
exports.calculateEVM = calculateEVM;
exports.calculateEAC = calculateEAC;
exports.formatEVMJson = formatEVMJson;
exports.formatEVMMarkdown = formatEVMMarkdown;
// Default thresholds from PMBOK
exports.DEFAULT_THRESHOLDS = {
    cpiCritical: 0.85,
    cpiWarning: 0.95,
    spiCritical: 0.80,
    spiWarning: 0.90,
};
/**
 * Calculate all EVM metrics
 */
function calculateEVM(input, thresholds) {
    const { bac, pv, ev, ac } = input;
    const t = { ...exports.DEFAULT_THRESHOLDS, ...thresholds };
    // Variances
    const cv = ev - ac;
    const sv = ev - pv;
    // Performance indices (avoid division by zero)
    const cpi = ac === 0 ? 0 : Number((ev / ac).toFixed(4));
    const spi = pv === 0 ? 0 : Number((ev / pv).toFixed(4));
    // Forecasting (typical variance formula)
    const eac = cpi === 0 ? ac : Number((bac / cpi).toFixed(2));
    const etc = Number((eac - ac).toFixed(2));
    const vac = Number((bac - eac).toFixed(2));
    const tcpiDenom = bac - ac;
    const tcpi = tcpiDenom === 0 ? 0 : Number(((bac - ev) / tcpiDenom).toFixed(4));
    // Percent complete
    const percentComplete = bac === 0 ? 0 : Number(((ev / bac) * 100).toFixed(1));
    // Determine status
    let status = 'GREEN';
    if (cpi < t.cpiCritical || spi < t.spiCritical) {
        status = 'RED';
    }
    else if (cpi < t.cpiWarning || spi < t.spiWarning) {
        status = 'AMBER';
    }
    // Generate interpretation
    const interpretation = generateInterpretation(cpi, spi, cv, sv);
    return {
        bac, pv, ev, ac,
        cv, sv,
        cpi, spi,
        eac, etc, vac, tcpi,
        percentComplete,
        status,
        interpretation,
    };
}
/**
 * Generate human-readable interpretation
 */
function generateInterpretation(cpi, spi, cv, sv) {
    const parts = [];
    // Cost interpretation
    if (cpi > 1.05) {
        parts.push('Under budget (cost efficient)');
    }
    else if (cpi < 0.95) {
        parts.push('Over budget (cost overrun)');
    }
    else {
        parts.push('On budget');
    }
    // Schedule interpretation
    if (spi > 1.05) {
        parts.push('ahead of schedule');
    }
    else if (spi < 0.95) {
        parts.push('behind schedule');
    }
    else {
        parts.push('on schedule');
    }
    // Variances
    if (Math.abs(cv) > 1000) {
        const cvFormatted = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(cv);
        parts.push(`Cost variance: ${cvFormatted}`);
    }
    return parts.join(', ');
}
/**
 * Calculate Estimate at Completion using different formulas
 */
function calculateEAC(bac, ac, ev, cpi, spi, method = 'typical') {
    switch (method) {
        case 'typical':
            return cpi === 0 ? ac : Number((bac / cpi).toFixed(2));
        case 'atypical':
            return Number((ac + (bac - ev)).toFixed(2));
        case 'combined':
            const combinedIndex = cpi * spi;
            return combinedIndex === 0 ? ac : Number((ac + ((bac - ev) / combinedIndex)).toFixed(2));
        default:
            throw new Error(`Unknown EAC method: ${method}`);
    }
}
/**
 * Format EVM results as JSON for CLI output
 */
function formatEVMJson(result) {
    return JSON.stringify(result, null, 2);
}
/**
 * Format EVM results as Markdown for reports
 */
function formatEVMMarkdown(result) {
    const currency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
    return `# Earned Value Dashboard

## Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| BAC | ${currency.format(result.bac)} | — |
| PV | ${currency.format(result.pv)} | — |
| EV | ${currency.format(result.ev)} | — |
| AC | ${currency.format(result.ac)} | — |
| CV | ${currency.format(result.cv)} | ${result.cv >= 0 ? '🟢' : '🔴'} |
| SV | ${currency.format(result.sv)} | ${result.sv >= 0 ? '🟢' : '🔴'} |
| CPI | ${result.cpi.toFixed(2)} | ${result.status} |
| SPI | ${result.spi.toFixed(2)} | ${result.status} |
| EAC | ${currency.format(result.eac)} | — |
| ETC | ${currency.format(result.etc)} | — |
| VAC | ${currency.format(result.vac)} | ${result.vac >= 0 ? '🟢' : '🔴'} |
| TCPI | ${result.tcpi.toFixed(2)} | — |
| % Complete | ${result.percentComplete}% | — |

## Interpretation
${result.interpretation}

## Status: ${result.status}
${result.status === 'GREEN' ? '✅ Project is on track' : result.status === 'AMBER' ? '⚠️ Project needs attention' : '🔴 Project is in trouble'}
`;
}
//# sourceMappingURL=evm.js.map