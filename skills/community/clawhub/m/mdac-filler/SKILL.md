---
name: mdac-filler
description: "Auto-fill and submit Malaysia Digital Arrival Card (MDAC) for travelers entering Malaysia. Use when a user wants to fill or submit MDAC (马来西亚数字入境卡) for Malaysia entry. Handles form filling, slider CAPTCHA solving, and submission automatically. Requires traveler info: name, passport number, DOB, passport expiry, email, phone, arrival/departure dates, transport, accommodation address."
---

# MDAC Auto-Filler

Automates filling and submitting the Malaysia Digital Arrival Card at:
`https://imigresen-online.imi.gov.my/mdac/main?registerMain`

(Use `?registerMain` to skip the announcement popup)

## Quick Start

```bash
python3 skills/mdac-filler/scripts/fill_and_submit.py --data '{
  "name": "JOHN DOE",
  "passNo": "A1234567",
  "nationality": "CHN",
  "pob": "CHN",
  "dob": "01/01/1990",
  "sex": "1",
  "passExpDte": "01/01/2030",
  "email": "email@example.com",
  "confirmEmail": "email@example.com",
  "region": "65",
  "mobile": "91234567",
  "arrDt": "25/03/2026",
  "trvlMode": "2",
  "depDt": "25/03/2026",
  "embark": "SGP",
  "vesselNm": "Bus 170",
  "accommodationStay": "99",
  "accommodationAddress1": "106-108, Jalan Wong Ah Fook, Bandar Johor Bahru",
  "accommodationAddress2": "Johor Bahru City Square",
  "accommodationState": "01",
  "accommodationCity": "0118",
  "accommodationPostcode": "80250"
}'
```

Or use a JSON file:
```bash
python3 skills/mdac-filler/scripts/fill_and_submit.py --file traveler.json
```

## CAPTCHA Bypass Strategy

The MDAC uses `longbow.slidercaptcha.js`. Bypass approach:
1. **Patch `$.ajax`** to handle the `/captcha` verification response
2. **Read `instance.x`** (real gap coordinate) via `$('.slidercaptcha').data('plugin_sliderCaptcha').x`
3. **Calculate moveX**: `instance.x * (width-40) / (width-40-20)` where width=271
4. **Drag slider** with ease-in-out-cubic + slight y-jitter to avoid bot detection

Success condition: `sliderContainer_success` class appears on container.

## Manual JS Fill (browser console)

If using the script is not possible, paste this in the browser console:

```js
(function(data){
  retrieveRefCity(data["accommodationState"]);
  document.getElementById("accommodationState").value=data["accommodationState"];
  setTimeout(function(){
    document.getElementById("accommodationCity").value=data["accommodationCity"];
    retrievePostcode(data["accommodationCity"]);
    for (var key in data){ document.getElementById(key).value=data[key]; }
  }, 1000);
})({ /* traveler data object */ });
```

## Field Values Reference

See `references/field-values.md` for:
- Country/nationality codes
- Sex, travel mode, accommodation type codes
- State and city codes (Johor focus)
- Common Johor Bahru addresses
- CAPTCHA technical details

## Requirements

- Python 3.8+
- `pip install playwright && playwright install chromium`
- Headless=False (site detects headless browsers)

## Notes

- MDAC must be submitted within 3 days before arrival
- Singapore citizens are exempt
- Each traveler needs a separate submission
- Confirmation email sent to provided address after success
