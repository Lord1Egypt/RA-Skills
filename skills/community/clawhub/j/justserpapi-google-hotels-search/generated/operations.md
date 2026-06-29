# Google SERP Hotels Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `hotels/search`.

## `hotelsSearch`

- Method: `GET`
- Path: `/api/v1/google/hotels/search`
- Summary: Search
- Description: Get Google hotels Search data, including prices, ratings, and availability details, for travel comparison and hospitality market analysis.
- Tags: `Google Hotels`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The destination or specific hotel name you are searching for (e.g., 'Paris', 'Hilton New York'). |
| `check_in_date` | `query` | yes | `string` | n/a | The hotel check-in date in 'YYYY-MM-DD' format (e.g., '2026-05-20'). |
| `check_out_date` | `query` | yes | `string` | n/a | The hotel check-out date in 'YYYY-MM-DD' format (e.g., '2026-05-25'). |
| `next_page_token` | `query` | no | `string` | n/a | The token used to retrieve the next page of hotel results. This token is found in the 'next_page_token' field of a previous response. |
| `adults` | `query` | no | `integer` | n/a | The number of adults staying in the room. |
| `children` | `query` | no | `integer` | n/a | The number of children staying in the room. |
| `children_ages` | `query` | no | `string` | n/a | The ages of the children, separated by commas (e.g., '5,10'). The number of ages must match the 'children' parameter. |
| `html` | `query` | no | `boolean` | n/a | Set to true to return the raw HTML of the Google search results page alongside the structured data. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `currency` | `query` | no | `string` | n/a | The three-letter ISO currency code for displaying prices (e.g., 'USD', 'EUR'). See <a href="/reference/hotels/google-hotels-currency">Google Hotels Currency</a>. |
| `sort_by` | `query` | no | `string` | n/a | The criteria to sort hotel results. Supported values: '3' (Lowest price), '8' (Highest rating), '13' (Most reviews). |
| `min_price` | `query` | no | `string` | n/a | Minimum price filter for the hotel stay. |
| `max_price` | `query` | no | `string` | n/a | Maximum price filter for the hotel stay. |
| `property_types` | `query` | no | `string` | n/a | Filter by hotel property types. See the <a href="/reference/hotels/google-hotels-property-types">Google Property Types</a> for the full list of supported hotel property types. For vacation rentals, refer to the <a href="/reference/hotels/google-hotels-vacation-rentals-property-types">Google Hotels Vacation Rentals Property Types</a>. |
| `amenities` | `query` | no | `string` | n/a | Filter by specific amenities (e.g., '35' for free Wi-Fi). <a href="/reference/hotels/google-hotels-amenities">Google Hotels Amenities</a> (hotel amenities). <a href="/reference/hotels/google-hotels-vacation-rentals-amenities">Google Hotels Vacation Rentals Amenities</a> (vacation rental amenities) |
| `rating` | `query` | no | `string` | n/a | Filter by minimum guest rating. Supported values: '7' (3.5+), '8' (4.0+), '9' (4.5+). |
| `brands` | `query` | no | `string` | n/a | Filter by specific hotel brand IDs. IDs can be comma-separated. |
| `hotel_class` | `query` | no | `string` | n/a | Filter by hotel star ratings. Supported values: '2', '3', '4', '5'. Can be comma-separated. |
| `free_cancellation` | `query` | no | `string` | n/a | Filter for hotels that offer free cancellation. Set to '1' or 'true' to enable. |
| `special_offers` | `query` | no | `string` | n/a | Filter for hotels currently offering special deals or discounts. Set to '1' or 'true' to enable. |
| `eco_certified` | `query` | no | `string` | n/a | Filter for hotels that are eco-certified. Set to '1' or 'true' to enable. |
| `vacation_rentals` | `query` | no | `boolean` | n/a | Set to true to search for vacation rentals instead of standard hotels. |
| `bedrooms` | `query` | no | `string` | n/a | Minimum number of bedrooms required (applies to vacation rentals). |
| `bathrooms` | `query` | no | `string` | n/a | Minimum number of bathrooms required (applies to vacation rentals). |
| `property_token` | `query` | no | `string` | n/a | The unique token for a specific hotel property to fetch detailed information. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
