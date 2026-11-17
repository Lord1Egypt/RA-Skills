# Playbook: applied AI engineering school, cohort-based

Loaded by the direction and build skills alongside `../DOCTRINE.md`. The doctrine is the law. This
file supplies the vertical's facts.

## 1. The real content model

A cohort program is a schedule, a set of deliverables, a rubric, a refund clause and named people.
Every field below is one a prospective student asks before paying, and one a competitor cannot
copy-paste because it is specific to how this program actually runs.

```ts
type Iso = string;                      // "2026-09-14"
type Minutes = number;

interface Program {
  id: string;
  slug: string;
  title: string;                        // "Applied AI Engineering"
  positioning: string;                  // one sentence, what a graduate can build that they could not before
  level: "foundation" | "professional" | "advanced";
  format: "live_online" | "live_in_person" | "hybrid";
  languageOfInstruction: string;
  durationWeeks: number;
  weeklyCommitment: { liveHours: number; asyncHours: number };   // publish both, honestly
  totalContactHours: number;

  /* ---------- who this is for, and who it is not ---------- */
  prerequisites: Array<{
    requirement: string;                // "you can read a Python stack trace and fix it"
    hard: boolean;                      // hard prerequisites gate admission, soft ones are advisory
    selfCheckUrl?: string;              // a real task the applicant can attempt in 20 minutes
  }>;
  notForYouIf: string[];                // the disqualifiers, printed. Raises conversion, cuts refunds
  expectedBackground: string[];         // "backend engineer, 2+ years", "data analyst moving to engineering"

  /* ---------- what it teaches ---------- */
  outcomes: Array<{
    statement: string;                  // "ship a retrieval service over 2,000 of your own documents"
    evidencedBy: string;                // the artifact that proves it, by module id
  }>;
  outOfScope: string[];                 // what this program deliberately does not cover
  modules: Module[];
  capstone: Capstone;
  toolchain: Array<{
    name: string;                       // "PostgreSQL", "pgvector", "Anthropic API", "Modal"
    version: string;                    // pinned. "latest" reads as a curriculum that is not maintained
    role: string;                       // why this one, in one clause
    costToStudent?: { amount: number; currency: string; note: string };  // API credits are a real cost
    alternativeAllowed: boolean;
  }>;
  repositoryTemplateUrl?: string;       // the repo students actually clone. Public, or a screenshot of it

  /* ---------- how it is assessed ---------- */
  assessment: {
    rubric: RubricCriterion[];
    passingBar: string;
    reviewCadence: "weekly" | "biweekly";
    reviewFormat: string;               // "one hour, everyone presents, recorded"
    feedbackTurnaroundHours: number;
    retakePolicy: string;
  };
  credential?: {
    kind: "certificate" | "none" | "accredited";
    issuedBy: string;
    verifiableUrl?: string;             // a real verification endpoint, or drop the field
    accreditationBody?: string;
    fundingEligibility?: string[];      // e.g. Bildungsgutschein, employer L&D, veterans funding
  };
}

interface Module {
  id: string;                           // "m04"
  index: number;
  weekRange: [number, number];
  title: string;                        // "Retrieval that survives contact with real documents"
  thesis: string;                       // the one idea, one sentence
  deliverable: {
    name: string;                       // "a retrieval service with a 60-question eval set"
    artifactType: "repository" | "service" | "dataset" | "eval_harness" | "writeup" | "deployment";
    acceptanceCriteria: string[];       // checkable, not adjectives
    estimatedHours: number;
  };
  sessions: Session[];
  concepts: string[];                   // named concepts, not tool logos
  commonFailure: string;                // what most students get wrong here, from having run it before
  readings: Array<{ title: string; author: string; url: string; required: boolean; minutes: number }>;
  prerequisiteModuleIds: string[];
}

interface Session {
  id: string;
  kind: "lecture" | "workshop" | "review" | "office_hours" | "guest" | "lab";
  title: string;
  durationMinutes: Minutes;
  liveAt?: Iso;                         // with an IANA timezone, not "evenings"
  timezone: string;                     // "Europe/Berlin"
  recorded: boolean;
  recordingRetentionMonths?: number;
  instructorIds: string[];
  materials: Array<{ kind: "slides" | "notebook" | "repo" | "dataset" | "transcript"; url?: string }>;
}

interface Capstone {
  brief: string;
  constraints: string[];                // "must serve real traffic", "must have a cost ceiling"
  durationWeeks: number;
  reviewedBy: string[];                 // named reviewers, external if possible
  publicDemoDay: boolean;
  examples: Array<{                     // real past projects only, with permission
    title: string;
    studentName?: string;               // omit or initial where consent is limited
    repoUrl?: string;
    demoUrl?: string;
    oneLine: string;
    cohortId: string;
  }>;
}

interface RubricCriterion {
  name: string;                         // "Evaluation", "Cost awareness", "Failure handling"
  weight: number;
  levels: Array<{ label: "not yet" | "meets" | "exceeds"; descriptor: string }>;
}

interface Instructor {
  id: string;
  name: string;
  photo: string;
  role: string;
  shipped: Array<{                      // systems, not employers. This is the credibility field
    what: string;                       // "the retry and dead-letter path in <system>"
    where: string;
    scale?: string;                     // "roughly 40k requests a day", only if publishable
    url?: string;
  }>;
  teachesModuleIds: string[];
  writing?: Array<{ title: string; url: string }>;
  availabilityNote?: string;            // "in every Thursday review", or say they are a guest
}

interface Cohort {
  id: string;                           // "c07"
  programId: string;
  startsOn: Iso;
  endsOn: Iso;
  applicationsCloseOn: Iso;
  capacity: number;                     // a number, because "small cohort" is not one
  seatsRemaining: number;
  status: "open" | "waitlist" | "closed" | "running" | "completed";
  liveSchedule: Array<{ weekday: 1|2|3|4|5|6|7; startLocal: string; durationMinutes: Minutes }>;
  timezone: string;
  cohortLanguage: string;
  instructorIds: string[];
  teachingAssistantRatio?: string;      // "1 TA per 8 students"
}

interface Admission {
  steps: Array<{ index: number; name: string; whatHappens: string; typicalDays: number }>;
  applicationFields: string[];          // keep this list short and publish it
  technicalScreen?: { format: string; durationMinutes: Minutes; whatIsAssessed: string[] };
  decisionSlaDays: number;
  acceptanceNote?: string;              // if you publish a rate, it must be real and dated
}

interface Pricing {
  listPrice: { amount: number; currency: string; taxNote: string };  // "plus 19% VAT" or "incl. VAT"
  paymentOptions: Array<
    | { kind: "upfront"; discountPercent?: number }
    | { kind: "instalments"; count: number; amountEach: number; feePercent: number }
    | { kind: "employer_invoice"; leadTimeDays: number; poAccepted: boolean }
    | { kind: "deferred"; trigger: string; capAmount: number; termMonths: number }
  >;
  scholarships?: Array<{ name: string; criteria: string; seats: number; deadline: Iso }>;
  additionalCosts: Array<{ item: string; estimate: string }>;   // API credits, cloud, a laptop spec
  refundPolicy: {
    fullRefundBeforeDay: number;        // relative to cohort start
    partialSchedule: Array<{ beforeDay: number; refundPercent: number }>;
    conditions: string;
    quotedVerbatim: string;             // the exact contract sentence, printed
  };
  deferralPolicy: { allowed: boolean; feeAmount?: number; noticeDays: number; maxDeferrals: number };
  guarantee?: {                          // only if it exists and is contractual
    statement: string;
    conditions: string[];
    claimProcess: string;
    contractUrl: string;
  };
}

interface Alumnus {
  name?: string;
  cohortId: string;
  before: string;                       // role before, in their own words
  after?: string;                       // only if verifiable and consented
  projectUrl?: string;
  quote?: { body: string; consentedAt: Iso; verifiedBy: "linkedin" | "email" | "video" };
}
```

## 2. The surfaces

| Surface | Mode | Job |
|---|---|---|
| Home | Persuade | State what a graduate can build, name the next cohort date, route to the syllabus in one action. |
| Program overview | Persuade | Carry decisions 1 through 4 below in a single scroll, with the syllabus reachable throughout. |
| Syllabus / curriculum | Read | Week by week, with the deliverable and its acceptance criteria for each. The page that converts engineers. |
| Module detail | Read | Thesis, concepts, deliverable, readings, the named common failure. |
| Instructors | Persuade | Systems shipped, not employers listed. Which modules each one is actually in. |
| Projects / capstone gallery | Experience | Real repos and demos from past cohorts, with cohort ids and dates. |
| Admissions | Operate | The steps, the fields, the screen, the decision window. |
| Pricing and financing | Operate | Total, instalments, refund schedule quoted verbatim, additional costs itemised. |
| Cohort schedule | Operate | Dates, weekday slots, timezone, capacity, seats remaining, application close. |
| Apply | Operate | The shortest form that can produce a decision. Progress visible, save and resume. |
| FAQ | Read | Only questions that were actually asked. Sorted by how often. |
| Student handbook / policies | Read | Attendance, deferral, code of conduct, recording retention, data handling. |
| Open resources | Read | One genuinely useful public artifact. The strongest single acquisition surface in this vertical. |

## 3. The decision sequence

| # | Decision | What must be on screen |
|---|---|---|
| 1 | Am I the right person for this? | Hard prerequisites, the `notForYouIf` list, a self-check task the visitor can attempt now |
| 2 | What will I be able to build that I cannot build now? | Outcomes, each bound to the artifact that evidences it |
| 3 | What actually happens in a week? | Weekly commitment split live and async, the weekday slots with a timezone, the review format |
| 4 | Is the curriculum real or a list of tool names? | Module deliverables with acceptance criteria, pinned tool versions, the repository template |
| 5 | Who teaches it and have they shipped? | Systems built with links, which modules they are in, whether they are present or a guest |
| 6 | Can I afford the time? | Total contact hours, deliverable hour estimates, the deferral policy |
| 7 | Can I afford the money? | Price with tax treatment, instalment terms with fee, additional costs, employer invoicing |
| 8 | What if it goes wrong? | Refund schedule by day, quoted verbatim, deferral terms, what happens if I miss reviews |
| 9 | When does it start and is there room? | Cohort start, application close, capacity as a number, seats remaining |

Mobile order differs, and why:

- **Cohort date, price and apply must be reachable in one thumb reach on mobile**, as a persistent
  bar. On desktop those live in a sticky sidebar next to the syllabus, so the reader compares
  commitment against cost continuously without a bar covering content.
- **The syllabus becomes an accordion on mobile with module 1 expanded.** A fully collapsed accordion
  is an empty page and it is the most common self-inflicted wound in this vertical.
- **Prerequisites move above outcomes on mobile.** A visitor who is not qualified should find that
  out in the first screen, not after four. On desktop the two sit side by side and the order stops mattering.
- **Instructor detail collapses to name, one shipped system, and the modules taught.** Full bios go
  to a separate route so the back button behaves.
- **The application form is one field per screen on mobile with a saved-progress indicator**, and a
  single scrolling page on desktop. A 14-field wall on a phone is where applications die.

## 4. The trust problem

This buyer is technical, has seen the bootcamp collapse cycle, and assumes the program is a wrapper
around public documentation. They will attempt to falsify the claims before applying.

| Suspicion | Real evidence that answers it |
|---|---|
| "This is prompt engineering with a certificate" | A published syllabus where every week names a shipped artifact and its acceptance criteria, plus an out-of-scope list that admits what is not covered |
| "The instructor has never run this in production" | Systems named with links, a specific mechanism attributed ("the retry path in X"), their public writing, their commit history |
| "The teaching is prerecorded and the live part is a Q and A" | Session kinds and durations published per module, one full unedited recorded session available before payment, the review format described as a mechanic |
| "The cohort is 300 people in a Discord" | Capacity as a number, TA ratio, the review format that only works at that size ("one hour, everyone presents") |
| "The curriculum is stale" | Pinned tool versions with a last-reviewed date, the public repository template with visible commit dates |
| "The job guarantee is a legal fiction" | The contract linked and the clause quoted verbatim, with its conditions and claim process. If there is no guarantee, say so plainly rather than implying one |
| "The projects in the gallery are the instructor's" | Repos with cohort ids, commit histories, student attribution where consented, demo URLs that resolve |
| "I will lose my money if life happens" | The refund schedule as a table by day, the deferral policy with notice period and fee, quoted from the contract |
| "The outcomes are survivorship" | Publish the cohort size alongside any outcome figure, dated. An outcome without a denominator is not evidence |

Never fabricate: placement rates, salary figures, alumni employers, partner logos, accreditation, or
a student quote. If an outcome cannot be sourced, the correct move is to ship the syllabus harder,
not to invent a statistic.

## 5. Component picks

This is the one vertical where technical-looking components are correct, on the strict condition
that they carry real information. A diagram that does not draw the actual pipeline is chrome.

| Component | Registry | Real cost | Use |
|---|---|---|---|
| `circuit-board` | `@componentry` | zero runtime deps, broken `cn` import, fix on install | The standout. A real node-and-edge primitive with `status: "active" \| "processing" \| "error"` per node. Draw the actual RAG pipeline, agent loop or eval harness the students build. Node labels must be the real stage names |
| `silk-aurora` | `@componentry` | raw WebGL, zero deps | Hero. Dark and composed without cliche. Own the type in `children`, never its title props |
| `closing-plasma` | `@componentry` | raw WebGL, zero deps | Enrolment band in the footer, matching the hero without a second library |
| `ascii-effect` | `@componentry` | zero deps | Instructor portrait or the program mark. Terminal culture, genuinely uncommon |
| `split-flap-display` | `@componentry` | zero deps | Cohort start date, seats remaining, application close. Mechanical rather than SaaS-generic. Only for figures that are real |
| `mac-keyboard` | `@componentry` | needs `lucide-react`, which it does not declare | CLI and shortcut teaching visuals. Instructional rather than decorative |
| `scroll-choreography` | `@componentry` | framer-motion, broken `cn` import | Module sections with four converging artifacts. Rigid API, exact fit when a module has four deliverables |
| `@ncdai/contribution-graph` | `@ncdai` | small, no live API call | The "your first 12 weeks" commitment visual, driven by the real session schedule. Prefer this over `github-calendar`, which hits a live third-party API |
| `@kibo-ui/code-block` | `@kibo-ui` | shiki | Real, selectable, copyable code. Never ship code as an image |
| `@kibo-ui/gantt` | `@kibo-ui` | moderate | The cohort schedule as a real timeline on the desktop schedule surface |
| `@kibo-ui/tree` | `@kibo-ui` | small | The repository template structure, expandable |
| `@bklit/line-chart` | `@bklit` | visx | An eval-score-over-iterations plot from a real module dataset. Label it as course material |
| **Asciify** | `@canvas-ui` | `drawElement` origin trial token | Signature effect. `charset: "binary", baseStrength: 0.08, radius: 0.35`. The page reads 8 percent terminal with a cursor lens pushing it to full. One draw call |
| **Laser** | `@canvas-ui` | origin trial token | Syllabus scroll: content prints in from behind a beam, beam width DOM-measured to the text column. `reactivity: 1.5` |
| **Glass** | `@canvas-ui` | origin trial token | Documentation and reference surfaces, `targets: "code, pre, h2"`. A magnifier over code blocks is useful, not decorative |
| **Grid** | `@canvas-ui` | origin trial token, mid-weight | "How the platform works", tiles rippling over a real architecture diagram, `idleRipples: 4` so it lives at frame zero |

### AVOID

| Component | Reason |
|---|---|
| `matrix-rain` | The single most exhausted "we do AI" cliche. Using it spends the exact credibility the page is buying |
| `particle-galaxy` | Neural-network-as-nebula, the second most exhausted one, and 600 KB of three.js |
| `dither-prism-hero` | three plus R3F on a page that converts on mobile, and its welded `uMouseIntensity` destroys any dark palette |
| `github-calendar` | Calls a live third-party API at render. It fails silently, rate limits, and leaks a dependency into your uptime |
| `border-beam`, `shimmer-button`, `hyper-text` | Every AI bootcamp landing page already has these. If one is used, use one, restyled past recognition |
| `eye-tracking`, `music-player`, `flight-status-card` | Off-topic novelty on a page selling rigor |
| **Cloth**, **Droplets**, **Clouds**, **Blaze** | Wrong register. Reads as decoration where the brief is capability |
| **Hex Float** | Owns the frame budget and the load time. Acceptable on one non-funnel showcase page, never on the enrolment path |
| `circuit-board` used decoratively | If the nodes do not carry real pipeline stage names, it is a background pretending to be a diagram, which is worse than a background |

## 6. The category rut

**What every AI school site looks like.** Near-black hero with a particle mesh or matrix rain. A
headline in a violet-to-blue gradient: "Learn AI Engineering" or "Become an AI Engineer". Two buttons,
one filled, one ghost. A greyscale logo bar of tools (OpenAI, LangChain, Pinecone, Hugging Face)
labelled "the stack you will master". A 12-row fully collapsed curriculum accordion where each row
reads "Week 5: Agents". Three instructor cards, circular avatars, "ex-Google", "ex-Meta". A metric
band: "500+ graduates", "94% completion", "3x salary increase", none sourced. A testimonial grid with
five stars. A Discord CTA. Inter or Space Grotesk. Glass cards with a 1px border under a soft glow.

**The obvious contrarian move, also excluded.** White page, LaTeX-flavoured serif, numbered
theorem-style sections, a monospace abstract, no images, "A Rigorous Programme in Applied Machine
Learning". Academic-journal cosplay is what the category produces when told to look serious, so it is
a prior too. So is its cousin: the terminal-green monospace page with a blinking cursor.

**Four material worlds that are neither:**

1. **A bound chemistry lab notebook.** Pre-numbered pages, a date and an objective at the top of each,
   observations in the left column and calculations in the right, errors struck through with a single
   line and initialled, a witness signature at the bottom of the page. The module page becomes a lab
   entry, and the struck-through error is the honest failure mode this vertical usually hides.
2. **A flight training syllabus and checkride standards booklet.** Every lesson has objectives,
   completion standards with tolerances (plus or minus 100 feet, plus or minus 10 knots), an
   instructor endorsement block, and a stage check. Acceptance criteria stop being adjectives and
   become a tolerance table. Prerequisites become endorsements.
3. **A Heathkit electronics assembly manual.** Numbered steps with a checkbox beside each, exploded
   diagrams, "if the meter reads other than 4.5 V, see step 41", a parts inventory to be counted
   before starting. The onboarding and toolchain surfaces become an assembly manual with a bill of materials.
4. **A machine shop job traveller.** A card that follows the part through operations, each op stamped
   by the operator who did it, with setup notes, tooling, and inspection sign-off. The student's
   deliverable travels through the cohort with visible operations and sign-offs.
5. **A topographic survey sheet.** Contours, benchmarks with elevations, a legend, a declination
   diagram, a grid reference system, a revision date in the margin. Curriculum as terrain with
   measured elevation rather than a list of weeks.

## 7. Copy register

How working engineers who teach talk. Specific, numeric, willing to name what the program will not do.

Sounds right:

- "Week 4 you ship a retrieval service over 2,000 of your own documents, measured against a 60-question eval set you wrote in week 3."
- "Prerequisite: you can read a stack trace and you have written Python that another person ran in production."
- "The cohort is capped at 24, because the Thursday review is one hour and everyone presents."
- "We use Postgres with pgvector, not a managed vector database, because you need to see the index."
- "You will not learn prompt engineering. You will learn evaluation, retrieval, cost, and what to do when the model is wrong."
- "Miss two consecutive reviews and we move you to the next cohort at no charge. That is the policy, not a favour."
- "Budget 40 to 60 EUR of API credits across the twelve weeks. We give you the cost ceiling script in week 1."
- "The instructor's on-call system is at <link>. The retry logic you will build in week 7 is that one, simplified."

Sounds like a template, do not ship:

- "Master AI and transform your career."
- "Learn from industry-leading experts."
- "Join a thriving community of builders."
- "Hands-on, project-based learning."
- "No experience necessary. Anyone can learn AI."

## 8. The specific failure modes

1. **The fully collapsed curriculum accordion.** The page's entire substance is behind twelve closed
   rows, so at frame zero the page says nothing. Open the first module, always.
2. **Tool logos standing in for a curriculum.** A logo bar is a list of nouns. Engineers read
   deliverables and acceptance criteria and nothing else.
3. **Week titles with no deliverable.** "Week 5: Agents" is not information. "Week 5: an agent loop
   with a tool budget, a timeout and a replay log" is.
4. **Price behind a call.** On a program under roughly 5,000 this reads as a sales-call funnel and
   loses the exact audience that would have paid. Publish the number.
5. **The 14-field application form before any pricing.** The form is a cost imposed before value is
   established. Publish price, syllabus and cohort dates first, form last, shortest possible.
6. **Instructor bios that name employers, not systems.** "ex-Google" is a filter, not evidence. The
   thing built, the mechanism, the link.
7. **Code as an image.** Not selectable, not copyable, not readable at 390px, not indexed. This is the
   single fastest way to lose a technical reader's trust.
8. **A cohort date in the past still on the page.** Instantly reads as abandoned. Cohort status must
   be a real state with a waitlist path, not a hardcoded string.
9. **Unsourced outcome metrics.** "94% completion" with no denominator and no date. One unsourced
   number makes every sourced one on the page look invented too.
10. **`circuit-board` as decoration.** Nodes with no real stage names is chrome pretending to be a
    diagram on a page whose whole argument is that it teaches real systems.
11. **Dark palette with 3.8:1 body text.** The hero drove the palette and the reading surfaces
    inherited it. Curriculum pages are Read mode: measure the contrast on the computed styles.
12. **No timezone on a live schedule.** "Tuesdays at 19:00" is meaningless to a third of the audience,
    and it is the first question in every FAQ that has one.
13. **Full-bleed effects on the syllabus.** Read mode has a near-zero effect budget. The budget belongs
    to the home and the projects gallery.
14. **The recording-retention question left unanswered.** Working students buy on it. Publish the
    number of months and whether it survives the cohort ending.
