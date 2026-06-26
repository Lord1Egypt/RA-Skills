import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from loguru import logger
from datetime import datetime

# Import your actual production modules to ensure 1:1 parity
from features.microstructure import FeatureEngine
from models.agent import AI_Trader

class BacktestEngine:
    def __init__(self, data_path, model_path=None, initial_capital=10000):
        self.data_path = data_path
        self.capital = initial_capital
        self.balance = initial_capital
        self.position = 0  # Current position size in units (e.g., BTC)
        self.equity_curve = []
        self.trades = []
        
        # Configuration
        self.maker_fee = -0.0002  # Negative fee = rebate (if applicable) or 0.02%
        self.taker_fee = 0.0005   # 0.05%
        self.slippage = 0.5       # $0.50 assumed slippage per trade for BTC
        self.leverage = 10
        
        # Initialize Core Components
        self.feature_engine = FeatureEngine()
        self.agent = AI_Trader(model_path)
        
    def load_data(self):
        """
        Loads tick or 1-second OHLCV data. 
        Expected format: CSV with timestamp, bid, ask, last_price, volume
        """
        logger.info(f"Loading data from {self.data_path}...")
        # For demonstration, generating synthetic data if file doesn't exist
        # In production: self.df = pd.read_csv(self.data_path)
        self.df = self._generate_synthetic_data()
        logger.info(f"Loaded {len(self.df)} ticks.")

    def _generate_synthetic_data(self):
        # Generates a random walk for testing architecture
        dates = pd.date_range(start="2024-01-01", periods=10000, freq="S")
        prices = 40000 + np.cumsum(np.random.randn(10000) * 10)
        df = pd.DataFrame({
            'timestamp': dates,
            'last_price': prices,
            'bid': prices - 0.5,
            'ask': prices + 0.5,
            'bid_vol': np.random.rand(10000) * 10,
            'ask_vol': np.random.rand(10000) * 10
        })
        return df

    def run(self):
        logger.info("Starting Event-Driven Backtest...")
        
        for index, row in self.df.iterrows():
            # 1. Simulate Data Stream (Tick Ingestion)
            tick_payload = {
                'last_price': row['last_price'],
                'bid': row['bid'],
                'ask': row['ask'],
                'bid_vol': row['bid_vol'],
                'ask_vol': row['ask_vol']
            }
            
            # 2. Update Feature Engine (Stateful)
            self.feature_engine.update(tick_payload)
            
            # Warmup period for windows (e.g., 50 ticks)
            if index < 50:
                continue

            # 3. Get Features & Model Inference
            # Mocking orderbook snapshot structure expected by microstructure.py
            ob_snapshot = {
                'bid': row['bid'], 'ask': row['ask'],
                'bid_vol': row['bid_vol'], 'ask_vol': row['ask_vol']
            }
            features = self.feature_engine.get_features(ob_snapshot)
            
            # 4. Get Action from AI Agent
            action = self.agent.predict(features)
            
            # 5. Simulate Execution
            self._execute_logic(action, row)
            
            # Track Equity
            unrealized_pnl = 0
            if self.position != 0:
                # Mark to market
                unrealized_pnl = (row['last_price'] * self.position) - self.entry_cost
            
            current_equity = self.balance + unrealized_pnl
            self.equity_curve.append(current_equity)

            # Drawdown Check (Kill Switch Simulation)
            if (self.capital - current_equity) > (self.capital * 0.03):
                logger.warning("Max Drawdown Hit! Stopping Backtest.")
                break

        self._generate_report()

    def _execute_logic(self, signal, row):
        """
        Simulates order execution with fees and slippage.
        Signal > 0.5 -> BUY
        Signal < -0.5 -> SELL
        """
        price = row['last_price']
        
        # CLOSE EXISTING POSITIONS (Simplification: Flip position)
        if self.position > 0 and signal < -0.2:
            self._close_position(price, 'sell')
        elif self.position < 0 and signal > 0.2:
            self._close_position(price, 'buy')
            
        # OPEN NEW POSITIONS
        if self.position == 0:
            if signal > 0.5:
                self._open_position(price, 'buy', signal)
            elif signal < -0.5:
                self._open_position(price, 'sell', signal)

    def _open_position(self, price, side, signal_strength):
        # Kelly Criterion Sizing (simplified from execution.py)
        size_usd = 10000 * abs(signal_strength) * self.leverage
        quantity = size_usd / price
        
        cost = quantity * price
        
        # Apply Slippage & Fees
        execution_price = price + self.slippage if side == 'buy' else price - self.slippage
        fee = cost * self.taker_fee
        
        self.balance -= fee
        self.position = quantity if side == 'buy' else -quantity
        self.entry_price = execution_price
        self.entry_cost = self.position * self.entry_price # Signed cost
        
        self.trades.append({
            'type': 'entry', 'side': side, 'price': execution_price, 
            'size': quantity, 'fee': fee, 'time': str(datetime.now())
        })

    def _close_position(self, price, side):
        quantity = abs(self.position)
        cost = quantity * price
        
        # Apply Slippage & Fees
        execution_price = price - self.slippage if side == 'sell' else price + self.slippage
        fee = cost * self.taker_fee
        
        # PnL Calculation
        # If long, sell to close. PnL = (Exit - Entry) * Qty
        # If short, buy to close. PnL = (Entry - Exit) * Qty
        if self.position > 0: # Closing Long
            pnl = (execution_price - self.entry_price) * quantity
        else: # Closing Short
            pnl = (self.entry_price - execution_price) * quantity
            
        self.balance += pnl - fee
        self.position = 0
        self.entry_price = 0
        self.entry_cost = 0
        
        self.trades.append({
            'type': 'exit', 'side': side, 'price': execution_price, 
            'pnl': pnl, 'fee': fee
        })

    def _generate_report(self):
        equity_series = pd.Series(self.equity_curve)
        returns = equity_series.pct_change().dropna()
        
        total_return = (self.equity_curve[-1] - self.capital) / self.capital
        sharpe = returns.mean() / returns.std() * np.sqrt(365 * 24 * 60 * 60) # Annualized (approx)
        max_dd = (equity_series / equity_series.cummax() - 1).min()
        
        print("\n" + "="*40)
        print("📊 BACKTEST PERFORMANCE REPORT")
        print("="*40)
        print(f"Final Balance:   ${self.equity_curve[-1]:.2f}")
        print(f"Total Return:    {total_return*100:.2f}%")
        print(f"Sharpe Ratio:    {sharpe:.2f}")
        print(f"Max Drawdown:    {max_dd*100:.2f}%")
        print(f"Total Trades:    {len(self.trades)}")
        print("="*40 + "\n")
        
        # Simple Plot
        plt.figure(figsize=(10, 6))
        plt.plot(self.equity_curve)
        plt.title(f"NeuroScalp Strategy Equity Curve (Sharpe: {sharpe:.2f})")
        plt.ylabel("Account Equity ($)")
        plt.xlabel("Ticks")
        plt.grid(True, alpha=0.3)
        plt.savefig("backtest_results.png")
        logger.info("Chart saved to backtest_results.png")