#!/bin/bash
# ml-notebook-finder.sh v2.0.0
# Machine learning skill: explain algorithms, get notebooks, generate code
# Based on trekhleb/homemade-machine-learning (MIT License)

set -euo pipefail

CMD="${1:-list}"
QUERY="${2:-}"
NBBASE="https://nbviewer.jupyter.org/github/trekhleb/homemade-machine-learning/blob/master/notebooks"
GHBASE="https://github.com/trekhleb/homemade-machine-learning/blob/master/homemade"

# ── Resolve algorithm key ──────────────────────────────────────
resolve() {
    local q
    q=$(echo "$1" | tr '[:upper:]' '[:lower:]')
    if echo "$q" | grep -qE "linear|regress|univar|multivari|predict"; then
        echo "linear_regression"
    elif echo "$q" | grep -qE "logistic|sigmoid|classif|mnist|iris|spam|binary"; then
        echo "logistic_regression"
    elif echo "$q" | grep -qE "neural|mlp|perceptron|deep|backprop|network"; then
        echo "neural_network"
    elif echo "$q" | grep -qE "kmean|k-mean|cluster|segment|unsupervis"; then
        echo "k_means"
    elif echo "$q" | grep -qE "anomal|outlier|gaussian|fraud|detect"; then
        echo "anomaly_detection"
    else
        echo ""
    fi
}

# ── Explain command ────────────────────────────────────────────
do_explain() {
    local key="$1"
    case "$key" in

    linear_regression)
cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 LINEAR REGRESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IT DOES:
  Predicts a continuous numeric value by fitting a line (or plane)
  through training data. Minimizes the sum of squared errors.

WHEN TO USE:
  • Stock/house price prediction
  • Sales forecasting
  • Any "predict a number" task

MATH (core):
  hypothesis:  h(x) = θ₀ + θ₁x₁ + θ₂x₂ + ...
  cost:        J(θ) = (1/2m) Σ(h(xᵢ) - yᵢ)²
  update:      θⱼ := θⱼ - α · ∂J/∂θⱼ
  (gradient descent — α is learning rate)

PYTHON SNIPPET:
  import numpy as np

  class LinearRegression:
      def __init__(self, lr=0.01, epochs=1000):
          self.lr = lr
          self.epochs = epochs

      def fit(self, X, y):
          m, n = X.shape
          self.theta = np.zeros(n + 1)
          X_b = np.c_[np.ones(m), X]  # add bias column
          for _ in range(self.epochs):
              pred = X_b @ self.theta
              grad = X_b.T @ (pred - y) / m
              self.theta -= self.lr * grad

      def predict(self, X):
          X_b = np.c_[np.ones(len(X)), X]
          return X_b @ self.theta

INTERACTIVE NOTEBOOKS:
  ▶ Univariate (predict happiness by GDP):
    $NBBASE/linear_regression/univariate_linear_regression_demo.ipynb

  ▶ Multivariate (multiple features):
    $NBBASE/linear_regression/multivariate_linear_regression_demo.ipynb

  ▶ Non-linear (polynomial features):
    $NBBASE/linear_regression/non_linear_regression_demo.ipynb

SOURCE CODE: $GHBASE/linear_regression/linear_regression.py
EOF
        ;;

    logistic_regression)
cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 LOGISTIC REGRESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IT DOES:
  Classifies input into discrete categories. Uses sigmoid function
  to output a probability (0–1), then applies a threshold.

WHEN TO USE:
  • Spam detection (spam / not spam)
  • Medical diagnosis (positive / negative)
  • Handwritten digit recognition (MNIST)

MATH (core):
  sigmoid:    σ(z) = 1 / (1 + e⁻ᶻ)
  hypothesis: h(x) = σ(θᵀx)
  cost:       J = -(1/m) Σ [y·log(h) + (1-y)·log(1-h)]
  update:     θⱼ := θⱼ - α · (1/m) Σ(h(xᵢ)-yᵢ)·xᵢⱼ

PYTHON SNIPPET:
  import numpy as np

  class LogisticRegression:
      def __init__(self, lr=0.1, epochs=1000):
          self.lr = lr
          self.epochs = epochs

      def sigmoid(self, z):
          return 1 / (1 + np.exp(-z))

      def fit(self, X, y):
          m, n = X.shape
          self.theta = np.zeros(n + 1)
          X_b = np.c_[np.ones(m), X]
          for _ in range(self.epochs):
              h = self.sigmoid(X_b @ self.theta)
              grad = X_b.T @ (h - y) / m
              self.theta -= self.lr * grad

      def predict(self, X, threshold=0.5):
          X_b = np.c_[np.ones(len(X)), X]
          return (self.sigmoid(X_b @ self.theta) >= threshold).astype(int)

INTERACTIVE NOTEBOOKS:
  ▶ Linear boundary (Iris flower classification):
    $NBBASE/logistic_regression/logistic_regression_with_linear_boundary_demo.ipynb

  ▶ Non-linear boundary (microchip validity):
    $NBBASE/logistic_regression/logistic_regression_with_non_linear_boundary_demo.ipynb

  ▶ MNIST handwritten digits (28x28 pixels):
    $NBBASE/logistic_regression/multivariate_logistic_regression_demo.ipynb

  ▶ Fashion MNIST (clothes recognition):
    $NBBASE/logistic_regression/multivariate_logistic_regression_fashion_demo.ipynb

SOURCE CODE: $GHBASE/logistic_regression/logistic_regression.py
EOF
        ;;

    neural_network)
cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 NEURAL NETWORK (Multilayer Perceptron)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IT DOES:
  Stacks layers of neurons to learn complex non-linear patterns.
  Each neuron computes a weighted sum + activation function.
  Trains via backpropagation (chain rule of calculus).

WHEN TO USE:
  • Image/voice recognition
  • Complex classification where linear models fail
  • Foundation for CNN, RNN, Transformers

MATH (core):
  forward pass:   a[l] = σ(W[l] · a[l-1] + b[l])
  loss (cross-entropy): L = -Σ y·log(ŷ)
  backprop:       δ[l] = (W[l+1]ᵀ · δ[l+1]) ⊙ σ'(z[l])
  weight update:  W[l] -= α · δ[l] · a[l-1]ᵀ

PYTHON SNIPPET:
  import numpy as np

  def sigmoid(z): return 1 / (1 + np.exp(-z))
  def sigmoid_prime(z): s = sigmoid(z); return s * (1 - s)

  class MLP:
      def __init__(self, layers):  # e.g. [784, 128, 10]
          self.W = [np.random.randn(layers[i+1], layers[i]) * 0.01
                    for i in range(len(layers)-1)]
          self.b = [np.zeros((n, 1)) for n in layers[1:]]

      def forward(self, x):
          a = x
          self.activations = [a]
          for W, b in zip(self.W, self.b):
              z = W @ a + b
              a = sigmoid(z)
              self.activations.append(a)
          return a

      def predict(self, x):
          return np.argmax(self.forward(x))

INTERACTIVE NOTEBOOKS:
  ▶ MNIST handwritten digits (28x28):
    $NBBASE/neural_network/multilayer_perceptron_demo.ipynb

  ▶ Fashion MNIST (clothes type recognition):
    $NBBASE/neural_network/multilayer_perceptron_fashion_demo.ipynb

SOURCE CODE: $GHBASE/neural_network/multilayer_perceptron.py
EOF
        ;;

    k_means)
cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 K-MEANS CLUSTERING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IT DOES:
  Unsupervised algorithm that groups data into K clusters.
  Iteratively assigns points to nearest centroid, then
  recomputes centroids until convergence.

WHEN TO USE:
  • Customer segmentation
  • Image compression (reduce colors)
  • Document clustering
  • Any task where you need to group unlabeled data

MATH (core):
  assign:    cᵢ = argmin_k ||xᵢ - μₖ||²
  update:    μₖ = (1/|Cₖ|) Σᵢ∈Cₖ xᵢ
  (repeat until centroids stop moving)

PYTHON SNIPPET:
  import numpy as np

  class KMeans:
      def __init__(self, k=3, epochs=100):
          self.k = k
          self.epochs = epochs

      def fit(self, X):
          # Random init
          idx = np.random.choice(len(X), self.k, replace=False)
          self.centroids = X[idx]
          for _ in range(self.epochs):
              # Assign
              dists = np.linalg.norm(X[:, None] - self.centroids, axis=2)
              labels = np.argmin(dists, axis=1)
              # Update
              new_c = np.array([X[labels==k].mean(0) for k in range(self.k)])
              if np.allclose(self.centroids, new_c): break
              self.centroids = new_c
          return labels

INTERACTIVE NOTEBOOK:
  ▶ Cluster Iris flowers by petal dimensions:
    $NBBASE/k_means/k_means_demo.ipynb

SOURCE CODE: $GHBASE/k_means/k_means.py
EOF
        ;;

    anomaly_detection)
cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 ANOMALY DETECTION (Gaussian)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IT DOES:
  Models normal data as a multivariate Gaussian distribution.
  Points with very low probability density are flagged as anomalies.
  No labels needed — purely unsupervised.

WHEN TO USE:
  • Fraud detection (unusual transactions)
  • Server health monitoring (CPU/latency spikes)
  • Manufacturing defect detection
  • Network intrusion detection

MATH (core):
  fit:      μⱼ = (1/m) Σ xᵢⱼ
            σⱼ² = (1/m) Σ (xᵢⱼ - μⱼ)²
  density:  p(x) = Π p(xⱼ; μⱼ, σⱼ²)
  flag:     if p(x) < ε → anomaly

PYTHON SNIPPET:
  import numpy as np

  class GaussianAnomalyDetector:
      def fit(self, X):
          self.mu = X.mean(axis=0)
          self.sigma2 = X.var(axis=0)

      def probability(self, X):
          coef = 1 / np.sqrt(2 * np.pi * self.sigma2)
          exponent = np.exp(-((X - self.mu)**2) / (2 * self.sigma2))
          return np.prod(coef * exponent, axis=1)

      def predict(self, X, epsilon=1e-5):
          return self.probability(X) < epsilon  # True = anomaly

INTERACTIVE NOTEBOOK:
  ▶ Detect server anomalies by latency + throughput:
    $NBBASE/anomaly_detection/anomaly_detection_gaussian_demo.ipynb

SOURCE CODE: $GHBASE/anomaly_detection/gaussian_anomaly_detection.py
EOF
        ;;
    esac
}

# ── Notebook command ────────────────────────────────────────────
do_notebook() {
    local key="$1"
    echo "📓 Jupyter Notebooks for: ${key//_/ }"
    echo ""
    case "$key" in
    linear_regression)
        echo "▶ Univariate Linear Regression"
        echo "  $NBBASE/linear_regression/univariate_linear_regression_demo.ipynb"
        echo ""
        echo "▶ Multivariate Linear Regression"
        echo "  $NBBASE/linear_regression/multivariate_linear_regression_demo.ipynb"
        echo ""
        echo "▶ Non-linear Regression (polynomial)"
        echo "  $NBBASE/linear_regression/non_linear_regression_demo.ipynb"
        ;;
    logistic_regression)
        echo "▶ Logistic Regression — Linear Boundary (Iris)"
        echo "  $NBBASE/logistic_regression/logistic_regression_with_linear_boundary_demo.ipynb"
        echo ""
        echo "▶ Logistic Regression — Non-Linear Boundary"
        echo "  $NBBASE/logistic_regression/logistic_regression_with_non_linear_boundary_demo.ipynb"
        echo ""
        echo "▶ Multivariate — MNIST Digits"
        echo "  $NBBASE/logistic_regression/multivariate_logistic_regression_demo.ipynb"
        echo ""
        echo "▶ Multivariate — Fashion MNIST"
        echo "  $NBBASE/logistic_regression/multivariate_logistic_regression_fashion_demo.ipynb"
        ;;
    neural_network)
        echo "▶ MLP — MNIST Handwritten Digits"
        echo "  $NBBASE/neural_network/multilayer_perceptron_demo.ipynb"
        echo ""
        echo "▶ MLP — Fashion MNIST Clothes"
        echo "  $NBBASE/neural_network/multilayer_perceptron_fashion_demo.ipynb"
        ;;
    k_means)
        echo "▶ K-Means Clustering — Iris Flowers"
        echo "  $NBBASE/k_means/k_means_demo.ipynb"
        ;;
    anomaly_detection)
        echo "▶ Anomaly Detection — Server Monitoring"
        echo "  $NBBASE/anomaly_detection/anomaly_detection_gaussian_demo.ipynb"
        ;;
    esac
    echo ""
    echo "💡 Open any link in browser for interactive demo"
    echo "📜 Source: github.com/trekhleb/homemade-machine-learning (MIT)"
}

# ── Code command ────────────────────────────────────────────────
do_code() {
    local key="$1"
    do_explain "$key" | grep -A 999 "PYTHON SNIPPET:" | grep -B 999 "INTERACTIVE NOTEBOOKS:" | grep -v "INTERACTIVE NOTEBOOKS:"
}

# ── Learning path ───────────────────────────────────────────────
do_path() {
    local level="${1:-beginner}"
    echo "🎓 ML Learning Path: $level"
    echo "============================================"
    case "$level" in
    beginner)
        echo ""
        echo "Step 1 — Linear Regression (predict numbers)"
        echo "  → Understand gradient descent and cost functions"
        echo "  → bash scripts/ml-notebook-finder.sh explain 'linear regression'"
        echo ""
        echo "Step 2 — Logistic Regression (classify things)"
        echo "  → Learn sigmoid, cross-entropy loss, decision boundaries"
        echo "  → bash scripts/ml-notebook-finder.sh explain 'logistic regression'"
        echo ""
        echo "Step 3 — K-Means (group without labels)"
        echo "  → Your first unsupervised algorithm"
        echo "  → bash scripts/ml-notebook-finder.sh explain 'kmeans'"
        echo ""
        echo "Prerequisites: Python basics, NumPy arrays, high school math"
        ;;
    intermediate)
        echo ""
        echo "Step 1 — Neural Network (MLP)"
        echo "  → Backpropagation, activation functions, weight init"
        echo "  → bash scripts/ml-notebook-finder.sh explain 'neural network'"
        echo ""
        echo "Step 2 — Anomaly Detection"
        echo "  → Gaussian distributions, probability density"
        echo "  → bash scripts/ml-notebook-finder.sh explain 'anomaly detection'"
        echo ""
        echo "Prerequisites: linear regression + logistic regression"
        ;;
    advanced)
        echo ""
        echo "All 5 algorithms → implement from scratch:"
        echo "  1. linear_regression → 2. logistic_regression"
        echo "  3. neural_network → 4. k_means → 5. anomaly_detection"
        echo ""
        echo "Full source: github.com/trekhleb/homemade-machine-learning"
        echo "Run all notebooks via Binder (no install):"
        echo "  https://mybinder.org/v2/gh/trekhleb/homemade-machine-learning/master?filepath=notebooks"
        ;;
    *)
        echo "Levels: beginner, intermediate, advanced"
        ;;
    esac
    echo ""
    echo "📜 MIT License | bytesagain.com/skill/ml-notebook-finder"
}

# ── List ────────────────────────────────────────────────────────
do_list() {
    echo "🤖 ML Notebook Finder v2.0 — Skill by BytesAgain"
    echo "================================================="
    echo "5 algorithms · 11 interactive notebooks · Python from scratch"
    echo ""
    echo "SUPERVISED LEARNING"
    echo "  linear regression    3 notebooks  predict continuous values"
    echo "  logistic regression  4 notebooks  classification (MNIST, Iris)"
    echo "  neural network       2 notebooks  MLP, image recognition"
    echo ""
    echo "UNSUPERVISED LEARNING"
    echo "  kmeans               1 notebook   clustering, segmentation"
    echo "  anomaly detection    1 notebook   fraud detection, monitoring"
    echo ""
    echo "COMMANDS"
    echo "  explain   \"algorithm\"  — math + Python code + notebook links"
    echo "  notebook  \"algorithm\"  — all notebook links for algorithm"
    echo "  code      \"algorithm\"  — Python implementation snippet"
    echo "  path      [level]      — learning roadmap (beginner/intermediate/advanced)"
    echo "  list                   — this menu"
    echo ""
    echo "EXAMPLE"
    echo "  bash scripts/ml-notebook-finder.sh explain 'neural network'"
    echo ""
    echo "📜 Based on github.com/trekhleb/homemade-machine-learning (MIT)"
    echo "🌐 bytesagain.com/skill/ml-notebook-finder"
}

# ── Main ────────────────────────────────────────────────────────
case "$CMD" in
explain|notebook|code)
    if [ -z "$QUERY" ]; then
        echo "Usage: ml-notebook-finder.sh $CMD \"algorithm name\""
        echo "Algorithms: linear regression, logistic regression, neural network, kmeans, anomaly detection"
        exit 1
    fi
    KEY=$(resolve "$QUERY")
    if [ -z "$KEY" ]; then
        echo "❌ Algorithm not found: '$QUERY'"
        echo "Try: linear regression, logistic regression, neural network, kmeans, anomaly detection"
        exit 1
    fi
    case "$CMD" in
        explain)  do_explain "$KEY" ;;
        notebook) do_notebook "$KEY" ;;
        code)     do_code "$KEY" ;;
    esac
    ;;
path)
    do_path "$QUERY"
    ;;
list)
    do_list
    ;;
*)
    echo "Usage: ml-notebook-finder.sh [list|explain|notebook|code|path] [query]"
    ;;
esac
