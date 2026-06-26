import { Extension } from '../core/types';

const CognitiveExtension: Extension = {
  name: 'ext.cognitive_attestation',
  version: '1.0',

  async init(guard) {
    console.log('[JEP Guard] ext.cognitive_attestation v1.0 loaded');
  },

  async evaluate(request) {
    if (request.type === 'model_inference') {
      return { action: 'allow', rule_matched: 'cognitive_not_configured' };
    }
    return { action: 'allow', rule_matched: 'not_applicable' };
  }
};

export default CognitiveExtension;