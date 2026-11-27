# Setting up localhost.run

Walk the user through these steps when the skill isn't set up, and also when a saved setup stops working: `start` says the key was refused, or that it needs setup. At the end, `tunnel verify` has connected to the user's domain with the skill's key and saved the domain, and `tunnel start` just works.

Users who set up with an older version of this skill will land here: it used a key in `~/.ssh`, and now only uses its own. If so, tell them in one line that the skill now keeps its own key, and that their domain stays the same.

Ask one question at a time, and wait for the user where a step happens in their browser.

If the user says partway through that they'd rather not set up an account, that's their call: `tunnel start <port> --temporary` gives them a temporary address (see "A temporary address" in `SKILL.md`). They can come back to this guide any time.

## 1. The skill's key

The skill signs in with a key of its own, kept apart from the user's SSH keys. Step 3 adds it to their account.

```
tunnel key
```

The first time, this creates `~/.local/share/localhost-run/id_ed25519` (and `.pub`). After that it just shows the key. Tell the user in one line: it's a key just for localhost.run, it unlocks nothing else, and they can remove it from their account at https://admin.localhost.run/ at any time.

It has no passphrase, because an agent can't type one. That's why it's a separate key: it gives access to this user's localhost.run tunnels and nothing more.

The skill only ever uses this key. Don't look in `~/.ssh` or offer the user's other keys: the script has no option for another key. If the user asks to use one of their own, explain that the skill keeps its own key so it never touches theirs.

Never show, copy or move a private key. Only `.pub` files are shared.

## 2. A domain

If `tunnel config` shows a saved domain, ask: **"Shall I keep using `<domain>`?"** If yes, go to step 3 with it.

Otherwise, ask: **"Do you already have a domain you'd like to use, either your own or one on your localhost.run account? Or shall I give you a link to set one up?"**

- **They have one:** ask for it exactly, e.g. `dev.example.com`, and go to step 3. It doesn't need to be set up on localhost.run yet: if it isn't, step 3 gives them a link to the page that does it, including the DNS record their own domain needs.
- **They'd like to set one up:** give them https://admin.localhost.run/domains/add to open in their browser. Explain that they'll sign in or create an account there, and choose either a domain localhost.run provides (no DNS to set up, the quickest) or their own. The page may offer plans; that's their choice. Ask them to come back and tell you the domain once it's set up, exactly as the admin site shows it. Then go to step 3 with it.

  Tell them now that there'll be one more link after this, to connect this skill to their account, so it doesn't come as a surprise.

https://localhost.run/docs/custom-domains explains how custom domains work, if they ask.

## 3. Connect

```
tunnel verify --domain <domain>
```

This connects to the domain with the skill's key. If something needs fixing, it says what, and usually prints a `link:` to the page in the user's localhost.run account that fixes it. Give the user the link, wait for them to say they're done, then run `tunnel verify` again. Repeat until it exits 0. Usually that's at most two links: one for the key, then one for the domain.

| Exit | Result | What to do |
|---|---|---|
| 0 | Connected: the key signs in and the domain is on the account. The domain is saved. | Done. Offer to start a tunnel. |
| 3, with `link:` | The skill's key isn't on a localhost.run account. | Give the user the link and the `fingerprint:`, for example: "Open this link to connect this skill to your localhost.run account. Sign in (or create an account), check the page shows this fingerprint, `SHA256:…`, and approve." It adds the skill's SSH key to the account they're signed in to, so it must be **their own**. |
| 3, no link | The same, and localhost.run gave no link. | Show the user the contents of `~/.local/share/localhost-run/id_ed25519.pub` (the public key only) to add at https://admin.localhost.run/. |
| 2, with `link:` | The domain isn't ready on the account: it isn't on it yet, or (for their own domain) something such as its DNS record needs fixing. | Show the `denied:` message and the link. Say it opens a page in their own account to add or fix the domain; the page may offer plans, and that's their choice. |
| 2, no link | Denied, and it's not something a page fixes: often a misspelling, or a domain on another account. | Show the message. Check the spelling, or ask for another domain. |
| 4 | No answer. | Check the network, then try again. |
| 5 | Host key mismatch. | Stop, and tell the user, as in the rules in `SKILL.md`. |

- **Run `verify` again only when the user says they're done,** never in a loop while waiting. localhost.run takes up to about 30 s to see a change; `verify` waits that out by itself.
- **Still the same answer after they say they're done:** ask them to check they finished on the page (approved the key, or added the domain). A denial's `signed in as:` line is the account the skill's key is on: if they added the domain on a different account, tell them so plainly, by name. They can add the domain on the key's account, or approve the key on the other one.
- **The links are only for this user, in their own browser.** Approving a key link adds the key to whichever account is signed in. Never send a link to anyone else, never open one yourself, and only ever use links `tunnel` printed (see the rules in `SKILL.md`).

If the user set up with an older version, they can remove its old key from their account at https://admin.localhost.run/ once this works.

The domain is saved to `~/.config/localhost-run/agent.conf`. The key itself stays in `~/.local/share/localhost-run/`, never in `~/.config`, which people often sync to dotfiles repos. They're for this user, not the project, so every project uses the same domain unless `--domain` says otherwise.
