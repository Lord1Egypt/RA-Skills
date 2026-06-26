# mal-anime-tracker Skill

## Purpose
Track anime/manga lists on MyAnimeList (MAL) and receive automatic notifications via OpenClaw when new episodes are available.

## Setup
1. Set the following environment variables (e.g., in your shell configuration or `openclaw` vault):
   ```bash
   ACCESS_TOKEN=your_access_token
   REFRESH_TOKEN=your_refresh_token
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Authorization
1. Register your application on the [MyAnimeList Developer Portal](https://myanimelist.net/apiconfig).
2. Generate a `code_challenge` (12-char alphanumeric) and navigate to the MAL OAuth2 authorization URL to get your `code`.
3. Run the authorization command:
   ```bash
   python3 auth.py authorize <CLIENT_ID> <CLIENT_SECRET> <code> <code_challenge>
   ```
   This will output your tokens, which you should add to your environment.

## Features
- Monitor progress for anime you are currently watching.
- Query current anime/manga lists.
- Automatic token refresh.
- Search and manage personal MAL data.

## CLI Reference
- `python3 api.py search <query>` - Search for anime.
- `python3 api.py update <anime_id> <status>` - Update anime status (e.g., watching, completed).
- `python3 api.py delete <anime_id>` - Remove anime from list.
- `python3 api.py list-anime` - Show your anime list.
- `python3 api.py check-updates` - Check for new episodes and output updates.
- `python3 api.py refresh-auth` - Force a token refresh using your credentials.
- `python3 api.py list-manga` - Show your reading list.
- `python3 api.py search-forums <query>` - Search MAL forums.

## Automation
```bash
# Refresh token and check updates every 6 hours
0 */6 * * * python3 /path/to/skills/mal-anime-tracker/api.py refresh-auth && python3 /path/to/skills/mal-anime-tracker/api.py check-updates | xargs -I {} openclaw message send --target <CHAT_ID> --message "{}"
```
