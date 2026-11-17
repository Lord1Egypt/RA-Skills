from dataclasses import dataclass, field
from .money import D, ZERO
SIDES = ("Up", "Down")
TERMINAL = {"CANCELLED", "REJECTED", "FILLED"}

@dataclass
class Order:
    id: str
    market: str
    side: str
    qty: D
    price: D
    kind: str
    sent_ms: int
    status: str = 'SENT'
    final_total: D | None = None
    cancel_ms: int | None = None

@dataclass
class Fill:
    id: str
    order: str
    qty: D
    price: D
    fee: D
    status: str = 'MATCHED'

@dataclass
class Window:
    id: str
    start: int
    side: str | None
    k: float
    provisional: bool
    tick: D
    min_qty: D
    ptb: float
    qty: dict = field(default_factory=lambda: dict.fromkeys(SIDES, ZERO))
    cost: dict = field(default_factory=lambda: dict.fromkeys(SIDES, ZERO))
    books: dict = field(default_factory=dict)
    spot: float | None = None
    sigma: float | None = None
    price_ms: int = -1
    health_ms: int = -1
    clock_ms: float = 999
    blocked: str | None = None
    fair: float | None = None
    quote_count: int = 0
    last_quote_ms: int = -100000
    hedge_attempted: bool = False
    chain: tuple | None = None
    merge_failed: bool = False
    winner: str | None = None
    closed: bool = False
    realized: D = ZERO
    maintenance: bool = False