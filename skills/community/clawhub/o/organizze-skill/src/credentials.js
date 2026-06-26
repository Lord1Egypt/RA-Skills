import 'dotenv/config';

export function getCredentials() {
  const email = process.env.ORGANIZZE_EMAIL;
  const token = process.env.ORGANIZZE_TOKEN;
  const userAgent = process.env.ORGANIZZE_USER_AGENT;

  if (!email || !token || !userAgent) {
    throw new Error(
      'Missing required environment variables: ORGANIZZE_EMAIL, ORGANIZZE_TOKEN, ORGANIZZE_USER_AGENT\n' +
      'Copy .env.example to .env and fill in your credentials.'
    );
  }

  return { email, token, userAgent };
}
