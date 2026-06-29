"""
Investment Decision System - Database Layer
SQLite database with tables for profile, holdings, trades, decisions, watchlist, risk_rules.
"""

import sqlite3
import os
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "investment.db")


def get_db_path():
    """Return the database path, creating the directory if needed."""
    os.makedirs(DB_DIR, exist_ok=True)
    return DB_PATH


def get_connection():
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize all database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        -- 投资画像
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            risk_tolerance TEXT NOT NULL DEFAULT 'moderate',
            investment_goal TEXT DEFAULT 'growth',
            time_horizon TEXT DEFAULT 'medium',
            total_capital REAL DEFAULT 0,
            monthly_contribution REAL DEFAULT 0,
            max_single_position_pct REAL DEFAULT 20.0,
            max_industry_pct REAL DEFAULT 40.0,
            hard_stop_loss_pct REAL DEFAULT 8.0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 持仓
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            name TEXT,
            asset_class TEXT NOT NULL DEFAULT 'stock',
            market TEXT DEFAULT 'A-share',
            quantity REAL NOT NULL DEFAULT 0,
            avg_cost REAL NOT NULL DEFAULT 0,
            current_price REAL,
            currency TEXT DEFAULT 'CNY',
            sector TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 交易记录
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            trade_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            amount REAL NOT NULL,
            fee REAL DEFAULT 0,
            decision_id INTEGER,
            trade_date DATE,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (decision_id) REFERENCES decisions(id)
        );

        -- 决策记录 (INVEST 框架)
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            name TEXT,
            decision_type TEXT NOT NULL DEFAULT 'buy',
            intent_score INTEGER DEFAULT 0,
            numbers_score INTEGER DEFAULT 0,
            value_score INTEGER DEFAULT 0,
            edge_score INTEGER DEFAULT 0,
            safety_score INTEGER DEFAULT 0,
            timing_score INTEGER DEFAULT 0,
            total_score REAL DEFAULT 0,
            position_size_pct REAL,
            stop_loss_pct REAL,
            take_profit_pct REAL,
            thesis TEXT,
            risks TEXT,
            status TEXT DEFAULT 'pending',
            decision_date DATE DEFAULT (date('now')),
            executed_at TIMESTAMP,
            reviewed_at TIMESTAMP,
            outcome TEXT,
            outcome_pnl REAL,
            outcome_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 关注列表
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            name TEXT,
            asset_class TEXT DEFAULT 'stock',
            market TEXT DEFAULT 'A-share',
            reason TEXT,
            target_price REAL,
            status TEXT DEFAULT 'watching',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 风控规则
        CREATE TABLE IF NOT EXISTS risk_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT NOT NULL,
            rule_type TEXT NOT NULL,
            rule_value TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 决策日志
        CREATE TABLE IF NOT EXISTS decision_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_id INTEGER,
            action TEXT NOT NULL,
            old_status TEXT,
            new_status TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (decision_id) REFERENCES decisions(id)
        );
    """)

    # Insert default risk rules if none exist
    cursor.execute("SELECT COUNT(*) FROM risk_rules")
    if cursor.fetchone()[0] == 0:
        default_rules = [
            ('单票最大仓位', 'position', '20', 1, '单只股票最大仓位不超过总资产的20%'),
            ('行业最大仓位', 'diversification', '40', 1, '单一行业最大仓位不超过总资产的40%'),
            ('硬止损比例', 'stop_loss', '8', 1, '单笔交易最大亏损不超过买入成本的8%'),
            ('现金保留比例', 'position', '10', 1, '始终保持至少10%现金仓位'),
            ('单月最大交易次数', 'discipline', '10', 1, '每月交易次数不超过10次，避免过度交易'),
            ('最少持有天数', 'discipline', '5', 1, '买入后至少持有5个交易日'),
        ]
        cursor.executemany(
            "INSERT INTO risk_rules (rule_name, rule_type, rule_value, is_active, description) VALUES (?, ?, ?, ?, ?)",
            default_rules
        )

    conn.commit()
    conn.close()


# ---- Profile Operations ----

def get_profile():
    """Get the investor profile. Creates default if none exists."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM profile ORDER BY id DESC LIMIT 1").fetchone()
    if not row:
        conn.execute("INSERT INTO profile DEFAULT VALUES")
        conn.commit()
        row = conn.execute("SELECT * FROM profile ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    return dict(row) if row else None


def update_profile(**kwargs):
    """Update investor profile fields."""
    conn = get_connection()
    profile = get_profile()
    if not profile:
        conn.close()
        return None
    allowed = ['risk_tolerance', 'investment_goal', 'time_horizon', 'total_capital',
               'monthly_contribution', 'max_single_position_pct', 'max_industry_pct',
               'hard_stop_loss_pct', 'notes']
    updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
    updates['updated_at'] = datetime.now().isoformat()
    if updates:
        set_clause = ', '.join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [profile['id']]
        conn.execute(f"UPDATE profile SET {set_clause} WHERE id = ?", values)
        conn.commit()
    conn.close()
    return get_profile()


# ---- Holdings Operations ----

def add_holding(symbol, name, asset_class='stock', market='A-share', quantity=0,
                avg_cost=0, current_price=None, currency='CNY', sector=None, notes=None):
    """Add a new holding."""
    conn = get_connection()
    conn.execute("""
        INSERT INTO holdings (symbol, name, asset_class, market, quantity, avg_cost,
                              current_price, currency, sector, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (symbol, name, asset_class, market, quantity, avg_cost, current_price, currency, sector, notes))
    conn.commit()
    hid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return hid


def update_holding(holding_id, **kwargs):
    """Update holding fields."""
    conn = get_connection()
    allowed = ['symbol', 'name', 'asset_class', 'market', 'quantity', 'avg_cost',
               'current_price', 'currency', 'sector', 'notes']
    updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
    updates['updated_at'] = datetime.now().isoformat()
    if updates:
        set_clause = ', '.join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [holding_id]
        conn.execute(f"UPDATE holdings SET {set_clause} WHERE id = ?", values)
        conn.commit()
    conn.close()


def delete_holding(holding_id):
    """Delete a holding."""
    conn = get_connection()
    conn.execute("DELETE FROM holdings WHERE id = ?", (holding_id,))
    conn.commit()
    conn.close()


def get_all_holdings():
    """Get all current holdings."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM holdings ORDER BY asset_class, symbol").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_portfolio_summary():
    """Get portfolio summary with asset allocation and P&L."""
    holdings = get_all_holdings()
    profile = get_profile()

    total_cost = 0
    total_market_value = 0
    asset_allocation = {}
    sector_allocation = {}

    for h in holdings:
        cost = h['quantity'] * h['avg_cost']
        mv = h['quantity'] * (h['current_price'] or h['avg_cost'])
        total_cost += cost
        total_market_value += mv

        ac = h['asset_class']
        asset_allocation[ac] = asset_allocation.get(ac, 0) + mv

        if h.get('sector'):
            sector_allocation[h['sector']] = sector_allocation.get(h['sector'], 0) + mv

    # Calculate percentages
    total = total_market_value if total_market_value > 0 else 1
    for k in asset_allocation:
        asset_allocation[k] = round(asset_allocation[k] / total * 100, 1)
    for k in sector_allocation:
        sector_allocation[k] = round(sector_allocation[k] / total * 100, 1)

    return {
        'total_cost': round(total_cost, 2),
        'total_market_value': round(total_market_value, 2),
        'total_pnl': round(total_market_value - total_cost, 2),
        'total_pnl_pct': round((total_market_value - total_cost) / total_cost * 100, 2) if total_cost > 0 else 0,
        'holding_count': len(holdings),
        'asset_allocation': asset_allocation,
        'sector_allocation': sector_allocation,
        'holdings': holdings,
        'total_capital': profile.get('total_capital', 0) if profile else 0,
        'cash_estimate': round((profile.get('total_capital', 0) or total_cost) - total_cost, 2) if profile else 0,
    }


# ---- Trade Operations ----

def record_trade(symbol, trade_type, quantity, price, fee=0, decision_id=None,
                 trade_date=None, notes=None):
    """Record a buy or sell trade."""
    amount = quantity * price
    conn = get_connection()
    conn.execute("""
        INSERT INTO trades (symbol, trade_type, quantity, price, amount, fee,
                           decision_id, trade_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (symbol, trade_type, quantity, price, amount, fee, decision_id,
          trade_date or datetime.now().date().isoformat(), notes))
    conn.commit()
    tid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # Update holding
    holding = conn.execute("SELECT * FROM holdings WHERE symbol = ?", (symbol,)).fetchone()
    if trade_type == 'buy':
        if holding:
            new_qty = holding['quantity'] + quantity
            new_cost = (holding['avg_cost'] * holding['quantity'] + amount + fee) / new_qty
            conn.execute("UPDATE holdings SET quantity = ?, avg_cost = ?, updated_at = ? WHERE id = ?",
                         (new_qty, round(new_cost, 4), datetime.now().isoformat(), holding['id']))
        else:
            conn.execute("""
                INSERT INTO holdings (symbol, name, quantity, avg_cost, current_price)
                VALUES (?, ?, ?, ?, ?)
            """, (symbol, symbol, quantity, round((amount + fee) / quantity, 4), price))
    elif trade_type == 'sell':
        if holding and holding['quantity'] >= quantity:
            new_qty = holding['quantity'] - quantity
            if new_qty <= 0.001:
                conn.execute("DELETE FROM holdings WHERE id = ?", (holding['id'],))
            else:
                conn.execute("UPDATE holdings SET quantity = ?, updated_at = ? WHERE id = ?",
                             (new_qty, datetime.now().isoformat(), holding['id']))

    conn.commit()
    conn.close()
    return tid


def get_trade_history(limit=50):
    """Get trade history."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM trades ORDER BY trade_date DESC, created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---- Decision Operations ----

def create_decision(symbol, name=None, decision_type='buy', **kwargs):
    """Create a new INVEST decision record."""
    conn = get_connection()
    fields = ['symbol', 'name', 'decision_type', 'intent_score', 'numbers_score',
              'value_score', 'edge_score', 'safety_score', 'timing_score',
              'position_size_pct', 'stop_loss_pct', 'take_profit_pct',
              'thesis', 'risks', 'status']
    values = {
        'symbol': symbol,
        'name': name or symbol,
        'decision_type': decision_type,
        'status': 'pending'
    }
    values.update({k: v for k, v in kwargs.items() if k in fields and v is not None})

    # Calculate total score (weighted)
    weights = {'intent': 0.15, 'numbers': 0.20, 'value': 0.20,
               'edge': 0.10, 'safety': 0.20, 'timing': 0.15}
    total = 0
    for key, weight in weights.items():
        score = values.get(f'{key}_score', 0) or 0
        total += score * weight
    values['total_score'] = round(total, 1)

    columns = ', '.join(values.keys())
    placeholders = ', '.join('?' for _ in values)
    conn.execute(f"INSERT INTO decisions ({columns}) VALUES ({placeholders})", list(values.values()))
    conn.commit()
    did = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # Log creation
    conn.execute("INSERT INTO decision_log (decision_id, action, new_status) VALUES (?, 'created', 'pending')", (did,))
    conn.commit()
    conn.close()
    return did


def update_decision(decision_id, **kwargs):
    """Update a decision."""
    conn = get_connection()
    current = conn.execute("SELECT * FROM decisions WHERE id = ?", (decision_id,)).fetchone()
    if not current:
        conn.close()
        return None

    allowed = ['intent_score', 'numbers_score', 'value_score', 'edge_score',
               'safety_score', 'timing_score', 'position_size_pct', 'stop_loss_pct',
               'take_profit_pct', 'thesis', 'risks', 'status', 'outcome',
               'outcome_pnl', 'outcome_notes', 'name', 'decision_type']
    updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}

    # Recalculate total score if any score changed
    score_fields = ['intent_score', 'numbers_score', 'value_score',
                    'edge_score', 'safety_score', 'timing_score']
    if any(k in updates for k in score_fields):
        weights = {'intent_score': 0.15, 'numbers_score': 0.20, 'value_score': 0.20,
                   'edge_score': 0.10, 'safety_score': 0.20, 'timing_score': 0.15}
        total = 0
        for key, weight in weights.items():
            score = updates.get(key, current[key]) or 0
            total += score * weight
        updates['total_score'] = round(total, 1)

    if 'status' in updates and updates['status'] == 'executed':
        updates['executed_at'] = datetime.now().isoformat()
    if 'outcome' in updates and updates['outcome'] in ('win', 'loss'):
        updates['reviewed_at'] = datetime.now().isoformat()

    if updates:
        set_clause = ', '.join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [decision_id]
        conn.execute(f"UPDATE decisions SET {set_clause} WHERE id = ?", values)
        conn.commit()

    conn.close()


def get_decision(decision_id):
    """Get a single decision with full details."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM decisions WHERE id = ?", (decision_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_decisions(status=None, limit=50):
    """Get all decisions, optionally filtered by status."""
    conn = get_connection()
    if status:
        rows = conn.execute(
            "SELECT * FROM decisions WHERE status = ? ORDER BY created_at DESC LIMIT ?",
            (status, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM decisions ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_decision_stats():
    """Get decision performance statistics."""
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM decisions WHERE outcome IS NOT NULL").fetchone()[0]
    wins = conn.execute("SELECT COUNT(*) FROM decisions WHERE outcome = 'win'").fetchone()[0]
    losses = conn.execute("SELECT COUNT(*) FROM decisions WHERE outcome = 'loss'").fetchone()[0]
    avg_score_win = conn.execute(
        "SELECT AVG(total_score) FROM decisions WHERE outcome = 'win'"
    ).fetchone()[0]
    avg_score_loss = conn.execute(
        "SELECT AVG(total_score) FROM decisions WHERE outcome = 'loss'"
    ).fetchone()[0]
    total_pnl = conn.execute(
        "SELECT COALESCE(SUM(outcome_pnl), 0) FROM decisions WHERE outcome_pnl IS NOT NULL"
    ).fetchone()[0]
    avg_pnl_win = conn.execute(
        "SELECT AVG(outcome_pnl) FROM decisions WHERE outcome = 'win' AND outcome_pnl IS NOT NULL"
    ).fetchone()[0]
    avg_pnl_loss = conn.execute(
        "SELECT AVG(outcome_pnl) FROM decisions WHERE outcome = 'loss' AND outcome_pnl IS NOT NULL"
    ).fetchone()[0]
    conn.close()

    return {
        'total_decisions': total,
        'wins': wins,
        'losses': losses,
        'win_rate': round(wins / total * 100, 1) if total > 0 else 0,
        'avg_score_win': round(avg_score_win, 1) if avg_score_win else 0,
        'avg_score_loss': round(avg_score_loss, 1) if avg_score_loss else 0,
        'total_pnl': round(total_pnl or 0, 2),
        'avg_pnl_win': round(avg_pnl_win or 0, 2),
        'avg_pnl_loss': round(avg_pnl_loss or 0, 2),
        'profit_factor': round(abs((avg_pnl_win or 0) / (avg_pnl_loss or 1)), 2) if avg_pnl_loss and avg_pnl_loss != 0 else 0,
    }


# ---- Watchlist Operations ----

def add_to_watchlist(symbol, name=None, asset_class='stock', market='A-share',
                     reason=None, target_price=None):
    """Add a symbol to the watchlist."""
    conn = get_connection()
    conn.execute("""
        INSERT INTO watchlist (symbol, name, asset_class, market, reason, target_price)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (symbol, name or symbol, asset_class, market, reason, target_price))
    conn.commit()
    wid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return wid


def get_watchlist():
    """Get all watchlist items."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM watchlist WHERE status = 'watching' ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def remove_from_watchlist(watch_id):
    """Mark a watchlist item as removed."""
    conn = get_connection()
    conn.execute("UPDATE watchlist SET status = 'removed' WHERE id = ?", (watch_id,))
    conn.commit()
    conn.close()


# ---- Risk Rules ----

def get_risk_rules(active_only=True):
    """Get risk rules."""
    conn = get_connection()
    if active_only:
        rows = conn.execute("SELECT * FROM risk_rules WHERE is_active = 1 ORDER BY rule_type").fetchall()
    else:
        rows = conn.execute("SELECT * FROM risk_rules ORDER BY rule_type").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def check_risk_compliance(decision_id=None):
    """Check portfolio against risk rules. Returns violations."""
    summary = get_portfolio_summary()
    rules = get_risk_rules()
    violations = []

    for rule in rules:
        try:
            value = float(rule['rule_value'])
        except (ValueError, TypeError):
            continue

        rtype = rule['rule_type']
        rname = rule['rule_name']

        if rtype == 'position' and '单票' in rname:
            total = summary['total_market_value'] or summary['total_cost']
            for h in summary['holdings']:
                mv = h['quantity'] * (h['current_price'] or h['avg_cost'])
                pct = mv / total * 100 if total > 0 else 0
                if pct > value:
                    violations.append({
                        'rule': rname,
                        'detail': f"{h['symbol']} 仓位 {pct:.1f}% 超过限制 {value}%",
                        'severity': 'high' if pct > value * 1.5 else 'medium'
                    })

        elif rtype == 'diversification' and '行业' in rname:
            for sector, pct in summary['sector_allocation'].items():
                if pct > value:
                    violations.append({
                        'rule': rname,
                        'detail': f"{sector} 行业仓位 {pct}% 超过限制 {value}%",
                        'severity': 'high' if pct > value * 1.2 else 'medium'
                    })

        elif rtype == 'position' and '现金' in rname:
            cash_pct = 0
            total = summary['total_capital'] or summary['total_market_value']
            if total > 0:
                cash_pct = (1 - summary['total_market_value'] / total) * 100
            if cash_pct < value:
                violations.append({
                    'rule': rname,
                    'detail': f"现金比例 {cash_pct:.1f}% 低于最低要求 {value}%",
                    'severity': 'medium'
                })

    return violations


# ---- Initialize on import ----
if __name__ == '__main__':
    init_db()
    print(f"Database initialized at: {DB_PATH}")
else:
    # Ensure DB exists when imported
    os.makedirs(DB_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        init_db()
