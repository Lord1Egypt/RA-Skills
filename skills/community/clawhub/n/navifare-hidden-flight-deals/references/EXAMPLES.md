# Navifare Hidden Flight Deals - Usage Examples

Real conversation examples showing how to use this skill effectively.

---

## Example 1: One-Way Request (Limitation)

### Conversation

**User**: I found a flight from New York to London on Skyscanner for $450. It's BA553 departing Sep 15 at 6 PM.

**Agent** (activates skill):
I'd love to help you check if that's the best price! However, Navifare currently only supports **round-trip** flight searches.

Do you have a return flight as well? If so, share the return flight details (airline, flight number, date, and times) and I'll compare prices across multiple booking sites for the full round trip.

---

## Example 2: Screenshot Upload from Kayak

### Conversation

**User**: *[Uploads screenshot of Kayak search showing Milan to Barcelona round-trip for EUR 299]*

**Agent** (activates skill):
I can see your flight search. Let me extract the details and find the best price for you.

*[Extracts flight itinerary details from screenshot -- no personal info]*

Extracted from your screenshot:
- Route: MXP (Milan Malpensa) -> BCN (Barcelona)
- Outbound: Sep 20, 2026
- Return: Sep 27, 2026
- Airline: Vueling
- Passengers: 1 adult
- Class: Economy
- Reference price: EUR 299 on Kayak

*[Calls format_flight_pricecheck_request, then flight_pricecheck]*

Searching multiple booking sites...

*[Results come back]*

**Price verified!**

Your reference: EUR 299 on Kayak
Navifare best price: **EUR 295 on Kiwi.com**
Difference: EUR 4 (1.3%)

Your price is very competitive! The best available is nearly identical.

**Top 5 Options:**

| # | Website | Price | Fare Type | Booking Link |
|---|---------|-------|-----------|--------------|
| 1 | Kiwi.com | EUR 295 | Standard | [Book Now](https://kiwi.com/...) |
| 2 | Kayak | EUR 299 | Standard | [Book Now](https://kayak.com/...) |
| 3 | Momondo | EUR 305 | Standard | [Book Now](https://momondo.com/...) |
| 4 | Skyscanner | EUR 310 | Standard | [Book Now](https://skyscanner.com/...) |
| 5 | eDreams | EUR 315 | Special Fare | [Book Now](https://edreams.com/...) |

All prices checked: 2026-04-08 16:45 UTC

The price you found is excellent. I'd recommend booking soon as prices for September travel tend to increase closer to departure.

---

## Example 3: Multi-Segment Connection Flight

### Conversation

**User**: Google Flights shows $890 for LAX to Tokyo via Seattle on Oct 10, returning Oct 20. Alaska AS338 to Seattle, then ANA NH178 to Tokyo. Should I book it?

**Agent** (activates skill):
Let me verify that's the best price for your itinerary with the connection in Seattle.

*[Extracts details]*
- Segment 1: AS338, LAX -> SEA, Oct 10
- Segment 2: NH178, SEA -> NRT, Oct 10
- Need departure/arrival times for accurate search

**Question**: What are the departure and arrival times for each segment?
- AS338 LAX -> SEA: Departure time?
- NH178 SEA -> NRT: Departure time?

**User**: AS338 departs 10 AM arrives 12:30 PM. NH178 departs 2:30 PM arrives 5 PM next day.

**Agent**:
Perfect! Searching now...

*[Calls format then search with both segments]*

**Prices have changed**

Your reference: $890 on Google Flights
Current best price: **$925 on Kiwi.com**
Increase: $35 (3.9%)

Prices for this route have gone up slightly since you checked.

**Top 3 Options:**

| # | Website | Price | Fare Type | Booking Link |
|---|---------|-------|-----------|--------------|
| 1 | Kiwi.com | $925 | Standard | [Book Now](https://kiwi.com/...) |
| 2 | Momondo | $945 | Standard | [Book Now](https://momondo.com/...) |
| 3 | Google Flights | $890* | Standard | [Book Now](https://google.com/flights/...) |

*Note: The $890 price on Google Flights may no longer be available. Verify on their site.*

All prices checked: 2026-04-08 17:00 UTC

**Recommendation**: If the $890 price is still available on Google Flights when you check, that's your best option. Otherwise, Kiwi.com at $925 is the next best choice.

---

## Example 4: Round-Trip Validation Before Booking

### Conversation

**User**: I'm about to book this flight to Athens. Can you check if it's a good price first?

Details:
- London Gatwick to Athens, Sep 10-17 2026
- British Airways outbound, Aegean return
- GBP 380 total on Skyscanner

**Agent** (activates skill):
Absolutely! Let me verify that's the best price before you commit.

I need a few more details for an accurate search:
- Outbound: BA flight number and departure time?
- Return: Aegean (A3) flight number and departure time?
- Travel class (Economy, Business)?

**User**:
- Outbound: BA632, departs 7:30 AM, arrives 1:15 PM
- Return: A3605, departs 9:00 AM, arrives 11:30 AM
- Economy class

**Agent**:
Thank you! Searching now...

*[Builds round-trip search with both flights]*

**I found savings!**

Your reference: GBP 380 on Skyscanner
Best price found: **GBP 365 on Momondo**
You save: GBP 15 (3.9%)

**Top 5 Options:**

| # | Website | Price | Fare Type | Booking Link |
|---|---------|-------|-----------|--------------|
| 1 | Momondo | GBP 365 | Standard | [Book Now](https://momondo.com/...) |
| 2 | Kiwi.com | GBP 370 | Standard | [Book Now](https://kiwi.com/...) |
| 3 | Kayak | GBP 375 | Standard | [Book Now](https://kayak.com/...) |
| 4 | Skyscanner | GBP 380 | Standard | [Book Now](https://skyscanner.com/...) |
| 5 | eDreams | GBP 395 | Special Fare | [Book Now](https://edreams.com/...) |

All prices checked: 2026-04-08 17:15 UTC

I recommend booking with Momondo to save GBP 15. However, verify that both flights (BA632 and A3605) are included in their quote before purchasing.

---

## Example 5: Missing Information Handling

### Conversation

**User**: Found a flight to Paris for $600. Is that good?

**Agent** (activates skill):
I'd be happy to check if that's the best price! To search accurately, I need more details:

**Missing information:**
- Departure city/airport
- Travel dates (outbound and return)
- Airline and flight number
- Departure/arrival times
- Travel class

Could you provide:
1. **Where are you flying from?** (e.g., "New York JFK")
2. **What dates?** (e.g., "Sep 15-22, 2026")
3. **Which airline and flight?** (e.g., "Air France AF007")
4. **What time does it depart?** (e.g., "6:00 PM")
5. **Economy or Business class?**

**User**: Oh right! Flying from Boston to Paris CDG on Sep 8 returning Sep 15. Air France AF334 leaving at 8:30 PM, arriving 9:45 AM next day. Return AF335 leaving 11:00 AM arriving 1:30 PM. Economy.

**Agent**:
Perfect! Now I can search properly.

*[Extracts details]*
- Outbound: BOS -> CDG, AF334, Sep 8 2026, 20:30 -> 09:45 (+1 day)
- Return: CDG -> BOS, AF335, Sep 15 2026, 11:00 -> 13:30
- Economy, 1 adult
- Reference: $600

Searching across multiple booking sites...

*[Results]*

**Better prices available!**

Your reference: $600 on [unknown site]
Best price found: **$565 on Kiwi.com**
You save: $35 (5.8%)

**Top 3 Options:**

| # | Website | Price | Fare Type | Booking Link |
|---|---------|-------|-----------|--------------|
| 1 | Kiwi.com | $565 | Standard | [Book Now](https://kiwi.com/...) |
| 2 | Momondo | $580 | Standard | [Book Now](https://momondo.com/...) |
| 3 | Google Flights | $595 | Standard | [Book Now](https://google.com/flights/...) |

All prices checked: 2026-04-08 17:30 UTC

---

## Example 6: No Better Price Found

### Conversation

**User**: Kayak shows EUR 450 for Zurich to Rome round-trip on LX1612/LX1613, Nov 15-22. Can you beat it?

**Agent** (activates skill):
Let me check what other booking sites have for that flight.

*[Needs more info]*

**Question**: What time does LX1612 depart and arrive on Nov 15? And LX1613 on Nov 22?

**User**: LX1612 departs 10:40 AM arrives 12:25 PM. LX1613 departs 13:10 arrives 14:55.

**Agent**:
Searching...

*[Results show no cheaper prices]*

**Your price is the best available!**

Your reference: EUR 450 on Kayak
Navifare best price: EUR 450 on Kayak
Match: EUR 0 (0%)

**All available prices:**

| # | Website | Price | Fare Type | Booking Link |
|---|---------|-------|-----------|--------------|
| 1 | Kayak | EUR 450 | Standard | [Book Now](https://kayak.com/...) |
| 2 | Skyscanner | EUR 450 | Standard | [Book Now](https://skyscanner.com/...) |
| 3 | Momondo | EUR 465 | Standard | [Book Now](https://momondo.com/...) |
| 4 | Kiwi.com | EUR 475 | Standard | [Book Now](https://kiwi.com/...) |
| 5 | eDreams | EUR 490 | Special Fare | [Book Now](https://edreams.com/...) |

All prices checked: 2026-04-08 17:45 UTC

The EUR 450 price you found is the best current rate. I recommend booking it through Kayak or Skyscanner (both offer the same price).

**Note**: Swiss International Air Lines (LX) is a reputable carrier. This is a direct flight with good timing, making it excellent value.

---

## Example 7: Peak Season Route

### Conversation

**User**: Is $1,200 good for Miami to London round-trip on December 20? American Airlines.

**Agent** (activates skill):
Let me check current prices for that route and date.

*[Extracts details, asks for flight number, times, and return date]*

**User**: AA38 departs 9:15 PM arrives 10:30 AM next day. Returning Dec 27 on AA39 departs 11:00 AM arrives 3:30 PM.

**Agent**:
Searching...

**Peak season alert**

Your reference: $1,200
Current best price: **$1,150 on Momondo**
Savings: $50 (4.2%)

**Top 3 Options:**

| # | Website | Price | Fare Type | Booking Link |
|---|---------|-------|-----------|--------------|
| 1 | Momondo | $1,150 | Standard | [Book Now](https://momondo.com/...) |
| 2 | Kayak | $1,195 | Standard | [Book Now](https://kayak.com/...) |
| 3 | Google Flights | $1,200 | Standard | [Book Now](https://google.com/flights/...) |

All prices checked: 2026-04-08 18:00 UTC

**Important context:**
- December 20 is peak Christmas travel
- Transatlantic flights are in very high demand
- Prices typically increase significantly closer to departure
- $1,150-$1,200 is actually reasonable for this route/date

**Recommendation**: If you need to travel on December 20 specifically, I'd suggest booking the $1,150 Momondo option soon. If you have flexibility, flying a few days earlier (Dec 17-19) or later (Dec 21-23) could save $300-500.

Would you like me to check alternative dates?

---

## Example 8: Error Handling - No Results

### Conversation

**User**: Can you check if GBP 250 is good for Manchester to Ibiza round-trip on Aug 30? Flight ZZ1234.

**Agent** (activates skill):
Let me search for that flight.

*[Searches but gets no results]*

**No results found**

Navifare couldn't find current prices for this exact itinerary.

**Possible issues:**
1. **Airline code "ZZ"** is not recognized in our database
2. **Flight number 1234** may be incorrect or the flight may not exist
3. The route may not be currently scheduled for Aug 30

**Can you help me verify:**
- Which airline operates this flight? (Ryanair, easyJet, Jet2?)
- Are you sure about the flight number ZZ1234?
- Is this a direct flight or with connections?
- What's the return flight details?

**User**: Oh sorry, it's Jet2 flight LS449 outbound and LS450 return on Sep 6!

**Agent**:
No problem! Let me search for Jet2 LS449/LS450 now.

*[Searches with correct airline/flight]*

**Found better prices!**
... [continues with normal results]

---

## Key Patterns from Examples

### What Triggers the Skill
1. "I found a flight for $X on [site]"
2. "Is this a good price?"
3. "Can you beat this deal?"
4. Screenshot of booking site
5. "I'm about to book..."
6. "Should I book this flight?"

### What Information to Extract
- **Route**: Departure and arrival airports (IATA codes)
- **Date(s)**: Departure date, return date
- **Flight(s)**: Airline code + flight number(s) for both legs
- **Times**: Departure and arrival times (24-hour format)
- **Class**: Economy, Premium Economy, Business, First
- **Passengers**: Adults, children, infants
- **Reference Price**: Amount user saw + currency

### How to Handle Missing Data
1. **Ask specific questions** -- don't guess
2. **Reference documentation** -- check AIRPORTS.md, AIRLINES.md
3. **Provide examples** -- show format you need
4. **Be patient** -- walk user through each missing field

### How to Present Results
1. **Clear comparison** -- reference price vs best found
2. **Savings calculation** -- amount and percentage
3. **Top 3-5 options** -- formatted table
4. **Clickable links** -- make booking easy
5. **Timestamp** -- show when prices were checked
6. **Context** -- explain price trends, seasonality
7. **Recommendations** -- guide user to best choice

### Edge Cases to Handle
- No results: Verify flight details, suggest alternatives
- Price increased: Warn user, explain demand
- Price matched: Validate user's research
- Price decreased: Celebrate savings!
- Timeout: Show partial results, explain delay
- Unclear airports: Clarify multi-airport cities
- Codeshares: Use operating carrier
- Past dates: Ask for correct year/date
- One-way flights: Explain round-trip only limitation

---

These examples demonstrate the full workflow from user inquiry to actionable booking recommendations. Always prioritize clarity, accuracy, and helpfulness.
