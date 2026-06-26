/**
 * Configuration for Knitify API skill.
 * Reads environment variables declared in SKILL.md config,
 * set by the user via `openclaw config set`.
 */
module.exports = {
  apiKey: process.env.KNITIFY_API_KEY || '',
  apiUrl: process.env.KNITIFY_API_URL || 'https://knitify.innovohealthlabs.com',
};
