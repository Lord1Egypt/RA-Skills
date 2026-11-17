import jcs from 'canonicalize';
export function canonicalize(obj: unknown): string {
  const result=jcs(obj);
  if (typeof result !== 'string' || Buffer.byteLength(result)>262144) throw new Error('Invalid or oversized canonical JSON');
  return result;
}
