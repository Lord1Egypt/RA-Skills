import sys
import os

# Add root directory to python path to find 'core'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine.backtest import BacktestEngine

if __name__ == "__main__":
    # You would point this to a real CSV in production
    # e.g., data_path="./data/BTC-USDT-SWAP-2023.csv"
    
    bt = BacktestEngine(
        data_path="synthetic", 
        initial_capital=10000
    )
    
    bt.load_data()
    bt.run()