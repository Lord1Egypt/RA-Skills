import sys
import os
# Ensure we can import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine.walk_forward import WalkForwardOptimizer

if __name__ == "__main__":
    # Create directory for model checkpoints
    os.makedirs("models/checkpoints", exist_ok=True)
    
    # Train on 30 days, Test on 7 days, then slide forward
    wfo = WalkForwardOptimizer(data_path="synthetic", window_size_days=30, step_size_days=7)
    wfo.load_data()
    wfo.run()