# Recipes

Common multi-step tasks. Each recipe assumes credentials are already configured per `references/authentication.md` (Method A / B / C). Examples invoke `bash scripts/imap.sh`; substitute your alias if you set one up.

## Recipe 1 — Quick inbox check

The user asks: "any new email?" or "what's in my inbox?"

```bash
bash scripts/imap.sh --count 10
```

Then summarise the result as a short table: date, from, subject. Don't paste full bodies.

## Recipe 2 — Find a specific email and read it

The user asks: "find the email from the GitHub team about the security alert."

```bash
# Step 1 — list candidates
bash scripts/imap.sh --search "security alert" --count 20

# Step 2 — once the user picks an ID, or you pick the most plausible candidate,
# read the body
MAILID=12345
bash scripts/imap.sh "$MAILID"
```

If the search returns many results, list the top 5–10 and ask the user which one. If it returns one obvious match, read it directly and summarise.

## Recipe 3 — Save an attachment

The user asks: "download the PDF attached to that invoice email."

```bash
# Step 1 — open the message to see the attachment names
MAILID=12345
bash scripts/imap.sh "$MAILID"

# Step 2 — pull the named attachment
ATT="invoice-2026-04.pdf"
DEST="$HOME/Downloads/$ATT"
bash scripts/imap.sh "$MAILID" "$ATT" > "$DEST"

# Step 3 — verify
ls -lh "$DEST"
file "$DEST"
```

If the user didn't specify a destination, default to `~/Downloads/` (Linux/macOS). Never overwrite an existing file silently — check with `[ -e "$DEST" ]` first and append a numeric suffix if needed.

## Recipe 4 — Render an HTML email locally

The user asks: "show me the actual newsletter, not the plain text."

```bash
MAILID=12345
HTML_OUT="/tmp/mail-${MAILID}.html"
bash scripts/imap.sh --html "$MAILID" > "$HTML_OUT"
echo "Saved HTML to $HTML_OUT"

# Optionally open in a browser
xdg-open "$HTML_OUT"   # Linux
open      "$HTML_OUT"  # macOS
```

In an agent context where there's no browser, summarise the HTML in chat after stripping tags:

```bash
python3 -c "
from html.parser import HTMLParser
import sys
class T(HTMLParser):
    def __init__(self): super().__init__(); self.out=[]
    def handle_data(self,d): self.out.append(d)
p=T(); p.feed(sys.stdin.read()); print(' '.join(''.join(p.out).split())[:2000])
" < "$HTML_OUT"
```

## Recipe 5 — Archive a message as `.eml`

The user asks: "I need that email as a file I can forward / archive / re-import."

```bash
MAILID=12345
EML_OUT="$HOME/Documents/email-${MAILID}.eml"
bash scripts/imap.sh --raw "$MAILID" > "$EML_OUT"
ls -lh "$EML_OUT"
```

`.eml` is the standard portable email format — readable by Outlook, Apple Mail, Thunderbird, and most other clients.

## Recipe 6 — Periodic check (one-shot, not a daemon)

The user asks: "ping my inbox every 5 minutes for an hour."

```bash
for i in $(seq 1 12); do
  echo "--- $(date) ---"
  bash scripts/imap.sh --count 5
  sleep 300
done
```

For real persistent monitoring (cron, systemd timers), prefer `mbsync` + `notmuch` or a dedicated tool. The skill is fine for ad-hoc ticks; it's not built to be a long-running mail daemon.

## Recipe 7 — Filter today's mail by sender, locally

`myl --search` is limited to what IMAP SEARCH supports. For more complex filters, fetch a window and post-process:

```bash
bash scripts/imap.sh --search "SINCE $(date +%d-%b-%Y)" --count 100 \
  | grep -i "from.*acme.com"
```

If the server doesn't accept the `SINCE` syntax through `--search`, drop it and filter the full listing locally.

## Recipe 8 — Count unread

```bash
bash scripts/imap.sh --search "UNSEEN" --count 200 \
  | grep -c "^From:" 2>/dev/null \
  || echo "no unread (or grep pattern needs adjusting for this myl version)"
```

The exact pattern to grep depends on `myl`'s output format on the user's version — check `bash scripts/imap.sh --count 1` output once and adjust.

## Recipe 9 — Multi-account: work + Yandex personal

The user has two mailboxes — work on a custom domain, personal on Yandex — and wants to check both.

The right OpenClaw pattern is **two agents, each with its own env**: define separate skill-allowlist agents and assign different `skills.entries.imap-client.env` per agent. But for a quick CLI check inside a single shell, scope the env per subshell so the exports don't pollute the parent:

```bash
# Work
(
  export IMAP_USER='kirill@codd.tech'
  export IMAP_PASSWORD="$WORK_APP_PASSWORD"
  export IMAP_PROVIDER='auto'
  echo "=== work ==="
  bash scripts/imap.sh --count 5
)

# Personal — Yandex
(
  export IMAP_USER='kirill@yandex.ru'
  export IMAP_PASSWORD="$YANDEX_APP_PASSWORD"
  export IMAP_PROVIDER='yandex'
  echo "=== yandex ==="
  bash scripts/imap.sh --count 5
)
```

Suggest the user keep the per-account passwords in a password manager and only put them in env vars for the duration of the operation.

## Recipe 10 — Mail.ru: search across the domain group

Mail.ru gives one mailbox access to all four domain aliases (`@mail.ru`, `@bk.ru`, `@inbox.ru`, `@list.ru`) under the same account. So a single `imap-client` config covers all of them:

```bash
export IMAP_USER='your-name@mail.ru'   # primary login
export IMAP_PASSWORD="$MAILRU_APP_PASSWORD"
export IMAP_PROVIDER='mailru'

bash scripts/imap.sh --count 20         # see the latest 20 across all aliases
bash scripts/imap.sh --search "счёт"    # works in Russian
```

Note that Mail.ru's IMAP requires explicit enablement in the web UI (Settings → "Все настройки" → "Почтовые программы" → IMAP). Without that, `AUTHENTICATIONFAILED` even with a correct app password.

## Recipe 11 — One-off ad-hoc account without touching config

Sometimes the user wants to check a colleague's mailbox or a one-off support address without reconfiguring OpenClaw. Use a subshell with inline env, no persistence:

```bash
(
  read -r -p "Username: " IMAP_USER
  read -r -s -p "App password: " IMAP_PASSWORD; echo
  export IMAP_USER IMAP_PASSWORD
  export IMAP_PROVIDER='auto'
  bash scripts/imap.sh --count 5
)
# When the subshell exits, the password disappears with it.
```

The `read -s` flag suppresses echo, so the password doesn't appear on screen or in scrollback. It still ends up in process memory of the subshell — that's unavoidable for any command-line IMAP client.
