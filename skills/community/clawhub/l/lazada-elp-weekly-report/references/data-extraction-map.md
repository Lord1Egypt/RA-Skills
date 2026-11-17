## Data Extraction Quick Reference

### Performance Summary Cell Map

```
Row 4:  platform_item_sell_rate (大盘动销率) | C4: WoW (pt)
Row 7:  joined_item (招商商品数)              | C7: WoW (%)
Row 8:  sold_item (大盘动销商品数)             | C8: WoW (%)
Row 14: lazflash_item_sell_rate (频道动销率)   | C14: WoW (pt)
Row 17: guided_sold_item (频道动销商品数)      | C17: WoW (%)
Row 23: ord (日均平台订单数)                   | C23: WoW (%)
Row 24: gmv (日均平台GMV)                      | C24: WoW (%)
Row 26: venture_ord (D-J: 7天明细)             → SUM for OrderC denominator
Row 27: venture_gmv (D-J: 7天明细)             → SUM for GMVC denominator
Row 32: guided_ord (频道引导订单数)            | C32: WoW (%)
Row 33: guided_gmv (频道引导GMV)               | C33: WoW (%)
Row 37: venture_guided_ord (D-J: 7天明细)      → SUM for order share denominator
Row 38: venture_guided_gmv (D-J: 7天明细)      → SUM for GMV share denominator
```

### Calculated Metrics

```
OrderC       = B23 / SUM(D26:J26)
GMVC         = B24 / SUM(D27:J27)
Order Share  = B32 / SUM(D37:J37)
GMV Share    = B33 / SUM(D38:J38)
```

### Traffic Performance (single sheet)

```
Row 1: Headers
Row 2: ID    Row 3: MY    Row 4: PH
Row 5: SG    Row 6: TH    Row 7: VN

Col B: DAU          Col C: DAU WoW
Col E: DAU share    Col F: UVCR
Col G: UVCR WoW     Col I: UVCR vs channel
```
