# Example: Statement Scan

> Drop a bank statement, find every subscription hiding in it.

---

## Scenario

Sarah downloads her Chase Visa statement for January–March 2026 as a CSV and sends it to her OpenClaw agent.

---

## Conversation

**Sarah:** Here's my Chase Visa statement for the last 3 months. Find all my subscriptions.

*[Uploads: chase-visa-jan-mar-2026.csv]*

**Agent:**

Scanning your Chase Visa statement (Jan 1 – Mar 11, 2026)... Found 247 transactions. Analyzing for recurring charges.

📋 **Statement Scan Results — Chase Visa ending 4821**

🟢 **HIGH CONFIDENCE** (matched 3+ times, consistent amount & timing):

| Service | Amount | Frequency | Next Renewal |
|---------|--------|-----------|--------------|
| Netflix | $17.99/mo | Monthly | Apr 15 |
| Spotify Premium | $11.99/mo | Monthly | Apr 3 |
| ChatGPT Plus | $20.00/mo | Monthly | Apr 8 |
| iCloud+ (Apple) | $2.99/mo | Monthly | Apr 1 |
| Planet Fitness | $26.99/mo | Monthly | Apr 5 |
| Notion | $10.00/mo | Monthly | Apr 12 |

🟡 **NEEDS YOUR REVIEW** (2 matches or unclear pattern):

1. **AMZN MKTP US** — $14.99 on Jan 22, $14.99 on Feb 22
   → Looks like Amazon Prime. Is this your Prime membership? **(Y/N)**

2. **SQ *CROSSFIT MILE HIGH** — $225.00 on Jan 3, $225.00 on Feb 3, $225.00 on Mar 3
   → Gym/fitness membership? **(Y/N)**

3. **GOOGLE *YOUTUBE** — $13.99 on Feb 18 (single charge)
   → YouTube Premium? Only one charge in 3 months — might be new. **(Y/N)**

🔴 **UNKNOWN RECURRING:**

4. **BRTCL*BRITEBOX** — $4.99 on Jan 8, $4.99 on Feb 8, $4.99 on Mar 8
   → I don't recognize this merchant. Do you? **(Identify / Skip / Ghost)**

5. **WIX.COM** — $16.00 on Feb 3 (single charge)
   → Wix website hosting? **(Y/N)**

---

**Sarah:** Yes to Amazon Prime. Yes to CrossFit. No to YouTube — that was a gift purchase. The Britebox one... I have no idea what that is. And yes to Wix.

**Agent:**

Updated! Here's your subscription dashboard:

📊 **Your Subscriptions — Chase Visa ending 4821**

| Service | Amount | Category |
|---------|--------|----------|
| CrossFit Mile High | $225.00/mo | 💪 Fitness |
| Planet Fitness | $26.99/mo | 💪 Fitness |
| ChatGPT Plus | $20.00/mo | 🤖 AI Tools |
| Netflix | $17.99/mo | 🎬 Streaming |
| Wix | $16.00/mo | 🔧 Productivity |
| Amazon Prime | $14.99/mo | 🎬 Streaming |
| Spotify Premium | $11.99/mo | 🎵 Music |
| Notion | $10.00/mo | 🔧 Productivity |
| iCloud+ | $2.99/mo | ☁️ Cloud Storage |

**Monthly total: $346.95**
**Annual projected: $4,163.40**

---

⚠️ **OVERLAP DETECTED: Fitness**

You have 2 gym/fitness subscriptions:
- CrossFit Mile High — $225.00/mo
- Planet Fitness — $26.99/mo

Combined: $251.99/month ($3,023.88/year) on fitness.

Do you use both? If CrossFit is your primary gym, Planet Fitness might be one to cut — that's $323.88/year back.

---

👻 **GHOST SUBSCRIPTION: BRTCL*BRITEBOX**

This has been charging $4.99/month since at least January. You've paid at least $14.97 for something you don't recognize.

Want me to help you figure out what this is and how to cancel it?

---

**Sarah:** Oh wow, I totally forgot about Planet Fitness. I haven't been since I started CrossFit in November. And yeah, figure out what Britebox is.

**Agent:**

Let me help with both.

🚪 **HOW TO CANCEL: Planet Fitness**

Unfortunately, Planet Fitness requires cancellation **in person** at your home club or via **certified mail**. No online or phone cancellation.

Steps:
1. Visit your home Planet Fitness location
2. Ask the front desk to cancel your membership
3. They'll process a 30-day notice — you'll have one more billing cycle
4. Alternatively: send a certified letter to your home club requesting cancellation

⚠️ If your annual fee is coming up (usually in June or November), try to cancel before it hits.

💰 Cancelling saves you: $26.99/month ($323.88/year)

---

🔍 **Investigating: BRTCL*BRITEBOX**

"Britebox" appears to be a meal kit/snack box subscription. The "BRTCL" prefix is their payment processor. Check your email for any signup confirmation from Britebox or a similar-sounding service.

If you want to cancel: search your email for "britebox" or "brite box" to find the account, then log in and cancel from their website.

---

**Sarah:** This is amazing. I just saved $30/month without even trying.

**Agent:**

$30.00/month = **$359.88/year**. 💰

Once you've confirmed both cancellations, let me know and I'll update your tracker. Your new monthly total will drop to $316.96.

Do you have statements from any other cards or bank accounts? Subscriptions tend to spread across multiple payment methods.
