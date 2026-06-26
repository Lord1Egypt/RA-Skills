# Demo Site HTML Template

Replace all `[PLACEHOLDERS]` with actual business data before saving.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>[BUSINESS NAME] | [TRADE] in [CITY]</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Inter',sans-serif;color:#1a1a1a;line-height:1.6}
    nav{background:#fff;padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center;box-shadow:0 1px 3px rgba(0,0,0,.1);position:sticky;top:0;z-index:10}
    .logo{font-weight:700;font-size:1.25rem;color:#1a1a1a}
    .nav-phone{font-weight:600;color:#2563eb;text-decoration:none}
    .hero{background:linear-gradient(135deg,#1e3a5f,#2563eb);color:#fff;padding:5rem 2rem;text-align:center}
    .hero h1{font-size:clamp(2rem,5vw,3.5rem);font-weight:700;margin-bottom:1rem}
    .hero p{font-size:1.25rem;opacity:.9;margin-bottom:2rem;max-width:600px;margin-left:auto;margin-right:auto}
    .btn{display:inline-block;background:#f59e0b;color:#fff;padding:.875rem 2rem;border-radius:.5rem;text-decoration:none;font-weight:700;font-size:1.05rem;transition:background .2s}
    .btn:hover{background:#d97706}
    .services{padding:4rem 2rem;background:#f9fafb}
    .services h2{text-align:center;font-size:2rem;margin-bottom:3rem;color:#1a1a1a}
    .services-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.5rem;max-width:900px;margin:0 auto}
    .service-card{background:#fff;padding:2rem;border-radius:.75rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.06)}
    .service-icon{font-size:2.5rem;margin-bottom:1rem}
    .service-card h3{font-weight:600;font-size:1.1rem;color:#1a1a1a}
    .why{padding:4rem 2rem;max-width:800px;margin:0 auto;text-align:center}
    .why h2{font-size:1.75rem;margin-bottom:2rem}
    .why-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1.5rem;margin-top:2rem}
    .why-item{padding:1.5rem;background:#eff6ff;border-radius:.5rem}
    .why-item strong{display:block;font-size:1.1rem;color:#1e40af;margin-bottom:.5rem}
    .contact{background:#1e3a5f;color:#fff;padding:4rem 2rem;text-align:center}
    .contact h2{font-size:2rem;margin-bottom:1rem}
    .contact p{font-size:1.1rem;opacity:.85;margin-bottom:2rem}
    .contact a{color:#f59e0b;text-decoration:none;font-weight:700;font-size:1.25rem}
    footer{background:#111;color:#888;text-align:center;padding:1.5rem;font-size:.875rem}
  </style>
</head>
<body>
  <nav>
    <div class="logo">[BUSINESS NAME]</div>
    <a class="nav-phone" href="tel:[PHONE]">[PHONE]</a>
  </nav>

  <section class="hero">
    <h1>[BUSINESS NAME]</h1>
    <p>Professional [TRADE] Services in [CITY] — Licensed, Insured &amp; Ready to Help</p>
    <a href="tel:[PHONE]" class="btn">Call Now: [PHONE]</a>
  </section>

  <section class="services">
    <h2>Our Services</h2>
    <div class="services-grid">
      <div class="service-card"><div class="service-icon">[EMOJI1]</div><h3>[SERVICE 1]</h3></div>
      <div class="service-card"><div class="service-icon">[EMOJI2]</div><h3>[SERVICE 2]</h3></div>
      <div class="service-card"><div class="service-icon">[EMOJI3]</div><h3>[SERVICE 3]</h3></div>
      <div class="service-card"><div class="service-icon">[EMOJI4]</div><h3>[SERVICE 4]</h3></div>
    </div>
  </section>

  <section class="why">
    <h2>Why Choose [BUSINESS NAME]?</h2>
    <div class="why-grid">
      <div class="why-item"><strong>✅ Licensed &amp; Insured</strong>Fully certified for your protection</div>
      <div class="why-item"><strong>⚡ Fast Response</strong>Same-day service available</div>
      <div class="why-item"><strong>💰 Fair Pricing</strong>Free estimates, no hidden fees</div>
      <div class="why-item"><strong>📍 Local</strong>Proudly serving [CITY] &amp; surrounding areas</div>
    </div>
  </section>

  <section class="contact">
    <h2>Ready to Get Started?</h2>
    <p>Call or text us anytime — we're here to help.</p>
    <a href="tel:[PHONE]">[PHONE]</a>
  </section>

  <footer>&copy; <script>document.write(new Date().getFullYear())</script> [BUSINESS NAME] · [CITY], [STATE]</footer>
</body>
</html>
```

## Trade-Specific Services & Emojis

| Trade | Services | Emojis |
|---|---|---|
| Plumber | Leak Repair, Drain Cleaning, Water Heater, Emergency Service | 🚿 🔧 💧 🚨 |
| Electrician | Panel Upgrades, Outlet Install, Lighting, EV Chargers | ⚡ 💡 🔌 🏠 |
| HVAC | AC Repair, Heating, Installation, Maintenance | ❄️ 🔥 🏠 🔧 |
| Landscaper | Lawn Care, Tree Trimming, Irrigation, Cleanup | 🌿 🌳 💧 🍂 |
| Painter | Interior, Exterior, Cabinet, Commercial | 🎨 🏠 🖌️ ✨ |
| Roofer | Roof Repair, Replacement, Gutters, Inspection | 🏠 🔨 💧 🔍 |
| Cleaner | Deep Clean, Move-In/Out, Commercial, Weekly | 🧹 ✨ 🏠 📅 |
