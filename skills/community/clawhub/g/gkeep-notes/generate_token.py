import gpsoauth
import json

print("=== GKEEP MASTER TOKEN GENERATOR ===")
email = input("Email: ")
print("\nOption 1: App-Passwort (2FA nötig)")
print("Option 2: OAuth Token (sicherer)")
choice = input("1 oder 2? ")

aid = "android-1234567890abcdef"

if choice == "1":
    pw = input("App-Passwort (16-stellig): ")
    resp = gpsoauth.perform_master_login(email, pw, aid)
else:
    print("👉 https://accounts.google.com/EmbeddedSetup")
    print("Login → I agree → F12 → Application → Cookies → oauth_token kopieren")
    oauth = input("oauth_token: ")
    resp = gpsoauth.exchange_token(email, oauth, aid)

print("\n=== RESULT ===")
print(json.dumps(resp, indent=2))
token = resp.get('Token')
if token:
    print(f"\n✅ TOKEN: {token}")
    print(f'\nIn config.json: "token": "{token}"')
else:
    print("❌ FEHLER:", resp.get('Error'))
