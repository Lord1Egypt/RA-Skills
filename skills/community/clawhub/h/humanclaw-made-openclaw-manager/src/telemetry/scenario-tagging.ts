import { SessionRecord } from '../types';

export const deriveScenarioSignature = (session: SessionRecord, closureType = 'completed') => {
  const source = `${session.tags.join(' ')} ${session.title} ${session.objective} ${closureType}`.toLowerCase();
  const normalized = source
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, ' ')
    .trim()
    .split(/\s+/)
    .slice(0, 8)
    .join('-');
  return normalized || 'general-work';
};

