# Playbook: go-to-market and UGC ad creative school

Loaded by the direction and build skills alongside `../DOCTRINE.md`. The doctrine is the law. This
file supplies the vertical's facts.

## 1. The real content model

The teachable unit in this vertical is not a lesson, it is an ad that ran. Everything below exists so
the page can show a real creative, prove it ran, break down why it worked, and hand the student the
brief and spec to make one. The `adLibraryId` field is the single most important field in this file:
it is the only claim on the entire page a stranger can verify without trusting you.

```ts
type Iso = string;
type Platform = "meta" | "tiktok" | "youtube" | "snapchat" | "pinterest" | "reddit" | "linkedin";

interface AdAsset {
  id: string;
  /* ---------- proof that it existed ---------- */
  platform: Platform;
  adLibraryId?: string;                  // Meta Ad Library ID. Publicly resolvable, publish it
  adLibraryUrl?: string;                 // the full permalink a visitor can open
  creativeCenterUrl?: string;            // TikTok Creative Center equivalent
  ranFrom?: Iso;
  ranTo?: Iso;
  advertiser: { name: string; permissionOnFile: boolean; logoUrl?: string };
  archivedCopy: { videoSrc?: string; posterSrc: string; capturedAt: Iso };  // ads get deleted

  /* ---------- what it physically is ---------- */
  format: "video" | "static" | "carousel" | "collection" | "story";
  aspectRatio: "9:16" | "4:5" | "1:1" | "16:9";
  resolution: { width: number; height: number };
  durationS?: number;
  hasSound: boolean;
  burnedInCaptions: boolean;
  languageCode: string;
  shotOn: "phone" | "camera" | "screen_capture" | "mixed" | "ai_generated";
  productionCost?: { amount: number; currency: string; note: string };

  /* ---------- the craft, broken down ---------- */
  hook: {
    firstFrameDescription: string;
    spokenOpener?: string;               // the literal first line
    onScreenText?: string;
    archetype: "problem_agitate" | "pattern_interrupt" | "pov" | "unboxing" | "testimonial"
             | "listicle" | "comparison" | "green_screen" | "stitch" | "day_in_life" | "founder_direct";
    lengthMs: number;                    // where the hook ends and the body begins
  };
  beats: Array<{ atS: number; label: string; purpose: "retain" | "prove" | "objection" | "cta" }>;
  cta: { spoken?: string; onScreen?: string; atS: number; destination: "pdp" | "lp" | "app" | "form" | "dm" };
  objectionsAddressed: string[];
  socialProofDevice?: "review_overlay" | "duet" | "ugc_stack" | "before_after" | "none";

  /* ---------- performance, only where it is real and attributable ---------- */
  performance?: {
    source: "meta_ads_manager" | "tiktok_ads_manager" | "triple_whale" | "northbeam" | "client_reported";
    sourceScreenshot?: string;           // with the account name visible, uncropped
    window: { from: Iso; to: Iso };
    spend?: { amount: number; currency: string };
    impressions?: number;
    hookRatePercent?: number;            // 3s views / impressions
    holdRatePercent?: number;            // thruplays / 3s views
    outboundCtrPercent?: number;
    cpm?: number;
    cpa?: number;
    roas?: number;
    isIllustrative: boolean;             // true means synthetic teaching data, and it must be labelled
  };
}

interface Teardown {
  id: string;
  adAssetId: string;
  authorId: string;                       // who did the teardown, an instructor
  thesis: string;                         // one sentence: why this worked
  annotations: Array<{ atS: number; note: string; frameSrc?: string }>;
  whatToSteal: string[];
  whatNotToCopy: string[];                // the parts that only worked for that brand
  rebuildBrief?: string;                  // a brief for the student to make their own version
  publishedAt: Iso;
  isPublic: boolean;                      // teardowns are the acquisition surface, publish some
}

interface DeliverableSpec {
  name: string;                           // "TikTok in-feed, 9:16, 30s"
  platform: Platform;
  placements: string[];                   // "Reels", "Stories", "In-feed", "Explore"
  aspectRatio: "9:16" | "4:5" | "1:1" | "16:9";
  resolution: { width: number; height: number };
  maxDurationS: number;
  maxFileMb: number;
  container: "mp4" | "mov";
  codec: string;
  safeZones: { topPx: number; bottomPx: number; leftPx: number; rightPx: number; note: string };
  captionRequirement: "burned_in" | "srt" | "either";
  audioRequirement: "must_work_muted" | "sound_on";
  brandAssetsProvided: string[];
  namingConvention: string;               // "brand_concept_hook_variant_date.mp4"
}

interface Brief {
  id: string;
  brandId: string;
  campaign: string;
  objective: "prospecting" | "retargeting" | "retention" | "launch";
  audience: { description: string; painPoint: string; currentSolution: string; objection: string };
  offer: string;
  mandatoryClaims: string[];
  prohibitedClaims: string[];             // the compliance half, which every course skips
  toneReferences: Array<{ url: string; whatToTake: string }>;
  concepts: Array<{ name: string; hookIdea: string; angle: string }>;
  deliverableSpecIds: string[];
  variantCount: number;
  revisionRounds: number;
  dueOn: Iso;
  usageRights: UsageRights;
  rate: { amount: number; currency: string; perDeliverable: boolean };
}

interface UsageRights {
  organic: boolean;
  paid: boolean;
  whitelisting: boolean;                  // Spark Ads / Partnership Ads: running from the creator handle
  termDays: 30 | 60 | 90 | 180 | 365 | -1;   // -1 is perpetual, price it accordingly
  territory: string[];
  exclusivityDays: number;                // category exclusivity, the thing creators forget to price
  creditRequired: boolean;
  renegotiationTerms?: string;
}

interface RateCardLine {
  deliverable: string;
  baseRate: { amount: number; currency: string };
  modifiers: Array<{ condition: string; multiplier: number }>;  // whitelisting, exclusivity, term
  includesRevisions: number;
  rushFeePercent?: number;
}

/* ---------- the GTM half ---------- */
interface GtmPlay {
  id: string;
  name: string;                           // "Founder-led outbound into a narrow ICP"
  motion: "plg" | "sales_led" | "community_led" | "paid_acquisition" | "partnerships" | "outbound";
  icp: { segment: string; sizeBand: string; trigger: string; buyer: string; blocker: string };
  positioning: { category: string; against: string; claim: string; proof: string };
  channels: Array<{ name: string; role: "acquire" | "nurture" | "convert" | "expand"; cadence: string }>;
  funnel: Array<{ stage: string; definition: string; instrumentedBy: string }>;
  economics: {
    aov?: number; cac?: number; paybackMonths?: number; mer?: number;
    isIllustrative: boolean;              // if this is a worked example, label it
  };
  artifacts: Array<{ kind: "brief" | "sequence" | "landing_page" | "sheet" | "dashboard"; url?: string }>;
  failureModes: string[];
}

/* ---------- the program ---------- */
interface Program {
  slug: string;
  title: string;
  forWhom: Array<"freelance_creator" | "in_house_marketer" | "agency_owner" | "founder" | "media_buyer">;
  notForYouIf: string[];
  durationWeeks: number;
  weeklyCommitment: { liveHours: number; productionHours: number };
  format: "live_cohort" | "self_paced" | "hybrid";
  outputQuota: { hooksPerWeek: number; editsPerWeek: number; postedPerWeek: number };  // the real workload
  modules: Array<{
    index: number;
    title: string;
    thesis: string;
    deliverable: string;                  // an ad, a brief, a rate card, a funnel, not "a worksheet"
    teardownIds: string[];
    critiqueFormat: string;               // "live, on your own footage, 8 minutes each"
  }>;
  toolsTaught: Array<{ name: string; version?: string; costToStudent?: string; required: boolean }>;
  adSpendRequired?: { amount: number; currency: string; note: string };   // say it plainly, it is real
  portfolioOutcome: string;               // what the student walks out holding
  swipeFile: { entryCount: number; publicSampleUrl?: string; updateCadence: string };
  community: { platform: string; size?: number; moderated: boolean; retentionAfterProgram: string };
}

interface Offer {
  listPrice: { amount: number; currency: string; taxNote: string };
  paymentOptions: Array<{ kind: "upfront" | "instalments"; count?: number; amountEach?: number; feePercent?: number }>;
  deadline?: { closesAt: Iso; reason: string };   // a real reason, e.g. the cohort starts
  bonuses: Array<{ name: string; description: string; realStandaloneValue?: number }>;
  guarantee?: { statement: string; conditions: string[]; windowDays: number; claimProcess: string; contractUrl: string };
  refundPolicy: { quotedVerbatim: string; windowDays: number; conditions: string };
}

interface Proof {
  kind: "ad_library_link" | "platform_screenshot" | "student_ad" | "brand_permission" | "video_testimonial";
  subject: string;
  url?: string;                           // resolvable, and it must resolve
  capturedAt: Iso;
  attributedTo: { name: string; consentedAt: Iso; role: string };
  accountNameVisible: boolean;            // an uncropped dashboard or it is not proof
  claimSupported: string;                 // the exact sentence on the page this proof backs
}
```

## 2. The surfaces

| Surface | Mode | Job |
|---|---|---|
| Home / sales page | Persuade | Show a real ad, prove it ran, name the offer, in that order. |
| Teardown library | Read | The acquisition engine. Public breakdowns of ads with their ad library links. |
| Teardown detail | Experience | The ad playing, annotated on a timeline, with the rebuild brief attached. |
| Creative wall | Experience | Student and instructor work, each frame linking to the ad it came from. |
| Curriculum | Read | Modules by deliverable, with the weekly output quota stated. |
| Who this is for | Persuade | Four audience paths (creator, marketer, agency, founder) with different first modules. |
| Proof | Persuade | Every claim on the site with its evidence, one page, dated. Rare, and it converts. |
| Offer and pricing | Operate | Total, instalments, what closes when and why, refund terms verbatim. |
| Rate card and rights | Read | The commercial half creators are never taught. Usable as a template. |
| Spec sheet | Read | Deliverable specs by platform and placement, with safe zones. A genuinely useful public asset. |
| Enrol / checkout | Operate | Zero effects, one screen, price visible throughout. |
| Free resource | Persuade | One brief template, spec sheet or swipe sample in exchange for an email. |

## 3. The decision sequence

| # | Decision | What must be on screen |
|---|---|---|
| 1 | Does this person actually do this, or only teach it? | A real ad in the first viewport with its ad library link open-able |
| 2 | Is this for my situation? | Named audience paths and the `notForYouIf` list, not a generic "for anyone" |
| 3 | What do I physically get? | Module deliverables, the weekly output quota, the critique format, the portfolio outcome |
| 4 | Is the proof verifiable? | Ad library links, uncropped dashboards with account names, dated student ads |
| 5 | What does it cost me beyond money? | Hours per week split live and production, required ad spend, required tools |
| 6 | What is the price and the terms? | Price with tax, instalment count and fee, what the deadline is and why it exists |
| 7 | What if it does not work? | Refund window quoted verbatim, guarantee conditions and claim process, or an honest absence |
| 8 | When does it start? | Cohort date, close date, and what happens if I miss it |

Mobile order differs, and why:

- **Proof precedes price on mobile, always.** The mobile visitor arrives from a paid ad, cold, and
  will not scroll past an offer they have no reason to trust. On desktop the offer stack and the proof
  band can sit adjacent in two columns, so ordering matters less.
- **The hero ad must be muted, captioned and poster-loaded.** Autoplay with sound on mobile is an
  instant exit and, on some devices, a system-level block that leaves a dead frame.
- **The offer stack collapses to price, what is included as a short list, and one action.** Bonus
  stacks with struck-through values read as a scam on a 390px screen where they cannot be scanned.
- **The creative wall becomes a horizontal scroller with 4:5 frames on mobile**, not a tilted grid.
  A tilt effect on a 390px viewport crops the ad and loses the hook frame, which is the only frame
  that matters.
- **Video testimonials become a poster plus a transcript excerpt on mobile.** A visitor who will not
  press play must still be able to read the claim.

## 4. The trust problem

This audience sells persuasion for a living. They read the page as a piece of creative and they are
looking for the tell. They assume the teacher's income comes from teaching, not from doing.

| Suspicion | Real evidence that answers it |
|---|---|
| "The screenshots are fabricated or cherry-picked" | Meta Ad Library and TikTok Creative Center permalinks. A stranger can open them and see the ad, the advertiser and the run dates without trusting you. This is the strongest evidence available in this vertical and almost nobody uses it |
| "That dashboard number is not theirs" | Uncropped platform screenshots with the account name and date range visible, plus the spend alongside the return. A return figure without a spend figure is not a figure |
| "The students are affiliates" | Student work shown as ads that ran, with their own ad library entries, cohort id and date. A quote is a quote, an ad that ran is evidence |
| "The results came from someone else's budget" | Name the brand, with permission on file, and state who funded the spend |
| "They teach virality, not performance" | Publish a full teardown including the beats and the objection handling, and publish one ad that failed with the reason |
| "The guarantee is theatre" | The contract linked, the clause quoted, the conditions listed, the claim process named. If there is no guarantee, saying so plainly outperforms implying one |
| "The deadline is fake" | A deadline with a stated structural reason (the cohort starts, the critique groups are formed on that date). A timer that resets on reload destroys the entire page |
| "This is a rebranded dropshipping course" | The rate card, the usage rights model, the compliance section on prohibited claims. Nobody selling a rebrand knows what category exclusivity costs |

Never fabricate: revenue screenshots, ad account performance, student earnings, brand logos, "as seen
in", follower counts, or a testimonial. In this vertical fabricated proof is not only a doctrine
violation, it is the exact accusation the audience arrives with.

Illustrative teaching data is allowed and useful, on the condition that `isIllustrative` is true and
the label is visible on the surface, not in a tooltip.

## 5. Component picks

Page weight is revenue here, because the traffic is paid. Motion should read expensive and fast, and
every heavy component has to be paid for out of the same budget as the ad frames themselves.

| Component | Registry | Real cost | Use |
|---|---|---|---|
| `webgl-liquid` | `@componentry` | raw WebGL, zero deps beyond `clsx` and `tailwind-merge` | Hero backdrop with configurable reveal timing so the headline lands after the shader settles. Own the type in `children` |
| `scroll-tilted-grid` | `@componentry` | framer-motion | The creative wall, desktop only. Ad frames tilting into focus is literally what this does. Best in class here |
| `letter-cascade` | `@componentry` | framer-motion, undeclared, and a broken `cn` import | One headline, once. Letters scatter and reassemble. High impact, and it stays DOM text |
| `sticky-scroll-cards` | `@componentry` | framer-motion, ships Unsplash defaults, replace them | The offer stack: modules pinning and scaling. Classic high-ticket motion, used once |
| `testimonial-marquee` | `@componentry` | pure CSS, drop its phantom `framer-motion` declaration | Proof band. Zero runtime animation cost. Every card links to its source |
| `text-repel` | `@componentry` | framer-motion, undeclared, broken `cn` import | One interactive headline. DOM text, so it stays selectable. Needs a Law 3 idle resolution declared |
| `orbit-card-stack` | `@componentry` | framer-motion | Tier or payment-option picker. `onActiveChange` wires into checkout state |
| `magnet-lines` | `@componentry` | ~3 KB, zero deps | Section divider that reads designed rather than templated |
| `@kibo-ui/stories` | `@kibo-ui` | small | The teardown library as a stack of vertical video cards, which is the native grammar of the medium |
| `@kibo-ui/video-player` | `@kibo-ui` | media-chrome | The ad player. Real controls, real captions track, muted by default, poster required |
| `@kibo-ui/comparison` | `@kibo-ui` | small | Before and after on a rebuilt ad. The single most legible teaching device in this vertical |
| `@kibo-ui/announcement` | `@kibo-ui` | tiny | Cohort close notice, if it is real |
| `@bklit/line-chart`, `@bklit/bar-chart` | `@bklit` | visx | Retention curves and hook-rate comparisons. Only with real or explicitly labelled illustrative data |
| **Peel** | `@canvas-ui` | `drawElement` origin trial token | The teardown card: front is the creative frame, `under` is the annotated breakdown (hook, retention, CTA). `side: "left", mode: "hover"`. The strongest content pattern available for this niche |
| **Magnify** | `@canvas-ui` | origin trial token | Critique tool over a real ad frame, `hud: 1, readout: true, grid: true`. Reads as an analysis instrument rather than a filter |
| **Shatter** | `@canvas-ui` | origin trial token, mid-weight | One place only: the before-and-after where a weak ad breaks into the rebuilt one. This is the right home for a component that is wrong everywhere else |
| **VHS**, **Glitch** | `@canvas-ui` | origin trial token, cheap | Bounded to a section, never site-wide and never over pricing. Every creator in this audience knows this look from CapCut, which makes it legible and also makes it cheap. Use once, at full strength, inside a boundary |

### AVOID

| Component | Reason |
|---|---|
| `dither-prism-hero`, `particle-galaxy` | 600 KB of three.js on a page bought with paid traffic. Weight is spend |
| `cursor-driven-particle-typography` | The headline must be crawlable and readable on mobile. Canvas text is neither |
| `image-trail` | GSAP for one effect, and it is dead weight on touch, where the traffic lives |
| `command-menu`, `mac-keyboard` | Developer-tool signals on a marketing page. Wrong audience entirely |
| `border-beam`, `shimmer-button`, `pulsating-button`, `interactive-hover-button` | This audience has seen all four on a hundred other course pages this month. They are the tell |
| `matrix-rain`, `circuit-board` | Nothing here is a terminal or a pipeline |
| **Frost**, **Clouds**, **Cloth** | Too soft for the register, and Frost owns the frame budget |
| **Hex Float** | Too slow to load on a page whose only job is conversion speed |
| **VHS** or **Glitch** site-wide | At low strength it becomes the filter left on. At full strength over pricing it reads as a broken page |
| Any canvas-rendered creative wall | The ad frames must link to their ad library entries. Canvas frames cannot be links, which destroys the page's only verifiable proof |

## 6. The category rut

**What every UGC and ads course page looks like.** Near-black background, one acid accent, green or
yellow. Headline at 5 rem: "Make $10k/month with UGC" or "The creative system that scaled us to 7
figures". A video sales letter thumbnail with a large play triangle and a red progress bar. A stack of
testimonial screenshots: green Stripe notification bars, cropped Ads Manager panels, WhatsApp messages
with the name blurred. A countdown timer. A "what you get" checklist with green ticks and struck-through
values summing to "a total value of $4,997, yours today for $997". Three bonus boxes. A payment button
that pulses. A guarantee seal in a gold circle. Inter Black or a condensed grotesk, uppercase.

**The obvious contrarian move, also excluded.** Quiet Swiss editorial: white ground, a thin serif,
generous margins, small tracked labels, "a programme for serious operators", one restrained sentence
per screen, muted greys. This is precisely what the second-tier info product does the moment it wants
to look premium, so it is a prior wearing better clothes. The third reflex, agency-portfolio dark grey
with a huge cursor blob, is also out.

**Five material worlds that are neither:**

1. **A boxing fight poster and undercard bill.** A main event in enormous condensed type, the
   undercard in descending sizes, weight classes, rounds, the venue and date in a band across the
   bottom, a promoter's mark. The offer becomes a card: the main deliverable billed as the headline
   fight, the modules as the undercard, the cohort date as the venue line. Loud is correct here and
   this is loud with a real structural grammar.
2. **A film contact sheet with grease-pencil selects.** Frames in strict rows, frame numbers along the
   edge, circled selects, crossed rejects, a chinagraph annotation in the margin. The creative wall
   becomes a contact sheet, and the teardown annotation becomes a grease-pencil mark. Every frame
   carries its own reference number, which is exactly what a swipe file needs.
3. **A broadcast playout log and traffic sheet.** Time in, duration, spot id, advertiser, break
   position, a dot-matrix printer face, a schedule that runs down the page in fixed columns. The
   curriculum becomes a schedule with durations, and the ad library becomes a log with run times.
4. **A magazine media kit and rate card.** Circulation figures, reader demographics, a rate table by
   size and position, bleed and trim specs, mechanical requirements, closing dates. The deliverable
   spec sheet and rate card surfaces already are this document. Committing to it makes the commercial
   half of the program the visual centre instead of an afterthought.
5. **A screen-print separations proof.** Registration marks, a colour bar, one plate per channel shown
   separately then composited, a pantone chip strip, an approval signature block. Before-and-after
   teardowns become separations: hook plate, retention plate, CTA plate, then the composite.

## 7. Copy register

How people who actually run creative talk. Numeric about time and format, blunt about how much of the
work is repetition, and specific about money.

Sounds right:

- "The hook is the first 1.2 seconds. Everything after it is retention maintenance."
- "You will write 40 hooks a week and cut 12 of them. Most will be bad. That is the mechanism, not a warning."
- "Here is the ad. Here is its Meta Ad Library link, so you can see it ran from March to July and who paid for it."
- "Deliverable: 9:16, 1080x1920, hook at 0.0, nothing in the bottom 480 px because the CTA sits there."
- "Rate card: 3 variations, 2 revisions, 30 days paid usage, no whitelisting. Whitelisting is priced separately, because it is."
- "We do not teach you to go viral. We teach you to make an ad a media buyer will scale."
- "Your first 20 deliverables will be for brands paying under 300 EUR. Price up after the case study, not before."
- "Budget 200 EUR of test spend across the six weeks. If you cannot, take the self-paced version, it does not need it."

Sounds like a template, do not ship:

- "Unlock the secrets of viral content."
- "Turn your phone into a six-figure business."
- "Everything you need to succeed as a creator."
- "Our proven, step-by-step system."
- "Limited spots available. Enrol now before it is too late."

## 8. The specific failure modes

1. **Testimonial screenshots with no source, no date and no alt text.** The entire trust budget spent
   on an image a stranger cannot check. One ad library link outperforms twenty of them.
2. **A video sales letter as the only content.** A visitor who will not press play sees an empty page.
   Every claim the video makes must exist as text on the same page.
3. **Autoplaying video with sound.** Instant exit on mobile, blocked on many devices, and it leaves a
   dead first frame where the hook was supposed to be.
4. **A countdown timer that resets on reload.** One refresh and the page's credibility is gone, along
   with every honest claim on it. If the deadline is real, it has a date and a structural reason.
5. **Page weight over 3 MB on paid traffic.** Every 100 ms of load is paid for twice, in bounced clicks
   and in a worse quality score. Budget the effects against the ad frames.
6. **A creative wall built on canvas.** The frames cannot link to their ad library entries, so the one
   verifiable proof on the site is destroyed by the component that displays it.
7. **Numbers without denominators.** "4.8 ROAS" with no spend, no window and no account. In this
   audience an unattributed number is read as a fabricated one by default.
8. **A bonus stack with struck-through values that were never charged.** The audience prices things
   for a living and recognises this immediately.
9. **The offer stack that hides the price.** A committed form that hides the offer or the action has
   not finished translating. This is the Persuade-mode conversion law and this vertical breaks it most.
10. **Full-bleed VHS or glitch at low strength.** Turned down enough to keep text legible, it becomes
    a filter someone left on. Bounded region at full strength or not at all.
11. **13px text over a full-bleed video.** Unreadable in daylight, which is where a phone is. Text over
    video needs a solid or heavily blurred plate, and the plate is a design decision, not an overlay opacity.
12. **The rate card and rights section missing entirely.** Every course in this category teaches
    shooting and none teach pricing, exclusivity or usage terms. Publishing it is both the strongest
    differentiator and the cheapest one.
13. **Compliance ignored.** Prohibited claims, disclosure requirements and platform ad policy are part
    of the job. A program that never mentions them is teaching students to get accounts banned.
14. **One identical entrance on every section.** Fade-up, 0.6s, stagger 0.1, from the hero to the
    footer. On a page whose subject is attention, uniform motion is a self-inflicted argument against
    the product.
