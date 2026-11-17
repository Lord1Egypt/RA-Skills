# Playbook: independent car dealership, used and EV stock

Loaded by the direction and build skills alongside `../DOCTRINE.md`. The doctrine is the law. This
file supplies the vertical's facts.

## 1. The real content model

Everything a vehicle page needs, typed. A field left out of this model becomes a question the
visitor has to phone in, and the phone call is where the sale is lost.

```ts
type Currency = "EUR" | "CHF" | "GBP" | "PLN";
type DistanceUnit = "km" | "mi";

/** Germany and AT/CH use the margin scheme constantly. Getting this wrong is a legal problem,
 *  not a copy problem. */
type VatStatus =
  | { kind: "deductible"; ratePercent: 19 | 20 | 7.7; netPrice: number }   // MwSt. ausweisbar
  | { kind: "margin_scheme"; statute: "§25a UStG" }                        // differenzbesteuert
  | { kind: "private_seller" };                                            // no VAT line at all

interface Vehicle {
  /* ---------- identity ---------- */
  id: string;                    // internal stock id, also printed on the windscreen card
  stockNumber: string;           // human-facing, e.g. "K-2291"
  vin: string;                   // 17 chars, ISO 3779. Publish last 6 by default, full on request
  make: string;                  // "Volkswagen"
  model: string;                 // "ID.4"
  trim: string;                  // "Pro Performance 77 kWh"
  variantCode?: string;          // HSN/TSN in DE, type approval code elsewhere
  bodyStyle: "hatchback" | "saloon" | "estate" | "suv" | "coupe" | "cabriolet" | "van" | "pickup";
  doors: 2 | 3 | 4 | 5;
  seats: number;
  exteriorColor: { name: string; hex: string; finish: "solid" | "metallic" | "pearl" | "matte" };
  interiorColor: { name: string; material: "cloth" | "part_leather" | "leather" | "vegan" | "alcantara" };

  /* ---------- age and use ---------- */
  modelYear: number;             // 2021
  firstRegistration: string;     // "2021-06" month precision, that is what the papers carry
  buildDate?: string;            // "2021-03", differs from registration on stock cars
  mileage: { value: number; unit: DistanceUnit; readAt: string };  // readAt is the odometer read date
  priorOwners: number;           // Zulassungsbescheinigung Teil II, count of registered keepers
  previousUse: "private" | "company" | "rental" | "driving_school" | "taxi" | "demo" | "press_fleet";
  importHistory: "domestic" | "eu_import" | "non_eu_import";

  /* ---------- drivetrain ---------- */
  drivetrain: "fwd" | "rwd" | "awd";
  transmission: {
    kind: "manual" | "automatic" | "dual_clutch" | "cvt" | "single_speed";
    gears: number;               // single_speed EVs are 1, say so rather than hiding the field
  };
  power: { kw: number; hp: number };            // print both, kW is the legal figure in DE
  torqueNm?: number;
  topSpeedKph?: number;
  zeroToHundredS?: number;

  /* ---------- energy: exactly one of these three ---------- */
  energy:
    | {
        kind: "combustion";
        fuel: "petrol" | "diesel" | "lpg" | "cng";
        displacementCcm: number;
        cylinders: number;
        tankLitres: number;
        consumptionCombinedL100: number;        // WLTP
        co2CombinedGkm: number;                 // WLTP
        emissionsClass: "Euro 5" | "Euro 6b" | "Euro 6c" | "Euro 6d-TEMP" | "Euro 6d" | "Euro 6e";
        particleFilter: boolean;
        environmentalBadge: "green" | "yellow" | "red" | "none";  // Umweltplakette
      }
    | {
        kind: "hybrid";
        subtype: "mhev" | "hev" | "phev";
        fuel: "petrol" | "diesel";
        batteryGrossKwh: number;
        electricRangeWltpKm: number;             // the number PHEV buyers are actually taxed on
        consumptionCombinedL100: number;
        co2CombinedGkm: number;
        emissionsClass: string;
      }
    | {
        kind: "electric";
        batteryGrossKwh: number;
        batteryNetKwh: number;                   // usable. The one buyers compare, publish it first
        batteryChemistry: "NMC" | "LFP" | "NCA";
        batteryOwnership: "owned" | "leased";    // Zoe-style battery rental changes the price entirely
        stateOfHealthPercent?: number;           // only if measured, see `batteryReport`
        rangeWltpKm: number;
        rangeMeasured?: { km: number; conditions: string; measuredAt: string }; // your own test, dated
        consumptionWltpKwh100: number;
        dcPeakKw: number;
        dcTenToEightyMinutes: number;
        acOnboardChargerKw: 3.7 | 7.4 | 11 | 22;
        chargePort: "CCS2" | "CCS1" | "NACS" | "CHAdeMO" | "Type2_only";
        heatPump: boolean;                       // the single most asked EV winter question
        preconditioning: boolean;
        v2lWatts?: number;
      };

  /* ---------- condition and paperwork ---------- */
  inspectionDue: string;                 // "2028-04" HU/TÜV in DE, MOT expiry in UK
  emissionsTestDue?: string;             // AU where tracked separately
  serviceHistory: {
    complete: boolean;                   // "scheckheftgepflegt"
    entries: Array<{ date: string; mileage: number; workshop: string; work: string }>;
    documentScans: string[];             // paths, not a promise that they exist
  };
  accidentDeclaration: "accident_free" | "repaired_damage_declared" | "unrepaired_damage";
  damageNotes: Array<{ location: string; description: string; photoIndex: number; deductionEur?: number }>;
  tyres: {
    fitted: "summer" | "winter" | "all_season";
    treadMm: { frontLeft: number; frontRight: number; rearLeft: number; rearRight: number };
    brand: string;
    secondSetIncluded: boolean;
  };
  brakeDiscMm?: { front: number; rear: number };
  batteryReport?: {                      // EV only, and only when a real read exists
    provider: "Aviloo" | "TÜV" | "manufacturer" | "in_house_obd";
    sohPercent: number;
    testedAt: string;
    documentPath: string;
  };
  keysIncluded: 1 | 2 | 3;
  ownersManualPresent: boolean;

  /* ---------- warranty ---------- */
  warranty: {
    manufacturerRemaining?: { untilDate: string; untilKm?: number };
    batteryWarranty?: { untilDate: string; untilKm: number; sohFloorPercent: number }; // usually 70%
    dealerWarrantyMonths: 0 | 12 | 24;
    extendedAvailable: boolean;
    provider?: string;
  };

  /* ---------- equipment ---------- */
  factoryOptions: Array<{ code: string; name: string; listPriceEur?: number }>;  // real option codes
  retrofits: Array<{ name: string; fittedBy: string; fittedAt: string }>;
  towbar?: { kind: "fixed" | "detachable" | "retractable"; maxBrakedKg: number };
  roofLoadKg?: number;
  payloadKg?: number;

  /* ---------- commerce ---------- */
  price: { amount: number; currency: Currency; vat: VatStatus; negotiable: boolean };
  previousPrice?: { amount: number; changedAt: string };   // show the change and its date, not a fake RRP
  financing?: {
    available: boolean;
    exampleMonthly?: number;
    exampleTermMonths?: number;
    exampleDepositEur?: number;
    exampleAprPercent?: number;
    representativeDisclosure: string;    // the legally required sentence, verbatim
    partners: string[];
  };
  leasing?: { available: boolean; businessOnly: boolean };
  tradeInAccepted: boolean;
  registrationFeeEur?: number;           // Zulassungskosten, itemised or it reads as a surprise
  deliveryOptions: Array<{ kind: "collect" | "delivered"; radiusKm?: number; feeEur?: number }>;

  /* ---------- availability and place ---------- */
  status: "available" | "reserved" | "sold" | "incoming" | "in_preparation";
  availableFrom?: string;
  location: { siteName: string; street: string; postcode: string; city: string; countryCode: string };
  testDrive: { bookable: boolean; durationMinutes: number; requirements: string[] };

  /* ---------- media ---------- */
  media: {
    photos: Array<{
      src: string;
      alt: string;
      kind: "exterior" | "interior" | "engine" | "underbody" | "wheel" | "damage" | "document" | "dashboard";
      shotAt: string;
      isOfThisVehicle: true;             // hard true. A manufacturer render belongs in a different field
    }>;
    manufacturerRenders?: string[];      // separate array, separate section, never in the gallery
    walkaroundVideo?: { src: string; durationS: number; captionsSrc: string };
    odometerPhoto: string;               // one photo of the actual cluster, with the date
  };

  /* ---------- the human ---------- */
  contact: { name: string; role: string; phone: string; email: string; photo: string; languages: string[] };
  listedAt: string;
  updatedAt: string;
}
```

Dealer-level model, needed by the trust surfaces:

```ts
interface Dealer {
  legalName: string;
  register: { court: string; number: string };   // Handelsregister, HRB xxxxx
  vatId: string;                                  // USt-IdNr.
  managingDirectors: string[];
  address: Address;
  openingHours: Array<{ day: number; open: string; close: string }>;
  workshopOnSite: boolean;
  brandCertifications: string[];                  // only ones that are real and current
  staff: Array<{ name: string; role: string; photo: string; yearsHere: number; speaks: string[] }>;
  reviews: { source: "google" | "mobile.de" | "autoscout24"; url: string; count: number; average: number };
}
```

## 2. The surfaces

| Surface | Mode | Job |
|---|---|---|
| Home | Persuade | Prove this is a real place with real cars, and route to inventory in one action. |
| Inventory index | Operate | Let a visitor narrow 80 to 400 vehicles to the 3 they will consider. |
| Vehicle detail (VDP) | Persuade | Answer every question in section 3 without a phone call, then make contact trivial. |
| Vehicle gallery / walkaround | Experience | Show this exact car in enough detail that the buyer stops suspecting the photos. |
| EV explainer | Read | Answer range, charging, battery health, and winter honestly, once, so the VDP does not have to. |
| Financing and leasing | Operate | Turn a price into a monthly figure the dealership will actually honor. |
| Trade-in valuation | Operate | Capture the other half of the deal, with a range, not a fake exact number. |
| Test drive booking | Operate | Slot, duration, documents required, confirmation. |
| Workshop and service | Persuade | The recurring-revenue half of the business, usually neglected on dealer sites. |
| About / the team | Persuade | Named humans, the workshop, the yard. The antidote to "is this a broker". |
| Legal (Impressum, Widerruf, Datenschutz) | Read | Required in DE/AT. Also read by careful buyers as a trust signal. |
| Sold archive | Read | Optional and underused: proves turnover and photographic consistency over time. |

## 3. The decision sequence

What the buyer decides, in order. Anything answered late gets answered by a competitor.

| # | Decision | What must be on screen |
|---|---|---|
| 1 | Is this car real and still here? | `status`, `updatedAt`, photo count, the odometer photo, the stock number |
| 2 | Is it the right spec? | make/model/trim, drivetrain, transmission, energy block, power in kW and hp |
| 3 | Can I pay for it in the shape I pay? | total price, VAT status, and monthly example with its disclosure, adjacent |
| 4 | Has it been used up or abused? | mileage against first registration, prior owners, previous use, service history |
| 5 | Has it been crashed? | accident declaration, damage notes with photo indices, underbody and wheel-arch photos |
| 6 | What will it cost me to keep? | inspection due, warranty remainder, tyre tread in mm, EV state of health and battery warranty |
| 7 | Will it work for my actual life? | EV range measured by you with conditions, heat pump, charge port, towbar, payload, boot |
| 8 | How do I touch it? | location, opening hours, test drive duration and requirements, named contact with a direct number |
| 9 | Who am I dealing with? | register number, workshop on site, staff photos, review link that leaves the site |

Mobile order differs, and why:

- **Price and monthly rate become a persistent bar at the bottom** on mobile, because decisions 4 through 7 are a long scroll and a buyer who scrolls away from the price stops calibrating against it. On desktop the gallery and the fact panel sit side by side, so the price never leaves the viewport and a sticky bar is redundant chrome.
- **Call before form.** On mobile the primary action is a `tel:` link. On desktop the primary action is a form with a callback slot, because desktop visitors are frequently at work and cannot talk.
- **Damage photos move up on mobile**, directly after the exterior set, because the mobile gallery is swiped linearly and a damage photo at position 34 will not be seen. On desktop the thumbnail rail shows all of them at once and grouping by `kind` reads better.
- **The spec table collapses into named groups on mobile** (Energy, Condition, Paperwork, Equipment) with Energy and Condition open by default. A fully collapsed accordion is an empty page.
- **Financing calculator is a link on mobile, inline on desktop.** Four numeric inputs and a slider is a bad mobile form and a fine desktop panel.

## 4. The trust problem

This buyer has been lied to before, usually by a listing portal. What they suspect, and the only
evidence that answers it:

| Suspicion | Real evidence that answers it |
|---|---|
| "Those photos are not this car" | 30 to 60 photographs shot in one session with `shotAt` dates, one continuous walkaround video, the odometer photo with the cluster legible, manufacturer renders kept in a separate labelled block |
| "The mileage is rolled back" | Service history entries with mileage at each visit, so the sequence is checkable, plus the odometer photo dated |
| "It has been crashed and repaired" | Underbody, wheel-arch, door-shut and boot-floor photographs, panel gap shots, the appraiser report as a PDF if one exists, damage notes that name the panel and deduct money |
| "The price is bait" | VAT status stated as the statute (`§25a UStG` or the rate), registration fee itemised, the financing disclosure sentence verbatim, `previousPrice` with the date it changed |
| "The TÜV is about to fail" | `inspectionDue` as a month, plus the last inspection report, plus brake disc and tyre measurements in mm |
| "The EV battery is finished" | A third-party state-of-health test with provider, date and downloadable protocol. Manufacturer battery warranty end date, kilometre cap, and the SOH floor it guarantees |
| "The advertised range is fiction" | Your own measured run with route, speed, temperature and date, printed next to the WLTP figure, not instead of it |
| "This is a broker with no premises" | Photographs of the yard and the workshop taken on one day, Handelsregister number, named staff with years at this business, opening hours |
| "Nobody will pick up after I pay" | Dealer warranty months stated, the workshop on site, a named contact with a direct line rather than a shared inbox |

Never fabricate: review counts, sold volumes, "over 500 happy customers", certification badges, or an
average rating. Link to the review source and let it count. An unlinked rating is a decoration.

## 5. Component picks

Semantics matter more than novelty here. Chrome, glass, and photographic light read automotive.
Particles, circuitry and neon do not.

| Component | Registry | Real cost | Use |
|---|---|---|---|
| `liquid-chrome` | `@componentry` | raw WebGL, zero deps, ~11 KB. Ships the `@workspace/ui/lib/utils` broken import, fix on install | Home hero backdrop behind the yard photograph, or a bounded band behind the brand mark. Literal liquid metal, on-brand without being a car cliche |
| `ripple-transition` | `@componentry` | framer-motion (~50 KB gzip via `LazyMotion` + `m`, ~110 KB if imported whole) | Photo swap in the VDP gallery. Click origin follows the tap point. Better than a carousel because it never implies more photos exist off-screen |
| `spotlight-card` | `@componentry` | zero deps, five variants. Broken `cn` import, fix on install | Inventory tiles. Stays semantic HTML so the whole card remains one link and one tab stop |
| `scroll-tilted-grid` | `@componentry` | framer-motion | The "recently arrived" or sold-archive wall. Cinematic without shouting |
| `split-flap-display` | `@componentry` | zero deps | Only for figures that are genuinely mechanical: kW, kWh, tread depth, 0 to 100. Never for price, because a price that animates reads as a slot machine |
| `noise-texture` | `@componentry` | ~2 KB, zero deps | Fine grain over hero photography. Kills the flat-render look at almost no cost |
| `scrub-input` | `@componentry` | zero deps. Broken `cn` import | Price, mileage and range filters on the inventory index. A real control, not an effect |
| **Peel** | `@canvas-ui` | needs the `drawElement` origin trial token on your domain; without it visitors see plain DOM | Inventory tile: front is photo plus model, `under` is price, mileage, finance rate. `side: "bottom", mode: "hover", reveal: 180`. `pointerEvents` gating keeps the revealed layer clickable |
| **Magnify** | `@canvas-ui` | origin trial token; cheap when idle | Damage and condition photographs. `readout: true, hud: 0.6, zoom: 2.5`. Reads as an inspection instrument, which is exactly the register a used-car page needs |
| **Glass** | `@canvas-ui` | origin trial token | Spec comparison table only, `targets: "td, .spec-value"`. Solves a real legibility problem on a dense table |
| **Glass Object** | `@canvas-ui` | three.js, roughly 600 KB. No Chrome flag needed | Justified once, for a single hero emblem or wheel, never in addition to `liquid-chrome` |
| `@bklit/line-chart` | `@bklit` | visx | Real charge-curve or consumption plot on the EV explainer. Only with measured data |
| `@kibo-ui/comparison` | `@kibo-ui` | small | Before and after on a reconditioned panel, or summer against winter range |

### AVOID

| Component | Reason |
|---|---|
| `matrix-rain`, `circuit-board` | Wrong industry semantics. A workshop is mechanical, not digital |
| `particle-galaxy` | 600 KB of three.js for a space nebula on a car site |
| `dither-prism-hero` | three plus R3F weight, and its welded `uMouseIntensity` blows out any dark palette (Law 1) |
| `border-beam`, `shimmer-button`, `pulsating-button`, `interactive-hover-button` | The four most-cloned Magic UI ports. Every AI-assembled page has them |
| `eye-tracking`, `music-player`, `magnetic-dock` | Toys on a purchase where trust is the whole job |
| `cursor-driven-particle-typography`, `infinite-image-field` | Canvas text and canvas images. Not crawlable, not linkable. Inventory must be indexable |
| **Retro Dither**, **VHS**, **Glitch**, **Asciify** over any photograph | These distort colour. Paint colour is a commercial fact. A buyer who sees the wrong shade rejects the car in person |
| **Shatter**, **Blaze** site-wide | Acceptable once, as a trade-in "old to new" transition or a performance-trim band. Anywhere else it reads as damage, on a page about damage |
| **Frost**, **Hex Float** | Own the frame budget on a page whose LCP is a 2 MB photograph |
| Any full-bleed effect behind the gallery | It has to be turned down to keep the photos truthful, which lands it in "the filter left on" (doctrine tell 8) |

## 6. The category rut

**What every dealer site looks like.** Dusk photograph of a car on a coastal road, full bleed,
navy or black gradient overlay at 60 percent. Headline "Find your perfect car" over a three-dropdown
search (Make, Model, Max price) in a white rounded box. Below it a three-up grid of stock: 16:9
rounded thumbnail, model name in semibold, a strip of four icons (calendar, gauge, fuel pump, gearbox)
with values, a red or blue price pill, a ghost "Details" button. Then "Why choose us" with three
icon-heading-two-lines cards (shield, handshake, wrench). Then a financing slider. Then a Google
reviews carousel with five gold stars. Then a full-width map and a contact form with six fields.
Type is Poppins or Inter. Radius is 12 px everywhere. One accent, applied to every button.

**The obvious contrarian move, also excluded.** All-black page, uppercase monospace, no photographs
above the fold, an inventory rendered as a bare table with hairline rules, "WE SELL CARS" at 8 rem,
a single acid accent. This is what the category produces the moment it is told to be different, so it
is a prior too. Predictable contrarianism is still the prior.

**Three material worlds that are neither:**

1. **Industrial auction catalogue** (Ritchie Bros machinery sale, Bonhams collector-car lot book).
   Lot numbers, condition grades A to D printed as a stamp, a hammer estimate range, tight caption
   typography under each plate, the schedule of sale as a table. Inventory is a lot list, the VDP is
   a lot page, and the condition grade is the organising idea rather than the price.
2. **Vehicle appraiser's report** (Kfz-Sachverständigengutachten, or a UK HPI condition report).
   Form-field structure, monospace measurements, a body diagram with numbered damage callouts,
   a signature block, a date stamp on every page. The damage section stops being an apology and
   becomes the site's strongest artifact.
3. **1970s parts microfiche and dealer parts catalogue.** Exploded diagrams, part numbers in a
   fixed-width column, thin rules, section tabs down the edge, a two-colour print budget. Options
   and equipment become a numbered parts list with real factory codes.
4. **Aircraft logbook and maintenance release.** Chronological entries, hours at each entry,
   an authorising signature, tamper-evident numbering. Service history becomes the primary
   navigation rather than a collapsed accordion at the bottom.
5. **Race scrutineering and homologation sheet.** Measured dimensions, tolerance bands, pass and
   fail stamps, a technical delegate's initials. Tyre depths, brake discs and inspection dates get a
   measurement register instead of an icon row.

## 7. Copy register

How people who actually sell cars talk. Terse, specific, unit-carrying, willing to name a fault.

Sounds right:

- "Zweite Hand, Scheckheft lückenlos, HU neu bis 04/2028."
- "77 kWh netto, 412 km WLTP. Wir sind im Februar bei 4 Grad 340 km bei Tempo 130 gefahren."
- "Reifen Sommer: 6,5 mm vorn, 7,0 mm hinten. Winterräder auf Stahl liegen dabei."
- "24.900 EUR, § 25a UStG, Mehrwertsteuer nicht ausweisbar."
- "Der Kratzer an der Fahrertür ist auf Bild 18. Entweder 300 EUR runter oder wir machen ihn vor Übergabe."
- "Batteriezustand 94 Prozent, gemessen am 12.06. mit Aviloo. Protokoll liegt als PDF dabei."
- "Probefahrt ab Dienstag, 45 Minuten, Führerschein und Ausweis mitbringen."
- "Steht bei uns auf dem Hof in Neumünster. Lieferung bis 200 km gegen 249 EUR."

English equivalents, same register:

- "Two owners. Full service history, stamped. MOT runs to April 2028."
- "77 kWh usable. 412 km WLTP. We measured 340 km at 130 km/h in February, 4 degrees."
- "Front tyres 6.5 mm, rears 7.0 mm. Winter set on steels included."

Sounds like a template, do not ship:

- "Find your perfect car today."
- "Quality vehicles at unbeatable prices."
- "Our friendly team is here to help you every step of the way."
- "Discover our extensive range of premium pre-owned vehicles."
- "Drive away happy."

## 8. The specific failure modes

1. **The gallery that is not this car.** Manufacturer renders mixed into the photo carousel. Once a
   visitor spots one render, every photograph is suspect. Keep `manufacturerRenders` in a separate,
   labelled block or drop them.
2. **Colour lied to by an effect layer.** Any shader, dither, or tint over vehicle photography changes
   the paint. Buyers reject cars in person over this and the trip is a lost sale plus a lost afternoon.
3. **The 40-row undifferentiated spec table.** No grouping, no scan structure, so the buyer reads none
   of it. Group by the section-3 decisions, not by the DMS export order.
4. **Price on request.** Reads as "we price by how you look". If financing is the pitch, show total
   price and monthly figure adjacent, with the disclosure.
5. **Mileage without a unit.** `45.000` is ambiguous the moment a non-German reader lands, and the
   German thousands separator makes it worse.
6. **Stale stock.** The car sold three weeks ago and the page still says available. Publish
   `updatedAt` and let the sold state be a real, indexed page rather than a 404.
7. **A 360 spin viewer that is 60 JPEGs and 4 MB.** Blocks LCP, and on mobile data it never loads at
   all. A dated walkaround video with captions costs less and proves more.
8. **The finance calculator the dealership will not honor.** Any figure it shows becomes an expectation.
   Bind it to real partner rates or make it a range with the disclosure attached.
9. **Filters that return zero and offer nothing.** The empty state is the most-hit state on an
   inventory index. It must name the constraint that killed the result and offer to relax it.
10. **The EV page that quotes WLTP alone.** Every EV buyer knows WLTP is optimistic. Quoting it without
    a measured figure signals either ignorance or bad faith.
11. **Contact as a shared inbox.** `info@` on a 25,000 EUR purchase. A named person, a photograph and a
    direct number outperform every trust badge on the page.
12. **Damage photographed apologetically.** Small, dark, at the end. The dealers who convert put the
    damage set early, well lit, with a measurement and a price deduction next to it.
