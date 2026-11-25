# Setting up localhost.run

Walk the user through these steps when the skill isn't set up, and also when a saved setup stops working: `start` says the key was refused, or that it needs setup. At the end, `tunnel verify` has checked the key and domain and saved the domain, and `tunnel start` just works.

Users who set up with an older version of this skill will land here: it used a key in `~/.ssh`, and now only uses its own. If so, tell them in one line that the skill now keeps its own key, and that their domain stays the same.

Ask one question at a time, and wait for the user where a step happens in their browser.

If the user says partway through that they'd rather not set up an account, that's their call: `tunnel start <port> --temporary` gives them a temporary address (see "A temporary address" in `SKILL.md`). They can come back to this guide any time.

## 1. The skill's key

The skill signs in with a key of its own, kept apart from the user's SSH keys. The quickstart link in step 2 adds it to their account.

```
tunnel key
```

The first time, this creates `~/.local/share/localhost-run/id_ed25519` (and `.pub`). After that it just shows the key. Tell the user in one line: it's a key just for localhost.run, it unlocks nothing else, and they can remove it from their account at https://admin.localhost.run/ at any time.

It has no passphrase, because an agent can't type one. That's why it's a separate key: it gives access to this user's localhost.run tunnels and nothing more.

The skill only ever uses this key. Don't look in `~/.ssh` or offer the user's other keys: the script has no option for another key. If the user asks to use one of their own, explain that the skill keeps its own key so it never touches theirs.

Never show, copy or move a private key. Only `.pub` files are shared.

## 2. A domain

If `tunnel config` shows a saved domain, ask: **"Shall I keep using `<domain>`?"** If yes, it's an existing domain: go to the **Yes** case below with it. If no, ask the question below.

Otherwise, ask: **"Do you already have a domain on localhost.run?"**

- **No (the quickstart):** a **managed domain**. localhost.run provides it, so there's no DNS to set up.
  1. Ask what name they'd like: short, lowercase letters, digits and hyphens (e.g. their name or the project's).
  2. Make the link, which carries the name and the key's public half:
     ```
     tunnel claim-url <name>
     ```
  3. Give the user the link to open in their browser. Explain that they'll sign in or create an account there, choose a plan if they need one, and claim the domain; the key is added to their account at the same time. Opening it again is harmless.
  4. Ask them to come back with the domain they ended up with, exactly as the admin site shows it.
- **Yes:** ask for it, exactly as it appears at https://admin.localhost.run/. This includes custom domains the user has already set up there (their own domain, with DNS done). The skill's key won't be on their account yet: step 3 will say so, and you can then show them the contents of `~/.local/share/localhost-run/id_ed25519.pub` to paste into their account at https://admin.localhost.run/.

Don't offer to set up a custom domain from scratch here. It needs DNS changes, and the user does it in the admin site. If they ask, point them to https://localhost.run/docs/custom-domains, and come back to this step once it's done.

## 3. Verify and save

```
tunnel verify --domain <domain>
```

| Exit | Result | What to do |
|---|---|---|
| 0 | It signed in, the domain is on the account, and it's saved. | Done. Offer to start a tunnel. |
| 3 | Key refused: the key isn't on any localhost.run account. | Quickstart: check the claim finished in the browser. Existing domain: have the user add the `.pub` file's contents at https://admin.localhost.run/. Then verify again. |
| 2 | Denied: the key signed in, but the domain isn't on that account. | Show the message. Check the spelling, that the claim finished, and that it's the same account the key is on. |
| 4 | No answer. | Check the network, then try again. |
| 5 | Host key mismatch. | Stop, and tell the user, as in the rules in `SKILL.md`. |

If the user set up with an older version, they can remove its old key from their account at https://admin.localhost.run/ once this works.

The domain is saved to `~/.config/localhost-run/agent.conf`. The key itself stays in `~/.local/share/localhost-run/`, never in `~/.config`, which people often sync to dotfiles repos. They're for this user, not the project, so every project uses the same domain unless `--domain` says otherwise.
