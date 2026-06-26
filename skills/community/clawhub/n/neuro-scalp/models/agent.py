import torch
import torch.nn as nn
import numpy as np

class ScalpingActorCritic(nn.Module):
    def __init__(self, input_dim, action_dim):
        super(ScalpingActorCritic, self).__init__()
        # Actor Network (Policy)
        self.actor = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim),
            nn.Tanh()  # Output: -1 (Sell) to 1 (Buy)
        )
        # Critic Network (Value)
        self.critic = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        return self.actor(x), self.critic(x)

class AI_Trader:
    def __init__(self, model_path=None):
        self.model = ScalpingActorCritic(input_dim=3, action_dim=1)
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-4)
    
    def predict(self, features):
        """
        Returns action: 
        > 0.5: Buy Aggressively
        > 0.2: Buy Passive
        < -0.5: Sell Aggressively
        ...
        """
        state = torch.FloatTensor(features).unsqueeze(0)
        with torch.no_grad():
            action, _ = self.model(state)
        return action.item()

    def online_learn(self, replay_buffer):
        """
        Called periodically to update weights based on recent trade outcomes
        """
        # (Implementation of PPO update loop would go here)
        pass