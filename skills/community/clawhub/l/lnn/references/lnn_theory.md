# Liquid Neural Networks — Theory Reference

## 1. What is a Liquid Neural Network (LNN)?

A **liquid neural network** is a continuous-time recurrent neural network in
which each neuron's state evolves according to an **ordinary differential
equation (ODE)**. Instead of discrete time steps (LSTM/GRU), an LNN describes
a dynamical system:

    τ(x) · dx/dt = −x + f(x, input, θ)

The key property is the **liquid time-constant**: the rate at which a neuron
reacts to input is itself input-dependent, so the network's timing behavior
adapts to the signal. This gives LNNs several advantages over standard RNNs:

- **Causal, continuous-time dynamics** — outputs depend on the actual timing
  of inputs, not just their order.
- **Robustness** — small, sparse LNNs generalize well and are less prone to
  overfitting than large LSTMs on the same data.
- **Auditability** — the sparse structure can be inspected as a wiring diagram
  ("auditable autonomy").

## 2. Two neuron models in `ncps`

### LTC — Liquid Time-Constant network
Neurons are differential equations interconnected via sigmoidal synapses.
LTCs are **universal approximators** that implement causal dynamical models.
Because their outputs require a **numerical ODE solver**, training and
inference are slower than for standard RNNs.

### CfC — Closed-form Continuous-time network
CfC resolves the LTC bottleneck by **approximating the closed-form solution**
of the ODE. It is 1–2 orders of magnitude faster to train and infer while
keeping the liquid dynamics.

| | LTC | CfC |
|---|---|---|
| Math | ODE, numeric solver | Closed-form approximation |
| Speed | slower | fast |
| Use when | you need exact ODE behavior, small data | large data, production, most cases |

## 3. Neural Circuit Policies (NCP) wirings

NCPs are sparse recurrent networks **loosely inspired by the nervous system
of *C. elegans***. The wiring follows a 4-layer principle:

```
sensory → inter → command → motor
```

- **Sensory neurons** — receive the external input.
- **Inter neurons** — hidden processing layer.
- **Command neurons** — recurrent layer that integrates information.
- **Motor neurons** — produce the output.

`AutoNCP(units, output_size, sparsity_level, seed)` builds such a wiring
automatically: `units` = total neurons, `output_size` = motor neurons.
Good defaults: `output_size ≈ 0.3 × units`, `sparsity_level = 0.5`.

## 4. Papers

- Lechner, Hasani, Amini, Henzinger, Rus, Grosu. **Neural circuit policies
  enabling auditable autonomy**. *Nature Machine Intelligence*, 2020.
- Hasani et al. **Closed-form continuous-time neural networks**.
  *Nature Machine Intelligence*, 2022.
- Hasani et al. **Liquid Time-constant Networks**. *AAAI*, 2021.

## 5. When to use / not to use

**Use LNNs for:**
- time-series prediction with continuous/irregular timing
- control and autonomous-systems modeling (small models, robust behavior)
- few-shot / multi-task learning where compact models matter
- interpretable recurrent models (wiring is inspectable)

**Prefer something else for:**
- static (non-sequential) tabular or image tasks
- very long contexts (Transformers)
- tasks where a standard LSTM/GRU performs well and interpretability is not
  required
