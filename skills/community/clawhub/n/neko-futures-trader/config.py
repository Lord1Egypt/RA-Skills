# === Neko Futures Trader - CONFIGURATION ===
# Scanner v1.0.36 - Stable ATR-based SL/TP with PRICE fallback

# ── TRADING ──────────────────────────────────────────────────────────────────
LEVERAGE = 10                    # Futures leverage (10x)
MAX_POSITIONS = 7               # Max concurrent positions
AUTO_FILL_EMPTY_SLOTS = True     # Auto-find entries when positions < MAX
ENTRY_PERCENT = 6                # % of balance per trade

# ── SL/TP STRATEGY ────────────────────────────────────────────────────────────
# PRIMARY: ATR-based (adapts to token volatility)
# FALLBACK: Uses PRICE_TP/PRICE_SL when ATR is too tight or too wide

# ATR Multipliers (for fakeout protection - wider SL/TP)
ATR_HIGH_VOLATILITY = 3.0       # ATR > X% = high volatility token
ATR_MULTIPLIER_SL_HIGH = 3.0     # Wider SL for volatile tokens
ATR_MULTIPLIER_TP_HIGH = 6.0     # Wider TP for volatile tokens
ATR_MULTIPLIER_SL_NORMAL = 2.5    # Normal SL multiplier
ATR_MULTIPLIER_TP_NORMAL = 5.0   # Normal TP multiplier
ATR_MULTIPLIER_SL_LOW = 2.0      # Tighter SL for stable tokens
ATR_MULTIPLIER_TP_LOW = 4.0      # Tighter TP for stable tokens

# PRICE FALLBACK (when ATR-based SL would be too tight/wide)
PRICE_TP = 10.0                  # Take Profit: +10% for LONG, -10% for SHORT
PRICE_SL = 5.0                   # Stop Loss: -5% for LONG, +5% for SHORT
PRICE_FALLBACK_MAX_ATR = 10.0    # If ATR% > 10%, use PRICE_TP/PRICE_SL instead
PRICE_FALLBACK_MIN_ATR = 1.0     # If ATR% < 1%, use PRICE_TP/PRICE_SL instead

# ── BREAKEVEN & TRAILING ─────────────────────────────────────────────────────
MIN_PROFIT_BREAKEVEN = 5.0       # % profit to move SL to entry price
MIN_PROFIT_TRAILING_TP = 10.0    # % profit to activate trailing TP
TRAIL_PERCENT = 2.0              # Trail SL by this % when trailing

# ── NOTIFICATIONS ─────────────────────────────────────────────────────────────
POST_SIGNALS_TO_TELEGRAM = True
NOTIFY_ON_OPEN = True
NOTIFY_ON_CLOSE = True
NOTIFY_ON_BREAKEVEN = True
NOTIFY_ON_TRAILING_TP = True

# ── SCANNER ──────────────────────────────────────────────────────────────────
SCAN_INTERVAL = 300             # Scanner run every 5 minutes
MIN_PRICE_CHANGE = 3.0          # Min % price change for signal
MIN_SCORE = 3                    # Min signal score (1-10)
SKIP_RECENT_HOURS = 24           # Skip re-entry for 24h after close

# ── RISK ─────────────────────────────────────────────────────────────────────
MAX_MARGIN_PERCENT = 40          # Max margin usage %
MAX_RISK_PERCENT = 1.5           # Max risk per trade %

# ── SAFE COINS ───────────────────────────────────────────────────────────────
SAFE_COINS = [
    'BNBUSDT','ETHUSDT','BTCUSDT','XRPUSDT','ADAUSDT','DOGEUSDT',
    'SOLUSDT','DOTUSDT','MATICUSDT','LTCUSDT','AVAXUSDT','LINKUSDT',
    'ATOMUSDT','UNIUSDT','ETCUSDT','XLMUSDT','BCHUSDT','FILUSDT',
    'APTUSDT','NEARUSDT','ARBUSDT','OPUSDT','AAVEUSDT','MKRUSDT',
    'GRTUSDT','SNXUSDT','IMXUSDT','ALGOUSDT','FTMUSDT','SANDUSDT',
    'MANAUSDT','AXSUSDT','CHZUSDT','ENJUSDT','NEOUSDT','ZECUSDT',
    'EOSUSDT','THETAUSDT','KAVAUSDT','WAVESUSDT','ZILUSDT','KSMUSDT',
    'RUNEUSDT','KLAYUSDT','MINAUSDT','QNTUSDT','LDOUSDT','SUIUSDT',
    'SEIUSDT','TIAUSDT','INJUSDT','TIAUSD_PERP','WIFUSDT','ORDIUSDT'
]
