import { Extension } from '../core/types';

const AEGISExtension: Extension = {
  name: 'ext.aegis',
  version: '1.0',

  async init(guard) {
    const hasAEGIS = !!globalThis.aegisKernel || process.env.AEGIS_ENABLED === '1';
    console.log(`[JEP Guard] ext.aegis v1.0 ${hasAEGIS ? 'active' : 'inactive'}`);
  },

  async evaluate(request) {
    if (globalThis.aegisKernel?.evaluate) {
      const result = await globalThis.aegisKernel.evaluate({
        action: request.action,
        target: request.target,
        context: request.context
      });
      if (result.decision === 'block') {
        return {
          action: 'block',
          rule_matched: `aegis:${result.ruleId}`,
          metadata: {
            policy_anchor: result.policyHash,
            tee_quote: result.teeQuote
          }
        };
      }
    }
    return { action: 'allow', rule_matched: 'aegis_not_present' };
  },

  async onEvent(event) {
    if (globalThis.aegisKernel?.audit) {
      await globalThis.aegisKernel.audit({
        type: event.verb,
        timestamp: event.when,
        hash: event.what
      });
    }
  }
};

export default AEGISExtension;