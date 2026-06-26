# IMAP Connection Configurations

## Gmail

```js
const client = new ImapFlow({
    host: 'imap.gmail.com',
    port: 993,
    secure: true,
    auth: {
        user: 'user@gmail.com',
        accessToken: 'ya29.xxxx'  // OAuth2 access token
    }
});
```

- **Auth:** Gmail requires OAuth2 (use `accessToken`) or App Passwords (use `pass` with a 16-char app password). Regular passwords are blocked.
- **Gmail extensions:** Enable X-GM-EXT-1 for labels, thread IDs, and raw search. ImapFlow detects and enables automatically.
- **IMAP must be enabled** in Gmail settings → Forwarding and POP/IMAP.

## Outlook / Hotmail / Live.com

```js
const client = new ImapFlow({
    host: 'outlook.office365.com',
    port: 993,
    secure: true,
    auth: {
        user: 'user@outlook.com',
        pass: 'password'  // Or OAuth2 accessToken
    }
});
```

- Office 365 / Exchange Online uses `outlook.office365.com`.
- Consumer Outlook/Hotmail also works with `outlook.office365.com`.
- OAuth2 is supported via `accessToken`.

## Yahoo Mail

```js
const client = new ImapFlow({
    host: 'imap.mail.yahoo.com',
    port: 993,
    secure: true,
    auth: {
        user: 'user@yahoo.com',
        pass: 'app-password'  // Use Yahoo App Password, NOT regular password
    }
});
```

- **App Password required:** Generate at Yahoo Account Security → App passwords.
- Regular passwords are blocked unless "Allow apps that use less secure sign in" is enabled (deprecated).

## iCloud Mail

```js
const client = new ImapFlow({
    host: 'imap.mail.me.com',
    port: 993,
    secure: true,
    auth: {
        user: 'user@icloud.com',
        pass: 'app-specific-password'  // Generate at appleid.apple.com
    }
});
```

- **App-specific password required** (not your Apple ID password).
- Host aliases: `imap.mail.me.com` or `p35-imap.mail.me.com` (varies by region).

## Zoho Mail

```js
const client = new ImapFlow({
    host: 'imap.zoho.com',
    port: 993,
    secure: true,
    auth: {
        user: 'user@zoho.com',
        pass: 'password'  // Or app-specific password
    }
});
```

- IMAP must be enabled in Zoho Mail settings.
- For Zoho accounts with 2FA: use app-specific passwords.

## Fastmail

```js
const client = new ImapFlow({
    host: 'imap.fastmail.com',
    port: 993,
    secure: true,
    auth: {
        user: 'user@fastmail.com',
        pass: 'app-password'  // Generate in Settings → Privacy & Security
    }
});
```

## ProtonMail (via ProtonMail Bridge)

```js
const client = new ImapFlow({
    host: '127.0.0.1',
    port: 1143,
    secure: false,
    auth: {
        user: 'bridge-username',
        pass: 'bridge-password'
    }
});
```

ProtonMail uses encrypted storage; IMAP access requires the [ProtonMail Bridge](https://proton.me/mail/bridge) app running locally.

## Generic / Custom Server

```js
const client = new ImapFlow({
    host: 'mail.example.com',
    port: 993,
    secure: true,
    auth: {
        user: 'user@example.com',
        pass: 'password'
    }
});
```

**Common ports:** 993 (IMAPS/SSL), 143 (IMAP plain, use `secure: false`).

## TLS Options

```js
const client = new ImapFlow({
    host: 'imap.example.com',
    port: 993,
    secure: true,
    tls: {
        rejectUnauthorized: false,  // Allow self-signed certs (dev only!)
        ca: fs.readFileSync('/path/to/ca.pem'),  // Custom CA
        servername: 'imap.example.com'  // SNI hostname
    },
    auth: { user: 'user', pass: 'pass' }
});
```

**Security:** Never use `rejectUnauthorized: false` in production. It disables TLS certificate validation.

## STARTTLS (Upgrade from Plain Connection)

```js
const client = new ImapFlow({
    host: 'imap.example.com',
    port: 143,
    secure: false,
    auth: { user: 'user', pass: 'pass' }
});
// ImapFlow auto-upgrades to TLS via STARTTLS if server supports it
```

When connecting on port 143 with `secure: false`, ImapFlow negotiates STARTTLS automatically.

## Proxy Support

### SOCKS Proxy

```js
const client = new ImapFlow({
    host: 'imap.example.com',
    port: 993,
    secure: true,
    proxy: {
        host: 'proxy.example.com',
        port: 1080,
        // SOCKS5 auth (optional):
        auth: { user: 'proxyuser', pass: 'proxypass' }
    },
    auth: { user: 'user', pass: 'pass' }
});
```

### HTTP CONNECT Proxy

```js
const client = new ImapFlow({
    host: 'imap.example.com',
    port: 993,
    secure: true,
    proxy: {
        host: 'proxy.example.com',
        port: 3128,
        protocol: 'http',
        auth: { user: 'proxyuser', pass: 'proxypass' }
    },
    auth: { user: 'user', pass: 'pass' }
});
```

## OAuth2 / XOAUTH2

For providers that support OAuth2 (Gmail, Outlook, Yahoo):

```js
const client = new ImapFlow({
    host: 'imap.gmail.com',
    port: 993,
    secure: true,
    auth: {
        user: 'user@gmail.com',
        accessToken: 'ya29.xxxx'  // The OAuth2 access token
    }
});
```

- Set `accessToken` in the auth object (NOT `pass`).
- ImapFlow uses SASL XOAUTH2 automatically when `accessToken` is provided.
- You are responsible for obtaining and refreshing the token; ImapFlow does not handle OAuth2 flows.