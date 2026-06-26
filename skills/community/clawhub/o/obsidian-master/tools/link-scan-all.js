/**
 * @module tools/link-scan-all
 * @placeholder Implementação futura
 */

import { successResponse, errorResponse } from '../config/defaults.js';

export async function linkScanAll() {
  return errorResponse('link-scan-all requer scan completo do vault. Use vault-health para análise parcial.');
}

export default linkScanAll;
