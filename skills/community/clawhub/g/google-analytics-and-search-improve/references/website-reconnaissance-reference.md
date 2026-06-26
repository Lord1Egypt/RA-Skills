# Website Reconnaissance Reference

Detailed commands and classification tables for Phase 0: Website Reconnaissance & Goal Definition.

## Browser Commands for Site Exploration

### Take screenshots

```bash
agent-browser open "$SITE_URL" && agent-browser wait --load networkidle
agent-browser screenshot --full homepage_overview.png
```

Save screenshots to `$DATA_DIR/tmp/`.

### Extract page metadata

```bash
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify({
  title: document.title,
  meta_desc: document.querySelector('meta[name="description"]')?.content,
  h1: Array.from(document.querySelectorAll('h1')).map(h => h.textContent.trim()),
  h2s: Array.from(document.querySelectorAll('h2')).slice(0, 10).map(h => h.textContent.trim()),
  nav_links: Array.from(document.querySelectorAll('nav a, header a')).slice(0, 20).map(a => ({text: a.textContent.trim(), href: a.href})),
  cta_buttons: Array.from(document.querySelectorAll('a[class*="btn"], button[class*="btn"], a[class*="cta"], button[class*="cta"], [role="button"]')).slice(0, 10).map(el => ({text: el.textContent.trim(), href: el.href || ''})),
  footer_links: Array.from(document.querySelectorAll('footer a')).slice(0, 15).map(a => ({text: a.textContent.trim(), href: a.href})),
  forms: Array.from(document.querySelectorAll('form')).map(f => ({action: f.action, id: f.id, inputs: Array.from(f.querySelectorAll('input,select,textarea')).map(i => i.name || i.type)})),
  has_pricing: !!document.body.innerText.match(/pric(e|ing)|plan|subscribe|buy|purchase|付费|价格|套餐/i),
  has_login: !!document.querySelector('a[href*="login"], a[href*="signin"], a[href*="signup"], a[href*="register"]'),
  has_ecommerce: !!document.querySelector('[class*="cart"], [class*="product"], [class*="shop"]'),
  has_blog: !!document.querySelector('a[href*="blog"], a[href*="article"], a[href*="news"]'),
})
EVALEOF
```

### Extract front-end metadata (when no source code available)

```bash
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify({
  title: document.title,
  meta_desc: document.querySelector('meta[name="description"]')?.content,
  h1: Array.from(document.querySelectorAll('h1')).map(h => h.textContent),
  has_jsonld: document.querySelectorAll('script[type="application/ld+json"]').length,
  images_no_alt: document.querySelectorAll('img:not([alt])').length,
  viewport: document.querySelector('meta[name="viewport"]')?.content,
  canonical: document.querySelector('link[rel="canonical"]')?.href,
})
EVALEOF
```

## Website Type Classification

| Website Type | Key Signals | Primary Goal | Core Metrics |
|---|---|---|---|
| **Content/Blog** | Blog section, articles, tutorials | Reader engagement & return visits | Page views, time on page, pages/session, return visitor rate |
| **SaaS/Tool** | Login/signup, pricing page, app features | User registration → activation → retention | Signup rate, trial-to-paid, feature adoption |
| **E-commerce** | Product pages, cart, checkout | Purchase conversion | Add-to-cart rate, cart abandonment, purchase conversion, AOV |
| **Lead Generation** | Contact forms, demo requests, whitepapers | Form submissions / demo bookings | Form completion rate, lead quality, cost per lead |
| **Portfolio/Showcase** | Project galleries, about page, contact | Contact or inquiry | Contact form submissions, inquiry rate |
| **Documentation/Docs** | API docs, guides, reference pages | Help users find answers | Search usage, page depth, time on page, exit rate from docs |
| **Community/Forum** | User posts, comments, threads | User engagement & content creation | Posts per user, comment rate, return rate |
| **Landing Page** | Single page, strong CTA, no navigation depth | Single conversion action | CTA click rate, conversion rate, bounce rate |

## Analysis Dimension Ranking

Not all analysis dimensions are equally important for every website type. Based on the goal profile, select and **rank** the applicable dimensions:

| Analysis Dimension | When It Matters Most |
|---|---|
| **Acquisition / SEO** | Sites that depend on organic search traffic (content, SaaS, e-commerce) |
| **Conversion Funnel** | Sites with clear multi-step user journeys (SaaS signup, e-commerce purchase) |
| **Content Engagement** | Content-heavy sites (blogs, docs, tutorials) |
| **User Experience (UX)** | All sites, but especially mobile-first sites or sites with high bounce rates |
| **Performance** | All sites, but critical for e-commerce and landing pages where speed = money |
| **Retention / Return Visits** | SaaS, community, and content sites where repeat visits matter |
| **Technical SEO / GEO** | All sites that need search visibility |

Output a ranked list of dimensions for this specific site, e.g.:
```
Priority analysis dimensions for [site]:
1. Conversion Funnel (SaaS → signup → trial → paid is the core business flow)
2. Acquisition / SEO (organic search is the main traffic channel)
3. Content Engagement (blog is used for top-of-funnel acquisition)
4. UX (mobile bounce rate appears high from initial visit)
5. Performance (site loads well, lower priority)
```

## Goal Profile Presentation Template

> Based on my visit to your site, here's what I understand:
>
> **Website Type**: [e.g., SaaS Tool]
> **Primary Goal**: [e.g., Get users to sign up for free trial and convert to paid]
> **Secondary Goals**: [e.g., Build brand awareness through blog content, provide documentation for retention]
>
> **Intended User Journey** (the path you want users to follow):
> ```
> [e.g., Search/Ad → Landing Page → Explore Features → Sign Up → Onboarding → First Value → Upgrade]
> ```
>
> **Key Conversion Points** I'll focus on:
> 1. [e.g., Landing page → Sign up page (acquisition)]
> 2. [e.g., Sign up → Complete onboarding (activation)]
> 3. [e.g., Free trial → Paid plan (monetization)]
>
> Does this match your understanding? Please correct or add anything I missed.
> Also, if you have specific KPIs or targets (e.g., "we want to increase signup rate from 3% to 5%"), please share them.

## Information Request Template

> To give you the most actionable analysis, it would be very helpful if you could tell me:
>
> 1. **Your main traffic sources** — Is most traffic from organic search, paid ads, social media, or direct?
> 2. **Key GA4 events you've set up** — Do you track specific events like `signup`, `purchase`, `add_to_cart`, `form_submit`? (This determines whether I can do funnel analysis)
> 3. **Any known pain points** — Are there specific pages or flows where you suspect users are dropping off?
> 4. **Business context** — Any recent changes (redesign, new content, campaign launches) that might affect the data?
> 5. **Target audience** — Who are your primary users? (This helps interpret geographic and device data)
>
> Don't worry if you can't answer all of these — I'll work with what's available and flag areas where more data would help.
