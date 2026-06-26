## Open Food Facts API vs This Skill

| Feature | Open Food Facts API | This Skill | Notes |
|---------|---------------------|------------|-------|
| **Search by name/keywords** | ✅ `GET /api/v2/search` | ✅ `off_search.sh` | Basic keyword search implemented |
| **Get product by barcode** | ✅ `GET /api/v2/product/{barcode}` | ✅ `off_product.sh` | Full product details with nutrition |
| **Get product images** | ✅ `https://images.openfoodfacts.org/images/products/{barcode}/` | ❌ Not implemented | Images available via direct URL pattern |
| **Upload product data** | ✅ `POST /api/v2/product` | ❌ Not implemented | Requires authentication |
| **Add/edit product photos** | ✅ `POST /cgi/product_image_upload.pl` | ❌ Not implemented | Requires authentication |
| **Advanced search filters** | ✅ Categories, labels, origins, etc. | ❌ Not implemented | Can add filters like `&categories_tags=en:chocolates` |
| **Search by brand** | ✅ `&brands_tags=` | ⚠️ Partial | Can search within results, not dedicated filter |
| **Nutrition grades filter** | ✅ `&nutrition_grades=` | ❌ Not implemented | Filter by Nutri-Score (a, b, c, d, e) |
| **NOVA group filter** | ✅ `&nova_groups=` | ❌ Not implemented | Filter by processing level (1-4) |
| **User authentication** | ✅ `user_id` + `password` | ❌ Not implemented | Required for write operations |
| **Product history/changes** | ✅ `GET /api/v2/product/{barcode}?fields=history` | ❌ Not implemented | Track product modifications |
| **Facets/categories list** | ✅ `GET /api/v2/categories` | ❌ Not implemented | Browse all categories |
| **Additives info** | ✅ Included in product data | ✅ Partial | Displayed if present in API response |
| **Eco-Score** | ✅ Included for some products | ✅ Displayed if available | Environmental impact score |
| **Ingredient analysis** | ✅ `ingredients_analysis_tags` | ✅ Partial | Allergens and additives shown |

## What's Implemented

### ✅ `off_search.sh` - Search Products
- Search by keyword/name
- Configurable page size
- Returns: product name, barcode, brand

### ✅ `off_product.sh` - Product Lookup
- Lookup by barcode (EAN/UPC)
- Full nutritional information per 100g
- Ingredients and allergens
- Nutri-Score and NOVA group
- Product link for more details

## What's Not Implemented (Future Enhancements)

1. **Image Display**: Could add image URLs to output
   - Format: `https://images.openfoodfacts.org/images/products/{path}/front.{size}.jpg`
   
2. **Advanced Search Filters**:
   - By category (e.g., only "chocolates")
   - By label (e.g., "organic", "vegan")
   - By Nutri-Score
   - By country

3. **Write Operations** (requires auth):
   - Add new products
   - Edit existing products
   - Upload photos

4. **Additional Fields**:
   - Product history/changes
   - Packaging info
   - Manufacturing places
   - Stores where sold

5. **Facets Browsing**:
   - List all categories
   - List all brands
   - List all labels
