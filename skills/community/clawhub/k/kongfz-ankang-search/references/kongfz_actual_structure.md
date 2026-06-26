# Kongfz site structure update (2026-05-01)

## Actual URL structure discovered

1. **Main site**: `https://www.kongfz.com/` ✅ works
2. **Auction (竞拍)**: `https://www.kongfz.cn/` ✅ redirects to auction
   - My bids: `https://www.kongfz.cn/pm-buyer/bid-manage-pc/`
   - Favorites: `https://www.kongfz.cn/pm-buyer/bid-manage-pc/favorite/`
   - Trade history: `https://www.kongfz.cn/trade-views/management/buyer/list`
3. **Auction platform**: `https://www.kongpm.com/` ✅ separate auction site
   - e.g. `https://www.kongpm.com/yplm/web/` (艺拍联盟)
4. **Search**: `https://search.kongfz.com/`
   - Category: `https://search.kongfz.com/product/category?catId=xxx`
   - Latest: `https://search.kongfz.com/product/latest?sortType=3`
5. **Item pages**: `https://item.kongfz.com/book/{id}.html`

## ❌ Dead URLs from original SKILL.md
- `https://www.kongfz.com/auction/` → 404 Not Found
- `https://www.kongfz.com/auction/?keyword=...` → 404

## Search keyword format
- URL: `https://search.kongfz.com/product/search?q=安康文字&catId=...`
- The search works through the search.kongfz.com domain

## Action items
1. Update `references/kongfz_structure.md` with correct URLs
2. Update `scripts/kongfz_search.py` to use `search.kongfz.com` or `item.kongfz.com` API
3. The auction section now lives at `kongfz.cn` domain