# ncps API Cheatsheet

The `ncps` (Neural Circuit Policies) library provides two PyTorch RNN layers —
`LTC` and `CfC` — plus structured wiring classes. Author: Mathias Lechner,
Apache 2.0. Docs: https://ncps.readthedocs.io/en/latest/

## Installation

```bash
pip install ncps torch numpy pandas
```

## Models

```python
from ncps.torch import CfC, LTC

# Fully connected wiring (like LSTM/GRU)
rnn = CfC(20, 50)       # (input_size, units)
rnn = LTC(20, 50)

# Sparse structured wiring
from ncps.wirings import AutoNCP

wiring = AutoNCP(28, 4)  # 28 neurons total, 4 motor neurons (= output size)
rnn = CfC(20, wiring)
```

## Forward pass

```python
import torch

x = torch.randn(2, 3, 20)     # (batch, time_steps, features)
h0 = torch.zeros(2, 50)       # (batch, state_size)
output, hn = rnn(x, h0)       # output: (batch, time, units) if return_sequences=True
```

- `output[:, -1, :]` is the prediction for the **next** time step.
- `state_size` = `units` for fully connected, or the total neuron count for a
  wiring (e.g. 28 for `AutoNCP(28, 4)`).
- With a wiring, the RNN output dimension equals the wiring's output size.

## Wirings

| Class | Constructor | Purpose |
|---|---|---|
| `FullyConnected(units)` | full connectivity | standard RNN wiring |
| `Random(units, output_dim, sparsity_level=0.0)` | random sparse | simple sparse baseline |
| `AutoNCP(units, output_size, sparsity_level=0.5, seed=22222)` | automatic 4-layer NCP | recommended sparse wiring |
| `NCP(inter, command, motor, sensory_fanout, inter_fanout, recurrent_command_synapses, motor_fanin, seed)` | manual 4-layer NCP | full control |

AutoNCP constraints: `output_size` must be `< units − 2` (good: ~0.3 × units).

## LTC / CfC extra options

```python
rnn = LTC(20, 28, input_mapping="affine", solver="euler", ode_unfolds=6)
rnn = CfC(20, 28, input_mapping="linear", solver="euler")
```

- `solver`: `"euler"` (default), `"midpoint"`, `"rk4"` — accuracy vs speed.
- `input_mapping`: `"linear"` or `"affine"` — how inputs are encoded.

## Minimal training loop

```python
import torch
from torch import nn
from ncps.torch import CfC
from ncps.wirings import AutoNCP

wiring = AutoNCP(28, 4)
model = CfC(20, wiring, return_sequences=True)
opt = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.MSELoss()

# xb: (B, T, 20), yb: (B, 4)
for step in range(1000):
    h0 = torch.zeros(xb.size(0), 28)
    pred, _ = model(xb, h0)          # (B, T, 4)
    loss = loss_fn(pred[:, -1, :], yb)
    opt.zero_grad(); loss.backward(); opt.step()
```

## Inspecting a wiring

```python
wiring = AutoNCP(28, 4)
print(wiring.num_layers)              # 4
print(wiring.synapse_count)           # internal synapses
print(wiring.sensory_synapse_count)   # input → internal synapses
wiring.draw_graph(draw_labels=True)   # matplotlib figure (returns legend handles)
```

## Common mistakes

- Feeding non-sequential data: LNNs are recurrent and need `(B, T, F)`.
- Wrong `h0` size (state size ≠ input size).
- Using `output[:, -1, :]` on a model with `return_sequences=False`.
- `output_size` too close to `units` for AutoNCP (invalid / degenerate wiring).
- Forgetting to normalize time-series inputs (loss explodes / NaN).
