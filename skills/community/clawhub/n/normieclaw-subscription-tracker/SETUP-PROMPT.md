# Subscription Tracker — Setup Prompt

> Run this conversation with your OpenClaw agent after installing the Subscription Tracker skill.

---

## What This Does

This setup process will:
1. Create your subscription tracker directory and config files
2. Walk you through your first statement scan
3. Build your initial subscription database
4. Set your alert preferences
5. Optionally connect to Budget Buddy Pro

---

## The Prompt

Copy and paste the following to your OpenClaw agent:

---

**I just installed the Subscription Tracker skill. Let's set it up.**

**Here's what I need:**

1. Run the setup script at `~/.normieclaw/subscription-tracker/scripts/setup.sh` to create my directory structure and default config.

2. Ask me about my alert preferences:
   - How many days before a renewal should I be reminded? (default: 3 and 7 days)
   - What day of the month should I get my monthly summary? (default: 1st)
   - What month should my annual subscription audit run? (default: January)

3. Once setup is done, I'll drop my first bank/credit card statement (CSV preferred). Scan it and show me every recurring charge you find.

4. After the scan, show me:
   - Total monthly subscription spend
   - Total annual projected spend
   - Any duplicate/overlapping services you spotted
   - Any charges I might not recognize (ghost subscriptions)

5. If I have Budget Buddy Pro installed, show me how to export my subscription data to it.

**Let's start with step 1.**

---

## After Setup

Once your first scan is complete, you can:

- Drop additional statements from other cards/banks to build a complete picture
- Say "add a trial" to track any free trials you're currently using
- Say "upcoming renewals" to see what's coming up
- Say "monthly summary" anytime for a full report
- Say "subscription audit" to review everything and decide what to keep or cancel

## Tips for Best Results

- **Use CSV over PDF** — CSV parsing is more reliable. Most banks let you export CSV from their transaction history page.
- **Scan 3 months of history** — More data = better pattern detection. One month might miss quarterly or annual charges.
- **Scan every card/account** — Subscriptions often spread across multiple payment methods. Scan them all.
- **Check back monthly** — Drop a fresh statement each month and say "compare statements" to catch new charges and price changes.
- **Tell the agent about trials** — It can't detect free trials from statements (no charge yet). Manually add them so you get reminded before they convert.

## Ongoing Usage

After setup, you'll get the most value by:

**Weekly:** Ask "upcoming renewals" to see what's coming. Takes 5 seconds.

**Monthly:** Drop your latest statement and say "compare statements" to catch new charges, missing charges (cancelled?), and price increases. Then say "monthly summary" for the full picture.

**Quarterly:** Say "find duplicates" to check for overlapping services. Useful after adding new subscriptions.

**Annually:** Say "subscription audit" for a full walkthrough of every subscription. Keep, review, or cancel each one.

## Need Help?

Say any of these to your agent:
- "Show my subscriptions" — see everything being tracked
- "Find duplicates" — check for overlapping services
- "Cancel [service name]" — get step-by-step cancellation instructions
- "How much am I saving?" — see your running savings from cancelled subs
- "Export my subs" — get a CSV or markdown export
- "Add a trial" — track a free trial before it converts to paid
- "Upcoming renewals" — see what's renewing in the next 7 days
- "Subscription audit" — full review of all subscriptions
