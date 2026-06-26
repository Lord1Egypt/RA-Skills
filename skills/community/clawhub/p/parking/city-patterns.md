# City Patterns - Parking Radar

Use this file when the user names a city but not a provider.

| City cluster | First checks | Strong booking surfaces | Common gaps |
|--------------|--------------|-------------------------|-------------|
| New York, Chicago, Boston, Washington, San Francisco | Google Maps or Apple Maps plus ParkWhiz or SpotHero | SpotHero, ParkWhiz, BestParking, operator-native garages | Street-parking apps do not guarantee a bay |
| Los Angeles, Miami, Las Vegas, event-heavy US markets | Venue or airport parking first, then aggregator | SpotHero, ParkWhiz, ParkMobile Reserve, operator-native resorts | Walking distance and event surge pricing distort the obvious choice |
| Toronto, Montreal, Vancouver | Maps plus PayByPhone, ParkMobile, HONK, and operator sites | Operator-native airport and downtown garages, selected aggregators | Coverage varies sharply by municipality |
| London | JustPark, RingGo, Q-Park, APCOA, PayByPhone | JustPark and Q-Park Prebook, station and airport operator sites | Many apps start sessions only after the bay is found |
| Manchester, Birmingham, Glasgow, Liverpool | JustPark, Q-Park, RingGo, APCOA, YourParkingSpace | Q-Park, JustPark, station and venue operators | Driveway inventory quality varies by host |
| Paris, Brussels, Lille | Onepark, Q-Park, Indigo, EasyPark, operator-native station parking | Onepark, Q-Park, rail and airport operator sites | Urban payment apps often matter more than marketplaces for short stays |
| Madrid, Barcelona, Lisbon, Rome, Milan | Parclick, EasyPark, PayByPhone, operator-native airport or rail parking | Parclick, operator-native airport or central garages | Tourist-center inventory changes quickly; verify entry window and vehicle size |
| Stockholm, Copenhagen, Helsinki, Oslo, Berlin, Hamburg, Munich | EasyPark, Parkster, Q-Park, APCOA, city operators | Operator-native booking where available | Many workflows are payment-first rather than reservation-first |
| Sydney, Melbourne, Brisbane, Perth | Secure Parking, Wilson Parking, Care Park | Secure Parking and Wilson pre-book flows | CBD parking is highly operator-native; cross-market aggregators are weaker |
| Auckland, Wellington, Christchurch | Wilson, Care Park, Parkable for workplace or recurring use | Operator-native booking | Inventory can be fragmented across operators |
| Singapore | Parking.sg plus official agency or operator information | Operator-native parking linked to venue or property | Payment and enforcement are strong; reservation marketplaces are limited |
| Dubai | Parkin or RTA parking plus mall, airport, and venue operators | Operator-native booking for malls or airports | District payment does not equal guaranteed off-street inventory |
| Hong Kong | Government vacancy data, maps, and operator sites | Operator-native parking after vacancy signal | Real-time data exists, but booking still depends on the facility |
| Tokyo, Osaka, Kyoto | Discovery first, then local operator or facility site | Operator-native station, mall, or hotel parking | English-friendly reservation surfaces are inconsistent |
| Delhi, Mumbai, Bengaluru | Park+ plus operator-native mall or airport systems | Operator-native or venue-linked parking | Coverage is uneven and often local to the operator or complex |

## Escalation Rule

If the city is not listed:
- start with maps plus Parkopedia
- identify whether the local stack is reservation-first, payment-first, or operator-native
- save the outcome in `cities.md` only after the pattern is clear
