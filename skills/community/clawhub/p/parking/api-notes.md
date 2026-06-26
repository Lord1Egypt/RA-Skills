# API Notes - Parking Radar

Use this file when the user asks whether a parking platform has an API.

| Platform | Evidence | Access model | What it suggests |
|----------|----------|--------------|------------------|
| Parkopedia | Official parking data and parking payments products | Commercial platform and data products | Strong candidate for global discovery, data licensing, and partner integrations |
| SpotHero | Official developer portal and business integrations | Partner or approved developer access | API-backed reservation flows exist, but not every capability is open without partnership |
| ParkWhiz | Official `parking.dev` API docs, widgets, and v4 endpoints | Public documentation with keys and partner setup | Strong option for North America parking search or booking integrations |
| EasyPark | Official developer portal and API policy | Commercial or approved access | Useful for payment and some market-specific integrations, especially in Europe and the US |
| Hong Kong government parking data | Official public vacancy API via data portal | Public open data | Real-time parking-vacancy signals can be used without a commercial partnership |
| JustPark | Official partner, venue, and EventPass integrations | Commercial or partner access | Integration exists, but not as a broad open booking API in this research |
| Q-Park | Public booking and pre-book surfaces, but no open API discovered here | Closed or unclear | Good user-facing booking surface; weak assumption for automation |
| RingGo | Public consumer app and business pages, no open booking API discovered here | Closed or unclear | Strong payment workflow, not a safe assumption for reservation APIs |
| Parclick | Public booking product, no open API discovered here | Closed or unclear | Good user-facing reservation surface in Southern Europe |
| Onepark | Public booking product, no open API discovered here | Closed or unclear | Good user-facing reservation surface for France and nearby markets |
| ParkMobile | Official commercial parking-tech platform | Commercial or operator access | Strong user-facing payment and reserve workflows, but assume business integration rather than open public API |
| Parking.sg, Park+, Parkin | Public user apps, no open public booking API discovered here | Closed or unclear | Plan for app handoff, not direct automation |

## Interpretation Rules

- Public docs do not automatically mean self-serve production access.
- Closed API does not make a provider useless; it only changes the workflow from automation to user handoff.
- Booking API, pricing API, occupancy API, and payment API are different products. Verify which one the user actually needs.
