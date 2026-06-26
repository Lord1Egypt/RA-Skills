import { Extension } from '../core/types';

const HardwareTrustExtension: Extension = {
  name: 'ext.hardware_trust',
  version: '1.0',

  async init(guard) {
    const fs = require('fs');
    const hasTEE = fs.existsSync('/dev/tdx-guest') || fs.existsSync('/dev/sev');
    console.log(`[JEP Guard] ext.hardware_trust v1.0 ${hasTEE ? 'TEE detected' : 'software mode'}`);
  },

  async evaluate(request) {
    return { action: 'allow', rule_matched: 'hardware_trust_available' };
  }
};

export default HardwareTrustExtension;