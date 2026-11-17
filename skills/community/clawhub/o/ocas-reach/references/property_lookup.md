# Property Lookup — source reference for ocas-reach

## RealtyAPI (Redfin)
- Base: `https://redfin.realtyapi.io`
- Auth: `RT_KEY` env var (set in `~/.hermes/.env`)
- Header: `x-realtyapi-key`

## Working Endpoints

### Search
| Endpoint | Params | Notes |
|----------|--------|-------|
| `GET /autocomplete` | `query`, `listingStatus` (`"For_Sale"` or `"For_Sale_or_Sold"`) | Returns places, addresses, schools, agents |
| `GET /search/byaddress` | `propertyaddress` | Returns paginated results |

### Details
| Endpoint | Params | Notes |
|----------|--------|-------|
| `GET /detailsbyaddress` | `property_address` | May return `"Property address not found"` for off-market |
| `GET /detailsbyurl` | `property_url` | Unreliable, often returns `searchResult` error |
| `GET /detailsbyid` | `property_id`, `listing_id` | Needs IDs from autocomplete |

### Granular (need property_id + listing_id)
- `avm`, `walkScore`, `floodInfo`, `amenities`, `popularityInfo`
- `agentInfo`, `mortgageCalculatorInfo`, `priceDropInfo`
- `mainHouseInfoPanelInfo`, `hotMarketInfo`, `tourInsights`

## RealtyAPI (Zillow)
- Base: `https://zillow.realtyapi.io`
- `GET /client/byaddress` — param: `propertyaddress`
- `GET /byaddress` — param: `propertyaddress`
- `GET /search/byaddress` — param: `propertyaddress`

## City/County Assessor Fallback
- SF OpenData: `https://data.sfgov.org/resource/wv5m-vpq2.json`
- Query: `$where` with property_location like pattern
- Returns assessed values (land + improvement), not market values

## Pitfalls
- Redfin autocomplete: `hasFakeResults: true` = no dedicated page (map-only result)
- `detailsByAddress` returns `status: 404` in JSON body for off-market (200 HTTP)
- Zillow browser access blocked by PerimeterX bot detection
- `realtor.realtyapi.io` — DNS fails
- `api.realtyapi.io` — DNS fails
- Assessor data = Prop 13 assessed value, NOT current market value
