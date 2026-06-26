import pandas as pd
import numpy as np
import torch
from loguru import logger
from datetime import timedelta
from core.engine.backtest import BacktestEngine
from models.agent import AI_Trader

class WalkForwardOptimizer:
    def __init__(self, data_path, window_size_days=30, step_size_days=7):
        self.data_path = data_path
        self.window_size = timedelta(days=window_size_days) # Train duration
        self.step_size = timedelta(days=step_size_days)     # Test duration
        self.results = []

    def load_data(self):
        # In production: Load real CSV
        # self.df = pd.read_csv(self.data_path, parse_dates=['timestamp'])
        
        # Generating synthetic data for architecture test
        dates = pd.date_range(start="2024-01-01", end="2024-04-01", freq="1min")
        prices = 40000 + np.cumsum(np.random.randn(len(dates)) * 5)
        self.df = pd.DataFrame({
            'timestamp': dates,
            'last_price': prices,
            'bid': prices - 0.5, 'ask': prices + 0.5,
            'bid_vol': np.random.rand(len(dates)) * 10,
            'ask_vol': np.random.rand(len(dates)) * 10
        })
        logger.info(f"Loaded {len(self.df)} rows for Walk-Forward Analysis.")

    def run(self):
        start_date = self.df['timestamp'].min()
        end_date = self.df['timestamp'].max()
        
        current_train_start = start_date
        
        while True:
            train_end = current_train_start + self.window_size
            test_end = train_end + self.step_size
            
            if test_end > end_date:
                break
                
            logger.info(f"🔄 WFO Fold: Train[{current_train_start.date()} : {train_end.date()}] -> Test[{train_end.date()} : {test_end.date()}]")
            
            # 1. Slice Data
            train_data = self.df[(self.df['timestamp'] >= current_train_start) & (self.df['timestamp'] < train_end)]
            test_data = self.df[(self.df['timestamp'] >= train_end) & (self.df['timestamp'] < test_end)]
            
            # 2. Train Model (Simplified Simulation)
            # In production: You would call agent.train(train_data) here
            model_path = f"models/checkpoints/model_{train_end.date()}.pth"
            self._simulate_training(train_data, model_path)
            
            # 3. Run Backtest on OOS (Out-of-Sample) Data
            # We temporarily save test data to csv for the backtester to pick up
            test_data_path = f"temp_test_data_{train_end.date()}.csv"
            test_data.to_csv(test_data_path, index=False)
            
            bt = BacktestEngine(data_path=test_data_path, model_path=model_path)
            # Inject the dataframe directly to avoid file I/O overhead in this demo
            bt.df = test_data 
            bt.run()
            
            # 4. Collect Metrics
            final_equity = bt.equity_curve[-1] if bt.equity_curve else 10000
            returns = (final_equity - 10000) / 10000
            self.results.append({
                'test_period': f"{train_end.date()} to {test_end.date()}",
                'return': returns,
                'trades': len(bt.trades)
            })
            
            # Slide Window
            current_train_start += self.step_size

        self._print_summary()

    def _simulate_training(self, data, save_path):
        """
        Simulates the PPO training process.
        In reality, this would run the RL training loop for N epochs.
        """
        agent = AI_Trader()
        # Mock saving weights
        torch.save(agent.model.state_dict(), save_path)

    def _print_summary(self):
        print("\n" + "="*50)
        print("📈 WALK-FORWARD OPTIMIZATION RESULTS")
        print("="*50)
        df_res = pd.DataFrame(self.results)
        print(df_res)
        print("-" * 50)
        print(f"Average Return per Period: {df_res['return'].mean()*100:.2f}%")
        print(f"Positive Periods: {len(df_res[df_res['return'] > 0])} / {len(df_res)}")