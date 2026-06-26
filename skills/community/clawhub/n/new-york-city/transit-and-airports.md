# Transit and Airports — New York City

Use this file for subway logic, bus and ferry decisions, airport transfers, and daily commute design.

## NYC Transit Rule

Time, transfers, stairs, and reliability beat straight-line distance.

## Core Patterns

### 1. Subway first, but not blindly
- The subway solves most city movement, but service pattern, walking distance, and late-night changes matter.
- One-seat ride logic is often worth more than a theoretically cheaper neighborhood.

### 2. Buses, ferries, and regional rail are support tools
- Buses are useful when the subway grid is weak, ferries can be excellent for specific corridors, and commuter rail matters for airport or suburb access.
- The right answer depends on the actual start and end point, not a general preference.

### 3. Airport transfers need realism
- JFK, LaGuardia, and Newark solve different airline and routing needs.
- The best transfer depends on luggage, budget, arrival time, children, weather, and comfort with stairs and transfers.

## Commute Design Questions

- Daily office, hybrid, or occasional?
- Must they reach Midtown, Downtown, Brooklyn, Queens campus corridors, or airports?
- Can they tolerate crowded transfers and late-night service variation?
- Does the route still work in rain, heat, or after an event?

## Common Mistakes

- Calling a place "easy" because the map looks close.
- Underestimating last-mile walking and stairs.
- Overusing ride-hail for trips the subway handles better.
- Choosing an airport path that works only with no luggage and perfect timing.
