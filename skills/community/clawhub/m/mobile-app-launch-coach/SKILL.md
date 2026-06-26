---
name: mobile-app-launch-coach
description: End-to-end coach for indie devs / small teams launching mobile apps on iOS App Store + Google Play (and emerging app stores). Covers idea + ASO niche validation, native vs cross-platform (Swift/Kotlin/Flutter/React Native/Expo), App Store + Play Console submission and review survival (rejection patterns, IAP rules, privacy nutrition labels, AI-content disclosure 2026), monetization (subscription / one-time / freemium / ads / hybrid), App Tracking Transparency reality, ASO + paid UA + influencer + referral growth, retention and lifecycle messaging, exit options (acquisition, sale via Acquire.com / FE / direct). Use when builder asks about "should I build native or cross-platform", "App Store rejection", "Play Store policy", "ATT / IDFA", "subscription pricing tiers", "ASO keywords", "App Clip", "Instant App", "Apple Search Ads vs Meta UA", or transitioning a web SaaS to mobile. Triggers on phrases like "launch iOS app", "publish to App Store", "Google Play submission", "Flutter vs React Native", "Expo", "Apple subscription", "in-app purchase", "RevenueCat", "App Store rejection 4.3", "Privacy Manifest", "ASO ranking", "Apple Search Ads".
---

# mobile-app-launch-coach

Coach an indie dev / small team through shipping a mobile app as a real product (not a portfolio piece). The 4 phases: validate the idea + ASO niche before building (most app failures are demand failures, not product failures), pick a stack + architecture that ships fast without becoming legacy debt, survive App Store + Play Store review (the review processes have strict opinions, especially around AI content + subscriptions + privacy), and monetize + grow without burning your launch on a single bad review or rejected build. Most indie apps fail one of: pure-rip-off-of-popular-app (rejected immediately), free-with-no-monetization-path, building before any keyword research, or going in solo when iOS + Android + backend + design + marketing actually need a 2-3 person team.

## When to engage

Trigger when the builder mentions:
- New app idea or app already in flight (consumer / utility / productivity / fitness / health / finance / dating / social / education / entertainment / kids)
- Stack decisions: native (Swift / Kotlin), cross-platform (Flutter, React Native, Expo, Capacitor / Ionic, .NET MAUI, KMP)
- Apple-specific: SwiftUI vs UIKit, Combine, Swift Concurrency, SwiftData, App Intents, App Clips, WidgetKit, ActivityKit
- Android-specific: Jetpack Compose, ViewModel / Hilt, Navigation, Room, WorkManager
- App Store submission: TestFlight, App Store Connect, App Privacy nutrition labels, Privacy Manifest (iOS 17+), Required Reasons API, TCC permissions, App Tracking Transparency (ATT)
- Play Console: closed / open testing tracks, Play Console policy review, AAB (Android App Bundle), Play App Signing, Data Safety form
- IAP / subscriptions: StoreKit 2, Google Play Billing v6+, RevenueCat, Adapty, Stripe (rare for mobile due to platform rules)
- Monetization: subscription tiers, free trial vs intro pricing, paywall design, freemium, ad networks (AdMob, Mintegral, Liftoff/Vungle, IronSource, Unity LevelPlay)
- Privacy / regulatory: ATT, IDFA, AAID, GDPR, COPPA (kids apps), HIPAA (health), KYC (finance), SOC2
- Growth: ASO (keywords, screenshots, video), Apple Search Ads, Meta / TikTok / Google UA, influencer, referral, lifecycle messaging (Braze, OneSignal, CleverTap, Iterable)
- Retention: D1/D7/D30 metrics, churn, push notifications, deep links, Universal Links, App Links
- Specific niches: utility app, productivity app, fitness/wellness, meditation, language learning, journal, finance / budgeting, kids / education, social / dating, AI-feature wrapper apps
- Specific concerns: App Store rejection (4.3 spam, 5.1.1 privacy, 3.1.1 IAP), Play Store removal, account suspension, lockdown of paid app

Do not engage for: explicit ToS-violating apps (cheats / unauthorized scrapers / IP infringement / fake-account tools), pure web app / PWA without mobile-specific concerns, or "hire me to build the app" agency questions.

## Diagnostic sweep — run before recommending anything

Ask 12-16 questions. Pull at least one from each block.

**The product**
1. What is the JOB the user does with the app, in 1 sentence (no jargon)? Daily / weekly / monthly use frequency?
2. Who's the user? Specific persona (age, gender, country, situation, willingness to pay).
3. Closest 3 competitors. Their MAU / ASO ranking / monetization model. URL each.
4. Is mobile the right form factor? (Or is it really a web app + mobile companion? Or desktop?)

**Build state**
5. Built / unbuilt? If built: which platform(s) live, build version, current users? If unbuilt: stack chosen + why?
6. Backend: pure-client / cloud-API / Firebase / custom backend / SaaS-like?
7. Team: solo, founder + dev, founder + dev + designer, full team?

**Audience & monetization**
8. Owned audience size: email list, X / TikTok / IG followers, community.
9. Monetization model: subscription, one-time, freemium, ads, hybrid? Target ARPU / LTV?
10. Revenue target: month-3, month-12, month-24.

**Regulatory / risk**
11. Categories with extra scrutiny: kids (COPPA), health (HIPAA), finance (KYC / regulated), dating (age-gating), gambling (skill-vs-chance), crypto (FinCEN / SEC concerns).
12. Privacy: collecting which data? IDFA tracking? Third-party SDKs? GDPR / CCPA compliance plan?

**Constraints**
13. Budget for first 6 months (build + UA + tools + Apple/Google fees).
14. Timeline: aggressive (3 months to launch), normal (6 months), thoughtful (9-12 months)?
15. iOS-only / Android-only / both? (Most indies underestimate the cost of "both.")
16. Geographic launch scope: US-only / EN-speaking / global?

If they can't answer 8-12, the gap is the work. Many app projects fail because the "build" started before the demand validation, ASO research, and monetization model were grounded.

## Phase 1 — Idea validation + ASO research

Most failed apps die from missing demand, not poor build quality. Validate before code.

**Demand-validation gate (3 conditions)**:
1. **Real job, ≥1×/week**: the app must do something the user actually does (or wishes they did) at least weekly. Daily-frequency apps win monetization wars; monthly-use apps churn fast.
2. **ASO keyword traffic exists**: there are real searches for what your app does. Use AppFigures / SensorTower / data.ai / Mobile Action / AppTweak to verify keyword volume.
3. **Monetization aligned with category**: paid subscription apps win in productivity, fitness, learning, finance, photo. Ads win in casual / utility. Free + IAP wins in games. Pick the model that's already winning your category — don't fight it.

**ASO research methodology** (do this BEFORE building):
- Pick 20-50 candidate keywords your target user might search.
- For each, check: estimated search volume (high / mid / low), competition intensity (top 3 results), top results' download estimates.
- Goldilocks zone: mid volume + mid competition (vs high vol + saturated, or low vol + no demand).
- Examples of ASO niches with under-served demand: very-specific use cases ("calorie tracker for vegan athletes"), niche audiences ("Spanish-language meditation app for parents"), platform-specific gaps (an iPad-optimized app where competitors are iPhone-only).

**Tools**:
- **App Store Connect**: keyword density + impressions data once your app is live (limited but real).
- **Google Play Console**: similar data on Play side.
- **AppFigures / SensorTower / data.ai / Mobile Action / AppTweak**: ASO research + competitive intelligence ($30-300/mo).
- **Free**: Sensor Tower's free tier, App Annie (now data.ai) free dashboards, manual App Store search ranking checks.

**Demand-signal validation (low-cost)**:
- Landing page with email capture: post on TikTok / IG / Reddit / Twitter; collect 200-500 emails before building.
- TestFlight / Play Internal closed beta with 30-100 hand-picked users; measure D7 retention before building paid features.
- Interview 20 prospective users about the job; deeper than surveys.

**Demand-signal anti-patterns**:
- "Friends and family say cool" — survivorship bias, not demand.
- "I would use this myself" — sample size 1.
- Twitter likes on idea ≠ download intent.
- "Existing apps suck" without identifying the specific gap you fill.

## Phase 2 — Stack selection (native vs cross-platform)

The single biggest decision. Wrong stack = either ship-too-late OR build-on-sand.

**Decision matrix**:

| Stack | Best for | Pros | Cons | Effort 0→launch |
|---|---|---|---|---|
| **SwiftUI / Swift (iOS)** | iOS-first, polished UX, deep system integrations, < $200K MRR target initially | Best UX on iOS, fastest iteration on iOS, fewer build issues, smaller team works | Don't get Android for "free" | 8-16 weeks |
| **Jetpack Compose / Kotlin (Android)** | Android-first, mature material design, deep system integrations | Best Android UX, fastest iteration on Android | Don't get iOS for free | 10-16 weeks |
| **Native both (separate codebases)** | Larger team, scaling app, $1M+ ARR target | Best quality on each platform, no abstraction overhead | 1.7-1.9× cost vs single platform; need iOS + Android engineers | 14-20+ weeks |
| **React Native (Expo or bare)** | JS team, web → mobile, want shared code | Largest ecosystem, fastest hire pool, OTA updates with Expo | Animation / scrolling can lag, native module hell occasionally, MV3-style native API churn | 10-14 weeks |
| **Expo** | RN with managed runtime, fastest indie path | Fastest setup, OTA updates, fewer build pipeline headaches | Limited to Expo modules unless ejecting; bundle size larger | 8-12 weeks |
| **Flutter (Dart)** | Pixel-perfect UI control, gaming-adjacent UI, multi-platform incl desktop | Single codebase iOS + Android + (web/desktop), super smooth animations | Dart hire pool smaller, native integrations heavier | 10-14 weeks |
| **KMP (Kotlin Multiplatform)** | Android team adding iOS, share business logic | Native UI on both sides, share networking / domain logic | Maturity gap on iOS, native UI duplication | 14-18 weeks |
| **Capacitor / Ionic** | Existing web app needing thin mobile shell, hybrid web tech | Reuse web codebase | Web-feel on mobile; punished by App Store reviewers if "just a web view" | 6-10 weeks |
| **.NET MAUI** | Existing .NET / Xamarin codebase, enterprise app | Enterprise-friendly, C# stack | Smaller hire pool, animation / native integration tradeoffs | 12-16 weeks |

**Decision heuristics**:
- **Solo dev, iOS-only first launch** → SwiftUI. Ship faster, polish higher.
- **Solo dev, both platforms must launch** → Expo (fastest and most forgiving) or Flutter (best for highly polished UI).
- **Existing JS/TS team** → React Native (or Expo).
- **Existing native Android team adding iOS** → KMP or Flutter.
- **App heavy in animations / custom rendering** → SwiftUI / Jetpack Compose / Flutter.
- **App heavy in system integration (HealthKit, ARKit, deep widgets, App Intents, ActivityKit, Watch app, Vision Pro)** → Native (no cross-platform fully covers these).
- **Existing web SaaS adding companion mobile app** → React Native or Capacitor (depending on how mobile-native you want it to feel).

**Tradeoffs to confront honestly**:
- "Cross-platform" is rarely 1× cost; it's 1.2-1.5× because edge cases on each OS still need handling.
- "Single codebase" doesn't mean "single test surface" — you still test on iOS + Android.
- App Store reviewers reject apps that feel "obvious web view" (4.2 minimum-functionality rejection); Capacitor / pure Cordova are higher-risk.

**Backend stack**:
- **Firebase** (Auth, Firestore, FCM, Crashlytics, Analytics): fastest indie path, free tier generous, vendor lock-in concern over time.
- **Supabase**: open-source Firebase alternative, Postgres-based, growing ecosystem.
- **Custom backend (Node / Go / Python / Rails)**: more control, more ops; right at scale.
- **Serverless (Cloudflare Workers, Vercel, AWS Lambda)**: works for many app patterns; cold-start consideration.

**SDK ecosystem (typical mobile app stack)**:
- Auth: Firebase Auth, Auth0, Clerk, Supabase Auth, custom.
- Analytics: Firebase Analytics, Mixpanel, Amplitude, PostHog.
- Crash reporting: Firebase Crashlytics, Sentry, Bugsnag.
- Push notifications: FCM (cross-platform), APNs, OneSignal, Braze.
- Subscriptions / IAP: RevenueCat (most-popular for indie), Adapty, Qonversion, native StoreKit / Play Billing.
- Lifecycle / messaging: OneSignal, Braze, CleverTap, Iterable, Customer.io.
- Attribution: Adjust, AppsFlyer, Branch, Singular, SKAN-only (Apple).
- Feature flags / remote config: Firebase Remote Config, Statsig, LaunchDarkly, PostHog.

## Phase 3 — App Store + Play Store submission

The gauntlet. Indies underestimate the review cycle; plan 2-4 weeks of submission iteration.

**Apple App Store Review Guidelines (most-relevant)**:
- **Section 1 (Safety)**: harmful content, kids' safety, dating app safety, user-generated content moderation.
- **Section 2 (Performance)**: 2.1 (apps must run), 2.5.1 (Privacy Manifest required since iOS 17+), 2.5.2 (don't track without ATT consent).
- **Section 3 (Business)**: 3.1.1 (digital purchases use IAP, NOT Stripe), 3.1.3 (reader apps exception), 3.2.2 (avoid spam).
- **Section 4 (Design)**: 4.0 (general quality), 4.2 (minimum functionality — "doesn't do enough"), 4.3 (spam — "we already have hundreds like this"), 4.7 (mini-apps, gambling, dating restrictions).
- **Section 5 (Legal)**: 5.1.1 (privacy policy required, data collection disclosed), 5.1.2 (data minimization), 5.2 (intellectual property).

**Apple-specific 2026 details**:
- **Privacy Manifest** (iOS 17+, required since 2024): privacy practices declared in `PrivacyInfo.xcprivacy`; covers data usage + third-party SDKs you depend on.
- **Required Reasons API**: certain APIs (UserDefaults reads, file timestamp APIs, etc.) must declare reason for use.
- **App Tracking Transparency (ATT)**: mandatory prompt before using IDFA for tracking.
- **AI content disclosure** (2026 update): apps using generative AI must disclose AI-generated content; opt-in for user-facing AI features.
- **Subscription requirements**: weekly subscriptions require special justification; auto-renewable subscriptions require clear UI showing price + renewal terms before purchase.

**Common Apple rejections (and fixes)**:

| Reason | Cause | Fix |
|---|---|---|
| 4.3 (spam) | App "feels like" hundreds of others | Stronger differentiation in description, screenshots, video; unique value-prop |
| 4.2 (minimum functionality) | App doesn't do enough; mostly web view | Build native features; reduce "just a web wrapper" feel |
| 5.1.1 (privacy) | Missing privacy policy or unclear data practices | Host privacy policy, fill nutrition labels honestly |
| 3.1.1 (IAP) | Selling digital goods via Stripe / external | Switch digital goods to IAP; physical goods can use Stripe |
| 2.1 (performance) | Crash on launch / specific flow | Test on real iOS devices (not just simulator); test latest iOS |
| 2.3 (accurate metadata) | Screenshots show features not in app | Update screenshots to match actual product |
| 5.6.1 (developer code of conduct) | Suspicious developer activity | Use a clean Apple Developer account; respond to inquiries |

**Google Play Console policies**:
- **Restricted content**: gambling (region-specific), kids (Designed for Families), health (medical claims), financial services (KYC).
- **Privacy / security**: Data Safety form (mandatory), prominent disclosure for sensitive permissions, target SDK level.
- **Spam / minimum functionality**: similar to Apple's 4.3.
- **Intellectual property**: trademark / copyright / impersonation.
- **Subscription requirements**: clear pricing, easy cancellation, free trial / intro pricing rules.
- **AI content**: similar 2026 disclosure requirement.

**Common Play rejections**:
- Permission overreach (asking for permissions not used by app).
- Background location without justification.
- Foreground service without justification.
- Data Safety form mismatched with actual data collection.
- App targeting too-low SDK level (each year minimum target SDK rises).

**Submission process**:

**Apple flow (iOS)**:
1. Apple Developer account ($99/yr individual or $99/yr organization).
2. Create app in App Store Connect.
3. Build with Xcode → Archive → Distribute via App Store Connect.
4. Upload via Transporter or Xcode.
5. Internal testing (TestFlight) → external testing (TestFlight) → submit for review.
6. Review takes 24-48h typical (sometimes longer for complex apps).
7. Privacy nutrition labels + Privacy Manifest before submit.
8. Screenshots + preview video + description + keywords.
9. Pricing tier + availability per country.

**Google flow (Android)**:
1. Google Play Console account ($25 one-time fee).
2. Create app in Play Console.
3. Build AAB (Android App Bundle).
4. Internal testing → closed testing → open testing → production.
5. Data Safety form mandatory.
6. Pre-launch report runs automated tests on device matrix.
7. Review takes 1-7 days (variable; faster for established devs).

**TestFlight + Play closed testing — use them**:
- Internal: 100 testers (Apple), unlimited (Google internal track).
- External (Apple): 10,000 testers, requires beta review (~24h).
- Run beta for 2-4 weeks with 50+ engaged users; fixes 80% of bugs that would cause launch-day disasters.

## Phase 4 — Monetization (the indie reality)

Indie mobile apps have 4 viable models. Pick the one that fits your category, not the one trending on Twitter.

**Model 1: Subscription (recommended for most indie consumer apps)**:
- Best categories: productivity, fitness, meditation, learning, journaling, photo / video tools, AI-feature apps.
- Pricing: $4.99-$9.99/mo or $29.99-$59.99/yr typical for solo indie tools. Higher for B2B-adjacent.
- Free trial: 3-7 day for $/mo; 7-14 day for $/yr. Or "free + paywall" hard freemium.
- Tools: RevenueCat (industry standard, free tier 10K MTU), Adapty, Qonversion.
- Conversion: free trial → paid 30-50% typical. Paywall conversion 2-8% of installs.
- Trial-cancel rate: 50-70% — manage expectations.

**Model 2: One-time purchase (paid up-front)**:
- Best categories: utility apps, niche tools, dev tools, kids' apps (no recurring guilt), pro creative tools.
- Pricing: $0.99-$9.99 (impulse) / $9.99-$29.99 (premium niche tools) / $29.99-$99.99 (pro tools).
- Conversion: low (1-3% of organic installs); demands organic discovery + word-of-mouth.
- Math: needs 10× volume of subscription to match LTV.

**Model 3: Freemium with IAP / unlocks**:
- Best categories: games, photo apps, utility tools with "remove watermark / add color" unlocks.
- Mix of one-time IAP + maybe subscription tier.
- Conversion: 1-5% of installs purchase ANY IAP.

**Model 4: Ads (interstitial / banner / rewarded)**:
- Best categories: casual games, free utility apps with high engagement, content consumption apps.
- Networks: AdMob (default), Mintegral, Liftoff/Vungle, IronSource, Unity LevelPlay (mediation).
- ARPDAU: $0.05-$0.50 typical depending on ad density + geography. US/JP/UK pay best.
- Bad for: productivity apps, B2B-adjacent, anything with "professional" feel.

**Hybrid models**:
- Subscription + ads (free tier with ads, subscription removes ads + adds features) — common for casual fitness, meditation, content apps.
- Free + IAP + paywall for premium content (dating apps, content marketplaces).

**Pricing decision tree**:
- Daily-use, productivity, $5-15 willingness to pay → **subscription $4.99-9.99/mo**.
- Pro / specialist tool, $30-100 willingness → **one-time $19-49 OR yearly subscription $39-79**.
- Casual / occasional use → **freemium with ads or one-time $0.99-2.99**.
- Health / fitness / education recurring value → **annual subscription $39-79/yr** with free trial.

**Subscription paywall design**:
- Show value before paywall (free trial of feature, demo screen).
- 3-tier paywall (Lite / Pro / Premium) underperforms 1-tier with annual discount for most consumer apps.
- Annual default (often better LTV than monthly).
- Free trial visible: "Start 7-day free trial — $9.99 / mo after".
- Cancel-anytime visible: trust signal.
- Don't dark-pattern the cancel flow — lawsuit risk + Apple flag.

**Apple / Google revenue split**:
- 30% (standard) for first $1M revenue/yr.
- 15% small business program (under $1M annual revenue, on application).
- 15% on subscription year 2+ at Apple (auto-applies after 1 year retained).
- DMA / EU: Apple now allows alternative app stores + alternative payment processing in EU, with separate fee structure (Core Technology Fee, etc.). Watch for changes.

## Phase 5 — Privacy / regulatory (the 2026 reality)

Privacy is the biggest store rejection category. Get it right at design time, not at submission.

**iOS App Tracking Transparency (ATT)**:
- Mandatory prompt before tracking user across apps using IDFA.
- Most users opt out (60-80%); plan UA strategy around limited IDFA.
- Use SKAN (SKAdNetwork) for attribution; aggregate / privacy-preserving signal.
- Apple Search Ads: only platform where you keep IDFA-based attribution for paid UA.

**Privacy Manifest (iOS 17+)**:
- `PrivacyInfo.xcprivacy` file declaring:
  - Privacy practices: data types collected + linkage + tracking.
  - Required reasons API: justification for using certain APIs.
  - Tracking domains: domains used for tracking.
- Third-party SDKs must provide their own privacy manifests; you incorporate them.
- Apple validates at submission; missing or wrong → rejection.

**Privacy nutrition labels (App Store + Play Data Safety)**:
- Declare what data you collect, why, whether you share / sell, whether you link to identity.
- Categories: identifiers, contact info, location, contacts, search history, browsing history, financial info, health, sensitive info.
- BE HONEST. Lying caught at app review (rare) or post-launch by user reports / regulatory inquiry.

**GDPR (EU) / CCPA (CA) / similar**:
- Cookie / tracking consent in app via dedicated screen.
- Privacy policy linked from app + App Store listing.
- Data subject access requests (DSAR) handling — implement /privacy/delete endpoint.
- DPO if processing EU data at scale.

**Specific category regulations**:
- **Kids** (under 13 in US per COPPA): Designed for Families program (Google), Kids Category + Made for Kids (Apple); strict ad rules; no tracking; parental consent for any data collection.
- **Health**: HIPAA if you're a covered entity / business associate (medical records); medical claims need disclaimers; FDA scrutiny if functioning as medical device.
- **Finance**: KYC if handling money movement; SOC2 Type II for B2B; PCI DSS if handling cards directly (use Stripe / Plaid to avoid).
- **Dating**: age-gating, identity verification growing requirement, location safety features required by some jurisdictions.
- **Crypto**: SEC scrutiny on tokens that look like securities; Apple / Google have specific policies on crypto; airdrops in-app banned by Apple typically.

**AI / ML feature disclosure (2026)**:
- Apple and Google now require disclosure when app uses generative AI for user-facing content.
- Provide opt-in for AI features; clearly mark AI-generated content; provide reporting mechanism for problematic AI outputs.
- LLM cost should be modeled into your unit economics (see `ai-product-launch-coach`).

## Phase 6 — Growth (ASO + paid + organic)

Mobile UA is harder than 5 years ago. ATT broke Meta UA precision; CPI is up; retention is more important than ever.

**ASO (App Store Optimization)**:

| Lever | iOS | Android |
|---|---|---|
| Title | 30 chars; primary keyword + brand | 50 chars; richer keyword stuffing tolerated |
| Subtitle | 30 chars; secondary keyword | (no equivalent — use short description) |
| Keywords (iOS) / description (Android) | 100 chars hidden keyword field | 80 char short description (high weight) + 4000 char long description |
| Screenshots | 6.7" + 6.5" + 5.5" sets | Multiple screen sizes |
| Preview video | 30s landscape or portrait | Up to 30s YouTube link |
| App icon | Visual hook; A/B test in App Store Connect (Custom Product Pages) | Same; use Play Console experiments |
| Reviews + ratings | Highest weight in Apple ranking | High weight |
| Install velocity + retention | Strong recent ranking signal | Strong recent ranking signal |

**ASO playbook**:
- 20-50 candidate keywords; pick top 10-20 to target.
- A/B test screenshots via Custom Product Pages (iOS) or Play Console experiments (Android).
- First screenshot is the most important — convert browsers to installers in 2 seconds.
- Demo video: focus on the JOB; show the magic moment.
- Update visuals every 60-90 days; refresh keywords on observed performance.

**Paid UA**:
- **Apple Search Ads (ASA)**: highest-intent traffic; users searching your keyword. Best for low-volume specific keywords. Average CPI $1-5 in EN markets.
- **Meta (FB/IG) Ads**: broader reach, post-ATT precision lower; creative quality matters more. Average CPI $3-15 consumer apps.
- **TikTok Ads**: cheap CPM, hard to target precisely, works for impulse + Gen Z apps. Average CPI $1-5.
- **Google App Campaigns / UAC**: black box, set goal + creative, Google optimizes. Decent baseline.
- **YouTube**: skippable + non-skippable; works for video-friendly apps.
- **Influencers / creators**: high-engagement, high-CPI, but high retention from word-of-mouth users.
- **Apple Search Ads + Branch / Adjust attribution**: Apple Search Ads keeps IDFA attribution; combine with attribution platform for full funnel.

**ASA decision rule**:
- Below $50/day: branded search defense (own your name).
- $50-500/day: targeted competitor + category keywords.
- $500+/day: discovery search across full keyword set.

**Organic growth**:
- ASO compounding (slow burn 3-12 months).
- Word-of-mouth from delighted users — only happens with great D7 retention.
- Social content (TikTok / IG / X / YouTube): builder's content showing app + journey.
- Referral / share features: invite-friends-get-week-free; share-result-on-social.
- Press / launch coverage (Product Hunt, TechCrunch, niche blogs).

**Retention is everything**:
- D1 retention: 25-40% typical; <20% = problem.
- D7 retention: 10-20% typical; <5% = product fit issue.
- D30 retention: 5-10%; subscription apps survive on this number.
- Lifecycle messaging: push notifications, email, in-app cards. Tools: OneSignal, Braze, CleverTap.

## Phase 7 — Common indie failure modes

1. **Built before validated**. No keyword research; no competitor analysis; no email list. Result: 50 downloads, $0.
2. **Cross-platform when iOS-only would have been faster**. Spent 6 mo on Flutter; iOS-only would have shipped in 3 mo with same revenue.
3. **Subscription paywall too aggressive**. Hard paywall on screen 1 = 90% drop. Show value first.
4. **Free with no monetization plan**. 10K downloads, $0 MRR, founder discouraged.
5. **Permission bloat**. Asking for location / contacts / photos when app needs none. ATT prompt + privacy nutrition look bad. Rejection risk.
6. **Mismatched data safety form**. Declared "no data collection" while embedded SDK collects analytics. Caught in audit; account suspension risk.
7. **One-tier flat subscription** without annual discount. Leaves 30-50% LTV on table.
8. **Manual review fight on rejection**. 4.3 spam rejection — argue, reapply same product, get rejected again. Address the substance.
9. **Single-language app (English only)**. 30-40% of organic installs come from non-English markets. Localize top 5-10 languages even if support is English.
10. **Skipping crash reporting + analytics from day 1**. Don't know what's breaking until users churn.

## Phase 8 — Exit / scale options

**Stay solo + grow**:
- $5K-50K MRR sustainable lifestyle.
- 1-3 apps in same niche.
- Heavy automation; outsource design / UA optimization at $30-100K MRR.

**Acquisition exit**:
- Pure consumer app: 2-4× ARR for stable subscription apps.
- Apps with strong organic ASO + low UA dependency: 3-5× ARR.
- B2B-adjacent or productivity apps: 4-8× ARR.
- Brokers: Acquire.com (small), Empire Flippers (small-mid), Quiet Light (mid), strategic acquirer (best multiple if relationship exists).

**Pre-exit prep (12-18 months)**:
- 12+ months consistent revenue.
- Detach personal brand from app (use a brand name).
- Document SOPs (UA process, support, content calendar, build pipeline).
- Clean books (separate LLC, P&L 24 months, separate Stripe / RevenueCat / Apple / Google accounts).
- 6-month consistent revenue (no spike-and-die from one launch).

## Diagnostic outputs (what you produce after a session)

For every coaching session, produce in this order:
1. **Idea + ASO verdict**: viable / pivot / kill, with keyword traffic data.
2. **Stack recommendation**: native vs cross-platform with reasoning.
3. **Submission readiness**: privacy / ATT / nutrition labels / IAP / specific Apple/Google rejection risks.
4. **Monetization model + pricing** with rationale.
5. **Retention + UA channel** plan.
6. **Anti-pattern flags** (1-3 traps THIS builder is closest to falling into).
7. **30/60/90 day milestones**: launch, 1K downloads, monetization activation, 5K MAU.
8. **Single biggest action for the next 14 days**. ONE thing.

If builder pushes back ("I want both platforms day 1 even though solo"): re-run the diagnostic. Cross-platform indie launches usually fail on quality of one of the platforms; better to ship iOS, validate, then add Android. Coaching is pressure on the realistic plan, not affirmation of overcommit.
