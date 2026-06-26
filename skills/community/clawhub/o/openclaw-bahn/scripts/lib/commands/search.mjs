import { makeEnvelope, mergeMessages } from '../helpers.mjs';
import { searchStations } from '../data.mjs';

/**
 * --search <query>
 * Resolves station names via the source router.
 * Returns an Envelope with matching stations.
 */
export default async function search({ flags, positional }) {
  const query = typeof flags.search === 'string' ? flags.search : positional.join(' ');
  const envelope = makeEnvelope('search');

  if (!query) {
    envelope.errors.push('Missing search query. Usage: --search <query>');
    return envelope;
  }

  const result = await searchStations(query);
  mergeMessages(envelope, result);

  const stations = result.data;

  if (!stations.length) {
    envelope.errors.push(`Station not found: '${query}'`);
    return envelope;
  }

  // Fuzzy resolution: check for exact match (case-insensitive)
  const exactMatch = stations.some(s => s.name.toLowerCase() === query.toLowerCase());
  if (!exactMatch) {
    envelope.warnings.push(`No exact match for '${query}', using '${stations[0].name}'`);
  }

  envelope.stations = { query, results: stations };
  return envelope;
}
