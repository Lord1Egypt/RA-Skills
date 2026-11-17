#!/usr/bin/env bash
# Crawlora REST helper — minimal, dependency-free (curl only).
# Calls https://api.crawlora.net/api/v1 with your Crawlora API key.
# Get a free key (2,000 credits/mo, no card) at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills.
#
# Usage:
#   GET  :  crawlora.sh /amazon/search k=laptop s=relevanceblender
#   GET  :  crawlora.sh /youtube/transcript/dQw4w9WgXcQ
#   POST :  crawlora.sh -X POST /google/search '{"keyword":"web scraping api","language":"en","country":"us"}'
#   POST :  crawlora.sh -X POST /google/trends/explore/interest-over-time '{"keywords":["bitcoin"]}'
#
# GET key=value args become the query string. POST takes one JSON body argument
# (or pass it with -d '<json>'). Prints raw JSON to stdout — pipe into `jq`.
set -euo pipefail

: "${CRAWLORA_API_KEY:?Set CRAWLORA_API_KEY first — get a free key at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills}"
# The key is written to a curl config file below. Restrict it to the key
# alphabet so a newline, quote, or config directive cannot alter that file.
case "$CRAWLORA_API_KEY" in
  *[!A-Za-z0-9._-]*) echo "invalid CRAWLORA_API_KEY format" >&2; exit 2 ;;
esac
# Fixed, non-overridable: an env-configurable base URL would let anything that
# can set CRAWLORA_API_BASE redirect this key to an attacker-controlled host.
base="https://api.crawlora.net/api/v1"

method="GET"
body=""
args=()
while [ $# -gt 0 ]; do
  case "$1" in
    -X)
      [ $# -ge 2 ] || { echo "-X requires an HTTP method" >&2; exit 2; }
      method="$2"; shift 2 ;;
    -d)
      [ $# -ge 2 ] || { echo "-d requires a request body" >&2; exit 2; }
      body="$2"; shift 2 ;;
    *)  args+=("$1"); shift ;;
  esac
done

[ "${#args[@]}" -ge 1 ] || { echo "usage: crawlora.sh [-X METHOD] /path [k=v ... | json-body]" >&2; exit 2; }
path="${args[0]}"
rest=("${args[@]:1}")

# This skill's helper is limited to its documented Crawlora route set. Keep
# caller-account surfaces and unrelated API routes out of the helper even if
# someone supplies an undocumented path directly.
case "$method" in
  GET|POST) ;;
  *)
    echo "only GET and POST are supported by the product-price-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the product-price-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /adidas/product) route_allowed=true ;;
  /adidas/product/review-topics) route_allowed=true ;;
  /adidas/product/reviews) route_allowed=true ;;
  /adidas/search) route_allowed=true ;;
  /adidas/store) route_allowed=true ;;
  /adidas/stores) route_allowed=true ;;
  /adidas/suggest) route_allowed=true ;;
  /aliexpress/reviews) route_allowed=true ;;
  /aliexpress/search) route_allowed=true ;;
  /aliexpress/search-filters) route_allowed=true ;;
  /amazon/charts) route_allowed=true ;;
  /amazon/charts/categories) route_allowed=true ;;
  /amazon/search) route_allowed=true ;;
  /bestbuy/brands) route_allowed=true ;;
  /bestbuy/categories) route_allowed=true ;;
  /bestbuy/categories/trending) route_allowed=true ;;
  /bestbuy/category) route_allowed=true ;;
  /bestbuy/category/subcategories) route_allowed=true ;;
  /bestbuy/product) route_allowed=true ;;
  /bestbuy/product/questions) route_allowed=true ;;
  /bestbuy/product/related) route_allowed=true ;;
  /bestbuy/product/reviews) route_allowed=true ;;
  /bestbuy/search) route_allowed=true ;;
  /bestbuy/stores) route_allowed=true ;;
  /bigcommerce/category) route_allowed=true ;;
  /bigcommerce/product) route_allowed=true ;;
  /bigcommerce/search) route_allowed=true ;;
  /boots/search) route_allowed=true ;;
  /boots/suggest) route_allowed=true ;;
  /chewy/brands) route_allowed=true ;;
  /chewy/categories) route_allowed=true ;;
  /chewy/category) route_allowed=true ;;
  /chewy/facets) route_allowed=true ;;
  /chewy/gtin-lookup) route_allowed=true ;;
  /chewy/inventory) route_allowed=true ;;
  /chewy/item-attributes) route_allowed=true ;;
  /chewy/product) route_allowed=true ;;
  /chewy/product-questions) route_allowed=true ;;
  /chewy/product-reviews) route_allowed=true ;;
  /chewy/products) route_allowed=true ;;
  /chewy/search) route_allowed=true ;;
  /chewy/suggest) route_allowed=true ;;
  /chewy/variants) route_allowed=true ;;
  /costco/categories) route_allowed=true ;;
  /costco/search) route_allowed=true ;;
  /costco/warehouses) route_allowed=true ;;
  /cvs/brands) route_allowed=true ;;
  /cvs/categories) route_allowed=true ;;
  /cvs/category) route_allowed=true ;;
  /cvs/search) route_allowed=true ;;
  /cvs/store-locator) route_allowed=true ;;
  /ebay/live/streams) route_allowed=true ;;
  /ebay/live/streams/batch) route_allowed=true ;;
  /ebay/search) route_allowed=true ;;
  /hm/categories) route_allowed=true ;;
  /hm/listing) route_allowed=true ;;
  /hm/search) route_allowed=true ;;
  /hm/search/suggestions) route_allowed=true ;;
  /hm/stores) route_allowed=true ;;
  /homedepot/categories) route_allowed=true ;;
  /homedepot/category) route_allowed=true ;;
  /homedepot/search) route_allowed=true ;;
  /homedepot/suggest) route_allowed=true ;;
  /ikea/availability) route_allowed=true ;;
  /ikea/categories) route_allowed=true ;;
  /ikea/category) route_allowed=true ;;
  /ikea/product) route_allowed=true ;;
  /ikea/reviews) route_allowed=true ;;
  /ikea/search) route_allowed=true ;;
  /ikea/store) route_allowed=true ;;
  /ikea/stores) route_allowed=true ;;
  /ikea/suggest) route_allowed=true ;;
  /kohls/category) route_allowed=true ;;
  /kohls/product/reviews) route_allowed=true ;;
  /kohls/stores) route_allowed=true ;;
  /kohls/suggest) route_allowed=true ;;
  /lazada/categories) route_allowed=true ;;
  /lazada/category-products) route_allowed=true ;;
  /lazada/home) route_allowed=true ;;
  /lazada/product) route_allowed=true ;;
  /lazada/search) route_allowed=true ;;
  /lululemon/categories) route_allowed=true ;;
  /lululemon/category) route_allowed=true ;;
  /lululemon/outfit) route_allowed=true ;;
  /lululemon/stores) route_allowed=true ;;
  /macys/product/reviews) route_allowed=true ;;
  /macys/suggest) route_allowed=true ;;
  /nike/categories) route_allowed=true ;;
  /nike/product) route_allowed=true ;;
  /nike/product/availability) route_allowed=true ;;
  /nike/product/details) route_allowed=true ;;
  /nike/product/recommendations) route_allowed=true ;;
  /nike/product/reviews) route_allowed=true ;;
  /nike/search) route_allowed=true ;;
  /nike/stores) route_allowed=true ;;
  /nike/suggest) route_allowed=true ;;
  /oldnavy/categories) route_allowed=true ;;
  /oldnavy/category) route_allowed=true ;;
  /oldnavy/product) route_allowed=true ;;
  /oldnavy/product/availability) route_allowed=true ;;
  /oldnavy/product/reviews) route_allowed=true ;;
  /oldnavy/search) route_allowed=true ;;
  /oldnavy/stores) route_allowed=true ;;
  /otto/categories) route_allowed=true ;;
  /otto/product) route_allowed=true ;;
  /otto/search) route_allowed=true ;;
  /samsclub/category) route_allowed=true ;;
  /samsclub/departments) route_allowed=true ;;
  /sephora/brands) route_allowed=true ;;
  /sephora/categories) route_allowed=true ;;
  /sephora/category) route_allowed=true ;;
  /sephora/product) route_allowed=true ;;
  /sephora/product/questions) route_allowed=true ;;
  /sephora/product/reviews) route_allowed=true ;;
  /sephora/search) route_allowed=true ;;
  /sephora/stores) route_allowed=true ;;
  /sephora/suggest) route_allowed=true ;;
  /shein/category/filters) route_allowed=true ;;
  /shein/category/goods) route_allowed=true ;;
  /shein/category/nav) route_allowed=true ;;
  /shein/products/aggregation-filters) route_allowed=true ;;
  /shein/products/detail) route_allowed=true ;;
  /shein/products/search) route_allowed=true ;;
  /shein/search/autocomplete) route_allowed=true ;;
  /shein/search/keywords) route_allowed=true ;;
  /shop-app/analysis) route_allowed=true ;;
  /shop-app/categories) route_allowed=true ;;
  /shop-app/search) route_allowed=true ;;
  /shop-app/suggestions) route_allowed=true ;;
  /shopify/collections) route_allowed=true ;;
  /shopify/pages) route_allowed=true ;;
  /shopify/products) route_allowed=true ;;
  /shopify/search/suggest) route_allowed=true ;;
  /shopify/sitemap/urls) route_allowed=true ;;
  /shopify/sitemaps) route_allowed=true ;;
  /shopify/store) route_allowed=true ;;
  /sparkfun/categories) route_allowed=true ;;
  /sparkfun/category) route_allowed=true ;;
  /sparkfun/product) route_allowed=true ;;
  /sparkfun/search) route_allowed=true ;;
  /target/categories) route_allowed=true ;;
  /target/category-products) route_allowed=true ;;
  /target/filter-options) route_allowed=true ;;
  /target/product) route_allowed=true ;;
  /target/questions) route_allowed=true ;;
  /target/reviews) route_allowed=true ;;
  /target/search) route_allowed=true ;;
  /target/stores) route_allowed=true ;;
  /tokopedia/autocomplete) route_allowed=true ;;
  /tokopedia/category) route_allowed=true ;;
  /tokopedia/home) route_allowed=true ;;
  /tokopedia/home/tabs) route_allowed=true ;;
  /tokopedia/product) route_allowed=true ;;
  /tokopedia/product/review-filters) route_allowed=true ;;
  /tokopedia/search) route_allowed=true ;;
  /tokopedia/search/filters) route_allowed=true ;;
  /ulta/categories) route_allowed=true ;;
  /ulta/category) route_allowed=true ;;
  /ulta/product/questions) route_allowed=true ;;
  /ulta/product/reviews) route_allowed=true ;;
  /ulta/search) route_allowed=true ;;
  /ulta/stores) route_allowed=true ;;
  /ulta/suggest) route_allowed=true ;;
  /walgreens/stores) route_allowed=true ;;
  /walmart/search) route_allowed=true ;;
  /wayfair/categories) route_allowed=true ;;
  /wayfair/category) route_allowed=true ;;
  /wish/categories) route_allowed=true ;;
  /wish/search) route_allowed=true ;;
  /wish/suggest) route_allowed=true ;;
  /zalando/categories) route_allowed=true ;;
  /zalando/category) route_allowed=true ;;
  /zalando/markets) route_allowed=true ;;
  /zalando/product) route_allowed=true ;;
  /zalando/search) route_allowed=true ;;
  /zalando/suggest) route_allowed=true ;;
  /zappos/brand) route_allowed=true ;;
  /zappos/brands) route_allowed=true ;;
  /zappos/search) route_allowed=true ;;
  /zappos/suggest) route_allowed=true ;;
  /zara/categories) route_allowed=true ;;
  /zara/search) route_allowed=true ;;
  /zara/stores) route_allowed=true ;;
  /zara/suggest) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/amazon/product/[^/]+$'
  '^/amazon/suggest/[^/]+$'
  '^/costco/product/[^/]+$'
  '^/costco/product/[^/]+/availability$'
  '^/costco/product/[^/]+/reviews$'
  '^/cvs/product-ingredients/[^/]+$'
  '^/cvs/product/[^/]+$'
  '^/ebay/item/[^/]+$'
  '^/ebay/live/streams/[^/]+$'
  '^/ebay/live/streams/[^/]+/items$'
  '^/ebay/seller/[^/]+$'
  '^/ebay/seller/[^/]+/about$'
  '^/ebay/seller/[^/]+/feedback$'
  '^/ebay/seller/[^/]+/shop$'
  '^/hm/product/[^/]+$'
  '^/hm/product/[^/]+/related$'
  '^/homedepot/product/[^/]+$'
  '^/homedepot/product/[^/]+/questions$'
  '^/lululemon/product/[^/]+$'
  '^/macys/product/[^/]+$'
  '^/samsclub/content/[^/]+$'
  '^/samsclub/product/[^/]+$'
  '^/samsclub/product/[^/]+/related$'
  '^/shop-app/products/[^/]+$'
  '^/shop-app/products/[^/]+/related$'
  '^/shop-app/products/[^/]+/reviews$'
  '^/shop-app/products/[^/]+/shop$'
  '^/shop-app/products/[^/]+/variant$'
  '^/shop-app/products/[^/]+/variants$'
  '^/shop-app/shops/[^/]+$'
  '^/shop-app/shops/[^/]+/collections/[^/]+/products$'
  '^/shop-app/shops/[^/]+/locations$'
  '^/shop-app/shops/[^/]+/products$'
  '^/shop-app/shops/[^/]+/reviews$'
  '^/shop-app/shops/[^/]+/typeahead$'
  '^/shopify/collections/[^/]+/products$'
  '^/shopify/pages/[^/]+$'
  '^/shopify/products/[^/]+$'
  '^/shopify/products/[^/]+/recommendations$'
  '^/ulta/product/[^/]+$'
  '^/walmart/product/[^/]+$'
  '^/walmart/product/[^/]+/reviews$'
  '^/wayfair/product/[^/]+$'
  '^/wish/product/[^/]+$'
  '^/wish/product/[^/]+/related$'
  '^/wish/product/[^/]+/reviews$'
  '^/zappos/product/[^/]+$'
  '^/zara/category/[^/]+/products$'
  '^/zara/product/[^/]+$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the product-price-research skill catalog" >&2
  exit 2
fi

# Enforce the documented HTTP method for each route, not just the global method set.
route_method_allowed=false
route_method_regexes=(
  '^GET:/adidas/product$'
  '^GET:/adidas/product/review-topics$'
  '^GET:/adidas/product/reviews$'
  '^GET:/adidas/search$'
  '^GET:/adidas/store$'
  '^GET:/adidas/stores$'
  '^GET:/adidas/suggest$'
  '^GET:/aliexpress/reviews$'
  '^GET:/aliexpress/search$'
  '^GET:/aliexpress/search-filters$'
  '^GET:/amazon/charts$'
  '^GET:/amazon/charts/categories$'
  '^GET:/amazon/product/[^/]+$'
  '^GET:/amazon/search$'
  '^GET:/amazon/suggest/[^/]+$'
  '^GET:/bestbuy/brands$'
  '^GET:/bestbuy/categories$'
  '^GET:/bestbuy/categories/trending$'
  '^GET:/bestbuy/category$'
  '^GET:/bestbuy/category/subcategories$'
  '^GET:/bestbuy/product$'
  '^GET:/bestbuy/product/questions$'
  '^GET:/bestbuy/product/related$'
  '^GET:/bestbuy/product/reviews$'
  '^GET:/bestbuy/search$'
  '^GET:/bestbuy/stores$'
  '^GET:/bigcommerce/category$'
  '^GET:/bigcommerce/product$'
  '^GET:/bigcommerce/search$'
  '^GET:/boots/search$'
  '^GET:/boots/suggest$'
  '^GET:/chewy/brands$'
  '^GET:/chewy/categories$'
  '^GET:/chewy/category$'
  '^GET:/chewy/facets$'
  '^GET:/chewy/gtin-lookup$'
  '^GET:/chewy/inventory$'
  '^GET:/chewy/item-attributes$'
  '^GET:/chewy/product$'
  '^GET:/chewy/product-questions$'
  '^GET:/chewy/product-reviews$'
  '^GET:/chewy/products$'
  '^GET:/chewy/search$'
  '^GET:/chewy/suggest$'
  '^GET:/chewy/variants$'
  '^GET:/costco/categories$'
  '^GET:/costco/product/[^/]+$'
  '^GET:/costco/product/[^/]+/availability$'
  '^GET:/costco/product/[^/]+/reviews$'
  '^GET:/costco/search$'
  '^GET:/costco/warehouses$'
  '^GET:/cvs/brands$'
  '^GET:/cvs/categories$'
  '^GET:/cvs/category$'
  '^GET:/cvs/product-ingredients/[^/]+$'
  '^GET:/cvs/product/[^/]+$'
  '^GET:/cvs/search$'
  '^GET:/cvs/store-locator$'
  '^GET:/ebay/item/[^/]+$'
  '^GET:/ebay/live/streams$'
  '^GET:/ebay/live/streams/[^/]+$'
  '^GET:/ebay/live/streams/[^/]+/items$'
  '^GET:/ebay/live/streams/batch$'
  '^GET:/ebay/seller/[^/]+$'
  '^GET:/ebay/seller/[^/]+/about$'
  '^GET:/ebay/seller/[^/]+/feedback$'
  '^GET:/ebay/seller/[^/]+/shop$'
  '^GET:/hm/categories$'
  '^GET:/hm/listing$'
  '^GET:/hm/product/[^/]+$'
  '^GET:/hm/product/[^/]+/related$'
  '^GET:/hm/search$'
  '^GET:/hm/search/suggestions$'
  '^GET:/hm/stores$'
  '^GET:/homedepot/categories$'
  '^GET:/homedepot/category$'
  '^GET:/homedepot/product/[^/]+$'
  '^GET:/homedepot/product/[^/]+/questions$'
  '^GET:/homedepot/search$'
  '^GET:/homedepot/suggest$'
  '^GET:/ikea/availability$'
  '^GET:/ikea/categories$'
  '^GET:/ikea/category$'
  '^GET:/ikea/product$'
  '^GET:/ikea/reviews$'
  '^GET:/ikea/search$'
  '^GET:/ikea/store$'
  '^GET:/ikea/stores$'
  '^GET:/ikea/suggest$'
  '^GET:/kohls/category$'
  '^GET:/kohls/product/reviews$'
  '^GET:/kohls/stores$'
  '^GET:/kohls/suggest$'
  '^GET:/lazada/categories$'
  '^GET:/lazada/category-products$'
  '^GET:/lazada/home$'
  '^GET:/lazada/product$'
  '^GET:/lazada/search$'
  '^GET:/lululemon/categories$'
  '^GET:/lululemon/category$'
  '^GET:/lululemon/outfit$'
  '^GET:/lululemon/product/[^/]+$'
  '^GET:/lululemon/stores$'
  '^GET:/macys/product/[^/]+$'
  '^GET:/macys/product/reviews$'
  '^GET:/macys/suggest$'
  '^GET:/nike/categories$'
  '^GET:/nike/product$'
  '^GET:/nike/product/availability$'
  '^GET:/nike/product/details$'
  '^GET:/nike/product/recommendations$'
  '^GET:/nike/product/reviews$'
  '^GET:/nike/search$'
  '^GET:/nike/stores$'
  '^GET:/nike/suggest$'
  '^GET:/oldnavy/categories$'
  '^GET:/oldnavy/category$'
  '^GET:/oldnavy/product$'
  '^GET:/oldnavy/product/availability$'
  '^GET:/oldnavy/product/reviews$'
  '^GET:/oldnavy/search$'
  '^GET:/oldnavy/stores$'
  '^GET:/otto/categories$'
  '^GET:/otto/product$'
  '^GET:/otto/search$'
  '^GET:/samsclub/category$'
  '^GET:/samsclub/content/[^/]+$'
  '^GET:/samsclub/departments$'
  '^GET:/samsclub/product/[^/]+$'
  '^GET:/samsclub/product/[^/]+/related$'
  '^GET:/sephora/brands$'
  '^GET:/sephora/categories$'
  '^GET:/sephora/category$'
  '^GET:/sephora/product$'
  '^GET:/sephora/product/questions$'
  '^GET:/sephora/product/reviews$'
  '^GET:/sephora/search$'
  '^GET:/sephora/stores$'
  '^GET:/sephora/suggest$'
  '^GET:/shein/category/filters$'
  '^GET:/shein/category/goods$'
  '^GET:/shein/category/nav$'
  '^GET:/shein/products/detail$'
  '^GET:/shop-app/analysis$'
  '^GET:/shop-app/categories$'
  '^GET:/shop-app/products/[^/]+$'
  '^GET:/shop-app/products/[^/]+/related$'
  '^GET:/shop-app/products/[^/]+/reviews$'
  '^GET:/shop-app/products/[^/]+/shop$'
  '^GET:/shop-app/products/[^/]+/variant$'
  '^GET:/shop-app/products/[^/]+/variants$'
  '^GET:/shop-app/search$'
  '^GET:/shop-app/shops/[^/]+$'
  '^GET:/shop-app/shops/[^/]+/collections/[^/]+/products$'
  '^GET:/shop-app/shops/[^/]+/locations$'
  '^GET:/shop-app/shops/[^/]+/products$'
  '^GET:/shop-app/shops/[^/]+/reviews$'
  '^GET:/shop-app/shops/[^/]+/typeahead$'
  '^GET:/shop-app/suggestions$'
  '^GET:/shopify/collections$'
  '^GET:/shopify/collections/[^/]+/products$'
  '^GET:/shopify/pages$'
  '^GET:/shopify/pages/[^/]+$'
  '^GET:/shopify/products$'
  '^GET:/shopify/products/[^/]+$'
  '^GET:/shopify/products/[^/]+/recommendations$'
  '^GET:/shopify/search/suggest$'
  '^GET:/shopify/sitemap/urls$'
  '^GET:/shopify/sitemaps$'
  '^GET:/shopify/store$'
  '^GET:/sparkfun/categories$'
  '^GET:/sparkfun/category$'
  '^GET:/sparkfun/product$'
  '^GET:/sparkfun/search$'
  '^GET:/target/categories$'
  '^GET:/target/category-products$'
  '^GET:/target/filter-options$'
  '^GET:/target/product$'
  '^GET:/target/questions$'
  '^GET:/target/reviews$'
  '^GET:/target/search$'
  '^GET:/target/stores$'
  '^GET:/tokopedia/autocomplete$'
  '^GET:/tokopedia/category$'
  '^GET:/tokopedia/home$'
  '^GET:/tokopedia/home/tabs$'
  '^GET:/tokopedia/product$'
  '^GET:/tokopedia/product/review-filters$'
  '^GET:/tokopedia/search$'
  '^GET:/tokopedia/search/filters$'
  '^GET:/ulta/categories$'
  '^GET:/ulta/category$'
  '^GET:/ulta/product/[^/]+$'
  '^GET:/ulta/product/questions$'
  '^GET:/ulta/product/reviews$'
  '^GET:/ulta/search$'
  '^GET:/ulta/stores$'
  '^GET:/ulta/suggest$'
  '^GET:/walgreens/stores$'
  '^GET:/walmart/product/[^/]+$'
  '^GET:/walmart/product/[^/]+/reviews$'
  '^GET:/walmart/search$'
  '^GET:/wayfair/categories$'
  '^GET:/wayfair/category$'
  '^GET:/wayfair/product/[^/]+$'
  '^GET:/wish/categories$'
  '^GET:/wish/product/[^/]+$'
  '^GET:/wish/product/[^/]+/related$'
  '^GET:/wish/product/[^/]+/reviews$'
  '^GET:/wish/search$'
  '^GET:/wish/suggest$'
  '^GET:/zalando/categories$'
  '^GET:/zalando/category$'
  '^GET:/zalando/markets$'
  '^GET:/zalando/product$'
  '^GET:/zalando/search$'
  '^GET:/zalando/suggest$'
  '^GET:/zappos/brand$'
  '^GET:/zappos/brands$'
  '^GET:/zappos/product/[^/]+$'
  '^GET:/zappos/search$'
  '^GET:/zappos/suggest$'
  '^GET:/zara/categories$'
  '^GET:/zara/category/[^/]+/products$'
  '^GET:/zara/product/[^/]+$'
  '^GET:/zara/search$'
  '^GET:/zara/stores$'
  '^GET:/zara/suggest$'
  '^POST:/ebay/search$'
  '^POST:/shein/products/aggregation-filters$'
  '^POST:/shein/products/search$'
  '^POST:/shein/search/autocomplete$'
  '^POST:/shein/search/keywords$'
)
for route_method_regex in ${route_method_regexes[@]+"${route_method_regexes[@]}"}; do
  if [[ "$method:$path" =~ $route_method_regex ]]; then
    route_method_allowed=true
    break
  fi
done
if [ "$route_method_allowed" = false ]; then
  echo "method is not allowed for this product-price-research route" >&2
  exit 2
fi



# Keep the API key out of the curl process command line. A private temporary
# config supplies the header and is removed automatically on exit.
umask 077
curl_config="$(mktemp "${TMPDIR:-/tmp}/crawlora-curl.XXXXXX")"
chmod 600 "$curl_config"
trap 'rm -f "$curl_config"' EXIT
printf 'header = "x-api-key: %s"\n' "$CRAWLORA_API_KEY" >"$curl_config"
auth=(--config "$curl_config")

if [ "$method" = "GET" ]; then
  # -G + --data-urlencode URL-encodes each value (so spaces etc. are safe).
  qs=()
  for kv in ${rest[@]+"${rest[@]}"}; do
    [ -n "$kv" ] || continue
    # curl treats both @file and name@file forms as local-file input for
    # --data-urlencode. Reject @ outright so query arguments cannot disclose
    # local files to the Crawlora API.
    case "$kv" in
      *@*) echo "@ is not allowed in query arguments" >&2; exit 2 ;;
    esac
    qs+=(--data-urlencode "$kv")
  done
  # -q must be the first curl option: ignore any user ~/.curlrc so inherited
  # config cannot redirect the request, add uploads, or alter credential use.
  curl -q -fsS -G "${auth[@]}" ${qs[@]+"${qs[@]}"} "${base}${path}"
else
  [ -n "$body" ] || body="${rest[0]:-}"
  [ -n "$body" ] || body='{}'
  # Stream the body on stdin so curl never interprets a user value as its
  # @file shorthand (and cannot read local files supplied in a request body).
  printf '%s' "$body" | curl -q -fsS -X "$method" "${auth[@]}" \
    -H "Content-Type: application/json" --data-binary @- "${base}${path}"
fi
