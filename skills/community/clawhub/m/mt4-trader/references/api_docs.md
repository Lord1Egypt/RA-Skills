# MT4 Bridge API Reference

## Symbols: XAUUSD.s (Gold), BTCUSD, XAGUSD, XTIUSD.s

## Methods

### Trading
buy(symbol, lots), sell(symbol, lots), close_all(symbol), close_by_magic(symbol, magic)

### Pending Orders
buy_limit(symbol, lots, price), sell_limit(symbol, lots, price), buy_stop(symbol, lots, price), sell_stop(symbol, lots, price), cancel_order(ticket)

### SL/TP
set_sl(symbol, ticket, price), set_tp(symbol, ticket, price), modify_order(symbol, ticket, price, sl, tp)

### Grid (Sesame EA)
grid_start(symbol, direction), grid_stop(symbol), grid_close_all(symbol), grid_status(symbol), grid_set_sl_tp(symbol)

### Chart Objects (v1.86)
draw_sr_levels(symbol, timeframe), clear_chart_objects(symbol), draw_hline(symbol, name, price), clear_hline(symbol, prefix)

### Data
add_alert(symbol, price, tip), get_klines(symbol, timeframe, count), get_positions(symbol), get_notifications(symbol)
