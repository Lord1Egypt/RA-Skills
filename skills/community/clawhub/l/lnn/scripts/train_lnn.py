#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Train a Liquid Neural Network (LTC / CfC) with the ncps library.

Liquid Neural Networks are continuous-time recurrent networks whose neurons are
modeled by ordinary differential equations (ODEs):

  LTC  Liquid Time-Constant network — universal approximator, input-adaptive
       timing, but requires a numerical ODE solver (slower).
  CfC  Closed-form Continuous-time network — closed-form approximation of the
       LTC dynamics, 1-2 orders of magnitude faster.

Two kinds of wirings are supported:
  fc        fully connected (standard RNN wiring)
  autoncp   sparse structured Neural Circuit Policy wiring (recommended):
            sensory -> inter -> command -> motor layers (C. elegans inspired)
  random    random sparse wiring

Data can be generated synthetically (default) or loaded from a CSV file.
The model predicts the target variable(s) one step ahead given a history
window of --seq-len time steps.

Examples:
  # CfC, fully connected, synthetic data
  python train_lnn.py --model cfc --units 28 --output-size 1 --steps 1500

  # LTC with a sparse AutoNCP wiring, 28 neurons, 2 outputs
  python train_lnn.py --model ltc --wiring autoncp --wiring-units 28 --output-size 2 --steps 1500

  # Train on your own CSV time series and save the model
  python train_lnn.py --csv data.csv --features temperature,humidity --target power --steps 2000 --save model.pt

  # Evaluate on a validation split and print a rolling forecast
  python train_lnn.py --model cfc --wiring autoncp --wiring-units 24 --output-size 1 --steps 800 --eval --rollout 10
"""

import argparse
import os
import sys

import numpy as np


def build_parser():
    p = argparse.ArgumentParser(
        prog="train_lnn.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--model", choices=["cfc", "ltc"], default="cfc",
                   help="neuron model: 'cfc' (fast) or 'ltc' (ODE solver)")
    p.add_argument("--wiring", choices=["fc", "autoncp", "random"], default="fc",
                   help="wiring: 'fc', 'autoncp' (sparse NCP), or 'random'")
    p.add_argument("--units", type=int, default=28,
                   help="hidden units for fc/random wiring (default 28)")
    p.add_argument("--wiring-units", type=int, default=None,
                   help="total neurons for autoncp (defaults to --units)")
    p.add_argument("--output-size", type=int, default=1,
                   help="number of target variables (default 1)")
    p.add_argument("--input-size", type=int, default=3,
                   help="number of input features for synthetic data (default 3)")
    p.add_argument("--seq-len", type=int, default=32,
                   help="history window in time steps (default 32)")
    p.add_argument("--steps", type=int, default=1000,
                   help="number of training iterations (default 1000)")
    p.add_argument("--batch-size", type=int, default=64, help="batch size (default 64)")
    p.add_argument("--lr", type=float, default=0.01, help="learning rate (default 0.01)")
    p.add_argument("--sparsity", type=float, default=0.5,
                   help="sparsity for autoncp/random: 0.0 dense .. 0.9 sparse (default 0.5)")
    p.add_argument("--seed", type=int, default=0, help="random seed (default 0)")
    p.add_argument("--solver", choices=["euler", "midpoint", "rk4"], default=None,
                   help="ODE solver for LTC/CfC (default: library default)")
    p.add_argument("--input-mapping", choices=["linear", "affine"], default=None,
                   help="input encoding for LTC/CfC (default: library default)")
    p.add_argument("--csv", default=None, help="CSV file with time-series columns")
    p.add_argument("--features", default=None,
                   help="comma-separated CSV columns used as inputs (required with --csv)")
    p.add_argument("--target", default=None,
                   help="comma-separated CSV columns to predict (required with --csv)")
    p.add_argument("--eval", action="store_true",
                   help="compute validation MSE after training")
    p.add_argument("--rollout", type=int, default=5,
                   help="number of rolling-forecast steps to print (default 5)")
    p.add_argument("--save", default=None, help="save the trained model to a .pt file")
    p.add_argument("--no-cuda", action="store_true", help="force CPU even if CUDA is available")
    return p


BASE_SIGNALS = {
    0: lambda t: np.sin(t),
    1: lambda t: np.cos(t * 1.3),
    2: lambda t: np.tanh(np.sin(t) * 1.5),
    3: lambda t: np.sin(t * 0.5) * np.cos(t * 0.3),
    4: lambda t: np.sin(t * 2.0) ** 3,
}


def synthetic_data(n=4096, input_size=3, output_size=1, noise=0.05, seed=0):
    """Generate a smooth multi-variate time series for one-step-ahead prediction.

    The task: predict clean target signals from noisy input signals.
    """
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 60 * np.pi, n)
    ncols = max(input_size, output_size)
    clean = np.column_stack([BASE_SIGNALS[i % len(BASE_SIGNALS)](t) for i in range(ncols)])
    noisy = clean + rng.normal(0, noise, clean.shape)
    return noisy[:, :input_size], clean[:, :output_size]


def load_csv(path, features, target):
    """Load features and target columns from a CSV file as float64 arrays."""
    try:
        import pandas as pd
    except ImportError:
        sys.exit("pandas is required for --csv mode. Install it: pip install pandas")
    if not features or not target:
        sys.exit("--features and --target are required when using --csv")
    feat_cols = [c.strip() for c in features.split(",")]
    tgt_cols = [c.strip() for c in target.split(",")]
    df = pd.read_csv(path)
    for c in feat_cols + tgt_cols:
        if c not in df.columns:
            sys.exit(f"Column not found in CSV '{path}': {c}")
    X = df[feat_cols].to_numpy(dtype=np.float64)
    Y = df[tgt_cols].to_numpy(dtype=np.float64)
    if X.shape[0] != Y.shape[0]:
        sys.exit("Features and target must have the same number of rows")
    print(f"Loaded CSV: {len(df)} rows, {len(feat_cols)} feature(s), {len(tgt_cols)} target(s)")
    return X, Y


def zscore_fit(a):
    mean = a.mean(axis=0, keepdims=True)
    std = a.std(axis=0, keepdims=True) + 1e-8
    return mean, std


def zscore_apply(a, mean, std):
    return (a - mean) / std


def zscore_inverse(a, mean, std):
    return a * std + mean


def sliding_window(X, Y, seq_len):
    """Turn a time series into (window, next-step-target) training samples.

    Returns (xs, ys) where xs[i] = X[i : i+seq_len] and ys[i] = Y[i+seq_len].
    """
    n = len(X) - seq_len
    if n <= 0:
        sys.exit(f"Data too short for seq-len={seq_len}: need more than {seq_len} rows")
    xs = np.stack([X[i:i + seq_len] for i in range(n)])
    ys = Y[seq_len:]
    return xs, ys


def make_model(model_type, input_size, wiring, units, wiring_units, output_size,
               sparsity, seed, solver, input_mapping):
    """Build the ncps RNN. Returns (rnn, hidden_size, raw_out_dim)."""
    from ncps.torch import CfC, LTC
    rnn_cls = {"cfc": CfC, "ltc": LTC}[model_type]
    kwargs = {}
    if solver is not None:
        kwargs["solver"] = solver
    if input_mapping is not None:
        kwargs["input_mapping"] = input_mapping

    if wiring == "fc":
        rnn = rnn_cls(input_size, units, return_sequences=True, **kwargs)
        hidden, out_dim = units, units
    elif wiring == "random":
        from ncps.wirings import Random
        w = Random(units, output_dim=output_size, sparsity_level=sparsity,
                   random_seed=seed)
        rnn = rnn_cls(input_size, w, return_sequences=True, **kwargs)
        hidden, out_dim = units, output_size
    elif wiring == "autoncp":
        from ncps.wirings import AutoNCP
        wu = wiring_units if wiring_units else units
        w = AutoNCP(wu, output_size, sparsity_level=sparsity, seed=seed)
        rnn = rnn_cls(input_size, w, return_sequences=True, **kwargs)
        hidden, out_dim = wu, output_size
    else:
        sys.exit(f"Unknown wiring: {wiring}")
    return rnn, hidden, out_dim


def make_net(torch, rnn, out_dim, output_size):
    """Wrap the ncps RNN so its output dimension always matches output_size."""

    class Net(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.rnn = rnn
            self.head = (torch.nn.Linear(out_dim, output_size)
                         if out_dim != output_size else torch.nn.Identity())

        def forward(self, x, h0):
            out, hn = self.rnn(x, h0)
            return self.head(out[:, -1, :]), hn

    return Net()



def train(model, hidden_size, Xtr, Ytr, Xva, Yva, device, args, log_every=100):
    torch = __import__("torch")
    from torch import nn
    torch.manual_seed(args.seed)
    model = model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    loss_fn = nn.MSELoss()

    def run_batch(xb, yb, grad):
        xb = torch.from_numpy(xb).float().to(device)
        yb = torch.from_numpy(yb).float().to(device)
        h0 = torch.zeros(xb.size(0), hidden_size, device=device)
        pred, _ = model(xb, h0)
        loss = loss_fn(pred, yb)
        if grad:
            opt.zero_grad()
            loss.backward()
            opt.step()
        return loss.item()

    n = len(Xtr)
    last_val = float("nan")
    for step in range(args.steps):
        idx = np.random.default_rng(args.seed + step).permutation(n)[: args.batch_size]
        loss = run_batch(Xtr[idx], Ytr[idx], True)
        if step % log_every == 0 or step == args.steps - 1:
            last_val = run_batch(Xva[: args.batch_size], Yva[: args.batch_size], False)
            print(f"step {step:5d} | train loss {loss:.6f} | val loss {last_val:.6f}")
    return last_val


def eval_mse(model, hidden_size, Xva, Yva, device):
    torch = __import__("torch")
    from torch import nn
    model.eval()
    model = model.to(device)
    loss_fn = nn.MSELoss()
    with torch.no_grad():
        xb = torch.from_numpy(Xva).float().to(device)
        yb = torch.from_numpy(Yva).float().to(device)
        h0 = torch.zeros(xb.size(0), hidden_size, device=device)
        pred, _ = model(xb, h0)
        return loss_fn(pred, yb).item()


def forecast(model, hidden_size, X, Y, mean, std, seq_len, steps, device):
    """Teacher-forced rolling forecast demo using the last `steps` samples.

    X, Y are the *normalized* full-length time series in chronological order.
    """
    torch = __import__("torch")
    model.eval()
    n = len(X)
    if steps > n - seq_len:
        steps = max(n - seq_len, 1)
    print(f"\nRolling forecast (teacher-forced, last {steps} step(s)):")
    print(f"{'step':>4}  {'predicted':>12}  {'actual':>12}")
    with torch.no_grad():
        for i in range(steps):
            start = n - steps - seq_len + i
            xb = torch.from_numpy(X[start:start + seq_len][None]).float().to(device)
            h0 = torch.zeros(1, hidden_size, device=device)
            pred, _ = model(xb, h0)
            pred = pred.detach().cpu().numpy()[0]
            act = Y[start + seq_len]
            p_real = zscore_inverse(pred, mean, std)
            a_real = zscore_inverse(act, mean, std)
            cols = (p_real[0], a_real[0]) if p_real.size else (float("nan"), float("nan"))
            print(f"{i + 1:4d}  {cols[0]:12.4f}  {cols[1]:12.4f}")
    print()



def main(argv=None):
    args = build_parser().parse_args(argv)

    try:
        import torch
    except ImportError:
        sys.exit("PyTorch is not installed. Run: pip install -r scripts/requirements.txt")
    try:
        import ncps  # noqa: F401  (validates the dependency early)
    except ImportError:
        sys.exit("ncps is not installed. Run: pip install -r scripts/requirements.txt")

    device = torch.device("cuda" if (not args.no_cuda and torch.cuda.is_available()) else "cpu")
    print(f"Using device: {device} | model={args.model} wiring={args.wiring} "
          f"seq_len={args.seq_len} steps={args.steps}")

    # --- data ---------------------------------------------------------------
    if args.csv:
        X, Y = load_csv(args.csv, args.features, args.target)
    else:
        X, Y = synthetic_data(input_size=args.input_size,
                              output_size=args.output_size,
                              noise=0.05, seed=args.seed)
        print(f"Synthetic data: {len(X)} rows, {X.shape[1]} feature(s), "
              f"{Y.shape[1]} target(s)")

    split = int(len(X) * 0.8)
    Xtr, Xva = X[:split], X[split:]
    Ytr, Yva = Y[:split], Y[split:]

    x_mean, x_std = zscore_fit(Xtr)
    y_mean, y_std = zscore_fit(Ytr)
    Xtr_z, Ytr_z = zscore_apply(Xtr, x_mean, x_std), zscore_apply(Ytr, y_mean, y_std)
    Xva_z, Yva_z = zscore_apply(Xva, x_mean, x_std), zscore_apply(Yva, y_mean, y_std)

    Xtr_w, Ytr_w = sliding_window(Xtr_z, Ytr_z, args.seq_len)
    Xva_w, Yva_w = sliding_window(Xva_z, Yva_z, args.seq_len)
    print(f"Train windows: {len(Xtr_w)} | Val windows: {len(Xva_w)}")

    # --- model --------------------------------------------------------------
    rnn, hidden, out_dim = make_model(args.model, Xtr_w.shape[2], args.wiring,
                                      args.units, args.wiring_units,
                                      args.output_size, args.sparsity,
                                      args.seed, args.solver, args.input_mapping)
    model = make_net(torch, rnn, out_dim, args.output_size)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model: {args.model} + {args.wiring} | hidden={hidden} | "
          f"output_size={args.output_size} | parameters={n_params}")

    # --- train --------------------------------------------------------------
    val_loss = train(model, hidden, Xtr_w, Ytr_w, Xva_w, Yva_w, device, args)

    if args.eval:
        mse = eval_mse(model, hidden, Xva_w, Yva_w, device)
        print(f"\nValidation MSE: {mse:.6f} (last logged val loss was {val_loss:.6f})")

    forecast(model, hidden, Xva_z, Yva_z, y_mean, y_std, args.seq_len,
             args.rollout, device)

    if args.save:
        torch.save(model, args.save)
        print(f"Model saved to: {args.save}")


if __name__ == "__main__":
    main()

