# Setup

This is the click-by-click version. It assumes you have never opened Google Cloud Console
and do not want to learn it. Every button name and every URL below is exact. Follow it in
order and it takes about ten minutes.

**You may not need this document.** The agent can drive the whole thing in conversation:
say "use open-ga4 to set up my analytics" and it runs `doctor --json`, which reports one
blocking step at a time and hands you the link and the exact string to paste for each.

Name the skill rather than saying only "set up my analytics". Two reasons. A generic phrase
can pull in whichever skill happens to match, and you want this one. And `doctor` is a real
check, not a menu: it reads your local configuration and the credential file to work out
which step is missing, so it should run when you decide it runs. It prints which step is
missing and never prints the credential itself.

This file is here for anyone who would rather read the steps themselves, and as the
reference when a step does not behave.

You will do work in two different Google products. They look related. They are not:

- **Google Cloud Console**: where you create a robot account and switch on two APIs.
- **Google Analytics**: where you grant that robot account permission to read your data.

Doing one and not the other is the single most common reason this skill does not work.

---

## Before you start

You need three things.

| You need | How to check |
| --- | --- |
| A **GA4 property** that is collecting data | Open <https://analytics.google.com> and confirm you see reports with numbers in them. |
| A Google account with **Editor** or **Administrator** on that property | In Analytics, click the gear icon (**Admin**), then **Property access management**. If you can open that screen and see the blue **+** button, you have enough access. If the screen is missing or read-only, ask whoever owns the property to do steps 5 and 6 for you. |
| Permission to create a **Google Cloud project** | Most personal Google accounts can. Some company-managed accounts cannot. You will find out in step 1: if the **Create** button is greyed out or you see "Your organisation does not allow this", ask your IT administrator to create a project and give you the Editor role on it. |

You do not need a credit card. Everything here is free. The Google Analytics Data API has
no charge, only a usage quota.

---

## Step 1. Create a Google Cloud project

1. Open <https://console.cloud.google.com/projectcreate>
2. In **Project name**, type: `openclaw-ga4`
3. Look at the grey line just underneath the name box. It reads **Project ID:** followed by
   something like `openclaw-ga4-123456`. **Write that project ID down.** It is usually *not*
   the same as the project name (Google appends digits when the name is already taken)
   and it is the string that appears in error messages later.
4. Leave **Location** as it is (`No organisation` is fine).
5. Click **Create**.
6. Wait for the notification bell to say the project is ready, then check the **project
   picker**, the dropdown in the dark bar at the top of the page, immediately right of the
   Google Cloud logo. It must say **openclaw-ga4**. If it says anything else, click it and
   select `openclaw-ga4`.

Everything in steps 2 and 3 happens inside this project. If the project picker ever shows a
different name, you are configuring the wrong project.

---

## Step 2. Turn on two APIs

**These are two separate switches.** Enabling one does not enable the other. There is no
"Analytics" master switch. People routinely enable the first, get a working report, and are
then confused when listing properties fails; that is the second switch.

### 2a. Google Analytics Data API

1. Open <https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com>
2. Check the project picker at the top says **openclaw-ga4**. If it does not, click it and
   choose that project, then reload the page.
3. Click the blue **Enable** button.
4. Wait until the page changes to show **API Enabled** with a **Manage** button. That is the
   confirmation. It takes a few seconds.

This is the API that runs reports. Without it, nothing works.

### 2b. Google Analytics Admin API

1. Open <https://console.cloud.google.com/apis/library/analyticsadmin.googleapis.com>
2. Check the project picker **again**. It resets more often than you would expect.
3. Click **Enable**.
4. Wait for **API Enabled**.

This is the API that lists which properties your credential can reach, by name. Reports
still run without it, but `properties` will return nothing, `doctor` will report a failure
on the property-listing check, and you will have to type property IDs from memory. Turn it
on.

Give both about a minute to propagate before you test. A freshly enabled API sometimes
returns "not enabled" for the first few requests.

---

## Step 3. Create a service account

A service account is a robot Google account with its own email address. It is what the
skill logs in as, so that it never touches your personal Google login.

1. Open <https://console.cloud.google.com/iam-admin/serviceaccounts/create>
2. Confirm the project picker says **openclaw-ga4**.
3. **Service account name:** type `ga4-reader`
4. The **Service account ID** field fills itself in as `ga4-reader`. Leave it.
5. Under it you will see the full email address being built, something like
   `ga4-reader@openclaw-ga4-123456.iam.gserviceaccount.com`. **Copy that address somewhere
   you can find it.** You need it in step 5, and step 5 is the one everybody gets wrong.
6. Click **Create and continue**.
7. The next panel is **Grant this service account access to project (optional)**. Click
   **Continue** without picking a role.

   This looks wrong and is correct. Google Cloud roles have no effect on Google Analytics
   access. Adding "Viewer" or "Owner" here grants nothing useful and does not substitute for
   step 5. Leave it empty.
8. The last panel is **Grant users access to this service account (optional)**. Click
   **Done**.

You are now back on the service accounts list, with `ga4-reader` in it.

---

## Step 4. Create a JSON key and lock the file down

1. On the service accounts list, click the row for
   **`ga4-reader@openclaw-ga4-123456.iam.gserviceaccount.com`**.
2. Click the **Keys** tab.
3. Click **Add key** → **Create new key**.
4. Select **JSON** (it is the default) and click **Create**.
5. A file downloads, something like `openclaw-ga4-123456-a1b2c3d4e5f6.json`. Google shows a
   dialog saying the private key was saved to your computer. Click **Close**.

**Treat that file as a password.** Anyone who has it can read your analytics data as this
service account, from anywhere, until you delete the key in the console. Google will not
show it to you again; if you lose it, create a new key and delete the old one.

You will hand this key to the skill in step 7, in one of two forms: the file's **contents**,
pasted into a box, or a **path** to where you saved it. Pasting is fewer steps and is what
the Control UI's field is for; a path keeps the key in exactly one place on disk. Step 7
states the trade-off in full. If you intend to paste, you can skip straight there and come
back to this only if you change your mind.

For the path form, move the file somewhere private and take away everyone else's read
access:

```bash
mkdir -p ~/.openclaw/credentials
mv ~/Downloads/openclaw-ga4-*.json ~/.openclaw/credentials/ga4.json
chmod 600 ~/.openclaw/credentials/ga4.json
```

`chmod 600` means "only my user account may read or write this file". Without it, every
other account on the machine can read your key. Confirm it worked:

```bash
ls -l ~/.openclaw/credentials/ga4.json
# -rw------- 1 you you 2381 Aug 14 10:22 /home/you/.openclaw/credentials/ga4.json
```

The leading `-rw-------` is what you want. If you see `-rw-r--r--`, the `chmod` did not run.

<details>
<summary>Windows equivalent</summary>

```powershell
mkdir "$env:USERPROFILE\.openclaw\credentials" -Force
move "$env:USERPROFILE\Downloads\openclaw-ga4-*.json" "$env:USERPROFILE\.openclaw\credentials\ga4.json"
icacls "$env:USERPROFILE\.openclaw\credentials\ga4.json" /inheritance:r /grant:r "$($env:USERNAME):(R,W)"
```

</details>

While you are in the file, open it in a text editor and find the line beginning
`"client_email":`. That value is the address you copied in step 3. It is what step 5 needs.
Do not copy anything else out of this file; in particular `private_key` is the secret
itself.

---

## Step 5. Give the service account access **inside Google Analytics**

This is the step everyone gets wrong, so it gets its own explanation.

**Google Cloud access and Google Analytics access are unrelated systems.** They are both
Google, they both have the word "access", and they share your login, but a permission
granted in one is invisible to the other. Creating the service account in Cloud gives it an
identity and nothing else. It currently has permission to read exactly zero analytics
properties. You grant that permission in Google Analytics, by hand, once per property.

Skipping this step produces a `403` from Google that says only "user does not have
sufficient permissions", with no hint about which user, which property, or where to fix it.

1. Copy the service account address. It is in your key file as `client_email`, and on the
   service account page in Cloud:
   **`ga4-reader@openclaw-ga4-123456.iam.gserviceaccount.com`**
2. Open <https://analytics.google.com>
3. Click the **gear icon** at the bottom of the left-hand sidebar. It is labelled **Admin**.
4. Make sure the **Property** selector at the top of the Admin page shows the property you
   want the agent to read. If you have several, this matters: the grant is per property.
5. In the **Property** column, click **Property access management**. (In the newer Admin
   layout the same link sits under **Property settings** in the left-hand list.)
6. Click the blue **+** button at the top right, then **Add users**.
7. In **Email addresses**, paste
   `ga4-reader@openclaw-ga4-123456.iam.gserviceaccount.com`
8. **Untick "Notify new users by email".** A service account has no inbox; leaving it ticked
   generates a bounce.
9. Under **Direct roles and data restrictions**, select **Viewer**. Select nothing else. Not
   Editor, not Marketer, not Analyst, not Administrator. This skill only reads, and a
   credential that can write is a credential that can be made to write.
10. Click **Add** at the top right.

The service account now appears in the access list with the role Viewer. Repeat steps 4–10
for every property you want the agent to be able to read.

---

## Step 6. Find your property ID

1. Still in **Admin**, in the **Property** column, click **Property details** (older
   interfaces label this **Property Settings**).
2. At the top right you will see **PROPERTY ID** and a number, 9 or 10 digits, such as
   `123456789`. That is what you need.

The property ID is also in the URL of any Analytics report, as the part that looks like
`p123456789`.

**It is not the `G-XXXXXXXXXX` measurement ID.** The measurement ID is the string in your
website's tracking tag, it identifies a data stream rather than a property, and the
reporting API cannot use it. It is the string most people have in front of them, which is
why the skill detects it specifically and tells you where the right number is instead of
returning an unexplained error.

---

## Step 7. Point the skill at the key

Two settings, both environment variables. There is no configuration file to edit.

| Variable | Value |
| --- | --- |
| `GA4_CREDENTIALS` | The key file's contents, pasted, **or** a path to where you saved it. |
| `GA4_PROPERTY_ID` | The numeric property ID from step 6. Optional, but without it you get asked which site every time. |

### The easy way: the field in OpenClaw

The skill declares `GA4_CREDENTIALS` as its primary environment variable, which is what
gives it a labelled box in OpenClaw's own interface rather than a config file you have to
find. Open the skill's settings, paste the whole contents of the key file into that box,
and put the property ID in the `GA4_PROPERTY_ID` field beside it. That is the entire step.

### The other way: your shell

```bash
export GA4_CREDENTIALS=~/.openclaw/credentials/ga4.json
export GA4_PROPERTY_ID=123456789
```

Put those lines in your shell profile (`~/.bashrc`, `~/.zshrc`) so they survive a reboot,
and make sure they are set in the environment **OpenClaw itself** runs in; a variable
exported in a terminal is not visible to an app launched from a desktop icon.

### Contents or path: which to use

`GA4_CREDENTIALS` accepts both, and tells them apart by whether the value starts with `{`.

| The value looks like | Read as |
| --- | --- |
| `{"type":"service_account",...}` | The key's contents |
| `/home/you/key.json` or `~/key.json` | A path to the key file |

Pasting the contents is one action instead of three (move the file, `chmod` it, type the
path correctly), which is why it is the default advice. The cost, stated rather than
buried: the key then lives inside `~/.openclaw/openclaw.json`, and OpenClaw writes a `.bak`
beside that file on every change, so it comes to rest in two places rather than one. If
that matters to you, use the path form; step 4 already locked the file down.

If you paste a key where a path was expected, or the other way round, the skill says so
without ever echoing the value back at you.

### Where the skill looks, in order

The first source that yields a usable credential wins. Later sources are not consulted.

| Order | Source |
| --- | --- |
| 1 | `GA4_CREDENTIALS`, when it starts with `{`: the key's contents, read directly |
| 2 | `GA4_CREDENTIALS`, otherwise: the file at that path |
| 3 | `GOOGLE_APPLICATION_CREDENTIALS`: Google's standard variable, so an existing gcloud or migrated setup keeps working |
| 4 | `~/.config/gcloud/application_default_credentials.json`: whatever `gcloud auth application-default login` last wrote |

Two consequences worth knowing.

**A pasted key that does not parse stops the search.** If `GA4_CREDENTIALS` starts with `{`
and is not valid service-account JSON, the skill reports that and does not try the other
sources. Somebody who pasted a key and got it wrong needs to hear that the key is wrong,
not that gcloud credentials are also absent.

**A stale path does not.** If a path in `GA4_CREDENTIALS` or
`GOOGLE_APPLICATION_CREDENTIALS` points at a file that is gone or unreadable, the search
carries on down the list, and it can succeed with a gcloud credential you had forgotten was
there. That is why `doctor` prints the source it actually used, along with every location
it checked and what it found in each: if a report comes back for the wrong account, that
line is where it says so.

---

## Step 8. Verify

Restart OpenClaw so it picks up the new environment, then ask the agent to check the setup:
"check my analytics setup" is enough, and it runs `doctor` for you. To run it yourself,
`openclaw skills info open-ga4` prints the installed path, and the command is
`node <skill-dir>/lib/cli.js doctor`. A healthy setup looks like this:

```
## GA4 setup check

- **PASS** Google credentials: loaded from GA4_CREDENTIALS (file) at /home/you/.openclaw/credentials/ga4.json, service account ga4-reader@openclaw-ga4-123456.iam.gserviceaccount.com
- **PASS** Admin API and property access: 2 properties reachable
- **PASS** Data API report: property 123456789 returned 12480 active users over the last 7 days
- **PASS** Privacy settings: redaction on; user-identifying dimensions blocked; property allowlist not set

**Properties this credential can read**

| Property id | Name | Account |
| --- | --- | --- |
| `123456789` | Acme Marketing Site | Acme Inc |
| `287441055` | Acme Docs | Acme Inc |
```

Read it line by line:

- **Google credentials**: the key file was found, parsed, and Google accepted it. The
  address shown is the one that needs Viewer access in Analytics. If it is not the address
  you pasted in step 5, that is your bug.
- **Admin API and property access**: the Admin API is on, and this is the full list of
  properties this credential can read. A property missing from the table did not get step 5.
- **Data API report**: a real report ran against a real property. This is the only check
  that proves reporting works end to end.
- **Privacy settings**: redaction is on and person-identifying dimensions are blocked.
  These are the defaults; the line exists so the posture is visible rather than assumed.

Checks run in dependency order, and only a credential that cannot be found or read stops
the run: nothing after it can be checked without one. (A key Google later rejects is not
that case: it loads fine here and fails at the two checks that actually call Google.) Everything else keeps going, so the
checklist shows the whole picture. (The one other check that can be missing rather than
failing is the live report, which needs a property to have been chosen first.) Each
failure prints a **Fix:** line under it naming the exact next action.

`doctor --json` answers a narrower question and is what the agent uses: instead of the
whole checklist it reports the single next thing you must do, as `blocked_on` plus a link
and the exact string to paste. Every value it can report has a section in
[SKILL.md](SKILL.md).

Then ask a real question ("what were my top pages last month?") and confirm you get a
table with numbers in it.

---

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `403` mentioning **`SERVICE_DISABLED`**, or the message "The Google Analytics Data API is not enabled in project *X*" | Step 2a was skipped, or was done while the project picker was pointing at a different project. | Open <https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com>, confirm the project picker shows the project named in the error, click **Enable**, wait a minute, retry. |
| The same error but naming **`analyticsadmin.googleapis.com`**, or `doctor` failing only on "Admin API and property access" | Step 2b was skipped. Enabling the Data API does not enable the Admin API; they are two separate switches. | Open <https://console.cloud.google.com/apis/library/analyticsadmin.googleapis.com> and click **Enable**. Reports work meanwhile; pass a numeric property ID directly. |
| `403` **without** `SERVICE_DISABLED`, "cannot read property 123456789" | Step 5 was skipped, or was done on a different property, or the address pasted into Analytics does not match the key file's `client_email`. This is the most common failure by a wide margin. | In Analytics: **Admin → Property access management → + → Add users**, paste the `client_email` from your key file, untick the email notification, select **Viewer**, click **Add**. Then re-run `doctor` and check the address it prints matches character for character. |
| `403` on one property while others work | Access is granted per property. The others got step 5; this one did not. | Repeat step 5 on that property. Or grant at the account level if you genuinely want the agent to read everything under the account. |
| `404` / `NOT_FOUND`, "Google Analytics has no property with id *N*" | The number is not a property that exists. Usually a typo, a digit dropped, or a number copied from a different Google product. | Run `properties` and use a property ID from the table it prints. Or re-read it from **Admin → Property details**. |
| "*G-XXXXXXXXXX* is a measurement id, which identifies a data stream rather than a property" | You used the measurement ID from your website's tracking tag. It is the string most people have to hand, and the reporting API cannot use it. | Get the numeric property ID from **Admin → Property details**, top right, 9–10 digits. Put that in `GA4_PROPERTY_ID`. |
| "*UA-12345-1* is not a GA4 property id. Expected a numeric id such as 123456789" | That is a Universal Analytics property ID. Universal Analytics was shut down and its API no longer exists. | There is no fix for a UA property; the data is not reachable through any current API. You need a GA4 property. If you have one, its ID is under **Admin → Property details**. |
| `invalid_grant`, or "This machine's clock is about *N* seconds behind Google's" | Authentication is a token this machine signs with a timestamp inside it. If the clock has drifted more than about a minute, Google rejects every signature. It looks exactly like a bad key, and people regenerate perfectly good keys over it. | Turn on automatic network time: **Date & Time → Set automatically** on macOS and Windows, the same setting in your Date & Time panel on Linux, or `timedatectl set-ntp true` from a terminal, which needs administrator rights and is yours to run rather than the agent's. Your key and your Analytics access are fine. |
| "Google Analytics has run out of API quota for this property" (`429`) | GA4's API quota is per property and is **shared**: the GA4 web interface, Looker Studio, exports and every other API client draw from the same pool. Long date ranges, many dimensions and large row limits each cost more. | Daily allowances reset at midnight US Pacific; hourly ones reset within the hour. Meanwhile ask for fewer dimensions, shorter ranges and smaller row limits. If it recurs daily, something else on your account is consuming the quota. |
| A report comes back with no rows, and no error | Almost always the date range predates the property. GA4 has no data before the day collection started, and asking for "last year" on a property created in March returns an empty, entirely correct answer. | Ask for a range you know has data ("last 7 days") and work backwards. Check when the property started collecting under **Admin → Property details**. Also check you are pointed at the production property and not a staging one. |
| A report comes back with no rows, and "last 7 days" also returns nothing | The property is not receiving events at all: the tag was removed, the site moved, or this is a property that was created but never wired up. | Open the Realtime report in <https://analytics.google.com> and load your own site in another tab. If Realtime stays empty, the problem is the tracking tag on your site, not this skill. |
| "The request reached Google without a usable credential", or the credentials check fails outright | No credential source resolved: `GA4_CREDENTIALS` is unset or names a path that does not exist, `GOOGLE_APPLICATION_CREDENTIALS` points somewhere stale, or the file is not readable by the user OpenClaw runs as. | Run `doctor`: it lists every location it checked and what it found in each. Then fix the path, or re-do step 4. |
| "service-account file is missing client_email or private_key" | The file at that path is JSON but is not a Google service-account key, commonly an OAuth *client* secret downloaded from the Credentials page instead of a key from the service account's **Keys** tab. | Redo step 4: <https://console.cloud.google.com/iam-admin/serviceaccounts> → click `ga4-reader` → **Keys** → **Add key** → **Create new key** → **JSON**. |
| "Google rejected the credential" after it previously worked | The key was deleted or the service account was disabled in Google Cloud. Tokens refresh automatically, so this is not an expiry. | Create a fresh JSON key (step 4) and put it in `GA4_CREDENTIALS`. Delete the old key in the console while you are there. |
| `doctor` shows **FAIL** on Privacy settings, "redaction is turned OFF" | `GA4_REDACT` is set to a false value (`0`, `false`, `no` or `off`). | Unset `GA4_REDACT`, or set it to `1`, `true`, `yes` or `on`. There is no command-line flag for this, deliberately: see the Privacy section of [SKILL.md](SKILL.md). |

---

## Alternative for developers: gcloud application-default credentials

If you already have the `gcloud` CLI and your own Google account has access to the property,
you can skip the service account entirely. The skill reads
`~/.config/gcloud/application_default_credentials.json` as its last credential source.

```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform

gcloud auth application-default set-quota-project openclaw-ga4-123456
```

What each part is doing:

- **`--scopes` is required here.** Without it, `gcloud auth application-default login` grants
  gcloud's default scope set, which covers Cloud Platform but not Analytics, and GA4
  rejects the resulting token as insufficiently scoped. Naming `analytics.readonly`
  explicitly is what makes the credential able to read Analytics, and read is all it can do.
- **`cloud-platform` is in that list only so the second command works.**
  `set-quota-project` writes to the Cloud Resource Manager API and needs it. If you leave it
  out, the login still works, but gcloud prints a warning that it cannot set a quota project,
  and later calls can fail with a confusing "API not enabled" or quota error. You can either
  include the scope as above, or omit it and add the line `"quota_project_id":
  "openclaw-ga4-123456"` to `~/.config/gcloud/application_default_credentials.json` by hand.
- **The quota project must have the Data API enabled**: step 2a still applies. The quota
  project is the project whose quota and API enablement your requests are billed against.
  This is the trap: your personal account may have perfectly good Analytics access while the
  project attached to your ADC file has never had `analyticsdata.googleapis.com` switched on.

Two honest trade-offs before you choose this path:

1. **This credential is you.** It inherits your own Analytics access, which is why step 5 is
   unnecessary, and it means the agent reads everything you can read, not a scoped subset.
   A service account with Viewer on one property is the tighter grant.
2. **It expires.** ADC refresh tokens are revoked when you change your password, when an
   administrator resets sessions, and on their own schedule under some Workspace policies.
   A service account key does not. For anything that runs unattended, use the service
   account.

If both a service-account key and ADC are present, the service account wins: `GA4_CREDENTIALS`
is source 1 or 2 and gcloud is source 4. See the resolution order in step 7.

---

## Still stuck

Run `doctor` and read the **Fix:** line under the first `FAIL`. The checks run in
dependency order, so the first failure is the real one; everything after it is a consequence.

If the fix line does not resolve it, open an issue with the `doctor` output. It never
prints key material (credentials are reported as present or absent, by source, and never by
content), so it is safe to paste.

---

## Trademarks

This is an independent open-source project. It is not affiliated with, endorsed by, or
sponsored by Google LLC. Google Analytics and GA4 are trademarks of Google LLC.
