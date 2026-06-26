# Provider Registry - Parking Radar

Use this matrix to choose the right parking surface before searching.

| Market | Strong user-facing platforms | Best for | Transaction model | API status |
|--------|------------------------------|----------|-------------------|------------|
| Global fallback | Parkopedia, Google Maps, Apple Maps | Discovery, facility details, cross-border first pass | Discovery first; booking depends on downstream operator | Parkopedia has commercial data products; maps APIs vary by provider |
| United States | SpotHero, ParkWhiz, BestParking, ParkMobile, PayByPhone | Airports, downtown garages, events, venue parking, municipal payment | Reservation plus payment, with strong event and airport inventory | SpotHero and ParkWhiz expose developer or partner APIs; others are mostly commercial or closed |
| Canada | SpotHero in some cities, ParkWhiz or BestParking where inventory exists, ParkMobile, PayByPhone, HONK, operator-native lots | Downtowns, airports, municipal or operator payment | Mixed reservation and payment | Mostly closed or partner APIs; verify city by city |
| United Kingdom | JustPark, JustPark EventPass, RingGo, Q-Park, APCOA Connect, PayByPhone, YourParkingSpace | Stadiums, stations, city centers, driveway and garage rentals | Reservation, driveway marketplace, and payment-app mix | JustPark offers partner integrations; most others do not show open public booking APIs |
| France and Belgium | Onepark, Q-Park, Indigo Neo, EasyPark, PayByPhone, Zenpark, operator-native sites | Rail, airport, central-city garages, recurring urban parking | Reservation plus payment, with some monthly products | Mostly commercial or closed APIs |
| Spain, Portugal, and Italy | Parclick, Onepark in some corridors, EasyPark, PayByPhone, operator-native airport or city operators | Airports, tourist centers, urban garages, station parking | Reservation plus local payment apps | Mostly commercial or closed APIs |
| Nordics and DACH | EasyPark, Parkster, Q-Park, APCOA, city operators | Payment-heavy city parking with some off-street booking | Payment first, reservations where operators support them | EasyPark has developer and commercial APIs; most others are closed |
| Australia and New Zealand | Secure Parking, Wilson Parking, Care Park, Parkable, operator-native airport parking | CBD garages, airport parking, workplace or recurring use | Reservation and operator-native payment | Public booking APIs are uncommon |
| Singapore | Parking.sg plus agency or operator-native parking flows | On-street and public-space session payment | Payment first, not broad marketplace reservation | No broad public booking API found in this research |
| Dubai and UAE | Parkin, RTA parking flows, mall or airport operator apps | City payment, district parking, operator-specific garages | Payment first, operator-specific reservation | No broad public booking API found in this research |
| India | Park+, operator-native parking, mall or airport systems | Urban discovery, digital payment, car services around parking | Mixed payment and operator flows | No broad open booking API found; integration is mostly commercial |
| Hong Kong | Official open data plus operator-native parking systems | Real-time occupancy, government or facility discovery | Data plus operator transaction flows | Public parking-vacancy APIs exist via the government data portal |
| Japan | Operator-native systems plus discovery surfaces such as Parkopedia and local car-park databases | Discovery, city-specific operator lookup, station parking | Mostly operator-native, city-specific | Public reservation APIs are not common in this research |

## How to Read the Matrix

- Discovery-first markets: start with maps and a broad directory, then confirm operator-native rules.
- Payment-first markets: the user may still need to find a bay before the app becomes useful.
- Reservation-first markets: pre-booking is realistic and often better for airports, events, and dense downtowns.
- Closed API markets: plan for browser or app handoff, not direct automation.
