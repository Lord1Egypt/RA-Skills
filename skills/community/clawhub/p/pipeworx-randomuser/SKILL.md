# Random User

Need realistic fake user data? This pack generates random user profiles complete with names, addresses, emails, phone numbers, photos, and more.

## How to use

**generate_users** creates one or more profiles. Optionally filter by nationality (AU, BR, CA, CH, DE, DK, ES, FI, FR, GB, IE, IN, IR, MX, NL, NO, NZ, RS, TR, UA, US).

**generate_by_gender** does the same but filtered to male or female.

```bash
curl -X POST https://gateway.pipeworx.io/randomuser/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"generate_users","arguments":{"count":3,"nationality":"us,gb"}}}'
```

Each profile includes: full name, email, username, UUID, date of birth, age, phone, cell, nationality, street address, city, state, country, postcode, and a profile picture URL.

```json
{
  "mcpServers": {
    "randomuser": {
      "url": "https://gateway.pipeworx.io/randomuser/mcp"
    }
  }
}
```
