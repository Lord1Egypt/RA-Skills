# Kroger Grocery — First-Time Setup

## 1. Install kroget

```bash
pipx install kroget
# or: pip install kroget
```

Requires Python 3.11+.

## 2. Register a Kroger Developer App

1. Go to [developer.kroger.com](https://developer.kroger.com)
2. Create an account
3. Create a new app:
   - Name: anything (e.g., "My Grocery Assistant")
   - Redirect URI: `http://localhost:8400/callback`
   - API Products: Cart, Locations, Products, Profile (all public/production)
4. Note your **Client ID** and **Client Secret**

## 3. Configure kroget

```bash
kroget setup --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
```

This writes `~/.kroget/config.json`. Secure it:
```bash
chmod 600 ~/.kroget/config.json
```

## 4. Find Your Store's Location ID

Search by zip code or city:
```bash
kroget products search "test" --location-id ZIP_CODE --json
```

Or use the Kroger Locations API directly:
```bash
curl -s "https://api.kroger.com/v1/locations?filter.zipCode.near=YOUR_ZIP&filter.limit=5" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

The location ID is a numeric string (e.g., `01400443`). Save it — you'll use it in every command.

## 5. Authorize Your Account (OAuth)

```bash
kroget auth login
```

This opens a browser window. Sign in with your store account (Kroger, Fred Meyer, etc.) and authorize the app. The OAuth callback stores tokens at `~/.kroget/tokens.json`.

**Headless/remote setup:** If the browser can't open (e.g., SSH session), kroget will print the authorization URL. Open it on any device, sign in, and when it redirects to `localhost:8400/callback?code=XXXX`, copy the full redirect URL. Then manually exchange the code:

```bash
curl -s -X POST 'https://api.kroger.com/v1/connect/oauth2/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -u 'CLIENT_ID:CLIENT_SECRET' \
  -d 'grant_type=authorization_code&code=AUTH_CODE&redirect_uri=http://localhost:8400/callback'
```

Save the resulting tokens to `~/.kroget/tokens.json` (chmod 600).

## 6. Verify

```bash
kroget doctor
```

Should confirm product search and cart access are working.

## 7. Test

```bash
# Search for a product
kroget products search "bananas" --location-id YOUR_STORE_ID --json

# Add to cart (test)
kroget cart add --location-id YOUR_STORE_ID --product-id 0000000004011 --quantity 1 --apply --yes
```

Check your store's app/website to confirm the item appeared in your cart.

## Troubleshooting

| Issue | Fix |
|---|---|
| `401 Unauthorized` | Token expired — run `kroget auth login` again |
| `kroget: command not found` | Ensure `~/.local/bin` is in your PATH |
| Products return empty | Check location ID is correct for your store |
| Cart add fails | Ensure you completed OAuth (step 5), not just client credentials |

## Security Notes

- `~/.kroget/config.json` contains your API credentials — restrict permissions (600)
- `~/.kroget/tokens.json` contains OAuth tokens — restrict permissions (600)
- Never commit these files to version control
- The API **cannot** place orders or process payments — checkout always requires the user
