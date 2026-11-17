# Playbook: direct-to-consumer e-commerce store

Loaded by the direction and build skills alongside `../DOCTRINE.md`. The doctrine is the law. This
file supplies the vertical's facts.

## 1. The real content model

A D2C product is not a title, a price and three photos. It is a physical object with measurements,
provenance, a tax treatment, a delivery promise and a return cost. Every field below removes a
support email or a return.

```ts
type Currency = "EUR" | "USD" | "GBP" | "CHF";
type TaxMode = "inclusive" | "exclusive";           // EU stores are inclusive, US stores are not

interface Money { amount: number; currency: Currency; taxMode: TaxMode; }

interface Measurement { value: number; unit: "mm" | "cm" | "m" | "g" | "kg" | "ml" | "l"; }

interface Product {
  /* ---------- identity ---------- */
  id: string;
  handle: string;                       // URL slug, stable forever, redirects on change
  title: string;                        // "Loopback Crew, Ecru"
  subtitle?: string;                    // the one-line differentiator, not a slogan
  productType: string;                  // "Sweatshirt", internal taxonomy
  collectionIds: string[];
  status: "active" | "draft" | "archived";
  launchedAt: string;
  seo: { title: string; description: string; canonical?: string };

  /* ---------- what it actually is ---------- */
  materials: Array<{
    component: string;                  // "body", "rib", "lining", "shell", "sole"
    composition: Array<{ fibre: string; percent: number }>;   // must total 100
    weight?: Measurement;               // 280 gsm, 40 denier, 400 thread count
    mill?: string;                      // named supplier where the brand can name it
    countryOfOrigin: string;            // ISO 3166-1 alpha-2
    certifications: string[];           // "GOTS", "OEKO-TEX 100", "bluesign". Only if held
  }>;
  construction: string[];               // "flatlock seams", "YKK Excella zip", "Goodyear welted"
  hardware?: Array<{ part: string; material: string; supplier?: string }>;
  madeIn: string;
  factory?: { name: string; city: string; countryCode: string; workers?: number };
  careInstructions: string[];           // as sentences, not laundry pictograms alone
  expectedBehaviour: string[];          // "shrinks ~2% on a warm wash", "patinates", "dyes unevenly"
  lifespanNote?: string;
  repairable: boolean;
  spareParts?: Array<{ name: string; sku: string; priceEur: number }>;

  /* ---------- variants ---------- */
  optionAxes: Array<{ name: "Size" | "Colour" | "Length" | "Width" | "Scent" | "Format"; values: string[] }>;
  variants: Variant[];
  sizeChart?: SizeChart;
  fitNotes?: {
    fit: "slim" | "regular" | "relaxed" | "oversized";
    runs: "small" | "true" | "large";
    betweenSizesAdvice: string;         // "size down for a boxy fit"
  };

  /* ---------- media ---------- */
  media: Array<{
    src: string;
    alt: string;                        // written, never auto-generated from the title
    kind: "studio" | "on_body" | "detail" | "flat_lay" | "in_use" | "scale_reference" | "packaging";
    variantIds?: string[];              // which colourway this frame belongs to
    model?: { heightCm: number; sizeWorn: string; chestCm?: number; waistCm?: number };
    width: number; height: number;      // required, or the grid shifts on load
  }>;
  video?: { src: string; posterSrc: string; durationS: number; captionsSrc: string; hasAudio: boolean };

  /* ---------- commerce ---------- */
  price: Money;
  compareAtPrice?: Money;               // only if it was genuinely charged at that price, with a date
  compareAtValidFrom?: string;          // EU Omnibus: the lowest price of the last 30 days
  costPrice?: number;                   // internal, drives the "what it costs to make" breakdown
  priceBreakdown?: Array<{ label: string; amount: number }>;  // materials, labour, duty, margin
  subscription?: { available: boolean; intervals: Array<"4w" | "8w" | "12w">; discountPercent: number };
  bundleWith?: Array<{ productId: string; bundlePrice: Money }>;
  giftWrapAvailable: boolean;

  /* ---------- compliance ---------- */
  compliance: {
    gtin?: string;                      // EAN-13 / UPC. Required for most feeds and marketplaces
    hsCode?: string;                    // customs classification, drives duty at checkout
    euResponsiblePerson?: { name: string; address: string; email: string };  // GPSR, mandatory in the EU
    warnings: string[];                 // choking hazard, flammability, age rating
    ingredientsInci?: string[];         // cosmetics
    allergens?: string[];               // food and cosmetics
    batteryContained?: { chemistry: string; wattHours: number; removable: boolean };  // WEEE and shipping
    weeeRegistered?: boolean;
    packagingRecycling?: Array<{ part: string; material: string; stream: string }>;
  };

  /* ---------- logistics ---------- */
  shipping: {
    weight: Measurement;                // packed, not the product alone
    dimensions: { length: Measurement; width: Measurement; height: Measurement };
    shipsFrom: Array<{ warehouse: string; countryCode: string }>;
    handlingDays: number;
    restrictions?: string[];            // "no air freight", "no PO box"
  };

  /* ---------- proof ---------- */
  reviews?: {
    source: "internal" | "trustpilot" | "judgeme" | "okendo";
    count: number;
    average: number;
    distribution: Record<1 | 2 | 3 | 4 | 5, number>;
    verifiedPurchaseOnly: boolean;
    items: Array<{
      rating: 1 | 2 | 3 | 4 | 5;
      body: string;
      author: string;
      verifiedPurchase: boolean;
      variantPurchased: string;
      reviewerContext?: { heightCm?: number; sizeWorn?: string; usage?: string };
      publishedAt: string;
      photos?: string[];
      brandReply?: { body: string; publishedAt: string };
    }>;
  };
  press?: Array<{ publication: string; headline: string; url: string; publishedAt: string }>;
}

interface Variant {
  id: string;
  sku: string;
  gtin?: string;
  optionValues: Record<string, string>;             // { Size: "M", Colour: "Ecru" }
  price?: Money;                                    // only when it differs from the product price
  inventory: {
    policy: "deny" | "continue";                    // whether it can be oversold
    onHand: number;
    committed: number;
    available: number;                              // onHand minus committed, the number to display
    lowStockThreshold: number;
    backorderable: boolean;
    restockExpected?: string;                       // a date range, never "soon"
    discontinued: boolean;
  };
  weightOverride?: Measurement;
  swatch?: { hex: string; imageSrc?: string };      // hex alone lies about texture, ship both
  measurements?: Record<string, Measurement>;       // per-size garment-flat measurements
}

interface SizeChart {
  method: "garment_flat" | "body";                  // say which, they differ by several cm
  units: "cm" | "in";
  tolerance?: string;                               // "+/- 1 cm, measured by hand"
  rows: Array<{ size: string; values: Record<string, number> }>;
  howToMeasure: Array<{ point: string; instruction: string; diagramSrc?: string }>;
}

interface ShopPolicy {
  returns: {
    windowDays: number;
    condition: string;                              // "unworn, tags attached"
    whoPaysReturn: "brand" | "customer" | "brand_within_eu";
    returnFee?: Money;
    exchangeAvailable: boolean;
    exclusions: string[];                           // sale items, pierced jewellery, opened cosmetics
    address: Address;                               // the physical return address, in the country
    refundProcessingDays: number;
  };
  delivery: Array<{
    zone: string;
    carrier: string;
    service: string;
    priceThresholds: Array<{ overAmount: number; price: Money }>;
    estimateBusinessDays: { min: number; max: number };
    dutiesHandling: "DDP" | "DAP";                  // DAP means the customer gets a customs bill
    trackingProvided: boolean;
  }>;
  warranty?: { months: number; covers: string; excludes: string };
  company: { legalName: string; register: string; vatId: string; address: Address; email: string };
}
```

## 2. The surfaces

| Surface | Mode | Job |
|---|---|---|
| Home | Persuade | State what this brand makes and for whom, then route to one collection in one action. |
| Collection / category (PLP) | Operate | Let a visitor compare 12 to 120 items on the two axes that matter for this category. |
| Product detail (PDP) | Persuade | Answer decisions 1 to 7 below without a support email, then make adding trivial. |
| Size and fit | Read | The measured table, the method, the tolerance. Reachable from the PDP without losing scroll. |
| Cart | Operate | Show the real total, including shipping and duty, before the checkout hands off. |
| Checkout | Operate | Zero effects, zero surprises, fewest fields that complete the order. |
| Order confirmation and tracking | Operate | The delivery date and the tracking link, first screen. |
| Returns and exchanges | Operate | Start a return in three steps, and say who pays before the first one. |
| Materials / how it is made | Read | The trust surface. Named mill, named factory, real weights. |
| Care and repair | Read | Extends product life and is the cheapest differentiator in the category. |
| Journal / editorial | Read | Only if it is real. A three-post blog last updated in 2023 is negative evidence. |
| Legal (imprint, terms, privacy, withdrawal) | Read | Mandatory in the EU. Careful buyers open it. |

## 3. The decision sequence

| # | Decision | What must be on screen |
|---|---|---|
| 1 | Is this the thing I came for? | Title, the first image matching the referring ad or listing exactly, price |
| 2 | Does it come in my variant? | Option axes with unavailable combinations visibly disabled, not hidden |
| 3 | Will it fit me or my space? | Garment-flat measurements for the selected size, model height and size worn, a scale reference |
| 4 | What is it made of? | Composition with percentages, weight (gsm, denier, thread count), country of origin, mill |
| 5 | What does it truly cost? | Price plus shipping for my country plus duty treatment (DDP or DAP), before checkout |
| 6 | When does it arrive? | A date range for the selected country, computed from `handlingDays` plus carrier estimate |
| 7 | What if it is wrong? | Return window, who pays the return, the physical return address, exchange availability |
| 8 | Is anyone real behind this? | Company registration, a return address in the buyer's region, reviews with verified purchases |

Mobile order differs, and why:

- **The gallery leads, then price and variant, then a pinned add-to-cart.** On mobile a visitor
  arriving from a paid ad is verifying image match first. On desktop the gallery and the buy panel are
  adjacent, so decisions 1 through 3 happen in parallel and no pinning is needed.
- **Size guidance is inline at the variant selector on mobile, not in a modal.** A modal covers the
  whole screen, and closing it commonly resets scroll. On desktop a side panel keeps the selector and
  the table visible at once, which is the only place a modal is defensible.
- **Shipping and returns move above the description on mobile.** Decisions 5 through 7 are the ones
  that abandon a mobile session, and the long description pushes them below three screens.
- **Reviews collapse to the distribution bar plus three reviews on mobile**, filtered to the selected
  size where reviewer context exists. The full list is a separate route so the back button works.
- **Cart is a full page on mobile, a drawer on desktop.** A drawer on mobile traps the total below
  the fold and hides the delivery estimate.

## 4. The trust problem

The D2C buyer's default assumption is that this is a drop-shipper with a Shopify theme and stock
photographs. That assumption is correct often enough that it is rational.

| Suspicion | Real evidence that answers it |
|---|---|
| "These photos are from a supplier catalogue" | Unstyled frames: the product flat on a plain surface, a detail shot of the seam or hardware, the packaging as it arrives, a scale reference against a known object |
| "It will not fit" | A garment-flat table with the measuring method and tolerance stated, model height plus size worn on every on-body frame, reviewer context (height, size bought) attached to reviews |
| "The material is not what it says" | Composition to the percent, weight with a unit, the mill or tannery named, certification numbers that can be looked up |
| "The reviews are bought" | Verified-purchase flags, the full 1 to 5 distribution including the ones, brand replies to the negative ones, the variant each reviewer bought, dates |
| "There is a customs bill waiting" | DDP or DAP stated per zone, duty either quoted at checkout or explicitly named as payable on delivery |
| "Returns go to a warehouse in another continent" | The literal return address with a postcode, who pays the label, the refund processing window in days |
| "This brand will not exist in six months" | Company registration and VAT number in the footer, a physical address, repair and spare parts offered, restock dates that were kept |
| "The discount is fake" | The EU Omnibus figure: the lowest price in the previous 30 days, printed next to the sale price with its date |

Never fabricate: review counts, "as seen in" logos, sustainability certifications, customer numbers,
factory photographs that are not your factory. A single unverifiable badge poisons the ones that are
real.

## 5. Component picks

Product imagery must stay clickable and indexable. That excludes canvas galleries entirely. The
effect budget is Persuade on the home and collection surfaces, and near zero from the PDP onward.

| Component | Registry | Real cost | Use |
|---|---|---|---|
| `dither-gradient` | `@componentry` | ~3.5 KB, zero deps | Collection header backdrop. Cheap enough to run on every category page without touching Core Web Vitals |
| `ripple-transition` | `@componentry` | framer-motion (~50 KB gzip with `LazyMotion`) | Product image transition on variant switch, click origin at the swatch. Better than a fade because it ties the change to the control that caused it |
| `spotlight-card` | `@componentry` | zero deps, broken `cn` import, fix on install | Product tiles. Stays semantic HTML, so the tile is one link and one tab stop |
| `scrub-input` | `@componentry` | zero deps, broken `cn` import | Price and size filters on the PLP. A real primitive, not decoration |
| `kinetic-text-reveal` | `@componentry` | framer-motion | Collection headlines. Real DOM text, so it stays selectable and crawlable |
| `testimonial-marquee` | `@componentry` | pure CSS. Drop its phantom `framer-motion` declaration | Review band. Zero runtime animation cost on a page that carries paid traffic |
| `sticky-scroll-cards` | `@componentry` | framer-motion, ships Unsplash defaults, replace them | Editorial "shop the look" section between grid pages |
| `orbit-card-stack` | `@componentry` | framer-motion | Bundle or collection picker. `onActiveChange` makes it a real control |
| **Peel** | `@canvas-ui` | `drawElement` origin trial token on your domain | The workhorse for PLP tiles. Front is the product, `under` is price, size availability, restock. `side: "right", mode: "cursor", reveal: 220`. `pointerEvents` gating keeps the revealed layer clickable |
| **Glass** | `@canvas-ui` | origin trial token | PDP image zoom, `shape: "circle", size: 160, zoom: 2, targets: ".product-image"`. Replaces a jQuery magnifier and zooms live DOM, so badges and annotations scale with it |
| **Ripple** | `@canvas-ui` | origin trial token, free while idle | Add-to-cart confirmation, called imperatively as `splash(x, y, 1)` at the button position |
| **Glass Object** / **Dithered Object** | `@canvas-ui` | three.js, roughly 600 KB. No Chrome flag | One hero product as a rotating object. Glass Object for glassware, fragrance, jewellery. Dithered Object for hardware and streetwear. Budget it as the page's only heavy component |
| `@kibo-ui/image-zoom` | `@kibo-ui` | small | The no-token fallback for PDP zoom. Ship this and treat Glass as progressive enhancement |
| `@kibo-ui/comparison` | `@kibo-ui` | small | Before and after: worn against new, treated against untreated |
| `@bklit/heatmap-chart` | `@bklit` | visx | Only where real data exists, for example a restock or availability calendar |

### AVOID

| Component | Reason |
|---|---|
| `infinite-image-field` | Canvas. Products stop being links, stop being crawlable, stop being reachable by keyboard |
| `cursor-driven-particle-typography` | Canvas text is invisible to search engines and screen readers. Fatal on a commerce page |
| `image-trail` | Pulls in GSAP for one effect and degrades touch interaction, where most of the traffic is |
| `particle-galaxy`, `dither-prism-hero` | three.js weight measured directly against conversion rate |
| `magnetic-dock` | A macOS dock on a store is cosplay |
| `border-beam`, `shimmer-button`, `pulsating-button`, `interactive-hover-button` | The four most-cloned Magic UI ports |
| **Retro Dither** above `colorize: 0.15` on any product frame | Distorts product colour. Colour distortion converts directly into returns |
| **Glitch**, **VHS** anywhere on a PDP, cart, or checkout | Simulated malfunction on a page asking for a card number |
| **Shatter**, **Hex Float** anywhere on the conversion path | Breakage imagery next to a buy button, and Hex Float owns the frame budget |
| Any lens component (**Glass**, **Magnify**, **Bubble**) over a form field | They distort input text. Never near checkout |
| `matrix-rain` | Nothing about a physical product is a terminal |

## 6. The category rut

**What every D2C store looks like.** Full-bleed lifestyle photograph, model mid-laugh, warm grade.
Sticky announcement bar: "Free shipping over 50". Headline in a high-contrast display serif over the
image, a single ghost button "Shop now". Below it a four-up product grid, every crop 1:1, hover swaps
to image two, title in 14px medium, price under it, a "New" pill in the corner. Then a three-icon
value row (leaf, truck, return arrow) with two lines each. Then a founder-story block: portrait left,
warm serif paragraph right, a signature graphic. Then an Instagram embed. Then a newsletter modal at
15 seconds offering 10 percent. Type is a display serif plus Inter. One accent, terracotta or sage.

**The obvious contrarian move, also excluded.** Unstyled HTML, Times New Roman, left-aligned product
list with no images, a single 8 rem lowercase wordmark, "buy" as a plain text link, deliberate
anti-design. This is the reflex the moment the brief says "not generic", which makes it a prior. So is
the second reflex: brutalist grid, Helvetica, black on white, oversized numerals.

**Four material worlds that are neither:**

1. **A fabric swatch book** (Kvadrat sample card, Sandberg wallpaper book). Physical chips bound at one
   edge, each with a code, a composition line, a rub-test figure and a lightfastness rating. Variants
   become swatches with real specification data, and the PLP becomes a bound sample set rather than a grid.
2. **A seed packet rack.** Front is an illustration and a name, back is sowing depth, spacing,
   germination days, harvest window and a packed-by date. The reverse of the packet is the whole
   product data model, printed small and dense, and the rack is the collection page.
3. **A hardware store bin label system.** Numbered bins, a fixed-width part code, quantity on hand
   written by hand, tally marks, a price per unit and a price per hundred. Inventory becomes visible
   and legible instead of hidden behind "in stock".
4. **A chemist's dispensary label and apothecary drawer.** A name, a strength, a batch, an expiry, a
   directions line, a warning box. For anything with an ingredient list this outperforms every
   wellness-brand default because it is the actual grammar of ingredient disclosure.
5. **A museum wall label and object file.** Accession number, maker, date, material, dimensions,
   provenance, credit line, set in a small strict type block beside the object. Turns "materials and
   care" from a footer accordion into the reason the page exists.

## 7. Copy register

How people who actually make and sell things talk. Measured, willing to name a limitation, specific
about time and place.

Sounds right:

- "280 gsm loopback cotton, milled in northern Portugal. It shrinks about 2 percent on a warm wash, so we cut it long."
- "Model is 178 cm and wears a medium."
- "Measured flat across the chest, size M: 56 cm. Hand measured, so give it a centimetre either way."
- "Three left in this size. Ships from Hamburg, Monday to Thursday, so an order today leaves Tuesday."
- "Returns are 30 days. We pay the label inside the EU. Outside the EU you pay it and we refund the item."
- "The dye takes unevenly on purpose. Two of the same size will not match exactly, and that is the point."
- "Restock is week 38. Leave your email and you get one message when it lands. Nothing else."
- "This is the same jacket we sold in 2019 with a heavier zip. The old pulls still fit."

Sounds like a template, do not ship:

- "Elevate your everyday."
- "Crafted with love for the modern minimalist."
- "Our best seller for a reason."
- "The perfect addition to any wardrobe."
- "Free shipping on all orders over 50."

## 8. The specific failure modes

1. **Variant switch that updates only the swatch.** Price, gallery, availability, SKU and the URL all
   have to move together, or the buyer adds the wrong thing and returns it.
2. **Out-of-stock variants left selectable.** The visitor selects, hits add, gets an error, leaves.
   Disable and label, never hide, because hiding makes the size range look shorter than it is.
3. **Total cost revealed at the last checkout step.** Shipping and duty arriving on step four is the
   single largest cart abandonment cause in the category, and it is a layout decision, not a pricing one.
4. **The size guide modal that eats the screen and loses scroll position.** On mobile this ends the session.
5. **Auto-generated alt text.** `alt="product image 3"` on every frame. The alt is where the on-body
   context, the colourway and the detail actually live.
6. **Truncated titles to keep card heights even.** Doctrine tell 9. Let the grid be ragged and let the
   product keep its name.
7. **Missing image dimensions.** Layout shift on the PLP as each frame loads, which reads as cheapness
   before a single word is read.
8. **The review widget that ships 400 KB of third-party JavaScript** and inserts itself after paint.
   Render the summary server-side and lazy-load only the list.
9. **Three overlays at once:** cookie banner, announcement bar, newsletter modal. None dismissible by
   keyboard, all covering the price.
10. **Canvas galleries.** Not crawlable, not linkable, not keyboard reachable. The product images are
    the SEO asset of the entire store.
11. **A compare-at price that was never charged.** Illegal in the EU under the Omnibus rules, and
    visible to any buyer who checked last week.
12. **"Ships fast" instead of a date.** A date range computed from the buyer's country converts. An
    adjective does not.
13. **Colour communicated by a hex swatch alone.** Hex cannot carry texture, weave or sheen. Ship a
    photographed swatch next to the hex.
14. **Restock as "coming soon".** Either a date range or an honest "we do not know yet, here is the
    email list". "Soon" is read as never.
